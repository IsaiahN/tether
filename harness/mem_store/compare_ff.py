"""THE FORCED-FOLD N/N (the reviewer 2026-10-19 07:57 item 4a, 08:03 item 2). READ ONLY. Every row of stream.jsonl and
every row of stream.jsonl.body.jsonl in run A against run B, field for field at any depth, with ONLY the keys
commit_before / commit_after / ms dropped (readings of RAM and time); their values are printed side by side. @run rows
are compared the same way and their differing keys listed. Then the end-of-run save: the gen_/idx_/ak_ files each
lineage folder holds beyond the 54 originals, byte for byte.
argv: run_a run_b lineage_a lineage_b"""
import hashlib
import json
import os
import sys
from pathlib import Path

A, B, LA, LB = sys.argv[1:5]
DROP = {"commit_before", "commit_after", "ms"}


def strip(x, got):
    if isinstance(x, dict):
        out = {}
        for k, v in x.items():
            if k in DROP:
                got.append((k, v))
            else:
                out[k] = strip(v, got)
        return out
    if isinstance(x, list):
        return [strip(v, got) for v in x]
    return x


def load(d, f):
    with open(os.path.join(d, f), encoding="utf-8") as fh:
        return [json.loads(ln) for ln in fh if ln.strip()]


for f in ("stream.jsonl", "stream.jsonl.body.jsonl"):
    a, b = load(A, f), load(B, f)
    same, run_rows, diffs, readings = 0, [], [], []
    for i in range(max(len(a), len(b))):
        ga, gb = [], []
        ra = strip(a[i], ga) if i < len(a) else None
        rb = strip(b[i], gb) if i < len(b) else None
        if ga or gb:
            readings.append((i, ga, gb))
        if ra == rb:
            same += 1
        elif ra and rb and ra.get("slot") == rb.get("slot") == "@run":
            da, db = ra.get("detail") or {}, rb.get("detail") or {}
            run_rows.append((i, sorted(k for k in set(da) | set(db) if da.get(k) != db.get(k))))
        else:
            diffs.append((i, ra, rb))
    print(f"{f}: rows A {len(a)} B {len(b)}; identical {same}; @run rows differing {len(run_rows)}; "
          f"DIFFERENCES {len(diffs)}")
    for i, keys in run_rows:
        print(f"  @run row {i}: differing keys {keys}")
    for i, ga, gb in readings:
        print(f"  reading row {i}: A {ga} | B {gb}")
    for i, ra, rb in diffs[:10]:
        print(f"  --- row {i}\n    A {json.dumps(ra, sort_keys=True)[:1200]}\n"
              f"    B {json.dumps(rb, sort_keys=True)[:1200]}")


def sha(d, f):
    return hashlib.sha256(Path(d, f).read_bytes()).hexdigest()[:16]


na = {f for f in os.listdir(LA) if f.endswith(".json")}
nb = {f for f in os.listdir(LB) if f.endswith(".json")}
print(f"lineage json files: A {len(na)} B {len(nb)}; only A {sorted(na - nb)} only B {sorted(nb - na)}")
for f in sorted(na & nb):
    ha, hb = sha(LA, f), sha(LB, f)
    if ha != hb:
        print(f"  BYTES DIFFER {f}: A {ha} B {hb}")
print("save files compared byte for byte:", len(na & nb))
