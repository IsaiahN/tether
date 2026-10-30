import collections, json, sys
def rows(p):
    out = []
    for x in open(p, encoding="utf-8"):
        if not x.strip():
            continue
        r = json.loads(x); r.pop("seq", None); d = r.get("detail") or {}
        if r["event"] == "arms" and r["slot"] == "@run":
            continue
        if r["event"] == "goal_hypotheses":
            d.pop("wall_s", None)
        out.append(r)
    return out
base = rows(sys.argv[1])
def wins(rs):
    return sorted((r["cycle"], r["slot"], r["detail"].get("winner_rank")) for r in rs
                  if r["event"] == "stream" and r["detail"].get("site") == "stream_share" and (r["detail"].get("stop") or {}).get("found"))
SKIP = {"stream", "park"}
for p in sys.argv[2:]:
    rs = rows(p)
    print(p.split("/")[-2], "finds:", wins(rs))
    a = [r for r in base if r["event"] not in SKIP]; b = [r for r in rs if r["event"] not in SKIP]
    first = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), None)
    print("   rows without stream/park:", len(a), "vs", len(b), "first differ:", first, (json.dumps(a[first])[:250], json.dumps(b[first])[:250]) if first is not None else "")
    ev = collections.Counter(r["event"] for r in a) - collections.Counter(r["event"] for r in b)
    ev2 = collections.Counter(r["event"] for r in b) - collections.Counter(r["event"] for r in a)
    print("   events fewer:", dict(ev), "more:", dict(ev2))
print("baseline finds:", wins(base))
