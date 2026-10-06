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
from dataclasses import dataclass, field
from typing import Any

from sensors import CELL, CELLS, NOT_RESOLVED, Cells

sys.dont_write_bytecode = True

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
# THE FIFTH, AND ITS WIPE SEMANTICS ARE DELIBERATELY UNDECIDED -- 2026-09-26.
#
# Isaiah's THIRD clause, 2026-09-08: an atom may be handed when the agent's own machinery
# perceived and named the gap, when no in-run derivation is plausible, and when a human
# competitor would arrive already holding it. It is NOT §11's clause one -- the loop runs
# without any individual one of these -- and filing it as `NECESSARY` put twenty-eight atoms
# in the ablation's BLIND category that the domain's own table says were HANDED.
#
# **WHAT THE WIPE DOES WITH THIS VALUE IS NOT DECIDED HERE, AND THE SILENCE IS THE POINT.**
# The comment above already rules that *what each value IMPLIES for the wipe is a separate and
# deferred decision*; a fifth value arriving without saying so would answer that question by
# omission, which is the thing it was added to prevent. RECORDING is owed now because the
# clause is unrecoverable later. DECIDING is Isaiah's and the reviewer's, at 25/25.
#
# AND THE FINER SPLIT IS NOT COLLAPSED INTO THIS BUCKET. `arc_atoms.ADMITTED` distinguishes the
# atoms the machinery named (`unexpressible()`, §12.4) from the ones a measurement a seat ran
# named (`ON DEPTH`), and `CLAUDE.md` says the ablation must tell those apart. That lives in the
# table's prose, which is now enforced to exist. Deriving a second bucket by matching on the
# substring `ON DEPTH` would be logic where a table belongs.
HANDED = "handed"

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
# **A SEED, NOT A SETTING.** `Gamma.halflife` starts `None` and the agent writes it from its own
# books the moment it has any. Until then this is what decays a refutation -- and it is marked
# as unearned in the `books` row rather than passing silently as a decision.

# anchor: SPECIFIED, NOT GROUNDED, and seeded at its own NO-OP.
# **HOW MUCH ACCUMULATED, DECAYED WRONGNESS UNSETTLES A TERM -- Isaiah, 2026-09-24:**
# *"Definitely not a hard ban. In original Ouroboros things had DECAYS AND RATIOS
# instead of hard limits, for flexibility and scale."*
# **THE SHAPE IS RULED AND THE NUMBER IS NOT OURS**, so this is a SEED in
# exactly `REJECTION_HALFLIFE`'s sense and is marked as one wherever it is read.
#
# **1.0 IS THE VALUE THAT MAKES THIS CHANGE BEHAVIOUR-NEUTRAL ON ENTRY, AND THAT IS WHY IT IS
# HERE.** `refute` adds exactly `1.0`, so at a ceiling of `1.0` the first miss still unsettles --
# **byte-identical to the cliff it replaces.** What changes is that the ceiling now EXISTS and is
# a number someone can move; what does not change is any run. **A mechanism installed at its own
# no-op point cannot be accused of smuggling a policy in with it.**
# **AND IT IS THE AGENT'S CALL, NOT OURS AND NOT ISAIAH'S -- HIS RULING, 2026-09-30:** *"I
# leave this up to the agent -- but that means they should become able to bring it back, or
# dig at the bottom for older ones and reconsider them (agency)."* So this constant is not a
# number waiting for him to choose; it is the floor that stands UNTIL THE AGENT CAN WEIGH IT,
# which needs intent-level prediction it does not yet have.
#
# **WHAT THE (c) SPLIT BUYS IS THAT THE AGENT'S CHOICE IS SAFE WHEN IT MAKES ONE.** The
# ceiling reads `refusals` rather than the blend, so raising it can no longer demote a term
# for mistakes made while it was on trial. At 1.0 the two were indistinguishable -- one
# refusal adds exactly the ceiling -- so nothing moved on the day it was installed and the
# guard was in place for when something did.
#
# **AND SOMETHING DID, THE SAME DAY: the ceiling is 2.0 below, so the two ARE now
# distinguishable and the guard is load-bearing rather than latent.** The sentence above is
# left in the past tense rather than deleted -- it records why a mechanism was installed at
# its own no-op point, which is the reason it could be trusted when it started to bite.
# **INTERIM, AND IT IS STILL THE AGENT'S CALL -- Isaiah, 2026-09-30, twice.** He ruled the
# threshold the agent's, and then ruled this SOFTER INTERIM when 1.0 turned out to mean ONE
# REFUSAL UNSETTLES: `refusals` increments by exactly 1.0, so a ceiling of 1.0 is met by a
# single miss. This stands only until the agent can weigh it.
#
# **2.0 IS THE RULE READ MINIMALLY, NOT A NUMBER I PREFER.** *One failure is not a verdict*
# sets a floor above 1.0 and says nothing more; 2.0 is the smallest value satisfying it, and
# anything larger would assert that TWO failures are not a verdict either -- a claim the
# ruling does not make. Chosen from the rule and then measured, never tuned to a green.
#
# WHAT IT TAKES IN PRACTICE, computed against `decay`'s `0.5 ** (gap / 8.0)`:
#
#     two refusals, same tick      2.000   unsettles
#     two, one tick apart          1.917   survives
#     three, one tick apart        2.758   unsettles
#     three, four ticks apart      2.207   unsettles
#     FIVE, EIGHT TICKS APART      1.938   SURVIVES
#
# **AND THAT LAST ROW IS A PROPERTY OF THE VALUE, NOT AN ACCIDENT, SO IT IS STATED RATHER
# THAN DESIGNED AROUND.** Refusals spaced at the halflife are a geometric series whose LIMIT
# IS EXACTLY 2.0, approached from below -- so a term refused once every eight ticks FOREVER
# is never unsettled at this ceiling. The ruling asks that one failure not convict; it does
# not say a slow drip eventually must. If that is wanted, the ceiling is not the dial --
# a decaying counter cannot express "persistent but rare", and saying so is the finding.
REJECTION_CEILING = 2.0



def accepts_type(unit: Any, ty: str | None) -> bool:
    """**THE ONE PREDICATE.** Both the BINDING rule (`tether._head_accepts`) and the SEARCH rule
    (`enumerate_closure`) call this, so they cannot disagree again. They each implemented the
    question separately and answered it differently for a whole class of atoms.

    An untyped slot is not a mismatch; a declared-polymorphic unit takes anything.
    """
    if ty is None:
        return True
    if getattr(unit, "polymorphic", False):
        return True
    return ty in unit.accepts


