"""READ ONLY (the reviewer 2026-10-19 05:46 item 2): T2's candidates on a lineage copy. A kinds_landed key
(entry, role, kind_o, kind_x) is a T2 candidate only if its (entry, target kind) -- kind_x for a CAUSE, else kind_o
(tether.py:3671-3673) -- has NO kinds_landed_dk key (dk, entry, target kind) anywhere in the chain (with_dk, :3670).
Prediction 0; refuter > 0. One gen_ file in memory at a time. argv: lineage_dir"""
import glob
import json
import os
import sys

landed, with_dk, n_rows, n_dk = set(), set(), 0, 0
for f in sorted(glob.glob(os.path.join(sys.argv[1], "gen_*.json"))):
    with open(f, "rb") as fh:
        g = json.loads(fh.read())
    for k, r, ko, kx in g.get("kinds_landed", ()):
        n_rows += 1
        landed.add((k, json.dumps(kx if r == "CAUSE" else ko)))
    for _d, k, tgt, _n in g.get("kinds_landed_dk", ()):
        n_dk += 1
        with_dk.add((k, json.dumps(tgt)))
    del g
cand = landed - with_dk
print("kinds_landed rows", n_rows, "distinct (entry, target kind)", len(landed))
print("kinds_landed_dk rows", n_dk, "distinct (entry, target kind)", len(with_dk))
print("T2 candidates (in landed, not in with_dk):", len(cand))
for c in sorted(cand)[:10]:
    print("  e.g.", c[0], c[1][:120])
