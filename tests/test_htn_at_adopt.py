"""HTN AT THE PICK (TETHER_HTN_AT_ADOPT; Isaiah 2026-11-13 09:28-09:29, the walkthrough first;
the reviewer r1908). A goal picked with no route known is decomposed then, not after every route
has been refused (route_exhausted 0 in 1,206 archived ledgers, r1907).

A1  a goal picked with no route known and an open enabler: the enabler is pushed at the pick
    (htn_push when="pick", why the refusal's name)
MF-A1 the plant: TETHER_HTN_AT_ADOPT=0 -> nothing pushed -> RED
A2  through _goal_split: a goal whose route the interface realises is acted on and nothing is
    pushed; the same goal with no route realised is decomposed (split_refused no_realisation, then
    htn_push)
MF-A2 the plant: decompose on every pick, routed or not -> a routed goal is pushed -> RED
A3  a subtask that cannot be decomposed and has no route stays held while actions are untried,
    and leaves the stack (htn_pop how="routes") once every action has been tried
MF-A3 the plant: the untried count ignored (read as 0) -> the subtask leaves at once -> RED
A4  a held goal hypothesis is the agent's own pursuit: nothing is pushed while it is held
A5  gridworld 12 steps, the arm ON vs OFF: both complete and pass the gate (the commit's OFF
    identity against development is the seat's check)
Seconds.

    python tests/test_htn_at_adopt.py
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
env = world.bind(gridworld.family("default", 0))
led = ledger.Ledger()
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
ag.step()
owners, kinds, picks = set(), set(), []
for s in sorted(ag.slot_types):
    if not s.endswith(".row"):
        continue
    o = s.rsplit(".", 1)[0]
    k = ag._htn_edge(s, s)
    if o not in owners and k not in kinds:
        owners.add(o); kinds.add(k); picks.append(s)
if len(picks) < 3:                      # a board with fewer kinds: name-keyed edges for the test
    ag._htn_edge = lambda p, q: f"{p} -> {q}"
    owners, picks = set(), []
    for s in sorted(ag.slot_types):
        if not s.endswith(".row"):
            continue
        o = s.rsplit(".", 1)[0]
        if o not in owners:
            owners.add(o); picks.append(s)
A, B, C = picks[:3]
ag._res = {A: [3, 3], B: [2, 2], C: [1, 1]}
links = {A: [(B, "l")], B: [], C: []}
ag._enablers = lambda s: links.get(s, [])
ag._out_of_reach = lambda s: False
ag._hyp = None
ag._tasks, ag._subgoal, ag._htn_tried, ag._htn_pending = [], None, {}, {}
out = {}
def pushes():
    return [(r["slot"], r["detail"].get("when"), r["detail"].get("why")) for r in led.rows()
            if r.get("event") == "htn_push"]
if mode in ("pick", "pick_off"):
    ag._htn_adopt(A, "no_realisation")
    out["pushes"] = pushes()
    out["depth"] = len(ag._tasks)
elif mode in ("split_routed", "split_unrouted", "split_plant"):
    class R:
        action, why, mode, coord = ag.actions[0], "test route", "", None
    routed = mode in ("split_routed", "split_plant")
    def realise(want, offer, *a, **k):
        if mode == "split_plant":      # the plant: decompose on every pick, routed or not
            ag._htn_adopt(want.subject, "plant")
        return R() if routed else None
    ag.iface.realise = realise
    ag._goal_choice = lambda why=None, book=False: A
    ag._goal_target = lambda s, before: before[s] + 1
    ag._try_first_hold = lambda: False
    ag._predicted_serves = lambda *a, **k: ()
    ag._took = lambda r, want: r.action
    st = getattr(ag.env, "state", {})
    before = dict(st() if callable(st) else st)
    before.setdefault(A, 0)
    for s in (B, C):
        before.setdefault(s, 0)
    try:
        act = ag._goal_split(before, commit=True)
    except Exception as e:                  # noqa: BLE001  report, never hide
        act = f"raised {type(e).__name__}: {e}"
    out["act"] = act
    out["why"] = getattr(ag, "_split_why", None)
    out["pushes"] = pushes()
elif mode in ("held", "held_plant"):
    ag._htn_adopt(A, "no_realisation")            # A -> B
    untried = [2]
    ag._can_untried = (lambda t: 0) if mode == "held_plant" else (lambda t: untried[0])
    ag._htn_adopt(B, "no_realisation")            # B: no method, no route, actions untried
    out["held_while_untried"] = ag._subgoal is not None and ag._subgoal["sub"] == B
    untried[0] = 0
    ag._htn_adopt(B, "no_realisation")            # every action tried
    out["after_all_tried"] = None if ag._subgoal is None else ag._subgoal["sub"]
    out["pops"] = [(r["slot"], r["detail"].get("how")) for r in led.rows()
                   if r.get("event") == "htn_pop"]
    out["tried"] = sorted(ag._htn_tried.get(A, set()))
elif mode == "hyp":
    ag._hyp = {"slots": {A}}
    ag._htn_adopt(A, "no_realisation")
    out["pushes"] = pushes()
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
            sum(1 for r in rows if r.get("event") == "htn_push"))))
'''


def child(code: str, *args: str, **arms: str):
    env = {**os.environ, "TETHER_AGENT_SEED": "0", "PYTHONIOENCODING": "utf-8", **arms}
    p = subprocess.run([sys.executable, "-B", "-c", code, *args], cwd=HERE, env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=900,
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    return eval(p.stdout.strip().splitlines()[-1])  # noqa: S307  our own child's repr


def main() -> int:
    r = child(CHILD, "pick")
    ok1 = r["depth"] == 1 and len(r["pushes"]) == 1 and r["pushes"][0][1:] == (
        "pick", "no_realisation")
    print(f"  A1 {r}")
    print(f"A1 a goal picked with no route is decomposed at the pick: {'GREEN' if ok1 else 'RED'}")
    p = child(CHILD, "pick_off", TETHER_HTN_AT_ADOPT="0")
    red1 = not p["pushes"]
    print(f"MF-A1 the arm OFF: pushes {p['pushes']} -> {'RED (as required)' if red1 else 'GREEN'}")

    ro = child(CHILD, "split_routed")
    un = child(CHILD, "split_unrouted")
    ok2 = (not ro["pushes"] and ro["act"] is not None and not str(ro["act"]).startswith("raised")
           and un["why"] == "no_realisation"
           and [w for _s, w, _y in un["pushes"]] == ["pick"])
    print(f"  A2 routed {ro}")
    print(f"  A2 unrouted {un}")
    print(f"A2 a routed goal is acted on, an unrouted one decomposed: {'GREEN' if ok2 else 'RED'}")
    pl = child(CHILD, "split_plant")
    red2 = bool(pl["pushes"])
    print(f"MF-A2 decompose on every pick: pushes {pl['pushes']} -> "
          f"{'RED (as required)' if red2 else 'GREEN'}")

    h = child(CHILD, "held")
    ok3 = (h["held_while_untried"] and h["after_all_tried"] is None
           and h["pops"] and h["pops"][-1][1] == "routes" and h["tried"])
    print(f"  A3 {h}")
    print(f"A3 a stuck subtask is held while exploring, then leaves: {'GREEN' if ok3 else 'RED'}")
    hp = child(CHILD, "held_plant")
    red3 = not hp["held_while_untried"]
    print(f"MF-A3 the untried count ignored: held {hp['held_while_untried']} -> "
          f"{'RED (as required)' if red3 else 'GREEN'}")

    y = child(CHILD, "hyp")
    ok4 = not y["pushes"]
    print(f"A4 nothing pushed while a goal hypothesis is held: {'GREEN' if ok4 else 'RED'}")

    on = child(GW)
    off = child(GW, TETHER_HTN_AT_ADOPT="0")
    ok5 = on[1] == "pass" and off[1] == "pass"
    print(f"  A5 gw12 ON {on}, OFF {off}")
    print(f"A5 gridworld runs pass the gate both ways: {'GREEN' if ok5 else 'RED'}")
    assert ok1 and red1 and ok2 and red2 and ok3 and red3 and ok4 and ok5
    print("htn_at_adopt: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
