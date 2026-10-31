"""THE NOTEBOOKS' ONE SOURCE (corrections go here, never into the .ipynb): writes kaggle/tether_a.ipynb (shape A) and
kaggle/probe_machine.ipynb (the machine's cores, memory and interpreter, before shape B is designed; the reviewer
2026-10-30 r464 3). Every cell is plain Python, so kaggle/run_local.py runs the same cells here.
    python kaggle/make_notebook.py"""
import json
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))

PARAMS = '''\
import os
import sys
import time

T0 = time.time()
# the competition: a notebook runs at most 9 hours, internet off (the competition page, read 2026-10-30)
KAGGLE_WALL_S = 9 * 3600
# PLAY's whole-run margin (play_chain.sh: e4b_run.py ... 300); its end path measured 104-119 s (PLAY24 rounds 1-6)
MARGIN_S = 300
# today's slice rule (rule A, Isaiah 2026-10-23): Isaiah's to change, a parameter until he rules
SLICE_MIN_S, SLICE_MAX_S = 120, 300
INPUT = os.environ.get("NB_INPUT", "/kaggle/input")
WORKING = os.environ.get("NB_WORKING", "/kaggle/working")
GATEWAY = os.environ.get("NB_GATEWAY", "http://gateway:8001")
WHEELS = os.path.join(INPUT, "competitions", "arc-prize-2026-arc-agi-3", "arc_agi_3_wheels")
N_GAMES = os.environ.get("NB_N_GAMES")      # local runs only; on Kaggle every listed game is played
RERUN = bool(os.getenv("KAGGLE_IS_COMPETITION_RERUN"))
DEADLINE_AT = T0 + KAGGLE_WALL_S - MARGIN_S
print(f"T0 {T0:.1f} deadline_at {DEADLINE_AT:.1f} rerun {RERUN} slice {SLICE_MIN_S}/{SLICE_MAX_S} "
      f"input {INPUT} working {WORKING} gateway {GATEWAY} n_games {N_GAMES}")
'''

MACHINE = '''\
import platform
import shutil

mem = {}
if os.path.isfile("/proc/meminfo"):
    with open("/proc/meminfo") as fh:
        mem = {ln.split(":")[0]: ln.split(":")[1].strip() for ln in fh if ":" in ln}
cg = None
for p in ("/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"):
    if os.path.isfile(p):
        with open(p) as fh:
            cg = (p, fh.read().strip())
        break
print(f"python {sys.version.split()[0]} {platform.platform()}")
print(f"nproc os.cpu_count {os.cpu_count()} sched_getaffinity "
      f"{len(os.sched_getaffinity(0)) if hasattr(os, 'sched_getaffinity') else None}")
print(f"MemTotal {mem.get('MemTotal')} MemAvailable {mem.get('MemAvailable')} cgroup {cg}")
print(f"disk working free {shutil.disk_usage(WORKING if os.path.isdir(WORKING) else '.').free}")
'''

INSTALL = '''\
import importlib.metadata as md
import subprocess

if os.path.isdir(WHEELS):
    r = subprocess.run([sys.executable, "-m", "pip", "install", "--no-index", "--find-links", WHEELS,
                        "arc-agi", "python-dotenv"], capture_output=True, text=True)
    print(r.stdout[-2000:], r.stderr[-2000:])
    assert r.returncode == 0, "the offline install failed"
else:
    print(f"no wheelhouse at {WHEELS}: the interpreter's own packages are used")
for p in ("arc-agi", "arcengine", "numpy", "requests", "pydantic"):
    try:
        print(p, md.version(p))
    except md.PackageNotFoundError:
        print(p, "NOT INSTALLED")
'''

FIND = '''\
import glob
import hashlib
import json

MARK = "TETHER_KAGGLE_DATASET.json"
found = sorted(set(glob.glob(os.path.join(INPUT, "*", MARK))
                   + glob.glob(os.path.join(INPUT, "datasets", "*", "*", MARK))))
assert len(found) == 1, ("the dataset marker, under /kaggle/input/<slug> or /kaggle/input/datasets/<owner>/<slug>",
                         found)
DS = os.path.dirname(found[0])
with open(found[0]) as fh:
    META = json.load(fh)
print("dataset", DS, json.dumps(META))
CODE = os.path.join(WORKING, "tether")          # a writable copy: the input mount is read-only
assert not os.path.exists(CODE), ("a copy already exists", CODE)
shutil.copytree(os.path.join(DS, "code"), CODE)
with open(os.path.join(DS, "MANIFEST.sha256")) as fh:
    rows = [ln.rstrip("\\n").split("  ", 1) for ln in fh if ln.strip()]


def _sha(rel):
    with open(os.path.join(CODE, rel), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


bad = [rel for h, rel in rows if _sha(rel) != h]
assert len(rows) == META["files"] and not bad, ("the copy differs from the manifest", len(rows), bad[:5])
print(f"copied {len(rows)} files to {CODE}; every sha256 equals the manifest")
r = subprocess.run([sys.executable, "-B", "-c", "import tether, arc_holdout; print('agent imports ok')"],
                   cwd=CODE, capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
print(r.stdout[-1000:], r.stderr[-2000:])
assert r.returncode == 0, "the agent does not import on this interpreter"
'''

