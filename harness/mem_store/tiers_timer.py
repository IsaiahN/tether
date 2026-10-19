"""K2's T2 TIME (the reviewer 2026-10-19 10:45 item 4): e4_stream.py UNCHANGED, with Agent._tiers wrapped to time
every call (perf_counter, wall) -- the call that holds T2 -- and the totals written to <out>/tiers_time.json at exit:
calls, total s, mean ms, max ms. Decisions are untouched: the wrapper returns what _tiers returns.
argv: e4_stream.py's own argv (repo out ...)"""
import atexit
import json
import os
import runpy
import sys
import time

sys.dont_write_bytecode = True
REPO, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path = [p for p in sys.path if "scratchpad" not in p]
sys.path.insert(0, REPO)
os.chdir(REPO)
import tether  # noqa: E402

T = {"calls": 0, "s": 0.0, "max_s": 0.0}
_real = tether.Agent._tiers


def _timed(self, *a, **k):
    t0 = time.perf_counter()
    try:
        return _real(self, *a, **k)
    finally:
        dt = time.perf_counter() - t0
        T["calls"] += 1
        T["s"] += dt
        T["max_s"] = max(T["max_s"], dt)


def _dump():
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "tiers_time.json"), "w", encoding="utf-8") as fh:
        json.dump({**T, "mean_ms": round(T["s"] / T["calls"] * 1e3, 3) if T["calls"] else None,
                   "max_ms": round(T["max_s"] * 1e3, 3)}, fh)


tether.Agent._tiers = _timed
atexit.register(_dump)
sys.argv = [os.path.join(HERE, "e4_stream.py"), *sys.argv[1:]]
runpy.run_path(sys.argv[0], run_name="__main__")
