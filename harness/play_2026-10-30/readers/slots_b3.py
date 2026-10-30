"""Distinct object ids per cycle in B3's bet rows' slot field, and in the repeat rows' 'reach'."""
import collections, json, re, sys
sys.dont_write_bytecode = True
OID = re.compile(r"^o(\d+)\.")
per = collections.defaultdict(set)
for line in open(sys.argv[1], encoding="utf-8"):
    r = json.loads(line)
    if r.get("event") == "bet":
        m = OID.match(str(r.get("slot") or ""))
        if m:
            per[r.get("cycle")].add(int(m.group(1)))
for c in sorted(k for k in per if k is not None):
    ids = per[c]
    print(c, "objects bet on", len(ids), "id range", min(ids), "-", max(ids))
