"""The instruments. Built before the thing they measure.

Three readings, none of which needs a win:

  STAGE     how far down the chain a stall got. Seven codes, each subsuming the one
            before, and only ONE of them indicts the architecture. A stage-one or
            stage-three stall must never be written up as a verdict on the design.
  PHASE     every action tagged probe / directed / strategy. Humans run ~30 random,
            ~10 directed, ~5 strategy to a level win, and the phase 1 share shrinking
            across levels IS the transfer claim.
  CLOCKS    steps-to-model and steps-to-win, separately. A short first with a long
            second is a planning failure and must never be reported as a learning one.

Nothing here scores anything. They describe what the agent did; the ground still settles.
"""

from __future__ import annotations

import sys
from collections import Counter
from dataclasses import dataclass, field
from typing import Any

sys.dont_write_bytecode = True

# -- the chain, in order. A later stage cannot be reached without every earlier signal.
DIED_PRE_DIFF = "DIED_PRE_DIFF"        # implementation -- the diff never ran
RESIDUAL_EMPTY = "RESIDUAL_EMPTY"      # library -- wrong grain, nothing to explain
MINT_UNFIRED = "MINT_UNFIRED"          # gate calibration -- residual there, no mint
REUSE_UNWIRED = "REUSE_UNWIRED"        # implementation -- reuse never ATTEMPTED
MINTED_UNUSED = "MINTED_UNUSED"        # ARCHITECTURE -- the only code that indicts
USED_NOCLEAR = "USED_NOCLEAR"          # drive layer -- reused, nothing cleared
CLEARED = "CLEARED"                    # the loop fired once

STAGES = (DIED_PRE_DIFF, RESIDUAL_EMPTY, MINT_UNFIRED, REUSE_UNWIRED,
          MINTED_UNUSED, USED_NOCLEAR, CLEARED)

INDICTS = MINTED_UNUSED     # and nothing else

# funnel keys that record a fact about the search rather than a reuse attempt
NOT_ATTEMPTS = ("no-eligible-target", "rescan")

PROBE, DIRECTED, STRATEGY = "probe", "directed", "strategy"


@dataclass
class Segment:
    """One span of play between two break events. Signals are scoped HERE, never
    cumulated over the run: a mint in segment 3 must not credit the stall in segment 7,
    or a wiring gap silently reads as progress."""

    diff_ran: bool = False
    residual_live: bool = False
    minted: bool = False
    reuse_attempted: bool = False
    reused: bool = False
    cleared: bool = False
    steps: int = 0

    def stage(self) -> str:
        if not self.diff_ran:
            return DIED_PRE_DIFF
        if not self.residual_live:
            return RESIDUAL_EMPTY
        if not self.minted:
            return MINT_UNFIRED
        if not self.reuse_attempted:
            return REUSE_UNWIRED
        if not self.reused:
            return MINTED_UNUSED
        return CLEARED if self.cleared else USED_NOCLEAR


