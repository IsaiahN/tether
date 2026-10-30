"""T5b, launched (the reviewer 2026-10-19 07:12 c, 09:45 item 2): wal_probe.py alone under harness/supervise.py at its
default ceiling, --max-s 1800, with THIS process's pid as the owner. Every TETHER_ variable stripped.
argv: repo lineage_dir out_dir"""
import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True
repo, LIN, OUT = sys.argv[1:4]
PY = sys.executable      # the interpreter running this (r456: no machine path)
HERE = os.path.dirname(os.path.abspath(__file__))
ENV = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_") and k != "PYTHONMALLOC"}
ENV["PYTHONDONTWRITEBYTECODE"] = "1"
ENV["PYTHONHASHSEED"] = "0"
SUP = OUT + "_sup"
subprocess.run([PY, "-B", os.path.join(repo, "harness", "supervise.py"), "--out", SUP,
                "--watch-pid", str(os.getpid()), "--max-s", "1800", "--", PY, "-B",
                os.path.join(HERE, "wal_probe.py"), repo, LIN, OUT],
               env=ENV, cwd=repo, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
               stderr=subprocess.DEVNULL, check=False)
with open(os.path.join(SUP, "sup.json"), encoding="utf-8") as fh:
    print("wal", json.dumps(json.load(fh)), flush=True)
