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

import json
import pathlib
import random
import sys
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import Any

sys.dont_write_bytecode = True

PRIOR, MINTED, IMPORTED = "prior", "minted", "imported"

# The identity, by name. It predicts and it does not compose -- see the closure.
IDN_NAME = "idn"

# WHICH CLAUSE ADMITTED AN ENTRY -- Â§11's two, and `None` for "not stated".
# ORIGIN IS NOT THIS. `PRIOR` is stamped on every atom at construction, so it records that no
# mint occurred -- NOT that an entry rule was applied. The ablation partitions by CLAUDE.md's
# clause 3, which asks WHICH CLAUSE let a thing in, and that cannot be recovered from `prior`
# afterwards. Recorded at entry because it is unrecoverable later; what each value IMPLIES for
# the wipe is a separate and deferred decision, and nothing here presupposes it.
NECESSARY, PROMOTED, ACCEPTED = "necessary", "promoted", "accepted"

# AN OPERAND TYPE HAS TWO FORMS AND ONE SENTINEL IS THE MINIMUM THAT SAYS SO. `recolour`
# needs a COLOUR whatever slot it is applied to; `translate` needs whatever the TARGET is,
# because `v + operand` is only meaningful between commensurable quantities. A single fixed
# string could express the first and not the second, and the second is the one that produced
# the defect.
SAME_AS_TARGET = "@same"

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
    # WHAT THE OPERAND MUST BE, not only THAT there is one. `0a`'s typing half, whose
    # trigger fired on a real board: `idn . recolour<o11.h>` bound a HEIGHT as a colour
    # operator's operand and nothing refused it, because this class typed input and output
    # and not the operand. `None` means UNDECLARED and is checked nowhere -- an absence the
    # binder reports rather than a permission.
    operand_type: str | None = None

    def __repr__(self) -> str:
        return f"Atom({self.name})"


