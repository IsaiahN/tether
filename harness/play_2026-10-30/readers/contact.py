import json, sys
for x in open(sys.argv[1], encoding="utf-8"):
    r = json.loads(x)
    if r["slot"] in ("o11~o2.contact", "o0~o2.contact") and r["event"] in ("stream", "park", "derived_asked", "want_only", "g1", "process_bet"):
        d = r.get("detail") or {}
        keep = {k: d[k] for k in ("site", "stop", "walked_total", "walked_max", "winner", "winner_rank", "work_budget", "verdict",
                                  "candidates_tried", "candidates_priced", "candidates_seen", "depth", "space_estimate", "coverage", "cut_counts", "want", "echo", "calls", "turns_total") if k in d}
        print(r["cycle"], r["slot"], r["event"], json.dumps(keep, default=str)[:600])
