# RELATIONS.md (cited below) are docs/library-closure/ files DELETED 2026-10-11 (Section A);
# git holds them at the parent of the deleting commit (DOCS_CONSOLIDATION.md section A).
# RELATIONS.md's live successor: library/relations.json + LIBRARY_SPEC section 3.
"""The loop. Steps 1 to 5.

One track: an action is proposed by an utterance that type-checks and passes the gate, or
there is no action. There is no fast path, because a fast path is what makes the framework
optional.
"""

from __future__ import annotations

import collections
import hashlib
import heapq
import itertools
import json
import math
import os
import re
import sys
import time
from collections import Counter
from contextlib import contextmanager
from dataclasses import dataclass, field
from dataclasses import replace as _replace
from functools import cache, partial, wraps
from typing import Any

import armflag
import compile_term
import composer
import condition
import frontier as FR
import grammar as G
import inherited
import instruments as I
import interface as IFace
import lineage
import reach
import relations
import retrieval
import routine as Rt
from gamma import _SETTLED_CORE as G_SETTLED_CORE
from gamma import (
    ACTED_ON,
    ACTED_SELF,
    IMPORTED,
    INVENTED_GUARD,
    MINTED,
    REJECTION_HALFLIFE,
    Ctx,
    Gamma,
    Standing,
    Term,
    accepts_type,
    shared_token,
)
from gamma import SAME_AS_TARGET as G_SAME
from ledger import (
    ADVANCE,
    CHANNEL_CLOSED,
    ENDING_READS,
    GENUINE,
    NO_CHANGE,
    SLICE_TOO_SMALL,
    SPECIFIED,
    WIN,
    Ledger,
)
from priors import contact_first
from probe import Drive
from self_family import MIN_REPEAT
from sensors import COMMENSURABLE, DELTA, NOT_RESOLVED, OBJECT, POSITION

sys.dont_write_bytecode = True

IDN = "idn"
NO_INTENT = "no intent"
"""**AN EXPLICIT READING, NEVER AN EMPTY -- the reviewer, 2026-09-29.**

A trace row now carries the intent the agent formed. Two kinds of row carry none: an
action HANDED IN to `step()` rather than asked for, and a bare draw. **Both are real
states and neither is a missing value.**

**THE REASON IS A TRAP HE SAW COMING AND I HIT ONE LEVEL LATER:** a guard keyed on intent
must compare against something, and an EMPTY forces a choice between *treat unknown as
satisfied* -- the guard becomes invisible to pricing -- and *treat unknown as failing* --
guards die on contact. **An explicit reading forces neither: it is a value, so it can be
compared and found different.**
"""
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
_TYPED_BIND = armflag.arm("TETHER_TYPED_BIND")
# F130 arm C: supply `_library_fit`'s retrieval the relation channel its two
# sibling call sites already pass. Seat-side, off by default.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_REL_GAP = armflag.arm("TETHER_REL_GAP", default=True)
# F32 arm D: decide reuse by the ONE BARGAIN rather than by a zero remainder, which Isaiah
# ruled out. **ON BY DEFAULT SINCE 2026-09-30 -- the flip LANDED, and the four M2 failures
# that held it were diagnosed first, as the reviewer required.**
#
# WHAT THEY TURNED OUT TO BE, because the sequencing bought exactly this. The suite was at
# 30/30 on the default arm and 26/30 with the flag, and the four were NOT a capability the
# flip removed:
#   `trigger_is_the_residual_not_the_reward` -- VACUOUS. Its treatment (satisfying the reward
#       channel) was byte-identical to its control on both arms; `_mint_routine` reads no
#       reward in 363 lines. Repaired to raise if the trigger reads reward, mutation-tested.
#   `strategy_is_emitted` and the `routine` coverage case -- GREEN ONLY ON A PHANTOM SCOPE.
#       `_wide` appended four members no object carries; of the five failing exactly one was
#       real. Strip them and the routine is refused UPSTREAM on both arms -- OFF because the
#       objective is already satisfied, ON because there is no objective at all. Moved to
#       `conform/owed.py` intact under ruling 6.
#   `accumulation_commits` -- NOT ISOLATED. Its cold case inherited whatever the warm-up left
#       in `wants`, so its verdict turned on recurrence rather than on the price path it
#       names. It now sets that state itself.
#
# So the flip removed nothing. Three of the four were reading something other than what they
# claimed, and the fourth is owed to a world with a real gap.
_BARGAIN_FIT = armflag.arm("TETHER_BARGAIN_FIT", default=True)

# **THE ?ACTED GUARD, DEFAULT ON SINCE 2026-10-05 -- ISAIAH, on the settled/unsettled
# principle, SUPERSEDING the earlier zero-failure bar.** It was OFF from 2026-10-02, the
# reviewer honouring a refuter that fired: the guard is semantically correct (it reads what
# the press LANDED ON, 60/60 against the world) and it FAILED its pre-registered test --
# payments up and TOTAL refusals down on 6 of 6 world-seeds, the refusal rate collapsing
# 19.67% -> 0.40% on three.
#
# **THE LICENCE THIS COMMENT USED TO NAME WAS: guarded adoptions must SETTLE no worse than
# unguarded, and an unsettled term must never be acted on as trusted. STATE OF THAT TEST AT
# THE FLIP, RECORDED HERE BECAUSE IT IS WEAKER THAN A READER WOULD ASSUME:**
#
#     every one of SIX world-seeds reads INSUFFICIENT -- denominators below the threshold
#     borrowed from `probe.never_live` (>= 2, "the smallest number with the property, not
#     tuned"). ONLY THE POOLED FALLBACK PASSES: guarded 3/7 = 42.9% vs unguarded 0/2.
#
# **SO THE FLIP RESTS ON ISAIAH'S RULING, NOT ON THE PER-SEED TEST, AND THOSE ARE DIFFERENT
# WARRANTS.** He outranks the seat's own construction and the ruling is recorded in
# `docs/ISAIAH_RULINGS.md` -- but *per world, per seed, never pooled* is this project's
# hardest-won law, and a pooled 3/7-against-0/2 is exactly the shape it exists to distrust.
# **Nobody should later cite "the condition was met" as though it was met per seed.**
#
# WHAT IS STRUCTURALLY TRUE AND NOT A COUNT: no unsettled guarded term can act as trusted --
# `units()` iterates `settled_terms`, a `@property` computed live from `is_settled`.
_ACTED_GUARD = armflag.arm("TETHER_ACTED_GUARD", default=True)

# **THE AIMED CURIOSITY DRAW, DEFAULT ON -- the reviewer, 2026-10-01.** The flag exists so the
# before/after is ONE SCRIPT WITH ONE FLAG rather than two code states: OFF restores the
# subjectless `_explore` the curiosity exit used before `F401`. The `bored()` exit is not
# behind this and never becomes aimed -- its uninformed draw is a safety property, not an arm.
_AIMED_CURIOSITY = armflag.arm("TETHER_AIMED_CURIOSITY", default=True)

# ARM F -- RECIPE DEDUP. The novelty check below tests `term.name`, which carries operand AND
# guard, so `translate . recolour<o5.w>` and `<o12.w>` both read NOVEL and both get minted.
# Measured: 94% of mints re-derive a chain already held, and `translate . recolour` was minted
# 137 times in one run (F229). Isaiah: "adding a dup is a symptom of the found thing never being
# searched for -- a deeper usage-of-terms problem." This arm makes the check see the RECIPE.
# WAS DEFAULT OFF, like every other arm, so the baseline it is measured against is preserved.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_RECIPE_DEDUP = armflag.arm("TETHER_RECIPE_DEDUP", default=True)

# ARM G -- REBIND WHAT IS HELD. `_rebindings` returns early for any term that already carries an
# operand, so only IMPORTS (which arrive unbound, `save` drops it) are ever re-bound. A term the
# agent minted THIS RUN is offered to a new slot still pointing at the old one, `_explains` tests
# behaviour, and it cannot explain -- so mint re-derives it. CENSUSED at the reviewer's request:
# of the terms installed by mint, 100% (dc22) and 94% (ls20) were chains ALREADY IN THE LIBRARY,
# and 85% / 41% of those were held with an operand locked to a DIFFERENT slot.
# The principle is the method's own docstring: *composition crosses, binding does not* -- true of
# every term, applied to loaded ones only. WAS DEFAULT OFF like every other arm.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_REBIND_HELD = armflag.arm("TETHER_REBIND_HELD", default=True)

# ARM H -- THE GUARD AXIS IN RETRIEVAL. Reviewer ruling 2026-09-21, and it is the generation half
# of F238. `mint` walks (operand x GUARD) via `_guards(robs)`; `_rebindings` varies only the
# operand and inherits the held guard, so 31-42% of what mint installs is a Term retrieval can
# never produce -- no admission rule can accept a candidate that was never offered (F239: cost,
# left and base are identical in both paths, so generation is the whole of the gap).
# BOUNDED AS MINT IS: guards come from `_guards(robs)` -- None first, then ONLY the actions
# appearing in that residual's own observations -- never the full action set on every lookup.
# The playbook's lookup fires on a SETTLED CHANGE and that event carries the action that produced
# it, so handing retrieval the observation is giving it the event it was specified to key on.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_GUARD_AXIS = armflag.arm("TETHER_GUARD_AXIS", default=True)

# ARM I -- DECODE THE SHAPE STAND-IN. `arc_percept` computes the normalised offset frozenset every
# frame and publishes an episode-local INT in its place; every SHAPE atom guards on a frozenset, so
# seven of the 48 read NOT_RESOLVED on every call -- measured 0 of 40 (F242). `arc_world.shapes()`
# is the inverse map, built for exactly this, with zero callers. This hands it to the atoms through
# `Ctx` and changes NOTHING about what is published: the slot value, the alphabet and the bargain's
# inputs are untouched. RELATIONS.md calls it "a build and not a decision to revisit ... no new
# sensor, no entry rule, no exemption". WAS DEFAULT OFF, because it makes seven dead atoms live and
# that moves the closure.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_SHAPE_DECODE = armflag.arm("TETHER_SHAPE_DECODE", default=True)
# The incremental tally in `_cannot_pay`. ON by default, OFF for the identity A/B --
# ONE script with one flag, never two scripts.
_TALLY = not armflag.arm("TETHER_NO_TALLY")

# CARRY THE CANDIDACY. Reviewer 2026-09-30, on Isaiah's reuse-without-re-deriving ruling:
# *a carried term becomes a candidate the first time the agent binds or tests it in this game,
# then settles through the same ground check as any local term.* `candidates` had ONE writer
# (mint), so `settle()`'s `born is None` guard could never clear for an IMPORTED term and a
# carried schema could not leave the unsettled state on any board. INVERTED POLARITY like
# `_TALLY`: the fix is ON and the env var turns it OFF, so the A/B is one script.
_CARRY_CANDIDATE = not armflag.arm("TETHER_NO_CARRY_CANDIDATE")
# WHAT A SEARCH HAS ALREADY PRICED -- reviewer 2026-10-07, plan item 7. Under an unchanged scope key
# a chain prices the same way again, so a re-run of a search that stopped at the budget spends the
# budget re-reading what it already refused. The cue reorders ties every cycle, so the frontier is
# the SET of chains priced, never a position. ON by default; the env var turns it OFF.
_RESUME = not armflag.arm("TETHER_NO_RESUME")


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
# **EVERY EXIT `choose` CAN RETURN, AND ITS PHASE -- ENUMERATED, NOT MATCHED.** Three repairs
# at one line in one day: `== "discriminate"` admitted 1 of 3 labels; a PREFIX broke on the
# first rename; an EXCLUSION (`not in (probe, draw)`) flipped `system0` on the first label that
# was neither. **A guess about which side is the short list is still a guess.** This is short
# because `choose` HAS few exits, and a label missing from it is reported rather than defaulted.
#
# `system0` IS PROBE and its own site is the authority -- it *draws variously INSTEAD of
# exploiting the learned arm*. An undirected pick made deliberately is still an undirected pick:
# the deliberateness is in choosing to explore, not in choosing the button.
PHASE_OF: dict[str, str] = {
    "routine": I.STRATEGY,
    "discriminate:goal": I.DIRECTED,
    "distinguish": I.DIRECTED,
    "system0": I.PROBE,
    "probe": I.PROBE,
    "draw": I.PROBE,
    "given": I.PROBE,          # handed in by the caller: not a choice this loop made
}

ORDERED_TYPES = ("POSITION", "EXTENT", "DELTA")

# anchor: how many reachable terms an experiment weighs before choosing. Bounded because
# the choice is made every step and the closure grows; 200 covers depth 2 over the toy
# alphabet exactly, and truncation only ever narrows the spread, never invents one.

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

# ARM J -- DEFAULT ON since F497 (the reviewer 2026-10-07: a figure-mandated organ, Fig 5's
# amendment; off on the shipped path it was the "switch never set" genus). The bin is a RULING;
# the DIVERSION it causes is a policy change to the acting path, measured in F497. RE-READ
# 2026-10-07 at 2a43566: with it live, `shipped` (B5) PASSES and ONE M2 check failed -- on its
# fixture guard, because F485's frontier let the warmed mints replay rather than re-price -- not
# because of the bin or an amended figure; the fixture now prices fresh. (The earlier reading
# here -- B5 and three M2 checks failing -- predated F485 and is superseded.) *Reintroduce the
# defect, never disable the check.*
_REFUTED_BIN = not armflag.arm("TETHER_NO_REFUTED_BIN")

# THE PRICE OF NOT-t IS OPEN IN THE FIGURES (Fig 12/13: an atom slot, nothing, or the choice of what
# to negate). DEFAULT, the reviewer 2026-10-07: the bits to NAME which term is wrong among every
# term bound and predicting, agent-wide (Fig 5's enumeration; Fig 12 prices every part as a named
# choice). This arm prices it as one atom slot instead, so the choice can be read off the evidence.
_NOT_ATOM = armflag.arm("TETHER_NOT_ATOM")

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
_DELTA_OPERANDS = armflag.arm("TETHER_DELTA_OPERANDS")
# ITEM 6, THE RE-KEY. Was default OFF. `F303` measured the key BEFORE this was built: a GLOBAL frame
# delta is saturated at every granularity that crosses boards -- types 100% of cycles, attribute
# names 91% -- because *did ANY slot of this type move ANYWHERE* is always yes across 1,688
# slots. Scoped to the target's OWN OBJECT it is ~3%, median 0%, with nine objects in ten
# changing nothing. The reviewer's ordering requires this narrowing BEFORE mint's `out_type` is
# widened: widening without narrowing is how 735 million calls arrive nowhere.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_DELTA_KEY = armflag.arm("TETHER_DELTA_KEY", default=True)
# THE LOOK-UP'S PARTNER ORDERING. Direction ON (the reviewer 2026-10-08 00:54Z); `0` is the A/B
# control. Orders the operand candidates, never excludes one.
_LOOKUP_ORDER = armflag.arm("TETHER_LOOKUP_ORDER", default=True)
# AN OPERAND NAMED `slot~1` IS THAT SLOT ONE FRAME EARLIER (the reviewer 2026-10-08 06:25Z, Fig 6:
# the trace already holds it). Never a slot: not bet on, no residual, only bound as an operand.
PREV = "~1"
# THE WINDOW (R3 item 2, Isaiah's H1): `slot~j` is that slot j frames earlier; `~1` is j = 1.
_LAG = re.compile(r"^(.*)~(\d+)$")


def lag_of(name: str | None) -> tuple[str, int] | None:
    """(slot, j) for an operand reading j frames back, else None."""
    if not name or "~" not in name:
        return None
    m = _LAG.match(name)
    return (m.group(1), int(m.group(2))) if m and int(m.group(2)) > 0 else None
# THE ~1 OFFER IN `_bindings` (the reviewer 2026-10-09 06:39Z): OFF, reason in conform/arms.py.
_PREV_OFFER = armflag.arm("TETHER_PREV_OFFER")
# M4: the library's offered chains yielded BEFORE the closure stream, priced by the one body
# (the reviewer 2026-10-09 08:30Z). DEFAULT ON by the registered rule (10:02Z, re-measured after
# the operand fix 10:19Z). OFF: the offers are recorded and not read.
_LIBRARY_FIRST = armflag.arm("TETHER_LIBRARY_FIRST", default=True)
# THE SEAL REPAIR (R3 item 1, the reviewer 2026-10-09; Isaiah's H1 and H3(i)). ON (7.5 switch-on,
# the reviewer 2026-10-11 02:19Z); reason in conform/arms.py. Inert unless a term reading an
# earlier frame is bound (TETHER_PREV_OFFER).
_UNSEAL_START = armflag.arm("TETHER_UNSEAL_START", default=True)
# THE HISTORY WINDOW (R3 item 2; Isaiah's H1; the reviewer 18:10Z, 18:15Z). OFF; reason in
# conform/arms.py. Lags `slot~j` offered after every other binding, ranked; the budget bounds them.
_WINDOW = armflag.arm("TETHER_WINDOW")
# B2b's round 3 (the reviewer 2026-10-11 10:57 CDT): derived binds walked last; reason in
# conform/arms.py under TETHER_RELATION_SET.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_RELATION_SET = armflag.arm("TETHER_RELATION_SET", default=True)
# B4: the settled S7 entries (solidity / collide / obstacle) a blocked stall cues in the lookup.
S7_SOLIDITY = ("HUMAN|Solidity", "HUMAN|Collide", "ADHERENCE|Obstacle")
# ITEM 2b (the reviewer 19:45Z): under the window, the search runs in TWO PASSES -- every chain with
# its non-lag bindings and its EVIDENCE lags, then, only with budget left, the same recorded chains
# with their no-evidence lags. False restores item 2's one-pass order, for the tie guard only.
_TWO_PASS = True
# A reuse-installed term is a candidate the ground can grade (P1; the reviewer 23:01Z, 00:37Z).
# False restores the old path, for the must-fail only.
_REUSE_CANDIDATE = True
# A sweep's promotion to primitive waits for the term's first settle in this level (P2; the reviewer
# 23:01Z, 00:37Z: nothing is trusted before it settles). False restores the old path, for the
# must-fail only.
_PROMOTE_AFTER_SETTLE = True
# CARRY CREDIT (R3 item 3; DISCOVERY 503; H3(ii); R-D4; the reviewer 16:31Z, 21:18Z). OFF; reason in
# conform/arms.py. A minted term's cost is paid once: reused where it RE-GROUNDS (left < base on the
# slot's own record) it is priced on its leftover, and the library fit takes the lowest whole price.
_CARRY_PRICE = armflag.arm("TETHER_CARRY_PRICE")
# MC1 + MC2 (7a(4); R3; the reviewer 2026-10-10 07:57Z). ON; reason in conform/arms.py. The signal
# is the TRANSITION bet row itself (ledger.signal_sign); ON, each gets exactly one resolution row
# when its level ends (retarget) or the run ends with the level open (end_run). Record only.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_MC_SIGNAL = armflag.arm("TETHER_MC_SIGNAL", default=True)
# 7a(5) A + B, THE RUIN RECORD (ARC_AGENT 19.3-19.4; the reviewer 2026-10-10 10:41Z). ON; reason in
# conform/arms.py. A: every ending reaches `self.term` exactly once. B: a death adds (fingerprint,
# action, realised coordinate) to `self._vetoes`, which only grows (Fig 6). The fingerprint is the
# world's BOARD where it gives one, else observe(), which is the whole state there (Fig 1). Record
# only: nothing reads the vetoes until C, its own arm.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_RUIN_RECORD = armflag.arm("TETHER_RUIN_RECORD", default=True)
# 7a(5) C, RUIN ORDERED FIRST (R3 Part 1; the reviewer 10:41Z, 11:53Z). ON; reason in
# conform/arms.py. A pair the floor vetoes on THIS board is withheld from the one choose() call,
# at the sites below the seam where the button and coordinate are chosen, unless every option is
# vetoed. It reads the floor, so it cannot run without it.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_RUIN = armflag.arm("TETHER_RUIN", default=True)
if _RUIN and not _RUIN_RECORD:
    raise RuntimeError("TETHER_RUIN reads the veto floor: it needs TETHER_RUIN_RECORD on")
# 7a(5b) THE CONTACT INSTRUMENT (Isaiah 2026-10-10 06:46 CDT; the reviewer 11:46Z, 12:27Z). ON;
# reason in conform/arms.py. Record only: `gamma_read["fed"]` names, by seq, each library term read
# by the exit whose action is RETURNED, with its role (goal: it chose what to reach; route: its
# prediction chose the press; body: a routine's step). Nothing decides from it (Fig 1).
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_FED = armflag.arm("TETHER_CONTACT", default=True)
# 7a D5, SPLIT A SLOT'S RESIDUAL ON STRAIN (Fig 9 :4-5, :54-58; the reviewer 2026-10-10 15:58Z).
# ON; reason in conform/arms.py. When a held predicate cleanly separates the rows a bound term
# gets right from the rows it gets wrong (at least 2 each side), the slot gets two PARTS: the
# incumbent guarded by P, and the not-P rows searched on their own. Credit per (term, part); the
# incumbent is shadow-graded on not-P rows and a broken partition reverts the split.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_D5 = armflag.arm("TETHER_D5", default=True)
# F408, EVERY NAMED GUARD PRICED (Fig 12 :99-102; the reviewer 2026-10-10 21:31Z). ON (7.5
# switch-on, the reviewer 2026-10-11 02:19Z); reason in conform/arms.py. An intent guard (and
# "no intent") costs log2(G+1) like ACTED_* does.
_GUARD_PRICE = armflag.arm("TETHER_GUARD_PRICE", default=True)
# 7a(6) H2, THE IN-BETWEEN FRAMES (R3 part 2; the reviewer 2026-10-10 22:14Z). ON; reason in
# conform/arms.py. ON, the order objects change in inside one action gives each one a mode.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_CASCADE_AGENCY = armflag.arm("TETHER_CASCADE_AGENCY", default=True)
# 7a(8) MC3/MC4 (R3 part 2; the reviewer 2026-10-10 22:33Z). ON; reason in conform/arms.py. A
# reading only: the ground's record of every ending, and a plan's need read against it.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_MC34 = armflag.arm("TETHER_MC34", default=True)
# 7a(7) TWO READINGS (R3(a); the reviewer 2026-10-10 22:30Z). ON (7.5 switch-on, 02:19Z); reason
# in conform/arms.py.
_TWO_READINGS = armflag.arm("TETHER_TWO_READINGS", default=True)
# 7c M6 INVENT (ISAIAH_RULINGS "Mint, invent, import"; the reviewer 2026-10-10 23:14Z). ON by
# default (the reviewer 2026-10-11 02:55Z); reason in conform/arms.py. Not the retired
# TETHER_INVENT: it names a COMPOSITION, priced by the bargain.
_M6_INVENT = armflag.arm("TETHER_M6_INVENT", default=True)
# 7a(10) MC6 MUSE (R3 part 2; the reviewer 2026-10-10 23:50Z). ON; reason in conform/arms.py.
# Compute only: no action, no bet, nothing installed -- a MUSE row is all it writes.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_MC6 = armflag.arm("TETHER_MC6", default=True)
# 7e THE VIEW HOLD (Fig 12 :107-108; the reviewer 2026-10-14 00:49, 00:57). ON by default
# (Isaiah 2026-10-14 06:07: "the library never resets"); reason in conform/arms.py. A cost
# change only: the same views, looked up rather than re-derived. 0 is the one-flag control.
_VIEW_HOLD = armflag.arm("TETHER_VIEW_HOLD", default=True)
_HELD_ROLES = ("STATE", "TEST", "PROCESS", "CAUSE")   # RELATION/MEASURE filter on x (library 504)
# (b'-q) THE INDEX HOLD (Fig 12 :107-108; the reviewer 2026-10-14 12:19, 12:23). ON; reason in
# conform/arms.py. A held role's view is compiled ONCE per process under the placeholders and a
# question binds its names to the result: no compile per question. A cost change only.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_INDEX_HOLD = armflag.arm("TETHER_INDEX_HOLD", default=True)
PH_O, PH_X = "PHo", "PHx"   # no id generator makes these (arc_percept 638, gridworld 225)
_INDEX_STORE: dict = {}     # (compile_term.signature, entry, role) -> held compiles
_INDEX_N: Counter = Counter()   # held, bound, bound_memo_hit, named; the agent never reads it
# THE BOUND ANSWERS OUTLIVE THE GAME (Isaiah 2026-10-15 06:01; the reviewer 06:10, 06:56): one
# memo per PROCESS, keyed by the code primitives' content token, used only by an Agent whose
# Gamma holds the shared objects (gamma.shared_token); any other Agent keeps its own memo.
_BOUND_MEMO: dict = {}     # (atoms_token, sig, entry, role, o, x) -> bound answers
# S1: the slot-filtered answers, kept APART from _BOUND_MEMO so the lineage never writes a
# partial view as a whole one: (atoms_token, sig, entry, role, o, x, slot) -> the rows bound
_BOUND_SLOT_MEMO: dict = {}
_BOUND_SLOT_IDX: dict = {}   # S1b: the same key -> the HELD indices of its rows (bs_ carries)
# S1c (the reviewer 2026-10-15 12:02): keyed like _BOUND_MEMO and living with it. A pair (entry,
# role, o, x) asked for a second slot is the first evidence it is reused, so its WHOLE is bound once
# and held; a held whole is indexed ONCE by landing slot, so each slot is a lookup, never a scan
_PAIRS_SEEN: set = set()     # pairs whose first slot was answered (bound, or carried in bs_)
_BOUND_SLOT_MAP: dict = {}   # whole-memo key -> (landing slot -> row indices, every-slot indices)
_PLAIN = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")
# SPEED-2 (Isaiah 2026-10-15 17:24; the reviewer 17:31, 17:32): a pair's refusals are counted
# ONCE, into the Counter _index_reach adds, and never re-iterated per slot, bound, or kept in
# a slot's memo. The same views, causes and counts; OFF is today's line exactly
_SPEED2_COUNT = armflag.arm("TETHER_SPEED2_COUNT", default=True)
_PAIR_TALLY: dict = {}   # whole-memo key -> (the pair's refusal Counter, the held indices
#                          of its uncounted every-slot rows)
# (b'-l) THE LINEAGE HOLD, phase 1 (Fig 6, Fig 12, Fig 4; the reviewer 2026-10-14 16:29, 16:34,
# 16:38, 17:02). ON; reason in conform/arms.py. What a boundary clears is kept DORMANT in instance
# form, as the record, and never consulted by slot name on a later level; a same-level restart
# carries it back per object where identity is sure. One attempt row per attempt.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_LINEAGE_HOLD = armflag.arm("TETHER_LINEAGE_HOLD", default=True)
# F1, THE AGENT PERCEIVES A LEVEL CLEAR (the reviewer 2026-10-15 07:32, 07:42, 07:55): the runners
# deliver a levels_completed rise with no terminal edge as retarget(how=ADVANCE), the ending whose
# reading is "the next board is UNKNOWN by design" (ledger ENDING_READS). Read here, used there.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_LEVEL_EDGE = armflag.arm("TETHER_LEVEL_EDGE", default=True)
# A1-CONVERT (Isaiah 2026-10-15 08:07: "make sure it gives the autonomy to the agent to decide from
# what they inform"; the reviewer 08:55, 09:05, 09:11, 09:12, 09:19, 09:33, 09:38): where an order
# we wrote chose, the options go to frontier.frontier_pick in the agent's own readings and the
# pick is recorded. One switch per group; OFF restores our order exactly.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_A1_CHOOSE = armflag.arm("TETHER_A1_CHOOSE", default=True)          # the known-effect pick
_A1_STARVED = armflag.arm("TETHER_A1_STARVED", default=True)        # which starved slot to probe
_A1_OBJECTIVE = armflag.arm("TETHER_A1_OBJECTIVE", default=True)    # bound objective vs want
_A1_TIES = armflag.arm("TETHER_A1_TIES", default=True)              # the exact ties
# A1-CONVERT GROUP 2 (the reviewer 2026-10-15 09:05, 09:19, 14:23, 14:27; Isaiah 09:11, 14:15): the
# streams, walked in the agent's own readings' order (the residual gate, then actions, with bits
# inside), exact ties by the recorded draw; and an objective's unseen values priced, not removed.
# Each default ON (Isaiah 2026-10-15 07:53); each OFF is today exactly; the switches are kept.
_A1_STREAM = armflag.arm("TETHER_A1_STREAM", default=True)          # site 4: the stream share
_A1_LIBRARY = armflag.arm("TETHER_A1_LIBRARY", default=True)        # site 6: library chains merged
_A1_LOOKUP = armflag.arm("TETHER_A1_LOOKUP", default=True)          # sites 7-8: the bind key
_A1_DOMAIN = armflag.arm("TETHER_A1_DOMAIN", default=True)          # site 9: the unseen priced
# SPEED-1 S1 (the reviewer 2026-10-15 11:00, 11:05; Isaiah 10:56 "never at the sacrifice of
# functionality"): _index_reach asks for the views that land on ONE slot, so under the hold only
# the held rows that land there are bound (Fig 7: "The room is summoned by the residual rather
# than composed."); refusals and quantified rows are counted as before. Nothing perceived, held
# or checked is removed: only work whose result was thrown away is skipped. A5: an animal
# looking for water does not taste every stone on the way. default ON (Isaiah 2026-10-15
# 07:53); the switch is kept.
_SLOT_FILTER = armflag.arm("TETHER_SLOT_FILTER", default=True)
# S5 of the decay class (the reviewer 2026-10-15 16:18, 18:13): a reach verdict is filed with
# whether the agent was alive when it was watched, so a dead board's verdict does not decide
# a live one
_SITUATED_REACH = armflag.arm("TETHER_SITUATED_REACH", default=True)
# 7h (the reviewer 2026-10-15 17:32, 19:59). TRIED: least-known at site 8 reads how often each
# operand was tried on the slot THIS level (level, slot, operand; age only orders within a
# level, Isaiah 10-09). SHOWN: least-known at site 9 reads how often each value was shown. ROOT:
# one row per live situation answering what is shown, what is expected, what is still open,
# graded at the next boundary by the ground's ending -- a record only, read by no chooser (A1)
_7H_TRIED = armflag.arm("TETHER_7H_TRIED", default=True)
_7H_SHOWN = armflag.arm("TETHER_7H_SHOWN", default=True)
_7H_ROOT = armflag.arm("TETHER_7H_ROOT", default=True)
# 7j (the reviewer 2026-10-15 17:32, 20:27): a choice made to test a held hypothesis -- the goal
# exit acting on the agent's own objective term -- gets one row pairing the term's prediction
# with what the ground then showed, linked to the 7h root. A record read by no chooser (A1)
_7J_TEST = armflag.arm("TETHER_7J_TEST", default=True)
# 7l (the reviewer 2026-10-15 17:32, 20:41, 20:54): the library answers that LANDED, by KIND as
# the agent holds it (the sorted attribute types of an owner's slots; the SHAPE value is not
# canonical, arc_percept 853-855 numbers shapes in order of first sight), and one episode per
# ask (game, level, slot, pair, what landed, salience = the slot's outstanding surprise);
# carried by the lineage, read by no chooser. 7m: a pair whose kinds LANDED before goes first
# at site 8
_7L_KIND = armflag.arm("TETHER_7L_KIND", default=True)
_7M_ANALOGY = armflag.arm("TETHER_7M_ANALOGY", default=True)
# 7d, THE REVERSE LOOKUP (the reviewer 2026-10-16 11:56): the entries filed as PRODUCING a changed
# reading are asked after the forward ones (Library.light abduce="after"); one "abduce" row per
# lookup
_LIBRARY_ABDUCE = armflag.arm("TETHER_LIBRARY_ABDUCE", default=True)
_OBJ_ID = re.compile(r"o\d+")
# store name -> the Agent attribute it is cleared from at retarget (tether 1998-2010, 2049)
_LINEAGE_STORES = (("reach_tested", "_reach_tested"), ("wants", "wants"),
                   ("want_terms", "_want_terms"), ("undone", "_undone"),
                   ("undone_across", "_undone_across"), ("prev_gap", "_prev_gap"),
                   ("gap_delta", "_gap_delta"), ("refuted_slot", "_refuted_slot"),
                   ("d5_candidates", "_d5_candidates"), ("d5_pending", "_d5_pending"),
                   ("d5_parts", "_parts"), ("refuted", "refuted"), ("refuted_at", "refuted_at"),
                   ("trace", "trace"))   # every one a dict at __init__ but trace, a list (1513)
# carried back on a same-level restart (the rest stay dormant, the record only): see _carry_lineage
_LINEAGE_CARRY = ("reach_tested", "wants", "want_terms", "undone", "undone_across")
# 7a(10) D1-D3, THE SAME LOOP ONE LEVEL UP (R3 part 2; the reviewer 2026-10-10 23:50Z). ON with
# objective build 1 (02:19Z); reason in conform/arms.py. Process bets about GROUND outcomes,
# settled only at a level or game ending.
_D13 = armflag.arm("TETHER_D13", default=True)
# OBJECTIVE BUILD 1, THE COMPLETION SWEEP (ARC_AGENT 21.3; the reviewer 2026-10-11 02:19Z). ON;
# reason in conform/arms.py. Record only: fires when the WORLD's objective is reached.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_COMPLETION_SWEEP = armflag.arm("TETHER_COMPLETION_SWEEP", default=True)
# OBJECTIVE BUILD 2, THE GOAL CONDITION (the reviewer 2026-10-11 02:19Z). ON; reason in
# conform/arms.py. At a completion, a condition over readings that names when the world's
# objective holds -- the flag is the then-side, never the subject. Needs the sweep ON.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_GOAL_CONDITION = armflag.arm("TETHER_GOAL_CONDITION", default=True)
# OBJECTIVE BUILD 3, THE LINK TO COMPOSITION (the reviewer 2026-10-11 02:19Z, 03:14Z). ON; reason
# in conform/arms.py. A held goal condition becomes one of the agent's composed objectives.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_GOAL_LINK = armflag.arm("TETHER_GOAL_LINK", default=True)
# OBJECTIVE BUILD 2a, THE GOAL PAIR (the reviewer 2026-10-11 05:14Z). ON; reason in
# conform/arms.py. A held goal condition may be the AND of two conditions, priced as one term.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_GOAL_PAIR = armflag.arm("TETHER_GOAL_PAIR", default=True)
# F2 (the reviewer 2026-10-11 05:38Z): ONE lookup for a slot's objective. ON; reason in
# conform/arms.py. ON, _goal_target and _term_of read it as goal_residual already does.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_WANT_TARGET = armflag.arm("TETHER_WANT_TARGET", default=True)
# F2's fallback (the reviewer 2026-10-11 07:20Z): the target reads a retained want ONLY where it is
# subject-scoped (a goal-condition want); every own want keeps the masked lookup. OFF; reason in
# conform/arms.py. With TETHER_WANT_TARGET also ON, the full unmask subsumes it.
_WANT_TARGET_SUBJECT = armflag.arm("TETHER_WANT_TARGET_SUBJECT")
# R-dir (ii) (the reviewer 2026-10-11 10:39Z): a held routine whose live comparison now reads the
# OPPOSITE sign to the one it was minted with ends "stale" before pressing. ON; reason in
# conform/arms.py.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_ROUTINE_STALE = armflag.arm("TETHER_ROUTINE_STALE", default=True)
# R-dir (c) (the reviewer 2026-10-11 10:39Z): a one-slot BECOME body can change only its subject,
# so its budget, and the count it claims, come from that subject's own gap. ON; reason in
# conform/arms.py.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_ROUTINE_SUBJECT_BUDGET = armflag.arm("TETHER_ROUTINE_SUBJECT_BUDGET", default=True)
# B, DIRECTION MOVABLE (the reviewer 2026-10-12 05:43, 05:47 CDT): a slot is movable when, in one
# context -- its object's signed offset from the controlled owners, read off the agent's own pair
# slots -- two actions change it with different PURE signs. contingent()'s always/never, one level
# down (Fig 11's second-order effect). ON; reason in conform/arms.py.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_DIRECTION_MOVABLE = armflag.arm("TETHER_DIRECTION_MOVABLE", default=True)


@dataclass(frozen=True)
class _Pair:
    """Two compiled goal conditions held together: true only when both are (the `both` atom's
    meaning). Its length is both parts plus the joiner, priced once as one term."""
    parts: tuple

    @property
    def slot(self) -> str:
        return self.parts[0].slot

    def holds(self, state: dict) -> bool:
        return all(compile_term.run(c, state) is True for c in self.parts)


def _confirm_actions(r: Any) -> int | None:
    """The actions until a plan has been SEEN TO HOLD (Fig 12 :126, "Actions price finding out
    whether it holds"). A routine is confirmed only by running it, so this is its length in
    presses: the cost of finding out it holds, not a proxy for "long is bad". None where it
    cannot be counted (a choice, a library call), and such a plan is never dominated."""
    if isinstance(r, Rt.Act):
        return 1
    if isinstance(r, Rt.Seq):
        a, b = _confirm_actions(r.first), _confirm_actions(r.then)
        return None if a is None or b is None else a + b
    if isinstance(r, Rt.When):
        return _confirm_actions(r.body)
    if isinstance(r, Rt.Until):
        b = _confirm_actions(r.body)
        n = r.expect if r.expect is not None else r.budget
        return None if b is None or n is None else n * b
    return None
SELF_MOVED, REACTING, MOVES_WITH = "self-moved", "reacting", "controlled"
# an ending's word -> Termination's kind; the seat's budgets are caps, every other word is its own
_TERM_KIND = {"death": "death", "cap": "cap", "time": "cap", "run_end": "cap"}
# THE BOUNDARY ROWS' OWN CHAINS (the reviewer 2026-10-10 08:11Z, 09:40Z). retarget's boundary/ending
# and the death restart go on "@boundary", the 21.3 credit on "@credit", at THE CYCLE with the level
# as a field: at cycle = self.level on "@loop" they sat behind that cycle's REPEAT row, and credit
# (SETTLE) sat behind the IMPORT rows, so gate check 1 refused every level end and every restart.
# False reproduces that keying, for the must-fail only.
_BOUNDARY_CHAIN = True
# THE REFERENCE COST (the reviewer 21:55Z): a reused term's DEFINITION is paid once, but NAMING it
# is paid per use, log2(H+1) over the H held terms (the corpus's +log2(k+1), as `_guard_bits`).
# False removes it, for must-fail (r) only.
_CARRY_REF = True


def _kind_of(out_t: str) -> str:
    """A stream's kind, from its output type."""
    return ("predictor" if out_t == "val"
            else "objective" if out_t == OBJ_TYPE else f"typed:{out_t}")


def _floor_champion(by_kind: dict, kind: str, best, share: bool):
    """D2: the champion a stream's floor test reads. ON: its own kind's (the reviewer 06:19 CDT).
    OFF: the shared best, as before."""
    return by_kind.get(kind) if share else best


def _next_stream(live: list, spent: dict, share: bool, key: str | None = None,
                 seed: str | None = None) -> int:
    """D2: the stream that takes the next candidate. OFF: the first live stream, which is the old
    sequence (each stream to exhaustion before the next). ON: the least rank spent this round,
    ties to list order; under TETHER_A1_STREAM (site 4) an exact tie goes to the recorded draw,
    never to the list order. No share, weight or quota."""
    if share and key is not None:
        return min(live, key=lambda s: (spent[s], FR.draw_key(key, s, seed)))
    return min(live, key=lambda s: (spent[s], s)) if share else live[0]


def _merge_by_depth(lib_chains: list, closure, evidence: dict, key: str, seed: str | None = None):
    """A1 site 6 (the reviewer 2026-10-15 09:05 U3, 14:23): the library's chains enter the closure's
    own walk order (shortest first) at their own depth, never all ahead of it. Within a depth,
    evidence (the entries that offered the chain) orders a library chain ahead of the closure's,
    which carry none; library chains tied on depth and evidence go by the recorded draw. Nothing is
    enumerated twice: the closure is walked once, as before."""
    pend = sorted(lib_chains, key=lambda c: (len(c.atoms), -evidence.get(c.name, 0),
                                             FR.draw_key(key, c.name, seed)))
    i = 0
    for c in closure:
        while i < len(pend) and len(pend[i].atoms) <= len(c.atoms):
            yield pend[i]
            i += 1
        yield c
    yield from pend[i:]


def _test_outcome(before: Any, after: Any, target: Any, ordered: bool) -> str:
    """7j: what the ground showed against what the term predicted. Closer and farther need an
    ORDERED value (the slot's own type, ORDERED_TYPES); a categorical value is reached or not
    (J-a, the reviewer 2026-10-15 20:27)."""
    if after is None:
        return "slot gone"
    if after == target:
        return "reached"
    if after == before:
        return "no change"
    # J-c (the reviewer 2026-10-15 20:41): a value that is not a number (None, a tuple, a
    # string) cannot be closer or farther, so it is graded as categorical
    num = all(isinstance(v, (int, float)) and not isinstance(v, bool)
              for v in (before, after, target))
    if not ordered or not num:
        return "not reached"
    return "closer" if abs(after - target) < abs(before - target) else "farther"


def _lookup_order(names: list, comp: dict, dk: str, evidence=None, seed=None) -> list:
    """A1 sites 7-8 (the reviewer 2026-10-15 14:23, 14:27): the shape's order over operand slots.
    comp[s] = (contact, derived, library evidence, distinct values over the failing frames): the
    residual GATE (in contact with the open slot's owner, 0 first), the ACTIONS walk (a derived
    slot is one more composition step), BITS inside it (more evidence first), the residual
    MAGNITUDE (more distinct values first), then the recorded draw. `evidence` replaces the
    library count (site 7: this chain's offers). LEAST-KNOWN is comp[s][4] when present (7h's
    tried count this level, fewer first), before the draw. 7m puts ANALOGY before it (a kind
    pair seen before, first): the extra fields are read in order, so OFF keeps today's key."""
    def ev(s):
        return comp[s][2] if evidence is None else evidence(s)
    return sorted(names, key=lambda s: (comp[s][0], comp[s][1], -ev(s), -comp[s][3],
                                        *comp[s][4:], FR.draw_key(dk, s, seed)))


class _PricedDomain(frozenset):
    """A1 site 9 (U2, the reviewer 2026-10-15 09:05, 14:23): the values an objective searches FIRST
    (shown before this frame, and each operand +-1), carrying what prices the rest of the alphabet:
    its size, the shown counts, the draw key and the agent's row writer. Nothing is removed."""


def _priced_hit(evaluate, current: int, ordered: bool, dom: _PricedDomain):
    """The satisfying value an objective aims at, read in two currencies held apart (Fig 12):
    DISTANCE from current (actions) and NOVELTY (bits: 0 if shown, else log2 of the count of
    unseen values). Only two values can be on the frontier: the nearest satisfying shown value,
    and the nearest satisfying unseen one NEARER than it (a farther unseen one is dominated), so
    the unseen walk stops at the shown answer's distance. Comparable-only: every distance is
    equal, so a shown value dominates and the unseen are searched only when none is shown.
    Values at one distance are tied, and the recorded draw decides, never the lower value (F1,
    the reviewer 2026-10-15 14:42; TIES: never a position)."""
    def dk(v):
        return FR.draw_key(dom.key, v, getattr(dom, "seed", None))
    walk = sorted(dom, key=(lambda v: (abs(v - current), dk(v))) if ordered else dk)
    shown = next((v for v in walk if v != current and evaluate(v)), None)
    if shown is not None and not ordered:
        return shown
    unseen = None
    if ordered:
        for d in range(1, abs(shown - current) if shown is not None else dom.alpha):
            ring = [v for v in (current - d, current + d)
                    if 0 <= v < dom.alpha and v not in dom and evaluate(v)]
            if ring:
                unseen = min(ring, key=dk)
                break
    else:
        ring = [v for v in range(dom.alpha) if v != current and v not in dom and evaluate(v)]
        unseen = min(ring, key=dk) if ring else None
    if unseen is None or shown is None:
        return shown if unseen is None else unseen
    n = dom.alpha - len(dom)
    opts = [(shown, 0.0, abs(shown - current)),
            (unseen, math.log2(n) if n > 1 else 0.0, abs(unseen - current))]
    pick, by, front = FR.frontier_pick(opts, None, {shown: dom.counts.get(shown, 0), unseen: 0},
                                       dom.key, getattr(dom, "seed", None))
    if dom.note is not None:
        dom.note(opts, pick, by, front)
    return pick


def _recording(chains, into: list):
    """Yield each chain, recording it into `into`: pass 2 walks that record, a LOOKUP of what pass 1
    reached and never a second enumeration (the reviewer 19:45Z; Fig 12: nothing is re-earned)."""
    for c in chains:
        into.append(c)
        yield c


@cache
def _library():
    """The library runtime, loaded once per process (M4). None if the library is absent."""
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library")
    if not os.path.isdir(root):
        return None
    if root not in sys.path:
        sys.path.insert(0, root)
    import library_runtime
    return library_runtime.Library(root).load()


def _ph_sub(s: Any, o: str, x: str) -> Any:
    return s if s is None else s.replace(PH_O, o).replace(PH_X, x)


def _bound(c: Any, sub: Any, atoms: dict) -> Any:
    """A held compile under this question's names: the names put back, the bbox pair re-sorted
    (compile_term 296), the Term rebuilt from THIS Gamma's atoms by name. No compile."""
    if c is None:
        return None
    if isinstance(c, compile_term.Refusal):
        return compile_term.Refusal(sub(c.reason))

    def term(t: Term) -> Term:
        return _replace(t, atoms=tuple(atoms[a.name] for a in t.atoms), operand=sub(t.operand),
                        guard_ref=sub(t.guard_ref),
                        operand_term=term(t.operand_term) if t.operand_term is not None else None)
    parties = tuple(sub(p) for p in c.parties)
    slot = sub(c.slot)
    if slot.endswith(".bbox"):
        a, b = sorted(parties)
        slot = f"{a}~{b}.bbox"
    return compile_term.Compiled(slot, term(c.term), sub(c.operand), parties, c.absent, c.via)


def _slot_of(c: Any, sub: Any) -> str:
    """A held compile's slot under this question's names: _bound's own slot step (sub, then the bbox
    pair re-sorted), without rebuilding the Term (S1)."""
    slot = sub(c.slot)
    if slot.endswith(".bbox"):
        a, b = sorted(sub(p) for p in c.parties)
        slot = f"{a}~{b}.bbox"
    return slot


def _lands(role: str, a: Any, b: Any, slot: str, sub: Any) -> bool:
    """S1: is this held row needed for a question about `slot`? Every row _index_reach counts
    (a quantified view, a refusal on either side) is kept; otherwise the row's own slot (a CAUSE's
    then-slot) must be the asked one."""
    if role == "CAUSE":
        if (a is None or b is None or isinstance(a, compile_term.Refusal)
                or isinstance(b, compile_term.Refusal)):
            return True
        return _slot_of(b, sub) == slot
    if a is None or isinstance(a, compile_term.Refusal):
        return True
    return _slot_of(a, sub) == slot


def _same(s: Any) -> Any:
    """S1: the names of an already-bound row are this question's; nothing to put back."""
    return s


def _slot_map(role: str, whole: tuple) -> tuple:
    """S1c: a held WHOLE indexed once: landing slot -> its row indices (a CAUSE lands on its
    then-slot), and the rows _index_reach counts for every slot (quantified, a Refusal, a CAUSE
    with None on either side), each list in held order. A bound row's slot is already in the
    question's names, so c.slot is read, never substituted: the same rows _lands keeps."""
    by: dict = {}
    every = []
    for i, (_c, a, b) in enumerate(whole):
        if (a is None or isinstance(a, compile_term.Refusal)
                or (role == "CAUSE" and (b is None or isinstance(b, compile_term.Refusal)))):
            every.append(i)
        else:
            by.setdefault((b if role == "CAUSE" else a).slot, []).append(i)
    return {k: tuple(v) for k, v in by.items()}, tuple(every)


def _core_kind(offers: Any, term: Any) -> str | None:
    """7i: "inherit" when an offer is the library's description of the WHOLE term with its operand
    and the term is one atom or concept, "learn" when it is a whole multi-atom recipe, None when
    no offer equals it (an extension, another operand: new, earned in play)."""
    names = tuple(a.name for a in term.atoms)
    if any(o_["operand"] == term.operand and tuple(a.name for a in o_["term"].atoms) == names
           for o_ in offers):
        return "inherit" if len(names) == 1 else "learn"
    return None


def _tally_key(role: str, a: Any, b: Any, sub: Any) -> str | None:
    """SPEED-2: the key _index_reach counts a row under, or None for a row it reads. The
    reason is the bound text: _bound's Refusal is Refusal(sub(c.reason))."""
    if role == "CAUSE":
        if isinstance(a, compile_term.Refusal):
            return "if: " + sub(a.reason)
        if isinstance(b, compile_term.Refusal):
            return "then: " + sub(b.reason)
        return None
    if a is None:
        return compile_term.QUANTIFIED
    return sub(a.reason) if isinstance(a, compile_term.Refusal) else None


def _pair_tally_of(ag: Any, mkey: tuple) -> tuple | None:
    return (_PAIR_TALLY if ag._atoms_token else ag._pair_tally).get(mkey)


def _whole_rows(role: str, whole: tuple, slot: str, maps: dict, mkey: tuple) -> tuple:
    """S1c: the held indices of a held whole's rows for `slot`, from its slot map (built once)."""
    smap = maps.get(mkey)
    if smap is None:
        smap = maps[mkey] = _slot_map(role, whole)
    return tuple(heapq.merge(smap[0].get(slot, ()), smap[1]))


def _restore(held: list, o: str, x: str) -> list:
    """7e: a held view under the names o and x. Only the name-bearing fields (library view and
    candidates: "condition"; CAUSE "if"/"then") are substituted; every other field is copied."""
    out = []
    for c in held:
        c = dict(c)
        for f in ("condition", "if", "then"):
            if f in c:
                c[f] = c[f].replace("{o}", o).replace("{x}", x)
        out.append(c)
    return out


def _replace_lib(lib: Any) -> Any:
    """M6: a Library sharing the read-only seed and readings, with its own runtime and indexes."""
    import copy
    p = copy.copy(lib)
    p.runtime = dict(lib.runtime)
    dd = collections.defaultdict
    p.by_reading = dd(list, {k: list(v) for k, v in lib.by_reading.items()})
    p.by_affects = dd(list, {k: list(v) for k, v in lib.by_affects.items()})
    p.ingredient_of = dd(list, {k: list(v) for k, v in lib.ingredient_of.items()})
    return p
# THE out_type WIDENING -- Isaiah's 3A, reviewer-pre-registered 2026-09-23. `mint` asks for
# `("val","val")` and `(slot_type, OBJ)` and NOTHING ELSE, and the composition census says
# that IS the ceiling: 4 distinct compositions on every board, which are exactly those two
# streams. Widened, mint also asks for `(slot_type, T)` for each T THE DELTA LIGHTS.
#
# ABORT CRITERIA, declared before the first run and unchanged: candidates tried rises while
# arrivals do not -> OFF; calls-per-cycle growth steepens against the control -> OFF; binds
# per candidate rises -> OFF. Each is a RESULT, not a failure.
_STREAM_WIDEN = armflag.arm("TETHER_STREAM_WIDEN")
# D2, STREAM SHARE (the reviewer 2026-10-12 05:43, 06:19 CDT): within a round, the stream that has
# spent the least rank takes the next candidate (Fig 6: distribute the search, keep the searchers
# independent), and a stream stops at its OWN kind's floor. ON; reason in conform/arms.py.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_STREAM_SHARE = armflag.arm("TETHER_STREAM_SHARE", default=True)
# PARK WANT (the reviewer 2026-10-12 08:43, 08:52 CDT): the park return wrote no unpaid want, so
# Isaiah 09-25's retained want reached only mints where something else paid. ON; conform/arms.py.
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_PARK_WANT = armflag.arm("TETHER_PARK_WANT", default=True)
# ITEM 7. Default OFF: it APPENDS TO THE ATOM REGISTRY, which every term reads.
# **THE RANDOMISED HOLD -- MEASUREMENT ONLY, the reviewer 2026-10-03 ruling 3.** Withholds
# the `ACTED_SELF` offer on a seeded ~half of ELIGIBLE occasions so a measurement run carries
# its own within-run control. OFF in the shipping agent: a control that changes what the agent
# is offered is an instrument, not a capability, and leaving it on would make every later
# reading a reading of the instrument.
_HOLD = armflag.arm("TETHER_HOLD")
# THE SEED IS THE AGENT'S (HOLD_SEED; the reviewer 2026-10-15 14:56, 15:04): drawn at birth from
# the OS's entropy, recorded in the run header and the lineage, carried by a lineage (the same
# being, Isaiah 10-14) with its generation index so a continued life does not replay its day, and
# read back from a record for a replay (TETHER_SEED_FROM names the record, never a seed). Fig 10
# :72-74 "the pool must be unauthored first and examined second". OFF: "0", as before.
_AGENT_SEED = armflag.arm("TETHER_AGENT_SEED", default=True)


def _seed_from_record(path: str) -> dict:
    """A replay's seed and generation, READ from the record a run wrote: a ledger (the last @run
    row carrying a seed) or a lineage generation. Nothing is chosen here, and a record that
    carries no seed is refused by name; no constant stands in."""
    from pathlib import Path
    raw = Path(path).read_bytes()
    tag = f"replay:{hashlib.sha256(raw).hexdigest()[:16]}"
    text = raw.decode("utf-8")
    if path.endswith(".jsonl"):
        rows = [json.loads(ln) for ln in text.splitlines() if ln.strip()]
        got = [r["detail"] for r in rows if r.get("slot") == "@run"
               and (r.get("detail") or {}).get("seed_source", "constant") != "constant"]
    else:
        g = json.loads(text)
        got = [g] if g.get("seed") is not None else []
    if not got:
        raise ValueError(f"TETHER_SEED_FROM={path}: the record carries no seed of the agent's; "
                         "nothing is substituted")
    return {"seed": got[-1]["seed"], "generation": int(got[-1].get("generation") or 0),
            "seed_source": tag}


def _seed_at_birth() -> dict:
    """The agent's seed when it is made: OFF the old constant; a replay reads its record; else a
    fresh draw from the OS that nothing of ours picks."""
    if "TETHER_HOLD_SEED" in os.environ:
        raise ValueError("TETHER_HOLD_SEED is retired (the reviewer 2026-10-15 15:04): the seed "
                         "is the agent's; a replay names a record with TETHER_SEED_FROM")
    if not _AGENT_SEED:
        return {"seed": FR.SEED, "generation": 0, "seed_source": "constant"}
    src = os.environ.get("TETHER_SEED_FROM")
    if src:
        return _seed_from_record(src)
    import secrets
    return {"seed": secrets.token_hex(8), "generation": 0, "seed_source": "birth"}

# `_INVENT` / `_invent` REMOVED -- Isaiah 2026-10-04, *a bootleg composition*; RETIRED means
# gone. Why, measured: `F431.6`. `conform/arms.py` `RETIRED` refuses the flag if it returns.

# ARM M -- PERTURB THE STARVED SLOT, IN PARALLEL. SEAT-SIDE SWITCH, DEFAULT ON.
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
# default ON (Isaiah 2026-10-15 07:53); the switch is kept for the checklist's culprit isolation.
_STARVED_CONTACT = armflag.arm("TETHER_STARVED_CONTACT", default=True)

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


# anchor: how many idle cycles buy one unit of threshold relief. NOT a tuning dial and not
# derived from a run -- it is the RATE at which "the agent is always paying" is charged, and
# Isaiah ruled the charge exists without naming a rate. Set so that a full `MIN_REPEAT` bar is
# relieved to the floor after `MIN_REPEAT * _IDLE_RELIEF` idle cycles: with MIN_REPEAT 2 and
# this at 8, an agent that has committed to nothing for 8 cycles needs one contribution less.
# **A CALIBRATION CONSTANT under `F341`'s third category: visible, movable, not claimed
# correct.** Moving it changes how patient the agent is, which is exactly why it is one name
# in one place rather than an expression at the site.
_IDLE_RELIEF = 8.0

# anchor: DERIVED FROM THE QUORUM CONSTRAINT, NOT PICKED -- 2026-09-26, and the derivation is
# the whole justification the reviewer asked for.
#
# The floor was 1.0. Contributions are scaled so one contributor at full strength is worth 1.0,
# so a floor of 1.0 is cleared BY ONE -- and the single commitment the accumulator ever made
# was carried by `improving` alone. That is the defect: *a quorum reachable by one bee is not
# a quorum.*
#
# The obvious repair -- floor = MIN_REPEAT -- KILLS THE RELIEF MECHANISM. Relief decays the bar
# from `MIN_REPEAT` downward, so a floor AT `MIN_REPEAT` leaves it nowhere to fall and an idle
# agent becomes no more willing than a busy one. The floor therefore has to sit strictly
# between one contribution and the full bar.
#
# **SO IT IS THE LARGEST RELIEF THAT STILL LEAVES ONE CONTRIBUTOR INSUFFICIENT: half a vote.**
# `MIN_REPEAT - 0.5`. Patience can buy the agent half a contribution's worth of willingness and
# never a whole one, so a commitment always needs a second voice carrying at least the other
# half. The 0.5 is not a dial -- it is the midpoint of the only interval the two constraints
# leave open, and moving it to 1.0 reopens the defect while moving it to 0.0 disables relief.
# Since item 6 the BAR is the agent's own (`_commit_bar`), and the floor sits this half-vote under
# it, for the same reason.
_QUORUM_HALF = 0.5

# anchor: TWO, and it is the definition of a quorum rather than a calibration. One agreeing
# contributor is a report; two is the smallest number that can DISAGREE and did not. Raising
# it would be a tuning choice and is not made here.
_QUORUM_VOTERS = 2

# THE OBSERVER'S MUTATION CLASSES -> THE WORLD'S ATTRIBUTE NAMES. A TABLE, NOT A RULE, for
# `CLAUDE.md`'s stated reason: *exemptions as data, not logic -- a table can be pinned; logic
# widens quietly.* Matching on a substring or a shared prefix would silently absorb the next
# class the observer learns to emit.
#
# **THE UNMAPPED CLASSES ARE UNMAPPED ON PURPOSE AND THAT IS A READING, NOT A GAP.** `density`,
# `girth`, `solidity`, `orientation`, `holes`, `area`, `occupiedCells`, `perimeter` and
# `velocity` all mutate and NO SLOT HOLDS THEM -- perception computes them, the decomposition
# does not publish them. So a cue can fire with nothing to point at, and that is the honest
# state rather than something to paper over by guessing a nearest slot. It is also a measured
# statement of how much wider the observer sees than the slot set: nine classes to four.
_CUE_ATTR: dict[str, tuple[str, ...]] = {
    "position": ("row", "col"),
    "extent": ("h", "w"),
    "shape": ("shape",),
    "colour": ("colour",),
}

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
    "want_recurred",                    # a retained want that a LATER attempt wanted again
    "goal_link_made",                   # build 3 L2: a goal condition became its slot's want
    "goal_link_refused_wants",          # build 3 L2: refused, the slot already wanted
    "goal_unlinked",                    # build 3 L1: a linked condition stopped paying
    # THE MUTATION OBSERVER, wired to the agent path 2026-09-26. `cue_seen` is the
    # denominator -- frames with a predecessor, so a mutation was POSSIBLE -- and
    # `cue_mutated` the numerator. `cue_blind` counts the abstentions apart, because a
    # blind frame reporting no mutations and a clear frame reporting none are different
    # facts and one book key would collapse them.
    "cue_seen",                         # frames where a mutation could have been read
    "cue_mutated",                      # ... and at least one attribute actually did
    "cue_blind",                        # the observer abstained: no readable board
    # THE CUE REACHING THE INHERITED VOCABULARY. Declared here because the M2 seat
    # caught `focus_by_cue` written and undeclared -- a book key that exists only at
    # its write site is a number nobody can find.
    "mint_order_by_cue",                # cycles where the cue ordered mint's ties
    # ATTENTION MOVED BY A MUTATION. The counterpart to `focus_by_want`, and the pair is
    # the reading: `want` is the selector choosing, `cue` is surprise choosing where the
    # selector had nothing. Two keys because collapsing them would hide which mechanism
    # is actually directing the agent.
    "focus_by_cue",                     # surprise directed attention -- Berlyne 1960
    "committed_on_accumulation",        # the vector crossed where the bargain had refused
    "accumulation_short",               # the vector was read and did not reach the threshold
    "bargain_bounded_out",              # `_cannot_pay` -- a NECESSARY condition, not a choice
    "bargain_does_not_pay",             # `pays` -- the only one of the two that is a judgement
    "bargain_paid",                    # reached the contest
    "mint_no_residual",                 # refused by the residual precondition
    # CARRY CREDIT (item 3, TETHER_CARRY_PRICE) and the seal repair's refusal (item 1).
    "carry_pull_credited",              # a library pull priced on log2(H+1) + left
    "carry_pull_uncredited",            # a library pull priced on cost + left
    "carry_order_differs",              # the lowest whole price was not the first payer
    "carry_sweep_credited",             # a sweep close priced on log2(H+1) + left
    "carry_stale_close",                # a pre-boundary record closed by the sweep (MF-D3)
    "unseal_leaves_more",               # a challenger refused for leaving more than the held rule
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

# why a departed slot is not sorted: its miss is recorded, and no term is owed on a slot that
# no longer exists (the reviewer 2026-10-12 22:35, 22:42; no fifth kind)
LEFT_BOARD = "not sorted: left the board this step; the miss stays recorded"

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


def _press(coord, state: dict | None, landed: str | None) -> dict | None:
    """Where a positioned press went: its cell, the object it is attributed to, and every
    object whose box covers the cell. Read off the state the press was made in."""
    if coord is None or not state:
        return None
    x, y = int(coord[0]), int(coord[1])
    objs = {k.rsplit(".", 1)[0] for k in state if k.endswith(".row")}
    under = sorted(o for o in objs
                   if all(f"{o}.{a}" in state for a in ("row", "col", "h", "w"))
                   and state[f"{o}.row"] <= y < state[f"{o}.row"] + state[f"{o}.h"]
                   and state[f"{o}.col"] <= x < state[f"{o}.col"] + state[f"{o}.w"])
    return {"x": x, "y": y, "landed": landed, "under": under}


def term_bits(k: int, alphabet: int, bonds: int = BONDS) -> float:
    return (k + 1) * math.log2(alphabet + 1) + (k - 1) * math.log2(max(bonds, 1))


def _guard_bits(guard: Any, offered: int, refs: int = 0) -> float:
    """WHAT NAMING A GUARD COSTS. `+log2(G+1)` over the guards on offer.

    **THE FORM IS THE CORPUS'S, NOT THE SEAT'S** -- `ARC_AGENT` §2042 and
    `ARC_BUILD_PLAN` item 4d both price an added parameter at *`+log2(k+1)` bits*, and this
    is that applied to the guard axis. A cost function invented here would be a magic number
    at the one site the whole bargain rests on.

    **AN UNGUARDED TERM PAYS NOTHING EXTRA, AND THE `+1` IS WHY.** No-guard is the DEFAULT --
    the `+1` slot -- so every existing price is unchanged and only the choice among G named
    guards is charged. Without this `inc` and `inc ?ACTED_SELF` cost the SAME 7.8138, so a
    guard that explained even marginally better won for free, and the payment count on
    `click_only` went from 1 to 60 overnight.

    **AND IT CHARGES `ACTED_SELF` ALONE -- the reviewer, 2026-10-02: a HANDICAP ON THE NEW
    GUARD, not a repricing of the system.** Charging every guard also repriced `?TOUCH` and
    `?BECOME OTHER`, which have been free since they were built, and **broke 6 of 29 M2
    checks whose fixtures encode that behaviour.** With `?ACTED` default-OFF the global
    version bought nothing and cost six failures.

    **THE UNPRICED INTENT GUARDS REMAIN A REAL MDL HOLE AND ARE RECORDED AS ONE** (`F408`):
    a guarded term is strictly more specific than its unguarded form whatever the guard, so
    the free ride is wrong in principle. **It is a separate change needing its own
    pre-registration**, because whether those fixtures depend on it incidentally or by
    design is a question about `M2_STANDARD`'s intent and not about this code.
    """
    if guard is None or offered <= 0:
        return 0.0
    if guard not in (ACTED_SELF, ACTED_ON):
        # F408 under TETHER_GUARD_PRICE: the choice it records, among the G on offer.
        return math.log2(offered + 1) if _GUARD_PRICE else 0.0
    # **THE KIND, PLUS THE CHOICE OF REFERENT -- the reviewer, 2026-10-04.** Naming WHICH
    # object the press must land on is a second choice and costs its own bits, by the same
    # `log2(k+1)` form the corpus prices an added parameter at. **`ACTED_SELF` IS COLLAPSED
    # INTO THIS AND PAYS THE SAME**: it was `?ACTED_ON<the slot's own owner>` all along, and
    # a cheaper special case would be the seat deciding that one referent is privileged.
    #
    # PRE-REGISTERED: this RAISES SELF's price. On click_only the true rule paid with a wide
    # margin (9.8138 against a base of 18.0), so it should still pay -- and its new cost is
    # reported rather than assumed.
    return math.log2(offered + 1) + (math.log2(refs + 1) if refs else 0.0)


def _same_object(landed_on: str | None, slot: str) -> bool:
    """Did the press LAND ON the object this slot belongs to? Relative, never a name.

    Both sides reduce to their owner, so a press that landed on `o0` answers YES for `o0.row`
    and `o0.colour` alike -- which attribute is being explained is not what the guard asks.

    **`landed_on` IS THE REALISED PRESS'S TARGET, NOT THE INTENT'S SUBJECT, AND THAT IS WHY
    `a561fb2` WAS REVERTED.** The agent AIMS at a slot and the interface may realise that aim
    by pressing a DIFFERENT object -- on a wired world that IS the mechanism. Reading the aim
    made this TRUE on 48 of 60 steps where the object was never touched.

    `None` is False and not unknown: a press that landed on nothing did not act on this object.
    """
    if not landed_on:
        return False
    return landed_on.rsplit(".", 1)[0] == slot.rsplit(".", 1)[0]


# THE OBJECTIVE'S SEARCH DOMAIN IS WHAT THE WORLD HAS SHOWN -- the reviewer, 2026-10-08 (Fig 11
# "read it off the world"; Fig 12 "a goal is a comparison"). `0` searches the whole alphabet: the
# one-flag control.
_OBJECTIVE_DOMAIN = armflag.arm("TETHER_OBJECTIVE_DOMAIN", default=True)


def pays(cost: float, left: float, base: float) -> bool:
    """The bargain. Strict: a tie does not license a new term."""
    return cost + left < base


def objective_step(evaluate, current: int, ordered: bool, domain) -> Any:
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

    `domain` IS WHAT IS SEARCHED AND THE ALPHABET IS NOT -- the reviewer, 2026-10-08. The
    alphabet is the range a value COULD take, declared whole so pricing is honest; walking it
    cost cd82 2,112 s in one cycle over a 32,769-value perimeter alphabet. `Agent._domain` says
    what the domain is.
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
    if isinstance(domain, _PricedDomain):        # A1 site 9: the unseen priced, not removed
        hit = _priced_hit(evaluate, current, ordered, domain)
        if hit is None:
            return NOT_RESOLVED
        return hit if not ordered else (current - 1 if hit < current else current + 1)
    # P3: THE SAME ANSWER, ASKED AS A FIRST-MATCH. Both arms took ONE element out of a
    # fully-built list -- `hits[0]` and `min(key=(abs(v-current), v))` -- so the probe ran
    # the whole alphabet to answer a question the first hit settles. `evaluate` is `_sat`
    # over `term.apply`, which is pure, so calling it fewer times changes nothing but time.
    #
    # THE ORDER IS THE OLD KEY MADE INTO A WALK, not a new preference: at distance `d`,
    # `current - d` is the smaller `v` and therefore sorted first under `(abs, v)`. A
    # `current` outside the alphabet reduces to the one-sided walk the key already gave it.
    if not ordered:
        for v in sorted(domain):
            if v != current and evaluate(v):
                return v
        return NOT_RESOLVED
    # ONE STEP TOWARD THE NEAREST, WHICH IS THE ARM'S WHOLE CONTENT -- `lo < current` and
    # `hi > current` by construction, so the step is the sign and nothing is recomputed.
    for v in sorted(domain, key=lambda v: (abs(v - current), v)):
        if v != current and evaluate(v):
            return current - 1 if v < current else current + 1
    return NOT_RESOLVED


def objective_gap(evaluate, current: int, ordered: bool, domain) -> Any:
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
    if isinstance(domain, _PricedDomain):        # A1 site 9: the unseen priced, not removed
        hit = _priced_hit(evaluate, current, ordered, domain)
        return None if hit is None else (abs(hit - current) if ordered else 1)
    hits = [v for v in domain if v != current and evaluate(v)]
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
    # **IT BOUNDS THE CHAIN AXIS ONLY -- corrected 2026-10-05.** It counts `rank`, one per chain
    # candidate; operand-TREE candidates (`_trees`) are priced without entering it, and they were
    # 86.8% of all pricing on default seed 0. Trees are unconditional by Isaiah's 2026-09-24
    # ruling, so this is a REPORT of what the cap covers, not a reason to cap them.
    work_budget: int = 15000
    mode: str = SPECIFIED
    # SYSTEM 0 (Isaiah, 2026-09-14): motor babbling before means-end -- draw variously until
    # the action-effect map has coverage, then hand to strategy. Off by default; the A/B toggles.
    # **ON -- Isaiah, 2026-09-25.** *"System 0 is always on. It is almost like an UPTAKE VALVE
    # -- if it catches that nuance or attribute, the whole system set RECALIBRATES."* It has
    # been `False` since it was built, so the intake the reviewer calls the ELABORATION GUARD
    # had never once opened. Systems 1 and 2 are both SELECTIVE BY NATURE and neither can notice
    # anything outside its own frame; 0 has no frame, which is what lets it catch the nuance.
    # **THE OFF SWITCH IS GONE -- ISAIAH, 2026-09-29: *remove the "System 0 off"
    # override. System 0 is always on.* It is not a capability to be configured; it is
    # what notices what 1 and 2 cannot, and a frame-less faculty you can switch off is
    # one the run can silently lack. `conform/arms.py` had it recorded as a field-arm
    # FOUND OFF on the ARC path against a standing ruling -- removing the field ends
    # that class of silence rather than fixing one instance of it.
    # **THE ACCUMULATOR, DEFAULT *ON*. THIS HEADING READ `DEFAULT OFF` ABOVE A `True`
    # VALUE FROM THE DAY IT WAS WRITTEN -- CORRECTED 2026-09-28, AND THE BODY BELOW IS
    # KEPT BECAUSE IT IS THE REASONING, NOT THE ERROR.**
    # Isaiah ruled 2026-09-25 that the bargain KEEPS ITS PRICE AND LOSES ITS MONOPOLY. Five
    # `M2_STANDARD` checks encode the older contract that `pays` is the gate, and they FAIL
    # when this is on: `check_one_bargain` (wrong reason), `check_can_gates_until`,
    # `check_shelf_must_be_runnable_here`, `check_trigger_is_the_residual_not_the_reward`,
    # and `check_a_plan_that_succeeds_shelves_itself`.
    #
    # **THOSE FIVE ARE NOT WRONG. THEY ARE THE OLD RULING, WRITTEN DOWN AND ENFORCED**, and
    # rewriting five standards at once to make a new mechanism pass is how a suite stops
    # meaning anything. The mechanism is BUILT, REACHED and PROVEN BY ITS OWN CHECK with the
    # flag on; migrating the five is a deliberate job with the reviewer, not a 9pm one.
    #
    # **AND THAT JOB WAS DONE IN THIS COMMENT'S OWN COMMIT (`88b3d19`), WHICH IS WHY THE
    # HEADING WAS STALE ON ARRIVAL RATHER THAN OVER TIME.** `test_m2.py` from the same diff:
    # FOUR of the five pass once the flag is set on the COPY instead of during the fixture's
    # warm-up, so their failures were THAT TRAJECTORY MOVING AND NOT THEIR CONTRACTS; only
    # `check_one_bargain` was a real conflict and it is MIGRATED. The fixture pins
    # `accumulate=False` to hold one policy still, declares the pin, and says in its own
    # words that **a green `m2` does not certify the accumulator** --
    # `check_the_accumulation_commits_where_the_bargain_refused` does, with the flag ON.
    #
    # So there is no gate defect here and this note exists to stop the next reader finding
    # one: a comment asserting the opposite of the line beneath it costs a full
    # investigation before it costs nothing. `A6i`'s writing side, inverted -- written from
    # the PROBLEM just solved rather than from the state the row now holds.
    accumulate: bool = True


@dataclass
class SlotResidual:
    slot: str
    channel: str
    predicted: Any
    actual: Any
    bits: float
    gone: bool = False      # the slot was bet on and is not listed after the act (perceive)

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


def _in_step(step: str):
    """The loop step a method runs in, held on the agent while it runs and restored after (a nested
    call, route -> mint, gets its own). A row written from inside it -- a choice made mid-step -- is
    labelled with the step actually running, never by fiat (the reviewer 2026-10-16 07:45; A1's rows
    were labelled PLAN wherever they ran and failed the gate's step-order check)."""
    def wrap(f):
        @wraps(f)
        def run(self, *a, **k):
            with self._step_scope(step):
                return f(self, *a, **k)
        return run
    return wrap


class Agent:
    _running_step = "PLAN"     # the step running now; _in_step and _step_scope set it

    @contextmanager
    def _step_scope(self, step: str):
        """_in_step for an inline phase of step() or an entry point: the step running for
        the block, restored after (the reviewer 2026-10-16 09:23)."""
        prev, self._running_step = self._running_step, step
        try:
            yield
        finally:
            self._running_step = prev

    def __init__(self, env: Any, gam: Gamma, cfg: Config | None = None,
                 led: Ledger | None = None) -> None:
        self.env, self.gamma = env, gam
        self._trace_pos = None            # `_prev_of`'s index of the trace by row
        self._window_info: dict = {}      # per slot, the window's offer for the mint in hand
        # `setdefault`, NEVER ASSIGNMENT: a loaded library carries its books across attempts
        # (`08bb416`) and zeroing them here would silently undo the persistence that makes a
        # dial earnable at all. A key the blob predates simply arrives at 0.
        for _k in BOOKS:
            self.gamma.book.setdefault(_k, 0)
        self.actions = tuple(env.actions())        # asked for, never imported
        # THE ACTION INTERFACE -- `docs/ACTION_INTERFACE_PLAN.md`, Isaiah 2026-09-28.
        # **THE ONLY LAYER THAT MAY KNOW A BUTTON EXISTS.** Today it AUDITS: every step
        # records what the action was observed to do, so the table is built from acting
        # and never closed over at construction -- which is `tether.py:2876`'s defect in
        # the toy `act` atom, where *the primitive it was given already knew*. The strip
        # that moves CHOOSING through it is step 2 and is not done.
        self.iface = IFace.Interface()
        self.iface.chooser = self._choose_known      # F480: the agent prices the known
        self._subject_n: collections.Counter = collections.Counter()   # A1: curiosity aimed
        self._probe_n: collections.Counter = collections.Counter()     # A1: starved probes
        self._obj_pick: dict = {}                                     # A1: this cycle's
        self._attempt_actions = 0     # actions since this level, or its last restart, began
        # the decay class: the situation (level, alive) and its epoch, set at the agent's own
        # boundaries (retarget, restarted) and handed to the interface; never read from a frame
        self._alive, self._epoch = True, 0
        # 7h: tries per (level, slot, operand); the root of this situation's chain, and the
        # last root's shown scene (for what was added or is gone)
        self._tried: collections.Counter = collections.Counter()
        self._root_id: str | None = None
        self._root_held: list = []
        self._root_shown: dict | None = None
        self._test: dict | None = None   # 7j: the goal exit's prediction, until the outcome
        # 7l: kinds asked here, kinds loaded from the lineage, episodes; what the lineage wrote
        self._kind_landed: set = set()
        self._kind_pairs: set = set()   # 7m: (kind_o, kind_x) of every landed or loaded entry
        self._kind_known: set = set()
        self._kind_episodes: list = []
        self._kinds_carried: set = set()
        self._kind_episode_mark = 0
        self._kind_cache: dict = {}
        self._mc3: list = []          # MC3: every ending, as the ground recorded it (append-only)
        self._invented: dict = {}     # M6: invented key -> its compiled condition (this run only)
        self._inv_lib = None          # M6: this agent's private library copy, made on first use
        self._inv_seen: dict = {}     # M6: slot -> history length last tried
        self._step_row0 = 0           # MC6: the ledger length when this step began
        self._muse_last = None        # MC6 N2: (targets, methods) last tested, and its cycle
        self._deg_prev = None         # the completion sweep: the world's degree last step
        self._sweep_from = (0, 0, set(), set())   # (seq, cycle, settled, owed) at segment start
        self._reach_hist: list = []   # build 2: (after-state, world reached?) per step, this level
        self._reach_epoch = 0
        self._goal_conds: dict = {}   # build 2: held goal conditions, key -> compiled (in-episode)
        self._goal_text: dict = {}    # build 2: key -> the condition's text
        self._goal_links: dict = {}   # build 3 L1: key -> (slot, want name) this link wrote
        self._want_scope: dict = {}   # b-0: slot -> the want name scored on its SUBJECT alone
        self._process_bets: list = []  # D1: open process bets, settled only at an ending (D3)
        self._run_actions = 0         # MC3: actions this run
        self._level_attempts = 1      # MC3: attempts at this level (1 + restarts)
        # SET HERE AND NOT ONLY IN `retarget`. `_advertised` reads it at the top of every
        # step; it only ever REACHED that read after the set had changed, so the attribute's
        # absence before the first `retarget` was masked by an early return. Feeding the
        # denominator unconditionally is what surfaced it.
        self._last_action: str | None = None
        # THE HOLD'S OWN DENOMINATOR, and it is ELIGIBLE OCCASIONS rather than cycles.
        # A share divided by cycles would count occasions the guard could never have
        # taken, and would read low for a reason that is not the hold.
        self._hold_eligible = 0
        self._priced = 0                     # candidates priced by `_cannot_pay`, ever
        self._memo: dict | None = None       # live only inside one `mint` -- see `mint`
        self._hold_withheld = 0
        # **AND THE KEY-LEVEL DENOMINATOR BESIDE IT, because the coin is flipped per
        # (cycle, slot) and NOT per occasion.** Several eligible occasions can share one
        # key and therefore one verdict, so the share over OCCASIONS is not the share the
        # coin is fair on -- measured 0.33 over occasions against ~0.5 over keys. Reporting
        # one without naming its unit is the denominator error this seat keeps making, so
        # both are carried and every reading states which it used.
        self._hold_keys: set = set()
        self._hold_keys_held: set = set()
        # AND THE SAME FOR THESE FOUR, ADDED 2026-09-21 AND ALL PUT IN `retarget` ONLY.
        # The comment above records this exact bug once already. A fresh Agent that is read
        # before its first `retarget` raises AttributeError -- which is how `_shape_cache` was
        # caught, by constructing an Agent directly in a measurement instead of through `play`.
        self._guard_exit: str | None = None
        self._gamma_read: dict = {}
        self._held_chains: set[str] = set()
        self._shape_cache: tuple = (-1, None)
        self._cue_tag_cache: tuple = (-1, {})
        self._contact_seen: set = set()
        self._refuted_slot: dict = {}
        # the slots whose loop turn is still ahead this cycle (F500); None outside the loop
        self._turn_ahead: set | None = None
        # an acted routine's next step, advanced once at its deciding cycle's end (F501)
        self._routine_next: tuple | None = None
        self._recovered_pending: list = []
        self._contact_pick = None
        self._s0_target: str | None = None
        self.alphabet = self._alphabets(env)
        self.slot_types = self._slot_types(env)
        self._kind_cache = {}   # 7l: kinds read fresh
        self.cfg = cfg if cfg is not None else Config()
        # not `led or ...`: an empty Ledger has len 0 and is therefore falsy
        self.led = led if led is not None else Ledger(mode=self.cfg.mode)
        # THE RUN HEADER: which arms this agent runs with, read from the live module values,
        # ONCE, before any step (the reviewer 2026-10-08 18:56Z; F424). Its own slot, so the
        # per-(cycle, slot) step order the gate checks cannot see it displace a PLAN row.
        self._set_seed(**_seed_at_birth())
        if len(self.led) == 0:
            arms = I.Attribution.arms()
            self.led.record(0, "PLAN", "@run", "arms", on=arms["on"], off=arms["off"],
                            modules=arms["modules"], not_loaded=arms["not_loaded"],
                            seed=self.seed, generation=self.generation,
                            seed_source=self.seed_source,
                            **I.Attribution.code(), **I.Attribution.run(env, gam))
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
        # **THE TERM, NOT ONLY ITS NAME -- 2026-09-25, AND THE NAME ALONE WAS A DANGLING
        # REFERENCE.** Only the contest WINNER is `gamma.accept`ed, so a want retained from
        # the does-not-pay branch names a term that is not in the library. Both readers
        # resolve `library.get(want)` and get `None`, and the fallback then does nothing
        # **silently** -- the exit recorded is `out_type-not-OBJ`, which describes the BOUND
        # term and is indistinguishable from a want that resolved and was the wrong type.
        # Measured on gridworld seed 11 at five objects: 2 of 2 wants absent from the library,
        # `_res` empty for all sixteen cycles, the gate reading NO HYPOTHESIS 48 of 48.
        #
        # **AND THE UNPAID TERM IS NOT ACCEPTED INTO GAMMA, WHICH IS THE WHOLE POINT.** A term
        # that lost the bargain has not earned a place in the library; retention is Isaiah's
        # ruling that *a want proves itself by RECURRING across attempts, not by explaining a
        # frame*, and a separate store is what keeps those two facts from collapsing.
        self._want_terms: dict[str, Term] = {}
        # WHICH of `_goal_split`'s exits fired, so the caller can CITE it rather than name
        # one. The refusal string is the only place a reader learns why no action was chosen,
        # and it was naming a single exit for all of them. **THREE NOW, NOT FIVE** -- the
        # ballot's four went with the ballot, 2026-09-28, and a count written here would be
        # stale the next time an exit moves.
        self._split_why: str | None = None
        self._gt_which: str | None = None   # which of _goal_target's None exits fired (F207)
        # THE INTENT THE GOAL EXIT ASKED FOR, kept so `_mint_routine` can plan in it rather
        # than in the button the interface returned. The plan's 16.
        self._goal_want: Any = None
        # WHERE THE INTERFACE AIMED A POSITIONED ACTION, or `None`. Set by the contact exits,
        # read once by `step`. The agent never chooses it and never reads it as a position.
        # **WHERE THE INTERFACE AIMED A POSITIONED ACTION THIS STEP, or `None`.** Set by
        # EVERY exit that consumes a `Realisation`, read once by `step`. Named `_s0_coord`
        # until 2026-09-28 and that name lied the moment `_explore` started aiming too --
        # `A6i` caught before it cost anything, because the field is minutes old.
        self._aimed: tuple[int, int] | None = None
        # **THE REALISED LANDING FOR THE CURRENT STEP -- the reviewer, 2026-10-04.** The
        # live sites had `_last_action` and no landing, so a bound `?ACTED_SELF` term was
        # judged with its guard FORCED OFF: as identity, predicting "no change" against a
        # colour that increments. It mispredicted and was refuted -- the term right, the
        # judge blind. Computed ONCE per step in `perceive` and read by every live caller
        # through `_eval_ctx`, because two sites computing it is how today's defect began.
        self._last_landed: str | None = None
        self._pred_by: dict[str, str | None] = {}
        # WHAT THE AGENT MEANT BY THIS STEP, for the bet row. `None` where the action was
        # handed in rather than asked for -- which is a reading, not a gap.
        self._intent_now: Any = None
        # **THE INTENT ALPHABET AS A MEASURED POPULATION, NOT A DERIVED CONSTANT.** The routine
        # price still uses the ACTION alphabet (see `_mint_routine`), which is now the wrong
        # one; this is the count that makes the size of that gap readable. Distinct intents
        # THIS AGENT HAS ACTUALLY FORMED -- a denominator from the run, never a space anybody
        # enumerated, because enumerating one and taking its `log2` is the flat pricing Isaiah
        # ruled against.
        # **BY KIND, NOT BY VERB-PLUS-OPERAND -- ISAIAH, 2026-09-29 (ruling 3):** *pricing
        # counts intents by KIND -- TOUCH is one kind, not one per object.*
        #
        # **AND THE RULING RESOLVES AN `A6i` I HAD RECORDED AND COULD NOT ACT ON.** This
        # stored `says()`, so `TOUCH o1` and `TOUCH o3` were two entries and a field named
        # KINDS grew with the OBJECT COUNT -- on a fifty-object board `TOUCH` alone would
        # contribute fifty. I filed it and deliberately did NOT rename, because which of
        # the two quantities was wanted is exactly what the pricing ruling decides.
        # **It decided KIND, so the name was right and the contents were wrong.**
        self._intent_kinds: set[str] = set()
        # slot -> (triple, {term: (rows covered, `wrong` over them)}). Always a PREFIX
        # tally, so an aborted walk is stored and resumed rather than discarded.
        #
        # NESTED PER SLOT SO EVICTION IS A `clear()` AND NOT A SCAN. Measured at 25 cycles:
        # 1,077,893 entries / 188 MiB, and **78.7% of it stale with 100% of the staleness
        # from `held` moving** -- a rebind leaves every entry for that slot unreachable,
        # since they are reusable only if the slot returns to exactly that binding.
        self._tally: dict = {}
        self._trace_epoch = 0
        # (ctx, intent, slot, the discrepancy it was met at) -> times that pair undid it.
        # ISAIAH, 2026-09-29: a goal met then un-met is "data similar to actions becoming
        # available and not available -- it's a hint or indicator". The COUNT is what makes it
        # testable rather than anecdotal, against `MIN_REPEAT` like every other repeat claim.
        self._undone: dict = {}
        # **AND THE SAME PAIR POOLED ACROSS CONTEXTS -- A HINT, NEVER THE CLAIM.** The reviewer,
        # 2026-09-29, from last night's actor key, which split the evidence so finely that
        # nothing reached the bar. The per-context count is what `MIN_REPEAT` is tested against
        # because *repeating in the same situation* is Isaiah's test; this one exists so the
        # agent can pick WHAT TO TRY when no single situation has enough behind it yet.
        self._undone_across: dict = {}
        self._acts: Counter = Counter()   # System-0 instrument: concrete actions taken per cycle
        # the whole before-state is kept, because an operand is another slot's past value
        self.trace: list[tuple[dict[str, int], str, dict[str, int]]] = []
        self._shown_key, self._shown, self._frame_at = None, {}, {}
        self.owed_import: set[str] = set()
        # THIS CYCLE's appearance and disappearance events -- see `_present`. Empty is the
        # normal reading, not a missing one: most cycles change no slots.
        self._came: tuple[str, ...] = ()
        self._gone: tuple[str, ...] = ()
        # THE TERM'S OWN OUTPUT, before the alphabet's modulo. The row writes this beside the
        # observation so both sides are in one form; a residue beside a raw value read a correct
        # bet as a miss twice on 2026-10-07 (the reviewer 23:30Z, Fig 13).
        self._pred_raw: dict[str, int] = {}
        # WHAT THE LIBRARY NAMED FOR EACH SLOT'S LAST RESIDUAL: partner reading -> molecules
        # relating it to the target. Read by `_bindings` as an ORDER, never a filter.
        self._named: dict[str, dict[str, list]] = {}
        self._bind_key: dict = {}          # A1 sites 7-8: per slot, (draw key, its readings)
        self._lib_offers: dict[str, list] = {}   # M4: what the library offers each slot's mint
        self._reach_index: dict = {}       # M4: distinct compiled terms per description
        self._reach_verdicts: dict = {}    # M4: a CAUSE pair's verdict per trace length
        self._compile_cache: dict = {}     # M4: compile_term is pure in the condition
        self._bound_cache: dict = {}       # the hold's bound answers, (sig, entry, role, o, x)
        self._bound_slot_cache: dict = {}  # S1: the same, filtered to one slot (+ slot in the key)
        self._bound_slot_idx: dict = {}    # S1b: the held indices of those rows
        self._pair_tally: dict = {}        # SPEED-2: as _PAIR_TALLY, per Agent
        self._named_split: dict = {}       # SPEED-2 (c): a named compile split once per pair
        self._pairs_seen: set = set()      # S1c: as _PAIRS_SEEN, for an Agent with its own memo
        self._bound_slot_map: dict = {}    # S1c: as _BOUND_SLOT_MAP, likewise
        self._atoms_token = shared_token(self.gamma.atoms)   # None: this Agent's own memo
        self._view_hold: dict = {}         # 7e: (entry, role) -> the view under "{o}"/"{x}"
        self._view_hold_n: Counter = Counter()   # 7e: held/served/bypass_<why>; nothing reads it
        self._blocked_now: dict = {}       # B4: this step's blocked slots -> the partner
        self._reach_frames: tuple | None = None
        self.abstained: dict[str, dict] = {}
        self.candidates: dict[str, int] = {}     # term -> cycle accepted, awaiting the ground
        # WHERE THE EVIDENCE CAME FROM. Isaiah 2026-09-30: candidates survive a level change,
        # but *"it needs to have similar conditions"* -- so a carried candidate is DORMANT
        # until the level it was learned on comes round again in substance. Kept BESIDE
        # `candidates` rather than folded into it: the cycle is WHEN and the level is WHERE,
        # and `A6i` is what happens when two quantities share one name.
        self._cand_level: dict[str, int] = {}    # term -> the level its candidacy is live on
        # `settled` IS A PROPERTY NOW -- see below. There is no set here to drift.
        self._settled_at_level: set[str] = set()   # the segment's starting line
        self._settled_lvl: set[str] = set()        # what settled in THIS level (P2's hold)
        self._signals: list[tuple] = []    # MC2: this level's open signals (seq, slot, term)
        # CARRY (item 3): the ledger length at the level's start (CARRIED = entered before it), and
        # each credited binding + its fate (3(b))
        self._seq_at_level = 0
        self._carry_log: dict[tuple[str, str], dict] = {}
        self.demoted: list[str] = []
        self.chain = I.Chain()
        self.rank = I.Rank()
        self.gamma.unit_rank = self.rank.key
        self.phases = I.Phases()
        self.clocks = I.Clocks()
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
        # THE `sep` SHAPE PER CALL, NOT A TOTAL. `passed_per_call` says how many members
        # contributed and cannot say whether they AGREED -- four passing and all marking the
        # same action is unanimity, four marking four is total disagreement, and both read
        # `{4: n}`. Sorted descending so the shape is comparable across boards with different
        # action counts: `(4,0,0,0)` unanimous, `(1,1,1,1)` no separation, `(2,2,0,0)` split.
        #
        # A TRAJECTORY RATHER THAN A COUNTER, because the tie fraction MOVES: 100% ties at ten
        # cycles against 15.5% at 150, so a total describes the end of an episode and hides
        # that early ties are universal -- which is when the agent is choosing what to explore.
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
        # **WHAT THE ROUTINE ACTUALLY EMITTED, WHICH NOTHING COUNTED -- 2026-09-25.**
        # `REACH_STATUS` has carried `tested_yes`/`tested_no` since it was written and they
        # have ZERO PRODUCERS: `reach_status` may only read the SHAPE, and its docstring says
        # so -- *a caller that has watched the routine run may upgrade; nothing here may.*
        # This is the caller doing the watching. An ending alone cannot say it: `DONE` with no
        # action emitted is a routine that finished before it started.
        self._routine_acts = 0
        self._reach_tested: dict = {}
        # **THE PLAN AS COMPOSED, BECAUSE `advance` HANDS BACK A REMAINDER -- 2026-09-25.**
        # `advance(until(g/3))` returns `until(g/2)`: a DIFFERENT object with the budget spent
        # down. The shelf stored whatever `self.routine` held at the ending, so a plan that
        # took any steps before succeeding SHELVED ITS TAIL rather than the behaviour that was
        # composed. Invisible until now because the only success the suite had ever seen ended
        # on advance number one, where the remainder and the original coincide.
        self._routine_adopted = None
        self._plan_no = 0                      # adoptions so far: a plan's id in the record (F504)
        # **HOW OFTEN A WANT HAS COME BACK -- ISAIAH'S OWN CRITERION, PREVIOUSLY UNRECORDED.**
        # *A want proves itself by RECURRING across attempts, not by explaining a frame.* The
        # retention site ranked by COST alone and its comment said so, naming `_note_want` as
        # the thing that would supply standing -- a function with zero definitions. This is
        # the record it needed: how many separate attempts have wanted this composition.
        #
        # KEYED BY THE TERM'S NAME, WHICH IS THE COMPOSITION. Recurrence *under a RESEMBLING
        # shape* is the stronger form Isaiah stated and it is NOT BUILT: it needs an
        # equivalence over terms that this codebase does not have -- `resembling` is over gap
        # Characterisations, not over terms. Same composition is the narrow, checkable case,
        # and calling it the whole criterion would be the overstatement the comment made.
        self._want_seen: dict[str, int] = {}
        # slot -> (scope key, {(stream, chain): its lean increments}, novelty, verdict)
        self._frontiers: dict[str, tuple] = {}
        # WHEN THE AGENT LAST COMMITTED TO A PLAN. The threshold falls with the gap since --
        # *the agent is always paying with its time*, so a cycle that ends without a
        # commitment makes the next commitment cheaper. Starts at 0, so an agent that has
        # never committed is already under time pressure at cycle 0, which is correct: it has
        # spent its whole life not acting.
        self._last_commit = 0
        # ADD-ONLY: (total committed at, ended tested_yes, cycle it ended) per OVERRIDE; and the
        # cycle of every commitment. The commitment bar and the relief rate are read from these.
        self._overrides: list[tuple[float, bool, int]] = []
        self._override_open: float | None = None
        self._commit_cycles: list[int] = []
        # **THE EPISODE RECORD -- ISAIAH'S FOUR QUESTIONS, 2026-09-25.** *"Given the current
        # scenario or state of the board, HAS THIS BEEN EXPERIENCED IN A PREVIOUSLY RECORDED
        # PATTERN, WHAT ACTIONS DID I TAKE, WHAT OUTCOMES OCCURRED, WERE THEY FAVORABLE."*
        #
        #     1 have I been here before  -> the SITUATION SIGNATURE   `_gap_key`
        #     2 what did I do            -> the ACTIONS               `Rt.actions`
        #     3 what happened            -> the ENDING                done/exhausted/blocked
        #     4 was it favourable        -> the VERDICT               tested_yes / tested_no
        #
        # **KEYED ON `_gap_key` AND THAT IS WHAT MAKES IT TRANSFER.** *"It's MORE THAN JUST
        # EPISODIC -- don't forget TRANSFER. You play with blocks to learn other things."* A
        # fingerprint of the state only ever matches itself; `_gap_key` holds arity, the TYPES
        # that varied and the RELATION TYPES, with no slot names, so it asks *have I been in a
        # situation SHAPED LIKE THIS* rather than *on this board*.
        self._episodes: dict[tuple, list[tuple[tuple, str, str]]] = {}
        self._plan_sig: tuple | None = None    # the signature THIS plan was formed against
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
        # HELD at a death's boundary, for `restarted` to carry back where identity is sure (F479).
        self._held_refutations: tuple[dict, dict] | None = None
        # (b'-l) every boundary's cleared stores, instance form, in order; nothing is removed
        self._dormant: list[dict] = []
        self._attempt_cycle = 0
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
        # (gap shape, steps, guards) -> the scopes a plan of that shape was refused under. ADD-ONLY:
        # a refusal never leaves the record (Fig 6); it stops excluding when the scope grows.
        self._refusals: dict[tuple, list[tuple]] = {}
        # NOT-t, THE REFUSING TERM (F496; Figs 5, 6, 12, 13): (term name, gap shape) -> the scopes
        # it was refused under. ADD-ONLY and kept OUTSIDE the library, so minting a refusal does
        # not grow the scope that lifts it. The decaying tally in `Standing` stays the evidence.
        self._not: dict[tuple, list[tuple]] = {}
        self._digests: dict[str, frozenset] = {}
        self.agency = I.Agency()       # §16.8 sensor 3, a per-step read
        # B: (slot -> (action, ctx) -> signs seen). Agency's lifetime, never the trace's: the
        # trace clears at retarget, these do not, so the two movability readings cover one history.
        self._dir: dict = {}
        self._dir_scope_noted = False
        self.term = I.Termination()    # 2d / §20.1, latching and asymmetric
        self._vetoes: set[tuple] = set()       # 7a(5) B: (fingerprint, action, coordinate)
        self._ruin_step: tuple | None = None   # this step's (fp, of, action, coord, cycle)
        self._ending_counted: str | None = None  # the word counted with no step since
        self._step_fp: tuple[str, str] | None = None    # this step's board, read once
        self._step_before: dict | None = None           # the state that reading was taken of
        self._withheld = IFace.NO_WITHHELD               # 7a(5) C: set for choose() only
        self._split_term: dict | None = None    # 5b: the term the RETURNED goal split read
        self._routine_fed: list = []            # 5b: the routine exit's entries, this step
        self._plan_seqs: dict[int, int] = {}    # 5b: plan_no -> the seq of its mint row
        self._fed_rows: dict[str, list] = {}    # 5b: term -> (REPEAT seq, role) naming it
        self._parts: dict[str, dict] = {}       # D5: slot -> {P, A (incumbent), B, ...}
        self._d5_pending: dict[str, tuple] = {}  # D5: slot -> (P, numbers), split next step
        self._d5_candidates: dict[str, tuple] = {}  # D5: slot -> a cut awaiting its witness
        self._row_filter: dict = {}             # D5: slot -> the rows part B's search sees
        self._mint_part: dict | None = None     # D5: the part a running mint searches for
        self._shadow: dict[str, int | None] = {}  # D5: the incumbent's shadow on a not-P step
        self._d5_rows: dict[str, list] = {}     # D5: slot -> (trace row, predictor), this level
        self._d5_said: set = set()              # D5: (slot, term) whose not-split was recorded
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
        # THE LAST CUE READING -- what mutated and which primitives are lit. `None` until a
        # world that publishes `cues()` has been read once; a world without the observer
        # leaves it None forever, which is the honest state and not a failure.
        self.cue: dict | None = None
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

    def _boundary_key(self, slot: str) -> tuple[int, str, dict]:
        """(cycle, slot, extra fields) for a boundary row: its own chain at the real cycle with the
        level as a field, or -- _BOUNDARY_CHAIN False, the must-fail -- the old @loop keying."""
        if _BOUNDARY_CHAIN:
            return self.cycle, slot, {"level": self.level}
        return self.level, "@loop", {}

    def end_run(self, how: str = "cap") -> None:
        """The run ends with this level still open: its signals resolve at the GAME (MC2). The loops
        call it after their last step; `retarget` never sees a cap or a timeout."""
        self._intent_verdict(how)
        self._note_ending(how, "run")
        self._resolve_signals("game", how)
        if _D13:
            self._settle_process("game", how)
        if self._goal_conds:
            self._close_goals(how)

    def _fingerprint(self, before: dict) -> tuple[str, str]:
        """7a(5) B: the BOARD where the world gives one, else observe() (the whole state there).
        The interface's reading, so the floor's key and the withhold's check are one."""
        return IFace.fingerprint(self.env, before)

    @_in_step("IMPORT")
    def _mc3_note(self, how: str, scope: str) -> None:
        """MC3: the GROUND's record of an ending -- its word, its kind, whether the level was
        cleared, the actions this level and this run, the attempts -- appended, never edited
        (Fig 2, "The anchor must not update"). Nothing the frame produces (bets, mints) enters it
        (Fig 1 :27). The same word again with no action between is that same ending."""
        last = self._mc3[-1] if self._mc3 else None
        if last and last["how"] == how and last["actions_this_run"] == self._run_actions:
            return
        # CLEARED ONLY ON A CLEARING WORD (the reviewer 22:47Z): a reset is not a clear, and an
        # unknown word is recorded as itself, never defaulted to cleared (Fig 1 :27).
        cleared = how in (WIN, ADVANCE)
        entry = {"how": how, "kind": "cleared" if cleared else _TERM_KIND.get(how, how),
                 "cleared": cleared,
                 "level": self.level, "actions_this_level": self._attempt_actions,
                 "actions_this_run": self._run_actions, "attempts": self._level_attempts,
                 # WHICH BUDGET AN ENDING RAN OUT (the reviewer 23:18Z), read from what followed
                 # it, never from a cap: a new level (retarget) is "level", the run's end "run"
                 "scope": scope}
        self._mc3.append(entry)
        _c, _s, _lv = self._boundary_key("@boundary")
        self.led.record(_c, "IMPORT", _s, "ground_record", **_lv, **{
            k: v for k, v in entry.items() if k != "level"})

    def _mc4(self, cand: Any) -> dict:
        """MC4: a plan's need read against what MC3 recorded, each kept apart, never combined.
        The budget is learned by running out ("the agent discovers its budget by running out"; a
        cap the world holds is never read), AT ITS OWN SCOPE (the reviewer 23:18Z): a cap ending
        followed by a new level gives reserve_level_seen, read against this level's actions; one
        that ended the run gives reserve_run_seen, read against this run's. level_cost_seen is
        what cleared levels cost: context, not a reserve. With no such ending, "no record"."""
        lv = [e["actions_this_level"] for e in self._mc3 if e["kind"] == "cap"
              and e["scope"] == "level"]
        run = [e["actions_this_run"] for e in self._mc3 if e["kind"] == "cap"
               and e["scope"] == "run"]
        cleared = [e["actions_this_level"] for e in self._mc3 if e["cleared"]]
        return {"need": _confirm_actions(cand),
                "reserve_level_seen": ([c - self._attempt_actions for c in lv] if lv
                                       else "no record"),
                "reserve_run_seen": ([c - self._run_actions for c in run] if run
                                     else "no record"),
                "level_cost_seen": ([min(cleared), max(cleared)] if cleared else "no record")}

    @_in_step("IMPORT")
    def _note_ending(self, how: str, scope: str) -> None:
        """7a(5) A + B: one ending reaches Termination once -- the SAME word again with no step
        between (a WIN retargeted, then ended by the loop) is that ending, another word is another
        (a death, then the deadline) -- and a death adds its veto. Record only."""
        if _MC34:
            self._mc3_note(how, scope)
        if not _RUIN_RECORD or self._ending_counted == how:
            return
        self._ending_counted = how
        _c, _s, _lv = self._boundary_key("@boundary")
        was = self.term.klass()
        self.term.ending(_TERM_KIND.get(how, how))
        if self.term.klass() != was:
            self.led.record(_c, "IMPORT", _s, "termination", **_lv, how=how, was=was,
                            **self.term.report())
        if how != "death":
            return
        if self._ruin_step is None:
            self.led.record(_c, "IMPORT", _s, "veto", **_lv, killing_step=None,
                            reads="a death with no action taken this step: nothing to veto")
            return
        fp, of, act, coord, cyc = self._ruin_step
        key = (fp, act, coord)
        new = key not in self._vetoes
        self._vetoes.add(key)
        self.led.record(_c, "IMPORT", _s, "veto", **_lv, fingerprint=fp, fingerprint_of=of,
                        action=act, coord=list(coord) if coord is not None else None,
                        at_cycle=cyc, new=new, vetoes=len(self._vetoes))

    @_in_step("SETTLE")
    def _resolve_signals(self, kind: str, how: str) -> None:
        """MC2: exactly one resolution row per open signal, pointing at its bet row, never editing
        it (Fig 6). `kind` is an order (bet < level < game, Fig 13), never a weight; nothing is
        summed (Fig 1). `fed` points at the REPEAT rows after the bet whose `gamma_read["fed"]`
        names the bet's term (5b, TETHER_CONTACT); without that arm no row records it, so it is
        None and says so (Fig 10)."""
        for seq, slot, term in self._signals:
            # cycle = THE CYCLE, the level in its own field: a level number in the cycle field is
            # the @loop defect (the reviewer 08:11Z), and a new row kind must not inherit it.
            # [seq, role]: a goal and a route are two currencies, kept apart (Fig 12 :125/:130)
            fed = (sorted([x, r] for x, r in self._fed_rows.get(term, ()) if x > seq) if _FED
                   else None)
            self.led.record(self.cycle, "SETTLE", "@signal", "resolution", signal_seq=seq,
                            signal_slot=slot, level=self.level, kind=kind, how=how, fed=fed,
                            reads=("[REPEAT seq, role] after the bet whose fed names its term"
                                   if _FED else
                                   "no row in this code names the term an action was chosen "
                                   "through: choose() picks the action before the utterance "
                                   "names the bound term"))
        self._signals = []

    @_in_step("IMPORT")
    def retarget(self, env: Any, level: int, how: str = ADVANCE) -> None:
        """Move to the next level. Gamma and standing carry; the trace and the bindings
        do not, because slot names mean nothing across a boundary.

        Everything still owed is parked WITH its history, which is the only way a term
        minted three levels later can be tested against it -- the mint will never revisit
        it, so this is the sweep's one irreplaceable job."""
        self._intent_verdict(how)
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
        _c, _s, _lv = self._boundary_key("@boundary")
        self.led.record(_c, "IMPORT", _s, "boundary", **_lv,
                        env_dropped=drop is not None,
                        reads=("per-episode bindings the WORLD holds -- a colour identity is "
                               "valid only for the episode it was read in, so it drops where "
                               "`bound` and `trace` drop"))
        self.led.record(_c, "IMPORT", _s, "ending", **_lv, how=how, to_level=level,
                        reads=ENDING_READS.get(how, "unnamed ending"),
                        consumed_by="nothing yet -- boundary demotion is a separate item")
        self._note_ending(how, "level")
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
        if how in (ADVANCE, WIN):
            _cc, _cs, _clv = self._boundary_key("@credit")
            with self._step_scope("SETTLE"):
                self.led.record(_cc, "SETTLE", _cs, "credit", **_clv,
                                settled_here=sorted(self.settled - self._settled_at_level),
                                bound_here=sorted(set(self.bound.values())),
                                over_steps=len(self.trace), how=how,
                                note="the segment is credited, not the last action",
                                decay_half="boundary demotion, its own item -- credit without "
                                           "decay is the incumbency pathology (§21.4)")
        self._resolve_signals("level", how)
        if _D13:
            self._settle_process("level", how)
        if self._goal_conds:
            self._close_goals(how)
        self._settled_at_level = set(self.settled)
        self._settled_lvl = set()
        self._seq_at_level = len(self.led)
        self._touch_cache = None      # a new world invalidates owners and contact alike
        self._peer_cache = None
        self._decomp_cache = None
        self._frame_cache = {}
        self.env, self.level = env, level
        self.slots = env.slots()
        self.actions = tuple(env.actions())       # a new level may advertise differently
        self.alphabet = self._alphabets(env)      # a new level may value slots differently
        self.slot_types = self._slot_types(env)   # and may type them differently
        self._kind_cache = {}   # 7l: kinds read fresh
        if _D5:
            self._d5_level_end()
        if _LINEAGE_HOLD:
            self._hold_lineage(how)
        self.bound, self.trace = {}, []
        self._parts, self._d5_pending, self._shadow = {}, {}, {}
        self._d5_candidates = {}
        self._d5_rows, self._d5_said = {}, set()   # D5's scope is the level, a world event
        self._attempt_actions = 0
        # a death is a boundary into a dead situation; any other ending into a live one
        self._alive, self._epoch = how != "death", self._epoch + 1
        self.iface.situate(self._epoch, self._alive)
        if _MC34:
            self._level_attempts = 1
        self._trace_epoch += 1          # the tallies summarise a history that is gone
        self._tally.clear()             # (the epoch is in the triple; this is belt and braces)
        self._disc, self._res = {}, {}   # the slots did not survive, nor do their trends
        # NOR WHAT WAS KEYED BY THEM, by this block's own rule: a want, a tested reach, a gap's
        # last reading or step, an undone count, each read on the next level's same NAME.
        self.wants, self._want_terms, self._reach_tested = {}, {}, {}
        self._prev_gap, self._gap_delta, self._undone, self._undone_across = {}, {}, {}, {}
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
        # EXCEPT AT A DEATH, WHICH MAY BE FOLLOWED BY A RESTART OF THE SAME LEVEL -- the same
        # objects under the same names (measured, F479). Held, not lost; `restarted` decides.
        self._held_refutations = ((self.refuted, self.refuted_at) if how == "death" else None)
        self.refuted, self.refuted_at = {}, {}
        # AND `self.paths` IS A THIRD CASE AND STAYS, FOR THE REASON THIS BLOCK JUST GAVE.
        # The autoimmunity argument above is entirely about SLOT NAMES regenerating. `_gap_key`
        # holds none -- arity, the TYPES that varied, the target's TYPE, the relation types --
        # so the evidence it carries is about a KIND of situation and not about `o1.dcol`.
        # **Clearing it would be the mirror error**: discarding evidence that does cross, on a
        # rule written for evidence that does not. `retrieval.key_of`'s own note is the same
        # ruling one level down -- *vocabulary permanent, instances transient.*
        self._last_action: str | None = None   # what may have changed the gating
        self.owed_import, self.abstained = set(), {}
        self._guard_exit: str | None = None   # why the last guard read was unreadable
        self._gamma_read: dict = {}   # did action selection consult Gamma this cycle
        self._held_chains: set[str] = set()   # recipes in the library, per mint call
        self._shape_cache: tuple = (-1, None)   # (cycle, decoder) -- Ctx is built per candidate
        self._cue_tag_cache: tuple = (-1, {})   # (cycle, tags) -- mint asks per stream
        # SYSTEM 0's contact memory is NOT cleared here. The keys are (kind, shape, shape)
        # -- a KIND of situation, which is what `paths` survives a boundary
        # for. Clearing it would discard evidence that DOES cross, on a rule written for
        # evidence that does not.
        self._contact_pick = None
        self._s0_target = None
        # CLEARED AT RETARGET, unlike `_contact_seen`: this one is keyed by
        # SLOT NAME, and the slots do not survive a level boundary. Same rule the boundary
        # reset states for `_res` and `_disc`.
        self._refuted_slot: dict = {}
        # THE MOVE MAP SURVIVES A BOUNDARY for `_contact_seen`'s reason: what an action does
        # to the avatar is a fact about the ACTION, not about the slot names of one level.
        #
        # **AND `candidates` SURVIVES IT TOO, SINCE 2026-09-30. This read `self.candidates = {}`**
        # -- Isaiah ruled that rules awaiting the ground are not wiped by a level change, the
        # same shape as his routine ruling: a candidate is a behaviour-in-waiting, not a
        # binding. The clear also sat under the comment ABOVE it, which is about the move map
        # and not about this line, which is how it went unexamined.
        #
        # **DORMANT, NOT LIVE, AND THE TWO RULINGS ARE ONE COMMIT BECAUSE THE SECOND IS WHAT
        # MAKES THE FIRST SAFE.** `_cand_level` still points at the OLD level, and `settle`
        # requires the stamp to match, so a survivor cannot settle here on evidence it never
        # saw here. It wakes when it is bound on this level and then pays like anything else.
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
        return frozenset(self.step_effect(b, a) for b, _act, a, _intent, _landed in self.trace)

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

    def history(self, slot: str) -> list[tuple[dict[str, int], str, int, Any, Any]]:
        """(before-state, action, this slot's after-value, intent, landed-on) per step.

        **THE ANNOTATION SAID THREE AND THE RETURN HAS BEEN FIVE since `intent` and
        `landed` were added -- and the paragraph below already said so, so this
        docstring contradicted itself.** Corrected 2026-10-04, found because
        `bears_on` stopped unpacking with `*_`: a permissive unpack let every reader
        disagree about the shape without anything failing.

        Frames before the slot existed are skipped rather than faulted: a slot that
        arrived mid-episode has no history from before it arrived. BOTH ENDPOINTS are
        required, not just the after-value -- the ARRIVAL frame has the slot in `after`
        and not in `before`, so it is not a transition observation and a term applied to
        it would fault on the missing before-value."""
        # **AND THE INTENT RIDES WITH IT.** A guard is tested inside `Term.apply`, which
        # runs over THESE rows during replay -- so a guard keyed on an intent is
        # unevaluable unless the row carries the intent that produced it.
        rows = [(b, a, af[slot], i, land) for b, a, af, i, land in self.trace
                if slot in af and slot in b]
        keep = self._row_filter.get(slot)       # D5: part B's search prices its own rows only
        return [r for r in rows if keep(r)] if keep is not None else rows

    def _lookup(self, slot: str, hist: list) -> None:
        """FIG 9's ONE LOOKUP INTO THE LIBRARY, keyed by this residual (the reviewer 2026-10-07
        22:48Z, 22:53Z, 23:00Z). The description is `characterise`'s own, SCOPED to the target's
        object whatever the retrieval arm, because board-wide it fires on every type and lights
        everything (F303). Recorded, never adopted: the pairs the bond tests hold are offered to
        the ground, and nothing here binds, mints or bets."""
        own = self.env.slot_owner() if hasattr(self.env, "slot_owner") else {}
        mine = own.get(slot)
        if mine is None:
            return
        scope = {s for s, o in own.items() if o == mine}
        gap = retrieval.characterise(hist, slot, list(self.alphabet), self.slot_types, scope=scope)
        described = {s: self.slot_types[s] for s in (slot, *gap["varies"]) if s in self.slot_types}
        found = composer.lookup(described)
        read = composer.read_pairs(found["pairs"], [b for b, _act, _val, _intent, _landed in hist])
        held = [{k: r[k] for k in ("molecule", "left", "right", "left_reading", "right_reading",
                                   "held", "via", "occasions")} for r in read if r["held"]]
        named: dict[str, list] = {}
        for p in found["pairs"]:
            ends = (p["left_reading"], p["right_reading"])
            if slot in ends:
                other = ends[1] if ends[0] == slot else ends[0]
                if p["molecule"] not in named.setdefault(other, []):
                    named[other].append(p["molecule"])
        self._named[slot] = named
        self.led.record(self.cycle, "ROUTE", slot, "lookup", query=found["query"],
                        described=sorted(described), junctions=found["junctions"],
                        offered=len(found["pairs"]), held=held, named=sorted(named),
                        reads=("the library looked up by this residual's own description; "
                               "pairs offered, bonds read over its frames, nothing adopted"))
        self._library_reach(slot, mine, own, described)

    def _library_reach(self, slot: str, mine: str, own: dict, described: dict) -> None:
        """M4 (METAPROGRAMMING_DESIGN section 4; the reviewer 2026-10-09 07:14Z, 07:23Z). The
        library lit by THIS residual's description -- the slot and what varied with it, as
        readings -- and every view and CAUSE then-side that compiles onto this slot, recorded. A
        CAUSE is tested where bonds are tested; an offer is kept for the mint only if it holds
        now, is not held already, and passes the ~1 gate. Nothing lit, nothing written."""
        self._lib_offers[slot] = []
        lib = _library()
        att = getattr(self.env, "attribute_of", None)
        att = att() if att else {}
        known = compile_term.readings()
        changed: dict = {}
        for s_ in described:
            a = att.get(s_)
            if a in known:
                changed[a] = 1
            changed.update({r: 1 for r, base in compile_term.CHANGE_OF.items() if base == a})
        lit = lib.light(changed) if changed and lib is not None else []
        _extra: set = set()
        if _LIBRARY_ABDUCE and changed and lib is not None:
            _fwd = {k for k, _w in lit}
            lit = lib.light(changed, abduce="after")
            _extra = {k for k, _w in lit} - _fwd
        blk = self._blocked_now.get(slot) if _RELATION_SET and lib is not None else None
        if blk is not None:
            # B4's consumer (the reviewer 12:49 CDT): the stall described as an effect -- blocked
            # by a partner -- cues the settled S7 entries first. An order, never a cut.
            top = lit[0][1] if lit else 1.0
            lit = [(k, top) for k in S7_SOLIDITY] + [e for e in lit if e[0] not in S7_SOLIDITY]
            self.led.record(self.cycle, "ROUTE", slot, "blocked_cue", partners=list(blk),
                            keys=list(S7_SOLIDITY),
                            reads="blocked by a partner: the lookup tries solidity first")
        if not lit:
            return
        if _RELATION_SET:
            # C (c): a lit entry from the settled table says so -- provenance, nothing priced
            inh = sorted(k for k, _w in lit if k in relations.SETTLED)
            if inh:
                self.led.record(self.cycle, "ROUTE", slot, "inherited_lit", entries=inh,
                                settled_by=relations.SETTLED_BY,
                                reads="settled core knowledge lit by this residual")
        rep_slot: dict = {}
        for s_, o_ in sorted(own.items()):
            rep_slot.setdefault(o_, s_)
        touching = set(self._touching(slot))
        others = tuple(sorted((o_ for o_ in rep_slot if o_ != mine),
                              key=lambda o_: (o_ not in touching, o_)))
        # THE LIBRARY REPEATS ITSELF: hundreds of lit entries unfold into tens of thousands of
        # candidates over a few templates, so the DISTINCT compiled terms are indexed once per
        # (description, objects) and every entry that offered one is kept as its provenance.
        ikey = (frozenset(changed), slot, mine, others, blk)
        index = self._reach_index.get(ikey)
        if index is None:
            index = self._reach_index[ikey] = self._index_reach(lib, lit, slot, mine, others)
        views, causes, refused = index
        if _LIBRARY_ABDUCE:
            # 7d's row: what the reverse lookup added -- entries lit only by it, the distinct
            # terms they were first to offer, and the terms routed through an event (via)
            _new = (sum(1 for _c, p in views.values() if p["library"] in _extra)
                    + sum(1 for *_x, p in causes.values() if p["library"] in _extra))
            self.led.record(self.cycle, self._running_step, slot, "abduce",
                            lit=len(lit) - len(_extra), extra=len(_extra), new=_new,
                            routed=sum(1 for _c, p in views.values() if p.get("via"))
                            + sum(1 for *_x, p in causes.values() if p.get("via")),
                            refused=sum(refused.values()))
        if self._reach_frames is None or self._reach_frames[0] != self._trace_epoch \
                or self._reach_frames[1] != len(self.trace):
            self._reach_frames = (self._trace_epoch, len(self.trace), reach.frames(
                self.trace, lambda st: {o_: self._record(s_, st) for o_, s_ in rep_slot.items()}))
        frs = self._reach_frames[2]
        units = self._units_for(slot)
        offers, rows = [], []
        for c, prov in views.values():
            offers.append(self._lib_offer(c, prov))
        for if_c, then_c, prov in causes.values():
            vkey = (if_c.term.name, if_c.slot, then_c.term.name, then_c.slot,
                    self._trace_epoch, len(frs))
            v = self._reach_verdicts.get(vkey)
            if v is None:
                v = self._reach_verdicts[vkey] = reach.cause(if_c, then_c, frs)
            prov = {**prov, "if": if_c.term.name, "guard_bits": reach.bits(
                if_c, lambda t: term_bits(self.gamma.length(t, units), self.gamma.alphabet))}
            off = self._lib_offer(then_c, prov, v)
            offers.append(off)
            if v["supported"]:
                rows.append({**prov, "then": then_c.term.name, **v,
                             "offered": off["offered"], "why": off["why"]})
        self._lib_offers[slot] = [o_ for o_ in offers if o_["offered"]]
        self.led.record(self.cycle, "ROUTE", slot, "library", changed=sorted(changed),
                        lit=len(lit), views=len(views), causes=len(causes),
                        supported=rows, offered=len(self._lib_offers[slot]),
                        withheld=dict(Counter(o_["why"] for o_ in offers if not o_["offered"])),
                        refused=dict(refused),
                        reads=("the library lit by this residual's description; the distinct views "
                               "and CAUSE then-sides that compile onto this slot, tested and "
                               "recorded, each with the count of entries that offered it"))

    def _index_reach(self, lib: Any, lit: list, slot: str, mine: str, others: tuple) -> tuple:
        """The distinct compiled views and CAUSE pairs that land on `slot`, each with its first
        entry and the count of entries offering it; refusals counted by reason. Compiled once
        per condition (the compiler is a pure function of the condition and the atoms)."""
        atoms = {a.name: a for a in self.gamma.atoms}

        def comp(cond: str, subject: str | None = None) -> Any:
            # 7d: a frame event compiles on its subject, so only its key carries the subject;
            # OFF passes none, so came is refused as before the arm
            if not _LIBRARY_ABDUCE or not cond.startswith("frame."):
                subject = None
            k = cond if subject is None else (cond, subject)
            got = self._compile_cache.get(k)
            if got is None:
                got = self._compile_cache[k] = compile_term.compile_candidate(
                    {"condition": cond}, atoms, subject=subject)
            return got
        views: dict = {}
        causes: dict = {}
        refused: Counter = Counter()
        tally = refused if _SPEED2_COUNT else None
        partner = others[0] if others else mine
        sig = compile_term.signature(atoms) if _INDEX_HOLD else None
        for key, _w in lit:
            for role in reach.SINGLE:
                _landed = 0   # 7l G1: what this (entry, role) put on the slot
                for cand, c, _ in self._compiled(lib, key, role, mine, partner, comp, atoms, sig,
                                                 slot=slot, tally=tally):
                    if c is None:
                        refused[compile_term.QUANTIFIED] += 1
                        continue
                    if isinstance(c, compile_term.Refusal):
                        refused[c.reason] += 1
                    elif c.slot == slot:
                        hit = views.get(c.term.name)
                        if hit is None:
                            views[c.term.name] = (c, {"library": key, "role": role,
                                                      "template": cand.get("template"),
                                                      "entries": 1,
                                                      **({"via": c.via} if c.via else {})})
                        else:
                            hit[1]["entries"] += 1
                        _landed += 1
                if _7L_KIND and _landed:
                    # G1 (the reviewer 2026-10-15 20:54): the KIND entry records what LANDED,
                    # never only what was asked (Fig 12: the group fixes the outcome)
                    self._land_kind((key, role, self._kind(mine), self._kind(partner)))
            for o_ in others:
                _landed = 0
                for cand, if_c, then_c in self._compiled(lib, key, "CAUSE", o_, mine, comp, atoms,
                                                         sig, slot=slot, tally=tally):
                    if isinstance(if_c, compile_term.Refusal):
                        refused["if: " + if_c.reason] += 1
                        continue
                    if isinstance(then_c, compile_term.Refusal):
                        refused["then: " + then_c.reason] += 1
                        continue
                    if then_c.slot != slot:
                        continue
                    pk = (if_c.term.name, if_c.slot, then_c.term.name)
                    hit = causes.get(pk)
                    if hit is None:
                        _via = if_c.via or then_c.via
                        causes[pk] = (if_c, then_c, {"library": key, "role": "CAUSE",
                                                     "bond": cand.get("bond"), "entries": 1,
                                                     **({"via": _via} if _via else {})})
                    else:
                        hit[2]["entries"] += 1
                    _landed += 1
                if _7L_KIND and _landed:
                    self._land_kind((key, "CAUSE", self._kind(o_), self._kind(mine)))
        if _7L_KIND:
            self._kind_episodes.append({"game": self.gamma.game, "level": self.level, "slot": slot,
                                   "o": mine, "x": list(others),
                                   "outcome": len(views) + len(causes),
                                   "salience": self.outstanding(slot)})
        return views, causes, refused

    def _land_kind(self, entry: tuple) -> None:
        """7l: a landed (entry, role, kind_o, kind_x); 7m's pair set kept with it."""
        self._kind_landed.add(entry)
        self._kind_pairs.add((entry[2], entry[3]))

    def _kind(self, owner: str) -> tuple:
        """7l: an object's KIND as the agent holds it: the sorted attribute types of its slots."""
        k = (owner, len(self.slots))   # cleared wherever slot_types is replaced
        got = self._kind_cache.get(k)
        if got is None:
            got = self._kind_cache[k] = tuple(sorted({
                str(self.slot_types.get(s)) for s in self.slots if s.split(".")[0] == owner}))
        return got

    def _compiled(self, lib: Any, key: str, role: str, o: str, x: str, comp: Any, atoms: dict,
                  sig: tuple | None, slot: str | None = None,
                  tally: Counter | None = None) -> Any:
        """(cand, compiled, then-compiled) per candidate: a CAUSE's if and then, a view's condition
        with None for then, None for a quantified view. Under the index hold a held role whose
        names are plain ids binds the compile held for its entry; anything else, or the arm OFF,
        compiles the named text as before."""
        if (sig is not None and role in _HELD_ROLES and o != x
                and all(_PLAIN.fullmatch(n) and "PH" not in n for n in (o, x))):
            if slot is not None and _SLOT_FILTER:
                # S1: only the rows that land on the asked slot (or that _index_reach counts) are
                # bound, into the slot's OWN memo. What is already held is read first, never bound
                # again (the reviewer 2026-10-15 11:14 N1, 11:22): a whole view this process holds,
                # then a slot answer carried in bs_ (S1b), then a whole carried in bm_; a filtered
                # answer never enters the whole-view memo. S1c (12:02): a pair asked for a second
                # slot is PROMOTED, its whole bound once and held; a held whole is read through
                # its slot map, a lookup, never a scan
                _INDEX_N["bound_slot"] += 1
                smemo = _BOUND_SLOT_MEMO if self._atoms_token else self._bound_slot_cache
                sidx = _BOUND_SLOT_IDX if self._atoms_token else self._bound_slot_idx
                seen = _PAIRS_SEEN if self._atoms_token else self._pairs_seen
                maps = _BOUND_SLOT_MAP if self._atoms_token else self._bound_slot_map
                skey = (self._atoms_token, sig, key, role, o, x, slot)
                memo = _BOUND_MEMO if self._atoms_token else self._bound_cache
                mkey = (self._atoms_token, sig, key, role, o, x)
                if tally is not None:
                    # SPEED-2: the pair's counts, once; the slot's memo holds landing rows only
                    tally.update(self._pair_count(lib, key, role, o, x, atoms, sig, mkey)[0])
                got = smemo.get(skey)
                if got is not None:
                    _INDEX_N["bound_slot_hit"] += 1
                    return list(got)
                whole = memo.get(mkey)
                carried = None if whole is not None else lineage.resolve_bs(self, lib, skey, atoms)
                if carried is not None:
                    _INDEX_N["bound_slot_from_carry"] += 1
                    seen.add(mkey)
                    sidx[skey], got = carried
                    smemo[skey] = got
                    return list(got)
                if whole is None:
                    whole = lineage.resolve_memo(self, lib, mkey, atoms)
                    if whole is not None:
                        # resolve_memo hands a carried view over once: kept as the WHOLE answer
                        # it is, so other slots and the next boundary write still have it (S3)
                        _INDEX_N["bound"] += 1
                        memo[mkey] = whole
                sub = partial(_ph_sub, o=o, x=x)
                if whole is None and lineage._RECORD and lineage.recorded_whole(mkey):
                    # S1g: recorded as a WHOLE (reused) in an earlier process: bound at once, as
                    # promotion would, from the carried and live-checked index (S3)
                    _INDEX_N["bound_slot_from_record"] += 1
                    _INDEX_N["bound"] += 1
                    whole = memo[mkey] = tuple(
                        (cand, _bound(a, sub, atoms), _bound(b, sub, atoms))
                        for cand, a, b in self._held_index(lib, key, role, atoms, sig))
                if whole is None and mkey in seen:
                    # PROMOTE ON REUSE: held as the WHOLE it is, so bm_ carries it (S3)
                    _INDEX_N["bound_slot_promoted"] += 1
                    _INDEX_N["bound"] += 1
                    whole = memo[mkey] = tuple(
                        (cand, _bound(a, sub, atoms), _bound(b, sub, atoms))
                        for cand, a, b in self._held_index(lib, key, role, atoms, sig))
                # a whole view is aligned with the held rows, so its positions are the held indices
                if whole is not None:
                    _INDEX_N["bound_slot_from_whole"] += 1
                    idx = _whole_rows(role, whole, slot, maps, mkey)
                    if tally is not None:
                        idx = tuple(heapq.merge(maps[mkey][0].get(slot, ()),
                                                _pair_tally_of(self, mkey)[1]))
                    got = tuple(whole[i] for i in idx)
                else:
                    seen.add(mkey)
                    held = self._held_index(lib, key, role, atoms, sig)
                    _INDEX_N["bound_slot_scanned"] += len(held)
                    idx = tuple(i for i, (_c, a, b) in enumerate(held)
                                if _lands(role, a, b, slot, sub)
                                and (tally is None or _tally_key(role, a, b, sub) is None))
                    _INDEX_N["bound_slot_first_binds"] += 2 * len(idx)
                    got = tuple((held[i][0], _bound(held[i][1], sub, atoms),
                                 _bound(held[i][2], sub, atoms)) for i in idx)
                sidx[skey] = idx
                smemo[skey] = got
                return list(got)
            _INDEX_N["bound"] += 1
            # RECORDED ONCE PER AGENT, as OFF's text-keyed _compile_cache records its compiles:
            # _bound is pure in (the held compile, o, x, this Gamma's atoms), so a repeated
            # question is a lookup (Fig 12; the reviewer 2026-10-15 04:57). A tuple is stored and a
            # fresh list returned, so no caller can alter the memo.
            memo = _BOUND_MEMO if self._atoms_token else self._bound_cache
            mkey = (self._atoms_token, sig, key, role, o, x)
            got = memo.get(mkey)
            if got is not None:
                _INDEX_N["bound_memo_hit"] += 1
                return list(got)
            # a carried answer (lineage, under CARRY), checked whole at its first ask; counted
            # apart from hits, so memo entries == bound - bound_memo_hit holds (S3)
            got = lineage.resolve_memo(self, lib, mkey, atoms)
            if got is None:
                sub = partial(_ph_sub, o=o, x=x)
                got = tuple((cand, _bound(a, sub, atoms), _bound(b, sub, atoms))
                            for cand, a, b in self._held_index(lib, key, role, atoms, sig))
            memo[mkey] = got
            return list(got)
        if sig is not None:
            _INDEX_N["named"] += 1
        if tally is not None and slot is not None:
            # SPEED-2 (c): the named compile (a compound partner, a role not held) split ONCE
            # per pair into landing rows by slot and one Counter. Valid for this Agent's life:
            # its atoms are set once (gamma.py:849, tether.py:1590; a mint adds a Term, never
            # an atom) and the route's library is fixed for the process (_lib_view)
            nkey = (sig, key, role, o, x)
            hit = self._named_split.get(nkey)
            if hit is None:
                _INDEX_N["named_split"] += 1
                by: dict = {}
                rest, cnt = [], Counter()
                for cand in self._lib_view(lib, key, role, o, x):
                    row = ((cand, comp(cand["if"], o), comp(cand["then"], x))
                           if role == "CAUSE"
                           else (cand, None if "quantifier" in cand
                                 else comp(cand["condition"], o), None))
                    k = _tally_key(role, row[1], row[2], _same)
                    if k is not None:
                        cnt[k] += 1
                    elif role == "CAUSE" and (row[1] is None or row[2] is None):
                        rest.append(row)
                    else:
                        by.setdefault((row[2] if role == "CAUSE" else row[1]).slot,
                                      []).append(row)
                hit = self._named_split[nkey] = (by, cnt, tuple(rest))
            tally.update(hit[1])
            return list(hit[0].get(slot, ())) + list(hit[2])
        if role == "CAUSE":
            return ((cand, comp(cand["if"], o), comp(cand["then"], x))
                    for cand in self._lib_view(lib, key, role, o, x))
        return ((cand, None if "quantifier" in cand else comp(cand["condition"], o), None)
                for cand in self._lib_view(lib, key, role, o, x))

    def _pair_count(self, lib: Any, key: str, role: str, o: str, x: str, atoms: dict,
                    sig: tuple, mkey: tuple) -> tuple:
        """SPEED-2: (the pair's refusal Counter, the held indices of its uncounted every-slot
        rows), read from the held rows ONCE per pair under the pair's names. Keyed as the
        whole memo is (C3: the atoms' token and signature, which a mint does not move)."""
        got = _pair_tally_of(self, mkey)
        if got is None:
            _INDEX_N["pair_count"] += 1
            sub = partial(_ph_sub, o=o, x=x)
            cnt, rest = Counter(), []
            for i, (_c, a, b) in enumerate(self._held_index(lib, key, role, atoms, sig)):
                k = _tally_key(role, a, b, sub)
                if k is not None:
                    cnt[k] += 1
                elif role == "CAUSE" and (a is None or b is None):
                    rest.append(i)
            got = (_PAIR_TALLY if self._atoms_token else self._pair_tally)[mkey] = (
                cnt, tuple(rest))
        return got

    def _held_index(self, lib: Any, key: str, role: str, atoms: dict, sig: tuple) -> list:
        """An entry's view in a held role, compiled ONCE under the placeholders and kept for the
        process, keyed by what a compile can read of the atoms (compile_term.signature)."""
        held = _INDEX_STORE.get((sig, key, role))
        if held is None and lineage._CARRY:
            # (b'-g) D3, BOTH ARMS: a carried reference resolves at its first ask, or fails whole
            held = lineage.resolve(self, lib, key, role, sig)
        if held is None:
            def comp(cond: str, subject: str | None = None) -> Any:
                return compile_term.compile_candidate(
                    {"condition": cond}, atoms, subject=subject if _LIBRARY_ABDUCE else None)
            held = []
            for cand in lib.view(key, role, PH_O, PH_X):
                if role == "CAUSE":
                    held.append((cand, comp(cand["if"], PH_O), comp(cand["then"], PH_X)))
                else:
                    held.append((cand, None if "quantifier" in cand
                                 else comp(cand["condition"], PH_O), None))
            _INDEX_STORE[(sig, key, role)] = held
            _INDEX_N["held"] += 1
        return held

    def _lib_view(self, lib: Any, key: str, role: str, o: str, x: str) -> list:
        """lib.view, LOOKED UP rather than re-derived (7e; Fig 12 :107-108). An entry's view in a
        held role is derived once per run under the library's own placeholders and the names are
        put back as text: candidates() names o and x only through t.format (library 647), so the
        result is the named view. Bypassed, as the named call: a role that filters on a name
        (RELATION/MEASURE, library 504), o == x (PROCESS de-duplicates by text, library 497-498),
        a name with a brace. The key is (entry, role) because the route's library is fixed for the
        process (_library is cached; inventions go to the private copy). IF THE ROUTE EVER READS
        THE PRIVATE COPY, THE KEY MUST GAIN ITS VERSION."""
        if not _VIEW_HOLD:
            return lib.view(key, role, o, x)
        why = ("role" if role not in _HELD_ROLES else "same" if o == x
               else "brace" if any(b in o + x for b in "{}") else None)
        if why:
            self._view_hold_n["bypass_" + why] += 1
            return lib.view(key, role, o, x)
        held = self._view_hold.get((key, role))
        if held is None:
            held = self._view_hold[(key, role)] = lib.view(key, role, "{o}", "{x}")
            self._view_hold_n["held"] += 1
        self._view_hold_n["served"] += 1
        return _restore(held, o, x)

    def _library_chains(self, slot: str, in_t: str, out_t: str, stats: dict,
                        ops: dict, evidence: dict | None = None) -> list:
        """M4 library-first: this slot's offered terms as BARE chains valid for one stream, in
        offer order, each priced later by the one body. A view ends at PRED; into the
        objective stream it is closed with `all`. A chain longer than max_depth is not
        yielded and is counted, the bound the closure itself obeys."""
        out, seen = [], set()
        close = next((a for a in self.gamma.atoms if a.name == "all"), None)
        for o_ in self._lib_offers.get(slot, ()):
            atoms = tuple(o_["term"].atoms)
            if out_t == OBJ_TYPE and atoms and atoms[-1].out_type != OBJ_TYPE and close:
                atoms = atoms + (close,)
            if len(atoms) > self.cfg.max_depth:
                stats["beyond_depth"] += 1
                continue
            if not atoms or not accepts_type(Term((atoms[0],)), in_t):
                continue
            cur, elem = in_t, None
            for a in atoms:
                step = Gamma._iter_step(cur, elem, Term((a,)))
                if step is None:
                    break
                cur, elem = step
            else:
                chain = Term(atoms)
                if cur == out_t and elem is None:
                    if chain.name not in seen:
                        seen.add(chain.name)
                        out.append(chain)
                        stats["yielded"] += 1
                    if evidence is not None:   # A1 site 6: the entries that offered this chain
                        evidence[chain.name] = max(evidence.get(chain.name, 0),
                                                   int(o_["prov"].get("entries", 1)))
                    # EVERY offered operand, in offer order: one chain offered with two operands
                    # keeps both (keying by chain alone dropped the later one before pricing)
                    got = ops.setdefault(chain.name, [])
                    if o_["operand"] is not None and o_["operand"] not in got:
                        got.append(o_["operand"])
        return out

    # ---------------------------------------------------------------- objective build 1
    @_in_step("IMPORT")
    def _completion_sweep(self, degree: float) -> None:
        """ARC_AGENT 21.3, "a completion is a settle, and the sweep is how you find out what caused
        it", triggered by the completion itself (the reviewer 2026-10-11 02:19Z): the WORLD's
        objective degree reaching 1.0 ("reached", not "banked"), never the agent's own predicted
        completion. Re-examines the segment since the last completion -- what was live, which
        terms settled, which owed slots closed -- and records it. Nothing is retargeted, no
        binding dropped, no trace cleared."""
        prev, self._deg_prev = self._deg_prev, degree
        if _GOAL_CONDITION and self.trace:
            if self._reach_epoch != self._trace_epoch:
                self._reach_hist, self._reach_epoch = [], self._trace_epoch
            self._reach_hist.append((self._reach_row(self.trace[-1]), degree >= 1.0))
            if self._goal_conds:
                self._goal_recheck()
        start = max(self._sweep_from[0], self._seq_at_level)
        if prev is None or not (degree >= 1.0 > prev):
            if self._sweep_from[0] < self._seq_at_level:
                self._sweep_from = (len(self.led), self.cycle, set(self.settled),
                                    set(self.owed_import))
            return
        seq0, cyc0, settled0, owed0 = self._sweep_from
        rows = self.led.rows()[start:]
        self.led.record(self.cycle, "IMPORT", "@completion", "completion_sweep",
                        level=self.level, degree=round(degree, 4), segment_from_cycle=cyc0,
                        segment_rows=len(rows), live=dict(sorted(self.bound.items())),
                        settled_in_segment=sorted(set(self.settled) - settled0),
                        closed_in_segment=sorted(owed0 - set(self.owed_import)),
                        still_owed=sorted(self.owed_import),
                        open_process_bets=len(self._process_bets),
                        reads=("the world's objective was reached; the segment since the last "
                               "completion, re-examined (21.3); nothing changed"))
        self._sweep_from = (len(self.led), self.cycle, set(self.settled), set(self.owed_import))
        if _GOAL_CONDITION:
            self._goal_condition()

    @staticmethod
    def _reach_row(step: tuple) -> dict:
        """A reach-history row: the transition's after-state, with its BEFORE-values as `slot~1`
        (the reviewer 2026-10-11 12:35 CDT, ruled ungated). A goal condition that compares a slot
        with its own earlier reading -- CHANGE_OF's `colour_changed`, B3's toward -- reads its
        operand from here; without it every such condition read None and could never pay."""
        before, _a, after = step[0], step[1], step[2]
        assert not any(lag_of(k) for k in after), "a slot name already carries a lag suffix"
        return {**after, **{k + PREV: v for k, v in before.items()}}

    def _link_goal(self, key: str, c: Any) -> dict:
        """Objective build 3: a held goal condition becomes one of the agent's COMPOSED
        objectives, so `_goal_choice` and `_mint_routine` can pick it -- through a term the
        agent minted, never a goal we publish. The condition (a predicate on its slot) is closed
        into the objective stream with `all`, as the library-first path closes a view. Linked
        only where the slot holds no want: one want per slot, and replacing one the agent
        composed is not this item's to decide."""
        parts = list(c.parts) if isinstance(c, _Pair) else [c]
        if _RELATION_SET:
            parts = [self._movable_spelling(p) for p in parts]
        close = next((a for a in self.gamma.atoms if a.name == "all"), None)
        if close is None:
            return {"linked": False, "why": "no `all` atom to close the condition"}
        terms = []
        for part in parts:
            term = Term(tuple(part.term.atoms) + (close,), operand=part.term.operand,
                        operand_term=part.term.operand_term)
            if term.out_type != OBJ_TYPE:
                return {"linked": False, "why": f"closes to {term.out_type}, not an objective"}
            terms.append((part.slot, term))
        # (b): a pair links as one want per conjunct, each on its own subject slot -- all or
        # none: if any slot already wants, the whole pair is refused, counted once
        taken = {sl: self.wants[sl] for sl, _t in terms if sl in self.wants}
        if taken or len({sl for sl, _t in terms}) < len(terms):
            _book_add(self.gamma.book, "goal_link_refused_wants")      # L2
            return {"linked": False, "slots": [sl for sl, _t in terms],
                    "why": "the slot already wants", "held_want": taken}
        for sl, term in terms:
            self.wants[sl] = term.name
            self._want_terms[sl] = term
            self._want_scope[sl] = term.name                            # b-0: subject scope
        self._goal_links[key] = tuple((sl, t.name) for sl, t in terms)
        _book_add(self.gamma.book, "goal_link_made")                    # L2
        return {"linked": True, "slots": [sl for sl, _t in terms],
                "want": [t.name for _sl, t in terms], "scope": "subject"}

    def _movable_spelling(self, part: Any) -> Any:
        """BOTH SPELLINGS (TETHER_RELATION_SET; the reviewer 2026-10-11): a comparison of two slots
        can be wanted on either party. The want goes on the party the agent's OWN reading marks
        as movable -- a slot in Agency.contingent, the reading ARC B2's actor set is -- and on the
        spelling as written when neither or both are. Same truth either way, so the price is
        unchanged; only the subject of the want moves."""
        other = compile_term.converse(part, {a.name: a for a in self.gamma.atoms})
        if other is None:
            return part
        return other if (self._moves_by_sources(other.slot)
                         and not self._moves_by_sources(part.slot)) else part

    def _moves_by_sources(self, slot: str) -> bool:
        """BY SOURCES (the reviewer 2026-10-11 13:49 CDT): a pair slot is never bet on, so it is
        never in contingent(); it moves when ANY of its sources does -- o0.dist_o3 changes when
        o3 moves as much as when o0 does. An ordinary slot's only source is itself."""
        return self._movable_by(slot) is not None

    def _movable_by(self, slot: str) -> str | None:
        """Which reading says the slot moves: "contingent" (by sources), "direction" (B, arm only;
        it can only ADD movables), or None."""
        moving = set(self.agency.contingent())
        dv = getattr(self.env, "derived", None)
        derived = dv() if dv is not None else {}
        srcs = derived.get(slot, (slot,))
        if any(s in moving for s in srcs):
            return "contingent"
        if _DIRECTION_MOVABLE and any(self._moves_by_direction(s) for s in (slot, *srcs)):
            return "direction"
        return None

    def _note_direction(self, action: str, before: dict, after: dict, slots: list) -> None:
        """B: the sign of each ordered slot's change, keyed by (action, ctx). ctx is, for every
        controlled owner c (an owner of a contingent() slot; never a name taken on trust), the
        signs of the agent's own pair slots c.drow_X / c.dcol_X for the slot's object X ((c, 0, 0)
        when X is c). Nothing is recorded where a needed pair slot is absent. A slot is read when
        its type is ordered: the type map is the only categorical marker there is."""
        ctrl = sorted({s.rsplit(".", 1)[0] for s in self.agency.contingent() if "." in s})
        if not ctrl:
            return
        if not self._dir_scope_noted:
            self._dir_scope_noted = True
            kinds: dict = {}
            for _s, _ty in self.slot_types.items():
                kinds[str(_ty)] = kinds.get(str(_ty), 0) + 1
            self.led.record(self.cycle, "PERCEIVE", "@direction", "direction_scope",
                            ordered=list(ORDERED_TYPES), slot_types=kinds,
                            reads=("a slot is read when its type is ordered; a categorical slot "
                                   "the type map calls ordered is read too, and its sign means "
                                   "nothing (a perception item, steps 5/6)"))
        sg = lambda v: (v > 0) - (v < 0)              # noqa: E731
        for s in slots:
            if "." not in s or self.slot_types.get(s) not in ORDERED_TYPES:
                continue
            b, a = before.get(s), after.get(s)
            if not isinstance(b, int) or not isinstance(a, int):
                continue
            x = s.rsplit(".", 1)[0]
            ctx = []
            for c in ctrl:
                if c == x:
                    ctx.append((c, 0, 0))
                    continue
                dr, dc = before.get(f"{c}.drow_{x}"), before.get(f"{c}.dcol_{x}")
                if not isinstance(dr, int) or not isinstance(dc, int):
                    ctx = None
                    break
                ctx.append((c, sg(dr), sg(dc)))
            if ctx is None:
                continue
            self._dir.setdefault(s, {}).setdefault((action, tuple(ctx)), set()).add(sg(a - b))

    def _moves_by_direction(self, slot: str) -> bool:
        """Movable iff, in one ctx, the PURE cells (one sign seen) of two actions differ. A mixed
        cell abstains. A changer that moves the same way whatever the action never qualifies."""
        by_ctx: dict = {}
        for (_action, ctx), signs in self._dir.get(slot, {}).items():
            if len(signs) == 1:
                by_ctx.setdefault(ctx, set()).add(next(iter(signs)))
        return any(len(v) > 1 for v in by_ctx.values())

    def _respell_goals(self) -> None:
        """BOTH SPELLINGS, OVER TIME (the reviewer 2026-10-11 12:12 CDT): a want linked before the
        agent had read its own agency was spelled as written. When the reading now puts the
        movable party on the other side, the link is released (the counted release path) and
        re-linked there -- one want, never two. Left alone where the new subject already wants.
        Only when the verdict CHANGES from the last re-spell (the link holds it), so a wobbling
        reading cannot flip a want silently: every move writes a goal_respelled row."""
        if not _RELATION_SET:
            return
        for key in sorted(self._goal_links):
            c = self._goal_conds.get(key)
            if c is None:
                continue
            parts = list(c.parts) if isinstance(c, _Pair) else [c]
            now = [p.slot for p in (self._movable_spelling(p) for p in parts)]
            had = [sl for sl, _n in self._goal_links[key]]
            if now == had or any(sl in self.wants for sl in set(now) - set(had)):
                continue
            self._release_link(key)
            link = self._link_goal(key, c)
            self.led.record(self.cycle, "PLAN", "@completion", "goal_respelled", key=key,
                            want=self._goal_text.get(key), was=had, now=link.get("slots"),
                            linked=bool(link.get("linked")),
                            reads="the movable-party verdict changed: the want moves to it")

    @_in_step("IMPORT")
    def _close_goals(self, how: str) -> None:
        """E1 (the reviewer 2026-10-11 03:38Z): a held goal condition CLOSES with its level --
        at a retarget or the run's end -- and is never re-priced against the next level's
        empty history, which would unhold it with a false reason. No verdict, not counted as
        unlinked; the wants are cleared by retarget's own rule. Carry is M7."""
        for key in sorted(self._goal_conds):
            self.led.record(self.cycle, "IMPORT", "@completion", "goal_closed", key=key,
                            condition=self._goal_text.get(key), how=how, verdict=None,
                            reads="closed with its level: no verdict on the condition")
        self._goal_conds, self._goal_text, self._goal_links = {}, {}, {}
        self._want_scope = {}

    def _release_link(self, key: str) -> bool:
        """L1 / (b): release every want this link wrote that is still in place, and only those;
        a want the agent composed itself is never touched."""
        link = self._goal_links.pop(key, None) or ()
        released = False
        for sl, name in link:
            if self.wants.get(sl) == name:
                self.wants.pop(sl, None)
                self._want_terms.pop(sl, None)
                released = True
            if self._want_scope.get(sl) == name:
                self._want_scope.pop(sl, None)
        if released:
            _book_add(self.gamma.book, "goal_unlinked")                  # L2
        return released

    @_in_step("IMPORT")
    def _goal_recheck(self) -> None:
        """L1 (the reviewer 2026-10-11 03:28Z): a held goal condition stays held only while it
        still pays the one bargain on the growing history (Fig 5 :42-44). Once it does not, it
        is dropped and, if its link wrote a want that is still in place, the want is released;
        a want the agent composed itself is never touched."""
        rows = self._reach_hist
        n, k = len(rows), sum(1 for _, hit in rows if hit)
        base = k * math.log2(n) if n else 0.0
        for key, c in list(self._goal_conds.items()):
            cost, left, e = self._goal_price([c], rows)
            if pays(cost, left, base):
                continue
            self._goal_conds.pop(key)
            released = self._release_link(key)
            self.led.record(self.cycle, "IMPORT", "@completion", "goal_unheld",
                            key=key, condition=self._goal_text.pop(key, None), steps=n,
                            reached=k, cost=round(cost, 3), left=round(left, 3), errors=e,
                            base_bits=round(base, 3), want_released=released,
                            reads="the held goal condition no longer pays on the longer history")

    def _goal_price(self, conds: list, rows: list) -> tuple[float, float, int]:
        """The one bargain on a 1-bit history (Fig 5 :42-44), as two-part description length,
        positions named at log2 N bits each: with no term, naming each step where the world's
        objective held; with Q (any listed condition true), cost(Q) plus naming each step Q
        gets wrong. Monotone in mistakes, so the goal's negation never pays. Reads only the
        world's readings and the world's verdict. Listing occasions one by one pays for every
        one (M6-a)."""
        def size(c: Any) -> int:      # a pair is both parts plus the `both` joiner
            return (sum(self.gamma.length(x.term) for x in c.parts) + 1 if isinstance(c, _Pair)
                    else self.gamma.length(c.term))

        def true(c: Any, st: dict) -> bool:
            return c.holds(st) if isinstance(c, _Pair) else compile_term.run(c, st) is True
        cost = term_bits(sum(size(c) for c in conds), self.gamma.alphabet)
        e = sum(1 for st, hit in rows if any(true(c, st) for c in conds) != hit)
        return cost, e * math.log2(len(rows)), e

    def _goal_pairs(self, singles: list, rows: list) -> list:
        """Build 2a (the reviewer 2026-10-11 05:14Z): the AND of two DIFFERENT conditions, each
        priced as one term by `_goal_price`. SEARCH BOUND, recorded as one: a pair is formed only
        from conditions true on EVERY step where the objective held (necessity), since a pair is
        false wherever either part is."""
        reached = [st for st, hit in rows if hit]
        nec = sorted((x for x in singles
                      if all(compile_term.run(x[5], st) is True for st in reached)),
                     key=lambda x: x[4])
        out = []
        for i, a in enumerate(nec):
            for b in nec[i + 1:]:
                if a[4] == b[4]:
                    continue                    # identical parts are not a pair
                pair = _Pair((a[5], b[5]))
                cost, left, e = self._goal_price([pair], rows)
                out.append((cost + left, cost, left, e, f"{a[4]} and {b[4]}", pair))
        return out

    @_in_step("IMPORT")
    def _goal_condition(self) -> None:
        """Objective build 2 (the reviewer 2026-10-11 02:19Z): at a completion, conditions from
        the library's own templates over the readings, each priced by `_goal_price` against
        the history of when the world's objective held. The flag is the then-side, never the
        subject; nothing about the target is published; the cheapest that pays is held
        in-episode in the private library copy, its carry verdict recorded."""
        rows = self._reach_hist
        n, k = len(rows), sum(1 for _, hit in rows if hit)
        if not k or k == n:
            return
        base = k * math.log2(n)
        atoms = {a.name: a for a in self.gamma.atoms}
        refused: Counter = Counter()
        cands = []
        for text in self._inv_conditions(rows[-1][0]):
            c = self._compile_cache.get(text)
            if c is None:
                c = self._compile_cache[text] = compile_term.compile_candidate(
                    {"condition": text}, atoms)
            if isinstance(c, compile_term.Refusal):
                refused[c.reason] += 1
                continue
            cost, left, e = self._goal_price([c], rows)
            cands.append((cost + left, cost, left, e, text, c))
        n_plain = len(cands)
        if _GOAL_PAIR:
            cands += self._goal_pairs(cands, rows)
        lag = sum(1 for x in cands if any(lag_of(t) for t in re.findall(r"[\w.]+~\d+", x[4])))
        cands.sort(key=lambda x: (x[0], x[4]))
        if _A1_TIES and cands:          # A1: an exact tie in total, never by condition text
            tied = [x for x in cands if x[0] == cands[0][0]]
            if len(tied) > 1:
                _a1k = self._choice("goal_condition", None, [(x[4], x[0], None) for x in tied])
                cands.insert(0, cands.pop(next(i for i, x in enumerate(cands) if x[4] == _a1k)))
        detail = {"steps": n, "reached": k, "base_bits": round(base, 3),
                  "conditions": len(cands), "refused": dict(refused),
                  "offered": {"plain": n_plain, "pair": len(cands) - n_plain, "lag": lag},
                  "cheapest": [{"if": x[4], "cost": round(x[1], 3), "left": round(x[2], 3),
                                "errors": x[3]} for x in cands[:5]]}
        best = cands[0] if cands and pays(cands[0][1], cands[0][2], base) else None
        if best is None:
            detail["pick"] = "none paid"
        elif best[4] in self._goal_text.values():
            detail["pick"] = f"already held: {best[4]}"
        else:
            _t, cost, left, e, text, c = best
            lib = self._inv_library()
            try:
                key = lib.invent_atom(f"{self.gamma.game}_goal_{len(self._goal_conds) + 1}",
                                      text, game=self.gamma.game, cycle=self.cycle,
                                      receipt={"completion": self.cycle, "steps": n,
                                               "reached": k, "errors": e})
                self._goal_conds[key] = c
                self._goal_text[key] = text
                if _GOAL_LINK:
                    detail["link"] = self._link_goal(key, c)
                safe, why = sys.modules["library_runtime"].carry_check(text, lib.readings)
                detail.update(pick=text, key=key, carry=("may carry when M7 opens" if safe
                                                         else f"refused: {why}"))
            except ValueError as err:
                detail.update(pick="refused at creation", why=str(err), condition=text)
        self.led.record(self.cycle, "IMPORT", "@completion", "goal_condition", **detail)

    # ---------------------------------------------------------------- 7a(10) D1-D3
    def _process_bet(self, kind: str, slot: str, **what: Any) -> None:
        """D1: one of the agent's PROCESS states made a bet about a GROUND outcome (R3 part 2,
        seeded from routine.Expect). Recorded and held open; D3 settles it only at an ending."""
        row = self.led.record(self.cycle, self._running_step, "@process", "process_bet", kind=kind,
                              about=slot, level=self.level, **what)
        self._process_bets.append({"seq": row.seq, "kind": kind, "slot": slot,
                                   "level": self.level})

    def _park_bet(self, slot: str, detail: dict) -> None:
        """D1 + D2: a parked slot bets it will be explained by level end, its stall described as
        an EFFECT the lookup can match by shape (sealed at depth d; stopped at bound b; under the
        floor by x bits). One open bet per slot per level."""
        v = detail.get("verdict")
        if v not in ("under_floor", "budget_spent", "priced_out_at_depth") or any(
                b["slot"] == slot and b["kind"] == "parked_explained"
                for b in self._process_bets):
            return
        stall = ({"effect": "under the floor", "base_bits": detail.get("base_bits"),
                  "floor_bits": detail.get("floor_bits")} if v == "under_floor" else
                 {"effect": "search stopped at its bound", "seen": detail.get("candidates_seen"),
                  "coverage": detail.get("coverage")} if v == "budget_spent" else
                 {"effect": "sealed at depth", "depth": detail.get("depth"),
                  "seen": detail.get("candidates_seen")})
        self._process_bet("parked_explained", slot, park_verdict=v, stall=stall)

    @_in_step("SETTLE")
    def _settle_process(self, scope: str, how: str) -> None:
        """D3: a process bet settles ONLY on a level or game outcome, read from the GROUND, never
        from the agent's own diagnosis (Fig 10, "A verifier that can reconstruct the claim
        cannot verify it."). A plan bet is right iff the level cleared (win or advance). A park
        bet is graded on the slot's last CHANGE row after the park -- a step where the world
        moved it -- right iff that bet carried no mass; a quiet step is paid by "nothing
        happens" and explains nothing, so with no change after the park there is no ground
        reading and it says so (the reviewer 00:14Z). A departure is not a change: the slot left
        the listing, which says nothing about its explanation, so it is no reading either. D2: an
        uncleared level's stall is recorded as an effect, the actions it ran for."""
        rows = self.led.rows()[self._seq_at_level:]
        cleared = how in (WIN, ADVANCE)
        for b in self._process_bets:
            after = [r for r in rows if r["event"] == "bet" and r["slot"] == b["slot"]
                     and r["seq"] > b["seq"]]
            moved = [r for r in after if not r["detail"].get("vanished")
                     and r["detail"].get("actual") != r["detail"].get("from_value")]
            if b["kind"] == "plan_clears":
                right, by = cleared, f"the level's ending: {how}"
            elif moved:
                right = not float(moved[-1]["detail"].get("mass", 0) or 0)
                by = "the world's grade of the slot's last change after the park"
            elif any(r["detail"].get("vanished") for r in after):
                right, by = None, ("the slot left the board after the park: no ground reading "
                                   "on its explanation")
            else:
                right, by = None, "no change after the park: no ground reading"
            self.led.record(self.cycle, "SETTLE", "@process", "process_settle", bet_seq=b["seq"],
                            kind=b["kind"], about=b["slot"], right=right, settled_by=by,
                            scope=scope, how=how, level=self.level,
                            **({} if cleared else {"stall": {
                                "effect": "level stalled", "actions": self._attempt_actions}}))
        self._process_bets = []

    # ---------------------------------------------------------------- 7a(10) MC6, MUSE
    def _owes_nothing(self) -> bool:
        """MC6's mastery (R3 part 2): no residual outstanding on the level -- owed_import empty,
        an under_floor slot included ("the search is skipped; the debt is not"; the reviewer
        23:50Z) -- and this step's bets paying: at least one, none carrying mass."""
        if self.owed_import:
            return False
        bets = [r for r in self.led.rows()[self._step_row0:] if r["event"] == "bet"]
        return bool(bets) and all(not float(r["detail"].get("mass", 0) or 0) for r in bets)

    @_in_step("IMPORT")
    def _muse(self) -> None:
        """MC6 (R3 part 2; the reviewer 2026-10-10 23:50Z). On a step that owes nothing, the
        mastered methods (settled, non-atom terms) are re-tested against the residuals an
        EARLIER level left parked (Fig 8, then Fig 7's room, then Fig 4's round trip), priced as
        the sweep prices them. Compute only: a METHOD is its chain, re-bound on the parked slot's
        own history; no binding crosses, nothing is installed, no action is taken. The gap and
        the time spent are recorded."""
        targets = {k: r for k, r in self.parked.items() if r.get("level") != self.level
                   and r.get("hist")}
        if not targets or not self._owes_nothing():
            return
        t0 = time.perf_counter()
        methods = sorted(n for n, t in self.gamma.library.items()
                         if not self.gamma.is_atom(t) and self.gamma.is_settled(n))
        # N2 (the reviewer 00:05Z): nothing changed since the last muse, nothing is re-tested
        key = (tuple(sorted(targets)), tuple(methods))
        if self._muse_last is not None and self._muse_last[0] == key:
            self.led.record(self.cycle, "IMPORT", "@muse", "muse", level=self.level,
                            unchanged_since=self._muse_last[1], tried=0, paying=[],
                            compute_ms=round(1000 * (time.perf_counter() - t0), 3),
                            installed=False,
                            reads="the same targets and settled methods as that cycle's muse")
            return
        self._muse_last = (key, self.cycle)
        tried, paying, skipped = 0, [], Counter()
        for key, rec in sorted(targets.items()):
            slot, hist = rec["slot"], rec["hist"]
            if slot not in self.alphabet:
                skipped["slot has no alphabet this level"] += 1
                continue
            base = self._left(self.gamma.library[IDN], slot, hist)
            for name in methods:
                chain = self.gamma.library[name].atoms
                best = None
                for bind in [None] + [x for x in rec.get("slots", ()) if x != slot]:
                    cand = Term(chain, operand=bind)
                    tried += 1
                    left = self._left(cand, slot, hist)
                    if best is None or left < best[0]:
                        best = (left, cand)
                left, cand = best
                cost = term_bits(self.gamma.length(cand), self.gamma.alphabet)
                if pays(cost, left, base):
                    paying.append({"parked": key, "method": name, "as": cand.name,
                                   "cost": round(cost, 3), "left": round(left, 3),
                                   "base": round(base, 3)})
        self.led.record(self.cycle, "IMPORT", "@muse", "muse", level=self.level,
                        targets=sorted(targets), methods=len(methods), tried=tried,
                        paying=paying, skipped=dict(skipped),
                        compute_ms=round(1000 * (time.perf_counter() - t0), 3),
                        installed=False,
                        # N1 (the reviewer 00:05Z): as in the sweep, choosing the operand (bare
                        # or one of the record's slots) is not charged; operand-choice pricing
                        # is ONE queued item, never half-applied (the reviewer 2026-10-09 14:52Z)
                        binding="unpriced",
                        reads=("a mastered method re-tested on an earlier level's parked "
                               "residual; the gap recorded, nothing installed, no action"))

    # ---------------------------------------------------------------- 7c M6, INVENT
    def _inv_holds(self, key: str | None, state: dict) -> bool:
        c = self._invented.get(key) if key else None
        return c is not None and compile_term.run(c, state) is True

    def _inv_cost(self, f: Term, conds: list, units: tuple = ()) -> float:
        """M6-b: the WHOLE length, the then-term's atoms plus every condition's, priced as the mint
        prices a term of that length. Nothing is discounted for lying past the searched depth."""
        k = self.gamma.length(f, units) + sum(self.gamma.length(c.term) for c in conds)
        return term_bits(k, self.gamma.alphabet)

    def _inv_left(self, f: Term, conds: list, slot: str, hist: list) -> float:
        """What `f` when any condition holds, identity otherwise, leaves unexplained (in bits)."""
        idn = self.gamma.library[IDN]
        total = 0.0
        for row in hist:
            on = any(compile_term.run(c, row[0]) is True for c in conds)
            total += self._left(f if on else idn, slot, [row])
        return total

    def _inv_library(self) -> Any:
        """A private copy: an invention lights for THIS agent only, never another game in the
        process (Fig 4; carry is M7). library/ is never written."""
        if self._inv_lib is None:
            lib = _library()
            if lib is None:
                return None
            self._inv_lib = _replace_lib(lib)
        return self._inv_lib

    def _inv_conditions(self, state: dict) -> list[str]:
        """The library's own condition grammar (`TEMPLATES`, by reading type) filled over the
        objects and readings in this state: the shapes the library writes, never a list of ours."""
        if _library() is None:
            return []
        templates = sys.modules["library_runtime"].TEMPLATES
        rd = compile_term.readings()
        keys = sorted(k for k, v in state.items()
                      if isinstance(v, int) and "." in k and "~" not in k and "@" not in k)
        objs = sorted({k.split(".", 1)[0] for k in keys})
        out = []
        for k in keys:
            o, r = k.split(".", 1)
            for _label, t in templates.get((rd.get(r) or {}).get("type"), ()):
                for x in ([x for x in objs if x != o] if "{x}" in t else [None]):
                    out.append(t.format(o=o, x=x, r=r))
        return out

    def _invent(self, slot: str, hist: list, base: float, base_held: float, verdict: str) -> None:
        """7c M6 (ISAIAH_RULINGS "Mint, invent, import"; the reviewer 2026-10-10 23:14Z). At a park
        where the search could not close a change that RECURRED and nothing the library lit
        expresses it, the agent names a condition over the readings that held where the slot
        changed: `f` when Q holds, identity otherwise. Priced by the ONE bargain at its whole
        length; held only if it pays. M6-c: an under_floor park is never a trigger."""
        if verdict not in ("budget_spent", "priced_out_at_depth"):
            return
        moved = [i for i in range(len(hist)) if hist[i][2] != hist[i][0].get(slot)]
        if len(moved) < 2 or self._lib_offers.get(slot) or self._inv_seen.get(slot) == len(hist):
            return
        self._inv_seen[slot] = len(hist)
        atoms = {a.name: a for a in self.gamma.atoms}
        refused: Counter = Counter()
        conds, never_false = [], 0
        for text in self._inv_conditions(hist[-1][0]):
            c = self._compile_cache.get(text)
            if c is None:
                c = self._compile_cache[text] = compile_term.compile_candidate(
                    {"condition": text}, atoms)
            if isinstance(c, compile_term.Refusal):
                refused[c.reason] += 1
                continue
            truth = [compile_term.run(c, r[0]) is True for r in hist]
            if not all(truth[i] for i in moved):
                continue
            if all(truth):
                never_false += 1          # holds everywhere: the unguarded term, searched
                continue
            conds.append((text, c, truth))
        units = self._units_for(slot)
        idn = self.gamma.library[IDN]
        idb = [self._left(idn, slot, [r]) for r in hist]
        robs = self._residual_obs(slot, self.gamma.library[self.bound.get(slot, IDN)], hist)
        fs = []
        if conds:
            for ch in self.gamma.enumerate_closure("val", "val", 1, self.cfg.budget, {}):
                for b in (self._bindings(slot, robs) if ch.reads_operand else [None]):
                    f = Term(ch.atoms, operand=b)
                    fb = [self._left(f, slot, [r]) for r in hist]
                    if any(fb[i] == 0.0 for i in moved):
                        fs.append((f, fb))
        cands = []
        for text, c, truth in conds:
            for f, fb in fs:
                left = sum(fb[i] if truth[i] else idb[i] for i in range(len(hist)))
                cost = self._inv_cost(f, [c], units)
                cands.append((cost + left, cost, left, text, c, f))
        cands.sort(key=lambda x: (x[0], x[1], x[3], x[5].name))
        # park_verdict, never `verdict`: this row names the park that triggered it and is not
        # itself an abstention (gate rule 9 reads `verdict` as one)
        detail = {"park_verdict": verdict, "moved_rows": len(moved), "rows": len(hist),
                  "base_bits": round(base, 3), "conditions_held": len(conds),
                  "conditions_never_false": never_false, "refused": dict(refused),
                  "then_terms": len(fs), "priced": len(cands),
                  "cheapest": [{"if": x[3], "then": x[5].name, "cost": round(x[1], 3),
                                "left": round(x[2], 3)} for x in cands[:5]]}
        first = cands[0] if cands else None
        if _A1_TIES and first is not None:     # A1: an exact tie in total, never by text or name
            tied = [x for x in cands if x[0] == first[0]]
            if len(tied) > 1:
                _a1k = self._choice("invent", slot,
                                   [((x[3], x[5].name), x[0], None) for x in tied])
                first = next(x for x in tied if (x[3], x[5].name) == _a1k)
        best = first if first is not None and pays(first[1], first[2], base) else None
        if best is None:
            detail["pick"] = "none paid"
            self.led.record(self.cycle, "MINT", slot, "invent", of=(slot,), **detail)
            return
        _t, cost, _l, text, c, f = best
        self._hold_invention(slot, text, c, f, cost, base_held, hist, detail)

    def _hold_invention(self, slot: str, text: str, c: Any, f: Term, cost: float,
                        base_held: float, hist: list, detail: dict) -> Term | None:
        """The invention named in this agent's library (in memory; save_runtime is never called)
        and bound to the slot through the accept path, a candidate with no head start. A
        condition naming no reading is refused at creation and recorded."""
        lib = self._inv_library()
        name = f"{self.gamma.game}_inv_{len(self._invented) + 1}"
        try:
            key = lib.invent_atom(name, text, game=self.gamma.game, cycle=self.cycle,
                                  receipt={"slot": slot, "verdict": detail.get("park_verdict"),
                                           "moved_rows": detail.get("moved_rows"),
                                           "nothing_lit": True})
        except ValueError as e:
            detail.update(pick="refused at creation", why=str(e), condition=text)
            self.led.record(self.cycle, "MINT", slot, "invent", of=(slot,), **detail)
            return None
        self._invented[key] = c
        term = Term(f.atoms, operand=f.operand, guard=INVENTED_GUARD, guard_ref=key)
        left = self._left(term, slot, hist)
        detail.update(pick=term.name, condition=text, key=key, term_bits=round(cost, 3),
                      left_bits=round(left, 3), carry="M7, off")
        detail["explained"], detail["overclaimed"] = self.explain(slot, base_held - left)
        self.gamma.accept(term, seq=len(self.led), residual=f"{slot}@{self.cycle}")
        self.bound[slot] = term.name
        self.rank.note(term.name, self.cycle)
        self.candidates[term.name] = self.cycle
        self._cand_level[term.name] = self.level
        if left == 0.0:
            self.owed_import.discard(slot)
            self.abstained.pop(slot, None)
        else:
            self.owed_import.add(slot)
        self.led.record(self.cycle, "MINT", slot, "invent", of=(slot,), **detail)
        # (c) ACCEPT by design: this row records the ACCEPT this method itself performs, a later
        # step carried out inside MINT (the reviewer 2026-10-16 09:23)
        self.led.record(self.cycle, "ACCEPT", slot, "accept", term=term.name,
                        origin=term.origin, seq=len(self.led), status="candidate",
                        cited="no: candidate may be held, not cited",
                        **({"part": self._mint_part} if self._mint_part else {}))
        self.chain.note_mint()
        self.sweep(term, slot)
        return term

    def _lib_offer(self, c: Any, prov: dict, v: dict | None = None) -> dict:
        """One compiled term's verdict as an offer: offered, or withheld with why."""
        why = None
        if v is not None and not v["supported"]:
            why = "not supported on the frames"
        elif v is not None and v["if_now"] is not True:
            why = "if-side does not hold now"
        elif c.term.name in self.gamma.library:
            why = "already held"
        else:
            _ok, why = reach.offer_or_withhold(c, _PREV_OFFER)
        return {"term": c.term, "slot": c.slot, "operand": c.operand, "prov": prov,
                "offered": why is None, "why": why}

    def _ops(self, term: Term, state: dict[str, int]) -> tuple:
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
        # THE MEMO STAYS INSIDE `_ops`: `conform/evalctx.py` exempts the one direct Ctx below by
        # this function's name, on the checked fact that an operand tree is never guarded.
        memo, key = self._memo, None
        if memo is not None:
            key = ("ops", term.operand, term.operand_term, id(state))
            hit = memo.get(key)
            if hit is not None and hit[0] is state:
                return hit[1]
        op = term.operand
        value = (self._operand_value(op, state) if "~" in op
                 else state.get(op, NOT_RESOLVED))
        if term.operand_term is not None:
            value = term.operand_term.apply(value, Ctx(operands=(value,)))
        got: tuple | None = (value,)
        if term.operand_term is not None and value is NOT_RESOLVED:
            # `None`, NOT `()` -- RULED 2026-09-21. The docstring above argued an
            # unreadable branch may fall back to "no operand" because that is the
            # identity every operand-reading atom already takes. But the identity is
            # a CLAIM: `_translate` returning `v` asserts no translation happened,
            # where the truth is that nobody could tell. 12.2 forbids exactly that --
            # *a value or an explicit non-reading, never a guess, never a default.*
            # `()` means NO OPERAND; `None` means AN OPERAND THAT CANNOT BE READ, and
            # every evaluating caller turns it into NOT_RESOLVED or unexplained.
            got = None
        if key is not None:
            memo[key] = (state, got)
        return got

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

    @_in_step("SETTLE")
    def _settle_routine(self) -> None:
        """A routine that has ACTED is settled in the cycle whose observation decides it (F501;
        Fig 2). Its expectation, then one advance, read the state this cycle observed -- the state
        the next choose() would read -- so an ending is written here as SETTLE and a step is
        handed to that choose() without advancing twice (advance writes routine_state). A
        routine with no act yet is untouched: the zero-act ending stays in choose() (OPEN)."""
        if self.routine is None and self._routine_adopted is not None and self._routine_acts:
            # SPENT: its last act emptied the remainder (`advance` returns None), so it reached
            # no ending and its claim was never judged -- gridworld s0 re-adopted one such plan
            # three times and its claim abandoned a successor (F502). It is settled here: the
            # claim judged, then ended DONE if it held, or `completed-untested` if it made none.
            state = self.env.observe()
            claimed = self._expect is not None
            if self._check_expectation(state, step="SETTLE"):
                return
            self.routine = self._routine_adopted
            self._end_routine(Rt.DONE if claimed else "completed-untested", state, "SETTLE")
            return
        if self.routine is None or not self._routine_acts:
            return
        state = self.env.observe()
        if self._check_expectation(state, step="SETTLE"):
            return
        if self._routine_adopted is None:
            self._routine_adopted, self._plan_no = self.routine, self._plan_no + 1
        self.routine_state.pop("expect", None)
        emit, rest = Rt.advance(self.routine, self._holds(state, "SETTLE"),
                                self.routine_lib, self.routine_state)
        # DONE and EXHAUSTED are the ground's verdict on the plan. BLOCKED is not: an unreadable
        # guard is a channel fact (Fig 10), so it is handed on and ended at PLAN, with no verdict
        # (the reviewer 2026-10-07 16:58Z).
        if emit in (Rt.DONE, Rt.EXHAUSTED):
            slot, shown = self.routine_for or "*", Rt.render(self.routine)
            self._recovered_pending += [(w, slot, shown)
                                        for w in self.routine_state.pop("recovered", ())]
            self._end_routine(emit, state, step="SETTLE")
        else:
            self._routine_next = (self.routine, emit, rest)

    def _end_routine(self, why: str, before: dict, step: str | None = None,
                     detail: dict | None = None) -> None:
        """A routine's ending: its verdict, shelving, refutation and record. Run where the ending is
        evaluated -- at the deciding cycle's SETTLE for a routine that has acted (F501), at PLAN for
        an ending found while choosing (unrealisable, or the zero-act case left OPEN)."""
        # A CLAIM ENDS WITH THE PLAN THAT MADE IT (F502; the reviewer 2026-10-07 17:21Z): left
        # standing, an ended routine's expectation abandoned its successor (gridworld s0, c50).
        self._expect = None
        if why == Rt.DONE:
            _verdict = "tested_yes" if self._routine_acts else "tested_no"
        elif why == Rt.EXHAUSTED:
            _verdict = "tested_no"
        else:
            _verdict = None
        # THE EPISODE, FILED UNDER THE SHAPE OF THE GAP IT WAS FORMED AGAINST. Written
        # HERE because this is the only site where all four answers exist at once: the
        # signature was taken at mint, the actions are the routine's, the ending is `why`,
        # and the verdict is the emission count. Split them and the record cannot be made.
        if self._override_open is not None and _verdict:
            self._overrides.append((self._override_open, _verdict == "tested_yes",
                                    self.cycle))
        self._override_open = None
        if self.routine_for and self._plan_sig is not None:
            self._episodes.setdefault(self._plan_sig, []).append(
                (self._step_ids(self.routine, self.routine_lib), why,
                 _verdict or "untested"))
        if _verdict and self.routine_for:
            self._reach_tested[self._reach_key(
                self._reject_key(self.routine_for, self.routine,
                                 self.routine_lib))] = _verdict
            self.led.record(self.cycle, "SETTLE", self.routine_for, "reach_tested",
                            verdict=_verdict, ending=why, emitted=self._routine_acts,
                            routine=Rt.render(self.routine))
        # AND A ROUTINE THAT EMITTED NOTHING IS NOT SHELVED. Reaching `DONE` without acting
        # is not a settled behaviour -- it is a guard that was already true.
        _settled = self._routine_adopted or self.routine
        if (why == Rt.DONE and self._routine_acts
                and _settled not in self.routines):
            self.routines.append(_settled)
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
            self.refuted.setdefault(k, Standing(last_tick=self.cycle)).refute(
                self.cycle, self.gamma.halflife, where=self._scope)
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
            rk = self._refusal_key(gap, self.routine)
            self._refusals.setdefault(rk, []).append(self._refusal_scope())
            extra["refused_under"] = len(self._refusals[rk])
            if gap is not None:
                gk = (self._gap_key(gap), self._step_ids(self.routine, self.routine_lib),
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
        if detail:
            extra.update(detail)
        self.led.record(self.cycle, step or self._running_step, self.routine_for or "*",
                        "routine_end",
                        outcome=why, routine=Rt.render(self.routine), **extra)
        self._guard_exit = None
        self.routine, self.routine_for = None, None
        self._routine_adopted = None

    def _stale_sign(self, emit: Any, before: dict) -> dict | None:
        """R-dir (ii): the plan's premise is the sign it was minted with (Fig 12 :112); a live
        comparison reading the OPPOSITE sign ends it as "stale" (Fig 5, Fig 6) -- a non-trial, so
        no verdict and no refusal. An unreadable or held comparison is not an opposite reading
        (Fig 1; the reviewer's A1): None, and the routine runs as today."""
        sl = emit.subject
        if emit.kind != IFace.BECOME or emit.object not in ("+", "-") or sl not in before:
            return None
        keep = self._gt_which
        tgt = self._goal_target(sl, before)
        self._gt_which = keep
        if tgt is None:
            return None
        live = "+" if tgt > before[sl] else "-"
        if live == emit.object:
            return None
        return {"minted_sign": emit.object, "live_sign": live, "target": tgt,
                "at": before[sl], "subject": sl}

    def _subject_gap(self, before: dict) -> int | None:
        """R-dir (c): the body `_goal_want` is one BECOME on one slot, so the iterations it can
        spend are that subject's own gap (b-0's scope, carried to the budget): |target - now| on a
        signed want, 1 on a value want. The distance is objective_gap over the slot's domain, as
        goal_residual scores a subject want (`_goal_target` gives only the next step). None -- the
        group count stands -- where the body is not a BECOME intent or the gap is not readable."""
        w = self._goal_want
        if w is None or w.kind != IFace.BECOME or w.subject not in before:
            return None
        if w.value is not None:
            return 1
        sl = w.subject
        if w.object not in ("+", "-"):
            return None
        _, term = self._objective_of(sl) if _WANT_TARGET else self._target_lookup(sl)
        if (term is None or getattr(term, "out_type", None) != OBJ_TYPE
                or not self._applies(term, before)):
            return None
        ops = self._ops(term, before)
        if ops is None:
            return None
        ctx = self._eval_ctx(sl, before, action=self._last_action or "", operands=ops,
                             touching=self._touching(sl), shapes=False,
                             landed=self._last_landed)

        def _sat(v: int) -> bool | None:
            r = term.apply(v, ctx)
            return None if r is NOT_RESOLVED else bool(r)
        gap = objective_gap(_sat, before[sl], True, self._domain(sl, before, ctx))
        return gap if isinstance(gap, int) and not isinstance(gap, bool) and gap > 0 else None

    def _act_n(self) -> int:
        """Acts chosen so far, derived from `self._acts` (not a second counter): the act a claim is
        about is the one `step` counts right after `choose` returns it."""
        return sum(self._acts.values())

    def _check_expectation(self, before: dict, step: str | None = None) -> bool:
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
        slot, was, idx, *rest = exp
        setter, set_on, setter_no = (rest + [None, None, None])[:3]
        now = before.get(slot, was)
        if now != was:
            return False                      # the claim held; carry on
        saved = Rt.length(self.routine) if self.routine is not None else 0
        self.led.record(self.cycle, step or self._running_step, slot, "routine_abandoned",
                        reason="expected this slot to change and it did not",
                        # `step_index`, NOT `step`: `led.record`'s own first positional is
                        # `step`, so the obvious name silently shadowed it.
                        step_index=idx, unchanged_at=was, actions_saved=saved,
                        routine=Rt.render(self.routine) if self.routine else None,
                        set_by=Rt.render(setter) if setter is not None else None,
                        set_by_plan=setter_no,
                        held_plan=self._plan_no if self._routine_adopted is not None else None,
                        set_on_act=set_on, judged_after_act=self._act_n())
        self.routine, self.routine_for = None, None
        self._routine_adopted = None
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
                                 self._eval_ctx(slot, before, action=None,
                                                operands=ops, landed=None))
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
        self.led.record(self.cycle, self._running_step, "*", "books",
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
        self.led.record(self.cycle, self._running_step, "*", "vocabulary",
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

    def _trees(self, cand, bind, g, target=None):
        """The TREE variants of one flat candidate -- `f<g(s)>` for each branch atom.

        Empty unless the outer atom actually READS an operand and one is bound: a branch feeds
        the operand arm, so with nothing to feed it the tree is the flat term with a longer name.
        """
        if bind is None or not cand.reads_operand:
            return ()
        trees = (Term(cand.atoms, operand=bind, guard=g, operand_term=br)
                 for br in self._branches())
        return tuple(t for t in trees
                     if target is None or self._operand_fits(t, target, bind))

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
        self.led.record(self.cycle, self._running_step, "*", "placements",
                        distinct=p["distinct"], changed=len(p["multi"]))

    def _narrate_cues(self) -> None:
        """THE MUTATION OBSERVER, READ BY THE AGENT -- reviewer's ruling, 2026-09-26.

        `observe()` gives the agent VALUES. This gives it WHAT CHANGED and WHAT IS FIRING, which
        are different facts: a slot reading 4 says nothing about whether `position` mutated on two
        objects while `holes` mutated on none. **The mutation is what makes a search DIRECTED**
        -- the delta names which attributes to look up, instead of the whole space.

        `observer.py` held this the whole time and was imported ONLY by `test_perception.py`. Its
        single entry point took a LIST OF FRAMES, which on this project is a replay, which is the
        answer key -- so the shape of the door, not the room, is what kept the agent out.
        `observer.Live` is the same machinery fed one live grid at a time.

        **STORED ON THE AGENT, not only narrated.** A row is for the record; `self.cue` is what a
        consumer can read. Publishing to the ledger alone would be this project's own
        `a value that exists is not a value that crosses`, committed in the commit that cites it.

        NO CONSUMER YET, AND SAYING SO IS THE POINT. This is perception WIDENED and not yet
        SPENT: nothing in `choose` reads `self.cue` today. Under Figure 11 that makes this a
        contact change only if the agent can now reach something -- it cannot, until a consumer
        exists. **Reported as half a mechanism deliberately, because the other half is a
        judgement about what the agent should DO with a cue, and building both in one pass would
        bury that judgement inside a wiring commit.**
        """
        fn = getattr(self.env, "cues", None)
        if fn is None:
            return
        c = fn()
        if c is None:                      # blind frame: an ABSTENTION, not an empty reading
            _book_add(self.gamma.book, "cue_blind", 1)
            return
        self.cue = c
        muts = c["mutations"]
        loci = c["cue"].get("loci", {})
        if not c.get("first"):
            _book_add(self.gamma.book, "cue_seen", 1)
            if muts["attributes"]:
                _book_add(self.gamma.book, "cue_mutated", 1)
        self.led.record(self.cycle, self._running_step, "*", "cues",
                        mutated=dict(sorted(muts["attributes"].items())),
                        appeared=muts["appeared"], vanished=muts["vanished"],
                        objects=c["n_objects"], loci=len(loci),
                        primitives=sorted({p for ps in loci.values() for p in ps}))

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
        self.led.record(self.cycle, self._running_step, "*", "matches",
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
        self.led.record(self.cycle, self._running_step, "*", "cascade",
                        frames=len(frames), within_step=steps)

    def _two_readings(self, slot: str, ok: list, base: float) -> tuple:
        """7a(7): a plan is chosen on BOTH readings, never on their sum (Fig 12 :125, "A
        composition costs in two currencies, and they do not add"). Among the PAYING
        candidates, any plan another beats or ties in bits AND in confirm
        while beating it in one is dropped (Fig 13's spectrum orders without adding); the
        existing order (bits ascending, as `ok` is sorted) picks on the frontier, recorded.
        Ruin is not read here: a plan names intents, and its press is realised at execution,
        where 7a(5) C already withholds a vetoed press."""
        paying = [x for x in ok if pays(x[0], x[1], base)]
        if not paying:
            return ok[0]
        # 7a(9) MC4's READER: a plan whose need exceeds every reserve learned by running out
        # cannot finish, so it is dropped before dominance (an ORDER, like ruin), unless all are.
        # With no cap ending in the record it reads "no record" and drops nothing.
        unable = 0
        if _MC34:
            fits = [x for x in paying
                    if not self._cannot_finish(_confirm_actions(x[2]))]
            unable, paying = len(paying) - len(fits), (fits or paying)
        read = [(x, x[0] + x[1], _confirm_actions(x[2])) for x in paying]

        def beats(a, b) -> bool:
            if a[2] is None or b[2] is None:
                return False
            return a[1] <= b[1] and a[2] <= b[2] and (a[1] < b[1] or a[2] < b[2])
        frontier = [r for r in read if not any(beats(o, r) for o in read if o is not r)]
        pick = frontier[0][0]
        if _A1_TIES and len(frontier) > 1:     # A1: steps 3-5 on the frontier, never its order
            _a1k = self._choice("two_readings", slot,
                             [(Rt.render(x[2]), b, c) for x, b, c in frontier])
            pick = next(x for x, _b, _c in frontier if Rt.render(x[2]) == _a1k)
        self.led.record(self.cycle, "PLAN", slot, "two_readings", paying=len(paying) + unable,
                        unable_to_finish=unable, waiting=self._waiting_reading(),
                        dominated=len(read) - len(frontier),
                        frontier=[[Rt.render(x[2]), round(b, 4), c] for x, b, c in frontier],
                        pick=Rt.render(pick[2]), refute_min=1,
                        reads=("bits and confirm-actions held apart; the pick is the existing "
                               "order on the frontier"))
        return pick

    def _cannot_finish(self, need: int | None) -> bool:
        """7a(9) MC4's reader: True only when the need is known and exceeds every reserve the
        agent has learned by running out AT A SCOPE it would run out in -- this level's, or this
        run's -- each read against its own count (the reviewer 23:18Z)."""
        if need is None or not _MC34:
            return False
        m = self._mc4(None)
        return any(isinstance(r, list) and r and need > max(r)
                   for r in (m["reserve_level_seen"], m["reserve_run_seen"]))

    def _waiting_reading(self) -> dict | None:
        """7a(9) factor 8, Agency.order's reader (R3: "an advertised action whose settled effect on
        every controlled slot is null, while self-moved objects keep changing, IS waiting"). The
        actions that never moved a controlled slot, beside the objects H2 read as self-moved.
        None unless both exist (habitat: an ARC cascade, step 13). A reading, never a choice."""
        ctrl = self.agency.contingent()
        movers = sorted({o for (o, m) in self.agency.order if m == SELF_MOVED})
        if not ctrl or not movers:
            return None
        acts = sorted({a for (s_, a) in self.agency.tried if s_ in ctrl}
                      - {a for (s_, a), n in self.agency.moved.items() if s_ in ctrl and n})
        return {"wait": acts, "self_moved": movers} if acts else None

    def _cascade_agency(self) -> None:
        """H2: inside the last action, which sub-frame each object first changed in (a changed
        cell at its before or after position; a position two objects share is not read). Against
        the first sub-frame a CONTROLLED object (an action-contingent slot's owner) changed in:
        earlier, or with nothing controlled changing, is SELF-MOVED; the same sub-frame is moving
        WITH it; later and touching a controlled object is REACTING; later without contact has no
        mode. One frame is no order, never a mode (Fig 10's dropped transients; Fig 12's
        sequence bond: A then B, B needs A to have happened)."""
        casc = getattr(self.env, "cascade", None)
        if casc is None or not self.trace:
            return
        frames = casc()
        before, _a, after, _i, _l = self.trace[-1]
        if len(frames) < 2:
            self.agency.note_order(None)
            self.led.record(self.cycle, self._running_step, "*", "cascade_modes",
                            frames=len(frames),
                            modes=None, reads="one frame: no order, so no mode")
            return
        own = getattr(self.env, "slot_owner", None)
        att = getattr(self.env, "attribute_of", None)
        owners, attrs = (own() if own else {}), (att() if att else {})
        at: dict = {}
        for state in (before, after):
            pos: dict = {}
            for s_, v in state.items():
                if s_ in owners and attrs.get(s_) in ("row", "col"):
                    pos.setdefault(owners[s_], {})[attrs[s_]] = v
            for o_, p in pos.items():
                if "row" in p and "col" in p:
                    at.setdefault((p["row"], p["col"]), set()).add(o_)
        first: dict = {}
        for k, (a, b) in enumerate(zip(frames, frames[1:], strict=False)):
            for r, row in enumerate(a):
                for c, v in enumerate(row):
                    if b[r][c] != v and len(at.get((r, c), ())) == 1:
                        first.setdefault(next(iter(at[(r, c)])), k)
        controlled = {owners[s_] for s_ in self.agency.contingent() if s_ in owners}
        ks = [first[o_] for o_ in controlled if o_ in first]
        kc = min(ks) if ks else None
        touch = getattr(self.env, "contacts", None)
        near = touch() if touch else {}
        modes: dict = {}
        for o_, k in sorted(first.items()):
            if o_ in controlled:
                continue
            if kc is None or k < kc:
                modes[o_] = SELF_MOVED
            elif k == kc:
                modes[o_] = MOVES_WITH
            elif any(x in controlled for x in near.get(o_, ())):
                modes[o_] = REACTING
        self.agency.note_order(modes)
        self.led.record(self.cycle, self._running_step, "*", "cascade_modes", frames=len(frames),
                        modes=modes, first=first, controlled=sorted(controlled))

    def _narrate_order(self) -> None:
        """Layer 2's whole output: the order was USED and is SAID, and nothing keeps it."""
        ro = getattr(self.env, "read_order", None)
        if ro is None:
            return
        order, pattern = ro()
        self.led.record(self.cycle, self._running_step, "*", "read_order",
                        pattern=pattern, first=order[:3], n=len(order))
        md = getattr(self.env, "mode", None)
        if md is not None:
            m = md()
            self.led.record(self.cycle, self._running_step, "*", "mode",
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

    def _prev_of(self, state: dict, j: int = 1) -> dict | None:
        """The before-state j frames earlier than `state`: by position in the trace, or counted
        back from the trace's end for a live frame not yet in it. None before a trace's start."""
        idx = self._trace_pos
        if idx is None or idx[0] != len(self.trace) or idx[1] is not self.trace:
            idx = self._trace_pos = (len(self.trace), self.trace,
                                     {id(self.trace[i][0]): i for i in range(len(self.trace))})
        i = idx[2].get(id(state))
        if i is not None and self.trace[i][0] is state:
            return self.trace[i - j][0] if i >= j else None
        return self.trace[-j][0] if len(self.trace) >= j else None

    def _operand_value(self, name: str, state: dict):
        """The operand's reading on this frame, or NOT_RESOLVED where it did not exist."""
        lag = lag_of(name)
        if lag is not None:
            prev = self._prev_of(state, lag[1])
            return NOT_RESOLVED if prev is None else prev.get(lag[0], NOT_RESOLVED)
        return state.get(name, NOT_RESOLVED)

    def _applies(self, term: Term, state: dict[str, int]) -> bool:
        """Whether this term can be evaluated on this frame at all.

        A term reading an operand cannot be applied where that operand did not exist,
        which happens the moment a slot arrives mid-episode and something binds to it.
        INAPPLICABLE IS UNEXPLAINED, and every caller charges it as such: dropping the
        frame instead would let a term evaluable on half a history look like a perfect
        explainer, and evaluating it as if unary would silently change what it says.

        THE CHARGE STAYS IN THE BARGAIN, AND ONE FRAME KIND NO LONGER HOLDS A RESIDUAL OPEN (the
        reviewer 2026-10-08 06:43Z). A previous-frame operand cannot exist on a trace's first frame,
        on any board at any budget: that frame is the initial observation, not a miss (Fig 1,
        "residual R indexed by object slot"). It is still charged in `left` (Fig 5, "and so does a
        term that explains one occasion perfectly"), and recorded as a verdict with its k of n
        (Fig 13, "Unreachable is a verdict here, not a silence") -- see `_no_earlier_frame`. A slot
        that merely did not exist YET keeps the charge AND keeps the residual open.
        """
        op = term.operand
        if not op:
            return True
        # THE PLAIN READ INLINE: this runs on every candidate and every history row, and the
        # method call it replaces was ~15% of the prev operand's measured cost on gridworld s2.
        if "~" not in op:
            return state.get(op, NOT_RESOLVED) is not NOT_RESOLVED
        return self._operand_value(op, state) is not NOT_RESOLVED

    def _lag_evidence(self, slot: str, robs: list, j: int) -> dict:
        """Whether the residual names lag j (R-D3's correlation, Fig 9's description first): on
        the frames the held term got wrong, the outcome is a FUNCTION of the slot's own value j
        frames back -- no earlier value is followed by two outcomes -- and some earlier value
        recurs, so the claim could have been refuted and was not (the reviewer 18:10Z). A value
        repeat is one case; x_t = x_(t-2)+1 is another, which a repeat test misses."""
        seen: dict = {}
        pairs = recurred = 0
        functional = True
        for st, _a, actual, _i, _l in robs:
            v = self._operand_value(f"{slot}~{j}", st)
            if v is NOT_RESOLVED:
                continue
            pairs += 1
            if v in seen:
                recurred += 1
                if seen[v] != actual:
                    functional = False
            seen[v] = actual
        return {"j": j, "pairs": pairs, "recurred": recurred,
                "evidence": functional and recurred > 0}

    def _no_earlier_frame(self, term: Term, state: dict) -> bool:
        """Inapplicable by construction: the term reads j frames back and there are fewer."""
        lag = lag_of(term.operand)
        return lag is not None and self._prev_of(state, lag[1]) is None

    def _domain(self, slot: str, state: dict, ctx: Ctx):
        """WHERE AN OBJECTIVE ON `slot` IS SEARCHED: the values the slot has taken in the record
        BEFORE this frame, and each operand's value with its two neighbours -- where a comparison
        against it turns over (Fig 12). Inside the alphabet, which still bounds and prices.

        BEFORE THIS FRAME, so a replayed frame never searches a value shown after it: a domain
        holding the frame's own outcome would let the bet lean on it."""
        alpha = self.alphabet[slot]
        if not _OBJECTIVE_DOMAIN:
            return range(alpha)
        key = (id(self.trace), len(self.trace))
        if self._shown_key != key:
            self._shown_key, self._shown, self._frame_at = key, {}, {}
            for i in range(len(self.trace)):
                b, _act, _a, _intent, _landed = self.trace[i]
                self._frame_at[id(b)] = i
        first = self._shown.get(slot)
        if first is None:
            first = {}
            for i in range(len(self.trace)):
                b, _act, a, _intent, _landed = self.trace[i]
                for v, at in ((b.get(slot), i), (a.get(slot), i + 1)):
                    if isinstance(v, int) and v not in first:
                        first[v] = at
            self._shown[slot] = first
        # 7h SHOWN: the slot's value at each frame (frame i is trace[i]'s before, the last
        # frame the last after), so a value's frequency before this frame can be read
        seq = self._shown.get(("seq", slot)) if _7H_SHOWN else ()
        if seq is None:
            seq = [self.trace[i][0].get(slot) for i in range(len(self.trace))]
            if self.trace:
                seq.append(self.trace[-1][2].get(slot))
            self._shown[("seq", slot)] = seq
        n = self._frame_at.get(id(state), len(self.trace))
        dom = {v for v, at in first.items() if at <= n}
        for o in ctx.operands:
            if isinstance(o, int) and not isinstance(o, bool):
                dom.update((o - 1, o, o + 1))
        dom = {v for v in dom if 0 <= v < alpha}
        if not _A1_DOMAIN:
            return dom
        # A1 site 9: the rest of the alphabet stays reachable, priced by novelty (_priced_hit). The
        # least-known reading is presence: shown before this frame counts 1, an operand's
        # neighbour or an unseen value 0 (a per-value frequency is 7h's, named)
        out = _PricedDomain(dom)
        out.alpha, out.key = alpha, f"{self.cycle}:{slot}:objective_domain"
        out.seed = self.draw_seed
        out.counts = {v: 1 for v, at in first.items() if at <= n and 0 <= v < alpha}
        if _7H_SHOWN:
            for v in out.counts:
                out.counts[v] = max(1, sum(1 for x in seq[:n + 1] if x == v))
        out.note = partial(self._domain_row, slot)
        return out

    def _domain_row(self, slot: str, opts: list, pick: int, by: str, front: list) -> None:
        """A1 site 9's A2 row: both values on the frontier, their readings, the pick, its step."""
        self.led.record(self.cycle, self._running_step, slot, "choice", site="objective_domain",
                        options=len(opts), frontier=[[repr(v), b, a] for v, b, a in opts
                                                     if v in set(front)],
                        residual=None, seen=None, pick=repr(pick), by=by,
                        **({"root": self._root_id} if _7H_ROOT else {}))

    @_in_step("SETTLE")
    def _test_row(self) -> None:
        """7j: one SETTLE row per goal-exit test: the term, its prediction (the target), the slot
        before and after, the outcome by the slot's own type, and the 7h root it belongs to
        (in_root: the term is one of the root's held hypotheses)."""
        t, self._test = self._test, None
        slot = t["slot"]
        after = (self.trace[-1][2] if self.trace else {}).get(slot)
        ordered = self.slot_types.get(slot) in ORDERED_TYPES
        held = f"{slot}:{t['term']}" if t["term"] is not None else None
        self.led.record(self.cycle, "SETTLE", slot, "hypothesis_test", term=t["term"],
                        target=t["target"], before=t["before"], after=after, ordered=ordered,
                        outcome=_test_outcome(t["before"], after, t["target"], ordered),
                        intent=t["intent"], root=self._root_id,
                        in_root=held is not None and held in self._root_held)

    def _held_goal(self) -> list:
        """7h: the goal hypotheses the agent holds now, in its own terms (the held goal
        conditions, and each want as slot:term)."""
        return sorted(str(k) for k in self._goal_conds) + sorted(
            f"{s}:{t}" for s, t in self.wants.items())

    def _intent_root(self) -> None:
        """7h ROOT: what is shown (objects, and slots per attribute type, with what was added or
        is gone since the last root), what is expected (the held goal hypothesis, else "none
        held"), what is still open and owed. Interface-general: no button, coordinate or game
        name (A3). A record: no chooser reads it (A1)."""
        owners = {s.split(".")[0] for s in self.slots if "." in s}
        types = dict(sorted(collections.Counter(
            str(self.slot_types.get(s)) for s in self.slots).items()))
        shown = {"objects": len(owners), "slot_types": types}
        last = self._root_shown
        changed = None if last is None else {
            "objects": shown["objects"] - last["objects"],
            "added": sorted(set(types) - set(last["slot_types"])),
            "gone": sorted(set(last["slot_types"]) - set(types))}
        self._root_id = f"L{self.level}:E{self._epoch}"
        self._root_held = self._held_goal()
        self._root_shown = shown
        self.led.record(self.cycle, "PLAN", "@intent", "intent_root", root=self._root_id,
                        level=self.level, alive=self._alive, shown=shown, changed=changed,
                        expected=self._root_held or "none held",
                        open=sorted(s for s in self.slots if self.outstanding(s) > 0),
                        owed=sorted(self.owed_import),
                        reads="what is shown, what is expected, what is still open")

    @_in_step("SETTLE")
    def _intent_verdict(self, how: str) -> None:
        """7h GRADED: at the boundary the ground's ending under the root, and whether the held
        goal hypothesis was the one in force at the end. A record only."""
        if not _7H_ROOT or self._root_id is None:
            return
        self.led.record(self.cycle, "SETTLE", "@intent", "intent_verdict", root=self._root_id,
                        ending=how, held_in_force=self._held_goal() == self._root_held,
                        held=self._root_held or "none held")
        self._root_id = None

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
            return objective_step(_sat, state[slot], ordered, self._domain(slot, state, ctx))
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
        # **`_predict` IS THE CURRENT STEP, NOT A REPLAY ROW**, so its intent is the live one
        # rather than a row's. `NO_INTENT` when none was formed -- the explicit reading, so a
        # guard compares against a value instead of an absence.
        _now = self._intent_now.kind if self._intent_now is not None else NO_INTENT
        ctx = self._eval_ctx(slot, state, action=action, operands=ops, intent=_now,
                             touching=self._touching(slot), landed=self._last_landed,
                             guard_ref=term.guard_ref)
        got = self._value_of(term, slot, state, ctx)
        if got is NOT_RESOLVED:
            return None
        self._pred_raw[slot] = got
        return got % self.alphabet[slot]

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
            # **KERNEL A5's OWN KEY. Passing the slot is the fix** -- this line is the
            # consumer the defect was pinned to, and without the slot one settlement
            # anywhere licensed citation here.
            self._stood.append((slot, name, self.gamma.is_settled(name, slot)))

    @_in_step("PROMOTE")
    def _promote(self) -> None:
        """Step 6: what step 1 stood on, and what the sweep earned."""
        wait = []
        for name, shadow, echo in self._promotions:
            if self.gamma.is_primitive(name):
                continue
            # A PROMOTION IS TRUST, SO THE GROUND SPEAKS FIRST: a sweep's close waits until the term
            # has settled in this level; until then it is held, not dropped.
            if _PROMOTE_AFTER_SETTLE and name not in self._settled_lvl:
                wait.append((name, shadow, echo))
                continue
            self.gamma.promote(name, shadow, echo)
            self.led.record(self.cycle, "PROMOTE", echo["slot"], "promote", term=name,
                            primitive=True, shadow=shadow, echo=echo,
                            verdict="closed a residual recorded before it existed, "
                                    "on a slot it was not minted for")
        self._promotions[:] = wait

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

    @_in_step("PERCEIVE")
    def perceive(self, action: str,
                 coord: tuple[int, int] | None = None,
                 intent: Any = None) -> dict[str, SlotResidual]:
        before = self.env.observe()
        # A BET CAN ONLY BE MADE ON A SLOT THAT WAS THERE. With perception the slot set can
        # move WITHIN a step -- an object dies between the bet and the reading -- and
        # `_present` only catches that at step boundaries. So the bet is over `before`.
        betting = [s for s in self.slots if s in before]
        # ONE COMPUTATION PER STEP, AND IT MUST PRECEDE THE PREDICTION -- which is the
        # whole point and is where I first put it wrong. Placed after `pred` it was still
        # the step's reset `None` when `_predict` ran, so the guard stayed blind and the
        # refutation count did not move: 18 before, 18 after. The treatment-executed check
        # caught it. `_aimed` is set when the action is realised and cleared at the top of
        # the step, so here it is THIS step's aim -- the same value the trace row records.
        self._last_landed = self.iface._acted(getattr(self, "_aimed", None), before)
        self._press_seen = _press(getattr(self, "_aimed", None), before, self._last_landed)
        # **WHO MADE THIS PREDICTION -- the reviewer, 2026-10-04. PROVENANCE APPLIED TO
        # EVIDENCE.** Captured HERE, at the moment of the claim, because `route` binds
        # AFTER `perceive` returns and `settle` judges on THIS residual: a term bound
        # mid-step was being credited and blamed for a prediction made before it held the
        # slot. Measured: `o1.colour` is unbound at perceive-exit on 30 of 30 steps and
        # bound at settle-entry on 18 -- and those 18 are exactly the 18 refutations of a
        # term the habitat says is TRUE (`o1.colour` +1 mod 4 on 21 of 21 own clicks).
        if _D5 and (self._parts or self._d5_pending):
            self._d5_select(betting, before, action)
        # B2b (the reviewer 2026-10-11 10:30 CDT): a DERIVED slot (a pair relation the world
        # computes from other slots) is not an independent subject. It is not bet on; its
        # prediction is the world's own instrument applied to the PREDICTED sources, and it
        # enters the search only on a relational surprise (below). Fig 13: a member that draws
        # on the same evidence as others carries no information of its own.
        _derived = getattr(self.env, "derived", None)
        _derived = _derived() if _derived is not None else {}
        betting = [s for s in betting if s not in _derived]
        self._pred_by = {s: self.bound.get(s) for s in betting}
        pred = {s: self._predict(s, before, action) for s in betting}
        raw = {s: self._pred_raw.get(s) for s in betting if pred[s] is not None}
        # A SLOT THE BOUND TERM CANNOT READ IS NOT BET ON. §12.2's non-reading has to reach
        # somewhere that acts on it, or it is a sentinel that propagates into a shrug.
        for s in [s for s in betting if pred[s] is None]:
            self.led.record(self.cycle, "PERCEIVE", s, "unread", of=(s,),
                            bound=self.bound.get(s, NO_CHANGE),
                            reads=("the bound term returned no reading, so no bet is made and "
                                   "no prediction error is claimed on this slot"))
        betting = [s for s in betting if pred[s] is not None]
        _dpred: dict = {}
        if _derived:
            _ps = dict(before)
            _ps.update({s: (raw[s] if raw.get(s) is not None else pred[s]) for s in betting})
            _dpred = {k: v for k, v in self.env.derive(_ps).items() if k in _derived}
        self._derived_pred = _dpred
        _, deg_before = self.env.objective()
        _real = IFace.Realisation(action, coord)
        # **THE ACTING-OBJECT KEY WAS TRIED HERE AND MEASURED HARMFUL -- 2026-09-28, dropped
        # on the reviewer's ruling.** Keying on the actor's own contacts splits a remapped
        # action's presses across buckets so each holds ONE effect and nothing can be compared:
        # on fixture A it scored `[]` against the whole-board key's `[down, up]` -- same
        # precision, no recall. The matrix is in `docs/ACTION_INTERFACE_PLAN.md`.
        _ctx = IFace.Interface.context(self.env)
        if coord is not None:
            self.env.step(action, coord[0], coord[1])   # F28: positioned, coord from perception
        else:
            self.env.step(action)
        after = self.env.observe()
        # RE-READ AFTER THE OBSERVATION, BEFORE ANYTHING IS PRICED: a label the step created
        # was priced under the count from before it existed, so a new shape 8 read as 0 under
        # 8 and the miss cost nothing (8 of 12 games, 2026-10-07).
        # The alphabet the bets were made under: a slot that vanishes in this step is priced
        # from it (the reviewer 2026-10-12 16:12). Every slot in `betting` is a key of it by
        # construction: `betting` is drawn from `before`, read in the frame this was built in.
        bet_alphabet = self.alphabet
        self.alphabet = self._alphabets(self.env)
        # JOB B's HALF THAT RUNS TODAY: this action does not have ONE fixed effect.
        # **I WROTE HERE THAT IT CANNOT FIRE ON GRIDWORLD AND THE RUN DISPROVED IT** -- four
        # times in eight steps, because `down` is sometimes BLOCKED. The rule is invariant and
        # the outcome is not, so what fires is CONDITIONALITY, which is Isaiah's own separate
        # question. Telling it apart from *the mapping changed* needs a context key that does
        # not exist yet, so this claims the smaller thing and says so.
        # THE CONTEXT KEY IS READ BEFORE THE STEP, because it is the contact present WHEN THE
        # ACTION WAS TAKEN -- reading it after would key an effect by the world the effect made.
        if self.iface.audit(_real, before, after, _ctx,
                            IFace.Interface.context(self.env) if IFace._DEST_GAP else None):
            self.led.record(self.cycle, "PERCEIVE", "@interface", "conditional",
                            of=(action,), reads=("this action has now been seen to do more "
                                                 "than one thing -- it is conditional"))
        # AND WHAT THE BOARD NOW AFFORDS, **named as capability and never as a button** --
        # Isaiah: *"the board has enabled us to move to the left or right after doing xyz"*.
        # F28's line held: availability is legitimate to read, directional semantics never.
        # **REPORTED; NOT YET READ ABOVE THE SEAM; CONSUMED AFTER THE STRIP** -- the reviewer,
        # 2026-09-28, and it is owed at the site rather than only in the channel. `ISOLATED`
        # checks for a CALLER and not for a CONSUMER, so a report written to the record and
        # read by no mode passes it. **Nothing in systems 0, 1 or 2 reads this yet**, which is
        # why the commit that added it claims a RECORDED fact and not a changed decision.
        _cap = self.iface.capability(tuple(self.env.actions()), after=action)
        self._last_cap = _cap
        if _cap.moved():
            self.led.record(self.cycle, "PERCEIVE", "@interface", "capability",
                            of=tuple(_cap.opened + _cap.closed),
                            reads=("what the board affords has changed, stated as what became "
                                   "possible rather than as which action it is"))
        name, deg_after = self.env.objective()

        res: dict[str, SlotResidual] = {}
        # WHAT IS STILL LISTED, unreadable values included -- `observe` strips NOT_RESOLVED, so
        # `after` alone cannot tell an object gone from a reading the channel could not take.
        listed = set(self.env.slots()) if any(s not in after for s in betting) else ()
        for s in betting:
            # A READING THE CHANNEL COULD NOT TAKE IS SUSPENDED, NOT CHARGED -- Fig 10, the
            # reviewer 2026-10-07 (F493). The key is still listed, so the object is here and only
            # its value is unreadable: no bet is scored and no residual claimed, and the row says
            # so. Measured before: `o0.rem_row` billed 3.0 bits as a vanished object.
            if s not in after and s in listed:
                self.led.record(self.cycle, "PERCEIVE", s, "bet", channel=TRANSITION,
                                of=(s,), from_value=before[s], predicted=raw.get(s),
                                predicted_code=pred[s], suspended=True, mass=0.0,
                                bound=self.bound.get(s, NO_CHANGE),
                                meant=(intent.says() if intent is not None else None))
                continue
            # A SLOT THAT VANISHED UNDER THE BET IS UNEXPLAINED, not absent. The object was
            # there when the bet was made and is gone now, which is a full code's worth of
            # correction -- and `death only on evidence` means it went because its cells were
            # taken, so the disappearance is a reading rather than a gap. Same rule as
            # `_applies`: missing is charged, never skipped.
            gone = s not in after
            actual = pred[s] if gone else after[s]
            bits = (math.log2(bet_alphabet[s]) if gone
                    else correction_bits(pred[s], actual, self.alphabet[s]))
            r = SlotResidual(s, TRANSITION, pred[s], actual, bits, gone)
            res[s] = r
            # from_value is the input the bet was computed from, and it is the whole
            # difference between a bet on the BELIEF and one on the observation -- the
            # second has no model that could be wrong. It was always `before[s]`; it was
            # just never on the row, so nothing could tell the two apart.
            _bet = self.led.record(self.cycle, "PERCEIVE", s, "bet", channel=TRANSITION,
                            of=(s,),
                            from_value=before[s], predicted=raw.get(s), actual=actual,
                            predicted_code=pred[s],
                            alphabet=(bet_alphabet[s] if gone else self.alphabet[s]),
                            **({"vanished": True} if gone else {}),
                            mass=r.bits, cause=self._cause(s, r.bits),
                            # NOT `IDN`: an unbound slot rests on a persistence prior,
                            # and recording it as a term made 104 of 110 staleness
                            # readings noise. `_predict` still falls back to `idn`.
                            bound=self.bound.get(s, NO_CHANGE),
                            # **WHAT THE AGENT MEANT, ON THE ROW THAT RECORDS ITS BET.** It
                            # named neither the action nor the intent before, so the model's
                            # own record could not say what the prediction was made under.
                            # `None` where the action was handed in rather than asked for.
                            meant=(intent.says() if intent is not None else None),
                            )
            if _MC_SIGNAL:
                self._signals.append((_bet.seq, s, self.bound.get(s, NO_CHANGE)))
            self._standing(s)
        if _derived:
            self._relational_surprise(_derived, _dpred, res, after, before)
            self._blocked_reading(_derived, _ps, before, after, action)

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
        if _DIRECTION_MOVABLE:          # before Agency.note: the controlled set as it stood
            self._note_direction(action, before, after, sorted(res))
        self.agency.note(action, self._moved(res, before, after), sorted(res))
        self._integral += sum(r.mass for r in res.values())
        for _s, _r in res.items():
            self._outstanding[_s] = self._outstanding.get(_s, 0.0) + _r.mass
        live = any(r.mass > 0 for r in res.values())
        self.drive.note_step(live)      # once per step: SUPPORT is over slots, not per slot
        self.chain.note_diff(live)
        # **THE TRACE RECORDS WHAT WAS DONE *AND WHY* -- ISAIAH'S RULING 8, AT THE SOURCE.**
        # It carried `(before, action, after)` and never the intent, so every historical
        # replay -- `_left`, `_cannot_pay`, `_residual_obs` -- rebuilt a `Ctx` with no
        # intent in it. **That is why guards could not be re-keyed onto intents: the guard
        # is EVALUATED IN REPLAY, over rows that never carried the thing it would test.**
        # Found by starting that build and asking what the guard compares AGAINST.
        #
        # Stored as the KIND (ruling 3), so it is the same quantity the pricing counts.
        # **THE OBJECT THE PRESS LANDED ON RIDES AS A FIFTH FIELD.** Ruling 3 fixes the
        # intent column as the KIND, so widening it would change what `_guards` enumerates.
        # Deliberately NOT the intent's subject: `_aimed` is the coordinate the press was
        # REALISED at. **Reading the SUBJECT is what `a561fb2` did and was reverted for** --
        # the agent aims at one slot and the interface presses another to reach it.
        self.trace.append((before, action, after,
                           self._intent_now.kind if self._intent_now is not None
                           else NO_INTENT,
                           self._last_landed))
        # ONE CLOCK: the cycle, which a level boundary does not reset. The trace length did, so a
        # term's rejection froze at every boundary, while the halflife it decays at is in cycles.
        self.gamma.tick = self.cycle
        self._prev_pred = pred
        self._last_mass = {s: r.mass for s, r in res.items()}
        self._note_progress(after)
        self._note_goal_choice(action, before, after)
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
        # (c) ROUTE by design: this row records the routing perceive itself performs for the reward
        # slot, a later step carried out inside PERCEIVE (the reviewer 2026-10-16 09:23)
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

        IT EXCLUDES (corrected 2026-10-09): a NON-EMPTY kept set drops every slot outside it
        (`return keep or others`); only an EMPTY one falls back to the full list. So it is a
        cut, not an ordering, and arming it ON owes the must-hold the ~1 narrowing carries:
        no closer the unarmed run finds may be lost.
        """
        after_of = {id(b_): a_ for b_, _act, a_, _intent, _landed in self.trace}
        moved: set = set()
        for st, _a, _v, _intent, _landed in robs:
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
                    yield Term(term.atoms, operand=term.operand, guard=g,
                               operand_term=term.operand_term)
            return
        # ARM L AT THE LOOKUP'S OWN SITE. This loop is the other half of the operand axis and
        # was never bounded -- see `_delta_narrowed`. Same rule, same arm, one switch.
        cands = [b for b in self.slots if b != slot]
        if _DELTA_OPERANDS and robs:
            cands = self._delta_narrowed(cands, robs)
        for b in cands:
            if self._operand_fits(term, slot, b):
                for g in gs:
                    yield Term(term.atoms, operand=b, guard=g,
                               operand_term=term.operand_term)

    def _take_pull(self, n: str, cand: Term, slot: str, carry: dict | None = None) -> str:
        """Bind a library pull: install a re-binding if it is new, and write the pull row."""
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
        self.led.record(self.cycle, self._running_step, slot, "pull", term=n,
                        held=held, chain=" . ".join(a.name for a in cand.atoms),
                        rebound=held != n,
                        origin=(st or {}).get("origin"),
                        admitted=(st or {}).get("admitted"),
                        **({"carry": carry} if carry is not None else {}),
                        reads="a library entry REACHED FOR -- 14.7's bench pull")
        return n

    def _carry_credit(self, name: str, cand: Term, slot: str, left: float, base: float,
                      held: Term, robs: list | None) -> bool:
        """CARRY CREDIT (item 3). A MINTED term paid its cost at its own entry (DISCOVERY 503), so
        where it RE-GROUNDS -- pays on this slot's own record alone, `left < base` -- it is priced
        on its leftover. Never a prior or an import (nothing was paid), never pooled (one slot's
        record), never a spectator (`bears_on`)."""
        return ((self.gamma.stamps.get(name) or {}).get("origin") == MINTED and left < base
                and robs is not None and self.bears_on(cand, slot, robs, held))

    def _carry_ref(self) -> tuple[int, float]:
        """What naming one held term costs: log2(H+1), H the whole library as built (at least the
        fit's candidates), the +1 being none of them (mint instead). The form is `_guard_bits`'s,
        the corpus's."""
        h = len(self.gamma.library)
        return h, (math.log2(h + 1) if _CARRY_REF else 0.0)

    def _carry_note(self, name: str, slot: str, what: str) -> None:
        rec = self._carry_log.get((name, slot))
        if rec is not None:
            rec[what] += 1

    def _blocked_reading(self, derived: dict, pred: dict, before: dict, after: dict,
                         action: str) -> None:
        """B4, BLOCKED (the reviewer 2026-10-11 12:49 CDT), agent-side only -- the world's own
        answer is never read. A subject touching a partner before the step, which the agent's OWN
        prediction moved into the partner (boxes overlap), and which did not move: blocked by that
        partner. The subject's predicted slots carry it to the lookup as an effect (S7 cue)."""
        self._blocked_now = {}
        boxes = getattr(self.env, "boxes", None)
        if boxes is None:
            return
        pb, bb = boxes(pred), boxes(before)
        hit: dict = {}                                    # subject -> (partners, meant slots)
        for k, srcs in derived.items():
            subj, attr = k.split(".", 1)
            if relations.pair_attr(attr) != "touches" or before.get(k) != 1:
                continue
            x = attr.split("_", 1)[1]
            own = srcs[:len(srcs) // 2]
            if any(after.get(s) != before.get(s) for s in own):
                continue                                  # the subject moved
            meant = [s for s in own if pred.get(s) != before.get(s)]
            if not meant or subj not in pb or x not in pb or subj not in bb or x not in bb:
                continue                                  # no move predicted
            if not relations.overlaps(pb[subj], pb[x]) or relations.overlaps(bb[subj], bb[x]):
                continue                                  # not predicted INTO the partner
            ps, ms = hit.setdefault(subj, (set(), set()))
            ps.add(x)
            ms.update(meant)
        # EVERY PARTNER (the reviewer 13:07 CDT): one row per subject, the partners sorted, and the
        # slots map to the set -- never the first found.
        for subj in sorted(hit):
            ps, ms = hit[subj]
            for s in ms:
                self._blocked_now[s] = tuple(sorted(ps))
            self.led.record(self.cycle, "PERCEIVE", subj, "blocked", partners=sorted(ps),
                            action=action, predicted={s: pred.get(s) for s in sorted(ms)},
                            actual={s: after.get(s) for s in sorted(ms)},
                            reads="predicted into a partner it touched, and did not move")

    @staticmethod
    def _moved(res: dict, before: dict, after: dict) -> set:
        """Sensor 3 is defined on CHANGE (the reviewer 2026-10-11 12:49 CDT, ruled ungated): the
        slots whose VALUE differs, read from the same before/after the residual is computed from.
        It was fed the SURPRISED slots (mass > 0), so a well-predicted avatar dropped out of
        `contingent()` and a predicted move that did not happen counted as moved."""
        return {s for s in res if after.get(s) != before.get(s)}

    def _relational_surprise(self, derived: dict, dpred: dict, res: dict, after: dict,
                             before: dict) -> None:
        """B2b (d): a derived slot enters the search only when its observed value differs from
        the relation derived from the predicted sources WHILE every source prediction held --
        the genuinely relational residual (a blocked move: the mover was predicted to move,
        the gap to shrink, and it did not). One summary row per cycle keeps the rest legible."""
        held = surprised = 0
        for k, srcs in derived.items():
            if k not in dpred or k not in after:
                continue
            if not all(s in res and res[s].bits == 0 for s in srcs):
                continue                      # a source missed: its own residual carries it
            if after[k] == dpred[k]:
                held += 1
                continue
            surprised += 1
            bits = correction_bits(dpred[k] % self.alphabet[k], after[k], self.alphabet[k])
            res[k] = SlotResidual(k, TRANSITION, dpred[k] % self.alphabet[k], after[k], bits)
            self.led.record(self.cycle, "PERCEIVE", k, "relational_surprise", of=tuple(srcs),
                            from_value=before.get(k), derived=dpred[k], actual=after[k],
                            mass=bits, reads="the relation derived from the held source "
                                             "predictions did not hold")
        self.led.record(self.cycle, "PERCEIVE", "@derived", "derived", slots=len(derived),
                        predicted=len(dpred), held=held, surprised=surprised)

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
            slot, self.gamma.library[self.bound.get(slot, IDN)], hist), slot)
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
        self._lookup(slot, hist)
        # THE TRACK RECORD ENTERS HERE AND ONLY HERE. `track_of` decays on read, mirroring
        # `rejection_of`, so the order reads evidence of the current age rather than a total
        # frozen at whatever tick it was last touched.
        _gk = self._term_gkey(slot) if self._not else None
        _paying: list = []
        _today = None
        _held_t = self.gamma.library[self.bound.get(slot, IDN)]
        _carry_robs = (self._residual_obs(slot, _held_t, hist)
                       if _CARRY_PRICE and _BARGAIN_FIT else None)
        _h, _ref = self._carry_ref() if _CARRY_PRICE else (0, 0.0)
        for n in retrieval.retrieve(self.gamma.library, gap, track=self.gamma.track_of,
                                    youth=self.gamma.youth_of):
            if n == exclude or (self._not and self._term_refused(n, _gk)):
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
                # F32 ARM D, **ON BY DEFAULT SINCE 2026-09-30**. `_explains` is `_left(...) == 0.0`,
                # and ISAIAH RULED THAT OUT: *the residual NEVER fully closes -- the corpus would
                # have told you that. That kills `left == 0.0` outright.* Figure 5's "stating it,
                # PLUS WHAT REMAINS UNEXPLAINED AFTER IT" is vacuous under a zero-remainder rule,
                # and Figure 13 lists "no remainder left after each step" as a FAILURE condition.
                #
                # THE REPAIR EXISTED AND DID NOT REACH HERE, AND NOW IT DOES. The reuse sweep
                # cited F32 at its own site and accepted on the ONE BARGAIN while this path kept
                # the old test, so retrieval refused every partial improvement -- which is what
                # 200 `reach_failed` rows were, and the arity-2 split followed, a multi-slot
                # history rarely closing to zero. Same baseline as the sweep: what the currently
                # bound term leaves.
                if _BARGAIN_FIT:
                    _left = self._left(cand, slot, hist)
                    _cost = term_bits(self.gamma.length(cand, self._units_for(slot)),
                                      self.gamma.alphabet)
                    if _CARRY_PRICE:
                        # EVERY payer is collected and the lowest WHOLE price wins (H3: first is
                        # not best); `_today` is the one the arm-OFF walk would have returned.
                        if _today is None and pays(_cost, _left, _base):
                            _today = (n, cand.name)
                        _cred = self._carry_credit(n, cand, slot, _left, _base, _held_t,
                                                   _carry_robs)
                        _price = _ref + _left if _cred else _cost + _left
                        if _price < _base:
                            _paying.append((_price, len(_paying), n, cand, _cred, _left, _cost))
                        continue
                    if not pays(_cost, _left, _base):
                        continue
                elif not self._explains(cand, slot, hist):
                    continue
                return self._take_pull(n, cand, slot)
        if _paying:
            price, _o, n, cand, cred, left_, cost_ = min(_paying, key=lambda x: (x[0], x[1]))
            book = self.gamma.book
            if cred:
                book["carry_pull_credited"] = book.get("carry_pull_credited", 0) + 1
            else:
                book["carry_pull_uncredited"] = book.get("carry_pull_uncredited", 0) + 1
            if _today != (n, cand.name):
                book["carry_order_differs"] = book.get("carry_order_differs", 0) + 1
            carry = {"price": round(price, 4), "credited": cred, "left": round(left_, 4),
                     "held_terms": _h, "ref_bits": round(_ref, 4),
                     "cost": round(cost_, 4), "base": round(_base, 4), "paying": len(_paying),
                     "first_in_order": None if _today is None else _today[1],
                     "carried": (cred and (self.gamma.stamps.get(n) or {}).get("seq", 0)
                                 < self._seq_at_level)}
            out = self._take_pull(n, cand, slot, carry=carry)
            if cred:
                self._carry_log[(out, slot)] = {
                    "term": out, "slot": slot, "level": self.level, "cycle": self.cycle,
                    "frames": len(hist), "left": carry["left"], "base": carry["base"],
                    "carried": carry["carried"], "via": "pull", "settled": 0, "demoted": 0}
            return out
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

    def _eval_ctx(self, slot: str, state: dict, *, action, operands,
                  landed=None, intent=None, touching=None, shapes: bool = True,
                  guard_ref: str | None = None) -> Ctx:
        """THE ONE CONSTRUCTOR FOR A Ctx A TERM IS EVALUATED IN -- the reviewer, 2026-10-04.

        **`acted_self` WAS SET AT 3 OF 11 CONSTRUCTIONS AND THE THREE WERE THE PRICING
        FUNCTIONS**, so a guarded term read as IDENTITY wherever it was JUDGED. On
        `click_only` that refused all 23 perfect `?ACTED_SELF` candidates per seed.

        **AND THE ROOT WAS THE UNPACK, NOT THE CONSTRUCTOR.** `bears_on` looped
        `for state, action, _actual, *_ in robs` and threw `landed` away, so it had nothing
        to supply. A constructor alone would not have reached it.

        **WHAT IS UNIFORM HERE IS `acted_self` AND NOTHING ELSE.** `touching` is `None` on a
        REPLAY because contact is unknown there and `()` would file *I cannot see* as
        *nothing was touching*; `shapes` is absent at two goal sites. Flattening either would
        be a behaviour change smuggled inside a fix, so both stay explicit.

        **A LANDING IS ONLY AVAILABLE ON REPLAY.** The live callers have `_last_action` and no
        `_last_landed`, so they pass `landed=None` and read `acted_self` False exactly as
        before. They are routed so the next guarded caller is not blind -- NOT because this
        fixes them. `conform/census.py` asserts nothing builds one of these any other way.
        """
        memo, key = self._memo, None
        if memo is not None:
            key = ("ctx", slot, id(state), action, operands, landed, intent, touching, shapes,
                   guard_ref, self.cycle)
            try:
                hit = memo.get(key)
            except TypeError:                # an unhashable input: build it, do not cache it
                hit = key = None
            if hit is not None and hit[0] is state:
                return hit[1]
        ctx = Ctx(action=action, intent=intent, operands=operands, touching=touching,
                   # **AGAINST THE TERM'S OWN REFERENT WHEN IT HAS ONE.** `guard_ref`
                   # falls back to the slot, which is exactly what `ACTED_SELF` meant, so
                   # the collapse is behaviour-preserving for every term that had no
                   # referent. `_same_object` reduces both sides to their owner, so no new
                   # comparison is needed and no name crosses into the chain.
                   acted_self=_same_object(landed, guard_ref or slot),
                   cond_holds=bool(self._invented) and self._inv_holds(guard_ref, state),
                   group=self._group(slot, state), obj=self._record(slot, state),
                   shapes=self._shapes_now() if shapes else None)
        if key is not None:
            memo[key] = (state, ctx)
        return ctx

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
        # **`landed` WAS DISCARDED BY `*_` HERE AND THAT IS THE WHOLE DEFECT** --
        # the field the guard needs was not in scope to supply, so no change at
        # the constructor could have reached it.
        for state, action, _actual, _intent, landed in robs:
            # **`_applies` BEFORE `_ops`, WHICH EVERY OTHER CALLER DOES AND THIS ONE DID NOT.**
            # `_ops` is `state[term.operand]` with no guard; `_applies` exists for exactly the
            # case its docstring names -- *a term reading an operand cannot be applied where
            # that operand did not exist, which happens the moment a slot arrives mid-episode*.
            # `goal_residual` checks it and records `operand-unreadable`; this site crashed.
            #
            # LATENT UNTIL 2026-09-25: reaching it needs a frame in `robs` that lacks the
            # operand, and it took the accumulator committing plans the bargain had refused --
            # a different trajectory -- to produce one. **INAPPLICABLE IS UNEXPLAINED**, which
            # is what `ops is None` already means three lines down, so the frame is charged
            # rather than skipped and the fix changes no verdict it could already reach.
            if not self._applies(term, state) or (
                    held is not None and not self._applies(held, state)):
                ops = hops = None
            else:
                ops = self._ops(term, state)
                hops = self._ops(held, state) if held is not None else None
            ctx = self._eval_ctx(slot, state, action=action, operands=ops or (),
                                 landed=landed, guard_ref=term.guard_ref)
            got = self._value_of(term, slot, state, ctx) if ops is not None else NOT_RESOLVED
            if held is None:
                if got is not NOT_RESOLVED:
                    return True
                continue
            hctx = self._eval_ctx(slot, state, action=action, operands=hops or (),
                                  landed=landed,
                                  guard_ref=getattr(held, 'guard_ref', None))
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

    def _left(self, term: Term, slot: str, hist, ceiling: float | None = None,
              offset: float = 0.0) -> float:
        """What the term leaves unexplained across the slot's history, in bits.

        `ceiling` IS AN EXACT ABORT, NOT AN APPROXIMATION. Every term added here is
        non-negative -- `log2(alphabet)` or `correction_bits` -- so a running total that
        has reached the incumbent's can only grow past it. The caller compares with a
        STRICT `<`, so a candidate that returns an aborted total is one that could not
        have won. The winner is bit-identical; only the losers stop early.

        Default `None` leaves every existing caller walking the full history.

        **`offset` MAKES IT `pays`' OWN EXPRESSION -- 2026-10-06.** `mint` passes `ceiling=base,
        offset=cost`, so the abort is `cost + total >= base`, never `total >= base - cost`,
        which can disagree with `pays` at the last ulp. Float addition is monotone, so a
        partial total that fails `pays` is a full one that fails it. No mint site reads
        `left` from a term that does not pay. Default 0.0 adds exactly nothing.
        """
        total = 0.0
        for state, action, actual, intent, landed in hist:
            if ceiling is not None and offset + total >= ceiling:
                return total
            if not self._applies(term, state):
                total += math.log2(self.alphabet[slot])   # inapplicable is unexplained
                continue
            ops = self._ops(term, state)
            if ops is None:
                total += math.log2(self.alphabet[slot])   # unreadable operand, unexplained
                continue
            got = self._value_of(term, slot, state,
                                 self._eval_ctx(slot, state, action=action,
                                                operands=ops, intent=intent,
                                                landed=landed,
                                                guard_ref=term.guard_ref))
            if got is NOT_RESOLVED:
                total += math.log2(self.alphabet[slot])   # unread is unexplained
                continue
            total += correction_bits(got, actual, self.alphabet[slot])
        return total

    @_in_step("ROUTE")
    def route(self, res: dict[str, SlotResidual]) -> list[tuple[str, str, str | None]]:
        out = []
        for slot, r in res.items():
            if r.gone:
                filed = self._refuted_slot.pop(slot, None)
                self.led.record(self.cycle, "ROUTE", slot, "route", bin=None,
                                why_not=LEFT_BOARD, support=len(self.trace),
                                **({"refusal_not_priced": filed} if filed else {}))
                continue
            _dropped = None
            was_refused = self._refuted_slot.pop(slot, None)
            # ONLY WHILE THE REFUSED TERM'S RESIDUAL PERSISTS -- the reviewer 2026-10-07 14:58Z
            # (F498), superseding 13:06Z's "while this cycle's residual is nonzero", which could
            # never file a term wrong every other step: its refutation was read on its right step.
            # Fig 5's amendment ranks the wrong term by residual that PERSISTS and does not trend
            # down; a term that failed once and is right since is a recording of one occasion
            # (Fig 4) and stays tally evidence.
            # AND ONLY WHILE IT IS STILL THE TERM BOUND (Fig 1: blame only to the term that made
            # the prediction). Rebound in the cycle it was refused, the slot's new term may be
            # right, and filing the old term's window displaced it (gridworld s2, c39, F498).
            if (was_refused is not None and _REFUTED_BIN and self.bound.get(slot) == was_refused
                    and self._persists(was_refused, slot)):
                # ISAIAH'S SECOND CLAUSE -- *alternatives that DO work start to compete.*
                # `_library_fit` already takes an `exclude`, so asking it for the best fit
                # OTHER than the one just refused needs no new retrieval path. Standing still
                # fades through `rejections`, which is untouched: this changes what is ASKED
                # FOR, not the term's number.
                # ONE TYPE RULE FOR THE ONE ACT: THE SLOT'S -- the reviewer, 2026-10-07 13:57Z
                # (F497), superseding its own 2026-09-22 ruling (375ce42), which matched the
                # competitor to the REFUSED TERM's type. A competitor bind and a rebind are the
                # same act, so one rule: the term must fit what it is applied to (Fig 12; Fig 1,
                # the residual is per slot), and `_library_fit` already checks that with
                # `_may_bind`. Matching the wrong term's type assumed the answer looks like what
                # failed (Fig 5's amendment). Measured on gridworld seed 0, cycle 14: it dropped
                # an OBJ term (left 13.84 of base 24.22) and `mint` then bound a new OBJ term at
                # the same cost and the same remainder.
                # FILED HERE, PRICED AT MINT (the reviewer 2026-10-07 14:39Z): a refusal is made by
                # the mint operator (Fig 5's amendment), and the loop runs ROUTE then MINT, so
                # route only files the slot; `_price_refusal` takes it from `_refuted_slot`.
                self._refuted_slot[slot] = was_refused
                fit = self._library_fit(slot, was_refused)
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
                    fit, _dropped = None, "starved"   # let mint park it; the probe is what perturbs
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
                            why_not=WHY_NOT[b], support=len(self.trace),
                            # WHY THE BIN DROPPED ITS COMPETITOR, so the cause is read, not
                            # inferred (F497): a starved slot.
                            **({"competitor_dropped": _dropped} if _dropped else {}))
        return out

    # -- steps 3 to 5 -------------------------------------------------------------------

    def _cue_tags(self) -> dict:
        """This cycle's cue as a tag vector, CACHED PER CYCLE -- `_shapes_now`'s pattern and
        for its reason: `mint` asks once per stream per slot, and recomputing walks every
        object's attributes each time. The cue does not change inside a cycle."""
        c, m = self._cue_tag_cache
        if c != self.cycle:
            m = inherited.tags_of(self.cue)
            self._cue_tag_cache = (self.cycle, m)
        return m

    def _frontier_lookup(self, slot: str, key: tuple) -> tuple | None:
        """The slot's recorded search, if its scope key is unchanged; otherwise None."""
        e = self._frontiers.get(slot)
        return e if e is not None and e[0] == key else None

    def _frontier_store(self, slot: str, entry: tuple) -> None:
        self._frontiers[slot] = entry

    def _guard_scope(self, slot: str, robs: list, operand_binds: list) -> tuple:
        """The guards and referents the chain loop will walk -- the same expressions, which
        read no chain. In the key because `_separates` reads the WHOLE history, not only R, so
        a correct row can make a referent separate while the base stands still."""
        refs = self._guard_refs(slot, operand_binds)
        gs = self._guards(robs, slot, refs)
        sep = ([r for r in refs if self._separates(robs, slot, r)]
               if any(x in (ACTED_SELF, ACTED_ON) for x in gs) else [])
        return tuple(gs), tuple(sep)

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

    def _d5_holds(self, pred: str, slot: str, row: tuple | None = None) -> bool:
        """D5: does the held predicate P hold, on a history row or (row None) on this step."""
        owner = slot.rsplit(".", 1)[0]
        if row is None:
            if pred == ACTED_SELF:
                return _same_object(self._last_landed, owner)
            return (self._intent_now.kind if self._intent_now is not None else NO_INTENT) == pred
        return _same_object(row[4], owner) if pred == ACTED_SELF else row[3] == pred

    def _d5_cut(self, slot: str, name: str) -> tuple | None:
        """D5's trigger (Fig 9 :4-5): a held predicate P with the incumbent right on every P row
        and wrong on every other, at least 2 a side (probe.never_live's anchor: two is the
        smallest number that separates), and the split pays: the incumbent's miss on the not-P
        rows exceeds the guard's cost. Only predicates the agent already holds (Fig 6 :32)."""
        term = self.gamma.library.get(name)
        # THE TERM'S OWN RECORD, SCOPED BY THE LEVEL (the reviewer 16:24Z): every row on which
        # THIS term predicted the slot in this level, across any demote or rebind. A boundary the
        # agent produces (its own demote) may not decide which evidence counts (Fig 1 :27).
        idx = [i for i, n in self._d5_rows.get(slot, ()) if n == name]
        hist = [(b, a, af[slot], i, land) for b, a, af, i, land in
                (self.trace[j] for j in idx if 0 <= j < len(self.trace))
                if slot in af and slot in b]
        if term is None or len(hist) < 4:
            return None
        wrong = [bool(self._residual_obs(slot, term, [r])) for r in hist]
        preds = sorted({r[3] for r in hist if r[3] is not None})
        if _ACTED_GUARD:
            preds.append(ACTED_SELF)
        for pred in preds:
            on = [self._d5_holds(pred, slot, r) for r in hist]
            right_p = sum(1 for o, w in zip(on, wrong, strict=True) if o and not w)
            wrong_np = sum(1 for o, w in zip(on, wrong, strict=True) if not o and w)
            if right_p < 2 or wrong_np < 2 or right_p + wrong_np != len(hist):
                continue
            miss = self._left(term, slot, [hist[i] for i, o in enumerate(on) if not o])
            cost = _guard_bits(pred, len(preds))
            if miss > cost:
                return pred, {"right_on_p": right_p, "wrong_off_p": wrong_np,
                              "incumbent_miss_bits_off_p": round(miss, 3),
                              "guard_bits": round(cost, 3)}
        n_right, n_wrong = wrong.count(False), wrong.count(True)
        if n_right >= 2 and n_wrong >= 2 and (slot, name) not in self._d5_said:
            # A UNION THE HELD PREDICATES DO NOT SEPARATE: recorded once, never split (design 5).
            self._d5_said.add((slot, name))
            self.led.record(self.cycle, "SETTLE", "@d5", "not_split", split_slot=slot, term=name,
                            right=n_right, wrong=n_wrong, predicates=preds,
                            reason="no held predicate separates the term's right rows from its "
                                   "wrong rows in this level")
        return None

    @_in_step("MINT")
    def _flush_probe(self, turned: set) -> None:
        """THE PROBE'S RECORD. ONE ROW PER SLOT THAT ASKED FOR IT, and `@probe` only when the
        trigger was the global reading rather than any particular slot -- so a slot parked at
        no_support can be matched to the probe that answered it (B5). A starved slot whose own
        turn already ran this cycle takes NO MINT row after its ACCEPT (F500; the reviewer
        2026-10-14 07:33). The probe's act was taken at the top of the cycle; this only records."""
        late = sorted(s for s in self._starved if s in turned)
        due = [s for s in sorted(self._starved) if s not in turned] or ([] if late else ["@probe"])
        for slot in due:
            self.led.record(self.cycle, "MINT", slot, "probe",
                            **self.drive.report(),
                            guards={"support": False, "reachability": False,
                                    "novelty": False},
                            note="support at zero; the model does not choose this one")
        if late:
            self.led.record(self.cycle, "MINT", "@probe", "probe", **self.drive.report(),
                            already_turned=late,
                            reads=("starved slots whose own turn ran this cycle: the probe "
                                   "answered them, recorded here and not after their ACCEPT"))
        self._starved.clear()

    @_in_step("MINT")
    def _d5_splits(self, gone: frozenset = frozenset()) -> set:
        """D5: run the pending splits, before the route loop, which skips the slots split here.
        A SPLIT IS ITS SLOT'S TURN THIS CYCLE (F500; the reviewer 2026-10-11 22:59 CDT): part B's
        mint is the slot's one chain, so the slot leaves _turn_ahead AFTER _d5_split returns --
        never before, so the split's own mint sweeps as it did. Left in, a later mint's sweep this
        cycle reached the split slot: MINT after its ACCEPT, and an install path into a slot
        whose chain had run (the ALL-ON fake of panel c05a4bd, 14 rows on 6 of 7 splits)."""
        done: set = set()
        if _D5 and self._d5_pending:
            for _slot in sorted(self._d5_pending):
                if _slot in gone:
                    self.led.record(self.cycle, "MINT", _slot, "d5_split_not_run",
                                    reason="pending split not run: left the board")
                    continue
                self._d5_split(_slot, *self._d5_pending[_slot])
                done.add(_slot)
                if self._turn_ahead is not None:
                    self._turn_ahead.discard(_slot)
            self._d5_pending.clear()
        return done

    @_in_step("MINT")
    def _d5_split(self, slot: str, pred: str, numbers: dict, inc: str | None = None) -> None:
        """D5: part A keeps the incumbent on P rows; part B is searched by the SAME mint on the
        not-P rows alone (history filtered), and its verdict stays the part's: the slot's park
        state, wants and binding are restored after, so a part never speaks for the slot."""
        inc = inc or self.bound.get(slot)
        if not inc:
            return
        owed, abst = slot in self.owed_import, self.abstained.get(slot)
        want, want_t = self.wants.get(slot), self._want_terms.get(slot)
        self.bound.pop(slot, None)
        self._row_filter[slot] = lambda r, _p=pred, _s=slot: not self._d5_holds(_p, _s, r)
        self._mint_part = {"part": f"!{pred}", "slot": slot, "incumbent": inc}
        try:
            self.mint(slot)
            got = self.bound.get(slot)
        finally:
            self._row_filter.pop(slot, None)
            self._mint_part = None
        part_b = got if got and got != inc else None
        (self.owed_import.add if owed else self.owed_import.discard)(slot)
        for store, val in ((self.abstained, abst), (self.wants, want), (self._want_terms, want_t)):
            if val is None:
                store.pop(slot, None)
            else:
                store[slot] = val
        self.bound[slot] = inc
        self._parts[slot] = {"P": pred, "A": inc, "B": part_b}
        self.led.record(self.cycle, "MINT", "@d5", "split", split_slot=slot, P=pred,
                        part_a=inc, part_b=part_b or "parked (its own park row names the part)",
                        **numbers)

    def _d5_select(self, betting: list, before: dict, action: str) -> None:
        """D5: the part whose guard holds predicts this step; on a not-P step the incumbent's
        prediction is kept as a SHADOW (not a bet, not acted on, not settled). A cut found at
        the last settle is a partition from THIS step: its split runs in route, after the bet,
        so without this the incumbent was charged for a not-P row (s1, c30: demoted by it)."""
        parts = {**{s: {"P": c[0], "A": c[2], "B": None} for s, c in self._d5_pending.items()},
                 **self._parts}
        for slot, part in parts.items():
            if slot not in betting:
                continue
            if self._d5_holds(part["P"], slot):
                self.bound[slot] = part["A"]
                self._shadow.pop(slot, None)
                continue
            self.bound[slot] = part["A"]
            self._shadow[slot] = self._predict(slot, before, action)
            if part["B"]:
                self.bound[slot] = part["B"]
            else:
                self.bound.pop(slot, None)

    def _d5_witness(self, slot: str, name: str, r: SlotResidual) -> None:
        """D5: the candidate cut's witness -- the first not-P step after the cut on which the
        incumbent itself predicted. Wrong there: the claim held on a row it did not see, and the
        split takes effect from the next perceive. Right: the claim is refuted, nothing acted."""
        c = self._d5_candidates[slot]
        if c[2] != name:
            self._d5_candidates.pop(slot)
            self.led.record(self.cycle, "SETTLE", "@d5", "cut_withdrawn", split_slot=slot,
                            P=c[0], incumbent=c[2], predictor=name, verdict_on_the_cut=None,
                            reason="another term predicts the slot, so no witness can arrive")
            return
        if self._d5_holds(c[0], slot):
            # THE P SIDE IS A WITNESS TOO (the reviewer 20:30Z): the cut also claims the
            # incumbent is right on P. Wrong there refutes it; right there is no news.
            if r.mass > 0.0:
                self._d5_candidates.pop(slot)
                self.led.record(self.cycle, "SETTLE", "@d5", "cut_refuted", split_slot=slot,
                                P=c[0], incumbent=name, actual=r.actual, side="P",
                                verdict="the incumbent was wrong on a P row after the cut")
            return
        self._d5_candidates.pop(slot)
        if r.mass > 0.0:
            self._d5_pending[slot] = c
            self.led.record(self.cycle, "SETTLE", "@d5", "cut_confirmed", split_slot=slot,
                            P=c[0], incumbent=name, actual=r.actual)
        else:
            self.led.record(self.cycle, "SETTLE", "@d5", "cut_refuted", split_slot=slot, P=c[0],
                            incumbent=name, actual=r.actual, side="not-P",
                            verdict="the incumbent was right on the first not-P step after the cut")

    @_in_step("SETTLE")
    def _d5_level_end(self) -> None:
        """D5: the level is the cut's scope, so what is outstanding at its end leaves with a row.
        A candidate or a confirmed-but-unsplit cut is WITHDRAWN (no witness can arrive); a live
        split is dissolved with the level as its reason."""
        for slot, c in self._d5_candidates.items():
            self.led.record(self.cycle, "SETTLE", "@d5", "cut_withdrawn", split_slot=slot,
                            P=c[0], incumbent=c[2], verdict_on_the_cut=None,
                            reason="the level ended before a witness")
        for slot, c in self._d5_pending.items():
            self.led.record(self.cycle, "SETTLE", "@d5", "cut_withdrawn", split_slot=slot,
                            P=c[0], incumbent=c[2], verdict_on_the_cut="confirmed",
                            reason="the level ended before the confirmed split ran")
        for slot, part in self._parts.items():
            self.led.record(self.cycle, "SETTLE", "@d5", "dissolved", split_slot=slot,
                            P=part["P"], demoted=None, part_a=part["A"], part_b=part["B"],
                            reason="the level ended")

    def _d5_revert(self, slot: str) -> None:
        """D5: the incumbent was right on a not-P step, so the partition claim is broken."""
        part = self._parts.pop(slot)
        self.bound[slot] = part["A"]
        self.led.record(self.cycle, "SETTLE", "@d5", "partition_broken", split_slot=slot,
                        P=part["P"], incumbent=part["A"], unbound=part["B"],
                        verdict="the incumbent was right on a not-P row; the split reverts")

    def _d5_dissolve(self, slot: str, name: str) -> None:
        """D5: a part's term was demoted by the normal path; the split goes with it."""
        part = self._parts.pop(slot)
        self._shadow.pop(slot, None)
        self.led.record(self.cycle, "SETTLE", "@d5", "dissolved", split_slot=slot, P=part["P"],
                        demoted=name, part_a=part["A"], part_b=part["B"])

    def _residual_obs(self, slot: str, term: Term, hist: list) -> list:
        """R, DESCRIBED: the observations the bound term got wrong. Step 2 already sorts
        the residual and names what changed; this is the same object handed to step 3
        instead of being recomputed as a scalar."""
        out = []
        for state, action, actual, intent, landed in hist:
            if not self._applies(term, state):
                out.append((state, action, actual, intent, landed))   # inapplicable is unexplained
                continue
            ops = self._ops(term, state)
            if ops is None:
                out.append((state, action, actual, intent, landed))   # unreadable, unexplained
                continue
            got = self._value_of(term, slot, state,
                                 self._eval_ctx(slot, state, action=action,
                                                operands=ops, intent=intent,
                                                landed=landed,
                                                guard_ref=term.guard_ref))
            if got is NOT_RESOLVED or got % self.alphabet[slot] != actual % self.alphabet[slot]:
                out.append((state, action, actual, intent, landed))
        return out

    def _cannot_pay(self, term: Term, slot: str, robs: list, cost: float,
                    base: float, rkey: dict | None = None) -> bool:
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
        self._priced += 1
        unit = math.log2(self.alphabet[slot])
        # INCREMENTAL, AND EXACT BECAUSE `wrong` IS A PREFIX SUM. Each row adds 0 or 1 and
        # no row reads another, so a tally over the first N rows stays true as rows are
        # appended -- and `robs` only ever grows by appending while `rkey` is unchanged.
        # The abort below stores its PARTIAL total with the count it covered, so a refusal
        # is resumed rather than recomputed.
        cell = rkey if _TALLY else None
        wrong, start = 0, 0
        if cell is not None:
            seen = cell.get(term)
            if seen is not None:
                start, wrong = seen
                if start > len(robs):
                    start, wrong = 0, 0     # shrank under us: the triple did not separate them
                elif cost + unit * wrong >= base:
                    return True             # the stored prefix already proves it
        for i in range(start, len(robs)):
            state, action, actual, intent, landed = robs[i]
            # `_ops` was called TWICE per row here -- once to test for None and again to
            # build the Ctx -- while `_left` next door hoists it. Pure function of
            # (term, state), so hoisting is exact; it halves the hottest callee in the
            # profile. Nest rather than chain the `elif`, or the hoist just moves the
            # double call onto `_applies`.
            if not self._applies(term, state):
                wrong += 1                            # inapplicable is unexplained
            elif self._out_of_step_range(term, slot, state, actual):
                wrong += 1                            # P6: no reachable value equals `actual`
            else:
                ops = self._ops(term, state)
                if ops is None:
                    wrong += 1                        # unreadable operand is unexplained
                else:
                    got = self._value_of(term, slot, state,
                                         self._eval_ctx(slot, state, action=action,
                                                        operands=ops, intent=intent,
                                                        landed=landed,
                                                        guard_ref=term.guard_ref))
                    wrong += (got is NOT_RESOLVED
                              or got % self.alphabet[slot] != actual % self.alphabet[slot])
            if cost + unit * wrong >= base:
                if cell is not None:
                    cell[term] = (i + 1, wrong)
                return True          # `wrong` only grows; the rest of R adds nothing
        if cell is not None:
            cell[term] = (len(robs), wrong)
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

        The exits: routine (a held or just-minted routine's step), probe, system0, distinguish,
        discriminate:goal, draw. LIBRARY TERMS REACH THE ACTION AT TWO OF THEM, and only as the
        GOAL, never as the route: discriminate:goal reads the bound or wanted OBJ term to pick
        what to reach (`_goal_target`) while the interface's table picks the press; a routine's
        guards re-read that objective every step. probe, system0, distinguish and draw read no
        library term. 5b's `gamma_read["fed"]` records which term fed the exit that returned.

        CORRECTED 2026-10-10 (5b's census, the reviewer 12:27Z): this said no branch reads the
        bound term or the objective, and described the discriminate spread branch as live. That
        branch was deleted 2026-09-28 (option A: it ranked buttons with the agent's own model).
        """
        # PER STEP (5b; the reviewer 12:27Z): `_gamma_read` was set only at one branch, so a
        # routine or probe exit carried the PREVIOUS cycle's value onto its REPEAT row.
        self._gamma_read = {}
        self._split_term, self._routine_fed, self._last_real = None, [], None
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
        for _why, _slot, _shown in self._recovered_pending:
            self.led.record(self.cycle, "PLAN", _slot, "routine_recovered", outcome=_why,
                            routine=_shown,
                            note="a fallback ran; the body's ending is NOT a refutation")
        self._recovered_pending = []
        _next, self._routine_next = self._routine_next, None
        if _next is not None and _next[0] is not self.routine:
            _next = None                      # advanced for a routine no longer held
        if self.routine is not None and _next is None:
            self._check_expectation(before)
        if self.routine is not None:
            # CAPTURED AT THE FIRST ADVANCE, NOT ONLY AT THE MINT. A routine can arrive
            # without passing through `_mint_routine` -- a seat plants one, and a routine
            # that survived a boundary is already in hand -- and this is the last moment the
            # object is still the plan rather than a remainder.
            if self._routine_adopted is None:
                self._routine_adopted, self._plan_no = self.routine, self._plan_no + 1
            if _next is not None:
                _, emit, rest = _next         # advanced at its deciding cycle's end (F501)
            else:
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
            _stale = (self._stale_sign(emit, before)
                      if _ROUTINE_STALE and isinstance(emit, IFace.Intent) else None)
            _act = (None if _stale is not None or emit in (Rt.DONE, Rt.BLOCKED, Rt.EXHAUSTED)
                    else self._realise_step(emit, before))
            if _act is not None:
                # THE CLAIM, MADE BEFORE THE ACTION LANDS. `advance` published which slots this
                # step expects to move; the value is recorded NOW so next cycle compares against
                # what was true when the claim was made, not against a later frame.
                want = (self.routine_state.get("expect") or [None])[0]
                if want is not None:
                    self._expect_step += 1
                    # THE SETTER RIDES WITH THE CLAIM (F502), so an abandonment can show whose
                    # claim failed: the plan that made it, never its successor's.
                    self._expect = (want, before.get(want), self._expect_step,
                                    self._routine_adopted, self._act_n() + 1, self._plan_no)
                self._routine_acts += 1
                self.routine = rest
                self._routine_fed = self._routine_entries() if _FED else []
                return _act, "routine"
            # ENDED, AND THE FIVE ENDINGS ARE NOT ONE. `done` is the guard met; `exhausted` is
            # the budget spent without it -- the routine's own bet REFUTED; `blocked` is a
            # guard that could not be read; and an action this level does not advertise is a
            # routine that survived a boundary into a world that cannot run it. **Isaiah ruled
            # routines survive boundaries, and this is the other half of that ruling: it fails
            # its guard rather than crashing.**
            #
            # **AND `unrealisable` IS THE FIFTH -- the plan's 16e.** The body holds an INTENT and
            # the interface has nothing here that serves it. That is neither *the guard says no*
            # nor *the budget ran out*, and folding it into either would collapse two endings
            # into one -- `F207`'s defect exactly. It is a NON-TRIAL like the two beside it: the
            # plan never got to run, so it says nothing about whether the plan works.
            why = ("stale" if _stale is not None
                   else emit if emit in (Rt.DONE, Rt.BLOCKED, Rt.EXHAUSTED)
                   else Rt.UNREALISABLE if isinstance(emit, IFace.Intent)
                   else "unadvertised")
            # **THE ASSUMED -> TESTED UPGRADE, AND IT IS THE CALLER'S BY CONSTRUCTION.**
            # `reach_status` returns only `assumed_yes`/`unknown` and says why: it sees the
            # SHAPE, and `tested_*` are claims about what HAPPENED. Nothing had ever made one.
            # Reviewer, 2026-09-25, from the JPL rover record: their estimates are PESSIMISTIC
            # and execution RELEASES the slack, so a wrong prior costs one cycle. Ours is
            # optimistic -- `reach(Until)` is `budget * reach(body)` -- so a wrong prior costs
            # a shelved lie. This does not invert the prior; it records what the run showed.
            #
            # DONE WITH ZERO ACTIONS IS THE CASE THAT MATTERS: the guard already held, the
            # routine ended before acting, and `DONE` is what SHELVES it -- so without this it
            # would be filed as a settled behaviour, callable at a name's price while claiming
            # its budget's reach. `exhausted` is a trial that failed; `blocked` and
            # `unadvertised` are NON-TRIALS and say nothing either way, so they are left alone.
            self._end_routine(why, before, detail=_stale)
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
            pick = sorted(self._starved)[0]
            if _A1_STARVED and len(self._starved) > 1:
                # A1: what is unexplained NOW gates and ranks; then the less-probed; then the draw
                pick = self._choice("starved", None, [(s, None, None) for s in self._starved],
                                    {s: self.outstanding(s) for s in self._starved},
                                    {s: self._probe_n[s] for s in self._starved})
            self._probe_n[pick] += 1
            aim = pick.rsplit(".", 1)[0]
            self._s0_target = aim
            # **ONE INTENT, NOT A MODALITY CHOICE -- the plan's 19.** This read
            # `"ACTION6" if "ACTION6" in self.actions else self._toward(...)`, which is the
            # agent picking between two ways of touching something. It asks to touch.
            _t = self.iface.realise(IFace.Intent(IFace.TOUCH, object=aim),
                                    tuple(self.actions),
                                    IFace.Interface.context(self.env), before, self.env,
                                    withheld=self._withheld)
            act = (self._took(_t, IFace.Intent(IFace.TOUCH, object=aim))
                   if _t is not None else None)
            if _t is not None:
                self.led.record(self.cycle, "PLAN", aim, "intent",
                                reads=(f"{IFace.TOUCH} {aim}", _t.why))
            if act is None:
                act = self._undirected(before)
            return act, "probe"
        if self.drive.bored():
            # AND THE AIM IS CLEARED. `_s0_target` survives until `retarget`, so an ordinary
            # bored probe would otherwise inherit whatever arm M last pointed at and coordinate
            # an unrelated action on a stale slot.
            self._s0_target = None
            return self._explore(before), "probe"
        # **THE `discriminate` SPREAD BRANCH IS DELETED -- reviewer, 2026-09-28, option A.**
        # It enumerated Gamma's val->val closure, scored EACH ACTION by how many distinct values
        # the candidates predicted under it, and returned `max(self.actions, key=spread)`.
        # **That is the agent ranking BUTTONS with its own model**, the same crossing as the
        # `_predict` vote deleted at `4c233db`, and the ruling forbids it.
        #
        # AND IT COULD NOT FIRE HERE ANYWAY, structurally rather than by measurement: the live
        # ARC set has 62 atoms, yields 7 val->val candidates, 0 of them guarded and 0 reading
        # `ctx.action` -- so `spread` was a constant function of the action and `max == min`
        # always. The control was the toy set, whose `act` DOES read it. **Its only demonstrated
        # firing (33/96) is on a set containing `act`, and `act` is the handed answer.**
        #
        # **WHAT GOES WITH IT IS REAL AND IS NOT LOST -- the reviewer's addition, and it is the
        # part worth keeping in view.** Choosing the move that best SEPARATES competing
        # hypotheses is System 2 reasoning, and it returns AT THE INTENT LEVEL: the agent picks
        # the INTENT whose predicted outcomes differ most across its hypotheses, and the
        # interface realises it. That needs intent-level prediction -- `(before, INTENT, after)`
        # -- which the plan already owes. **The variety rule is NOT that**: variety is a
        # constraint against repeating, not a choice between hypotheses, and treating it as the
        # replacement would have quietly downgraded discrimination to exploration.
        #
        # `_gamma_read` STAYS AND NOW REPORTS ONE FACT HONESTLY. It existed to separate *the
        # gate was never entered* from *Gamma was consulted and came out flat*. There is no
        # longer a consulting branch, so `spread_split` would be a field that can only ever read
        # `None` -- a value that exists and never crosses. `owed` is still worth publishing:
        # it is what the deleted branch keyed on and what an intent-level discriminator will
        # key on next.
        owed = [s for s in sorted(self.owed_import) if s in before]
        self._gamma_read = {"owed": len(owed), "entered": False,
                            "note": "the spread branch is deleted; discrimination returns at "
                                    "the intent level"}
        # SYSTEM 0 -- Isaiah: start random, then jump to strategy. While the agent lacks the
        # contingency evidence to be strategic -- a surfaced action not yet tried at >=2 distinct
        # states, probe.py's `never_live` anchor -- draw variously INSTEAD of exploiting the
        # learned arm, so it generates the (before, action, after) evidence binding needs. The
        # switch is state-derived (coverage), never a cycle constant -- and ALWAYS ON as of
        # Isaiah's 2026-09-29 ruling, so the only gate left is whether the state calls for it.
        if self._system0_active():
            target, why = self._contact_target(before)
            self._s0_target = target
            act = self._undirected(before)
            self._intent_now = None      # a bare draw means nothing; `None` is the reading
            # **THE AGENT SAYS `TOUCH`, AND THE MODALITY IS NOT ITS BUSINESS -- the plan's
            # 19.** This read `"ACTION6" if "ACTION6" in self.actions else self._toward(...)`:
            # a button by name, and a fallback that ranked every action by the AVATAR's
            # observed displacement. Both are below the seam now, and the agent's whole
            # utterance is *bring me into contact with `target`*.
            #
            # AN UNTRIED ACTION STILL OUTRANKS BOTH MODALITIES, and it is not a preference --
            # it is the only order that works. Contact-seeking has to know what the actions
            # DO, and taking the positioned path before anything else has been tried STARVES
            # the action-effect coverage that is this switch's own first clause: measured on
            # dc22, `{ACTION6: 10}` in 10 cycles with no other action ever taken, so coverage
            # could never complete and the learned arm could never resume. **That rule is the
            # AGENT's -- it is about what the agent still needs to learn, not about which
            # button does what -- so it stays here and is said as an intent.**
            _untried = self.iface.realise(IFace.Intent(IFace.ELICIT), tuple(self.actions),
                                          IFace.Interface.context(self.env), before, self.env,
                                          withheld=self._withheld)
            # **NO LOCAL COPY OF THE AIM. `_took` OWNS IT.** This kept `_coord` and then
            # wrote `self._aimed = _coord` at the end of the branch, which CLOBBERED the aim
            # `_took` had just set -- so an exploratory click that the interface had aimed went
            # out unaimed. The same class as `_explore` discarding `r.coord`, reintroduced by me
            # three hours later in the branch next door. **One owner, no copies.**
            if _untried is not None and _untried.unmapped:
                # **THROUGH THE DOOR, LIKE EVERY OTHER EXIT.** This read `_untried.action`
                # directly and so dropped both the aim and the intent -- the exact defect
                # `_took` exists to prevent, left in the one branch that predates it. Caught by
                # the bet row reading `meant=None`. That figure was quoted over ALL `bet` rows;
                # two per cycle are `@objective`/`@bracket` and carry no `meant` by
                # construction, so the nameable denominator is the TRANSITION rows alone.
                act = self._took(_untried, IFace.Intent(IFace.ELICIT))
            elif target is not None:
                _t = self.iface.realise(IFace.Intent(IFace.TOUCH, object=target),
                                        tuple(self.actions),
                                        IFace.Interface.context(self.env), before, self.env,
                                        withheld=self._withheld)
                if _t is not None:
                    act = self._took(_t, IFace.Intent(IFace.TOUCH, object=target))
                    self.led.record(self.cycle, "PLAN", target, "intent",
                                    reads=(f"{IFace.TOUCH} {target}", _t.why))
                elif _untried is not None:
                    # When there IS a target and TOUCH abstains this branch used to end, so the
                    # `elif _untried` below was unreachable on exactly the cycles that had one.
                    # Do not collapse the two arms back together.
                    act = self._took(_untried, IFace.Intent(IFace.ELICIT))
            elif _untried is not None:
                # **AND THE DEFAULT ASKS FOR SOMETHING RATHER THAN DRAWING BLIND -- 2026-09-29.**
                # Measured over EXITS, not rows: all 12 gridworld cycles exit here and SIX
                # read `meant=None`, because
                # neither branch above fired and the branch fell through to `drive.choose`.
                # **System 0's default asked for nothing at all** -- the one exit left that
                # takes an action without wanting anything.
                #
                # `realise(ELICIT)` ALREADY does unmapped-first-then-variety, so this preserves
                # the coverage rule above it and replaces a blind stride with the variety rule.
                # Simpler, not an extra mechanism: the same call, its result no longer discarded
                # when the action happens to be mapped.
                act = self._took(_untried, IFace.Intent(IFace.ELICIT))
            if self._contact_pick is not None:
                self._contact_seen.add(self._contact_pick)
            # target is an OBJECT id (_contact_target), never a slot. The row is labelled with the
            # step running (PLAN, choose), first on the ladder, so F500's order holds without the
            # object-id workaround the old MINT label needed (the reviewer 2026-10-16 09:49).
            self.led.record(self.cycle, self._running_step, target or "@contact", "system0",
                            why=why, target=target, action=act,
                            unexplored=len([k for k in self._contact_keys(before)
                                            if k not in self._contact_seen]),
                            seen=len(self._contact_seen))
            return act, "system0"
        # **THE AGENT ASKS TO BE ABLE TO TELL THINGS APART; IT DOES NOT RANK BUTTONS.**
        # `docs/ACTION_INTERFACE_PLAN.md` 17. This was `_learned_split`, which ended in
        # `max(self.actions, key=lambda a: sep[a])` -- 93 of 131 acts on `g50t`, 128 of 150 on
        # `ls20`, and the largest single crossing of the seam in the system.
        #
        # **`DISTINGUISH` RATHER THAN `ELICIT`, AND THE REASON IS THE ABSTENTION.** The old
        # branch did two things: it ranked, and it declined when nothing separated. Everything
        # below this line runs only because of the declining -- so realising it as `ELICIT`,
        # which cannot fail while a button exists, would fire here every time and starve the
        # mint, the goal split and the draw. The verb keeps the refusal and drops the ranking.
        _want = IFace.Intent(IFace.DISTINGUISH)
        _r = self.iface.realise(_want, tuple(self.actions),
                                IFace.Interface.context(self.env), before, self.env,
                                withheld=self._withheld)
        if _r is not None:
            self.led.record(self.cycle, "PLAN", "@board", "intent",
                            reads=(_want.says(), _r.why))
            return self._took(_r, _want), "distinguish"
        # AND THE REFUSAL IS A READING ABOUT THE BOARD, NOT A NON-EVENT. *Nothing here tells my
        # alternatives apart* is what the contingency family exists to be able to say, and it
        # was previously an unrecorded `return None` inside the ranking loop.
        self.led.record(self.cycle, "PLAN", "@board", "split_refused",
                        why="nothing_separates", n_actions=len(self.actions))
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
                _act = (None if emit in (Rt.DONE, Rt.BLOCKED, Rt.EXHAUSTED)
                        else self._realise_step(emit, before))
                if _act is not None:
                    self._routine_acts += 1
                    self.routine = rest
                    self._routine_fed = self._routine_entries() if _FED else []
                    return _act, "routine"
                # **AND AN ENDING HERE IS KEPT, NOT DROPPED -- 2026-09-25.** This line used to
                # be `self.routine = None`, so a plan that ended on its FIRST advance VANISHED
                # WITHOUT A TRACE: no `routine_end` row, no `tested_yes`/`tested_no`, no
                # episode, no refutation on `exhausted`, no shelving on `done`.
                #
                # MEASURED: with the accumulator live, gridworld committed THREE times in 48
                # cycles and produced ZERO endings -- `routine_end 0`, `reach_tested 0`,
                # `routine_lib []`. Every plan it bought disappeared at this line.
                #
                # **THE FIX IS TO RECORD NOTHING HERE.** The top of `choose` already advances a
                # held routine and has the whole ending block -- the four endings, the verdict,
                # the episode, the refutation, the shelf. Duplicating that here would be two
                # producers of one fact, which this file names as *harmless exactly until one
                # side changes*. Leaving the routine HELD means the next cycle's normal path
                # reaches the same ending and records it properly.
                #
                # The cycle is not wasted: control falls through to the goal split and the
                # agent still acts, which is the *always paying* premise -- a cycle spent is
                # spent either way.
        goal = self._goal_split(before)
        if goal is not None:
            return goal, "discriminate:goal"
        # THE CURIOSITY EXIT, AND IT IS THE ONE THAT IS AIMED. The goal split refused, so
        # nothing is scoring -- `_curiosity_subject` names what is worth finding out.
        # The `bored()` exit above stays UNINFORMED and must: a probe chosen by the
        # current model can only confirm it, which is that branch's safety property.
        subject = self._curiosity_subject(before) if _AIMED_CURIOSITY else None
        return self._explore(before, subject=subject), "draw"

    # -- SYSTEM 0, CONTACT-SEEKING. Isaiah, 2026-09-21: *I said RANDOM, but more accurately
    # what humans do is: TRY TO MAKE CONTACT. What happens if this touches or interacts with
    # another thing? The more of that is done, the faster the contact clarifies relationship
    # mapping. So CONTACT is the main mode, and pure randomness is for when reasoning is in
    # progress and all contact points have been explored.*
    #
    # `F236` measured the old System 0 as BYTE-IDENTICAL to the uniform draw -- the switch was
    # right and the POLICY was the same call. This is the different policy.

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

    def _understanding(self, slot: str) -> float:
        """WHAT IS WORTH FINDING OUT ABOUT THIS SLOT. Figure 5's *seeks the gap that is LARGE
        AND COMPRESSIBLE*, as a product of two quantities the agent already holds.

            LARGE        `outstanding(slot)` -- surprise not yet explained, monotone
            COMPRESSIBLE `iface.recurrence(slot)` -- a PROXY, labelled at its own site

        **A PRODUCT, NOT A SUM, AND THAT IS WHAT THE *AND* MEANS.** A large incompressible gap
        is noise; a small compressible one is already understood. A sum lets either factor
        alone carry the term. The priors' information-gap curiosity (*peaks when a gap is felt
        but not vast*) falls out of the product with no tuned number, because a vast gap is
        typically incompressible -- two corpus sources, one term, no magic constant.

        `F400`: the two factors are NOT independent on every world -- one ratio on `buttons`,
        twelve on `default`. A world with a constant ratio cannot show the second factor.

        **AND ON THESE PANELS THE SECOND FACTOR IS NEAR-REDUNDANT WITH THE FIRST: it changes the
        chosen slot 1 TIME IN 22 (`F401`).** Kept rather than dropped -- it is the corpus's
        *compressible* and it is cheap -- but it is **a proxy waiting for a world where structure
        and surprise come apart**, and it is not carrying the aiming today. NOT TUNED, on the
        reviewer's ruling: the number is reported, not improved.
        """
        return self.outstanding(slot) * self.iface.recurrence(slot)

    def _curiosity_subject(self, before: dict) -> str | None:
        """The slot with the most to learn, or `None` when nothing has any.

        `None` IS A READING AND NOT A FALLBACK: it means no slot the agent can see carries
        both unexplained surprise and a record of having moved, and `_explore` then draws
        without a subject exactly as it did before. The ledger says which happened.
        """
        best, top = None, 0.0
        vals = {slot: self._understanding(slot) for slot in sorted(before)}
        for slot, v in vals.items():
            if v > top:
                best, top = slot, v
        if _A1_TIES and best is not None:      # A1: an exact tie goes to the less-aimed, not a name
            tied = [s for s, v in vals.items() if v == top]
            if len(tied) > 1:
                best = self._choice("curiosity", None, [(s, None, None) for s in tied], None,
                                    {s: self._subject_n[s] for s in tied})
        if best is not None:
            self._subject_n[best] += 1
        self.led.record(self.cycle, "PLAN", best or "@board", "curiosity",
                        subject=best, value=round(top, 4),
                        reads=("Figure 5 -- the gap that is large and compressible. "
                               "`None` means no slot carries both."))
        return best

    def _explore(self, before: dict, subject: str | None = None) -> str:
        """**THE EXPLORATORY EXITS GO THROUGH THE SEAM.** The agent forms an INTENT -- *elicit a
        response* -- and the interface chooses the action. `docs/ACTION_INTERFACE_PLAN.md`,
        Isaiah 2026-09-28: *the agent shouldn't really care about what action they choose.*

        **AND THE VARIETY RULE LIVES BELOW, NOT HERE.** `realise` will not repeat an action
        already known to do the same thing in this context -- the reviewer's condition, and what
        stops `discriminate:learned`'s one-button collapse (`ACTION2`, 105 of 150 on `ls20`)
        reappearing under the word *exploration*.

        The uniform draw is the FALLBACK and no longer the mechanism: it is what happens when
        the board offers nothing the interface can distinguish.
        """
        want = IFace.Intent(IFace.ELICIT, subject=subject)
        r = self.iface.realise(want, tuple(self.actions), IFace.Interface.context(self.env),
                               before, self.env, withheld=self._withheld)
        self.led.record(self.cycle, "PLAN", subject or "@board", "intent",
                        reads=(want.says(), r.why if r else "unrealisable"))
        if r is None:
            # **AN EXPLICIT FAILURE, NOT A FALLBACK THAT CANNOT WORK -- the reviewer,
            # 2026-09-28.** This used to draw uniformly. Measured: 0 abstentions in 56 `ELICIT`
            # calls across gridworld, gridworld `click_only` and the toy world, because
            # `realise(ELICIT)` tries unmapped, then effect-here-unknown, then least-seen and
            # one always returns. **It abstains ONLY when `offered` is empty** -- and
            # `drive.choose` divides by `len(actions)` and searches `range(7, 7 + len(actions))`
            # for a coprime stride, so it raised on exactly that input anyway.
            #
            # **A guard that fires only when it cannot work is worse than no guard**: it reads
            # as a safety net. This says what happened instead, at the moment it happens.
            raise RuntimeError(
                "the board advertises no actions, so exploration cannot be realised -- "
                f"`env.actions()` returned {self.actions!r}")
        return self._took(r, want)

    def _system0_active(self) -> bool:
        """UNEXPLORED CONTACT COUNT, with the action-effect coverage it replaces kept as the
        first clause. State-derived; no cycle constant and no budget.

        The old test was coverage alone -- every surfaced action tried at >=2 distinct states,
        probe.py's `never_live` anchor. That says nothing about whether the agent has found out
        what touches what, which is the thing System 0 is now for."""
        if not self.drive.covered(len(self.actions)):
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
                "acts": dict(self._acts), "system0": True}

    def _characterise(self, res: dict) -> Characterisation:
        """Describe THIS cycle's gap in §15.3's four keys. Types, never slot names."""
        t = self.slot_types
        involved = sorted(res)
        missed = [x for x in involved if res[x].mass > 0]

        def eff(x: str) -> str:
            r = res[x]
            if r.gone:
                return "gone"
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

    def _note_goal_choice(self, action: Any, before: dict, after: dict) -> None:
        """THE SELECTOR, EVERY CYCLE (the reviewer 2026-10-11 20:58 CDT). `progress` names the
        selected want only when something got closer, so a read of it sees the survivors only.
        This row is written whatever the outcome: what was chosen, why nothing was, and for
        the choice whether the agent can move it, whether it got closer, and whether this
        cycle's action changed it. A record; nothing reads it to decide."""
        why: dict = {}
        sel = self._goal_choice(why=why)
        row = {k: why.get(k, 0) for k in ("too_short", "flat", "rose", "qualified", "arrived")}
        if sel is not None:
            row.update(movable=self._moves_by_sources(sel), closer=self.improved(sel),
                       changed=after.get(sel) != before.get(sel))
            if _DIRECTION_MOVABLE:
                row["movable_by"] = self._movable_by(sel)
        self.led.record(self.cycle, "PERCEIVE", "*", "goal_choice", selected=sel,
                        longest=why.get("longest", 0), series=why.get("slots", 0),
                        wants_held=len(self.wants), action=action, **row)

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
        # **A HYPOTHESIS GETS A DISCREPANCY TOO -- §13.4's *express EACH as a scalar
        # discrepancy*, and `goal_residual` has had this fallback all along: *`bound` holds what
        # SYSTEM 1 does now; `wants` holds what SYSTEM 2 is still after.* This site never got it.
        #
        # **I WROTE THIS EXACT FIX EARLIER TODAY, MEASURED IT AT 2 DELTAS WITH AND 2 WITHOUT,
        # AND REVERTED IT AS A NO-OP.** It was a no-op because `peers()` was unpublished
        # upstream, so `_res` was empty and nothing downstream could show a difference.
        # **Measuring the fix is necessary and not sufficient: a correct repair reads as a
        # no-op whenever something ABOVE it is dead**, and the arm-with-and-without cannot tell
        # that from a useless change.
        if term is None or getattr(term, "out_type", None) != OBJ_TYPE:
            _w = self.wants.get(slot)
            term = (self.gamma.library.get(_w) or self._want_terms.get(slot)) if _w else term
        if (term is None or getattr(term, "out_type", None) != OBJ_TYPE
                or slot not in state or not self._applies(term, state)):
            return NOT_RESOLVED
        ops = self._ops(term, state)
        if ops is None:
            return NOT_RESOLVED
        ctx = self._eval_ctx(slot, state, action=self._last_action or "", operands=ops,
                             touching=self._touching(slot), landed=self._last_landed)

        def _sat(v: int) -> bool | None:
            r = term.apply(v, ctx)
            return None if r is NOT_RESOLVED else bool(r)
        return objective_gap(_sat, state[slot], self.slot_types.get(slot) in ORDERED_TYPES,
                             self._domain(slot, state, ctx))

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
        # **THE BOUND OBJECTIVE, ELSE THE RETAINED WANT** -- `bound` holds what SYSTEM 1 does now,
        # `wants` what SYSTEM 2 is still after; one lookup for every reader (F2).
        name, term = self._objective_of(slot)
        # WHICH None, NOT THAT None -- F207. The exits are different FACTS, not one abstention:
        # nothing bound is a SUPPLY claim, the wrong out_type is a TYPE claim, an absent slot is
        # a PERCEPTION claim, an empty group is a SCOPE claim. The first routine this project
        # ever formed died at `routine_end: blocked`, which means `holds(guard)` read None --
        # and nothing recorded which one.
        #
        # **EIGHT EXITS UNDER SEVEN LABELS. THIS SAID `five` UNTIL 2026-09-26** -- correct when
        # written, and exits were added under it without the count moving:
        #
        #     unbound · name-not-in-library · out_type-not-OBJ · slot-absent-from-state
        #     empty-group · operand-unreadable (TWO sites: `_applies`, then `_ops`)
        #     degree-unresolved
        #
        # **THE COUNT IS LOAD-BEARING AND NOT DECORATION, WHICH IS HOW IT WAS CAUGHT.** A census
        # of why this function abstains takes its BRANCHES from here, and a branch set that is
        # short by two accounts for 100% of the wrong denominator -- which reads exactly like a
        # finding. *A docstring is evidence about what its author believed, never about what the
        # code does today*, and the author was me-two-weeks-ago being right at the time.
        #
        # **SO A NEW EXIT ADDS A LABEL HERE IN THE SAME EDIT**, the way an `ATTRIBUTE_TYPE` key
        # is owed in the commit that emits its attribute. Prefer counting the `_why` calls to
        # trusting this list, and if the two disagree the list is the stale one.
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
        # b-0 (the reviewer 2026-10-11 05:29Z): the scope of an objective is what it is ABOUT. A
        # goal condition is about its own subject, so its population is this slot's value; every
        # other want (a view) keeps the peer group, DISCOVERY Q21 unchanged.
        subject = self._want_scope.get(slot) == name
        group = (state[slot],) if subject else self._group(slot, state)
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
        ctx = self._eval_ctx(slot, state, action=self._last_action or "", operands=ops,
                             touching=self._touching(slot), shapes=False,
                             landed=self._last_landed)

        def _sat(v: int) -> bool | None:
            r = term.apply(v, ctx)
            return None if r is NOT_RESOLVED else bool(r)
        deg = objective_degree(_sat, group, counts)
        if deg is None:
            _why(why, "degree-unresolved")
            return None
        # b-0 AMENDED (the reviewer 2026-10-11 08:34Z, 08:48Z; Fig 12 :112, "progress is a
        # subtraction"): a subject want on an ORDERED slot is scored by HOW FAR it is from
        # holding, so it can shrink under play (Sec 13.4). The search stays on the domain; the
        # UNIT is the alphabet, which already bounds and prices the slot -- a span built around
        # the operand moves with it and cancels the gap. Comparable-only stays 0/1.
        if subject and deg < 1.0 and self.slot_types.get(slot) in ORDERED_TYPES:
            dom = self._domain(slot, state, ctx)
            gap = objective_gap(_sat, state[slot], True, dom)
            span = self.alphabet[slot] - 1
            if isinstance(gap, int) and not isinstance(gap, bool) and span > 0:
                return min(1.0, gap / span)
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
            moves = [aft[slot] - bef[slot] for bef, act, aft, _intent, _landed in self.trace
                     if act == a and slot in bef and slot in aft]
            if not moves:
                continue                   # untried is not evidence either way
            wanted = self._predict(slot, state, a)
            if wanted is None or wanted == state[slot]:
                continue
            if not ordered:
                if any(aft[slot] == wanted for _bef, act, aft, _intent, _landed in self.trace
                       if act == a and slot in aft):
                    return YES
                continue
            step = 1 if wanted > state[slot] else -1
            if sum(1 for d in moves if d * step > 0) * 2 > len(moves):
                return YES                 # this agent has moved it that way, mostly
        return UNKNOWN

    # no _in_step: step() calls this BEFORE choose, so it runs in PLAN, deliberation before anything
    # acts; decorated PERCEIVE in f4a48c4 its choice rows broke the ladder (the reviewer 2026-10-16)
    def note_goals(self, state: dict[str, int]) -> None:
        """One discrepancy reading per goal hypothesis per step. Held, never aggregated."""
        reach: dict[str, str] = {}
        counts: dict[str, dict] = {}
        popped: dict[str, int] = {}
        undone: list = []
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
                # **MET -> UN-MET IS AN OBSERVATION, NOT NOISE TO DROP.** Detected before the
                # append, while the prior reading is still in hand.
                _was = self._res.get(slot)
                if _was and _was[-1] <= 0 < rg:
                    undone.append((slot, _was[-1], rg))
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
        # **WHICH INTENT UNDID WHICH GOAL -- the reviewer's row, 2026-09-29, from Isaiah's
        # ruling.** Recording only; what the agent DOES about it is his call and is not here.
        #
        # **THE ATTRIBUTION IS CORRECT HERE AND IS NOT ELSEWHERE, WHICH IS THE WHOLE REASON THE
        # ROW LIVES AT THIS SITE.** This runs at the TOP of the step, so `_res` is being updated
        # from the frame the PREVIOUS action produced -- and `_intent_now`/`_last_action` are
        # not cleared until `choose` further down, so they still name THAT action. Read them
        # after `step()` returns instead and every transition is paired with the intent taken
        # AFTER the one that caused it: measured, and it reported `down` four times when `down`
        # was responsible for none of them.
        #
        # Keyed like the other audit rows -- context and the value it was met at -- so the
        # repeat count is per situation and not per run. One row per transition rather than per
        # call: these are rare (13 in 60 cycles) and the flood `_why` warns about does not apply.
        if undone:
            _ctx = IFace.Interface.context(self.env)
            _said = self._intent_now.says() if self._intent_now is not None else None
            for _slot, _was, _now in undone:
                _key = (_ctx, _said, _slot, round(float(_was), 3))
                _n = self._undone[_key] = self._undone.get(_key, 0) + 1
                _ak = (_said, _slot)
                _an = self._undone_across[_ak] = self._undone_across.get(_ak, 0) + 1
                self.led.record(self.cycle, self._running_step, _slot, "goal_undone",
                                was=round(float(_was), 4), now=round(float(_now), 4),
                                # **THE DISCREPANCY IS NOT THE BOARD, AND A ROW THAT CARRIES
                                # ONLY THE DISCREPANCY CANNOT BE CROSS-REFERENCED AGAINST ONE.**
                                # ISAIAH's ruling 8: store what the agent did AND why, WITH the
                                # board state that prompted it, so an old intent can be checked
                                # against the scenario it was formed in.
                                #
                                # `was`/`now` are GOAL DISCREPANCIES; `value` is the SLOT'S OWN
                                # VALUE. Two quantities, and conflating them is not theoretical
                                # -- I joined this row against `lands` on the discrepancy, which
                                # keys on the slot value, and the match was a collision at zero.
                                value=state.get(_slot),
                                # The frame that prompted it. 13 rows in 60 cycles here, so the
                                # volume is trivial; on a board with many slots and more
                                # transitions it is not, and that is the thing to watch.
                                board=dict(state),
                                intent=_said, action=self._last_action, ctx=_ctx,
                                times=_n, repeated=_n >= MIN_REPEAT,
                                # SEPARATE AND LABELLED, so it cannot be mistaken for the
                                # tested quantity. `times` is the claim; this says only
                                # *worth trying here*, and it is deliberately NOT compared
                                # against `MIN_REPEAT`.
                                across=_an,
                                across_reads="seen this often across ALL contexts -- a hint "
                                             "about what to try, not a finding",
                                reads="a goal I had met is no longer met; this is what I did")
        if reach:
            self.led.record(self.cycle, self._running_step, "*", "can",
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
                self.cycle, self._running_step, "*", "goal_series",
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

    def _goal_choice(self, why: dict | None = None, book: bool = False) -> str | None:
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
        tally = {"too_short": 0, "flat": 0, "rose": 0, "qualified": 0, "arrived": 0}
        longest = 0
        for slot, series in sorted(self._res.items()):
            longest = max(longest, len(series))
            # **AN OBJECTIVE THAT HAS ARRIVED IS NOT ONE TO PURSUE, AND ARRIVING LOOKS EXACTLY
            # LIKE SHRINKING ON THE LAST READING.** §13.4 defines the series as *a scalar
            # discrepancy that is ZERO EXACTLY WHEN SATISFIED*, so `[2, 1, 0]` passes
            # *confidently shrinking* on its way to being done, and the selector spent its
            # choice there.
            #
            # Measured before this existed -- gridworld seed 11, 60 cycles: **7 of 26 mint
            # refusals read *the objective already holds across its whole scope*, and the ONE
            # routine that reached `done` did so having taken ZERO ACTIONS**, its guard already
            # true when it started. One cause, and the second half is why the library was empty.
            #
            # **THE READING WAS ALREADY PUBLISHED AND NEVER CONSULTED** -- `goal_series` computes
            # `satisfied` as exactly this test. *A value that exists and never crosses.* Same
            # expression here, so the row and the gate cannot drift apart.
            #
            # Tallied apart, never folded into `flat`: flat is *sitting at a gap*, this is
            # *there is no gap*.
            # **AND ARRIVED MEANS STAYED ARRIVED, BECAUSE ONE READING IS A COINCIDENCE.**
            # The first version tested `series[-1] <= 0` and it removed BOTH of the agent's
            # only real trials in 60 cycles. The tell was the ending: an `exhausted` means the
            # GUARD WAS NOT MET, so a series reading <= 0 at selection while the guard said no
            # at execution is a MOMENTARY TOUCH on an oscillating relational attribute, not
            # arrival. `MIN_REPEAT` is reused rather than a second constant invented -- the
            # same rule, from the same line, that makes *confidently* mean what it means here.
            if len(series) >= MIN_REPEAT and all(v <= 0 for v in series[-MIN_REPEAT:]):
                tally["arrived"] += 1
                continue
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
        # **WRITTEN ONLY BY GATE 1, WHICH IS WHAT THE KEYS ARE NAMED FOR -- `F440`.** Up to
        # four sites call this per cycle, so writing on every call counted CALLS x SLOTS
        # across all of them under a `gate 1` label.
        if not book:
            return best[1] if best else None
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

    def _holds(self, state: dict[str, int], step: str | None = None):
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
                # the CALLER'S step: `_settle_routine` advances at SETTLE (F501), so a guard read
                # there is a SETTLE row, after the cycle's demotes, never a PLAN row out of order
                self.led.record(self.cycle, step or self._running_step, guard, "guard_unreadable",
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

    @property
    def settled(self) -> set[str]:
        """What the GROUND has paid for -- read from gamma, never kept beside it.

        **THIS WAS AN ADD-ONLY SET AND IT DISAGREED WITH GAMMA -- measured 2026-09-30.**
        `gamma.settle` recorded a settlement and `self.settled.add` recorded it again; then
        ONE REFUSAL at `REJECTION_CEILING` cleared `settled_at` and the set never heard.
        Measured on the M2 fixture: **the agent said 4, gamma said 0**, and every reader of
        `ag.settled` -- including the probes that found this -- had been reading the stale one.

        **AND IT REACHED THE AGENT'S OWN DIAGNOSIS.** `_link` tests `if not self.settled`
        BEFORE its `owed_import` branch, so a non-empty stale set skipped the link-5 verdict:

            on the stale set   "2 - vocabulary (measured: 4 slot(s) unreached at budget)"
            on the truth       "5 - learn and carry (measured: nothing settled ...)"

        Two different halves of the system to go and look at. *A ground reading taken below
        the break is a reading of nothing*, and this is the reading that says where the break
        is.

        DERIVED RATHER THAN SYNCHRONISED, deliberately. The defect was not a missed update --
        it was that there were two answers at all, and an update path is two answers plus a
        promise. `Standing.settled` is a DIFFERENT quantity on a different object; the four
        assertions in `conform/stateful.py` that read it are correct and untouched.
        """
        return {n for n in self.gamma.library if self.gamma.is_settled(n)}

    @property
    def _scope(self) -> str:
        """WHERE evidence is being taken right now -- the game and the level together.

        Isaiah's ruling is about a BOARD lacking the mechanic; measured, the same failure
        exists one scale down at the LEVEL, and which of the two his weighing applies to is
        his and is open. **So the stamp records both and decides neither** -- a coarser scope
        cannot be recovered from a finer one afterwards, and this is written at the moment the
        failure happens, which is the only moment it can be written at all.
        """
        return f"{self.gamma.game}:L{self.level}"

    def _carry(self, name: str) -> None:
        """A term the agent just BOUND becomes a candidate awaiting the ground.

        `setdefault`, never assignment: a term already waiting keeps its ORIGINAL cycle, and
        `settle`'s `born >= self.cycle` guard means nothing registered here can settle on the
        cycle it was bound. Re-earned by acting; never settled on import.

        **IMPORTED ONLY, AND THE FIRST VERSION WAS NOT -- IT BROKE THREE SEATS.** Unscoped,
        this also gave LOCAL terms a second and earlier candidacy, which moved their birth
        cycle, what settled, `units()`, and therefore composition prices: `27/30` with
        `strategy` at 0.0 and the M2 suite no longer reaching `routine` at all. Measured both
        ways on the flag. **A local term already has its route -- mint registers it at the
        moment it is minted -- so widening this to every bind was scope the ruling never
        asked for**, and the ruling's subject is the term that has no route.
        """
        if not _CARRY_CANDIDATE:
            return
        # REACTIVATION, AND IT IS THE SAME DOOR ON PURPOSE. A candidate that survived a level
        # boundary is DORMANT because its stamp names the old level; being bound HERE is the
        # evidence that the conditions recur, so the stamp moves and nothing else does. **The
        # birth cycle is untouched** -- that is the quantity whose movement took M2 to 27/30.
        if name in self.candidates:
            if self._cand_level.get(name) != self.level:
                # (c) ACCEPT by design: this row records the ACCEPT this method itself performs, a
                # later step carried out inside MINT (the reviewer 2026-10-16 09:23)
                self.led.record(self.cycle, "ACCEPT", name, "candidate_woken",
                                was=self._cand_level.get(name), now=self.level,
                                born=self.candidates[name],
                                reads="dormant since a level change; bound here, so it is "
                                      "eligible again and must still pay on this level")
            self._cand_level[name] = self.level
            return
        t = self.gamma.library.get(name)
        if t is not None and t.origin == IMPORTED:
            self.candidates[name] = self.cycle
            self._cand_level[name] = self.level

    def _expected(self, cand, unsat: float, before: dict):
        """Attach the agent's OWN expected iteration count, or leave the routine as it is.

        **ASKED IN INTENTS, AND THE FIRST VERSION WAS NOT.** This looked the movement up BY
        ACTION and attached NOTHING on 76 of 76 loops: a routine body carries an `Intent`, and
        the delta table is keyed by the realised action, below the seam. The zero it produced
        was indistinguishable from *the agent has no model*, which is what I nearly filed.
        `expected_move` asks at the level the agent actually holds. No reading means NO EXPECT
        -- `reach` falls back to `budget`. Isaiah: *with no model it emits none.*

        **AND THE SLOT IS NOT A PARAMETER, BECAUSE THE INTENT CARRIES ITS OWN SUBJECT.** It was
        one, taken from the planning site, and that is two sources for one quantity: if the
        caller's slot and `intent.subject` ever disagreed, the expectation would be read off a
        different slot than the loop is driving, and nothing would say so.

        **ONLY A BARE `Until(g, Act(a), n)`.** A compound body's per-iteration movement is not
        one action's delta, and guessing it would be the seat supplying a number the agent has
        not observed -- which is the whole thing this replaces.
        """
        if not isinstance(cand, Rt.Until) or not isinstance(cand.body, Rt.Act):
            return cand
        _want = cand.body.action
        if not isinstance(_want, IFace.Intent):
            return cand
        # 7a(5) C: the withheld set is ONE board's; another state gets none (the reviewer 11:53Z)
        per = self.iface.expected_move(_want, tuple(self.actions),
                                       self.iface.context(self.env), before, self.env,
                                       self._withheld if before is self._step_before
                                       else IFace.NO_WITHHELD)
        if not per:
            return cand
        want = math.ceil(abs(unsat) / abs(per))
        return _replace(cand, expect=max(1, want))

    def _choice(self, site: str, slot: str | None, options: list, residual: dict | None = None,
                seen: dict | None = None):
        """A1-CONVERT's A2 row: frontier_pick over the agent's own readings, recorded with the
        frontier's readings, the residual and learning readings, the pick and its step."""
        pick, by, front = FR.frontier_pick(options, residual, seen,
                                           f"{self.cycle}:{site}:{slot}", self.draw_seed)
        fr = set(front)
        # a slot's choice is labelled with the step running; a slot-free one stays PLAN (its own
        # (cycle, slot)) and says when it was made in in_step
        self.led.record(self.cycle, self._running_step if slot else "PLAN", slot or "@choice",
                        "choice", site=site,
                        **({} if slot else {"in_step": self._running_step}),
                        options=len(options),
                        frontier=[[repr(n), b, a] for n, b, a in options if n in fr],
                        residual=(None if residual is None else
                                  {repr(n): residual.get(n, 0) for n, _b, _a in options}),
                        seen=None if seen is None else {repr(n): seen.get(n, 0) for n in front},
                        pick=repr(pick), by=by,
                        **({"root": self._root_id} if _7H_ROOT else {}))
        return pick

    def _choose_known(self, known: list[tuple[str, int]]) -> tuple[int, str]:
        """NOTHING IS UNKNOWN HERE, SO THE AGENT PRICES WHAT IS KNOWN -- Design A (the reviewer,
        2026-10-06; F480). `known` is one (effect, times seen here) per option, never a button.

        Fig 12: actions are a currency -- every option costs one, and a restart also throws away
        the actions spent since this level (or its last restart) began. Fig 5: only an effect
        that changes the board can reach a gap elsewhere; a restart can when there is progress
        to undo. Least-seen breaks ties, which keeps variety among equal moves.

        Under TETHER_DEST_GAP an option may carry a third field: whether it has been seen to lead
        somewhere with an unknown knob (the reviewer 2026-10-12 13:04 CDT). It ranks AFTER price,
        so a gap elsewhere never buys a restart (Fig 12)."""
        def price(e: str) -> int:
            return 1 + self._attempt_actions if e == IFace.RESTARTS else 1

        def reaches(e: str) -> bool:
            return e == IFace.CHANGES or (e == IFace.RESTARTS and self._attempt_actions > 0)

        if _A1_CHOOSE:
            # A1 (the reviewer 2026-10-15 09:33, 09:38). RESIDUAL = REACH toward what is open now:
            # a known no-change reaches nothing (0); otherwise the interface's count of unknowns
            # the option leads to (one when its destination is itself unrecorded). ACTIONS = the
            # acts it costs in the world (a restart throws away this attempt's), None for a known
            # no-change, whose finding-out is done (Fig 12). Then the least-seen, then the draw.
            def reach(k) -> int:
                if k[0] == IFace.NO_EFFECT:
                    return 0
                # leads back HERE: nothing thrown away, nothing reached (Design A's reaches).
                # S1: not on a dead board, where the restart is the way out and reads the
                # interface's reach like any option
                if (k[0] == IFace.RESTARTS and self._attempt_actions == 0
                        and (self._alive or not IFace._DEAD_PRICE)):
                    return 0
                return int(k[2]) if len(k) > 2 else 1
            i = self._choice("choose_known", None,
                             [(j, None, None if k[0] == IFace.NO_EFFECT else price(k[0]))
                              for j, k in enumerate(known)],
                             {j: reach(k) for j, k in enumerate(known)},
                             {j: k[1] for j, k in enumerate(known)})
            return i, (f"chose '{known[i][0]}' at price {price(known[i][0])}, reach "
                       f"{reach(known[i])}, of {sorted({(k[0], price(k[0])) for k in known})}")
        gap = [len(k) > 2 and bool(k[2]) for k in known]
        i = min(range(len(known)),
                key=lambda j: (not reaches(known[j][0]), price(known[j][0]), not gap[j],
                               known[j][1], j))
        return i, (f"chose '{known[i][0]}' at price {price(known[i][0])}"
                   f"{', toward an unknown knob' if gap[i] else ''} of "
                   f"{sorted({(k[0], price(k[0])) for k in known})}")

    @_in_step("IMPORT")
    def restarted(self, env: Any) -> None:
        """THE SAME LEVEL AGAIN, after a death and the agent's RESET -- called by the harness, as
        `retarget` is. The death's boundary HELD the slot-keyed refutations. Each comes back only
        where EVERY object its key names was re-found unambiguously (overlap, or a unique shape):
        a look-alike may have swapped names, and a refutation landing on the twin is a claim
        travelling changed and silent (the reviewer, 2026-10-06). The rest are NAMED, not carried.
        """
        held, self._held_refutations = self._held_refutations, None
        self._attempt_actions = 0
        self._alive, self._epoch = True, self._epoch + 1   # the same level, alive again
        self.iface.situate(self._epoch, self._alive)
        if _MC34:
            self._level_attempts += 1
        if _LINEAGE_HOLD:
            self._carry_lineage(env)
        if not held:
            return
        idn = getattr(env, "identity", None)
        carried, not_carried = [], {}
        for k, st in held[0].items():
            # (b'-l) C3, under the arm only: a pair owner (o12~o3) names BOTH objects (the
            # reviewer 2026-10-14 17:02); OFF keeps the old line, which names neither.
            objs = (sorted(self._objs_named((k[0], *k[2]))) if _LINEAGE_HOLD else
                    sorted({n.split(".", 1)[0] for n in (k[0], *k[2])
                            if re.fullmatch(r"o\d+", n.split(".", 1)[0])}))
            how = {o: idn(o) if idn else None for o in objs}
            unsure = {o: w for o, w in how.items() if w not in ("overlap", "unique-shape")}
            if unsure:
                not_carried[k[0]] = unsure
                continue
            self.refuted[k], self.refuted_at[k] = st, held[1][k]
            carried.append(k[0])
        _c, _s, _lv = self._boundary_key("@boundary")
        self.led.record(_c, "IMPORT", _s, "restart", **_lv,
                        carried=sorted(carried), not_carried=not_carried,
                        reads="refutations held at the death; carried only where identity is sure")

    @_in_step("SETTLE")
    def _hold_lineage(self, how: str) -> None:
        """(b'-l) D-c, D-a, D-selection at a boundary, BEFORE retarget clears. Every store it clears
        is kept dormant in instance form, copied by its own type (Fig 6: a store that deletes cannot
        tell never-held from held-and-given-up), a count row per store, and one attempt row: the
        ending's sign and what THIS attempt tried in kind form -- the action names in its own trace
        and the gap kinds filed (_gap_key, 7315) -- never a verdict on the items (Fig 7; the
        death guard, RL-6)."""
        stores = {nm: (list if isinstance(getattr(self, at), list) else dict)(getattr(self, at))
                  for nm, at in _LINEAGE_STORES}
        stores["drive_tried"] = {a: set(w) for a, w in self.drive.tried.items()}
        self._dormant.append({"level": self.level, "how": how, "cycle": self.cycle,
                              "stores": stores, "restarted": False})
        _c, _s, _lv = self._boundary_key("@lineage")
        for nm, st in stores.items():
            self.led.record(_c, "SETTLE", _s, "dormant", **_lv, store=nm, count=len(st), how=how,
                            reads="kept as the record; never consulted by slot name")
        gaps = sorted({str(k[0]) for k, rec in self.paths.items()
                       if rec.get("last_cycle", -1) >= self._attempt_cycle})
        # what THIS attempt did, re-tries of carried pairs included: the trace holds every step
        # since the last boundary (cleared only at retarget), each one
        # (before, action, after, intent, landed)
        tried = sorted({step[1] for step in self.trace})
        _ac, _as, _alv = self._boundary_key("@attempt")
        self.led.record(_ac, "SETTLE", _as, "attempt_end", **_alv, ending=how,
                        attempt=self._level_attempts, actions_tried=tried,
                        gap_kinds=gaps, reads="what was tried and how it ended; not a verdict")
        self._attempt_cycle = self.cycle

    @staticmethod
    def _objs_named(x: Any) -> set:
        """Every object id a key names: a slot's owner, a pair owner split on "~" (o12~o3)."""
        if isinstance(x, str):
            return {p for p in x.split(".", 1)[0].split("~") if _OBJ_ID.fullmatch(p)}
        if isinstance(x, (tuple, list, set, frozenset)):
            return set().union(*(Agent._objs_named(y) for y in x)) if x else set()
        return set()

    @_in_step("IMPORT")
    def _carry_lineage(self, env: Any) -> None:
        """(b'-l) D-b: on a same-level restart after the game's "death" ending (a loss in the game,
        not the agent's end: the agent, like a player, keeps everything), that boundary's stores in
        _LINEAGE_CARRY come back per entry where EVERY object the key names is re-found as
        "overlap" or "unique-shape" (restarted's rule, 6969-6978). The rest stay dormant. Gap
        readings, the one-step refusal filing and D5's withdrawn cuts stay the record only."""
        rec = self._dormant[-1] if self._dormant else None
        if rec is None or rec["how"] != "death" or rec["restarted"]:
            return
        rec["restarted"] = True
        idn = getattr(env, "identity", None)
        why: dict = {}

        def sure(objs: set) -> bool:
            for o in objs:
                if o not in why:
                    why[o] = idn(o) if idn else None
            return all(why[o] in ("overlap", "unique-shape") for o in objs)
        carried, not_carried = Counter(), Counter()
        attrs = dict(_LINEAGE_STORES)
        for nm in _LINEAGE_CARRY:
            live = getattr(self, attrs[nm])
            for k, v in rec["stores"][nm].items():
                if sure(self._objs_named(k)):
                    live[k] = v
                    carried[nm] += 1
                else:
                    not_carried[nm] += 1
        for a, wheres in rec["stores"]["drive_tried"].items():
            kept = {w for w in wheres if sure(self._objs_named(w))}
            self.drive.tried.setdefault(a, set()).update(kept)
            carried["drive_tried"] += len(kept)
            not_carried["drive_tried"] += len(wheres) - len(kept)
        _c, _s, _lv = self._boundary_key("@lineage")
        self.led.record(_c, "IMPORT", _s, "restart_lineage", **_lv, carried=dict(carried),
                        not_carried=dict(not_carried), identity=why,
                        reads="dormant stores carried back only where identity is sure")

    def _refusal_scope(self) -> tuple:
        """What a plan is refused UNDER: the vocabulary it can be composed from."""
        return (tuple(sorted(self.gamma.library)), tuple(sorted(self.routine_lib)))

    def _refusal_key(self, gap: dict | None, r) -> tuple:
        return (self._gap_key(gap) if gap is not None else None,
                self._step_ids(r, self.routine_lib), Rt.guards(r))

    def _refused(self, key: tuple) -> bool:
        """Refused while the scope it was refused under still stands. Lifted only by growth -- a
        new term or routine -- never by a clock (Fig 6; Isaiah 2026-09-29: never from disuse)."""
        scopes = self._refusals.get(key)
        return bool(scopes) and scopes[-1] == self._refusal_scope()

    def _term_gkey(self, slot: str) -> tuple | None:
        gap = self._characterise_gap(slot)
        return self._gap_key(gap) if gap is not None else None

    @_in_step("MINT")
    def refuse_term(self, name: str, slot: str, **detail) -> bool:
        """Record not-t on this slot's gap shape. Only a HELD term can be refused, so a refusal is
        the record of held-and-given-up (P5). Adds and removes nothing else (P1). A SETTLED term
        refused is a contradiction the figure leaves open: written down, not decided (P6)."""
        if name not in self.gamma.library:
            return False
        k = (name, self._term_gkey(slot))
        self._not.setdefault(k, []).append(self._refusal_scope())
        self.led.record(self.cycle, "MINT", slot, "refuse", term=name,
                        refused_under=len(self._not[k]), **detail)
        if self.gamma.is_settled(name):
            self.led.record(self.cycle, "MINT", slot, "contradiction", term=name,
                            reads=("a settled term and its refusal both stand: two scopes, an "
                                   "error in the ground, or a world that changed -- not decided"))
        return True

    def _persists(self, name: str, slot: str) -> bool:
        """The refused term's residual on this slot, row by row over the last MIN_REPEAT+1 rows,
        read by `_goal_choice`'s test with the sign reversed: not ARRIVED (the last MIN_REPEAT
        rows all explained) and not CONFIDENTLY SHRINKING (non-increasing with a real fall).
        A window too short to read is not persistence -- one observation is a coincidence."""
        t = self.gamma.library.get(name)
        rows = self.history(slot)[-(MIN_REPEAT + 1):]
        if t is None or len(rows) < MIN_REPEAT + 1:
            return False
        series = [self._left(t, slot, [row]) for row in rows]
        if all(v <= 0 for v in series[-MIN_REPEAT:]):
            return False
        deltas = [b - a for a, b in zip(series, series[1:], strict=False)]
        return not (all(d <= 0 for d in deltas) and any(d < 0 for d in deltas))

    @_in_step("MINT")
    def _price_refusal(self, slot: str) -> None:
        """The MINT step's act for a slot `route` filed to REFUTED, at that slot's own turn --
        priced on the library as its own mint would be. Priced for every filed slot up front, a
        later slot's reuse sweep wrote ROUTE rows after this MINT row (gridworld s0 seq 1813, F499).
        Every attempt is a row, so "none refused" and "none tried" read differently."""
        name = self._refuted_slot.pop(slot, None)
        if name is None:
            return
        ok, d = self._price_not(name, slot)
        self.led.record(self.cycle, "MINT", slot, "not_t", term=name,
                        verdict=("paid" if ok else "did not pay") if d
                        else "not priced: no history, or no idn to withdraw to", **d)
        if ok:
            self.refuse_term(name, slot, **d)

    def _price_not(self, name: str, slot: str) -> tuple[bool, dict]:
        """Fig 5's amendment, the same bargain: not-t pays iff its price plus what stays unexplained
        with t's predictions withdrawn (the persistence prior) is less than what t leaves now. So a
        refusal pays only when t does worse than saying nothing, by more than it costs to say it."""
        t = self.gamma.library.get(name)
        hist = self.history(slot)
        if t is None or not hist or IDN not in self.gamma.library:
            return False, {}
        k = len({n for n in self._pred_by.values() if n})
        cost = term_bits(self.gamma.length(t, self._units_for(slot)), self.gamma.alphabet)
        cost += (math.log2(self.gamma.alphabet + 1) if _NOT_ATOM
                 else math.log2(k) if k > 1 else 0.0)
        with_t = self._left(t, slot, hist)
        without = self._left(self.gamma.library[IDN], slot, hist)
        return pays(cost, without, with_t), {
            "predicting": k, "price": "atom" if _NOT_ATOM else "name the term",
            "cost_bits": round(cost, 3), "left_with": round(with_t, 3),
            "left_without": round(without, 3)}

    def _term_refused(self, name: str, gkey: tuple | None) -> bool:
        """Refused while the scope it was refused under still stands (`_refused`'s rule)."""
        scopes = self._not.get((name, gkey))
        return bool(scopes) and scopes[-1] == self._refusal_scope()

    def _units_for(self, slot: str) -> tuple:
        """The units a search on this slot composes from. A refused term's sequence is not a
        shortcut while its refusal stands, so terms that paid only through it re-price at full
        length and fall BY DERIVATION (P3). Found by SEQUENCE CONTAINMENT: no composition
        lineage is kept (F496 records it as a later improvement)."""
        units = tuple(self.gamma.units())
        if not self._not:
            return units
        gk = self._term_gkey(slot)
        out = {self.gamma.library[n].atoms for (n, g) in self._not
               if g == gk and n in self.gamma.library and self._term_refused(n, g)}
        return tuple(u for u in units if len(u.atoms) < 2 or u.atoms not in out)

    def _rejection(self, key: tuple) -> float:
        """The decayed strength of rejection. `Standing.decay` on the LOGICAL clock -- cycles,
        never wall time -- which is §18.2's first defeasance route and was already built."""
        st = self.refuted.get(key)
        if st is None:
            return 0.0
        st.decay(self.cycle, self.gamma.halflife)
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

    def _reach_seen(self, slot: str, cand) -> str:
        """`reach_status`, upgraded by what a run of THIS plan on THIS slot actually did.

        Structural by default -- `assumed_yes` / `unknown` -- and `tested_yes` / `tested_no`
        once the ending site has watched one. The record is keyed the way refutations are, so
        a plan differing only in its budget is the same hypothesis and inherits the verdict.
        """
        return self._reach_tested.get(
            self._reach_key(self._reject_key(slot, cand, self.routine_lib)),
            Rt.reach_status(cand))

    def _reach_key(self, k: tuple) -> tuple:
        """S5: a reach verdict's key, with whether it was watched alive."""
        return (k, self._alive) if _SITUATED_REACH else k

    @staticmethod
    def _step_ids(r, lib: dict | None = None) -> tuple[str, ...]:
        """A plan's steps AS THE RECORD SHOULD KEEP THEM -- `docs/ACTION_INTERFACE_PLAN.md` 16c.

        **ISAIAH, 2026-09-28: *save the intent ... so meaning is preserved when the board
        shifts.*** Every identity below this line used `Rt.actions`, which is the plan's BUTTON
        NAMES, and that fails in both directions. Re-map the button and the refutation history
        is LOST, so a shape already learned useless is re-tried. Keep the NAME and change what
        it does and the history is KEPT while no longer referring -- the worse one, because the
        agent then refuses a plan on evidence about something else.

        `says()` rather than the object, because a key is read by a human in a ledger row and
        *BECOME o0.row +* is the thing that stayed true across the shift.
        """
        return tuple(x.says() if isinstance(x, IFace.Intent) else str(x)
                     for x in Rt.actions(r, lib))

    def _runnable(self, r, before: dict[str, int], lib: dict | None = None) -> bool:
        """Can this plan still be RUN here? -- 16d, and it runs EVERY STEP.

        **IT WAS LABELLED "the level-boundary check" AND THAT UNDERSELLS WHAT IT DOES --
        corrected 2026-10-01.** The set it compares against is `self.actions`, which
        `_advertised` rewrites at the top of every step, so this fires whenever the advertised
        set moves and not only at a boundary. A mid-level MODE SWITCH -- avatar actions
        withdrawn, a positioned click left -- is therefore already handled here: the routines
        naming a vanished action drop out of `shelf` at :4962 and return when it does.
        **No refutation, no miss, no demotion is recorded on that path**, so it is dormancy
        rather than punishment, which is what a vanished action deserves.

        It used to be `set(Rt.actions(r)) <= set(self.actions)`: a string comparison against the
        advertised set. **A level that keeps every button name and changes what two of them do
        passes that and should not.** Asking the interface instead makes the check about the
        WORLD rather than about a name, and `audit`'s own `changed` set is what notices.
        """
        ctx = IFace.Interface.context(self.env)
        for step in Rt.actions(r, lib):
            if isinstance(step, IFace.Intent):
                # 7a(5) C: "can it run HERE" -- a press the floor vetoes on this board cannot
                # (the reviewer 11:53Z). env goes only with a set, so the check can read the board.
                if self.iface.realise(step, tuple(self.actions), ctx, before,
                                      self.env if self._withheld else None,
                                      self._withheld) is None:
                    return False
            elif step not in self.actions or self._withheld.action(step):
                return False
        return True

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
        return (slot, Agent._step_ids(r, lib), Rt.guards(r))

    def _accumulate(self, slot: str, gkey: tuple | None) -> dict:
        """MANY WEAK CONTRIBUTIONS -> ONE VECTOR, AND A THRESHOLD THAT CONVERTS IT INTO A
        COMMITMENT. Isaiah, 2026-09-25, superseding the three-mode rulebook.

        *"One end of the spectrum is PURE REASON AND VOTING AND BUDGETS, the other is PURE
        INTUITION OR BASE MECHANISMS THAT ARE FILTERED AND ARRIVE AS ONE SIGNAL (like with
        eyesight)... depending on the situation and YOUR CURRENT STANDING your decision
        might be influenced differently."*

        **DELIBERATION AND INTUITION ARE THE SAME MECHANISM AT DIFFERENT THRESHOLD HEIGHTS.**
        High threshold, much accumulation required -> it looks like reasoning. Low threshold,
        fast commitment -> it looks like instinct. **STANDING SETS THE HEIGHT; it does not
        vote.** That is the honeybee quorum, where bad weather lowers the bar and the swarm
        decides faster and worse.

        NO CONTRIBUTOR IS NEW. Every one is a quantity the agent already had and read alone:

            lean        recurrence of this want. Isaiah's *deterministic intuition* --
                        the gradient of past patterns, read off instead of recomputed
            improving   the goal residual's own trend
            episodes    how plans of this shape ended on this gap shape

        All on the ACTIONS side (item 6, 2026-10-07): `shortfall` (bits, always 0 here), `plant`
        and `refuted` (a failed plan is item 1's refusal) are gone. Their weights are an implicit
        1:1 -- OPEN, recorded, not chosen.

        **AND THE THRESHOLD FALLS WITH THE CLOCK, WHICH IS THE "ALWAYS PAYING" RULING IN
        MECHANISM FORM.** *"The agent is always paying with its time and life force... there
        is no real world where it doesn't move."* Refusing is not free: every cycle that ends
        without a commitment lowers the bar for the next one. An agent that drafts forever
        is not optimal, it is dead -- and this is what makes drafting cost something.

        TRACEABLE BY CONSTRUCTION: the return names every contribution and its weight, so a
        lean that goes wrong is a finding rather than a mystery.
        """
        v: dict[str, float] = {}
        # NO BARGAIN TERM, SINCE ITEM 6. This is reached only after `pays` refused, where the slope
        # `1 - (cost + left)/base` is always <= 0 -- it was 0.0 on 70 of 70 vectors measured. The
        # bits reading is the bargain's own verdict, held apart on its row (Fig 12).
        # THE LEAN. `_want_seen` counts attempts that wanted this composition; one sighting is
        # not a pattern, so the first is worth nothing and the gradient starts at the second.
        _w = self.wants.get(slot)
        v["lean"] = max(0, self._want_seen.get(_w, 0) - 1) / MIN_REPEAT if _w else 0.0
        # THE TREND. Improving is evidence for acting; flat and rising are not.
        _ser = self._res.get(slot) or []
        v["improving"] = 1.0 if len(_ser) > 1 and _ser[-1] < _ser[0] else 0.0
        # **THE FRESH READ -- ISAIAH, 2026-09-25.** *"A fresh read of current state and current
        # goals and current obstacles must ALSO GET A VOTE to 'price' or QUALIFY the data."*
        # It does both jobs here and they are different:
        #
        #   IT VOTES      past episodes under THIS signature contribute, favourable ones
        #                 positively and unfavourable ones negatively
        #   IT QUALIFIES  it scales the LEAN. Recurrence counts how often a want came back;
        #                 it does not know whether acting on it ever worked. **An accumulator
        #                 that weighs a pattern which has failed every time it was tried as
        #                 evidence FOR acting is exactly the failure transfer introduces** --
        #                 right neighbourhood, wrong house
        #
        # AND IT IS KEYED ON THE SIGNATURE, NOT THE BOARD, so a lesson learned on one
        # arrangement prices a want on another. That is the transfer half.
        _eps = self._episodes.get(gkey, []) if gkey else []
        _good = sum(1 for _a, _w, ver in _eps if ver == "tested_yes")
        _bad = sum(1 for _a, _w, ver in _eps if ver == "tested_no")
        v["episodes"] = float(_good - _bad)
        if _eps and _bad > _good:
            # QUALIFIED DOWN: this shape has cost more than it paid. The lean is what is
            # damped, never the bargain -- a price is not an opinion.
            v["lean"] = v["lean"] / (1.0 + _bad - _good)
        total = sum(v.values())

        # STANDING SETS THE HEIGHT. `MIN_REPEAT` is the agent's own bar for "confidently".
        # **THE ONLY TERM THAT MOVES IS THE CLOCK SINCE THE LAST COMMITMENT.**
        #
        # THE FLOOR WAS 1.0 AND IT IS NOW HALF A VOTE UNDER THE BAR -- reviewer, 2026-09-26,
        # on a defect I reported against my own build: *a quorum reachable by one bee is not
        # a quorum.* At 1.0 a single contributor at unit strength cleared the bar alone, and
        # the one commitment the accumulator ever made was carried by `improving` by itself.
        # **AND SINCE ITEM 6 (2026-10-07) THE HEIGHT IS THE AGENT'S OWN** -- Isaiah, 2026-09-25,
        # relayed verbatim: *your current standing (resources, energy, ability, restrictions,
        # history)* sets it. The bar is read from how its own overrides ended; the relief rate
        # from its own intervals between commitments. Each is a SEED, marked, until it has one.
        idle = self.cycle - self._last_commit
        bar, bar_earned = self._commit_bar()
        rate, rate_earned = self._relief_rate()
        threshold = max(bar - _QUORUM_HALF, bar - idle / rate)

        # AND THE HEIGHT ALONE CANNOT EXPRESS A QUORUM, WHICH IS WHY BOTH HALVES ARE HERE.
        # A floor is a sum, and one contributor at 2.0 clears any sum a quorum would set. The
        # honeybee rule is about HOW MANY AGREE, not how loudly one does -- so the count is
        # checked directly instead of being approximated by a number.
        #
        # POSITIVE ONLY. `episodes` can go negative, and a contribution arguing AGAINST is not a
        # vote for; counting it would let two objections constitute a quorum.
        voters = sum(1 for x in v.values() if x > 0)
        return {"vector": {k: round(x, 4) for k, x in v.items()},
                "total": round(total, 4), "threshold": round(threshold, 4),
                # UNROUNDED: a bar just above a failed total must read as above it on the row.
                "bar": bar, "bar_is": "earned" if bar_earned else "SEED",
                "relief_rate": round(rate, 4), "rate_is": "earned" if rate_earned else "SEED",
                "idle": idle, "voters": voters,
                "commits": total >= threshold and voters >= _QUORUM_VOTERS}

    def _commit_bar(self) -> tuple[float, bool]:
        """The height an override must reach, from how the agent's own overrides ended: the lowest
        level at which recency-weighted successes outnumber failures among outcomes at or above
        it. Moves both ways, fades at the agent's halflife, a ratio -- never a max (a ratchet)."""
        if not self._overrides:
            return float(MIN_REPEAT), False
        h = self.gamma.halflife or REJECTION_HALFLIFE
        ws = [(t, ok, 0.5 ** ((self.cycle - c) / h)) for t, ok, c in self._overrides]
        for lv in sorted({float(MIN_REPEAT), *(t for t, _ok, _w in ws)}):
            won = sum(w for t, ok, w in ws if ok and t >= lv)
            lost = sum(w for t, ok, w in ws if not ok and t >= lv)
            if won > lost:
                return lv, True
        return math.nextafter(max(t for t, _ok, _w in ws), math.inf), True

    def _relief_rate(self) -> tuple[float, bool]:
        """Idle cycles per unit of relief: the agent's own mean interval between commitments."""
        cs = self._commit_cycles
        if len(cs) < 2:
            return _IDLE_RELIEF, False
        return max(1.0, (cs[-1] - cs[0]) / (len(cs) - 1)), True

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
                         and it is the INTERFACE that answers that now, from a table `audit`
                         built out of this agent's own steps. `_goal_split` names the slot and
                         the direction. Never `act`, never the env
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
        slot = self._goal_choice(why=gwhy, book=True)
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
            elif gwhy.get("arrived") and not (gwhy.get("flat") or gwhy.get("rose")):
                reason = ("every objective held has ARRIVED -- nothing is left to pursue, so "
                          "this is neither the bar nor supply")
            else:
                reason = "no objective is confidently shrinking"
            # **`*` MEANT TWO THINGS AND THE GATE COULD SEE ONLY ONE -- `A6i` AT A LEDGER
            # KEY, 2026-09-28.** On the PERCEIVE rows `*` is the WHOLE-BOARD CENSUS (`can`,
            # `books`, `trend_popped`); here it meant NO PARTICULAR SLOT. The gate orders rows
            # per `(cycle, slot)`, so the two facts shared a chain and a planner with no
            # subject read as the board's own chain running backwards -- `PLAN after PERCEIVE`,
            # which is the refusal `can`'s site was already moved once to avoid.
            #
            # **LATENT, NOT NEW.** It needed `_mint_routine` to reach this gate in a cycle where
            # the census had already written, and on the toy world `discriminate` returned
            # first. Deleting that branch made it reachable; it did not create it. `@plan` is
            # its own key, in the `@board`/`@loop`/`@contact` convention already here.
            self.led.record(self.cycle, "PLAN", slot or "@plan", "routine_refused",
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
        # **THE OTHER ROUTE IS BUILT, AND THIS ROW SAID IT WAS NOT -- CORRECTED 2026-09-30.** It
        # read *not built ... a decay rate is a constant with no derivation available here, so it
        # is owed, not invented.* `_rejection` decays on the LOGICAL clock and the candidate
        # filter readmits a shape once its strength falls under 1.0 -- and `_rejection`'s own
        # docstring, in this file, says that route *was already built*. **Two comments
        # contradicting each other about one route, and the code agrees with the other one.**
        # **SINCE ITEM 1 (2026-10-07) THE FILTER READS `_refused`**, the shape-keyed refusal that
        # only growth lifts (Fig 6); this pop drops the slot Standing, which is now the VOTE.
        #
        # **THE RATE IS THE AGENT'S (Isaiah, 2026-09-30), AND SINCE ITEM 4 BOTH ROUTINE SITES PASS
        # IT** -- `refute` and `decay` take `gamma.halflife`, on the same cycle clock terms use.
        # Until the agent has a vindication, `halflife` is None and the seed applies, marked.
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
        self._split_why = None
        self._goal_want = None
        act = self._goal_split(before, commit=False)
        if act is None:
            # **CITE THE EXIT, DO NOT NAME ONE -- 2026-09-25.** This said *coverage incomplete,
            # or every action ties* for all five of `_goal_split`'s exits, and on gridworld
            # seed 11 the exit was actually `no_goal_read` on 4 of 4. **A refusal that names an
            # exit that did not fire is the same defect as `out_type-not-OBJ` describing a term
            # that was never the subject** -- a true-sounding string pointing at the wrong
            # mechanism, and the one thing a whitebox record must not do.
            #
            # **FOUR OF THE FIVE EXITS WENT WITH THE VOTES, AND THE MAP GOES WITH THEM.**
            # `coverage`, `no_goal_read`, `no_action_voted` and `all_tied` were properties of a
            # ballot over buttons; there is no ballot. Leaving their strings here would let
            # `_split_why` fall through to one of them and describe a mechanism that no longer
            # exists, which is the defect the comment above names.
            _why_txt = {
                "no_goal_term": "the chosen slot has no OBJ-typed goal term to read, in "
                                "`bound` or in the retained wants",
                "unordered_no_value_table": "the slot has no order, so I asked for a VALUE "
                                            "rather than a direction, and nothing I have done "
                                            "is known to leave it there reliably",
                "no_realisation": "I said which slot and which way, and nothing I have done "
                                  "here is known to move it that way",
            }.get(self._split_why, f"the split refused ({self._split_why})")
            self.led.record(self.cycle, "PLAN", slot, "routine_refused",
                            reason=_why_txt, split_why=self._split_why)
            return
        # **THE ALPHABET IS THE WRONG ONE NOW, AND IT IS LEFT WRONG ON PURPOSE -- 2026-09-28.**
        # `base` prices *naming an action myself for each unsatisfied member*, and the agent now
        # names INTENTS. The obvious repair -- count the intent space and use `log2` of that --
        # is the FLAT pricing Isaiah ruled against the same day (*"penny wise and pound foolish
        # ... they have different weight ... the agent may have to determine what types matter
        # per board and weight them dynamically"*), carried into a new alphabet while feeling
        # careful, because COUNTING an alphabet does not look like inventing a constant.
        #
        # So nothing changes here until that ruling lands. **The gap is PUBLISHED rather than
        # hidden** -- `intent_alphabet` beside it in the routine row -- because a wrong price
        # whose wrongness cannot be measured is worse than one with its gap printed. Reviewer,
        # 2026-09-28. Exemption as DATA: named, dated, and one line to remove.
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
                      if self._runnable(r, before, self.routine_lib))
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
        # **THIS CAP IS LOAD-BEARING FOR THE BARGAIN AND THE BARGAIN CANNOT SEE IT.**
        # `term_bits` prices LENGTH and ALPHABET -- a budget is neither -- so `until(g/3)` and
        # `until(g/99)` cost the SAME 6.9658 bits while `reach` is `budget * reach(body)` and
        # scales with it. `left` is `max(0, unsat - reach) * log2(n)`, so a bigger budget buys
        # a smaller `left` FOR FREE, and nothing in `pays` would refuse a term claiming
        # unbounded reach at a fixed price.
        #
        # WHAT STOPS IT IS THIS LINE: the budget is taken from the residual, so the agent
        # never proposes more reach than the gap needs. **The protection lives at the CALL
        # SITE and not in the pricing** -- raise this and the bargain has no defence, and the
        # place a reader would look for one is `term_bits`, which is specified to ignore it.
        loop_budget = max(int(round(unsat)), 1)
        _claim = unsat
        if _ROUTINE_SUBJECT_BUDGET:
            _gap = self._subject_gap(before)
            if _gap is not None:
                loop_budget = _claim = _gap
                self.led.record(self.cycle, "PLAN", slot, "subject_budget", budget=_gap,
                                group_budget=max(int(round(unsat)), 1),
                                subject=self._goal_want.subject)
        mine = tuple(s for s in sorted(self._disc) if s in before)
        # derived once: `reach` and `actions` both resolve a `Call` through it
        lib = self.routine_lib
        # THE COMPOUND GUARDS ARE APPENDED, so every shape reachable before this line is still
        # reachable and in the same order -- `cap` takes the shortest, and a compound guard now
        # costs its excess (`routine._guard_excess`), so it sorts AFTER the plain one it
        # extends rather than displacing it. **A looser guard has to be worth its extra bits.**
        gnames = mine or (slot,)
        # **THE BODY IS THE INTENT, NOT THE BUTTON -- the plan's 16, and the substitution is
        # one token wide because the enumeration was never over the action space.** `act` is the
        # ONE action `_goal_split` got back from the interface; `_goal_want` is what it ASKED
        # FOR. Planning in the ask means the loop re-realises every step, so a board that
        # re-maps mid-plan is followed rather than reported.
        #
        # `act` is still read -- above, as the gate that there IS a route at all. A plan for an
        # intent nothing can serve today is a plan that cannot start, and the agent has better
        # uses for the bargain.
        _step = self._goal_want if self._goal_want is not None else act
        cands = Rt.enumerate_routines((_step,), gnames + self._compound_guards(slot, gnames),
                                      shelf, loop_budget)
        # WEIGHTED AND CLOCKED, per §18.2 via `gamma.Standing`: a refutation excludes only while
        # its decaying strength stands, so a failed shape leaves the running and returns.
        _offered, _gap0 = len(cands), self._characterise_gap(slot)
        cands = [c for c in cands if not self._refused(self._refusal_key(_gap0, c))]
        # **THE AGENT SAYS HOW MANY IT EXPECTS -- ISAIAH, 2026-09-30.** `loop_budget` is
        # `round(unsat)`, and `reach` multiplied it back out, so a routine's CLAIM WAS ITS OWN
        # SAFETY CAP: the plain loop reached exactly the residual and could at best tie, and a
        # smaller residual shrank what a routine was ALLOWED to claim (measured: reach 5 -> 1
        # when the library-fit gate changed). `expect` is the claim; `budget` stays the cap.
        cands = [self._expected(c, _claim, before) for c in cands]
        if not cands:
            self.led.record(self.cycle, "PLAN", slot, "routine_refused",
                            reason="every plan offered was refused under this scope, "
                                   "and the scope has not grown",
                            offered=_offered,
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
            scored = [(self.paths.get((gkey, self._step_ids(c), Rt.guards(c)),
                                      {}).get("failed", 0), c) for c in cands]
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
        # **AND A PLAN THAT CANNOT ACT IS DROPPED HERE, WHICH IS THE SITE `reach` NAMES.**
        # `reach(Until)` is `budget * reach(body)` and over-states whenever the guard already
        # holds -- its docstring says so, says the repair *needs state this function must not
        # have*, and points at this gate. Measured on gridworld seed 11 cycle 20:
        # `until(o0.row/3) {down}` priced at `reach 3` with `o0.row` ALREADY 3.
        #
        # **IT IS NOT A PRICING FIX AND THAT IS THE POINT.** `advance` returns DONE for a
        # routine whose guard already holds, and DONE is what SHELVES a routine -- so buying
        # one would have put a no-op on the shelf, callable at a name's price and claiming its
        # budget's reach, forever. The bargain refused this one by 0.97 bits and would not
        # have refused a cheaper one.
        _holds = self._holds(before)
        _live = [(c, lf, r) for c, lf, r in priced if not Rt.inert(r, _holds, lib)]
        if len(_live) < len(priced):
            self.led.record(self.cycle, "PLAN", slot, "routine_inert",
                            reason="dropped: the plan's own termination condition already "
                                   "holds, so it would end before acting",
                            dropped=len(priced) - len(_live), considered=len(priced))
        ok = [(c, lf, r) for c, lf, r in _live
              if all(self.can(g, before) == YES for g in Rt.guards(r))]
        if not ok:
            self.led.record(self.cycle, "PLAN", slot, "routine_refused",
                            reason=("every candidate would end before acting -- its own "
                                    "termination condition already holds")
                                   if priced and not _live else
                                   "no candidate's guards are all reachable here",
                            considered=len(priced), live=len(_live))
            return
        cost, left, cand = ok[0]
        if _TWO_READINGS:
            cost, left, cand = self._two_readings(slot, ok, base)
        _ov = None
        if not pays(cost, left, base):
            # **THE BARGAIN KEEPS ITS PRICE AND LOSES ITS MONOPOLY -- ISAIAH, 2026-09-25.**
            # `pays` still says whether a plan is worth BANKING. It stops being the only route
            # from wanting to doing, because *the agent is always paying with its time* and a
            # refusal that costs nothing lets an agent draft forever and look optimal.
            _acc = (self._accumulate(slot, self._gap_key(gap) if gap is not None else None)
                    if self.cfg.accumulate else {"commits": False})
            self.led.record(self.cycle, "PLAN", slot, "routine_cut",
                            reason="does-not-pay", routine=Rt.render(cand),
                            cost=round(cost, 4), left=round(left, 4),
                            base=round(base, 4), reach=Rt.reach(cand),
                            reach_status=self._reach_seen(slot, cand),
                            considered=len(priced), shelf=len(shelf), **_acc)
            if not _acc["commits"]:
                _book_add(self.gamma.book, "accumulation_short")
                return
            # THE VECTOR CROSSED. The plan is adopted WITHOUT having paid, and the row says so
            # with every contribution named -- a lean that goes wrong must be a finding and
            # not a mystery.
            _book_add(self.gamma.book, "committed_on_accumulation")
            _ov = _acc["total"]
            self.led.record(self.cycle, "PLAN", slot, "committed_on_accumulation",
                            reason="the bargain refused and the accumulation crossed anyway",
                            routine=Rt.render(cand), **_acc,
                            **({"confirm": _confirm_actions(cand)} if _TWO_READINGS else {}))
        # **WRAPPED IN AN EXPECTATION AT ADOPTION.** The source is hardcoded and says so: a
        # routine minted FOR a slot expects THAT SLOT to change. A per-step predicted VALUE
        # would need the term space; a predicted CHANGE needs only the delta already published.
        # `Expect` rebuilds around the remainder, so the claim is re-made every step rather
        # than once at the start.
        self.routine, self.routine_for = Rt.Expect(slot, cand), slot
        self._routine_acts = 0                 # this plan's own tally, not the last one's
        self._last_commit = self.cycle         # the clock the threshold reads restarts here
        self._commit_cycles.append(self.cycle)
        self._override_open = _ov              # an override's outcome is recorded at its end
        self._routine_adopted = self.routine   # what to shelve; `advance` will erode it
        self._plan_no += 1
        self._plan_sig = self._gap_key(gap) if gap is not None else None
        _mint_row = self.led.record(
                        self.cycle, "PLAN", slot, "routine", verdict="pays", plan_no=self._plan_no,
                        **({"mc4": self._mc4(cand)} if _MC34 else {}),
                        routine=Rt.render(cand), length=Rt.length(cand),
                        units=Rt.length(cand, shelf),
                        chunked=Rt.length(cand) != Rt.length(cand, shelf),
                        cost=round(cost, 4), left=round(left, 4),
                        base=round(base, 4), gap=gap, reach=Rt.reach(cand),
                        # PRICED ON `n` ACTIONS AND PLANNED IN INTENTS -- the gap, printed.
                        # Distinct intents formed so far, which is a run population and not
                        # an enumerated space. See the note at `n`.
                        priced_alphabet=len(self.actions),
                        intent_alphabet=len(self._intent_kinds),
                        reach_status=self._reach_seen(slot, cand),
                        unsat=round(unsat, 4), considered=len(priced), shelf=len(shelf),
                        route="learned: observed to move this slot the wanted way")
        self._plan_seqs[self._plan_no] = _mint_row.seq     # 5b: the routine's own seq
        if _D13:
            self._process_bet("plan_clears", slot, plan_no=self._plan_no,
                              need=_confirm_actions(cand), plan_seq=_mint_row.seq)

    def _term_of(self, slot: str | None) -> dict | None:
        """5b: the objective term `_goal_target` reads for this slot, by the same lookup, with its
        seq (the gamma stamp's, or None and why)."""
        if _WANT_TARGET:
            name, term = self._objective_of(slot) if slot else (None, None)
            if getattr(term, "out_type", None) != OBJ_TYPE:
                return None             # a predictor is not an objective: neither is here
        else:
            name, term = self._target_lookup(slot) if slot else (None, None)
        if term is None:
            return None
        tname = getattr(term, "name", name)
        seq = self.gamma.stamps.get(tname, {}).get("seq")
        kind = "bound" if self.bound.get(slot) == tname else (
            "want" if name == tname else "want_term")
        return {"kind": kind, "name": tname, "slot": slot, "seq": seq,
                **({} if seq is not None else {"why": "not in the library"})}

    def _routine_entries(self) -> list[dict]:
        """5b: the routine whose step acts (role body) and the objective its guards read (goal)."""
        seq = self._plan_seqs.get(self._plan_no)
        out = [{"kind": "routine", "name": f"plan {self._plan_no}", "slot": self.routine_for,
                "seq": seq, "role": "body",
                **({} if seq is not None else {"why": "adopted without a mint row"})}]
        goal = self._term_of(self.routine_for)
        if goal is not None:
            out.append({**goal, "role": "goal"})
        return out

    def _objective_of(self, slot: str) -> tuple:
        """F2 (the reviewer 2026-10-11 05:38Z): this slot's objective, ONE lookup for every
        reader -- the bound term if it is an objective, else the retained want (library first,
        then _want_terms). goal_residual's order since it was written; _goal_target and _term_of
        read it under TETHER_WANT_TARGET, so the selector and the target cannot disagree."""
        name = self.bound.get(slot)
        term = self.gamma.library.get(name) if name else None
        if _A1_OBJECTIVE and getattr(term, "out_type", None) == OBJ_TYPE:
            # A1: a bound objective and a retained want both name this slot's objective; they are
            # weighed (settled here gates; bits; grade events), never "bound first". One pick per
            # (cycle, slot), so the selector and the target cannot disagree.
            _w = self.wants.get(slot)
            _wt = (self.gamma.library.get(_w) or self._want_terms.get(slot)) if _w else None
            if _wt is not None and _w != name:
                if self._obj_pick.get("cycle") != self.cycle:
                    self._obj_pick = {"cycle": self.cycle}
                if slot not in self._obj_pick:
                    opts, res, grades = [], {}, {}
                    for n, t in ((name, term), (_w, _wt)):
                        st = self.gamma.standing.get(n)
                        opts.append((n, term_bits(self.gamma.length(t, self._units_for(slot)),
                                                  self.gamma.alphabet), None))
                        res[n] = int(self.gamma.is_settled(n, slot))
                        grades[n] = (len(st.settled_on) + (1 if st.rejections else 0)) if st else 0
                    self._obj_pick[slot] = self._choice("objective", slot, opts, res, grades)
                if self._obj_pick[slot] == _w:
                    return _w, _wt
            return name, term
        if getattr(term, "out_type", None) != OBJ_TYPE:
            _w = self.wants.get(slot)
            _wt = (self.gamma.library.get(_w) or self._want_terms.get(slot)) if _w else None
            if _wt is not None:
                name, term = _w, _wt
        return name, term

    def _target_lookup(self, slot: str) -> tuple:
        """The target's lookup with TETHER_WANT_TARGET OFF: bound-or-want, so a val predictor bound
        on the slot masks its want (the known split, LEDGER (A)). Under TETHER_WANT_TARGET_SUBJECT
        a SUBJECT-SCOPED want (a goal-condition want, `_want_scope`) is read through
        `_objective_of` instead; every own want stays masked."""
        name = self.bound.get(slot) or self.wants.get(slot)
        term = (self.gamma.library.get(name) if name else None) or self._want_terms.get(slot)
        if (_WANT_TARGET_SUBJECT and getattr(term, "out_type", None) != OBJ_TYPE
                and self.wants.get(slot) is not None
                and self._want_scope.get(slot) == self.wants.get(slot)):
            return self._objective_of(slot)
        return name, term

    def _goal_target(self, slot: str, before: dict[str, int]) -> int | None:
        """What the agent's OWN objective predicts this slot should become, or None.

        Reuses `_value_of` -- *the edge from a term to a number, in one place* -- rather than
        recomputing it, so the intent and the bet cannot disagree about what the term MEANS.
        `None` where the slot already HOLDS (`objective_step` returns `current`), where nothing
        satisfies, or where no OBJ-typed term is there to read.
        """
        name, term = (self._objective_of(slot) if _WANT_TARGET else self._target_lookup(slot))
        # WHICH None, NOT THAT None (F207; the reviewer 2026-10-11 06:24Z): each exit is a
        # different fact, named in `_gt_which` for the refusal row; the return is unchanged.
        self._gt_which = None
        if term is None or getattr(term, "out_type", None) != OBJ_TYPE or slot not in before:
            self._gt_which = "no_obj_term"
            return None
        if not self._applies(term, before):
            self._gt_which = "not_applies"
            return None
        ops = self._ops(term, before)
        if ops is None:
            self._gt_which = "no_operands"
            return None
        ctx = self._eval_ctx(slot, before, action=self._last_action or "", operands=ops,
                             touching=self._touching(slot), shapes=False,
                             landed=self._last_landed)
        tgt = self._value_of(term, slot, before, ctx)
        if tgt is NOT_RESOLVED:
            self._gt_which = "not_resolved"
            return None
        if not isinstance(tgt, int):
            self._gt_which = "not_int"
            return None
        if tgt == before[slot]:
            self._gt_which = "already_holds"
            return None
        return tgt

    def _undirected(self, before: dict[str, int]) -> str | None:
        """*Something, no preference* -- asked of the interface, which picks the button.

        **THE SEAM, AT THE LAST SITE ON THE ACTING PATH THAT STILL CHOSE AMONG NAMES.** This
        read `self.drive.choose(self.actions, ...)`: the reasoning side ranking action strings.
        The SWEEP is unchanged and now lives in `Interface.undirected`; what the agent keeps is
        its own trial record, via `note_draw`.

        **BYTE-IDENTICAL BY CONSTRUCTION, NOT BY LUCK** -- same formula, same seed (0 at both
        `Drive()` sites), same bookkeeping, same order. The refuter is therefore exact: any
        difference in the per-action SEQUENCE on a fixed seed is a defect, not sampling.
        """
        r = self.iface.undirected(tuple(self.actions), self.cycle, withheld=self._withheld,
                                  env=self.env)
        if r is None:
            return None
        return self.drive.note_draw(self._took(r), _where(before))

    def _took(self, r: Any, want: Any = None) -> str:
        """Accept a `Realisation`: keep its aim and its INTENT, return its action. **One door,
        so no exit can drop either again.**

        **THE INTENT IS KEPT BECAUSE THE BET HAS TO CARRY IT** -- `TRAINING_PLAN` ~405, Isaiah
        2026-09-14: *RL trains on the REASONING/COMPOSITIONS ... never on the actions. Actions
        are doubly irrelevant: not the reward target AND not the training substrate.* The bet
        row named NEITHER the action nor the intent, so what the agent MEANT was unrecoverable
        from the record it keeps of its own predictions.

        Fixture B caught `_explore` returning `r.action` and discarding `r.coord`, so on a
        click-only world every press went out unaimed and 24 steps produced ZERO contact. The
        interface was aiming correctly and the loop was throwing it away -- **a value that
        exists and never crosses**, which is the defect this project files most often.
        """
        self._aimed = r.coord
        self._last_real = r                 # 5b: the realisation the taken press came from
        self._intent_now = want
        # The alphabet census was filled at `_realise_step` and `_mint_routine` and NOT here,
        # so it read 0 on 24 cycles where every exit named an intent. LOWER BOUND: an intent
        # formed in `choose` that fails to realise never reaches this door.
        if want is not None:
            self._intent_kinds.add(want.kind)
            self._note_decision(want)
        return r.action

    def _note_decision(self, want: Any) -> None:
        """**A CONFLICT THE AGENT WAS IN -- NOT YET A DECISION IT MADE.**

        **THE DISTINCTION IS THE REVIEWER'S, 2026-09-29, AND I HAD OVER-CLAIMED IT.** I filed
        these as decisions and reported *16 of 16, the agent disturbed a held goal every time*,
        which reads as the agent weighing the evidence and choosing exploration. **It did not.
        NOTHING READS `because` AT THE MOMENT OF CHOOSING** -- the evidence is recorded beside a
        choice the default path made regardless of it. **16 of 16 is what happens when nothing
        weighs the evidence at all**, and that is a different fact.

        **SO THE ROW IS LABELLED `conflict, not yet weighed` UNTIL SOMETHING READS IT.**

        **AND THE MISSING PIECE IS NAMED RATHER THAN LEFT AS A GAP:** for the agent to decide
        without a fixed policy it must predict WHAT EACH BRANCH LEADS TO -- the intent-level
        prediction `(before, intent, after)`. That is what would let `because` change the
        choice. Until it exists, this row is history and not agency.

        ISAIAH, 2026-09-29: *1 and 2 should be the agent's decision, and they should record
        choosing that for history and so they can backtrack.* **So nothing here decides
        anything.** The agent's existing exits already chose; what was missing is that the
        choice was never written down, so no history could be read off it and nothing could be
        backtracked to.

        **A DECISION EXISTS ONLY WHERE THIS INTENT HAS A RECORDED HISTORY OF UNDOING AN
        OBJECTIVE THAT CURRENTLY HOLDS.** Not *any* intent, and not a guess about effects: the
        evidence is `_undone`, which the agent built from its own transitions. **A conflict the
        agent has no record of is not a decision it is in a position to make.**

        `holds` reuses the selector's own arrived test -- last reading at or below zero -- so
        the gate and this row cannot drift apart on what *satisfied* means.
        """
        said = want.says()
        live = [(sl, n) for (_c, it, sl, _b), n in self._undone.items()
                if it == said and (self._res.get(sl) or [1.0])[-1] <= 0]
        if not live:
            return
        _slot, _n = max(live, key=lambda kv: kv[1])
        self.led.record(self.cycle, "PLAN", _slot, "decision",
                        chose=said,
                        # **THE ALTERNATIVE IS THE ABSTENTION, AND IT IS THE HONEST ONE.** At
                        # this door the other live options are not known -- `choose` has already
                        # picked. What IS known is the binary the conflict is actually about:
                        # take this intent and disturb a goal that holds, or hold off.
                        instead_of=("hold off -- leave the met objective alone",),
                        because={"undone_here": _n,
                                 "across": self._undone_across.get((said, _slot), 0),
                                 "repeated": _n >= MIN_REPEAT},
                        at=IFace.Interface.context(self.env),
                        status="conflict, not yet weighed",
                        reads="I have undone this objective with this intent before and it "
                              "holds right now -- recorded as a CONFLICT I was in, not a "
                              "decision I made: nothing read this before the choice")

    def _realise_step(self, emit: Any, before: dict[str, int]) -> str | None:
        """A routine step is an INTENT. Turn it into a button, or `None` if nothing serves it.

        `docs/ACTION_INTERFACE_PLAN.md` §16. **THE RESOLUTION HAPPENS EVERY STEP, NOT ONCE AT
        CONSTRUCTION**, and that is the behaviour change rather than a tidy-up: a loop that
        re-realises can follow a board which re-maps its buttons mid-plan, which is Isaiah's
        *"we are now no longer able to go (direction)"* becoming something the agent survives
        instead of something it reports afterwards.

        A bare string still passes through, because a fixture testing the SHAPES of routines has
        no interface to consult and should not have to build one.
        """
        if isinstance(emit, IFace.Intent):
            self._intent_kinds.add(emit.kind)
            r = self.iface.realise(emit, tuple(self.actions),
                                   IFace.Interface.context(self.env), before, self.env,
                                   withheld=self._withheld)
            if r is None:
                return None
            self.led.record(self.cycle, "PLAN", emit.subject or "@board", "intent",
                            reads=(emit.says(), r.why))
            return self._took(r, emit)
        # 7a(5) C: a bare step the floor vetoes here is unrealisable, unless every action is
        _w = self._withheld
        if _w.action(emit) and not all(_w.action(a) for a in self.actions):
            return None
        return emit if emit in self.actions else None

    def _goal_split(self, before: dict[str, int], commit: bool = True) -> str | None:
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
            the ROUTE    NOT HERE ANY MORE, and that is the point. The interface's delta
                         table answers it, built by `audit` from steps THIS AGENT took. This
                         function names a slot and a direction and never an action

        **`act` IS WHAT THIS MUST NOT BECOME**, and the difference is provenance alone: *it has
        never had to learn what pressing something does, because the primitive it was given
        already knew.* **That prohibition MOVED WITH THE MECHANISM rather than being dropped** --
        an empty delta table produces no preference either, which is what a closed-over effect
        table can never do.

        NEAREST IS THE TYPE'S, AND IT IS `objective_step`'s SPLIT REUSED RATHER THAN A SECOND
        ONE INVENTED. `ORDERED` has a direction, so *toward* is the sign of the wanted step;
        `COMPARABLE`-only has none, so *toward* can only be *did this action ever produce that
        value*. **Two arms because the type system has two, not because two cases turned up.**
        **AND ONLY THE ORDERED ARM IS SERVED BELOW THE SEAM**: `audit` records a signed delta
        and never a value reached, so the COMPARABLE arm abstains by name at
        `unordered_no_value_table` rather than reading as *nothing moves it*.

        COVERAGE AND THE ONE-SLOT-ONE-VOTE RULE WENT WITH THE VOTES, and neither was lost.
        `ARC_BUILD_PLAN`'s *goal pursuit gated on a complete action map* is now the interface's
        job: `realise` abstains where it has not watched the action, which is the same refusal
        keyed on the same evidence. And nothing here sums magnitudes across slots, because
        nothing here ranges over more than the ONE slot the selector chose.
        """
        # ITEM 3 GATES ITEM 2. Before the selector this ranged over EVERY OBJ-bound slot,
        # which is *pursue whichever objective happened to bind* -- and it measurably chose to
        # stand still, because `none_same` on a delta is satisfied by not moving. One selected
        # hypothesis, chosen on a shrinking discrepancy, is what §13.4 asks for.
        # **THIS EXIT RECORDED NOTHING, ONE LINE ABOVE A BRANCH WHOSE COMMENT CALLS AN
        # UNRECORDED-OR-WRONG REASON *the one thing a whitebox record must not do*.** Measured
        # on `buttons` and `click_only`: `_goal_split` refuses 5 of 5 times HERE, so the only
        # reason the goal never reaches the aim was the only reason not written down.
        #
        # **AND `_goal_choice` ALREADY BUILT THE ANSWER.** Its `why` parameter fills a tally --
        # `too_short` / `flat` / `rose` / `qualified` / `arrived`, plus `slots`, `longest` and
        # `needs`. The selector was always saying why it named nothing; no caller asked.
        _why: dict = {}
        chosen = self._goal_choice(_why)
        if chosen is None:
            self._split_why = "no_goal_choice"
            if commit:      # a probe writes no act rows; routine_refused names the why (5a')
                self.led.record(self.cycle, "PLAN", "@objective", "split_refused",
                                why="no_goal_choice", **_why)
            return None
        # **THE GOAL EXIT EMITS AN INTENT -- the first NON-exploratory one in the system.**
        # `docs/ACTION_INTERFACE_PLAN.md`. The selector above already chose the slot on the
        # agent's own objective, and `_value_of` already says what that objective PREDICTS for
        # it. **So the intent is assembled from parts that exist**: this slot, that way.
        #
        # **AND THE DIRECTION IS THE SLOT'S, NOT THE ACTION'S** -- `F28`'s line. The agent says
        # `o0.row +`; it does not know `down` exists. A board that renamed its buttons would
        # change nothing here.
        _tgt = self._goal_target(chosen, before)
        # **THE INTENT TAKES THE TYPE'S OWN SHAPE, and it is `objective_step`'s split reused
        # rather than a second one invented.** An ORDERED slot has a direction to want, so the
        # intent carries a SIGN. A COMPARABLE-only slot has none -- *make it 3* is the only
        # thing there is to say -- so it carries a VALUE. **Two arms because the type system has
        # two**, and the two never share a field (`A6i`, and see the plan's 15).
        #
        # THE AGENT STILL NAMES NO ACTION IN EITHER ARM. `o0.colour = 3` is as button-blind as
        # `o0.row +`; which press achieves it is the interface's to know.
        if _tgt is None:
            # **AND THIS IS ITS OWN REFUSAL, WHICH IT WAS NOT IN `4c233db` -- CORRECTED THE SAME
            # DAY.** It fell through to `no_realisation`, whose sentence is *I said which slot
            # and which way, and nothing I have done here is known to move it that way.* **The
            # agent never said which way.** `_goal_target` returns `None` where the slot ALREADY
            # HOLDS, where nothing satisfies, or where no OBJ-typed term is there to read --
            # three states about the OBJECTIVE, reported as a fact about the ACTION MODEL.
            # A true-sounding string pointing at the wrong mechanism, which is the one thing a
            # whitebox record must not do.
            self._split_why = "no_goal_target"
            if commit:
                self.led.record(self.cycle, "PLAN", chosen, "split_refused",
                                why="no_goal_target", which=self._gt_which,
                                at=before.get(chosen))
            return None
        _ordered = self.slot_types.get(chosen) in ORDERED_TYPES
        _want = (IFace.Intent(IFace.BECOME, chosen, "+" if _tgt > before[chosen] else "-")
                 if _ordered else
                 IFace.Intent(IFace.BECOME, chosen, value=_tgt))
        # **KEPT, NOT THROWN AWAY -- the plan's 16.** `_mint_routine` plans in INTENTS and this
        # is the one place the intent is formed. Re-forming it there would be two producers of
        # one fact, which is harmless exactly until one side changes.
        self._goal_want = _want
        self._intent_kinds.add(_want.kind)
        _r = self.iface.realise(_want, tuple(self.actions),
                                IFace.Interface.context(self.env), before, self.env,
                                withheld=self._withheld)
        if _r is not None:
            # FORMED IS NOT TAKEN (the reviewer 2026-10-10 12:27Z, 12:36Z). The routine mint asks
            # which press would serve this intent and does not press it this turn, so it writes no
            # intent row and leaves _aimed / _intent_now to the exit that acts.
            if not commit:
                return _r.action
            self._split_term = self._term_of(chosen) if _FED else None
            if _7J_TEST:
                _tt = self._split_term or self._term_of(chosen) or {}
                self._test = {"slot": chosen, "term": _tt.get("name"), "target": _tgt,
                              "before": before.get(chosen), "intent": _want.says()}
            self.led.record(self.cycle, "PLAN", chosen, "intent",
                            reads=(_want.says(), _r.why))
            return self._took(_r, _want)
        if not _ordered:
            # **THE TWO REFUSALS ARE NOT ONE REFUSAL.** On an ordered slot, unserved means
            # *nothing I have done moves it that way*. Here it means *nothing I have done
            # reliably LEAVES it there* -- and the interface refuses a cell holding several
            # values on purpose, so this fires on an action that once landed the value and
            # was never shown to do it again. Collapsing them would report a capability gap
            # as an absence of effect.
            self._split_why = "unordered_no_value_table"
            if commit:
                self.led.record(self.cycle, "PLAN", chosen, "split_refused",
                                why="unordered_no_value_table", target=_tgt,
                                slot_type=self.slot_types.get(chosen))
            return None
        # **THE INTERFACE ABSTAINED, AND THERE IS NO FALLBACK BEHIND IT ON PURPOSE.**
        # `docs/ACTION_INTERFACE_PLAN.md`. What stood here voted over `self.actions` using
        # `_predict` -- the agent scoring BUTTONS with its own world-model, which is the exact
        # crossing the seam exists to refuse. Its other input, `hist`, WAS the delta table:
        # `{action: [(before, after)]}` from `self.trace`, scored by direction moved. Same
        # information, same population. **So nothing was relocated; one half was already below
        # the seam and the other half was the violation.**
        #
        # WHAT IT COSTS, PRE-REGISTERED BEFORE THE DELETION so it cannot later be read as a
        # regression: `_predict` could rank an action in a situation the TABLE HAS NEVER SEEN,
        # and the table by construction cannot. That capability is not lost in the design --
        # it belongs to intent-level prediction, `(before, INTENT, after)` -- but it is NOT YET
        # BUILT, so **this exit fires less until it is**, and that is the expected direction.
        self._split_why = "no_realisation"
        if commit:
            self.led.record(self.cycle, "PLAN", chosen, "split_refused",
                            why="no_realisation", target=_tgt,
                            n_actions=len(self.actions))
        return None

    def members(self) -> dict:
        """Who passed the contingency gates, and which gate dropped the rest.

        `sep[a]` is bounded by the member count, so ONE passing member makes `sep` 0/1 valued
        and the argmax returns whatever that member found distinctive -- which would be the
        family reporting faithfully rather than the selector failing. The gates are counted
        apart because coverage and stability are different causes."""
        # **REPORTED HERE, COMPUTED BELOW THE SEAM -- 17.** The counters live on the
        # interface now, because the computation does. The agent may READ its own instruments;
        # what it may not do is choose a button from them.
        return {"per_member": dict(sorted(self.iface.member_gates.items())),
                "passed_per_call": dict(sorted(self.iface.sep_passes.items())),
                # THE SHAPES, WITH THEIR COUNTS -- and `agreed` is row 2's field, which the
                # first version of this instrument did not have: mass on ONE action while
                # several members passed is unanimity, and unanimity decides nothing.
                "sep_shapes": {str(k): v for k, v in sorted(
                    Counter(e["sep"] for e in self.iface.sep_log).items(),
                    key=lambda kv: -kv[1])},
                "agreed": sum(1 for e in self.iface.sep_log
                              if e["passed"] > 1 and sum(1 for v in e["sep"] if v) == 1),
                # `at_audit`, NOT `cycle`: the interface counts PRESSES and has no cycle. The
                # field is renamed rather than silently re-meaning the old one.
                "trajectory": [(e["at_audit"], e["passed"], e["sep"])
                               for e in self.iface.sep_log],
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
        # **THE DIFF IS THE INTERFACE'S, READ AS CAPABILITY -- queue item 2(c), 2026-10-05.** This
        # compared action NAMES above the seam. `perceive` already asked the interface once; a
        # second `capability()` call would see nothing, because it is a stateful diff.
        cap = getattr(self, "_last_cap", None)
        # §16.8 SENSOR 1 IS `the PREVIOUS ACTION changed the gating`, and the delta alone
        # does not say which action. This runs at the top of the step, so the action just
        # taken is the only candidate -- and attributing it is also sensor 2's whole input.
        #
        # NOTED EVERY STEP, INCLUDING THE STEPS THAT CHANGED NOTHING. An edge's denominator
        # is how often the predecessor was taken, and a no-change step is precisely the case
        # where it was taken and the edge did NOT fire. Returning early here counted only
        # the successes, so every edge read as a rule and none could read as gated.
        self._last_cap = None
        if cap is None or not cap.moved():
            self.actions = now
            return
        self.led.record(self.cycle, self._running_step, "@instrument", "advertised",
                        opened=len(cap.opened), closed=len(cap.closed),
                        was=len(self.actions), now=len(now),
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
            # AND THE WANTS, WHICH THIS LOOP ALSO MISSED -- the same omission as the trends
            # one line up, found the day `_want_terms` gave the wants a second home. A want
            # on a departed slot is a hypothesis about an object that is gone.
            self.wants.pop(g, None)
            self._want_terms.pop(g, None)
        # a term bound to a SURVIVING slot may read an operand on a departed one, and
        # `_ops` would fault on the next bet. It owes again rather than faulting.
        orphaned = sorted(k for k, n in self.bound.items()
                          if self.gamma.library[n].operand in gone)
        for k in orphaned:
            self.bound.pop(k, None)
            self.owed_import.add(k)
        self.led.record(self.cycle, self._running_step, "@instrument", "present",
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
        self._kind_cache = {}   # 7l: kinds read fresh

    def _guards(self, robs: list, slot: str | None = None,
                refs: list[str] | None = None) -> list[str | None]:
        """Which INTENT a guard may name. **None first, and then only what R contains.**

        **ISAIAH, 2026-09-29 (ruling 1): guards name INTENTS, not buttons.** This yielded the
        ACTIONS appearing in the residual -- so a guard was a claim about which button was
        pressed, and above the seam the agent names no buttons. It could only ever have been
        learned by the interface leaking upward.

        The bound is unchanged in KIND: the candidate set is what the residual's own rows
        contain, *let the residual say where to look*, the same bound `_cannot_pay` uses. It
        is now the intents those rows carry, which the trace records as of `536fab2`.

        **`NO_INTENT` IS A CANDIDATE LIKE ANY OTHER, AND DELIBERATELY SO.** *This term is wrong
        exactly when I acted without meaning anything* is a real and checkable claim; excluding
        it would be deciding for the agent that the distinction cannot matter.

        **None first for the same reason `_bindings` puts it first** -- an unguarded term is
        cheaper, so it wins when both fit, which is Occam priced rather than preferred.
        """
        # **`ACTED_SELF` IS OFFERED WHEN IT SEPARATES R FROM THE REST -- the reviewer,
        # 2026-10-01, correcting a condition of mine that had it backwards.** I first offered
        # it only where the boolean VARIES WITHIN R: the wrong population, because the
        # incumbent is wrong on exactly the rows a guard would excuse, so those rows SHARE the
        # value by construction. **A uniformly one-way residual is the SIGNATURE OF A MISSING
        # GUARD, not evidence against one.** Constant in R with the other value present
        # OUTSIDE -- not disjoint; demanding that took the funnel from 8,031 built to zero.
        # Counts, not sets: a history row holds a state DICT and is not hashable.
        out: list[str | None] = [None, *sorted({i for _, _, _, i, _ in robs if i is not None})]
        # **ASKED PER REFERENT -- item 7(a), 2026-10-05.** The test was asked only about the
        # slot's OWN object, so a slot moved by ANOTHER object's press was never offered a
        # guard naming that object. `refs=None` keeps the old question (own owner only).
        if robs and slot is not None:
            asked = refs if refs else [slot.rsplit(".", 1)[0]]
            if _ACTED_GUARD and any(self._separates(robs, slot, r) for r in asked):
                # **THE RANDOMISED HOLD -- the reviewer, 2026-10-03 ruling 3. MEASUREMENT
                # ONLY.** The offer is ELIGIBLE here; on a seeded coin-flip share of
                # eligible occasions it is WITHHELD, so every ?ACTED reading has a
                # within-run control BY CONSTRUCTION rather than needing a second run.
                #
                # **ELIGIBILITY IS DECIDED FIRST AND RECORDED EITHER WAY**, which is the
                # whole point: a hold counted over ALL cycles would divide by occasions the
                # guard could never have taken, and the share would read low for a reason
                # that is not the hold. The denominator is eligible occasions.
                #
                # Keyed on (cycle, slot) through the run's own seed, so the pattern is
                # REPRODUCIBLE and a row can be replayed. `_HOLD` is off in the shipping
                # agent and the arms registry refuses it being on by default.
                self._hold_eligible += 1
                self._hold_keys.add((self.cycle, slot))
                if _HOLD and self._held_now(slot):
                    self._hold_withheld += 1
                    self._hold_keys_held.add((self.cycle, slot))
                else:
                    out.append(ACTED_SELF)
        return out

    def _separates(self, robs: list, slot: str, ref: str) -> bool:
        """Is landing on `ref` CONSTANT across R and the other value present OUTSIDE R?
        The test `_guards` always applied, now asked of any referent rather than only the
        slot's own owner."""
        hist = self.history(slot)
        h_true = sum(1 for _s, _a, _v, _i, land in hist if _same_object(land, ref))
        r_true = sum(1 for _s, _a, _v, _i, land in robs if _same_object(land, ref))
        out_true = h_true - r_true
        out_false = (len(hist) - h_true) - (len(robs) - r_true)
        return r_true in (0, len(robs)) and (out_true if r_true == 0 else out_false) > 0

    def _guard_refs(self, slot: str | None, binds) -> list[str]:
        """Which objects a guard may point at. **READ OFF THE WORLD, NEVER INVENTED.**

        The owners of the slots `_bindings` already offers, plus the slot's own owner --
        because `?ACTED_SELF` is `?ACTED_ON<own owner>` and collapsing them means the own
        owner is one referent among the rest rather than a privileged case.

        **NO NEW SOURCE.** `_bindings`' own rule is *you do not invent the list, you read it
        off the world*, and this is that list reduced to owners. A referent the world does
        not offer cannot be named, which is what keeps the guard from naming a button the
        agent has not seen.
        """
        own = slot.rsplit(".", 1)[0] if slot else None
        refs = {b.rsplit(".", 1)[0] for b in binds if b}
        if own:
            refs.add(own)
        return sorted(refs)

    def _set_seed(self, seed: str, generation: int, seed_source: str) -> None:
        """One seed for the being: the mind's draws, the interface's and the minted handles. ON, the
        draw seed carries the generation index, so a continued life does not replay its day (the
        reviewer 15:04 Q1); OFF, it is the old constant exactly."""
        self.seed, self.generation, self.seed_source = seed, generation, seed_source
        self.draw_seed = seed if seed_source == "constant" else f"{seed}:{generation}"
        self.iface.draw_seed = self.draw_seed
        self.gamma.draw_seed = None if seed_source == "constant" else self.draw_seed

    def _seed_from_lineage(self, seeds: set, n: int, tip: str) -> None:
        """The same being, continued (the reviewer 15:04 Q1): the lineage's seed and its length as
        the generation index. A replay already carries both, and OFF has no seed to carry. A chain
        carrying no seed (written before HOLD_SEED) or more than one keeps the birth seed, and says
        so in the row."""
        if self.seed_source == "constant" or self.seed_source.startswith("replay:"):
            return
        if len(seeds) == 1:
            seed, src = next(iter(seeds)), f"lineage:{tip}"
        else:
            seed, src = self.seed, ("birth; the lineage carries no seed" if not seeds else
                                    f"birth; the lineage carries {len(seeds)} seeds")
        self._set_seed(seed, n, src)
        self.led.record(0, "PLAN", "@run", "seed", seed=seed, generation=n, seed_source=src,
                        lineage_seeds=sorted(seeds))

    def _held_now(self, slot: str | None) -> bool:
        """Is THIS eligible occasion in the withheld half? Seeded, so a run replays.

        **NOT `random.random()`.** An unseeded flip makes the hold pattern unrecoverable,
        and a row whose treatment cannot be reconstructed is a row that cannot be checked.
        """
        import hashlib
        key = f"{self.draw_seed}:{self.cycle}:{slot}".encode()
        return hashlib.blake2b(key, digest_size=8).digest()[0] < 128      # ~0.5

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
        if bind is None or not self.slot_types:
            return True
        _lg = lag_of(bind)
        got = self.slot_types.get(_lg[0] if _lg is not None else bind)
        # THROUGH THE TREE: the slot feeds the inner chain first, so each inner atom must
        # accept what reaches it, and what fills the operand is the chain's OUTPUT. `val`
        # declares nothing -- it admits and passes the type through (F470).
        for a in getattr(getattr(cand, "operand_term", None), "atoms", ()):
            if (a.in_type != "val" and got is not None and got not in a.accepts
                    and frozenset((a.in_type, got)) not in COMMENSURABLE):
                return False
            if a.out_type != "val":
                got = a.out_type
        if want is None:
            return True
        if want == G_SAME:
            want = self.slot_types.get(target)
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
        # `*_` -- this row gained the INTENT on 2026-09-29 and this site was missed twice:
        # once by scoping the search to one file, once by EXCLUDING that file from the
        # repo-wide search. The pattern, not the file, is what has to be searched.
        seen = {s: len({st[s] for st, _a, _v, _i, _l in robs if s in st}) for s in others}
        # ITS OWN PREVIOUS VALUE, ONE CANDIDATE, ordered like the rest by how much it varies.
        if _PREV_OFFER and not _WINDOW:      # under the window ~1 is one lag of the block below
            mine = slot + PREV
            seen[mine] = len({v for v in (self._operand_value(mine, st)
                                          for st, _a, _v, _i, _l in robs)
                              if v is not NOT_RESOLVED})
            others.append(mine)
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
        # THE LIBRARY'S WORD, AFTER CONTACT AND BEFORE VARIANCE (Fig 9: a lookup gives "a kind of
        # thing, never the answer itself"). An order, so every binding is still reached; it
        # matters because most mints stop on budget, where order decides what is reached.
        lib = self._named.get(slot, {}) if _LOOKUP_ORDER else {}
        # B2b, DERIVATION ORDER (the reviewer 2026-10-11 10:44 CDT): a derived slot (a pair
        # relation computed from other slots) comes after every slot it could be derived from --
        # it draws on the same evidence (Fig 13), so the higher-information operands are tried
        # first. An order, never a cut: once the ordinary operands are spent it is still reached.
        _der = getattr(self.env, "derived", None)
        _der = set(_der()) if _der is not None else set()
        if _A1_LOOKUP:
            # A1 sites 7-8 (the reviewer 2026-10-15 14:23, 14:27), the shape's order: the residual
            # GATE (contact with the open slot's owner), the ACTIONS walk (a derived slot is one
            # more composition step), BITS inside it (the library rows naming s), the residual
            # MAGNITUDE (distinct values over the failing frames), then the recorded draw.
            # Least-known has no reading here (7h's tried count, named), so it passes through.
            dk = f"{self.cycle}:{slot}:lookup_order"
            if _7M_ANALOGY:
                # 7m: the kind pairs that LANDED before, here or in the lineage (any entry, role)
                _pairs = self._kind_pairs   # kept as entries land and load (O(1) here)
                _mine = self._kind(slot.split(".")[0])
            comp = {s: (rank(s)[0], s in _der, len(lib.get(s, ())), seen[s],
                        *((-int((_mine, self._kind(s.split(".")[0])) in _pairs),)
                          if _7M_ANALOGY else ()),
                        *((self._tried[(self.level, slot, s)],) if _7H_TRIED else ()))
                    for s in others}
            self._bind_key[slot] = (dk, comp)
            out = [None] + _lookup_order(others, comp, dk, seed=self.draw_seed)
        else:
            out = [None] + sorted(others, key=lambda s: (s in _der, *rank(s), s not in lib,
                                                         -seen[s], s))
        if _WINDOW:
            out += self._window_lags(slot, robs)
        return out

    def _window_lags(self, slot: str, robs: list) -> list[str]:
        """THE WINDOW'S OFFER (the reviewer 14:52Z, 18:10Z, 18:15Z): every lag the trace can
        reach, AFTER every other binding (whose order and position do not move), ranked
        evidence first and nearest first, then the rest nearest first. A ranked cut, never a
        filter (Fig 9): the budget decides how far down it is walked, and what it does not reach
        is counted in the mint's record."""
        reach = len(self.trace) - 1
        recs = [self._lag_evidence(slot, robs, j) for j in range(1, reach + 1)]
        order = ([r["j"] for r in recs if r["evidence"]]
                 + [r["j"] for r in recs if not r["evidence"]])
        no_ev = [r for r in recs if not r["evidence"]]
        self._window_info[slot] = {"offered": len(order),
                                   "evidence": [r for r in recs if r["evidence"]],
                                   "tested_no_evidence": sum(1 for r in no_ev if r["recurred"]),
                                   "untested": sum(1 for r in no_ev if not r["recurred"])}
        return [f"{slot}~{j}" for j in order]

    @_in_step("MINT")
    def mint(self, slot: str) -> None:
        """ONE MINT WITH ITS EVALUATION MEMO. A Ctx and an operand read are pure functions of
        their inputs, and inside one mint they repeat ~1,281x and ~740x (counted, default seed 0,
        2026-10-05). SCOPED TO THE MINT, and every entry holds a reference to the row it keys on,
        so no row can be freed and its id reused while the memo lives. Byte-identical by
        construction; checked on four worlds."""
        self._memo = {}
        try:
            return self._mint(slot)
        finally:
            self._memo = None

    def _retain_unpaid_want(self, slot: str, wanted: tuple, detail: dict) -> None:
        """The one writer of an unpaid objective want (Isaiah 2026-09-25): the mint's tail, and
        under TETHER_PARK_WANT the park return too."""
        self.wants[slot] = wanted[1].name
        self._want_terms[slot] = wanted[1]
        detail["want"] = wanted[1].name
        detail["want_paid"] = False
        detail["want_seen"] = wanted[2]        # attempts that have wanted this
        _book_add(self.gamma.book, "want_recurred", 1 if wanted[2] > 1 else 0)
        self.gamma.book["want_retained_unpaid"] = (
            self.gamma.book.get("want_retained_unpaid", 0) + 1)

    def _mint(self, slot: str) -> None:
        _priced0 = self._priced              # every candidate priced in THIS mint, trees included
        _lf_stats = {"yielded": 0, "beyond_depth": 0}   # M4 library-first, read only when ON
        self._window_info.pop(slot, None)
        _win_reached: set = set()            # TETHER_WINDOW: lag bindings the budget reached
        _pass2_chains = 0                    # item 2b: recorded chains pass 2 walked (its cost)
        _derived_chains, _derb = 0, set()    # B2b: recorded chains round 3 walked; derived binds
        _lf_ops: dict = {}
        _lf_seen: set = set()                # every chain the library yielded in THIS mint
        _lf_ev: dict = {}                    # A1 site 6: each library chain's evidence (entries)
        _lf_reached: list = []               # A1 rows: the rank each evidenced chain was walked at
        _best_rank = None                    # A1 rows: the rank the winner was priced at
        _ns_calls = 0                        # A1 rows: stream-share picks this mint
        # THE RECIPES ALREADY HELD, once per mint rather than per candidate. A library Term's
        # chain is its atoms joined; `enumerate_closure` yields BARE chains, so `cand.name` is
        # exactly this key. O(library) against a per-candidate walk that is orders larger.
        self._held_chains = {" . ".join(a.name for a in t.atoms)
                             for t in self.gamma.library.values()}
        # A TERM CAN BE IN THE LIBRARY ONLY IF ITS CHAIN IS A HELD RECIPE -- 2026-10-06. The library
        # is keyed by `name` at one write site, and a name is the atom-join then `<..>` then
        # `?..`; so the join decides -- unless an atom's own name carries one of those marks,
        # in which case this is False and every lookup runs as before.
        _sep_free = not any(m in a.name for a in self.gamma.atoms for m in ("<", "?", " . "))
        hist = self.history(slot)
        held = self.gamma.library[self.bound.get(slot, IDN)]
        base = self._accumulated(slot, held)
        # THE SEAL (H3(i)): a held rule reading an earlier frame leaves its unseen starts as its
        # leftover, and that alone can sit under the floor, so no rule -- not one explaining all of
        # it -- could pay. The starts are the held rule's own price (H1: "paid ONCE, inside its own
        # price"), so a challenger is priced against its WHOLE two-part length (DISCOVERY 503):
        # cost_c + left_c < cost_h + base_h. `base_held` stays what `explain` and the record read.
        base_held, unseal = base, None
        if _UNSEAL_START and lag_of(held.operand) is not None:
            starts = sum(1 for r in hist if self._no_earlier_frame(held, r[0]))
            if starts:
                cost_h = term_bits(self.gamma.length(held, self._units_for(slot)),
                                   self.gamma.alphabet)
                base = base_held + cost_h
                unseal = {"starts": starts, "held_cost": round(cost_h, 3),
                          "base_held": round(base_held, 3), "bar": round(base, 3)}
        robs = self._residual_obs(slot, held, hist)
        # **`robs` IS NOT THE HISTORY** -- it is the history filtered by what the BOUND
        # term got wrong, so a rebind changes which rows are in it and the list is no
        # longer an extension of the old one. `held` therefore belongs in the key.
        # `alphabet[slot]` is in it because 5021 rebuilds the alphabet mid-level WITHOUT
        # clearing the trace; keying costs one fresh walk for that slot and nothing else.
        # `_shapes_now()` is per-cycle and unhashable, so under the shape arm the cycle
        # enters the triple and the tally simply stops reusing -- OFF rather than WRONG.
        _tri = (held, self.alphabet[slot], self._trace_epoch,
                self.cycle if _SHAPE_DECODE else 0)
        _seen = self._tally.get(slot)
        if _seen is None or _seen[0] != _tri:
            _seen = (_tri, {})          # the slot moved; its old tallies can never be hit
            self._tally[slot] = _seen
        rkey = _seen[1]
        # HOISTED, because `units()` rebuilds a list and the pricing runs once per candidate.
        _units = self._units_for(slot)
        # THE CHEAPEST TERM THE COST FUNCTION ADMITS. `pays` is `cost + left < base`,
        # `_left` is a sum of non-negative bits, and `term_bits` is monotone in `k` with
        # `length() >= 1` -- so `floor >= base` proves NO term pays, at any depth, under
        # any binding, before a candidate is enumerated. Same lemma as the inner break
        # 170 lines down, applied as a precondition instead of a stopping rule.
        floor = term_bits(1, self.gamma.alphabet)
        guards = {"support": base > 0.0, "reachability": False, "novelty": False}
        cuts: list[dict] = []
        # THE RECORD KEEPS 12 CUTS AND COUNTS EVERY REASON -- 2026-10-06. A cut beyond the
        # twelfth only ever contributed its reason, so only the reason is taken for it;
        # building its name for a dict that `cuts[:12]` then dropped was ~97% of late names.
        cut_n: collections.Counter = collections.Counter()
        best: tuple[float, float, float, Term] | None = None
        stats: dict = {"seen": 0, "budget_spent": False, "depth_exhausted": True,
                       "units": self.gamma.alphabet, "estimate": 0}
        by_kind: dict[str, tuple] = {}
        wanted: tuple[float, Term, int] | None = None
        rank = 0
        _share: dict = {}        # D2: per-stream rank/pays/turns, recorded under the arm
        _skey = _hit = None
        priced, _skipped = {}, 0

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
            _no_ev: set = set()                  # item 2b: the lags pass 2 walks
            if _WINDOW and slot in self._window_info:
                _evn = {f"{slot}~{r['j']}" for r in self._window_info[slot]["evidence"]}
                _no_ev = {b for b in operand_binds if b and lag_of(b) and b not in _evn}
            # B2b TWO ROUNDS (the reviewer 2026-10-11 10:57 CDT): derivation order across the
            # whole chain x bind enumeration, where the budget is charged. A DERIVED bind (a pair
            # relation, or a lag of one) is walked in a LAST round over the chains round 1
            # recorded, only with budget left -- an order, never a cut. THE ORDER OF THE
            # DEFERRALS, FIXED: round 1 ordinary binds and evidence lags; round 2 no-evidence lags
            # (item 2b, under the window); round 3 derived binds. A lag is a slot's own earlier
            # reading, a derived bind restates its sources (Fig 13), so the lag goes first.
            _dv = getattr(self.env, "derived", None)
            _dv = set(_dv()) if _dv is not None and _RELATION_SET else set()
            _derb = {b for b in operand_binds
                     if b and (b in _dv or (lag_of(b) or ("",))[0] in _dv)}
            _rounds = ((1,) + ((2,) if _WINDOW and _TWO_PASS else ())
                       + ((3,) if _derb else ()))

            def _round_of(b, _n=_no_ev, _d=_derb):
                return 3 if b in _d else 2 if b in _n else 1

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

            # The shape decoder enters by its SIZE: it is append-only (one writer, id = size,
            # `ArcWorld.shapes` asserts it), so within a run equal size is equal contents. A shape
            # slot's alphabet is max(2, size), so this part adds only the 1 -> 2 step it masks.
            # THE SCOPE KEY: what a chain's PRICE is read from. An unchanged base under the same
            # held term, alphabet and epoch means no new residual row, so `robs` is the same rows;
            # the rest fixes what is generated from them. The cue and the unit ORDER are not in it:
            # they decide when a chain is reached, never what it costs. The SLOT SET is not a
            # separate part: the alphabet map's keys are the slot set, on every world.
            _skey = (held.name, tuple(sorted(self.alphabet.items())), self._trace_epoch, base,
                     tuple(sorted(self.gamma.library)), tuple(sorted(u.name for u in _units)),
                     tuple(streams),
                     json.dumps(gap, sort_keys=True, default=str),
                     len(self._shapes_now() or ()) if _SHAPE_DECODE else 0,
                     self._guard_scope(slot, robs, operand_binds))
            _hit = self._frontier_lookup(slot, _skey) if _RESUME else None
            priced: dict = dict(_hit[1]) if _hit else {}
            _skipped = 0
            if _hit:
                # THE SKIPPED CHAINS' SIDE EFFECT IS REPLAYED: re-pricing them would count these
                # wants again, and the lean reads the count.
                for _ws in _hit[1].values():
                    for _w in _ws:
                        self._want_seen[_w] = self._want_seen.get(_w, 0) + 1
                guards["novelty"] = guards["novelty"] or _hit[2]

            # ITEM 2b: under the window, round 1 walks EVERY stream's chains (non-lag bindings and
            # evidence lags), and round 2, only with budget left, walks the chains round 1 recorded
            # with their no-evidence lags. One round otherwise, so OFF is the old loop exactly.
            _rec2: dict = {}

            def _stream_open(_si, _round):
                in_t, out_t = streams[_si]
                # A THIRD KIND EXISTS ONCE THE STREAMS WIDEN, and it is named rather than
                # folded into `objective`: a term ending at EXTENT is neither a prediction of
                # the slot's next value nor a complete objective, and calling it one would put
                # two quantities under one label at the site the contest is decided.
                kind = _kind_of(out_t)
                by_fit = partial(retrieval.fits, gap=gap, in_type=in_t, out_type=out_t)
                # THE INHERITED VOCABULARY ORDERS THE TIES, AND THE TIES ARE WHERE THE
                # ORDERING ACTUALLY HAPPENS. `fits` returns an INTEGER 0..5 and its own
                # docstring records it collapsing onto arity at 87.3%, so most candidates
                # arrive equal and are broken by registry order -- which `enumerate_closure`
                # calls *an accident*. `term_affinity` is bounded strictly below 1, so it can
                # only separate candidates `fits` scored the SAME; it never reorders across
                # fit levels and never excludes, because the closure admits everything it
                # enumerates. The cue is the agent's own perception, so this is the library
                # being reached BY WHAT IT SAW rather than by a name it cannot read.
                _want = self._cue_tags()
                if _want:
                    if _round == 1:                  # counted once per stream, not per round
                        _book_add(self.gamma.book, "mint_order_by_cue", 1)

                    def by_fit(u, _f=by_fit, _w=_want):        # noqa: F811
                        return _f(u) + inherited.term_affinity(u, _w)
                st: dict = {"seen": 0, "budget_spent": False, "depth_exhausted": True,
                            "units": self.gamma.alphabet, "estimate": 0}
                _lf = (self._library_chains(slot, in_t, out_t, _lf_stats, _lf_ops, _lf_ev)
                       if _LIBRARY_FIRST and _round == 1 else [])
                _lf_names = {c.name for c in _lf}
                _lf_seen.update(tuple(a.name for a in c.atoms) for c in _lf)
                _clo = (c for c in self.gamma.enumerate_closure(
                            in_t, out_t, self.cfg.max_depth, self.cfg.budget, st, order=by_fit)
                        if c.name not in _lf_names)
                _stream = (_merge_by_depth(_lf, _clo, _lf_ev, f"{self.cycle}:{slot}:library:{_si}",
                                           self.draw_seed)
                           if _A1_LIBRARY else itertools.chain(_lf, _clo))
                if _round > 1:
                    _walk_these = ((c, _round) for c in _rec2.get(_si, ()))
                elif len(_rounds) > 1:
                    _walk_these = ((c, 1) for c in _recording(_stream, _rec2.setdefault(_si, [])))
                else:
                    _walk_these = ((c, 1) for c in _stream)
                return kind, st, _walk_these

            # D2: ONE scheduler per round; the body below runs once per candidate with the picked
            # stream's kind/st/_si bound. OFF picks the first live stream: the old order.
            # "pays_called" counts pays() CALLS while the stream holds the turn, trees included.
            _share.update({k: {"rank": 0, "pays_called": 0, "turns": 0, "first_rank": None,
                               "floor_stop": None} for k in range(len(streams))})
            _floored: set = set()

            def _stop(_s, _open, _live):
                _live.remove(_s)
                _st = _open[_s][1]
                stats["seen"] += _st["seen"]
                stats["estimate"] += _st["estimate"]
                stats["budget_spent"] = stats["budget_spent"] or _st["budget_spent"]

            for _round in _rounds:
                _open: dict = {}
                _live = [k for k in range(len(streams)) if k not in _floored]
                _spent = dict.fromkeys(_live, 0)
                _cur, _r0 = None, rank
                while True:
                    if _cur is not None:
                        _spent[_cur] += rank - _r0
                        _share[_cur]["rank"] += rank - _r0
                        _cur = None
                    if not _live:
                        break
                    _ns_calls += 1
                    _si = _next_stream(_live, _spent, _STREAM_SHARE,
                                       f"{self.cycle}:{slot}:stream_share" if _A1_STREAM else None,
                                       self.draw_seed)
                    if _si not in _open:
                        _open[_si] = _stream_open(_si, _round)
                    kind, st, _walker = _open[_si]
                    _nx = next(_walker, None)
                    if _nx is None:
                        _stop(_si, _open, _live)
                        continue
                    cand, _pass = _nx
                    _cur, _r0 = _si, rank
                    _sh = _share[_si]
                    _sh["turns"] += 1
                    if _sh["first_rank"] is None:
                        _sh["first_rank"] = rank
                    # A deferred round's frontier key carries the round (the reviewer 11:34 CDT):
                    # a chain priced in round 1 has not had its deferred binds walked, so a resume
                    # must not skip them as priced.
                    _pk = (_si, cand.name, _pass) if _pass > 1 else (_si, cand.name)
                    if _hit and _pk in _hit[1]:
                        _skipped += 1
                        continue
                    if rank >= self.cfg.work_budget:
                        st["budget_spent"] = True
                        _stop(_si, _open, _live)
                        continue
                    if _lf_ev.get(cand.name, 0) > 0:
                        _lf_reached.append(rank)
                    binds = operand_binds if cand.reads_operand else [None]
                    if len(_rounds) > 1:
                        # PASS 1 walks what the window-OFF search walks plus the evidence lags;
                        # PASS 2 only the no-evidence lags, PASS 3 only the derived binds, so
                        # nothing is charged twice.
                        binds = [x for x in binds if _round_of(x) == _pass]
                        if _pass > 1 and not binds:
                            continue
                        _pass2_chains += _pass == 2
                        _derived_chains += _pass == 3
                    if _pass > 1:
                        _chain_incs = priced.setdefault(_pk, [])
                    else:
                        _chain_incs: list[str] = []
                        priced[(_si, cand.name)] = _chain_incs
                    binds = [x for x in binds if self._operand_fits(cand, slot, x)]
                    _lf_first = [x for x in _lf_ops.get(cand.name, ()) if x in binds]
                    if _lf_first and _A1_LOOKUP and slot in self._bind_key:
                        # A1 site 7: the same key as site 8, with THIS chain's library offers as
                        # the evidence; slots outside the key (None, window lags) keep their place
                        _dk, _cp = self._bind_key[slot]
                        _dk = f"{_dk}:{cand.name}"
                        _of = frozenset(_lf_first)
                        _in = _lookup_order([x for x in binds if x in _cp], _cp, _dk,
                                            evidence=lambda x, _o=_of: int(x in _o),
                                            seed=self.draw_seed)
                        _it = iter(_in)
                        binds = [next(_it) if x in _cp else x for x in binds]
                    elif _lf_first:                              # the offered operands first
                        binds = _lf_first + [x for x in binds if x not in _lf_first]
                    # HOISTED so the guard PRICE can read how many were on offer -- the
                    # denominator `log2(G+1)` is over, and it must be the same set the loop
                    # walks or the price is charged against a population that was not offered.
                    _cand_refs = self._guard_refs(slot, operand_binds)
                    _gs = self._guards(robs, slot, _cand_refs)
                    if _GUARD_PRICE:
                        self._offered_now = len(_gs) - 1
                    # **THE REFERENT IS PAIRED WITH THE GUARD, NOT WITH THE BIND.** Hoisted
                    # with `_gs` for the reason the hoist exists: the price denominator must
                    # be the set the loop actually walks. An ACTED guard now carries ITS OWN
                    # pointer, so `inc` -- which reads no operand and is the true rule on a
                    # wired slot -- can finally be guarded on the object that causes it.
                    # **FROM `operand_binds`, NOT `binds` -- and the difference IS the
                    # defect this change exists to fix.** `binds` is `[None]` for an atom
                    # that reads no operand, so enumerating from it collapses the referent
                    # set back to the slot's own owner and reproduces `ACTED_SELF` exactly.
                    # Measured when I got this wrong: `inc` guarded 23 times, pointed at its
                    # own button ZERO times. The referent must come from what the WORLD
                    # offers, not from what this candidate's computation happens to take.
                    # ONLY THE REFERENTS THAT SEPARATE are walked -- and so priced, because the
                    # price denominator is the set the loop walks (the hoist's own rule).
                    _refs = ([r for r in _cand_refs if self._separates(robs, slot, r)]
                             if any(x in (ACTED_SELF, ACTED_ON) for x in _gs) else [])
                    _pairs = [(g, r) for g in _gs
                              for r in (_refs if g in (ACTED_SELF, ACTED_ON) else [None])]
                    # PRICED ONCE PER (CHAIN, GUARD), NOT PER CANDIDATE -- 2026-10-06.
                    # `gamma.length` reads only a term's atoms and operand tree, so every
                    # binding of this chain costs the same, and every tree under it too
                    # (each branch is one atom). Same expression, evaluated once per key.
                    _price: dict = {}
                    _maybe_lib = not _sep_free or cand.name in self._held_chains
                    # A CHAIN WHOSE CHEAPEST INSTANCE CANNOT PAY IS NOT EXPANDED (item 2, F484).
                    # Within a chain cost varies only with the guard (length is keyed by the atom
                    # sequence), and a tree never costs less than its chain (F483), so if the
                    # cheapest instance's cost reaches `base`, every instance and every tree is
                    # refused on cost alone. Exact: `rank` (the work budget) still counts them and
                    # `novelty` is still read; only the cut bookkeeping differs, as its own reason.
                    _n = len(binds) * len(_pairs)
                    if _n and robs and (term_bits(self.gamma.length(Term(cand.atoms), _units),
                                         self.gamma.alphabet)
                               + min(_guard_bits(g, len(_gs) - 1, len(_refs)) for g in _gs)
                               >= base):
                        if not guards["novelty"]:
                            for bind, (g, gref) in ((b, p) for b in binds for p in _pairs):
                                t = Term(cand.atoms, operand=bind, guard=g, guard_ref=gref)
                                if not (self.gamma.is_atom(t) or (
                                        _maybe_lib and t.name in self.gamma.library)):
                                    guards["novelty"] = True
                                    break
                        rank += _n
                        cut_n["chain bounded out on cost: instances not generated"] += _n
                        if _WINDOW:
                            _win_reached.update(b for b in binds if lag_of(b))
                        continue
                    for bind, (g, gref) in ((b, p) for b in binds for p in _pairs):
                        if _WINDOW:
                            # THE BUDGET CHECKED INSIDE THE CHAIN (the reviewer 18:15Z), so the
                            # cut can fall between two lags and the low-ranked ones go first.
                            if rank >= self.cfg.work_budget:
                                st["budget_spent"] = True
                                break
                            if bind and "~" in bind and lag_of(bind):
                                _win_reached.add(bind)
                        rank += 1
                        if _7H_TRIED and bind is not None:
                            self._tried[(self.level, slot, bind)] += 1
                        term = Term(cand.atoms, operand=bind, guard=g, guard_ref=gref)
                        if self.gamma.is_atom(term) or (_maybe_lib
                                                        and term.name in self.gamma.library):
                            cut_n["not-novel"] += 1
                            if len(cuts) < 12:
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
                            cut_n["recipe-held"] += 1
                            if len(cuts) < 12:
                                cuts.append({"name": term.name, "rank": rank, "reversible": True,
                                             "reason": "recipe-held", "recipe": cand.name,
                                             # HERE, decided: the row is about minting on THIS
                                             # slot, so the reading that belongs in it is whether
                                             # the recipe settled HERE.
                                             "recipe_settled": self.gamma.is_settled(
                                                 cand.name, slot)})
                            if _RECIPE_DEDUP:
                                continue
                        guards["novelty"] = True
                        # PRICED IN UNITS, so a settled sub-composition costs what the
                        # ground already paid for it. `routine.length`'s rule, applied to
                        # the space it was always stated over.
                        cost = _price.get(g)
                        if cost is None:
                            cost = _price[g] = (term_bits(self.gamma.length(term, _units),
                                                          self.gamma.alphabet)
                                                + _guard_bits(g, len(_gs) - 1, len(_refs)))
                        # LET THE RESIDUAL SAY WHERE TO LOOK. Walking the whole history for
                        # every candidate is exhaustive search; R already names the
                        # observations that need fixing, and a term that cannot fix enough of
                        # them is refused without the walk. 6.7x less work over the panel and
                        # nothing lost, because the bound is necessary rather than plausible.
                        if self._cannot_pay(term, slot, robs, cost, base, rkey):
                            cut_n["bounded-out: cannot pay on R alone"] += 1
                            if len(cuts) < 12:
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
                            for bt in self._trees(cand, bind, g, slot):
                                if self.gamma.is_atom(bt) or (
                                        _maybe_lib and bt.name in self.gamma.library):
                                    continue
                                # THE GUARD PRICE APPLIES HERE TOO. `_trees` carries `g`
                                # onto the tree, so pricing it only in the main loop gave
                                # ONE TERM TWO PRICES depending on which path reached it.
                                bcost = _price.get((g, True))
                                if bcost is None:
                                    bcost = _price[(g, True)] = (
                                        term_bits(self.gamma.length(bt, _units),
                                                  self.gamma.alphabet)
                                        + _guard_bits(g, len(_gs) - 1, len(_refs)))
                                if self._cannot_pay(bt, slot, robs, bcost, base, rkey):
                                    continue
                                bleft = self._left(bt, slot, hist, base, bcost)
                                _sh["pays_called"] += 1
                                if not pays(bcost, bleft, base):
                                    continue
                                btotal = bcost + bleft
                                # THE TREE ARM WINS THE BARGAIN TOO AND RECORDED NEITHER.
                                # WHY THE FLAG IS TRUE HERE, AND NOT MERELY CONVENIENT: it is a
                                # PER-CALL SEARCH FLAG -- *this call reached something that pays*
                                # -- not a property of the winner. The third win-site raises it
                                # on exactly this event, immediately after `pays` and the same
                                # counter. These two sites ARE that event and recorded neither,
                                # so a mint arriving here wrote `reachability: False` and B4 read
                                # it. Not evidenced by B4 going quiet -- B4 READS this flag, so
                                # that test is circular (reviewer, 2026-09-27).
                                # AND `rebind-as-mint` IS CLOSED HERE, NOT OPEN -- it was asked
                                # on the premise that these were REBIND arms, and they are tree
                                # arms. Checked: `_rebindings` has ONE caller, `_library_fit`,
                                # which writes only ROUTE rows; and all three mint sites skip a
                                # term already in the library. So no path mints a rebind, and
                                # the kernel's BROKEN_REBINDING routing is not contradicted.
                                self.gamma.book["bargain_paid"] = (
                                    self.gamma.book.get("bargain_paid", 0) + 1)
                                guards["reachability"] = True
                                if kind not in by_kind or btotal < by_kind[kind][0]:
                                    by_kind[kind] = (btotal, bleft, bcost, bt)
                                if best is None or btotal < best[0]:
                                    best = (btotal, bleft, bcost, bt)
                                    _best_rank = rank
                            continue
                        left = self._left(term, slot, hist, base, cost)
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
                        for bt in self._trees(cand, bind, g, slot):
                            if self.gamma.is_atom(bt) or (
                                    _maybe_lib and bt.name in self.gamma.library):
                                continue
                            bcost = _price.get((g, True))
                            if bcost is None:
                                bcost = _price[(g, True)] = (
                                    term_bits(self.gamma.length(bt, _units),
                                              self.gamma.alphabet)
                                    + _guard_bits(g, len(_gs) - 1, len(_refs)))
                            # **THE SAME BOUND HERE, AND IT CHANGES NO OUTCOME.** `_cannot_pay`
                            # PROVES `cost + left >= base`, which is exactly `not pays` -- so
                            # anything it refuses, `pays` refuses too. A short-circuit, not a
                            # new filter, which is what makes this repair byte-identical where
                            # the bound was already correct.
                            if self._cannot_pay(bt, slot, robs, bcost, base, rkey):
                                continue
                            bleft = self._left(bt, slot, hist, base, bcost)
                            _sh["pays_called"] += 1
                            if not pays(bcost, bleft, base):
                                continue
                            btotal = bcost + bleft
                            # THE TREE ARM WINS THE BARGAIN TOO AND RECORDED NEITHER.
                            # WHY THE FLAG IS TRUE HERE, AND NOT MERELY CONVENIENT: it is a
                            # PER-CALL SEARCH FLAG -- *this call reached something that pays*
                            # -- not a property of the winner. The third win-site raises it
                            # on exactly this event, immediately after `pays` and the same
                            # counter. These two sites ARE that event and recorded neither,
                            # so a mint arriving here wrote `reachability: False` and B4 read
                            # it. Not evidenced by B4 going quiet -- B4 READS this flag, so
                            # that test is circular (reviewer, 2026-09-27).
                            # AND `rebind-as-mint` IS CLOSED HERE, NOT OPEN -- it was asked
                            # on the premise that these were REBIND arms, and they are tree
                            # arms. Checked: `_rebindings` has ONE caller, `_library_fit`,
                            # which writes only ROUTE rows; and all three mint sites skip a
                            # term already in the library. So no path mints a rebind, and
                            # the kernel's BROKEN_REBINDING routing is not contradicted.
                            self.gamma.book["bargain_paid"] = (
                                self.gamma.book.get("bargain_paid", 0) + 1)
                            guards["reachability"] = True
                            if kind not in by_kind or btotal < by_kind[kind][0]:
                                by_kind[kind] = (btotal, bleft, bcost, bt)
                            if best is None or btotal < best[0]:
                                best = (btotal, bleft, bcost, bt)
                                _best_rank = rank
                        _sh["pays_called"] += 1
                        if not pays(cost, left, base):
                            cut_n["does-not-pay"] += 1
                            if len(cuts) < 12:
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
                            # tie-break for retention, never a verdict.
                            #
                            # **AND THE THING THAT WOULD MAKE IT A VERDICT IS NOT BUILT.
                            # STANDING WOULD COME FROM RECURRENCE UNDER A RESEMBLING SHAPE,
                            # AND THIS COMMENT NAMED `_note_want` AS THOUGH IT EXISTED --
                            # WRITTEN 2026-09-25, CORRECTED THE SAME DAY.** `resembling`
                            # (3079) is real; `_note_want` has zero definitions and zero
                            # callers. **A comment citing a mechanism by name is the same
                            # false record as a map entry doing it** -- it reads as
                            # DERIVED, and the standing question is *is it actually
                            # reached*, which cannot be asked of something that was never
                            # written.
                            if kind == "objective":
                                # RECURRENCE FIRST, COST AS THE TIE-BREAK. Ranking by cost
                                # alone is *the cheapest way to say this want*, which is a
                                # property of the SENTENCE; standing is a property of the
                                # WANT, and Isaiah's criterion is that it keeps coming back.
                                _n = self._want_seen.get(term.name, 0) + 1
                                self._want_seen[term.name] = _n
                                _chain_incs.append(term.name)
                                if wanted is None or (_n, -cost) > (wanted[2], -wanted[0]):
                                    wanted = (cost, term, _n)
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
                            _best_rank = rank
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
                    # UNDER THE ARM THE FLOOR IS PER KIND (the reviewer 06:19 CDT): a want comes
                    # from by_kind["objective"] or `wanted`, never from the winner, so
                    # another kind's champion at the floor is no bound on this stream.
                    # OFF keeps the shared best (a FINDING: the same starvation, rare).
                    _fc = _floor_champion(by_kind, kind, best, _STREAM_SHARE)
                    if _fc is not None and _fc[0] <= term_bits(1, self.gamma.alphabet):
                        if _STREAM_SHARE:
                            _sh["floor_stop"] = _round
                            _floored.add(_si)
                        _stop(_si, _open, _live)
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
        # **`candidates_tried` IS `rank`: CHAIN CANDIDATES ONLY.** Operand-TREE candidates are
        # priced without entering `rank` -- 86.8% of all pricing on default (2026-10-05) -- so
        # it is not the mint's work. `candidates_priced` is: every `_cannot_pay` call this mint.
        detail = {**({"part": self._mint_part} if self._mint_part else {}),
                  "guards": guards, "candidates_seen": seen, "candidates_tried": rank,
                  "candidates_priced": self._priced - _priced0,
                  "contest": contest,
                  # **`cuts` IS A SAMPLE AND `cut_counts` IS THE POPULATION -- `F413`.**
                  # The twelve are kept for their NAMES and RANKS, which is what a reader
                  # wants when looking at one mint; the counts are what a MEASUREMENT needs.
                  # Taken on seed 5: 360 sampled rows against 663,423 constructions, and a
                  # term read ZERO cut rows on BOTH arms of an A/B -- including the arm
                  # where it WON -- which is how the truncation was found. A zero equal on
                  # both arms is a broken instrument, not a finding.
                  "code": CODE, "base_bits": round(base, 3), "cuts": cuts,
                  "cut_counts": dict(cut_n),
                  "budget_exhausted": bool(stats["budget_spent"]),
                  "depth": self.cfg.max_depth, "units": stats["units"],
                  "space_estimate": est,
                  "coverage": round(seen / est, 6) if est else 0.0}
        if _STREAM_SHARE and _share:
            detail["stream_share"] = {
                **{_kind_of(streams[k][1]): v for k, v in _share.items()},
                "unasked": [_kind_of(streams[k][1]) for k, v in _share.items()
                            if v["first_rank"] is None]}
        if _hit:
            detail["chains_already_priced"] = _skipped
        if unseal is not None:
            detail["unseal"] = unseal
        if _derb:
            detail["derived_round"] = {"binds": len(_derb), "chains": _derived_chains}
        _win = self._window_info.pop(slot, None)
        if _win is not None:
            # WHAT THE WINDOW OFFERED AND WHAT THE BUDGET REACHED, by kind (Fig 13: counted).
            _ev = {f"{slot}~{r['j']}" for r in _win["evidence"]}
            _lags = [b for b in operand_binds if b and lag_of(b)]
            _out = [b for b in _lags if b not in _win_reached]
            _win.update(reached=len(_win_reached), chains_reached=len(priced),
                        pass2_chains=_pass2_chains,
                        beyond_bound={"evidence": sum(b in _ev for b in _out),
                                      "no_evidence": sum(b not in _ev for b in _out)})
            detail["window"] = _win
        if guards["support"] and base > floor:
            # A1 GROUP 2's STREAM ROWS (the reviewer 2026-10-15 09:19, 14:23): one per (cycle, slot,
            # site), what the walk did and never the walk -- where the winner sat, how far it went
            # and why it stopped. No k: nothing is cut to a constant. The library row is written
            # with the arm OFF too, so the checklist can read ON against OFF.
            # Written under MINT, the step they happen in (labelled PLAN from fbe9f41 to this
            # fix, failing the gate's step-order check on every ALL-ON ledger; the reviewer
            # 2026-10-16).
            _won = best[3] if best is not None else None
            _stop_why = {"found": int(_won is not None),
                         "budget": int(bool(stats["budget_spent"])),
                         "exhausted": int(_won is None and not stats["budget_spent"])}
            if _LIBRARY_FIRST:
                self.led.record(
                    self.cycle, "MINT", slot, "stream", site="library_merge", arm=_A1_LIBRARY,
                    key=("depth; library evidence within a depth; the closure's by_fit; library "
                         "ties by the draw") if _A1_LIBRARY else "library chains first",
                    calls=1, walked_total=rank, walked_max=rank,
                    winner=_won.name if _won is not None else None, winner_rank=_best_rank,
                    stop=_stop_why, work_budget=self.cfg.work_budget,
                    evidence_offered=sum(1 for v in _lf_ev.values() if v > 0),
                    evidence_reached=len(_lf_reached), evidence_ranks=list(_lf_reached))
            if _A1_LOOKUP and slot in self._bind_key:
                _wop = _won.operand if _won is not None else None
                self.led.record(
                    self.cycle, "MINT", slot, "stream", site="lookup_order",
                    key=("contact gate; derived (actions); library evidence (bits); distinct "
                         "values over the residual; the draw"),
                    calls=1, walked_total=len(operand_binds), walked_max=len(operand_binds),
                    winner=None if _won is None else repr(_wop),
                    winner_rank=(operand_binds.index(_wop) if _won is not None
                                 and _wop in operand_binds else None),
                    stop=_stop_why, work_budget=self.cfg.work_budget)
            if _A1_STREAM and _STREAM_SHARE and _share:
                _wk = next((k for k, v in by_kind.items() if _won is not None and v[3] is _won),
                           None)
                self.led.record(
                    self.cycle, "MINT", slot, "stream", site="stream_share",
                    key="least rank spent this round; exact ties by the draw",
                    calls=_ns_calls, walked_total=sum(v["turns"] for v in _share.values()),
                    walked_max=max(v["turns"] for v in _share.values()),
                    winner=_wk, winner_rank=_best_rank, stop=_stop_why,
                    work_budget=self.cfg.work_budget)

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
                # RENAMED FROM `depth_exhausted` -- the reviewer, 2026-10-01, because the
                # old word named the one thing that was NOT the cause and cost an hour.
                # `F406`: coverage 1.0, budget_exhausted False, 3303 candidates priced and
                # none paid -- the space was fully searched and every term was too DEAR,
                # not out of reach. And raising `max_depth` is arithmetically guaranteed
                # to fail: `term_bits` is monotone in k, so a deeper term is a dearer one.
                detail["verdict"] = "priced_out_at_depth"
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
                                        "priced": self._priced - _priced0,
                                        "coverage": detail["coverage"],
                                        "verdict": detail["verdict"],
                                        "units_then": stats.get("units", 0),
                                        "base_bits": round(base, 3)}
            if _skey is not None and detail["verdict"] in ("budget_spent", "priced_out_at_depth",
                                                           "not_novel"):
                detail["chains_priced_in_scope"] = len(priced)
                self._frontier_store(slot, (_skey, {k: tuple(v) for k, v in priced.items()},
                                            guards["novelty"], detail["verdict"]))
            if _LIBRARY_FIRST:
                detail["library_first"] = dict(_lf_stats)
            if _PARK_WANT and wanted is not None and detail["verdict"] in (
                    "budget_spent", "not_novel", "priced_out_at_depth"):
                # written BEFORE the row, so the row carries it. A term still bound from an earlier
                # mint may mask it: under TETHER_WANT_TARGET only an OBJ-typed one (_objective_of);
                # otherwise any, for the mint's own wants (_target_lookup's bound-or-want).
                # bound_at_park says one is bound
                detail["bound_at_park"] = slot in self.bound
                self._retain_unpaid_want(slot, wanted, detail)
            self.led.record(self.cycle, "MINT", slot, "park", of=(slot,), **detail)
            if _D13:
                self._park_bet(slot, detail)
            if _M6_INVENT:
                self._invent(slot, hist, base, base_held, detail["verdict"])
            return

        self._frontiers.pop(slot, None)
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
            self._want_terms[slot] = _obj[3]
            detail["want"] = _obj[3].name
        elif wanted is not None:
            # THE RULING'S PATH, and the only one that has ever had traffic. A want that lost
            # the contest is still WANTED; what it does not get is the right to ACT.
            self._retain_unpaid_want(slot, wanted, detail)
        _total, left, cost, term = best
        if unseal is not None:
            # per rebinding (the reviewer 16:28Z, 16:31Z): both whole lengths, the start bits
            # inside the held rule's price, and which of the two reads an earlier frame
            unseal.update(winner=term.name, winner_whole=round(cost + left, 3),
                          held_whole=unseal["bar"],
                          start_bits=round(unseal["starts"] * math.log2(self.alphabet[slot]), 3),
                          held_reads_earlier=True,
                          winner_reads_earlier=lag_of(term.operand) is not None)
        if unseal is not None and left > base_held:
            # SHORTER BUT EXPLAINING LESS: `outstanding` only grows, and `explain` cannot unspend,
            # so a replacement may not leave more than the rule it replaces.
            self.gamma.book["unseal_leaves_more"] = self.gamma.book.get("unseal_leaves_more", 0) + 1
            detail["verdict"] = "unseal_leaves_more"
            self.led.record(self.cycle, "MINT", slot, "park", of=(slot,), **detail)
            return
        detail["explained"], detail["overclaimed"] = self.explain(slot, base_held - left)
        self.gamma.accept(term, seq=len(self.led), residual=f"{slot}@{self.cycle}")
        self.bound[slot] = term.name
        self.rank.note(term.name, self.cycle)
        closes = left == 0.0
        if not closes and lag_of(term.operand) is not None:
            _miss = self._residual_obs(slot, term, robs)
            _k = sum(self._no_earlier_frame(term, r[0]) for r in _miss)
            if _k:
                detail["inapplicable"] = {"why": "no earlier frame", "k": _k, "n": len(robs)}
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
        self._cand_level[term.name] = self.level
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
        _lib = self._named.get(slot, {})
        detail["operand_from_lookup"] = _lib.get(term.operand) if term.operand else None
        detail["verdict"] = "pays"
        detail["closes"] = closes
        if not closes:
            detail["note"] = "pays but does not close R; the slot still owes"
        detail.update(term=term.name, term_depth=len(term), operand=term.operand,
                      term_bits=round(cost, 3), left_bits=round(left, 3))
        if _GUARD_PRICE and term.guard is not None:
            _g = getattr(self, "_offered_now", None)
            detail.update(guard=str(term.guard), guards_offered=_g, guard_bits=(
                round(_guard_bits(term.guard, _g or 0), 3)
                if term.guard not in (ACTED_SELF, ACTED_ON) else None))
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
        if _LIBRARY_FIRST:
            detail["library_first"] = dict(_lf_stats)
            prov = next((o_["prov"] for o_ in self._lib_offers.get(slot, ())
                         if o_["operand"] == term.operand
                         and tuple(a.name for a in o_["term"].atoms)
                         == tuple(a.name for a in term.atoms)[:len(o_["term"].atoms)]), None)
            if prov is not None:
                detail["library"] = prov
                _core = _core_kind(self._lib_offers.get(slot, ()), term) if G_SETTLED_CORE else None
                if _core is not None:
                    detail["core"] = (self.gamma.inherit if _core == "inherit"
                                      else self.gamma.learn)(term.name)
            # HOW the library moved this winner (the reviewer 11:00Z): `described` -- chain and
            # operand both offered (the stamp); `chain_only` -- the chain arrived by the library's
            # order with an operand it did not offer; `none` -- not by this mint's offers. A
            # knock-on through another slot's library win is visible only against the OFF arm.
            names = tuple(a.name for a in term.atoms)
            detail["library_route"] = (
                "described" if prov is not None
                else "chain_only" if any(names[:len(ch)] == ch for ch in _lf_seen) else "none")
        self.led.record(self.cycle, "MINT", slot, "mint", of=(slot,), **detail)
        # THE PART RIDES ON THE ACCEPT TOO (the reviewer 2026-10-11 23:03 CDT): a D5 part-B accept
        # names the slot while the slot is restored to its incumbent; untagged, a count of
        # accepts per slot reads it as the slot's own.
        # (c) ACCEPT by design: this row records the ACCEPT this method itself performs, a later
        # step carried out inside MINT (the reviewer 2026-10-16 09:23)
        self.led.record(self.cycle, "ACCEPT", slot, "accept", term=term.name,
                        origin=term.origin, seq=len(self.led),
                        status=detail.get("core", "candidate"),
                        cited="no: candidate may be held, not cited",
                        **({"part": self._mint_part} if self._mint_part else {}))
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
        if self._turn_ahead is not None:
            # a slot of this level already past its turn is not offered the term now (F500);
            # a parked record from an earlier level has no turn here and is still swept
            keep = [t for t in targets if t[1] not in self.slots or t[1] in self._turn_ahead]
            if len(keep) < len(targets):
                self.chain.reuse_branch["deferred:turn-done"] += len(targets) - len(keep)
            targets = keep

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
            # CARRY (item 3): the floor lemma bounds a NEW term's cost, not one already paid, so
            # under the arm an under_floor record is swept too.
            return (rec.get("verdict") not in (("depth_exhausted",) if _CARRY_PRICE
                                               else ("depth_exhausted", "under_floor"))
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
            cost = term_bits(self.gamma.length(cand, self._units_for(slot)),
                             self.gamma.alphabet)
            # CARRY (item 3): the swept term was minted and paid its cost at its own entry, so
            # where it re-grounds on this record alone (left < base) it pays on its leftover.
            cred = (_CARRY_PRICE and left < base and (self.gamma.stamps.get(term.name) or {})
                    .get("origin") == MINTED)
            h_, ref_ = self._carry_ref() if cred else (0, 0.0)
            # an under_floor record is open to a CREDITED term only (the reviewer 21:37Z)
            floor_only = (_CARRY_PRICE and rec.get("verdict") == "under_floor"
                          and units_now <= rec.get("units_then", 0))
            if pays(ref_ if cred else cost, left, base) and (cred or not floor_only):
                self.explain(slot, base - left)
                if cred:
                    self.gamma.book["carry_sweep_credited"] = (
                        self.gamma.book.get("carry_sweep_credited", 0) + 1)
                # THE SWEEP IS A PULL AND EMITTED NO PULL ROW. `reused()` counts `pull` rows
                # and this is the only path that RE-BINDS, so every reuse it found was
                # invisible to the bench-pull and transfer columns both.
                self.led.record(self.cycle, self._running_step, slot, "pull", term=cand.name,
                                held=tkey, chain=" . ".join(a.name for a in cand.atoms),
                                rebound=True, via="sweep",
                                **({"carry_credited": cred, "held_terms": h_,
                                    "ref_bits": round(ref_, 4)} if _CARRY_PRICE else {}),
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
                    self._carry(name)
                    self.owed_import.discard(slot)
                    self.abstained.pop(slot, None)
                out = {"term": name, "slot": slot, "cycle": self.cycle,
                       "was": rec.get("verdict"), "via": how,
                       "cross_level": cross, "parked_on": rec.get("level")}
                # MF-D3 (R-D2): a pre-boundary record closed here is STALE -- evidence, not a
                # settle in this level, so its promotion waits for the term to settle here.
                stale = _CARRY_PRICE and cross
                if stale:
                    out["stale"] = True
                    self.gamma.book["carry_stale_close"] = (
                        self.gamma.book.get("carry_stale_close", 0) + 1)
                elif cred:
                    self._carry_log[(name, slot)] = {
                        "term": name, "slot": slot, "level": self.level, "cycle": self.cycle,
                        "frames": len(hist), "left": round(left, 4), "base": round(base, 4),
                        "carried": False, "via": "sweep", "settled": 0, "demoted": 0}
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
                        "cross_level": cross, "via": how,
                        **({"stale": True} if stale else {})}))
                # charged to the ORIGIN's chain, not the target's: the sweep is not the
                # target slot's per-step loop running a second time, it is part of what
                # happened when the origin minted. The target is named, not impersonated.
                # (c) ACCEPT by design: this row records the ACCEPT this method itself performs, a
                # later step carried out inside MINT (the reviewer 2026-10-16 09:23)
                self.led.record(self.cycle, "ACCEPT", origin_slot, "retro", term=name,
                                verdict="retroactive resolution", target=tkey,
                                guards={"support": True, "reachability": True,
                                        "novelty": False},
                                note="minted here; it explains a residual parked elsewhere",
                                was=out["was"], via=how, cross_level=cross,
                                **({"stale": True} if stale else {}))
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
                why = ("under-floor-uncredited" if floor_only and pays(cost, left, base)
                       else "did-not-pay" if left < base else "no-split")
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
        cost = term_bits(self.gamma.length(cand, self._units_for(slot)),
                         self.gamma.alphabet)
        left = self._left(cand, slot, hist)
        # `ROUTE`, NOT `ACCEPT`, AND THE GATE SAID SO. The sweep runs inside the ROUTE phase
        # and its own `pull` row is a ROUTE row, so an `ACCEPT` here puts a later ROUTE for the
        # same slot out of order -- `chase: ROUTE after ACCEPT`, refused at seq 39. **The step
        # is a fact about WHEN the row is written, not about what the event feels like.**
        self.led.record(self.cycle, self._running_step, slot, "reuse_install", term=cand.name,
                        cost=round(cost, 4), left=round(left, 4),
                        base=None if base is None else round(base, 4),
                        would_pay=None if base is None else pays(cost, left, base),
                        partial=partial,
                        note="F32: entered on the ONE bargain (cost+left<base); "
                             + ("partial -- a remainder remains" if partial else "full closure"))
        stamp = "partial" if partial else "closed"
        self.gamma.accept(cand, seq=len(self.led), residual=f"reuse:{slot}@{self.cycle}:{stamp}")
        # A CANDIDATE, AS A MINTED TERM IS (the mint's own route, ~"self.candidates[term.name]").
        # Without it `settle` skips the term: it could never settle, never be demoted, and stayed
        # bound and wrong in silence while the sweep promoted it (gridworld_arc_s0, 2026-10-09).
        if _REUSE_CANDIDATE:
            self.candidates.setdefault(cand.name, self.cycle)
            self._cand_level[cand.name] = self.level
        return cand.name

    @_in_step("SETTLE")
    def settle(self, res: dict[str, SlotResidual]) -> None:
        """The ground settles it, by held-out payment: a term predicts a transition it was
        never fitted to. And it un-settles the same way -- a settled term that mispredicts
        on fresh evidence is DEMOTED, defeasibly, never deleted."""
        for slot, r in res.items():
            # **THE MAKER, NOT THE HOLDER.** `self.bound` is read AFTER `route` has
            # rebound this step, so it answers *who holds the slot now* -- a different
            # question from *who made the prediction being judged*. Falling back to the
            # holder would reintroduce the defect wherever the maker is missing, so a
            # slot with no recorded maker is SKIPPED: an unattributed prediction is not
            # evidence against anybody.
            name = self._pred_by.get(slot)
            if r.gone:
                # a departure is not evidence against the term that predicted the slot's value
                self._shadow.pop(slot, None)
                self._d5_candidates.pop(slot, None)
                if name:
                    self.led.record(self.cycle, "SETTLE", slot, "not_judged", term=name,
                                    reason="left the board")
                continue
            if _D5 and slot in self._shadow:
                # THE CUT STAYS FALSIFIABLE (the reviewer 15:58Z): the incumbent's shadow on a
                # not-P step. Right there means the partition claim is broken; the split reverts.
                sh = self._shadow.pop(slot)
                if sh is not None and r.actual is not None and (
                        sh == r.actual % self.alphabet[slot]):
                    self._d5_revert(slot)
                    continue
            if _D5:
                self._d5_rows.setdefault(slot, []).append((len(self.trace) - 1, name))
            if not name:
                continue
            if _D5 and slot in self._d5_candidates:
                self._d5_witness(slot, name, r)
            if r.mass > 0.0:
                # express-before-judge: this term actually predicted, and was wrong
                # AND THE FIFTH BIN IS POPULATED HERE AND NOWHERE ELSE, which is the whole of
                # what makes it expressed-and-failed rather than not-retrieved. Recorded for
                # BOTH outcomes of `refute` below: a settled term demoted and a candidate
                # mispredicting are both the ground refusing what was said.
                self._refuted_slot[slot] = name
                _found = None
                if _D5 and slot not in self._parts and slot not in self._d5_pending and (
                        slot not in self._d5_candidates):
                    _found = self._d5_cut(slot, name)
                held = self.gamma.is_settled(name, slot)
                _demoted_now = self.gamma.refute(name, where=self._scope, slot=slot)
                if _found is not None and not _demoted_now:
                    # A CANDIDATE, NOT A PARTITION (the reviewer 18:46Z, Fig 9 :60): the cut was
                    # read off rows already seen, so it acts only after a row it did not see
                    # witnesses it. Registered only if its incumbent survives this step.
                    self._d5_candidates[slot] = (*_found, name)
                    self.led.record(self.cycle, "SETTLE", "@d5", "cut_candidate",
                                    split_slot=slot, P=_found[0], incumbent=name, **_found[1])
                if _demoted_now:
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
                    self._carry_note(name, slot, "demoted")
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
                    if _D5:
                        if self._d5_pending.pop(slot, None) is not None:
                            self.led.record(self.cycle, "SETTLE", "@d5", "cut_withdrawn",
                                            split_slot=slot, incumbent=name, verdict_on_the_cut=
                                            "confirmed", reason="confirmed, then its incumbent "
                                            "was demoted on the same step: no part A to keep")
                        if slot in self._parts:
                            self._d5_dissolve(slot, name)
                elif held:
                    # A MISS THAT COST NO STANDING: the evidence tally rose and stayed under the
                    # ceiling. Recorded as what it is; the binding stands, because only the
                    # ground REVERSING a settlement licenses an unbind (F462).
                    self.led.record(self.cycle, "SETTLE", slot, "miss_while_settled", term=name,
                                    status="settled", asked=[name, slot], ground_said=False,
                                    verdict="mispredicted; standing held under the ceiling",
                                    rejections=round(self.gamma.rejection_of(name), 3))
                elif name in self.candidates:
                    # A CANDIDATE REFUSED BY THE GROUND (P3; the reviewer 00:15Z): the refutation
                    # reached standing above and was written nowhere, so a term wrong on every
                    # bet read as never graded. Recording only; nothing here binds or unbinds.
                    self.led.record(self.cycle, "SETTLE", slot, "miss_while_candidate", term=name,
                                    status="candidate", asked=[name, slot], ground_said=False,
                                    verdict="mispredicted before it settled",
                                    rejections=round(self.gamma.rejection_of(name), 3))
                continue
            born = self.candidates.get(name)
            # HERE, decided: without the slot this skips settling a candidate on slot B
            # because it settled on slot A -- the MIRROR of the A5 defect, where one
            # settlement anywhere BLOCKS settling everywhere instead of licensing citation.
            if born is None or born >= self.cycle or self.gamma.is_settled(name, slot):
                continue
            # DORMANT UNTIL THE CONDITIONS RECUR -- Isaiah, 2026-09-30. A candidate that
            # crossed a level boundary keeps its birth cycle, so `born >= self.cycle` is
            # false and WITHOUT THIS IT WOULD SETTLE IMMEDIATELY on the new level, against
            # evidence it never saw there. **A missing stamp reads as dormant, never as
            # live**: the conservative direction is the one that cannot manufacture a
            # settlement, and nothing is deleted either way.
            if self._cand_level.get(name) != self.level:
                continue
            self.gamma.settle(name, where=self._scope, slot=slot)
            # NO `self.settled.add` -- the line above IS the record. Adding to a second set
            # here is what made the two disagree: gamma unsettles on refusal and the set
            # never heard.
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
                # **DID INVENTION EVER PAY?** The in-run inventor is REMOVED; an invented atom
                # can still arrive from a CARRIED library (`gamma.py` re-invents on load).
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
            self._carry_note(name, slot, "settled")
            self._settled_lvl.add(name)
            self.led.record(self.cycle, "SETTLE", slot, "settle", term=name,
                            status="accepted",
                            asked=[name, slot], ground_said=True,
                            verdict="held on a transition it was not fitted to",
                            held_out_cycle=self.cycle, fitted_through=born)

    # -- the utterance: the only way an action is proposed --------------------------------

    @_in_step("PERCEIVE")
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
        if _7H_ROOT and self._root_id is None and self._alive:
            self._intent_root()   # 7h: the first step of every live situation
        self._touch_cache = None      # a new step is a new frame, so contact and owners go
        self._peer_cache = None
        self._decomp_cache = None
        self._frame_cache = {}
        if _RELATION_SET:
            # ARC B2 (the reviewer 2026-10-11 11:48 CDT): the agent's own actor set -- the owners
            # of its contingent slots -- steers which pairs its sensors measure. Last step's
            # contingency, so actor pairs lag it by one step. Never reaches the game.
            _rel = getattr(self.env, "relate", None)
            if _rel is not None:
                _own = self._slot_owners(self.env)
                _rel({_own[s] for s in self.agency.contingent() if s in _own})
            if self._goal_links:
                self._respell_goals()
        if _MC6:
            self._step_row0 = len(self.led)
        if _COMPLETION_SWEEP and self._deg_prev is None:
            self._deg_prev = self.env.objective()[1]     # the world's degree before acting
        self._narrate_order()
        self._narrate_cascade()
        if _CASCADE_AGENCY:
            self._cascade_agency()
        self._narrate_matches()
        self._narrate_placements()
        self._narrate_cues()
        self._advertised()
        self._present()       # before the frame, so slots and frame cannot disagree
        # PER STEP, BECAUSE ONE SLOT TYPE'S RANGE IS NOT CONSTANT. A shape slot's alphabet is
        # `2**(h*w)` over its own bounding box, which moves when the object resizes -- and a
        # resize changes slot VALUES, not the slot SET, so the three existing refresh sites
        # never fire. The declaration is still the domain's; only when it is read has moved.
        self.alphabet = self._alphabets(self.env)
        before = self.env.observe()
        if _RUIN_RECORD:
            self._ruin_step, self._ending_counted = None, None
            # ONE reading of this board, before anything is chosen: B's key and C's lookup
            self._step_fp, self._step_before = self._fingerprint(before), before
        if _RUIN:
            _fp = self._step_fp[0]
            self._withheld = IFace.Withheld(
                _fp, frozenset((a, c) for f, a, c in self._vetoes if f == _fp))
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
            with self._step_scope("PERCEIVE"):
                self.led.record(self.cycle, "PERCEIVE", "@loop", "no_slots",
                                slots=0, cause=CHANNEL_CLOSED,
                                blind=getattr(self.env, "blind", None),
                                reads="the slot set is empty; what that MEANS is not read here")
            # NO ACTION WAS TAKEN, SO NOTHING PRECEDED THE NEXT FRAME. `_advertised` runs at
            # the top of every step and reads `_last_action` (Preconditions is fed in
            # `perceive` now, which a dead cycle never reaches); leaving it
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
            with self._step_scope("ROUTE"):
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
        elif self.cue is not None:
            # **SURPRISE DRIVES ATTENTION -- Berlyne 1960, in `ARC_HUMAN_PRIORS` §8's own
            # table, and a prior we are entitled to frontload.** A mutation IS a surprise: the
            # board differing from the frame before it. The capacity limit is the other half
            # and it is the one that makes this necessary rather than convenient -- Cowan's
            # 4+-1 focus of attention means a bounded agent NEEDS something to narrow what it
            # looks at, and until now nothing did on the 99.65% of slot-cycles where
            # `_goal_choice` has no objective to offer (Q12).
            #
            # **A COMPLEMENT, NOT A SECOND SELECTOR, and the difference is the branch it sits
            # in.** The comment above records me wiring a weaker duplicate ranking HERE once
            # already. This is the `elif`: it fires only where the selector returned nothing,
            # so the two can never compete for the same cycle and `_goal_choice` keeps every
            # choice it can make.
            #
            # **ATTENTION, NEVER ACTION -- the boundary, and it is what makes this takeable.**
            # A mutation narrows WHAT THE AGENT LOOKS AT. It does not touch `choose`, which
            # decides what to DO. Looking at the changed thing is a means the agent can still
            # be wrong about; picking the move is the test. `CLAUDE.md`'s question -- does this
            # hand an ANSWER or a MEANS -- puts attention-direction in MEANS.
            #
            # BY ATTRIBUTE CLASS, NOT BY OBJECT INDEX, and that is deliberate. The cue's
            # `loci` are keyed by the OBSERVER's index over `actors(components(board))`, which
            # has no guaranteed correspondence to the world's `o0`/`o1` naming. Reading index
            # 0 as slot `o0` would be the adjacent-reference class exactly: a lookup that
            # SUCCEEDS and returns the wrong neighbour. The attribute classes need no identity.
            _muts = self.cue["mutations"]["attributes"]
            _attr_of = getattr(self.env, "attribute_of", None)
            if _muts and _attr_of is not None:
                _want = {a for m in _muts for a in _CUE_ATTR.get(m, ())}
                _hit = sorted(s for s, a in _attr_of().items()
                              if a in _want and s in before)
                if _hit:
                    # STABLE PICK. `sorted` then first, so the focal slot does not wander
                    # between cycles on an unordered set -- an attention that moves for no
                    # reason is noise wearing a mechanism's clothes.
                    focal = _hit[0]
                    self.gamma.book["focus_by_cue"] = self.gamma.book.get("focus_by_cue", 0) + 1
        by = "given"
        self._intent_now = None
        # PER STEP. A coordinate is a property of THIS cycle's realisation, and leaving it would
        # aim a later positioned action at where something used to be -- the stale-state defect
        # in the shape that looks like a working aim.
        self._aimed = None
        self._last_landed = None
        self._press_seen = None
        if action is None:
            action, by = self.choose(before)
        self._acts[action] += 1   # System-0 instrument: the concrete action distribution
        _prov = getattr(self.env, "provenance", lambda _a: None)(action)
        # S1: a press on a dead board throws nothing away, so it adds nothing to the restart's price
        if _prov == "platform-universal":
            self._attempt_actions = 0
        elif self._alive or not IFace._DEAD_PRICE:
            self._attempt_actions += 1
        if _MC34:
            self._run_actions += 1
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
        # S5: THE FAMILY, NOT THE EXACT STRING. `choose` returned `discriminate`,
        # `discriminate:learned` and `discriminate:goal`, and an `==` admitted only the first
        # -- so a LEARNED split, which §18.4's proposer picks deliberately, was filed under
        # PROBE. Measured across ten boards: `discriminate:learned` fired on six of them, 33
        # of 125 cycles, and `phases.report()` read `directed 0.0` on every one. `draw` stays
        # in PROBE and is not part of this: it and `probe` are byte-identical calls to
        # `drive.choose`, so both really are undirected picks.
        #
        # **AND THE PREFIX BROKE THE MOMENT A LABEL WAS RENAMED -- 2026-09-28.**
        # `discriminate:learned` is now `distinguish`, which does not start with
        # `discriminate`, so the prefix would have filed the system's LARGEST directed exit
        # under PROBE -- **silently, and in the column the fix above exists to make non-zero.**
        # The repair for a string family being a string was a wider string match, and that is
        # the same shape one rename along.
        #
        # **AND MY FIRST REPAIR WAS THE SAME ERROR ONE LEVEL ALONG -- caught by the reviewer,
        # 2026-09-28, in the commit that fixed the prefix.** I wrote
        # `I.PROBE if by in ("probe", "draw") else I.DIRECTED`, reasoning that listing the
        # UNDIRECTED exits is a closed set while the directed ones grow. **`system0` is neither
        # of those two, so it silently flipped PROBE -> DIRECTED** -- 11 of 25 actions on
        # gridworld seed 3, in the same published column I had just finished protecting. A
        # guess about which side is the short list is still a guess.
        #
        # **SO THE SET IS ENUMERATED FROM `choose`'s OWN RETURNS, which is six labels and
        # checkable**: `routine` . `probe` . `draw` . `system0` . `discriminate:goal` .
        # `distinguish`, plus `given` when the caller hands the action in. `system0` STAYS
        # PROBE and its own site says why -- it *draws variously INSTEAD of exploiting the
        # learned arm*, which is an undirected pick made deliberately, not a directed one.
        # **The two failures here were a PATTERN and an EXCLUSION; the fix for both is the
        # enumeration, and it is short because `choose` has few exits, not because I hope so.**
        # **AND AN UNLISTED LABEL IS LOUD, NOT DEFAULTED -- the reviewer, 2026-09-28, so this
        # cannot happen a fourth time.** An enumeration with an `else` is still a silent
        # classifier for the one case that matters: the NEXT exit somebody adds. It would land
        # in a column nobody chose for it, exactly as `distinguish` and `system0` just did.
        # **Same shape as narratability refusing a row with no sentence** -- the new thing has
        # to be classified when it is added, not discovered in a census later.
        #
        # FILED RATHER THAN RAISED: a board run must not die because a phase is unnamed, and
        # `UNCLASSIFIED` is a reading the seats can refuse while the run continues -- which is
        # this project's own *an abstention counts only when it names what it searched*.
        phase = PHASE_OF.get(by)
        if phase is None:
            phase = "unclassified"
            self.led.record(self.cycle, "PLAN", "@loop", "unclassified_by",
                            by=by, known=sorted(PHASE_OF),
                            reason="this exit has no phase; classify it at `PHASE_OF`")
        self.phases.note(phase)

        with self._step_scope("PERCEIVE"):
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
        # **THE COORDINATE RIDES ON THE REALISATION NOW, NOT ON A BUTTON'S NAME -- 19.** This
        # read `if action == "ACTION6"`, which is `step` knowing which button is positioned:
        # the last such test outside the interface. `realise` aims it and sets `_s0_coord`, so
        # a board spelling its positioned action differently needs no change here at all.
        #
        # **AND THE AIM-SELECTION WENT WITH IT, WHICH IS A REAL SIMPLIFICATION AND NOT A LOSS.**
        # This site used to pick the aim itself -- `_s0_target` for `system0`/`probe`, else
        # `focal` -- carrying two earned facts: that `focal` is residual mass and therefore the
        # right subject for a BET and the WRONG one for going to touch something (`F236`), and
        # that ARM M returns `probe` rather than `system0` so keying on `by` alone would aim a
        # starved-slot perturbation at the most-residual slot. **Both are now structural: the
        # exit that WANTS the contact names its own target in the intent, so there is no second
        # site guessing whose aim this was.**
        coord = self._aimed
        if _RUIN and self._withheld and by != "given":
            _w, _c = self._withheld, tuple(coord) if coord is not None else None
            self.led.record(self.cycle, "PLAN", "@ruin", "withheld", fingerprint=_w.fp,
                            withheld=sorted([a, list(c) if c else None] for a, c in _w.pairs),
                            chosen=[action, list(_c) if _c else None],
                            all_vetoed=_w.action(action) or _w.at(action, _c), by=by)
        self._withheld = IFace.NO_WITHHELD
        if _FED and by != "given":
            _fed = ([{**self._split_term, "role": "goal"}]
                    if by == "discriminate:goal" and self._split_term is not None
                    else list(self._routine_fed) if by == "routine" else [])
            # THE ROUTE, WITH ITS SOURCE (the reviewer 15:49Z): which press came from the table and
            # which from a library term, so a zero here is read and not built in (Fig 10 :19).
            _r = self._last_real
            if by in ("discriminate:goal", "routine") and _r is not None:
                _t = getattr(_r, "term", None)
                _fed.append({"kind": "press", "name": _t, "slot": None, "role": "route",
                             "source": "term" if _t else "table", "why": _r.why,
                             "seq": self.gamma.stamps.get(_t, {}).get("seq") if _t else None})
            self._gamma_read = {**self._gamma_read, "fed": _fed, "entered": bool(_fed)}
        if _RUIN_RECORD:
            # the board BEFORE the act and the coordinate it was REALISED at (never the intent's
            # subject, the a561fb2 lesson): the killing step's key if this step dies
            self._ruin_step = (*self._step_fp, action,
                               tuple(coord) if coord is not None else None, self.cycle)
        res = self.perceive(action, coord, self._intent_now)
        # WHAT THAT ACTION DID TO THE AVATAR, recorded from the frames either side of it.
        routed = self.route(res)
        # ONE CHAIN PER SLOT PER CYCLE (Fig 5; the reviewer 2026-10-07 16:12Z, F500): a term
        # minted this cycle is swept only into slots whose own turn is still to come; a slot
        # already past its turn meets it through its own route next cycle.
        self._turn_ahead = {s for s, b, *_ in routed if b in (REBIND, REFUTED, MECHANISM)}
        _split_now = self._d5_splits(frozenset(s for s, r in res.items() if r.gone))
        # THE SLOTS WHOSE OWN TURN RUNS THIS CYCLE, for the probe flush below: a slot past its
        # turn takes no MINT row after its ACCEPT (F500's rule; the probe flush, 2026-10-14).
        _turned = set(self._turn_ahead) | set(_split_now)
        with self._step_scope("ACCEPT"):
            for slot, b, fit, _why in routed:
                if slot in _split_now:
                    continue
                if b == REBIND and fit:
                    self.bound[slot] = fit
                    self._carry(fit)
                    self.rank.note(fit, self.cycle)
                    self.owed_import.discard(slot)
                    self.abstained.pop(slot, None)
                    self.led.record(self.cycle, "ACCEPT", slot, "rebind", term=fit,
                                    status="candidate", note="refit; the library did not change")
                elif b == REFUTED:
                    self._price_refusal(slot)
                    # a competitor where the library holds one; otherwise the gap is genuinely
                    # new and MECHANISM's answer is the right one.
                    if fit:
                        self.bound[slot] = fit
                        self._carry(fit)
                        self.rank.note(fit, self.cycle)
                        # THE SAME ACT AS A REBIND, SO THE SAME BOOKKEEPING (the reviewer 2026-10-07
                        # 13:11Z, F497): a fitting library term bound, awaiting the ground. Left
                        # owed, the slot drove seed 0's decisions apart from the rebind path.
                        self.owed_import.discard(slot)
                        self.abstained.pop(slot, None)
                        self.led.record(self.cycle, "ACCEPT", slot, "compete", term=fit,
                                        status="candidate",
                                        note=("the bound term was refused here; this is its "
                                              "competitor"))
                    else:
                        self.mint(slot)
                elif b == MECHANISM:
                    self.mint(slot)
                self._turn_ahead.discard(slot)
        self._turn_ahead = None
        if by == "probe":
            self._flush_probe(_turned)
        if self.drive.never_live(len(self.actions)) and not self._said_never_live:
            # NAMED, AND THE REMEDY IS NOT BUILT. Every action has been drawn and no slot
            # has ever carried mass, so either the world is static or the slots do not
            # reach what moves -- indistinguishable from here. The second is
            # CHANNEL_CLOSED about the INTERFACE, and its remedy is step 7 INWARD, which
            # does not exist. Recording it beats a silent zero.
            self._said_never_live = True
            with self._step_scope("IMPORT"):
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
        if self._test is not None:
            # 7j's grade, written in SETTLE time after the slot's ROUTE and MINT rows (moved from
            # right after perceive, where it broke the ladder; the reviewer 2026-10-16 10:56)
            self._test_row()
        self._settle_routine()
        self._promote()
        if _MC6:
            self._muse()
        _, degree = self.env.objective()
        if _COMPLETION_SWEEP:
            self._completion_sweep(degree)
        self.clocks.note(not self.owed_import and bool(self.bound),
                         1 if degree >= 1.0 else 0)
        self.cycle += 1
        # §12.4's trigger is a PERCEPTION reading -- the vocabulary failing to resolve two
        # things the world distinguishes -- so it is recorded, not acted on here.
        indist = self.indistinguishable()
        with self._step_scope("PERCEIVE"):
            self.led.record(self.cycle - 1, "PERCEIVE", "@vector", "indistinct",
                            pairs=len(indist), top=indist[:3],
                            remedy=self.resolve() if indist else None,
                            reads=("same featural vector, different |R|. Ranked by how many "
                                   "objects shared the vector, which the remedy cannot move"))
        if _FED:
            for _e in self._gamma_read.get("fed", ()):
                if _e["name"] is None:
                    continue                                    # a table route names no term
                self._fed_rows.setdefault(_e["name"], []).append((len(self.led), _e["role"]))
        with self._step_scope("REPEAT"):
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
                            # It was reachable only as a substring of the `ACT(NEED(...))`
                            # utterance, and parsing a rendering to recover a value the loop already
                            # holds is
                            # the reconstruction `transcript.py` exists to refuse.
                            action=action,
                            # WHERE IT LANDED (Fig 11, the habitat's half; the reviewer 2026-10-08
                            # 02:30Z). `None` for an action with no position.
                            press=getattr(self, "_press_seen", None),
                            # WHO OFFERED IT: the game by declaration, or the platform in every
                            # state (RESET, F477). None where the world cannot say.
                            provenance=getattr(self.env, "provenance", lambda _a: None)(action),
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
