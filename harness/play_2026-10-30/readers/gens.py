"""The E4 lineage's generations (zlib JSON): game, generation, parent, term count, and how many terms were born
in an earlier generation (carried). argv: lineage_dir"""
import glob
import json
import os
import sys
import zlib

for f in sorted(glob.glob(os.path.join(sys.argv[1], "gen_*.json")), key=os.path.getmtime):
    raw = open(f, "rb").read()
    j = json.loads(zlib.decompress(raw) if raw[:1] == b"\x78" else raw)
    top = {k: j[k] for k in ("game", "generation", "parent", "how", "born") if k in j}
    terms = j.get("terms") or j.get("library") or {}
    n = len(terms)
    print(os.path.basename(f)[:24], top, "keys", sorted(j)[:12], "terms", n, "bytes", len(raw))
