"""P3 LOOK-AHEAD (the reviewer 2026-11-02 r832 c): tether.lookahead on a game-free model.
  P-a  the goal (x == 0) needs three presses in a fixed order, and the first makes the gap WORSE:
       "a" sets a mode and adds 1; "b" subtracts 2 only in that mode. From x = 3: a, b, b. A budget
       that reaches one press deep (greedy) finds nothing nearer than now (None); one that reaches
       three finds "a" first, depth 3, gap 3 -> 0.
  P-b  no predictor reads (predict -> None everywhere): None, never a guess.
  P-c  the budget is what stops it: more() is asked before every predicted press, and the count of
       presses predicted never exceeds what more() allowed.

    python tests/test_lookahead.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import tether  # noqa: E402


def model(st, a):
    x, m = st["x"], st["m"]
    if a == "a":
        return {"x": x + 1, "m": 1}
    return {"x": x - 2 if m else x, "m": m}


def run(budget: int, predict=model):
    calls = [0]

    def counted(st, a):
        calls[0] += 1
        return predict(st, a)
    got = tether.lookahead({"x": 3, "m": 0}, ("a", "b"), counted, lambda st: abs(st["x"]),
                           lambda: calls[0] < budget)
    return got, calls[0]


def main():
    assert tether._LOOKAHEAD and "lookahead" in tether._HYP_OWN_BY, "ON, and its press is own"
    greedy, g_calls = run(2)
    deep, d_calls = run(10_000)
    assert greedy is None, ("P-a MUST-FAIL: one press deep finds nothing nearer", greedy)
    assert deep == ("a", 3, 0, 3, ("a", "b", "b")), ("P-a: three deep, through a worse first",
                                                      deep)
    none, _ = run(10_000, predict=lambda _st, _a: None)
    assert none is None, ("P-b: nothing predicted, nothing chosen", none)
    assert g_calls <= 2 and d_calls <= 10_000, ("P-c: the budget bounds the presses", g_calls)
    print(f"test_lookahead: greedy ({g_calls} presses) -> None; look-ahead ({d_calls} presses) -> "
          f"{deep[:4]} by {deep[4]}; nothing predicted -> None")


if __name__ == "__main__":
    main()
