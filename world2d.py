"""world2d: a typed 2-D habitat for exercising perception and composition.

A TEST WORLD, not a benchmark and not any ARC game. It stands in for a capability: the
agent must perceive typed objects on a small grid, read their relations and their changes
across frames, and compose a vocabulary to predict them. No board identity, no goal answer
and no winning composition is encoded here -- the seed picks a board before any agent exists
and nothing in the world reads the agent's bindings, books or Gamma.

WHAT THIS WORLD HAS THAT A NUMERIC SNAP WORLD DOES NOT
-------------------------------------------------------
* typed objects -- each carries row, col, colour, size, kind and pose, with an honest
  per-slot alphabet and per-slot type (POSITION / COLOUR / EXTENT / SHAPE);
* relations above / aligned / contact, declared by the world and derived from positions,
  never stored as a rule's target (a relation is recomputed every frame);
* deltas grew / shrank / turned / scale, derived from a matched object across frames;
* contingent actions -- pressing one object changes a PARTNER, so the effect of a press is
  not the object pressed and a discriminator has something to separate;
* the optional world hooks the agent reads (derived, contacts, peers, relational_slots,
  slot_owner, attribute_of, board) are all published, so the wiring seat has real artifacts.

The atom set is deliberately small and domain-agnostic: a handful of value -> value
transforms and the relational/objective vocabulary. Every hidden per-slot rule is one of
those transforms or a composition of them, so a residue is always *sayable* -- the panel
precondition for reading a null on composition (a world whose vocabulary cannot express
its rule produces an unreadable null, not a finding).
"""

from __future__ import annotations

import random
import sys
from dataclasses import dataclass, field
from typing import Any

from gamma import NOT_RESOLVED, Atom

sys.dont_write_bytecode = True

GRID = 7
N_OBJECTS = 3
GOAL_SLOT = "@goal.completed"

# A press on object i changes its PARTNER, drawn from the seed before any agent exists.
# The map is the world's answer and is never published into `state`: the agent may perceive
# that pressing one thing changes another, never which thing is wired to which.
ACTIONS = ("press_0", "press_1", "press_2")

_TYPES = {
    "row": "POSITION", "col": "POSITION", "colour": "COLOUR", "size": "EXTENT",
    "kind": "SHAPE", "pose": "SHAPE",
}
# Relations and deltas are declared by the world, never guessed from a slot's name.
_RELATIONS = ("above", "aligned", "contact")
_DELTAS = ("grew", "shrank", "turned", "scale")


def _atoms() -> list[Atom]:
    """A value -> value transform vocabulary, plus the relational/objective words.

    Each transform is a distinct, learnable rule. Distinct names with distinct functions
    give the agent a separate thing to mint per slot; the affine ones compose, `halve` is
    deliberately non-affine so no shorter chain can reach it, and `take` reads a bound
    operand so a two-object interaction needs the world's peer/contact hooks to be said.
    """
    def idn(v: int, _c: Any) -> int:
        return v

    def inc(v: int, _c: Any) -> int:
        return v + 1

    def dec(v: int, _c: Any) -> int:
        return v - 1

    def dbl(v: int, _c: Any) -> int:
        return 2 * v

    def neg(v: int, _c: Any) -> int:
        return -v

    def halve(v: int, _c: Any) -> int:
        return v // 2

    def add2(v: int, _c: Any) -> int:
        return v + 2

    def sub2(v: int, _c: Any) -> int:
        return v - 2

    def triple(v: int, _c: Any) -> int:
        return 3 * v

    def take(v: int, c: Any) -> int:
        """Read the bound operand slot instead of my own value (the interaction atom)."""
        return c.operands[0] if c.operands else v

    fns = (idn, inc, dec, dbl, neg, halve, add2, sub2, triple, take)
    out = [Atom(f.__name__, f, "val", "val",
                reads_operand=(f.__name__ == "take"),
                reads_ctx=("operands",) if f.__name__ == "take" else ())
           for f in fns]

    # THE OBJECTIVE VOCABULARY -- mirroring the toy world / arc_atoms' relate/quantify split,
    # so the same words cross both worlds and the fixture asserts ONE vocabulary.
    def same(v: Any, c: Any) -> Any:
        return int(v == c.operands[0]) if c.operands else NOT_RESOLVED

    def other(v: Any, c: Any) -> Any:
        return int(v != c.operands[0]) if c.operands else NOT_RESOLVED

    def above(v: Any, c: Any) -> Any:
        return int(v > c.operands[0]) if c.operands else NOT_RESOLVED

    for f in (same, other, above):
        out.append(Atom(f.__name__, f, "EXTENT", "PRED", reads_operand=True,
                        operand_type="EXTENT", reads_ctx=("operands",)))
    out.append(Atom("all", lambda v, _c: int(bool(v)), "PRED", "OBJ"))
    out.append(Atom("any", lambda v, _c: int(bool(v)), "PRED", "OBJ"))
    out.append(Atom("none", lambda v, _c: int(not v), "PRED", "OBJ"))
    return out