@dataclass
class Chain:
    """Per-segment chain accounting: which link breaks, as a measured distribution."""

    seg: Segment = field(default_factory=Segment)
    stalls: Counter = field(default_factory=Counter)
    advances: int = 0          # counted apart: an advance is drive/search, NOT the loop
    capped: int = 0            # PSEUDO-DEATHS: the seat ended it, not the world
    reuse_attempts: int = 0
    reuse_branch: Counter = field(default_factory=Counter)
    last_stage: str | None = None

    # -- notes, each called from the exact site where the event happens ---------------

    def note_diff(self, live: bool) -> None:
        self.seg.diff_ran = True
        self.seg.residual_live |= live
        self.seg.steps += 1

    def note_mint(self) -> None:
        self.seg.minted = True

    def note_reuse_attempt(self, branch: str) -> None:
        """Every attempt is charged to the branch that resolved it, so the identity
        sum(reuse_branch) == reuse_attempts is published rather than assumed."""
        self.seg.reuse_attempted = True
        self.reuse_attempts += 1
        self.reuse_branch[branch] += 1

    def note_reused(self) -> None:
        self.seg.reused = True

    def note_cleared(self) -> None:
        """Only a break closed by acting on a TRANSFERRED operator. A level advancing by
        search or by the drive layer can never set this."""
        self.seg.cleared = True

    # -- segment ends ------------------------------------------------------------------

    def close(self, how: str) -> str:
        """how: one of `2e`'s five -- `win`, `death`, `reset`, `advance`, `cap` -- or
        `run_end`. An advance is not scored: it is not a loop firing.

        **A CAP IS A PSEUDO-DEATH IMPOSED FROM OUTSIDE THE GAME**, and it is neither. It ends
        the episode like a death, but the cause is THE SEAT rather than the world -- and it is
        not a stall either, because the loop did not fail to progress: **it ran out of room
        the seat granted.** Counting it as a stall attributes a reasoning stage to a
        resource exhaustion, which is §19's bug in a third place -- the first two being the
        mint's `UNREACHED` and the episode's ending. *Never let a filter hand you a verdict*,
        and a budget is a filter.
        """
        stage = self.seg.stage()
        self.last_stage = stage
        if how in ("advance", "win"):
            self.advances += 1
        elif how == "cap":
            self.capped += 1        # neither an advance nor a stall: the seat ended it
        else:
            self.stalls[stage] += 1
        self.seg = Segment()
        return stage

    def report(self) -> dict:
        # the identity is published rather than assumed. Two keys are bookkeeping, not
        # attempts: "no-eligible-target" (there was no second task to fail on) and
        # "rescan" (the unit set grew, so the search was re-run). Both are counted so
        # their zeros are measured, and both are excluded from the identity.
        attempts_charged = sum(v for k, v in self.reuse_branch.items()
                               if k not in NOT_ATTEMPTS)
        return {"stage": self.last_stage or self.seg.stage(), "stalls": dict(self.stalls),
                "advances": self.advances, "reuse_attempts": self.reuse_attempts,
                "reuse_branch": dict(self.reuse_branch),
                "branch_identity_holds": attempts_charged == self.reuse_attempts,
                "indicted": self.stalls.get(INDICTS, 0)}


@dataclass
class Phases:
    """The action mix over time. The composition test that needs no win."""

    counts: Counter = field(default_factory=Counter)
    window: list[str] = field(default_factory=list)
    per_level: list[Counter] = field(default_factory=list)

    def note(self, phase: str) -> None:
        self.counts[phase] += 1
        self.window.append(phase)

    def level_done(self) -> None:
        self.per_level.append(Counter(self.window))
        self.window = []

    def mix(self, c: Counter | None = None) -> dict[str, float]:
        c = c if c is not None else self.counts
        n = sum(c.values()) or 1
        return {p: round(c.get(p, 0) / n, 3) for p in (PROBE, DIRECTED, STRATEGY)}

    def report(self) -> dict:
        return {"total": self.mix(),
                "per_level": [self.mix(c) for c in self.per_level],
                "probe_share_trend": [self.mix(c)[PROBE] for c in self.per_level]}


@dataclass
class Preconditions:
    """§16.8 sensor 2: pairwise `a became available after b`, with counts.

    An action appearing is a CONDITION MET, and the action just taken is the only candidate
    for having met it. This counts the pairs and nothing else -- it does not rank them, name
    a cause, or gate anything. **A count is not a claim**: `b` preceding `a` many times is
    evidence the agent can read, and reading it is the agent's job rather than this table's.

    Cheap by construction: at most |actions| squared cells, 49 for ARC's seven.
    """

    after: Counter = field(default_factory=Counter)
    gone_after: Counter = field(default_factory=Counter)

    def note(self, prev: str | None, came: list[str], gone: list[str]) -> None:
        if prev is None:
            return                      # nothing preceded the first frame
        for a in came:
            self.after[(prev, a)] += 1
        for a in gone:
            self.gone_after[(prev, a)] += 1

    def report(self) -> dict:
        return {"came_after": {f"{b}->{a}": n for (b, a), n in sorted(self.after.items())},
                "gone_after": {f"{b}->{a}": n for (b, a), n in sorted(self.gone_after.items())},
                "reads": "a count, not a claim: what followed what, for the agent to read"}


