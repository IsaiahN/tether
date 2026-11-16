"""HTN RETURN (TETHER_HTN_RETURN, default ON; Isaiah 2026-11-16 "fix HTN"; T0c r1971: the repair
subtask ends without helping the parent). A refused parent's repair subtask that ARRIVES re-adopts
the parent.
  H1  refusal -> push (when="refused"): the return is registered; the edge leaves _htn_pending
  H2  the subtask arrives with an empty stack: the parent is held again (source "htn_return"),
      htn_return row resumed True, a goal_hypotheses row (G2), the parent's tkey out of _hyp_tried
  H3  the returned parent refused again: htn_not_prerequisite row, the subtask joins _htn_tried
  H4  the returned parent's end credits its edge (paid = won)
  H5  a subtask that ends "gone": nothing returns (resumed False), no hold
  MF-H1 TETHER_HTN_RETURN=0 -> the parent is not held again -> RED as required
  H6  gridworld 12 steps ON and OFF both pass the gate
Seconds.
    python tests/test_htn_return.py
"""
from __future__ import annotations

import os
import sys
from collections import Counter

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gate  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

P, S = "o1.col", "o2.row"


def agent():
    env = world.bind(gridworld.family("default", 0))
    led = ledger.Ledger()
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
    ag.step()
    return ag, led


def hold(ag):
    ag._hyp = {"key": ("k",), "text": "o1.col == o2.col", "slots": [P], "tkey": ("t",),
               "cond": None, "source": "library", "shelf": None, "steps": 3, "r0": 1.0,
               "budget": 5, "born": ag.cycle, "displaced": {}, "reads": {}, "seg": {},
               "touches": 2, "losses": 0, "held_unreadable": 0, "acted": Counter()}


def fake_push(ag):
    """_htn_push's effect on the stack, without the board: one subtask S for the parent."""
    def push(chosen, when="routes", why=None):  # noqa: ARG001  _htn_push's signature
        edge = ag._htn_edge(chosen, S)
        ag._tasks.append({"parent": chosen, "sub": S, "edge": edge})
        ag._subgoal = {"parent": chosen, "sub": S}
        ag._htn_pending.setdefault(chosen, set()).add(edge)
        return True
    ag._htn_push = push


def refuse(ag, **kw):
    fake_push(ag)
    hold(ag)
    ag._hyp_end("arrived_no_clear", loss=True, **kw)


def ev(led, n0, name):
    return [r for r in led.rows()[n0:] if r.get("event") == name]


def main() -> int:
    assert tether._HTN_RETURN is True, "the arm defaults ON"
    ag, led = agent()
    ag._res.setdefault(P, [1, 1])
    ag._res.setdefault(S, [1, 1])
    refuse(ag)
    assert P in ag._htn_return and ag._htn_return[P]["sub"] == S, ag._htn_return
    assert not ag._htn_pending.get(P), ("H1: the edge is still pending", ag._htn_pending)
    assert ag._hyp is None and ("t",) in ag._hyp_tried, "the refusal ended the hold"
    print("H1 refusal -> push: return registered, edge not pending: GREEN")

    n0 = len(led.rows())
    ag._subgoal_end("arrived")
    assert ag._hyp is not None and ag._hyp["source"] == "htn_return", ("H2", ag._hyp)
    assert ("t",) not in ag._hyp_tried, "H2: the parent is still tried"
    rr = ev(led, n0, "htn_return")
    gh = ev(led, n0, "goal_hypotheses")
    assert rr and rr[0]["detail"]["resumed"] is True and gh and \
        gh[0]["detail"]["source"] == "htn_return", (rr, gh)
    print("H2 the subtask arrives: the parent is held again, htn_return + goal_hypotheses "
          "rows: GREEN")

    n0 = len(led.rows())
    edge = ag._hyp["htn_edge"]
    ag._hyp_end("arrived_no_clear", loss=True)    # the returned parent refused again
    cr = [r for r in ev(led, n0, "htn_credit") if r["detail"]["edge"] == edge]
    assert cr and cr[0]["detail"]["paid"] is False, ("H4", cr)
    print("H4 the returned parent's end credits its edge unpaid (no win): GREEN")
    # its own repair ran in that end: the earlier subtask is dropped before the push
    np = ev(led, n0, "htn_not_prerequisite")
    assert np and np[0]["detail"]["subs"] == [S] and S in ag._htn_tried.get(P, set()), (np,)
    print("H3 refused again after a return: htn_not_prerequisite, the subtask joins tried: GREEN")

    ag2, led2 = agent()
    ag2._res.setdefault(P, [1, 1])
    refuse(ag2)
    n0 = len(led2.rows())
    ag2._subgoal_end("gone")
    rr = ev(led2, n0, "htn_return")
    assert ag2._hyp is None and rr and rr[0]["detail"]["resumed"] is False, ("H5", rr)
    print("H5 a subtask gone: resumed False, no hold: GREEN")

    tether._HTN_RETURN = False
    ag3, _led3 = agent()
    ag3._res.setdefault(P, [1, 1])
    refuse(ag3)
    ag3._subgoal_end("arrived")
    tether._HTN_RETURN = True
    assert ag3._hyp is None, "MF-H1 should not return with the arm OFF"
    print("MF-H1 the arm OFF: the parent is not held again -> RED (as required)")

    for on in (True, False):
        tether._HTN_RETURN = on
        env = world.bind(gridworld.family("default", 0))
        led4 = ledger.Ledger()
        ag4 = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                           led4)
        for _ in range(12):
            ag4.step()
        ag4.end_run("cap")
        v = gate.check(led4.rows())["verdict"]
        assert v == "pass", ("H6: the gate refused", on, v)
    tether._HTN_RETURN = True
    print("H6 gridworld 12 steps ON and OFF: both pass the gate: GREEN")
    print("htn_return: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
