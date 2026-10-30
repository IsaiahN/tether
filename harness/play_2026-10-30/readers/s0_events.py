"""r356 read: su15's first-step choice, system0 and repeat rows in PLAY19 round 1. argv: round dir."""
import json
import sys

sys.dont_write_bytecode = True
R = sys.argv[1]
rows = [json.loads(x) for x in open(f"{R}/stream.jsonl", encoding="utf-8")]
for r in rows[3:366]:
    if r.get("event") in ("choice", "system0", "repeat", "mode", "budget"):
        print(json.dumps(r)[:900])
