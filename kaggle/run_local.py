"""THE NOTEBOOK, RUN HERE BEFORE ANY UPLOAD (the reviewer 2026-10-30 r464 3): a stand-in /kaggle/input holding the
dataset under one mount layout, a stand-in /kaggle/working, and a local gateway (kaggle/local_gateway.py) in place of
the competition's; then every code cell of the notebook, in order, in one namespace, as Jupyter would. Each cell's
start, end and outcome go to stdout. The game count is the gateway's.
    python kaggle/run_local.py NOTEBOOK DATASET_DIR WORK_DIR ENV_DIR PORT [--layout flat|nested] [--n-games N]
        [--no-rerun]
DATASET_DIR is kaggle/build_dataset.py's output; it is copied, not moved. --no-rerun runs the cells as a save run does
(no gateway, the dummy submission)."""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import traceback
import urllib.request

sys.dont_write_bytecode = True
ap = argparse.ArgumentParser()
for a in ("notebook", "dataset", "work", "env_dir"):
    ap.add_argument(a)
ap.add_argument("port", type=int)
ap.add_argument("--layout", choices=("flat", "nested"), default="nested")
ap.add_argument("--n-games", default=None)
ap.add_argument("--no-rerun", action="store_true")
# kaggle/build_lineage.py's output, MOUNTED (a junction; a link off Windows), never copied: the notebook's own copy into
# working is the one a Kaggle run makes too
ap.add_argument("--lineage-ds", default=None)
ap.add_argument("--cells", type=int, default=None)   # only the first N code cells (5: up to the lineage, no play)
A = ap.parse_args()
assert not os.path.exists(A.work), ("the work dir exists", A.work)
inp, working = os.path.join(A.work, "input"), os.path.join(A.work, "working")
mount = (os.path.join(inp, "tether-agent") if A.layout == "flat"
         else os.path.join(inp, "datasets", "owner", "tether-agent"))
shutil.copytree(A.dataset, mount)
if A.lineage_ds:
    lmount = os.path.join(os.path.dirname(mount), "tether-lineage")
    if os.name == "nt":
        import _winapi
        _winapi.CreateJunction(os.path.abspath(A.lineage_ds), lmount)
    else:
        os.symlink(os.path.abspath(A.lineage_ds), lmount, target_is_directory=True)
os.makedirs(working)
os.environ.update(NB_INPUT=inp, NB_WORKING=working, NB_GATEWAY=f"http://127.0.0.1:{A.port}")
os.environ.pop("KAGGLE_IS_COMPETITION_RERUN", None)
if A.n_games:
    os.environ["NB_N_GAMES"] = A.n_games
gw = None
if not A.no_rerun:
    os.environ["KAGGLE_IS_COMPETITION_RERUN"] = "1"
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(A.work, "gateway.log"), "w", encoding="utf-8") as log:   # the child holds its own handle
        gw = subprocess.Popen([sys.executable, "-B", os.path.join(here, "local_gateway.py"), A.env_dir,
                               os.path.join(A.work, "gateway_out"), str(A.port)], stdout=log,
                              stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
with open(A.notebook, encoding="utf-8") as fh:
    cells = [("".join(c["source"])) for c in json.load(fh)["cells"] if c["cell_type"] == "code"][:A.cells]
ns = {"__name__": "__main__"}
rc = 0
try:
    for i, src in enumerate(cells):
        t = time.time()
        print(f"===== CELL {i} START {time.strftime('%H:%M:%S')}", flush=True)
        try:
            exec(compile(src, f"<cell {i}>", "exec"), ns)
            print(f"===== CELL {i} OK {time.time() - t:.1f} s", flush=True)
        except Exception:
            print(f"===== CELL {i} FAILED {time.time() - t:.1f} s\n{traceback.format_exc()}", flush=True)
            rc = 1
            break
finally:
    if gw is not None:
        try:
            print("gateway healthcheck", urllib.request.urlopen(
                f"http://127.0.0.1:{A.port}/api/healthcheck", timeout=5).read(), flush=True)
        finally:
            gw.terminate()
            gw.wait(30)
sys.exit(rc)
