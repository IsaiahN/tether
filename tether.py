"""The loop. Steps 1 to 5.

One track: an action is proposed by an utterance that type-checks and passes the gate, or
there is no action. There is no fast path, because a fast path is what makes the framework
optional.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from itertools import islice
from typing import Any

import grammar as G
import instruments as I
import retrieval
from gamma import Ctx, Gamma, Term
from ledger import (
    ADVANCE,
    CHANNEL_CLOSED,
    ENDING_READS,
    GENUINE,
    SLICE_TOO_SMALL,
    SPECIFIED,
    Ledger,
)
from probe import Drive

sys.dont_write_bytecode = True

IDN = "idn"

# anchor: how many reachable terms an experiment weighs before choosing. Bounded because
# the choice is made every step and the closure grows; 200 covers depth 2 over the toy
# alphabet exactly, and truncation only ever narrows the spread, never invents one.
DISCRIMINATE_BUDGET = 200

# THE CODE, declared. Both halves of the bargain are lengths under it.
#   a correction on one slot-transition: log2(M) bits, a uniform code over the M values
#   a term of k atoms:                   (k+1) * log2(|atoms|+1), the atoms plus a stop
CODE = "uniform(M) per correction; (k+1)*log2(|atoms|+1) per term"

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


def term_bits(k: int, alphabet: int) -> float:
    return (k + 1) * math.log2(alphabet + 1)


def pays(cost: float, left: float, base: float) -> bool:
    """The bargain. Strict: a tie does not license a new term."""
    return cost + left < base


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
        self.alphabet = self._alphabets(env)
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
        self.env, self.level = env, level
        self.slots = env.slots()
        self.actions = tuple(env.actions())       # a new level may advertise differently
        self.alphabet = self._alphabets(env)      # a new level may value slots differently
        self.bound, self.trace = {}, []
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
        return (state[term.operand],) if term.operand else ()

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

    def _predict(self, slot: str, state: dict[str, int], action: str) -> int:
        term = self.gamma.library[self.bound.get(slot, IDN)]
        return term.apply(state[slot],
                          Ctx(action=action,
                              operands=self._ops(term, state))) % self.alphabet[slot]

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
                            bound=self.bound.get(s, IDN),
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
        gap = retrieval.characterise(hist, slot, list(self.alphabet))
        for n in retrieval.retrieve(self.gamma.library, gap):
            if n != exclude and self._explains(self.gamma.library[n], slot, hist):
                return n
        return None

    def _explains(self, term: Term, slot: str, hist) -> bool:
        return bool(hist) and self._left(term, slot, hist) == 0.0

    def _left(self, term: Term, slot: str, hist) -> float:
        """What the term leaves unexplained across the slot's history, in bits."""
        total = 0.0
        for state, action, actual in hist:
            if not self._applies(term, state):
                total += math.log2(self.alphabet[slot])   # inapplicable is unexplained
                continue
            got = term.apply(state[slot], Ctx(action=action, operands=self._ops(term, state)))
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
            got = term.apply(state[slot], Ctx(action=action,
                                              operands=self._ops(term, state)))
            if got % self.alphabet[slot] != actual % self.alphabet[slot]:
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
                got = term.apply(state[slot], Ctx(action=action,
                                                  operands=self._ops(term, state)))
                wrong += got % self.alphabet[slot] != actual % self.alphabet[slot]
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
        """
        # SUPPORT AT ZERO REFUSES THE MODEL THE WHEEL. `bored()` means no slot carried
        # live mass: the model explains everything it can currently see, and an action
        # IT selects can only confirm it. So boredom does not pick a different draw --
        # the draw was always uninformed and always the default, which is why `fires`
        # counted 441 perturbations that changed no action. What it changes is who is
        # allowed to choose, and 26 of those 441 steps were being steered by the model.
        if self.drive.bored():
            return self.drive.choose(self.actions, self.cycle, _where(before)), "probe"
        owed = [s for s in sorted(self.owed_import) if s in before]
        if owed:
            cands = list(islice(self.gamma.enumerate_closure(
                "val", "val", 2, DISCRIMINATE_BUDGET), DISCRIMINATE_BUDGET))
            spread = {}
            for act in self.actions:
                spread[act] = sum(
                    len({t.apply(before[s], Ctx(action=act, operands=())) % self.alphabet[s]
                         for t in cands})
                    for s in owed)
            if spread and max(spread.values()) > min(spread.values()):
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
                        v = t.apply(before[s], Ctx(action=pick, operands=()))
                        buckets[v % self.alphabet[s]] = buckets.get(
                            v % self.alphabet[s], 0) + 1
                    self._disproof[s] = {
                        "live": len(cands), "splits": len(buckets),
                        "refuted_at_least": len(cands) - max(buckets.values()),
                        "by": f"any outcome on {s} after {pick}"}
                return pick, "discriminate"
        return self.drive.choose(self.actions, self.cycle, _where(before)), "draw"

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
        if now == self.actions:
            return
        gone = sorted(set(self.actions) - set(now))
        came = sorted(set(now) - set(self.actions))
        # §16.8 SENSOR 1 IS `the PREVIOUS ACTION changed the gating`, and the delta alone
        # does not say which action. This runs at the top of the step, so the action just
        # taken is the only candidate -- and attributing it is also sensor 2's whole input.
        self.pre.note(self._last_action, came, gone)
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

    def _bindings(self, slot: str, robs: list) -> list[str | None]:
        """Which slots may fill operand 0, ORDERED by contact and NEVER FILTERED by it.

        None first -- a unary term is cheaper, so it wins when both fit, which is Occam
        priced rather than preferred. Then the rest by how much each VARIES across the
        residual's own frames: a slot constant wherever the bound term was wrong carries
        nothing that could discriminate those frames, so it is tried last. §16.5
        enumerates contact; Figure 11 ranks by cascade.

        ORDERING, NEVER EXCLUSION, and the difference is measured rather than argued.
        The version that DROPPED operand-reading terms when R showed no dependence on
        another slot LOST A CLOSING TERM -- `_cannot_pay` records it. Ranking cannot:
        every binding is still reached, and since the mint breaks on the first closer,
        order decides WHICH closer is found and never WHETHER one exists."""
        others = [s for s in self.slots if s != slot]
        seen = {s: len({st[s] for st, _, _ in robs if s in st}) for s in others}
        return [None] + sorted(others, key=lambda s: (-seen[s], s))

    def mint(self, slot: str) -> None:
        hist = self.history(slot)
        held = self.gamma.library[self.bound.get(slot, IDN)]
        base = self._accumulated(slot, held)
        robs = self._residual_obs(slot, held, hist)
        guards = {"support": base > 0.0, "reachability": False, "novelty": False}
        cuts: list[dict] = []
        best: tuple[float, float, Term] | None = None
        stats: dict = {"seen": 0, "budget_spent": False, "depth_exhausted": True,
                       "units": self.gamma.alphabet, "estimate": 0}
        rank = 0

        if guards["support"]:
            for cand in self.gamma.enumerate_closure("val", "val", self.cfg.max_depth,
                                                     self.cfg.budget, stats):
                for bind in (self._bindings(slot, robs) if cand.reads_operand else [None]):
                    rank += 1
                    term = Term(cand.atoms, operand=bind)
                    if self.gamma.is_atom(term) or term.name in self.gamma.library:
                        cuts.append({"name": term.name, "rank": rank, "reversible": True,
                                     "reason": "not-novel"})
                        continue
                    guards["novelty"] = True
                    cost = term_bits(len(term), self.gamma.alphabet)
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
                    if best is None or left < best[0]:
                        best = (left, cost, term)
                if best is not None and best[0] == 0.0:
                    break

        seen = stats["seen"]
        est = max(stats["estimate"], seen)
        detail = {"guards": guards, "candidates_seen": seen, "candidates_tried": rank,
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

        left, cost, term = best
        self.gamma.accept(term, seq=len(self.led), residual=f"{slot}@{self.cycle}")
        self.bound[slot] = term.name
        self.rank.note(term.name, self.cycle)
        closes = left == 0.0
        if closes:
            self.candidates[term.name] = self.cycle
            self.owed_import.discard(slot)
            self.abstained.pop(slot, None)
        else:
            # it pays and it is not the mechanism. Accepting is correct; settling for it
            # is not -- the slot keeps owing until something closes R.
            self.owed_import.add(slot)
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
            self.chain.reuse_branch["no-eligible-target"] += 1
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
        name, deg = self.env.objective()
        want = G.compose(G.WANT, G.compose("ALL", G.compose(
            "BECOME", G.Leaf(G.T.OBJECT, name), G.Leaf(G.T.ATTR, "satisfied"))))

        bound = self.bound.get(focal)
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
        self._advertised()
        self._present()       # before the frame, so slots and frame cannot disagree
        before = self.env.observe()
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
        # STRATEGY arrives with routines and is 0 until then: an honest zero, not a gap.
        phase = I.DIRECTED if by == "discriminate" else I.PROBE
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
        self.led.record(self.cycle - 1, "REPEAT", "@loop", "repeat",
                        integral=round(self._integral, 3),
                        phase=phase, by=by, stage=self.chain.seg.stage(),
                        gamma_size=len(self.gamma.library), owed=sorted(self.owed_import))
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