# **THE RELATIVE GUARD, A SENTINEL AND NEVER A NAME -- the reviewer, 2026-10-01.** A guard
# naming an OBJECT could not transfer: `o0` means nothing on the next board. This names the
# RELATION between the slot being explained and the object the press LANDED ON.
#
# **AND *LANDED ON* IS THE SECOND VERSION. The first read the INTENT'S SUBJECT -- what the agent
# AIMED AT -- and `a561fb2` was reverted for it:** on a wired world the agent aims at `o0.colour`
# and the interface clicks `o1` to get it, so the guard was TRUE on 48 of 60 steps where `o0` was
# never touched. It validated clean only on `click_only`, where aim and landing coincide.
ACTED_SELF = "ACTED_SELF"
# **THE GENERAL FORM -- the reviewer, 2026-10-04, and it SUBSUMES `ACTED_SELF`.** *"When the
# press lands on x"*, where x is the term's OWN referent rather than the computation's
# operand. `ACTED_SELF` was `?ACTED_ON<the slot's own owner>` all along and is now priced as
# one choice among the referents, with no cheaper special case.
#
# **WHY IT HAD TO BE DECOUPLED:** `binds = operand_binds if cand.reads_operand else [None]`,
# and `inc.reads_operand` is False -- so `inc`, the one computation that IS the rule on a
# wired slot, could never carry a pointer for the guard to test. The operand slot was doubly
# booked: the term's computational input AND the only place a guard could name a cause.
ACTED_ON = "ACTED_ON"


