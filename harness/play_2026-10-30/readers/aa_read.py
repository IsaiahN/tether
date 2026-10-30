"""r437's PLAY23 round-1 read of arm 10 (a READ, no run): every arrival_alias row in the round's stream, whole, then
totals -- rows, left, with_form, aliases by form / by successor, kept / aliased / dormant / alias_collision -- and held /
dormant_held at the first and last row and their max. argv: round dir [round dir]."""
import json
import os
import sys

sys.dont_write_bytecode = True
F = ("left", "with_form", "aliases_by_form", "aliases_by_successor", "kept", "aliased", "dormant", "alias_collision")
for O in sys.argv[1:]:
    rows = []
    with open(os.path.join(O, "stream.jsonl"), encoding="utf-8") as fh:
        for line in fh:
            if '"arrival_alias"' not in line:
                continue
            r = json.loads(line)
            if r.get("event") == "arrival_alias":
                rows.append((r.get("cycle"), r["detail"]))
    print(f"== {O}: arrival_alias rows {len(rows)}")
    for c, d in rows:
        print(f"  c{c} break_at {d.get('break_at')} " + " ".join(f"{k} {d.get(k)}" for k in F)
              + f" held {d.get('held')} dormant_held {d.get('dormant_held')} alias {d.get('alias')}")
    if rows:
        tot = {k: sum(d.get(k) or 0 for _c, d in rows) for k in F}
        held = [d.get("held") or 0 for _c, d in rows]
        print("  TOTAL " + " ".join(f"{k} {v}" for k, v in tot.items())
              + f"; held first {held[0]} last {held[-1]} max {max(held)}; dormant_held last "
              f"{rows[-1][1].get('dormant_held')}")
