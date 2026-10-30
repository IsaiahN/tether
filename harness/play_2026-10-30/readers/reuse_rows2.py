"""Read-only: lineage library rows with a reuse: residual; whether their operand / guard fields name an object id."""
import glob, json, re, sys, zlib
sys.dont_write_bytecode = True
OBJ = re.compile(r"\bo\d+\b")
n = obj = 0
seen = set()
sample = []
for p in sorted(glob.glob("C:/TETHER_RUNS/E4_2026-10-18/lineage/gen_*.json")):
    raw = open(p, "rb").read()
    g = json.loads(zlib.decompress(raw) if raw[:1] == b"\x78" else raw)
    rows = g.get("library") or g.get("rows") or g.get("terms") or []
    rows = list(rows.values()) if isinstance(rows, dict) else rows
    for r in rows:
        if isinstance(r, dict) and str(r.get("residual") or "").startswith("reuse:"):
            key = json.dumps({k: r.get(k) for k in ("atoms", "operand", "operand_term", "guard")}, sort_keys=True, default=str)
            if key in seen:
                continue
            seen.add(key)
            n += 1
            txt = json.dumps({k: r.get(k) for k in ("operand", "operand_term", "guard", "guard_ref")}, default=str)
            hit = bool(OBJ.search(txt))
            obj += hit
            if len(sample) < 8:
                sample.append((r.get("atoms"), str(r.get("operand"))[:60], str(r.get("guard"))[:30], r.get("residual")[:40], hit))
print(f"distinct reuse: rows across all generations: {n}; whose operand/guard names an object id: {obj}")
for s in sample:
    print("  ", s)
