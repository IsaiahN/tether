"""7a(6) H2, the in-between frames (TETHER_CASCADE_AGENCY; R3 part 2; the reviewer 2026-10-10
22:14Z). A stub env whose cascade() returns hand-built frames (oldest first, the shape arc_world
hands over), read through _cascade_agency as a step reads it. o0 is controlled (its slot is
action-contingent); inside one action:

    sub-frame 0->1  o1 moves                    -> o1 changed before anything controlled: self-moved
    sub-frame 1->2  o0 moves, o3 moves          -> o3 moved with the controlled object: controlled
    sub-frame 2->3  o2 moves (touching o0), o4  -> o2 reacting; o4 later with no contact: no mode

  must-pass: the modes above, one cascade_modes row;
  1. a self-mover is never read as controlled (R3);
  2. one frame (every intermediate dropped) reads no order, never a mode (R3);
  3. arm OFF: a 3-step run on gridworld never reaches the H2 path and leaves Agency's new fields
     empty, so Agency reads as before (the reviewer 22:14Z).

    python test_cascade_agency.py
"""
from __future__ import annotations

import sys

import gamma
import gridworld
import ledger
import tether
import world

sys.dont_write_bytecode = True

BEFORE = {"o0": (1, 1), "o1": (3, 3), "o2": (1, 3), "o3": (4, 1), "o4": (0, 5)}
MOVES = [{"o1": (3, 4)}, {"o0": (1, 2), "o3": (4, 2)}, {"o2": (1, 4), "o4": (0, 4)}]


def _grid(pos: dict) -> list[list[int]]:
    g = [[0] * 6 for _ in range(5)]
    for i, (_o, (r, c)) in enumerate(sorted(pos.items())):
        g[r][c] = i + 1
    return g


class Stub:
    def __init__(self, frames):
        self.frames = frames

    def cascade(self):
        return self.frames

    def slot_owner(self):
        return {f"{o}.{a}": o for o in BEFORE for a in ("row", "col")}

    def attribute_of(self):
        return {f"{o}.{a}": a for o in BEFORE for a in ("row", "col")}

    def contacts(self):
        return {"o0": ["o2"], "o2": ["o0"]}


def _state(pos):
    return {f"{o}.{a}": v for o, (r, c) in pos.items() for a, v in (("row", r), ("col", c))}


def _agent(frames):
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="h2_fixture"), tether.Config(),
                      ledger.Ledger())
    after = {**BEFORE, **{k: v for m in MOVES for k, v in m.items()}}
    ag.env = Stub(frames)
    ag.trace = [(_state(BEFORE), "A", _state(after), None, None)]
    ag.agency.contingent = lambda: ["o0.row", "o0.col"]
    return ag


if __name__ == "__main__":
    pos, frames = dict(BEFORE), [_grid(BEFORE)]
    for m in MOVES:
        pos.update(m)
        frames.append(_grid(pos))
    ag = _agent(frames)
    ag._cascade_agency()
    rows = [r for r in ag.led.rows() if r["event"] == "cascade_modes"]
    modes = rows[0]["detail"]["modes"]
    assert len(rows) == 1 and modes == {"o1": tether.SELF_MOVED, "o3": tether.MOVES_WITH,
                                        "o2": tether.REACTING}, modes
    print(f"  must-pass: {modes}; o4 (later, no contact) has no mode")
    assert modes["o1"] != tether.MOVES_WITH and ag.agency.order[("o1", tether.SELF_MOVED)] == 1
    print("  1: the self-mover is read as self-moved, never as controlled")
    one = _agent([frames[-1]])
    one._cascade_agency()
    r1 = [r["detail"] for r in one.led.rows() if r["event"] == "cascade_modes"]
    assert r1[0]["modes"] is None and one.agency.no_order == 1 and not one.agency.order, r1
    print("  2: one frame reads no order and no mode")
    was = tether._CASCADE_AGENCY
    tether._CASCADE_AGENCY = False
    env = world.bind(gridworld.family("default", 0, 4))
    off = tether.Agent(env, gamma.Gamma(env.atoms(), game="h2_off"), tether.Config(),
                       ledger.Ledger())

    def _never():
        raise AssertionError("the H2 path ran with the arm OFF")
    off._cascade_agency = _never
    try:
        for _ in range(3):
            off.step()
    finally:
        tether._CASCADE_AGENCY = was
    assert not off.agency.order and off.agency.no_order == 0
    assert not [r for r in off.led.rows() if r["event"] == "cascade_modes"]
    print("  3: arm OFF, 3 steps: the H2 path never runs, Agency's new fields stay empty, no row")
    print("ok")
