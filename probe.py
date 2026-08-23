"""The two zero-density branches.

density(R) is the first factor of the guard product, and it is the one that goes unattacked
while effort goes to the third. If |R| is about zero the bargain is unsatisfiable whatever
atoms exist -- you cannot compress what you never observed.

Two triggers, on two channels:
    nothing is surprising  -> perturb. The agent's own prediction error has gone to zero.
    nothing is scoring     -> the curiosity drive, aimed at the NOVEL bin.

UNINFORMED BY CONSTRUCTION, and that is the safety property. The draw sees the advertised
action set and nothing else -- not the score, not the goal, not the effect model, not a
slot's value. A probe chosen by the current model can only confirm the current model, and a
probe aimed at reward is Goodhart wearing a probe's coat.

Nothing here scores, mints, promotes or exempts. Its outcome re-enters as an ordinary
observation and is judged under the unchanged bargain.
"""

from __future__ import annotations

import sys
import zlib

sys.dont_write_bytecode = True

ALPHA = 0.1     # the error EMA's weight on the newest step: about a ten-step memory
EPS = 0.02      # what "explains everything" means numerically
WARM = 12       # observations before an untrained model is allowed to call itself bored


class Drive:
    """The trigger and the draw. Owns a counter nothing else touches.

    The error starts at MAXIMAL, never at zero: a fresh model that claimed to explain
    everything would fire on step one, from no evidence at all.
    """

    def __init__(self, seed: str = "") -> None:
        self.err = 1.0
        self.n = 0
        self.misses = 0
        self.fires = 0
        self.scored = 0
        self._seed = zlib.crc32(seed.encode()) & 0xFFFF

    def note(self, _action: str, missed: bool) -> None:
        """Every outcome feeds the same model -- including a probe's own, which is what
        closes the loop: a probe that shakes something loose raises the error and
        suppresses the next probe until the agent has explained what it found."""
        self.n += 1
        self.misses += int(missed)
        self.err = (1.0 - ALPHA) * self.err + ALPHA * (1.0 if missed else 0.0)

    def note_score(self, moved: bool) -> None:
        self.scored += int(moved)

    def bored(self) -> bool:
        """Is the agent learning nothing? Its own error, and nothing else."""
        return self.n >= WARM and self.err <= EPS

    def starving(self) -> bool:
        """Nothing is scoring: the curiosity drive's trigger, on the reward channel."""
        return self.n >= WARM and self.scored == 0

    def choose(self, actions: tuple[str, ...], cycle: int) -> str:
        """A draw over the labels the environment advertised, and nothing else.
        Deterministic in the cycle so a run is reproducible; no wall clock, no RNG state."""
        if self.bored():
            self.fires += 1
        return sorted(actions)[(cycle * 7 + self._seed) % len(actions)]

    def report(self) -> dict[str, object]:
        return {"probe_fires": self.fires, "probe_n": self.n, "probe_misses": self.misses,
                "probe_err": round(self.err, 5), "bored": self.bored(),
                "starving": self.starving(), "eps": EPS, "warm": WARM}
