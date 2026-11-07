"""ROAD CLOSED (the reviewer 2026-11-07 r1379; TETHER_HYP_ROAD_CLOSED): a budget ending is never a
verdict. Forcing fixtures on a gridworld agent with a held goal hypothesis planted (gridworld's own
runs hold none), each with the arm ON and its MUST-FAIL with the arm OFF.

check_park     a hypothesis parked by "no_route" with steps 1: on the _untested shelf, not in
               _hyp_tried, not barred; its goal_hypothesis_end row says why "parked", by
               "no_route" and its read count
check_stepped  (ii) one with steps 2 that ends "untested" by "elsewhere": shelved, not barred.
               MUST-FAIL, run: arm OFF, it is in _hyp_tried and barred
check_leave    (iii) a reopened rate-left one that ends "untested": its ("leave", ("hyp", kind))
               paid is unchanged. MUST-FAIL, run: arm OFF, paid + 1

    python tests/test_road_closed.py [check ...]
"""
from __future__ import annotations

import collections
import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def _agent():
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    for _ in range(2):
        ag.step()
    return ag


def _plant(ag, steps: int = 0, reopened=None, no_route: int = 0) -> dict:
    sl = sorted(ag.slots)[0]
    ag._hyp = {"key": "k", "text": f"{sl} == 1", "slots": [sl], "tkey": ("x == 1", sl, None),
               "cond": None, "source": "library", "shelf": None, "steps": steps, "r0": 1.0,
               "budget": 3, "born": ag.cycle, "displaced": {}, "reads": {}, "seg": {},
               "touches": 0, "losses": 0, "held_unreadable": 0, "acted": collections.Counter(),
               "out0": {sl: 0.0}, "reopened": reopened, "no_route": no_route}
    return ag._hyp


def _ends(ag) -> list:
    return [r["detail"] for r in ag.led.rows() if r["event"] == "goal_hypothesis_end"]


def _armed(on: bool, fn):
    keep = tether._HYP_ROAD_CLOSED
    tether._HYP_ROAD_CLOSED = on
    try:
        return fn()
    finally:
        tether._HYP_ROAD_CLOSED = keep


def check_park() -> None:
    def run():
        ag = _agent()
        h = _plant(ag, steps=1, no_route=2)
        ag._hyp_end("parked", by="no_route")
        return ag, h
    ag, h = _armed(True, run)
    end = _ends(ag)[-1]
    assert h["tkey"] in ag._untested and h["tkey"] not in ag._hyp_tried, ag._hyp_tried
    assert not ag._hyp_barred(h["tkey"])
    assert (end["why"], end["by"], end.get("no_route_reads")) == ("parked", "no_route", 2), end
    print("  parked at steps 1: shelved, not barred; the row says parked by no_route, 2 reads")


def check_stepped() -> None:
    def run():
        ag = _agent()
        h = _plant(ag, steps=2)
        ag._hyp_end("untested", by="elsewhere")
        return ag, h
    ag, h = _armed(True, run)
    assert h["tkey"] in ag._untested and not ag._hyp_barred(h["tkey"]), ag._hyp_tried
    off, h_off = _armed(False, run)
    assert h_off["tkey"] in off._hyp_tried and off._hyp_barred(h_off["tkey"]), "MF: not barred"
    print("  steps 2, untested by elsewhere: ON shelved and offerable; MF, OFF: barred")


def check_leave() -> None:
    def run():
        ag = _agent()
        h = _plant(ag, steps=0, reopened=ag.cycle)
        kind = ag._kind_key(h["slots"][0])
        before = ag._rf_standing("leave", ("hyp", kind))["paid"]
        ag._hyp_end("untested", by="elsewhere")
        return before, ag._rf_standing("leave", ("hyp", kind))["paid"]
    assert tether._LEAVE_RATE, "precondition: TETHER_LEAVE_RATE on (the leave is booked under it)"
    b, a = _armed(True, run)
    assert a == b, (b, a)
    ob, oa = _armed(False, run)
    assert oa == ob + 1, ("MF: the leave was not booked with the arm off", ob, oa)
    print(f"  reopened, ended untested: ON leave paid {b} -> {a}; MF, OFF: {ob} -> {oa}")


def main() -> int:
    want = set(sys.argv[1:])
    for c in (check_park, check_stepped, check_leave):
        if not want or c.__name__ in want:
            c()
            print("ok  ", c.__name__)
    print("test_road_closed OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
