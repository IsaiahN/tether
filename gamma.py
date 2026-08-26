"""Gamma: the executable library.

Atoms are given. Molecules are priors -- named type-valid composites, loaded at start,
stamped so the record separates what the agent was handed from what it worked out.
MINT composes inside the closure and can never add an atom; only IMPORT moves the wall.

Three things beyond a plain library:

  ARITY     a term reads its own slot AND bound operands, so an interaction is expressible
  CHUNKING  a SETTLED term re-enters the search as one unit, so depth is measured in units
            and reach compounds while the closure itself is unchanged
  STANDING  a settled term the ground later refutes is demoted, weighted and clocked --
            defeasible, never deleted

Reports lambda, the spectral radius of the type transfer matrix, against V = |atoms|.
"""

from __future__ import annotations

import sys
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import Any

sys.dont_write_bytecode = True

PRIOR, MINTED, IMPORTED = "prior", "minted", "imported"

# anchor: specified, not grounded -- the formula requires demotion to be weighted and
# clocked, so a halflife is specified; nothing measures THIS halflife. A refutation is
# retractable, and how fast is a target for measurement rather than a finding.
REJECTION_HALFLIFE = 8.0


@dataclass(frozen=True)
class Ctx:
    """What an atom may read. All before-state: there is no accessor to the outcome, so a
    term that predicts by peeking is not constructible."""

    action: Any = None
    operands: tuple = ()          # other slots' values, in the term's binding order


@dataclass(frozen=True)
class Atom:
    name: str
    fn: Callable[[Any, Ctx], Any]
    in_type: str
    out_type: str
    reads_operand: bool = False   # declared at construction, never inferred from the name

    def __repr__(self) -> str:
        return f"Atom({self.name})"


@dataclass(frozen=True)
class Term:
    """A composition of atoms applied left to right, with an optional operand binding."""

    atoms: tuple[Atom, ...]
    origin: str = MINTED
    operand: str | None = None    # which slot fills operand 0, or None for unary

    @property
    def name(self) -> str:
        base = " . ".join(a.name for a in self.atoms)
        return f"{base}<{self.operand}>" if self.operand else base

    @property
    def in_type(self) -> str:
        return self.atoms[0].in_type

    @property
    def out_type(self) -> str:
        return self.atoms[-1].out_type

    @property
    def reads_operand(self) -> bool:
        return any(a.reads_operand for a in self.atoms)

    def __len__(self) -> int:
        return len(self.atoms)

    def __repr__(self) -> str:
        return f"Term({self.name})"

    def apply(self, value: Any, ctx: Ctx) -> Any:
        for a in self.atoms:
            value = a.fn(value, ctx)
        return value


@dataclass
class Standing:
    """A term's record against the ground. Weighted, clocked, and never a hard ban."""

    settled_at: int | None = None
    rejections: float = 0.0
    last_tick: int = 0

    def refute(self, tick: int) -> None:
        self.decay(tick)
        self.rejections += 1.0
        self.settled_at = None

    def decay(self, tick: int) -> None:
        gap = max(0, tick - self.last_tick)
        if gap:
            self.rejections *= 0.5 ** (gap / REJECTION_HALFLIFE)
            self.last_tick = tick

    @property
    def settled(self) -> bool:
        return self.settled_at is not None


