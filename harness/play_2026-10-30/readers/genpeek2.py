import json, sys, zlib
for p in sys.argv[1:]:
    b = open(p, "rb").read()
    try:
        b = zlib.decompress(b)
    except zlib.error:
        pass
    d = json.loads(b)
    eu, uu = d.get("entry_use"), d.get("unit_used")
    print(p[-26:], "entry_use", type(eu).__name__, len(eu) if hasattr(eu, "__len__") else eu, repr(list(eu.items())[:3] if isinstance(eu, dict) else eu[:3])[:300])
    print("   unit_used", type(uu).__name__, repr(uu)[:300])
    print("   origins", {o: sum(1 for t in d["terms"] if t.get("origin") == o) for o in {t.get("origin") for t in d["terms"]}})
