"""Seat-side run control. THE AGENT DOES NOT IMPORT THIS.

Harness configuration is the seat's business and the agent may read only the frame -- so the
cap lives here, the agent discovers it by running out, and `capped` reaches the loop as an
EVENT rather than as a number. A cap value inside the agent's reasoning is the second
firewall's whole subject.

One module rather than a copy in each runner: the fixture uses it now and the harness bridge
will use it at Phase 5, and two implementations of an accruing budget would drift on exactly
the clause that is easiest to lose.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

# anchor: `[I]`, measured from agents Isaiah has trained -- **just enough room to make
# mistakes**. An observation about how learners behave, not a guess and not a preference. And
# EXTERNAL in §22.1's sense: not a quantity the agent produces, and not movable by performing
# differently within a run, which is what makes it an anchor rather than a number tuned toward
# a behaviour by the frame that benefits from it. The harness's 80 is a comment about infinite
# loops; §22.1's 1000 is 2x a human's move count; this is measured on LEARNERS.
PER_LEVEL = 500


class Budget:
    """500 actions per level, ACCRUING. Unspent budget carries forward.

    **THE ACCRUAL IS THE PART THAT GETS LOST.** `500 per level` reads as a flat cap and the
    flat version passes a short fixture perfectly, so it is written as one line that can be
    pointed at: `left += per_level`, never `left = per_level`. An efficient agent has more
    room later, which is the whole intent -- and it is why `bounded` is a fact about the
    AGENT-GAME PAIR rather than about the game.
    """

    def __init__(self, per_level: int = PER_LEVEL) -> None:
        self.per_level = per_level
        self.left = 0
        self.levels = 0
        self.spent = 0

    def level_starts(self) -> None:
        self.levels += 1
        self.left += self.per_level      # ACCRUAL. `=` here would be the flat cap.

    def spend(self) -> bool:
        """One action. False once the budget is gone, which is the CAP event."""
        self.left -= 1
        self.spent += 1
        return self.left > 0

    def exhausted(self) -> bool:
        return self.left <= 0

    def report(self) -> dict:
        return {"per_level": self.per_level, "levels": self.levels,
                "spent": self.spent, "left": self.left,
                "accrued": self.levels * self.per_level,
                "reads": "unspent carries forward; `left` above one level's worth is proof "
                         "the accrual ran rather than the flat version"}
