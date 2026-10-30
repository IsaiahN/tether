"""Read-only: aliases and instance-named aliases in ONE generation file (by its 16-hex hash), from a
lineage folder (the backup or the live folder AFTER a round ends; never during a write)."""
import json, re, sys, zlib
sys.dont_write_bytecode = True
d, h = sys.argv[1], sys.argv[2]
raw = open(f"{d}/gen_{h}.json", "rb").read()
try:
    g = json.loads(zlib.decompress(raw))
except zlib.error:
    g = json.loads(raw)
al = g.get("aliases") or []
oid = re.compile(r"\bo\d+\b")
print(f"gen {h}: terms {len(g.get('terms', []))}, aliases {len(al)} (instance-named "
      f"{sum(1 for a in al if oid.search(str(a.get('was'))))}), evidence {len(g.get('evidence', []))}")
