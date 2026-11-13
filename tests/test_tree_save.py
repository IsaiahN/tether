"""10d STEP 3, A TREE'S SHAPE CROSSES A SAVE (TETHER_TIERED_TERMS; the reviewer 2026-11-12).
The save kept only an operand tree's first node (its atom names), so any deeper idea arrived
flattened. Under the arm a tree deeper than one node also writes operand_tree, its nested shape
with no bindings.

TS-S1 a depth-two tree saves and loads with its nested shape (atoms per node, unbound)
TS-S2 a depth-one tree's saved row (its handle aside: a per-run hash) and row_key equal the arm
      OFF's (old saves keep)
TS-S3 a row with no operand_tree (an old save) loads exactly as before
MF-TS-S the arm OFF: the loaded tree is one node deep -> TS-S1 RED (asserted)
Seconds: no game.

    python tests/test_tree_save.py
"""
from __future__ import annotations

import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

CHILD = r'''
import json, os, sys
sys.path.insert(0, os.getcwd())
import arc_predict, gamma
from gamma import Term
held = {a.name: a for a in arc_predict.predict()}
tr, sb = held["translate"], held["subtract"]
def g():
    return gamma.Gamma([tr, sb], game="t")
def shape(t):
    out = []
    while t is not None:
        out.append(([a.name for a in t.atoms], t.operand))
        t = t.operand_term
    return out
deep = Term((tr,), operand="o1.a", operand_term=Term((sb,), operand="o2.b",
            operand_term=Term((sb,), operand="o3.c")))
flat = Term((tr,), operand="o1.a", operand_term=Term((sb,), operand="o2.b"))
a = g(); a.accept(deep, 1, "test"); a.accept(flat, 2, "test")
blob = a.blob(with_names=True)
deep_row = [r for r in blob["terms"] if r.get("operand_tree") is not None]
flat_row = [r for r in blob["terms"] if r.get("name") == flat.name]
b = g(); b.load_blob(blob)
loaded = [shape(t) for t in b.library.values() if t.operand_term is not None]
old = dict(flat_row[0]) if flat_row else None
c = g(); rep = c.load_blob({**blob, "terms": [old]}) if old else None
print(repr((loaded, [json.dumps({k: v for k, v in r.items() if k != "handle"}, sort_keys=True)
             for r in flat_row],
            [gamma.Gamma.row_key(r) for r in flat_row], len(deep_row),
            [shape(t) for t in c.library.values() if t.operand_term is not None])))
'''


def child(arm: str):
    env = {**os.environ, "TETHER_TIERED_TERMS": arm}
    r = subprocess.run([sys.executable, "-B", "-c", CHILD], cwd=_repo.ROOT, env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=300)
    assert r.returncode == 0, r.stderr[-3000:]
    return eval(r.stdout.strip().splitlines()[-1])  # noqa: S307  our own child's repr


def main() -> int:
    on_loaded, on_flat, on_key, n_deep, old_loaded = child("1")
    off_loaded, off_flat, off_key, _n, _o = child("0")
    deepest = max(on_loaded, key=len)
    print(f"  ON  loaded shapes: {on_loaded}")
    ok1 = n_deep == 1 and len(deepest) == 3 and [n for n, _op in deepest] == [
        ["translate"], ["subtract"], ["subtract"]]
    print(f"TS-S1 the depth-two tree crosses with its shape: {'GREEN' if ok1 else 'RED'}")
    ok2 = on_flat == off_flat and on_key == off_key
    print(f"TS-S2 depth-one row + row_key identical ON and OFF: {'GREEN' if ok2 else 'RED'}")
    ok3 = old_loaded and all(len(s) == 2 for s in old_loaded)
    print(f"TS-S3 a row without operand_tree loads as before: {'GREEN' if ok3 else 'RED'}"
          f" ({old_loaded})")
    print(f"  OFF loaded shapes: {off_loaded}")
    red = max(len(s) for s in off_loaded) < 3
    print(f"MF-TS-S the arm OFF flattens the tree: {'RED (as required)' if red else 'GREEN'}")
    assert ok1 and ok2 and ok3 and red
    print("tree_save: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
