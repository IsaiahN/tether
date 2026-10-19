"""PROBE BASELINE (the reviewer 2026-10-18 23:42 item 2): per E4a game, the commit at the first move (~ just after
load) beside the lineage size at that game's start, from the sampler rows already on disk. READ ONLY.
  start         the supervisor's start line (sup.log)
  chain_gb      sum of lineage file sizes with mtime before start (decimal GB, 1e9 B); n_files beside it
  first_move_s  the first sampler row whose move count is >= 1 (the first move ENDED by then)
  commit_first  that row's commit (MiB and GiB)
  pre_move_max  the largest commit before that row (the load, plus the first move in flight)
  play_start_s  result.json's play_start_s (deadline_after_load games only), and the sampler commit nearest it
Fit commit_first_gib = a + b * chain_gb by least squares, on the games of the named head only. argv: e4_dir"""
import datetime
import glob
import json
import os
import sys

E4 = sys.argv[1]
LIN = os.path.join(E4, "lineage")
lin = [(os.path.getmtime(p), os.path.getsize(p)) for p in glob.glob(os.path.join(LIN, "*"))]
rows = []
for d in sorted(glob.glob(os.path.join(E4, "public", "[0-9][0-9]_*"))):
    idx, g = os.path.basename(d).split("_", 1)
    with open(os.path.join(d, "sup.log"), encoding="utf-8") as fh:
        first = fh.readline()
    start = datetime.datetime.strptime(first[:19], "%Y-%m-%d %H:%M:%S").timestamp()
    have = [s for t, s in lin if t < start]
    try:
        with open(os.path.join(d, f"{g}.commit.tsv"), encoding="utf-8") as fh:
            smp = [(float(a), int(b), int(c)) for a, b, c in (ln.rstrip("\n").split("\t")[:3] for ln in fh if ln.strip())]
    except OSError:
        smp = []
    fm = next((r for r in smp if r[2] >= 1), None)
    pre = max((r[1] for r in smp if fm and r[0] < fm[0]), default=None)
    ps, near = None, None
    try:
        with open(os.path.join(d, f"{g}.result.json"), encoding="utf-8") as fh:
            ps = json.load(fh).get("play_start_s")
    except (OSError, ValueError):
        pass
    if ps is not None and smp:
        near = min(smp, key=lambda r: abs(r[0] - ps))
    rows.append((int(idx), g, round(sum(have) / 1e9, 3), len(have), fm, pre, ps, near))
print("idx\tgame\tchain_gb\tn_files\tfirst_move_s\tcommit_first_mib\tcommit_first_gib\tpre_move_max_mib\t"
      "play_start_s\tcommit_near_play_start_mib(at s)")
for i, g, gb, n, fm, pre, ps, near in rows:
    print(f"{i}\t{g}\t{gb}\t{n}\t{fm[0] if fm else None}\t{fm[1] if fm else None}\t"
          f"{round(fm[1] / 1024, 2) if fm else None}\t{pre}\t{ps}\t{f'{near[1]} ({near[0]})' if near else None}")


def fit(sel, name):
    pts = [(gb, fm[1] / 1024) for i, g, gb, n, fm, pre, ps, near in rows if i in sel and fm]
    if len(pts) < 3:
        print(f"# fit {name}: {len(pts)} points, too few")
        return
    n = len(pts)
    mx, my = sum(x for x, _ in pts) / n, sum(y for _, y in pts) / n
    sxx = sum((x - mx) ** 2 for x, _ in pts)
    b = sum((x - mx) * (y - my) for x, y in pts) / sxx if sxx else float("nan")
    a = my - b * mx
    res = [y - (a + b * x) for x, y in pts]
    print(f"# fit {name}: n {n}, commit_first_gib = {a:.3f} + {b:.3f} x chain_gb; chain range "
          f"{min(x for x, _ in pts):.3f}-{max(x for x, _ in pts):.3f} GB; residuals "
          f"{', '.join(f'{r:+.2f}' for r in res)}")


fit(set(range(18, 25)), "7c77689 games (idx 18+)")
fit(set(range(0, 25)), "all games, both heads (a check, not the ask)")
