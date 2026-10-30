import json, sys, collections
def rows(p):
    out = []
    for x in open(p, encoding="utf-8"):
        if not x.strip():
            continue
        r = json.loads(x); r.pop("seq", None); d = r.get("detail") or {}
        if r.get("event") == "arms" and r.get("slot") == "@run":
            continue
        if r.get("event") == "goal_hypotheses":
            d.pop("wall_s", None)
        if r.get("event") == "choice" and d.get("site") == "objective_domain":
            continue
        out.append(r)
    return out
a, b = rows(sys.argv[1]), rows(sys.argv[2])
keys = collections.Counter()
n = 0
for x, y in zip(a, b):
    if x != y:
        n += 1
        dx, dy = x.get("detail") or {}, y.get("detail") or {}
        diff = sorted(k for k in set(dx) | set(dy) if dx.get(k) != dy.get(k))
        top = sorted(k for k in set(x) | set(y) if k != "detail" and x.get(k) != y.get(k))
        keys[(x["event"], tuple(diff), tuple(top))] += 1
print("rows differing:", n)
for k, v in keys.most_common():
    print(v, k)
