"""E4b's launcher: e4b_box.py under harness/supervise.py --max-s MAX_S, this process the watched owner. Every TETHER_
variable stripped (the arms at the tree's defaults; the box names TETHER_AGENT_SEED 0 itself); PYTHONHASHSEED 0;
PYTHONDONTWRITEBYTECODE 1. THE NET (the reviewer 07:08 (i)): deadline_at = this process's clock, read immediately
before the supervisor starts, + MAX_S - MARGIN, so it is never later than sup_start + MAX_S - MARGIN. The lineage is the
REAL one, or (the dry runs) a folder under E4B/dry_*. launcher.txt records every number.
argv: tree lineage out max_s margin seed slice_min_s slice_max_s [n_games]"""
import json
import os
import subprocess
import sys
import time

sys.dont_write_bytecode = True
tree, lin, OUT, MAXS, MARGIN, SEED, MN, MX, *rest = sys.argv[1:]
NG = rest[0] if rest else "25"
PY = "C:/Users/Admin/Documents/GitHub/tether/.venv/Scripts/python.exe"
L = lin.replace("\\", "/")
assert L == "C:/TETHER_RUNS/E4_2026-10-18/lineage" or L.startswith("C:/TETHER_RUNS/S6_2026-10-19/E4B/dry_"), L
assert float(MAXS) > float(MARGIN) > 0 and 0 < float(MN) <= float(MX), (MAXS, MARGIN, MN, MX)
assert not os.path.exists(os.path.join(OUT, "stream.jsonl")), "the out dir already holds a stream"
os.makedirs(OUT, exist_ok=True)
ENV = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_") and k != "PYTHONMALLOC"}
ENV.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0")
BOX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "e4b_box.py")
t_launch = time.time()
deadline_at = t_launch + float(MAXS) - float(MARGIN)
CHILD = [PY, "-B", BOX, tree, OUT, "--seed", SEED, "--lineage", lin, "--slice-min-s", MN, "--slice-max-s", MX,
         "--deadline-at", repr(deadline_at), "--n-games", NG]
rec = {"t_launch": t_launch, "max_s": float(MAXS), "margin_s": float(MARGIN), "deadline_at": deadline_at,
       "deadline_after_launch_s": round(deadline_at - t_launch, 1), "child": CHILD, "tree": tree, "lineage": lin}
with open(os.path.join(OUT, "launcher.txt"), "w", encoding="utf-8", newline="\n") as fh:
    json.dump(rec, fh, indent=1)
p = subprocess.run([PY, "-B", os.path.join(tree, "harness", "supervise.py"), "--out", os.path.join(OUT, "sup"),
                    "--watch-pid", str(os.getpid()), "--max-s", MAXS, "--", *CHILD],
                   env=ENV, cwd=tree, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, check=False)
with open(os.path.join(OUT, "launcher.txt"), "a", encoding="utf-8", newline="\n") as fh:
    fh.write(f"\nsupervise rc {p.returncode} at {time.time():.1f}\n")
sys.exit(p.returncode)
