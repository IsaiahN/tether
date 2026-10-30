"""E4a per game: result.json's end / levels / actions / cycles / wall / error, and the lineage generations' games and
parents (gen_*.json, header fields only). argv: e4_dir"""
import glob
import json
import os
import sys

E = sys.argv[1]
for d in sorted(glob.glob(os.path.join(E, "public", "*"))):
    g = os.path.basename(d)
    rj = glob.glob(os.path.join(d, "*.result.json"))
    if not rj:
        print(g, "NO result.json")
        continue
    r = json.load(open(rj[0], encoding="utf-8"))
    keys = ("end", "levels", "levels_completed", "acted", "agent_steps", "cycles", "wall_s", "error", "won", "lineage")
    print(g, {k: (str(r.get(k))[:80] if k == "lineage" else r.get(k)) for k in keys if k in r})
print("--- lineage generations")
for f in sorted(glob.glob(os.path.join(E, "lineage", "gen_*.json")), key=os.path.getmtime):
    j = json.load(open(f, encoding="utf-8"))
    h = j.get("header", j) if isinstance(j, dict) else {}
    print(os.path.basename(f), {k: h.get(k) for k in ("game", "generation", "parent", "born", "how") if k in h},
          "size", os.path.getsize(f))
