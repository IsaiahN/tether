import json, sys, collections
def rows(p):
    out = []
    for x in open(p, encoding="utf-8"):
        if not x.strip():
            continue
        r = json.loads(x); d = r.get("detail") or {}
        r.pop("seq", None)
        if r.get("event") == "arms" and r.get("slot") == "@run":
            continue
        if r.get("event") == "goal_hypotheses":
            d.pop("wall_s", None)
        if r.get("event") == "books":
            for k in ("fit_dedup_agree", "fit_dedup_disagree"):
                d.pop(k, None)
        out.append(r)
    return out
a, b = rows(sys.argv[1]), rows(sys.argv[2])
ca = collections.Counter((r["event"], (r.get("detail") or {}).get("site")) for r in a)
cb = collections.Counter((r["event"], (r.get("detail") or {}).get("site")) for r in b)
print("count diffs:", {k: (ca[k], cb[k]) for k in set(ca) | set(cb) if ca[k] != cb[k]})
fa = [r for r in a if not (r["event"] == "choice" and r["detail"].get("site") == "objective_domain")]
fb = [r for r in b if not (r["event"] == "choice" and r["detail"].get("site") == "objective_domain")]
print("without objective_domain choices:", len(fa), len(fb))
for i, (x, y) in enumerate(zip(fa, fb)):
    if x != y:
        print("FIRST DIFF", i, json.dumps(x)[:500], "\n   vs", json.dumps(y)[:500]); break
else:
    print("IDENTICAL apart from them" if len(fa) == len(fb) else "prefix equal, lengths differ")
oa = [r for r in a if r["event"] == "choice" and r["detail"].get("site") == "objective_domain"]
print("objective_domain choice rows A:", len(oa), " distinct (cycle,slot):", len({(r['cycle'], r['slot']) for r in oa}))
import itertools
g = collections.Counter((r["cycle"], r["slot"]) for r in oa)
gb = collections.Counter((r["cycle"], r["slot"]) for r in b if r["event"] == "choice" and r["detail"].get("site") == "objective_domain")
print("per (cycle,slot) A vs B where differ:", {k: (g[k], gb[k]) for k in set(g) | set(gb) if g[k] != gb[k]})