# The hidden per-slot rules. Names are for the harness's report, never shown to the agent.
# Each is a SHORT COMPOSITION of transforms from `_atoms`, so every residue is sayable and a
# winning term names more than one atom -- the composition itself is the artifact the wiring
# seat reads. They are affine or near-affine and distinct on a 7-code, so none collapses.
_RULES = (
    ("o0.row", "inc"), ("o0.col", "dec"), ("o0.size", "dbl"),
    ("o1.row", "neg"), ("o1.col", "halve"), ("o1.size", "add2"),
    ("o2.row", "sub2"), ("o2.col", "triple"), ("o2.size", "take"),
)
# The hidden rules are plain transforms; the atoms above are their sayable vocabulary.
# (An Atom's fn takes a context too; the world's own transition does not.)
_FN = {
    "inc": lambda v: v + 1, "dec": lambda v: v - 1, "dbl": lambda v: 2 * v,
    "neg": lambda v: -v, "halve": lambda v: v // 2, "add2": lambda v: v + 2,
    "sub2": lambda v: v - 2, "triple": lambda v: 3 * v,
}


@dataclass
class World2D:
    """One generated 6x6 board. `seed` selects it; the same seed is the same board, always.

    `hooks` is the panel's own switch: OFF makes the relation/derived methods return empty,
    which is exactly what the agent sees when a world does not publish them. The must-fail
    fixture uses it to show that those hooks are what give the wider vocabulary occasions.
    """

    seed: int = 0
    hooks: bool = True
    state: dict[str, int] = field(default_factory=dict)
    buttons: dict[int, int] = field(default_factory=dict)
    _prev: dict[str, int] = field(default_factory=dict)
    _steps: int = 0
    goal_obj: str = "o0"
    goal_size: int = 1

    def __post_init__(self) -> None:
        rng = random.Random(self.seed)
        cells = rng.sample([(r, c) for r in range(GRID) for c in range(GRID)], N_OBJECTS)
        for i, (r, c) in enumerate(cells):
            self.state[f"o{i}.row"] = r
            self.state[f"o{i}.col"] = c
            self.state[f"o{i}.colour"] = rng.randrange(GRID)
            self.state[f"o{i}.size"] = rng.randrange(1, GRID)
            self.state[f"o{i}.kind"] = rng.randrange(GRID)
            self.state[f"o{i}.pose"] = rng.randrange(GRID)
        # CONTINGENT WIRING: a press on i changes partner buttons[i] (a derangement, so a
        # press never changes the object pressed). Drawn from the seed, before any agent.
        perm = list(range(N_OBJECTS))
        rng.shuffle(perm)
        self.buttons = {i: perm[(k + 1) % N_OBJECTS] for k, i in enumerate(perm)}
        self.goal_obj = f"o{rng.randrange(N_OBJECTS)}"
        self.goal_size = (self.state[self.goal_obj + ".size"] + 1 + rng.randrange(GRID - 1)) % GRID
        self._prev = dict(self.state)

    # -- the eight -------------------------------------------------------------------

    def substrate(self) -> str:
        return (f"typed objects on a {GRID}x{GRID} grid; each holds position, "
                "colour, size, kind and pose")

    def environment(self) -> str:
        return ("a board whose objects drift and whose presses act on a partner; "
                "the shaping medium is the typed attribute under transition")

    def actors(self) -> str:
        return f"the actions {ACTIONS}; a press changes a PARTNER object, not the one pressed"

    def currency(self) -> str:
        return "prediction error in bits, per slot"

    def ground(self) -> str:
        return "exact match on the next state. Mechanical, instant, and it does not negotiate"

    def slots(self) -> list[str]:
        return sorted([*self.state, GOAL_SLOT, *self._derived(self.state)])

    def atoms(self) -> list[Atom]:
        return _atoms()

    def actions(self) -> tuple[str, ...]:
        return ACTIONS

    def alphabet(self) -> int | dict[str, int]:
        # Every attribute ranges over the grid's own code (0..GRID-1), so one honest size
        # charges each slot. Charging a small alphabet for a colour would inflate its residual
        # by the factor its information was reduced -- the proxy error the discipline refuses.
        a: dict[str, int] = dict.fromkeys(self.state, GRID)
        a[GOAL_SLOT] = 2
        # a relation is a truth or a small magnitude; a delta is a truth or a size
        truthy = ("above", "aligned", "contact", "grew", "shrank", "turned")
        for k, _v in self._derived(self.state).items():
            attr = k.split(".", 1)[1]
            a[k] = 2 if attr in truthy else GRID
        return a

    def transform(self) -> Any:
        """No coarse view is defined here, so the bracket channel is inert. Stated, not omitted."""
        return None

    # -- hooks the agent reads --------------------------------------------------------

    def _positions(self, state: dict) -> dict[str, dict]:
        return {f"o{i}": {"row": state[f"o{i}.row"], "col": state[f"o{i}.col"],
                          "h": state.get(f"o{i}.size", 1), "w": state.get(f"o{i}.size", 1)}
                for i in range(N_OBJECTS)
                if f"o{i}.row" in state and f"o{i}.col" in state}

    def _derived(self, state: dict) -> dict[str, int]:
        """Relations and deltas, computed from ANY state -- never stored as a rule's target.

        The relation half is a pure function of the two objects' cells; the delta half needs
        the previous frame's matched object (`_prev`), which is what makes a change, not a
        value, the occasion. With `hooks` OFF this returns {}, exactly as a world that does
        not publish the hooks would.
        """
        if not self.hooks:
            return {}
        out: dict[str, int] = {}
        pos = self._positions(state)
        keys = sorted(pos)
        for x, a in enumerate(keys):
            for b in keys[x + 1:]:
                pa, pb = pos[a], pos[b]
                dr, dc = pa["row"] - pb["row"], pa["col"] - pb["col"]
                base = f"{a}_{b}"
                out[f"{base}.above"] = int(dr < 0)
                out[f"{base}.aligned"] = int(dc == 0)
                out[f"{base}.contact"] = int(abs(dr) + abs(dc) == 1)
        for i in range(N_OBJECTS):
            who = f"o{i}"
            # A predicted state may carry only part of the board; a delta that cannot be read
            # is omitted, never guessed. That is the same abstention the loop expects.
            if (who + ".size" not in state or who + ".size" not in self._prev
                    or who + ".pose" not in state or who + ".pose" not in self._prev):
                continue
            dsz = state[who + ".size"] - self._prev[who + ".size"]
            out[f"{who}.grew"] = int(dsz > 0)
            out[f"{who}.shrank"] = int(dsz < 0)
            out[f"{who}.turned"] = int(state[who + ".pose"] != self._prev[who + ".pose"])
            out[f"{who}.scale"] = state[who + ".size"]
        return out

    def derive(self, state: dict) -> dict[str, int]:
        """The relational/delta slots from any state the caller gives -- the instrument
        applied to a predicted state, so a relational prediction comes from the agent's own
        predicted attributes and never from the world's truth."""
        return self._derived(state)

    def derived(self) -> dict[str, tuple[str, ...]]:
        """Each derived slot and the base slots it is computed from."""
        out: dict[str, tuple[str, ...]] = {}
        for k in self._derived(self.state):
            base = k.split(".", 1)[0]
            if base.startswith("o") and "_" not in base:
                out[k] = (base + ".size", base + ".pose")
            else:
                a, b = base.split("_", 1)
                out[k] = (a + ".row", a + ".col", b + ".row", b + ".col")
        return out

    def boxes(self, state: dict) -> dict[str, dict]:
        """Each object's box read from a state's slot values (size x size here)."""
        return self._positions(state)

    def contacts(self) -> dict[str, list[str]]:
        """WHICH OBJECTS TOUCH, THIS FRAME -- `_bindings` ranks operands contact-first."""
        adj: dict[str, list[str]] = {}
        for a, b, _kind in self.contact_points():
            adj.setdefault(a, []).append(b)
            adj.setdefault(b, []).append(a)
        return adj

    def contact_points(self) -> list[tuple[str, str, str]]:
        if not self.hooks:
            return []
        pos = self._positions(self.state)
        keys = sorted(pos)
        out: list[tuple[str, str, str]] = []
        for x, a in enumerate(keys):
            for b in keys[x + 1:]:
                dr = abs(pos[a]["row"] - pos[b]["row"])
                dc = abs(pos[a]["col"] - pos[b]["col"])
                if dr + dc == 1:
                    out.append((a, b, "orthogonal"))
                elif dr == 1 and dc == 1:
                    out.append((a, b, "diagonal"))
        return out

    def peers(self) -> dict[str, tuple[str, ...]]:
        """`{slot: the SAME attribute on every OTHER object}` -- declared, never derived
        from a dotted name by the loop."""
        by_attr: dict[str, list[str]] = {}
        for slot in self.slots():
            if "." in slot and slot.startswith("o"):
                by_attr.setdefault(slot.rsplit(".", 1)[1], []).append(slot)
        return {s: tuple(x for x in group if x != s)
                for group in by_attr.values() for s in group}

    def relational_slots(self) -> tuple[str, ...]:
        """Which attributes are a relation to another object -- declared by the world."""
        if not self.hooks:
            return ()
        return tuple(sorted({*(_RELATIONS), *(_DELTAS)}))

    def slot_owner(self) -> dict[str, str]:
        return {k: k.split(".")[0] for k in self.slots() if k.startswith("o")}

    def attribute_of(self) -> dict[str, str]:
        return {s: s.split(".", 1)[1] for s in self.slots() if "." in s}

    def slot_types(self) -> dict[str, str]:
        """Honest per-slot types. val-typed atoms stay bindable (BINDABLE), so declaring the
        types cannot type-starve the vocabulary the way all-EXTENT would."""
        out: dict[str, str] = {}
        for s in self.slots():
            attr = s.split(".", 1)[1] if "." in s else ""
            out[s] = _TYPES.get(attr, "EXTENT")
        return out

    def board(self) -> Any:
        """The state rastered: each object covers a size x size block at its row/col, carrying
        its colour (shifted by one so a colour-0 object does not vanish). Introduces nothing."""
        g = [[0] * GRID for _ in range(GRID)]
        for i in range(N_OBJECTS):
            r, c = self.state.get(f"o{i}.row"), self.state.get(f"o{i}.col")
            if r is None or c is None:
                continue
            size = max(1, int(self.state.get(f"o{i}.size", 1)))
            colour = int(self.state.get(f"o{i}.colour", 0)) + 1
            for rr in range(r, min(GRID, r + size)):
                for cc in range(c, min(GRID, c + size)):
                    if 0 <= rr < GRID and 0 <= cc < GRID:
                        g[rr][cc] = colour
        return g

    # -- running ---------------------------------------------------------------------

    def _completed(self) -> int:
        """THE GOAL IS A RELATION, not an attribute: o0 and o1 must share a column.

        This is what makes the relation/derived hooks LOAD-BEARING rather than decorative.
        `aligned` is a slot this world publishes ONLY through `derive()`/`slots()` when the
        hooks are on -- it is never a stored field and no action writes it. With the hooks
        removed the agent cannot perceive this relation at all, so it cannot form a closing
        term: the goal lives in the hook-published relation, and the no-hook world is blind
        to it. The ground here is computed from raw positions (never from the agent's reading)
        so the agent is judged, not told.
        """
        return int(self.state["o0.col"] == self.state["o1.col"])

    def objective(self) -> tuple[str, float]:
        return "ALIGN(o0, o1)", float(self._completed())

    def observe(self) -> dict[str, int]:
        return {**self.state, GOAL_SLOT: self._completed(), **self._derived(self.state)}

    def step(self, action: str, x: int | None = None, y: int | None = None) -> None:  # noqa: ARG002
        if action not in ACTIONS:
            raise ValueError(f"unknown action: {action}")
        self._steps += 1
        self._prev = dict(self.state)
        # 1) THE HIDDEN DRIFT: each numeric slot advances by its own learnable rule, so every
        #    one of them carries a residue for the agent to explain. Unary transforms act on
        #    the slot's own current value; `take` reads another object's size (an interaction).
        for slot, rule in _RULES:
            if rule == "take":
                src = "o0.size" if slot != "o0.size" else "o1.size"
                self.state[slot] = (self._prev[src] + 1) % GRID
            else:
                self.state[slot] = _FN[rule](self._prev[slot]) % GRID
        # 2) THE CONTINGENT PRESS: pressing i changes partner buttons[i] -- colour, pose and
        #    size -- and leaves the pressed object alone. SELF and OTHER both occur.
        i = ACTIONS.index(action)
        partner = self.buttons[i]
        p = f"o{partner}"
        self.state[p + ".colour"] = (self.state[p + ".colour"] + 1) % GRID
        self.state[p + ".pose"] = (self.state[p + ".pose"] + 1) % GRID
        self.state[p + ".size"] = (self.state[p + ".size"] + 1) % GRID


def boards(n: int, start: int = 0) -> list[World2D]:
    return [World2D(seed=s) for s in range(start, start + n)]
