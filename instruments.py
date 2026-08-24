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
        """how: 'advance' (not scored -- not a loop firing), 'death', or 'run_end'."""
        stage = self.seg.stage()
        self.last_stage = stage
        if how == "advance":
            self.advances += 1
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
