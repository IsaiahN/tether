"""The loop. Steps 1 to 5.

One track: an action is proposed by an utterance that type-checks and passes the gate, or
there is no action. There is no fast path, because a fast path is what makes the framework
optional.
"""

from __future__ import annotations

import hashlib
import itertools
import math
import os
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from functools import partial
from itertools import islice
from typing import Any

import composer
import condition
import grammar as G
import instruments as I
import retrieval
import routine as Rt
from gamma import INVENTED, Ctx, Gamma, Standing, Term, accepts_type
from gamma import SAME_AS_TARGET as G_SAME
from ledger import (
    ADVANCE,
    CHANNEL_CLOSED,
    ENDING_READS,
    GENUINE,
    NO_CHANGE,
    SLICE_TOO_SMALL,
    SPECIFIED,
    Ledger,
)
from priors import contact_first
from probe import Drive
from self_family import MIN_REPEAT
from sensors import COMMENSURABLE, DELTA, NOT_RESOLVED, OBJECT, POSITION

sys.dont_write_bytecode = True

IDN = "idn"
# THE EDGE'S TWO FACTS, named here so `_predict` reads constants rather than strings.
OBJ_TYPE = "OBJ"
# WHAT MAY BIND A SLOT. `_predict`'s two arms are the whole contract -- a `val` term is the
# prediction, an `OBJ` term is the want -- so a third out_type is a state the dispatch cannot
# read, and `_discrepancy` answers NOT_RESOLVED for the rest of the run. `mint` honours this by
# construction (its streams ARE these two); the retrieval path did not, and was satisfied by
# accident until an atom carrying a third type reached it.
BINDABLE = ("val", OBJ_TYPE)
# STEP 1 NARROW. `BINDABLE` filters the OUTPUT type and never asked `_head_accepts`, the INPUT
# rule written one screen up -- so a term could be refused for its output while its input was
# never consulted. Widening on BOTH conditions admits 7 atoms; on the output alone it admits 26,
# of which 19 could only ever abstain.
#
# **A TABLE AND NOT A PREDICATE, because an exemption in logic widens quietly and a table can be
# diffed.** A type is listed here only when the census MEASURED its slot representation and its
# atom-output representation to survive the consuming operation -- `correction_bits`' `a %
# alphabet`, four call sites, all identical. **The verdict is DOES `%` WORK, never do the names
# match**: `BOOL` holds an `int` in the slot and returns a `bool`, which a name comparison calls
# a mismatch and `%` accepts.
#
# `SHAPE` WAS ABSENT ON A MEASURED FACT AND IS NOW ADMITTED ON ONE. It read 36 of 36 `%`
# failures across six boards because a SHAPE slot holds the episode-local INT id while a
# SHAPE-typed atom returned a FROZENSET of offsets. **The inverse encoder (`_to_shape_id`)
# landed, so the three SHAPE atoms now return the published id or abstain**: measured on
# `g50t`, `rotate` 16 int / 14 abstain, `reflect` 20 / 10, `canonical` 20 / 10 -- zero
# frozensets, zero raises. The condition this table states is met, so the row moves.
#
# **THE ABSTENTIONS ARE THE MECHANISM WORKING, NOT A SHORTFALL:** a rotated shape the board
# never published has no id, and minting one would let a PREDICTION grow the alphabet it is
# priced against.
#
# COLOUR/POSITION/DELTA remain UNCHECKABLE rather than agreeing -- every producer of those
# takes `OBJECT`, so none was ever called and the census has no atom-side reading to compare.
REPR_AGREES = ("EXTENT", "SHAPE")


def _may_bind(cand: Any, slot_type: str | None) -> bool:
    """Both halves: the output type must be bindable, AND the head must accept the slot."""
    out = getattr(cand, "out_type", "val")
    if out in BINDABLE:
        return True
    return out == slot_type and out in REPR_AGREES and _head_accepts(cand, slot_type)

# F127's arm B. Seat-side and off unless asked for, so the default build is byte-identical.
_TYPED_BIND = bool(os.environ.get("TETHER_TYPED_BIND"))
# F130 arm C: supply `_library_fit`'s retrieval the relation channel its two
# sibling call sites already pass. Seat-side, off by default.
_REL_GAP = bool(os.environ.get("TETHER_REL_GAP"))
# F32 arm D: decide reuse by the ONE BARGAIN rather than by a zero remainder,
# which Isaiah ruled out. Seat-side, off by default.
_BARGAIN_FIT = bool(os.environ.get("TETHER_BARGAIN_FIT"))
# F141 arm E: vote by the movement RATE rather than a majority flag. Seat-side, off.
_FINE_VOTE = bool(os.environ.get("TETHER_FINE_VOTE"))

# ARM F -- RECIPE DEDUP. The novelty check below tests `term.name`, which carries operand AND
# guard, so `translate . recolour<o5.w>` and `<o12.w>` both read NOVEL and both get minted.
# Measured: 94% of mints re-derive a chain already held, and `translate . recolour` was minted
# 137 times in one run (F229). Isaiah: "adding a dup is a symptom of the found thing never being
# searched for -- a deeper usage-of-terms problem." This arm makes the check see the RECIPE.
# DEFAULT OFF, like every other arm, so the baseline it is measured against is preserved.
_RECIPE_DEDUP = bool(os.environ.get("TETHER_RECIPE_DEDUP"))

# ARM G -- REBIND WHAT IS HELD. `_rebindings` returns early for any term that already carries an
# operand, so only IMPORTS (which arrive unbound, `save` drops it) are ever re-bound. A term the
# agent minted THIS RUN is offered to a new slot still pointing at the old one, `_explains` tests
# behaviour, and it cannot explain -- so mint re-derives it. CENSUSED at the reviewer's request:
# of the terms installed by mint, 100% (dc22) and 94% (ls20) were chains ALREADY IN THE LIBRARY,
# and 85% / 41% of those were held with an operand locked to a DIFFERENT slot.
# The principle is the method's own docstring: *composition crosses, binding does not* -- true of
# every term, applied to loaded ones only. DEFAULT OFF like every other arm.
_REBIND_HELD = bool(os.environ.get("TETHER_REBIND_HELD"))

# ARM H -- THE GUARD AXIS IN RETRIEVAL. Reviewer ruling 2026-09-21, and it is the generation half
# of F238. `mint` walks (operand x GUARD) via `_guards(robs)`; `_rebindings` varies only the
# operand and inherits the held guard, so 31-42% of what mint installs is a Term retrieval can
# never produce -- no admission rule can accept a candidate that was never offered (F239: cost,
# left and base are identical in both paths, so generation is the whole of the gap).
# BOUNDED AS MINT IS: guards come from `_guards(robs)` -- None first, then ONLY the actions
# appearing in that residual's own observations -- never the full action set on every lookup.
# The playbook's lookup fires on a SETTLED CHANGE and that event carries the action that produced
# it, so handing retrieval the observation is giving it the event it was specified to key on.
_GUARD_AXIS = bool(os.environ.get("TETHER_GUARD_AXIS"))

# ARM I -- DECODE THE SHAPE STAND-IN. `arc_percept` computes the normalised offset frozenset every
# frame and publishes an episode-local INT in its place; every SHAPE atom guards on a frozenset, so
# seven of the 48 read NOT_RESOLVED on every call -- measured 0 of 40 (F242). `arc_world.shapes()`
# is the inverse map, built for exactly this, with zero callers. This hands it to the atoms through
# `Ctx` and changes NOTHING about what is published: the slot value, the alphabet and the bargain's
# inputs are untouched. RELATIONS.md calls it "a build and not a decision to revisit ... no new
# sensor, no entry rule, no exemption". DEFAULT OFF, because it makes seven dead atoms live and
# that moves the closure.
_SHAPE_DECODE = bool(os.environ.get("TETHER_SHAPE_DECODE"))


def _norm_name(x: str) -> str:
    """The join between the CORPUS's names and the REGISTRY's. Same normalisation
    `composer.candidates` uses, and it exists for the same measured reason: the corpus writes
    `Contact` and `Sign` and `SIGN`, the registry writes `contact` and `sign`."""
    return re.sub(r"[^a-z0-9]", "", x.lower())


def _head_accepts(cand: Any, slot_type: str | None) -> bool:
    """Does the candidate's HEAD atom accept what the slot actually holds?

    Three channels, and missing one is how this class of measurement keeps going wrong:
    `in_type`, `also_accepts`, and `val` as the universal. An untyped slot is not a mismatch.
    """
    if slot_type is None:
        return True
    head = getattr(cand, "atoms", None)
    if not head:
        return True
    # ONE PREDICATE, shared with `enumerate_closure`. This used to read `val` as a universal
    # while the search read it as a literal, so the binder admitted `owner` on every slot and
    # the search never offered it. The three channels are unchanged -- `in_type`,
    # `also_accepts`, and now an EXPLICIT `polymorphic` where `val` used to be inferred.
    return accepts_type(head[0], slot_type)
# `CAN`'s THREE OUTCOMES. Named rather than bare strings because `UNKNOWN` is the one that gets
# quietly folded into `NO` -- they behave alike at the commit and are different claims on the
# record, which is check 3 exactly.
YES, NO, UNKNOWN = "yes", "no", "unknown"
OBJECT_TYPE = "OBJECT"
ORDERED_TYPES = ("POSITION", "EXTENT", "DELTA")

# anchor: how many reachable terms an experiment weighs before choosing. Bounded because
# the choice is made every step and the closure grows; 200 covers depth 2 over the toy
# alphabet exactly, and truncation only ever narrows the spread, never invents one.
DISCRIMINATE_BUDGET = 200

# THE CODE, declared. Both halves of the bargain are lengths under it.
#   a correction on one slot-transition: log2(M) bits, a uniform code over the M values
#   a term of k atoms:                   (k+1) * log2(|atoms|+1), the atoms plus a stop
CODE = ("uniform(M) per correction; (k+1)*log2(|atoms|+1) + (k-1)*log2(|bonds|) per term")

# HOW MANY BOND TYPES THE TERM LANGUAGE HAS. A `Term` is applied left to right, which is ONE
# bond -- sequence -- so this is 1 and the bond term is `log2(1) = 0`.
#
# **THE SOURCE IS `THE_FORMULA` NOTE 32**, which states the code and says why the previous draft
# was wrong: *it said declare the code and left the arrangement uncharged, so a formula recorded
# its ingredients and not its structure.* The derivation below is the same result reached from
# §11.2's signature, kept because it says why the value here is ONE and not merely zero-for-now.
#
# **THE ZERO IS A CONSEQUENCE, NOT A DESIGN.** `CODE` charges `log2(alphabet)` per position and
# the alphabet is WHAT IS AVAILABLE; a symbol drawn from a one-symbol alphabet costs nothing
# because it tells you nothing. Charging `log2(7)` for a choice among one would be charging for
# information that is not there, which is the one thing a description length refuses to do.
#
# **NO STOP SYMBOL, AND THE ASYMMETRY IS DERIVED.** The atom term carries `+1` because a
# sequence's LENGTH is unknown and must be terminated. There are exactly `k-1` bonds and `k` is
# already read, so nothing terminates them.
#
# **AND IN THIS SPACE IT IS FIXED AT ONE, WHICH IS THE SIGNATURE'S AND NOT A STAGE.** §11.2 types
# PREDICT as `slot x action -> slot`, so composition here IS function composition, and each of
# the other six fails on what it would do to a VALUE: `+` gives two values with no combining
# rule; `⇒` is creation and a slot's value cannot not-exist-then-exist; `∥` needs a selector,
# which is a truth PREDICT has no type for; `−` is a set operation on a scalar; `≡` is a synonym
# and not a computation; `⋛` yields a truth. **One of seven has a form here and it is the one
# implemented** -- so `Term` being a chain is the signature, not a limitation.
#
# **AN EARLIER VERSION OF THIS COMMENT SAID THE TERM WOULD RISE SILENTLY AND PREDICTED FOUR
# MARGINAL PAYERS STOPPING AT 1.49 BITS AGAINST A 2.8-BIT BOND. THAT CANNOT HAPPEN HERE.** The
# expression stays general because a space that admits more bonds prices them automatically;
# the value in THIS space does not move.
BONDS = 1
# `[I]` NOTE, NOT A FINDING: the bond term is an entropy term, and not by analogy. Shannon and
# thermodynamic entropy are the same mathematics and MDL is built on Shannon -- both already cited
# on Figure 5. So `log2(|bonds|)` is the entropy of the ARRANGEMENT SPACE in bits: more bond types
# means more distinguishable arrangements, priced at the log of the increase. Two laws in one line
# -- the first says you cannot create atoms, the second says rearranging them is not free. Its
# value is that the formula is checkable against Shannon instead of taken on trust.

HELD, NOVEL, REBIND, MECHANISM = "held", "novel", "rebinding", "mechanism"
# THE FIFTH BIN -- the reviewer, 2026-09-21. The four above all sort the gap by what is
# MISSING, so a refusal can be composed and is never DEMANDED. This one sorts by what is
# WRONG: a HELD term was EXPRESSED on this slot and the ground refused it. Expressed-and-
# failed ONLY -- a term retrieval never reached has not been tested and loses nothing, which
# is Isaiah's hit-rate ruling and is already how `gamma.refute` behaves.
REFUTED = "refuted"

# ARM J -- SEAT-SIDE SWITCH, DEFAULT OFF. The bin is a RULING and the plumbing is built ON;
# the DIVERSION it causes is a policy change to the acting path and is not. With it live, two
# conform seats fail -- `shipped`'s B5 (support at zero and no probe followed) and three M2
# checks -- because slots that reached `mint` now reach a competitor instead. That is a
# READING of what the bin does, not a reason to edit the checks: *reintroduce the defect,
# never disable the check.*
_REFUTED_BIN = bool(os.environ.get("TETHER_REFUTED_BIN"))

# ARM L -- BOUND THE OPERAND AXIS BY THE DELTA. SEAT-SIDE SWITCH, DEFAULT OFF.
# `F258`: yields expand 32-106x into ranked candidates and the operand axis is the multiplier.
# Arm H already bounds the GUARD axis by the actions present in the residual's own
# observations; this is the same construction one axis over, and no constant.
#
# TWO CORPUS CLAUSES POINT OPPOSITE WAYS AND THE DISTINCTION RECONCILES THEM. 12.1 admits a
# BIAS only as a ranked reversible cut, and `_bindings`' own comment says a filter would make
# contact decide REACHABILITY rather than order. But Layer 5 and the mapping section say the
# CHANGED ATTRIBUTES BECOME THE KEY, and Isaiah's note on the sixth enforcer says why that is
# different: *a delta-cue selects by WHAT ACTUALLY CHANGED, ground-supplied rather than
# prior-supplied.* So the DELTA may select and CONTACT may not -- which is why contact enters
# here only to WIDEN the set and never to exclude from it.
#
# AND DEFAULT OFF BECAUSE THE FILE RECORDS THIS FAILING BEFORE: *the version that DROPPED
# operand-reading terms when R showed no dependence on another slot LOST A CLOSING TERM.*
# Different rule, same family. `distinct compositions must not fall` is the falsifier.
_DELTA_OPERANDS = bool(os.environ.get("TETHER_DELTA_OPERANDS"))
# ITEM 6, THE RE-KEY. Default OFF. `F303` measured the key BEFORE this was built: a GLOBAL frame
# delta is saturated at every granularity that crosses boards -- types 100% of cycles, attribute
# names 91% -- because *did ANY slot of this type move ANYWHERE* is always yes across 1,688
# slots. Scoped to the target's OWN OBJECT it is ~3%, median 0%, with nine objects in ten
# changing nothing. The reviewer's ordering requires this narrowing BEFORE mint's `out_type` is
# widened: widening without narrowing is how 735 million calls arrive nowhere.
_DELTA_KEY = bool(os.environ.get("TETHER_DELTA_KEY"))
# THE out_type WIDENING -- Isaiah's 3A, reviewer-pre-registered 2026-09-23. `mint` asks for
# `("val","val")` and `(slot_type, OBJ)` and NOTHING ELSE, and the composition census says
# that IS the ceiling: 4 distinct compositions on every board, which are exactly those two
# streams. Widened, mint also asks for `(slot_type, T)` for each T THE DELTA LIGHTS.
#
# ABORT CRITERIA, declared before the first run and unchanged: candidates tried rises while
# arrivals do not -> OFF; calls-per-cycle growth steepens against the control -> OFF; binds
# per candidate rises -> OFF. Each is a RESULT, not a failure.
_STREAM_WIDEN = bool(os.environ.get("TETHER_STREAM_WIDEN"))
# ITEM 7. Default OFF: it APPENDS TO THE ATOM REGISTRY, which every term reads.
_INVENT = bool(os.environ.get("TETHER_INVENT"))

# ARM M -- PERTURB THE STARVED SLOT, IN PARALLEL. SEAT-SIDE SWITCH, DEFAULT OFF.
# `F269`'s table is the premise: on sk48 all seven probes fire in cycles 1-7 and all seventeen
# `no_support` parks land in 16-18, so NO PROBE FOLLOWS ANY OF THEM. `bored()` is true EARLY,
# when almost nothing is bound and there is nothing to perturb FOR, and false LATE, which is
# exactly when slots starve. **The agent perturbs when it has nothing to perturb for and cannot
# perturb once it does.** A temporal anti-correlation, not a threshold.
#
# ISAIAH'S SYSTEM 0 SPEC IS WHAT RULES IT: *a fallback for when higher-level reasoning is IN
# PROGRESS, like systems 1 and 2 happening IN PARALLEL ... CONTACT is the main mode.* So a
# starved slot does not wait for the board to go quiet -- and the STARVED SET IS THE SWITCH,
# no counter and no quota, exactly as the unexplored-contact count is System 0's.
_STARVED_CONTACT = bool(os.environ.get("TETHER_STARVED_CONTACT"))

# THE SATISFACTION PREDICATE'S SPELLING, AND IT EXISTS BECAUSE OF AN `A6i` OF MINE.
# `condition.py`'s grammar is `expr := INSTRUMENT(args) | SLOT | NUMBER` -- **a bare SLOT is an
# EXPRESSION, so it denotes the slot's VALUE.** The first version of the guard reader returned
# the slot's SATISFACTION PREDICATE for the same node. One name, two quantities, and both
# readings are well-formed: `and`/`or`/`not` over predicates worked, and the first `Cmp` to
# arrive would have compared a BOOL to a number and reported a clean `False`.
#
# **A PREFIXED NAME RATHER THAN A NEW NODE, because `evaluate` evaluates a `Call`'s arguments
# BEFORE the reader sees them** -- so `Call("satisfied", (Slot(s),))` would hand the reader the
# slot's VALUE and lose the name. The prefix keeps the grammar untouched, renders legibly, and
# is one place rather than a second node kind every walker would have to learn.

_SAT = "satisfied:"

# EVERY QUANTITY THE AGENT RECORDS ABOUT ITSELF, DECLARED IN ONE PLACE AND INITIALISED TO ZERO.
#
# **THE DEFECT THIS REMOVES BY CONSTRUCTION BIT THREE TIMES IN ONE NIGHT.** A counter written
# only when it increments reads ABSENT at zero, and **absent cannot be told from
# never-recorded** -- gate 1's tally, `plan_gate_no_hypothesis`, and the bargain book, the last
# of them committed an hour AFTER the first two were fixed. **Knowing the class did not stop me
# repeating it**, which is this project's own rule for when prose has to become a mechanism.
#
# A ZERO IS THE MOST INFORMATIVE READING A BOOK HAS. *Not one candidate reached `pays`* and *the
# agent holds no goal hypothesis* are both zeros, and both were invisible. **So the store starts
# with every key, and an increment can never be the thing that makes a key exist.**
#
# DECLARED HERE RATHER THAN IN `gamma` BECAUSE THE KEYS ARE THE AGENT'S, not the library's --
# `Gamma` owns the STORE so it persists with the terms, and this owns what goes in it.
def _book_add(book: dict, key: str, n: int = 1) -> None:
    """Increment a book, and REFUSE a key `BOOKS` does not declare.

    **A GREP CANNOT GUARD A CONSTRUCTED KEY, AND TWO SITES BUILD ONE.** The declaration check
    scans for a quoted key; `arrived_at_depth_{d}` and `plan_gate_{k}` are assembled at
    runtime, so they were invisible to it -- **and all nine depth buckets were undeclared,
    therefore uninitialised, therefore reading ABSENT at zero.** In the book built to inform
    the `max_depth` fork, where the whole reading is the histogram's SHAPE.

    **SO THE CHECK MOVES FROM THE GREP TO THE WRITE SITE**, where a constructed key cannot
    evade it. `routine.advance` raising on a shape it cannot walk is the precedent:
    a key nobody declared is a programming error, and it surfaces the first time the line runs
    rather than as a quantity that silently never appears.
    """
    if key not in BOOKS:
        raise KeyError(f"undeclared book key: {key!r} -- add it to tether.BOOKS")
    book[key] = book.get(key, 0) + n


def _contains(whole: tuple, part: tuple) -> bool:
    """Is `part` a CONTIGUOUS subsequence of `whole`? §14.7's *appears as a constituent*.

    CONTIGUOUS, not scattered: a chain is applied left to right, so a settled term is a
    constituent only where its atoms run consecutively. Scattered atoms are a coincidence of
    the alphabet and counting them would inflate the one number the chunking claim rests on.
    """
    n = len(part)
    return n > 0 and any(whole[i:i + n] == part for i in range(len(whole) - n + 1))


BOOKS: tuple[str, ...] = (
    "promoted_then_wrong",              # settled, then mispredicted
    "demoted_would_have_been_right",    # the counterfactual `F327` destroys unrecorded
    "demoted_stayed_wrong",             # released unvindicated at the watch cap
    "arrived_using_an_invented_atom",   # did inventing ever reach a SETTLED term
    "plan_gate_too_short",              # gate 1: the bar was never APPLIED
    "plan_gate_flat",                   # gate 1: the bar genuinely refusing
    "plan_gate_rose",                   # gate 1: the bar genuinely refusing
    "plan_gate_qualified",              # gate 1: an objective passed
    "plan_gate_no_hypothesis",          # gate 1: nothing to filter. SUPPLY, not the bar
    "bargain_bounded_out",              # `_cannot_pay` -- a NECESSARY condition, not a choice
    "bargain_does_not_pay",             # `pays` -- the only one of the two that is a judgement
    "bargain_paid",                    # reached the contest
    "mint_no_residual",                 # refused by the residual precondition
    # THE FIFTH TURN. Isaiah's crane game: the toy slipped and the SITUATION IMPROVED, and a
    # system recording only win/lose throws that entire turn away. Three buckets, never summed.
    "gap_improved",                     # the goal gap SHRANK on a slot since last cycle
    "gap_worsened",
    "gap_flat",
    "gap_shapes_seen",                  # distinct cycles characterised (S15.3)
    "gap_shape_repeat",                 # all four keys matched: the LOOP case
    "want_retained_unpaid",             # a want kept though it did not pay
    "focus_by_want",                    # System 2 set the focal slot, not surprise
    "chunk_reuse",                      # §14.7: a settled term inside a later mint
    # THE ARRIVAL-DEPTH HISTOGRAM, ALL NINE BUCKETS. Declared because **a histogram with a
    # missing bucket is not a histogram** -- *no term arrived at depth 3* and *depth 3 was
    # never recorded* are different readings, and this book exists to be read as a SHAPE.
    # It was written through a CONSTRUCTED key, so the grep-based guard could not see it.
    *(f"arrived_at_depth_{_i}" for _i in range(1, 10)),
)

# why not the neighbouring bin. A bin without its discriminator is a label, not a diagnosis.
WHY_NOT = {
    HELD: "not novel: the slot is bound and the bound term predicted it",
    NOVEL: "not mechanism: too little history to distinguish a wrong model from a new one",
    REBIND: "not mechanism: a term already in the library explains the whole history",
    MECHANISM: "not rebinding: no library term explains the history, so the model is wrong",
    REFUTED: "not rebinding: the bound term was expressed here and the ground refused it",
}

# why a zero reading is not always HELD
OWES = "not held: this step read zero and the slot still owes"

TRANSITION, REWARD, BRACKET = "transition", "reward", "bracket"


def correction_bits(a: int, b: int, alphabet: int) -> float:
    """The code's FORM is the loop's -- uniform over the alphabet -- and its SIZE is the
    domain's. Neither half is a module global reached across a boundary."""
    return 0.0 if a % alphabet == b % alphabet else math.log2(alphabet)


def round_trip_gap(t_a, state: dict[str, int], alphabet: dict[str, int]) -> float:
    """R_T: THE GAP BETWEEN `x` AND `T_E(T_A(x))`, per PHILOSOPHY §0.3 and §16.1.

    Send it up, bring it back, charge what came back wrong. `T_E` is the coarse value taken
    literally, so the extensive law `x <= T_E(T_A(x))` holds and the gap is non-negative by
    construction rather than by hope.

    A SLOT THE VIEW DROPPED COSTS ITS WHOLE CODE, not nothing. Reconstructing a missing key
    from the true value would let `T_E` recover exactly what `T_A` discarded and read a
    dropping view as lossless -- measured, `drop:s0` read 0.000 bits before that line went
    in. **A fallback in a reconstruction is a claim that nothing was lost.**

    THIS REPLACED A PRE-IMAGE SWEEP, which measured a different quantity -- the VIEW's global
    lossiness rather than THIS state's loss -- and was over budget on every panel that
    exists: 8.24e+05 on the toy world against 4,000, 1.68e+04 on `snaps`, 3.32e+13 on a 4x4
    board, past float range on 64x64. The gap is O(slots) and has no budget at all.
    """
    back = t_a(state)
    total = 0.0
    for slot, v in state.items():
        if slot in back:
            total += correction_bits(back[slot], v, alphabet[slot])
        else:
            total += math.log2(alphabet[slot])
    return total


def term_bits(k: int, alphabet: int, bonds: int = BONDS) -> float:
    return (k + 1) * math.log2(alphabet + 1) + (k - 1) * math.log2(max(bonds, 1))


def pays(cost: float, left: float, base: float) -> bool:
    """The bargain. Strict: a tie does not license a new term."""
    return cost + left < base


def objective_step(evaluate, current: int, ordered: bool, alphabet: int) -> Any:
    """THE EDGE: what a composed objective predicts about a slot value.

    An objective is a TRUTH and a bet is a VALUE, so something has to say what wanting a
    thing predicts about the slot. This is that rule, and it sits beside `pays` for `pays`'
    reason: the bargain is seat-written and uniform because what a bet COSTS is not a move,
    and what a bet MEANS is not a move either. A piece does not redefine winning.

    UNIFORM OVER EVERY OBJECTIVE. It never asks what the objective is about -- it PROBES,
    evaluating the objective at candidate values, which is a numerical gradient and assumes
    nothing about the term's contents.

    NEAREST IS THE TYPE'S, and that is the whole of the two arms:

        ORDERED           step ONE UNIT toward the nearest satisfying value. There is a
                          more-and-less, so there is a direction and a distance
        COMPARABLE-only   return the satisfying value ITSELF -- next-frame satisfaction --
                          because with no ordering every value is equidistant and "one step
                          toward" names nothing

    SATISFIED ALREADY -> the slot HOLDS. NOTHING SATISFIES -> NOT_RESOLVED, never a guess:
    *the instrument could not read* rather than a value nobody has evidence for.
    """
    here = evaluate(current)
    if here is None:
        # THE OBJECTIVE COULD NOT BE READ HERE. Falsy is not the same claim as unreadable,
        # and `NOT_RESOLVED` is falsy -- so testing it for truth would file *I cannot see*
        # as *not satisfied* and send the probe hunting for a value to fix a gap nobody
        # measured. Same rule as a null attribute, at the objective.
        return NOT_RESOLVED
    if here:
        return current
    # P3: THE SAME ANSWER, ASKED AS A FIRST-MATCH. Both arms took ONE element out of a
    # fully-built list -- `hits[0]` and `min(key=(abs(v-current), v))` -- so the probe ran
    # the whole alphabet to answer a question the first hit settles. `evaluate` is `_sat`
    # over `term.apply`, which is pure, so calling it fewer times changes nothing but time.
    #
    # THE ORDER IS THE OLD KEY MADE INTO A WALK, not a new preference: at distance `d`,
    # `current - d` is the smaller `v` and therefore sorted first under `(abs, v)`. A
    # `current` outside the alphabet reduces to the one-sided walk the key already gave it.
    if not ordered:
        for v in range(alphabet):
            if v != current and evaluate(v):
                return v
        return NOT_RESOLVED
    # ONE STEP TOWARD THE NEAREST, WHICH IS THE ARM'S WHOLE CONTENT -- `lo < current` and
    # `hi > current` by construction, so the step is the sign and nothing is recomputed.
    for d in range(1, alphabet + abs(current) + 1):
        lo, hi = current - d, current + d
        if 0 <= lo < alphabet and evaluate(lo):
            return current - 1
        if 0 <= hi < alphabet and evaluate(hi):
            return current + 1
    return NOT_RESOLVED


def objective_gap(evaluate, current: int, ordered: bool, alphabet: int) -> Any:
    """§13.4's SCALAR DISCREPANCY: *zero exactly when satisfied.*

    Beside `objective_step` and for its reason -- what a bet MEANS is not a move, so the two
    things an objective says about a slot (**which way to go**, and **how far it is**) are
    written once, uniformly, in the same place. It PROBES exactly as the step does and asks
    nothing about the term's contents.

    NEAREST IS THE TYPE'S, THE SAME TWO ARMS. `ORDERED` has a distance, so the gap is the
    distance to the nearest satisfying value. `COMPARABLE`-only has none -- every unsatisfied
    value is equidistant -- so the gap is 1, which is *not satisfied* and says nothing more
    than it can support.

    THREE OUTCOMES, NOT TWO, AND THE THIRD WAS COLLAPSED WHEN THIS WAS WRITTEN -- `A6i`, found
    by `CAN`'s spec read the next day. `None` meant BOTH *I could not read the objective here*
    and *nothing in the alphabet satisfies it*. **For a discrepancy series those collapse
    harmlessly, because either way the trend breaks. For `CAN` they are OPPOSITE ANSWERS** --
    unreadable is `unknown` and nothing-satisfies is a real `no`, and a `CAN` built on the
    collapsed version would report *not achievable* for *I could not see*, which is check 3's
    absence-as-fact at the one place a routine commits to looping.

        NOT_RESOLVED   the objective could not be read here
        None           nothing in the alphabet satisfies it -- a genuine negative
        int            the distance, and zero exactly when satisfied

    Neither non-integer is a large gap: a big number would sort below a small one and read as
    *nearly there*.
    """
    here = evaluate(current)
    if here is None:
        return NOT_RESOLVED
    if here:
        return 0
    hits = [v for v in range(alphabet) if v != current and evaluate(v)]
    if not hits:
        return None
    return min(abs(v - current) for v in hits) if ordered else 1


def objective_degree(evaluate, scope, counts: dict | None = None) -> float | None:
    """`degree(molecule)` — **the fraction of the SCOPE that satisfies the objective.**

    `DISCOVERY` Q21 answers *is `R_goal` measurable* and gives the measurement: a molecule is a
    quantified typed objective evaluated across a scope, and it returns *a verdict **and a
    continuous degree*** — `ALL -> fraction satisfied`, `NONE -> 1 - fraction satisfied`. **So
    `R_goal = 1 - degree`, and it is graded rather than binary, which is what makes progress
    measurable at all.**

    THE FRACTION WAS ALREADY BEING COMPUTED AND THROWN AWAY. `arc_atoms._over_group`'s `fold` is
    `int(q(x == v for x in c.group))` — the generator IS the per-member verdict and only the
    quantifier's boolean survives. **This reads the same scope and keeps the fraction**, so it
    adds no atom, no sensor and no prior: it is a specified quantity the code was discarding.

    AND IT IS A THIRD READING OF AN OBJECTIVE, NOT A REPLACEMENT FOR EITHER. `objective_step`
    says WHICH WAY to move a slot, `objective_gap` says HOW FAR that slot is, and this says HOW
    MUCH OF THE POPULATION is unsatisfied. **The first two are about one slot and cannot be
    wide; only this one ranges over a scope.**

    `None` when the scope is empty — an absent population is not a satisfied one, which is
    `_over_group`'s own rule for the boolean and holds for the fraction too.
    """
    vals = [evaluate(x) for x in scope]
    seen = [v for v in vals if v is not None]
    # THE COUNTS ARE THE ONLY THING THAT SEPARATES THREE STATES A FLAT SERIES CANNOT (2026-09-20).
    # A constant `R_goal` reads identically whether the residual is never recomputed, correctly
    # static, or LIVE AND INSENSITIVE -- recomputed each cycle over moving values while the
    # satisfier count does not move. Measured on ls20: the agent drove `o20.w` from 40 to 27 and
    # the series held 0.7143 to four places. A ratio hides that; a numerator and a denominator
    # do not. Optional out-param so no caller's signature changes.
    if counts is not None:
        counts.update(scope=len(vals), resolved=len(seen),
                      satisfied=sum(1 for v in seen if v))
    if not seen:
        return None
    return sum(1 for v in seen if v) / len(seen)


@dataclass
class Config:
    # anchor: grounded in the toy world's own falsifier. `world._ladder` is four atoms
    # deep -- `dbl . neg . inc . wrap` -- which is PAST this depth, so it is unreachable
    # in atoms and reachable in units once `swing` settles. Depth 3 is what makes the
    # chunking claim falsifiable; at 4 the falsifier would be reachable without chunking.
    max_depth: int = 3
    # anchor: specified, and it bounds the wrong quantity -- stated rather than fixed
    # here. It caps CLOSURE YIELDS in `enumerate_closure`, and the search's work is yields
    # times operand bindings. Measured over 12 worlds: max yields 1884, max tried 4206,
    # and `budget_exhausted` reported zero times. So the depth-3 space is exhaustive here
    # and the declared bound never binds -- while the work exceeded it.
    budget: int = 4000
    # anchor: grounded in the toy world's own exhaustion, as `max_depth` is grounded in its
    # ladder. The toy's depth-3 search over its few operands prices ~13,298 candidates before
    # it finds `dbl.neg.inc.wrap` (measured); this sits just above so the falsifier is never
    # truncated. `budget` bounds YIELDS and the work is yields x operand-binds, so on a dense
    # frame (166 operands) the walk grows unbounded per step -- this bounds THAT axis, which
    # the runaway `budget` cannot.
    work_budget: int = 15000
    mode: str = SPECIFIED
    # SYSTEM 0 (Isaiah, 2026-09-14): motor babbling before means-end -- draw variously until
    # the action-effect map has coverage, then hand to strategy. Off by default; the A/B toggles.
    # **ON -- Isaiah, 2026-09-25.** *"System 0 is always on. It is almost like an UPTAKE VALVE
    # -- if it catches that nuance or attribute, the whole system set RECALIBRATES."* It has
    # been `False` since it was built, so the intake the reviewer calls the ELABORATION GUARD
    # had never once opened. Systems 1 and 2 are both SELECTIVE BY NATURE and neither can notice
    # anything outside its own frame; 0 has no frame, which is what lets it catch the nuance.
    system0: bool = True


@dataclass
class SlotResidual:
    slot: str
    channel: str
    predicted: Any
    actual: Any
    bits: float

    @property
    def mass(self) -> float:
        return self.bits


@dataclass(frozen=True)
class Characterisation:
    """**§15.3's CHARACTERISED RESIDUAL. The corpus specified this and I nearly designed one.**

    *"The whole library is present and reachable. What you cannot do is ask for a primitive by
    NAME -- you get it by DESCRIBING THE GAP IT FITS."* Figure 9's own four keys, and this
    class is them:

        type signature   the TYPES the gap involves
        arity            how many slots it involves
        varies/invariant the residual's own structure
        effect shape     what changed, not what caused it

    **NAME-FREE ON PURPOSE, AND THAT IS THE WHOLE POINT.** `ARC_AGENT` §15.3 keys retrieval by
    *structural distance, not surface similarity*, and slot NAMES are surface: a signature
    carrying `o1.col` matches only the world it came from. **Types transfer; names do not**, and
    transfer is the claim this exists to serve.

    **NOT CALLED `Shape`, DELIBERATELY.** `shape` in this package already means SHAPE-typed grid
    data -- `_shapes_now`, `_as_shape`, the SHAPE atoms. One word over two quantities is `A6i`,
    and this file carries three filed instances of it.
    """

    signature: tuple[str, ...]      # the types of every slot the gap involves, sorted
    arity: int                      # how many slots -- Figure 9 names arity explicitly
    varies: tuple[str, ...]         # types of the slots that MISSED
    invariant: tuple[str, ...]      # types of the slots the residual left alone
    effect: tuple[str, ...]         # per missed slot, in EFFECT terms: over / under / other

    def overlap(self, other: Characterisation) -> int:
        """HOW MUCH STRUCTURE TWO GAPS SHARE. A COUNT, NEVER A RATIO AND NEVER A VERDICT.

        **Isaiah, 2026-09-25: distance is REGIONAL.** *Wherever a threshold is tempting, ask
        whether the right thing is a comparison against local conditions.* So this returns a
        number to RANK BY and no cutoff exists anywhere: *similar* means **more similar than the
        other candidates here**, which is an ordering and needs no figure from anyone.
        """
        return (int(self.signature == other.signature) + int(self.arity == other.arity)
                + int(self.varies == other.varies) + int(self.invariant == other.invariant)
                + int(self.effect == other.effect))


@dataclass
class Report:
    cycles: int = 0
    bound: dict[str, str] = field(default_factory=dict)
    minted: list[str] = field(default_factory=list)
    settled: list[str] = field(default_factory=list)
    owed_import: set[str] = field(default_factory=set)
    abstained: dict[str, dict] = field(default_factory=dict)
    refusals: list[str] = field(default_factory=list)
    demoted: list[str] = field(default_factory=list)
    chain: dict = field(default_factory=dict)
    phases: dict = field(default_factory=dict)
    clocks: dict = field(default_factory=dict)
    retro: list = field(default_factory=list)
    stopped_at_link: str = "1 - perception"


def _where(state: dict[str, int]) -> tuple:
    """A hashable state, so a trial can be located. Two draws of one action from
    the same state are one trial, which is the whole of Q18's defect."""
    return tuple(sorted(state.items()))


def _why(d: dict | None, reason: str) -> None:
    """Name which `None` a None was. Out-param rather than a ledger row because
    `goal_residual` runs per slot per step and a row per call would drown the trace -- only the
    GUARD read records, which is the one place the question is live (F207)."""
    if d is not None:
        d["exit"] = reason


