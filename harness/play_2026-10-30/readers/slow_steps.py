"""Read-only: per cycle of a round's stream.jsonl, the step clock's REPEAT row (wall_s per scope),
the step_mint / park wall_s, and the ask rows' wall_s -- for the cycles named. argv: stream, cycles."""
import json
import sys

sys.dont_write_bytecode = True
want = {int(c) for c in sys.argv[2].split(",")}
for ln in open(sys.argv[1], encoding="utf-8"):
    if '"cycle"' not in ln:
        continue
    if not any(f'"cycle": {c},' in ln for c in want):
        continue
    r = json.loads(ln)
    if r.get("cycle") not in want:
        continue
    e, d = r.get("event"), r.get("detail") or {}
    if e in ("repeat", "step_mint", "step_derived") or (e in ("park", "ask", "divide") and d.get("wall_s", 0) and d.get("wall_s", 0) > 5):
        keep = {k: v for k, v in d.items() if k not in ("reads",)}
        s = json.dumps(keep)[:600]
        print(r["cycle"], r["step"], r["slot"], e, s)
