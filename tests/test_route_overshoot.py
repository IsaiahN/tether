"""R-B'S OVERSHOOT MUST-FAIL, PRE-REGISTERED (the reviewer 2026-10-24 07:14, ruling 3), written
before any redesign so it cannot be fitted later. EXPECTED TO FAIL on cf749912 (R-B ON, as built),
whose "farther" refuses a route at once.
  THE RULE   on a DIRECTIONAL intent, a press that moves WITH the intent's sign and passes the
             target must NOT be refused at once.
  OCCASION   from a real row: round 4 of the 2026-10-23/24 play run, sb26, cycle 89 -- "BECOME
             o485.stability +", before 43, after 85, target 44, ACTION5 at the goal exit, graded
             "farther". The stub world replays its numbers: target = before + 1, each press +42.
  OCCASIONS  asserted: a goal-exit press graded "farther" that moved with the intent's sign, on
             sb26's receding target, so the case cannot pass by not happening.
  OFF        no route is ever refused (today's code): OFF passes trivially; the must-fail is ON.
    python tests/test_route_overshoot.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
tree = sys.argv[1]
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import arc_holdout, tether
import interface as IFace
from test_entry import FakeWrapper
env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
for _ in range(12):
    ag.step()
sl = sorted(s for s, t in ag.slot_types.items() if t in tether.ORDERED_TYPES)[0]
ag.slot_types[sl] = "POSITION"
ag._hyp = None
ag._goal_choice = lambda why=None, book=False: sl
ag._goal_target = lambda s, bf: bf[s] + 1        # sb26's receding target: one above the value
ag.iface.realise = (lambda want, offered, ctx, state=None, env=None,
                    withheld=IFace.NO_WITHHELD, cell=True:
                    IFace.Realisation(offered[0], why="probe: first offered") if offered else None)
IFace.Interface.context = staticmethod(lambda env, actor=None: (("probe", 1),))
ag._route_refused, ag._route_run, ag._test = {}, {}, None
k0 = len([r for r in ag.led.rows() if r["event"] == "route_refused"])
value, presses = 43, []
for _ in range(2):                         # sb26 cycles 89 and 90: 43 -> 85, then 85 -> 127
    before = {sl: value}
    act = ag._goal_split(before)
    intent = ag._test["intent"] if ag._test else None
    target = ag._test["target"] if ag._test else None
    after = value + 42
    ag.trace.append((act, before, {sl: after}))
    ag._audit_at = ag.cycle
    n = len(ag.led.rows())
    ag._test_row()
    oc = [r["detail"]["outcome"] for r in ag.led.rows(n) if r["event"] == "hypothesis_test"]
    presses.append({"action": act, "intent": intent, "before": value, "after": after,
                    "target": target, "outcome": oc[-1] if oc else None})
    value = after
refused = [r["detail"] for r in ag.led.rows() if r["event"] == "route_refused"][k0:]
print(json.dumps({"arm": tether._ROUTE_REFUSE, "presses": presses, "refused": refused},
                 default=str))
'''


def child(arm: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               TETHER_ROUTE_REFUSE=arm)
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, str(_repo.ROOT)], env=env,
                         capture_output=True, text=True, timeout=1800, cwd=str(_repo.ROOT),
                         stdin=subprocess.DEVNULL)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def main() -> None:
    on, off = child("1"), child("0")
    print("  ON :", json.dumps(on, default=str)[:900])
    print("  OFF:", json.dumps(off, default=str)[:400])
    assert on["arm"] is True and off["arm"] is False, "the switch did not reach the module"
    first = on["presses"][0]
    # OCCASIONS: a goal-exit press graded "farther" that moved WITH the intent's sign
    assert first["action"] is not None and first["outcome"] == "farther", (
        "occasion: no farther", first)
    assert str(first["intent"]).endswith(" +") and first["after"] > first["before"], (
        "occasion: the press did not move with the intent's sign", first)
    assert first["target"] == first["before"] + 1, ("occasion: not sb26's receding target", first)
    print(f"  occasions: 1 overshoot press (before {first['before']}, after {first['after']}, "
          f"target {first['target']}, outcome {first['outcome']})")
    assert not off["refused"], "OFF: a route was refused"
    # THE RULE: the overshoot must NOT refuse the route at once. What the next press does is
    # PRINTED, not asserted: asserting it would presume option A (the reviewer 07:28)
    print(f"  next press ON: {json.dumps(on['presses'][1], default=str)}")
    assert not [r for r in on["refused"] if r.get("why") == "farther"], (
        "ON: a right-way overshoot refused the route at once", on["refused"])
    print("route_overshoot: OK")


if __name__ == "__main__":
    main()
