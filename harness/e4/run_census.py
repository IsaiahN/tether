"""THE MEMORY-CENSUS RUN 1 (the reviewer 2026-10-19 02:52, 03:00): e4_stream.py on 7c77689, seed 49b07888, sc25 only
(--n-games 1), exactly 3 agent steps (--slice-steps 3), the sampled census at 4 between-step points (--census), on a
COPY of the E4 lineage, PYTHONHASHSEED 0, under the supervisor with --max-s 5400. Alone on the machine; DETACHED.
argv: repo lineage_copy [--dry]
--dry: the SAME env and supervisor, the child replaced by census_heap.dry (A4: the version and build, the allocator,
one malloc-stats capture parsed, the hash seed) into <out>_dry/dry.txt."""
import os
import subprocess
import sys

sys.dont_write_bytecode = True
repo, lin = sys.argv[1:3]
DRY = "--dry" in sys.argv[3:]
R = "C:/TETHER_RUNS/E4_2026-10-18"
OUT = f"{R}/census_run1" + ("_dry" if DRY else "")
PY = "C:/Users/Admin/Documents/GitHub/tether/.venv/Scripts/python.exe"
HERE = os.path.dirname(os.path.abspath(__file__))
assert not os.path.exists(os.path.join(OUT, "switch.tsv")), "the out dir already holds a stream"
assert os.path.abspath(lin) != os.path.abspath(f"{R}/lineage"), "the census must run on a COPY, never the E4 lineage"
assert os.path.isdir(lin) and os.listdir(lin), "the lineage copy is empty"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_") and k != "PYTHONMALLOC"}
ENV["PYTHONDONTWRITEBYTECODE"] = "1"
ENV["PYTHONHASHSEED"] = "0"          # the reviewer 2026-10-19 00:22: every post-E4a run, recorded in the header
os.makedirs(OUT, exist_ok=True)
CHILD = ([PY, "-B", "-c", "import sys; sys.path.insert(0, sys.argv[1]); import census_heap; "
          "census_heap.dry(sys.argv[2])", HERE, OUT] if DRY else
         [PY, "-B", os.path.join(HERE, "e4_stream.py"), repo, OUT, "--seed", "49b07888", "--n-games", "1",
          "--slice-steps", "3", "--census", "--lineage", lin])
p = subprocess.run([PY, "-B", os.path.join(repo, "harness", "supervise.py"), "--out", os.path.join(OUT, "sup"),
                    "--watch-pid", str(os.getpid()), "--max-s", "60" if DRY else "5400", "--", *CHILD],
                   env=ENV, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                   check=False)
with open(os.path.join(OUT, "launcher.txt"), "w", encoding="utf-8") as fh:
    fh.write(f"supervisor exit {p.returncode} (the child's rc is in sup/sup.json)\n")
