"""THE 26 s LOAD, SPLIT (the reviewer 2026-10-19 07:57 item 5 i). state_digest.py's set-up (the agent built over sc25
through arc_holdout.wire on a lineage COPY, nothing played), with wall-clock timers around the load's phases:
the store's open and catch_up, _store_view (the store read), Gamma.load_blob, Gamma.carry_used, Gamma.replay (the
evidence replay, with the length of what it replays), _store_index, _store_asked, the whole of lineage.load, and the
whole of wire(). The agent's own start-up = wire() minus lineage.load. Run with TETHER_MEMORY_STORE=1.
argv: repo lineage_copy out_json"""
import functools
import json
import os
import random
import sys
import time

sys.dont_write_bytecode = True
REPO, LIN, OUT = sys.argv[1:4]
sys.path = [p for p in sys.path if "scratchpad" not in p]
sys.path.insert(0, REPO)
os.chdir(REPO)
import arc_holdout  # noqa: E402, I001
import gamma  # noqa: E402
import lineage  # noqa: E402
import lineage_store  # noqa: E402
from arc_agi import Arcade  # noqa: E402

T: dict = {}


def timed(owner, name, label, size=None):
    f = getattr(owner, name)

    @functools.wraps(f)
    def w(*a, **k):
        t0 = time.perf_counter()
        try:
            return f(*a, **k)
        finally:
            r = T.setdefault(label, {"calls": 0, "s": 0.0})
            r["calls"] += 1
            r["s"] = round(r["s"] + time.perf_counter() - t0, 3)
            if size is not None:
                r["items"] = size(a, k)
    setattr(owner, name, w)


timed(lineage_store, "open_store", "store_open")
timed(lineage_store, "catch_up", "store_catch_up")
timed(lineage, "_store_view", "store_view (the store read)")
timed(gamma.Gamma, "load_blob", "gamma.load_blob")
timed(gamma.Gamma, "carry_used", "gamma.carry_used")
timed(gamma.Gamma, "replay", "gamma.replay (evidence)", size=lambda a, _k: len(a[1]) if len(a) > 1 else None)
timed(lineage, "_store_index", "store_index")
timed(lineage, "_store_asked", "store_asked")
timed(lineage, "load", "lineage.load (whole)")
timed(arc_holdout, "wire", "wire (whole)")
assert lineage._MEMORY_STORE, "run with TETHER_MEMORY_STORE=1"
games = sorted(os.listdir(os.path.join(REPO, "environment_files")))
first = random.Random("49b07888").sample(games, len(games))[0]
arc = Arcade(operation_mode=arc_holdout._mode())
arc_holdout.wire(arc.make(first), "stream", led_path=os.path.join(os.path.dirname(OUT), "phases.jsonl"),
                 lineage_dir=LIN)
w, ld = T["wire (whole)"]["s"], T["lineage.load (whole)"]["s"]
T["agent start-up (wire minus lineage.load)"] = {"s": round(w - ld, 3)}
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(T, fh, indent=1)
for k, v in T.items():
    print("PHASE", k, json.dumps(v), sep="\t", flush=True)
