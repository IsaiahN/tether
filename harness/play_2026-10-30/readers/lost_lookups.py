import collections, json, sys
def rows(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]
base = rows(sys.argv[1])
def lk(rs):
    return collections.Counter((r["cycle"], r["slot"]) for r in rs if r["event"] == "lookup")
def owed(rs):
    return [(r["cycle"], r["slot"], (r.get("detail") or {}).get("question")) for r in rs if r["event"] == "budget_owed"]
b = lk(base)
for p in sys.argv[2:]:
    rs = rows(p)
    k = lk(rs)
    lost = b - k; extra = k - b
    print(p.split("/")[-2], "lookups lost:", sorted(lost.items()), "| extra:", sorted(extra.items()))
    ow = owed(rs)
    print("   budget_owed rows:", len(ow), "by cycle", dict(collections.Counter(c for c, _s, _q in ow)))
    # was each owed question asked later?
    asked_later = sum(1 for c, s, q in ow if any(r["event"] == "lookup" and r["slot"] == s and r["cycle"] > c for r in rs))
    print("   owed then asked in a later cycle (same slot):", asked_later, "of", len(ow))
    ends = [(r["cycle"], r["event"]) for r in rs if r["event"] in ("ending", "retarget", "boundary")]
    print("   ends/boundaries:", ends[:6])
