"""E4b's 5-GAME MEMORY PROBE (the reviewer 2026-10-18 23:21): e4_stream.py on 7c77689, the E4b seed (so its games
are E4b's first five), --n-games 5, --slice-s 120, on a COPY of the E4 lineage taken after game 25, under the
supervisor with a 90 min backstop (the reviewer 2026-10-19 00:32 (B); the 45 min of 23:21 was never priced against the
slice table). Alone on the machine, after E4a. Launch DETACHED. argv: repo seed lineage_copy [--dry]
--dry: the SAME env and supervisor, the child replaced by a print of PYTHONHASHSEED and sys.flags.hash_randomization
into <out>_dry/dry.txt (the reviewer 00:32 item 4: the hash seed is checked BEFORE launch)."""
import os
import subprocess
import sys

sys.dont_write_bytecode = True
repo, seed, lin = sys.argv[1:4]
DRY = "--dry" in sys.argv[4:]
R = "C:/TETHER_RUNS/E4_2026-10-18"
OUT = f"{R}/stream_probe" + ("_dry" if DRY else "")
PY = "C:/Users/Admin/Documents/GitHub/tether/.venv/Scripts/python.exe"
HERE = os.path.dirname(os.path.abspath(__file__))
assert not os.path.exists(os.path.join(OUT, "switch.tsv")), "the probe's out dir already holds a stream"
assert os.path.abspath(lin) != os.path.abspath(f"{R}/lineage"), "the probe must run on a COPY, never the E4 lineage"
assert os.path.isdir(lin) and os.listdir(lin), "the lineage copy is empty"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
ENV["PYTHONDONTWRITEBYTECODE"] = "1"
ENV["PYTHONHASHSEED"] = "0"          # the reviewer 2026-10-19 00:22: every post-E4a run, recorded in the header
os.makedirs(OUT, exist_ok=True)
CHILD = ([PY, "-B", "-c", "import os,sys; open(sys.argv[1],'w').write(f\"{os.environ.get('PYTHONHASHSEED')} "
          "{sys.flags.hash_randomization}\\n\")", os.path.join(OUT, "dry.txt")] if DRY else
         [PY, "-B", os.path.join(HERE, "e4_stream.py"), repo, OUT, "--seed", seed, "--slice-s", "120",
          "--n-games", "5", "--lineage", lin])
p = subprocess.run([PY, "-B", os.path.join(repo, "harness", "supervise.py"), "--out", os.path.join(OUT, "sup"),
                    "--watch-pid", str(os.getpid()), "--max-s", "60" if DRY else "5400", "--", *CHILD],
                   env=ENV, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                   check=False)
with open(os.path.join(OUT, "launcher.txt"), "w", encoding="utf-8") as fh:
    fh.write(f"supervisor exit {p.returncode} (the child's rc is in sup/sup.json)\n")
