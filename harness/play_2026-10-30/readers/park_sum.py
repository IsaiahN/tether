"""Read-only: per park row in the named cycles of a stream.jsonl: slot, budget_exhausted, candidates seen/tried,
space_estimate, coverage, chains bounded out, wall_s, verdict -- and the divide row's credited if any. argv: stream, cycles."""
import json
import sys

sys.dont_write_bytecode = True
cyc = {int(c) for c in sys.argv[2].split(",")}
cred = {}
rows = []
for ln in open(sys.argv[1], encoding="utf-8"):
    if '"park"' not in ln and '"divide"' not in ln:
        continue
    r = json.loads(ln)
    if r.get("cycle") not in cyc:
        continue
    d = r.get("detail") or {}
    if r["event"] == "divide":
        cred[(r["cycle"], r["slot"])] = d.get("credited")
    elif r["event"] == "park":
        rows.append(r)
for r in rows:
    d = r["detail"]
    cc = d.get("cut_counts") or {}
    print(r["cycle"], r["slot"], "exhausted", d.get("budget_exhausted"), "seen", d.get("candidates_seen"),
          "tried", d.get("candidates_tried"), "space", d.get("space_estimate"), "cov", d.get("coverage"),
          "bounded", cc.get("chain bounded out on cost: instances not generated"), "wall", d.get("wall_s"),
          "credited", cred.get((r["cycle"], r["slot"])), d.get("verdict"))
