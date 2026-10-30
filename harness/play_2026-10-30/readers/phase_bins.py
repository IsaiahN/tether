"""r438 (a READ, no run): every phase of the step clock (the repeat rows' wall_s, one row per step) binned by cycle,
mean s per step per bin, and Spearman rho of each phase with the cycle -- so a climb is placed in PERCEIVE only or in
every phase. argv: round dir [round dir]."""
import json
import os
import sys

sys.dont_write_bytecode = True


def rank(xs):
    o = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    for k, i in enumerate(o):
        r[i] = k
    return r


def rho(a, b):                                   # read_a2's, copied (importing it runs its loop)
    ra, rb = rank(a), rank(b)
    n = len(a)
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb, strict=True))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
    return num / den if den else 0.0


for O in sys.argv[1:]:
    rows = {}
    with open(os.path.join(O, "stream.jsonl"), encoding="utf-8") as fh:
        for line in fh:
            if '"repeat"' not in line:
                continue
            r = json.loads(line)
            w = (r.get("detail") or {}).get("wall_s")
            if r.get("event") == "repeat" and isinstance(w, dict):
                rows[r.get("cycle")] = w
    cs = sorted(rows)
    ph = sorted({k for w in rows.values() for k in w}, key=lambda k: (k == "total", k))
    print(f"== {O}: {len(cs)} steps; phases {ph}")
    print("  rho with cycle: " + "  ".join(f"{k} {rho(cs, [rows[c].get(k, 0.0) for c in cs]):+.2f}" for k in ph))
    print("  bins (mean s per step): " + " ".join(f"{k:>8}" for k in ph))
    for b in range(0, len(cs), 12):
        bc = cs[b:b + 12]
        print(f"   c{bc[0]:3d}-{bc[-1]:3d}              "
              + " ".join(f"{sum(rows[c].get(k, 0.0) for c in bc) / len(bc):8.2f}" for k in ph))
