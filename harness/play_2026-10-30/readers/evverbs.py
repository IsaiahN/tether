import collections, json, sys, zlib
for p in sys.argv[1:]:
    b = open(p, "rb").read()
    try:
        b = zlib.decompress(b)
    except zlib.error:
        pass
    d = json.loads(b)
    print(p[-26:], collections.Counter(e[0] for e in d["evidence"]), "status", d.get("status"), "vind", repr(d.get("vindication_tail"))[:120])