RUN = '''\
import urllib.request

OUT = os.path.join(WORKING, "run_a")
LIN = os.path.join(WORKING, "lineage")          # a fresh lineage: the learned one waits on Isaiah
if RERUN:
    t = time.time()
    while True:                                 # the gateway, as the competition's sample waits for it (600 s)
        try:
            n = len(json.loads(urllib.request.urlopen(GATEWAY + "/api/games", timeout=10).read()))
            break
        except Exception as e:
            assert time.time() - t < 600, ("the gateway never answered", repr(e))
            time.sleep(5)
    print(f"gateway up after {time.time() - t:.1f} s, listing {n} games")
    NO_ENVS = os.path.join(WORKING, "no_local_envs")   # empty: the Arcade's list is the gateway's alone
    os.makedirs(NO_ENVS, exist_ok=True)
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    # as the competition's sample sets them; the key is the sample's own placeholder, never ours
    env.update(OPERATION_MODE="online", ARC_BASE_URL=GATEWAY + "/", ARC_API_KEY="test-key-123",
               ENVIRONMENTS_DIR=NO_ENVS, RECORDINGS_DIR=os.path.join(WORKING, "recordings"),
               ONLY_RESET_LEVELS="true", PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1", MPLBACKEND="agg")
    cmd = [sys.executable, "-B", os.path.join(CODE, "kaggle", "run_a.py"), CODE, OUT, LIN,
           str(SLICE_MIN_S), str(SLICE_MAX_S), repr(DEADLINE_AT)] + ([N_GAMES] if N_GAMES else [])
    print("run", cmd)
    p = subprocess.run(cmd, env=env, cwd=CODE, stdin=subprocess.DEVNULL)
    print(f"run_a rc {p.returncode} wall {time.time() - T0:.1f} s since T0")
    for f in ("switch.tsv", "stream.result.json", "kaggle_a.json", "stream.traceback.txt"):
        f = os.path.join(OUT, f)
        if os.path.isfile(f):
            with open(f, encoding="utf-8") as fh:
                print("=====", f)
                print(fh.read()[-6000:])
'''

DUMMY = '''\
# Non-rerun mode: produce a dummy submission (the competition's sample, its import moved under the test: a rerun
# never needs pandas)
if not os.getenv('KAGGLE_IS_COMPETITION_RERUN'):
    import pandas as pd

    submission = pd.DataFrame(
        data=[['1_0', '1', True, 1]],
        columns=['row_id', 'game_id', 'end_of_game', 'score'])
    submission.to_parquet(os.path.join(WORKING, 'submission.parquet'), index=False)
'''


def nb(cells: list[tuple[str, str]]) -> dict:
    return {"cells": [{"cell_type": k, "metadata": {}, "source": s.splitlines(True),
                       **({"outputs": [], "execution_count": None} if k == "code" else {})} for k, s in cells],
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                         "language_info": {"name": "python"}},
            "nbformat": 4, "nbformat_minor": 5}


A = [("markdown", "# tether, shape A\nOne process, one agent, the games the gateway lists, in its order. "
                  "The code is the dataset's, copied and checked by sha256. No lineage is carried in yet.\n"),
     ("code", PARAMS), ("code", MACHINE), ("code", INSTALL), ("code", FIND), ("code", RUN), ("code", DUMMY)]
PROBE = [("markdown", "# machine probe\nCores, memory and interpreter of the submit machine; nothing is played.\n"),
         ("code", PARAMS), ("code", MACHINE), ("code", DUMMY)]

if __name__ == "__main__":
    for name, cells in (("tether_a.ipynb", A), ("probe_machine.ipynb", PROBE)):
        with open(os.path.join(HERE, name), "w", encoding="utf-8", newline="\n") as fh:
            json.dump(nb(cells), fh, indent=1)
            fh.write("\n")
        print("wrote", name)
