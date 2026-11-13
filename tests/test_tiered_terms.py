"""STEP 10d, TIERED TERMS (TETHER_TIERED_TERMS; the reviewer 2026-11-12; Isaiah 12:41
"f(g(h(i(...))))", 15:15). The operand tree recursed one level only: _ops read a node's second leaf
as a raw slot, so translate<subtract<x>(y)> was the deepest idea the agent could hold. Under the arm
a node whose own term carries a tree reads that leaf through _ops, one tier down.

TT1  depth 2: translate<subtract<X>(subtract<Y>(Z))> on frame f predicts
     M + (X - (Y - Z)); _ops returns X - (Y - Z) on every frame
TT2  depth 1 unchanged: translate<subtract<X>(Y)> still reads X - Y (r1145's node, byte for byte)
TT3  an unreadable inner leaf (Z absent) gives None (an operand that cannot be read), never a guess
MF-TT1 the arm OFF: the inner tree is ignored, _ops reads X - Y -> TT1 RED (asserted here)
Seconds: a synthetic frame, no game.

    python tests/test_tiered_terms.py
"""
from __future__ import annotations

import os
import subprocess
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

CHILD = r'''
import os, sys
sys.path.insert(0, os.getcwd())
import arc_predict, gamma, gridworld, ledger, tether, world
from gamma import Term
held = {a.name: a for a in arc_predict.predict()}
env = world.bind(gridworld.family("default", 0))
ag = tether.Agent(env, gamma.Gamma([*env.atoms(), held["translate"], held["subtract"]],
                                   game="fam_default_0"), tether.Config(), ledger.Ledger())
ag._memo = None
tr, sb = held["translate"], held["subtract"]
X, Y, Z = "o1.a", "o2.b", "o3.c"
inner = Term((sb,), operand=Z)                      # leaf: subtract with operand Z
mid = Term((sb,), operand=Y, operand_term=inner)    # node: subtract<Y>(...) whose leaf is a tree
deep = Term((tr,), operand=X, operand_term=mid)     # translate<subtract<X>(subtract<Y>(Z))>
flat = Term((tr,), operand=X, operand_term=Term((sb,), operand=Y))
out = []
for x, y, z in ((9, 4, 1), (7, 7, 3), (2, 5, 8)):
    st = {X: x, Y: y, Z: z, "o0.m": 0}
    out.append((ag._ops(deep, st), ag._ops(flat, st), x - (y - z), x - y))
st = {X: 9, Y: 4, "o0.m": 0}
print(repr((out, ag._ops(deep, st), deep.name)))
'''


def child(arm: str):
    env = {**os.environ, "TETHER_TIERED_TERMS": arm}
    r = subprocess.run([sys.executable, "-B", "-c", CHILD], cwd=_repo.ROOT, env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=300)
    assert r.returncode == 0, r.stderr[-2000:]
    return eval(r.stdout.strip().splitlines()[-1])  # noqa: S307  our own child's repr


def main() -> int:
    rows, missing, name = child("1")
    print(f"  tree: {name}")
    ok1 = all(d == (want,) for d, _f, want, _w1 in rows)
    print(f"  ON  depth 2: {[(d, want) for d, _f, want, _w1 in rows]}")
    print(f"TT1 depth 2 reads X - (Y - Z): {'GREEN' if ok1 else 'RED'}")
    ok2 = all(f == (w1,) for _d, f, _w, w1 in rows)
    print(f"TT2 depth 1 unchanged (X - Y): {'GREEN' if ok2 else 'RED'}")
    ok3 = missing is None
    print(f"TT3 an unreadable inner leaf gives None: {'GREEN' if ok3 else 'RED'} ({missing!r})")
    off, _m, _n = child("0")
    red = not all(d == (want,) for d, _f, want, _w1 in off)
    print(f"  OFF depth 2: {[(d, want) for d, _f, want, _w1 in off]}")
    print(f"MF-TT1 the arm OFF ignores the inner tree: {'RED (as required)' if red else 'GREEN'}")
    assert ok1 and ok2 and ok3 and red
    print("tiered_terms: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
