"""Read-only: tr87's first-step rows [seqP, seq1) in one round's stream (the reviewer 2026-10-26 13:53).
argv: round folder, game. Prints the run-length sequence of (step, event), the top counts, and the named rows."""
import collections
import json
import os
import sys

sys.dont_write_bytecode = True
O, G = sys.argv[1], sys.argv[2]
row = None
for ln in open(os.path.join(O, "switch.tsv"), encoding="utf-8"):
    f = ln.rstrip("\n").split("\t")
    if len(f) > 12 and f[1] == G:
        row = f
seqP, seq1, c0 = int(row[11]), int(row[12]), int(row[3])
print(f"{G}: cycle_start {c0} seq0 {row[10]} seqP {seqP} seq1 {seq1} steps {row[5]} first_act_s {row[14]}")
rows = []
for ln in open(os.path.join(O, "stream.jsonl"), encoding="utf-8"):
    try:
        r = json.loads(ln)
    except ValueError:
        continue
    s = r.get("seq")
    if isinstance(s, int) and seqP <= s < seq1:
        rows.append(r)
rows.sort(key=lambda r: r["seq"])
print(f"rows in [seqP, seq1): {len(rows)}; seq {rows[0]['seq'] if rows else None}..{rows[-1]['seq'] if rows else None}; cycles {sorted({r.get('cycle') for r in rows})}")
runs = []
for r in rows:
    k = (r.get("step"), r.get("event"))
    if runs and runs[-1][0] == k:
        runs[-1][1] += 1
    else:
        runs.append([k, 1, r["seq"]])
print(f"== run-length order ({len(runs)} runs)")
for k, n, s in runs:
    print(f"  seq {s:>6}  {k[0]:<9} {k[1]:<28} x{n}")
c = collections.Counter((r.get("step"), r.get("event")) for r in rows)
print("== top 25 (step, event)")
for (st, ev), n in c.most_common(25):
    print(f"  {n:>6}  {st:<9} {ev}")
print("== named rows")
for r in rows:
    e, d = r.get("event"), r.get("detail") or {}
    if e in ("lookup_deferred", "walk_cut", "step_act", "cap_mid_step", "budget", "budget_owed", "load",
             "index_installed") or r.get("slot") == "@cap" or "index" in (e or ""):
        dd = {k: v for k, v in d.items() if k not in ("reads", "code")}
        print(f"  seq {r['seq']} c{r.get('cycle')} {r.get('step')} {e} {r.get('slot')} {json.dumps(dd)[:300]}")
