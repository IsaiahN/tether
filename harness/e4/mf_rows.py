import json, sys
rows = [json.loads(x) for x in open(sys.argv[1], encoding="utf-8") if x.strip()]
print("rows", len(rows), "seq range", rows[0].get("seq"), rows[-1].get("seq"))
print("rows with seq in [1843, 1844):", [(r["seq"], r["event"], r["slot"], r["cycle"]) for r in rows if 1843 <= r.get("seq", -1) < 1844])
print("restart rows:", [(r["seq"], r["event"], r["cycle"]) for r in rows if r["event"] in ("restart", "restart_lineage", "boundary", "ending")])
