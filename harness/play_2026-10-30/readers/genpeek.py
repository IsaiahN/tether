import json, sys, zlib
b = open(sys.argv[1], "rb").read()
try:
    b = zlib.decompress(b)
except zlib.error:
    pass
d = json.loads(b)
print(type(d).__name__, list(d)[:30] if isinstance(d, dict) else len(d))
for k in ("terms", "library", "evidence", "parent", "game"):
    v = d.get(k) if isinstance(d, dict) else None
    if v is not None:
        print(k, type(v).__name__, (len(v) if hasattr(v, "__len__") else v), repr(v[:2] if isinstance(v, list) else (list(v)[:3] if isinstance(v, dict) else v))[:400])
