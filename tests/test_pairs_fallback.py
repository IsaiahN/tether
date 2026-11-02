"""(i) PAIRS_FALLBACK (the reviewer 2026-11-01 r747), on the fake world: singles first, pairs
only when no single pays.

  A reach history marked where one single condition holds (so that single pays): _goal_pairs is
  not called and that single is the pick. The history marked at one step only (no single pays):
  _goal_pairs is called. With the arm OFF _goal_pairs is called on the paying history too (the
  must-fail).

    python tests/test_pairs_fallback.py
"""
from __future__ import annotations

import math
import os
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")


def main():
    import arc_holdout
    import compile_term
    import tether
    from test_entry import FakeWrapper
    assert tether._PAIRS_FALLBACK, "the arm is ON by default"
    env, ag, _led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
    states = []
    for _ in range(20):
        states.append(dict(env.observe()))
        ag.step()
    n = len(states)
    once = [(st, i == n - 1) for i, st in enumerate(states)]
    _b, d1 = ag._goal_candidates(once)
    paying = None
    for x in d1["cheapest"] + [{"if": t} for t in ag._inv_conditions(states[-1])]:
        c = ag._compile_cache.get(x["if"])
        if c is None or isinstance(c, compile_term.Refusal):
            continue
        rows = [(st, compile_term.run(c, st) is True) for st in states]
        k = sum(h for _st, h in rows)
        if 0 < k < n and ag._goal_price([c], rows)[0] < k * math.log2(n):
            paying = rows        # exact on every row, so left is 0 and the cost alone decides
            break
    assert paying is not None, "occasions: no single condition can be made to pay"
    calls = []
    real = ag._goal_pairs

    def spy(singles, rows):
        calls.append(len(singles))
        return real(singles, rows)
    ag._goal_pairs = spy
    best, _d = ag._goal_candidates(paying)
    assert best is not None and not calls, ("a paying single: no pairs", best, calls)
    ag._goal_candidates(once)
    assert len(calls) == 1, ("no single pays: pairs are the fallback", calls)
    tether._PAIRS_FALLBACK = False
    try:
        calls.clear()
        ag._goal_candidates(paying)
    finally:
        tether._PAIRS_FALLBACK = True
    assert calls, "must-fail: with the arm OFF pairs are built beside a paying single"
    print(f"test_pairs_fallback: a paying single ({best[4]}) builds no pairs; none paying builds "
          f"them; OFF builds them beside the paying single")


if __name__ == "__main__":
    main()
