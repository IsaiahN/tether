"""P3 LOOK-AHEAD (the reviewer 2026-11-02 r832 c): tether.lookahead on a game-free model.
  P-a  the goal (x == 0) needs three presses in a fixed order, and the first makes the gap WORSE:
       "a" sets a mode and adds 1; "b" subtracts 2 only in that mode. From x = 3: a, b, b. A budget
       that reaches one press deep (greedy) finds nothing nearer than now (None); one that reaches
       three finds "a" first, depth 3, gap 3 -> 0.
  P-b  no predictor reads (predict -> None everywhere): None, never a guess.
  P-c  the budget is what stops it: more() is asked before every predicted press, and the count of
       presses predicted never exceeds what more() allowed.
  P-r  REACHED IS COUNTABLE: Agent._lookahead_act with nothing settled on the subject chooses
       nothing and writes one lookahead_none row naming why.
  P-k  OFF THE BOARD IS "COULD NOT READ" (the reviewer 2026-11-03 r867; B1 sp80 c177, KeyError
       'o1617.rem_col'): the subject and a second slot are bound and settled, and the second is
       absent from the board. RED (118bf81) KeyError; GREEN one lookahead row naming it unread.
       The subject itself off the board: one lookahead_none "slot not on the board".

    python tests/test_lookahead.py
"""
from __future__ import annotations

import sys
from types import SimpleNamespace

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import ledger  # noqa: E402
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
    ag = SimpleNamespace(_hyp={"slots": ["o1.x"]}, bound={}, cycle=4, led=ledger.Ledger(None),
                         gamma=SimpleNamespace(library={}))
    ag._la_none = lambda *a: tether.Agent._la_none(ag, *a)
    got = tether.Agent._lookahead_act(ag, {})
    rows = [r["detail"]["why"] for r in ag.led.rows() if r["event"] == "lookahead_none"]
    assert got is None and rows == ["no settled predictor reads the subject"], (
        "P-r: reached, nothing chosen, one row naming why", got, rows)
    on = covered()
    got = tether.Agent._lookahead_act(on, {"o1.x": 3})
    la = [r["detail"] for r in on.led.rows() if r["event"] == "lookahead"]
    assert got == "A" and len(la) == 1 and la[0]["unread"] == ["o2.rem"], (
        "P-k MUST-FAIL: a settled slot off the board is unread, never a KeyError", got, la)
    off = covered()
    got = tether.Agent._lookahead_act(off, {"o2.rem": 1})
    why = [r["detail"]["why"] for r in off.led.rows() if r["event"] == "lookahead_none"]
    assert got is None and why == ["slot not on the board"], ("P-k: the subject off the board",
                                                             got, why)
    print(f"test_lookahead: greedy ({g_calls} presses) -> None; look-ahead ({d_calls} presses) -> "
          f"{deep[:4]} by {deep[4]}; nothing predicted -> None; reached with nothing settled -> "
          f"lookahead_none ({rows[0]}); a settled slot off the board -> unread {la[0]['unread']}; "
          f"the subject off the board -> lookahead_none ({why[0]})")


def covered():
    """P-k: o1.x (the subject) and o2.rem bound and settled; _predict indexes the board as
    _value_of does (state[slot]), so a slot off the board raises unless look-ahead skips it."""
    ag = SimpleNamespace(
        _hyp={"slots": ["o1.x"], "key": "k"}, bound={"o1.x": "t1", "o2.rem": "t2"}, cycle=9,
        led=ledger.Ledger(None), _pred_raw={}, _spent=0, actions=["A"], env=SimpleNamespace(),
        _withheld=(), _la_trail=None,
        gamma=SimpleNamespace(library={"t1": 1, "t2": 1}, is_settled=lambda _n, _s: True),
        iface=SimpleNamespace(realise=lambda w, *_a, **_k: SimpleNamespace(
            action="A", coord=(w.kind, w.subject, w.object), unmapped=False)))
    ag._objs_named = lambda s: [s.split(".")[0]]
    ag._predict = lambda s, st, _a: st[s] - 1
    ag._discrepancy = lambda s, st: abs(st[s]) if s in st else tether.NOT_RESOLVED
    ag._took = lambda real, _want: real.action
    ag._la_none = lambda *a: tether.Agent._la_none(ag, *a)
    ag._la_predict = lambda *a: tether.Agent._la_predict(ag, *a)   # 14b: the per-press step
    return ag


if __name__ == "__main__":
    main()
