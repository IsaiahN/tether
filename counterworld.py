"""counterworld: a typed 2-D habitat whose numeric goal advances only on the Nth press.

A TEST WORLD, not a benchmark and not any ARC game. It stands in for one capability: the
agent must discover a CAUSE over a numeric slot from its own trace -- "this slot changed
after I pressed that action n times since it last changed" -- which is exactly the
`TETHER_INFERRED_CAUSE` mechanism (interface cause inference: a COUNT of presses since the
slot changed, or a LATCH). That mechanism is built, default ON, but has never had a world
where the changing slot and the count share a TYPE: on latchworld the slot was BOOL and the
cause candidates were type-refused ("above does not accept POSITION"). Here the goal slot
is EXTENT/val, so a count cause can bind.

WHY A NEW WORLD, not a gridworld family: the four gridworld families each put the goal on a
position or a one-press colour; none requires a count-conditioned numeric change. A standalone
world (the world2d pattern) keeps all four byte-identical.

THE MECHANIC (drawn from the seed before any agent exists, never published as a rule):
Three objects, three `press_i` actions. One action is the COUNTER (hidden), one period N in
2..4 (hidden). Each press of the counter increments a per-action count it can see in its own
trace; on the Nth such press since the goal last changed, the goal object's SIZE advances by
one and that count resets. Other presses advance distractor colours. The goal is
`BECOME(oG.size, target)`, reachable by repeating the counter press N times per advance.
No press changes the goal on any other cadence, so a cause with the wrong n or the wrong action
is refuted by the ground. The world reads nothing from the agent.

VOCABULARY: `world2d._atoms()` verbatim (inc/dec/dbl/... are val->val), so the only variable
against world2d is the habitat, not the atom set.
"""

from __future__ import annotations

import random
import sys
from dataclasses import dataclass, field
from typing import Any

from gamma import Atom
from world2d import _atoms

sys.dont_write_bytecode = True

GRID = 6
N_OBJECTS = 3
GOAL_SLOT = "@goal.completed"
ACTIONS = ("press_0", "press_1", "press_2")