class Agent:
    def __init__(self, env: Any, gam: Gamma, cfg: Config | None = None,
                 led: Ledger | None = None) -> None:
        self.env, self.gamma = env, gam
        # `setdefault`, NEVER ASSIGNMENT: a loaded library carries its books across attempts
        # (`08bb416`) and zeroing them here would silently undo the persistence that makes a
        # dial earnable at all. A key the blob predates simply arrives at 0.
        for _k in BOOKS:
            self.gamma.book.setdefault(_k, 0)
        self.actions = tuple(env.actions())        # asked for, never imported
        # SET HERE AND NOT ONLY IN `retarget`. `_advertised` reads it at the top of every
        # step; it only ever REACHED that read after the set had changed, so the attribute's
        # absence before the first `retarget` was masked by an early return. Feeding the
        # denominator unconditionally is what surfaced it.
        self._last_action: str | None = None
        # AND THE SAME FOR THESE FOUR, ADDED 2026-09-21 AND ALL PUT IN `retarget` ONLY.
        # The comment above records this exact bug once already. A fresh Agent that is read
        # before its first `retarget` raises AttributeError -- which is how `_shape_cache` was
        # caught, by constructing an Agent directly in a measurement instead of through `play`.
        self._guard_exit: str | None = None
        self._gamma_read: dict = {}
        self._held_chains: set[str] = set()
        self._shape_cache: tuple = (-1, None)
        self._contact_seen: set = set()
        self._refuted_slot: dict = {}
        self._move_map: dict = {}
        self._contact_pick = None
        self._s0_target: str | None = None
        self.alphabet = self._alphabets(env)
        self.slot_types = self._slot_types(env)
        self.cfg = cfg if cfg is not None else Config()
        # not `led or ...`: an empty Ledger has len 0 and is therefore falsy
        self.led = led if led is not None else Ledger(mode=self.cfg.mode)
        self.slots = env.slots()
        self.bound: dict[str, str] = {}

        # SYSTEM 2'S CHANNEL -- Isaiah, 2026-09-24. **`bound` IS SYSTEM 1: the term that ACTS.**
        # The contest between kinds was winner-take-all, so an objective that PAID THE BARGAIN was
        # discarded by a cheaper predictor, and `goal_residual` then reported `out_type-not-OBJ` --
        # **a TYPE claim standing in for a DISCARD.** The agent had no want because the want was
        # thrown away, not because none was found.
        #
        # **BOTH ARMS, WITH A RANKING BETWEEN THEM, NOT A SINGLE CHAIR.** The ranking decides which
        # term ACTS; it does not decide which term EXISTS. A verdict that deletes the loser is the
        # wireheading shape he named -- whatever wins an argument becomes the whole of what
        # you want.
        self.wants: dict[str, str] = {}
        self._acts: Counter = Counter()   # System-0 instrument: concrete actions taken per cycle
        # the whole before-state is kept, because an operand is another slot's past value
        self.trace: list[tuple[dict[str, int], str, dict[str, int]]] = []
        self.owed_import: set[str] = set()
        # THIS CYCLE's appearance and disappearance events -- see `_present`. Empty is the
        # normal reading, not a missing one: most cycles change no slots.
        self._came: tuple[str, ...] = ()
        self._gone: tuple[str, ...] = ()
        self.abstained: dict[str, dict] = {}
        self.candidates: dict[str, int] = {}     # term -> cycle accepted, awaiting the ground
        self.settled: set[str] = set()
        self._settled_at_level: set[str] = set()   # the segment's starting line
        self.demoted: list[str] = []
        self.chain = I.Chain()
        self.rank = I.Rank()
        self.gamma.unit_rank = self.rank.key
        self.phases = I.Phases()
        self.clocks = I.Clocks()
        self.pre = I.Preconditions()   # §16.8 sensor 2, fed by the delta
        # HOW MANY ACTIONS TIE AT THE TOP OF `spread`, per discriminate call. The argmax
        # names WHICH action was picked and never says whether anything else scored the
        # same -- and a tie resolved by `self.actions` order is a different finding from one
        # action genuinely discriminating best. `1` is genuine; `>= 2` is tuple order deciding.
        self._ties: Counter = Counter()
        # WHICH MEMBER, AND WHICH GATE DROPPED IT. `sep[a]` is bounded by the number of
        # contingency members -- FOUR (§18.3's table order) -- and BOTH gates drop members, so
        # the argmax is over a very small integer. `sep:1` at 84.5% is exactly what a 0/1 `sep`
        # with ONE contributor produces, and that would make the family the finding rather than
        # the selector. Three outcomes: one passing, several agreeing, several with one
        # dominating -- and only the third warrants a selector repair.
        self._members: Counter = Counter()
        self._passes: Counter = Counter()
        # THE `sep` SHAPE PER CALL, NOT A TOTAL. `passed_per_call` says how many members
        # contributed and cannot say whether they AGREED -- four passing and all marking the
        # same action is unanimity, four marking four is total disagreement, and both read
        # `{4: n}`. Sorted descending so the shape is comparable across boards with different
        # action counts: `(4,0,0,0)` unanimous, `(1,1,1,1)` no separation, `(2,2,0,0)` split.
        #
        # A TRAJECTORY RATHER THAN A COUNTER, because the tie fraction MOVES: 100% ties at ten
        # cycles against 15.5% at 150, so a total describes the end of an episode and hides
        # that early ties are universal -- which is when the agent is choosing what to explore.
        self._sep_log: list = []
        # PER-STEP CACHE FOR `_touching`. `slot_owner()` rebuilds a dict with a `rsplit` per
        # slot on every call, and `_touching` sits in five loops that run per candidate and
        # per history entry -- so it was candidates x history x 120 splits per step, measured
        # at 10s/cycle against a pre-regression whole-episode average of 13s dominated by LATE
        # cycles. `contacts()` was already frame-cached for this exact reason, with the reason
        # in its docstring, and I added an uncached caller into the same class of loop.
        self._touch_cache: tuple | None = None
        # PER-STEP, for `_touching`'s reason: `peers()` rebuilds a dict over every slot and
        # `_group` sits in the same per-candidate loops.
        self._peer_cache: dict | None = None
        self._decomp_cache: tuple | None = None
        # P2. `_record` and `_group` read (slot, state) and NOTHING ELSE -- not the term --
        # while the pricing loop rebuilds a `Ctx` per candidate. Measured: 1,144,007 calls
        # for at most ~235 distinct answers on a six-cycle ls20 run, `_record` 24% of wall.
        #
        # KEYED ON `id(state)` AND THE STATE IS HELD IN THE VALUE, which is what makes the
        # key exact rather than probabilistic: a live reference cannot have its id reused,
        # so `cached is state` either hits the same object or misses. Invalidated at the two
        # sites the other frame caches use -- a new world and a new step.
        self._frame_cache: dict = {}
        # §13.4 wants goal hypotheses held AT ONCE and compared on a TREND, so the scalar has
        # to be kept per slot across steps -- a single reading cannot be shrinking.
        self._disc: dict[str, list[int]] = {}
        # THE WIDE AXIS, KEPT APART FROM THE NARROW ONE. `_disc` is `objective_gap` -- one
        # slot's distance to its nearest satisfying value, measured 0-or-1 on 86 readings across
        # two boards -- and `_res` is `R_goal`, the fraction of a SCOPE that fails. **The
        # selector needs a discrepancy that can be wide to shrink THROUGH**; on a 0/1 gap the
        # only qualifying window ends at 0, which is exactly where there is nothing left to
        # pursue. Two quantities, two dicts, for the reason `refuted` and `refuted_at` are two.
        self._res: dict[str, list[float]] = {}
        # WHICH CYCLE FORMATION WAS LAST ATTEMPTED ON. System 2 now deliberates beside System 1
        # as well as at the fall-through, so without this a cycle reaching both sites would
        # refuse twice and write the gate's reason twice.
        self._planned = -1
        # THE HELD ROUTINE, AS ITS REMAINDER. `advance` hands back what is left and what is
        # left is a Routine, so a behaviour spanning cycles is ONE field -- no program counter,
        # no index into a script, and the thing stored is inspectable as the object it is.
        self.routine: Any = None
        self.routine_for: str | None = None
        # SETTLED ROUTINES -- the ACT space's chunk shelf. A routine arrives here by reaching
        # `done`, which is its guard MET, which is the ground paying. `exhausted` never settles:
        # that ending is the routine's own claim refuted, and shelving it would make a failed
        # plan into a cheap building block.
        self.routines: list = []
        # `routine.Let`'s store. Published by `advance`, read by the caller's `holds`, so the
        # act space keeps its invariant that `routine.py` never evaluates a predicate.
        self.routine_state: dict = {}
        # `(slot, value when the claim was made, step index)`, or None. One at a time: the loop
        # takes ONE action per cycle, so a second claim cannot be outstanding.
        self._popped: dict[str, int] = {}
        # THE SELF-OBSERVATION BOOKS. Facts about THIS AGENT'S OWN PAST, written by the ground.
        # **RECORDS, NOT THRESHOLDS: they decide nothing.** They are what a decision would have
        # to be made FROM, and none of them existed. Isaiah, 2026-09-24: the agent sets its own
        # terms, and a term set from nothing is a guess -- the books are what make it not one.
        #
        # **AND THE DEMOTED ARE KEPT, WHICH IS THE ONE THE GROUND DESTROYS UNRECORDED.** `F327`
        # clears a standing on one miss and the term is gone; whether it would have been RIGHT
        # on the next frame is the counterfactual nobody could read. Kept here, evaluated each
        # cycle, and bounded so a long run does not accumulate forever.

        self._demoted_watch: dict[str, tuple] = {}    # term -> (slot, cycle it was demoted)
        # **THE DIAL'S EVIDENCE.** Cycles between a demotion and the frame that would have
        # vindicated it. Already in CYCLES, which is what a halflife is measured in -- so the
        # agent reads its own observation DIRECTLY and no mapping is chosen by us.

        self._settled_at: dict[str, int] = {}
        self._expect: tuple | None = None
        self._expect_step = 0
        # THE REJECT MEMORY, §18.2's `falsified_ledger` at routine scale. Without it the loop
        # found by re-verification is: mint, exhaust, release, re-mint the identical routine in
        # the same cycle, forever -- **the failure `M2_STANDARD` names in its own words,
        # *looking like the agent planning while it is looping on a bad guard.***
        #
        # **AND IT REUSES `Standing`, WHICH IS THE MECHANISM ALREADY BUILT FOR THIS.** Its own
        # docstring is §18.2's requirement verbatim -- *a term's record against the ground:
        # weighted, clocked, and never a hard ban* -- with a decaying `rejections` float and
        # `REJECTION_HALFLIFE` anchored in `gamma`. **I built a binary dict beside it and called
        # the decay rate underivable, one tick after noting the corpus asks for weighted.** The
        # class is reused; the registry is not, because a routine is not a term and `gamma.
        # standing` is keyed by library name.
        #
        # TWO QUANTITIES, TWO DICTS, for the reason `shape` and `structure` are two keys: the
        # STRENGTH decays on the logical clock, and the SURPRISE THRESHOLD is the goal residual
        # at the moment of refutation. Merging them would make one of the two defeasance routes
        # unreadable.
        self.refuted: dict[tuple, Standing] = {}
        self.refuted_at: dict[tuple, float] = {}
        # THE FAILED-PATH CATALOGUE, AND IT IS THE SAME KEY THE TERM PATH ALREADY USES.
        # Isaiah's BAR ruling: *catalogue and save the failed paths, the salient attributes and
        # the interactions, so each replay retrieves past information and cuts the problem down.*
        # `refuted` above cannot be that, and the boundary comment says why in its own words --
        # the reject key is `(slot, actions, guards)` and two of those three REGENERATE, so it
        # is cleared at every level and nothing crosses. §15.3's retrieval is already built for
        # TERMS (`retrieval.characterise` -> `fits` -> `retrieve`, keyed on TYPES, ordering and
        # never excluding). **This gives the routine path that key.** Not a second mechanism:
        # `_gap_key` is the name-free half of the gap `characterise` already returns.
        self.paths: dict[tuple, dict] = {}
        self._digests: dict[str, frozenset] = {}
        self.agency = I.Agency()       # §16.8 sensor 3, a per-step read
        self.term = I.Termination()    # 2d / §20.1, latching and asymmetric
        self.retro: list[dict] = []
        # parked residuals survive a level boundary; the trace does not. So a parked
        # record carries its OWN evidence -- retrospective re-attribution is free in
        # actions and is not free in memory.
        self.parked: dict[str, dict] = {}
        self.level = 0
        self.drive = Drive()
        self.cycle = 0
        self._last_mass: dict[str, float] = {}
        self._prev_gap: dict[str, int] = {}
        self._seen_gaps: list[Characterisation] = []
        self._gap_delta: dict[str, int] = {}
        # THE INTEGRAL IS READ, NEVER REDUCED. Every step's surprise is added and nothing
        # subtracts, so a drive that learned to make the number go down would be
        # forgetting a surprise rather than explaining one. Monotone by construction
        # because correction_bits is never negative.
        self._integral = 0.0
        # `DISCOVERY`'s SECOND QUANTITY, and the corpus calls it *the aim and the currency*.
        # The integral is every surprise ever; this is surprise NOT YET EXPLAINED, and only
        # `explain` reduces it -- understanding a surprise afterwards does not unmake having
        # been surprised. PER SLOT because R is, and a single number cannot say WHERE the
        # surprise is; `outstanding()` sums on read, so the total is a reading rather than
        # the storage.
        self._outstanding: dict[str, float] = {}
        self._stood: list[tuple[str, str, bool]] = []
        # slots whose accumulated residual is zero: nothing to compress, so nothing to
        # mint. The instruction is per slot and the wheel is not, so they queue here
        # until a probe actually takes the wheel and can be recorded against them.
        self._starved: set[str] = set()
        self._promotions: list[tuple[str, dict, dict]] = []
        self._said_never_live = False
        # THE INSTRUMENT IN USE. `full` is the finest the env offers, so the agent
        # starts where nothing is lost and INWARD has nowhere to sharpen to -- which is
        # the honest default until step 7 exists to move it. Choosing a coarse one here
        # would be picking the agent's perception for it.
        self._view: tuple = ("full", dict)
        self._prev_bet: str | None = None
        self._prev_pred: dict[str, int] | None = None
        self.refusals: list[str] = []

    def retarget(self, env: Any, level: int, how: str = ADVANCE) -> None:
        """Move to the next level. Gamma and standing carry; the trace and the bindings
        do not, because slot names mean nothing across a boundary.

        Everything still owed is parked WITH its history, which is the only way a term
        minted three levels later can be tested against it -- the mint will never revisit
        it, so this is the sweep's one irreplaceable job."""
        for slot in sorted(self.owed_import):
            rec = dict(self.abstained.get(slot, {}))
            rec.update(slot=slot, level=self.level, hist=self.history(slot),
                       slots=list(self.slots))
            self.parked[f"L{self.level}:{slot}"] = rec
        # NO BOUNDARY REVERT. Reverting unpromoted terms to candidate here was built,
        # measured on two independent panels, and cost opportunity, uptake and carried in
        # both -- with nothing measurable bought: the target did not move, the side
        # effect did not replicate, and the rate difference was 1.3 SE.
        #
        # The diagnosis is why it stays out. Settled-ness was never the property that
        # separates a mechanism from a term that closed a slice -- all ten wrong terms in
        # the false-mint read fired the held-out test and survived it -- so gating a
        # boundary on it removed good terms along with bad. `promote` remains and still
        # records: shadow-then-echo does fire on a ladder, and that is worth keeping
        # observable for whatever gates on it next.
        # 2e. WHICH ENDING, recorded with its reading. §21.5: reset and advance produce
        # the SAME residual spike and mean OPPOSITE things -- known board versus unknown --
        # so the kind is carried rather than inferred, and the frame keeps `full_reset` and
        # `levels_completed` so it survives COMPETITION collapsing the two.
        #
        # RECORDED, NOT YET CONSUMED. What reads this is boundary demotion, which is its own
        # item: the revert was withdrawn because settled-ness was the wrong gate, and §21.5
        # proposes a different one. Building the consumer here would be the same mistake in
        # the other direction.
        # THE TENTH THING CLEARING HERE, and it is the world's rather than the loop's.
        # The agent cannot see a board, so anything a colour was bound to lives on the far
        # side -- but the BOUNDARY is the loop's event, so the trigger belongs here with the
        # nine. A world with no episode bindings records that it had no hook: absence stated,
        # never assumed.
        drop = getattr(self.env, "boundary", None)
        if drop is not None:
            drop()
        self.led.record(self.level, "IMPORT", "@loop", "boundary",
                        env_dropped=drop is not None,
                        reads=("per-episode bindings the WORLD holds -- a colour identity is "
                               "valid only for the episode it was read in, so it drops where "
                               "`bound` and `trace` drop"))
        self.led.record(self.level, "IMPORT", "@loop", "ending", how=how, to_level=level,
                        reads=ENDING_READS.get(how, "unnamed ending"),
                        consumed_by="nothing yet -- boundary demotion is a separate item")
        # §21.3: A COMPLETION IS A SETTLE, AND THE SWEEP IS HOW YOU FIND OUT WHAT CAUSED IT.
        # *A level completes at step 500 and the last action did not cause it -- the
        # trajectory did*, so crediting the final action is the delayed-effects bug at the
        # scale of a whole segment. This credits the SEGMENT: what was bound while it ran and
        # what settled during it, over a RECORDED history, costing no actions.
        #
        # CREDIT ONLY, AND THE OTHER HALF IS ELSEWHERE. §21.4: *crediting without the decay is
        # the incumbency pathology; decaying without the credit throws away the only positive
        # evidence there is.* The decay is boundary demotion, which is its own item and turns
        # on §21.5's event type -- so this row says where the missing half lives rather than
        # leaving a both-and looking finished.
        if how in ("advance", "win"):
            self.led.record(self.level, "SETTLE", "@loop", "credit",
                            settled_here=sorted(self.settled - self._settled_at_level),
                            bound_here=sorted(set(self.bound.values())),
                            over_steps=len(self.trace), how=how,
                            note="the segment is credited, not the last action",
                            decay_half="boundary demotion, its own item -- credit without "
                                       "decay is the incumbency pathology (§21.4)")
        self._settled_at_level = set(self.settled)
        self._touch_cache = None      # a new world invalidates owners and contact alike
        self._peer_cache = None
        self._decomp_cache = None
        self._frame_cache = {}
        self.env, self.level = env, level
        self.slots = env.slots()
        self.actions = tuple(env.actions())       # a new level may advertise differently
        self.alphabet = self._alphabets(env)      # a new level may value slots differently
        self.slot_types = self._slot_types(env)   # and may type them differently
        self.bound, self.trace = {}, []
        self._disc, self._res = {}, {}   # the slots did not survive, nor do their trends
        # AND NEITHER DO THE REFUTATIONS, FOR THE REASON THIS METHOD'S OWN DOCSTRING GIVES:
        # *slot names mean nothing across a boundary.* The reject key is
        # `(slot, actions, guards)` and two of those three are slot names, which REGENERATE --
        # `o1.dcol` on the next level is a different object. **A refutation surviving into that
        # is §18.2's autoimmunity, rejecting something needed, on evidence about something
        # else.**
        #
        # THE SETTLED SHELF IS A DIFFERENT CASE AND STAYS, because something already protects
        # it: every guard is `CAN`-checked at mint, and a guard naming a dead slot reads
        # `unknown`, which the mint refuses. **Checked rather than assumed** -- the shelf needs
        # no rule here precisely because it has one already.
        self.refuted, self.refuted_at = {}, {}
        # AND `self.paths` IS A THIRD CASE AND STAYS, FOR THE REASON THIS BLOCK JUST GAVE.
        # The autoimmunity argument above is entirely about SLOT NAMES regenerating. `_gap_key`
        # holds none -- arity, the TYPES that varied, the target's TYPE, the relation types --
        # so the evidence it carries is about a KIND of situation and not about `o1.dcol`.
        # **Clearing it would be the mirror error**: discarding evidence that does cross, on a
        # rule written for evidence that does not. `retrieval.key_of`'s own note is the same
        # ruling one level down -- *vocabulary permanent, instances transient.*
        self._disproof: dict[str, dict] = {}
        self._last_action: str | None = None   # what may have changed the gating
        self.owed_import, self.abstained = set(), {}
        self._guard_exit: str | None = None   # why the last guard read was unreadable
        self._gamma_read: dict = {}   # did action selection consult Gamma this cycle
        self._held_chains: set[str] = set()   # recipes in the library, per mint call
        self._shape_cache: tuple = (-1, None)   # (cycle, decoder) -- Ctx is built per candidate
        # SYSTEM 0's contact memory is NOT cleared here. The keys are (kind, shape, shape)
        # -- a KIND of situation, which is what `paths` and `_disproof` survive a boundary
        # for. Clearing it would discard evidence that DOES cross, on a rule written for
        # evidence that does not.
        self._contact_pick = None
        self._s0_target = None
        # CLEARED AT RETARGET, unlike `_contact_seen` and `_move_map`: this one is keyed by
        # SLOT NAME, and the slots do not survive a level boundary. Same rule the boundary
        # reset states for `_res` and `_disc`.
        self._refuted_slot: dict = {}
        # THE MOVE MAP SURVIVES A BOUNDARY for `_contact_seen`'s reason: what an action does
        # to the avatar is a fact about the ACTION, not about the slot names of one level.
        self.candidates = {}
        # a new level is a new instrument: the verdict was about the OLD slot set
        self._said_never_live = False
        self._view = ("full", dict)
        self._prev_bet = self._prev_pred = None
        self.drive = Drive()

    # -- step 1 -----------------------------------------------------------------------

    def step_effect(self, before: dict, after: dict) -> frozenset:
        """ONE STEP OF THE TRANSFORMATION TRACE, WITH EVERY ENVIRONMENT LABEL REMOVED.

        *An input produced THESE ATTRIBUTE TYPES CHANGED* -- and nothing else survives:

            the ACTION is anonymous     `ACTION1` is advertised by the environment, and it is
                                        not stable even at home: its meaning shifts within a
                                        level and across levels of one game. So it carries no
                                        identity into the key -- not its name, and not a
                                        learned per-game role either, because there is no
                                        stable per-game meaning to learn
            NAME-FREE                   types, never slot names. `characterise`'s own rule:
                                        *a slot name is an instance and can only ever match
                                        at home*
            COLOUR-FREE                 a COLOUR contributes THAT it changed, never WHAT to

        **The firewall, at the action layer.** The game string, the slot names, the colour
        values and now the action name are all environment labels, all stripped. What is left
        is how the game BEHAVED under the agent's own intervention.
        """
        types = self.slot_types
        return frozenset(types[s] for s in after
                         if s in before and s in types and after[s] != before[s])

    def signature(self) -> frozenset:
        """The game's identity: every effect-pattern this play produced, accumulated.

        **COMPUTED, NEVER READ.** Derived from what the agent perceived under its own actions;
        nothing from the environment's game string reaches it.

        A SET AND NOT A SEQUENCE, because the agent's action ORDER is its own choice and two
        plays of one game differ in it. Whether that is enough to make two plays agree is a
        MEASUREMENT and not a claim -- see the run beside this build.
        """
        return frozenset(self.step_effect(b, a) for b, _, a in self.trace)

    def store_key(self, episode: int, level: int) -> str:
        """`{digest}_{episode}_{level}` -- the story's shape, keyed on what the agent computed.

        **TWO COLLISIONS, AND ONLY ONE IS DETECTABLE. Keeping them apart is the point.**

            HASH collision       two DIFFERENT signatures, one digest. RARE, and CHECKED --
                                 `_digests` holds digest -> signature and the mismatch raises
            SIGNATURE collision  two different GAMES, one signature. EXPECTED, and UNDETECTABLE
                                 BY CONSTRUCTION: five attribute types give 32 effect-patterns
                                 and one game used four, so the space is small and sharing it
                                 is the common case rather than the exception

        **So the signature BUCKETS and does not NAME.** *It identifies a game up to a
        32-pattern equivalence class; `episode` and `level` index within the bucket; and two
        games in one bucket are not separated by this key at all.* **Stated because a key
        described as an identity would have the next reader trust it to distinguish games it
        cannot.**
        """
        sig = self.signature()
        digest = hashlib.sha1(
            repr(sorted(sorted(e) for e in sig)).encode()).hexdigest()[:7]
        seen = self._digests.setdefault(digest, sig)
        if seen != sig:
            # THE DETECTABLE ONE. Never silent: a shared digest over different signatures is
            # the prefix being too short, which is a fact about the prefix and fixable.
            raise ValueError(f"digest collision on {digest!r}: two distinct signatures")
        return f"{digest}_{episode}_{level}"

    def history(self, slot: str) -> list[tuple[dict[str, int], str, int]]:
        """(before-state, action, this slot's after-value) for every recorded step.

        Frames before the slot existed are skipped rather than faulted: a slot that
        arrived mid-episode has no history from before it arrived. BOTH ENDPOINTS are
        required, not just the after-value -- the ARRIVAL frame has the slot in `after`
        and not in `before`, so it is not a transition observation and a term applied to
        it would fault on the missing before-value."""
        return [(b, a, af[slot]) for b, a, af in self.trace if slot in af and slot in b]

    @staticmethod
    def _ops(term: Term, state: dict[str, int]) -> tuple:
        """The operand's value, and §4's whole mechanism sits in the middle three lines.

        THE BRANCH GETS THE RAW SLOT VALUE AS ITS OWN OPERAND, and a bare `Ctx` was the first
        version -- which made the branch INERT. Every `val -> val` atom is identity without an
        operand (`_translate` is `v + c.operands[0] if c.operands else v`), so a branch with
        nothing bound returned exactly what it was given and the tree computed nothing. Caught
        by evaluating it rather than by reading it.

        IT STILL CANNOT RECURSE, and that bound is now structural rather than incidental: the
        branch's operand is a VALUE, never a term, so there is no second branch to descend
        into. Binary tree, depth one, by construction.

        AND AN UNREADABLE BRANCH FALLS BACK TO NO OPERAND, which is not a new failure mode:
        `_translate` is `v + c.operands[0] if c.operands else v`, so an empty tuple is
        already the identity every operand-reading atom takes when nothing is bound.
        """
        if not term.operand:
            return ()
        value = state[term.operand]
        if term.operand_term is not None:
            value = term.operand_term.apply(value, Ctx(operands=(value,)))
            if value is NOT_RESOLVED:
                # `None`, NOT `()` -- RULED 2026-09-21. The docstring above argued an
                # unreadable branch may fall back to "no operand" because that is the
                # identity every operand-reading atom already takes. But the identity is
                # a CLAIM: `_translate` returning `v` asserts no translation happened,
                # where the truth is that nobody could tell. 12.2 forbids exactly that --
                # *a value or an explicit non-reading, never a guess, never a default.*
                # `()` means NO OPERAND; `None` means AN OPERAND THAT CANNOT BE READ, and
                # every evaluating caller turns it into NOT_RESOLVED or unexplained.
                return None
        return (value,)

    def _ingredient_slots(self, ingredient: str) -> tuple | None:
        """INGREDIENT NAME -> THE SLOTS IT ACTUALLY TOUCHES. The join that did not exist.

        **A JUNCTION'S OPERANDS ARE INGREDIENT NAMES (`Rotate`); THE DELTA'S QUANTITIES ARE SLOT
        NAMES (`o0.dcol`). NOTHING CONNECTED THEM**, so a bond test could only have asserted
        *the ingredient `Rotate` came or went*, which has no referent. This is the missing hop,
        and it computes nothing new -- both names already exist and the route between them is
        two lookups.

        `ingredient -> atom` is the normalised join (`945f8da`): the corpus writes `Rotate`, the
        registry writes `rotate`, and matching them case-sensitively is what returned zero.

        `atom -> slots` IS THE BINDING, WHICH IS THE ONLY HONEST ANSWER AVAILABLE. An atom is a
        function and touches nothing by itself; what makes it bear on a slot is that a term
        CONTAINING it is bound there. So the slots are the bound ones whose term names this
        atom -- evidence the agent itself produced, never a declaration about what the atom is
        for.

        **`None`, NOT `()`, WHEN THE INGREDIENT DOES NOT RESOLVE** -- `_ops` established this
        distinction on the same day and for the same reason: `()` says NO SLOTS and `None` says
        I COULD NOT TELL, and a test that reads those alike will settle a junction on an
        absence it never measured.
        """
        atom = _norm_name(ingredient)
        if atom not in {_norm_name(a.name) for a in self.gamma.atoms}:
            return None                       # names nothing this agent holds
        hit = []
        for slot, tname in self.bound.items():
            term = self.gamma.library.get(tname)
            if term is None:
                continue
            if any(_norm_name(a.name) == atom for a in term.atoms):
                hit.append(slot)
        return tuple(sorted(hit))

    def _check_expectation(self, before: dict) -> bool:
        """Did the last step's claim hold? **ABANDON on divergence -- not revise, not re-plan.**

        Returns True when the routine was abandoned, so the caller stops running it.

        **ABANDONMENT IS NOT REFUTATION, and the two must not share a channel.** A refutation
        says *this routine is wrong*; this says *it is not working HERE*. So it is keyed by the
        CONTEXT -- the gap shape the routine was minted against -- and it does not touch the
        rejection ledger, which is what would make a routine that failed on one board unusable
        on every other.

        **THE CURRENCY IS ACTIONS.** The number reported is steps NOT SPENT: what the routine
        still had left when it was dropped, which is exactly what noticing bought.
        """
        exp = self._expect
        if not exp:
            return False
        self._expect = None
        slot, was, idx = exp
        now = before.get(slot, was)
        if now != was:
            return False                      # the claim held; carry on
        saved = Rt.length(self.routine) if self.routine is not None else 0
        self.led.record(self.cycle, "PLAN", slot, "routine_abandoned",
                        reason="expected this slot to change and it did not",
                        # `step_index`, NOT `step`: `led.record`'s own first positional is
                        # `step`, so the obvious name silently shadowed it.
                        step_index=idx, unchanged_at=was, actions_saved=saved,
                        routine=Rt.render(self.routine) if self.routine else None)
        self.routine, self.routine_for = None, None
        return True

    def _delta(self) -> dict:
        """THE FRAME'S DELTA, in the shape `composer.settle` reads.

        **`came` AND `gone` WERE COMPUTED AND NEVER READ.** `_present` assigns `self._came` and
        `self._gone` every cycle -- with a careful comment about clearing them on the no-change
        path so a stale event cannot masquerade as a real one -- and NOTHING IN THE PACKAGE
        CONSUMED EITHER. `composer.NEEDS` names the gap from the other side, in the table's own
        text: *"gone -- a value->null transition, computed in `_present` and UNPUBLISHED"*.

        **THE OTHER FOUR KEYS ARE ABSENT AND THAT IS A STATEMENT, NOT AN OMISSION.** `order`
        (`+`, `→`), `history` (`∥`) and `values` (`⋛`) are computed nowhere, so publishing an
        empty one would let `settle` read *present but undecidable* where the truth is *not
        carried at all*. `settle` distinguishes those in its `None` reasons, and a fabricated
        key would collapse the distinction.
        """
        return {"came": self._came, "gone": self._gone}

    def _read_books(self, before: dict) -> None:
        """THE FOUR BOOKS, read each cycle and recorded against THE SCORE.

        **THEY DECIDE NOTHING.** No policy reads them, no constant is derived from them, and
        none is turned into a dial here. **Isaiah, 2026-09-24: the agent sets its own terms --
        and a term set from nothing is a guess. These are what make it not a guess.**

        **EVERY ONE IS RELATABLE TO THE SCORE, which is not decoration.** The score is the ONE
        thing outside the agent, and without the link the agent could set terms that optimise
        its own bookkeeping -- the single failure the score exists to prevent.

        **AND THE CLOCK IS WHY THEY ARE FOUR AND NOT FORTY.** An episode is 128-309 actions. A
        book that needs 200 cycles to say anything is a book the agent never reads in the time
        it has, so each is counted from cycle ONE and reported with its own denominator -- a
        reader can see immediately whether a quantity has spoken yet or not.

        **THE ROW LAGS BY A CYCLE, AND ON A SHORT RUN IT REPORTS NOTHING -- measured 2026-09-24.**
        This runs at the TOP of the step and the cycle's own minting happens after it, so every
        row describes the state BEFORE that cycle's work. On `vc33` at three cycles the rows read
        `bargain_bounded_out` 0, 0, 0 **while the final book held 14,938.**

        **SO A BOOK ROW IS A LOWER BOUND, NEVER THE TOTAL**, and a reading taken off the last row
        of a short run is not the run's answer -- **read `gamma.book` after the run for that.**

        **AND THE OTHER READINGS WERE SWEPT RATHER THAN LEFT OPEN.** Of the book figures reported
        on 2026-09-24: the BARGAIN counts came off a row and were re-taken (`F350`); the ARRIVAL
        DEPTH histogram also came off a row and is **verified IDENTICAL to the final book** on the
        toy run, because every arrival there precedes the last row; `chunk_reuse` and the gate-1
        tally were read at their write sites and never touched this path. **One corrupted, one
        clean, none left to guess at.**

        **NOT MOVED, AND DELIBERATELY.** `ledger.STEPS` orders `PLAN` before `PERCEIVE`, so a row
        relocated to the end of the step becomes the NEXT cycle's first row -- the step-order
        trap this file already records twice, both times with byte-identical demo output and only
        the exit code moving. **Restructuring the step is a change with its own ruling; saying
        what the row means costs nothing and is true today.**
        """
        # BOOK 2, THE COUNTERFACTUAL: would the demoted term have been RIGHT this frame?
        # `F327` clears a standing on one miss and the term is gone; nothing ever asked what it
        # would have said next. Evaluated against the actual, then released -- one frame of
        # hindsight per demotion, which is all the ground offers before the slot moves on.
        for name, (slot, since) in list(self._demoted_watch.items()):
            term = self.gamma.library.get(name)
            actual = before.get(slot)
            if term is None or actual is None:
                self._demoted_watch.pop(name, None)
                continue
            ops = self._ops(term, before)
            if ops is None:
                self._demoted_watch.pop(name, None)
                continue
            got = self._value_of(term, slot, before,
                                 Ctx(action=None, operands=ops, touching=None,
                                     group=self._group(slot, before),
                                     obj=self._record(slot, before),
                                     shapes=self._shapes_now()))
            if got is not NOT_RESOLVED and got == actual:
                # **VINDICATED, AND THE DELAY IS THE QUANTITY.** How many cycles this agent's
                # own demoted term took to come good -- already in CYCLES, which is what a
                # halflife is measured in. **So the dial reads the observation directly and no
                # mapping is chosen by us.** A rate would have needed a function; this does not.
                self.gamma.vindication.append(self.cycle - since)
                self.gamma.book["demoted_would_have_been_right"] = (
                    self.gamma.book.get("demoted_would_have_been_right", 0) + 1)
                self._demoted_watch.pop(name, None)
            elif self.cycle - since >= 16:
                # RELEASED UNVINDICATED. The bound is OURS and it is substrate -- a watch list
                # that never releases is a leak -- and it is NOT a claim that 16 cycles is long
                # enough to be sure. Counted separately so the two are never summed.
                self.gamma.book["demoted_stayed_wrong"] = (
                    self.gamma.book.get("demoted_stayed_wrong", 0) + 1)
                self._demoted_watch.pop(name, None)

        # **THE AGENT TURNS ITS OWN DIAL.** Not a function of an observation -- THE
        # OBSERVATION. The mean number of cycles its own demoted terms took to come good IS
        # how long a refutation should keep counting for THIS agent on THIS board. Until it
        # has one, `halflife` stays `None` and `gamma`'s seed applies, MARKED UNEARNED below
        # so an unearned value is never mistaken for a decision.
        if self.gamma.vindication:
            self.gamma.halflife = (sum(self.gamma.vindication)
                                   / len(self.gamma.vindication))
        lv = getattr(self.env, "levels", None)
        done, win = lv() if lv else (0, 0)
        self.led.record(self.cycle, "PERCEIVE", "*", "books",
                        # THE SCORE. Every other number here is read against it.
                        score_levels=done, score_target=win,
                        # **DERIVED FROM `self._acts`, NOT A SECOND COUNTER.** I declared
                        # `_acts_total` and never incremented it -- a dead field on its first
                        # run, which is tonight's own pattern. And a second store WOULD have
                        # diverged from `_acts` the way the routine shelf diverged from
                        # `self.routines` earlier: one name, one store.
                        actions_spent=(_spent := sum(self._acts.values())),
                        # **ACTIONS PER ARRIVAL, the fourth book, and it was NAMED AND NOT
                        # BUILT.** I recorded actions SPENT and stopped -- an arrival is a term
                        # landing in the library, which is the sense `_STREAM_WIDEN`'s own abort
                        # criteria already use (*candidates tried rises while ARRIVALS do not*).
                        #
                        # **`None` WHEN NOTHING HAS ARRIVED, never 0 and never the raw spend.**
                        # Zero arrivals makes the ratio undefined, and reporting the spend alone
                        # would read as *cheap* when it means *nothing was bought at any price*.
                        per_arrival=(round(_spent / len(self.settled), 2)
                                     if self.settled else None),
                        # AND THE SAME AGAINST THE SCORE, which is the one that finally matters:
                        # actions per LEVEL. Undefined until a level moves, and saying so is the
                        # reading -- not a zero.
                        per_level=(round(_spent / done, 2) if done else None),
                        settled=len(self.settled), demoted=len(self.demoted),
                        watching=len(self._demoted_watch),
                        halflife=self.gamma.halflife,
                        halflife_earned=bool(self.gamma.vindication),
                        vindications=len(self.gamma.vindication), **self.gamma.book)

    def _narrate_vocabulary(self) -> None:
        """ONCE PER RUN: what the corpus CALLS what this agent can already reach.

        **A READING, NEVER AN INPUT.** It names compositions the agent's own atoms cover; it
        does not select them, price them or bet on them. The skill-map rule applies exactly --
        *the moment it is available beforehand the mechanism has been handed its answer* -- and
        a NAME for a composition the agent could already build hands it nothing it did not have.

        Recorded rather than printed because the ledger is where a claim can be checked later.
        """
        if getattr(self, "_vocab_said", False):
            return
        self._vocab_said = True
        mols = self._molecules()
        # OFFERED TO THE GROUND, not merely held. `settle_tree` walks each junction and asks
        # whether THIS delta decides it; an undecided junction stays UNKNOWN.
        d = self._delta()
        tallies = [composer.settle_tree(m["node"], d) for m in mols]
        # THE JOIN, REPORTED PER INGREDIENT. `None` = names no atom this agent holds;
        # `()` = holds the atom and it is bound nowhere, so it touched nothing this cycle.
        reach = {i: self._ingredient_slots(i) for m in mols for i in m["recipe"]}
        self.led.record(self.cycle, "PERCEIVE", "*", "vocabulary",
                        delta_keys=sorted(d),
                        ingredient_slots={k: (None if v is None else len(v))
                                          for k, v in reach.items()},
                        junctions_decided=sum(t["decided"] for t in tallies),
                        junctions_undecided=sum(t["undecided"] for t in tallies),
                        why_undecided=[w for t in tallies for w in t["why"]][:3],
                        covered=[m["molecule"] for m in mols],
                        # WHAT IT SAYS, not just what it is called -- §12.2, and the whole
                        # reason the tree is held rather than the name.
                        says=[m["says"] for m in mols],
                        expressible=[m["molecule"] for m in mols if m["expressible"]],
                        unknown_junctions=sum(m["unknown_junctions"] for m in mols),
                        inexpressible=[{"molecule": m["molecule"], "says": m["says"],
                                        "why": m["why"]}
                                       for m in mols if not m["expressible"]])

    def _molecules(self) -> tuple:
        """WHAT THE CORPUS CALLS WHAT THIS AGENT CAN ALREADY REACH -- the composer as librarian.

        `composer.candidates` answers *which recipes do my atoms cover*, and until `945f8da` it
        answered ZERO for every possible input: the corpus capitalises ingredients and the
        registry lower-cases atoms, so the join matched nothing. With it normalised the agent's
        own 61 atoms exactly cover ONE molecule -- `Orbit = Rotate ? Translate` -- and partly
        cover fifty.

        **EXACT COVER ONLY.** A partially covered recipe names something the agent cannot yet
        build, and `candidates`' own docstring says whether partial cover is admissible *is a
        ruling, not a parse detail*. Reporting coverage is not the same as claiming it.

        **AND EACH IS MARKED EXPRESSIBLE OR NOT, which is the half that makes this more than a
        lookup.** A recipe's `?` is an UNDECIDED JUNCTION, not a composition operator --
        `composer.light` keeps junctions UNKNOWN on purpose and `settle` returns `None` from
        every branch because no bond test is written (deliberately: *never stub anything that
        would fake a pass*). So a covered molecule is a NAME plus a bond the ground has not
        decided, and whether the term space can even hold it is a separate, checkable question.
        """
        got = getattr(self, "_molecule_cache", None)
        if got is not None:
            return got
        by_norm = {_norm_name(a.name): a
                   for a in self.gamma.atoms}
        out = []
        for m in composer.candidates({a.name for a in self.gamma.atoms}):
            parts = [by_norm.get(_norm_name(i))
                     for i in m["recipe"]]
            # EXPRESSIBLE means a type-valid CHAIN exists over exactly these atoms, in some
            # order. Nothing else in the term space can hold a two-atom molecule today.
            ok = None
            if all(parts):
                for seq in itertools.permutations(parts):
                    if all(seq[i].out_type in seq[i + 1].accepts
                           for i in range(len(seq) - 1)):
                        ok = " . ".join(a.name for a in seq)
                        break
            # **HELD AS THE TREE, NOT AS A LIST OF NAMES.** `candidates` already lights each
            # recipe into a `Bonded` node and the first version of this method threw it away,
            # keeping only the ingredient strings -- so the agent could say WHICH molecule it
            # covered and could not hold the thing itself.
            #
            # **APPLICABILITY IS STATED, NOT SILENTLY ABSENT.** A molecule cannot be applied
            # today and the reason is structural rather than missing work: its junction is
            # UNKNOWN, and `composer.settle` returns `None` from every branch BY DESIGN because
            # a real-looking bond test there faked a pass and was removed. **An unknown bond is
            # an honest hypothesis; a guessed one is a meaning we supplied.** So this records
            # NOT_RESOLVED's reason at the site rather than leaving a caller to discover it.
            js = composer.junctions(m["node"])
            out.append({"molecule": m["molecule"], "recipe": m["recipe"],
                        "expressible": ok, "node": m["node"],
                        "says": composer.render_node(m["node"]),
                        "length": composer.node_length(m["node"]),
                        "unknown_junctions": sum(1 for b, _ in js if b == composer.UNKNOWN),
                        "applicable": False,
                        "why": "junction UNKNOWN -- no bond test is written, deliberately"})
        self._molecule_cache = tuple(out)
        return self._molecule_cache

    def _trees(self, cand, bind, g):
        """The TREE variants of one flat candidate -- `f<g(s)>` for each branch atom.

        Empty unless the outer atom actually READS an operand and one is bound: a branch feeds
        the operand arm, so with nothing to feed it the tree is the flat term with a longer name.
        """
        if bind is None or not cand.reads_operand:
            return ()
        return tuple(Term(cand.atoms, operand=bind, guard=g, operand_term=br)
                     for br in self._branches())

    def _branches(self) -> tuple:
        """The one-atom terms that may sit on a term's OPERAND arm -- §4's second chain.

        **`idn` IS EXCLUDED AND THAT IS THE WHOLE FILTER.** `_ops` hands the branch the raw slot
        value as its own operand, so `idn(s)` returns `s` and `f<idn(s)>` is `f<s>` spelled
        longer -- a distinct NAME for an identical computation, which is the one thing that
        makes a closure grow without reaching anything. Every other `val -> val` atom is
        operand-reading (`_translate` is `v + c.operands[0]`), so it computes something the flat
        binding could not say.

        **DERIVED FROM THE REGISTRY, NOT LISTED.** A hardcoded pair would go stale the first
        time an atom is added, and the staleness would present as nothing.
        """
        got = getattr(self, "_branch_cache", None)
        if got is None:
            got = tuple(Term((a,)) for a in self.gamma.atoms
                        if a.in_type == "val" and a.out_type == "val" and a.name != "idn")
            self._branch_cache = got
        return got

    def _narrate_placements(self) -> None:
        """The encounter half's reading. **`multi` is the mid-game colour change, counted.**"""
        fn = getattr(self.env, "placements", None)
        if fn is None:
            return
        p = fn()
        self.led.record(self.cycle, "PERCEIVE", "*", "placements",
                        distinct=p["distinct"], changed=len(p["multi"]))

    def _narrate_matches(self) -> None:
        """The tracker's own certainty, per step. **Fixture-readable, and that is the point.**

        A store whose only consumer is another unbuilt phase is silent with extra steps, so
        this half of the pair store reads NOW: *how was identity established this frame, and
        how certain was the match.* **`overlap` with a high IoU is a confident match; a low one
        is marginal; `shape` means overlap was ZERO and sensor 5 carried the identity across a
        move; `birth` means nothing carried it.**

        WHAT THIS IS NOT: the relational-history half -- *does keeping pair history improve
        prediction* -- which means *does it PAY*, and the fixture pays nothing. That half waits
        on a payable board; this one does not.
        """
        fn = getattr(self.env, "matches", None)
        if fn is None:
            return
        m = fn()
        if not m:
            return
        by = Counter(r for r, _ in m.values())
        scores = [s for r, s in m.values() if r == "overlap"]
        self.led.record(self.cycle, "PERCEIVE", "*", "matches",
                        routes=dict(sorted(by.items())), n=len(m),
                        min_overlap=round(min(scores), 4) if scores else None)

    def _narrate_cascade(self) -> None:
        """The cascade's shape, per step. **A one-frame response is a READING, not silence.**

        §16.3's stack is the mechanism evidence the endpoint erases, and *how many frames came
        back* is the first thing it says. **One frame means this board has no cascade** -- which
        is a per-game capability fact, measured rather than assumed, and the reason Seam 9
        conditions the animation claim: `g50t` carries 7 or 9 on 39% of responses and `ls20`
        carries one, always.

        THE ORDERING IS THE PAYLOAD WHEN THERE IS ONE. Consecutive sub-frames give *what
        changed between them*, which is the within-step order -- and the causality tracker that
        would COMPOSE from it is not built, so this publishes and records rather than explains.
        """
        casc = getattr(self.env, "cascade", None)
        if casc is None:
            return
        frames = casc()
        steps = []
        for a, b in zip(frames, frames[1:], strict=False):
            try:
                steps.append(sum(1 for r, row in enumerate(a)
                                 for c, v in enumerate(row) if b[r][c] != v))
            except (TypeError, IndexError, KeyError):
                return
        self.led.record(self.cycle, "PERCEIVE", "*", "cascade",
                        frames=len(frames), within_step=steps)

    def _narrate_order(self) -> None:
        """Layer 2's whole output: the order was USED and is SAID, and nothing keeps it."""
        ro = getattr(self.env, "read_order", None)
        if ro is None:
            return
        order, pattern = ro()
        self.led.record(self.cycle, "PERCEIVE", "*", "read_order",
                        pattern=pattern, first=order[:3], n=len(order))
        md = getattr(self.env, "mode", None)
        if md is not None:
            m = md()
            self.led.record(self.cycle, "PERCEIVE", "*", "mode",
                            board=m["board"], by=m["by"],
                            n_embodied=sum(1 for v in m["per_locus"].values()
                                           if v == "embodied"),
                            n_locus=len(m["per_locus"]))

    def _record(self, slot: str, state: dict) -> dict | None:
        """The slot owner's object record, REASSEMBLED from `state`. One function, every site.

        **NOTHING IS STORED.** `_decomposed` publishes exactly the keys `_extract` reads, so
        the eight values a record is read FOR are in the flattened state already -- the
        flattening scattered the object, it did not destroy it. And because history stores the
        same shape, the same call works on a replayed state as on the live one.

        ONE FUNCTION ON PURPOSE. Two assemblers could drift, and a live/historical mismatch is
        exactly the defect `Ctx.touching` carries.
        """
        key = ("rec", slot, id(state))
        hit = self._frame_cache.get(key)
        if hit is not None and hit[0] is state:
            return hit[1]
        if self._decomp_cache is None:
            own = getattr(self.env, "slot_owner", None)
            att = getattr(self.env, "attribute_of", None)
            shp = getattr(self.env, "shapes", None)
            self._decomp_cache = (own() if own else {}, att() if att else {},
                                  shp() if shp else {})
        owners, attrs, shapes = self._decomp_cache
        mine = owners.get(slot)
        if mine is None:
            self._frame_cache[key] = (state, None)
            return None
        rec = {attrs[s]: v for s, v in state.items()
               if owners.get(s) == mine and s in attrs}
        if not rec:
            self._frame_cache[key] = (state, None)
            return None
        # THE STRUCTURE BESIDE THE LABEL, NEVER IN PLACE OF IT. `shape` stays the published
        # id because that is what `Ctx.group` and every equality comparison hold; swapping in
        # the frozenset would compare a set against a table of ints and read FALSE in silence.
        # Two quantities, two keys -- check 5, at the one site where merging them is tempting
        # because they name the same thing.
        cells = shapes.get(rec.get("shape"))
        if cells is not None:
            rec["structure"] = cells
        # SHARED, AND EVERY CONSUMER IS READ-ONLY -- checked rather than assumed: the eight
        # `_extract` atoms, `_area`, `_centroid` and `_touch_n` all `.get`/index and none
        # assigns. A mutating consumer would make this a defect, not a speedup.
        self._frame_cache[key] = (state, rec)
        return rec

    def _group(self, slot: str, state: dict) -> tuple:
        """The outer stream for one slot: this attribute's values on the other objects."""
        key = ("grp", slot, id(state))
        hit = self._frame_cache.get(key)
        if hit is not None and hit[0] is state:
            return hit[1]
        if self._peer_cache is None:
            fn = getattr(self.env, "peers", None)
            self._peer_cache = fn() if fn is not None else {}
        out = tuple(state[p] for p in self._peer_cache.get(slot, ()) if p in state)
        self._frame_cache[key] = (state, out)
        return out

    def _touching(self, slot: str) -> tuple[str, ...]:
        """§12.3 sensor 8's second operand, resolved for one slot. Mirrors `_bindings`' read:
        the domain owns both `slot_owner` and `contacts` and the loop only asks.

        BEFORE-STATE. `contacts()` is frame-cached and invalidated on `step`, so this is the
        contact set the action has not yet changed -- which is what keeps `Ctx` free of the
        outcome and the tautology guard satisfied by absence."""
        if self._touch_cache is None:
            touch = getattr(self.env, "contacts", None)
            self._touch_cache = (self._slot_owners(self.env),
                                 touch() if touch is not None else None)
        owners, adj = self._touch_cache
        if adj is None or not owners:
            return ()
        return tuple(sorted(adj.get(owners.get(slot), ()) or ()))

    @staticmethod
    def _applies(term: Term, state: dict[str, int]) -> bool:
        """Whether this term can be evaluated on this frame at all.

        A term reading an operand cannot be applied where that operand did not exist,
        which happens the moment a slot arrives mid-episode and something binds to it.
        INAPPLICABLE IS UNEXPLAINED, and every caller charges it as such: dropping the
        frame instead would let a term evaluable on half a history look like a perfect
        explainer, and evaluating it as if unary would silently change what it says.
        """
        return not term.operand or term.operand in state

    def _value_of(self, term: Term, slot: str, state: dict[str, int], ctx: Ctx):
        """A term's PREDICTED SLOT VALUE -- the edge from a term to a number, in one place.

        **IT WAS IN `_predict` ONLY, AND THAT MADE AN OBJECTIVE UNPRICEABLE.** `_predict` is
        the BET; `_left`, `_residual_obs` and `_cannot_pay` are the PRICE, and all three called
        `term.apply` directly. So a `WANT` was BET through `objective_step` and PRICED as its
        own truth value -- 0 or 1 against a slot whose alphabet is 14. **The objective arm
        could never pay, on any board**, and the failure presented as *the other stream fielded
        nobody*, which reads as a fair contest lost.

        Measured on the two-arm board: `any_same . all` on `o1.col` predicts the true next
        value EXACTLY and priced as unexplained on every step.

        One function, four callers, for `_record`'s reason -- a bet and a price that disagree
        about what a term MEANS is not a disagreement any test names.
        """
        if getattr(term, "out_type", "val") == OBJ_TYPE:
            ordered = self.slot_types.get(slot) in ORDERED_TYPES
            def _sat(v: int) -> bool | None:
                r = term.apply(v, ctx)
                return None if r is NOT_RESOLVED else bool(r)
            return objective_step(_sat, state[slot], ordered, self.alphabet[slot])
        return term.apply(state[slot], ctx)

    def _predict(self, slot: str, state: dict[str, int], action: str) -> int | None:
        """`None` is THE INSTRUMENT COULD NOT READ, and it is not a prediction of anything.

        TWO ARMS, ONE RULE. A `val` term IS the prediction; an `OBJ` term is a WANT, and what
        wanting predicts is `objective_step`'s. The type decides, and both facts it reads --
        `out_type` and `slot_types` -- are already here.
        """
        term = self.gamma.library[self.bound.get(slot, IDN)]
        # AND AN UNREADABLE OPERAND IS AN INAPPLICABLE TERM -- `_applies` already says so
        # ("cannot be applied where that operand did not exist"), and a COVERED object is
        # absent for exactly that reason. `_left` and `_residual_obs` consult it and the
        # three evaluating callers did not. None here is the documented non-reading, and
        # NOT an empty operand tuple, which would make `_translate` return `v` unchanged
        # and thereby assert no translation happened.
        if not self._applies(term, state):
            return None
        ops = self._ops(term, state)
        if ops is None:
            return None
        ctx = Ctx(action=action, operands=ops,
                  touching=self._touching(slot), group=self._group(slot, state),
                  obj=self._record(slot, state), shapes=self._shapes_now())
        got = self._value_of(term, slot, state, ctx)
        return None if got is NOT_RESOLVED else got % self.alphabet[slot]

    def _invent(self, slot: str, licence: dict, hist: list) -> None:
        """ITEM 7's CONSUMER. **The agent's own recorded abstention IS the atom's definition** --
        the reviewer's ruling, 2026-09-22, and it deliberately authors no pattern language:
        *no abstraction is chosen; the agent's failure record is the content.*

        The delta it observed and could not compose, as a function: **the recorded before-value
        maps to the recorded after-value, and everything else ABSTAINS.** Literal on purpose --
        the reviewer: *if that turns out to be too literal to ever match twice, THAT is a
        finding about the derivation rule, and it is the agent's own record that produced it.*

        **THE NAME IS ARBITRARY AND CARRIES NO DESCRIPTION.** A name like `moved_right` would be
        me naming the agent's concept for it; the identity is the recorded delta, and the atom
        is found by its behaviour rather than read off its label. **`val -> val`, so it can be
        composed from the start** -- and with an ordinary `Standing`, no head start.
        """
        obs = self._residual_obs(slot, self.gamma.library[self.bound.get(slot, IDN)], hist)
        pairs = {}
        for st, _a, v in obs:
            was = st.get(slot)
            if was is not None and v is not None and was != v:
                pairs[was] = v
        if not pairs:
            return                      # nothing observed to invent FROM. Not a failure.
        name = f"inv{len(self.gamma.invented)}_{self.cycle}"

        frozen = dict(pairs)

        def fn(v, _c):
            # closed over, not a mutable default -- B006, and the map must not be
            # reachable for edit from a call site either way
            got = frozen.get(v)
            return NOT_RESOLVED if got is None else got

        lic = dict(licence)
        # THE RECORDED DELTA TRAVELS WITH THE LICENCE. Reviewer, 2026-09-23, route 2: persist
        # the observation and RE-INVENT on load, rather than writing the function. The pairs
        # are DATA the agent recorded, so a library file carrying them is not a second producer
        # of the vocabulary -- it is the same evidence that licensed the atom the first time.
        # Keys are stringified because this round-trips through JSON.
        lic["delta"] = {str(k): v for k, v in pairs.items()}
        lic["observed"] = len(pairs)
        lic["slot_type"] = self.slot_types.get(slot)
        if self.gamma.invent(name, fn, "val", "val", lic):
            self.led.record(self.cycle, "MINT", slot, "invent", term=name,
                            origin=INVENTED, observed=len(pairs),
                            verdict=licence.get("verdict"),
                            note="the level below TRIED AND COULD NOT: composition abstained "
                                 "with this verdict, and the recorded delta is the definition")

    def _standing(self, slot: str) -> None:
        """HELD AND CITED ARE TWO ROWS, not one. A candidate may be held -- bound, and
        driving the bet, which is the only way it ever accumulates the held-out evidence
        that settles it -- and it may not be cited. The bet at step 1 IS derived from the
        bound term, so this is where the distinction is either taken or lost, and it was
        being lost: nothing in the record said which of the two was happening.

        READ HERE, WRITTEN AT STEP 6. `cite` is a PROMOTE-step event, so writing it from
        step 1 put a ROUTE row after a PROMOTE row inside the cycle and the gate refused
        the record. The settled-ness has to be read at the bet, though -- a term that
        settles later in this same cycle was still a candidate when the bet stood on it.

        An atom is exempt: the ground never owed anything for a primitive, so there is
        nothing for it to have settled.
        """
        name = self.bound.get(slot)
        if name and not self.gamma.is_atom(self.gamma.library[name]):
            self._stood.append((slot, name, self.gamma.is_settled(name)))

    def _promote(self) -> None:
        """Step 6: what step 1 stood on, and what the sweep earned."""
        for name, shadow, echo in self._promotions:
            if self.gamma.is_primitive(name):
                continue
            self.gamma.promote(name, shadow, echo)
            self.led.record(self.cycle, "PROMOTE", echo["slot"], "promote", term=name,
                            primitive=True, shadow=shadow, echo=echo,
                            verdict="closed a residual recorded before it existed, "
                                    "on a slot it was not minted for")
        self._promotions.clear()

        for slot, name, settled in self._stood:
            if settled:
                self.led.record(self.cycle, "PROMOTE", slot, "cite", term=name,
                                allowed=True, via="bound: it drove this step's bet")
            else:
                self.led.record(self.cycle, "PROMOTE", slot, "hold", term=name,
                                status="candidate", asked=[name, slot], ground_said=False,
                                via="bound and unsettled: held, and not cited")
        self._stood.clear()

    def _round_trip(self, t_a, before: dict[str, int]) -> float:
        """R_T in bits: THE GAP BETWEEN `x` AND `T_E(T_A(x))`, per §16.1 and §0.3.

        Send it up, bring it back, charge what came back wrong. `T_E` is the coarse value
        taken literally -- the concretisation the view contract already implies -- so the
        extensive law `x <= T_E(T_A(x))` holds and the gap is non-negative by construction
        rather than by hope.

        The arithmetic is `round_trip_gap` at module level, so the loop and anything
        scoring a view share ONE implementation rather than two that can drift.
        """
        return round_trip_gap(t_a, before, self.alphabet)

    def _cause(self, slot: str, bits: float) -> str:
        """Which of the three a reading has. Every branch is read off state the loop
        already holds -- no new measurement, and no branch on the slot's identity."""
        if bits > 0.0:
            return GENUINE               # not a low reading; the question does not arise
        if len(self.trace) < 2:
            return SLICE_TOO_SMALL       # nothing has been held out yet, so nothing held
        if slot in self.owed_import:
            # THE SLOT OWES AND THIS STEP READ ZERO. The residual is known live, so the
            # zero is what this step failed to deliver and not the model being right.
            # It is the same distinction OWES makes at step 2, on the row rather than
            # in the routing.
            return CHANNEL_CLOSED
        return GENUINE

    def _action6_coord(self, slot: str | None, before: dict[str, int]) -> tuple[int, int] | None:
        """F28: the coordinate for a positioned action, chosen from PERCEPTION -- the object of the
        given slot, at its own perceived row/col. Returns (x=col, y=row) or None when the object has
        no position slots (no spatial basis, so the action stays unpositioned rather than noise)."""
        if not slot:
            return None
        obj = slot.rsplit(".", 1)[0] if "." in slot else slot
        col, row = before.get(f"{obj}.col"), before.get(f"{obj}.row")
        if col is None or row is None:
            return None
        return int(col), int(row)

    def perceive(self, action: str,
                 coord: tuple[int, int] | None = None) -> dict[str, SlotResidual]:
        before = self.env.observe()
        # A BET CAN ONLY BE MADE ON A SLOT THAT WAS THERE. With perception the slot set can
        # move WITHIN a step -- an object dies between the bet and the reading -- and
        # `_present` only catches that at step boundaries. So the bet is over `before`.
        betting = [s for s in self.slots if s in before]
        pred = {s: self._predict(s, before, action) for s in betting}
        # A SLOT THE BOUND TERM CANNOT READ IS NOT BET ON. §12.2's non-reading has to reach
        # somewhere that acts on it, or it is a sentinel that propagates into a shrug.
        for s in [s for s in betting if pred[s] is None]:
            self.led.record(self.cycle, "PERCEIVE", s, "unread", of=(s,),
                            bound=self.bound.get(s, NO_CHANGE),
                            reads=("the bound term returned no reading, so no bet is made and "
                                   "no prediction error is claimed on this slot"))
        betting = [s for s in betting if pred[s] is not None]
        _, deg_before = self.env.objective()
        if coord is not None:
            self.env.step(action, coord[0], coord[1])   # F28: positioned, coord from perception
        else:
            self.env.step(action)
        after = self.env.observe()
        name, deg_after = self.env.objective()

        res: dict[str, SlotResidual] = {}
        for s in betting:
            # A SLOT THAT VANISHED UNDER THE BET IS UNEXPLAINED, not absent. The object was
            # there when the bet was made and is gone now, which is a full code's worth of
            # correction -- and `death only on evidence` means it went because its cells were
            # taken, so the disappearance is a reading rather than a gap. Same rule as
            # `_applies`: missing is charged, never skipped.
            gone = s not in after
            actual = pred[s] if gone else after[s]
            bits = (math.log2(self.alphabet[s]) if gone
                    else correction_bits(pred[s], actual, self.alphabet[s]))
            r = SlotResidual(s, TRANSITION, pred[s], actual, bits)
            res[s] = r
            # from_value is the input the bet was computed from, and it is the whole
            # difference between a bet on the BELIEF and one on the observation -- the
            # second has no model that could be wrong. It was always `before[s]`; it was
            # just never on the row, so nothing could tell the two apart.
            self.led.record(self.cycle, "PERCEIVE", s, "bet", channel=TRANSITION,
                            of=(s,),
                            from_value=before[s], predicted=pred[s], actual=actual,
                            **({"vanished": True} if gone else {}),
                            mass=r.bits, cause=self._cause(s, r.bits),
                            # NOT `IDN`: an unbound slot rests on a persistence prior,
                            # and recording it as a term made 104 of 110 staleness
                            # readings noise. `_predict` still falls back to `idn`.
                            bound=self.bound.get(s, NO_CHANGE),
                            **({"disproof": self._disproof[s]}
                               if s in self._disproof else {}))
            self._standing(s)

        # the reward channel: on the figures, and reported here. Its remedy is the
        # composition of actions, which is not built -- so it is recorded, not actioned.
        # a zero here is degree == 1.0: the objective is met and there is genuinely
        # nothing owing on this channel. Not a channel that failed to deliver.
        # THE REWARD CHANNEL IS NOT R, SO IT IS NOT `mass`. `1 - degree` where degree
        # is hit/len(slots) is a SCORE OVER THE WHOLE BOARD: how well the objective is
        # met, not a gap between a prediction and an outcome at a slot. R is always a
        # slice, and a quantity that cannot be sliced is not R -- keying it `mass` was
        # the conflation, and declaring `of` honestly is what exposed it.
        #
        # Per-slot reporting would not repair this. Dividing a global score by slot
        # manufactures a slice rather than finding one, which is the same defect
        # installed deliberately, so the contract keeps returning one scalar.
        shortfall = round(1.0 - deg_after, 4)
        self.led.record(self.cycle, "PERCEIVE", "@objective", "bet", channel=REWARD,
                        objective=name, degree=round(deg_after, 4),
                        from_value=round(deg_before, 4), actual=round(deg_after, 4),
                        shortfall=shortfall,
                        moved=round(deg_after - deg_before, 4))
        self._route_reward(deg_after, deg_after - deg_before)
        # the bracket channel: this env defines no coarse view, so it is inert. The
        # cause was already here and it was in prose -- `inert=...` says CHANNEL_CLOSED
        # in a sentence, on a row that then reported cause=None. The taxonomy is the
        # field; the sentence stays because it names WHICH channel and why.
        # ASKED, NOT ASSERTED. This row used to say `env.transform() is None` in a
        # string and the loop never called it -- so a world that DID define a coarse view
        # would have had the channel reported closed anyway, which is a cause stated
        # without being observed. The contract member is now read.
        #
        # An explicit null, not a missing field: with no coarse view there is no value
        # this bet could have been computed from. Those are different rows.
        coarse = self.env.transform()
        if coarse is None:
            self.led.record(self.cycle, "PERCEIVE", "@bracket", "bet", channel=BRACKET,
                            of=("@bracket",), from_value=None, actual=None,
                            mass=0.0, cause=CHANNEL_CLOSED, coarse_view=False,
                            inert="env.transform() returned None; no coarse view defined")
        else:
            # R_T IS A READING NOW. It is the round-trip loss of the view the agent is
            # ACTUALLY USING -- `full` until INWARD exists, where it is measured to be
            # zero rather than assumed to be. The offered alternatives are reported once
            # per level, not per step: the set does not change within one.
            # ALWAYS MEASURED NOW. The `measured` flag guarded a capped sweep, and with
            # the gap there is nothing to cap -- so the flag and its `is not the same as
            # small` caveat are gone rather than left as a branch that cannot fire.
            rt = self._round_trip(self._view[1], before)
            self.led.record(self.cycle, "PERCEIVE", "@bracket", "bet", channel=BRACKET,
                            of=("@bracket",), from_value=None, actual=None,
                            mass=round(rt, 3), cause=GENUINE,
                            coarse_view=True, view=self._view[0])
        # §16.8 SENSOR 3. Which slots moved under THIS action, so the control mode is a
        # contingency read rather than a label -- §16.2: it blends mid-game, so it is
        # detected per step and never used to name the game.
        self.agency.note(action, {s for s, r in res.items() if r.mass > 0}, sorted(res))
        self._integral += sum(r.mass for r in res.values())
        for _s, _r in res.items():
            self._outstanding[_s] = self._outstanding.get(_s, 0.0) + _r.mass
        live = any(r.mass > 0 for r in res.values())
        self.drive.note_step(live)      # once per step: SUPPORT is over slots, not per slot
        self.chain.note_diff(live)
        self.trace.append((before, action, after))
        self.gamma.tick = len(self.trace)
        self._prev_pred = pred
        self._last_mass = {s: r.mass for s, r in res.items()}
        self._note_progress(after)
        self._note_gap_shape(res)
        return res

    def _route_reward(self, degree: float, moved: float) -> None:
        """The reward channel is a channel of R, so the boundary diff sorts it too.

        It is routed and diagnosed here; its remedy -- composing actions that advance the
        objective -- is not built, and the entry says so rather than going silent.
        """
        self.drive.note_score(moved > 0)
        if degree >= 1.0:
            b, why = HELD, "not novel: the objective is satisfied, nothing owed"
        elif self.cycle < 2:
            b, why = NOVEL, "not mechanism: too little history on the objective"
        elif moved > 0:
            b, why = REBIND, "not mechanism: the current approach advanced the degree"
        else:
            b, why = MECHANISM, "not rebinding: nothing in the library advances the degree"
        self.led.record(self.cycle, "ROUTE", "@objective", "route", bin=b, why_not=why,
                        channel=REWARD, degree=round(degree, 4),
                        remedy="deferred: composition of actions is not built at agent scale")

    # -- step 2 -----------------------------------------------------------------------

    def _delta_narrowed(self, others: list, robs: list) -> list:
        """ARM L's operand bound, as ONE rule serving BOTH sites that walk the slot set.

        The slots whose value actually MOVED in the frames where the bound term was wrong --
        read off `self.trace`'s own before/after pairs, matched to the residual's observations
        by the IDENTITY of the before-state, which is the same object the trace holds. Contact
        partners of those slots are then ADDED, never subtracted.

        **IT LIVED INSIDE `_bindings` AND THEREFORE BOUNDED ONLY MINT, WHICH IS HALF THE COST.**
        `_library_fit` runs its own `for b in self.slots` through `_rebindings` and was never
        narrowed. Measured on sk48 cycle 8: `enum_calls = 0` and `cand_closure = 0` -- mint
        reached no enumeration at all -- against **1,521,205 operand binds**, every one of them
        the lookup's. So re-keying route (b) without this MOVES the cost rather than removing
        it. Reviewer's ruling, 2026-09-22: conflict 4 applies at both sites.

        ORDERING, NEVER EXCLUSION is preserved by the caller: an empty narrowing returns the
        full list, so every binding is still reachable and only the ORDER of arrival changes.
        """
        after_of = {id(b_): a_ for b_, _act, a_ in self.trace}
        moved: set = set()
        for st, _a, _v in robs:
            aft = after_of.get(id(st))
            if aft is None:
                continue
            moved |= {k for k, v in st.items() if k in aft and aft[k] != v}
        if not moved:
            return others
        own = self._slot_owners(self.env)
        tch = getattr(self.env, "contacts", None)
        grown = set(moved)
        if tch is not None and own:
            adj_of = tch()
            nearby: set = set()
            for m in moved:
                nearby |= set(adj_of.get(own.get(m), ()))
            grown |= {x for x in others if own.get(x) in nearby}
        keep = [x for x in others if x in grown]
        return keep or others

    def _rebindings(self, term: Term, slot: str, guards=None, robs: list | None = None):
        """The term as held, then -- only if it arrived unbound and reads an operand -- the
        typed re-bindings of it. **Composition crosses, binding does not**, so a loaded term
        has to be re-bound at the destination or it is the identity here.

        ARM H adds the GUARD axis, which `mint` has always walked and this has not."""
        yield term
        gs = tuple(guards) if (_GUARD_AXIS and guards) else (term.guard,)
        if not term.reads_operand or (term.operand and not _REBIND_HELD):
            # A TERM WITH NO OPERAND STILL TAKES A GUARD, and mint gives it one: its `binds` is
            # `[None]` there and the guard loop runs anyway. Without this the axis would reach
            # only operand-readers, which is not the population F238 measured.
            for g in gs:
                if g != term.guard:
                    yield Term(term.atoms, operand=term.operand, guard=g)
            return
        # ARM L AT THE LOOKUP'S OWN SITE. This loop is the other half of the operand axis and
        # was never bounded -- see `_delta_narrowed`. Same rule, same arm, one switch.
        cands = [b for b in self.slots if b != slot]
        if _DELTA_OPERANDS and robs:
            cands = self._delta_narrowed(cands, robs)
        for b in cands:
            if self._operand_fits(term, slot, b):
                for g in gs:
                    yield Term(term.atoms, operand=b, guard=g)

    def _library_fit(self, slot: str, exclude: str | None) -> str | None:
        """3c / §15.3: ask for the term by DESCRIBING THE GAP, not by walking the registry.

        The version this replaces scored every library term against the whole history and took
        the shortest that explained -- *walking it in registry order*, which §23.5 names as
        what makes a big library a liability. Now the residual is characterised, the library is
        ordered by how well each term's key fits that description, and the first explainer
        wins. **Nothing is excluded**, so a term that would have been found before is still
        found; it is reached sooner or later, never not at all.
        """
        hist = self.history(slot)
        if not hist:
            return None
        # F130 ARM C, SEAT-SIDE SWITCH, DEFAULT OFF. `characterise` takes a `relations` channel
        # built for exactly this break -- its own comment: *a relation is between two objects and
        # `slot_types` can name neither the pair nor its type, WHICH IS THE BREAK*. Two sibling
        # sites supply it with this same idiom; THIS one, the retrieval that actually binds, does
        # not, so `rel_types` is always empty here and `fits()`'s `relational` term is always 0.
        # Measured: arity-2 gaps are met 0-4.5% on three boards against 75-100% for arity-1.
        #
        # NOT ON BY DEFAULT: `retrieve` returns every name ordered by fit, so this is a RANKING
        # change, not an exclusion, and whether ranking is what the wall is made of is unmeasured.
        # The supply side may simply be thin -- 7 arity-2 atoms of 48.
        _base = (self._left(self.gamma.library[self.bound.get(slot, IDN)], slot, hist)
                 if _BARGAIN_FIT else 0.0)
        # ARM H's pool, computed ONCE per lookup and never per candidate -- `_residual_obs` walks
        # the history and `_guards` is a filter over it, so doing it inside the candidate loop
        # would pay for it on every library term. Same two calls mint makes, same order.
        _guard_pool = (self._guards(self._residual_obs(
            slot, self.gamma.library[self.bound.get(slot, IDN)], hist))
            if _GUARD_AXIS else None)
        # ARM L needs the same residual observations the guard pool does. Computed ONCE per
        # lookup and never per candidate, for the reason stated two lines up: `_residual_obs`
        # walks the history, so doing it inside the candidate loop pays for it on every term.
        _robs = (self._residual_obs(slot, self.gamma.library[self.bound.get(slot, IDN)], hist)
                 if _DELTA_OPERANDS else None)
        _rel = getattr(self.env, "contact_changes", None) if _REL_GAP else None
        # THE SCOPE IS READ FROM `slot_owner`, NEVER DERIVED BY SPLITTING THE NAME -- the loop
        # may not read domain structure, which is that side channel's whole reason.
        _scope = None
        if _DELTA_KEY:
            own = self.env.slot_owner()
            mine = own.get(slot)
            _scope = {s_ for s_, o_ in own.items() if o_ == mine} if mine else None
        gap = retrieval.characterise(hist, slot, list(self.alphabet), self.slot_types,
                                     relations=_rel() if _rel else None, scope=_scope)
        # THE GAP IS CITED BEFORE THE PULL, AND THE ROW IS WHAT PROVES IT. §15.3: *a retrieval
        # requires a characterised residual, so it is a derivation step: it cites the gap, it
        # lands in the ledger, and the gate can check that the citation preceded the pull.*
        # Nothing recorded it until now -- the ordering was real at this site and unwritten,
        # which is the one thing this session found genuinely ABSENT rather than unconsumed.
        self.led.record(self.cycle, "ROUTE", slot, "reach",
                        gap={k: v for k, v in gap.items() if k != "varies"},
                        reads=("the gap, cited BEFORE the library is read. One record, three "
                               "consumers: the pull count, the description's ordering proof, "
                               "and an import's shadow test"))
        for n in retrieval.retrieve(self.gamma.library, gap):
            if n == exclude:
                continue
            # RE-BIND WHAT ARRIVED WITHOUT A BINDING. `save` drops the operand because a slot
            # name is an instance, so an IMPORTED operand-reading term is `idn` here -- both
            # `translate` and `recolour` return `v` on empty operands -- and `_explains` tests
            # behaviour, so it could never explain a slot that moves. Binding is re-decided at
            # the destination for every locally minted term; the import path never did it.
            #
            # ONLY IMPORTS PAY THIS. Every term made here carries its binding, so the candidates
            # are exactly the loaded ones, and a cold run adds nothing. Typed by
            # `_operand_fits`, which is the same filter the mint uses.
            for cand in self._rebindings(self.gamma.library[n], slot, _guard_pool, _robs):
                # BEFORE `_explains`, and separately from it: may this BIND is a type question
                # and does it EXPLAIN is a behavioural one. Folding the first into the second
                # would put two quantities under one name at the site that decides both.
                if not _may_bind(cand, self.slot_types.get(slot)):
                    continue
                # F127 EXPERIMENT, SEAT-SIDE SWITCH, DEFAULT OFF. The line above filters the OUT
                # type and nothing filters the IN type against the slot's, so `none` -- a
                # zero-test typed `PRED` -- binds to an EXTENT slot and reads `int(not width)`,
                # unsatisfiable because a width is never 0. 354 of 424 measured mismatches are
                # that one atom. The comment two lines up already says binding is a type
                # question; it checks the wrong end.
                #
                # NOT ON BY DEFAULT because removing 354 bindings changes every board and the
                # replacement is unmeasured -- those slots may simply lose their objective. An
                # env switch so the two arms are one build and the comparison is real.
                if _TYPED_BIND and not _head_accepts(cand, self.slot_types.get(slot)):
                    continue
                # F32 ARM D, SEAT-SIDE SWITCH, DEFAULT OFF. `_explains` is `_left(...) == 0.0`,
                # and ISAIAH RULED THAT OUT: *the residual NEVER fully closes -- the corpus would
                # have told you that. That kills `left == 0.0` outright.* Figure 5's "stating it,
                # PLUS WHAT REMAINS UNEXPLAINED AFTER IT" is vacuous under a zero-remainder rule,
                # and Figure 13 lists "no remainder left after each step" as a FAILURE condition.
                #
                # THE REPAIR EXISTS AND DID NOT REACH HERE. The reuse sweep cites F32 at its own
                # site and accepts on the ONE BARGAIN instead; this path kept the old test. So
                # retrieval refuses every partial improvement, which is what 200 `reach_failed`
                # rows are, and the arity-2 split follows -- a multi-slot history rarely closes
                # to zero. Same baseline as the sweep: what the currently bound term leaves.
                if _BARGAIN_FIT:
                    _left = self._left(cand, slot, hist)
                    _cost = term_bits(self.gamma.length(cand, tuple(self.gamma.units())),
                                      self.gamma.alphabet)
                    if not pays(_cost, _left, _base):
                        continue
                elif not self._explains(cand, slot, hist):
                    continue
                held, n = n, (n if cand.name == n
                              else (cand.name if cand.name in self.gamma.library
                                    else self._install_reuse(cand, slot)))
                st = self.gamma.stamps.get(held)
                # STAMPS ARE DICTS. `getattr(st, "origin")` returned None on every pull, so
                # the transfer column would have read *no imported term was ever pulled*
                # whatever the truth -- sixth instance of an absence rendered as a value, and
                # written in the same session that recorded the flavour.
                #
                # AND THE ROW CARRIES THE COMPOSITION AND THE HELD NAME. A re-bound import is
                # installed under a NEW name stamped `accepted`, so a column keyed on the
                # imported NAME could never match it however well transfer worked. The
                # composition is what crossed, and it is what the reading has to key on.
                self.led.record(self.cycle, "ROUTE", slot, "pull", term=n,
                                held=held, chain=" . ".join(a.name for a in cand.atoms),
                                rebound=held != n,
                                origin=(st or {}).get("origin"),
                                admitted=(st or {}).get("admitted"),
                                reads="a library entry REACHED FOR -- 14.7's bench pull")
                return n
        # REACHED AND FAILED, WHICH IS THE HALF NOTHING COULD SEE. *I looked for something with
        # this shape and found nothing* is an UNREACHED with a subject, and a retrieval that
        # returns nothing leaves no other trace at all.
        self.led.record(self.cycle, "ROUTE", slot, "reach_failed",
                        reads="described the gap and the library held nothing that explains it")
        return None

    def _explains(self, term: Term, slot: str, hist) -> bool:
        return bool(hist) and self._left(term, slot, hist) == 0.0

    def indistinguishable(self) -> list[dict]:
        """§12.4's TRIGGER: *two slots with the same attribute vector and different residuals.*

        **A corpus SLOT is an object and a code slot is one of its attributes** -- five to one
        here -- so the vector is an object's slots and `slot_owner` supplies the grouping.

        **THE VECTOR IS FEATURAL, AND TWO TYPES ARE EXCLUDED FOR OPPOSITE REASONS.** `DELTA`
        is BEHAVIOUR, and the premise is *look alike, behave differently* -- a vector holding
        motion collapses the two sides of the trigger, since objects that move differently
        would leave the group on the very difference the residual is there to detect.
        `POSITION` is excluded from the other direction: it is what the REMEDY reads.

        **AND `POSITION` IS EXCLUDED BY DERIVATION.** Two distinct
        objects cannot share a position, which `priors.py` carries as solidity, so a vector
        holding one can never match and the trigger could never fire. §12.4's own remedy is
        `parity(position)` -- **position is what the new sensor READS to split them, so it
        cannot also be what made them look alike.** Expressible only because the types exist:
        *featural* is *not POSITION*, not a list of attribute names.

        **RANKED BY VECTOR MULTIPLICITY, WHICH THE REMEDY CANNOT MOVE.** Ranking by the
        residual gap would rank on a quantity the mechanism changes. **How many objects shared
        the vector is fixed before any sensor is composed** -- the remedy changes what splits
        them, never how many looked alike. A ranking, never a cut: the bargain still decides
        which remedy pays.
        """
        # READ FRESH, AND AN UNDECLARED OWNER IS NOT AN OWNER. `slots`, `alphabet` and
        # `slot_types` are refreshed at THREE sites -- init, retarget, and the per-step one
        # that fires when an object arrives or leaves. Holding owners as a field meant
        # maintaining that invariant, and it was added at two of the three: the missing one is
        # the object-arrival site, which is the exact case this trigger exists for. `get(s, s)`
        # then made every unmapped slot its own single-attribute object; ten matched each other
        # on a bare colour and read as a 21-object discrimination failure. Reading fresh
        # removes the invariant instead of maintaining it, and absence is now an exclusion.
        owners = self._slot_owners(self.env)
        if not owners:
            return []
        state = self.env.observe()
        groups: dict[tuple, list[str]] = {}
        owned: dict[str, list[str]] = {}
        for s in self.slots:
            if s in owners:
                owned.setdefault(owners[s], []).append(s)
        for owner, ss in owned.items():
            feat = [x for x in ss if self.slot_types.get(x) not in (POSITION, DELTA)]
            # A PARTIAL VECTOR IS NOT A WEAKER MATCH, IT IS A DIFFERENT CLAIM. `self.slots` is
            # a snapshot and objects vanish, so a missing attribute silently SHRANK the vector
            # and two objects agreeing on the one that survived read as indistinguishable --
            # 21 objects "matching" on a bare colour. An object that cannot supply its whole
            # featural set is excluded, never matched on the remainder.
            if not feat or any(x not in state for x in feat):
                continue
            groups.setdefault(tuple(sorted((self.slot_types.get(x), state[x])
                                           for x in feat)), []).append(owner)
        out = []
        for vec, members in groups.items():
            if len(members) < 2:
                continue
            rs = {}
            for o in members:
                rs[o] = round(sum(self._left(self.gamma.library[self.bound.get(x, IDN)],
                                             x, self.history(x))
                                  for x in owned[o] if self.history(x)), 3)
            if len(set(rs.values())) < 2:
                continue
            out.append({"vector": [list(p) for p in vec], "multiplicity": len(members),
                        "residuals": rs, "gap": round(max(rs.values()) - min(rs.values()), 3)})
        return sorted(out, key=lambda d: -d["multiplicity"])

    def resolve(self) -> dict:
        """§12.4's REMEDY: can a composition of existing sensors split what the vocabulary
        cannot? The INWARD branch, and its verdict today is the OUTWARD one.

        **NOVELTY EXCLUDES THE BARE SENSORS.** A chain of length one is a sensor the agent
        already has, and *the current sensor set says those slots are identical* is the
        trigger's premise -- so a remedy must be a COMPOSITION. §12.5 names the guard:
        *novelty (not already a sensor)*.

        **THE VERDICT IS STRUCTURAL, WHICH IS WHY IT NEEDS NO OBJECT.** If the closure holds
        no chain longer than one, nothing composable exists to try and the answer does not
        depend on which objects triggered. **Evaluating a candidate against two objects is
        what needs them, and there are no candidates** -- so the blocker defers to the moment
        it becomes real rather than blocking now.

        **AND THE ABSTENTION CARRIES ITS DENOMINATOR.** §12.4: *we can know the closure of our
        own sensor set, and therefore we can still score whether abstention was correct.* An
        abstention without the number is a word.
        """
        reg = getattr(self.env, "sensors", None)
        if reg is None:
            return {"verdict": "no_registry", "reads": "the domain declares no instruments"}
        chains = reg().closure((OBJECT,), self.cfg.max_depth)
        composable = [c for c in chains if len(c) > 1]
        return {"closure": len(chains), "composable": len(composable),
                "verdict": "reachable" if composable else "unreached",
                "reads": ("UNREACHED at the SENSOR level: every chain is length one, so every "
                          "candidate is a sensor already held and novelty refuses it. NOT "
                          "because sensors cannot compose -- `components . colour` does, from "
                          "a FRAME -- but because nothing accepts an ATTRIBUTE type, so a "
                          "chain that reaches one terminates, and from an OBJECT that is one "
                          "step. What would accept one is `parity(POSITION)` or `holes(SHAPE)` "
                          "-- §12.4's own examples, and §12.3 forbids installing them")}

    def pe_integral(self) -> float:
        """Every surprise ever. Monotone: there is no `suppress`, and no drive may zero it."""
        return self._integral

    def outstanding(self, slot: str | None = None) -> float:
        """Surprise not yet explained -- per slot, or summed when no slot is named."""
        if slot is not None:
            return self._outstanding.get(slot, 0.0)
        return sum(self._outstanding.values())

    def bears_on(self, term: Term, slot: str, robs: list, held: Term) -> bool:
        """**MINTED AGAINST THE RESIDUAL -- Isaiah, 2026-09-24. A PRECONDITION, NOT A THRESHOLD.**

        *"Too much wandering is daydreaming. But if the wandering is DIRECTED -- like how I go on
        a side tangent, or connect dots -- it's worth the time. In other words, minted against
        the residual."* **A tangent and a daydream are the same motion; the difference is whether
        the other end is held.**

            **NO OPEN RESIDUAL THE TERM BEARS ON -> NO MINT.**

        **AND IT NEEDS NO FIGURE FROM ANYONE**, which is why it is a precondition and not a
        weight: it asks whether the candidate SAYS ANYTHING DIFFERENT about a question that is
        still open, and that is a yes or a no.

        **HOW IT REFUSES A SPECTATOR.** `F354`: five of seven paid predictors sit on slots the
        agent's action cannot move, and one of them READS THE ACTION to predict a slot the action
        does not reach. **A spectator the incumbent already predicts perfectly leaves `robs`
        EMPTY -- there is no open question -- so nothing further is minted there.** The agent
        stops buying claims about what it has already nailed and cannot influence. **Correctness
        was never the test; bearing on something open is.**

        **AND IT IS THE CORPUS'S OWN RULE, UNHONOURED.** §14.4 mints a routine *when a goal
        residual no routine closes*; `M2_STANDARD` clause 2 already files the violation.
        """
        if not robs:
            return False
        for state, action, _actual in robs:
            ops = self._ops(term, state)
            hops = self._ops(held, state) if held is not None else None
            ctx = Ctx(action=action, operands=ops or (), touching=None,
                      group=self._group(slot, state), obj=self._record(slot, state),
                      shapes=self._shapes_now())
            got = self._value_of(term, slot, state, ctx) if ops is not None else NOT_RESOLVED
            if held is None:
                if got is not NOT_RESOLVED:
                    return True
                continue
            hctx = Ctx(action=action, operands=hops or (), touching=None,
                       group=self._group(slot, state), obj=self._record(slot, state),
                       shapes=self._shapes_now())
            was = self._value_of(held, slot, state, hctx) if hops is not None else NOT_RESOLVED
            if got != was:
                return True
        return False

    def _rank_by_consequence(self, by_kind: dict, best):
        """Order the kinds by HOW SOON NOT-ACTING COSTS, and keep the losers. Isaiah, 2026-09-24.

        **RETURNS THE QUEUE, HEAD FIRST. The head is installed; the tail is RECORDED rather than
        discarded**, which is the whole of what makes this a queue and not a second verdict.

        **THE ORDER IS THE AGENT'S AND IS NOT SUPPLIED HERE.** `consequence_in(kind)` is the
        measured delay between binding a term of that kind and its consequence being READABLE --
        one cycle for a predictor, however long satisfaction takes for an objective. Until the
        agent has observed one it returns `None`, every kind ties, and the fallback is `total`:
        **the exact order `best` already produced.** So the installed term is unchanged on every
        run today and the mechanism is in place for the moment the board fills the dial.

        **URGENCY CUTS THE LINE, and the hook is here with nothing feeding it.** *A faster hazard
        always moves to the front, even if it is absent from the mnemonic.* A kind marked urgent
        sorts ahead of its consequence time; nothing marks one yet, and inventing the trigger
        would be picking the number Isaiah reserved.
        """
        self._queue_kinds = []
        if not by_kind or best is None:
            return []
        # **THE DIAL ORDERS A CONTEST ONLY WHEN IT CAN SPEAK ABOUT EVERY CONTESTANT -- repaired
        # 2026-09-25, and it is this docstring's own stated intent rather than a new rule.**
        #
        # The sort read `soon if soon is not None else 0.0`. **UNEARNED COLLAPSED TO ZERO, WHICH
        # SORTS FIRST**, so the moment ANY kind earned a reading every kind that had not earned
        # one jumped ahead of it -- *the agent installs the term it knows LEAST about*, and the
        # head is what gets installed. Unknown is not zero; it is the one thing an absent
        # reading cannot mean.
        #
        # **FILED AND LEFT UNREPAIRED IN `F360` BECAUSE THERE WERE ZERO CONTESTS TO EXERCISE IT.
        # `F366`'s habitat run produced THREE**, so the precondition for touching it is met --
        # shipping an unexercised change to the decision path is how the last three dead
        # mechanisms got in.
        speaks = all(self.consequence_in(k) is not None for k in by_kind)
        rows = []
        for kind, v in by_kind.items():
            soon = self.consequence_in(kind) if speaks else None
            rows.append(((0 if self._urgent(kind) else 1),
                         (soon if soon is not None else 0.0), v[0], kind, v))
        rows.sort(key=lambda r: (r[0], r[1], r[2]))
        self._queue_kinds = [(r[3], r[4][0]) for r in rows]
        return [r[4] for r in rows]

    def consequence_in(self, kind: str) -> float | None:
        """HOW SOON A CLAIM OF THIS KIND IS ANSWERABLE, in cycles, or `None` when unearned.

        **`None` IS THE HONEST STATE AND IT IS WHAT SHIPS.** The seat may not say how soon an
        objective pays off relative to a predictor -- that is a reading of the board, and
        `gamma.vindication` already shows the agent earning exactly this shape of quantity for
        its halflife. **A number here would be the judgement Isaiah withheld**, so the dial is
        declared, empty, and visible.
        """
        got = getattr(self.gamma, "consequence", None)
        return (got or {}).get(kind)

    def _urgent(self, _kind: str) -> bool:
        """**PREEMPTION, DECLARED AND UNFED.** *A faster hazard always moves to the front.* What
        makes a kind urgent on a given board is the agent's to read; nothing sets it, so this is
        False for every kind and the queue is ordered by consequence alone."""
        return False

    def explain(self, slot: str, bits: float) -> tuple[float, float]:
        """Reduce OUTSTANDING only. The integral is untouched.

        Returns `(explained, overclaimed)`. **The clamp is reported, never silent**: the
        per-step mass and `_left` are two accountings of one slot's residual, so a claim
        larger than the slot has outstanding is the two disagreeing -- which is a reading,
        and a clamp that swallowed it would be the third flavour of an absence rendered as
        a value.
        """
        have = self._outstanding.get(slot, 0.0)
        took = max(0.0, min(bits, have))
        self._outstanding[slot] = have - took
        return round(took, 3), round(max(0.0, bits - have), 3)

    def _left(self, term: Term, slot: str, hist, ceiling: float | None = None) -> float:
        """What the term leaves unexplained across the slot's history, in bits.

        `ceiling` IS AN EXACT ABORT, NOT AN APPROXIMATION. Every term added here is
        non-negative -- `log2(alphabet)` or `correction_bits` -- so a running total that
        has reached the incumbent's can only grow past it. The caller compares with a
        STRICT `<`, so a candidate that returns an aborted total is one that could not
        have won. The winner is bit-identical; only the losers stop early.

        Default `None` leaves every existing caller walking the full history.
        """
        total = 0.0
        for state, action, actual in hist:
            if ceiling is not None and total >= ceiling:
                return total
            if not self._applies(term, state):
                total += math.log2(self.alphabet[slot])   # inapplicable is unexplained
                continue
            ops = self._ops(term, state)
            if ops is None:
                total += math.log2(self.alphabet[slot])   # unreadable operand, unexplained
                continue
            got = self._value_of(term, slot, state,
                                 Ctx(action=action, operands=ops,
                                     touching=None,      # replay: contact unknown
                                     group=self._group(slot, state),
                                     obj=self._record(slot, state),
                                     shapes=self._shapes_now()))
            if got is NOT_RESOLVED:
                total += math.log2(self.alphabet[slot])   # unread is unexplained
                continue
            total += correction_bits(got, actual, self.alphabet[slot])
        return total

    def route(self, res: dict[str, SlotResidual]) -> list[tuple[str, str, str | None]]:
        out = []
        for slot, r in res.items():
            was_refused = self._refuted_slot.pop(slot, None)
            if was_refused is not None and _REFUTED_BIN:
                # ISAIAH'S SECOND CLAUSE -- *alternatives that DO work start to compete.*
                # `_library_fit` already takes an `exclude`, so asking it for the best fit
                # OTHER than the one just refused needs no new retrieval path. Standing still
                # fades through `rejections`, which is untouched: this changes what is ASKED
                # FOR, not the term's number.
                # THE COMPETITOR MUST MATCH THE REFUTED TERM'S TYPE -- ruled 2026-09-22,
                # SCOPED TO THIS MECHANISM. `F263`: `_library_fit` has no type filter, so it
                # handed back `recolour<o0.colour>` (`val`) to replace `none` (`OBJ`), and
                # `_discrepancy` then reads NOT_RESOLVED -- the goal machinery on that slot
                # dies silently while the bargain check still passes.
                #
                # THIS IS NOT THE WITHHELD PRICING. That question is how an objective and a
                # predictor are WEIGHED when both are legitimate candidates for a role. This
                # only refuses a term of one type STANDING IN for a term of another, which
                # the typed grammar already forbids -- a `val` competitor for an `OBJ` slot
                # is a category error, not a cheaper rival.
                #
                # AND IT IS NOT A FILTER ON `_library_fit`: that is the ESCALATED test and it
                # stays parked. The result is filtered HERE, at the one caller the ruling
                # covers, so every other retrieval baseline is untouched.
                fit = self._library_fit(slot, was_refused)
                want = getattr(self.gamma.library.get(was_refused), "out_type", None)
                got = getattr(self.gamma.library.get(fit), "out_type", None) if fit else None
                if fit is not None and got != want:
                    fit = None          # a category error is not a competitor
                # AND ZERO SUPPORT FALLS THROUGH TO MINT -- ruled 2026-09-22 on B5.
                # *Support at zero is an INSTRUCTION, not a stop: perturb.* A rebind changes
                # what the agent BELIEVES and does not touch the world, so it cannot discharge
                # that instruction: zero support means there is no evidence, and a competitor
                # drawn from the library brings none. Nor can the competitor be JUDGED -- 
                # express-before-judge means nothing is tested by a swap, which is Isaiah's
                # hit-rate rule at a third site. Figure 8: a frame cannot certify its own
                # limit, and the library cannot stand in for contact with the ground.
                #
                # `_starved` IS the condition, already maintained: `mint` adds a slot on a
                # `no_support` verdict and the probe flush clears it. So it reads exactly
                # *last mint verdict was no_support and no probe has answered it yet*, and
                # this needs no new bookkeeping.
                if slot in self._starved:
                    fit = None          # let mint park it; the probe is what perturbs
                b = REFUTED
            elif r.mass == 0.0 and slot not in self.owed_import:
                b, fit = HELD, None
            elif r.mass == 0.0:
                # a slice reading zero while the accumulated residual is live. HELD says
                # "the slot is bound and the bound term predicted it" -- neither is true
                # of a slot that owes, and routing it here retires a debt on one step's
                # evidence. It is why an unbound slot fell back to idn and was never
                # revisited.
                b, fit = MECHANISM, self._library_fit(slot, self.bound.get(slot))
                if fit:
                    b = REBIND
            elif len(self.trace) < 2:
                b, fit = NOVEL, None
            else:
                fit = self._library_fit(slot, self.bound.get(slot))
                b = REBIND if fit else MECHANISM
            why = OWES if (r.mass == 0.0 and slot in self.owed_import) else WHY_NOT[b]
            out.append((slot, b, fit, why))
            self.led.record(self.cycle, "ROUTE", slot, "route", bin=b,
                            why_not=WHY_NOT[b], support=len(self.trace))
        return out

    # -- steps 3 to 5 -------------------------------------------------------------------

    def _shapes_now(self) -> dict | None:
        """The shape decoder for this cycle, or None. CACHED PER CYCLE because `Ctx` is built once
        per candidate and `shapes()` rebuilds its dict on every call -- putting it in the Ctx
        constructor would pay for it thousands of times a step."""
        if not _SHAPE_DECODE:
            return None
        c, m = self._shape_cache
        if c != self.cycle:
            f = getattr(self.env, "shapes", None)
            m = f() if f is not None else None
            self._shape_cache = (self.cycle, m)
        return m

    @staticmethod
    def _slot_types(env) -> dict[str, str]:
        """PER SLOT, and ABSENT IS A READING. A world that declares no types gets `{}` and
        every operand check is skipped -- which is reported, not assumed. The loop compares
        strings the domain supplied; it never derives a type from a slot's name."""
        f = getattr(env, "slot_types", None)
        return {str(k): str(v) for k, v in f().items()} if f is not None else {}

    @staticmethod
    def _slot_owners(env) -> dict[str, str]:
        """PER SLOT, and ABSENT IS A READING. A world that declares no owners gets `{}` and
        §12.4's trigger reports that it has no vector to form, rather than forming one from
        a name."""
        f = getattr(env, "slot_owner", None)
        return {str(k): str(v) for k, v in f().items()} if f is not None else {}

    @staticmethod
    def _alphabets(env) -> dict[str, int]:
        """PER SLOT. A domain with one range declares one number and every slot gets it;
        a domain whose slots differ declares the difference. The loop's code is uniform
        either way -- that is the FORM, and it is the loop's; the SIZE is the domain's,
        and there was never a reason it had to be a single size."""
        a = env.alphabet()
        if isinstance(a, dict):
            return {s: int(v) for s, v in a.items()}
        return dict.fromkeys(env.slots(), int(a))

    def _residual_obs(self, slot: str, term: Term, hist: list) -> list:
        """R, DESCRIBED: the observations the bound term got wrong. Step 2 already sorts
        the residual and names what changed; this is the same object handed to step 3
        instead of being recomputed as a scalar."""
        out = []
        for state, action, actual in hist:
            if not self._applies(term, state):
                out.append((state, action, actual))   # inapplicable is unexplained
                continue
            ops = self._ops(term, state)
            if ops is None:
                out.append((state, action, actual))   # unreadable operand, unexplained
                continue
            got = self._value_of(term, slot, state,
                                 Ctx(action=action, operands=ops,
                                     touching=None,      # replay: contact unknown
                                     group=self._group(slot, state),
                                     obj=self._record(slot, state),
                                     shapes=self._shapes_now()))
            if got is NOT_RESOLVED or got % self.alphabet[slot] != actual % self.alphabet[slot]:
                out.append((state, action, actual))
        return out

    def _cannot_pay(self, term: Term, slot: str, robs: list, cost: float,
                    base: float) -> bool:
        """A BOUND FROM THE RESIDUAL, not a guess about which atoms are needed.

        correction_bits is binary, so |R|phi| is log2(V) times the count of observations
        phi gets wrong, and `base` is that count over R. A term wrong on k of R is wrong
        at least k times overall, so `cost + log2(V)*k >= base` proves it cannot pay --
        at any history length, whatever it does on the rest.

        Necessary, so nothing that would have paid or closed is lost. That is the whole
        difference from the version that skipped operand-reading terms when R showed no
        dependence on another slot: THAT reasons about what a term ought to need, and it
        drops terms that read an operand without varying with it on the observed slice.
        Measured, it lost a closing term. This cannot.
        """
        unit = math.log2(self.alphabet[slot])
        wrong = 0
        for state, action, actual in robs:
            if not self._applies(term, state):
                wrong += 1                            # inapplicable is unexplained
            elif self._out_of_step_range(term, slot, state, actual):
                wrong += 1                            # P6: no reachable value equals `actual`
            elif self._ops(term, state) is None:
                wrong += 1                            # unreadable operand is unexplained
            else:
                got = self._value_of(term, slot, state,
                                     Ctx(action=action, operands=self._ops(term, state),
                                         touching=None,  # replay: contact unknown
                                         group=self._group(slot, state),
                                         obj=self._record(slot, state),
                                         shapes=self._shapes_now()))
                wrong += (got is NOT_RESOLVED
                          or got % self.alphabet[slot] != actual % self.alphabet[slot])
            if cost + unit * wrong >= base:
                return True          # `wrong` only grows; the rest of R adds nothing
        return False

    def _out_of_step_range(self, term: Term, slot: str, state: dict, actual: int) -> bool:
        """P6: `_cannot_pay` needs a BOOLEAN and `objective_step` computes a VALUE.

        The ORDERED arm returns only `current`, `current - 1`, `current + 1` or
        `NOT_RESOLVED` -- *step ONE UNIT toward the nearest*, its own docstring. When `actual`
        is none of those three, every outcome counts wrong, so the alphabet walk that proves
        it is skipped. Necessary, not plausible: it cannot drop a term that would have matched.

        COMPARABLE-only is exempt -- that arm returns the satisfying value itself, so any
        value in the alphabet is reachable and there is no range to test.
        """
        if getattr(term, "out_type", "val") != OBJ_TYPE:
            return False
        if self.slot_types.get(slot) not in ORDERED_TYPES:
            return False
        alpha = self.alphabet[slot]
        cur = state[slot]
        return actual % alpha not in (cur % alpha, (cur - 1) % alpha, (cur + 1) % alpha)

    def _accumulated(self, slot: str, term: Term) -> float:
        """|R| over the slot's whole history. Accumulated, because the model cost is paid
        once and the savings scale with n -- which is what makes the bargain discriminate.
        No min_support: the arithmetic is its own support gate."""
        return self._left(term, slot, self.history(slot))

    def choose(self, before: dict[str, int]) -> tuple[str, str]:
        """(action, by). `by` names the site that chose, so the phase label can be
        checked against the mechanism instead of believed.

        DISCRIMINATE: a slot owes and the reachable terms disagree about what an action
        will produce there. An outcome every candidate predicts alike teaches nothing,
        so the action worth taking is the one that separates them most -- which is the
        difference between a probe and an experiment, and it is derived from Gamma
        rather than from any knowledge of the answer.

        DRAW: nothing owes, or no action separates anything. Then the draw is
        UNINFORMED BY CONSTRUCTION, which is the safety property: a probe chosen by the
        current model can only confirm the current model.

        **DISCRIMINATE READING ZERO ON ARC IS THE DESIGNED STATE, NOT A DEFECT. Read this
        before proposing an atom against it.** `ARC_AGENT` measured both arms:

            spread distinguishes the actions, WITH `act`     33/96   (34%)
            spread distinguishes the actions, WITHOUT `act`   0/96   ( 0%)

        `act` is `v + DELTA.get(c.action, 0)` with its effect table **closed over at
        construction** -- so *`choose`'s discriminate branch is a property of the atom set,
        not a model the agent built. It has never had to learn what pressing something does,
        because the primitive it was given already knew.* **That is the thing the action
        world has to take away**, and the ARC set has no `act` for exactly that reason.

        **So a flat spread is the honest reading of an agent that has not learned what its
        actions do.** Measured here: 80 of 82 eligible steps on `ls20`, which is the toy
        panel's 0/96 reproduced on a real board. **It was read as a defect three times --
        twice by me -- and each time the proposed fix was an atom that reads `c.action`,
        which is the encoded answer with a name and a measurement already against it.**

        **WHAT MOVED IT LEGITIMATELY WAS A LEARNED CONTINGENCY BECOMING BINDABLE, AND IT IS
        BUILT -- CORRECTED 2026-09-05.** This said `contingency()` *is consumed by nothing* and
        called §18.4's proposer half *still owed*, while `_learned_split` -- forty lines below,
        called by this method -- opens *"§18.4's proposer half"* and consumes exactly it.
        **Two docstrings in one file disagreeing about whether a mechanism exists**, and the
        stale one is the one a reader meets first. `discriminate:learned` fires on 93 of 131
        acts.

        **SO THE GAP IS NARROWER THAN THIS DOCSTRING IMPLIED, AND NAMING IT NARROWLY IS THE
        POINT.** Two branches here already choose on model-derived quantities -- `spread` over
        a Gamma closure, and the self-model's learned contingency. **What no branch reads is
        the BOUND TERM or the OBJECTIVE**: nothing selects an action because it ADVANCES A
        GOAL. `DOCTRINE_AUDIT` §1's blanket form -- *nothing about Gamma, the bound terms, the
        residual, or the objective ever enters action selection* -- was written against a
        `drive.choose` one-liner and is now half true. **The surviving half is the objective,
        and that is `M2`'s middle item.**
        """
        # SUPPORT AT ZERO REFUSES THE MODEL THE WHEEL. `bored()` means no slot carried
        # live mass: the model explains everything it can currently see, and an action
        # IT selects can only confirm it. So boredom does not pick a different draw --
        # the draw was always uninformed and always the default, which is why `fires`
        # counted 441 perturbations that changed no action. What it changes is who is
        # allowed to choose, and 26 of those 441 steps were being steered by the model.
        # A HELD ROUTINE RUNS BEFORE ANYTHING ELSE IS CONSULTED, because that is what
        # committing to a behaviour MEANS. A routine that re-decided every cycle against the
        # branches would be a single-step chooser wearing a plan's name.
        # THE CHECK COMES FIRST, BEFORE THE NEXT STEP IS SPENT. That ordering is the whole
        # point: noticing after the action would cost the step it was meant to save.
        # **FALLS THROUGH RATHER THAN RETURNING.** `_check_expectation` clears `self.routine`,
        # so the branch below simply does not fire and `choose` goes on to pick normally.
        # Returning here would hand `None` to `env.step` AND make abandoning cost the very
        # action it exists to save -- the currency is actions, so noticing must be free.
        if self.routine is not None:
            self._check_expectation(before)
        if self.routine is not None:
            self.routine_state.pop("expect", None)
            emit, rest = Rt.advance(self.routine, self._holds(before),
                                    self.routine_lib, self.routine_state)
            # **THE FALLBACK'S FAILURE IS RECORDED, OR THE FALLBACK HIDES IT.** `Try` recovers
            # from `blocked`/`exhausted` and publishes what it recovered FROM, because a
            # routine that recovers quietly has destroyed the very ending `F207` was diagnosed
            # at -- and it would do so while looking like robustness. **This is the only
            # consumer, and without it the publish is a value that exists and never crosses.**
            #
            # DRAINED, NOT READ. The list is per-step; leaving it would make one recovery
            # reappear on every later cycle, which is the stale-state defect in the shape that
            # inflates a count rather than losing one.
            for _why in self.routine_state.pop("recovered", ()):
                self.led.record(self.cycle, "PLAN", self.routine_for or "*",
                                "routine_recovered", outcome=_why,
                                routine=Rt.render(self.routine),
                                note="a fallback ran; the body's ending is NOT a refutation")
            if emit not in (Rt.DONE, Rt.BLOCKED, Rt.EXHAUSTED) and emit in self.actions:
                # THE CLAIM, MADE BEFORE THE ACTION LANDS. `advance` published which slots this
                # step expects to move; the value is recorded NOW so next cycle compares against
                # what was true when the claim was made, not against a later frame.
                want = (self.routine_state.get("expect") or [None])[0]
                if want is not None:
                    self._expect_step += 1
                    self._expect = (want, before.get(want), self._expect_step)
                self.routine = rest
                return emit, "routine"
            # ENDED, AND THE FOUR ENDINGS ARE NOT ONE. `done` is the guard met; `exhausted` is
            # the budget spent without it -- the routine's own bet REFUTED; `blocked` is a
            # guard that could not be read; and an action this level does not advertise is a
            # routine that survived a boundary into a world that cannot run it. **Isaiah ruled
            # routines survive boundaries, and this is the other half of that ruling: it fails
            # its guard rather than crashing.**
            why = emit if emit in (Rt.DONE, Rt.BLOCKED, Rt.EXHAUSTED) else "unadvertised"
            if why == Rt.DONE and self.routine not in self.routines:
                self.routines.append(self.routine)
            # EXPRESS-BEFORE-JUDGE, AND IT IS THE PROPERTY THE ENDINGS WERE ALREADY BUILT FOR.
            # §18.2: *a refutation is recorded ONLY after the hypothesis actually ran a trial --
            # "I failed to do X" must never be coded as "X is inert." A blocked or never-reached
            # attempt is a non-trial.* **`exhausted` is a trial: the routine ran its whole budget
            # and the guard never held. `blocked` and `unadvertised` are non-trials** -- one
            # could not read its guard, the other was never runnable here -- and neither says
            # anything about whether the routine works.
            #
            # AND THE REFUTATION IS A ROW, WHICH IT WAS NOT. A TERM's demotion carries `asked`,
            # `ground_said`, `verdict` and `rejections` -- **a first-class inspectable event** --
            # while a routine's refutation was in-memory state that nothing recorded. It gates
            # future minting, so it is **a decision input that left no trace**: `speak` could not
            # say it, the gate could not check it, and express-before-judge was unverifiable
            # from the record. Same fields as `demote`, so the two read alike.
            extra: dict = {}
            if why == Rt.EXHAUSTED and self.routine_for:
                rg = self.goal_residual(self.routine_for, before)
                k = self._reject_key(self.routine_for, self.routine, self.routine_lib)
                self.refuted.setdefault(k, Standing(last_tick=self.cycle)).refute(self.cycle)
                self.refuted_at[k] = 1.0 if rg is None else rg
                # AND FILED A SECOND TIME UNDER THE SHAPE OF THE GAP IT FAILED AGAINST. The two
                # keys answer different questions and neither replaces the other: `k` says *this
                # exact plan, on this exact slot, is spent* and dies at the boundary with the
                # slot; `gk` says *a plan of this shape did not close a gap of this shape* and
                # is the only half that can still be true next level.
                extra = {"asked": [Rt.render(self.routine), self.routine_for],
                         "ground_said": False, "status": "refuted",
                         "verdict": "spent its whole budget and the guard never held",
                         "rejections": round(self._rejection(k), 3),
                         "reopens_above": round(self.refuted_at[k], 4)}
                gap = self._characterise_gap(self.routine_for)
                if gap is not None:
                    gk = (self._gap_key(gap), Rt.actions(self.routine, self.routine_lib),
                          Rt.guards(self.routine))
                    rec = self.paths.setdefault(gk, {"failed": 0, "first_cycle": self.cycle})
                    rec["failed"] += 1
                    rec["last_cycle"] = self.cycle
                    extra["gap"] = {k2: v for k2, v in gap.items()
                                    if k2 not in ("varies", "invariant")}
                    extra["shape_failed"] = rec["failed"]
            # BLOCKED IS THREE ENDINGS WEARING ONE NAME. `routine.py` says BLOCKED means only
            # *the guard could not be read*; `blocked_why` says which, so a later run can report
            # how many routines died to the world removing their subject versus to supply.
            if why == Rt.BLOCKED and self._guard_exit:
                extra["blocked_why"] = self._guard_exit
            self.led.record(self.cycle, "PLAN", self.routine_for or "*", "routine_end",
                            outcome=why, routine=Rt.render(self.routine), **extra)
            self._guard_exit = None
            self.routine, self.routine_for = None, None
        # SYSTEM 2 RUNS BESIDE SYSTEM 1, NOT BEHIND IT -- Isaiah, 2026-09-09.
        # Formation used to sit ONLY at the fall-through, so `discriminate:learned` returning
        # first foreclosed it: `_mint_routine` was last called at cycle 11 on `ka59` and 7 on
        # `ls20`, while a qualifying series arrived at 14 and 18. **The asking window shut
        # before the supply opened**, and every refusal in between was correct.
        #
        # DEMAND-DRIVEN, WHICH IS WHAT MAKES IT AFFORDABLE HERE. The watcher is `_goal_choice`,
        # a pure read over `_res` measured at 1.2us against an 87.6s cycle -- five parts per
        # billion to run every cycle -- and it gates the composer, which fired 2 of 24 on both
        # boards rather than 24 of 24. Deliberating every turn ON the acting path is the
        # expensive shape; this is not that.
        #
        # IT DOES NOT TAKE THE TURN. A routine formed here runs from the held-routine branch
        # ABOVE on the next cycle, which is the precedence execution already implements.
        if (self.routine is None and self._planned != self.cycle
                and self._goal_choice() is not None):
            self._planned = self.cycle
            self._mint_routine(before)
        # ARM M. BEFORE the global `bored()` gate, because the whole finding is that the gate
        # answers *is anything live* -- which is true precisely when a starved slot most needs
        # answering. Returning `probe` is not a relabel: the flush writes one row per slot in
        # `_starved`, which IS *the parks that precede this probe*, so B5's `followed` is
        # satisfied by construction rather than by a second mechanism.
        if _STARVED_CONTACT and self._starved:
            aim = sorted(self._starved)[0].rsplit(".", 1)[0]
            self._s0_target = aim
            # positioned where ACTION6 exists, else steer the avatar into it
            act = ("ACTION6" if "ACTION6" in self.actions
                   else self._toward(before, aim))
            if act is None:
                act = self.drive.choose(self.actions, self.cycle, _where(before))
            return act, "probe"
        if self.drive.bored():
            # AND THE AIM IS CLEARED. `_s0_target` survives until `retarget`, so an ordinary
            # bored probe would otherwise inherit whatever arm M last pointed at and coordinate
            # an unrelated action on a stale slot.
            self._s0_target = None
            return self.drive.choose(self.actions, self.cycle, _where(before)), "probe"
        owed = [s for s in sorted(self.owed_import) if s in before]
        # THE ONLY BRANCH THAT READS GAMMA, AND `by` CANNOT SAY WHY IT DID NOT FIRE. `by ==
        # discriminate` reads 0 of 100 action rows across dc22 and m0r0, bare and trained -- but
        # that is TWO facts: the gate below was never entered (no slot owes, so Gamma is never
        # consulted at all), or it was entered and the spread came out flat (Gamma consulted and
        # silent). Those want different repairs. Published per cycle so the next reading does
        # not have to infer it -- F225.
        self._gamma_read = {"owed": len(owed), "entered": bool(owed), "spread_split": None}
        if owed:
            cands = list(islice(self.gamma.enumerate_closure(
                "val", "val", 2, DISCRIMINATE_BUDGET), DISCRIMINATE_BUDGET))
            spread = {}
            for act in self.actions:
                spread[act] = sum(
                    len({g % self.alphabet[s]
                         for g in (t.apply(before[s], Ctx(action=act, operands=(),
                                                           touching=self._touching(s),
                                                           group=self._group(s, before),
                                                           obj=self._record(s, before)))
                                   for t in cands)
                         if g is not NOT_RESOLVED})
                    for s in owed)
            self._gamma_read["spread_split"] = bool(
                spread and max(spread.values()) > min(spread.values()))
            self._gamma_read["cands"] = len(cands)
            if spread and max(spread.values()) > min(spread.values()):
                top = max(spread.values())
                self._ties[("spread", sum(1 for v in spread.values() if v == top))] += 1
                pick = max(self.actions, key=lambda a: spread[a])
                # WHAT THIS ACTION BUYS, stated before it is taken. Listing the values
                # the candidates predict is TRUE AND UNFALSIFIABLE -- it spans the
                # whole alphabet, so no outcome contradicts it. The falsifiable form
                # is the guarantee: group the candidates by prediction, and
                # `live - largest bucket` die WHATEVER happens. The outcome can land
                # in the largest bucket and meet it exactly, or elsewhere and beat it.
                self._disproof = {}
                for s in owed:
                    buckets: dict[int, int] = {}
                    for t in cands:
                        v = t.apply(before[s], Ctx(action=pick, operands=(),
                                                   touching=self._touching(s),
                                                   group=self._group(s, before),
                                                   obj=self._record(s, before)))
                        if v is NOT_RESOLVED:
                            continue      # a candidate that cannot read splits nothing
                        buckets[v % self.alphabet[s]] = buckets.get(
                            v % self.alphabet[s], 0) + 1
                    self._disproof[s] = {
                        "live": len(cands), "splits": len(buckets),
                        "refuted_at_least": len(cands) - max(buckets.values()),
                        "by": f"any outcome on {s} after {pick}"}
                return pick, "discriminate"
        # SYSTEM 0 -- Isaiah: start random, then jump to strategy. While the agent lacks the
        # contingency evidence to be strategic -- a surfaced action not yet tried at >=2 distinct
        # states, probe.py's `never_live` anchor -- draw variously INSTEAD of exploiting the
        # learned arm, so it generates the (before, action, after) evidence binding needs. The
        # switch is state-derived (coverage), never a cycle constant. Off unless Config.system0.
        if self.cfg.system0 and self._system0_active():
            target, why = self._contact_target(before)
            self._s0_target = target
            act = self.drive.choose(self.actions, self.cycle, _where(before))
            # A TARGET IS ONLY REACHABLE THROUGH THE POSITIONED ACTION. Where ACTION6 is
            # surfaced and something is worth touching, take it; otherwise the target is
            # unaimable and the drawn action stands, which is the honest fall-through.
            # AN UNTRIED ACTION OUTRANKS BOTH MODALITIES, and this is not a preference --
            # it is the only order that works. Contact-seeking has to know what the
            # actions DO, and overriding the draw with ACTION6 before anything else has
            # been tried STARVES the action-effect coverage that is this switch's own
            # first clause: measured on dc22, `{ACTION6: 10}` in 10 cycles and no other
            # action ever taken, so coverage could never complete and the learned arm
            # could never resume. `_toward` already yields untried actions first; this
            # puts the positioned path under the same rule instead of around it.
            untried = [x for x in sorted(self.actions) if x not in self._move_map]
            if untried:
                act = untried[0]
            elif target is not None and "ACTION6" in self.actions:
                act = "ACTION6"
            elif target is not None:
                # NO POSITIONED ACTION: the board is DIRECTIONAL, and the agent makes
                # contact by moving its avatar into things -- which is most of the set.
                # The direction comes from what the actions were OBSERVED to do.
                step = self._toward(before, target)
                if step is not None:
                    act = step
            if self._contact_pick is not None:
                self._contact_seen.add(self._contact_pick)
            self.led.record(self.cycle, "MINT", target or "@contact", "system0",
                            why=why, target=target, action=act,
                            unexplored=len([k for k in self._contact_keys(before)
                                            if k not in self._contact_seen]),
                            seen=len(self._contact_seen))
            return act, "system0"
        learned = self._learned_split()
        if learned is not None:
            return learned, "discriminate:learned"
        # THE FALL-THROUGH ATTEMPT STAYS, AND IS NOT REDUNDANT. Here System 1 has no opinion --
        # the alternative is a blind draw -- so a routine formed now may take the turn at once.
        # The guard is only against attempting TWICE in one cycle, which would refuse twice and
        # write the gate's reason twice.
        if self.routine is None and self._planned != self.cycle:
            self._planned = self.cycle
            self._mint_routine(before)
            if self.routine is not None:   # adopted now: run its first action this cycle
                emit, rest = Rt.advance(self.routine, self._holds(before),
                                    self.routine_lib, self.routine_state)
                if emit not in (Rt.DONE, Rt.BLOCKED, Rt.EXHAUSTED) and emit in self.actions:
                    self.routine = rest
                    return emit, "routine"
                self.routine, self.routine_for = None, None
        goal = self._goal_split(before)
        if goal is not None:
            return goal, "discriminate:goal"
        return self.drive.choose(self.actions, self.cycle, _where(before)), "draw"

    # -- SYSTEM 0, CONTACT-SEEKING. Isaiah, 2026-09-21: *I said RANDOM, but more accurately
    # what humans do is: TRY TO MAKE CONTACT. What happens if this touches or interacts with
    # another thing? The more of that is done, the faster the contact clarifies relationship
    # mapping. So CONTACT is the main mode, and pure randomness is for when reasoning is in
    # progress and all contact points have been explored.*
    #
    # `F236` measured the old System 0 as BYTE-IDENTICAL to the uniform draw -- the switch was
    # right and the POLICY was the same call. This is the different policy.

    def _avatar(self) -> str | None:
        """The embodied locus, from the self-model the world already runs -- `mode()`'s
        `per_locus`, which is `embodied` where a member has explained that locus for
        `MIN_REPEAT`. Read, never derived here: the family exists so that no single claim
        about what the self is gets privileged, and picking one in the loop would do that."""
        fn = getattr(self.env, "mode", None)
        if fn is None:
            return None
        try:
            per = (fn() or {}).get("per_locus") or {}
        except Exception:                                  # noqa: BLE001
            return None
        emb = sorted(k for k, v in per.items() if v == "embodied")
        return emb[0] if emb else None

    def _note_move(self, before: dict, action: str, after: dict) -> None:
        """LEARN what an action does to the avatar, from what it DID. One running mean of
        `(drow, dcol)` per action.

        **NOT A HANDED TABLE.** `contingency`'s docstring names the failure this avoids: *it
        has never had to learn what pressing something does, because the primitive it was
        given already knew -- the difference is provenance, and provenance is the whole of
        it.* An empty map before anything is observed is what a closed-over direction table
        can never produce, and the agent explores precisely the actions it has no entry for.
        """
        a = self._avatar()
        if a is None:
            return
        r0, c0 = before.get(a + ".row"), before.get(a + ".col")
        r1, c1 = after.get(a + ".row"), after.get(a + ".col")
        if None in (r0, c0, r1, c1):
            return
        n, dr, dc = self._move_map.get(action, (0, 0.0, 0.0))
        self._move_map[action] = (n + 1,
                                  dr + (int(r1) - int(r0)),
                                  dc + (int(c1) - int(c0)))

    def _toward(self, before: dict, target: str) -> str | None:
        """The action whose OBSERVED displacement most reduces distance to `target`.

        Unobserved actions are not guessed at and not ranked -- they are what System 0 is for,
        so an action with no entry is returned FIRST when one exists. That is the exploration
        and the direction-learning being the same act, which is Isaiah's *every new step
        compounds data for search*."""
        a = self._avatar()
        if a is None or a == target:
            return None
        r0, c0 = before.get(a + ".row"), before.get(a + ".col")
        tr, tc = before.get(target + ".row"), before.get(target + ".col")
        if None in (r0, c0, tr, tc):
            return None
        untried = [x for x in sorted(self.actions) if x not in self._move_map]
        if untried:
            return untried[0]
        here = abs(int(tr) - int(r0)) + abs(int(tc) - int(c0))
        best, gain = None, 0.0
        for act, (n, sr, sc) in self._move_map.items():
            if not n or act not in self.actions:
                continue
            nr, nc = int(r0) + sr / n, int(c0) + sc / n
            d = abs(int(tr) - nr) + abs(int(tc) - nc)
            if here - d > gain:
                best, gain = act, here - d
        return best

    def _contact_keys(self, before: dict) -> dict:
        """`{key: (a, b)}` for this frame's contact points, keyed by KIND OF SITUATION rather
        than by object name -- `(contact kind, the two shape ids sorted)`. Names churn every
        frame and would leave everything permanently unexplored; `_gap_key` and `paths` settled
        that once already -- *vocabulary permanent, instances transient.*

        AND RE-OPENING NEEDS NO MACHINERY. Isaiah: *new states of a board introduce new items
        or change the state of something, in which case the rules of how that contact works
        might need to be re-examined.* A changed kind or shape IS A DIFFERENT KEY, so it is
        unexplored by construction rather than by an expiry rule nobody could justify.
        """
        fn = getattr(self.env, "contact_points", None)
        if fn is None:
            return {}
        out = {}
        for a, b, kind in fn():
            sa, sb = before.get(a + ".shape"), before.get(b + ".shape")
            if sa is None or sb is None:
                continue        # an unreadable participant is not a contact point to try
            out.setdefault((kind,) + tuple(sorted((int(sa), int(sb)))), (a, b))
        return out

    def _contact_target(self, before: dict):
        """The object to aim at, and why. Isaiah's ordering: an untried contact is the main
        mode; an object touching NOTHING is the next thing to go and make contact with; the
        uniform draw is last."""
        keys = self._contact_keys(before)
        unexplored = [k for k in keys if k not in self._contact_seen]
        if unexplored:
            k = min(unexplored)          # deterministic, so a run is reproducible
            self._contact_pick = k
            return keys[k][0], "untried-contact"
        touching = {n for pair in keys.values() for n in pair}
        owners = sorted({x.rsplit(".", 1)[0] for x in before if "." in x} - touching)
        self._contact_pick = None
        if owners:
            return owners[self.cycle % len(owners)], "seek-contact"
        return None, "all-contacts-explored"

    def _system0_active(self) -> bool:
        """UNEXPLORED CONTACT COUNT, with the action-effect coverage it replaces kept as the
        first clause. State-derived; no cycle constant and no budget.

        The old test was coverage alone -- every surfaced action tried at >=2 distinct states,
        probe.py's `never_live` anchor. That says nothing about whether the agent has found out
        what touches what, which is the thing System 0 is now for."""
        if any(len(self.drive.tried.get(a, ())) < 2 for a in self.actions):
            return True
        return bool([k for k in self._contact_keys(self.env.observe())
                     if k not in self._contact_seen])

    def binding_stats(self) -> dict:
        """The System-0 A/B instrument. Binding density = slots bound to a non-IDN term over all
        slots -- F118's quantity, per game, board-independent by definition. Plus the concrete
        action tally (did the agent act variously) and the switch state."""
        bound = [s for s in self.slots if self.bound.get(s, IDN) != IDN]
        return {"bound_slots": len(bound), "total_slots": len(self.slots),
                "binding_density": round(len(bound) / max(1, len(self.slots)), 4),
                "acts": dict(self._acts), "system0": self.cfg.system0}

    def _characterise(self, res: dict) -> Characterisation:
        """Describe THIS cycle's gap in §15.3's four keys. Types, never slot names."""
        t = self.slot_types
        involved = sorted(res)
        missed = [x for x in involved if res[x].mass > 0]

        def eff(x: str) -> str:
            r = res[x]
            if isinstance(r.actual, int) and isinstance(r.predicted, int):
                if r.actual > r.predicted:
                    return "over"
                return "under" if r.actual < r.predicted else "exact"
            # NOT A FAILURE, AND NOT FOLDED INTO `exact`. A gap whose terms cannot be ordered
            # has an effect shape we cannot state, and saying `exact` would claim we could.
            return "other"

        return Characterisation(
            signature=tuple(sorted(t.get(x, "?") for x in involved)),
            arity=len(missed),
            varies=tuple(sorted(t.get(x, "?") for x in missed)),
            invariant=tuple(sorted(t.get(x, "?") for x in involved if res[x].mass <= 0)),
            effect=tuple(eff(x) for x in sorted(missed)),
        )

    def resembling(self, c: Characterisation) -> list[tuple[int, Characterisation]]:
        """Every gap seen before, RANKED by how much structure it shares with this one.

        **A RANKING, NOT A FILTER -- Isaiah's regional rule.** Nothing is excluded and no cutoff
        exists: the caller reads the ORDER. *Similarly shaped* means at the top of this list,
        which is a comparison against what is actually around rather than against a constant.
        """
        return sorted(((c.overlap(p), p) for p in self._seen_gaps), key=lambda x: -x[0])

    def _note_gap_shape(self, res: dict) -> None:
        """**THE SAME-SHAPE PREQUALIFIER'S RAW MATERIAL -- Isaiah, 2026-09-25.** *Recurrence has
        a prequalifier of the problem being SIMILARLY SHAPED to one solved this way before.*

        **AND IT IS WHY A LOOP IS NOT EVIDENCE.** An agent circling inside one episode meets the
        SAME shape over and over, which satisfies plain recurrence trivially. Recorded here so
        the distinction is available: **same-shape-different-situation is evidence;
        same-situation-repeatedly is a loop**, and only a record of past shapes can tell them
        apart.

        Published, not acted on. What to DO with a resemblance is item 3's ruling.
        """
        if not res:
            return
        c = self._characterise(res)
        ranked = self.resembling(c)
        best = ranked[0] if ranked else None
        self.gamma.book["gap_shapes_seen"] = len(self._seen_gaps) + 1
        if best is not None:
            self.led.record(self.cycle, "PERCEIVE", "*", "gapshape", arity=c.arity,
                            signature=c.signature, effect=c.effect,
                            nearest_overlap=best[0], exact_repeat=bool(best[1] == c))
            # EQUALITY, NOT `overlap == 5`. Counting the keys hard-codes how many there are,
            # so adding one would silently stop every repeat being detected -- a guard that
            # goes quiet rather than failing, which is the class this package keeps filing.
            if best[1] == c:
                # EVERY KEY MATCHED. Counted apart from a partial match because an exact
                # repeat is the LOOP case, and summing the two would make circling look
                # like transfer.
                self.gamma.book["gap_shape_repeat"] = (
                    self.gamma.book.get("gap_shape_repeat", 0) + 1)
        self._seen_gaps.append(c)

    def _note_progress(self, state: dict[str, int]) -> None:
        """**THE FIFTH TURN, AND IT IS ONE SUBTRACTION. Isaiah, 2026-09-25.** The crane claw
        drops the toy, and the toy lands unblocked and reoriented: *the attempt FAILED and the
        SITUATION IMPROVED.* **A system that records only win/lose throws the whole turn away.**

        `objective_gap` already says HOW FAR a slot is from satisfying its objective -- zero
        exactly when satisfied -- and it had **four consumers, every one reading it WITHIN a
        cycle**. Nothing carried it across one, so *did the gap shrink* could not be asked.
        This stores the previous reading; `improved` does the subtraction.

        **NO THRESHOLD, AND THAT IS WHY IT COULD BE BUILT WITHOUT A RULING.** *Smaller than
        last cycle* is a strict comparison. **What to DO about it -- try again, or move on --
        is the judgement, and it is not taken here.** `F327`'s shape: build the mechanism so
        the judgement can be expressed, leave the figure to Isaiah.
        """
        for slot in self.slots:
            g = self._discrepancy(slot, state)
            # **NOT_RESOLVED IS THE COMMON CASE AND IT IS NOT A DISTANCE.** Its own docstring
            # says so -- *no objective here is NOT_RESOLVED, never None* -- and the SIGNATURE
            # said `int | None`, which is what I read. Corrected at that site too.
            if not isinstance(g, int) or isinstance(g, bool):
                continue
            prev = self._prev_gap.get(slot)
            self._prev_gap[slot] = g
            if prev is None:
                # FIRST READING ON THIS SLOT. Not flat -- there is nothing to compare, and
                # counting it as flat would fill the no-change bucket with non-observations.
                continue
            self._gap_delta[slot] = g - prev
            # WRITTEN AS THREE LITERALS, NOT ONE CONSTRUCTED KEY. The declaration guard greps
            # for a subscripted string literal, so a computed key reads as a declared-but-
            # unwritten row -- which is how the depth buckets evaded that guard entirely.
            if g < prev:
                self.gamma.book["gap_improved"] = self.gamma.book.get("gap_improved", 0) + 1
            elif g == prev:
                self.gamma.book["gap_flat"] = self.gamma.book.get("gap_flat", 0) + 1
            else:
                self.gamma.book["gap_worsened"] = self.gamma.book.get("gap_worsened", 0) + 1

        # PUBLISHED AT THE WRITE SITE, AND PUBLISHED IS ALL IT IS. `improved` reads the delta
        # this method just stored; ACTING on it -- try again, or move on -- is the judgement
        # Isaiah has not taken, so nothing here consults it to decide anything. The row exists
        # so the reading is legible in the record rather than only in a counter.
        better = [s for s in self.slots if self.improved(s)]
        if better:
            # `PERCEIVE`, because that is the step this runs inside -- and it is written at the
            # END of it, not the top, so it reports the state AFTER the cycle rather than the
            # one-cycle lag that the top-of-step rows carry.
            self.led.record(self.cycle, "PERCEIVE", "*", "progress", closer=tuple(better),
                            deltas={s: self._gap_delta[s] for s in better},
                            # THE SELECTOR'S OWN CHOICE, published beside the deltas. `None`
                            # here is the honest and current state: it has never once chosen.
                            selected_want=self._goal_choice(),
                            wants_held=len(self.wants))

    def improved(self, slot: str) -> bool | None:
        """Did this slot get CLOSER to satisfying its objective since last cycle?

        **`None` IS NOT `False`.** No previous reading is *I cannot say*; a zero delta is
        *it did not move*. Collapsing them is the silent-zero class this repo keeps filing."""
        d = self._gap_delta.get(slot)
        return None if d is None else d < 0

    def _discrepancy(self, slot: str, state: dict[str, int]) -> Any:
        """How far this slot is from satisfying the objective bound to it. Zero iff satisfied.

        NO OBJECTIVE HERE IS `NOT_RESOLVED`, NEVER `None`. `None` is reserved for *nothing in
        the alphabet satisfies it*, which is a claim about an objective that EXISTS. A slot
        holding a `val` term has no objective at all, and returning `None` for it made `CAN`
        report `no` — **not achievable, about a goal nobody stated.** Caught by P1's own
        verification run on `o1.col`, one level below the `A6i` this method was just repaired
        for, and the same shape: *absent* filed as *false*.
        """
        name = self.bound.get(slot)
        term = self.gamma.library.get(name) if name else None
        if (term is None or getattr(term, "out_type", None) != OBJ_TYPE
                or slot not in state or not self._applies(term, state)):
            return NOT_RESOLVED
        ops = self._ops(term, state)
        if ops is None:
            return NOT_RESOLVED
        ctx = Ctx(action=self._last_action or "", operands=ops,
                  touching=self._touching(slot), group=self._group(slot, state),
                  obj=self._record(slot, state), shapes=self._shapes_now())

        def _sat(v: int) -> bool | None:
            r = term.apply(v, ctx)
            return None if r is NOT_RESOLVED else bool(r)
        return objective_gap(_sat, state[slot], self.slot_types.get(slot) in ORDERED_TYPES,
                             self.alphabet[slot])

    def goal_residual(self, slot: str, state: dict[str, int],
                      counts: dict | None = None,
                      why: dict | None = None) -> float | None:
        """`R_goal = 1 - degree`, over the slot's peer group as the scope.

        **THIS IS THE QUANTITY §14.4 PRICES THE ACT SPACE AGAINST, AND P5 WAS KEYED ON ANOTHER
        ONE.** The trigger was `_discrepancy` — one slot's distance to its nearest satisfying
        value — chosen after ruling out `degree` (the sparse reward channel) and never checked
        against the corpus's own answer. `DISCOVERY` Q21 names a third quantity that is neither:
        **the fraction of a SCOPE that fails the objective.**

        **The difference is not a refinement, it is why the routine mint could never fire.** A
        per-slot distance is bounded by how far that slot sits from a value that satisfies it,
        and an objective minted to explain that slot is satisfied AT it — 86 readings across two
        boards, every one 0 or 1. **A scope fraction is bounded by the population**, so an
        objective true of one object in four reads 0.75 whatever any single slot is doing.
        """
        name = self.bound.get(slot)
        term = self.gamma.library.get(name) if name else None
        # **AND IF THE ACTING TERM IS NOT A WANT, READ THE RETAINED ONE.** `bound` holds what
        # SYSTEM 1 does now; `wants` holds what SYSTEM 2 is still after. While the contest was
        # winner-take-all this function had nothing to read whenever a predictor won.
        if getattr(term, "out_type", None) != OBJ_TYPE:
            _w = self.wants.get(slot)
            _wt = self.gamma.library.get(_w) if _w else None
            if _wt is not None:
                name, term = _w, _wt
        # WHICH None, NOT THAT None -- F207. This function has five None exits and they are
        # different facts: nothing bound is a SUPPLY claim, the wrong out_type is a TYPE claim,
        # an absent slot is a PERCEPTION claim, an empty group is a SCOPE claim. The first
        # routine this project ever formed died at `routine_end: blocked`, which means
        # `holds(guard)` read None -- and nothing recorded which of the five.
        if name is None:
            _why(why, "unbound")
            return None
        if term is None:
            _why(why, "name-not-in-library")
            return None
        if getattr(term, "out_type", None) != OBJ_TYPE:
            _why(why, "out_type-not-OBJ")
            return None
        if slot not in state:
            _why(why, "slot-absent-from-state")
            return None
        group = self._group(slot, state)
        if not group:
            _why(why, "empty-group")
            return None
        if not self._applies(term, state):
            _why(why, "operand-unreadable")
            return None
        ops = self._ops(term, state)
        if ops is None:
            _why(why, "operand-unreadable")
            return None
        ctx = Ctx(action=self._last_action or "", operands=ops,
                  touching=self._touching(slot), group=group,
                  obj=self._record(slot, state))

        def _sat(v: int) -> bool | None:
            r = term.apply(v, ctx)
            return None if r is NOT_RESOLVED else bool(r)
        deg = objective_degree(_sat, group, counts)
        if deg is None:
            _why(why, "degree-unresolved")
            return None
        return 1.0 - deg

    def can(self, guard: Any, state: dict[str, int]) -> str:
        """`CAN(P)` — §14.3's affordance, and it is **ACHIEVABLE, not SATISFIABLE.**

        **THE ARGUMENT IS A GUARD, NOT A SLOT, AND IT WAS CALLED `slot` UNTIL 2026-09-24.**
        It takes a slot NAME or a `condition` node -- `satisfied:<slot>`, `and`/`or`/`not` over
        those, a value comparison -- so the old name said one of the two things it can be, in
        the method whose docstring calls it `P`. One name, two quantities, and cheap to fix
        while the second quantity is hours old rather than months.

        THE TWO SOURCES DISAGREED AND THE DISAGREEMENT IS THE POINT. `grammar.py` glosses
        `CAN` as *a relation is **achievable***; §14.3 calls it *the affordance that says the
        guard is **satisfiable***. **Two quantities.** Satisfiable is logical — some value in
        the alphabet makes `P` true. Achievable is evidential — this agent has grounds to
        believe it can GET there. **`Until` needs the second**: a guard that is satisfiable and
        unreachable is exactly the loop that never terminates.

        THREE OUTCOMES, AND THE THIRD IS CHECK 3. *I have no evidence* is not *the guard is
        false* — the same error as `disembodied`-by-absence, at the one place a routine commits
        to repeating. **Only `no` is a claim about the world; `unknown` is a claim about the
        record**, and `Until` may commit on neither.

            `no`        nothing in the alphabet satisfies it. A real negative, and the only one
            `yes`       POSITIVE CAUSAL EVIDENCE, never absential: it holds now, or it has held
                        before, or an action of this agent's has been observed to move the SLOT
                        toward it. *Prefer "I tried and something happened" over "I have never
                        been there"*
            `unknown`   satisfiable, and nothing in this agent's record says it can be reached
        """
        # **A COMPOUND GUARD'S AFFORDANCE IS COMPOSED, NOT GUESSED, and each case falls out of
        # `CAN`'s own three outcomes rather than being chosen.**
        #
        #   `not P`     ACHIEVABLE WHEN P DOES NOT HOLD NOW, by this method's own rule two
        #               paragraphs down -- *holds now, or has held: reached, so reachable*.
        #               Read off the same `_discrepancy`, no new evidence
        #   `a and b`   both must be achievable. `all`, and the conservative direction is also
        #               the correct one: a conjunction you can only half-reach is not reachable
        #   `a or b`    either suffices. Achieving one disjunct achieves the disjunction
        #
        # **`unknown` PROPAGATES AND DOES NOT BECOME `no`** -- check 3 at the affordance, the
        # same distinction the evaluator keeps at execution.
        if isinstance(guard, condition.Not):
            inner = self.can(guard.inner, state)
            if inner is NO:
                return YES                 # nothing satisfies P, so `not P` holds always
            tgt = guard.inner
            if isinstance(tgt, condition.Slot) and tgt.name.startswith(_SAT):
                tgt = tgt.name[len(_SAT):]
            g = self._discrepancy(tgt, state) if isinstance(tgt, str) else None
            if g is NOT_RESOLVED:
                return UNKNOWN
            return YES if (isinstance(g, int) and g != 0) else UNKNOWN
        if isinstance(guard, condition.Cmp):
            # **HOLDS NOW -> YES, WHICH IS THIS METHOD'S OWN RULE** (*holds now, or has held:
            # reached, so reachable*), read through the ONE evaluator rather than a second
            # copy of the comparison logic. Otherwise UNKNOWN: nothing in this agent's record
            # speaks to whether two slots can be MADE equal, and `unknown` is a claim about
            # the record where `no` would be a claim about the world this cannot support.
            return YES if self._holds(state)(guard) is True else UNKNOWN
        if isinstance(guard, condition.Bool):
            lf, rt = self.can(guard.left, state), self.can(guard.right, state)
            if guard.op == "and":
                return YES if lf == YES and rt == YES else (NO if NO in (lf, rt) else UNKNOWN)
            if YES in (lf, rt):
                return YES
            return NO if lf == NO and rt == NO else UNKNOWN
        if isinstance(guard, condition.Slot):
            # A BARE SLOT IS A VALUE AND MAKES NO CLAIM, so there is nothing to achieve and
            # this is not a `no` -- it is a shape the affordance has no question to ask about.
            return (self.can(guard.name[len(_SAT):], state)
                    if guard.name.startswith(_SAT) else UNKNOWN)
        if not isinstance(guard, str):
            return UNKNOWN                 # a shape this affordance cannot read is not a `no`
        # NARROWED, AND RE-NAMED FOR IT. Everything below is about a SLOT and reads the trace,
        # the alphabet and the bindings by that name -- calling it `guard` here would hide the
        # very distinction the parameter's rename exists to make.
        slot = guard
        gap = self._discrepancy(slot, state)
        if gap is NOT_RESOLVED:
            return UNKNOWN                 # could not read the objective here
        if gap is None:
            return NO                      # nothing satisfies it -- the only real negative
        if gap == 0 or 0 in self._disc.get(slot, ()):
            return YES                     # holds now, or has held: reached, so reachable
        name = self.bound.get(slot)
        term = self.gamma.library.get(name) if name else None
        if term is None:
            return UNKNOWN
        ordered = self.slot_types.get(slot) in ORDERED_TYPES
        for a in self.actions:
            moves = [aft[slot] - bef[slot] for bef, act, aft in self.trace
                     if act == a and slot in bef and slot in aft]
            if not moves:
                continue                   # untried is not evidence either way
            wanted = self._predict(slot, state, a)
            if wanted is None or wanted == state[slot]:
                continue
            if not ordered:
                if any(aft[slot] == wanted for _, act, aft in self.trace
                       if act == a and slot in aft):
                    return YES
                continue
            step = 1 if wanted > state[slot] else -1
            if sum(1 for d in moves if d * step > 0) * 2 > len(moves):
                return YES                 # this agent has moved it that way, mostly
        return UNKNOWN

    def note_goals(self, state: dict[str, int]) -> None:
        """One discrepancy reading per goal hypothesis per step. Held, never aggregated."""
        reach: dict[str, str] = {}
        counts: dict[str, dict] = {}
        popped: dict[str, int] = {}
        for slot in self.slots:
            g = self._discrepancy(slot, state)
            if not isinstance(g, int):
                # BOTH non-integer outcomes break the trend, and for the SAME reason here --
                # a series needs a distance and neither is one. `CAN` is where they part.
                self._disc.pop(slot, None)
            else:
                self._disc.setdefault(slot, []).append(g)
            cnt: dict = {}
            # **THE POP SAYS WHY, AND IT DID NOT.** `goal_residual` can name which `None` a
            # `None` was -- eight distinct exits via `_why` -- and THIS caller passed `counts`
            # and no `why`, so the site that DESTROYS an accumulated trend recorded nothing.
            # Measured before this line existed: 969 of 985 calls on `vc33` pop the series,
            # 98.4%, every one of them silent. The ledger could not have shown it; the
            # information was discarded one argument short of being recorded.
            #
            # **AND THE COUNTS ARE AGGREGATED PER CYCLE, NOT ROWED PER CALL** -- `_why`'s own
            # docstring is explicit that a row per call would drown the trace, and it is right:
            # this runs per slot per step. One row per cycle carries the split without the flood.
            why: dict = {}
            rg = self.goal_residual(slot, state, cnt, why)
            if rg is None:
                # WHY THE SPLIT MATTERS RATHER THAN THE TOTAL: `unbound` and `slot-absent`
                # are HONEST -- a trend SHOULD die when there is nothing to trend -- and only
                # an exit where the quantity exists and could not be READ is a defect. The
                # total cannot tell those apart and was being read as if it could.
                _x = why.get("exit", "unknown")
                popped[_x] = popped.get(_x, 0) + 1
                self._res.pop(slot, None)
            else:
                self._res.setdefault(slot, []).append(rg)
                counts[slot] = cnt
            if g is not NOT_RESOLVED:      # an OBJ term is bound and readable here
                reach[slot] = self.can(slot, state)
        # PUBLISHED EVERY STEP, BECAUSE P1 SHIPS BEFORE ITS CONSUMER. `Until` is what GATES on
        # `CAN` and it does not exist yet, so without this row the producer would be code that
        # runs and says nothing. The counts are the thing to watch: `no` is a claim about the
        # world, `unknown` a claim about the record, and a board that is all `unknown` has told
        # you the trace is too thin rather than that nothing is reachable.
        # STASHED, NOT RECORDED HERE. `ledger.STEPS` orders PLAN BEFORE PERCEIVE and this
        # function runs at the TOP of the step, so a row written here becomes the cycle's first
        # and turns its own PLAN into `PLAN after PERCEIVE` -- the gate refused exactly that
        # when the vocabulary row was emitted from the same position. Carried to the first
        # point where a PERCEIVE row is already in order.
        self._popped = popped
        if reach:
            self.led.record(self.cycle, "PERCEIVE", "*", "can",
                            **{k: sum(1 for v in reach.values() if v == k)
                               for k in (YES, NO, UNKNOWN)})
        # AND THE SERIES ITSELF, BECAUSE `R_goal` IS THE ONE QUANTITY THE CHAIN TURNS ON AND WAS
        # THE ONLY ONE NOT WRITTEN DOWN. `_goal_choice` selects over `self._res` and nothing
        # published it, so *the mechanism is right and the input never satisfies it* was a claim
        # the ledger could not check -- and three sweeps had to wrap this function from outside to
        # read what it already held. A checker reads the ledger, not the machine.
        #
        # THE WINDOW, NOT ONLY THE VALUE, because the criterion is a TREND: `_goal_choice` wants
        # `MIN_REPEAT + 1` non-increasing readings carrying one real decrease, and a bare current
        # value cannot be read against that. `qualifies` is the criterion's own verdict per slot,
        # so a gate-1 refusal traces to the series that produced it instead of being inferred.
        if self._res:
            w = MIN_REPEAT + 1
            def _deltas(ser: list[float]) -> list[float]:
                return [b - a for a, b in zip(ser[-w:], ser[-w + 1:], strict=False)]
            self.led.record(
                self.cycle, "PERCEIVE", "*", "goal_series",
                series={k: [round(float(v), 4) for v in ser[-w:]]
                        for k, ser in sorted(self._res.items())},
                qualifies=sorted(k for k, ser in self._res.items()
                                 if len(ser) >= w and all(d <= 0 for d in _deltas(ser))
                                 and any(d < 0 for d in _deltas(ser))),
                satisfied=sorted(k for k, ser in self._res.items() if ser and ser[-1] <= 0),
                too_short=sorted(k for k, ser in self._res.items() if len(ser) < w),
                # the numerator and the denominator, because the RATIO cannot separate
                # never-recomputed from correctly-static from live-and-insensitive
                counts=counts)

    def _goal_choice(self, why: dict | None = None) -> str | None:
        """M2 ITEM 3, THE SELECTOR. §13.4, quoted whole because the criterion is its wording:

        > *hold several goal hypotheses at once, express each as a scalar discrepancy that is
        > zero exactly when satisfied, and select the one whose discrepancy is CONFIDENTLY
        > SHRINKING UNDER PLAY.*

        **AND THE CRITERION IS NOT *WHICH ONE ADVANCES THE GROUND REWARD*, WHICH THE CORPUS
        RULES OUT IN THE SAME BREATH IT SETS THIS ONE.** §11: *`levels_completed` might not
        move for five hundred actions -- the reward channel is not merely sparse, it is ABSENT
        for most of a run.* **A selector keyed to it would abstain forever and could not be
        told from one that was broken.** The rule above it is the whole design: *learn the
        mechanics from the dense channel; use the sparse channel ONLY TO SELECT AMONG GOALS.*

        CONFIDENTLY IS `MIN_REPEAT`, REUSED RATHER THAN A SECOND CONSTANT INVENTED, which is
        the rule written at `MIN_REPEAT` itself: *one observation is a coincidence.* So a
        hypothesis qualifies on `MIN_REPEAT` consecutive non-increasing readings carrying at
        least one real decrease -- **flat is not shrinking**, and an objective that sits at a
        constant gap is not making progress however long it sits there.
        """
        best: tuple[float, str] | None = None
        # **WHY IT REFUSED, AND IT IS FOUR FACTS THAT WERE ONE STRING.** `_mint_routine`'s gate 1
        # reports *no objective is confidently shrinking* for all of: nothing is held, the
        # series are too SHORT for the bar to have been applied at all, they are FLAT, or they
        # ROSE. **Only the last two are the bar doing work; the first two are supply**, and the
        # difference decides whether `MIN_REPEAT` is even the thing in the way.
        #
        # This is the `unbound` split of 2026-09-21 -- *stop letting one number mean three
        # things* -- applied at the gate that turned out to refuse EVERY cycle. It was measured
        # rather than assumed: six cycles, `enumerate_routines` reached zero times, every exit
        # here. **The whole ACT space is downstream of this one string.**
        tally = {"too_short": 0, "flat": 0, "rose": 0, "qualified": 0}
        longest = 0
        for slot, series in sorted(self._res.items()):
            longest = max(longest, len(series))
            if len(series) < MIN_REPEAT + 1:
                tally["too_short"] += 1
                continue
            window = series[-(MIN_REPEAT + 1):]
            deltas = [b - a for a, b in zip(window, window[1:], strict=False)]
            if all(d <= 0 for d in deltas) and any(d < 0 for d in deltas):
                tally["qualified"] += 1
                shrink = -sum(deltas)
                if best is None or shrink > best[0]:
                    best = (shrink, slot)
            elif any(d > 0 for d in deltas):
                tally["rose"] += 1
            else:
                tally["flat"] += 1
        if why is not None:
            why.update(tally)
            why["slots"] = len(self._res)
            # **THE LOAD-BEARING NUMBER.** `longest` against `MIN_REPEAT + 1` says whether the
            # bar was ever REACHED. A gate that refuses because no series is long enough is not
            # a bar set too high -- it is nothing to measure, and moving the bar could not help.
            why["longest"] = longest
            why["needs"] = MIN_REPEAT + 1
        # THE BOOK, AND IT IS A RECORD RATHER THAN A DIAL. `F341` sorted `MIN_REPEAT` as THE
        # AGENT'S and the reviewer left it untouched because *it has no books deep enough yet*.
        # This is that book: persisted with the others, so *have I ever held a series long
        # enough for my own bar to matter* survives the attempt in which it is asked. **Nothing
        # reads it to decide anything, and `MIN_REPEAT` is not moved here.**
        for k in ("too_short", "flat", "rose", "qualified"):
            if tally[k]:
                _book_add(self.gamma.book, f"plan_gate_{k}", tally[k])
        if not self._res:
            # **COUNTED SEPARATELY BECAUSE IT IS THE CASE THE OTHER FOUR CANNOT REPORT.** An
            # empty population writes no tally at all, so the book would be SILENT about the
            # one state it most needs to carry: *I have never held a goal hypothesis*. A book
            # that says nothing when nothing happened cannot be told from a book nobody wrote.
            self.gamma.book["plan_gate_no_hypothesis"] = (
                self.gamma.book.get("plan_gate_no_hypothesis", 0) + 1)
        return best[1] if best else None

    def _holds(self, state: dict[str, int]):
        """`holds(guard) -> True | False | None` for `routine.advance`. A guard is a SLOT NAME,
        and it holds when the objective bound there is satisfied.

        **GUARD B, BY CONSTRUCTION AT A FIFTH SITE.** This goes through `_discrepancy`, which
        goes through `objective_gap`, which probes the term via the same `Ctx` every other
        consumer builds. `routine.py` cannot call `t.apply` -- it has no import for it -- so
        the pricing bypass the two-arm board found cannot reappear in the ACT space.
        """
        def holds(guard: str) -> bool | None:
            # THE GUARD READS `R_goal`, THE SAME QUANTITY THE MINT TRIGGERED AND PRICED ON.
            # It read `_discrepancy` -- one slot's distance -- while the trigger and price read
            # the SCOPE fraction, and the two disagree about what the routine is for. **A
            # routine raised to close a population's residual, terminating when one slot is
            # satisfied, is a plan whose success condition is not the thing that summoned it**;
            # measured, it exhausted every time and was re-minted identically forever.
            why: dict = {}
            rg = self.goal_residual(guard, state, why=why)
            if rg is None:
                # SEPARATE THE OUTCOME -- reviewer ruling 2026-09-21, and it chooses no key.
                # `unbound` is TWO different facts and was reported as one: the guard's slot
                # DEPARTED the board (the `present` handler popped its binding), or the slot is
                # here and nothing was ever bound to it. The first is the world removing the
                # plan's subject; the second is supply. **The used==1 lesson applied forward:
                # stop letting one number mean three things.**
                exit_ = why.get("exit", "unknown")
                if exit_ == "unbound":
                    exit_ = ("subject_departed" if guard not in self.slots
                             else "never_bound")
                self._guard_exit = exit_
                # THE ROW THAT DID NOT EXIST WHEN THE FIRST ROUTINE DIED. `routine_end:
                # blocked` means only *the guard was unreadable*; `routine.py` is explicit that
                # this is not *the guard is false*. Which of `goal_residual`'s five Nones fired
                # is a different fact each time -- supply, type, perception or scope -- and no
                # artifact could say. F207: the first routine this project formed died here.
                self.led.record(self.cycle, "PLAN", guard, "guard_unreadable",
                                exit=exit_,
                                bound=self.bound.get(guard),
                                note="BLOCKED is 'could not read', never 'does not hold'")
            return None if rg is None else rg <= 0.0

        def read(name: str, args: tuple):
            """`condition.evaluate`'s reader. **A BARE SLOT IS A VALUE, PER THE GRAMMAR.**

            See `_SAT`: reading it as the satisfaction predicate was `A6i`, mine, and nothing
            could reach it yet -- **which is why it was worth fixing now rather than after a
            `Cmp` produced a clean wrong answer.** The item that would have collided with it is
            nameable, which is the condition for recording a cleared hazard: comparison guards,
            the thing this unlocks.

            An INSTRUMENT this reader cannot evaluate ABSTAINS. `None` is *I could not tell* and
            BLOCKS the routine; raising would turn a gap here into a crash in the ACT space.
            """
            if name.startswith(_SAT):
                return holds(name[len(_SAT):])
            return None if args else state.get(name)

        def holds_any(guard):
            # **A STRING IS THE OLD PATH, UNTOUCHED.** Every guard the composer has ever built
            # is a slot name, and this returns exactly what it always did for one.
            if isinstance(guard, str):
                return holds(guard)
            # **KLEENE, AND IT IS `condition.py`'s RATHER THAN A SECOND ONE.** `False and None`
            # is `False`; `True and None` is `None`. Writing that logic here would be the same
            # rule in two places, and the one in `condition` has its own seat.
            return condition.evaluate(guard, read)

        return holds_any

    def _compound_guards(self, subject: str, names: tuple) -> tuple:
        """Guards that say more than one slot -- the agent-formed half of Part 5.9.5.

        **A GUARD WAS ONE SLOT NAME, SO A ROUTINE'S TERMINATION CONDITION COULD ONLY EVER SAY
        *this one objective is satisfied*.** `condition.py` was built for the OTHER half --
        conditions DERIVED from corpus prose -- and `F299`/`F300` read that census at
        `DRAFTABLE 0`, which is why nothing imported it. **The parser was never the unreached
        part; the agent forming its own conditions was.**

        **EVERY COMPOUND MENTIONS THE SUBJECT, AND THAT IS A BOUND RATHER THAN A CAP.** A
        routine is composed FOR a slot, so a guard that does not mention it is a guard for a
        different plan. That makes this linear in the slots the agent has objectives about,
        and the bound is read off the call site instead of being a number I picked.

        **THIS IS NOT AGGREGATION ACROSS SLOTS.** The prohibition is on AVERAGING -- *R is
        indexed per object slot, and averaging is how a live signal disappears*. A conjunction
        reads each slot's residual SEPARATELY and dilutes neither; both readings survive
        individually, and `guard_unreadable` still records the slot that could not be read.
        **An average destroys the per-slot signal; a conjunction preserves both.**
        """
        Nt, Bl = condition.Not, condition.Bool

        def sat(n: str):
            return condition.Slot(_SAT + n)

        out = [Nt(sat(subject))]
        for other in names:
            if other == subject:
                continue
            out.append(Bl("and", sat(subject), sat(other)))
            out.append(Bl("or", sat(subject), sat(other)))
            # **A CLAIM ABOUT THE WORLD, NOT ABOUT THE AGENT'S OWN OBJECTIVES.** Every guard
            # above is built from `satisfied:` -- *my objective here is met* -- so a routine
            # could only ever terminate on its own bookkeeping. `o1.dcol == o2.dcol` is a
            # statement about the BOARD, and *act until these two agree* is the shape of an
            # ARC goal rather than of a status report.
            #
            # **EQUALITY ONLY, AND THE OTHER FIVE OPERATORS ARE REFUSED FOR A REASON.** `<`
            # needs an ORDER, and `slot_types` already separates `ORDERED_TYPES` from the
            # rest -- offering `<` over a COLOUR would compare two episode-local labels and
            # return a clean, meaningless answer. That is the `row < shape` case `evaluate`'s
            # own `TypeError` guard was written for, and the honest fix is not to OFFER it.
            out.append(condition.Cmp("==", condition.Slot(subject),
                                     condition.Slot(other)))
        return tuple(out)

    def _rejection(self, key: tuple) -> float:
        """The decayed strength of rejection. `Standing.decay` on the LOGICAL clock -- cycles,
        never wall time -- which is §18.2's first defeasance route and was already built."""
        st = self.refuted.get(key)
        if st is None:
            return 0.0
        st.decay(self.cycle)
        return st.rejections

    @property
    def routine_lib(self) -> dict:
        """The shelf ADDRESSED BY NAME -- what makes `routine.Call` reachable by the agent.

        **DERIVED, NEVER STORED, AND THAT IS THE WHOLE POINT.** A settled routine was already
        reusable as a CHUNK but by VALUE: the object was inlined, so `render` printed the entire
        expansion and the plan never said which learned behaviour it invoked. Part 12 -- PRINTING
        THE TREE IS THE EXPLANATION -- and an inlined tree explains the steps while hiding the
        structure. A name costs 1 in `length` exactly as the inlined chunk did, so this changes
        what the plan SAYS, not what it can afford.

        **IT WAS A SECOND DICT FOR TEN MINUTES AND `m2` CAUGHT IT.** Registering names at
        settlement made a store that could DIVERGE from `self.routines`, and anything appending
        to the list directly -- which `check_shelf_must_be_runnable_here` does -- got a routine
        the shelf could not see. One name, one store; the names are positional over the list.

        Positional because the agent has no vocabulary for what a routine is ABOUT. That is the
        description layer and it is not built. **A stub, marked as one.**
        """
        return {f"r{i}": r for i, r in enumerate(self.routines)}

    @staticmethod
    def _reject_key(slot: str, r, lib: dict | None = None) -> tuple:
        """The identity a refutation is filed under. **BUDGET-FREE ON PURPOSE.**

        §18.2's immune audit names **pathogen mimicry** -- *a dead idea re-tried under a slightly
        different key* -- and calls the signature granularity a problem *left to the caller
        rather than baked in*. Here the caller is this method, and the answer is that a routine
        differing only in its budget is THE SAME HYPOTHESIS: the budget is derived from the gap
        and moves every cycle, so keying on it would let one refuted routine return under a new
        number every step.
        """
        # `lib` RESOLVES A `Call`. Without it a named callee reports `?name`, which would file
        # two routines invoking the SAME learned behaviour under two different keys -- the
        # pathogen mimicry this docstring is about, introduced by the fix for it.
        return (slot, Rt.actions(r, lib), Rt.guards(r))

    @staticmethod
    def _gap_key(gap: dict) -> tuple:
        """THE NAME-FREE HALF of a characterised gap. What a failure is filed under so it can
        be read on a board where every slot has a different name.

        **The fields dropped are dropped for two different reasons and both are `_reject_key`'s
        own.** `varies` and `invariant` hold SLOT NAMES -- the exact thing that makes the
        instance key uncrossable -- and `n` is a running count of observed frames, which moves
        every step, so keying on it would let one shape return under a new number exactly as a
        budget-keyed routine would. **What survives is what `retrieval.fits` already scores
        on**, which is the point: the routine path is being given the term path's key, not a
        second one invented beside it.
        """
        # AND THE MULTIPLICITY IS A SLOT COUNT, WHICH IS THE SAME INSTANCE LEAK THIS METHOD
        # DROPS `varies` FOR. `characterise` emits one entry PER VARYING SLOT, so a gap reads
        # ('COLOUR','COLOUR','COLOUR','DELTA'x7,...) -- *how many objects changed*, not *which
        # attributes changed*. Its own author's line, one file over: "WHICH TYPES VARIED, NOT
        # WHICH SLOTS ... the key that CROSSES." Measured on four boards: the catalogue splits
        # into 34-132 keys where the SET gives 10-18, so one failure shape files under up to
        # 8.8x as many entries and never accumulates.
        #
        # RETRIEVAL IS UNAFFECTED AND THAT WAS CHECKED FIRST: `fits` reads `varies_types` only
        # through `in`, where multiplicity cannot matter. This key is the only consumer that
        # can see it.
        return (gap.get("arity"), tuple(sorted(set(gap.get("varies_types", ())))),
                gap.get("target_type"), gap.get("rel_types", ()))

    def _characterise_gap(self, slot: str) -> dict | None:
        """The gap at a slot, or None when there is nothing to describe.

        **ABSTAINS ON NO EVIDENCE, which is `M2_STANDARD`'s check 3.** No history is *I cannot
        describe this*, never *the gap is empty* -- and an empty description would key every
        failure under one shape and make the catalogue say the opposite of what it saw.
        """
        hist = self.history(slot)
        if not hist:
            return None
        rel = getattr(self.env, "contact_changes", None)
        return retrieval.characterise(hist, slot, list(self.alphabet), self.slot_types,
                                      relations=rel() if rel else None)

    def _mint_routine(self, before: dict[str, int]) -> None:
        """§14.4: **a routine is minted when a goal residual no routine closes.**

        THE TRIGGER IS THE DENSE CHANNEL, NEVER THE REWARD. `_route_reward` bins on `degree`,
        which §11 measures as ABSENT for most of a run -- *`levels_completed` might not move
        for five hundred actions.* **A routine trigger keyed there would fire almost never and
        could not be told from a broken one**, which is the criterion error the selector
        already had once.

        EVERY PART COMES FROM THE AGENT, WHICH IS GUARD A AT EVERY CONSTRUCTOR:

            the GOAL     `_goal_choice` -- the composed objective whose discrepancy is
                         confidently shrinking. The agent minted it; the selector chose it
            the GUARD    `CAN(P) == yes`, and ONLY yes. `unknown` is *nothing in my record
                         says I can get there*, and committing to repeat on that is the loop
                         that never ends
            the ROUTE    the action THIS agent has observed moves THIS slot the wanted way --
                         `_goal_split`, over `self.trace`. Never `act`, never the env
            the BUDGET   the objective's own gap. A guard `g` units away needs at most `g`
                         iterations, so the bound is DERIVED and not picked

        AND THE PRICE IS THE ONE BARGAIN, NOT A SECOND ONE. `pays(cost, left, base)`, with the
        action set as the alphabet where a term uses the slot's: **without the routine the
        agent must name `g` actions itself, so `base` is what that costs; the routine costs
        `term_bits` of its own length; and `left = 0` is the routine CLAIMING it closes the
        gap.** That claim is what `exhausted` refutes -- which is why that ending is recorded
        apart from `done` rather than folded into it.
        """
        # S3: FOUR OF THE EIGHT GATES HERE RETURNED IN SILENCE, and the cost was measured
        # rather than argued -- sweep 7 read `rows written 0` across thirty-seven entries of
        # this function and could not tell gate 1 from gate 6, so two later sweeps had to
        # wrap it from outside to find out. Each now says which gate and why, in the shape
        # the four row-writing gates already use.
        gwhy: dict = {}
        slot = self._goal_choice(why=gwhy)
        if slot is None or slot not in before:
            # **THE REASON IS DERIVED FROM THE TALLY RATHER THAN ASSERTED, AND THE OLD STRING
            # WAS A FALSE CAUSAL STORY.** *No objective is confidently shrinking* reads as *I
            # hold objectives and none is shrinking*. Measured on one board: `slots: 0` -- the
            # agent holds NONE, so `MIN_REPEAT` filters an empty population and could not be
            # the thing in the way. **A null carrying a satisfying causal story is harder to
            # doubt than a bare one**, and this one had been quoted as a finding about the bar.
            if slot is not None:
                reason = "the selected objective's slot is not in this frame"
            elif not gwhy.get("slots"):
                reason = ("no goal hypothesis is held at all -- the bar filters an empty "
                          "population, so this is SUPPLY and not the bar")
            elif gwhy.get("longest", 0) < gwhy.get("needs", 0):
                reason = ("every series is shorter than the bar needs -- the bar has not been "
                          "applied yet, so this is not a bar set too high")
            else:
                reason = "no objective is confidently shrinking"
            self.led.record(self.cycle, "PLAN", slot or "*", "routine_refused",
                            reason=reason, **gwhy)
            return
        gap = self._discrepancy(slot, before)
        if not isinstance(gap, int):
            self.led.record(self.cycle, "PLAN", slot, "routine_refused",
                            reason=f"the discrepancy is not a distance: {gap!r}")
            return
        # §14.4: **a goal residual no routine closes.** `R_goal` is the trigger and the price;
        # the GAP stays the budget, because a step count is what bounds a loop and a fraction is
        # not. Two readings, two jobs, and neither doing the other's is the whole correction.
        rg = self.goal_residual(slot, before)
        if rg is None or rg <= 0.0:
            self.led.record(self.cycle, "PLAN", slot, "routine_refused",
                            reason="no goal residual to close"
                                   if rg is None else
                                   "the objective already holds across its whole scope",
                            r_goal=rg)
            return
        unsat = rg * len(self._group(slot, before))
        # DEFEASIBLE ON SURPRISE -- §18.2's second route: *a fitness-conditional gate-drop
        # where DECISIVE NEW SURPRISE reopens a refuted hypothesis.* The surprise here is the
        # goal residual RISING above what it was when the routine was refuted: the world has got
        # further from the objective than it was when the plan failed, so the plan's failure is
        # no longer evidence about the situation it now faces.
        #
        # **THE OTHER ROUTE IS NOT BUILT AND IS NAMED RATHER THAN SKIPPED.** §18.2 wants decay on
        # a LOGICAL clock as well, and a decay rate is a constant with no derivation available
        # here -- so it is owed, not invented.
        for key, was in [(k, w) for k, w in self.refuted_at.items()
                         if k[0] == slot and (rg or 0.0) > w]:
            self.refuted.pop(key, None)
            del self.refuted_at[key]
            self.led.record(self.cycle, "PLAN", slot, "refutation_dropped",
                            reason="the goal residual rose above where the plan failed",
                            was=round(was, 4), now=round(rg, 4))
        verdict = self.can(slot, before)
        if verdict != YES:
            self.led.record(self.cycle, "PLAN", slot, "routine_refused",
                            reason=f"CAN is {verdict}, and only yes commits")
            return
        act = self._goal_split(before)
        if act is None:
            self.led.record(self.cycle, "PLAN", slot, "routine_refused",
                            reason="no action this agent has observed moves this slot the "
                                   "wanted way -- coverage incomplete, or every action ties")
            return
        n = max(len(self.actions), 2)
        # WHAT NOT HAVING THE ROUTINE COSTS: naming an action for each unsatisfied member of the
        # scope. Same shape as before -- a count times `log2(n)` -- with the count now taken
        # from the goal residual instead of from one slot's distance.
        base = unsat * math.log2(n)
        # THE BODY IS CHOSEN BY THE BARGAIN, NOT BY ME. Candidates are the learned single action
        # and every SETTLED routine this level can still run; each is priced with the settled
        # ones counting as one unit, and the cheapest that pays wins. **A shelf that is empty
        # leaves exactly the old behaviour**, which is what makes the chunk a shortcut rather
        # than a second mechanism.
        # THE SHELF IS FILTERED TO WHAT THIS LEVEL CAN RUN, WHICH IS `M2_STANDARD` 3 AT THE
        # CONSTRUCTOR I FORGOT. This filter existed before the composer replaced the hand-built
        # candidate list and was dropped with it. **Measured: 6 of 10 candidates then named an
        # action the level does not advertise**, and one of them -- the chunked
        # `until(g/5) {until(g/3) {ACTION9}}` -- tied the winner on total, so validity was
        # decided by sort order.
        #
        # A SETTLED ROUTINE'S ACTIONS ARE EVIDENCE FROM THE WORLD IT SETTLED IN. The shelf
        # survives a boundary and its GUARDS are re-checked by `CAN`; its ACTIONS had nothing
        # checking them. `unadvertised` at execution was catching it a cycle too late -- the
        # plan was already minted and the cycle already spent.
        # OFFERED BY NAME. The actions check is unchanged and still runs over the RESOLVED
        # body -- a `Call` whose callee names an unadvertised action is refused here exactly as
        # the inlined object was. What changes is that the candidate the composer builds, and
        # the plan it prints, carry `r0()` instead of the whole expansion.
        shelf = tuple(Rt.Call(nm) for nm, r in self.routine_lib.items()
                      if set(Rt.actions(r, self.routine_lib)) <= set(self.actions))
        # THE COMPOSER ENUMERATES SHAPES; THE ROUTE STAYS LEARNED, AND THE SPLIT IS GUARD A.
        # `compose` is handed exactly ONE action -- the one this agent's own trace says moves
        # this slot the wanted way -- because enumerating over every ADVERTISED action would let
        # a routine pick a move it has no evidence for. **That is `act` with more steps**, and it
        # is the difference between composing a plan and guessing one.
        #
        # The guards offered are the agent's OWN objectives: slots it has composed something
        # about. Every one is `CAN`-checked below, so an unreachable guard is refused rather
        # than trusted.
        # THE BUDGET IS THE UNSATISFIED COUNT -- `R_goal` is a fraction and cannot bound a loop,
        # but `unsat` COUNTS members that must change, each needing at least one iteration, so
        # it is the step floor the guard implies rather than a number picked.
        loop_budget = max(int(round(unsat)), 1)
        mine = tuple(s for s in sorted(self._disc) if s in before)
        # derived once: `reach` and `actions` both resolve a `Call` through it
        lib = self.routine_lib
        # THE COMPOUND GUARDS ARE APPENDED, so every shape reachable before this line is still
        # reachable and in the same order -- `cap` takes the shortest, and a compound guard now
        # costs its excess (`routine._guard_excess`), so it sorts AFTER the plain one it
        # extends rather than displacing it. **A looser guard has to be worth its extra bits.**
        gnames = mine or (slot,)
        cands = Rt.enumerate_routines((act,), gnames + self._compound_guards(slot, gnames),
                                      shelf, loop_budget)
        # WEIGHTED AND CLOCKED, per §18.2 via `gamma.Standing`: a refutation excludes only while
        # its decaying strength stands, so a failed shape leaves the running and returns.
        cands = [c for c in cands
                 if self._rejection(self._reject_key(slot, c, self.routine_lib)) < 1.0]
        if not cands:
            self.led.record(self.cycle, "PLAN", slot, "routine_refused",
                            reason="every rejection still stands and nothing has surprised",
                            strengths=[round(self._rejection(k), 3) for k in self.refuted
                                       if k[0] == slot])
            return
        # RETRIEVAL, AND IT ORDERS RATHER THAN EXCLUDES -- `retrieval.py`'s own standing rule,
        # *order, never exclude*, whose docstring records `_cannot_pay` as having LOST A CLOSING
        # TERM by filtering. So a shape that failed ten times is still tried; it is tried LAST.
        # **THIS IS THE HALF THAT CUTS THE PROBLEM DOWN** -- the exclusion above is the same-slot
        # ban, which dies at the boundary; this is what a replay retrieves.
        gap = self._characterise_gap(slot)
        if gap is not None and self.paths:
            gkey = self._gap_key(gap)
            # STABLE ORDER: `sorted` is stable, so candidates with equal failure counts keep the
            # composer's ordering exactly. A gap shape never seen scores 0 for every candidate
            # and the order is UNCHANGED -- check 3, no evidence changes nothing.
            scored = [(self.paths.get((gkey, Rt.actions(c), Rt.guards(c)), {}).get("failed", 0),
                       c) for c in cands]
            if any(f for f, _ in scored):
                cands = [c for _, c in sorted(scored, key=lambda p: p[0])]
                self.led.record(self.cycle, "PLAN", slot, "paths_retrieved",
                                reason="a plan of this shape failed against a gap of this shape",
                                gap={k2: v for k2, v in gap.items()
                                     if k2 not in ("varies", "invariant")},
                                deprioritised=sum(1 for f, _ in scored if f),
                                considered=len(cands))
        # `left` IS WHAT THE CANDIDATE CANNOT REACH, NOT ZERO. See `routine.reach`.
        # THE BARGAIN IS TWO-PART AND STAYS TWO-PART ON THE ROW. These were folded into one
        # number and handed to `pays` as `cost` with `left = 0` -- arithmetically identical and
        # **unreadable**: the ledger then said `cost` for a quantity that was description PLUS
        # residual, so no reader could see which half bought the term. *A change that makes the
        # agent better and its reasoning unreadable has destroyed the instrument*, and the
        # mislabelled row is `A6i` at the site a future reader would trust.
        priced = [(term_bits(Rt.length(c, shelf), n),
                   max(0.0, unsat - Rt.reach(c, lib)) * math.log2(n), c) for c in cands]
        # ORDERED BY WHAT THE BARGAIN SPENDS, `cost + left`, which is the correction the two-arm
        # board already paid for once in the PREDICT space -- selecting on either half alone
        # buys the most-explaining term at any price, or the cheapest term that explains nothing.
        priced.sort(key=lambda p: p[0] + p[1])
        # EVERY GUARD OF EVERY CANDIDATE -- `M2_STANDARD` 3. A candidate whose guard this level
        # cannot reach is dropped rather than ending the search, because the composer now offers
        # many shapes and one unreachable guard is a fact about THAT shape. **A nested `Until`
        # whose guard nobody re-checked is the durable contamination the standard names**: it
        # looks like planning and loops on a condition this level cannot reach.
        ok = [(c, lf, r) for c, lf, r in priced
              if all(self.can(g, before) == YES for g in Rt.guards(r))]
        if not ok:
            self.led.record(self.cycle, "PLAN", slot, "routine_refused",
                            reason="no candidate's guards are all reachable here",
                            considered=len(priced))
            return
        cost, left, cand = ok[0]
        if not pays(cost, left, base):
            self.led.record(self.cycle, "PLAN", slot, "routine_cut",
                            reason="does-not-pay", routine=Rt.render(cand),
                            cost=round(cost, 4), left=round(left, 4),
                            base=round(base, 4), reach=Rt.reach(cand),
                            reach_status=Rt.reach_status(cand),
                            considered=len(priced), shelf=len(shelf))
            return
        # **WRAPPED IN AN EXPECTATION AT ADOPTION.** The source is hardcoded and says so: a
        # routine minted FOR a slot expects THAT SLOT to change. A per-step predicted VALUE
        # would need the term space; a predicted CHANGE needs only the delta already published.
        # `Expect` rebuilds around the remainder, so the claim is re-made every step rather
        # than once at the start.
        self.routine, self.routine_for = Rt.Expect(slot, cand), slot
        self.led.record(self.cycle, "PLAN", slot, "routine", verdict="pays",
                        routine=Rt.render(cand), length=Rt.length(cand),
                        units=Rt.length(cand, shelf),
                        chunked=Rt.length(cand) != Rt.length(cand, shelf),
                        cost=round(cost, 4), left=round(left, 4),
                        base=round(base, 4), gap=gap, reach=Rt.reach(cand),
                        reach_status=Rt.reach_status(cand),
                        unsat=round(unsat, 4), considered=len(priced), shelf=len(shelf),
                        route="learned: observed to move this slot the wanted way")

    def _goal_split(self, before: dict[str, int]) -> str | None:
        """M2 ITEM 2: pick an action because the agent's OWN model says it advances the
        agent's OWN objective. **The first branch in `choose` that reads what the agent WANTS.**

        `DOCTRINE_AUDIT` §1 said *nothing about Gamma, the bound terms, the residual, or the
        objective ever enters action selection.* Gamma entered with `spread`, perception with
        `_learned_split`; **the objective is the half that was still true, and this is it.**

        THE ROUTE IS THE AGENT'S OWN, WHICH IS THE WHOLE PROHIBITION. Two halves, and neither
        may come from anywhere else:

            the GOAL     `_predict` on an OBJ-bound slot -- the objective the agent COMPOSED
                         and minted, reaching this through item 1's wire. Routed through
                         `_value_of`, so the objective is never scored as its own truth value
            the ROUTE    `self.trace` -- what THIS AGENT observed ITS OWN actions do to THIS
                         slot. Not a table, not `act`, not the env

        **`act` IS WHAT THIS MUST NOT BECOME**, and the difference is provenance alone: *it has
        never had to learn what pressing something does, because the primitive it was given
        already knew.* An empty trace produces no preference here, which is what a closed-over
        effect table can never do.

        NEAREST IS THE TYPE'S, AND IT IS `objective_step`'s SPLIT REUSED RATHER THAN A SECOND
        ONE INVENTED. `ORDERED` has a direction, so *toward* is the sign of the wanted step;
        `COMPARABLE`-only has none, so *toward* can only be *did this action ever produce that
        value*. **Two arms because the type system has two, not because two cases turned up.**

        COVERAGE FIRST, AND THE CORPUS ORDERED IT. `ARC_BUILD_PLAN`: *coverage-first as a
        PHASE, with goal pursuit gated on a complete action map -- the loop has no such
        ordering.* It has one now, in the small: **a slot contributes only when every
        advertised action appears in ITS OWN history**, so the branch cannot prefer an action
        it has never tried, and it sits AFTER both discriminate branches, which are what build
        the map.

        VOTES, NEVER SUMMED MAGNITUDES -- `_learned_split`'s rule at a second site. Slots carry
        different alphabets, so a distance on `col` and a distance on `colour` are not
        commensurable and adding them is a category error. **One slot, one vote.**
        """
        # ITEM 3 GATES ITEM 2. Before the selector this ranged over EVERY OBJ-bound slot,
        # which is *pursue whichever objective happened to bind* -- and it measurably chose to
        # stand still, because `none_same` on a delta is satisfied by not moving. One selected
        # hypothesis, chosen on a shrinking discrepancy, is what §13.4 asks for.
        chosen = self._goal_choice()
        if chosen is None:
            return None
        votes: dict[str, float] = dict.fromkeys(self.actions, 0.0)
        n_goals = 0
        for s in [chosen]:
            if s not in before:
                continue
            name = self.bound.get(s)
            term = self.gamma.library.get(name) if name else None
            if term is None or getattr(term, "out_type", None) != OBJ_TYPE:
                continue
            hist: dict[str, list[tuple[int, int]]] = {}
            for bef, act, aft in self.trace:
                if s in bef and s in aft:
                    hist.setdefault(act, []).append((bef[s], aft[s]))
            missing = [a for a in self.actions if a not in hist]
            if missing:
                # FIVE EXITS, ONE MESSAGE. `_mint_routine` reports every `None` from here as
                # "coverage incomplete, OR every action ties" and the code has more ways out
                # than that names. This one reads `self.trace`, NOT the ledger -- which is why
                # a `bet`-row census read coverage as COMPLETE while this gate was refusing on
                # it. Publish which exit fired, the same move `goal_series` was.
                self.led.record(self.cycle, "PLAN", s, "split_refused",
                                why="coverage", untried=sorted(missing),
                                tried=sorted(hist), trace_len=len(self.trace),
                                n_actions=len(self.actions))
                continue                      # the coverage gate: untried is not neutral
            ordered = self.slot_types.get(s) in ORDERED_TYPES
            n_goals += 1
            for a in self.actions:
                wanted = self._predict(s, before, a)
                if wanted is None or wanted == before[s]:
                    continue                  # unreadable, or the objective already holds
                if ordered:
                    step = 1 if wanted > before[s] else -1
                    moved = sum(1 for b, f in hist[a] if (f - b) * step > 0)
                    if _FINE_VOTE:
                        # F141 ARM E, SEAT-SIDE SWITCH, DEFAULT OFF. The binary vote is why gate 3
                        # ties: with ONE goal (fixed by §13.4, and multi-goal is a REVERTED option
                        # -- it measurably chose to stand still) any two actions that both clear
                        # the majority bar score 1 and tie BY CONSTRUCTION. Measured `all_tied`
                        # 9/9.
                        #
                        # THE SAME QUANTITY, UN-THRESHOLDED. `moved / len(hist[a])` is what the
                        # majority test already computes; this stops rounding it to a flag. NO NEW
                        # CONSTANT and nothing borrowed -- F32's confidence is a ruling about
                        # ACCEPTANCE and transplanting it here would be F135's error again.
                        votes[a] += moved / len(hist[a])
                    elif moved * 2 > len(hist[a]):
                        votes[a] += 1         # this action MOSTLY moved it the wanted way
                elif any(f == wanted for _, f in hist[a]):
                    votes[a] += 1             # unordered: it has produced that value
        if not n_goals or max(votes.values()) == 0:
            self.led.record(self.cycle, "PLAN", chosen,
                            "split_refused",
                            why="no_goal_read" if not n_goals else "no_action_voted",
                            votes=dict(votes), n_actions=len(self.actions))
            return None
        top = max(votes.values())
        tied = sum(1 for v in votes.values() if v == top)
        self._ties[("goal", tied)] += 1
        if tied == len(self.actions):
            # AN ABSTENTION COUNTS ONLY WHEN IT NAMES THE CLOSURE IT SEARCHED, and this one did
            # not. With ONE action the tie test compares the winner against a field of itself, so
            # `all_tied` fires by construction and reads identically to a real tie among four --
            # a FALSE ABSTENTION indistinguishable from an honest one, on 6 of the 25 games
            # (F151). `n_actions` is the closure; `vacuous` is the verdict, published rather than
            # left to be re-derived from it.
            self.led.record(self.cycle, "PLAN", chosen, "split_refused",
                            why="all_tied", votes=dict(votes),
                            n_actions=len(self.actions),
                            vacuous=len(self.actions) < 2)
            return None                       # nothing separates; the draw stays uninformed
        return max(self.actions, key=lambda a: votes[a])

    def members(self) -> dict:
        """Who passed the contingency gates, and which gate dropped the rest.

        `sep[a]` is bounded by the member count, so ONE passing member makes `sep` 0/1 valued
        and the argmax returns whatever that member found distinctive -- which would be the
        family reporting faithfully rather than the selector failing. The gates are counted
        apart because coverage and stability are different causes."""
        return {"per_member": dict(sorted(self._members.items())),
                "passed_per_call": dict(sorted(self._passes.items())),
                # THE SHAPES, WITH THEIR COUNTS -- and `agreed` is row 2's field, which the
                # first version of this instrument did not have: mass on ONE action while
                # several members passed is unanimity, and unanimity decides nothing.
                "sep_shapes": {str(k): v for k, v in sorted(
                    Counter(e["sep"] for e in self._sep_log).items(),
                    key=lambda kv: -kv[1])},
                "agreed": sum(1 for e in self._sep_log
                              if e["passed"] > 1 and sum(1 for v in e["sep"] if v) == 1),
                "trajectory": [(e["cycle"], e["passed"], e["sep"]) for e in self._sep_log],
                "reads": ("passed_per_call {1: n} means one member contributed and the argmax "
                          "had no competition. >=2 with agreement means the members are not "
                          "independent. >=2 with one dominating is the only reading that makes "
                          "the selector the subject")}

    def ties(self) -> dict:
        """Tied-at-top counts for the discriminate branch. `{1: n}` means the winner was
        alone every time and the selector is doing what it says; any mass at `>= 2` is
        `self.actions` order breaking a tie, which is arbitrary and stable."""
        return {"tied_at_max": {f"{k}:{n}": c for (k, n), c in sorted(self._ties.items())},
                "reads": ("1 = one action scored highest alone. >=2 = that many tied and "
                          "tuple order chose. A flat spread never reaches here -- the "
                          "`max > min` guard drops it to the uniform draw")}

    def _learned_split(self) -> str | None:
        """§18.4's proposer half: perception ENTERS the proposal, it does not veto.

        *The sensorium found the right self and changed nothing, because the only consumer of
        perception was the post-hoc veto.* This picks an action; it forbids none.

        **`contingency()`, NEVER `selected()`.** The question is *do any members separate
        these actions* -- an existential over members. No member is chosen, so *what kind of
        thing I am* is never consulted; only *what responded when I acted*.

        **AND IT IS NEVER SUMMED WITH `spread`.** `spread` is Gamma's prediction and this is a
        measurement; sharing a scale would be a frame scoring itself with a quantity it
        produces. Two readings, two `by` labels, so the phase can be checked against the
        mechanism instead of believed.

        **THE TIME SHAPE IS A GATE, AND THE FIRST VERSION ASSERTED IT INSTEAD.** That build
        claimed *keyed on observed actions, so it cannot separate until every action has been
        tried* -- and its own pre-registered falsifier caught it: **every action observed at
        step 22, first fire at step 2.** `contingency()` being keyed on observed actions is
        true and does not imply it; **`act` separates on ZERO evidence and that separated on
        PARTIAL evidence, which is a difference of degree.** The guard was in the claim.

        **SO THE CONDITION IS NOW IN THE CODE**: a member contributes only when every
        advertised action appears in ITS OWN dict. Not *should not* fire early -- **cannot**,
        and if it does the gate is not where this docstring says it is.

        **AND NOTHING SUMS ACROSS MEMBERS, WHICH IS LOAD-BEARING RATHER THAN TIDY.** The four
        signals are not commensurable: three report an explained fraction in [0,1] and
        `value` reports a signed count difference. Every comparison here is WITHIN one
        member; cross-member arithmetic would be a category error, and a fifth member added
        later must not introduce one.
        """
        f = getattr(self.env, "contingency", None)
        if f is None:
            return None
        sep: dict[str, int] = dict.fromkeys(self.actions, 0)
        passed = 0
        # `.items()`, NOT `.values()`: the member's NAME was being discarded, and "which member"
        # is half the question. `arc_world.contingency` keys by `m.name` and nothing read it.
        for name, rec in f().items():
            per_action, stable = rec["per_action"], rec["stable"]
            # TWO GATES, BOTH FROM THE START. Population alone is satisfied by ONE observation
            # per action, and four single values are trivially all-different -- so `sep` would
            # credit noise, which is a non-flat spread on nothing and worse than a flat one.
            #
            # AND THEY ARE COUNTED SEPARATELY. One `or` cannot say WHICH gate fired, and
            # coverage and stability are different causes with different repairs -- one number
            # asked to carry two questions is the shape caught twice this week.
            if not set(sep) <= set(per_action):
                self._members[f"{name}:no_coverage"] += 1
                continue
            if not stable:
                self._members[f"{name}:unstable"] += 1
                continue
            self._members[f"{name}:passed"] += 1
            passed += 1
            vals = {a: v for a, v in per_action.items() if a in sep}
            for a, v in vals.items():
                # DISTINCTIVE MEANS DISTINGUISHABLE FROM EVERY ALTERNATIVE, NOT FROM SOME.
                # The first version asked *differs from at least one*, which nearly every
                # action satisfies -- so `sep` came out uniform, `max == min`, and the branch
                # never fired in 150 cycles. A coding error against a stated intent rather
                # than a parameter that read wrong, which is why correcting it is not tuning.
                if all(w != v for b, w in vals.items() if b != a):
                    sep[a] += 1          # this member finds THIS action distinctive
        self._passes[passed] += 1
        self._sep_log.append({"cycle": self.cycle, "passed": passed,
                              "sep": tuple(sorted(sep.values(), reverse=True))})
        if not sep or max(sep.values()) == 0 or max(sep.values()) == min(sep.values()):
            return None
        # THE SAME ARGMAX AS `spread`'s, AND THIS IS THE ONE THAT FIRES. Measured on `g50t`:
        # `discriminate:learned` 93 of 131 acts, `discriminate` 0. The first `ties` build
        # instrumented `spread` -- the branch I had been naming -- and read empty, because it
        # never runs. Both are counted now, keyed by which dict they came from.
        top = max(sep.values())
        self._ties[("sep", sum(1 for v in sep.values() if v == top))] += 1
        return max(self.actions, key=lambda a: sep[a])

    def _advertised(self) -> None:
        """The action set is re-read every step, and a CHANGE is recorded.

        It was read once at construction and never again, so a set that varies -- ARC's
        does, per frame -- left `never_live` counting against a total that no longer
        meant what it meant. An action appearing or disappearing is a CONDITION met or
        unmet, so it is an observation and not bookkeeping.

        A PLAIN EVENT AND NOT A FOURTH CHANNEL, decided rather than defaulted: what a
        condition looks like on a real board is Phase 2's to say, and a channel built
        for a shape nobody has seen is a decomposition from a description. A plain
        event can become a channel later; a channel is harder to unbuild."""
        now = tuple(self.env.actions())
        gone = sorted(set(self.actions) - set(now))
        came = sorted(set(now) - set(self.actions))
        # §16.8 SENSOR 1 IS `the PREVIOUS ACTION changed the gating`, and the delta alone
        # does not say which action. This runs at the top of the step, so the action just
        # taken is the only candidate -- and attributing it is also sensor 2's whole input.
        #
        # NOTED EVERY STEP, INCLUDING THE STEPS THAT CHANGED NOTHING. An edge's denominator
        # is how often the predecessor was taken, and a no-change step is precisely the case
        # where it was taken and the edge did NOT fire. Returning early here counted only
        # the successes, so every edge read as a rule and none could read as gated.
        self.pre.note(self._last_action, came, gone)
        if not came and not gone:
            return
        self.led.record(self.cycle, "PERCEIVE", "@instrument", "advertised",
                        gone=gone, came=came, was=len(self.actions), now=len(now),
                        after=self._last_action,
                        note="a condition was met or unmet; the denominator moved")
        self.actions = now

    def _present(self) -> None:
        """The slot set is re-read every step, and a CHANGE is recorded.

        It was read at construction and at retarget and nowhere else, so an object
        arriving mid-episode produced NO BET, NO RESIDUAL AND NO ROW -- invisible
        rather than an error, which is why Phase 2's falsifier could not fire. Cells
        never do this and objects always will.

        A plain event, for the same reason the action set's is: what an arrival means
        on a real board is Phase 2's to say."""
        now = tuple(self.env.slots())
        # THE CARRY -- observer step 1, reviewer 2026-09-22. `came` and `gone` were computed,
        # written to one ledger row and DISCARDED, so the agent could not read its own
        # appearance/disappearance events at any later point in the cycle. They are the two
        # delta kinds `⇒` (it did not exist before) and `−` (the absence is the point) are read
        # off, and route (a) already RESPONDS to `gone` -- it drops the bindings of departed
        # slots three lines down -- without ever recording it as part of the delta.
        #
        # CLEARED ON THE NO-CHANGE PATH AND NOT ONLY SET ON THE CHANGED ONE. The early return
        # below fires on most cycles, so assigning only past it would leave the previous
        # cycle's events standing and every reader would see a change that already happened.
        # A stale event is worse than a missing one: it is indistinguishable from a real one.
        self._came, self._gone = (), ()
        if now == tuple(self.slots):
            return
        gone = sorted(set(self.slots) - set(now))
        came = sorted(set(now) - set(self.slots))
        self._came, self._gone = tuple(came), tuple(gone)
        # WHAT A DEPARTURE COSTS IS HOW MANY OF THEM WERE BOUND, AND THAT WAS NOT PUBLISHED.
        # `gone` counts slots; the loop pops bindings three lines down and no row says how
        # many there were, so *the board shed 88 slots the agent never used* and *the board
        # took 88 slots the agent had bound* are the same row. Counted BEFORE the pops.
        bound_lost = sum(1 for g in gone if g in self.bound)
        for g in gone:
            self.bound.pop(g, None)
            self.owed_import.discard(g)
            self.abstained.pop(g, None)
            # AND THE TRENDS, WHICH THIS LOOP MISSED -- F214. `_res` is only ever popped inside
            # `for slot in self.slots`, so a DEPARTED slot is never visited and its series
            # survives indefinitely. `_goal_choice` selects over `_res`, so it picks slots that
            # left the board and `_mint_routine` throws them away at `slot not in before` --
            # measured at 63% of tape refusals.
            #
            # THE RULE IS THE AUTHOR'S OWN, ONE SCALE UP: the level-boundary reset says
            # *the slots did not survive, nor do their trends*. Per-frame departure is the same
            # event and was not covered. This extends a stated rule to the site that misses it.
            self._res.pop(g, None)
            self._disc.pop(g, None)
        # a term bound to a SURVIVING slot may read an operand on a departed one, and
        # `_ops` would fault on the next bet. It owes again rather than faulting.
        orphaned = sorted(k for k, n in self.bound.items()
                          if self.gamma.library[n].operand in gone)
        for k in orphaned:
            self.bound.pop(k, None)
            self.owed_import.add(k)
        self.led.record(self.cycle, "PERCEIVE", "@instrument", "present",
                        gone=gone, came=came, orphaned=orphaned,
                        bound_lost=bound_lost,
                        # A BLIND FRAME LOOKS EXACTLY LIKE A BOARD THAT LOST EVERYTHING.
                        # `arc_world._decomposed` returns `{}` when the components sensor
                        # does not resolve, so every slot reads as departed. Measured:
                        # `long_vc33` c51 `was=88 now=0` and `sp80_wall` c31 `was=64 now=0`
                        # are both this, and both were counted as turnover.
                        blind=getattr(self.env, "blind", None),
                        was=len(self.slots), now=len(now),
                        note="an object arrived or left; a new slot has no history "
                             "and owes nothing yet")
        self.slots = list(now)
        self.alphabet = self._alphabets(self.env)
        self.slot_types = self._slot_types(self.env)

    def _guards(self, robs: list) -> list[str | None]:
        """Which actions a guard may name. **None first, and then only what R contains.**

        A guard on an action the term was never wrong under explains nothing, so the
        candidate set is the actions appearing in the residual's own observations -- *let
        the residual say where to look*, the same bound `_cannot_pay` uses. **Necessary
        condition, not a preference**: it cannot remove a guard that could have paid.

        **None first for the same reason `_bindings` puts it first** -- an unguarded term is
        cheaper, so it wins when both fit, which is Occam priced rather than preferred.
        """
        return [None, *sorted({a for _, a, _ in robs if a is not None})]

    def _operand_fits(self, cand, target: str, bind: str | None) -> bool:
        """`0a`'s TYPING half, whose trigger fired on a real board.

        `idn . recolour<o11.h>` bound a HEIGHT as a colour operator's operand. `gamma` typed
        an atom's input and output **and not its operand**, so nothing refused it.

        **A NECESSARY CONDITION, NOT A PREFERENCE.** It refuses a binding that cannot mean
        anything -- a row plus a colour -- and never ranks one binding above another. The
        narrowing costs no capability, which is the only kind of narrowing that is free.

        **AND AN UNDECLARED TYPE ADMITS.** A world with no `slot_types` and an atom with no
        `operand_type` both fall through to True: the check is absent, not passing.
        """
        want = getattr(cand, "operand_type", None)
        if bind is None or want is None or not self.slot_types:
            return True
        if want == G_SAME:
            want = self.slot_types.get(target)
        got = self.slot_types.get(bind)
        return (want is None or got is None or want == got
                or frozenset((want, got)) in COMMENSURABLE)

    def _bindings(self, slot: str, robs: list) -> list[str | None]:
        """Which slots may fill operand 0, ordered by VARIANCE and never filtered.

        **THIS IS NOT CONTACT RANKING AND THE PREVIOUS DOCSTRING SAID IT WAS.** It cited
        §16.5 and Figure 11 and then did neither: the list is EVERY other slot -- which is
        exactly what §16.5 forbids, *you do not invent the list, you read it off the world*
        -- and the order is variance, not contact. `touching()` is built and unused.

        **THE CITATION IS WHY IT SURVIVED.** A wrong implementation with no source reads as
        unfinished; with a correct source it reads as DERIVED, and so as already checked. It
        outlived a status of `built`, a report calling it *specified*, and an owed-DEMONSTRATION
        row that presupposed the mechanism existed. Read a cited clause against the CODE.

        **AND CONTACT CANNOT BE CONSULTED FROM HERE AT ALL, WHICH IS THE HONEST REASON.** The
        loop sees `env.slots()` (names) and `env.observe()` (name -> int). `touching(a, b)`
        needs two object dicts with cells, and objects live inside the decomposition. **A
        relation is not a slot, so it never crosses into the loop** -- and making it cross IS
        §16.5, not a step before it. Approximating contact with a proxy available here would
        be the same defect with a better docstring.

        WHAT IT ACTUALLY DOES. None first -- a unary term is cheaper, so it wins when both
        fit, which is Occam priced rather than preferred. Then by how much each slot VARIES
        across the residual's own frames: a slot constant wherever the bound term was wrong
        carries nothing that could discriminate those frames, so it is tried last. That is a
        real signal and a defensible order. It is not the specified one.

        ORDERING, NEVER EXCLUSION, and the difference is measured rather than argued.
        The version that DROPPED operand-reading terms when R showed no dependence on
        another slot LOST A CLOSING TERM -- `_cannot_pay` records it. Ranking cannot:
        every binding is still reached, and since the mint breaks on the first closer,
        order decides WHICH closer is found and never WHETHER one exists."""
        others = [s for s in self.slots if s != slot]
        if _DELTA_OPERANDS and robs:
            others = self._delta_narrowed(others, robs)
        seen = {s: len({st[s] for st, _, _ in robs if s in st}) for s in others}
        # CONTACT FIRST, THEN VARIANCE. §16.5: *list everything in contact with the residual,
        # then what is in contact with those, and outward until the cascade stops mattering --
        # you do not invent the list, you read it off the world.* The docstring above records
        # that this returned EVERY other slot ordered by variance, which §16.5 forbids, and
        # that `touching()` was built and unused. **`priors.contact_first` was the only BIAS
        # declared without a function**, cited to Michotte 1946, and this is it.
        #
        # **STILL ORDERS AND STILL REMOVES NOTHING.** §12.1 admits a bias only as a *ranked,
        # reversible cut*, and a filter here would make contact decide REACHABILITY rather than
        # order -- which is the first ring of the cascade mistaken for the whole of it.
        owners = self._slot_owners(self.env)
        touch = getattr(self.env, "contacts", None)
        near: set[str] = set()
        if touch is not None and owners:
            mine = owners.get(slot)
            adj = set(touch().get(mine, ()))
            near = {s for s in others if owners.get(s) in adj}
        rank = contact_first(near)
        return [None] + sorted(others, key=lambda s: (*rank(s), -seen[s], s))

    def mint(self, slot: str) -> None:
        # THE RECIPES ALREADY HELD, once per mint rather than per candidate. A library Term's
        # chain is its atoms joined; `enumerate_closure` yields BARE chains, so `cand.name` is
        # exactly this key. O(library) against a per-candidate walk that is orders larger.
        self._held_chains = {" . ".join(a.name for a in t.atoms)
                             for t in self.gamma.library.values()}
        hist = self.history(slot)
        held = self.gamma.library[self.bound.get(slot, IDN)]
        base = self._accumulated(slot, held)
        robs = self._residual_obs(slot, held, hist)
        # HOISTED, because `units()` rebuilds a list and the pricing runs once per candidate.
        _units = tuple(self.gamma.units())
        # THE CHEAPEST TERM THE COST FUNCTION ADMITS. `pays` is `cost + left < base`,
        # `_left` is a sum of non-negative bits, and `term_bits` is monotone in `k` with
        # `length() >= 1` -- so `floor >= base` proves NO term pays, at any depth, under
        # any binding, before a candidate is enumerated. Same lemma as the inner break
        # 170 lines down, applied as a precondition instead of a stopping rule.
        floor = term_bits(1, self.gamma.alphabet)
        guards = {"support": base > 0.0, "reachability": False, "novelty": False}
        cuts: list[dict] = []
        best: tuple[float, float, float, Term] | None = None
        stats: dict = {"seen": 0, "budget_spent": False, "depth_exhausted": True,
                       "units": self.gamma.alphabet, "estimate": 0}
        by_kind: dict[str, tuple] = {}
        wanted: tuple[float, Term] | None = None
        rank = 0

        if guards["support"] and base > floor:
            # THE GAP IS ALREADY CHARACTERISED FOR RETRIEVAL; the search gets the same key.
            # §23.5: retrieval and the rank function are PREREQUISITES for a loaded library,
            # *otherwise loading makes the agent worse by drowning every search* -- and the
            # library is loaded by design as of the persistence ruling.
            rel = getattr(self.env, "contact_changes", None)
            gap = retrieval.characterise(robs, slot, list(self.alphabet), self.slot_types,
                                         relations=rel() if rel else None)
            # HOISTED. `_bindings` depends on `slot` and `robs` and not on the candidate, and
            # it was being rebuilt identically for every one -- an owner map, a contact set and
            # a variance count per candidate. Computed once here; the ORDER is unchanged.
            operand_binds = self._bindings(slot, robs)

            # TWO STREAMS, ONE BARGAIN. A `val` term IS a prediction; an OBJ term is a WANT,
            # and `objective_step` turns it into one -- so both produce a predicted slot value
            # and both are priced by how well it matched. **They compete on the same residual
            # ground, which is what `cost + left < base` was always for**, and nothing about
            # the bargain changes to let them.
            #
            # THE OBJECTIVE STREAM STARTS AT THE SLOT'S OWN TYPE, NOT AT `OBJECT`. The loop
            # hands a SCALAR, so an `OBJECT`-typed chain abstains on its first atom -- which
            # `_extract` states at its own site and which cost several rounds of calling this
            # query `OBJECT -> OBJ`.
            streams = [("val", "val")]
            stype = self.slot_types.get(slot)
            if stype:
                streams.append((stype, OBJ_TYPE))
            # THE out_type WIDENING -- Isaiah's 3A, arm `TETHER_STREAM_WIDEN`, default OFF.
            #
            # THESE TWO STREAMS ARE THE COMPOSITION CEILING, measured rather than argued: the
            # agent mints 74 multi-atom terms on `ar25` and gets FOUR distinct compositions --
            # `translate . recolour` and `above . {all,any,none}` -- which ARE these two
            # streams. The type graph admits 682 type-checking pairs; mint asks for two.
            # **More instances, never more structures, because two streams are all that is
            # ever asked for.**
            #
            # BOUNDED BY THE DELTA, NEVER BY THE TYPE GRAPH'S CAPACITY, and that is the whole
            # safety argument. `gap["varies_types"]` is what the CURRENT residual actually
            # involves -- the graph says which pairs are LEGAL, the delta says which are
            # RELEVANT NOW. Widening to the graph's capacity would rebuild the enumeration
            # explosion deliberately.
            if _STREAM_WIDEN and stype:
                seen_out = {o for _i, o in streams}
                for t in (gap.get("varies_types") or ()):
                    if t and t not in seen_out:
                        streams.append((stype, t))
                        seen_out.add(t)
            # THE THIRD STREAM IS WITHDRAWN, AND THE REASON IS A DEFECT IT INTRODUCED.
            # `OBJECT -> OBJ` was legitimate once `Ctx.obj` stopped the extract atoms
            # abstaining -- and it is NOT type-coherent, which the reachability check missed.
            #
            # `Ctx.group` is resolved for THE SLOT'S attribute: on `o0.row` it holds the other
            # objects' ROW values. An extract atom changes which attribute the chain carries,
            # and the group does not follow -- so `colour . all_same . all` on `o0.row`
            # compares o0's COLOUR against a group of ROWS. **Measured: colour 6 against
            # `(0,)`, answered 0.** Well-typed and meaningless, which is `above(shape)`'s
            # family at a site this build created.
            #
            # `operand_type` does not catch it: that guards the OPERAND BINDING, not `group`.
            # The two-stream form has no such hole -- a chain starting at the slot's own type
            # carries that attribute, so the group matches BY CONSTRUCTION.
            #
            # WHAT WOULD RESTORE IT: `group` keyed by the attribute the chain currently
            # holds, which `Ctx` cannot know because it is built once, before the chain runs.
            # That is a design question, not a parameter.
            by_kind: dict[str, tuple] = {}

            for in_t, out_t in streams:
                # A THIRD KIND EXISTS ONCE THE STREAMS WIDEN, and it is named rather than
                # folded into `objective`: a term ending at EXTENT is neither a prediction of
                # the slot's next value nor a complete objective, and calling it one would put
                # two quantities under one label at the site the contest is decided.
                kind = ("predictor" if out_t == "val"
                        else "objective" if out_t == OBJ_TYPE else f"typed:{out_t}")
                by_fit = partial(retrieval.fits, gap=gap, in_type=in_t, out_type=out_t)
                st: dict = {"seen": 0, "budget_spent": False, "depth_exhausted": True,
                            "units": self.gamma.alphabet, "estimate": 0}
                for cand in self.gamma.enumerate_closure(in_t, out_t, self.cfg.max_depth,
                                                         self.cfg.budget, st, order=by_fit):
                    if rank >= self.cfg.work_budget:
                        st["budget_spent"] = True
                        break
                    binds = operand_binds if cand.reads_operand else [None]
                    binds = [x for x in binds if self._operand_fits(cand, slot, x)]
                    for bind, g in ((b, g) for b in binds for g in self._guards(robs)):
                        rank += 1
                        term = Term(cand.atoms, operand=bind, guard=g)
                        if self.gamma.is_atom(term) or term.name in self.gamma.library:
                            cuts.append({"name": term.name, "rank": rank, "reversible": True,
                                         "reason": "not-novel"})
                            continue
                        # THE RECIPE, NOT THE INSTANCE -- ARM F. Reported ALWAYS so the rate is
                        # visible on the baseline too; ACTED ON only under the arm.
                        if cand.name in self._held_chains:
                            # AND WHETHER THE HELD RECIPE WAS EVER CONFIRMED. Isaiah: settled
                            # vs unsettled is how the agent knows what WORKS from what is
                            # UNTRIED. Recorded, NOT ranked on -- ordering retrieval by it
                            # would install a preference that is the agent's to reason.
                            cuts.append({"name": term.name, "rank": rank, "reversible": True,
                                         "reason": "recipe-held", "recipe": cand.name,
                                         "recipe_settled": self.gamma.is_settled(cand.name)})
                            if _RECIPE_DEDUP:
                                continue
                        guards["novelty"] = True
                        # PRICED IN UNITS, so a settled sub-composition costs what the
                        # ground already paid for it. `routine.length`'s rule, applied to
                        # the space it was always stated over.
                        cost = term_bits(self.gamma.length(term, _units),
                                         self.gamma.alphabet)
                        # LET THE RESIDUAL SAY WHERE TO LOOK. Walking the whole history for
                        # every candidate is exhaustive search; R already names the
                        # observations that need fixing, and a term that cannot fix enough of
                        # them is refused without the walk. 6.7x less work over the panel and
                        # nothing lost, because the bound is necessary rather than plausible.
                        if self._cannot_pay(term, slot, robs, cost, base):
                            cuts.append({"name": term.name, "rank": rank, "reversible": True,
                                         "reason": "bounded-out: cannot pay on R alone"})
                            self.gamma.book["bargain_bounded_out"] = (
                                self.gamma.book.get("bargain_bounded_out", 0) + 1)
                            # **ISAIAH'S RULING, 2026-09-24: THE TREE IS JUDGED BY ITS OWN
                            # BOUND.** *`_cannot_pay` applied to the tree route using a figure
                            # COMPUTED ON A DIFFERENT TERM is a DEFECT, not a policy.* A tree is
                            # a different function from its flat parent and can be right where
                            # the parent is wrong, so the parent's bound says nothing about it
                            # -- and the bound's whole value is that it is NECESSARY *for the
                            # term it was computed on*.
                            #
                            # **NO ARM.** `TETHER_TREE_BOUND` was a workaround for this defect
                            # and is removed. The route opens WITHOUT a blanket widening,
                            # because every tree still pays `_cannot_pay` AND `pays` on its own
                            # terms -- nothing enters that the bargain would not admit.
                            # **A TREE MUST BE NOVEL TOO, AND NOTHING CHECKED IT.** The flat
                            # term is refused as `not-novel` when it is an atom or already in
                            # the library; the tree path had no such check at either site.
                            # **The dead branch hid it** -- with `_trees` reaching nothing, a
                            # duplicate tree never got as far as `accept`. Opening the route
                            # surfaced it immediately as `ValueError: already in library`.
                            #
                            # **A SECOND PRE-EXISTING DEFECT, NOT A CHANGE TO THE BOUND** --
                            # reported as such. A route that opens onto a crash is not open.
                            for bt in self._trees(cand, bind, g):
                                if self.gamma.is_atom(bt) or bt.name in self.gamma.library:
                                    continue
                                bcost = term_bits(self.gamma.length(bt, _units),
                                                  self.gamma.alphabet)
                                if self._cannot_pay(bt, slot, robs, bcost, base):
                                    continue
                                bleft = self._left(bt, slot, hist)
                                if not pays(bcost, bleft, base):
                                    continue
                                btotal = bcost + bleft
                                if kind not in by_kind or btotal < by_kind[kind][0]:
                                    by_kind[kind] = (btotal, bleft, bcost, bt)
                                if best is None or btotal < best[0]:
                                    best = (btotal, bleft, bcost, bt)
                            continue
                        left = self._left(term, slot, hist)
                        # §4's TREE, AND THIS IS ITS FIRST PRODUCER. `operand_term` was
                        # DECLARED, RENDERED, PRICED and APPLIED (`_ops`, :914) with ZERO sites
                        # constructing one -- so every term the agent has ever composed is a
                        # FLAT CHAIN. The consumer was finished; the producer did not exist.
                        #
                        # **HERE AND NOT IN `_reach`, MEASURED RATHER THAN READ.** Built at
                        # `_reach` first on the strength of that site's operand comment --
                        # and `_reach` is called ZERO times in four cycles of `vc33` while
                        # `_operand_fits` fires 850,833 times from HERE. **The site that READS
                        # like the producer is not the site that RUNS.**
                        #
                        # **AND IT COMPETES RATHER THAN RESCUING, WHICH IS ALSO MEASURED.** It
                        # sat in the `does-not-pay` branch first -- *a tree is what you reach
                        # for when the chain could not say it* -- and that branch is nearly
                        # dead: `_cannot_pay` cuts 346,992 of 347,494, only 502 candidates
                        # reach `pays`, and 502 of them PASS. **29 failures in a whole run, so
                        # the rescue site had almost no occasions.** The 502 survivors are
                        # what R says could matter, so the tree is offered THERE and priced by
                        # the same bargain as everything else. ~2 extra evaluations per
                        # survivor against 347k already spent.
                        #
                        # **AND THE ARGUMENT ABOVE INVERTS WHEN THE SURVIVOR COUNT IS ZERO --
                        # `F348`, 2026-09-24.** Measured on `vc33`: the bargain book reads
                        # 5268 bounded out, 0 reaching `pays`, and **`_trees` is called ZERO
                        # times in three cycles.** A mechanism attached to the survivors of a
                        # filter dies exactly when the filter tightens, and nothing recomputes
                        # the premise a placement was chosen under.
                        #
                        # **THE COST ARGUMENT IS STILL RIGHT AND IT WAS NEVER THE PROBLEM.**
                        # The problem is that `_cannot_pay` is NECESSARY *for the term it was
                        # computed on*, and a tree is a different function -- so gating trees
                        # on the FLAT term's bound is the one use that bound cannot support.
                        # **REPAIRED 2026-09-24 under Isaiah's ruling**: the bounded-out
                        # branch now offers trees under their OWN `_cannot_pay`, with no arm,
                        # and this site applies the same bound as a short-circuit.
                        for bt in self._trees(cand, bind, g):
                            if self.gamma.is_atom(bt) or bt.name in self.gamma.library:
                                continue
                            bcost = term_bits(self.gamma.length(bt, _units),
                                              self.gamma.alphabet)
                            # **THE SAME BOUND HERE, AND IT CHANGES NO OUTCOME.** `_cannot_pay`
                            # PROVES `cost + left >= base`, which is exactly `not pays` -- so
                            # anything it refuses, `pays` refuses too. A short-circuit, not a
                            # new filter, which is what makes this repair byte-identical where
                            # the bound was already correct.
                            if self._cannot_pay(bt, slot, robs, bcost, base):
                                continue
                            bleft = self._left(bt, slot, hist)
                            if not pays(bcost, bleft, base):
                                continue
                            btotal = bcost + bleft
                            if kind not in by_kind or btotal < by_kind[kind][0]:
                                by_kind[kind] = (btotal, bleft, bcost, bt)
                            if best is None or btotal < best[0]:
                                best = (btotal, bleft, bcost, bt)
                        if not pays(cost, left, base):
                            cuts.append({"name": term.name, "rank": rank, "reversible": True,
                                         "reason": "does-not-pay"})
                            # BOOK 5, AND IT IS THE ONE `pays` WOULD NEED. `F341` sorted `pays`
                            # strictness as THE AGENT'S and the reviewer left it untouched
                            # because it has no book deep enough. This is that book, and it is
                            # THREE COUNTS rather than a margin, because the three answer the
                            # question and a margin would need a boundary I picked.
                            #
                            # **THE SPLIT IS THE FINDING WAITING TO BE READ.** `_cannot_pay` is
                            # a NECESSARY condition -- *a term wrong on k of R is wrong at
                            # least k* -- so what it refuses is LOGICALLY incapable, not
                            # refused by a constant. `pays` is the only one of the two that is
                            # a judgement. If `bounded_out` dwarfs `does_not_pay`, then
                            # relaxing the strictness changes almost nothing and the contest is
                            # decided by logic rather than by anything the agent could set:
                            # `F342`'s shape, at the site `F342` named first.
                            self.gamma.book["bargain_does_not_pay"] = (
                                self.gamma.book.get("bargain_does_not_pay", 0) + 1)
                            # **A WANT IS RETAINED EVEN THOUGH IT DID NOT PAY -- ISAIAH,
                            # 2026-09-25: *a want proves itself by RECURRING across attempts,
                            # not by explaining a frame.*** `pays` is `cost + left < base` and
                            # `left` IS explanation, so requiring a want to pay judges it on
                            # exactly the thing the ruling says does not prove it.
                            #
                            # **AND THIS SITE IS WHY `wants` HAS ALWAYS BEEN EMPTY.** `F360`
                            # measured `by_kind` holding only `predictor`, and `F357` measured
                            # 0 of 2,695 objectives paying -- so the `wants` write below could
                            # never fire. The channel existed and nothing could reach it.
                            #
                            # RANKED BY COST ALONE, which is DESCRIPTION LENGTH and not
                            # explanation -- the cheapest way to say this want. It is a
                            # tie-break for retention, never a verdict: standing comes from
                            # recurrence under a resembling shape, which is `_note_want`.
                            if kind == "objective" and (wanted is None or cost < wanted[0]):
                                wanted = (cost, term)
                            continue
                        self.gamma.book["bargain_paid"] = (
                            self.gamma.book.get("bargain_paid", 0) + 1)
                        guards["reachability"] = True
                        # `cost + left`, WHICH IS WHAT `pays` SPENDS. This compared `left`
                        # alone -- *buy the most-explaining term at any price* -- and the
                        # bargain's whole content is that explanation is bought WITH
                        # description. The currency was never mine to pick: `pays` is
                        # `cost + left < base` and its docstring already called the strictness
                        # a feature. Read, not designed.
                        #
                        # It decided a reading. On the two-arm board both arms field a term at
                        # `left = 0.0`, so under the old comparison they TIED at 0.0 and the
                        # winner fell to `by_kind` insertion order -- which is stream order,
                        # which is `("val","val")` first. **`winner=predictor` was the dict
                        # remembering who arrived, not the bargain preferring anyone.**
                        # **THE PRECONDITION -- Isaiah 2026-09-24. A candidate that says
                        # nothing different about anything still OPEN is a daydream, and the
                        # bargain cannot see the difference: `cost + left < base` reads
                        # explanation and never asks whether the explained thing was in play.
                        # Refused BEFORE the contest, so a spectator cannot even be a champion.
                        if not self.bears_on(term, slot, robs, held):
                            self.gamma.book["mint_no_residual"] = (
                                self.gamma.book.get("mint_no_residual", 0) + 1)
                            continue
                        total = cost + left
                        if kind not in by_kind or total < by_kind[kind][0]:
                            by_kind[kind] = (total, left, cost, term)
                        if best is None or total < best[0]:
                            best = (total, left, cost, term)
                    # AND THE STOPPING BOUND HAS TO BE NECESSARY, WHICH `left == 0.0` WAS NOT.
                    # Enumeration is ordered by retrieval fit, not by cost, so a term that
                    # explains everything says nothing about what a LATER, SHORTER one totals:
                    # `cost 5, left 0` loses to `cost 1, left 0.5`. Under the corrected currency
                    # the old test is also dead -- cost is strictly positive, so a total of
                    # exactly 0.0 cannot occur, and the break would have gone silent rather
                    # than wrong.
                    #
                    # The floor is the cheapest term the cost function admits, `k = 1`, and
                    # `term_bits` is monotone in `k`. Nothing remaining can beat an incumbent
                    # already at or under it. Necessary, like `_cannot_pay`'s bound.
                    if best is not None and best[0] <= term_bits(1, self.gamma.alphabet):
                        break
                stats["seen"] += st["seen"]
                stats["estimate"] += st["estimate"]
                stats["budget_spent"] = stats["budget_spent"] or st["budget_spent"]
                # NO BREAK ACROSS STREAMS. There was one, and it made the contest a FALLBACK
                # CHAIN rather than a contest: `("val","val")` runs first, so a predictor that
                # explained perfectly ENDED THE SEARCH and the objective stream was never
                # asked -- while `contest` recorded `margin: None`, whose own comment reads
                # *the other stream fielded nobody*. **Never-asked and fielded-nobody are
                # different claims, and the first was being written as the second.**
                #
                # The INNER break stays: within one stream, a bound on that stream's own
                # search skips nobody who was going to be asked.

        # WHICH KIND WON THE SLOT, AND BY HOW MUCH. The residual alone buries the answer:
        # *did an objective ever out-predict a plain value bet* is the question the two-stream
        # query exists to ask, and a single `left` number cannot say which kind produced it.
        # Same shape as `by` naming the carrying self-hypothesis -- the reading says WHICH,
        # not only how well. `None` on either side means that stream fielded no payer, which
        # is a different claim from losing.
        # REPORTED IN THE CURRENCY THAT DECIDED IT. This published `left`, so two arms that
        # both explained perfectly printed `0.0` and `0.0` with a `margin` of `0.0` -- a tie
        # on the readout that was not a tie in the bargain, because their COSTS differed and
        # cost is half of what `pays` spends. A contest reported in a quantity other than the
        # one it was decided by is not a reading of the contest.
        contest = {k: round(v[0], 4) for k, v in sorted(by_kind.items())} if best else {}
        # GUARDED ON THE KEYS, NOT ON THE COUNT. `len(contest) == 2` was safe while there were
        # exactly two kinds; the widening admits a third, and two kinds that are `predictor`
        # and `typed:EXTENT` would have raised a KeyError here. The margin is a PREDICTOR vs
        # OBJECTIVE reading and says nothing about a third kind, so it is computed only when
        # both are actually present.
        if "predictor" in by_kind and "objective" in by_kind:
            contest["margin"] = round(abs(by_kind["predictor"][0]
                                          - by_kind["objective"][0]), 4)
            # A TIE IS A READING, AND NAMING A WINNER ERASES IT. `term_bits(k, alphabet)` is a
            # function of LENGTH and ALPHABET and of nothing else, so two terms of equal depth
            # cost the same to the bit whatever atoms they are built from. When both arms also
            # drive `left` to zero the totals are IDENTICAL, `min` returns whichever key the
            # dict holds first, and `by_kind` fills in stream order -- so `winner` reported
            # `predictor` as a preference the bargain never expressed.
            #
            # Measured, two-arm board, `o1.col`: `translate . recolour<o2.col>` against an
            # objective, both depth 2, both `left = 0.0`, both 13.3783 against a base of
            # 15.2290. **The bargain prices HOW LONG, never WHAT KIND** -- the two arms are
            # separable only when their depths differ, and then by the whole 4.4594 bits
            # between a two-atom term and a three-atom one.
            #
            # NOT BROKEN HERE, AND DELIBERATELY. Ruling that an objective outranks a predictor
            # at equal cost answers the question the two streams exist to ASK. The tie is
            # published as a tie; whatever breaks it has to earn its way in.
            contest["winner"] = ("tie" if contest["margin"] == 0.0
                                 else min(by_kind, key=lambda k: by_kind[k][0]))
        elif contest:
            contest["winner"] = next(iter(by_kind))
            contest["margin"] = None      # unopposed: the other stream fielded nobody

        seen = stats["seen"]
        est = max(stats["estimate"], seen)
        detail = {"guards": guards, "candidates_seen": seen, "candidates_tried": rank,
                  "contest": contest,
                  "code": CODE, "base_bits": round(base, 3), "cuts": cuts[:12],
                  "budget_exhausted": bool(stats["budget_spent"]),
                  "depth": self.cfg.max_depth, "units": stats["units"],
                  "space_estimate": est,
                  "coverage": round(seen / est, 6) if est else 0.0}

        if best is None:
            # THE VERDICT IS NOT ONE WORD. "I stopped early" and "the whole space at this
            # depth does not contain one" are different claims and only one is strong.
            if not guards["support"]:
                detail["verdict"] = "no_support"
            elif base <= floor:
                # A THIRD WORD, BECAUSE THE OTHER TWO BOTH MISREPORT IT. `no_support` says
                # the residual is empty and it is not; `depth_exhausted` says the space was
                # searched and it was not -- and it sends the next reader at DEPTH, the one
                # remedy that provably cannot help. This is not an abstention from an
                # incomplete search: nothing was searched because the arithmetic closed it.
                #
                # AND IT IS A WAIT, NOT A FAILURE. `base` grows with the slot's history, so
                # a residual under the floor crosses it once the ground has shown enough to
                # be worth a term -- measured on `ls20`: o10.col 6.00 at hist 2, 12.00 at
                # hist 3, and the search ran. Nothing is given up, only deferred to when it
                # could have succeeded.
                detail["verdict"] = "under_floor"
                detail["note"] = ("the residual is smaller than the cheapest term the cost "
                                  "function admits, so no term pays AT ANY DEPTH. Proved, "
                                  "not searched -- check base_bits against floor_bits")
                detail["floor_bits"] = round(floor, 3)
            elif stats["budget_spent"]:
                detail["verdict"] = "budget_spent"
                detail["note"] = (f"stopped early; coverage {detail['coverage']:.4f}. "
                                  "Says nothing about whether a term exists")
            elif not guards["novelty"]:
                detail["verdict"] = "not_novel"
                detail["note"] = "the machinery worked; the answer was already known"
            else:
                detail["verdict"] = "depth_exhausted"
                detail["note"] = ("the whole space at this depth was seen and none paid; "
                                  "not at this depth, NOT unreachable")
            detail["base_bits"] = round(base, 3)
            if detail["verdict"] == "no_support":
                self._starved.add(slot)
            # `under_floor` OWES LIKE THE OTHER TWO, and the write site at `accept` is what
            # decides it: *the slot keeps owing until something closes R* -- a fact about the
            # SLOT, not about the search. Its residual is unclosed, so it owes. Leaving it out
            # dropped five of six slots from the retro sweep's target list on a six-cycle run,
            # which is a capability loss wearing a speedup's clothes. The search is skipped;
            # the debt is not.
            if detail["verdict"] in ("budget_spent", "depth_exhausted", "under_floor"):
                self.owed_import.add(slot)
                self.abstained[slot] = {"depth": self.cfg.max_depth, "candidates": seen,
                                        "coverage": detail["coverage"],
                                        "verdict": detail["verdict"],
                                        "units_then": stats.get("units", 0),
                                        "base_bits": round(base, 3)}
                if _INVENT:
                    self._invent(slot, self.abstained[slot], hist)
            self.led.record(self.cycle, "MINT", slot, "park", of=(slot,), **detail)
            return

        # THE CONSUMER -- Isaiah, 2026-09-24. **`by_kind` WAS COMPUTED, PUBLISHED AND READ BY
        # NOTHING**: it keeps the best candidate PER KIND and `best` installed the single lowest
        # `cost + left` across all of them, so an objective could PAY THE BARGAIN, be recorded as
        # its kind's champion, and be dropped on the floor. Measured on the toy world: OBJ passes
        # `pays` twice and never binds once.
        #
        # **HIS RULING IS A QUEUE, NOT A VERDICT.** *"System 2 is the long-term thinker, system 1
        # more reactive... sometimes option 1 is urgent and important and binding so it gets cut
        # in line."* A binding verdict is wireheading-adjacent -- whatever wins an argument
        # instantly becomes what you want, with no check against existing commitments -- so the
        # losing kind is RETAINED rather than discarded.
        #
        # **AND THE RANK IS TIME-TO-CONSEQUENCE, NOT IMPORTANCE.** *"There are certain things that
        # will kill me soonest. Food is not less important -- it is FURTHER AWAY."*
        #
        # **WHAT COUNTS AS *SOON* IS THE AGENT'S AND IS NOT SEEDED HERE.** `consequence_in` reads
        # the agent's own earned record and returns `None` until it has one; with `None` the order
        # falls back to `total`, which is **exactly what `best` already chose**, so this installs
        # the mechanism and changes NO run. The queue exists, the preemption path exists, and
        # both are inert until the board fills the dial -- the same shape as `REJECTION_CEILING`.
        queue = self._rank_by_consequence(by_kind, best)
        if queue:
            best = queue[0]
            detail["queued"] = [k for k, _v in self._queue_kinds]
        # **THE TAIL IS KEPT, AND THAT IS THE WHOLE OF THE CHANGE.** The head installs into
        # `bound` exactly as before; an OBJ-typed champion that did not win is written to
        # `wants` rather than dropped. Nothing about WHO ACTS moves.
        _obj = by_kind.get("objective")
        if _obj is not None:
            self.wants[slot] = _obj[3].name
            detail["want"] = _obj[3].name
        elif wanted is not None:
            # THE RULING'S PATH, and the only one that has ever had traffic. A want that lost
            # the contest is still WANTED; what it does not get is the right to ACT.
            self.wants[slot] = wanted[1].name
            detail["want"] = wanted[1].name
            detail["want_paid"] = False
            self.gamma.book["want_retained_unpaid"] = (
                self.gamma.book.get("want_retained_unpaid", 0) + 1)
        _total, left, cost, term = best
        detail["explained"], detail["overclaimed"] = self.explain(slot, base - left)
        self.gamma.accept(term, seq=len(self.led), residual=f"{slot}@{self.cycle}")
        self.bound[slot] = term.name
        self.rank.note(term.name, self.cycle)
        closes = left == 0.0
        # Q7: THE MINT MAKES A CANDIDATE; THE GROUND SETTLES IT BY HELD-OUT PAYMENT. *A
        # candidate becomes accepted once it predicts transitions it was never fitted to.*
        # Candidacy was gated on `closes` and NOTHING EVER CLOSED -- 13 of 13 and 7 of 7 paid
        # without closing -- so `candidates` stayed empty, `settle()` never fired, `units()`
        # was 17 atoms at step 1 and 17 at step 20, and the composite system had ONE LEVEL
        # structurally. Chunk reuse read zero as a TAUTOLOGY, not as a finding.
        #
        # THE SLOT STILL OWES, AND THAT IS UNCHANGED. *The slot keeps owing until something
        # closes R* is true and is a fact about the SLOT -- `owed_import` keeps it. Whether
        # the TERM is a real regularity is Q7's separate question and the ground answers it on
        # a later step. §14.2 is the guard that makes this safe: an unsettled term is *usable
        # as a slot's binding, NOT as a building block*, and `units()` admits settled only --
        # which is Q7's *held but not cited*, already built.
        self.candidates[term.name] = self.cycle
        if closes:
            self.owed_import.discard(slot)
            self.abstained.pop(slot, None)
        else:
            self.owed_import.add(slot)
        # THE CONTACT CLAUSE, RECORDED HERE BECAUSE IT CANNOT BE RECOVERED LATER. Contact is a
        # fact about THIS frame and `summary` reads after the run, so *bound to a slot that was
        # in contact* has to be written when the binding is chosen. Same shape as `level` on the
        # repeat row: the reader forces a field the ledger did not carry.
        detail["operand_in_contact"] = None
        if term.operand:
            owners = self._slot_owners(self.env)
            touch = getattr(self.env, "contacts", None)
            if owners and touch is not None:
                adj = set(touch().get(owners.get(slot), ()))
                detail["operand_in_contact"] = owners.get(term.operand) in adj
        detail["verdict"] = "pays"
        detail["closes"] = closes
        if not closes:
            detail["note"] = "pays but does not close R; the slot still owes"
        detail.update(term=term.name, term_depth=len(term), operand=term.operand,
                      term_bits=round(cost, 3), left_bits=round(left, 3))
        # **§14.7's CHUNK REUSE COUNT, SPECIFIED IN THE CORPUS AND COMPUTED NOWHERE.**
        # *How often a term appears as a CONSTITUENT of a later mint* -- a composition event,
        # not a reading of R, which is why `behaviour.py` separates it from the per-slot rule.
        # `chain.reuse_branch` is the RETRIEVAL path and a different quantity entirely.
        #
        # **IT IS THE ONLY EVIDENCE THE CHUNKING CLAIM HAS LEFT.** `F349`: the falsifier does
        # not falsify -- `ladder` is declared unreachable in atoms and `dbl . dec . neg` reaches
        # it at depth 3 -- and the winning NAME is identical whether the chain was found through
        # a settled unit or through atoms. **So the claim is unproven in both directions, and
        # nothing recorded which route was taken.** This records it.
        #
        # **A RECORD, NOT A DIAL, AND NOT A CALIBRATION CHANGE.** It touches neither the toy
        # world, nor `max_depth`, nor the atom set -- the three repairs `F341`'s third category
        # says are not the seat's to take. Nothing reads it.
        #
        # TWO ATOMS MINIMUM: a one-atom unit is in every chain that uses that atom, so counting
        # it would measure the alphabet rather than reuse. And SETTLED EARLIER than this cycle,
        # because a term cannot have been a constituent of the mint that produced it.
        for _nm, _u in self.gamma.library.items():
            if (_nm != term.name and len(getattr(_u, "atoms", ())) >= 2
                    and self.gamma.is_settled(_nm)
                    and _contains(term.atoms, _u.atoms)):
                self.gamma.book["chunk_reuse"] = self.gamma.book.get("chunk_reuse", 0) + 1
        self.led.record(self.cycle, "MINT", slot, "mint", of=(slot,), **detail)
        self.led.record(self.cycle, "ACCEPT", slot, "accept", term=term.name,
                        origin=term.origin, seq=len(self.led),
                        status="candidate", cited="no: candidate may be held, not cited")
        self.chain.note_mint()
        self.sweep(term, slot)

    def _reach(self, slot: str, hist: list, slots: list) -> tuple[float, Term] | None:
        """Re-run the search for a parked slot because the UNIT SET grew.

        This is the chunking claim made falsifiable: closure(Gamma) is unchanged and no
        atom was added, but a settled term now counts as one unit, so a composition that
        was past max_depth in atoms can be within it in units. No actions are spent -- it
        re-reads evidence already on the trace -- so it is search cost, never budget.
        """
        best = None
        for cand in self.gamma.enumerate_closure("val", "val", self.cfg.max_depth,
                                                 self.cfg.budget):
            for bind in [None] + [s2 for s2 in slots if s2 != slot]:
                # `_operand_fits` IS ALREADY RULED AND THIS SITE NEVER CALLED IT. Its own
                # docstring: *a NECESSARY CONDITION, NOT A PREFERENCE -- it refuses a
                # binding that cannot mean anything, a row plus a colour*, and *the
                # narrowing costs no capability*. `mint` applies it; `_reach` scored those
                # bindings and picks by `left` ALONE, so one could win here. This is the
                # existing ruling applied at the site that lacked it, not a new decision.
                if not self._operand_fits(cand, slot, bind):
                    continue
                t = Term(cand.atoms, operand=bind)
                # BRANCH AND BOUND, and `_reach` had no bound of any kind -- 323,400 of
                # 333,000 `_left` calls on a nine-cycle ls20 run against `mint`'s 2,193,
                # each walking the whole history. The incumbent is the ceiling.
                left = self._left(t, slot, hist, ceiling=best[0] if best else None)
                if best is None or left < best[0]:
                    best = (left, t)
                if left == 0.0:
                    return best

        return best

    def sweep(self, term: Term, origin_slot: str) -> None:
        """Re-run a newly accepted term against every outstanding parked residual.

        Costs no actions -- it re-reads evidence already paid for. A term minted for one
        slot that explains another slot's old residual is an operator REUSED on a task it
        was not minted for, which is the stated bar for the loop firing once. Targets come
        from this level (which the mint also revisits) and from earlier levels (which it
        never does -- the only place the sweep is irreplaceable).
        """
        units_now = len(self.gamma.units())
        targets = [(s, s, self.history(s), self.abstained.get(s, {}), self.slots)
                   for s in sorted(self.owed_import - {origin_slot})]
        targets += [(k, r["slot"], r["hist"], r, r["slots"])
                    for k, r in sorted(self.parked.items())]

        def stale(rec: dict) -> bool:
            """`depth_exhausted` is not permanent. It means 'the whole space AT THIS UNIT
            SET', so a settled chunk that adds a unit retracts it."""
            # BOTH EXHAUSTED WORDS, because `stale` reads the verdict STRING and P1 added
            # one. Renaming a park verdict silently made five slots always-eligible on a
            # six-cycle run -- a behaviour change smuggled in by a word, at a site 150 lines
            # from the rename. P1's warrant is arithmetic and reaches the SEARCH only.
            #
            # OPEN, AND NOT SETTLED HERE: `under_floor` retracts on `base` growing, not on
            # `units_now` -- `base` climbs with the slot's history every cycle while units
            # sit at the atom floor. Under this line it is never retracted. That is the
            # baseline's behaviour preserved exactly, which is the point; whether it is the
            # RIGHT condition is a separate question and a separate change.
            return (rec.get("verdict") not in ("depth_exhausted", "under_floor")
                    or units_now > rec.get("units_then", 0))

        eligible = [t for t in targets if stale(t[3]) and t[2]]
        if not eligible:
            # NAME WHICH CONDITION REFUSED, not merely that one did. §18.1's discipline is
            # *charge every attempt to a string literal written at the branch that resolved
            # it*, so a finer literal is INSIDE that rule rather than an extension of it.
            #
            # AND THE READING IS NOT THE RUNG'S TO GIVE. `THE_FORMULA`: one reading, three
            # causes, and one of them is *a seat's office*. `none-stale` is a refusal whose
            # condition legitimately holds -- the loop working -- and `no-targets` is nothing
            # supplying the condition. Same flag, opposite diagnoses, and the layer above
            # decides which. It could not, while both arrived as one bucket.
            n_stale = sum(1 for t in targets if stale(t[3]))
            n_hist = sum(1 for t in targets if t[2])
            if not targets:
                why = "no-eligible-target:no-targets"
            elif not n_stale:
                why = "no-eligible-target:none-stale"
            elif not n_hist:
                why = "no-eligible-target:no-history"
            else:
                why = "no-eligible-target:none-eligible"
            self.chain.reuse_branch[why] += 1
            return
        for tkey, slot, hist, rec, slots in eligible:
            how = "direct"
            base = self._left(self.gamma.library[self.bound.get(slot, IDN)], slot, hist)
            best = None
            for bind in [None] + [s for s in slots if s != slot]:
                cand = Term(term.atoms, operand=bind)
                left = self._left(cand, slot, hist)
                if best is None or left < best[0]:
                    best = (left, cand)
            left, cand = best
            if left > 0.0 and units_now > rec.get("units_then", units_now):
                self.chain.reuse_branch["rescan"] += 1
                found = self._reach(slot, hist, slots)
                if found is not None and found[0] < left:
                    left, cand, how = found[0], found[1], "chunk"
            cross = tkey != slot
            # F32 RULED (all-or-nothing is WRONG): the residual never fully closes, so
            # `left == 0.0` discarded 42 strict improvements AND admitted 19/21 full-closures
            # that do not pay. THE FIX IS THE ONE BARGAIN (14.4), not a second gate: accept when
            # the candidate PAYS -- `cost + left < base` -- read off the trace (cost/left/base),
            # never a constant. The provenance rides in the residual stamp (`:partial`/`:closed`)
            # so the ablation separates a bargain-accepted partial from a full closure.
            cost = term_bits(self.gamma.length(cand, tuple(self.gamma.units())),
                             self.gamma.alphabet)
            if pays(cost, left, base):
                self.explain(slot, base - left)
                # THE SWEEP IS A PULL AND EMITTED NO PULL ROW. `reused()` counts `pull` rows
                # and this is the only path that RE-BINDS, so every reuse it found was
                # invisible to the bench-pull and transfer columns both.
                self.led.record(self.cycle, "ROUTE", slot, "pull", term=cand.name,
                                held=tkey, chain=" . ".join(a.name for a in cand.atoms),
                                rebound=True, via="sweep",
                                origin=(self.gamma.stamps.get(tkey) or {}).get("origin"),
                                reads="a library entry reached for BY THE SWEEP")
                self.chain.note_reuse_attempt(f"{'partial' if left > 0.0 else 'closed'}:{how}")
                self.chain.note_reused()
                self.chain.note_cleared()
                name = (cand.name if cand.name in self.gamma.library
                        else self._install_reuse(cand, slot, partial=left > 0.0))
                # 3d: COUNT REUSE WHERE THE FUNNEL ALREADY DETECTS IT. The bind sites are
                # once-per-term by construction -- a rebind picks a DIFFERENT term, since
                # `_library_fit` excludes the incumbent -- so counting there reads 1 forever.
                # And the `cross` case never touches `bound` at all, which is precisely the
                # reuse §17.7 means.
                self.rank.note(name, self.cycle)
                if cross:
                    self.parked.pop(tkey, None)
                else:
                    self.bound[slot] = name
                    self.owed_import.discard(slot)
                    self.abstained.pop(slot, None)
                out = {"term": name, "slot": slot, "cycle": self.cycle,
                       "was": rec.get("verdict"), "via": how,
                       "cross_level": cross, "parked_on": rec.get("level")}
                self.retro.append(out)
                # SHADOW AND ECHO, and the sweep was throwing the verdict away. The
                # target's residual is on the record before this term was accepted --
                # `hist` is evidence already paid for -- and the term closes it on a slot
                # it was not minted for. That is the pair, and it queues for step 6.
                if slot != origin_slot or cross:
                    self._promotions.append((name, {
                        "target": tkey, "parked_on": rec.get("level"),
                        "observations": len(hist),
                        "recorded_before": self.gamma.stamps[name]["seq"],
                    }, {"closed": True, "slot": slot, "minted_for": origin_slot,
                        "cross_level": cross, "via": how}))
                # charged to the ORIGIN's chain, not the target's: the sweep is not the
                # target slot's per-step loop running a second time, it is part of what
                # happened when the origin minted. The target is named, not impersonated.
                self.led.record(self.cycle, "ACCEPT", origin_slot, "retro", term=name,
                                verdict="retroactive resolution", target=tkey,
                                guards={"support": True, "reachability": True,
                                        "novelty": False},
                                note="minted here; it explains a residual parked elsewhere",
                                was=out["was"], via=how, cross_level=cross)
            else:
                # THE TWO REJECT ARMS WROTE NO ROW, AND THAT IS WHY THE ACCEPTANCE RULING
                # CANNOT BE TAKEN YET. `F40` filed it as owed: `note_reuse_attempt` bumps a
                # counter and emits nothing, so the 42 `did-not-pay` candidates' `cost`,
                # `left` and `base` are NOT ON DISK. The ruling on this gate -- *the residual
                # never fully closes, so `left == 0.0` is wrong* -- needs to know which
                # direction the one bargain actually moves the funnel, and **`would_pay` is
                # measured only on the ACCEPT arm**, where it reads False 19 times in 21.
                #
                # SO THE COUNTERFACTUAL IS COMPUTED ON THE SIDE THAT IS ALREADY IN, AND NOT
                # ON THE SIDE THAT IS OUT. Reading one arm and ruling on both is the shape
                # this window keeps logging -- a check that covers half the ground. Same
                # fields as `_install_reuse` computes, so the two arms read alike and a
                # future census can pool them without re-deriving anything.
                # F32: the label is now ACCURATE -- the gate IS `pays`, so did-not-pay means the
                # candidate improved (`left < base`) but cost made the bargain refuse it
                # (`cost + left >= base`), and no-split means it reached nothing. The A6i misnomer
                # (did-not-pay when pays was never consulted) is gone with the zero-remainder gate.
                why = "did-not-pay" if left < base else "no-split"
                self.chain.note_reuse_attempt(why)
                # **THE STEP WAS WRONG AND A NEW SLOT EXPOSED IT -- 2026-09-24.** This row said
                # `ROUTE` and is written from the MINT sweep, AFTER `park` has already run. For
                # every slot but the first in sorted order the interleaving happened to come out
                # ordered, so the gate stayed green; `@goal.completed` sorts before every object
                # slot and the mismatch surfaced immediately as `ROUTE after MINT`.
                #
                # It is a MINT fact by its own content -- *the ONE bargain refused this
                # candidate* is the bargain speaking, not the router binning a slot. **Relabelled
                # rather than the slot renamed**: a name chosen to keep a checker quiet is the
                # defect wearing a disguise.
                self.led.record(self.cycle, "MINT", slot, "reuse_refused",
                                reason=why, term=cand.name, held=tkey,
                                term_bits=round(cost, 4), left_bits=round(left, 4),
                                base_bits=round(base, 4),
                                would_pay=pays(cost, left, base), via=how, cross_level=cross,
                                reads="the ONE bargain refused this candidate: cost+left >= base")

    def _install_reuse(self, cand: Term, slot: str, partial: bool = False) -> str:
        """The SWEEP's entry into Gamma. **F32 RULED: it now consults THE ONE BARGAIN.**

        **ONE GATE ON ONE LIBRARY (was two).** `mint` requires `cost + left < base`, and the
        caller now gates this path on the same `pays()` rather than on `left == 0.0`. §14.4 said
        *one bargain*; this was the site where there were two, and the second is gone. A term that
        closes a residual completely but is longer than the residual is worth no longer enters
        (19/21 such installs read `would_pay=False`); a strict improvement that pays but leaves a
        remainder now does (42 were discarded under the old gate).

        **PROVENANCE (F32 constraint 3).** `partial` records whether the bargain accepted a
        remainder-leaving term (`left > 0`) or a full closure, and it rides into the stamp so the
        ablation separates a bargain-accepted partial from a full closure.
        """
        hist = self.history(slot)
        held = self.gamma.library.get(self.bound.get(slot, IDN))
        base = self._left(held, slot, hist) if held is not None else None
        # THE REUSE PATH PRICED A REUSE AT DERIVATION COST, which is the one place the
        # asymmetry was load-bearing: 19 of 21 installs read `would_pay=False` against a
        # cost that charged for work the ground had already bought.
        cost = term_bits(self.gamma.length(cand, tuple(self.gamma.units())),
                         self.gamma.alphabet)
        left = self._left(cand, slot, hist)
        # `ROUTE`, NOT `ACCEPT`, AND THE GATE SAID SO. The sweep runs inside the ROUTE phase
        # and its own `pull` row is a ROUTE row, so an `ACCEPT` here puts a later ROUTE for the
        # same slot out of order -- `chase: ROUTE after ACCEPT`, refused at seq 39. **The step
        # is a fact about WHEN the row is written, not about what the event feels like.**
        self.led.record(self.cycle, "ROUTE", slot, "reuse_install", term=cand.name,
                        cost=round(cost, 4), left=round(left, 4),
                        base=None if base is None else round(base, 4),
                        would_pay=None if base is None else pays(cost, left, base),
                        partial=partial,
                        note="F32: entered on the ONE bargain (cost+left<base); "
                             + ("partial -- a remainder remains" if partial else "full closure"))
        stamp = "partial" if partial else "closed"
        self.gamma.accept(cand, seq=len(self.led), residual=f"reuse:{slot}@{self.cycle}:{stamp}")
        return cand.name

    def settle(self, res: dict[str, SlotResidual]) -> None:
        """The ground settles it, by held-out payment: a term predicts a transition it was
        never fitted to. And it un-settles the same way -- a settled term that mispredicts
        on fresh evidence is DEMOTED, defeasibly, never deleted."""
        for slot, r in res.items():
            name = self.bound.get(slot)
            if not name:
                continue
            if r.mass > 0.0:
                # express-before-judge: this term actually predicted, and was wrong
                # AND THE FIFTH BIN IS POPULATED HERE AND NOWHERE ELSE, which is the whole of
                # what makes it expressed-and-failed rather than not-retrieved. Recorded for
                # BOTH outcomes of `refute` below: a settled term demoted and a candidate
                # mispredicting are both the ground refusing what was said.
                self._refuted_slot[slot] = name
                if self.gamma.refute(name):
                    self.demoted.append(name)
                    # BOOK 1: a term that had SETTLED and then mispredicted. The ground gave it
                    # a standing and took it back, which is the only honest reading of
                    # *did promotion hold*.
                    if name in self._settled_at:
                        self.gamma.book["promoted_then_wrong"] = (
                            self.gamma.book.get("promoted_then_wrong", 0) + 1)
                    # BOOK 2's SUBJECT: kept so the counterfactual can be read next cycle.
                    # Capped -- a book that grows without bound is a leak, not a record.
                    if len(self._demoted_watch) < 64:
                        self._demoted_watch[name] = (slot, self.cycle)
                    self.led.record(self.cycle, "SETTLE", slot, "demote", term=name,
                                    status="candidate",
                                    asked=[name, slot], ground_said=False,
                                    verdict="mispredicted on fresh evidence",
                                    rejections=round(self.gamma.rejection_of(name), 3),
                                    note="defeasible: the rejection decays and it may settle again")
                    # YOU CAN PROPOSE ON A CANDIDATE; YOU CANNOT STAND ON ONE. Only
                    # on a REFUTATION -- the ground reversing a settlement it had made.
                    # A candidate that mispredicts has not been refused; it has not yet
                    # proven itself, and unbinding there would stop any term ever
                    # accumulating the evidence it needs to settle.
                    self.bound.pop(slot, None)
                    self.owed_import.add(slot)
                continue
            born = self.candidates.get(name)
            if born is None or born >= self.cycle or self.gamma.is_settled(name):
                continue
            self.gamma.settle(name)
            self.settled.add(name)
            self._settled_at[name] = self.cycle
            # **AT WHAT DEPTH DO THIS AGENT'S TERMS ACTUALLY ARRIVE?** `F341` left `max_depth`
            # as the one row it could not assign -- genuinely a COMPUTE BOUND and a BELIEF
            # about where answers live. The corpus splits it: `PHILOSOPHY` makes search depth
            # `d` cost `λᵈ` with λ the MEASURED spectral radius, so **the cost is substrate and
            # the depth is a judgement.**
            #
            # **A RECORD, NOT A DIAL. Nothing reads this to set anything.** It is the evidence
            # a later dial would need, and it is already in the units a depth is measured in --
            # the same property that let the halflife read its observation directly rather than
            # through a function we chose. If every arrival is depth 1, depth 3 is spend with
            # no return; if arrivals crowd the ceiling, the ceiling is what is cutting them off.
            _d = len(term) if (term := self.gamma.library.get(name)) is not None else 0
            if _d:
                _book_add(self.gamma.book, f"arrived_at_depth_{min(_d, 9)}")
                # **DID INVENTION EVER PAY?** Isaiah names INVENT as the agent's own call, and
                # the reviewer noted we built the path and never made WHEN a decision. Reading
                # the site: `_invent`'s only guard is *nothing observed to invent from*, which
                # is a CAPABILITY check -- **given a delta it invents unconditionally, so no
                # discretion exists for anyone to exercise.**
                #
                # **THIS IS THE EVIDENCE A DECISION WOULD NEED, NOT THE DECISION.** An invented
                # atom that never reaches a settled term cost actions and bought nothing; one
                # that does is the only proof invention pays at all. `F307` recorded that
                # invention could not transfer; nothing recorded whether it ARRIVES.
                if any(a.name in self.gamma.invented for a in term.atoms):
                    self.gamma.book["arrived_using_an_invented_atom"] = (
                        self.gamma.book.get("arrived_using_an_invented_atom", 0) + 1)
            # WHAT WAS ASKED AND WHAT CAME BACK. The question is `does this term
            # predict a transition it was never fitted to`, and `r.mass == 0.0` on a
            # cycle later than the one it was minted on IS the answer. Both facts were
            # here; neither was on the row, so a frame that never asked and one the
            # ground paid arrived looking the same.
            self.led.record(self.cycle, "SETTLE", slot, "settle", term=name,
                            status="accepted",
                            asked=[name, slot], ground_said=True,
                            verdict="held on a transition it was not fitted to",
                            held_out_cycle=self.cycle, fitted_through=born)

    # -- the utterance: the only way an action is proposed --------------------------------

    def _utter(self, action: str, before: dict[str, int], focal: str) -> tuple[str, list]:
        see = [G.compose(G.SEE, G.Leaf(G.T.OBJECT, s), G.Leaf(G.T.REGION, s),
                         G.Leaf(G.T.ATTR, before[s])) for s in self.slots if s in before]
        # OVER THE SLOTS THAT HAVE A VALUE, WHICH IS `perceive`'s OWN IDIOM: *the slot
        # set can move WITHIN a step, so the bet is over `before`.* A COVERED object is
        # in `self.slots` (it exists) and not in `before` (it cannot be read), and the
        # agent cannot SAY it sees an attribute it never read. Every other consumer of
        # the pair already guards this way -- `_discrepancy`'s `slot not in state`, the
        # group vector's `any(x not in state)`. This was the one site indexing blind.
        per = G.compose(G.PERCEIVE, *see)
        pid = f"p{self.cycle}"

        # THE OBJECTIVE THE ENV NAMED, not a constant. This line used to call
        # objective(), discard the name, and assert ALL(BECOME(slot, 0)) -- which is
        # false wherever the objective is anything else, and speak.py renders the
        # utterance as the agent's account of itself. The frame supplies the shape; the
        # domain supplies the content.
        name, _deg = self.env.objective()
        bound = self.bound.get(focal)

        # M2 ITEM 1 -- THE WIRE. The agent's OWN composed objective fills `WANT` when it has
        # one. `grammar` declares `WANT : OBJ -> PRED`, and `arc_atoms` declares that its
        # `OBJ` IS `grammar.T.OBJ` -- so a minted OBJ-typed term ALREADY IS the thing this
        # node wants. **Producer and consumer were built to the same type and never met**,
        # because this line took `env.objective()`'s single hardcoded string either way.
        #
        # NECESSARY AND NOT SUFFICIENT, and the spec says so at the site. `_utter` runs AFTER
        # `choose()` and can only raise `Ill` to refuse, so the utterance is a VETO -- and it
        # has never fired. **This changes what the agent SAYS it wants and what type-checks,
        # not what it does.** Item 2 is the branch in `choose` that reads it.
        #
        # THE GROUND STAYS THE FALLBACK, AND THAT IS NOT A CONCESSION. Reading THAT the goal
        # is levels-completed is reading THE GROUND, and the ground is the only metric -- an
        # environment reporting its own win condition is not an answer. The fault would be
        # reading WHICH ACTION advances it from anywhere but the agent's own model.
        #
        # AND THE HOLE IS NOT AVAILABLE AS THE FALLBACK, WHICH THE GRAMMAR SAYS AND I READ
        # BEFORE WRITING. `_check_terminal` refuses a holed `WANT` unless the `DERIVE` is a
        # probe -- so holing it whenever nothing is composed would refuse every step that has
        # a `val` term bound, and the loop would stop BECAUSE the agent has a model.
        mine = self.gamma.library.get(bound) if bound else None
        if mine is not None and getattr(mine, "out_type", None) == OBJ_TYPE:
            want_by, said = "composed", mine.name
            want = G.compose(G.WANT, G.Leaf(G.T.OBJ, mine.name, tag="composed"))
        else:
            want_by, said = "ground", name
            want = G.compose(G.WANT, G.compose("ALL", G.compose(
                "BECOME", G.Leaf(G.T.OBJECT, name), G.Leaf(G.T.ATTR, "satisfied"))))
        # WHOSE OBJECTIVE THIS STEP CARRIED, on its own row. The wire is invisible in
        # `repr(bet)` unless a reader knows which shape means which, and *how often the
        # agent's own composition fills the node* is the only thing item 1 can be measured by.
        # AFTER THE PLAN PHASE, NOT AT THE TOP OF THE STEP. `ledger.STEPS` orders
        # `PLAN` BEFORE `PERCEIVE`, and the other top-of-step narrations are no-ops in worlds
        # that publish no read-order or placements -- so emitting here at the top made this the
        # FIRST row of the run and turned the cycle's own `PLAN` into `PLAN after PERCEIVE`.
        # The gate refused it. This is the first point at which a `PERCEIVE` row is already
        # in order.
        self._narrate_vocabulary()
        self._read_books(before)
        # THE DESTRUCTION, ONE ROW PER CYCLE. Absent when nothing popped, so a quiet cycle says
        # nothing rather than saying zero eight times. `_why`'s docstring forbids a row per
        # call and it is right -- this runs per slot per step.
        if self._popped:
            self.led.record(self.cycle, "PERCEIVE", "*", "trend_popped",
                            total=sum(self._popped.values()), **self._popped)
            self._popped = {}
        self.led.record(self.cycle, "PERCEIVE", focal, "want", by=want_by, objective=said)

        refs = [G.ref(pid, "perceive")] + ([G.ref(bound, "term")] if bound else [])
        ground = G.compose(G.GROUND, *refs)

        if bound:
            pred = self._predict(focal, before, action)
            bet = G.compose("BECOME", G.Leaf(G.T.OBJECT, focal), G.Leaf(G.T.ATTR, pred))
            der = G.compose(G.DERIVE, ground, G.ref(bound, "term"), bet)
            pay = G.compose(G.PAY, G.price(float(len(self.trace)), len(self.trace)))
        else:
            der = G.compose(G.DERIVE, ground, G.T.PRED)       # the typed hole: a probe
            pay = G.compose(G.PAY, G.price(None, None, "explicit-null: nothing bound"))

        bet_t = G.compose(G.BET, want, ground, der, pay)
        bid = f"b{self.cycle}"
        act = G.compose(G.ACT, G.compose(G.NEED, G.ref(bid, "bet"),
                                         G.Leaf(G.T.ATTR, action)))
        return bid, [("PERCEIVE", pid, per), ("BET", bid, bet_t), ("ACT", f"a{self.cycle}", act)]

    # -- driving ---------------------------------------------------------------------------

    def step(self, action: str | None = None) -> bool:
        """One turn. Returns False if no action was proposed -- which is a legal outcome."""
        self._touch_cache = None      # a new step is a new frame, so contact and owners go
        self._peer_cache = None
        self._decomp_cache = None
        self._frame_cache = {}
        self._narrate_order()
        self._narrate_cascade()
        self._narrate_matches()
        self._narrate_placements()
        self._advertised()
        self._present()       # before the frame, so slots and frame cannot disagree
        # PER STEP, BECAUSE ONE SLOT TYPE'S RANGE IS NOT CONSTANT. A shape slot's alphabet is
        # `2**(h*w)` over its own bounding box, which moves when the object resizes -- and a
        # resize changes slot VALUES, not the slot SET, so the three existing refresh sites
        # never fire. The declaration is still the domain's; only when it is read has moved.
        self.alphabet = self._alphabets(self.env)
        before = self.env.observe()
        # ONE READING PER GOAL HYPOTHESIS, EVERY STEP, BEFORE ANYTHING ACTS ON IT. A trend
        # needs a series, and a series only exists if the reading is unconditional -- taking
        # it inside the branch that consumes it would record only the steps that already
        # pursued something.
        self.note_goals(before)
        if not self.slots:
            # NO SLOTS IS A STATE OF THE WORLD, NOT AN IMPOSSIBILITY. `max()` on an empty
            # sequence made a legal state fatal: `ls20` reaches GAME_OVER at cycle 130,
            # `board()` returns None, and the loop died on the frame that told it so.
            #
            # AND IT REPORTS RATHER THAN ADJUDICATES, which is the corpus's own division.
            # `THE_FORMULA`: *R stops arriving because the prediction is perfect* and *R
            # stops arriving because the channel closed* look alike from inside, and
            # **detecting the second is not something the loop can do -- that job belongs
            # to a position outside the loop.** So this records the reading and names
            # nothing: whether an empty slot set is a terminal frame, a closed channel or
            # a perception failure is a seat's office. `PHILOSOPHY` Q3 gives the positive
            # form -- *what the agent can do instead is report its own epistemic state
            # soundly*, which is achievable where knowing the truth is not.
            #
            # `False` is the existing contract for *no action was proposed*, so a step that
            # cannot happen returns what a step that proposed nothing returns, and the
            # monotone surprise integral is untouched -- a turn with no reading must not
            # look like a turn that went well.
            # AND `blind` IS THE ONE THING THE LOOP MAY SAY HERE, BECAUSE IT IS NOT A CAUSE.
            # `arc_world._decomposed` already computes it -- the `components` sensor returned
            # NOT_RESOLVED -- and its own comment warns that `{}` from an unreadable board
            # asserts *this board has no slots*. That is the read/empty confusion one layer
            # down, and it was costing whole runs: `long_vc33` spends its last 9 of 60 cycles
            # here and `sp80_wall` its last 9 of 40, indistinguishable in the ledger from a
            # board that lost its objects. `None` where the world does not compute it -- a
            # world that cannot say must not report `False`, which would claim a clean read.
            self.led.record(self.cycle, "PERCEIVE", "@loop", "no_slots",
                            slots=0, cause=CHANNEL_CLOSED,
                            blind=getattr(self.env, "blind", None),
                            reads="the slot set is empty; what that MEANS is not read here")
            # NO ACTION WAS TAKEN, SO NOTHING PRECEDED THE NEXT FRAME. `_advertised` runs at
            # the top of every step and feeds `Preconditions` with `_last_action`; leaving it
            # set meant a DEAD cycle credited the last live action again. Measured: `taken`
            # summed to 998 over 1000 cycles while `by` -- which counts only steps that
            # acted -- summed to 131, and `ACTION1: 881` was one action held for 850 cycles
            # after GAME_OVER rather than taken 881 times. The denominator built to stop a
            # count reading as a rule was itself miscounting.
            self._last_action = None
            self.cycle += 1
            return False
        # THE SAME OUTCOME ONE FIELD OVER, and it is the fix for a CRASH rather than a
        # silence. `drive.choose` indexes `sorted(actions)[... % len(actions)]` and divides
        # by zero on an empty tuple, so six of twenty-five public games died at cycle 0 --
        # every game that advertises exactly one action and surfaces none. `tether`'s own
        # first line already names the legal outcome: *an action is proposed ... OR THERE IS
        # NO ACTION*, and the loop never reached it because it died one layer down.
        if not self.actions:
            self.led.record(self.cycle, "ROUTE", "@loop", "no_action",
                            actions=0, cause=CHANNEL_CLOSED,
                            reads="the environment surfaced no action; what that MEANS is "
                                  "not read here")
            self._last_action = None
            self.cycle += 1
            return False
        # ATTEND TO WHAT OWES MOST. R+_s is defined and already measured; picking
        # slots[0] made the phase histogram a function of alphabetical order, so
        # renaming a slot moved an instrument. Ties break on owing, then on name, which
        # only decides the first step -- before any mass exists.
        # OVER THE READABLE SLOTS. `self.slots` now carries COVERED objects -- they exist,
        # so their slots stay in the set and their bindings survive (ruling (b)) -- but
        # `_utter` predicts on the focal slot and `_value_of` indexes `state[slot]`, so an
        # unreadable focal is a KeyError. You cannot attend to what you cannot read this
        # frame; the binding is untouched and it is eligible again the moment it uncovers.
        readable = sorted(s for s in self.slots if s in before) or sorted(self.slots)
        focal = max(readable,
                    key=lambda s: (self._last_mass.get(s, 0.0), s in self.owed_import))
        # **SYSTEM 2 SETS WHAT TO ATTEND TO; SYSTEM 1 EXECUTES -- Isaiah, 2026-09-25, and it is
        # the crane game's own division of labour.** *"Tries 3-4: SYSTEM 2 drives -- deliberate
        # measurement, not exploration. 1 still does the steering. 2 SETS WHAT TO ATTEND TO; 1
        # EXECUTES."*
        #
        # The line above is System 1's attention: WHAT OWES MOST, driven by surprise. §13.4's
        # selector is System 2's: the want whose discrepancy is most confidently shrinking. When
        # System 2 has a view, it sets the focus. **When it does not, `_goal_choice` returns None
        # and this is a no-op** -- so the fallback is System 1 exactly as before, and nothing is
        # deleted: `focal` is what is ATTENDED TO, never what is believed.
        #
        # **AND IT IS GATED ON READABILITY FOR THE REASON ABOVE, NOT AS A COURTESY.** `_utter`
        # predicts on the focal slot and `_value_of` indexes `state[slot]`, so an unreadable
        # focal is a KeyError -- a want on a covered object must wait rather than crash.
        # **`_goal_choice`, NOT A SECOND SELECTOR. It is labelled M2 ITEM 3, THE SELECTOR, it
        # quotes §13.4 whole, and its *confidently* is `MIN_REPEAT` consecutive non-increasing
        # readings with a real decrease -- *flat is not shrinking*. I built a weaker duplicate
        # ranking on ONE cycle's delta and wired that here first; a duplicate selector is a
        # reinvention no grep can see, and the laxer criterion was mine rather than the
        # corpus's.**
        _want_slot = self._goal_choice()
        if _want_slot is not None and _want_slot in before:
            focal = _want_slot
            self.gamma.book["focus_by_want"] = self.gamma.book.get("focus_by_want", 0) + 1
        by = "given"
        self._disproof = {}
        if action is None:
            action, by = self.choose(before)
        self._acts[action] += 1   # System-0 instrument: the concrete action distribution
        # THE PHASE IS READ OFF THE SITE THAT CHOSE, never asserted alongside it. It
        # used to be `DIRECTED if a term is bound`, attached to an action drawn by the
        # identical mechanism either way -- a label the mechanism could not make.
        # STRATEGY ARRIVED WITH ROUTINES, WHICH IS WHAT THIS COMMENT PROMISED. It read *0
        # until then: an honest zero, not a gap* -- and once a routine drives an action the
        # zero stops being honest and becomes the gap it distinguished itself from. `by ==
        # "routine"` IS the site that chose, so this is the stated rule applied, not a new one.
        #
        # **AND THE `DIRECTED` DISAGREEMENT IS DELIBERATELY LEFT ALONE.** That one is `A6i` --
        # `by == "discriminate"` reads 9% where §22.2's *bets with bound terms* reads 37% on the
        # same runs -- and it is a dispute about which quantity the word names, with both
        # readings defensible. **A phase that is never emitted at all is a different thing from
        # two defensible definitions**, and only the first is fixed here.
        #
        # THIS MOVES A PUBLISHED METRIC. `phases.report()` is §22.2's transfer instrument and
        # its STRATEGY column has been structurally zero; it will not be on any run where a
        # routine executes. Flagged rather than slipped in.
        # S5: THE FAMILY, NOT THE EXACT STRING. `choose` returns `discriminate`,
        # `discriminate:learned` and `discriminate:goal`, and an `==` admitted only the first
        # -- so a LEARNED split, which §18.4's proposer picks deliberately, was filed under
        # PROBE. Measured across ten boards: `discriminate:learned` fires on six of them, 33
        # of 125 cycles, and `phases.report()` read `directed 0.0` on every one. `draw` stays
        # in PROBE and is not part of this: it and `probe` are byte-identical calls to
        # `drive.choose`, so both really are undirected picks.
        phase = (I.STRATEGY if by == "routine"
                 else I.DIRECTED if by.startswith("discriminate") else I.PROBE)
        self.phases.note(phase)

        try:
            bid, utts = self._utter(action, before, focal)
        except G.Ill as exc:
            self.refusals.append(str(exc))
            self.led.record(self.cycle, "PERCEIVE", focal, "refused", reason=str(exc))
            return False

        for kind, uid, term in utts:
            # all three belong to step 1 -- "bet, act, observe" is one step
            self.led.record(self.cycle, "PERCEIVE", focal, "utterance", kind=kind,
                            id=uid, text=repr(term),
                            heads=[a.head for a in term.args if hasattr(a, "head")])

        self._last_action = action
        # F28: a positioned action needs a position, and the agent chooses it from PERCEPTION --
        # the focal object's own row/col, which are perceived slots. No spatial basis (the focal
        # object has no position slots) means ACTION6 would be noise, so the coordinate is None and
        # the world leaves the action unpositioned rather than emitting a baseless one.
        # SYSTEM 0 AIMS. `focal` is chosen by residual mass, which is the right subject for a
        # BET and the wrong one for going to touch something: contact-seeking has to point at
        # what it has not touched, or it is a draw wearing a label -- which is `F236`.
        # ARM M REACHES HERE TOO. It returns `probe`, not `system0`, so keying the coordinate on
        # `by == "system0"` alone would aim a starved-slot perturbation at `focal` -- the slot
        # with the most residual mass, which is precisely NOT the starved one.
        aim = (self._s0_target if (by in ("system0", "probe") and self._s0_target)
               else focal)
        coord = self._action6_coord(aim, before) if action == "ACTION6" else None
        res = self.perceive(action, coord)
        # WHAT THAT ACTION DID TO THE AVATAR, recorded from the frames either side of it.
        self._note_move(before, action, self.env.observe())
        for slot, b, fit, _why in self.route(res):
            if b == REBIND and fit:
                self.bound[slot] = fit
                self.rank.note(fit, self.cycle)
                self.owed_import.discard(slot)
                self.abstained.pop(slot, None)
                self.led.record(self.cycle, "ACCEPT", slot, "rebind", term=fit,
                                status="candidate", note="refit; the library did not change")
            elif b == REFUTED:
                # a competitor where the library holds one; otherwise the gap is genuinely
                # new and MECHANISM's answer is the right one.
                if fit:
                    self.bound[slot] = fit
                    self.rank.note(fit, self.cycle)
                    self.led.record(self.cycle, "ACCEPT", slot, "compete", term=fit,
                                    status="candidate",
                                    note="the bound term was refused here; this is its competitor")
                else:
                    self.mint(slot)
            elif b == MECHANISM:
                self.mint(slot)
        if by == "probe":
            # ONE ROW PER SLOT THAT ASKED FOR IT, and `@probe` only when the trigger was
            # the global reading rather than any particular slot. It used to be `@probe`
            # always, so a slot parked at no_support could never be matched to the probe
            # that answered it -- which is what B5 reads, and it was failing on it.
            for slot in sorted(self._starved) or ["@probe"]:
                self.led.record(self.cycle, "MINT", slot, "probe",
                                **self.drive.report(),
                                guards={"support": False, "reachability": False,
                                        "novelty": False},
                                note="support at zero; the model does not choose this one")
            self._starved.clear()
        if self.drive.never_live(len(self.actions)) and not self._said_never_live:
            # NAMED, AND THE REMEDY IS NOT BUILT. Every action has been drawn and no slot
            # has ever carried mass, so either the world is static or the slots do not
            # reach what moves -- indistinguishable from here. The second is
            # CHANNEL_CLOSED about the INTERFACE, and its remedy is step 7 INWARD, which
            # does not exist. Recording it beats a silent zero.
            self._said_never_live = True
            self.led.record(self.cycle, "IMPORT", "@instrument", "unreached",
                            observations=self.drive.n, trials=self.drive.trials(),
                            slots=sorted(self.slots),
                            verdict="no SINGLE action, each drawn from at least two "
                                    "distinct states, changed any slot",
                            scope="single actions, from the states occupied -- this "
                                  "does not exclude a SEQUENCE, because the "
                                  "denominator is over actions",
                            remedy="step 7 INWARD: a slot set that reaches what moves",
                            built=False)
        self.settle(res)
        self._promote()
        _, degree = self.env.objective()
        self.clocks.note(not self.owed_import and bool(self.bound),
                         1 if degree >= 1.0 else 0)
        self.cycle += 1
        # §12.4's trigger is a PERCEPTION reading -- the vocabulary failing to resolve two
        # things the world distinguishes -- so it is recorded, not acted on here.
        indist = self.indistinguishable()
        self.led.record(self.cycle - 1, "PERCEIVE", "@vector", "indistinct",
                        pairs=len(indist), top=indist[:3],
                        remedy=self.resolve() if indist else None,
                        reads=("same featural vector, different |R|. Ranked by how many "
                               "objects shared the vector, which the remedy cannot move"))
        self.led.record(self.cycle - 1, "REPEAT", "@loop", "repeat",
                        integral=round(self.pe_integral(), 3),
                        outstanding=round(self.outstanding(), 3),
                        # DID THIS CHOICE CONSULT GAMMA AT ALL -- F225. Set in `choose`;
                        # `{}` where a held routine returned before selection ran.
                        gamma_read=self._gamma_read,
                        # LEVEL ON EVERY REPEAT ROW, because a per-level series cannot be
                        # reconstructed without it. The `ending` row carries `to_level` and
                        # records the BOUNDARY; nothing said which level a given cycle was in,
                        # so the four columns had no way to be segmented.
                        level=self.level,
                        # THE ACTION, BESIDE THE EXIT THAT CHOSE IT. `by` said WHICH BRANCH
                        # picked, and nothing said WHAT WAS PRESSED -- so a reader could see a
                        # prediction miss and not what preceded it, which is half the loop.
                        # It was reachable only as a substring of the `ACT(NEED(...))` utterance,
                        # and parsing a rendering to recover a value the loop already holds is
                        # the reconstruction `transcript.py` exists to refuse.
                        action=action,
                        phase=phase, by=by, stage=self.chain.seg.stage(),
                        gamma_size=len(self.gamma.library), owed=sorted(self.owed_import),
                        # REACH BESIDE THE LIBRARY, because the pair is the reading and one
                        # of them was a RECONSTRUCTION. `F50` replayed `units()` from SETTLE
                        # rows to put the two series side by side -- the count agreed with an
                        # independently derived one at both boards, so the reconstruction was
                        # sound, and it was still a reconstruction of a value the loop holds.
                        # The figure's sentence is *reach is DERIVED and can fall while the
                        # record only grows*, and a reader cannot check that against a number
                        # the ledger does not carry.
                        reach=len(self.gamma.units()),
                        # AND `any_live`, WHICH `F57` FOUND UNREACHABLE WHERE IT MATTERS.
                        # `Drive.report()` carries it and reaches the ledger at ONE site,
                        # inside `if by == "probe"` -- so the state explaining the probe
                        # branch's silence is written only when the branch speaks, and reads
                        # 4 rows in the toy world against 0 on every ARC board. **An
                        # instrument placed where it can only ever confirm.** Here it is on a
                        # row that exists every cycle regardless of which branch ran.
                        any_live=self.drive.live,
                        admissions=self.gamma.admissions())
        return True

    def run(self, cycles: int) -> Report:
        for _ in range(cycles):
            self.step()
        rep = Report(cycles=self.cycle, bound=dict(self.bound),
                     minted=[e.detail["term"] for e in self.led.by_event("mint")],
                     demoted=list(self.demoted),
                     settled=sorted(self.settled), owed_import=set(self.owed_import),
                     abstained=dict(self.abstained), refusals=list(self.refusals))
        self.chain.close("run_end")
        rep.chain = self.chain.report()
        rep.phases = self.phases.report()
        rep.clocks = self.clocks.report()
        rep.retro = list(self.retro)
        rep.stopped_at_link = self._link()
        return rep

    def _link(self) -> str:
        """Figure 3's diagnostic: which link did it stop at, and was that measured?"""
        if not self.trace:
            return "1 - perception (measured: no observations)"
        if not self.gamma.library:
            return "2 - vocabulary (measured: empty library)"
        if not self.settled:
            return "5 - learn and carry (measured: nothing settled against the ground)"
        if self.owed_import:
            return (f"2 - vocabulary (measured: {len(self.owed_import)} "
                "slot(s) unreached at budget)")
        return "3 - the objective (measured: prediction closed, no goal composition built)"
