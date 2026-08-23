"""Gamma: the executable library.

Atoms are given. Molecules are priors -- named type-valid composites, loaded at start,
stamped so the record separates what the agent was handed from what it worked out.
MINT composes inside the closure and can never add an atom; only IMPORT moves the wall.

Reports lambda, the spectral radius of the type transfer matrix, against V = |atoms|.
That is "typing beats size" as a measured quantity, available before anything runs, and
it gives REACHABILITY a cost model: depth d costs lambda^d, not V^d.
"""

from __future__ import annotations

import sys
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import Any

sys.dont_write_bytecode = True

PRIOR, MINTED, IMPORTED = "prior", "minted", "imported"


@dataclass(frozen=True)
class Ctx:
    action: Any = None


@dataclass(frozen=True)
class Atom:
    name: str
    fn: Callable[[Any, Ctx], Any]
    in_type: str
    out_type: str

    def __repr__(self) -> str:
        return f"Atom({self.name})"


@dataclass(frozen=True)
class Term:
    """A composition of atoms, applied left to right."""

    atoms: tuple[Atom, ...]
    origin: str = MINTED

    @property
    def name(self) -> str:
        return " . ".join(a.name for a in self.atoms)

    @property
    def in_type(self) -> str:
        return self.atoms[0].in_type

    @property
    def out_type(self) -> str:
        return self.atoms[-1].out_type

    def __len__(self) -> int:
        return len(self.atoms)

    def __repr__(self) -> str:
        return f"Term({self.name})"

    def apply(self, value: Any, ctx: Ctx) -> Any:
        for a in self.atoms:
            value = a.fn(value, ctx)
        return value


class Gamma:
    def __init__(self, atoms: list[Atom],
                 molecules: list[tuple[str, tuple[str, ...]]] = ()) -> None:
        if not atoms:
            raise ValueError("Gamma needs at least one atom")
        self.atoms = list(atoms)
        self._by_name = {a.name: a for a in atoms}
        self.library: dict[str, Term] = {}
        self.stamps: dict[str, dict[str, Any]] = {}
        for a in atoms:
            self._install(Term((a,), origin=PRIOR), seq=-1, residual=None)
        for label, chain in molecules:
            self._install(self.build(chain, origin=PRIOR), seq=-1, residual=f"molecule:{label}")

    # -- construction ---------------------------------------------------------------

    def build(self, names: tuple[str, ...], origin: str = MINTED) -> Term:
        return Term(tuple(self._by_name[n] for n in names), origin=origin)

    def _install(self, term: Term, seq: int, residual: str | None) -> Term:
        self.library[term.name] = term
        self.stamps[term.name] = {"origin": term.origin, "seq": seq, "residual": residual}
        return term

    def accept(self, term: Term, seq: int, residual: str) -> Term:
        """Stamped with where it came from and when. The stamp is not bookkeeping:
        a derived term and an adopted one differ only in the record."""
        if term.name in self.library:
            raise ValueError(f"already in library: {term.name}")
        return self._install(term, seq, residual)

    # -- reach ----------------------------------------------------------------------

    @property
    def alphabet(self) -> int:
        return len(self.atoms)

    def is_atom(self, term: Term) -> bool:
        """NOVEL means novel relative to atoms, not to the world."""
        return len(term) == 1 and term.atoms[0].name in self._by_name

    def enumerate_closure(self, in_type: str, out_type: str, max_depth: int,
                          budget: int) -> Iterator[Term]:
        """Type-valid pipelines, shortest first, capped by budget.

        Yielding a term is a WITNESS that it is reachable. Exhausting the budget without
        yielding is UNREACHED -- a fact about this search, never a proof of absence.
        """
        emitted = 0
        frontier = [(a,) for a in self.atoms if a.in_type == in_type]
        depth = 1
        while frontier and depth <= max_depth:
            nxt: list[tuple[Atom, ...]] = []
            for chain in frontier:
                if chain[-1].out_type == out_type:
                    if emitted >= budget:
                        return
                    emitted += 1
                    yield Term(chain)
                if depth < max_depth:
                    nxt += [chain + (a,) for a in self.atoms if a.in_type == chain[-1].out_type]
            frontier, depth = nxt, depth + 1

    # -- typing beats size, as a number -----------------------------------------------

    def type_report(self, iters: int = 200) -> dict[str, float]:
        """lambda = spectral radius of the type transfer matrix, by power iteration.

        The number of well-typed terms of size n grows as lambda^n; an untyped bag of V
        symbols grows as V^n. The ratio is what typing buys, per unit depth.
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
