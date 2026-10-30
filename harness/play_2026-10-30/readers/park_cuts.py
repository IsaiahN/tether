import collections, json, sys
rows = [json.loads(x) for x in open(sys.argv[1], encoding="utf-8") if x.strip()]
pk = [r for r in rows if r["event"] == "park"]
print("example park cut_counts / cuts / space_estimate / depth / coverage:")
for r in pk[:3]:
    d = r["detail"]
    print(" ", json.dumps({k: d.get(k) for k in ("verdict", "depth", "cut_counts", "cuts", "space_estimate", "coverage", "candidates_seen", "candidates_tried")})[:700])
agg = collections.Counter(); depth = collections.Counter()
for r in pk:
    d = r["detail"]
    for k, v in (d.get("cut_counts") or {}).items():
        if isinstance(v, (int, float)):
            agg[k] += v
    depth[str(d.get("depth"))] += 1
print("cut_counts summed over 72 parks:", dict(agg))
print("depth reached:", dict(depth))
