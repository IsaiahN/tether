"""Load (game start -> first step, a window from the 10 s sampler) against the carried chain's size at that
game's start (the reviewer 18:15: the fit to post when the load's lower bound passes 60 s). Read only.
Chain size at a game's start = the bytes of the lineage files whose mtime precedes the game folder's sup.log
start. argv: e4_dir"""
import glob
import json
import os
import sys

E4 = sys.argv[1]
files = [(os.path.getmtime(p), os.path.getsize(p)) for p in glob.glob(os.path.join(E4, "lineage", "*.json"))]
rows = []
for d in sorted(glob.glob(os.path.join(E4, "public", "[0-9][0-9]_*"))):
    g = os.path.basename(d).split("_", 1)[1]
    try:
        with open(os.path.join(d, f"{g}.result.json"), encoding="utf-8") as fh:
            s = json.load(fh).get("step_s") or []
        start = os.path.getmtime(os.path.join(d, "sup.log")) if False else os.path.getctime(
            os.path.join(d, f"{g}.commit.tsv"))
    except (OSError, ValueError):
        continue
    t0, t1 = 0.0, None
    with open(os.path.join(d, f"{g}.commit.tsv"), encoding="utf-8") as fh:
        for ln in fh:
            f = ln.split("\t")
            if len(f) < 3:
                continue
            if int(f[2]) == 0:
                t0 = float(f[0])
            elif t1 is None:
                t1 = float(f[0])
    if not s or t1 is None:
        continue
    lo, hi = max(0.0, t0 - s[0]), t1 - s[0]
    chain = sum(sz for mt, sz in files if mt < start)
    rows.append((g, round(chain / 2**20), round(lo, 1), round(hi, 1)))
print("game\tchain_MiB_at_start\tload_lo_s\tload_hi_s")
for r in rows:
    print("\t".join(str(x) for x in r))
pts = [(c, (lo + hi) / 2) for _g, c, lo, hi in rows if c > 0]
if len(pts) >= 2:
    n = len(pts)
    mx, my = sum(x for x, _ in pts) / n, sum(y for _, y in pts) / n
    b = sum((x - mx) * (y - my) for x, y in pts) / sum((x - mx) ** 2 for x, _ in pts)
    a = my - b * mx
    print(f"# least-squares on the window midpoints, games with a chain ({n}): load ~ {a:.1f} s + "
          f"{b * 1024:.1f} s per GiB of chain")
