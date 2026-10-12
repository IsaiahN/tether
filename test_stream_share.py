"""D2, TETHER_STREAM_SHARE (the reviewer 2026-10-12 05:43, 06:14, 06:19 CDT): within a round of
mint's search, the stream that has spent the least rank takes the next candidate, and a stream stops
at its OWN kind's floor.

  s4 the scheduler: OFF takes the first live stream whatever was spent; ON the least spent; ties to
     list order; a stopped stream is never offered. MUST-FAIL: max for min.
  s1 a synthetic mint (gridworld_s1 stepped, then one mint with the cap lowered so the predictor
     ALONE spends it), arm OFF: the objective makes 0 pays() calls. Read by a spy on pays() keyed
     by the stream holding the turn, so both arms are read with the same instrument.
  s2 the same mint, arm ON: the objective reaches pays() and stream_share["objective"]["rank"] > 0.
  s3 MUST-FAIL: ON with the scheduler patched to strict sequence -> the objective is back to 0.
  s5 the floor is per kind: a stream stops at its own kind's floor, never at another's. The
     predictor is put at the floor after its first candidate (the floor's champion lookup is
     spied): ON, the objective still takes turns and reaches pays(), and floor_stop is recorded
     for the predictor only. MUST-FAIL s5m: the lookup answering the shared best for every kind
     ends the objective too.

    python test_stream_share.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True

# Found by search over every slot at 2/4/6 cycles and caps 3000/15000, and pinned: on gridworld_s1
# after 6 steps, o5.distance at cap 3000 has the predictor spend the cap (1 pays) with the objective
# never asked; at 15000 the objective is reached (24 pays). Before 6 steps no slot calls pays().
SLOT, CAP, CYCLES = "o5.distance", 3000, 6

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
import gamma, ledger, tether, world
from conform import panel
SLOT, CAP, CYCLES, MODE = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
g, seed = panel._gridworld("gridworld_s1")
env = world.bind(g)
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"t_{seed}"), tether.Config(), ledger.Ledger())
for _ in range(CYCLES):
    ag.step()
tether._STREAM_SHARE = MODE != "off"
picked = [None]
orig_next, orig_pays = tether._next_stream, tether.pays
def ns(live, spent, share):
    r = live[0] if MODE == "strict" else orig_next(live, spent, share)
    picked[0] = r
    return r
counts = {}
def spy(*a):
    counts[picked[0]] = counts.get(picked[0], 0) + 1
    return orig_pays(*a)
tether._next_stream, tether.pays = ns, spy
ag.cfg.work_budget = CAP
ag._frontiers.pop(SLOT, None)
n0 = len(ag.led.rows())
ag.mint(SLOT)
row = next((r["detail"] for r in ag.led.rows()[n0:] if r["step"] == "MINT"), {})
print(json.dumps({"pays": {str(k): v for k, v in counts.items()},
                  "share": row.get("stream_share"),
                  "budget_exhausted": row.get("budget_exhausted")}))
'''

FLOOR = r'''
import json, sys
sys.dont_write_bytecode = True
import gamma, ledger, tether, world
from conform import panel
SLOT, CYCLES, MODE = sys.argv[1], int(sys.argv[2]), sys.argv[3]
g, seed = panel._gridworld("gridworld_s1")
env = world.bind(g)
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"t_{seed}"), tether.Config(), ledger.Ledger())
for _ in range(CYCLES):
    ag.step()
tether._STREAM_SHARE = True
# The predictor is put at the floor after its first candidate: the floor test's champion lookup
# answers a total of -inf for it. "floor" keeps every other kind's own champion (the ruling);
# "global", the mutant, answers that floored champion for EVERY kind -- a stop on the shared best.
FLOORED = (float("-inf"), 0.0, 0.0, None)
turns, pays_n, picked = {}, {}, [None]
orig_next, orig_pays, orig_fc = tether._next_stream, tether.pays, tether._floor_champion
def ns(live, spent, share):
    r = orig_next(live, spent, share)
    picked[0] = r
    turns[r] = turns.get(r, 0) + 1
    return r
def spy(*a):
    pays_n[picked[0]] = pays_n.get(picked[0], 0) + 1
    return orig_pays(*a)
def fc(by_kind, kind, best, share):
    if turns.get(0, 0) >= 1 and (kind == "predictor" or MODE == "global"):
        return FLOORED
    return orig_fc(by_kind, kind, best, share)
tether._next_stream, tether.pays, tether._floor_champion = ns, spy, fc
ag.cfg.work_budget = 3000
ag._frontiers.pop(SLOT, None)
n0 = len(ag.led.rows())
ag.mint(SLOT)
row = next((r["detail"] for r in ag.led.rows()[n0:] if r["step"] == "MINT"), {})
print(json.dumps({"turns": {str(k): v for k, v in turns.items()},
                  "pays": {str(k): v for k, v in pays_n.items()},
                  "want": row.get("want"), "share": row.get("stream_share")}))
'''


def _run(code: str, *args: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    here = os.path.dirname(os.path.abspath(__file__))
    out = subprocess.run([sys.executable, "-c", code, *args], cwd=here, env=env,
                         capture_output=True, text=True, timeout=600)
    assert out.returncode == 0, out.stderr[-2000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def _scheduler(nxt) -> bool:
    try:
        assert nxt([0, 1, 2], {0: 900, 1: 5, 2: 5}, False) == 0          # OFF: first live
        assert nxt([0, 1, 2], {0: 900, 1: 5, 2: 40}, True) == 1          # ON: least spent
        assert nxt([0, 1, 2], {0: 7, 1: 7, 2: 7}, True) == 0             # tie: list order
        assert nxt([1, 2], {0: 0, 1: 30, 2: 60}, True) == 1              # stopped 0 not offered
        return True
    except AssertionError:
        return False


def main() -> None:
    import tether
    assert _scheduler(tether._next_stream), "s4: the scheduler"
    assert not _scheduler(lambda live, spent, share: (
        max(live, key=lambda s: (spent[s], s)) if share else live[0])), "s4: max-for-min not caught"
    off = _run(PROBE, SLOT, str(CAP), str(CYCLES), "off")
    on = _run(PROBE, SLOT, str(CAP), str(CYCLES), "on")
    strict = _run(PROBE, SLOT, str(CAP), str(CYCLES), "strict")
    assert off["budget_exhausted"] and off["share"] is None, ("s1 precondition", off)
    assert off["pays"].get("0", 0) > 0 and off["pays"].get("1", 0) == 0, ("s1", off)
    ok = lambda r: r["pays"].get("1", 0) > 0 and (r["share"] or {}).get(          # noqa: E731
        "objective", {}).get("rank", 0) > 0
    assert ok(on), ("s2", on)
    assert on["share"]["objective"]["pays_called"] == on["pays"].get("1", 0), (
        "s2: the record's pays_called disagrees with the spy", on)
    assert not ok(strict), ("s3: the strict-sequence mutant was not caught", strict)
    fl = _run(FLOOR, SLOT, str(CYCLES), "floor")
    gl = _run(FLOOR, SLOT, str(CYCLES), "global")
    assert fl["turns"].get("0", 0) == 1 and fl["pays"].get("1", 0) > 0, ("s5", fl)
    assert fl["share"]["predictor"]["floor_stop"] == 1 and fl["share"]["objective"][
        "floor_stop"] is None, ("s5: floor_stop per kind", fl["share"])
    assert gl["turns"].get("1", 0) < fl["turns"].get("1", 0), ("s5m: global-stop mutant", gl, fl)
    print(f"test_stream_share: s4 scheduler + max-for-min caught; s1 OFF objective pays 0 "
          f"(predictor {off['pays'].get('0', 0)}); s2 ON objective pays {on['pays'].get('1', 0)}, "
          f"rank {on['share']['objective']['rank']}; s3 strict mutant caught; "
          f"s5 per-kind floor: objective turns {fl['turns'].get('1', 0)} vs global-stop mutant "
          f"{gl['turns'].get('1', 0)}")


if __name__ == "__main__":
    main()
