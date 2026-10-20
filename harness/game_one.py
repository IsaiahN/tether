import sys

sys.dont_write_bytecode = True   # first, before any other import (Isaiah 10-17 05:01)
# ruff: noqa: E402 -- every import follows the bytecode switch above
"""ONE ARC game offline under the PROCTOR'S wall cap (never in the codebase; Isaiah 10-13 20:38),
the lineage carried from the games before. Run it through harness/supervise.py, never bare.

    python -B harness/game_one.py --repo R --game G --cap-s S --out DIR
        [--cycles N] [--lineage L] [--saves V] [--profile] [--trace]

After the cap the agent's step is a no-op, so play() ends the run itself (end_run, the lineage
write) and the ending is CENSORED; a game win ends it too. Per game it records what E4 needs:
actions, seconds per action, levels and the time of each level change, peak commit, the error.
--profile samples the main thread's stack every 0.5 s (by function, inclusive, and by line);
--trace keeps tracemalloc (one frame) with a top-20 snapshot every 2 min and at 90% of the
supervisor's ceiling. Both are instruments on the harness side; the agent never reads them.
"""
import argparse
import collections
import contextlib
import ctypes
import ctypes.wintypes as wt
import faulthandler
import json
import os
import threading
import time
import tracemalloc

ap = argparse.ArgumentParser()
for a in ("--repo", "--game", "--out"):
    ap.add_argument(a, required=True)
ap.add_argument("--cap-s", type=float, required=True)
ap.add_argument("--cycles", type=int, default=2000)
ap.add_argument("--lineage")
ap.add_argument("--saves")
ap.add_argument("--profile", action="store_true")
ap.add_argument("--trace", action="store_true")
A = ap.parse_args()
os.makedirs(A.out, exist_ok=True)
sys.path = [p for p in sys.path if "scratchpad" not in p]
sys.path.insert(0, A.repo)
os.chdir(A.repo)
if A.trace:
    tracemalloc.start(1)
P = os.path.join(A.out, A.game)
_dumpfh = open(P + ".stacks.txt", "a")   # noqa: SIM115 -- held open for faulthandler
faulthandler.enable(_dumpfh, all_threads=True)
faulthandler.dump_traceback_later(A.cap_s + 840, file=_dumpfh)   # before the cap+15 stop

import arc_holdout  # noqa: E402
import tether  # noqa: E402

T0 = time.time()
DEADLINE = T0 + A.cap_s
CEILING = int(os.environ.get("SUP_CEILING", "0")) or None
st = {"censored": False, "won": False, "steps": 0, "actions": 0, "step_s": [], "levels": [],
      "peak_commit_mb": 0.0, "near_ceiling": False}


class PMC(ctypes.Structure):
    _fields_ = [("cb", wt.DWORD), ("PageFaultCount", wt.DWORD)] + [
        (n, ctypes.c_size_t) for n in (
            "PeakWorkingSetSize", "WorkingSetSize", "QuotaPeakPagedPoolUsage",
            "QuotaPagedPoolUsage",
            "QuotaPeakNonPagedPoolUsage", "QuotaNonPagedPoolUsage", "PagefileUsage",
            "PeakPagefileUsage", "PrivateUsage")]


_k32, _ps = ctypes.windll.kernel32, ctypes.windll.psapi
_k32.GetCurrentProcess.restype = wt.HANDLE
_ps.GetProcessMemoryInfo.argtypes = [wt.HANDLE, ctypes.POINTER(PMC), wt.DWORD]


def commit() -> tuple[int, int]:
    c = PMC()
    c.cb = ctypes.sizeof(c)
    _ps.GetProcessMemoryInfo(_k32.GetCurrentProcess(), ctypes.byref(c), c.cb)
    return int(c.PrivateUsage), int(c.PeakPagefileUsage)


_orig = tether.Agent.step


def _capped(self, *a, **k):
    if st["won"]:
        return False
    if time.time() > DEADLINE:
        st["censored"] = True
        return False
    st["steps"] += 1
    st["agent"] = self
    t = time.time()
    out = _orig(self, *a, **k)
    st["step_s"].append(round(time.time() - t, 2))
    if out:
        st["actions"] += 1
    try:
        lv = self.env.levels()[0]
        if not st["levels"] or st["levels"][-1][1] != lv:
            st["levels"].append((round(time.time() - T0, 1), lv, st["actions"]))
    except Exception:  # noqa: BLE001 -- a world without levels(): no level reading
        pass
    if self.env.terminal() == "game_win":
        st["won"] = True
    return out


tether.Agent.step = _capped

leaf: collections.Counter = collections.Counter()
incl: collections.Counter = collections.Counter()
samples = [0]
MAIN = threading.main_thread().ident


