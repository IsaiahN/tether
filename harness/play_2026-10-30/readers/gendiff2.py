"""Read-only: per term row, which fields differ between two generations. argv: a b"""
import json, sys, zlib
sys.dont_write_bytecode = True
def rd(p):
    raw = open(p, "rb").read()
    return json.loads(zlib.decompress(raw) if raw[:1] == b"\x78" else raw)
a, b = rd(sys.argv[1]), rd(sys.argv[2])
ta, tb = a["terms"], b["terms"]
print("rows", len(ta), len(tb))
for i, (x, y) in enumerate(zip(ta, tb)):
    ks = sorted(k for k in set(x) | set(y) if x.get(k) != y.get(k))
    print(i, ks, [(x.get(k), y.get(k)) for k in ks])