@dataclass(frozen=True)
class Term:
    """A composition of atoms applied left to right, with an optional operand binding."""

    atoms: tuple[Atom, ...]
    origin: str = MINTED
    operand: str | None = None    # which slot fills operand 0, or None for unary
    # Â§15.5's `When(P, R)` -- guarded by a predicate -- and it is a CONSTRUCTOR there, not
    # an atom. A chain has no branch, so a gate written as an atom would have to
    # short-circuit the rest of it, which `val -> val` gives it no way to do. So the guard
    # lives on the Term: `f` when the action matches, IDENTITY otherwise.
    #
    # BOUND, NEVER ENUMERATED, and that is what makes it survive ARC: the action set changes
    # per frame, so a per-action ATOM would have to be rebuilt. This adds no atom.
    #
    # WHAT IT DOES NOT DO, AND IT WAS BUILT ON THE CLAIM THAT IT DID. It does not reach
    # `discriminate`. `units()` strips the operand and the guard before emitting -- *the
    # chunk IS the atom sequence and the operand has no business in the key* -- so
    # `enumerate_closure` yields bare chains and `spread` never sees a guard. That is
    # DELIBERATE and documented one method away, and the justification was written without
    # reading it. **The guard works where `_ops` supplies operands, which is bets.**
    guard: str | None = None

    @property
    def name(self) -> str:
        base = " . ".join(a.name for a in self.atoms)
        if self.operand:
            base = f"{base}<{self.operand}>"
        return f"{base}?{self.guard}" if self.guard else base

    @property
    def in_type(self) -> str:
        return self.atoms[0].in_type

    @property
    def out_type(self) -> str:
        return self.atoms[-1].out_type

    @property
    def reads_operand(self) -> bool:
        return any(a.reads_operand for a in self.atoms)

    def handle(self, game: str) -> str:
        """`{game}_{INITIALS}_{kind}_{suffix}` -- PROVENANCE, assigned by the system.

        **The letters are the first letter of each atom IN COMPOSITION ORDER**, so the handle
        carries its own decomposition: `ls20_ITR_chain_7f21` pulled against a `bp35` residual
        says *minted on one game, composed from these three, reused on another* **without
        opening anything.**

        **THE PREFIX IS BIRTH, NEVER USE.** A term minted on `ls20` and pulled on `bp35` keeps
        `ls20_`; the pull count is its life.

        **AND THE LETTERS ARE A MNEMONIC, NEVER A KEY -- MEASURED, NOT CAUTIONED.** The 14-atom
        ARC set has **10 distinct initials**: `A` is `above`/`all`/`any`, `C` is `col`/`colour`,
        `R` is `recolour`/`row`. A 3-chain has at most 1000 letter-triples against a depth-3
        closure far larger than that, **and this is the smallest atom set this will ever run
        on.** The suffix is what makes a handle unique.

        **NOTHING SHOULD EVER PARSE THEM, AND THE REASON IS THAT IT NEVER NEEDS TO**: `name` IS
        the composition, exactly and unambiguously, one field away. A letter-parse is never the
        shortest path to the parts, so the way to stop one being written is that a correct
        alternative is nearer -- not a warning that a reader has to obey.

        **The letters derive from `Atom.name` and are NOT stable across a rename.** Tolerable
        only because they are not a key; if anything ever keys on them, that becomes a defect.
        """
        letters = "".join(a.name[0].upper() for a in self.atoms)
        kind = "chain" if len(self.atoms) > 1 else "term"
        # EIGHT RANDOM CHARACTERS, AND THE DEDUP IS WHAT MAKES IT REPRODUCIBLE -- NOT THE
        # SUFFIX. I argued a drawn suffix cannot reproduce across runs; **that describes the
        # design as a defect.** The library PERSISTS by design -- *humans do not reset their
        # memory every time they play a new game* -- so a composition minted once keeps its
        # handle for the life of the library. **There is no cold start after the first, and a
        # first run has nothing to reproduce against**, the same as a person's first game.
        #
        # So the suffix is generated ONCE, for a composition the library does not already
        # hold: the mint path cuts `term.name in library` as `not-novel` before anything is
        # minted, and `_install` uses `setdefault`. **The lookup is stable, so the handle is.**
        #
        # THE CASE A HASH WOULD HAVE COVERED, recorded so the objection is not re-derived: two
        # libraries that DIVERGED -- separate machines, or a swarm minting independently and
        # merging later -- would carry two handles for one composition. **Dedup on the
        # COMPOSITION fixes that at merge**, which is why the check is on `name` and not on
        # the handle.
        #
        # `random` rather than a wall clock, so nothing here reads the outside world.
        h = "".join(random.choices("0123456789abcdef", k=8))
        return f"{game}_{letters}_{kind}_{h}"

    @property
    def operand_type(self) -> str | None:
        """What the OPERAND-READING atom requires. A Term is what the binder sees, so the
        requirement has to be reachable from here -- reading it off the Term returned `None`
        on every one of 911,035 calls and the check was inert."""
        for a in self.atoms:
            if a.reads_operand:
                return a.operand_type
        return None

    def __len__(self) -> int:
        return len(self.atoms)

    def __repr__(self) -> str:
        return f"Term({self.name})"

    def apply(self, value: Any, ctx: Ctx) -> Any:
        """IDENTITY WHEN THE GUARD FAILS, which is the whole conditional. `When(P, R)` with
        `idn` as the else-branch -- the only two-branch form a left-to-right chain admits."""
        if self.guard is not None and ctx.action != self.guard:
            return value
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
    def __init__(self, atoms: list[Atom], game: str = "x") -> None:
        """NO `molecules` PARAMETER, and its removal is the 2026-08-27 ruling in code.

        It installed TERM priors at construction with `origin=PRIOR` -- **the one route by
        which a term could enter Î“ without being earned**, which Â§11 forbids and which the
        VISIBLE SET replaces: a term is visible, aimed at, and enters only when regenerated,
        under clause two. It had zero call sites, so it was not dormant but a **trapdoor to a
        forbidden state**, and leaving it would have made `admissions` report a bucket that
        must never be populated. **It also retires half of `molecule`'s A6i collision.**
        """
        if not atoms:
            raise ValueError("Gamma needs at least one atom")
        self.atoms = list(atoms)
        self._by_name = {a.name: a for a in atoms}
        self.library: dict[str, Term] = {}
        # PROVENANCE, one field. `{game}_{INITIALS}_{kind}_{suffix}` -- the game is where the
        # term was MINTED, and it does not change when the term is later pulled elsewhere.
        self.game = str(game)
        self.handles: dict[str, str] = {}
        self.stamps: dict[str, dict[str, Any]] = {}
        self.standing: dict[str, Standing] = {}
        # name -> the two verdicts that promoted it. A dict rather than a set because
        # `primitive requires both` is only checkable if both are on the record.
        self.primitives: dict[str, dict] = {}
        self.tick = 0
        # 3d / Â§17.7. Set by the agent to a `(unit) -> tuple` ranking. None keeps the
        # registry order this had, so installing a rank is an observable change and not
        # installing one changes nothing.
        self.unit_rank = None
        for a in atoms:
            self._install(Term((a,), origin=PRIOR), seq=-1, residual=None,
                          admitted=NECESSARY)   # the loop cannot run without a vocabulary

    # -- construction ---------------------------------------------------------------

    def build(self, names: tuple[str, ...], origin: str = MINTED,
              operand: str | None = None) -> Term:
        return Term(tuple(self._by_name[n] for n in names), origin=origin, operand=operand)

    def _install(self, term: Term, seq: int, residual: str | None,
                 admitted: str | None = None) -> Term:
        self.library[term.name] = term
        # THE HANDLE IS STAMPED AT INSTALL, because the prefix is BIRTH: where it was minted,
        # never where it is later pulled. Assigning it anywhere else would let a pull rewrite
        # a provenance.
        if term.origin != PRIOR:
            # A HANDLE IS PROVENANCE FOR SOMETHING MINTED. An atom was never minted anywhere,
            # so it gets none: every atom installs at the same seq, and handling them collided
            # 4 of 14 while saying nothing true about any.
            #
            # ASSIGNED ONCE, NEVER REASSIGNED -- and this is what makes a DRAWN suffix safe.
            # **Identity is the COMPOSITION, not the handle**: `term.name` is exact, so a
            # composition that already exists keeps the handle it was born with and a second
            # install cannot rewrite its provenance. Without this a re-mint would draw a fresh
            # handle for the same term and the two would read as two discoveries.
            self.handles.setdefault(term.name, term.handle(self.game))
        self.stamps[term.name] = {"origin": term.origin, "seq": seq, "residual": residual,
                                  "admitted": admitted}
        self.standing.setdefault(term.name, Standing(last_tick=self.tick))
        return term

    def admissions(self) -> dict[str, int]:
        """How many entries cited each of Â§11's two clauses.

        **FOUR CLAUSES, AND `unstated` IS STILL THE FALSIFIER.**

            necessary   the atoms -- Â§11 clause one, *the loop cannot run without it*
            accepted    minted, closed a residual, paid the bargain. **Earned and pre-boundary**
            promoted    survived a boundary -- Â§11 clause two
            imported    minted on another game. Across games there is no *first*, so it is not
                        clause two; it wipes like `promoted` and is counted apart

        **`accepted` WAS ADDED AFTER THIS COUNTER FIRED, WHICH IS THE ONLY REASON IT IS HERE.**
        The text above once read *the only ways in are `necessary` and `promoted`, so a
        non-zero `unstated` means something entered by a route that should not exist* -- and
        that was **correct about the routes it knew and silent about the one that carries
        everything.** It could not fail, because it also read `origin != PRIOR: continue` and
        so counted the atoms alone. Fixed, it read **19 of 21 unstated** on the first run with
        real mints in it.

        **AND `unstated` MUST STILL BE ABLE TO FIRE.** Four clauses and a fifth bucket for
        *none of these* -- **a falsifier that cannot be non-zero is exactly what this one had
        just stopped being.**
        """
        out: dict[str, int] = {}
        for st in self.stamps.values():
            # EVERY INSTALLED TERM, NOT ONLY THE PRIORS. This read `origin != PRIOR: continue`
            # and so counted the ATOMS ALONE -- which made `unstated should read zero forever`
            # true for a reason that had nothing to do with the check: its population could
            # only contain priors, and a prior always carries `necessary`. **A falsifier over
            # a population that cannot contain the defect it looks for.** Confirmed by running
            # it on a fresh Gamma, reading `{necessary: 14}`, and reporting the zero as clean.
            key = st.get("admitted") or "unstated"
            out[key] = out.get(key, 0) + 1
        return out

    def accept(self, term: Term, seq: int, residual: str) -> Term:
        """Stamped with where it came from and when. A derived term and an adopted one
        differ only in the record."""
        if term.name in self.library:
            raise ValueError(f"already in library: {term.name}")
        # THE FOURTH CLAUSE, RULED. A term that closed a residual and paid the bargain is
        # EARNED -- it simply has not crossed a boundary yet, and `promoted` is a claim about
        # surviving one. Leaving it clauseless made `unstated` read 19 of 21 on the first run
        # that put real mints through the counter.
        return self._install(term, seq, residual, admitted=ACCEPTED)

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

    # -- persistence: Â§17.8's decision, made rather than defaulted -------------------------

    def save(self, path: str) -> dict:
        """Write the minted library. **SEAT-SIDE: the agent never calls this.**

        Â§17.8 asked for a POLICY and a SWITCH -- *state it, and make it switchable so the
        ablation is runnable* -- and recorded its own inclination as *start cold across games*.
        **Isaiah ruled the opposite: the library persists, because transfer is the claim.**
        Â§17.8 calls that a decision rather than a default, so both are in bounds and this is
        the one taken. **The switch is that nothing calls save/load unless the seat does**, so
        the ablation stays runnable by simply not loading.

        **ATOMS ARE NOT WRITTEN.** They are the registry, identical on both sides; writing them
        would be a second producer of the vocabulary. What is written is the COMPOSITION -- the
        atom NAMES in order -- plus origin, admitting clause and handle.
        """
        out = []
        for name, t in self.library.items():
            if t.origin == PRIOR:
                continue          # an atom was not minted; there is nothing to carry
            st = self.stamps.get(name)
            out.append({"atoms": [a.name for a in t.atoms], "origin": t.origin,
                        "handle": self.handles.get(name), "game": self.game,
                        "admitted": getattr(st, "admitted", None) if st else None,
                        "residual": getattr(st, "residual", None) if st else None})
        pathlib.Path(path).write_text(json.dumps(out, indent=1), encoding="utf-8")
        return {"written": len(out), "path": path}

    def load(self, path: str) -> dict:
        """Read a saved library into this Gamma. **SEAT-SIDE, and it REFUSES loudly.**

        **THE COMPOSITION CROSSES AND THE BINDING DOES NOT**, which is the colour ruling
        applied to a term: *vocabulary permanent, instances transient*. `translate<o11.row>`
        names a slot that does not exist in another game and an action another game may not
        advertise -- so **operand and guard are dropped and the atom chain is kept**, which is
        exactly what `units()` already does when it emits a settled term: *the chunk IS the
        atom sequence*.

        **A TERM WHOSE ATOMS THIS REGISTRY LACKS IS REFUSED, NOT SKIPPED.** A different domain
        has a different atom set, and silently dropping half a library would read as a small
        library rather than as an incompatible one.

        **AND A TERM FROM ANOTHER GAME ENTERS AS `IMPORTED`, NEVER AS `promoted`.** Â§11 clause
        two is *the agent minted a crude version first and we are promoting it* -- and across
        games there is no first. `necessary` stays, `promoted` wipes, **`IMPORTED` wipes and is
        counted apart**, so the transfer number is readable and the ablation is unaffected.
        """
        rows = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
        took, refused = [], []
        for r in rows:
            names = tuple(r["atoms"])
            if not all(n in self._by_name for n in names):
                refused.append({"atoms": list(names), "why": "atom not in this registry"})
                continue
            t = Term(tuple(self._by_name[n] for n in names),
                     origin=IMPORTED if r.get("game") != self.game else r["origin"])
            if t.name in self.library:
                took.append({"handle": r.get("handle"), "already_held": True})
                continue          # dedup on the COMPOSITION -- it keeps the handle it has
            self._install(t, seq=-2, residual=r.get("residual"),
                          admitted=IMPORTED if t.origin == IMPORTED else r.get("admitted"))
            if r.get("handle"):
                self.handles[t.name] = r["handle"]   # the birth handle, carried
            took.append({"handle": r.get("handle"), "already_held": False})
        return {"loaded": sum(1 for x in took if not x["already_held"]),
                "already_held": sum(1 for x in took if x["already_held"]),
                "refused": refused,
                "reads": ("composition crosses, binding does not. A refused row is an "
                          "INCOMPATIBLE registry, not a small library")}

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
        # 3d: ORDER IS THE SEARCH'S ONLY FREE VARIABLE. `enumerate_closure` breaks on the
        # first zero-residual term, so what the units are sorted by decides how many
        # candidates get tried before it is found. Registry order when nothing is installed.
        return sorted(out, key=self.unit_rank) if self.unit_rank else out

    def enumerate_closure(self, in_type: str, out_type: str, max_depth: int, budget: int,
                          stats: dict | None = None,
                          order: Callable[[Term], float] | None = None) -> Iterator[Term]:
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
        start = [u for u in units if u.in_type == in_type]
        # §23.5's PREREQUISITE, and it is not a new judgement. *Loading generously requires
        # retrieval-by-characterised-residual, not enumeration -- a big library is an asset
        # when you look things up by the shape of your gap and a liability when you walk it in
        # registry order.* Under a budget SOMETHING already decides what is seen, and it is
        # currently the order units happen to be in. This replaces an accident with a ranking.
        #
        # **IT ORDERS, IT NEVER ADMITS.** The bargain is untouched, so nothing passes here that
        # would not have passed before -- what changes is which candidates are REACHED inside
        # `budget`, never which are accepted.
        #
        # **A DEGENERATE RANKING IS REFUSED.** All units scoring alike makes the argmax
        # arbitrary, and acting on an arbitrary argmax is noise wearing an ordering's name.
        # `max > min` is the existential `discriminate` already uses -- no parameter.
        if order is not None and start:
            sc = [order(u) for u in start]
            if max(sc) > min(sc):
                start = [u for _, u in sorted(zip(sc, start, strict=True),
                                              key=lambda x: (-x[0], x[1].name))]
        frontier = [u.atoms for u in start]
        frontier = [u.atoms for u in start]
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
                    # THE IDENTITY IS NOT COMPOSABLE. `X . idn` and `idn . X` compute `X`, so
                    # every occurrence inside a chain is a longer spelling of a shorter term --
                    # and the closure was counting them as distinct candidates. **39 names
                    # computed 7 functions at depth 3, 25 of the 39 containing `idn`**, a 5.57x
                    # inflation growing 1.00 -> 2.40 -> 5.57 with depth.
                    #
                    # THAT NUMBER IS COVERAGE'S DENOMINATOR. §19.1 turns `UNREACHED` into a
                    # measurement with `candidates_seen / estimate`, and both sides were
                    # counting each function several times -- **so it does not cancel**: the
                    # numerator spends real budget on duplicates, the denominator is a `λ^d`
                    # estimate that never saw one.
                    #
                    # **IT STAYS A DEPTH-1 CANDIDATE.** *This slot does not change* is a real
                    # prediction and `idn` alone is how it is said -- removing it from `units()`
                    # entirely was tried and the falsifier caught it: **7 functions fell to 6.**
                    # So the cut is on COMPOSITION, not on membership, and `_predict`'s fallback
                    # reads `library["idn"]` directly and is untouched.
                    nxt += [chain + u.atoms for u in units
                            if u.in_type == chain[-1].out_type
                            and not any(a.name == IDN_NAME for a in (*chain, *u.atoms))]
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

    def type_report(self, iters: int = 400) -> dict[str, float]:
        """lambda = spectral radius of the type transfer matrix. SHIFTED, and that is the fix.

        Well-typed terms of size n grow as lambda^n; an untyped bag of V symbols grows as
        V^n. The ratio is what typing buys per unit of depth.

        **PLAIN POWER ITERATION DOES NOT CONVERGE ON A PERIODIC MATRIX, AND A TYPE GRAPH IS
        PERIODIC WHENEVER IT HAS A CYCLE.** Measured on the three-space set: the graph is a
        3-cycle `OBJ -> ATTR -> PRED -> OBJ` plus an aperiodic `val` self-loop, the true
        spectral radius is **3.5569 = (5*3*3)^(1/3)**, and the old iteration reported
        **3.0000** -- it oscillated on the cyclic block and settled on the self-loop. **The
        missing 0.557 was exactly the cycle**, on the quantity the Stage 1 falsifier was
        answered with, which `CLAUDE.md` cites as *the spectral radius* by name.

        **THE SHIFT IS EXACT, NOT AN APPROXIMATION.** For a NON-NEGATIVE matrix -- and a
        transfer matrix is counts -- Perron-Frobenius gives a real dominant root `r` with
        `r >= |lambda_i|` for every eigenvalue, so `rho(M + cI) = r + c`. Adding `c` to the
        diagonal gives every node a self-loop, which makes the matrix APERIODIC and the
        iterate converge; subtracting `c` afterwards recovers `r`.

        **AND THE NORM CHANGED WITH IT.** The old code took the max-norm of the iterate as
        the eigenvalue; the growth ratio is what converges, so `v` is normalised to sum 1 and
        `lambda` is the L1 mass of `Mv`.
        """
        types = sorted({a.in_type for a in self.atoms} | {a.out_type for a in self.atoms})
        idx = {t: i for i, t in enumerate(types)}
        n = len(types)
        m = [[0.0] * n for _ in range(n)]
        for a in self.atoms:
            m[idx[a.in_type]][idx[a.out_type]] += 1.0
        shift = 1.0
        for i in range(n):
            m[i][i] += shift
        v = [1.0 / n] * n if n else []
        lam = 0.0
        for _ in range(iters):
            w = [sum(m[i][j] * v[i] for i in range(n)) for j in range(n)]
            total = sum(w)
            if total <= 0.0:
                break
            lam = total
            v = [x / total for x in w]
        lam = max(0.0, lam - shift)
        v_count = float(self.alphabet)
        return {"lambda": round(lam, 4), "V": v_count, "types": n,
                "advantage_per_depth": round(v_count / lam, 4) if lam else float("inf")}
