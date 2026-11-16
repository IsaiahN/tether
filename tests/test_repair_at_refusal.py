"""REPAIR AT THE REFUSAL (TETHER_REPAIR_AT_REFUSAL, default ON; the reviewer r1957; T0 2026-11-14:
refused, not repaired). A goal hypothesis that ends at contact without a win is decomposed there.
  R1  arrived_no_clear: _htn_push is asked with when="refused", a repair_at_refusal row (pushed
      True) and the agenda's "Three texts before acting" row are written
  R2  stalled with touches > 0 -> repaired; stalled with 0 touches -> not (never reached its test)
  R3  a win, a boundary close, and a non-PLAN step -> no repair
  R4  nothing to push: repair_at_refusal row with pushed False, the agenda row says "narrow"
  R5  _contact_candidates: the open goal slots of objects touching the goal's object, not its own,
      not far ones; _htn_push(when="refused") offers them after the law and tier 2
  MF-R1 TETHER_REPAIR_AT_REFUSAL=0 -> no push asked, no repair row -> RED as required
  R6  gridworld 12 steps ON and OFF both pass the gate
Seconds.
    python tests/test_repair_at_refusal.py
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


def agent():
    env = world.bind(gridworld.family("default", 0))
    led = ledger.Ledger()
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
    ag.step()
    return ag, led


def hold(ag, touches=2):
    ag._hyp = {"key": ("k",), "text": "o1.col == o2.col", "slots": ["o1.col"], "tkey": ("t",),
               "cond": None, "source": "library", "shelf": None, "steps": 3, "r0": 1.0,
               "budget": 5, "born": ag.cycle, "displaced": {}, "reads": {}, "seg": {},
               "touches": touches, "losses": 0, "held_unreadable": 0, "acted": Counter()}


def ended(ag, led, why, push_ok=True, touches=2, **kw):
    calls = []
    ag._htn_push = lambda s, when="routes", why=None: calls.append((s, when, why)) or push_ok
    n0 = len(led.rows())
    hold(ag, touches)
    ag._hyp_end(why, **kw)
    rows = led.rows()[n0:]
    rep = [r for r in rows if r.get("event") == "repair_at_refusal"]
    ags = [r for r in rows if r.get("event") == "agenda"
           and r["detail"].get("card") == "Three texts before acting"]
    return calls, rep, ags


def main() -> int:
    assert tether._REPAIR_AT_REFUSAL is True, "the arm defaults ON"
    ag, led = agent()
    calls, rep, ags = ended(ag, led, "arrived_no_clear", loss=True)
    assert calls == [("o1.col", "refused", "arrived_no_clear")], calls
    assert rep and rep[0]["detail"]["pushed"] is True, rep
    assert ags and "subgoal" in ags[0]["detail"]["answer"], ags
    print("R1 arrived_no_clear: pushed when='refused', repair row, Three texts row: GREEN")

    calls, rep, _a = ended(ag, led, "stalled", touches=3)
    assert calls and rep, ("R2: stalled at contact not repaired", calls)
    calls, rep, _a = ended(ag, led, "stalled", touches=0)
    assert not calls and not rep, ("R2: a stall that never touched was repaired", calls)
    print("R2 stalled with touches repaired, without touches not: GREEN")

    for why, kw in (("arrived_no_clear", {"won": True}), ("arrived_no_clear", {"boundary": True}),
                    ("arrived_no_clear", {"step": "ROUTE", "loss": True})):
        calls, rep, _a = ended(ag, led, why, **kw)
        assert not calls and not rep, ("R3", kw, calls)
    print("R3 a win, a boundary close and a non-PLAN step: no repair: GREEN")

    calls, rep, ags = ended(ag, led, "arrived_no_clear", push_ok=False, loss=True)
    assert rep and rep[0]["detail"]["pushed"] is False and "narrow" in ags[0]["detail"]["answer"]
    print("R4 nothing to push: pushed False, the agenda says narrow: GREEN")

    ag2, _led2 = agent()
    boxes = {"o1": {"row": 2, "col": 2, "h": 1, "w": 1}, "o2": {"row": 2, "col": 3, "h": 1, "w": 1},
             "o3": {"row": 9, "col": 9, "h": 1, "w": 1}}
    ag2.env.boxes = lambda _state: boxes
    ag2._res = {"o1.col": [2, 2], "o2.row": [1, 1], "o3.row": [1, 1]}
    got = [s for s, _ln in ag2._contact_candidates("o1.col")]
    assert got == ["o2.row"], ("R5: contact candidates", got)
    print(f"R5 contact candidates: {got} (o2 touches o1; o3 far; o1's own left out): GREEN")

    tether._REPAIR_AT_REFUSAL = False
    ag3, led3 = agent()
    calls, rep, _a = ended(ag3, led3, "arrived_no_clear", loss=True)
    tether._REPAIR_AT_REFUSAL = True
    assert not calls and not rep, ("MF-R1 should not repair with the arm OFF", calls)
    print("MF-R1 the arm OFF: no push, no repair row -> RED (as required)")

    for on in (True, False):
        tether._REPAIR_AT_REFUSAL = on
        env = world.bind(gridworld.family("default", 0))
        led4 = ledger.Ledger()
        ag4 = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                           led4)
        for _ in range(12):
            ag4.step()
        ag4.end_run("cap")
        v = gate.check(led4.rows())["verdict"]
        assert v == "pass", ("R6: the gate refused", on, v)
    tether._REPAIR_AT_REFUSAL = True
    print("R6 gridworld 12 steps ON and OFF: both pass the gate: GREEN")
    print("repair_at_refusal: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
