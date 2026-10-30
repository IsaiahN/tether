import collections, json, sys
rows = [json.loads(x) for x in open(sys.argv[1], encoding="utf-8") if x.strip()]
c = collections.Counter()
for r in rows:
    if r["event"] == "park":
        d = r["detail"]; c[(bool(d.get("budget_exhausted")), str(d.get("verdict"))[:70], str(d.get("note"))[:50])] += 1
for k, v in c.most_common():
    print(v, k)
