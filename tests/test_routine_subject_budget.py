"""R-dir (c), TETHER_ROUTINE_SUBJECT_BUDGET (the reviewer 2026-10-11 10:39Z): a routine whose body
is one BECOME on one slot takes its budget, and the count it claims, from that subject's own gap
(the comment at the budget site: "the agent never proposes more reach than the gap needs";
routine.py:748, reach is expect else budget). Agent: the recorded gridworld_arc_s1 pair, o0.col
linked to o3.col.

  4. a signed want o0.col + at 2 toward o3.col 4 -> gap 2; a value want -> 1; no want, a non-BECOME
     want, or an unreadable target -> None (the group count stands);
  4'. at the mint (stubs named in _mint): budget ON is the subject gap (2), OFF the group count
     (3), and the claim handed to _expected follows it, so expect cannot exceed the budget;
  x. the STALE arm alone leaves the budget as OFF's; this arm alone writes no stale ending.

    python tests/test_routine_subject_budget.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
import interface as IFace
import routine as Rt
import tether
from test_goal_pair import ROWS
from test_gt_which import _linked

sys.dont_write_bytecode = True


def _gap(ag, want, st):
    ag._goal_want = want
    return ag._subject_gap(st)


def _mint(budget_on: bool, stale_on: bool, st: dict, series):
    """One mint under fixture STUBS, the same in every arm: CAN yes and a realiser serving the
    intent (this agent has watched no press move o0.col), and a six-member peer group so the
    group count (R x 6 = 3) differs from the subject gap (2). `_expected` is spied for the
    claim it is handed."""
    tether._WANT_TARGET = True
    tether._ROUTINE_SUBJECT_BUDGET, tether._ROUTINE_STALE = budget_on, stale_on
    try:
        ag = _linked()
        ag._res = {"o0.col": list(series)}
        ag.can = lambda _g, _s: "yes"
        ag.iface.realise = lambda *_a, **_k: IFace.Realisation("right", why="STUB")
        ag._group = lambda _sl, _s: tuple(range(6))
        claims, real = [], ag._expected

        def _spy(cand, unsat, before):
            claims.append(unsat)
            return real(cand, unsat, before)
        ag._expected = _spy
        n0 = len(ag.led.rows())
        ag._mint_routine(dict(st))
        return ag, ag.led.rows()[n0:], claims
    finally:
        tether._WANT_TARGET = tether._ROUTINE_SUBJECT_BUDGET = tether._ROUTINE_STALE = False


def _untils(r):
    out, todo = [], [r]
    while todo:
        x = todo.pop()
        if isinstance(x, Rt.Until):
            out.append(x)
        for f in ("body", "first", "then", "otherwise"):
            if hasattr(x, f):
                todo.append(getattr(x, f))
    return out


if __name__ == "__main__":
    base = dict(next(st for st, hit in ROWS if not hit), **{"o0.col": 2, "o3.col": 4})
    tether._WANT_TARGET = True
    try:
        ag = _linked()
        B = IFace.BECOME
        assert _gap(ag, IFace.Intent(B, "o0.col", "+"), base) == 2
        assert _gap(ag, IFace.Intent(B, "o0.col", value=4), base) == 1
        assert _gap(ag, None, base) is None
        assert _gap(ag, IFace.Intent("OTHER", "o0.col"), base) is None
        assert _gap(ag, IFace.Intent(B, "o0.col", "+"),
                    {k: v for k, v in base.items() if k != "o3.col"}) is None
    finally:
        tether._WANT_TARGET = False
    print("  4: signed 2, value 1, none/non-BECOME/unreadable -> None")
    near = []
    tether._WANT_TARGET = True
    try:
        a0 = _linked()
        near = [a0.goal_residual("o0.col", dict(base, **{"o0.col": c})) for c in (0, 1, 2)]
    finally:
        tether._WANT_TARGET = False
    on, on_rows, on_claims = _mint(True, False, base, near)
    off, off_rows, off_claims = _mint(False, False, base, near)
    st_only, st_rows, st_claims = _mint(False, True, base, near)
    sb = [r["detail"] for r in on_rows if r["event"] == "subject_budget"]
    assert sb and sb[0]["budget"] == 2 and sb[0]["group_budget"] == 3, sb
    assert not [r for r in off_rows if r["event"] == "subject_budget"]
    assert on_claims and set(on_claims) == {2}, on_claims
    assert off_claims and set(off_claims) == {3.0}, off_claims
    print(f"  4': mint ON budget {sb[0]['budget']} (group {sb[0]['group_budget']}), claim handed "
          f"to _expected {sorted(set(on_claims))}; OFF no row, claim {sorted(set(off_claims))}")

    def _no_arms(rows):
        return [r for r in rows if r["event"] != "arms"]
    assert _no_arms(st_rows) == _no_arms(off_rows) and st_claims == off_claims
    assert not [r for r in on_rows if r["event"] == "routine_end"
                and r["detail"].get("outcome") == "stale"]
    print("  x: STALE alone == OFF at the mint (rows and claim); the budget arm writes no stale")
    print("routine subject budget: OK")
