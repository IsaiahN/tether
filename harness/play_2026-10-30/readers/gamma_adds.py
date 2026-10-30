"""Read-only (the reviewer r263 (a)): per cycle, Gamma's growth (REPEAT gamma_size, next minus this) against
each event's count in the cycle; the events whose counts track the growth are the adders."""
import collections
import json
import sys

sys.dont_write_bytecode = True
B = sys.argv[1]
gam, ev = {}, collections.defaultdict(collections.Counter)
for ln in open(f"{B}/stream.jsonl", encoding="utf-8"):
    try:
        r = json.loads(ln)
    except ValueError:
        continue
    c = r.get("cycle")
    if not isinstance(c, int):
        continue
    ev[c][(r.get("step"), r.get("event"))] += 1
    if r.get("event") == "repeat":
        gam[c] = (r.get("detail") or {}).get("gamma_size")
cs = sorted(gam)
delta = {c: gam[cs[i + 1]] - gam[c] for i, c in enumerate(cs[:-1])}
grow = [c for c in cs[:-1] if delta[c] > 0]
print(f"cycles {len(cs)}; gamma {gam[cs[0]]} -> {gam[cs[-1]]}; cycles with growth {len(grow)}; total growth "
      f"{sum(delta[c] for c in grow)}; shrink {sum(-delta[c] for c in cs[:-1] if delta[c] < 0)}")
keys = collections.Counter()
for c in cs[:-1]:
    keys.update(ev[c].keys())
rows = []
for k in keys:
    xs = [ev[c][k] for c in cs[:-1]]
    ds = [delta[c] for c in cs[:-1]]
    on_grow = sum(ev[c][k] for c in grow)
    n = len(xs)
    mx, md = sum(xs) / n, sum(ds) / n
    cov = sum((a - mx) * (b - md) for a, b in zip(xs, ds, strict=True))
    vx = sum((a - mx) ** 2 for a in xs) ** 0.5
    vd = sum((b - md) ** 2 for b in ds) ** 0.5
    rows.append((cov / (vx * vd) if vx and vd else 0.0, k, sum(xs), on_grow))
rows.sort(reverse=True)
print("top events by Pearson r with per-cycle gamma growth (r, step/event, total, in growth cycles):")
for r_, k, t, g in rows[:25]:
    print(f"  {r_:+.2f} {k} total {t} in-growth {g}")
