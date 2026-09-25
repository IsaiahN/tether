"""gridworld: an ARC-SHAPED HABITAT. Generated boards, objects, reachable goals. No ARC game.

**ISAIAH, 2026-09-25, and it is the ONLY exception to the board stop:** *"Why can't we make an
ARC-shaped world with randomly generated objects and goals to be reachable? Nothing complex but
good enough to fully test its capabilities."* It replaces both the toy-world patch and the
minimal grid fixture that was queued at 6.5.

    IT IS A HABITAT, NOT A BENCHMARK. What it is for is WHETHER THE MECHANISMS FIRE.
    It is not for a performance number, and a score taken here would be a score of the
    generator.

**WHY IT EXISTS: THREE FINDINGS ARE DEAD FOR ONE REASON AND IT IS THE WORLD, NOT THE CODE.**
`F356` the spectator test reads empty · `F359` the residual precondition refuses nothing because
`robs` is never empty · `F360` the consumer has one kind in contention and no contest. **The toy
world is seven scalar slots under arithmetic where every action moves everything**, so none of
the three can be exhibited there. They are habitat-shaped and this is the habitat.

**THE VOCABULARY IS DELIBERATELY UNCHANGED.** `world._atoms()` is reused verbatim, so the ONLY
variable that moves between the toy world and this one is the HABITAT. A mechanism that fires
here and not there is then a fact about contact rather than about the atom set. Grid-native atoms
are a follow-on and would confound exactly this comparison if taken first.

---

**WHAT THE GENERATOR DOES NOT CONTROL — the reviewer asked for this explicitly, and it is the
guard against the failure I nearly committed with the toy-world patch: *a repair validated on its
own case*, building the habitat that makes your own finding pass.**

    it does NOT read the agent's atom set, bindings, Gamma, or any book
    it does NOT choose goals the agent can express -- a target is a random reachable
      cell, drawn before any agent exists
    it does NOT vary with the finding under test. One generator, one seed -> one board,
      and the seed is the caller's
    it does NOT place the mover at its target, and it does NOT guarantee a SHORT path --
      only that a path EXISTS, because it was walked to build the target

**What it DOES control is the thing that makes the three findings exhibitable at all: SOME SLOTS
DO NOT MOVE UNDER SOME ACTIONS.** That is not tuning -- it is the defining property of a grid
with more than one object, and its absence is what made the toy world unable to show them.
"""

from __future__ import annotations

import random
import sys
from dataclasses import dataclass, field
from typing import Any

import world as _toy
from gamma import Atom

sys.dont_write_bytecode = True

# anchor: three objects need room to be non-adjacent and a walk needs somewhere to go;
# 5x5 is the smallest board where both hold, and small enough to sweep exhaustively.
GRID = 5
ACTIONS = ("up", "down", "left", "right")
GOAL_SLOT = _toy.GOAL_SLOT                      # one name, and it is the toy world's

_DELTA = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}


