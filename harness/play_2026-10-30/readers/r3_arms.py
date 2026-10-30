"""PLAY19 round 3's launch read (r355 (c) 6): the arms row's CREDIT state and the first divide row. argv: stream."""
import json
import sys

sys.dont_write_bytecode = True
rows = []
for line in open(sys.argv[1], encoding="utf-8"):
    try:
        rows.append(json.loads(line))
    except json.JSONDecodeError:
        break                                   # the line being written
head = rows[0]["detail"]
print("rows", len(rows), "| head", head.get("head"))
for k in ("on", "off"):
    print(k, [x for x in head.get(k, []) if "CREDIT" in x or "DIVIDE" in x or "S1_REPRICE" in x])
arms = next((r for r in rows if r.get("event") == "arms"), None)
if arms:
    d = arms["detail"]
    print("arms row:", {k: v for k, v in d.items() if "CREDIT" in str(k) or "DIVIDE" in str(k)} or
          json.dumps(d)[:600])
dv = next((r for r in rows if r.get("event") == "divide"), None)
print("first divide row:", json.dumps(dv)[:700] if dv else None)
