"""HTN TIERS (TETHER_HTN_TIERS; Isaiah 2026-11-13 09:29 the tier ladder, bottom-up, and 10:24
"build part 2"; DESIGN_2026-11-13_HTN_at_the_pick part 2). What has to hold first is learned from
the board: each OPENED crossing is kept whole (tier 1), counted by kind into "K opens after J
changes" (tier 2), and offered to the planner as candidate subtasks.

T1  tier 1: an opened crossing is kept whole -- the item, its kind, the press, the OTHER objects'
    changed slots (the item's own object left out) -- and written as an htn_tier1 row
T2  tier 2: three openings of kind K after a J change and one after an L change read
    K: after J 3 of 4, after L 1 of 4
T3  at the pick: a goal of kind K with no law (no enablers) and an open J slot on the board is
    decomposed into that J slot (htn_push, its read naming tier 2)
MF-T3 the plant: TETHER_HTN_TIERS=0 -> nothing to decompose into -> RED
T4  the coincidence bar: a kind seen once (below MIN_REPEAT) offers nothing
MF-T4 the plant: the bar removed (MIN_REPEAT 1) -> the once-seen kind is offered -> RED
T5  gridworld 12 steps, the arm ON vs OFF: both complete and pass the gate (the commit's OFF
    identity against development is the seat's check)
Seconds.

    python tests/test_htn_tiers.py
"""
from __future__ import annotations

import os
import subprocess
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

HERE = _repo.ROOT
CHILD = r'''
import os, sys
sys.path.insert(0, os.getcwd())
import gamma, gridworld, ledger, tether, world
mode = sys.argv[1]
if mode == "bar_plant":
    tether.MIN_REPEAT = 1
env = world.bind(gridworld.family("default", 0))
led = ledger.Ledger()
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
ag.step()
# three slots on three objects whose kind keys differ
picks, keys, owners = [], set(), set()
for s in sorted(ag.slot_types):
    if "@" in s or "~" not in s and "." not in s:
        continue
    o = s.rsplit(".", 1)[0]
    try:
        k = ag._can_kind_key(s)
    except Exception:
        continue
    if o in owners or k in keys:
        continue
    owners.add(o); keys.add(k); picks.append(s)
A, B, C = picks[:3]
own = sorted(s for s in ag.slot_types if s.rsplit(".", 1)[0] == A.rsplit(".", 1)[0] and s != A)
out = {"A": A, "B": B, "C": C}
row = {"item": A, "kind": "opened"}
if mode in ("tier1",):
    ag._tier_note(row, "up", [A] + own[:1] + [B])
    t = ag._tier1[-1]
    out["changed"] = t["changed"]
    out["press"] = t["press"]
    out["rows"] = sum(1 for r in led.rows() if r.get("event") == "htn_tier1")
elif mode == "tier2":
    for _ in range(3):
        ag._tier_note(row, "up", [B])
    ag._tier_note(row, "up", [C])
    rule = ag._tier2[ag._can_kind_key(A)]
    out["opened"] = rule["opened"]
    out["after"] = sorted(rule["after"].values())
else:
    n = 1 if mode in ("bar", "bar_plant") else 3
    for _ in range(n):
        ag._tier_note(row, "up", [B])
    ag._res = {A: [3, 3], B: [2, 2]}
    ag._enablers = lambda s: []
    ag._out_of_reach = lambda s: False
    ag._hyp = None
    ag._tasks, ag._subgoal, ag._htn_tried, ag._htn_pending = [], None, {}, {}
    ag._htn_adopt(A, "no_realisation")
    out["pushes"] = [(r["slot"], r["detail"].get("when")) for r in led.rows()
                     if r.get("event") == "htn_push"]
    out["read"] = [r["detail"].get("read") for r in led.rows()
                   if r.get("event") == "subgoal_adopted"]
print(repr(out))
'''

GW = r'''
import sys
import gamma, gate, gridworld, ledger, tether, world
env = world.bind(gridworld.family("default", 0))
led = ledger.Ledger()
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
for _ in range(12):
    ag.step()
ag.end_run("cap")
rows = led.rows()
print(repr((len(rows), gate.check(rows)["verdict"],
            sum(1 for r in rows if r.get("event") == "htn_tier1"))))
'''


def child(code: str, *args: str, **arms: str):
    env = {**os.environ, "TETHER_AGENT_SEED": "0", "PYTHONIOENCODING": "utf-8", **arms}
    p = subprocess.run([sys.executable, "-B", "-c", code, *args], cwd=HERE, env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=900,
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    return eval(p.stdout.strip().splitlines()[-1])  # noqa: S307  our own child's repr


def main() -> int:
    t1 = child(CHILD, "tier1")
    ok1 = t1["changed"] == [t1["B"]] and t1["press"] == "up" and t1["rows"] == 1
    print(f"  T1 {t1}")
    print(f"T1 an opened crossing is kept whole, other objects only: {'GREEN' if ok1 else 'RED'}")

    t2 = child(CHILD, "tier2")
    ok2 = t2["opened"] == 4 and t2["after"] == [1, 3]
    print(f"  T2 {t2}")
    print(f"T2 tier 2 counts by kind: {'GREEN' if ok2 else 'RED'}")

    t3 = child(CHILD, "pick")
    ok3 = t3["pushes"] == [(t3["B"], "pick")] and t3["read"] and "tier2" in t3["read"][0]
    print(f"  T3 {t3}")
    print(f"T3 a goal with no law is decomposed by tier 2: {'GREEN' if ok3 else 'RED'}")
    p3 = child(CHILD, "pick", TETHER_HTN_TIERS="0")
    red3 = not p3["pushes"]
    print(f"MF-T3 the arm OFF: pushes {p3['pushes']} -> {'RED (as required)' if red3 else 'GREEN'}")

    t4 = child(CHILD, "bar")
    ok4 = not t4["pushes"]
    print(f"T4 a kind seen once offers nothing: {'GREEN' if ok4 else 'RED'}")
    p4 = child(CHILD, "bar_plant")
    red4 = bool(p4["pushes"])
    print(f"MF-T4 the bar removed: pushes {p4['pushes']} -> "
          f"{'RED (as required)' if red4 else 'GREEN'}")

    on = child(GW)
    off = child(GW, TETHER_HTN_TIERS="0")
    ok5 = on[1] == "pass" and off[1] == "pass" and off[2] == 0
    print(f"  T5 gw12 ON {on}, OFF {off}")
    print(f"T5 gridworld runs pass the gate both ways: {'GREEN' if ok5 else 'RED'}")
    assert ok1 and ok2 and ok3 and red3 and ok4 and red4 and ok5
    print("htn_tiers: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
