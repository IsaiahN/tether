"""B4, BLOCKED, TETHER_RELATION_SET (the reviewer 2026-10-11 12:49 CDT): agent-side only --
never the world's own answer. A subject touching a partner before the step, which the agent's
OWN prediction moved into the partner (the boxes overlap), and which did not move, is blocked
by that partner; the stall cues the lookup to the settled S7 entries first.

  b1 o0 against o3, predicted into o3's cell, o0 unchanged -> one `blocked` row naming o3;
  b2-b4 MUST-FAILS: a free step (no contact before), the subject moved, a predicted move AWAY;
  b5 the cue: a blocked slot's lookup writes a `blocked_cue` row with the S7 keys;
  b6 a prediction carrying only the ROW (o0 above o3): the other sources hold their before
     values, so it still reads blocked (the reviewer 13:07 CDT, (i));
  b7 two partners in the target cell: ONE row naming both, sorted, and one cue ((ii));
  OFF: no derived slots, no `blocked` row, no cue.

    python tests/test_relation_blocked.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
from test_goal_condition import _agent
ag = _agent()
g = ag.env
st = dict(g.state)
r3, c3 = st["o3.row"], st["o3.col"]
taken = {(st[f"o{i}.row"], st[f"o{i}.col"]) for i in range(6) if i != 0}
side = -1 if (r3, c3 - 1) not in taken else 1        # a free cell beside o3 for o0
def before_at(c):
    s = dict(st); s["o0.row"], s["o0.col"] = r3, c
    return {**s, **g.derive(s)}
derived = g.derived()
def case(before, pred_set, after_set):
    pred = dict(before); pred.update(pred_set)
    after = dict(before); after.update(after_set)
    n0 = len(ag.led.rows())
    ag._blocked_reading(derived, pred, before, after, "A")
    rows = [r for r in ag.led.rows()[n0:] if r["event"] == "blocked"]
    return [[r["slot"], r["detail"]["partners"]] for r in rows]
b = before_at(c3 + side)
import relations
out = {"n_derived": len([k for k in derived if relations.pair_attr(k.split(".", 1)[1])])}
out["blocked"] = case(b, {"o0.col": c3}, {})
out["free"] = case(before_at(c3 + 3 * side), {"o0.col": c3 + 2 * side}, {})
out["moved"] = case(b, {"o0.col": c3}, {"o0.col": c3})
out["away"] = case(b, {"o0.col": c3 + 2 * side}, {})
up = -1 if (r3 - 1, c3) not in taken else 1
sv = dict(st); sv["o0.row"], sv["o0.col"] = r3 + up, c3
out["row_only"] = case({**sv, **g.derive(sv)}, {"o0.row": r3}, {})
s2 = dict(st); s2["o0.row"], s2["o0.col"] = r3, c3 + side
s2["o4.row"], s2["o4.col"] = r3, c3                  # a second partner in the target cell
out["two"] = case({**s2, **g.derive(s2)}, {"o0.col": c3}, {})
ag._blocked_now = {"o0.col": ("o3", "o4")}
n1 = len(ag.led.rows())
ag._library_reach("o0.col", "o0", g.slot_owner(), {"o0.col": ag.slot_types.get("o0.col")})
out["two_cue"] = len([r for r in ag.led.rows()[n1:] if r["event"] == "blocked_cue"])
ag._blocked_now = {"o0.col": ("o3",)}
n0 = len(ag.led.rows())
ag._library_reach("o0.col", "o0", g.slot_owner(), {"o0.col": ag.slot_types.get("o0.col")})
cue = [r for r in ag.led.rows()[n0:] if r["event"] == "blocked_cue"]
out["cue"] = [[r["detail"]["partners"], r["detail"]["keys"]] for r in cue]
print(json.dumps(out))
'''


def _run(on: bool) -> dict:
    env = dict(os.environ, TETHER_RELATION_SET="1" if on else "0", PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, "-c", PROBE], capture_output=True, text=True, env=env,
                       cwd=_repo.ROOT, timeout=300)
    assert p.returncode == 0, p.stderr[-2500:]
    return json.loads(p.stdout.strip().splitlines()[-1])


if __name__ == "__main__":
    off = _run(False)
    assert off["n_derived"] == 0 and not any(off[k] for k in ("blocked", "cue", "row_only",
                                                               "two", "two_cue")), off
    print("  OFF: no derived slots, no `blocked` row, no cue")
    on = _run(True)
    assert on["blocked"] == [["o0", ["o3"]]], on
    print(f"  b1 predicted into o3, did not move: {on['blocked']}")
    assert on["free"] == [] and on["moved"] == [] and on["away"] == [], on
    print("  b2-b4 free step / subject moved / predicted away: no `blocked` row")
    assert on["cue"] == [[["o3"], ["HUMAN|Solidity", "HUMAN|Collide", "ADHERENCE|Obstacle"]]], on
    print(f"  b5 the lookup is cued: {on['cue']}")
    assert on["row_only"] == [["o0", ["o3"]]], on
    print(f"  b6 a row-only prediction still reads blocked: {on['row_only']}")
    assert on["two"] == [["o0", ["o3", "o4"]]] and on["two_cue"] == 1, on
    print(f"  b7 two partners: {on['two']}, one cue")
    print("relation blocked: OK")
