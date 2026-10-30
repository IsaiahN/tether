"""Read-only, one generation at a time, from the verified BACKUP (never the live lineage): saved term rows whose
residual is a reuse install, split by whether the term's name ("was") names an object id; and aliases whose
"was" names an object id."""
import json, os, re, sys, zlib
sys.dont_write_bytecode = True
B = sys.argv[1]
OID = re.compile(r"\bo\d+\b")
tot = {"reuse_rows": 0, "reuse_named_ids": 0, "rows": 0, "rows_named_ids": 0, "aliases": 0, "aliases_named_ids": 0, "no_was": 0}
for f in sorted(os.listdir(B)):
    if not f.startswith("gen_"):
        continue
    raw = open(os.path.join(B, f), "rb").read()
    try:
        g = json.loads(zlib.decompress(raw))
    except zlib.error:
        g = json.loads(raw)
    for r in g.get("terms", []):
        was = r.get("was")
        tot["rows"] += 1
        if was is None:
            tot["no_was"] += 1
        ids = bool(OID.search(str(was or "")))
        tot["rows_named_ids"] += ids
        if str(r.get("residual") or "").startswith("reuse:"):
            tot["reuse_rows"] += 1
            tot["reuse_named_ids"] += ids
    for a in g.get("aliases", []) or []:
        tot["aliases"] += 1
        tot["aliases_named_ids"] += bool(OID.search(str(a.get("was") or "")))
print(tot)
