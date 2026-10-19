"""Per E4a game with result.json: the sampler commit nearest each move's START, the count at or above the size-fold
line (SUP_CEILING / 2), and the size-fold rows in the body file. READ ONLY. argv: e4_dir"""
import glob
import json
import os
import sys

E4 = sys.argv[1]
LINE = 27.94 * 2**30 / 2 / 2**20       # MiB; the supervisor's ceiling / 2
print(f"# line {round(LINE)} MiB")
for d in sorted(glob.glob(os.path.join(E4, "public", "[0-9][0-9]_*"))):
    g = os.path.basename(d).split("_", 1)[1]
    try:
        r = json.load(open(os.path.join(d, f"{g}.result.json"), encoding="utf-8"))
    except OSError:
        continue
    smp = [(float(a), int(b)) for a, b, *_ in (ln.split("\t") for ln in open(os.path.join(d, f"{g}.commit.tsv")))]
    if r.get("play_start_s") is None:
        continue
    t, starts = r["play_start_s"], []
    for x in r["step_s"]:
        starts.append(min(smp, key=lambda s: abs(s[0] - t))[1])
        t += x
    body = os.path.join(d, f"{g}.jsonl.body.jsonl")
    size = sum('"trigger": "size"' in ln for ln in open(body, encoding="utf-8")) if os.path.exists(body) else None
    over = sum(c >= LINE for c in starts)
    print(f"{g}\tsteps {len(starts)}\tmax start MiB {max(starts)}\tstarts >= line {over}\tsize folds {size}")