def sampler() -> None:
    while True:
        time.sleep(0.5)
        f = sys._current_frames().get(MAIN)
        if f is None:
            continue
        samples[0] += 1
        leaf[f"{os.path.basename(f.f_code.co_filename)}:{f.f_lineno} {f.f_code.co_name}"] += 1
        seen = set()
        while f is not None:
            seen.add(f"{os.path.basename(f.f_code.co_filename)}:{f.f_code.co_name}")
            f = f.f_back
        for s in seen:
            incl[s] += 1


def snapshot(why: str) -> None:
    with open(P + ".mem.txt", "a") as fh:
        cur, peak = commit()
        fh.write(f"=== {time.strftime('%H:%M:%S')} t={time.time() - T0:.0f}s {why} "
                 f"commit {cur / 2**20:.0f} MB actions {st['actions']}\n")
        sizes = {n: len(getattr(tether, n)) for n in dir(tether)
                 if n.startswith("_") and n == n.upper()
                 and isinstance(getattr(tether, n, None), (dict, set, list))}
        live = {k: v for k, v in sorted(sizes.items()) if v}
        fh.write("module stores (len): " + json.dumps(live) + "\n")
        fh.write("_INDEX_N: " + json.dumps(dict(getattr(tether, "_INDEX_N", {}))) + "\n")
        ag = st.get("agent")
        if ag is not None:
            big = {n: len(v) for n, v in list(vars(ag).items())
                   if isinstance(v, (dict, set, list)) and len(v) > 1000}
            fh.write("agent stores (len > 1000): " + json.dumps(dict(sorted(big.items()))) + "\n")
        if tracemalloc.is_tracing():
            traced, tpeak = tracemalloc.get_traced_memory()
            fh.write(f"traced {traced / 2**20:.0f} MB peak {tpeak / 2**20:.0f} MB\n")
            for s in tracemalloc.take_snapshot().statistics("lineno")[:20]:
                fh.write(f"  {s.size / 2**20:9.1f} MB {s.count:10d} blocks  {s.traceback[0]}\n")


def profile_dump() -> None:
    with open(P + ".prof.txt", "w") as fh:
        fh.write(f"samples {samples[0]} (0.5 s each)\n-- inclusive by function --\n")
        for k, n in incl.most_common(30):
            fh.write(f"  {n:6d} {100 * n / max(1, samples[0]):5.1f}%  {k}\n")
        fh.write("-- leaf by line --\n")
        for k, n in leaf.most_common(30):
            fh.write(f"  {n:6d} {100 * n / max(1, samples[0]):5.1f}%  {k}\n")


def watcher() -> None:
    last = time.time()
    while True:
        time.sleep(10)
        cur, _ = commit()
        st["peak_commit_mb"] = max(st["peak_commit_mb"], cur / 2**20)
        with open(P + ".commit.tsv", "a") as fh:
            fh.write(f"{time.time() - T0:.0f}\t{cur / 2**20:.0f}\t{st['actions']}\n")
        if CEILING and not st["near_ceiling"] and cur > 0.9 * CEILING:
            st["near_ceiling"] = True
            faulthandler.dump_traceback(_dumpfh, all_threads=True)
            with contextlib.suppress(MemoryError):
                snapshot("90% of the ceiling")
        if A.trace and time.time() - last >= 120:
            last = time.time()
            with contextlib.suppress(MemoryError):
                snapshot("every 2 min")
        if A.profile:
            profile_dump()


if A.profile:
    threading.Thread(target=sampler, daemon=True).start()
threading.Thread(target=watcher, daemon=True).start()

led = P + ".jsonl"
err = None
rep: dict = {}
try:
    rep = arc_holdout.play(A.game, A.cycles, led_path=led, lineage_dir=A.lineage,
                           save_only_dir=A.saves)
except MemoryError as e:
    err = f"MemoryError: {e}"[:400]
except Exception as e:  # noqa: BLE001 -- recorded; the lane goes on
    err = f"{type(e).__name__}: {e}"[:400]
faulthandler.dump_traceback(_dumpfh, all_threads=True)
if A.profile:
    profile_dump()
sp = st["step_s"]
out = {"game": A.game, "wall_s": round(time.time() - T0, 1), "cap_s": A.cap_s,
       "censored": st["censored"], "won": st["won"], "agent_steps": st["steps"],
       "actions": st["actions"], "s_per_step_mean": round(sum(sp) / len(sp), 1) if sp else None,
       "s_per_step_max": max(sp) if sp else None,
       "step_s": sp, "level_changes": st["levels"],
       "peak_commit_mb": round(max(st["peak_commit_mb"], commit()[1] / 2**20), 0), "error": err,
       "levels": rep.get("levels"), "endings": rep.get("endings"), "cycles": rep.get("cycles"),
       "gate": rep.get("gate"), "lineage": str((rep.get("persistence") or {}).get("lineage"))[:300]}
with open(P + ".result.json", "w") as fh:
    json.dump(out, fh, default=str)
print(json.dumps(out, default=str), flush=True)
