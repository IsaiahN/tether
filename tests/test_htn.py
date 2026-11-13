"""A REAL HTN (TETHER_HTN; the reviewer 2026-11-13; Isaiah 04:39; DESIGN_2026-11-13_HTN): R-C's
single detour becomes a task stack -- recursive, bounded by the dependency chain -- with methods by
kind ordered by what paid, a walkthrough that rejects an unreachable subtask first, and methods
carried in the lineage.

H1  recursion: A's routes ran out -> B pushed (depth 1); B's ran out -> C pushed (depth 2); C
    arrives and pops -> B is the selected subtask again
MF-H1 the plant: the stack pinned to one level (today's R-C) -> C is never pushed -> RED
H2  the walkthrough: A's enablers B (out of reach) and C -> B rejected (htn_method_rejected), C
    pushed
MF-H2 the plant: no reach check -> B pushed -> RED
H3  the ground orders methods: A's enablers B, C; the edge A->C has paid 5 of 5 -> C pushed first
MF-H3 the plant: the record ignored -> the model's first (B) -> RED
H4  credit: A arrives after its subtask -> the edge paid; A gone from the board -> ended unpaid
H5  carry: htn_n round trip through the store and the archive as increments (5/5, a save with
    nothing new loads 5/5, one more ending loads 6/5)
H6  gridworld 12 steps, TETHER_HTN ON vs OFF both complete and pass the gate (the commit's OFF
    identity against development is the seat's check)
Seconds.

    python tests/test_htn.py
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
    o = s.rsplit(".", 1)[0]
    k = ag._htn_edge(s, s)
    if o not in owners and k not in kinds:
        owners.add(o); kinds.add(k); picks.append(s)
if len(picks) < 3:                      # a board with fewer kinds: name-keyed edges for the test
    ag._htn_edge = lambda p, q: f"{p} -> {q}"
    owners, picks = set(), []
    for s in sorted(ag.slot_types):
        o = s.rsplit(".", 1)[0]
        if o not in owners:
            owners.add(o); picks.append(s)
A, B, C = picks[:3]
ag._res = {A: [3, 3], B: [2, 2], C: [1, 1]}
links = {A: [(B, "l"), (C, "l")] if mode in ("walk", "walk_plant", "ground", "ground_plant")
         else [(B, "l")], B: [(C, "l")], C: []}
ag._enablers = lambda s: links.get(s, [])
far = {B} if mode in ("walk", "walk_plant") else set()
ag._out_of_reach = (lambda s: False) if mode == "walk_plant" else (lambda s: s in far)
if mode == "rec_plant":
    _orig = ag._htn_push
    ag._htn_push = lambda c: False if ag._tasks else _orig(c)
if mode in ("ground", "ground_plant"):
    e = ag._htn_edge(A, C)
    ag._htn[e] = [5, 5]
    if mode == "ground_plant":
        ag._htn.clear()
out = {}
if mode in ("rec", "rec_plant"):
    ag._htn_push(A)
    ag._htn_push(B)
    out["depth"] = len(ag._tasks)
    out["subs"] = [t["sub"] == C for t in ag._tasks]
    if len(ag._tasks) == 2:
        ag._res[C] = [0, 0, 0]
        ag._subgoal_end("arrived")
        out["after_pop_is_B"] = ag._subgoal is not None and ag._subgoal["sub"] == B
elif mode in ("walk", "walk_plant", "ground", "ground_plant"):
    ag._htn_push(A)
    out["pushed_C"] = bool(ag._tasks) and ag._tasks[-1]["sub"] == C
    out["rejected"] = sum(1 for r in led.rows() if r.get("event") == "htn_method_rejected")
elif mode == "credit":
    ag._htn_push(A)
    ag._res[A] = [0, 0, 0]
    ag._htn_settle()
    e = ag._htn_edge(A, B)
    out["paid"] = list(ag._htn.get(e, []))
    ag._tasks, ag._subgoal = [], None
    ag._res[A] = [3, 3]
    ag._htn_tried = {}
    ag._htn_push(A)
    del ag._res[A]
    ag._htn_settle()
    out["after_gone"] = list(ag._htn.get(e, []))
print(repr(out))
'''

CARRY = r'''
import os, sys, tempfile
from pathlib import Path
sys.path.insert(0, os.getcwd())
import gamma, gridworld, ledger, lineage, tether, world
def agent():
    env = world.bind(gridworld.family("default", 0))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                        ledger.Ledger())
d = Path(tempfile.mkdtemp(prefix="htn_"))
E = "('K1',) -> ('K2',)"
a = agent(); a._htn = {E: [5, 5]}
lineage.write(d, a, "default")
b = agent(); lineage.load(d, b); first = {k: list(v) for k, v in b._htn.items()}
lineage.write(d, a, "default")
c = agent(); lineage.load(d, c); again = {k: list(v) for k, v in c._htn.items()}
c._htn[E][0] += 1
lineage.write(d, c, "default")
e = agent(); lineage.load(d, e); grown = dict(e._htn)
print(repr((first, again, grown)))
'''

GW = r'''
import json, sys
import gamma, gate, gridworld, ledger, tether, world
env = world.bind(gridworld.family("default", 0))
led = ledger.Ledger()
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
for _ in range(12):
    ag.step()
ag.end_run("cap")
rows = led.rows()
print(repr((len(rows), gate.check(rows)["verdict"])))
'''


def child(code: str, *args: str, **arms: str):
    env = {**os.environ, "TETHER_AGENT_SEED": "0", "PYTHONIOENCODING": "utf-8", **arms}
    p = subprocess.run([sys.executable, "-B", "-c", code, *args], cwd=HERE, env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=900,
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    return eval(p.stdout.strip().splitlines()[-1])  # noqa: S307  our own child's repr


def main() -> int:
    r = child(CHILD, "rec")
    ok1 = r["depth"] == 2 and r["subs"] == [False, True] and r.get("after_pop_is_B")
    print(f"  H1 {r}")
    print(f"H1 recursion, and the stack unwinds to the task under it: {'GREEN' if ok1 else 'RED'}")
    p = child(CHILD, "rec_plant")
    red1 = p["depth"] < 2
    print(f"MF-H1 one level only: depth {p['depth']} -> {'RED (as required)' if red1 else 'GREEN'}")
    w = child(CHILD, "walk")
    ok2 = w["pushed_C"] and w["rejected"] == 1
    print(f"  H2 {w}")
    print(f"H2 the walkthrough rejects the unreachable subtask: {'GREEN' if ok2 else 'RED'}")
    wp = child(CHILD, "walk_plant")
    red2 = not wp["pushed_C"]
    print(f"MF-H2 no reach check: pushed C {wp['pushed_C']} -> "
          f"{'RED (as required)' if red2 else 'GREEN'}")
    g = child(CHILD, "ground")
    ok3 = g["pushed_C"]
    print(f"H3 the method that paid goes first: {'GREEN' if ok3 else 'RED'}")
    gp = child(CHILD, "ground_plant")
    red3 = not gp["pushed_C"]
    print(f"MF-H3 the record ignored: pushed C {gp['pushed_C']} -> "
          f"{'RED (as required)' if red3 else 'GREEN'}")
    c = child(CHILD, "credit")
    ok4 = c["paid"] == [1, 1] and c["after_gone"] == [2, 1]
    print(f"  H4 {c}")
    print(f"H4 an arrival pays the method, a departure ends it unpaid: {'GREEN' if ok4 else 'RED'}")
    ok5 = True
    for store in ("1", "0"):
        first, again, grown = child(CARRY, TETHER_MEMORY_STORE=store)
        E = "('K1',) -> ('K2',)"
        good = first.get(E) == [5, 5] and again.get(E) == [5, 5] and grown.get(E) == [6, 5]
        print(f"  H5 store={store}: {first} / {again} / {grown}")
        ok5 = ok5 and good
    print(f"H5 methods carry across generations as increments: {'GREEN' if ok5 else 'RED'}")
    on = child(GW)
    off = child(GW, TETHER_HTN="0")
    ok6 = on[1] == "pass" and off[1] == "pass"
    print(f"  H6 gw12 ON {on}, OFF {off}")
    print(f"H6 gridworld runs pass the gate both ways: {'GREEN' if ok6 else 'RED'}")
    assert ok1 and red1 and ok2 and red2 and ok3 and red3 and ok4 and ok5 and ok6
    print("htn: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
