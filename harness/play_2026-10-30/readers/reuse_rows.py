"""Read-only (the reviewer r277 (2)): the lineage's saved library rows whose residual starts "reuse:", over every
generation file in the lineage dir (zlib JSON, written once; memory.db not opened): how many name an object id."""
import glob
import json
import re
import sys
import zlib

sys.dont_write_bytecode = True
OBJ = re.compile(r"\bo\d+\b")
LIN = "C:/TETHER_RUNS/E4_2026-10-18/lineage"
names_reuse, names_reuse_obj = {}, {}
keyset = set()
for p in sorted(glob.glob(f"{LIN}/gen_*.json")):
    raw = open(p, "rb").read()
    g = json.loads(zlib.decompress(raw) if raw[:1] == b"\x78" else raw)
    rows = g.get("library") or g.get("rows") or g.get("terms") or []
    if isinstance(rows, dict):
        rows = list(rows.values())
    for r in rows:
        if isinstance(r, dict):
            keyset.update(r.keys())
            res = str(r.get("residual") or "")
            nm = str(r.get("name") or r.get("term") or r.get("key") or "")
            if res.startswith("reuse:"):
                names_reuse[nm] = p[-21:-5]
                if OBJ.search(nm):
                    names_reuse_obj[nm] = p[-21:-5]
print(f"generation files {len(glob.glob(f'{LIN}/gen_*.json'))}; row keys seen {sorted(keyset)[:20]}")
print(f"distinct saved library rows with a reuse: residual: {len(names_reuse)}; naming an object id: {len(names_reuse_obj)}")
for n in list(names_reuse)[:: max(1, len(names_reuse) // 10)][:10]:
    print(f"  {n[:100]}  | object id: {bool(OBJ.search(n))}")
