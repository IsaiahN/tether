"""Read-only (the reviewer r261): per game position, steps, first action, routed slots at step 1; Spearman of
position against first action and against steps; and r1 against r2 paired by game. argv: PLAY dir, rounds."""
import json
import sys

sys.dont_write_bytecode = True
B = "C:/TETHER_RUNS/S6_2026-10-19/" + sys.argv[1]


def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(x, y):
    rx, ry = ranks(x), ranks(y)
    n = len(x)
    mx, my = sum(rx) / n, sum(ry) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry, strict=True))
    vx = sum((a - mx) ** 2 for a in rx) ** 0.5
    vy = sum((b - my) ** 2 for b in ry) ** 0.5
    return cov / (vx * vy) if vx and vy else float("nan")


def read(rnd):
    g = {}
    for ln in open(f"{B}/{rnd}/switch.tsv", encoding="utf-8"):
        f = ln.rstrip("\n").split("\t")
        if len(f) > 17 and f[0].isdigit() and f[14] != "None":
            g[f[1]] = {"pos": int(f[0]), "c0": int(f[3]), "steps": int(f[5]), "first": float(f[14])}
    first_c = {v["c0"]: k for k, v in g.items()}
    routed = dict.fromkeys(g, 0)
    for ln in open(f"{B}/{rnd}/stream.jsonl", encoding="utf-8"):
        if '"event": "route"' not in ln:
            continue
        try:
            r = json.loads(ln)
        except ValueError:
            continue
        k = first_c.get(r.get("cycle"))
        if k is not None and r.get("event") == "route":
            routed[k] += 1
    for k in g:
        g[k]["routed1"] = routed[k]
    return g


rounds = {r: read(r) for r in sys.argv[2:]}
for rnd, g in rounds.items():
    names = sorted(g, key=lambda k: g[k]["pos"])
    print(f"== {rnd}: {len(names)} games")
    for k in names:
        v = g[k]
        print(f"  {v['pos']:>2} {k} steps {v['steps']:>2} first {v['first']:>6} routed@step1 {v['routed1']}")
    pos = [g[k]["pos"] for k in names]
    print(f"  Spearman position~first_action {spearman(pos, [g[k]['first'] for k in names]):+.2f}; "
          f"position~steps {spearman(pos, [g[k]['steps'] for k in names]):+.2f}; "
          f"routed@step1~first_action "
          f"{spearman([g[k]['routed1'] for k in names], [g[k]['first'] for k in names]):+.2f}")
if len(rounds) == 2:
    (r1, g1), (r2, g2) = rounds.items()
    both = sorted(set(g1) & set(g2))
    dpos = [g2[k]["pos"] - g1[k]["pos"] for k in both]
    dfirst = [g2[k]["first"] - g1[k]["first"] for k in both]
    print(f"== paired {r1}->{r2}: {len(both)} games; Spearman d(position)~d(first_action) "
          f"{spearman(dpos, dfirst):+.2f}")
    for k in both:
        print(f"  {k} pos {g1[k]['pos']}->{g2[k]['pos']} first {g1[k]['first']}->{g2[k]['first']} "
              f"steps {g1[k]['steps']}->{g2[k]['steps']}")
