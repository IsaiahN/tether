"""snaps: generated worlds, each carrying an answer key the agent never sees.

Heritage -- the retro-snaps corpus: 57,170 games reverse-classified against ARC to guess
the private set's families. It failed as a solver and was logged as "a diagnostic, not a
solver". This is that diagnostic doing the job it is actually good at. The families are a
COVERAGE MAP for generation, and a generated world is the only kind that arrives with a
key. The original catalogued real games; this generates synthetic ones. Same intent.

The key answers the question the ledger cannot ask itself:

    when the agent said it knew the mechanism, was it right about the MECHANISM,
    or only about the steps it happened to see?

A term that fits twelve observations and is wrong on the thirteenth is indistinguishable
from the truth in the record. Against a key it is not. Nothing here reaches the agent --
the key is read after the run, by the harness, exactly like world.unreachable_slots.
"""

from __future__ import annotations

import random
import sys
from collections.abc import Callable
from typing import Any

from gamma import Ctx, Term
from world import ACTIONS, DELTA, M, _atoms

sys.dont_write_bytecode = True

# families the delta table named as real and previously inexpressible. Two of the six are
# outside closure(atoms) by construction, so abstention has something honest to be right
# about; `delayed` is the vc33 gap -- cause and effect separated in time, 0 wins in 5000+
# generations of the previous build.
FAMILIES = ("identity", "affine", "quadratic", "action", "interact", "delayed")
OBJECTIVES = ("ALL", "ANY", "COUNT", "AVOID")


def _rule(rng: random.Random, others: list[str]) -> tuple[str, Callable, str | None]:
    """(family, fn(v, action, before, prev) -> int, the slot it reads or None)."""
    k = rng.randrange(1, M)
    a = rng.choice([2, 3, 4, 5, 6])
    o = rng.choice(others) if others else None
    fam = rng.choice(FAMILIES if o else FAMILIES[:4])
    # every family takes the same four arguments whether it reads them or not: one
    # uniform signature, no branching on family. ARG005 is the doctrine, not a defect.
    fns: dict[str, Callable] = {  # noqa: ARG005
        "identity": lambda v, ac, b, p: v,  # noqa: ARG005
        "affine": lambda v, ac, b, p: (a * v + k) % M,  # noqa: ARG005
        "quadratic": lambda v, ac, b, p: (v * v + k) % M,  # noqa: ARG005
        "action": lambda v, ac, b, p: (v + DELTA[ac] * k) % M,  # noqa: ARG005
        "interact": lambda v, ac, b, p: (b[o] + k) % M,  # noqa: ARG005
        "delayed": lambda v, ac, b, p: ((p or b)[o] + k) % M,  # noqa: ARG005
    }
    return fam, fns[fam], (o if fam in ("interact", "delayed") else None)


