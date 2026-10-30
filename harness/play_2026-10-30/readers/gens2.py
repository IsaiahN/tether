"""Per generation (in chain order): game, terms, inventions, entry_use entries and how many have a use > 0, the
book's size, and the compressed and raw bytes; plus the lineage folder's total bytes by file kind. argv: lineage_dir"""
import collections
import glob
import json
import os
import sys
import zlib

d = sys.argv[1]
gens = {}
for f in glob.glob(os.path.join(d, "gen_*.json")):
    raw = open(f, "rb").read()
    body = zlib.decompress(raw) if raw[:1] == b"\x78" else raw
    j = json.loads(body)
    gens[os.path.basename(f)[4:20]] = (j, len(raw), len(body))
order, cur = [], next(k for k, (j, _, _) in gens.items() if j.get("parent") is None)
while cur:
    order.append(cur)
    cur = next((k for k, (j, _, _) in gens.items() if j.get("parent") == cur), None)
for k in order:
    j, zb, rb = gens[k]
    eu = j.get("entry_use") or {}
    used = sum(1 for v in eu.values() if (v if isinstance(v, (int, float)) else (v.get("used", 0) if isinstance(v, dict) else len(v) if isinstance(v, list) else 0)))
    print(f"gen {j.get('generation'):2d} {j.get('game'):7s} terms {len(j.get('terms') or {}):3d} inventions {len(j.get('inventions') or []):3d} "
          f"entry_use {len(eu):5d} used>0 {used:5d}  zbytes {zb:9d} raw {rb:10d}")
kinds = collections.Counter()
for f in os.listdir(d):
    p = os.path.join(d, f)
    if os.path.isfile(p):
        kinds[f.split("_")[0].split(".")[0]] += os.path.getsize(p)
print("folder bytes by kind:", dict(kinds), "total", sum(kinds.values()))
