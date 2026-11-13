"""10d STEP 2b, THE MINT DEEPENS ITS TREES (TETHER_TREE_DEEPEN; the reviewer 2026-11-12). The mint's
depth-one trees that passed their own _cannot_pay are the roots of tree_search.deepen; each deeper
tree is priced by the mint's own bargain (_cannot_pay, _left, pays) and the best one that beats the
mint's best is taken.

TD1  a planted mover o0.m += X - (Y - Z): from the depth-one roots translate<subtract<X>(b)>,
     Agent._deepen_trees returns translate<subtract<X>(subtract<Y>(Z))>, under base
TD2  gridworld 12 steps, the arm ON vs OFF: the ledgers equal once the tree_deepen rows are dropped,
     unless a deeper tree paid (then it is named, and it must be a deeper tree)
MF-TD1 the plant: tree_search.replace_leaf returns None (no tier down) -> TD1 finds nothing -> RED
Seconds: synthetic frames for TD1; gw12 runs twice for TD2.

    python tests/test_tree_deepen.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

HERE = _repo.ROOT

TD1 = r'''
import os, sys
sys.path.insert(0, os.getcwd())
import arc_predict, gamma, gridworld, ledger, tether, tree_search, world
from gamma import Term
if sys.argv[1] == "plant":
    tree_search.replace_leaf = lambda t, sub: None
held = {a.name: a for a in arc_predict.predict()}
tr, sb = held["translate"], held["subtract"]
env = world.bind(gridworld.family("default", 0))
ag = tether.Agent(env, gamma.Gamma([*env.atoms(), tr, sb], game="fam_default_0"),
                  tether.Config(), ledger.Ledger())
ag.step()
M, X, Y, Z, W = "o0.m", "o1.a", "o2.b", "o3.c", "o4.d"
VALS = [(9, 4, 1, 3), (7, 7, 3, 0), (2, 5, 8, 6), (6, 1, 2, 9), (4, 8, 5, 2), (8, 3, 6, 4),
        (3, 9, 7, 1), (5, 2, 4, 8)]
frames, m = [], 0
for a, b, c, d in VALS:
    frames.append({M: m, X: a, Y: b, Z: c, W: d})
    m = m + (a - (b - c))
frames.append({M: m, X: 1, Y: 1, Z: 1, W: 1})
ag.trace = [(frames[t], "ACTION1", frames[t + 1], tether.NO_INTENT, None)
            for t in range(len(frames) - 1)]
ag.slots = [M, X, Y, Z, W]
ag.slot_types = {**ag.slot_types, M: "POSITION", X: "DELTA", Y: "DELTA", Z: "DELTA", W: "DELTA"}
ag.bound = {}
ag._memo = None
for s in ag.slots:
    ag.alphabet[s] = 64
hist = ag.history(M)
heldt = ag.gamma.library[ag.bound.get(M, tether.IDN)]
base = ag._accumulated(M, heldt)
robs = ag._residual_obs(M, heldt, hist)
rkey = ({}, {}) if tether._SPEED2_BOUND else {}
units = ag._units_for(M)
roots = [(Term((tr,), operand=X, operand_term=Term((sb,), operand=s)), 0.0, "predictor")
         for s in (Y, Z, W)]
found, st = ag._deepen_trees(M, roots, hist, base, robs, rkey, units, 500, base)
print(repr((found[3].name if found else None, round(found[0], 3) if found else None,
            round(base, 3), st)))
'''


def td1(mode: str):
    p = subprocess.run([sys.executable, "-B", "-c", TD1, mode], cwd=HERE, capture_output=True,
                       text=True, encoding="utf-8", timeout=600, stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    return eval(p.stdout.strip().splitlines()[-1])  # noqa: S307  our own child's repr


GW = r'''
import json, sys
import gamma, gridworld, ledger, tether, world
env = world.bind(gridworld.family("default", 0))
led = ledger.Ledger()
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
for _ in range(12):
    ag.step()
ag.end_run("cap")
with open(sys.argv[1], "w", encoding="utf-8", newline="\n") as fh:
    for r in led.rows():
        fh.write(json.dumps(r, sort_keys=True, default=str) + "\n")
'''


def gw(path: str, arm: str) -> list[dict]:
    env = {**os.environ, "TETHER_TREE_DEEPEN": arm, "TETHER_AGENT_SEED": "0"}
    p = subprocess.run([sys.executable, "-B", "-c", GW, path], cwd=HERE, env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=600,
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    with open(path, encoding="utf-8") as fh:
        return [json.loads(x) for x in fh]


def strip(rows: list[dict]) -> list[str]:
    out = []
    for r in rows:
        if r.get("event") == "tree_deepen":
            continue
        r = dict(r)
        if r.get("slot") == "@run" and r.get("event") == "arms":
            continue
        r.pop("wall_s", None)
        d = r.get("detail")
        if isinstance(d, dict):
            # timings are not behaviour: wall clocks, *_ms, *_s
            r["detail"] = {k: v for k, v in d.items()
                           if "wall" not in k and k != "s" and not k.endswith(("_ms", "_s"))}
        out.append(json.dumps(r, sort_keys=True))
    return out


def main() -> int:
    name, tot, base, st = td1("on")
    want = "translate<subtract<subtract<o3.c>(o2.b)>(o1.a)>"
    print(f"  TD1: found {name} total {tot} (base {base}); stats {st}")
    ok1 = name == want and tot is not None and tot < base
    print(f"TD1 the mint's deepening finds the depth-two mover: {'GREEN' if ok1 else 'RED'}")
    pname, _pt, _pb, pst = td1("plant")
    red = pname != want
    print(f"  plant: found {pname}; stats {pst}")
    print(f"MF-TD1 no tier down (replace_leaf None): {'RED (as required)' if red else 'GREEN'}")
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        off = gw(os.path.join(td, "off.jsonl"), "0")
        on = gw(os.path.join(td, "on.jsonl"), "1")
    rows = [r for r in on if r.get("event") == "tree_deepen"]
    found = [r["detail"].get("found") for r in rows if r.get("detail", {}).get("found")]
    a, b = strip(off), strip(on)
    diff = sum(1 for x, y in zip(a, b, strict=False) if x != y) + abs(len(a) - len(b))
    print(f"  gw12: {len(off)} rows OFF, {len(on)} ON; tree_deepen rows {len(rows)};"
          f" found {found}; differing (tree_deepen dropped) {diff}")
    ok2 = diff == 0 or bool(found)
    print(f"TD2 gw12 identical unless a deeper tree paid: {'GREEN' if ok2 else 'RED'}")
    assert ok1 and red and ok2
    print("tree_deepen: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
