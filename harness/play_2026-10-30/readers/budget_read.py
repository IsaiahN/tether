import collections, json, sys
p = sys.argv[1]
rows = [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]
print("STEP_BUDGET (@budget rows): cycle, spent, asked, not_asked, owed")
for r in rows:
    if r["event"] == "budget" and r["slot"] == "@budget":
        d = r["detail"]; print(f"  c{r['cycle']}: spent {d['spent']:,} of {d['budget']:,} | asked {d['asked']} not_asked {d['not_asked']} owed {d['owed_lookups']}")
pk = [r for r in rows if r["event"] == "park"]
ex = sum(1 for r in pk if r["detail"].get("budget_exhausted"))
print(f"MINT parks: {len(pk)}, budget_exhausted {ex}; per cycle:")
pc = collections.defaultdict(lambda: [0, 0, 0, 0])
for r in pk:
    d = r["detail"]; c = pc[r["cycle"]]; c[0] += 1; c[1] += bool(d.get("budget_exhausted")); c[2] += d.get("candidates_tried", 0); c[3] += d.get("candidates_priced", 0)
for k in sorted(pc):
    print(f"  c{k}: parks {pc[k][0]} exhausted {pc[k][1]} tried {pc[k][2]:,} priced {pc[k][3]:,}")
st = collections.Counter()
for r in rows:
    if r["event"] == "stream":
        s = r["detail"].get("stop") or {}
        for k, v in s.items():
            st[(r["detail"].get("site"), k)] += v
print("MINT stream stops (site, why):", dict(st))
print("MINT keys seen in park detail:", sorted(pk[0]["detail"].keys()) if pk else None)
for r in rows:
    if r["event"] in ("goal_hypotheses", "subject_budget", "routine_cut"):
        d = r["detail"]; print(f"  c{r['cycle']} {r['event']}: " + json.dumps({k: d[k] for k in list(d)[:8] if k != 'ranked'})[:300])
lt = [r["detail"] for r in rows if r["event"] == "lookup_tiers"]
print(f"lookup_tiers {len(lt)}: late_not_asked sum {sum(d.get('late_not_asked', 0) for d in lt)}, late_asked sum {sum(d.get('late_asked', 0) for d in lt)}")
res = [r for r in rows if r["event"] in ("termination", "ending", "attempt_end", "progress", "goal_hypothesis_end")]
for r in res:
    print("  END", r["event"], json.dumps(r["detail"])[:300])
