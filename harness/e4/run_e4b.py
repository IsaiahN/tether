"""E4b LAUNCHER (Isaiah 2026-10-18 14:21-14:23; the reviewer 14:24, 17:05 2a, 17:16): the 25 public games as ONE
agent life, a seeded random order (the stream driver draws and records the seed), 120 s each, at least one full
move each (a move is never cut), no boundary signal at a switch, the lineage carried on from E4a's folder. One
game process under the supervisor; this launcher is the watch pid. Launch DETACHED (Start-Process, no wait).
argv: repo max_s"""
import os
import subprocess
import sys

sys.dont_write_bytecode = True
repo, max_s = sys.argv[1], sys.argv[2]
R = "C:/TETHER_RUNS/E4_2026-10-18"
OUT, LIN = f"{R}/stream", f"{R}/lineage"
PY = "C:/Users/Admin/Documents/GitHub/tether/.venv/Scripts/python.exe"
HERE = os.path.dirname(os.path.abspath(__file__))
assert not os.path.exists(os.path.join(OUT, "switch.tsv")), "E4b's out dir already holds a stream"
assert os.path.isdir(LIN) and os.listdir(LIN), "E4a's lineage folder is empty: E4b would start from the root"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
ENV["PYTHONDONTWRITEBYTECODE"] = "1"
ENV["PYTHONHASHSEED"] = "0"          # the reviewer 2026-10-19 00:22: every post-E4a run, recorded in the header
SEED = "49b07888"                    # E4b's order (e4b_seed.txt; the reviewer 23:21): the probe's 5 are its first 5
os.makedirs(OUT, exist_ok=True)
p = subprocess.run([PY, "-B", os.path.join(repo, "harness", "supervise.py"), "--out", os.path.join(OUT, "sup"),
                    "--watch-pid", str(os.getpid()), "--max-s", str(max_s), "--",
                    PY, "-B", os.path.join(HERE, "e4_stream.py"), repo, OUT, "--seed", SEED, "--slice-s", "120",
                    "--lineage", LIN],
                   env=ENV, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                   check=False)
with open(os.path.join(OUT, "launcher.txt"), "w", encoding="utf-8") as fh:
    fh.write(f"supervisor exit {p.returncode} (the child's rc is in sup/sup.json)\n")
