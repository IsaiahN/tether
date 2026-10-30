"""The warm read over an explicit ledger list (the kept runs written after wall_s began, 2026-10-20 18:18):
per file the goal_hypotheses rows with wall_s; then per GAME (the first row's header game, else the file name)
the count, median and max, and the largest overall with its file and cycle. Background mode first. argv: list"""
import ctypes
import collections
import json
import os
import statistics
import sys

ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00100000)
files = [x.strip() for x in open(sys.argv[1], encoding="utf-8") if x.strip()]
per = collections.defaultdict(list)
nofield = collections.Counter()
for f in files:
    g = os.path.basename(f).split(".")[0]
    with open(f, encoding="utf-8") as fh:
        for ln in fh:
            if "goal_hypotheses" not in ln:
                continue
            r = json.loads(ln)
            if r.get("event") != "goal_hypotheses":
                continue
            d = r.get("detail") or {}
            if d.get("wall_s") is None:
                nofield[g] += 1
                continue
            per[g].append((d["wall_s"], f, r.get("cycle"), d.get("candidates"), d.get("checked"),
                           d.get("pick") is not None))
print(f"files {len(files)}; rows without wall_s by game: {dict(nofield)}")
best = None
for g, v in sorted(per.items()):
    w = [x[0] for x in v]
    top = max(v)
    print(f"{g}\trows {len(v)}\tmedian {statistics.median(w):.3f}\tp90 {sorted(w)[int(0.9 * (len(w) - 1))]:.3f}\t"
          f"max {top[0]:.3f} (cycle {top[2]}, candidates {top[3]}, checked {top[4]}, picked {top[5]}, "
          f"{top[1].replace('C:/TETHER_RUNS/', '')})")
    if best is None or top > best:
        best = top
print("LARGEST", best)
