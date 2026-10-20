"""GQ3, ONE ARRIVAL PREDICATE (TETHER_ARRIVAL; the reviewer 2026-10-20 14:27 CDT). Each reader of a
goal series is fed the same synthetic series on a gridworld agent after one real step, each arm in
its own process (the flag resolves at import):
  TOUCH = [3, 2, 0] (one reading at zero), CONFIRM = [3, 0, 0] (MIN_REPEAT readings at zero).
  ON:  every reader reads TOUCH as touched (never done / met / holds / refused / selected) and
       CONFIRM as confirmed.
  MUST-FAIL OFF: today's readers take TOUCH as met somewhere (the selector picks it, the gate
       refuses it "already holds", the guard is DONE, the row says satisfied, ...), so the ON
       assertions fail on the OFF results.

    python test_arrival.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
tree = sys.argv[1]
sys.path = [tree] + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")]
import gamma, gridworld, ledger, routine as Rt, tether, world

TOUCH, CONFIRM = [3.0, 2.0, 0.0], [3.0, 0.0, 0.0]
env = world.bind(gridworld.family("default", 0))
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="arrival"), tether.Config(), ledger.Ledger())
ag.step()
before = env.observe()
S = next(s for s in sorted(before) if "." in s and not s.startswith("@"))
out = {"arm": tether._ARRIVAL}

def rows(event, slot=S):
    return [r for r in ag.led.rows() if r.get("event") == event and r.get("slot") == slot]

for name, ser in (("touch", TOUCH), ("confirm", CONFIRM)):
    res = {}
    # 1 the selector
    ag._res = {S: list(ser)}
    why = {}
    res["choice"] = ag._goal_choice(why=why)
    res["choice_tally"] = {k: why.get(k, 0) for k in ("arrived", "touched", "qualified")}
    # 2 the mint gate
    keep = (ag._goal_choice, ag._discrepancy, ag.goal_residual)
    ag._goal_choice = lambda *a, **k: S
    ag._discrepancy = lambda *a, **k: 1
    ag.goal_residual = lambda *a, **k: 0.0
    ag._res = {S: list(ser)}
    n0 = len(ag.led.rows())
    ag._mint_routine(before)
    last = [r for r in ag.led.rows()[n0:] if r.get("slot") == S]
    res["gate"] = [(r["event"], r["detail"].get("reason")) for r in last]
    # 4 the routine guard, at PLAN (the series' last is this reading) and at SETTLE (appended)
    ag._res = {S: list(ser)}
    res["guard_plan"] = repr(ag._holds(before)(S))
    ag._res = {S: list(ser[:-1])}
    res["guard_settle"] = repr(ag._holds(before, "SETTLE")(S))
    ag._res = {S: list(ser)}
    emit, rest = Rt.advance(Rt.Until(S, Rt.Act("x"), 3), ag._holds(before))
    res["until"] = emit
    ag._goal_choice, ag._discrepancy, ag.goal_residual = keep
    # 5 + 6 the goal_series row, goal_undone / goal_touch_lost: the series so far, then one
    # more reading; then a reopening reading
    ag.goal_residual = lambda *a, **k: ser[-1]
    ag._res = {S: list(ser[:-1])}
    n0 = len(ag.led.rows())
    ag.note_goals(before)
    gs = [r["detail"] for r in ag.led.rows()[n0:] if r.get("event") == "goal_series"][-1]
    res["series_satisfied"] = S in gs.get("satisfied", ())
    res["series_touched"] = S in gs.get("touched", ())
    res["series_qualifies"] = S in gs.get("qualifies", ())
    ag.goal_residual = lambda *a, **k: 2.0
    ag._res = {S: list(ser)}
    n0 = len(ag.led.rows())
    ag.note_goals(before)
    new = [r for r in ag.led.rows()[n0:] if r.get("slot") == S]
    res["undone"] = sum(1 for r in new if r["event"] == "goal_undone")
    res["touch_lost"] = sum(1 for r in new if r["event"] == "goal_touch_lost")
    del ag.goal_residual
    # 7 G1 met / unmet
    ag.wants[S] = "w"
    ag._g1 = {S: {"want": "w", "met": 0, "unmet": 0}}
    ag._res = {S: list(ser)}
    trace, ag.trace = ag.trace, []
    ag._g1_wants()
    ag.trace = trace
    res["g1"] = {k: v for k, v in ag._g1[S].items() if k in ("met", "unmet", "touched")}
    ag.wants.pop(S, None)
    # 8 _note_decision
    class W:
        def says(self):
            return "SAY"
    ag._undone = {("c", "SAY", S, 0.0): 2}
    ag._res = {S: list(ser)}
    n0 = len(ag.led.rows())
    ag._note_decision(W())
    res["decision"] = sum(1 for r in ag.led.rows()[n0:] if r.get("event") == "decision")
    # 3 _goal_target: the subject at its target
    class T:
        out_type = tether.OBJ_TYPE
    keep = (ag._objective_of, ag._applies, ag._ops, ag._eval_ctx, ag._value_of)
    ag._objective_of = lambda s: ("t", T())
    ag._applies = lambda *a, **k: True
    ag._ops = lambda *a, **k: ()
    ag._eval_ctx = lambda *a, **k: None
    ag._value_of = lambda term, s, b, c: b[s]
    res["goal_target"] = (ag._goal_target(S, before), ag._gt_which)
    (ag._objective_of, ag._applies, ag._ops, ag._eval_ctx, ag._value_of) = keep
    out[name] = res

# 9 can(): a zero in the slot's discrepancy history, not now, nothing bound
keep = ag._discrepancy
ag._discrepancy = lambda *a, **k: 2
ag._disc = {S: [3, 0, 2]}
ag.bound.pop(S, None)
out["can_past_zero"] = ag.can(S, before)
ag._discrepancy = keep
out["arrival_fn"] = ([tether.arrival(x) for x in (TOUCH, CONFIRM, [1.0], [], [0.0])]
                     if hasattr(tether, "arrival") else None)
print(json.dumps(out, default=str))
'''


def _run(arm: str) -> dict:
    here = os.path.dirname(os.path.abspath(__file__))
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", TETHER_ARRIVAL=arm, TETHER_AGENT_SEED="0")
    out = subprocess.run([sys.executable, "-c", PROBE, here], env=env, capture_output=True,
                         text=True, timeout=600)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def _on_holds(r: dict) -> list[str]:
    """Every ON assertion; returns the failures (empty = all hold)."""
    bad = []
    t, c = r["touch"], r["confirm"]

    def chk(ok, what):
        if not ok:
            bad.append(what)
    chk(r["arrival_fn"] == ["touched", "confirmed", "open", "open", "touched"], "arrival()")
    chk(t["choice"] is None and t["choice_tally"]["touched"] == 1
        and t["choice_tally"]["arrived"] == 0, "1 selector: touch not selected, not arrived")
    chk(c["choice"] is None and c["choice_tally"]["arrived"] == 1, "1 selector: confirm arrived")
    chk([e for e, _ in t["gate"]] == ["routine_recheck"], "2 gate: touch re-checked, not refused")
    chk(c["gate"] and c["gate"][-1][0] == "routine_refused" and "ARRIVED" in str(c["gate"][-1][1]),
        "2 gate: confirm refused as arrived")
    chk(t["goal_target"][1] == "subject_met", "3 _goal_target: subject_met, not already_holds")
    chk(t["guard_plan"] == "'touch'" and t["guard_settle"] == "'touch'", "4 guard: touch -> TOUCH")
    chk(c["guard_plan"] == "True" and c["guard_settle"] == "True", "4 guard: confirm holds")
    chk(t["until"] == "hold" and c["until"] == "done", "4 Until: HOLD on touch, DONE on confirm")
    chk(not t["series_satisfied"] and t["series_touched"] and not t["series_qualifies"],
        "5 goal_series: touch listed touched, not satisfied, not qualifies")
    chk(c["series_satisfied"], "5 goal_series: confirm satisfied")
    chk(t["undone"] == 0 and t["touch_lost"] == 1, "6 a reopened touch is touch_lost, not undone")
    chk(c["undone"] == 1, "6 a reopened confirm is undone")
    chk(t["g1"].get("met", 0) == 0 and t["g1"].get("touched", 0) == 1, "7 G1: touch not met")
    chk(c["g1"].get("met", 0) == 1, "7 G1: confirm met")
    chk(t["decision"] == 0 and c["decision"] == 1, "8 _note_decision: confirmed only")
    chk(r["can_past_zero"] != "yes", "9 can(): a past zero is not YES")
    return bad


def main() -> None:
    on, off = _run("1"), _run("0")
    assert on["arm"] is True and off["arm"] is False, (on["arm"], off["arm"])
    bad_on = _on_holds(on)
    assert not bad_on, f"ON: {bad_on}\n{json.dumps(on, indent=1)}"
    off["arrival_fn"] = on["arrival_fn"]       # the function exists either way; judge the readers
    bad_off = _on_holds(off)
    assert len(bad_off) >= 8, f"MUST-FAIL OFF: only {bad_off} failed\n{json.dumps(off, indent=1)}"
    print(f"test_arrival: pass (ON: all 9 readers, touched vs confirmed; MUST-FAIL OFF: "
          f"{len(bad_off)} assertions fail -- {bad_off})")


if __name__ == "__main__":
    main()
