"""ONE child under harness/supervise.py (from the given repo) at its default ceiling, with THIS process's pid as the
owner (never a shell's $$), every TETHER_ variable stripped, PYTHONHASHSEED 0, PYTHONDONTWRITEBYTECODE 1; prints the
supervisor's sup.json. The pattern of run_digest.py / run_k0.py, with the child given on the command line.
argv: repo sup_dir max_s child_script [child args ...]"""
import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True
repo, SUP, MAXS, *CHILD = sys.argv[1:]
PY = "C:/Users/Admin/Documents/GitHub/tether/.venv/Scripts/python.exe"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_") and k != "PYTHONMALLOC"}
ENV["PYTHONDONTWRITEBYTECODE"] = "1"
ENV["PYTHONHASHSEED"] = "0"
assert not os.path.exists(os.path.join(SUP, "sup.json")), "the sup dir already holds a run"
subprocess.run([PY, "-B", os.path.join(repo, "harness", "supervise.py"), "--out", SUP,
                "--watch-pid", str(os.getpid()), "--max-s", MAXS, "--", PY, "-B", *CHILD],
               env=ENV, cwd=repo, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
               stderr=subprocess.DEVNULL, check=False)
with open(os.path.join(SUP, "sup.json"), encoding="utf-8") as fh:
    print("SUP", SUP, json.dumps(json.load(fh)), flush=True)