@dataclass(frozen=True)
class Ctx:
    """What an atom may read. All before-state: there is no accessor to the outcome, so a
    term that predicts by peeking is not constructible."""

    action: Any = None
    # **THE INTENT, AND IT IS A SEPARATE FIELD -- ISAIAH, 2026-09-29 (ruling 1): a separate
    # intent field, NOT an intent in `Ctx.action`.** Two quantities never share a field here:
    # `action` stays the button and gains no second sense, which is the `A6i` this avoids.
    #
    # **IT PASSES THIS CLASS'S OWN BEFORE-STATE TEST**, which the docstring above requires of
    # any new field: an intent is formed BEFORE the action is realised, so it cannot smuggle
    # the outcome in. A term guarded on an intent still cannot peek.
    intent: Any = None
    # **RESOLVED PER SLOT BY THE CALLER, as sensor 8's second operand is, and for the same
    # reason: `apply` gets a value and a `Ctx` and NEVER THE SLOT**, so it cannot ask whether
    # the object acted on was this slot's. The caller can, and resolving it there is what keeps
    # the object's NAME out of the term entirely.
    #
    # **IT PASSES THE BEFORE-STATE TEST.** It is derived from the coordinate the press was
    # realised at, read against the BEFORE state -- so it says what the press LANDED ON, not
    # what the press DID. A term guarded on it still cannot peek at the outcome.
    acted_self: bool = False
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
    # **POLYMORPHISM DECLARED, NEVER INFERRED FROM A SPELLING.** `val` was a type NAME doing a
    # polymorphism's job, and two call sites read the same name two ways: `tether`'s
    # `_head_accepts` treated `val` as ACCEPTS-ANYTHING, `enumerate_closure` treated it as a
    # literal that must match exactly. The binder admitted `owner` on every slot; the search
    # never offered it, so `POSITION -> OBJECT` was 0 and the 18 OBJECT-typed atoms sat
    # unreachable. Same fault as `SHAPE` over two representations, one level up: in the type
    # system's own vocabulary. An atom that genuinely takes anything now SAYS SO.
    polymorphic: bool = False
    # WHAT THE ELEMENTS MUST BE, for a reducer that consumes a whole collection. `count_true`
    # REFUSES a non-boolean `Cells` at runtime -- *a reading or an explicit non-reading, never
    # a guess* -- and that refusal was invisible to the composer, which offered 70 chains
    # ending `. count_true` over collections of coordinates. **Every one of them is guaranteed
    # to abstain**, and they spend real enumeration budget doing it.
    #
    # DECLARED, LIKE EVERY OTHER TYPE FACT HERE, and for the reason two fields up: a runtime
    # refusal the type system cannot see is a guard that is CAUGHT rather than one that cannot
    # be BUILT. `None` means the reducer does not care.
    elem_type: str | None = None
    # WHICH CLAUSE LET THIS ATOM IN -- carried on the atom so it reaches `_install`, which is
    # the only place the ablation's partition is written. `None` means the constructor did not
    # say, and `_install` reads that as `NECESSARY`: the historic behaviour, unchanged for
    # every world that does not supply one.
    #
    # ON THE FIELD RATHER THAN A CONSTRUCTOR ARGUMENT, and `sensors.Sensor` is the precedent --
    # it carries `admitted` with NO DEFAULT so it cannot be forgotten. The default here is the
    # one concession: fifteen construction sites across five worlds, and a required field would
    # make every toy fixture declare a clause it has no opinion about.
    #
    # THE ALTERNATIVE WAS `Gamma(atoms, clauses=...)` AND IT IS WORSE: the mapping would have
    # to be threaded through `env.atoms()` at every site, and a world that forgot would report
    # a clean `necessary` -- a wrong partition presenting as a default, which is the exact
    # failure this field exists to close.
    admitted: str | None = None

    @property
    def accepts(self) -> tuple[str, ...]:
        return (self.in_type, *self.also_accepts)

    def __repr__(self) -> str:
        return f"Atom({self.name})"

    def __hash__(self) -> int:
        # CACHED, SAME VALUE as the generated one -- the field tuple in declaration order -- so
        # set iteration order cannot move. Every Term hash walks its atoms; see Term.__hash__.
        h = self.__dict__.get("_hash")
        if h is None:
            h = hash((self.name, self.fn, self.in_type, self.out_type, self.reads_operand,
                      self.operand_type, self.also_accepts, self.reads_ctx, self.polymorphic,
                      self.elem_type, self.admitted))
            object.__setattr__(self, "_hash", h)
        return h


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
    # **THE GUARD'S OWN REFERENT -- which object the press must land on.** Carried like
    # `operand`: a per-board binding that is RE-RESOLVED on a new board, never a name the
    # chain owns. Isaiah's 2026-09-29 ruling stands -- the guard names a RELATION and the
    # binding is resolved per board, so nothing above the seam names a button.
    guard_ref: str | None = None
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

    def __hash__(self) -> int:
        # CACHED, SAME VALUE: the generated hash re-walked every nested field on every call --
        # 30M calls in three late `default` steps (the 2026-10-05 runtime profile), mostly the
        # `_cannot_pay` tally lookup. This is the generated formula itself, so order holds.
        h = self.__dict__.get("_hash")
        if h is None:
            h = hash((self.atoms, self.origin, self.operand, self.guard, self.guard_ref,
                      self.operand_term))
            object.__setattr__(self, "_hash", h)
        return h

    @property
    def name(self) -> str:
        base = " . ".join(a.name for a in self.atoms)
        if self.operand:
            inner = (f"{self.operand_term.name}({self.operand})"
                     if self.operand_term is not None else self.operand)
            base = f"{base}<{inner}>"
        if not self.guard:
            return base
        # **THE REFERENT IS PART OF THE IDENTITY.** Two guards of the same KIND pointing at
        # DIFFERENT objects are different claims, and `name` is what the library keys on --
        # without this they would collide on one entry and the second would be refused as
        # already present, which is the quiet failure rather than the loud one.
        return (f"{base}?{self.guard}<{self.guard_ref}>" if self.guard_ref
                else f"{base}?{self.guard}")

    @property
    def accepts(self) -> tuple[str, ...]:
        return self.atoms[0].accepts

    @property
    def polymorphic(self) -> bool:
        return self.atoms[0].polymorphic

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
        # **THE GUARD NAMES AN INTENT, NOT A BUTTON -- ISAIAH, 2026-09-29 (ruling 1).**
        # This read `ctx.action != self.guard`, which made a guard a claim about which BUTTON
        # was pressed. Above the seam the agent names no buttons, so such a guard could only
        # ever be learned by the interface leaking upward.
        # **THE RELATIVE GUARD IS TESTED AGAINST A RESOLVED BOOLEAN, NEVER A NAME.** Every
        # other guard is an intent KIND compared by equality; `ACTED_SELF`'s truth depends on
        # WHICH SLOT is being explained, so the caller resolves it and this reads the answer.
        if self.guard == ACTED_SELF:
            if not ctx.acted_self:
                return value
        elif self.guard is not None and ctx.intent != self.guard:
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
    # WHERE THE FAILURES WERE TAKEN. Isaiah, 2026-09-30: *"I wouldn't want the agent to throw
    # away a useful routine just because one board didn't have the mechanic."* Measured before
    # building: **NO refutation key in the system carries a board or level id** -- not
    # `_reject_key`, not `_gap_key`, and `rejections` was a bare float. So "failed" could not
    # be read as "failed THERE", and the distinction was being made by WHEN THINGS ARE
    # FORGOTTEN instead: routine refutations wiped at every boundary, term rejections never.
    #
    # **A RECORD, NOT A RULE.** How a failure taken elsewhere should be WEIGHED is Isaiah's and
    # is not decided here -- `rejections` is untouched and every run is unchanged. What this
    # buys is that the question becomes answerable at all, and the ablation cannot reconstruct
    # it afterwards, which is the same reason the admitting clause is stamped at entry.
    # **RULED, AND THE ANSWER IS *NOT YET* RATHER THAN *NEVER* -- ISAIAH, 2026-10-01.** The
    # question above was put to him: should a failure taken elsewhere be weighed differently
    # here? **KEEP COUNTING THEM THE SAME FOR NOW**, and the reason is a property of where the
    # record is consumed rather than a judgement about failures:
    #
    #     `track_of` enters `retrieve`'s sort key in its OWN SLOT, AFTER fit. So a failure
    #     taken on another level can only move a term AMONG TERMS THAT FIT THE GAP EQUALLY
    #     WELL, and it can never exclude one. **That already satisfies *failing somewhere is
    #     not a verdict everywhere*** -- a nudge among equals is not a verdict.
    #
    # **SO THIS FIELD AND `paid` STAY RECORDED AND UNREAD, DELIBERATELY.** I proposed reading
    # them per-scope on 2026-10-01 and withdrew it: the comment below was right that the
    # weighting is Isaiah's, and his ruling is that no weighting is needed while the consumer
    # is a tie-break. **Revisit when RELEVANCE is built** -- 5.10.8's
    # `confidence x 0.5 ** (games_since_last_use / RELEVANCE_HALFLIFE_GAMES) + youth` -- because
    # that one is not a tie-break and the question becomes live again.
    where: dict = field(default_factory=dict)      # scope -> failures taken under it
    # WHERE IT PAID. The mirror of `where`. Isaiah ruled surfacing is by LIKELIHOOD OF
    # WORKING -- fit plus TRACK RECORD -- and a track record with only failures in it sorts
    # the most-tried term LAST. Measured before building: `Standing` held `settled_at` (ONE
    # tick, overwritten every settle), so there was no count of successes and no record of
    # where they happened.
    # **THE NUMERATOR SURFACING READS IS `confirmations`, NOT THIS -- corrected 2026-10-01.**
    # This line said `paid` was it. `confidence` (:933) and the youth bonus (:973) read the
    # TOTAL; `paid` is its per-scope breakdown and NO DECISION READS IT -- audited, the only
    # reads in the tree are `conform/stateful.py`'s property tests. Recorded like `where`.
    paid: dict = field(default_factory=dict)       # scope -> settlements earned under it
    # **WHICH SLOTS IT SETTLED ON -- kernel A5, the reviewer 2026-10-03.** `settled_at` is one
    # tick and `paid` is keyed by SCOPE (game:level), so nothing recorded WHICH SLOT paid, and
    # `is_settled(name)` could only answer "somewhere". **One settlement anywhere licensed
    # citation everywhere, and the state could not express otherwise.**
    #
    # A NEW FIELD RATHER THAN A REPURPOSED ONE, ruled: `admitted`, `origin` and `paid` stay
    # byte-identical so the ablation partition and the provenance record are untouched.
    settled_on: set = field(default_factory=set)   # slots this term settled on
    # **THE OTHER HALF OF A5 -- the reviewer, 2026-10-04.** A5 made SETTLEMENT per-slot
    # (`settled_on`) and left REFUTATION a scalar, so a term settled on `o0` and wrong on
    # `o1` lost its standing EVERYWHERE. Mirrors `settled_on` deliberately: the same shape,
    # one record, never a parallel store. `refusals` is kept and still totals across slots,
    # because the burial and decay readings are over the term and not over a slot.
    refusals_on: dict = field(default_factory=dict)   # slot -> post-settlement refusals
    # **THE (c) SPLIT -- ISAIAH, 2026-09-30: count misprediction-while-candidate SEPARATELY
    # from refusal-after-settling. Two quantities, two names.** `refute` is called on EVERY
    # mispredicting bound term, and the site's own comment says *a candidate that mispredicts
    # has not been refused; it has not yet proven itself*. Measured: 90.5-97.6% of all
    # increments across three gridworld seeds are on candidates.
    #
    # **A RECORD, NOT A RULE. `rejections` IS UNCHANGED AND STILL COUNTS BOTH**, so the
    # ceiling reads exactly what it read before and NO RUN MOVES. Refusals-after-settling are
    # `rejections - misses`. Whether the ceiling and the burial should read the narrower
    # quantity is a behaviour change and is not decided here.
    # **AND IT DECAYS ON THE SAME CLOCK, WHICH THE FIRST VERSION DID NOT.** Left as a raw
    # count it was not subtractable from a DECAYING total: measured immediately,
    # `rejections - misses` read -8.40 and -5.11 -- refusals cannot be negative. Two
    # quantities under one subtraction, measured differently, which is the denominator rule
    # at the level of a single row. It halves with `rejections` so the difference is a
    # refusal count and not an artefact of the two clocks.
    misses: float = 0.0                            # the candidate half, on the same clock
    # **AND THE REFUSAL HALF IS COUNTED, NOT DERIVED.** `rejections - misses` SHOULD cancel to
    # the refusal count and does not: measured, a term needed TWO post-settlement refusals to
    # cross a ceiling of 1.0 instead of one, because the two floats decay through different
    # arithmetic and leave error where an exact zero was assumed. Counting it directly makes
    # `misses + refusals == rejections` true by construction rather than by cancellation.
    refusals: float = 0.0                          # the settled half, on the same clock
    # **THE RISE. `Standing` IMPLEMENTED THE FADE AND NOT THE RISE** -- `LIBRARY_RETRIEVAL`
    # Sec 5.10.3: *settling ten times leaves exactly what settling once leaves, so a recipe
    # that is right in nine games and wrong in one carries a rejection and no credit, which
    # is precisely backwards.* This is the counterpart of `rejections`: the DECAYED TOTAL of
    # success, with `paid` as its per-scope breakdown exactly as `where` is `rejections`'.
    #
    # **THE SHAPE IS THE REVIEWER'S AND IT IS NOT A SECOND CONFIDENCE NUMBER** (2026-10-01):
    # one quantity with a total and a breakdown, which is the shape this class already has
    # on the failure side, written at ONE site in one statement block so they cannot disagree.
    confirmations: float = 0.0                     # the success total, on the same clock

    def refute(self, tick: int, halflife: float | None = None,
               ceiling: float | None = None, where: Any = None,
               slot: str | None = None) -> None:
        """**ISAIAH, 2026-09-24: NOT A HARD BAN. A DECAY OR A RATIO, NEVER A CLIFF.**

        This read `self.settled_at = None` -- **one miss and a standing was gone, unconditionally
        and with no decay involved**, which contradicted this class's own first line (*weighted,
        clocked, and never a hard ban*) and `F327` recorded the contradiction.

        **THE REPAIR IS THAT SETTLED-NESS NOW TURNS ON THE QUANTITY THAT ALREADY DECAYS.**
        `rejections` is accumulated wrongness with a half-life; a term keeps its standing while
        that total stays under the ceiling, and **evidence can therefore overturn a miss by
        outlasting it.** Nothing new is measured and nothing new is stored -- the cliff simply
        stops being a special case beside a decay that was already there.

        **THE NUMBER IS NOT MINE.** `REJECTION_CEILING` was 1.0 here, so the first miss
        unsettled; it is 2.0 since `fa3cba6` -- read the table at its definition.
        The mechanism is installed, visible and movable; the judgement of how much
        one failure should cost is Isaiah's, and `F341` files it as a judgement constant.
        """
        self.decay(tick, halflife)
        self.rejections += 1.0
        # STAMPED BESIDE THE TOTAL, NEVER INSTEAD OF IT. The scalar is what the ceiling reads
        # and it is unchanged; this only says where the weight came from.
        if where is not None:
            self.where[where] = self.where.get(where, 0) + 1
        # WHICH HALF THIS ONE IS. Read BEFORE the ceiling below can clear `settled_at`, or a
        # refusal would be filed as a miss on the very cycle it unsettles the term. PER SLOT
        # when one is given, as `is_settled` reads it: a miss where the term never settled is
        # a miss, not a refusal, however settled it is elsewhere (F465).
        held = (slot in self.settled_on) if slot is not None else self.settled
        if held:
            self.refusals += 1.0
        else:
            # IT WAS NEVER SETTLED, SO THIS IS NOT A REFUSAL. Counted beside the total, never
            # taken out of it -- see the field's own note.
            self.misses += 1.0
        # **THE CEILING READS REFUSALS, NOT THE BLEND -- ISAIAH'S (c), 2026-09-30.** It read
        # `rejections`, which counts BOTH, and `settle` does not reset it. Measured: five
        # candidate-era misses, then settle, then ONE post-settlement miss -> unsettled
        # immediately, because 5.24 was already over a ceiling of 1.0. **A term could be
        # unsettled by mistakes it made while on trial**, which is precisely what counting
        # them separately exists to prevent, so this is his ruling applied rather than a new
        # behaviour decision. `rejections` itself is untouched and still totals both.
        cap = REJECTION_CEILING if ceiling is None else ceiling
        if slot is None:
            # NO SLOT GIVEN -- the pre-A5 behaviour, kept for callers that genuinely mean
            # "anywhere" and named rather than inherited by accident.
            if self.refusals >= cap:
                self.settled_at = None
                self.settled_on.clear()
            return
        # PER SLOT, MIRRORING SETTLEMENT. A refusal here unsettles HERE; the term keeps its
        # standing on every other slot it earned, which is exactly what A5 did for settling.
        if held:
            self.refusals_on[slot] = self.refusals_on.get(slot, 0.0) + 1.0
        if self.refusals_on.get(slot, 0.0) >= cap:
            self.settled_on.discard(slot)
            # AND THE GLOBAL FLAG FOLLOWS THE SET RATHER THAN LEADING IT: with no slot left,
            # `is_settled(name)` with no slot must not still read True.
            if not self.settled_on:
                self.settled_at = None

    def decay(self, tick: int, halflife: float | None = None) -> None:
        """**THE SHAPE IS OURS; THE RATE IS THE AGENT'S.** Isaiah, 2026-09-24: the agent controls
        everything except the score, and *we give it the dial and the fact that a dial exists.*

        THAT A REFUTATION FADES is a fact about the substrate -- a hard ban would make one miss
        permanent and no evidence could ever overturn it. **HOW FAST it fades is a judgement
        about how long being wrong should count**, which is a claim, and Figure 10 is explicit:
        *the seat may author what has no truth value and nothing that does.*

        `REJECTION_HALFLIFE` REMAINS AS A SEED AND IS MARKED AS ONE. With no experience the
        agent has no basis, and **a seed that is replaced the moment evidence exists is the
        floor without the ceiling** -- not a default hiding the absence of a reading.
        """
        gap = max(0, tick - self.last_tick)
        if gap:
            _f = 0.5 ** (gap / (halflife or REJECTION_HALFLIFE))
            self.rejections *= _f
            # THE SAME FACTOR ON ALL THREE, so the two halves stay comparable with the total
            # and with each other. See `misses`.
            #
            # **THIS COMMENT SAID "ALL FOUR" FOR TWO HOURS AND BOTH EDITS WERE RIGHT WHEN
            # MADE.** `confirmations` joined the list and then left it. What decays here is
            # FAILURE ONLY, and the reason is that the two sides are not symmetric:
            #
            #     decaying `refusals`       FORGIVENESS -- a hard ban would make one miss
            #                               permanent and no evidence could overturn it
            #     decaying `confirmations`  AMNESIA -- it has no such rationale, and
            #                               `LIBRARY_RETRIEVAL` 5.10.8 forbids it in terms:
            #                               CONFIDENCE "never moves when NOT USED. Disuse is
            #                               not evidence." Isaiah: *decay may never touch
            #                               belief.*
            #
            # **MEASURED BEFORE THE REMOVAL: one settle then nothing but elapsed cycles took
            # confidence 0.667 -> 0.600 -> 0.556 -> 0.515 -> 0.501 -- a confirmed term
            # reverting to the untried prior by being left alone.**
            #
            # Disuse-fading is not abandoned, it is RELOCATED: 5.10.8 puts it in RELEVANCE,
            # `confidence x 0.5 ** (games_since_last_use / RELEVANCE_HALFLIFE_GAMES) + youth`,
            # on a clock of GAMES rather than cycles. That needs a games counter, which does
            # not exist yet, and it is the next item rather than a gap left here.
            self.misses *= _f
            self.refusals *= _f
            # THE PER-SLOT COUNT IS ON THE TERM'S CLOCK TOO. The live refute always passes a
            # slot, so `refusals_on` is what the ceiling reads; undecayed, two misses ever
            # made every later miss a cliff -- against Isaiah's 2026-09-24 ruling (F463).
            # An EVIDENCE TALLY behind settled-as-a-spectrum, NOT Fig 6's refusal: that is a
            # minted refusing TERM and never leaves the record. Nothing else reads this count.
            for _s in self.refusals_on:
                self.refusals_on[_s] *= _f
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
        # SET AT LOAD, never at mint: a term that originated elsewhere says so without the
        # reader having to parse a game name out of a handle.
        self.carried: dict[str, dict] = {}
        # **A MERGE THAT FORGETS ITS MEMBERS FAILS THE PROVENANCE CLAIM -- the reviewer,
        # 2026-10-03.** When N carried compositions reduce to ONE chain, that may be right
        # for TRANSFER -- one law, many instances -- but Isaiah's condition is that we can
        # prove where everything in the library came from. Surviving name -> the birth
        # handle of every instance absorbed into it.
        self.merged: dict[str, list[dict]] = {}
        self.stamps: dict[str, dict[str, Any]] = {}
        self.standing: dict[str, Standing] = {}
        # name -> the two verdicts that promoted it. A dict rather than a set because
        # `primitive requires both` is only checkable if both are on the record.
        self.primitives: dict[str, dict] = {}
        # item 7: what the agent invented, and the abstention that licensed each
        self.invented: dict[str, dict] = {}
        self.tick = 0
        # **THE AGENT'S DIAL.** `None` means it has not earned a value yet and the seed applies.
        # Written by `tether.Agent` from its own books; never set here, and never defaulted to
        # a number we picked at any point after construction.
        self.halflife: float | None = None
        # THE EVIDENCE BEHIND IT, carried across attempts by `save`/`load`. The agent appends;
        # the seat persists; the value is re-derived rather than restored.
        self.vindication: list[int] = []
        # AND THE REST OF THE BOOKS, for the same reason and with the same consequence. I fixed
        # `vindication` because I tripped over it and left its four siblings resetting every
        # attempt -- `I25`, repaired the instance and left the class, in the commit that
        # diagnosed the class.
        #
        # **COUNTS OF OBSERVED EVENTS CROSS DIRECTLY: they are evidence, not conclusions.** The
        # library already crosses games because Isaiah ruled transfer is the claim, and a book
        # about how THIS AGENT'S terms behave is no more game-local than the terms are.
        self.book: dict[str, int] = {}
        # 3d / Â§17.7. Set by the agent to a `(unit) -> tuple` ranking. None keeps the
        # registry order this had, so installing a rank is an observable change and not
        # installing one changes nothing.
        self.unit_rank = None
        for a in atoms:
            # THE ATOM'S OWN CLAUSE IF IT DECLARED ONE. A blanket `NECESSARY` was true of the
            # VOCABULARY and false of most of its members, and `admissions()` read
            # `{necessary: 62}` on a registry whose own table says 28 were handed.
            self._install(Term((a,), origin=PRIOR), seq=-1, residual=None,
                          admitted=a.admitted or NECESSARY)

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

    def settle(self, name: str, where: Any = None, slot: str | None = None) -> None:
        """The ground paid on evidence the term was never fitted to.

        `where` records WHERE it paid, the mirror of `refute`'s. Without it a track record has
        a denominator and no numerator, and ordering by it sorts the most-tried term last.

        **AND IT DECAYS BEFORE IT COUNTS, WHICH THIS DID NOT DO AND `refute` ALWAYS HAS.**
        Measured before building: `decay` had exactly two callers -- `refute`, and the
        `rejection_of` READ -- so the clock was driven by refutation and by reading, never by
        time. A `confirmations` incremented here without decaying first would never fade,
        while `rejections` faded on every refutation: not the same clock, not a clock at all.

        The extra decay is neutral on the failure fields because exponential decay composes
        -- 0.5^(a/h) x 0.5^(b/h) = 0.5^((a+b)/h) -- so the value at the next refutation, and
        therefore the ceiling test, is unchanged. `rejection_of` already decays mid-stream on
        a mere read, so this is the established pattern rather than a new one. **Asserted as
        a refuter with a mutation control, not taken on the arithmetic.**
        """
        st = self.standing.setdefault(name, Standing())
        st.decay(self.tick, self.halflife)
        st.settled_at = self.tick
        # THE TOTAL, UNCONDITIONAL -- and the breakdown BESIDE it, never instead of it. The
        # same two lines `refute` writes, in the same order, so the pair cannot drift apart.
        st.confirmations += 1.0
        if where is not None:
            st.paid[where] = st.paid.get(where, 0) + 1
        # THE SLOT, BESIDE THE SCOPE AND NEVER INSTEAD OF IT. `where` answers which BOARD
        # paid; this answers which SLOT did, and kernel A5 keys on the second.
        if slot is not None:
            st.settled_on.add(slot)

    def promote(self, name: str, shadow: dict, echo: dict) -> None:
        """PRIMITIVE. Settled is held-out payment on the slot the term was minted for,
        and that does not discriminate -- every wrong term in the false-mint read fired
        the held-out test and survived it. A primitive is the stronger thing: it closed a
        residual RECORDED BEFORE IT EXISTED, somewhere it was not minted for.

        Both verdicts or neither. Echo alone is apophenia -- a structure found and given
        somewhere to live. Shadow alone is a local hack called a primitive.

        **AND IT STAMPS THE CLAUSE, WHICH IT DID NOT UNTIL 2026-09-26.** `admissions()`
        documents `promoted` as one of its four buckets and NOTHING WROTE IT -- the bucket
        could not be non-zero, which is the exact defect that docstring records having just
        fixed for `unstated`: *a falsifier over a population that cannot contain the defect
        it looks for.* Repaired the instance, left the class, one bucket over.

        The clause is unrecoverable later (`PRIOR` marks every atom alike), and §11 partitions
        the ablation by it: `promoted` is WIPED, `necessary` is BLIND. So promotion moves a
        term from `accepted` -- earned, pre-boundary -- to `promoted`, the claim about having
        survived one.

        **`necessary` IS NOT OVERWRITTEN, and that is the arrival/conduct line.** An atom's
        clause is a fact about what the agent ARRIVED WITH; nothing it does later changes it.
        `_standing` exempts atoms one screen up for the same reason -- *the ground never owed
        anything for a primitive*.
        """
        self.primitives[name] = {"shadow": shadow, "echo": echo}
        st = self.stamps.get(name)
        if st is not None and st.get("admitted") != NECESSARY:
            st["admitted"] = PROMOTED

    def is_primitive(self, name: str) -> bool:
        return name in self.primitives


    def refute(self, name: str, where: Any = None, slot: str | None = None) -> bool:
        """A settled term mispredicted on fresh evidence. Demoted to candidate -- not
        deleted, and the rejection decays, so it can settle again if it starts paying.

        `where` is PASSED IN rather than read from `self.game`: Γ knows the game and not the
        level, and the failure this records is *one board did not have the mechanic*, which
        happens at both scales. The caller is the one holding both.
        """
        st = self.standing.setdefault(name, Standing())
        was = self.is_settled(name, slot)
        st.refute(self.tick, self.halflife, where=where, slot=slot)
        # TRUE ONLY WHEN THIS MISS COST STANDING, on the slot when one is given. This returned
        # `was settled (anywhere)`, so the caller unbound on every miss by a settled term --
        # a slot it never settled on included -- whether or not standing was lost (F462).
        return was and not self.is_settled(name, slot)

    def is_settled(self, name: str, slot: str | None = None) -> bool:
        """Settled -- ANYWHERE by default, HERE when a slot is given. Kernel A5.

        **ONE FUNCTION AND ONE ANSWER, ruled by the reviewer 2026-10-03 against the seat's
        proposal of a second differently-named predicate.** The seat's objection was that an
        optional parameter lets a caller get the other answer by forgetting; the ruling is
        that two names are two answers, which is the defect `4599`'s docstring was written
        about ("it was that there were TWO ANSWERS AT ALL"). **The forgetting risk is carried
        by the tests instead: a term settled on A must read NOT settled on B.**

        `slot=None` is the deliberate reading for `chunk_reuse` and `settled_terms`, where
        settled-ELSEWHERE is the whole concept and passing a slot would change what they mean.
        """
        st = self.standing.get(name)
        if st is None or not st.settled:
            return False
        return True if slot is None else slot in st.settled_on

    def rejection_of(self, name: str) -> float:
        st = self.standing.get(name)
        if st is None:
            return 0.0
        st.decay(self.tick, self.halflife)
        return st.rejections

    def track_of(self, name: str) -> float:
        """THE NET TRACK RECORD, DECAYED ON READ -- the mirror of `rejection_of`.

        Higher is better and the range is (0, 1). **`misses` IS DELIBERATELY ABSENT.** Isaiah's (c)
        split exists to separate mispredicting-while-candidate from breaking a settled
        promise; a term with many misses and no refusals has been TRIED OFTEN AND NEVER
        BETRAYED ONE. Counting those against it would score exploration as failure, which is
        the system working as designed read as the system failing.

        **THE FORM IS THE CORPUS'S AND NOT MINE -- `LIBRARY_RETRIEVAL` Sec 5.10.4, THE LAPLACE
        POSTERIOR MEAN.** I first wrote `confirmations - refusals` and that was an improvised
        metric with the instrument already specified one file away, which is this project's
        most-repeated failure: *assume it is already specified, and go look -- nine times the
        corpus had already named the instrument, and nine times the specified one was better.*

            confidence = (confirmations + 1) / (confirmations + failures + 2)

        **IT HAS NO FREE CONSTANT.** The `+1 / +2` is a uniform prior, not a knob -- there is
        no value to fit. **AND IT FIXES A REAL DEFECT IN THE DIFFERENCE FORM**, which the spec
        names as its point: an UNTRIED term reads 0.5, *neither favoured nor penalised*, while
        under a difference an untried term and an equally-tried one both read 0 and are
        INDISTINGUISHABLE. The difference form collapsed exactly the distinction the ordering
        exists to make.

        **ONE SUBSTITUTION FROM THE SPEC'S LETTER, FLAGGED AND NOT SILENT: it writes
        `rejections`, this reads `refusals`.** Sec 5.10.4 predates Isaiah's (c) ruling of
        2026-09-30, which moved the CEILING off the blend for a reason that applies here
        unchanged -- *a term could be unsettled by mistakes it made while on trial, which is
        precisely what counting them separately exists to prevent.* Dragging confidence down
        with candidate-era misses scores exploration as failure. **The reviewer approved
        refusals-not-misses in the plan; the spec's own wording is older than the split.**
        """
        st = self.standing.get(name)
        if st is None:
            return 0.5                       # UNTRIED READS 0.5, as the spec requires
        st.decay(self.tick, self.halflife)
        return (st.confirmations + 1.0) / (st.confirmations + st.refusals + 2.0)

    def youth_of(self, name: str) -> float:
        """THE YOUTH BONUS -- `1 / (1 + confirmations + refusals)`. Sec 5.10.8, no constant.

        1.0 untried, 0.5 after one trial, -> 0. Isaiah: *balance rich-get-richer with a YOUTH
        BONUS.* **Large at zero and shrinking as evidence accumulates, which is exactly what
        was asked for** -- and not UCB1, whose constant and `n = 0` singularity would both
        need a special case, nor Thompson, which makes the ranking stochastic and every A/B
        here depends on a deterministic one.

        **IT ORDERS WITHIN EQUAL CONFIDENCE AND NOWHERE ELSE, AND THAT PLACEMENT IS NOT THE
        SPEC'S -- the reviewer, 2026-10-01.** 5.10.8 writes
        `relevance = confidence x 0.5**(games_since_last_use / H) + youth`, an ADDITIVE form.
        **There is no games counter, so the decay term is 1, and the sum then falls
        MONOTONICALLY with experience:**

            untried      0.500 + 1.000 = 1.500
            proven x10   0.917 + 0.091 = 1.008

        An untried term would outrank one that has worked ten times, always -- surfacing
        exactly backwards. **The decay term is LOAD-BEARING and it is the half that cannot be
        built yet**: an untried term has never been used, so its confidence contribution
        vanishes and only youth remains, which is what holds youth in check.

        **SO THIS IS THE PLACEMENT WHILE RELEVANCE IS UNBUILDABLE, AND THE ADDITIVE FORM
        RETURNS WITH THE DECAY TERM.** In its own slot after confidence, youth can never
        compare terms of different confidence, so no inversion is possible by construction.

        **AND IT ACTS WHERE THE LAPLACE MEAN IS DELIBERATELY AMBIGUOUS**, which is the point:
        `confidence(0,0)` and `confidence(1,1)` are BOTH 0.5 -- a uniform prior collapses *no
        evidence* and *balanced evidence*. Youth separates them, 1.0 against 0.333.

        REFUSALS, NOT REJECTIONS, for `track_of`'s reason: 5.10.8 predates Isaiah's (c) split
        and counting candidate-era misses would score exploration as failure.
        """
        st = self.standing.get(name)
        if st is None:
            return 1.0                       # never seen: maximally young
        st.decay(self.tick, self.halflife)
        return 1.0 / (1.0 + st.confirmations + st.refusals)

    @property
    def settled_terms(self) -> list[Term]:
        return [t for n, t in self.library.items() if self.is_settled(n)]

    # -- reach ----------------------------------------------------------------------

    @property
    def alphabet(self) -> int:
        return len(self.atoms)

    def is_atom(self, term: Term) -> bool:
        """NOVEL is relative to atoms, not to the world.

        **AND A GUARDED TERM IS NOT THE ATOM IT WRAPS -- the reviewer, 2026-10-01.** This read
        `len(term) == 1 and ...`, which called `inc ?ACTED_SELF` an atom and had the mint cut it
        as not-novel BEFORE PRICING. A guarded term is a STRICTLY MORE SPECIFIC claim than the
        atom it wraps, not a duplicate of it.

        Invisible until now because the guard axis is an arm and `_guards` returned only intent
        kinds, so a single-atom GUARDED term was a shape the mint had never built.
        """
        return len(term) == 1 and term.guard is None and term.atoms[0].name in self._by_name

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
            # **THE GUARD CROSSES AND THE OPERAND'S BINDING DOES NOT -- the reviewer,
            # 2026-10-03.** A guard is a CONDITION and game-agnostic: `?ACTED_SELF` is a
            # per-slot boolean and never a name, `?BECOME OTHER` is an intent kind. An
            # OPERAND is a slot of THIS board -- `o1.colour` names an object another board
            # lacks -- so it is written for the RECORD only and `load` does not re-bind it.
            # **Writing neither is what destroyed every guarded term on carry (`F420`):
            # the atom names alone made `inc?ACTED_SELF` indistinguishable from `inc`.**
            out.append({"atoms": [a.name for a in t.atoms], "origin": t.origin,
                        "guard": t.guard, "operand": t.operand,
                        "handle": self.handles.get(name), "game": self.game,
                        # `stamps` holds DICTS: `getattr` on one returned None, so every term
                        # was saved with no admitting clause and no residual (F464).
                        "admitted": st.get("admitted") if st else None,
                        "residual": st.get("residual") if st else None})
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
        # **THE AGENT'S OWN EVIDENCE TRAVELS WITH ITS TERMS -- Isaiah's *metacog across solves
        # over time*, which he named as a level 4-5 requirement and which did not exist.** The
        # library persisted and THE SELF-KNOWLEDGE DID NOT, so a dial the agent earns was reset
        # to unearned at the start of every attempt. Against a clock of 128-309 actions that is
        # not a slow start, it is a value THAT CAN NEVER BE EARNED.
        #
        # **THE EVIDENCE IS WRITTEN, NOT THE CONCLUSION.** `vindication` is the raw list of
        # cycles-to-vindication; the halflife is re-derived from it on the far side. Carrying
        # the derived number instead would carry a conclusion without its basis -- and a value
        # whose provenance is gone cannot be revised by later evidence, only overwritten.
        blob = {"terms": out,
                "invented": {n: rec for n, rec in self.invented.items() if rec.get("delta")},
                "vindication": list(self.vindication),
                "book": dict(self.book)}
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
        # **THE EVIDENCE COMES BACK AND THE VALUE IS RE-DERIVED, never restored.** An older file
        # with no `vindication` key loads to an empty list and the agent starts unearned -- the
        # honest reading of *this file predates the books*, rather than a zero that would look
        # like measured evidence of nothing.
        self.vindication = list(blob.get("vindication") or []) if isinstance(blob, dict) else []
        # **MERGED, NEVER REPLACED, AND THE ORDER OF EVENTS IS WHY.** `arc_holdout` constructs
        # the `Agent` at :107 and calls this at :109 -- so `tether.BOOKS`' `setdefault` pass has
        # ALREADY run, and an assignment here wipes every key the saved blob predates.
        # Measured: 12 keys before, **1 after loading a blob written before tonight's books
        # existed.** Eleven quantities silently absent for the whole attempt.
        #
        # **THE SILENT-ZERO CLASS ARRIVING THROUGH PERSISTENCE**, which is the one route
        # `BOOKS` could not close from where it sits: a declaration at construction cannot
        # survive a later assignment. A key the blob has is RESTORED; a key it lacks stays at
        # the 0 the declaration put there, **which is what *this quantity has never moved*
        # should look like and not what *nobody recorded it* looks like.**
        if isinstance(blob, dict):
            self.book.update(blob.get("book") or {})
        if self.vindication:
            self.halflife = sum(self.vindication) / len(self.vindication)
        took, refused = [], []
        # INVENTED ATOMS ARE SKIPPED AND COUNTED, NEVER RE-INVENTED -- Isaiah, 2026-10-06
        # (decision 6). A replayed delta is a recorded effect table carried up as a method
        # (Fig 4) -- `act`'s shape. The records are kept in the report; nothing enters the
        # alphabet, and a term built on one is counted apart below (F466).
        skipped = sorted(n for n in (blob.get("invented") or {} if isinstance(blob, dict) else {})
                         if n not in self._by_name)
        built_on_skipped = []
        for r in rows:
            names = tuple(r["atoms"])
            if any(n in skipped for n in names):
                built_on_skipped.append({"atoms": list(names), "handle": r.get("handle")})
                continue
            if not all(n in self._by_name for n in names):
                refused.append({"atoms": list(names), "why": "atom not in this registry"})
                continue
            # THE GUARD IS RESTORED; THE OPERAND IS NOT RE-BOUND. Until an operand can be
            # saved as a TYPED PLACEHOLDER and re-bound per board, a term that had one
            # arrives without it and says so -- `crossed_without_binding` -- rather than
            # arriving as a different term with no record that anything was dropped.
            t = Term(tuple(self._by_name[n] for n in names),
                     origin=IMPORTED if r.get("game") != self.game else r["origin"],
                     guard=r.get("guard"))
            if t.name in self.library:
                # **`already_held` WAS ONE NUMBER OVER TWO OPPOSITE OUTCOMES -- `F420`.** A row
                # can land on a composition this registry genuinely holds, which is a real
                # dedup and costs nothing; or it can land on a PRIOR ATOM, which means the
                # saved term's whole content was its guard and operand and `save` wrote
                # neither, so the term is DESTROYED and the old report said `already_held`.
                # **A loss wearing the words of a successful dedup.** Measured: `click_only`
                # seed 6 carried 2 terms, arrived with 0, and read `already_held: 2`.
                onto_atom = self.library[t.name].origin == PRIOR
                self.merged.setdefault(t.name, []).append(
                    {"handle": r.get("handle"), "from": r.get("game"),
                     "operand": r.get("operand"), "guard": r.get("guard"),
                     "onto_atom": onto_atom})
                took.append({"handle": r.get("handle"), "already_held": True,
                             "onto_atom": onto_atom, "name": t.name, "unbound": False,
                             "lost": r.get("guard") or r.get("operand")})
                continue          # dedup on the COMPOSITION -- it keeps the handle it has
            self._install(t, seq=-2, residual=r.get("residual"),
                          admitted=IMPORTED if t.origin == IMPORTED else r.get("admitted"))
            if r.get("handle"):
                self.handles[t.name] = r["handle"]   # the birth handle, carried
            # THE `carried` FIELD -- set at LOAD, so a term can say it did not originate here
            # without the reader having to parse a handle for a game name.
            self.carried[t.name] = {"from": r.get("game"), "handle": r.get("handle")}
            took.append({"handle": r.get("handle"), "already_held": False,
                         "onto_atom": False, "name": t.name, "lost": None,
                         "unbound": bool(r.get("operand"))})
        # THE SKIPPED INVENTIONS AND WHAT THEY TOOK DOWN ARE REPORTED, because a silent count
        # is how an old library's dependence on them would be invisible.
        onto_atom = [x for x in took if x["already_held"] and x["onto_atom"]]
        onto_comp = [x for x in took if x["already_held"] and not x["onto_atom"]]
        return {"loaded": sum(1 for x in took if not x["already_held"]),
                "skipped_invented": skipped,
                "built_on_skipped_invention": built_on_skipped,
                # KEPT, so a caller reading the old key still gets the old number and the
                # split sits beside it rather than replacing it silently.
                "already_held": len(onto_atom) + len(onto_comp),
                "deduped_onto_composition": len(onto_comp),
                "destroyed_on_carry": len(onto_atom),
                "destroyed": [{"handle": x["handle"], "collapsed_to": x["name"],
                               "lost": x["lost"]} for x in onto_atom],
                # AN ARRIVAL THAT LOST ITS OPERAND IS NOT A CLEAN ARRIVAL, and counting it
                # among `loaded` without saying so is the same silence `destroyed_on_carry`
                # was split out to end, one step milder.
                "crossed_without_binding": sum(
                    1 for x in took if not x["already_held"] and x["unbound"]),
                # THE MERGE IS VISIBLE IN THE REPORT, not only in the object: a reader who
                # sees `loaded 1` from a 14-row blob can ask what the 1 absorbed.
                "merged_into": {k: len(v) for k, v in self.merged.items() if len(v) > 1},
                "refused": refused,
                "reads": ("composition crosses, binding does not. A refused row is an "
                          "INCOMPATIBLE registry, not a small library. "
                          "`destroyed_on_carry` is a row that collapsed onto a PRIOR ATOM "
                          "because save wrote neither its guard nor its operand -- a LOSS, "
                          "not a dedup, and it was counted as `already_held` until F420")}

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

    @staticmethod
    def _iter_step(cur: str, elem: str | None, unit: Term) -> tuple[str, str | None] | None:
        """Where a chain's type goes when `unit` is appended, `None` if it cannot be.

        **THE ENUMERATOR AND THE INTERPRETER DISAGREED ABOUT WHAT `in_type` MEANS, AND THE
        INTERPRETER WAS RIGHT -- `F347`.** `Term.apply` maps ANY non-reducer across a `Cells`
        value, and says so at its own site: *with this rule EVERY EXISTING ATOM becomes usable
        inside an iteration.* This walk asked `accepts_type(u, chain[-1].out_type)`, so after
        `cells` the running type was `CELLS` and **`count_true` was the only atom in the
        registry that accepted it.**

        **MEASURED BEFORE THIS EXISTED: 0 of 87,244 enumerated chains contained `cell_row` or
        `cell_col`**, and the one fold the composer could propose was `cells . count_true` --
        which `count_true` REFUSES, because the collection holds coordinates and not booleans.
        **The construct ran and could never be composed.**

        MID-ITERATION THE TYPE THAT MATTERS IS THE ELEMENT'S. A `CELLS`-typed unit CLOSES the
        iteration and anything the element type feeds MAPS, which is `apply`'s rule restated
        where the composer can act on it rather than a second rule.

        **`CELL` IS NOT A CHOICE HERE -- `CELLS` IS DEFINED AS A COLLECTION OF `CELL`**, so the
        element type of a fresh collection is the type system's own answer, not a constant.

        INERT WITH THE ARM OFF, WHICH IS WHY IT NEEDS NO RULING. `cells` is the ONLY producer
        of `CELLS` and it exists only under `TETHER_ITERATE`, so with the arm off `elem` is
        always `None` and this reduces, line for line, to the check it replaces.
        """
        # **FOLDED OVER THE UNIT'S ATOMS, NOT READ OFF ITS ENDS -- and the first version read
        # its ends.** A unit is an ATOM or a SETTLED TERM, and a settled term carries several
        # atoms that `apply` runs one at a time, each deciding independently whether it maps or
        # closes. A chunk like `cells . cell_row` leaves the value a COLLECTION while its last
        # atom's `out_type` says `POSITION` -- so reading the ends would call the walk flat when
        # it is still mid-iteration, and every extension after it would be wrongly typed.
        #
        # **IT IS UNREACHABLE TODAY AND THAT IS NOT A REASON TO ASSUME IT.** The emission rule
        # refuses an unclosed iteration, so no such chunk can be minted and settled HERE -- but
        # `units()` also admits what promotion and import put there, and *a term that cannot
        # arrive by the route I checked* is the assumption this project keeps paying for.
        for a in unit.atoms:
            if elem is not None:
                if a.in_type == CELLS:
                    if a.elem_type is not None and elem != a.elem_type:
                        return None                        # the reducer would refuse it
                    cur, elem = a.out_type, None           # closed
                    continue
                if not (a.polymorphic or elem in a.accepts):
                    return None
                cur, elem = CELLS, a.out_type              # mapped: the ELEMENT type moves
                continue
            if not (a.polymorphic or cur in a.accepts):
                return None
            cur = a.out_type
            elem = CELL if cur == CELLS else None
        return cur, elem

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
        start = [u for u in units if accepts_type(u, in_type)]
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
        # CARRIED, NOT RECOMPUTED. The state is (chain, current type, element type or None);
        # re-deriving it per extension would walk every chain again inside the hot loop.
        frontier = [(u.atoms, *Gamma._iter_step(in_type, None, u)) for u in start]
        depth = 1
        spent = False
        while frontier and depth <= max_depth:
            nxt: list[tuple] = []
            for chain, cur, elem in frontier:
                # AN UNCLOSED ITERATION IS NOT A TERM. Its value is a `Cells`, whatever the
                # last atom's `out_type` says -- so it may only be emitted once a reducer has
                # closed it, which is exactly `elem is None`.
                if elem is None and cur == out_type:
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
                    for u in units:
                        if any(a.name == IDN_NAME for a in (*chain, *u.atoms)):
                            continue
                        step = Gamma._iter_step(cur, elem, u)
                        if step is not None:
                            nxt.append((chain + u.atoms, *step))
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
        total = sum(1 for u in units if accepts_type(u, in_type) and u.out_type == out_type)
        # length 1 counts every unit; length > 1 only the idn-free ones, both as the head of
        # the chain and as each extension -- the closure's rule, not a separate policy
        live: dict[str, int] = {}
        for u in free:
            if accepts_type(u, in_type):
                live[u.out_type] = live.get(u.out_type, 0) + 1
        for _ in range(2, max_depth + 1):
            nxt: dict[str, int] = {}
            for t, n in live.items():
                for u in free:
                    if accepts_type(u, t):
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
