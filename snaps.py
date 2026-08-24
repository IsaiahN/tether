"""snaps: generated worlds with an answer key, and a DS-controlled level ladder.

Heritage -- the retro-snaps corpus: 57,170 games reverse-classified against ARC to guess
the private set. It failed as a solver and was logged as "a diagnostic, not a solver".
This is that diagnostic in the role it is good at. Three things came across, all of them
descriptions of WORLDS and never of solvers:

  families   F1-F15 as rule shapes to generate, not experts to build
  weights    the private-set composition estimate, as a sampling prior
  DS         deviation strength -- the level ladder, and the only reason transfer is
             measurable at all

A level sequence measures transfer only if the relationship between consecutive levels is
known: unrelated levels make the metric read zero meaninglessly, identical levels make it
read one meaninglessly. DS makes it a curve instead of a verdict.

The key answers what the ledger cannot ask itself: when the agent said it knew the
mechanism, was it right about the MECHANISM, or only about the steps it happened to see?
Read after the run, never by the agent.
"""

from __future__ import annotations

import random
import sys
from collections.abc import Callable
from copy import deepcopy
from dataclasses import dataclass, field, replace
from typing import Any

from gamma import Atom, Ctx, Gamma, Term

# This module's OWN domain facts. Importing world's was a boundary crossing between two
# domains, and it also meant the generated worlds inherited the vocabulary designed for
# the hand-built toy -- so `in_closure`, the denominator under every abstention number
# here, was defined against a choice made for a different world. Declared locally the
# values are the same and the dependency is not.
M = 7          # anchor: prime, and small enough that the key can sweep the whole domain
ACTIONS = ("A", "B", "C")
DELTA = {"A": 1, "B": 2, "C": 4}


def _atoms() -> list[Atom]:
    """The generator's own primitives. Same set as the toy world's today; the point is
    that changing one no longer silently changes the other."""
    def idn(v, _c):
        return v

    def inc(v, _c):
        return v + 1

    def dec(v, _c):
        return v - 1

    def dbl(v, _c):
        return v * 2

    def neg(v, _c):
        return -v

    def act(v, c):
        return v + DELTA.get(c.action, 0)

    def wrap(v, _c):
        return v % M

    out = [Atom(f.__name__, f, "val", "val") for f in (idn, inc, dec, dbl, neg, act, wrap)]

    def take(v, c):
        """Reads the bound operand slot instead of this one. The one atom that makes an
        interaction expressible at all."""
        return c.operands[0] if c.operands else v

    out.append(Atom("take", take, "val", "val", reads_operand=True))
    return out

sys.dont_write_bytecode = True

# families that need another slot, and families provably outside closure(atoms)
RELATIONAL = ("interact", "delayed", "chain", "lagged", "constraint")
FAMILIES = ("identity", "affine", "quadratic", "action", *RELATIONAL, "hidden", "regime")

# sampling prior from EXPERT_AUDIT_DEEP 4A's private-set estimate. Whether that estimate
# is right is unknowable; as a coverage prior over generated worlds it beats uniform.
WEIGHTS = {"identity": 3, "affine": 8, "quadratic": 6, "action": 8, "interact": 10,
           "delayed": 6, "chain": 12, "lagged": 8, "constraint": 14, "hidden": 8,
           "regime": 10}

OBJECTIVES = ("ALL", "ANY", "COUNT", "AVOID")
LATE = 999   # anchor: greater than any switch the generator emits (max 16), so the
#              key probes a tick strictly past every regime change


@dataclass
class SlotSpec:
    """The generative description of one slot. DS edits operate on this, never on the
    executable rule, so a deviation is a stated edit rather than a fudge factor."""

    family: str
    k: int = 1
    a: int = 2
    reads: str | None = None
    lag: int = 2
    switch: int = 12
    k2: int = 3


