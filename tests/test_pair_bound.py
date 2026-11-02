"""E, PAIR_BOUND (lp85's first clear, 2026-11-01), on the fake world: a reach history with
one reached step makes every single "necessary", so every pair was priced.

  With the arm ON a pair whose cost alone exceeds the cheapest single's total is not priced: the
  pick and its total are identical to OFF, fewer pairs are priced, and the bounded count is
  recorded (the occasions check: some pair is bounded, else the test has no content).

    python tests/test_pair_bound.py
"""
from __future__ import annotations

import os
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")


def _history():
    import arc_holdout
    from test_entry import FakeWrapper
    env, ag, _led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
    states = []
    for _ in range(10):
        states.append(dict(env.observe()))
        ag.step()
    return ag, [(st, i == len(states) - 1) for i, st in enumerate(states)]


def main():
    import tether
    assert tether._PAIR_BOUND and tether._GOAL_PAIR, "the arms are ON by default"
    ag, rows = _history()
    on_best, on = ag._goal_candidates(rows)
    tether._PAIR_BOUND = False
    try:
        off_best, off = ag._goal_candidates(rows)
    finally:
        tether._PAIR_BOUND = True
    assert on["offered"]["pair_bounded"] > 0, ("occasions: no pair bounded", on["offered"])
    assert "pair_bounded" not in off["offered"], "OFF records no bound"
    assert (on_best is None) == (off_best is None), (on_best, off_best)
    if on_best is not None:
        assert (on_best[4], on_best[0]) == (off_best[4], off_best[0]), (on_best[:5], off_best[:5])
    assert on["cheapest"][0] == off["cheapest"][0], (on["cheapest"][:1], off["cheapest"][:1])
    assert on["offered"]["pair"] < off["offered"]["pair"], (on["offered"], off["offered"])
    print(f"test_pair_bound: {off['offered']['pair']} pairs priced OFF, {on['offered']['pair']} "
          f"ON ({on['offered']['pair_bounded']} bounded); the pick is identical "
          f"({on['cheapest'][0]['if']})")


if __name__ == "__main__":
    main()
