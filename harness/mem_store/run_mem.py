"""THE MEMORY-STORE COMPARE (the reviewer 2026-10-19 07:35: the build, S3): e4_stream.py on the NEW tree (wt_mem), seed
49b07888, sc25 only (--n-games 1), exactly 2 agent steps (--slice-steps 2), on a lineage COPY, PYTHONHASHSEED 0,
under the supervisor at its default ceiling, --max-s 1800, alone, DETACHED. One script, one flag:
--on sets TETHER_MEMORY_STORE=1 (was
in run_a3.py: TETHER_ONE_PASS=1); without it every arm is at its default.
argv: repo lineage_copy out_dir [--on] [--dry]"""
import os
import subprocess
import sys

sys.dont_write_bytecode = True
repo, lin, OUT = sys.argv[1:4]
ON, DRY = "--on" in sys.argv[4:], "--dry" in sys.argv[4:]
R = "C:/TETHER_RUNS/E4_2026-10-18"
PY = "C:/Users/Admin/Documents/GitHub/tether/.venv/Scripts/python.exe"
HERE = os.path.dirname(os.path.abspath(__file__))
assert not os.path.exists(os.path.join(OUT, "switch.tsv")), "the out dir already holds a stream"
assert os.path.abspath(lin) != os.path.abspath(f"{R}/lineage"), "a COPY, never the E4 lineage"
assert os.path.isdir(lin) and len([f for f in os.listdir(lin) if f.endswith(".json")]) == 54, "54 originals"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_") and k != "PYTHONMALLOC"}
ENV["PYTHONDONTWRITEBYTECODE"] = "1"
ENV["PYTHONHASHSEED"] = "0"
ENV["TETHER_MEMORY_STORE"] = "1" if ON else "0"   # both ways explicit: the default is ON (17:03)
os.makedirs(OUT, exist_ok=True)
CHILD = ([PY, "-B", "-c", "import lineage, sys; print('MEMORY_STORE', lineage._MEMORY_STORE, 'hashseed', "
          "__import__('os').environ.get('PYTHONHASHSEED'))"] if DRY else
         [PY, "-B", os.path.join(HERE, "e4_stream.py"), repo, OUT, "--seed", "49b07888", "--n-games", "1",
          "--slice-steps", "2", "--lineage", lin])
p = subprocess.run([PY, "-B", os.path.join(repo, "harness", "supervise.py"), "--out", os.path.join(OUT, "sup"),
                    "--watch-pid", str(os.getpid()), "--max-s", "60" if DRY else "1800", "--", *CHILD],
                   env=ENV, cwd=repo, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, check=False)
with open(os.path.join(OUT, "launcher.txt"), "w", encoding="utf-8") as fh:
    fh.write(f"supervisor exit {p.returncode} (the child's rc is in sup/sup.json); ON={ON}\n")
