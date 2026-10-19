"""The practice worlds' goal readings, from their ledgers after the fact (the reviewer 15:16). argv: out_dir"""
import json
import os
import sys
from collections import Counter

out = sys.argv[1]
print("world\tcycles\tfirst_want_cycle\tderived_wants_formed\tderived_asked\tg1_questions\tg1_wants\troutines\t"
      "routine_refused_top\tlevel_advances")
for m in ("gridworld_s0", "gridworld_s1", "gridworld_s2", "fake", "gridworld_arc_s0", "gridworld_arc_s1", "gridworld_arc_s2"):
    p = os.path.join(out, "practice", m, f"{m}.jsonl")
    rows = [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]
    ev = Counter(r.get("event") for r in rows)
    wants = [r["cycle"] for r in rows if (r.get("detail") or {}).get("want")]
    wo = {r["slot"] for r in rows if r.get("event") == "want_only" and (r.get("detail") or {}).get("want")}
    ref = Counter(str((r.get("detail") or {}).get("reason"))[:40] for r in rows if r.get("event") == "routine_refused")
    adv = sum(1 for r in rows if r.get("event") == "ending" and (r.get("detail") or {}).get("how") == "level_advance")
    print(f"{m}\t{max(r['cycle'] for r in rows)}\t{min(wants) if wants else None}\t{len(wo)}\t{ev.get('derived_asked', 0)}\t"
          f"{ev.get('g1', 0)}\t{ev.get('g1_want', 0)}\t{ev.get('routine', 0)}\t{ref.most_common(1)}\t{adv}")