def _objective(rng: random.Random, names: list[str]) -> tuple[str, Callable]:
    kind = rng.choice(OBJECTIVES)
    tgt = rng.randrange(M)
    who = rng.choice(names)
    n = max(1, len(names) // 2)
    fns: dict[str, Callable] = {
        "ALL": lambda st: sum(1 for v in st.values() if v % M == tgt) / len(st),
        "ANY": lambda st: 1.0 if any(v % M == tgt for v in st.values()) else 0.0,
        "COUNT": lambda st: min(1.0, sum(1 for v in st.values() if v % M == tgt) / n),
        "AVOID": lambda st: 0.0 if st[who] % M == tgt else 1.0,
    }
    label = {"ALL": f"ALL(BECOME(slot, {tgt}))", "ANY": f"ANY(BECOME(slot, {tgt}))",
             "COUNT": f"COUNT(BECOME(slot, {tgt})) >= {n}",
             "AVOID": f"MAINTAIN({who} != {tgt})"}[kind]
    return label, fns[kind]


class Snap:
    """One generated world. Fills the same eight-member contract as Transitions."""

    def __init__(self, seed: int, n_slots: int = 5) -> None:
        rng = random.Random(seed)
        self.seed = seed
        names = [f"s{i}" for i in range(n_slots)]
        self.rules: dict[str, Callable] = {}
        self.meta: dict[str, dict] = {}
        for nm in names:
            fam, fn, dep = _rule(rng, [o for o in names if o != nm])
            self.rules[nm] = fn
            self.meta[nm] = {"family": fam, "reads": dep}
        self.state = {nm: rng.randrange(M) for nm in names}
        self.prev: dict[str, int] | None = None
        self.obj_label, self._obj = _objective(rng, names)

    # -- the eight -------------------------------------------------------------------

    def substrate(self) -> str:
        return f"named slots holding integers mod {M}"

    def environment(self) -> str:
        return f"generated per-slot rules (snap {self.seed}); the medium is arithmetic mod {M}"

    def actors(self) -> str:
        return f"the actions {ACTIONS}"

    def currency(self) -> str:
        return "prediction error in bits, per slot"

    def ground(self) -> str:
        return "exact match on the next state"

    def slots(self) -> list[str]:
        return sorted(self.state)

    def atoms(self) -> list:
        return _atoms()

    def transform(self) -> Any:
        return None

    # -- running ---------------------------------------------------------------------

    def objective(self) -> tuple[str, float]:
        return self.obj_label, self._obj(self.state)

    def observe(self) -> dict[str, int]:
        return dict(self.state)

    def step(self, action: str) -> None:
        if action not in ACTIONS:
            raise ValueError(f"unknown action: {action}")
        before, prev = dict(self.state), self.prev
        self.state = {k: self.rules[k](v, action, before, prev) % M
                      for k, v in before.items()}
        self.prev = before


# -- the key. Read by the harness, never by the agent ---------------------------------


def _same(term: Term, rule: Callable, slot: str, dep: str | None,
          bind: str | None, names: list[str]) -> bool:
    """Extensional equality over the WHOLE finite domain, not the observed slice.

    This is the only thing that separates a correct mint from a lucky one, and it is
    exactly what the agent cannot do -- it has history, the harness has the function.
    """
    varies = sorted({s for s in (dep, bind) if s})
    grid = ([()] if not varies else
            [(w,) for w in range(M)] if len(varies) == 1 else
            [(w1, w2) for w1 in range(M) for w2 in range(M)])
    for v in range(M):
        for ac in ACTIONS:
            for combo in grid:
                st = dict.fromkeys(names, 0)
                st[slot] = v
                for s2, w in zip(varies, combo, strict=False):
                    st[s2] = w
                ops = (st[bind],) if bind else ()
                try:
                    got = term.apply(v, Ctx(action=ac, operands=ops)) % M
                except (KeyError, TypeError):
                    return False
                # a term has no accessor for prev, so a rule that reads it is unmatchable.
                # Two DISTINCT prev states expose that; one fixed offset does not, because
                # a constant shift is just an interaction with a different constant.
                for shift in (1, 4):
                    pst = {s2: (w2 + shift) % M for s2, w2 in st.items()}
                    try:
                        want = rule(v, ac, st, pst) % M
                    except (KeyError, TypeError):
                        return False
                    if got != want:
                        return False
    return True


def key(snap: Snap, gam, max_depth: int = 3, budget: int = 4000) -> dict:
    """Per slot: the family, the shortest atom-composition equal to it, whether one
    exists at all. Computed over atoms only -- the key describes the CLOSURE, not
    whatever the agent's library happens to hold at the time."""
    names = snap.slots()
    out = {}
    for slot in names:
        rule, dep = snap.rules[slot], snap.meta[slot]["reads"]
        minimal = None
        for cand in gam.enumerate_closure("val", "val", max_depth, budget):
            for b in [None] + [s for s in names if s != slot]:
                t = Term(cand.atoms, operand=b)
                if _same(t, rule, slot, dep, b, names):
                    minimal = t
                    break
            if minimal:
                break
        out[slot] = {"family": snap.meta[slot]["family"], "reads": dep,
                     "minimal": minimal.name if minimal else None,
                     "minimal_len": len(minimal) if minimal else None,
                     "in_closure": minimal is not None}
    return {"seed": snap.seed, "objective": snap.obj_label, "slots": out}


def grade(agent, snap: Snap, k: dict) -> dict:
    """Four numbers the ledger cannot produce alone.

    A false mint is the alignment failure in its purest form: the agent stated a
    mechanism, the record is clean, the guards all fired, and it is wrong. Nothing
    inside the frame can catch it, which is precisely why the grader is outside.
    """
    names = snap.slots()
    true_mint = false_mint = true_abst = false_abst = 0
    gaps, mixture, wrong = [], [], []
    for slot in names:
        fact = k["slots"][slot]
        name = agent.bound.get(slot)
        held = slot in agent.owed_import
        if name and not held:
            term = agent.gamma.library[name]
            ok = _same(term, snap.rules[slot], slot, fact["reads"], term.operand, names)
            if ok:
                true_mint += 1
                if fact["minimal_len"]:
                    gaps.append(len(term) - fact["minimal_len"])
            else:
                false_mint += 1
                wrong.append({"slot": slot, "claimed": name,
                              "family": fact["family"], "truth": fact["minimal"]})
            mixture.append({"slot": slot, "depth": len(term),
                            "operand": term.operand is not None,
                            "family": fact["family"]})
        elif held:
            if fact["in_closure"]:
                false_abst += 1
            else:
                true_abst += 1
    claimed = true_mint + false_mint
    abst = true_abst + false_abst
    # every slot lands in exactly one bucket or the rates are computed over a denominator
    # that quietly shrank. A slot the loop never reached is not an abstention.
    unresolved = len(names) - claimed - abst
    return {"seed": snap.seed, "slots": len(names), "unresolved": unresolved,
            "claimed": claimed, "false_mint": false_mint,
            "false_mint_rate": round(false_mint / claimed, 4) if claimed else None,
            "abstained": abst, "false_abstention": false_abst,
            "abstention_accuracy": round(true_abst / abst, 4) if abst else None,
            "minimality_gap": round(sum(gaps) / len(gaps), 3) if gaps else None,
            "mixture": mixture, "wrong": wrong}
