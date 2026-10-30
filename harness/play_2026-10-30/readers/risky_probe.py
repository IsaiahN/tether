"""Read-only: item 6 as proposed. Each settle row (slot, held_out_cycle) joined to the PERCEIVE bet row of that
slot at that cycle: risky iff the bet predicted a value other than its from_value (persistence would have said
from_value), and the ground agreed (actual == predicted). argv: play dir, rounds."""
import collections, json, sys
sys.dont_write_bytecode = True
for n in sys.argv[2:]:
    f = f"{sys.argv[1]}/round_{int(n):02d}/stream.jsonl"
    bets, sets = {}, []
    for ln in open(f, encoding="utf-8"):
        if '"event": "bet"' in ln and '"step": "PERCEIVE"' in ln:
            r = json.loads(ln); bets[(r["cycle"], r["slot"])] = r["detail"]
        elif '"event": "settle"' in ln:
            r = json.loads(ln); sets.append((r["slot"], r["detail"]))
    c = collections.Counter()
    for s, d in sets:
        b = bets.get((d.get("held_out_cycle"), s))
        if b is None or "actual" not in b:
            c["no scored bet at the held-out cycle"] += 1
        elif b.get("predicted") != b.get("from_value"):
            c["risky: predicted a change" + (", held" if b["actual"] == b.get("predicted") else ", NOT held")] += 1
        else:
            c["not risky: predicted no change"] += 1
    print(f"round {n}: settles {len(sets)}: {dict(c)}")
