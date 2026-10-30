"""T5c, launched (the reviewer 2026-10-19 09:36 item 3c): synth_prep.py once, then synth_ak.py in three separate
processes (s4, whole, stream), each alone under harness/supervise.py at its default ceiling, --max-s 900, with THIS
process's pid as the owner (a Git Bash $$ is not a Windows pid; the 09:43 attempt ended OWNER_GONE at 0 s and ran
nothing). Every TETHER_ variable stripped, PYTHONHASHSEED 0.
argv: repo ak_file out_dir"""
import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True
repo, AK, OUT = sys.argv[1:4]
PY = sys.executable      # the interpreter running this (r456: no machine path)
HERE = os.path.dirname(os.path.abspath(__file__))
ENV = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_") and k != "PYTHONMALLOC"}
ENV["PYTHONDONTWRITEBYTECODE"] = "1"
ENV["PYTHONHASHSEED"] = "0"
assert not os.path.exists(os.path.join(OUT, "out")), "the out dir already holds a run"
PKL = os.path.join(OUT, "counter.pkl")


def sup(tag: str, child: list) -> None:
    d = os.path.join(OUT, f"sup_{tag}")
    subprocess.run([PY, "-B", os.path.join(repo, "harness", "supervise.py"), "--out", d,
                    "--watch-pid", str(os.getpid()), "--max-s", "900", "--", PY, "-B", *child],
                   env=ENV, cwd=repo, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, check=False)
    with open(os.path.join(d, "sup.json"), encoding="utf-8") as fh:
        print(tag, json.dumps(json.load(fh)), flush=True)


os.makedirs(OUT, exist_ok=True)
if not os.path.exists(PKL):
    sup("prep2", [os.path.join(HERE, "synth_prep.py"), AK, PKL])
for m in ("s4", "whole", "stream"):
    sup(f"{m}2", [os.path.join(HERE, "synth_ak.py"), repo, PKL, os.path.join(OUT, "out"), m])
