"""Read-only, on COPIES: per generation, its game, parent, dormant item count and dormant_refused
(count and the refused types). argv: folder of gen_*.json copies"""
import collections, glob, json, os, sys, zlib
sys.dont_write_bytecode = True
tot_d = tot_r = 0
types = collections.Counter()
for f in sorted(glob.glob(os.path.join(sys.argv[1], "gen_*.json"))):
    raw = open(f, "rb").read()
    g = json.loads(zlib.decompress(raw) if raw[:1] == b"\x78" else raw)
    d, r = g.get("dormant") or [], g.get("dormant_refused") or []
    tot_d += len(d); tot_r += len(r)
    for x in r:
        types[x.get("type")] += 1
    print(os.path.basename(f)[4:20], g.get("game"), "parent", str(g.get("parent"))[:16],
          "ended", g.get("ended"), "dormant", len(d), "refused", len(r),
          sorted({x.get("type") for x in r}))
print("TOTAL generations", len(glob.glob(os.path.join(sys.argv[1], "gen_*.json"))),
      "dormant written", tot_d, "dormant refused", tot_r, "refused types", dict(types))
