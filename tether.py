"""The loop. Steps 1 to 5.

One track: an action is proposed by an utterance that type-checks and passes the gate, or
there is no action. There is no fast path, because a fast path is what makes the framework
optional.
"""

from __future__ import annotations

import hashlib
import math
import sys
from collections import Counter
from dataclasses import dataclass, field
from functools import partial
from itertools import islice
from typing import Any

import grammar as G
import instruments as I
import retrieval
import routine as Rt
from gamma import SAME_AS_TARGET as G_SAME
from gamma import Ctx, Gamma, Standing, Term
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

# why not the neighbouring bin. A bin without its discriminator is a label, not a diagnosis.
WHY_NOT = {
    HELD: "not novel: the slot is bound and the bound term predicted it",
    NOVEL: "not mechanism: too little history to distinguish a wrong model from a new one",
    REBIND: "not mechanism: a term already in the library explains the whole history",
    MECHANISM: "not rebinding: no library term explains the history, so the model is wrong",
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
    hits = [v for v in range(alphabet) if v != current and evaluate(v)]
    if not hits:
        return NOT_RESOLVED
    if not ordered:
        return hits[0]
    target = min(hits, key=lambda v: (abs(v - current), v))
    return current + (1 if target > current else -1)


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


def objective_degree(evaluate, scope) -> float | None:
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
    mode: str = SPECIFIED


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


class Agent:
    def __init__(self, env: Any, gam: Gamma, cfg: Config | None = None,
                 led: Ledger | None = None) -> None:
        self.env, self.gamma = env, gam
        self.actions = tuple(env.actions())        # asked for, never imported
        # SET HERE AND NOT ONLY IN `retarget`. `_advertised` reads it at the top of every
        # step; it only ever REACHED that read after the set had changed, so the attribute's
        # absence before the first `retarget` was masked by an early return. Feeding the
        # denominator unconditionally is what surfaced it.
        self._last_action: str | None = None
        self.alphabet = self._alphabets(env)
        self.slot_types = self._slot_types(env)
        self.cfg = cfg if cfg is not None else Config()
        # not `led or ...`: an empty Ledger has len 0 and is therefore falsy
        self.led = led if led is not None else Ledger(mode=self.cfg.mode)
        self.slots = env.slots()
        self.bound: dict[str, str] = {}
        # the whole before-state is kept, because an operand is another slot's past value
        self.trace: list[tuple[dict[str, int], str, dict[str, int]]] = []
        self.owed_import: set[str] = set()
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
        self._disproof: dict[str, dict] = {}
        self._last_action: str | None = None   # what may have changed the gating
        self.owed_import, self.abstained = set(), {}
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
                return ()
        return (value,)

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
        if self._decomp_cache is None:
            own = getattr(self.env, "slot_owner", None)
            att = getattr(self.env, "attribute_of", None)
            shp = getattr(self.env, "shapes", None)
            self._decomp_cache = (own() if own else {}, att() if att else {},
                                  shp() if shp else {})
        owners, attrs, shapes = self._decomp_cache
        mine = owners.get(slot)
        if mine is None:
            return None
        rec = {attrs[s]: v for s, v in state.items()
               if owners.get(s) == mine and s in attrs}
        if not rec:
            return None
        # THE STRUCTURE BESIDE THE LABEL, NEVER IN PLACE OF IT. `shape` stays the published
        # id because that is what `Ctx.group` and every equality comparison hold; swapping in
        # the frozenset would compare a set against a table of ints and read FALSE in silence.
        # Two quantities, two keys -- check 5, at the one site where merging them is tempting
        # because they name the same thing.
        cells = shapes.get(rec.get("shape"))
        if cells is not None:
            rec["structure"] = cells
        return rec

    def _group(self, slot: str, state: dict) -> tuple:
        """The outer stream for one slot: this attribute's values on the other objects."""
        if self._peer_cache is None:
            fn = getattr(self.env, "peers", None)
            self._peer_cache = fn() if fn is not None else {}
        return tuple(state[p] for p in self._peer_cache.get(slot, ()) if p in state)

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
        ctx = Ctx(action=action, operands=self._ops(term, state),
                  touching=self._touching(slot), group=self._group(slot, state),
                  obj=self._record(slot, state))
        got = self._value_of(term, slot, state, ctx)
        return None if got is NOT_RESOLVED else got % self.alphabet[slot]

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

    def perceive(self, action: str) -> dict[str, SlotResidual]:
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

    def _rebindings(self, term: Term, slot: str):
        """The term as held, then -- only if it arrived unbound and reads an operand -- the
        typed re-bindings of it. **Composition crosses, binding does not**, so a loaded term
        has to be re-bound at the destination or it is the identity here."""
        yield term
        if not term.reads_operand or term.operand:
            return
        for b in self.slots:
            if b != slot and self._operand_fits(term, slot, b):
                yield Term(term.atoms, operand=b, guard=term.guard)

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
        gap = retrieval.characterise(hist, slot, list(self.alphabet), self.slot_types)
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
            for cand in self._rebindings(self.gamma.library[n], slot):
                # BEFORE `_explains`, and separately from it: may this BIND is a type question
                # and does it EXPLAIN is a behavioural one. Folding the first into the second
                # would put two quantities under one name at the site that decides both.
                if getattr(cand, "out_type", "val") not in BINDABLE:
                    continue
                if not self._explains(cand, slot, hist):
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

    def _left(self, term: Term, slot: str, hist) -> float:
        """What the term leaves unexplained across the slot's history, in bits."""
        total = 0.0
        for state, action, actual in hist:
            if not self._applies(term, state):
                total += math.log2(self.alphabet[slot])   # inapplicable is unexplained
                continue
            got = self._value_of(term, slot, state,
                                 Ctx(action=action, operands=self._ops(term, state),
                                     touching=None,      # replay: contact unknown
                                     group=self._group(slot, state),
                                     obj=self._record(slot, state)))
            if got is NOT_RESOLVED:
                total += math.log2(self.alphabet[slot])   # unread is unexplained
                continue
            total += correction_bits(got, actual, self.alphabet[slot])
        return total

    def route(self, res: dict[str, SlotResidual]) -> list[tuple[str, str, str | None]]:
        out = []
        for slot, r in res.items():
            if r.mass == 0.0 and slot not in self.owed_import:
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
            got = self._value_of(term, slot, state,
                                 Ctx(action=action, operands=self._ops(term, state),
                                     touching=None,      # replay: contact unknown
                                     group=self._group(slot, state),
                                     obj=self._record(slot, state)))
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
            else:
                got = self._value_of(term, slot, state,
                                     Ctx(action=action, operands=self._ops(term, state),
                                         touching=None,  # replay: contact unknown
                                         group=self._group(slot, state),
                                         obj=self._record(slot, state)))
                wrong += (got is NOT_RESOLVED
                          or got % self.alphabet[slot] != actual % self.alphabet[slot])
            if cost + unit * wrong >= base:
                return True          # `wrong` only grows; the rest of R adds nothing
        return False

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
        if self.routine is not None:
            emit, rest = Rt.advance(self.routine, self._holds(before))
            if emit not in (Rt.DONE, Rt.BLOCKED, Rt.EXHAUSTED) and emit in self.actions:
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
                k = self._reject_key(self.routine_for, self.routine)
                self.refuted.setdefault(k, Standing(last_tick=self.cycle)).refute(self.cycle)
                self.refuted_at[k] = 1.0 if rg is None else rg
                extra = {"asked": [Rt.render(self.routine), self.routine_for],
                         "ground_said": False, "status": "refuted",
                         "verdict": "spent its whole budget and the guard never held",
                         "rejections": round(self._rejection(k), 3),
                         "reopens_above": round(self.refuted_at[k], 4)}
            self.led.record(self.cycle, "PLAN", self.routine_for or "*", "routine_end",
                            outcome=why, routine=Rt.render(self.routine), **extra)
            self.routine, self.routine_for = None, None
        if self.drive.bored():
            return self.drive.choose(self.actions, self.cycle, _where(before)), "probe"
        owed = [s for s in sorted(self.owed_import) if s in before]
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
        learned = self._learned_split()
        if learned is not None:
            return learned, "discriminate:learned"
        if self.routine is None:
            self._mint_routine(before)
            if self.routine is not None:   # adopted now: run its first action this cycle
                emit, rest = Rt.advance(self.routine, self._holds(before))
                if emit not in (Rt.DONE, Rt.BLOCKED, Rt.EXHAUSTED) and emit in self.actions:
                    self.routine = rest
                    return emit, "routine"
                self.routine, self.routine_for = None, None
        goal = self._goal_split(before)
        if goal is not None:
            return goal, "discriminate:goal"
        return self.drive.choose(self.actions, self.cycle, _where(before)), "draw"

    def _discrepancy(self, slot: str, state: dict[str, int]) -> int | None:
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
        if term is None or getattr(term, "out_type", None) != OBJ_TYPE or slot not in state:
            return NOT_RESOLVED
        ctx = Ctx(action=self._last_action or "", operands=self._ops(term, state),
                  touching=self._touching(slot), group=self._group(slot, state),
                  obj=self._record(slot, state))

        def _sat(v: int) -> bool | None:
            r = term.apply(v, ctx)
            return None if r is NOT_RESOLVED else bool(r)
        return objective_gap(_sat, state[slot], self.slot_types.get(slot) in ORDERED_TYPES,
                             self.alphabet[slot])

    def goal_residual(self, slot: str, state: dict[str, int]) -> float | None:
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
        if term is None or getattr(term, "out_type", None) != OBJ_TYPE or slot not in state:
            return None
        group = self._group(slot, state)
        if not group:
            return None
        ctx = Ctx(action=self._last_action or "", operands=self._ops(term, state),
                  touching=self._touching(slot), group=group,
                  obj=self._record(slot, state))

        def _sat(v: int) -> bool | None:
            r = term.apply(v, ctx)
            return None if r is NOT_RESOLVED else bool(r)
        deg = objective_degree(_sat, group)
        return None if deg is None else 1.0 - deg

    def can(self, slot: str, state: dict[str, int]) -> str:
        """`CAN(P)` — §14.3's affordance, and it is **ACHIEVABLE, not SATISFIABLE.**

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
                        before, or an action of this agent's has been observed to move the slot
                        toward it. *Prefer "I tried and something happened" over "I have never
                        been there"*
            `unknown`   satisfiable, and nothing in this agent's record says it can be reached
        """
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
        for slot in self.slots:
            g = self._discrepancy(slot, state)
            if not isinstance(g, int):
                # BOTH non-integer outcomes break the trend, and for the SAME reason here --
                # a series needs a distance and neither is one. `CAN` is where they part.
                self._disc.pop(slot, None)
            else:
                self._disc.setdefault(slot, []).append(g)
            rg = self.goal_residual(slot, state)
            if rg is None:
                self._res.pop(slot, None)
            else:
                self._res.setdefault(slot, []).append(rg)
            if g is not NOT_RESOLVED:      # an OBJ term is bound and readable here
                reach[slot] = self.can(slot, state)
        # PUBLISHED EVERY STEP, BECAUSE P1 SHIPS BEFORE ITS CONSUMER. `Until` is what GATES on
        # `CAN` and it does not exist yet, so without this row the producer would be code that
        # runs and says nothing. The counts are the thing to watch: `no` is a claim about the
        # world, `unknown` a claim about the record, and a board that is all `unknown` has told
        # you the trace is too thin rather than that nothing is reachable.
        if reach:
            self.led.record(self.cycle, "PERCEIVE", "*", "can",
                            **{k: sum(1 for v in reach.values() if v == k)
                               for k in (YES, NO, UNKNOWN)})

    def _goal_choice(self) -> str | None:
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
        for slot, series in sorted(self._res.items()):
            if len(series) < MIN_REPEAT + 1:
                continue
            window = series[-(MIN_REPEAT + 1):]
            deltas = [b - a for a, b in zip(window, window[1:], strict=False)]
            if all(d <= 0 for d in deltas) and any(d < 0 for d in deltas):
                shrink = -sum(deltas)
                if best is None or shrink > best[0]:
                    best = (shrink, slot)
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
            rg = self.goal_residual(guard, state)
            return None if rg is None else rg <= 0.0
        return holds

    def _rejection(self, key: tuple) -> float:
        """The decayed strength of rejection. `Standing.decay` on the LOGICAL clock -- cycles,
        never wall time -- which is §18.2's first defeasance route and was already built."""
        st = self.refuted.get(key)
        if st is None:
            return 0.0
        st.decay(self.cycle)
        return st.rejections

    @staticmethod
    def _reject_key(slot: str, r) -> tuple:
        """The identity a refutation is filed under. **BUDGET-FREE ON PURPOSE.**

        §18.2's immune audit names **pathogen mimicry** -- *a dead idea re-tried under a slightly
        different key* -- and calls the signature granularity a problem *left to the caller
        rather than baked in*. Here the caller is this method, and the answer is that a routine
        differing only in its budget is THE SAME HYPOTHESIS: the budget is derived from the gap
        and moves every cycle, so keying on it would let one refuted routine return under a new
        number every step.
        """
        return (slot, Rt.actions(r), Rt.guards(r))

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
        slot = self._goal_choice()
        if slot is None or slot not in before:
            self.led.record(self.cycle, "PLAN", slot or "*", "routine_refused",
                            reason="no objective is confidently shrinking"
                                   if slot is None else
                                   "the selected objective's slot is not in this frame")
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
        shelf = tuple(r for r in self.routines
                      if set(Rt.actions(r)) <= set(self.actions))
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
        cands = Rt.enumerate_routines((act,), mine or (slot,), shelf, loop_budget)
        # WEIGHTED AND CLOCKED, per §18.2 via `gamma.Standing`: a refutation excludes only while
        # its decaying strength stands, so a failed shape leaves the running and returns.
        cands = [c for c in cands
                 if self._rejection(self._reject_key(slot, c)) < 1.0]
        if not cands:
            self.led.record(self.cycle, "PLAN", slot, "routine_refused",
                            reason="every rejection still stands and nothing has surprised",
                            strengths=[round(self._rejection(k), 3) for k in self.refuted
                                       if k[0] == slot])
            return
        # `left` IS WHAT THE CANDIDATE CANNOT REACH, NOT ZERO. See `routine.reach`.
        # THE BARGAIN IS TWO-PART AND STAYS TWO-PART ON THE ROW. These were folded into one
        # number and handed to `pays` as `cost` with `left = 0` -- arithmetically identical and
        # **unreadable**: the ledger then said `cost` for a quantity that was description PLUS
        # residual, so no reader could see which half bought the term. *A change that makes the
        # agent better and its reasoning unreadable has destroyed the instrument*, and the
        # mislabelled row is `A6i` at the site a future reader would trust.
        priced = [(term_bits(Rt.length(c, shelf), n),
                   max(0.0, unsat - Rt.reach(c)) * math.log2(n), c) for c in cands]
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
                            considered=len(priced), shelf=len(shelf))
            return
        self.routine, self.routine_for = cand, slot
        self.led.record(self.cycle, "PLAN", slot, "routine", verdict="pays",
                        routine=Rt.render(cand), length=Rt.length(cand),
                        units=Rt.length(cand, shelf),
                        chunked=Rt.length(cand) != Rt.length(cand, shelf),
                        cost=round(cost, 4), left=round(left, 4),
                        base=round(base, 4), gap=gap, reach=Rt.reach(cand),
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
        votes: dict[str, int] = dict.fromkeys(self.actions, 0)
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
            if any(a not in hist for a in self.actions):
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
                    if moved * 2 > len(hist[a]):
                        votes[a] += 1         # this action MOSTLY moved it the wanted way
                elif any(f == wanted for _, f in hist[a]):
                    votes[a] += 1             # unordered: it has produced that value
        if not n_goals or max(votes.values()) == 0:
            return None
        top = max(votes.values())
        tied = sum(1 for v in votes.values() if v == top)
        self._ties[("goal", tied)] += 1
        if tied == len(self.actions):
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
        if now == tuple(self.slots):
            return
        gone = sorted(set(self.slots) - set(now))
        came = sorted(set(now) - set(self.slots))
        for g in gone:
            self.bound.pop(g, None)
            self.owed_import.discard(g)
            self.abstained.pop(g, None)
        # a term bound to a SURVIVING slot may read an operand on a departed one, and
        # `_ops` would fault on the next bet. It owes again rather than faulting.
        orphaned = sorted(k for k, n in self.bound.items()
                          if self.gamma.library[n].operand in gone)
        for k in orphaned:
            self.bound.pop(k, None)
            self.owed_import.add(k)
        self.led.record(self.cycle, "PERCEIVE", "@instrument", "present",
                        gone=gone, came=came, orphaned=orphaned,
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
        hist = self.history(slot)
        held = self.gamma.library[self.bound.get(slot, IDN)]
        base = self._accumulated(slot, held)
        robs = self._residual_obs(slot, held, hist)
        # HOISTED, because `units()` rebuilds a list and the pricing runs once per candidate.
        _units = tuple(self.gamma.units())
        guards = {"support": base > 0.0, "reachability": False, "novelty": False}
        cuts: list[dict] = []
        best: tuple[float, float, float, Term] | None = None
        stats: dict = {"seen": 0, "budget_spent": False, "depth_exhausted": True,
                       "units": self.gamma.alphabet, "estimate": 0}
        by_kind: dict[str, tuple] = {}
        rank = 0

        if guards["support"]:
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
                kind = "predictor" if out_t == "val" else "objective"
                by_fit = partial(retrieval.fits, gap=gap, in_type=in_t, out_type=out_t)
                st: dict = {"seen": 0, "budget_spent": False, "depth_exhausted": True,
                            "units": self.gamma.alphabet, "estimate": 0}
                for cand in self.gamma.enumerate_closure(in_t, out_t, self.cfg.max_depth,
                                                         self.cfg.budget, st, order=by_fit):
                    binds = operand_binds if cand.reads_operand else [None]
                    binds = [x for x in binds if self._operand_fits(cand, slot, x)]
                    for bind, g in ((b, g) for b in binds for g in self._guards(robs)):
                        rank += 1
                        term = Term(cand.atoms, operand=bind, guard=g)
                        if self.gamma.is_atom(term) or term.name in self.gamma.library:
                            cuts.append({"name": term.name, "rank": rank, "reversible": True,
                                         "reason": "not-novel"})
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
                            continue
                        left = self._left(term, slot, hist)
                        if not pays(cost, left, base):
                            cuts.append({"name": term.name, "rank": rank, "reversible": True,
                                         "reason": "does-not-pay"})
                            continue
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
        if len(contest) == 2:
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
            if detail["verdict"] == "no_support":
                self._starved.add(slot)
            if detail["verdict"] in ("budget_spent", "depth_exhausted"):
                self.owed_import.add(slot)
                self.abstained[slot] = {"depth": self.cfg.max_depth, "candidates": seen,
                                        "coverage": detail["coverage"],
                                        "verdict": detail["verdict"],
                                        "units_then": stats.get("units", 0),
                                        "base_bits": round(base, 3)}
            self.led.record(self.cycle, "MINT", slot, "park", of=(slot,), **detail)
            return

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
                t = Term(cand.atoms, operand=bind)
                left = self._left(t, slot, hist)
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
            return (rec.get("verdict") != "depth_exhausted"
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
            if left == 0.0:
                self.explain(slot, base - left)
                # THE SWEEP IS A PULL AND EMITTED NO PULL ROW. `reused()` counts `pull` rows
                # and this is the only path that RE-BINDS, so every reuse it found was
                # invisible to the bench-pull and transfer columns both.
                self.led.record(self.cycle, "ROUTE", slot, "pull", term=cand.name,
                                held=tkey, chain=" . ".join(a.name for a in cand.atoms),
                                rebound=True, via="sweep",
                                origin=(self.gamma.stamps.get(tkey) or {}).get("origin"),
                                reads="a library entry reached for BY THE SWEEP")
                self.chain.note_reuse_attempt(f"closed:{how}")
                self.chain.note_reused()
                self.chain.note_cleared()
                name = (cand.name if cand.name in self.gamma.library
                        else self._install_reuse(cand, slot))
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
            elif left < base:
                self.chain.note_reuse_attempt("did-not-pay")
            else:
                self.chain.note_reuse_attempt("no-split")

    def _install_reuse(self, cand: Term, slot: str) -> str:
        """The SWEEP's entry into Gamma, and it is the one path that does not consult `pays`.

        **TWO GATES ON ONE LIBRARY.** `mint` requires `cost + left < base`; this fires when
        `_reach` returns a term with `left == 0.0`, and a term that explains a parked residual
        completely can still be LONGER than the residual is worth. §14.4 says *one bargain*, and
        this is the site where there are two.

        **NOT REPAIRED, AND NOT SILENT EITHER.** `_install_reuse` was never called across the
        demo panel -- the single sweep pull reused a term already in the library -- so a gate
        added here would change what enters Gamma with **no board on which to read the change**,
        which is the fitting-to-an-argument the deferred repairs have all been held against.
        **So the row states what the bargain WOULD have said**, exactly as `can` published its
        reading before `Until` existed to consume it: the first run that exercises this path
        answers the question instead of a decision made without one.
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
                        note="entered on left==0 alone; `pays` is not consulted on this path")
        self.gamma.accept(cand, seq=len(self.led), residual=f"reuse:{slot}@{self.cycle}")
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
                if self.gamma.refute(name):
                    self.demoted.append(name)
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
                         G.Leaf(G.T.ATTR, before[s])) for s in self.slots]
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
            self.led.record(self.cycle, "PERCEIVE", "@loop", "no_slots",
                            slots=0, cause=CHANNEL_CLOSED,
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
        focal = max(sorted(self.slots),
                    key=lambda s: (self._last_mass.get(s, 0.0), s in self.owed_import))
        by = "given"
        self._disproof = {}
        if action is None:
            action, by = self.choose(before)
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
        res = self.perceive(action)
        for slot, b, fit, _why in self.route(res):
            if b == REBIND and fit:
                self.bound[slot] = fit
                self.rank.note(fit, self.cycle)
                self.owed_import.discard(slot)
                self.abstained.pop(slot, None)
                self.led.record(self.cycle, "ACCEPT", slot, "rebind", term=fit,
                                status="candidate", note="refit; the library did not change")
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
                        # LEVEL ON EVERY REPEAT ROW, because a per-level series cannot be
                        # reconstructed without it. The `ending` row carries `to_level` and
                        # records the BOUNDARY; nothing said which level a given cycle was in,
                        # so the four columns had no way to be segmented.
                        level=self.level,
                        phase=phase, by=by, stage=self.chain.seg.stage(),
                        gamma_size=len(self.gamma.library), owed=sorted(self.owed_import),
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
