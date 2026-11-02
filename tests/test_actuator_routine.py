"""I/J, ACTUATOR_ROUTINE (the reviewer 2026-11-01 r750 2), on the fake world: an open actuator goal
is committed as a routine (a "routine" row, verdict "actuator", Until(@actuator, TOUCH it)), the
held-routine branch presses it (by "routine"), and its END writes a routine_end row with its reason
and commits the next actuator; with the arm OFF no actuator routine is committed (the must-fail).

    python tests/test_actuator_routine.py
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
    assert tether._ACTUATOR_ROUTINE, "the arm is ON by default"
    env, ag = _run(10)
    rt = [r for r in ag.led.rows() if r["event"] == "routine"
          and (r.get("detail") or {}).get("verdict") == "actuator"]
    assert rt, "occasions: no actuator routine committed on the fixture"
    first = rt[0]["slot"]
    assert "@actuator:" + first in rt[0]["detail"]["routine"], rt[0]["detail"]["routine"]
    pressed = [r for r in ag.led.rows() if r["event"] == "repeat"
               and (r.get("detail") or {}).get("by") == "routine"]
    assert pressed, "the held-routine branch pressed the actuator (by routine)"
    held = ag._act_rt
    assert held is not None and ag.routine_for == held, (held, ag.routine_for)
    ag.iface.last_changed = ()                      # the next reading: its press changed nothing
    ag._routine_acts += 1
    ag._actuator_routine(env.observe())
    ends = [r for r in ag.led.rows() if r["event"] == "routine_end" and r["slot"] == held]
    assert ends and ends[-1]["detail"]["outcome"] == "arrived_no_clear" \
        and ends[-1]["detail"].get("why") == "no change", ends[-1:]
    assert held in ag._act_refuted and ag._act_rt != held, (ag._act_rt, held)
    tether._ACTUATOR_ROUTINE = False
    try:
        _e, ag2 = _run(10)
    finally:
        tether._ACTUATOR_ROUTINE = True
    off = [r for r in ag2.led.rows() if r["event"] == "routine"
           and (r.get("detail") or {}).get("verdict") == "actuator"]
    assert not off, ("must-fail: actuator routines with the arm OFF", len(off))
    print(f"test_actuator_routine: {first} committed as {rt[0]['detail']['routine']}; pressed by "
          f"routine {len(pressed)}x; its END wrote routine_end arrived_no_clear (no change); none "
          f"with the arm OFF")


if __name__ == "__main__":
    main()
