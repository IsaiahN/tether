"""THE ROW COMPARE (the reviewer 2026-10-19 02:52 item 2, 03:00 item 1): every ledger row of cycles 0..MAX in run A
against run B, field for field (seq, cycle, step, slot, event, the whole detail). @run rows are compared too, but
their differing keys are listed and not counted as a decision difference. The body file's fold rows are compared on
fold, cycle and trigger only, and printed as "folds fired: run N / probe N". READ ONLY.
argv: run_dir probe_dir [max_cycle]"""
import json
import os
import sys

A_DIR, B_DIR = sys.argv[1], sys.argv[2]
MAXC = int(sys.argv[3]) if len(sys.argv) > 3 else 2


def rows(d):
    with open(os.path.join(d, "stream.jsonl"), encoding="utf-8") as fh:
        return [r for r in (json.loads(ln) for ln in fh if ln.strip()) if r.get("cycle", 0) <= MAXC]


def folds(d):
    p = os.path.join(d, "stream.jsonl.body.jsonl")
    with open(p, encoding="utf-8") as fh:
        return [(r.get("fold"), r.get("cycle"), r.get("trigger")) for r in (json.loads(ln) for ln in fh if ln.strip())
                if r.get("event") == "consolidate" and r.get("cycle", 0) <= MAXC]


a, b = rows(A_DIR), rows(B_DIR)
same, diffs, run_keys = 0, [], {}
for i in range(max(len(a), len(b))):
    ra = a[i] if i < len(a) else None
    rb = b[i] if i < len(b) else None
    if ra == rb:
        same += 1
        continue
    if ra and rb and ra.get("slot") == rb.get("slot") == "@run" and ra.get("event") == rb.get("event"):
        da, db = ra.get("detail") or {}, rb.get("detail") or {}
        keys = sorted(k for k in set(da) | set(db) if da.get(k) != db.get(k))
        rest = {k: v for k, v in ra.items() if k != "detail"} == {k: v for k, v in rb.items() if k != "detail"}
        if rest:
            run_keys[i] = keys
            continue
    diffs.append((i, ra, rb))
fa, fb = folds(A_DIR), folds(B_DIR)
print(f"rows compared {max(len(a), len(b))} (run {len(a)}, probe {len(b)}, cycles 0-{MAXC})")
print(f"identical {same}; @run rows differing only in their detail {len(run_keys)}; decision differences {len(diffs)}")
for i, keys in run_keys.items():
    print(f"  @run row {i}: differing keys {keys}")
print(f"folds fired: run {len(fa)} / probe {len(fb)}; sequence (fold, cycle, trigger) "
      f"{'IDENTICAL' if fa == fb else 'DIFFERS'}: run {fa} probe {fb}")
for i, ra, rb in diffs[:20]:
    print(f"--- difference at row {i}\n  run   {json.dumps(ra, sort_keys=True)[:1500]}\n"
          f"  probe {json.dumps(rb, sort_keys=True)[:1500]}")
