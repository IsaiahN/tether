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

# no ALPHA, no EPS, no WARM.
#
# SUPPORT is `|R+_s| > 0 for SOME slot s` -- a PREDICATE over slots, not a magnitude
# averaged across them. The EMA existed to smooth an average that should never have
# been computed, the two epsilons were thresholds standing in for the predicate, and
# the warmup guarded a fresh model from calling itself bored -- which a predicate does
# by construction, because a fresh model has live mass on its first miss.
#
# Four deletions and one boolean, and A7's violation goes with them.


class Drive:
    """The trigger and the draw. Owns a counter nothing else touches."""

    def __init__(self, seed: str = "") -> None:
        self.live = True        # a fresh model has not yet failed to be surprised
        self.n = 0
        self.misses = 0
        self.fires = 0
        self.scored = 0
        # WHERE, not just WHICH. An action drawn three times from one state is not
        # three trials -- inert is a verdict earned by trials from DIFFERENT states,
        # because an action can look dead from having been tried against a wall.
        self.tried: dict[str, set] = {}   # action -> distinct states it was drawn from
        self._seed = zlib.crc32(seed.encode()) & 0xFFFF

    def note_step(self, any_live: bool) -> None:
        """ONE call per step, not one per slot. Whether SOME slot carried live mass --
        a predicate over slots, never an average across them, because averaging is how
        a live signal disappears. A probe that shakes something loose sets this true
        and suppresses the next probe until the agent has explained what it found."""
        self.n += 1
        self.live = any_live
        self.misses += int(any_live)

    def note_score(self, moved: bool) -> None:
        self.scored += int(moved)

    def bored(self) -> bool:
        """SUPPORT at zero ON THIS STEP: no slot carried live mass. You cannot compress
        what you never observed, so the answer is perturb, not stop."""
        return self.n > 0 and not self.live

    def never_live(self, n_actions: int) -> bool:
        """SUPPORT at zero FOR THE WHOLE RUN, with every action tried.

        `bored` reads the last step, so a momentary quiet and an instrument that has
        never once registered anything come back identical -- and only the second is
        evidence about the INSTRUMENT rather than about the model. This is the third
        cause of a low reading, CHANNEL_CLOSED, at the level of what the slots are:
        nothing the frame can see has ever moved.

        The action clause is what makes it positive rather than absential. `I drew every
        action on offer and nothing changed` is a bound reporting back. `nothing has
        changed yet` is true on step one of every run there has ever been.

        It does NOT distinguish a static world from an instrument that cannot reach one.
        Those are the same from in here, and saying so is the honest half.

        AND THE DENOMINATOR IS OVER ACTIONS WHILE THE THING REQUIRED MAY BE A SEQUENCE,
        so this cannot mean `nothing I can do changes anything`. It means the narrow
        thing: no SINGLE action, from the states occupied, changed anything.
        """
        # anchor: an action earns `inert` at TWO distinct states, never one. One state
        # cannot separate a dead action from a positional artefact; two is the smallest
        # number that can. Not tuned -- the smallest with the property.
        earned = sum(1 for seen in self.tried.values() if len(seen) > 1)
        return self.n > 0 and self.misses == 0 and earned >= n_actions

    def trials(self) -> dict[str, int]:
        """How many distinct states each action was drawn from -- the evidence behind
        `never_live`, put on the row so the claim can be checked rather than believed."""
        return {a: len(seen) for a, seen in sorted(self.tried.items())}

    def starving(self) -> bool:
        """Nothing is scoring: the curiosity drive's trigger, on the reward channel."""
        return self.n > 0 and self.scored == 0

    def choose(self, actions: tuple[str, ...], cycle: int, where: object = None) -> str:
        """A draw over the labels the environment advertised, and nothing else.
        Deterministic in the cycle so a run is reproducible; no wall clock, no RNG state.

        `where` is the state it was drawn from, and it is what makes a trial a trial."""
        if self.bored():
            self.fires += 1
        pick = sorted(actions)[(cycle * 7 + self._seed) % len(actions)]
        self.tried.setdefault(pick, set()).add(where)
        return pick

    def report(self) -> dict[str, object]:
        return {"probe_fires": self.fires, "probe_n": self.n, "probe_misses": self.misses,
                "any_live": self.live, "bored": self.bored(),
                "starving": self.starving(), "tried": self.trials(),
                "support": "|R+_s| > 0 for SOME slot s -- a predicate, not a threshold"}
