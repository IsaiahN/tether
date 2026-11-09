"""C2 FELT and G (the reviewer 2026-11-01 r742, r743): KIND_TOUCH_FELT and GOAL_BY_MOVED on the fake
world (it offers a positioned action, so a kind touch is realised there).

  KIND_TOUCH_FELT: in 10 steps at least one contact row of kind "kind-touch" is written, carrying
  the whole credited change (moved_n, owners_n); with the arm OFF none is (the must-fail).
  GOAL_BY_MOVED: the per-board set of slots the presses moved fills, and a new_board boundary
  clears it while a game loss does not.

    python tests/test_kind_touch_felt.py
"""
from __future__ import annotations

import os
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")


def _run(steps: int = 10):
    import arc_holdout
    from test_entry import FakeWrapper
    env, ag, _led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
    for _ in range(steps):
        ag.step()
    rows = [r for r in ag.led.rows() if r["event"] == "contact"
            and r["detail"].get("kind") == "kind-touch"]
    return env, ag, rows


def main():
    import tether
    assert tether._KIND_TOUCH_FELT and tether._GOAL_BY_MOVED, "both arms ON by default"
    env, ag, rows = _run()
    assert rows, "no kind-touch contact row in 10 steps"
    assert all("moved_n" in r["detail"] and "owners_n" in r["detail"] for r in rows), rows[:2]
    moved = set(ag._board_moved)
    assert moved, "GOAL_BY_MOVED: the presses moved nothing on the record"
    ag.retarget(env, ag.level, how="game_loss")
    assert ag._board_moved == moved, "a game loss is not a new board"
    ag.retarget(env, ag.level, how=tether.NEW_BOARD)
    assert not ag._board_moved, "a new board's moved set starts empty"
    tether._KIND_TOUCH_FELT = False
    try:
        _e, _a, off = _run()
    finally:
        tether._KIND_TOUCH_FELT = True
    assert not off, ("must-fail: kind-touch rows written with the arm OFF", len(off))
    print(f"test_kind_touch_felt: {len(rows)} kind-touch rows (moved_n "
          f"{[r['detail']['moved_n'] for r in rows]}), none with the arm OFF; {len(moved)} slots "
          f"moved on the board, kept at game loss, cleared at new_board")


if __name__ == "__main__":
    main()
