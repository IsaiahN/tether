"""Read-only: the fields that differ between two generation files (zlib or plain). argv: a b"""
import json, sys, zlib
sys.dont_write_bytecode = True
def rd(p):
    raw = open(p, "rb").read()
    return json.loads(zlib.decompress(raw) if raw[:1] == b"\x78" else raw)
a, b = rd(sys.argv[1]), rd(sys.argv[2])
for k in sorted(set(a) | set(b)):
    if a.get(k) != b.get(k):
        va, vb = json.dumps(a.get(k), default=str), json.dumps(b.get(k), default=str)
        print(f"{k}: len {len(va)} vs {len(vb)} | {va[:300]} || {vb[:300]}")
print("keys", len(a), len(b))
