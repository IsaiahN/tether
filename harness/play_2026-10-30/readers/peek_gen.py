"""Read-only: one term row and one invention row from generation files (zlib or plain JSON). argv: folders..."""
import glob
import json
import os
import sys
import zlib

sys.dont_write_bytecode = True
for d in sys.argv[1:]:
    for f in sorted(glob.glob(os.path.join(d, "gen_*.json"))):
        raw = open(f, "rb").read()
        g = json.loads(zlib.decompress(raw) if raw[:1] == b"\x78" else raw)
        t = g.get("terms") or []
        inv = g.get("inventions") or []
        print(os.path.basename(f), "terms", len(t), "inventions", len(inv), "ended", g.get("ended"))
        if t:
            print("  term:", json.dumps(t[0])[:600])
        if inv:
            print("  inv:", json.dumps(inv[0])[:600])
