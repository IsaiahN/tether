import json, sys
sys.dont_write_bytecode = True
rd = sys.argv[1]
c0 = {}
for l in open(rd + "/switch.tsv", encoding="utf-8"):
    f = l.split("\t")
    if f[0].isdigit(): c0[int(f[3])] = f[1]
for l in open(rd + "/stream.jsonl", encoding="utf-8"):
    if '"event": "repeat"' not in l: continue
    r = json.loads(l); d = r["detail"]
    if r["cycle"] in c0 or r["cycle"] - 1 in c0:
        print(r["cycle"], c0.get(r["cycle"]) or (str(c0.get(r["cycle"] - 1)) + "+1"), "live", d.get("gamma_reuse_live"), "on_board", d.get("gamma_reuse_on_board"), "route_s", (d.get("wall_s") or {}).get("ROUTE"))
