"""K0, launched (the reviewer 10:13 item 3): k0_pairs.py under the supervisor, as run_digest.py
at its default ceiling, --max-s 900, PYTHONHASHSEED 0, every TETHER_ variable stripped; --on sets TETHER_MEMORY_STORE=1.
argv: repo lineage_copy out_dir [--on]"""
import os
import subprocess
import sys

sys.dont_write_bytecode = True
repo, lin, OUT = sys.argv[1:4]
ON = "--on" in sys.argv[4:]
PY = "C:/Users/Admin/Documents/GitHub/tether/.venv/Scripts/python.exe"
HERE = os.path.dirname(os.path.abspath(__file__))
assert not os.path.exists(os.path.join(OUT, "k0")), "the out dir already holds a digest"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_") and k != "PYTHONMALLOC"}
ENV["PYTHONDONTWRITEBYTECODE"] = "1"
ENV["PYTHONHASHSEED"] = "0"
if ON:
    ENV["TETHER_MEMORY_STORE"] = "1"
os.makedirs(OUT, exist_ok=True)
CHILD = [PY, "-B", os.path.join(HERE, "k0_pairs.py"), repo, lin, os.path.join(OUT, "k0")]
p = subprocess.run([PY, "-B", os.path.join(repo, "harness", "supervise.py"), "--out", os.path.join(OUT, "sup"),
                    "--watch-pid", str(os.getpid()), "--max-s", "900", "--", *CHILD],
                   env=ENV, cwd=repo, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, check=False)
with open(os.path.join(OUT, "launcher.txt"), "w", encoding="utf-8") as fh:
    fh.write(f"supervisor exit {p.returncode}; ON={ON}\n")