class Gamma:
    def __init__(self, atoms: list[Atom],
                 molecules: list[tuple[str, tuple[str, ...]]] = ()) -> None:
        if not atoms:
            raise ValueError("Gamma needs at least one atom")
        self.atoms = list(atoms)
        self._by_name = {a.name: a for a in atoms}
        self.library: dict[str, Term] = {}
        self.stamps: dict[str, dict[str, Any]] = {}
        self.standing: dict[str, Standing] = {}
        # name -> the two verdicts that promoted it. A dict rather than a set because
        # `primitive requires both` is only checkable if both are on the record.
        self.primitives: dict[str, dict] = {}
        self.tick = 0
        for a in atoms:
            self._install(Term((a,), origin=PRIOR), seq=-1, residual=None)
        for label, chain in molecules:
            self._install(self.build(chain, origin=PRIOR), seq=-1, residual=f"molecule:{label}")

    # -- construction ---------------------------------------------------------------

    def build(self, names: tuple[str, ...], origin: str = MINTED,
              operand: str | None = None) -> Term:
        return Term(tuple(self._by_name[n] for n in names), origin=origin, operand=operand)

    def _install(self, term: Term, seq: int, residual: str | None) -> Term:
        self.library[term.name] = term
        self.stamps[term.name] = {"origin": term.origin, "seq": seq, "residual": residual}
        self.standing.setdefault(term.name, Standing(last_tick=self.tick))
        return term

    def accept(self, term: Term, seq: int, residual: str) -> Term:
        """Stamped with where it came from and when. A derived term and an adopted one
        differ only in the record."""
        if term.name in self.library:
            raise ValueError(f"already in library: {term.name}")
        return self._install(term, seq, residual)

    # -- standing: the ground's verdict, defeasibly ----------------------------------

    def settle(self, name: str) -> None:
        """The ground paid on evidence the term was never fitted to."""
        self.standing.setdefault(name, Standing()).settled_at = self.tick

    def promote(self, name: str, shadow: dict, echo: dict) -> None:
        """PRIMITIVE. Settled is held-out payment on the slot the term was minted for,
        and that does not discriminate -- every wrong term in the false-mint read fired
        the held-out test and survived it. A primitive is the stronger thing: it closed a
        residual RECORDED BEFORE IT EXISTED, somewhere it was not minted for.

        Both verdicts or neither. Echo alone is apophenia -- a structure found and given
        somewhere to live. Shadow alone is a local hack called a primitive.
        """
        self.primitives[name] = {"shadow": shadow, "echo": echo}

    def is_primitive(self, name: str) -> bool:
        return name in self.primitives


    def refute(self, name: str) -> bool:
        """A settled term mispredicted on fresh evidence. Demoted to candidate -- not
        deleted, and the rejection decays, so it can settle again if it starts paying."""
        st = self.standing.setdefault(name, Standing())
        was = st.settled
        st.refute(self.tick)
        return was

    def is_settled(self, name: str) -> bool:
        return self.standing.get(name, Standing()).settled

    def rejection_of(self, name: str) -> float:
        st = self.standing.get(name)
        if st is None:
            return 0.0
        st.decay(self.tick)
        return st.rejections

    @property
    def settled_terms(self) -> list[Term]:
        return [t for n, t in self.library.items() if self.is_settled(n)]

    # -- reach ----------------------------------------------------------------------

    @property
    def alphabet(self) -> int:
        return len(self.atoms)

    def is_atom(self, term: Term) -> bool:
        """NOVEL is relative to atoms, not to the world."""
        return len(term) == 1 and term.atoms[0].name in self._by_name

    def units(self) -> list[Term]:
        """What the search composes FROM: the atoms, plus every SETTLED term as one unit.

        The closure does not change -- MINT still cannot add an atom. What changes is what
        is reachable at a given budget: a settled 3-atom term makes depth 3 reach 9 atoms.
        Only what the ground has paid for becomes a shortcut.
        """
        # DEDUP ON WHAT IS EMITTED, not on what was settled. `t.name` carries the
        # operand binding and the emitted unit does not, so two settled terms differing
        # only in their binding both passed the check and both went in -- one unit
        # counted twice, inflating `space_estimate` and with it the `coverage`
        # denominator on every mint row. The binding is re-decided per slot at mint, and
        # `enumerate_closure` composes over `.atoms` alone, so the chunk IS the atom
        # sequence and the operand has no business in the key.
        seen = {a.name for a in self.atoms}
        out = [Term((a,), origin=PRIOR) for a in self.atoms]
        for t in self.settled_terms:
            if len(t) <= 1:
                continue
            unit = Term(t.atoms, origin=t.origin)
            if unit.name not in seen:
                seen.add(unit.name)
                out.append(unit)
        return out

    def enumerate_closure(self, in_type: str, out_type: str, max_depth: int, budget: int,
                          stats: dict | None = None) -> Iterator[Term]:
        """Type-valid pipelines over UNITS, shortest first, capped by budget.

        Yielding a term is a WITNESS that it is reachable. Stopping is one of two facts and
        they are not the same claim: `budget_spent` (we stopped early) or `depth_exhausted`
        (we saw the whole space at this depth and it did not contain one).
        """
        units = self.units()
        emitted = 0
        # written UP FRONT: a caller that breaks early abandons the generator, so anything
        # only written at exhaustion is never seen. `units` and `estimate` are known now;
        # `seen` is kept live per yield so an early break still reports honest coverage.
        if stats is not None:
            stats["units"] = len(units)
            stats["estimate"] = self.space_estimate(len(units), max_depth)
            stats["seen"] = 0
        frontier = [u.atoms for u in units if u.in_type == in_type]
        depth = 1
        spent = False
        while frontier and depth <= max_depth:
            nxt: list[tuple[Atom, ...]] = []
            for chain in frontier:
                if chain[-1].out_type == out_type:
                    if emitted >= budget:
                        spent = True
                        break
                    emitted += 1
                    if stats is not None:
                        stats["seen"] = emitted
                    yield Term(chain)
                if depth < max_depth:
                    nxt += [chain + u.atoms for u in units if u.in_type == chain[-1].out_type]
            if spent:
                break
            frontier, depth = nxt, depth + 1
        if stats is not None:
            stats["seen"] = emitted
            stats["budget_spent"] = spent
            stats["depth_exhausted"] = not spent

    @staticmethod
    def space_estimate(units: int, max_depth: int) -> int:
        """Roughly how many compositions exist at this depth: sum of units^d.

        The denominator that turns 'unreached' from a word into a measurement.
        """
        return sum(units ** d for d in range(1, max_depth + 1))

    # -- typing beats size, as a number -----------------------------------------------

    def type_report(self, iters: int = 200) -> dict[str, float]:
        """lambda = spectral radius of the type transfer matrix, by power iteration.

        Well-typed terms of size n grow as lambda^n; an untyped bag of V symbols grows as
        V^n. The ratio is what typing buys per unit of depth.
        """
        types = sorted({a.in_type for a in self.atoms} | {a.out_type for a in self.atoms})
        idx = {t: i for i, t in enumerate(types)}
        n = len(types)
        m = [[0.0] * n for _ in range(n)]
        for a in self.atoms:
            m[idx[a.in_type]][idx[a.out_type]] += 1.0
        v = [1.0] * n
        lam = 0.0
        for _ in range(iters):
            w = [sum(m[i][j] * v[i] for i in range(n)) for j in range(n)]
            lam = max(abs(x) for x in w) or 0.0
            if lam == 0.0:
                break
            v = [x / lam for x in w]
        v_count = float(self.alphabet)
        return {"lambda": round(lam, 4), "V": v_count, "types": n,
                "advantage_per_depth": round(v_count / lam, 4) if lam else float("inf")}