@dataclass
class Rank:
    """3d / §17.7. The interim rank function -- `(cost, reuse count, recency)`, IN THAT ORDER.

    §17.7: *no principled rank function anywhere -- enumeration is registry-order everywhere
    it appears ... the reuse funnel does supply the beginnings of one (**a φ that has been
    reused should rank above one that has not**), but nobody wired it.* And the fix it names
    is explicit: *rank by `(cost, reuse count, recency of the residual it last closed)`.*

    **THE TUPLE ORDER IS THE SPEC'S, NOT A CHOICE.** Cost first means reuse only breaks ties
    among units of equal cost, which is weaker than the parenthetical's *above one that has
    not* -- and the two are in tension. **The stated tuple wins**, because an improvised
    ordering is a repair fitted to the case that prompted it, and what the weaker version
    turns out to do is a reading about the interim rank rather than a reason to redesign it.

    IT RANKS UNITS, NOT CANDIDATES. A minted candidate is by construction NOT in the library
    -- the novelty guard cuts the ones that are -- so its own reuse count is zero always, and
    a rank over candidates would be dead on arrival. **The objects that HAVE reuse histories
    are the units the search composes from** (§14.2: a settled term re-enters the search as
    one unit), and ordering `units()` reorders every composition downstream for free.

    §17.7 also says the trained proposer (§15.6) replaces this and **should not be waited
    for**, which is why this is four fields rather than a model.
    """

    used: dict[str, int] = field(default_factory=dict)
    last: dict[str, int] = field(default_factory=dict)

    def note(self, name: str, cycle: int) -> None:
        """This term just closed a residual. Both terms of the rank come off one event."""
        self.used[name] = self.used.get(name, 0) + 1
        self.last[name] = cycle

    def key(self, unit: Any) -> tuple:
        n = unit.name
        return (len(unit), -self.used.get(n, 0), -self.last.get(n, -1))

    def report(self) -> dict:
        return {"tracked": len(self.used), "reused": sum(1 for v in self.used.values() if v > 1),
                "reads": "cost first, per §17.7's stated tuple; reuse breaks ties within a cost"}


@dataclass
class Termination:
    """§16.8 sensor / §20.1: what KIND of ending this environment has.

    Nothing in the frame announces it, so it is read -- and **the evidence is asymmetric**:

        a win is possible    `win_levels > 0`              given up front
        DEATH is possible    a GAME_OVER, once             PROVEN, never disproven
        bounded              an ending with no death and no cap firing   proven by observation
        OPEN                 none of the above, so far     NEVER PROVEN -- only defaulted to

    ***Not having died is not evidence that you cannot die.*** So `death_possible` LATCHES
    true and never latches back, and **`OPEN` is a standing ASSUMPTION rather than a
    finding.** The two-state version reports *this game has no death*, which is the absential
    claim the corpus rules out everywhere else: *absence of evidence resting on completeness
    never holds mid-episode.* `report()` therefore says which reads are PROVEN and which are
    ASSUMED, and the class alone is never the whole answer.

    THE AGENT DOES NOT READ THE CAP. `capped` arrives as an EVENT from the seat, because
    harness configuration is the seat's business and the agent discovers its budget by
    running out. A cap value in here would be a config number inside the agent's reasoning,
    which is the second firewall's whole subject.

    AND UNDER AN ACCRUING BUDGET `bounded` IS ABOUT THE PAIR, NOT THE GAME. The cap firing is
    partly a fact about the AGENT's efficiency, so the same board is `bounded` for a careful
    agent and `capped` for a wasteful one. Said on the row, because *termination class* reads
    as a property of the world and under accrual it is not.
    """

    win_possible: bool = False
    death_possible: bool = False        # latches; never latches back
    bounded_seen: bool = False
    capped_seen: bool = False
    endings: int = 0

    def offer(self, win_levels: int) -> None:
        """Given up front, and the only read that needs no observation."""
        self.win_possible = self.win_possible or win_levels > 0

    def ending(self, kind: str) -> None:
        """One episode ended. `kind` is the seat's word: `death`, `cap`, or an ordinary end."""
        self.endings += 1
        if kind == "death":
            self.death_possible = True      # LATCHED
        elif kind == "cap":
            self.capped_seen = True
        else:
            self.bounded_seen = True

    def klass(self) -> str:
        if self.death_possible:
            return "death_possible"
        if self.bounded_seen:
            return "bounded"
        return "open"

    def report(self) -> dict:
        k = self.klass()
        return {
            "class": k,
            "win_possible": self.win_possible,
            "death_possible": self.death_possible,
            "capped_seen": self.capped_seen,
            "endings": self.endings,
            "proven": [n for n, v in (("win_possible", self.win_possible),
                                      ("death_possible", self.death_possible),
                                      ("bounded", self.bounded_seen)) if v],
            "assumed": ["open -- never proven, only defaulted to"] if k == "open" else [],
            "reads": ("not having died is not evidence that you cannot die; and under an "
                      "accruing budget `bounded` is about the AGENT-GAME PAIR, since the cap "
                      "firing is partly a fact about efficiency"),
        }


