"""C6 DOORS (the reviewer 2026-11-10 r1638, r1640; Isaiah 11-06 answer 7), arm TETHER_DOORS.

  D1  a parked guess is set aside "not reachable right now" with its pick-up condition; MF: while
      its subject slot stands still and no effect is new, it stays set aside
  D2  it is picked back up when a subject slot moves, or when a new effect is known: its parked
      count is cleared, with a row naming which
  D3  the change pattern: a period is read only after two full cycles (MF: not after one), and a
      door that never changes is no rotation
  D4  OFF: a set-aside guess is never picked back up

    python tests/test_doors.py
"""
from __future__ import annotations

import os
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

TKEY = ("o0.col > 2",)


def _agent() -> tether.Agent:
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="doors"), tether.Config(),
                      ledger.Ledger())
    ag.step()
    return ag


def _rows(ag: tether.Agent, ev: str) -> list:
    return [r["detail"] for r in ag.led.rows() if r["event"] == ev]


def _aside(ag: tether.Agent) -> dict:
    last = ag.trace[-1][2]
    ag._parked_n[TKEY] = 1
    ag._door_set_aside({"tkey": TKEY, "slots": ["o0.col"], "text": "o0.col > 2"})
    return dict(last)


def check_d1_d2() -> None:
    ag = _agent()
    state = _aside(ag)
    d = _rows(ag, "door_set_aside")[-1]
    assert d["verdict"] == "not reachable right now" and d["pick_up_when"]["slots"], d
    ag._door_pick_up(state)
    assert TKEY in ag._door_aside and ag._parked_n[TKEY] == 1, "MF: picked up with nothing new"
    moved = dict(state, **{"o0.col": state["o0.col"] + 1})
    ag._door_pick_up(moved)
    up = _rows(ag, "door_picked_up")
    assert up and up[-1]["by"] == "a subject slot moved" and TKEY not in ag._parked_n, up
    ag2 = _agent()
    state2 = _aside(ag2)
    ag2._kn_eff[-1] = frozenset({"?.zz+"})          # a form the agent did not know
    ag2._door_pick_up(state2)
    assert _rows(ag2, "door_picked_up")[-1]["by"] == "a new effect is known"
    print("  D1-D2: set aside 'not reachable right now'; held while nothing changes; picked back "
          "up by a moved slot, and by a new effect")


def check_d3() -> None:
    ag = _agent()
    lk = ag._lk()
    for e in ["probe", "goal", "probe"]:
        ag._door_pattern(lk, e)
    assert not _rows(ag, "door_pattern"), "MF: a pattern read inside two cycles"
    ag._door_pattern(lk, "goal")
    d = _rows(ag, "door_pattern")[-1]
    assert d["period"] == 2 and d["predicted"] == "probe", d
    ag2 = _agent()
    for e in ["goal"] * 6:
        ag2._door_pattern(ag2._lk(), e)
    assert not _rows(ag2, "door_pattern"), "a door that never changes read as a rotation"
    print("  D3: probe, goal, probe: no pattern; a second goal completes two cycles: period 2, "
          "next probe; goal x6 is no rotation")


def check_d4() -> None:
    keep, tether._DOORS = tether._DOORS, False
    try:
        ag = _agent()
        _aside(ag)
        ag._door_aside[TKEY]["forms"] = -1          # would fire on any pass
        for _ in range(3):
            ag.step()
    finally:
        tether._DOORS = keep
    assert not _rows(ag, "door_picked_up") and TKEY in ag._door_aside, "OFF: picked up"
    on = _agent()
    _aside(on)
    on._door_aside[TKEY]["forms"] = -1
    for _ in range(3):
        on.step()
    assert _rows(on, "door_picked_up"), "occasion: no proposal pass ON"
    print("  D4: OFF, a set-aside guess stays aside; ON the same guess is picked back up")


if __name__ == "__main__":
    for c in (check_d1_d2, check_d3, check_d4):
        c()
    print("doors: OK")
