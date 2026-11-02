"""G, GOAL_FROM_ACTUATOR (the reviewer 2026-11-01 r746): a two-actuator board (the fake world: its
kind touches find two objects that move others).

  The actuator with the larger credited change is continued first, through a TOUCH of it; a press
  that yields no credited change refutes it (arrived without a clear) and the other actuator is
  continued next; an actuator whose whole effect is the per-press baseline (what every press of
  the board changed) is not continued; a new_board boundary clears the actuators and a death
  keeps them; with the arm OFF no press is chosen as "actuator" (the must-fail).

    python tests/test_goal_from_actuator.py
"""
from __future__ import annotations

import os
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")


def _run(steps: int):
    import arc_holdout
    from test_entry import FakeWrapper
    env, ag, _led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
    for _ in range(steps):
        ag.step()
    return env, ag


def main():
    import tether
    assert tether._GOAL_FROM_ACTUATOR, "the arm is ON by default"
    env, ag = _run(10)
    acts = ag._actuators
    assert len(acts) >= 2, ("occasions: fewer than two actuators on the fixture", acts)
    first, second = sorted(acts, key=lambda o: (-acts[o][0], acts[o][1], int(o[1:])))[:2]
    picks = [r["slot"] for r in ag.led.rows() if r["event"] == "actuator_goal"]
    assert picks and picks[0] == first, ("the stronger actuator is continued first", picks, acts)
    ag._act_pending = first
    ag.iface.last_changed = ()                      # the next read: the press changed nothing
    ag._actuator_press(env.observe())
    assert first in ag._act_refuted, "a press with no credited change refutes the actuator"
    assert ag._act_pending == second, ("the next actuator is continued", ag._act_pending, second)
    ag._act_refuted.discard(second)
    ag._press_every, ag._act_pending = set(acts[second][2]), None   # every press moved these
    ag._actuator_press(env.observe())
    assert ag._act_pending != second, "an actuator whose whole effect is the per-press baseline"
    ag._press_every = None
    ag.retarget(env, ag.level, how="death")
    assert ag._actuators and first in ag._act_refuted, "a death keeps the actuators"
    ag.retarget(env, ag.level, how=tether.NEW_BOARD)
    assert not ag._actuators and not ag._act_refuted, "a new board's actuators start empty"
    tether._GOAL_FROM_ACTUATOR = False
    try:
        _e, ag2 = _run(10)
    finally:
        tether._GOAL_FROM_ACTUATOR = True
    off = [r for r in ag2.led.rows() if r["event"] == "actuator_goal"]
    assert not off, ("must-fail: actuator goals with the arm OFF", len(off))
    print(f"test_goal_from_actuator: actuators {({o: v[:2] for o, v in acts.items()})}; {first} "
          f"continued first, refuted on no change, then {second}; none whose effect is the "
          f"per-press baseline; cleared at new_board, kept at death; none with the arm OFF")


if __name__ == "__main__":
    main()
