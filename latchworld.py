"""latchworld: a typed 2-D habitat whose goal needs a TWO-STEP causal chain.

A TEST WORLD, not a benchmark and not any ARC game. It stands in for one capability:
the agent must perceive that one press ARMS a latch and a second, different press FIRES it,
then plan the two-press sequence -- the `Until`/`Seq` metaprogram algebra and the
`TETHER_INFERRED_CAUSE` count/latch mechanism are built but have never had a world that
requires them. No board identity, no goal answer and no winning composition is encoded here:
the wiring is drawn from the caller's seed before any agent exists and nothing in the world
reads the agent's bindings, books or Gamma.

WHY A NEW WORLD AND NOT A NEW FAMILY IN `gridworld.py`
------------------------------------------------------
`gridworld`'s four families are all single-condition (one position, one colour, one remote
colour, one mapping swap). Each already has a one-press route to its goal. A two-step goal
needs a different action/outcome structure, and adding it to `GridWorld` would fork `step` and
`_assert_reachable` for every family. A standalone habitat (the `world2d` pattern) keeps all
four existing families byte-identical and keeps the new mechanic in one readable file.

THE MECHANIC (drawn from the seed, never published as a rule)
-------------------------------------------------------------
Three objects; three actions (`press_0/1/2`). One object is the GOAL `g`, one is the ARM
button `a`, one is the FIRE button `f`, a permutation drawn before any agent exists.
  - press(a): sets the published `latch.armed` slot to 1. Nothing else moves.
  - press(f) while armed: advances g.colour by one and clears armed to 0.
  - any other press: advances a DISTRACTOR object's colour, and does not move g.
So the ONLY way to advance the goal is the sequence [press(a), press(f)]. A single press,
repeated, never moves the goal -- the refuter is structural, not a threshold. Achieving a
target colour needs that pair one or more times. The pair is reachable by construction.

The latch state is PUBLISHED (`latch.armed`), so the causal chain is perceivable: the agent
can see press(a) change armed, then press(f) change the goal. A world that hid the latch
would produce an unreadable null (Fig 11 :48 -- what you cannot perceive is the residual).

VOCABULARY: `world2d._atoms()` is reused verbatim, so the only variable against `world2d` is
the habitat. A term that composes in one composes in the other; the wiring seat can read a
residual as a difference in contact, never in the atom set.
"""

from __future__ import annotations

import random
import sys
from dataclasses import dataclass, field
from typing import Any

from gamma import Atom
from world2d import _atoms  # one vocabulary, deliberately -- see module docstring

sys.dont_write_bytecode = True

GRID = 6
N_OBJECTS = 3
GOAL_SLOT = "@goal.completed"
ARMED_SLOT = "latch.armed"
ACTIONS = ("press_0", "press_1", "press_2")


@dataclass
class LatchWorld:
    """One generated board. `seed` selects it; the same seed is the same board, always.

    `wired` is the panel's switch: OFF makes the two-step chain degenerate -- every press
    advances its OWN object's colour and the goal object is directly reachable. That is the
    control arm: the must-fail fixture uses it to show that the two-step structure, not the
    colour alphabet or the actions, is what makes the single-press policy fail.
    """

    seed: int = 0
    wired: bool = True
    state: dict[str, int] = field(default_factory=dict)
    arm: int = 0
    fire: int = 1
    goal: int = 2
    _steps: int = 0

    def __post_init__(self) -> None:
        rng = random.Random(self.seed)
        cells = rng.sample([(r, c) for r in range(GRID) for c in range(GRID)], N_OBJECTS)
        for i, (r, c) in enumerate(cells):
            self.state[f"o{i}.row"] = r
            self.state[f"o{i}.col"] = c
            self.state[f"o{i}.colour"] = rng.randrange(4)
            self.state[f"o{i}.size"] = rng.randrange(1, GRID)
        # The wiring: arm, fire and goal are a permutation of the objects, drawn here, before
        # any agent. It is NOT published into `state` -- the agent may perceive colours and
        # the latch changing, never which press is arm and which is fire.
        perm = list(range(N_OBJECTS))
        rng.shuffle(perm)
        self.arm, self.fire, self.goal = perm
        self.state[ARMED_SLOT] = 0
        target = (self.state[f"o{self.goal}.colour"] + 1 + rng.randrange(3)) % 4
        self.state["@goal.target"] = target
        self._target = target

    # -- the eight contract methods -------------------------------------------------

    def substrate(self) -> str:
        return (f"typed objects on a {GRID}x{GRID} grid; a press changes an object, "
                "and one press arms a latch that another press fires")

    def environment(self) -> str:
        return "a board whose goal advances only through a two-press causal chain"

    def actors(self) -> str:
        return f"the actions {ACTIONS}; one arms, one fires when armed, the rest distract"

    def currency(self) -> str:
        return "prediction error in bits, per slot"

    def ground(self) -> str:
        return "exact match on the goal colour. Mechanical, instant, it does not negotiate"

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
            if k == ARMED_SLOT or k.startswith("@goal"):
                a[k] = 2 if k == ARMED_SLOT else 4
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
            out[s] = "POSITION" if attr in ("row", "col") else (
                "COLOUR" if attr == "colour" else "EXTENT")
        out[ARMED_SLOT] = "BOOL"
        out[GOAL_SLOT] = "BOOL"
        return out

    def board(self) -> Any:
        g = [[0] * GRID for _ in range(GRID)]
        for i in range(N_OBJECTS):
            r, c = self.state.get(f"o{i}.row"), self.state.get(f"o{i}.col")
            if r is None or c is None:
                continue
            if 0 <= r < GRID and 0 <= c < GRID:
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

    # -- running --------------------------------------------------------------------

    def _completed(self) -> int:
        return int(self.state[f"o{self.goal}.colour"] == self._target)

    def objective(self) -> tuple[str, float]:
        return f"BECOME(o{self.goal}.colour, {self._target})", float(self._completed())

    def observe(self) -> dict[str, int]:
        return {**self.state, GOAL_SLOT: self._completed()}

    def step(self, action: str, x: int | None = None, y: int | None = None) -> None:  # noqa: ARG002
        if action not in ACTIONS:
            raise ValueError(f"unknown action: {action}")
        self._steps += 1
        i = ACTIONS.index(action)
        if not self.wired:
            # CONTROL ARM: the goal is directly reachable by pressing it. No latch.
            self.state[f"o{i}.colour"] = (self.state[f"o{i}.colour"] + 1) % 4
            return
        goal_key = f"o{self.goal}.colour"
        if i == self.arm:
            # ARMS: only the latch changes. The agent can perceive exactly this one effect.
            self.state[ARMED_SLOT] = 1
            return
        if i == self.fire and self.state[ARMED_SLOT] == 1:
            # FIRES: the ONLY transition that moves the goal, and it needs the arm first.
            self.state[goal_key] = (self.state[goal_key] + 1) % 4
            self.state[ARMED_SLOT] = 0
            return
        # DISTRACTOR: a single press always changes something, so the residual is real, but
        # no single press (or repetition of one) ever moves the goal. The distractor is the
        # ARM object, which is a different object from the goal by construction (the three
        # are a permutation) -- using (i+1)%N here would sometimes BE the goal and break the
        # refuter, which is exactly the kind of off-by-one this check exists to catch.
        self.state[ARMED_SLOT] = 0
        self.state[f"o{self.arm}.colour"] = (self.state[f"o{self.arm}.colour"] + 1) % 4


def boards(n: int, start: int = 0, wired: bool = True) -> list[LatchWorld]:
    return [LatchWorld(seed=s, wired=wired) for s in range(start, start + n)]
