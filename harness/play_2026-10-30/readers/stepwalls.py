"""Every ledger row that carries wall_s / step_s style fields, with cycle, slot, event. argv: ledger"""
import json
import sys

for ln in open(sys.argv[1], encoding="utf-8"):
    r = json.loads(ln)
    d = r.get("detail") or {}
    keys = {k: d[k] for k in d if any(w in k for w in ("wall", "step_s", "_s_", "elapsed", "clock", "secs"))}
    if keys or r.get("event") in ("clock", "step_time", "turn"):
        print(r.get("cycle"), r.get("slot"), r.get("event"), {k: v for k, v in list(keys.items())[:6]})