@dataclass
class Agency:
    """§16.8 sensor 3, and §16.2 rules how it may be read.

    `THE_MISSION`: *the ONLY legitimate distinction is topical I/O -- is there an AVATAR my
    directional actions translate, or do I act through a CLICK ACTUATOR -- and even that
    **BLENDS mid-game**, so it must be detected CONTINGENTLY PER STEP, never used to label
    the game.*

    So this is a sensor, not a config flag, and `mode()` is re-read every step:

        one slot's delta correlates with my action   -> avatar
        no slot correlates but the board changes     -> actuator, acting at a distance
        several correlate                            -> coupled bodies

    A PREDICATE, NOT A THRESHOLD. A slot is action-contingent when SOME action has always
    moved it and SOME OTHER action has never moved it -- an existence claim over what was
    observed, with no rate, no cutoff and no window to tune. Weaker than a correlation and
    it cannot be gamed by a number nobody chose.
    """

    moved: Counter = field(default_factory=Counter)     # (slot, action) -> times it changed
    tried: Counter = field(default_factory=Counter)     # (slot, action) -> times it was tried
    any_change: int = 0
    steps: int = 0

    def note(self, action: str, changed: set[str], slots: list[str]) -> None:
        self.steps += 1
        self.any_change += int(bool(changed))
        for s in slots:
            self.tried[(s, action)] += 1
            if s in changed:
                self.moved[(s, action)] += 1

    def contingent(self) -> list[str]:
        """Slots whose movement depends on WHICH action was taken."""
        out = []
        for s in {k[0] for k in self.tried}:
            acts = [a for (sl, a) in self.tried if sl == s]
            always = [a for a in acts if self.moved[(s, a)] == self.tried[(s, a)]]
            never = [a for a in acts if self.moved[(s, a)] == 0]
            if always and never:
                out.append(s)
        return sorted(out)

    def mode(self) -> str:
        c = self.contingent()
        if len(c) == 1:
            return "avatar"
        if len(c) > 1:
            return "coupled"
        return "actuator" if self.any_change else "unread"

    def report(self) -> dict:
        c = self.contingent()
        return {"control_mode": self.mode(), "contingent_slots": c, "steps": self.steps,
                "reads": "per step, never a label -- it blends mid-game (§16.2)"}


@dataclass
class Clocks:
    """Two, because understanding is not winning and they fail differently."""

    steps_to_model: int | None = None
    steps_to_win: int | None = None
    _step: int = 0

    def note(self, all_explained: bool, levels: int) -> None:
        """`modelled` is NO SLOT OWES -- not an averaged error under a threshold. A
        global reading near zero with one live slot is a legal state and not an inert
        one, so an average would declare the model complete while a slot is unexplained,
        and it would do so sooner the more slots there are."""
        self._step += 1
        if self.steps_to_model is None and all_explained:
            self.steps_to_model = self._step
        if self.steps_to_win is None and levels > 0:
            self.steps_to_win = self._step

    def report(self) -> dict:
        m, w = self.steps_to_model, self.steps_to_win
        return {"steps_to_model": m, "steps_to_win": w,
                "execution_gap": (w - m) if (m is not None and w is not None) else None,
                "reads": ("modelled, not won -- links 3-5" if m is not None and w is None
                          else "won without modelling -- suspect luck" if w is not None
                          and m is None else "neither yet" if m is None else "both")}
