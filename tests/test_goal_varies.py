"""GOAL CONDITIONS THAT COULD COME OUT THE OTHER WAY (TETHER_GOAL_VARIES, default ON; the reviewer
r1960; T0b lp85 cycle 16: 43,102 tied goal conditions, ~27 minutes in one step).
  V1  a reach history with met and unmet rows where one slot varies with the outcome: ON skips
      the conditions over constant slots before compiling them ("constant over the history"),
      every other text is handled as OFF handles it, and the pick is the same
  V2  all rows met: nothing is skipped (ON == OFF, condition for condition)
  V3  the cost: on a board with many constant slots, ON compiles a fraction of OFF's texts
  MF-V1 TETHER_GOAL_VARIES OFF: no "constant over the history" refusals -> RED as required
Seconds.
    python tests/test_goal_varies.py
"""
from __future__ import annotations

import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

KEY = "constant over the history: cannot tell met from unmet"


def agent():
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                      ledger.Ledger())
    ag.step()
    return ag


def history(ag, all_met=False):
    s0 = {k: v for k, v in ag.env.observe().items() if isinstance(v, int)}
    mover = next(k for k in sorted(s0) if k.endswith(".col") and k.startswith("o"))
    rows = []
    for t in range(8):
        st = dict(s0)
        st[mover] = t
        rows.append((st, all_met or t >= 5))
    return rows, mover


def run(on, all_met=False):
    tether._GOAL_VARIES = on
    ag = agent()
    rows, mover = history(ag, all_met)
    best, d = ag._goal_candidates(rows)
    return best, d, mover


def main() -> int:
    assert tether._GOAL_VARIES is True, "the arm defaults ON"
    b_on, d_on, mover = run(True)
    b_off, d_off, _m = run(False)
    tether._GOAL_VARIES = True
    skipped = d_on["refused"].get(KEY, 0)
    seen_on = sum(d_on["refused"].values()) + d_on["offered"]["plain"]
    seen_off = sum(d_off["refused"].values()) + d_off["offered"]["plain"]
    assert skipped > 0 and seen_on == seen_off, (d_on, d_off)
    assert (b_on and b_on[4]) == (b_off and b_off[4]), ("V1: the pick changed", b_on, b_off)
    print(f"V1 met and unmet rows: {skipped} of {seen_off} texts skipped before compiling "
          f"(slots constant over the history); the pick unchanged ({b_on and b_on[4]!r}): GREEN")
    assert KEY not in d_off["refused"], "MF-V1"
    print("MF-V1 the arm OFF: no 'constant over the history' refusals -> RED (as required)")

    _b, d_all_on, _m = run(True, all_met=True)
    _b, d_all_off, _m = run(False, all_met=True)
    tether._GOAL_VARIES = True
    assert d_all_on["conditions"] == d_all_off["conditions"] and KEY not in d_all_on["refused"]
    print(f"V2 all rows met: nothing skipped ({d_all_on['conditions']} = "
          f"{d_all_off['conditions']}): GREEN")

    share = (seen_off - skipped) / max(1, seen_off)
    assert share < 0.5, share
    print(f"V3 the cost: ON compiles {share:.0%} of OFF's texts on this board: GREEN")
    print("goal_varies: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
