"""SHAPE A (the reviewer 2026-10-30 r464 3): ONE process, ONE agent, the games the Arcade lists, in its order, back to
back -- harness/mem_store/e4_stream.py with --games arcade, run here through runpy so that, however the life ends, the
scorecard its games were played on is CLOSED afterwards (the close is what scores every listed game). Harness only:
nothing in the agent. Seeds as PLAY's box: PYTHONHASHSEED 0 from the launcher, TETHER_AGENT_SEED 0 here.
Writes <out>/kaggle_a.json: rc, the error if any, each card closed and what the close returned.
argv: code out lineage slice_min_s slice_max_s deadline_at [n_games]"""
import json
import os
import runpy
import sys
import time
import traceback

sys.dont_write_bytecode = True
CODE, OUT, LIN, MN, MX, DL, *rest = sys.argv[1:]
assert os.environ.get("PYTHONHASHSEED") == "0", "the hash seed must be pinned by the launcher"
os.environ["TETHER_AGENT_SEED"] = "0"
os.makedirs(OUT, exist_ok=True)
os.makedirs(LIN, exist_ok=True)
sys.path.insert(0, CODE)

import arc_agi  # noqa: E402

MADE = []


class _Kept(arc_agi.Arcade):
    """The Arcade e4_stream makes, kept so its card can be closed after the life."""

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        MADE.append(self)


arc_agi.Arcade = _Kept
STREAM = os.path.join(CODE, "harness", "mem_store", "e4_stream.py")
sys.argv = [STREAM, CODE, OUT, "--games", "arcade", "--lineage", LIN, "--slice-min-s", MN, "--slice-max-s", MX,
            "--deadline-at", DL] + (["--n-games", rest[0]] if rest else [])
rec = {"argv": sys.argv, "t_start": time.time(), "error": None, "cards": []}
rc = 0
try:
    runpy.run_path(STREAM, run_name="__main__")
except BaseException as e:   # noqa: BLE001 -- every ending, SystemExit included, still closes the card
    rc = 1
    rec["error"] = "".join(traceback.format_exception(type(e), e, e.__traceback__))
finally:
    for a in MADE:
        card = getattr(a, "_default_scorecard_id", None)
        if card is None:
            continue
        try:
            sc = a.close_scorecard(card)
            dump = sc.model_dump(mode="json") if hasattr(sc, "model_dump") else repr(sc)
            rec["cards"].append({"card": card, "closed": dump})
        except Exception as e:   # noqa: BLE001
            rc = 1
            rec["cards"].append({"card": card, "close_error": repr(e)})
    rec["t_end"] = time.time()
    with open(os.path.join(OUT, "kaggle_a.json"), "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1, default=repr)
print(f"kaggle_a rc {rc}; cards closed {len(rec['cards'])}; error {'yes' if rec['error'] else 'no'}", flush=True)
sys.exit(rc)
