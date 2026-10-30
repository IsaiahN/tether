import json, sys, collections
c = collections.Counter(); ev = collections.Counter()
with open(sys.argv[1], encoding="utf-8") as f:
    for i, line in enumerate(f):
        try:
            r = json.loads(line)
        except Exception:
            continue
        c[tuple(sorted(r))[:8]] += 1
        ev[(r.get("game"), r.get("step"), r.get("event"))] += 0
        if i > 200000:
            break
for k, v in c.most_common(8):
    print(v, k)
