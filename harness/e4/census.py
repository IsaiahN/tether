import json, sys, collections
c = collections.Counter(); keys = collections.defaultdict(collections.Counter); slots = collections.defaultdict(collections.Counter)
for p in sys.argv[1:]:
    for ln in open(p, encoding="utf-8"):
        r = json.loads(ln)
        e = (r.get("step"), r.get("event"))
        c[e] += 1
        for k in (r.get("detail") or {}):
            keys[e][k] += 1
        s = r.get("slot") or ""
        slots[e][s if s.startswith("@") else "<obj>"] += 1
for e, n in sorted(c.items(), key=lambda x: (str(x[0][0]), str(x[0][1]))):
    print(n, e, dict(slots[e].most_common(3)), sorted(keys[e])[:14])
