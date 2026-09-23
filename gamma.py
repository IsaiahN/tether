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

from sensors import CELLS, NOT_RESOLVED, Cells

sys.dont_write_bytecode = True

def _replay_delta(d: dict):
    """The re-invented atom's body: the agent's RECORDED observation, replayed.

    A FACTORY AT MODULE LEVEL, not a closure in the loop -- defining it inside the loop binds
    the loop variable, so every re-invented atom would end up carrying the LAST delta in the
    file. Each call closes over its own map.

    Keys are strings because the delta round-trips through JSON; the lookup stringifies to
    match, and an unrecognised value ABSTAINS rather than guessing.
    """
    def fn(v, _c):
        got = d.get(str(v))
        return NOT_RESOLVED if got is None else got
    return fn


PRIOR, MINTED, IMPORTED = "prior", "minted", "imported"
# THE FOURTH ORIGIN, AND IT IS A FOURTH RATHER THAN A REUSE OF `IMPORTED` ON PURPOSE. Isaiah,
# 2026-09-22: *import comes from OUTSIDE the library... it is the CREATION OF A BRAND-NEW ATOM
# described from what the agent has observed.* But `IMPORTED` already means ADOPTED-FROM-
# ELSEWHERE here, in `tether.py:1448` and in `CLAUDE.md`'s provenance law -- so writing
# "import = invent" would put two quantities under one word AT THE SITE THAT DEFINES BOTH,
# which is `A6i` in its guaranteed form. `INVENTED` keeps them apart and leaves `IMPORTED`
# untouched.
INVENTED = "invented"

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
# THE `Ctx` FIELDS THAT REACH ANOTHER SLOT'S VALUE. `action` does not; the rest do -- `operands`
# reaches the bound slot, `group` every peer holding the same attribute, `obj` every attribute
# of the term's own owner, and `touching` the positions of whatever is in contact. **An atom
# declaring any of these cannot claim invariance to the other slots**, which is the whole of
# what `key_of` was getting wrong.
SLOT_REACHING = ("operands", "group", "obj", "touching")

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
    # SENSOR 8's SECOND OPERAND, resolved PER SLOT by the caller. `_extract` wrapped the
    # one-place sensors eight times and nothing wrapped a two-place one: an atom receives one
    # value and a `Ctx`, so the second operand has to arrive here or not at all.
    #
    # **BEFORE-STATE, AND THAT IS THE TEST RATHER THAN AN EXCEPTION.** The tautology guard is
    # satisfied by what `Ctx` does NOT contain -- *a term that reads the after-state compresses
    # perfectly and predicts nothing*, and there is no guard because the capability is absent.
    # `contacts()` is frame-cached and invalidated on `step`, so it is read before the action
    # and cannot reach the outcome. **Any future field must pass that same test**; a plausible
    # one that does not would delete the guard silently, which is the recorded hazard.
    #
    # `action` IS DELIBERATELY LEFT `Any`. `ARC_AGENT` §22 records a run -- *5 bare + 9
    # positioned on a 3x3 board: binds, three steps run* -- and positioned actions pass through
    # BECAUSE it is untyped. Typing it would delete a measured capability.
    # `None` MEANS UNKNOWN AND `()` MEANS KNOWN-EMPTY, which are different claims. Contact
    # is computed from cells and the loop's state carries none, so on a REPLAY of history
    # there is no way to know what touched what -- and returning `()` there would file *I
    # cannot see* as *nothing was touching*. The atom abstains on `None`.
    touching: tuple[str, ...] | None = None
    # THE OUTER STREAM. The values THIS attribute takes on every OTHER object, so a term can
    # quantify instead of comparing to one bound operand. Resolved per slot by the caller,
    # exactly as `touching` is, and ABSENT FROM THE HANDLE -- which is what makes it survive
    # the membrane: a binding is dropped on export, a population read is vocabulary.
    #
    # VALUES, NEVER SLOT NAMES. A name is an instance and would not mean anything on the next
    # board; the values are what a quantifier ranges over.
    group: tuple = ()
    # THE SLOT'S OWNER'S RECORD, REASSEMBLED FROM THE STATE. Not stored anywhere: the
    # flattening scattered an object into `owner.attr` keys and never destroyed the values,
    # so the record the OBJECT-typed atoms need is recoverable from the same `dict[str, int]`
    # the loop already holds -- live at the bet, historical on replay, one assembler both.
    obj: dict | None = None
    # THE SHAPE DECODER -- `{published id: the normalised offset frozenset}`. The published slot
    # carries an episode-local integer and every SHAPE atom guards on a frozenset, so seven atoms
    # read NOT_RESOLVED on every call (F242, measured 0 of 40). `arc_world.shapes()` computes this
    # inverse and had no callers.
    #
    # IT PASSES THE FIELD TEST ABOVE, WHICH IS WHY IT MAY BE HERE: it is a DECODER, not state.
    # Knowing that id 3 stands for a particular cell pattern says nothing about what the action
    # will do -- there is no outcome in it, so the tautology guard is untouched.
    shapes: dict | None = None


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
    # MORE THAN ONE INPUT TYPE, because `ATTR` was one name over two quantities. §11.2 names
    # `ATTR x ATTR -> PRED` as a composition SPACE and §12.3 names the TYPES in it -- COLOUR,
    # POSITION, EXTENT, SHAPE -- and reading the space's name as a type is what let `above`
    # apply to a colour. Equality holds on all of them; order holds only on some. An atom
    # therefore accepts a SET, and duplicating atoms per type was the alternative: `units()`
    # dedups on name, so that would have put the type into the term's identity and its handle.
    also_accepts: tuple[str, ...] = ()
    # WHICH `Ctx` FIELDS THIS ATOM READS -- DECLARED AT CONSTRUCTION, NEVER INFERRED, which is
    # `reads_operand`'s rule and for `reads_operand`'s reason.
    #
    # **THE FIELD-COUNT ARGUMENT BROKE THE FIRST TIME A FIELD WAS ADDED.** `retrieval.key_of`
    # derived a term's invariance from *`Ctx` has two fields, so it cannot vary with a slot it
    # has no accessor for* -- and `touching`, `group` and `obj` were added, each an accessor to
    # other slots' values, so the claim went false without the argument moving. A declaration
    # survives the NEXT field too; a field count does not.
    reads_ctx: tuple[str, ...] = ()

    @property
    def accepts(self) -> tuple[str, ...]:
        return (self.in_type, *self.also_accepts)

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
    # §4: THE OPERAND MAY BE COMPUTED, WHICH IS WHAT MAKES THIS A TREE. `operand` names the
    # slot; this transforms that slot's value before it fills operand 0. A chain has no
    # branch and still has none -- what it gains is a SECOND chain feeding its one operand,
    # so `f<g(s)>` joins two computed values where `f<s>` could only join a computation with
    # a reading. That was the whole of §4's absence and G1's other face.
    #
    # BESIDE `operand` RATHER THAN WIDENING IT, deliberately: ten sites read `.operand` and
    # every one still gets a slot name. The census said only `_ops` is the mechanism, and
    # only `_ops` changes.
    operand_term: Term | None = None

    @property
    def name(self) -> str:
        base = " . ".join(a.name for a in self.atoms)
        if self.operand:
            inner = (f"{self.operand_term.name}({self.operand})"
                     if self.operand_term is not None else self.operand)
            base = f"{base}<{inner}>"
        return f"{base}?{self.guard}" if self.guard else base

    @property
    def accepts(self) -> tuple[str, ...]:
        return self.atoms[0].accepts

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
        # THE SUBTREE COUNTS, because `term_bits(len(t))` is what prices it and a tree that
        # priced only its trunk would buy its operand branch for nothing.
        return len(self.atoms) + (len(self.operand_term) if self.operand_term else 0)

    def __repr__(self) -> str:
        return f"Term({self.name})"

    def apply(self, value: Any, ctx: Ctx) -> Any:
        """IDENTITY WHEN THE GUARD FAILS, which is the whole conditional. `When(P, R)` with
        `idn` as the else-branch -- the only two-branch form a left-to-right chain admits."""
        if self.guard is not None and ctx.action != self.guard:
            return value
        for a in self.atoms:
            # ELEMENTWISE WHEN THE CHAIN IS MID-ITERATION -- §12.2.1. An atom typed `CELL` sees
            # ONE cell and is mapped across the collection; an atom typed `CELLS` consumes the
            # whole thing and closes the iteration. The chain's own POSITION is the body, which
            # is why this needs no operand channel and no `Ctx` field: the term's entire meaning
            # stays in its atom sequence, and `units()` rebuilds a promoted chunk from exactly
            # that. A `fold<body>` failed the census here -- two bodies, one atom sequence, one
            # unit, executing as each other.
            #
            # A NON-READING INSIDE THE COLLECTION KILLS THE WHOLE COLLECTION, for §12.2's reason
            # one level down: a cell the instrument could not read must not silently shrink the
            # set, because a shorter collection is a different reading rather than a missing one.
            # ANY non-reducer maps, not only `CELL`-typed atoms. The first version mapped only
            # `in_type == CELL`, so `cells . cell_row . parity` died: after `cell_row` the
            # collection holds POSITIONs and `parity` is `POSITION -> BOOL`, which was handed
            # the whole collection and abstained. **The consequence is the point of the whole
            # construct -- with this rule EVERY EXISTING ATOM becomes usable inside an
            # iteration**, so the agent composes over the 57 it already has rather than over
            # four new ones. A `CELLS`-typed atom is the only thing that closes.
            if isinstance(value, Cells) and a.in_type != CELLS:
                out = []
                for cell in value:
                    got = a.fn(cell, ctx)
                    if got is NOT_RESOLVED:
                        return NOT_RESOLVED
                    out.append(got)
                value = Cells(tuple(out))
                continue
            value = a.fn(value, ctx)
            # §12.2's non-reading PROPAGATES: *it lets "this instrument cannot see it" go up
            # instead of becoming a wrong attribute.* Short-circuiting is the whole of it --
            # feeding NOT_RESOLVED to the next atom is how a non-reading becomes a value.
            if value is NOT_RESOLVED:
                return NOT_RESOLVED
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
        # item 7: what the agent invented, and the abstention that licensed each
        self.invented: dict[str, dict] = {}
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

    def invent(self, name: str, fn, in_type: str, out_type: str, licence: dict) -> bool:
        """ITEM 7. **THE REGISTRY WAS FIXED AT CONSTRUCTION AND THIS IS THE ONLY THING THAT
        OPENS IT.** `self.atoms` and `self._by_name` were built once and nothing appended.

        **LICENSED BY THE LADDER, NEVER BY USEFULNESS.** `CLAUDE.md`: *`composition -> atom ->
        sensor`, and every step is licensed by the same thing: THE LEVEL BELOW TRIED AND COULD
        NOT.* So `licence` must carry the agent's OWN abstention record -- a `verdict` of
        `budget_spent`, `depth_exhausted` or `under_floor`, with the closure it searched. **An
        invention with no recorded failure beneath it is refused**, because without one it is
        the library being made more complete, which steals the discovery.

        **NO HEAD START.** It enters with an ordinary `Standing` and earns its place like any
        term. **The name is arbitrary and meaningless** -- the identity is the recorded delta
        it was formed from, so a name that described it would be the seat naming the agent's
        concept for it.

        Returns False if the name is taken: re-inventing is not invention, and silently
        replacing a live atom would change what every existing term means.
        """
        if name in self._by_name:
            return False
        if licence.get("verdict") not in ("budget_spent", "depth_exhausted", "under_floor"):
            raise ValueError(
                f"invent({name!r}) needs the agent's own abstention record -- a verdict of "
                f"budget_spent, depth_exhausted or under_floor. Got {licence.get('verdict')!r}. "
                f"The level below must have TRIED AND FAILED; usefulness is not a licence.")
        a = Atom(name, fn, in_type, out_type)
        self.atoms.append(a)
        self._by_name[name] = a
        self.invented[name] = dict(licence)
        return True

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
        # ROUTE 2 -- reviewer, 2026-09-23. **THE RECORDED DELTA AND ITS LICENCE, NEVER THE
        # FUNCTION.** `invent` made the registry run-local, which broke this file's standing
        # assumption that atoms are "identical on both sides" -- so a term built on an invented
        # atom was refused on load and invention could not transfer at all (`F307`).
        #
        # WRITING THE DEFINITION IS STILL REFUSED, and the docstring's reason still holds: it
        # would make this file a second producer of the vocabulary. **What is written is the
        # OBSERVATION the agent recorded and the abstention that licensed it** -- data, not a
        # function -- and `load` RE-INVENTS from it, through the same `invent` gate, so the
        # licence is re-checked on the way in rather than trusted from the file.
        blob = {"terms": out,
                "invented": {n: rec for n, rec in self.invented.items() if rec.get("delta")}}
        pathlib.Path(path).write_text(json.dumps(blob, indent=1), encoding="utf-8")
        return {"written": len(out), "invented": len(blob["invented"]), "path": path}

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
        blob = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
        # BACKWARD-COMPATIBLE BY SHAPE, not by a version flag: files written before route 2 are
        # a bare list. A flag would be a second thing to keep in step with the format.
        rows = blob if isinstance(blob, list) else blob.get("terms", [])
        took, refused = [], []
        # RE-INVENT FIRST, so a term naming an invented atom can resolve below. Each goes back
        # through `invent`, so **the licence is re-checked on the way in rather than trusted
        # from the file** -- a file claiming an invention without an abstention behind it is
        # refused exactly as a live one would be.
        reinvented = []
        for nm, rec in (blob.get("invented") or {} if isinstance(blob, dict) else {}).items():
            delta = rec.get("delta") or {}
            if not delta or nm in self._by_name:
                continue

            try:
                if self.invent(nm, _replay_delta(dict(delta)), "val", "val", rec):
                    reinvented.append(nm)
            except ValueError:
                refused.append({"atoms": [nm], "why": "invention without a licence in the file"})
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
        # `reinvented` IS REPORTED, because a silent count is how an invented atom
        # crossing a game boundary would be invisible -- and that crossing is the claim.
        return {"loaded": sum(1 for x in took if not x["already_held"]),
                "reinvented": len(reinvented),
                "already_held": sum(1 for x in took if x["already_held"]),
                "refused": refused,
                "reads": ("composition crosses, binding does not. A refused row is an "
                          "INCOMPATIBLE registry, not a small library")}

    # P5's single-slot memo: (the units tuple, the frozenset of its atom sequences).
    _UNIT_SET: tuple = ((), frozenset())

    @staticmethod
    def length(t: Term, units: tuple = ()) -> int:
        """How many units the term costs to say. **`routine.length`'s rule, for terms.**

        THE ASYMMETRY THIS CLOSES WAS MEASURED, NOT REASONED. `routine.length(r, chunks)`
        counts a settled routine as ONE -- *only what the ground has paid for becomes a
        shortcut* -- and the term side priced raw atoms, so `mint` and `_install_reuse`
        charged the DERIVATION price for something already derived. The rule was stated once
        and implemented on one of the two spaces it governs.

        **THE KEY IS THE ATOM SEQUENCE**, which is `units()`'s own rule one method down: *the
        chunk IS the atom sequence and the operand has no business in the key*, because the
        binding is re-decided per slot at mint.

        `units` DEFAULTS TO EMPTY, so `length(t)` is the raw atom count and every caller that
        has no settled set to offer keeps exactly the price it had.
        """
        # P5: THE SCAN ANSWERED `False` 110.7M TIMES BY WALKING A LIST. `any(t.atoms ==
        # u.atoms for u in units)` ran the whole unit set per candidate -- 19% of wall on a
        # nine-cycle ls20 run, and `units` is HOISTED per mint, so it is the same object for
        # every one of them.
        #
        # EXACTLY EQUIVALENT, and `Atom` is what makes it so: `@dataclass(frozen=True)`
        # generates `__eq__` and `__hash__` from the same fields, so set membership and the
        # `==` scan cannot disagree. Checked at the declaration, not assumed from hashability.
        #
        # ONE SLOT, NEVER A DICT -- `units` is a fresh tuple per mint, so an id-keyed map
        # would grow without bound. The recursion below passes the same object, so it hits.
        if units:
            cached = Gamma._UNIT_SET
            if cached[0] is not units:
                cached = (units, frozenset(u.atoms for u in units))
                Gamma._UNIT_SET = cached
            if t.atoms in cached[1]:
                return 1
        n = len(t.atoms)
        if t.operand_term is not None:
            n += Gamma.length(t.operand_term, units)
        return n

    def units(self) -> list[Term]:
        """What the search composes FROM: the atoms, plus every SETTLED term as one unit.

        The closure does not change -- MINT still cannot add an atom. What changes is what
        is reachable at a given budget: a settled 3-atom term makes depth 3 reach 9 atoms.
        Only what the ground has paid for becomes a shortcut.
        """
        # DEDUP ON WHAT IS EMITTED, not on what was settled. `t.name` carries the
        # operand binding and the emitted unit does not, so two settled terms differing
        # only in their binding both passed the check and both went in -- one unit
        # counted twice, inflating the space count and with it the `coverage`
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
            stats["estimate"] = self.space_exact(units, in_type, out_type, max_depth)
            stats["seen"] = 0
        start = [u for u in units if in_type in u.accepts]
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
                            if chain[-1].out_type in u.accepts
                            and not any(a.name == IDN_NAME for a in (*chain, *u.atoms))]
            if spent:
                break
            frontier, depth = nxt, depth + 1
        if stats is not None:
            stats["seen"] = emitted
            stats["budget_spent"] = spent
            stats["depth_exhausted"] = not spent

    @staticmethod
    def space_exact(units: list[Term], in_type: str, out_type: str, max_depth: int) -> int:
        """How many terms the closure WOULD emit with no budget. Not an estimate.

        §19.1 asks for `candidates_seen / estimate` and offers `~ lambda^d` because lambda was
        already computed. **`lambda^d` is the asymptotic form of this count**, and three things
        it cannot see are decided per call: the closure starts only at `in_type`, yields only
        at `out_type`, and refuses `idn` inside a chain. Same quantity, counted rather than
        approximated -- and it is CHECKABLE, which an estimate is not: enumerate with an
        unbounded budget and the two numbers must agree exactly.

        **AND IT IS COUNTED OVER `units`, WHICH IS WHY §23.5's MECHANISM CAN APPEAR AT ALL.**
        *More atoms means a larger lambda, so lambda^d grows and a fixed budget covers a
        smaller fraction.* `lambda` is the spectral radius of the ATOM table and never moves
        when a term settles, so under it a loaded library would show no fall in coverage
        whatever happened. `units` grows as the ground pays for chunks.
        """
        free = [u for u in units if not any(a.name == IDN_NAME for a in u.atoms)]
        total = sum(1 for u in units if in_type in u.accepts and u.out_type == out_type)
        # length 1 counts every unit; length > 1 only the idn-free ones, both as the head of
        # the chain and as each extension -- the closure's rule, not a separate policy
        live: dict[str, int] = {}
        for u in free:
            if in_type in u.accepts:
                live[u.out_type] = live.get(u.out_type, 0) + 1
        for _ in range(2, max_depth + 1):
            nxt: dict[str, int] = {}
            for t, n in live.items():
                for u in free:
                    if t in u.accepts:
                        nxt[u.out_type] = nxt.get(u.out_type, 0) + n
            live = nxt
            total += live.get(out_type, 0)
        return total

    # -- typing beats size, as a number -----------------------------------------------

    def type_report(self, iters: int = 400) -> dict[str, float]:
        """lambda = spectral radius of the type transfer matrix. SHIFTED, and that is the fix.

        Well-typed terms of size n grow as lambda^n; an untyped bag of V symbols grows as
        V^n. The ratio is what typing buys per unit of depth.

        **PLAIN POWER ITERATION DOES NOT CONVERGE ON A PERIODIC MATRIX, AND A TYPE GRAPH IS
        PERIODIC WHENEVER IT HAS A CYCLE.** The shift below is the general fix and it stays.

        **BUT THE CYCLE THIS DOCSTRING USED TO MEASURE ON DOES NOT EXIST, AND `4222e32` IS WHY.**
        It read the graph as a 3-cycle `OBJ -> ATTR -> PRED -> OBJ` and gave the true radius as
        `3.5569 = (5*3*3)^(1/3)`, calling the iteration's `3.0000` the bug. That arithmetic
        closes the cycle by treating `OBJECT` and `OBJ` as one node -- **the exact conflation
        `4222e32` split apart**, `OBJECT` being a thing on the board and `OBJ` a complete
        objective. Post-split the graph is `OBJECT -> ATTR -> PRED -> OBJ`, a path that
        terminates, plus the `val` self-loop. **So 3.0 is the true spectral radius and the
        number this docstring named as the defect is the correct one.** A repair one layer up
        falsifying the reading below, and the reading was left asserting the old world.

        **THE SHIFT IS EXACT, NOT AN APPROXIMATION.** For a NON-NEGATIVE matrix -- and a
        transfer matrix is counts -- Perron-Frobenius gives a real dominant root `r` with
        `r >= |lambda_i|` for every eigenvalue, so `rho(M + cI) = r + c`. Adding `c` to the
        diagonal gives every node a self-loop, which makes the matrix APERIODIC and the
        iterate converge; subtracting `c` afterwards recovers `r`.

        **AND THE NORM CHANGED WITH IT.** The old code took the max-norm of the iterate as
        the eigenvalue; the growth ratio is what converges, so `v` is normalised to sum 1 and
        `lambda` is the L1 mass of `Mv`.
        """
        types = sorted({t for a in self.atoms for t in a.accepts}
                      | {a.out_type for a in self.atoms})
        idx = {t: i for i, t in enumerate(types)}
        n = len(types)
        m = [[0.0] * n for _ in range(n)]
        for a in self.atoms:
            for t in a.accepts:
                m[idx[t]][idx[a.out_type]] += 1.0
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
