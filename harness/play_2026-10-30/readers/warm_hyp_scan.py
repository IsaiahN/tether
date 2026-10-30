"""C1-fix's warm read (the reviewer 2026-10-22 10:25 (2), 10:31), read-only: every "@goal goal_hypotheses" row
in the E4a public ledgers (the warm panel, played on the E4 lineage), per game: rows, rows with wall_s, the
median and max wall_s, the step (cycle) of the max, and the candidates/checked of that row; then the single
largest value overall. The process enters Windows background mode first (low CPU and I/O priority), since it
reads beside the 4d re-run. Only lines containing "goal_hypotheses" are parsed. argv: public_dir"""
import ctypes
import glob
import json
import os
import statistics
import sys

ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00100000)
root = sys.argv[1]
files = sorted(glob.glob(os.path.join(root, "*", "*.jsonl")))
files = [f for f in files if not f.endswith(".body.jsonl")]
assert files, root
print(f"ledgers {len(files)} under {root}")
best = None
for f in files:
    walls, rows, top = [], 0, None
    with open(f, encoding="utf-8") as fh:
        for ln in fh:
            if "goal_hypotheses" not in ln:
                continue
            r = json.loads(ln)
            if r.get("event") != "goal_hypotheses":
                continue
            rows += 1
            d = r.get("detail") or {}
            w = d.get("wall_s")
            if w is None:
                continue
            walls.append(w)
            if top is None or w > top[0]:
                top = (w, r.get("cycle"), d.get("candidates"), d.get("checked"), d.get("pick") is not None)
    g = os.path.basename(os.path.dirname(f))
    if walls:
        print(f"{g}\trows {rows}\twith_wall {len(walls)}\tmedian {statistics.median(walls):.3f}\t"
              f"max {top[0]:.3f} at cycle {top[1]} (candidates {top[2]}, checked {top[3]}, picked {top[4]})")
        if best is None or top[0] > best[0]:
            best = (top[0], g, top[1])
    else:
        print(f"{g}\trows {rows}\twith_wall 0")
print("LARGEST", best)
