"""THE COUNTER'S PEAK ON THE LARGEST GAME (the reviewer 2026-10-19 08:26, 08:40 (b), 08:45 item 4). harness/game_one.py
UNCHANGED, with lineage.write_ak wrapped: at each memory save, BEFORE the real write_ak runs (so before the counter
clears), it records the counter's entries, the sum of its counts, the largest n, the n distribution (top 20), and
its bytes -- the dict container (sys.getsizeof) and the key tuples (sys.getsizeof per key; an UPPER bound on the
counter's own cost, since a key may be the same tuple object the slot memo holds) -- and the time the reading took.
Appended to <out>/counter_at_write.jsonl. Run with TETHER_MEMORY_STORE=1.
argv: game_one.py's own argv (--repo R --game G --cap-s S --out D --lineage L)"""
import collections
import json
import os
import runpy
import sys
import time

sys.dont_write_bytecode = True
REPO = sys.argv[sys.argv.index("--repo") + 1]
OUT = sys.argv[sys.argv.index("--out") + 1]
sys.path = [p for p in sys.path if "scratchpad" not in p]
sys.path.insert(0, REPO)
os.chdir(REPO)
import lineage  # noqa: E402

assert lineage._MEMORY_STORE, "run with TETHER_MEMORY_STORE=1"
_real = lineage.write_ak


def _measured(d, ag, h):
    t0 = time.perf_counter()
    c = ag._ak_asked
    rec = {"save": h, "entries": len(c), "sum_n": sum(c.values()), "max_n": max(c.values(), default=0),
           "n_dist_top20": sorted(collections.Counter(c.values()).items())[:20],
           "dict_bytes": sys.getsizeof(c), "key_tuple_bytes": sum(sys.getsizeof(k) for k in c)}
    rec["read_s"] = round(time.perf_counter() - t0, 3)
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "counter_at_write.jsonl"), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec) + "\n")
    return _real(d, ag, h)


lineage.write_ak = _measured
print("COUNTER_PROBE wraps lineage.write_ak", flush=True)
game_one = os.path.join(REPO, "harness", "game_one.py")
sys.argv = [game_one, *sys.argv[1:]]
runpy.run_path(game_one, run_name="__main__")