@dataclass
class CounterWorld:
    """One generated board. `seed` selects it. `wired=False` is the control: the goal is
    advanced by pressing the goal object directly, with no count condition.
    """

    seed: int = 0
    wired: bool = True
    state: dict[str, int] = field(default_factory=dict)
    counter: int = 0
    period: int = 3
    goal: int = 0
    _presses: dict[int, int] = field(default_factory=dict)
    _steps: int = 0

    def __post_init__(self) -> None:
        rng = random.Random(self.seed)
        cells = rng.sample([(r, c) for r in range(GRID) for c in range(GRID)], N_OBJECTS)
        for i, (r, c) in enumerate(cells):
            self.state[f"o{i}.row"] = r
            self.state[f"o{i}.col"] = c
            self.state[f"o{i}.colour"] = rng.randrange(4)
            self.state[f"o{i}.size"] = rng.randrange(1, GRID)
        # hidden wiring, drawn before any agent
        self.counter = rng.randrange(N_OBJECTS)
        self.period = 2 + rng.randrange(3)          # 2..4
        self.goal = rng.randrange(N_OBJECTS)
        start = self.state[f"o{self.goal}.size"]
        self.state["@goal.target"] = (start + 1 + rng.randrange(GRID - 1)) % GRID
        self._presses = dict.fromkeys(range(N_OBJECTS), 0)

    # -- contract ------------------------------------------------------------------

    def substrate(self) -> str:
        return f"typed objects on a {GRID}x{GRID} grid; a size advances on the Nth press"

    def environment(self) -> str:
        return "a board where one numeric slot responds to a count of presses, not a single one"

    def actors(self) -> str:
        return f"the actions {ACTIONS}; one counts toward the goal, the rest distract"

    def currency(self) -> str:
        return "prediction error in bits, per slot"

    def ground(self) -> str:
        return "exact match on the goal size. Mechanical, instant, it does not negotiate"

    def slots(self) -> list[str]:
        return sorted([*self.state, GOAL_SLOT])

    def atoms(self) -> list[Atom]:
        return _atoms()

    def transform(self) -> Any:
        return None

    def actions(self) -> tuple[str, ...]:
        return ACTIONS

    def alphabet(self) -> int | dict[str, int]:
        a: dict[str, int] = {}
        for k in self.state:
            if k.startswith("@goal"):
                a[k] = GRID
            elif k.endswith(".colour"):
                a[k] = 4
            else:
                a[k] = GRID
        a[GOAL_SLOT] = 2
        return a

    def relational_slots(self) -> tuple[str, ...]:
        return ()

    def slot_owner(self) -> dict[str, str]:
        return {k: k.split(".", 1)[0] for k in self.slots() if k.startswith("o")}

    def attribute_of(self) -> dict[str, str]:
        return {s: s.split(".", 1)[1] for s in self.slots() if "." in s}

    def slot_types(self) -> dict[str, str]:
        out: dict[str, str] = {}
        for s in self.slots():
            attr = s.split(".", 1)[1] if "." in s else ""
            out[s] = ("POSITION" if attr in ("row", "col") else
                      "COLOUR" if attr == "colour" else "EXTENT")
        out[GOAL_SLOT] = "BOOL"
        return out

    def board(self) -> Any:
        g = [[0] * GRID for _ in range(GRID)]
        for i in range(N_OBJECTS):
            r, c = self.state.get(f"o{i}.row"), self.state.get(f"o{i}.col")
            if r is not None and c is not None and 0 <= r < GRID and 0 <= c < GRID:
                g[r][c] = int(self.state.get(f"o{i}.colour", 0)) + 1
        return g

    def derive(self, state: dict) -> dict[str, int]:  # noqa: ARG002
        return {}

    def derived(self) -> dict[str, tuple[str, ...]]:
        return {}

    def boxes(self, state: dict) -> dict[str, dict]:
        return {f"o{i}": {"row": state[f"o{i}.row"], "col": state[f"o{i}.col"],
                          "h": state.get(f"o{i}.size", 1), "w": state.get(f"o{i}.size", 1)}
                for i in range(N_OBJECTS) if f"o{i}.row" in state}

    def contacts(self) -> dict[str, list[str]]:
        adj: dict[str, list[str]] = {}
        for a, b, _kind in self.contact_points():
            adj.setdefault(a, []).append(b)
            adj.setdefault(b, []).append(a)
        return adj

    def contact_points(self) -> list[tuple[str, str, str]]:
        out: list[tuple[str, str, str]] = []
        objs = [f"o{i}" for i in range(N_OBJECTS)]
        for x, a in enumerate(objs):
            for b in objs[x + 1:]:
                dr = abs(self.state[a + ".row"] - self.state[b + ".row"])
                dc = abs(self.state[a + ".col"] - self.state[b + ".col"])
                if dr + dc == 1:
                    out.append((a, b, "orthogonal"))
                elif dr == 1 and dc == 1:
                    out.append((a, b, "diagonal"))
        return out

    def peers(self) -> dict[str, tuple[str, ...]]:
        by_attr: dict[str, list[str]] = {}
        for slot in self.slots():
            if "." in slot and slot.startswith("o"):
                by_attr.setdefault(slot.rsplit(".", 1)[1], []).append(slot)
        return {s: tuple(x for x in group if x != s)
                for group in by_attr.values() for s in group}

    # -- running -------------------------------------------------------------------

    def _completed(self) -> int:
        return int(self.state[f"o{self.goal}.size"] == self.state["@goal.target"])

    def objective(self) -> tuple[str, float]:
        return f"BECOME(o{self.goal}.size, {self.state['@goal.target']})", float(self._completed())

    def observe(self) -> dict[str, int]:
        return {**self.state, GOAL_SLOT: self._completed()}

    def step(self, action: str, x: int | None = None, y: int | None = None) -> None:  # noqa: ARG002
        if action not in ACTIONS:
            raise ValueError(f"unknown action: {action}")
        self._steps += 1
        i = ACTIONS.index(action)
        if not self.wired:
            # control: pressing the goal advances it directly
            if i == self.goal:
                self.state[f"o{self.goal}.size"] = (self.state[f"o{self.goal}.size"] + 1) % GRID
            return
        if i == self.counter:
            self._presses[i] += 1
            if self._presses[i] >= self.period:
                self.state[f"o{self.goal}.size"] = (self.state[f"o{self.goal}.size"] + 1) % GRID
                self._presses[i] = 0
            return
        # distractor: a non-counter press advances a distractor's colour and never the goal
        distractor = (i + 1) % N_OBJECTS
        self.state[f"o{distractor}.colour"] = (self.state[f"o{distractor}.colour"] + 1) % 4


def boards(n: int, start: int = 0, wired: bool = True) -> list[CounterWorld]:
    return [CounterWorld(seed=s, wired=wired) for s in range(start, start + n)]