@dataclass
class WorldSpec:
    slots: list[str]
    rules: dict[str, SlotSpec]
    obj: str = "ALL"
    tgt: int = 0
    who: str = "s0"
    n: int = 2
    # the objective must be HELD, not merely touched. A state hit by chance is not a win:
    # holding it requires predicting what the next action does, so 3 is the smallest hold
    # that cannot be satisfied by one-step luck. Anchored, not tuned.
    hold: int = 3
    start: dict[str, int] = field(default_factory=dict)


def _pick(rng: random.Random, pool) -> str:
    pool = list(pool)
    return rng.choices(pool, weights=[WEIGHTS[f] for f in pool])[0]


def spec_for(seed: int, n_slots: int = 5) -> WorldSpec:
    rng = random.Random(seed)
    names = [f"s{i}" for i in range(n_slots)]
    rules = {}
    for nm in names:
        others = [o for o in names if o != nm]
        pool = FAMILIES if others else [f for f in FAMILIES if f not in RELATIONAL]
        fam = _pick(rng, pool)
        rules[nm] = SlotSpec(family=fam, k=rng.randrange(1, M),
                             a=rng.choice([2, 3, 4, 5, 6]),
                             reads=rng.choice(others) if others and fam in RELATIONAL
                             else None,
                             lag=rng.choice([2, 3]), switch=rng.choice([8, 12, 16]),
                             k2=rng.randrange(1, M))
    return _acyclic(WorldSpec(slots=names, rules=rules, obj=rng.choice(OBJECTIVES),
                              tgt=rng.randrange(M), who=rng.choice(names),
                              n=max(1, n_slots // 2),
                              start={nm: rng.randrange(M) for nm in names}), rng)


def _acyclic(spec: WorldSpec, rng: random.Random) -> WorldSpec:
    """A `chain` slot reads its target's NEW value, so chain-to-chain would be a cycle
    inside one tick. Repair at the SPEC, not with a guard at evaluation -- a world that
    cannot be evaluated is a malformed world, not a runtime case to handle."""
    for nm, r in spec.rules.items():
        if r.family != "chain":
            continue
        free = [o for o in spec.slots if o != nm and spec.rules[o].family != "chain"]
        if not free:
            spec.rules[nm] = replace(r, family="interact")
        elif r.reads not in free:
            spec.rules[nm] = replace(r, reads=rng.choice(free))
    return spec


def deviate(spec: WorldSpec, ds: float, rng: random.Random) -> WorldSpec:
    """Level n+1 at a stated deviation from level n. The DS table, as concrete edits.

    0.0 identical rules, new start     0.6 objective family changes
    0.2 constants change                0.8 half the rules change, and the objective
    0.4 one new family introduced       1.0 nothing shared

    DS 0.0 must leave the RULES untouched. A rung that re-rolls constants has already
    changed the function, so nothing can transfer even at the bottom and the curve has
    no top anchor to fall away from -- which is a ladder that cannot measure anything.
    """
    if ds >= 1.0:
        return spec_for(rng.randrange(10 ** 6), len(spec.slots))
    s = deepcopy(spec)
    s.start = {n: rng.randrange(M) for n in s.slots}       # DS 0.0: a reskin
    if ds >= 0.2:
        for nm in s.slots:
            s.rules[nm] = replace(s.rules[nm], k=rng.randrange(1, M),
                                  a=rng.choice([2, 3, 4, 5, 6]))
    if ds >= 0.4:
        nm = rng.choice(s.slots)
        others = [o for o in s.slots if o != nm]
        fam = _pick(rng, FAMILIES)
        s.rules[nm] = replace(s.rules[nm], family=fam,
                              reads=rng.choice(others) if fam in RELATIONAL else None)
    if ds >= 0.6:
        s.obj = rng.choice([o for o in OBJECTIVES if o != s.obj])
        s.tgt, s.who = rng.randrange(M), rng.choice(s.slots)
    if ds >= 0.8:
        for nm in rng.sample(s.slots, max(1, len(s.slots) // 2)):
            others = [o for o in s.slots if o != nm]
            fam = _pick(rng, FAMILIES)
            s.rules[nm] = replace(s.rules[nm], family=fam,
                                  reads=rng.choice(others) if fam in RELATIONAL else None)
    return _acyclic(s, rng)


# -- the executable world --------------------------------------------------------------


def _rule_fn(sp: SlotSpec, spec: WorldSpec) -> Callable:
    """One uniform signature for every family whether it reads the argument or not:
    (v, action, before, prev, tick). No branching on family at the call site."""

    def fn(v, ac, before, prev, tick=0):
        f = sp.family
        if f == "identity":
            return v
        if f == "affine":
            return sp.a * v + sp.k
        if f == "quadratic":
            return v * v + sp.k
        if f == "action":
            return v + DELTA[ac] * sp.k
        if f == "interact":
            return before[sp.reads] + sp.k
        if f == "delayed":
            return prev[sp.reads] + sp.k
        if f == "chain":
            # within-step cascade: reads the target's NEW value, not its old one
            t = spec.rules[sp.reads]
            return _rule_fn(t, spec)(before[sp.reads], ac, before, prev, tick) + sp.k
        if f == "lagged":
            return prev[sp.reads] + sp.k          # prev stands for the lag-k state
        if f == "constraint":
            return v + 1 if v % M == before[sp.reads] % M else v
        if f == "hidden":
            return tick * 3 + sp.k                # driver is not in the state at all
        if f == "regime":
            return v + (sp.k if tick < sp.switch else sp.k2)
        raise ValueError(f)

    return fn


class Snap:
    """One generated world. Fills the same eight-member contract as Transitions."""

    def __init__(self, spec: WorldSpec) -> None:
        self.spec = spec
        self.state = dict(spec.start)
        self.past: list[dict[str, int]] = []
        self.tick = 0
        self.held = 0
        self.dead = False
        self.rules = {nm: _rule_fn(sp, spec) for nm, sp in spec.rules.items()}

    # -- the eight -------------------------------------------------------------------

    def substrate(self) -> str:
        return f"named slots holding integers mod {M}"

    def environment(self) -> str:
        fams = sorted({s.family for s in self.spec.rules.values()})
        return f"generated rules over {', '.join(fams)}; the medium is arithmetic mod {M}"

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

    def actions(self) -> tuple[str, ...]:
        return ACTIONS

    def alphabet(self) -> int:
        return M

    # -- running ---------------------------------------------------------------------

    def objective(self) -> tuple[str, float]:
        sp, st = self.spec, self.state
        if sp.obj == "ALL":
            hit = sum(1 for v in st.values() if v % M == sp.tgt)
            return f"ALL(BECOME(slot, {sp.tgt}))", hit / len(st)
        if sp.obj == "ANY":
            return (f"ANY(BECOME(slot, {sp.tgt}))",
                    float(any(v % M == sp.tgt for v in st.values())))
        if sp.obj == "COUNT":
            hit = sum(1 for v in st.values() if v % M == sp.tgt)
            return f"COUNT(BECOME(slot, {sp.tgt})) >= {sp.n}", min(1.0, hit / sp.n)
        return f"MAINTAIN({sp.who} != {sp.tgt})", 0.0 if self.dead else 1.0

    def terminal(self) -> str | None:
        """advance, death, or None. AVOID can never advance -- surviving the budget is
        the win, so exhaustion is scored as the advance for that family."""
        if self.dead:
            return "death"
        if self.spec.obj != "AVOID" and self.held >= self.spec.hold:
            return "advance"
        return None

    def observe(self) -> dict[str, int]:
        return dict(self.state)

    def step(self, action: str) -> None:
        if action not in ACTIONS:
            raise ValueError(f"unknown action: {action}")
        before = dict(self.state)
        sp = self.spec
        prev = self.past[-1] if self.past else before
        nxt = {}
        for nm, r in sp.rules.items():
            p = prev
            if r.family == "lagged":
                p = self.past[-r.lag] if len(self.past) >= r.lag else before
            nxt[nm] = self.rules[nm](before[nm], action, before, p, self.tick) % M
        self.past.append(before)
        self.state, self.tick = nxt, self.tick + 1
        self.held = self.held + 1 if self.objective()[1] >= 1.0 else 0
        if sp.obj == "AVOID" and self.state[sp.who] % M == sp.tgt:
            self.dead = True


# -- the key. Read by the harness, never by the agent ---------------------------------


def _same(term: Term, rule: Callable, slot: str, dep: str | None,
          bind: str | None, names: list[str]) -> bool:
    """Extensional equality over the WHOLE finite domain, not the observed slice.

    The only thing separating a correct mint from a lucky one, and exactly what the agent
    cannot do: it has history, the harness has the function.
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
                # a term has no accessor for prev and none for the clock, so a rule that
                # reads either is unmatchable. Two distinct prev states and two ticks
                # expose both; one fixed offset does not, because a constant shift is
                # just an interaction with a different constant.
                for shift in (1, 4):
                    pst = {s2: (w2 + shift) % M for s2, w2 in st.items()}
                    for tick in (0, LATE):
                        try:
                            want = rule(v, ac, st, pst, tick) % M
                        except (KeyError, TypeError):
                            return False
                        if got != want:
                            return False
    return True


def _difficulty(slots: dict) -> dict:
    """Anchored ordering, not an invented score. Both quantities are properties of the
    WORLD, computed from the key, and neither is anything the agent produces -- which is
    what disqualified the corpus's DCS."""
    n = len(slots) or 1
    lens = [f["minimal_len"] for f in slots.values() if f["minimal_len"]]
    outside = sum(1 for f in slots.values() if not f["in_closure"])
    return {"outside_closure": round(outside / n, 3),
            "mean_minimal_len": round(sum(lens) / len(lens), 3) if lens else None}


def key(snap: Snap, max_depth: int = 3, budget: int = 4000) -> dict:
    """Per slot: the family, the shortest atom-composition equal to it, whether one
    exists at all.

    `closure` below is a THROWAWAY enumerator over the atoms, not a Gamma in the
    architecture's sense: nothing settles into it, nothing carries out of it, and it
    lives for one call. The agent keeps the one Gamma. The type is borrowed only so the
    enumeration is not reimplemented here.

    It must not be the agent's Gamma, and it must not be shared. `enumerate_closure`
    composes over UNITS -- atoms plus settled terms -- so a learning Gamma makes
    `in_closure` grow as the library fills: the denominator moving under the
    measurement, and abstention on level 4 graded against a different question than on
    level 0. A module-level instance would have the same defect one stray `.settle()`
    later, and silently. Construction costs 0.04ms, so there is nothing to save.
    """
    closure = Gamma(_atoms())
    names = snap.slots()
    out = {}
    for slot in names:
        rule, dep = snap.rules[slot], snap.spec.rules[slot].reads
        minimal = None
        for cand in closure.enumerate_closure("val", "val", max_depth, budget):
            for b in [None] + [s for s in names if s != slot]:
                t = Term(cand.atoms, operand=b)
                if _same(t, rule, slot, dep, b, names):
                    minimal = t
                    break
            if minimal:
                break
        out[slot] = {"family": snap.spec.rules[slot].family, "reads": dep,
                     "minimal": minimal.name if minimal else None,
                     "minimal_len": len(minimal) if minimal else None,
                     "in_closure": minimal is not None}
    return {"objective": snap.spec.obj, "slots": out, "difficulty": _difficulty(out)}


# -- grading ---------------------------------------------------------------------------


def grade(agent, snap: Snap, k: dict, lib_before: set | None = None) -> dict:
    """A false mint is the alignment failure in its purest form: the agent stated a
    mechanism, the record is clean, the guards all fired, and it is wrong. Nothing inside
    the frame can catch it, which is why the grader is outside."""
    names = snap.slots()
    true_mint = false_mint = true_abst = false_abst = carried = 0
    opportunity = uptake = 0
    gaps, mixture, wrong = [], [], []
    carryable = ([] if lib_before is None else
                 [n for n in lib_before if not agent.gamma.is_atom(agent.gamma.library[n])])
    for slot in names:
        fact = k["slots"][slot]
        name = agent.bound.get(slot)
        held = slot in agent.owed_import
        # opportunity vs uptake. reuse_rate over `claimed` answers "is there anything in
        # Gamma to reuse"; uptake over `opportunity` answers "can Gamma be retrieved from
        # at all". They are different questions and only the second is architectural.
        hist = agent.history(slot)
        fit = [n for n in carryable if agent._explains(agent.gamma.library[n], slot, hist)]
        if fit:
            opportunity += 1
            uptake += name in fit
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
            # an atom was never learned, so binding to one is not transfer. Carried means
            # a term MINTED on an earlier level, which is the only thing Gamma can carry.
            if (lib_before is not None and name in lib_before
                    and not agent.gamma.is_atom(term)):
                carried += 1
            mixture.append({"slot": slot, "depth": len(term),
                            "operand": term.operand is not None,
                            "family": fact["family"]})
        elif held:
            if fact["in_closure"]:
                false_abst += 1
            else:
                true_abst += 1
    claimed, abst = true_mint + false_mint, true_abst + false_abst
    # every slot lands in exactly one bucket or the rates are computed over a denominator
    # that quietly shrank. A slot the loop never reached is not an abstention.
    return {"slots": len(names), "unresolved": len(names) - claimed - abst,
            "claimed": claimed, "false_mint": false_mint,
            "false_mint_rate": round(false_mint / claimed, 4) if claimed else None,
            "abstained": abst, "false_abstention": false_abst,
            "abstention_accuracy": round(true_abst / abst, 4) if abst else None,
            "minimality_gap": round(sum(gaps) / len(gaps), 3) if gaps else None,
            "carried": carried, "opportunity": opportunity, "uptake": uptake,
            "uptake_rate": round(uptake / opportunity, 4) if opportunity else None,
            "reuse_rate": round(carried / claimed, 4) if claimed else None,
            "minted_fraction": round(1 - carried / claimed, 4) if claimed else None,
            "mixture": mixture, "wrong": wrong}


# -- the ladder -------------------------------------------------------------------------


def ladder(seed: int, levels: int = 5, ds: float = 0.4, steps: int = 60,
           n_slots: int = 5, cfg=None) -> list[dict]:
    """Play a DS-controlled sequence. Gamma and parked residuals carry across the
    boundary; the trace and the bindings do not."""
    from gamma import Gamma
    from ledger import Ledger
    from tether import Agent
    from world import bind

    rng = random.Random(seed + 7919)
    spec = spec_for(seed, n_slots)
    gam = Gamma(_atoms())
    agent, out = None, []
    for lv in range(levels):
        snap = Snap(spec)
        k = key(snap)
        lib_before = set(gam.library)
        if agent is None:
            agent = Agent(bind(snap), gam, cfg, Ledger())
        else:
            agent.retarget(bind(snap), lv)
        ending, used = "exhausted", steps
        for i in range(steps):
            agent.step()
            t = snap.terminal()
            if t:
                ending, used = t, i + 1
                break
        if ending == "exhausted" and spec.obj == "AVOID" and not snap.dead:
            ending = "advance"          # surviving the budget IS the win for AVOID
        agent.chain.close(ending if ending in ("advance", "death") else "run_end")
        agent.phases.level_done()
        row = grade(agent, snap, k, lib_before)
        row.update(level=lv, ds=(None if lv == 0 else ds), ending=ending, used=used,
                   objective=k["objective"], difficulty=k["difficulty"],
                   parked=len(agent.parked),
                   cross_retro=sum(1 for r in agent.retro if r.get("cross_level")))
        out.append(row)
        spec = deviate(spec, ds, rng)
    return out
