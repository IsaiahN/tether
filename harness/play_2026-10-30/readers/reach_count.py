import collections, json, sys
p = sys.argv[1]
ev = collections.Counter(); per = collections.defaultdict(collections.Counter); verd = collections.Counter()
bud = []
for x in open(p, encoding="utf-8"):
    if not x.strip():
        continue
    r = json.loads(x); e = r["event"]; d = r.get("detail") or {}
    ev[(r["step"], e)] += 1
    per[r["cycle"]][e] += 1
    for k in ("verdict", "why", "status"):
        if k in d and e in ("mint", "settle", "accept", "frontier", "search", "mint_search"):
            verd[(e, k, str(d[k])[:60])] += 1
    if "budget" in e or "budget" in json.dumps(d)[:2000] and e not in ("arms",):
        bud.append((r["cycle"], r["step"], r["slot"], e, json.dumps(d)[:300]))
print("EVENTS (step, event): count")
for k, v in sorted(ev.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")
print("VERDICTS:")
for k, v in sorted(verd.items(), key=lambda x: -x[1])[:40]:
    print(f"  {k}: {v}")
print("BUDGET-MENTIONING ROWS:", len(bud))
c = collections.Counter((b[3]) for b in bud)
print(" by event:", dict(c))
for b in bud[:12]:
    print("  ", b)
