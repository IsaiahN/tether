"""E4b, THE BOX, WITH THE KIND-ROUTE SPY (the reviewer 2026-10-25 15:17 item 3): E4B/e4b_box.py unchanged except the three
lines after the import of arc_holdout, which install kind_spy.py (this directory, appended to sys.path, never ahead of the
tree) to write OUT/kind_spy.jsonl. No agent code changed.

E4b, THE BOX (Isaiah 2026-10-23 "i like c and then a", the cap "120"; the reviewer 06:29 B1-B6, 06:54, 07:08):
harness/mem_store/e4_stream.py at the tree's defaults, the agent's code untouched, one life over the 25 public games.
One harness-side wrap, nothing in the agent: arc_holdout.wire is wrapped to write <out>/load_report.json (the head the
load read, the library size after it, the lineage load report wire returns), PF's wrap; e4_stream writes its own
traceback (stream.traceback.txt). Agent seed 0 in-script; hash seed 0 from the launcher.
argv: e4_stream's (repo out --seed --lineage --slice-min-s --slice-max-s --deadline-at [--n-games])"""
import json
import os
import runpy
import sys

sys.dont_write_bytecode = True
ARGV = sys.argv[1:]
TREE, OUT = ARGV[0], ARGV[1]
os.environ["TETHER_AGENT_SEED"] = "0"
assert os.environ.get("PYTHONHASHSEED") == "0", "the hash seed must be pinned by the launcher"
assert not any(k.startswith("TETHER_") and k != "TETHER_AGENT_SEED" for k in os.environ), "a TETHER_ arm is set"
sys.path = [p for p in sys.path if "scratchpad" not in p]
sys.path.insert(0, TREE)
import arc_holdout
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import kind_spy
kind_spy.install(OUT)

_wire = arc_holdout.wire


def wire(*a, **k):
    out = _wire(*a, **k)
    _env, ag, _led, _board, _palette, loaded = out
    rec = {"lineage_parent": ag.lineage_parent, "library_n": len(ag.gamma.library),
           "loaded_lineage": (loaded or {}).get("lineage") if isinstance(loaded, dict) else None}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "load_report.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(rec, fh, default=repr, sort_keys=True, indent=1)
    return out


arc_holdout.wire = wire
sys.argv = [os.path.join(TREE, "harness", "mem_store", "e4_stream.py"), *ARGV]
runpy.run_path(sys.argv[0], run_name="__main__")
