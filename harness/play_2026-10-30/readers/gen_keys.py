"""Read-only, on COPIES: which generations carry the dormant / dormant_refused keys at all. argv: folder"""
import glob, json, os, sys, zlib
sys.dont_write_bytecode = True
for f in sorted(glob.glob(os.path.join(sys.argv[1], "gen_*.json"))):
    raw = open(f, "rb").read()
    g = json.loads(zlib.decompress(raw) if raw[:1] == b"\x78" else raw)
    print(os.path.basename(f)[4:20], g.get("game"), "has dormant", "dormant" in g,
          "has dormant_refused", "dormant_refused" in g, "n_keys", len(g),
          "evidence", len(g.get("evidence") or []), "terms", len(g.get("terms") or []))
