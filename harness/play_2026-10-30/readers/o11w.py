import collections, json, sys
rows = [json.loads(x) for x in open(sys.argv[1], encoding="utf-8") if x.strip()]
S = "o11.w"
ev = collections.Counter((r["cycle"], r["step"], r["event"]) for r in rows if r["slot"] == S)
for k in sorted(ev):
    print(k, ev[k])
print("---- key rows on o11.w (not choice/bet):")
for r in rows:
    if r["slot"] != S or r["event"] in ("choice", "bet", "stream", "resolution"):
        continue
    d = r.get("detail") or {}
    keep = {k: d[k] for k in list(d)[:10] if k not in ("reads", "code", "cuts", "frontier")}
    print(r["cycle"], r["step"], r["event"], json.dumps(keep, default=str)[:330])