@dataclass
class GridWorld:
    """One generated board. `seed` selects it; the same seed is the same board, always.

    THREE OBJECT ROLES, and the middle one is why this is not just a bigger toy world:

        o0  THE MOVER      every action moves it (bounded by the wall and the board edge)
        o1  THE PUSHED     moves ONLY when o0 is behind it in the action's direction --
                           so it is action-bearing on SOME actions and a spectator on others
        o2  THE WALL       never moves under any action. A pure spectator, by construction

    Colours never change. They are there because an ARC board has them and because a slot
    that no action can reach is exactly what `F356`'s spectator test needs to find.
    """

    seed: int = 0
    state: dict[str, int] = field(default_factory=dict)
    target: tuple[int, int] = (0, 0)
    # THE HABITAT DOES NOT OWN THE VOCABULARY, and `lint`'s TID251 is what said so: reaching
    # into another module's private atom set is the coupling that makes "one variable moves"
    # unverifiable. Passed in, or taken from the toy world's PUBLIC accessor.
    atom_set: list[Atom] | None = None

    def __post_init__(self) -> None:
        rng = random.Random(self.seed)
        cells = rng.sample([(r, c) for r in range(GRID) for c in range(GRID)], 3)
        (r0, c0), (r1, c1), (r2, c2) = cells
        # **o1 IS PLACED WITHIN REACH OF o0, AND THE REASON IS ARC-FIDELITY, NOT A FINDING.**
        # Measured on the first version: ONE slot of ten carried any residual, the integral was
        # 27.86 against the toy world's 128.26, and NOTHING bound -- a slot with no surprise has
        # nothing to buy, so `cost + left < base` cannot hold at `base = 0`.
        #
        # **A BOARD WHERE ONE OBJECT MOVES THROUGH EMPTY SPACE IS A MAZE, NOT AN ARC TASK.** ARC
        # boards have objects that INTERACT. That is the justification and it is independent of
        # any finding -- which matters, because the reviewer's standing warning is that a
        # generated world can be generated until a finding passes.
        near = [(r0 + dr, c0 + dc) for dr in (-2, -1, 1, 2) for dc in (-2, -1, 0, 1, 2)
                if 0 <= r0 + dr < GRID and 0 <= c0 + dc < GRID and (r0 + dr, c0 + dc) != (r2, c2)]
        if near:
            r1, c1 = rng.choice(near)
        self.state = {
            "o0.row": r0, "o0.col": c0, "o0.colour": rng.randrange(4),
            "o1.row": r1, "o1.col": c1, "o1.colour": rng.randrange(4),
            "o2.row": r2, "o2.col": c2, "o2.colour": rng.randrange(4),
        }
        # REACHABLE BY CONSTRUCTION, not by assertion. The target is where the mover ends up
        # after a random legal walk from its own start, so a path provably exists and nothing
        # had to be searched to know it. A generator that PICKED a target would have to prove
        # reachability afterwards, and that proof is exactly the thing that tends to be skipped.
        #
        # AND THE WALK IS REJECTED IF IT LANDS BACK HOME. Measured on the first 60 boards:
        # **10 of 60 STARTED ALREADY SOLVED**, because a random walk returns to its origin
        # often on a 5x5. A board whose goal is met at step 0 exercises nothing and would
        # have quietly inflated any later "the goal was reached" reading.
        r, c = r0, c0
        for _ in range(20):
            r, c = r0, c0
            for _ in range(rng.randrange(2, 8)):
                dr, dc = _DELTA[rng.choice(ACTIONS)]
                nr, nc = r + dr, c + dc
                if 0 <= nr < GRID and 0 <= nc < GRID and (nr, nc) != (r2, c2):
                    r, c = nr, nc
            if (r, c) != (r0, c0):
                break
        self.target = (r, c)

    # -- the eight -------------------------------------------------------------------

    def substrate(self) -> str:
        return f"objects on a {GRID}x{GRID} grid; each holds row, col and colour"

    def environment(self) -> str:
        return "a board with a wall; the shaping medium is position under bounded movement"

    def actors(self) -> str:
        return f"the actions {ACTIONS}, which move ONE object and leave the rest untouched"

    def currency(self) -> str:
        return "prediction error in bits, per slot"

    def ground(self) -> str:
        return "exact match on the next state. Mechanical, instant, and it does not negotiate"

    def slots(self) -> list[str]:
        return sorted([*self.state, GOAL_SLOT])

    def atoms(self) -> list[Atom]:
        """THE TOY WORLD'S ATOMS, VERBATIM. See the module docstring: one variable moves."""
        return self.atom_set if self.atom_set is not None else _toy.Transitions().atoms()

    def actions(self) -> tuple[str, ...]:
        return ACTIONS

    def alphabet(self) -> int | dict[str, int]:
        """PER SLOT. Positions range over the grid, colours over four, the goal over 0..1 --
        three different sizes, so one number would charge a colour the grid's code."""
        a: dict[str, int] = {}
        for k in self.state:
            a[k] = 4 if k.endswith(".colour") else GRID
        a[GOAL_SLOT] = 2
        return a

    def slot_types(self) -> dict[str, str]:
        """EXTENT THROUGHOUT, AND IT IS A DELIBERATE UNDER-DECLARATION -- stated so no reader
        mistakes it for an oversight. `POSITION` and `COLOUR` are the honest types, and the
        reused atom set consumes `EXTENT`, so declaring them would type-starve every candidate
        and the world would read dead for a reason that has nothing to do with the habitat.
        Richer typing lands with grid-native atoms, together, or neither."""
        return dict.fromkeys(self.slots(), "EXTENT")

    def transform(self) -> Any:
        """No coarse view is defined here, so the bracket channel is inert. Stated, not omitted."""
        return None

    # -- running ---------------------------------------------------------------------

    def _blocked(self, r: int, c: int) -> bool:
        """Only the WALL blocks. Edges wrap -- see `_wrap`."""
        return (r % GRID, c % GRID) == (self.state["o2.row"], self.state["o2.col"])

    @staticmethod
    def _wrap(r: int, c: int) -> tuple[int, int]:
        """**POSITIONS WRAP, AND REAL ARC GRIDS DO NOT. Stated as a limit, not hidden.**

        The first version CLAMPED at the edges. **CLAMPING IS NOT MODULAR ARITHMETIC**, so no
        chain of `inc`/`dec` can express it; a wrapped step IS `inc`/`dec` mod the slot's
        alphabet, exactly.

        **AND I FIRST WROTE THIS UP ON A FALSE PREMISE -- that the atoms bake in `world.M = 7`
        and therefore could not speak about a 5-wide grid at all.** They do not: `_value_of`
        normalises every prediction `% self.alphabet[slot]`, so `dec(0)` reads as 4 on a
        5-alphabet slot. **The conclusion survived and the reasoning did not**, which is worth
        the two lines because the false version is the more persuasive one.

        **A WORLD THE AGENT'S VOCABULARY CANNOT EXPRESS PRODUCES AN UNINTERPRETABLE NULL** --
        *the mechanism is broken* and *the agent has no words for this place* read identically.
        That is the panel precondition, and it is the reason for the wrap rather than
        convenience: `inc` and `dec` mod GRID express a wrapped step EXACTLY, so movement
        becomes sayable and what remains unexplained is the WALL and the PUSH, which are the
        parts worth discovering.

        **THE HONEST COST: a real ARC board has edges and this one has none.** An agent that
        learns *position wraps* has learned something false about ARC. It is a habitat for
        exercising mechanisms, never a benchmark, and this is the sharpest way it differs.
        """
        return r % GRID, c % GRID

    def _completed(self) -> int:
        """ONE SITE. `objective()` and the published `@goal.completed` slot are one quantity,
        and computing it twice is the `A6i` collision this repo keeps filing."""
        return int((self.state["o0.row"], self.state["o0.col"]) == self.target)

    def objective(self) -> tuple[str, float]:
        return "BECOME(o0, target)", float(self._completed())

    def observe(self) -> dict[str, int]:
        """DERIVED, NEVER STORED -- no rule can write the goal; the agent only perceives it."""
        return {**self.state, GOAL_SLOT: self._completed()}

    def step(self, action: str) -> None:
        if action not in ACTIONS:
            raise ValueError(f"unknown action: {action}")
        dr, dc = _DELTA[action]
        r0, c0 = self.state["o0.row"], self.state["o0.col"]
        r1, c1 = self.state["o1.row"], self.state["o1.col"]
        nr0, nc0 = self._wrap(r0 + dr, c0 + dc)
        nr1, nc1 = self._wrap(r1 + dr, c1 + dc)

        # THE PUSH IS RESOLVED BEFORE THE MOVE, because o1's rule reads o0's OLD cell. Resolving
        # it after would make the mover's new position the cause of its own push.
        if (nr0, nc0) == (r1, c1) and not self._blocked(r1 + dr, c1 + dc):
            self.state["o1.row"], self.state["o1.col"] = nr1, nc1
            r1, c1 = nr1, nc1

        if not self._blocked(r0 + dr, c0 + dc) and (nr0, nc0) != (r1, c1):
            self.state["o0.row"], self.state["o0.col"] = nr0, nc0
            r0, c0 = nr0, nc0

        # CONTACT PAINTS. Adjacent after the move -> o1 takes o0's colour. One of the most
        # common ARC mechanics, and it makes an ATTRIBUTE conditionally action-bearing where
        # every attribute was previously a pure spectator.
        #
        # **o0.colour AND ALL THREE o2 SLOTS STAY UNREACHABLE BY ANY ACTION**, deliberately:
        # the spectator property is what `F356`/`F359` need, and enriching the world until
        # nothing is a spectator would destroy the thing it was built to exhibit.
        if abs(r0 - self.state["o1.row"]) + abs(c0 - self.state["o1.col"]) == 1:
            self.state["o1.colour"] = self.state["o0.colour"]


def boards(n: int, start: int = 0) -> list[GridWorld]:
    """MANY BOARDS, so nothing can be overfitted to one. Seeds are consecutive and the caller's;
    a finding read on one board is a finding about that board until it is read on the rest."""
    return [GridWorld(seed=s) for s in range(start, start + n)]
