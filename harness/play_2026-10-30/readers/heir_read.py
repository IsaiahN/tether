"""r442 (a READ): each arrival_alias heir against contingent(). No row writes contingent() itself; cascade_modes rows
(multi-frame cycles only) carry 'controlled' = the owners of contingent()'s slots (tether.py's _cascade_modes). For
each alias old -> new at cycle c: was old controlled at the last such row before c, and is new controlled at the first
such row after c (and how many cycles later). Also the break's successor for old, when the break row names one.
argv: round dir."""
import json
import os
import sys

sys.dont_write_bytecode = True
O = sys.argv[1]
cm, aliases = [], []
for ln in open(os.path.join(O, "stream.jsonl"), encoding="utf-8"):
    if '"cascade_modes"' in ln or '"arrival_alias"' in ln:
        r = json.loads(ln)
        d = r["detail"]
        if r["event"] == "cascade_modes" and d.get("controlled") is not None:
            cm.append((r["cycle"], set(d["controlled"])))
        elif r["event"] == "arrival_alias" and d.get("alias"):
            for o, n in d["alias"].items():
                aliases.append((r["cycle"], o, n))
print(f"== {O}: cascade_modes rows with 'controlled' {len(cm)}; aliases {len(aliases)}")
for c, o, n in aliases:
    before = [x for x in cm if x[0] < c]
    after = [x for x in cm if x[0] > c]
    b = before[-1] if before else None
    a = after[0] if after else None
    print(f"  c{c} {o} -> {n}: old controlled before (c{b[0] if b else None}): {o in b[1] if b else None} | "
          f"new controlled after (c{a[0] if a else None}, +{a[0] - c if a else None}): {n in a[1] if a else None} | "
          f"controlled then {sorted(a[1]) if a else None}")
