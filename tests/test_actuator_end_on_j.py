"""J END, ACTUATOR_END_ON_J (the reviewer 2026-11-02 r759), on the fake world.

  (a) an actuator routine that J ends exhausted refutes that actuator (an actuator_goal_end row
      naming the end), and it is not re-committed; with the arm OFF it is re-committed at once (the
      must-fail, KS1's tu93 loop);
  (b) with every actuator refuted, the next cycle commits nothing and the step still runs through
      choose to a press: no hang and no empty commit;
  (c) a routine committed before a level edge and ending after it refutes nothing (its row says
      "after a boundary"); the same end on the board it was committed on refutes (r761).

    python tests/test_actuator_end_on_j.py
"""
from __future__ import annotations

import os
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")


def _held(steps: int = 14):
    import arc_holdout
    from test_entry import FakeWrapper
    env, ag, _led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
    for _ in range(steps):
        ag.step()
        if ag._act_rt is not None and ag.routine_for == ag._act_rt:
            break       # the first held actuator routine is the moment read below (P2'
                        # HYP_OWN_PRESS reaches it a cycle earlier than a fixed count)
    assert ag._act_rt is not None and ag.routine_for == ag._act_rt, \
        ("occasions: no actuator routine held on the fixture", ag._act_rt, ag.routine_for)
    return env, ag


def _exhaust(env, ag) -> str:
    import routine as Rt
    held = ag._act_rt
    ag._end_routine(Rt.EXHAUSTED, env.observe(), "SETTLE")
    ag._actuator_routine(env.observe())
    return held


def main():
    import tether
    assert tether._ACTUATOR_END_ON_J, "the arm is ON by default"
    env, ag = _held()
    held = _exhaust(env, ag)
    rows = [r for r in ag.led.rows() if r["event"] == "actuator_goal_end" and r["slot"] == held]
    assert rows and rows[-1]["detail"]["why"] == "routine exhausted", rows[-1:]
    assert held in ag._act_refuted and ag._act_rt != held, ("(a) not re-committed", ag._act_rt)
    tether._ACTUATOR_END_ON_J = False
    try:
        env2, ag2 = _held()
        held2 = _exhaust(env2, ag2)
        assert ag2._act_rt == held2, ("must-fail: OFF re-commits it", ag2._act_rt, held2)
    finally:
        tether._ACTUATOR_END_ON_J = True
    # (c) a routine committed before a level edge and ending after it refutes nothing (r761); the
    # control, the same end on the board it was committed on, refutes: the epoch is what blocks it
    import routine as Rt
    env3, ag3 = _held()
    held3, n0 = ag3._act_rt, ag3.iface.board_n
    ag3.retarget(env3, ag3.level, how=tether.NEW_BOARD)
    if ag3.iface.board_n == n0:
        ag3.iface.board_n += 1                 # the fixture's edge, where retarget did not move it
    ag3.routine, ag3.routine_for = ag3.routine or Rt.Act(None), held3   # it survives the edge
    ag3._end_routine(Rt.EXHAUSTED, env3.observe(), "SETTLE")
    late = [r for r in ag3.led.rows() if r["event"] == "actuator_goal_end" and r["slot"] == held3]
    assert not ag3._act_refuted and late \
        and late[-1]["detail"]["why"].endswith("after a boundary"), \
        ("(c) an end after a boundary refutes nothing", ag3._act_refuted, late[-1:])
    ag3._act_commit = (held3, ag3.iface.board_n)    # control: committed on this board
    ag3.routine, ag3.routine_for = Rt.Act(None), held3
    ag3._end_routine(Rt.EXHAUSTED, env3.observe(), "SETTLE")
    assert held3 in ag3._act_refuted, "(c) control: on its own board the end refutes"
    # (b) every actuator refuted: nothing is committed and the step still presses
    ag._act_refuted = set(ag._actuators)
    if ag.routine_for in ag._act_refuted:
        ag.routine, ag.routine_for, ag._routine_adopted = None, None, None
    ag._act_rt = None
    ag._actuator_routine(env.observe())
    assert ag._act_rt is None and ag.routine is None, ("(b) no empty commit", ag._act_rt)
    n0 = len(ag.led.rows())
    ag.step()
    assert len(ag.led.rows()) > n0 and ag._last_action is not None, "(b) the step ran to a press"
    print(f"test_actuator_end_on_j: {held} exhausted -> refuted and not re-committed (OFF "
          f"re-commits {held2}); all {len(ag._actuators)} refuted -> no commit, the step pressed "
          f"{ag._last_action}")


if __name__ == "__main__":
    main()
