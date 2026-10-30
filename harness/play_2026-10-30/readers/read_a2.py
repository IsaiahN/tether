"""A2 (a READ, no run): per cycle, the repeat row's PERCEIVE and other wall beside what the one agent carries --
gamma_size, trace_len, outstanding (repeat row), bet and resolution rows written that cycle, and the highest object
id seen so far. Printed in bins of cycles, and Spearman rho of PERCEIVE against each. argv: round dir [round dir]."""
import collections
import json
import os
import re
import sys

sys.dont_write_bytecode = True
OID = re.compile(r'"o(\d+)[.~"]')


def rank(xs):
    o = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    for k, i in enumerate(o):
        r[i] = k
    return r


def rho(a, b):
    ra, rb = rank(a), rank(b)
    n = len(a)
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb, strict=True))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
    return num / den if den else 0.0


for O in sys.argv[1:]:
    rows, bets, res, top, maxid = {}, collections.Counter(), collections.Counter(), {}, 0
    with open(os.path.join(O, "stream.jsonl"), encoding="utf-8") as fh:
        for line in fh:
            for m in OID.finditer(line):
                maxid = max(maxid, int(m.group(1)))
            r = json.loads(line)
            c, e = r.get("cycle"), r.get("event")
            if e == "bet":
                bets[c] += 1
            elif e == "resolution":
                res[c] += 1
            elif e == "repeat" and isinstance((r.get("detail") or {}).get("wall_s"), dict):
                d = r["detail"]
                rows[c] = (d["wall_s"].get("PERCEIVE", 0.0), d["wall_s"].get("other", 0.0), d.get("gamma_size"),
                           d.get("trace_len"), d.get("outstanding"))
                top[c] = maxid
    cs = sorted(rows)
    per = [rows[c][0] for c in cs]
    cols = {"cycle": cs, "gamma_size": [rows[c][2] or 0 for c in cs], "trace_len": [rows[c][3] or 0 for c in cs],
            "outstanding": [rows[c][4] or 0 for c in cs], "bets": [bets[c] for c in cs],
            "resolutions": [res[c] for c in cs], "max_oid": [top[c] for c in cs],
            "other_s": [rows[c][1] for c in cs]}
    print(f"== {O}: {len(cs)} cycles")
    print("  Spearman rho of PERCEIVE per step with: "
          + "  ".join(f"{k} {rho(per, v):+.2f}" for k, v in cols.items()))
    print("  bins of cycles: PERCEIVE / other mean s; gamma_size, trace_len, outstanding, bets, resolutions, max_oid at "
          "the bin's last cycle")
    for b in range(0, len(cs), 12):
        bc = cs[b:b + 12]
        last = bc[-1]
        print(f"   c{bc[0]:3d}-{last:3d}  PERCEIVE {sum(rows[c][0] for c in bc) / len(bc):6.2f}  other "
              f"{sum(rows[c][1] for c in bc) / len(bc):5.2f}  gamma {rows[last][2]}  trace {rows[last][3]}  "
              f"outstanding {rows[last][4]}  bets/step {sum(bets[c] for c in bc) / len(bc):6.0f}  "
              f"res/step {sum(res[c] for c in bc) / len(bc):6.0f}  max_oid {top[last]}")
