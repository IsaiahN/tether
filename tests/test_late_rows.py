"""LATE_DECLARED'S REFUSALS AS ONE ROW PER HEAD (the reviewer 2026-11-04 r1163 FIX 1). The end-of-
Build-3 A/B's arm B wrote 280,725 late_refused rows on ls20: one ROUTE row per refused candidate.
Now a fit's refusals are counted and written as ONE row per declared head, with n; the tally
(_late_refused) is unchanged. Seconds: test_late_declared's fixture holding THREE translate terms.

MF-L1  three translate<x> terms refused at an add_n slot in one fit write ONE late_refused row,
       head translate, n 3, terms the three names (r1164: which, not only how many); tally 3
MF-L2  (the r1176 speed probe: 201,358 late_refused rows still, 82 of them collapsed) EVERY
       _library_fit call goes through _fit_counted -- three call sites in route called it directly,
       so their refusals were each still a row
The red is behavioural on 58b843a's tether.py (swapped in, run, restored): three rows, no n.
MF-L2's red is 1538cb5's tether.py: the three direct calls in route.

    python tests/test_late_rows.py
"""
from __future__ import annotations

import ast
import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import arc_predict  # noqa: E402
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402
from gamma import Term  # noqa: E402

TR = next(a for a in arc_predict.predict() if a.name == "translate")


def main():
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma([*env.atoms(), TR], game="late_rows_fixture"),
                      tether.Config(), ledger.Ledger())
    for _ in range(6):
        ag.step()
    slot = next(s for s in sorted(ag.slots) if ag.history(s))
    others = [s for s in sorted(ag.slots) if s != slot][:3]
    ag.slot_types = {**ag.slot_types, slot: "add_n", **dict.fromkeys(others, "DELTA")}
    ag.bound.pop(slot, None)
    ag._fit_none.pop(slot, None)
    terms = [ag.gamma.accept(Term((TR,), operand=o), seq=0, residual="fixture") for o in others]
    ag._left = lambda _t, _s, _h, **_k: 10.0
    ag._bits = lambda _x: 1.0
    ag._units_for = lambda _s: ()
    ag._rebindings = lambda t, _s, _g=None, _r=None: iter([t])
    ag._carry_credit = lambda *_a: False
    keep = (tether._may_bind, tether.retrieval.retrieve)
    try:
        tether._may_bind = lambda _c, _t: True
        tether.retrieval.retrieve = lambda *_a, **_k: iter([t.name for t in terms])
        n0 = len(ag.led.rows())
        before = sum((ag.__dict__.get("_late_refused") or {}).values())
        ag._fit_tier0(slot, None)
    finally:
        tether._may_bind, tether.retrieval.retrieve = keep
    rows = [r["detail"] for r in ag.led.rows()[n0:] if r.get("event") == "late_refused"]
    tally = sum((ag.__dict__.get("_late_refused") or {}).values()) - before
    assert tally == 3, ("MF-L1 premise: three refusals", tally, rows)
    assert len(rows) == 1 and rows[0].get("head") == "translate" and rows[0].get("n") == 3, (
        "MF-L1: N refusals write N rows, not one row with n", rows)
    assert rows[0].get("terms") == sorted(t.name for t in terms), ("MF-L1 terms (r1164)", rows)
    print(f"  MF-L1 3 refusals in one fit -> 1 row {{head {rows[0]['head']}, n {rows[0]['n']}}}; "
          f"tally +{tally}")
    with open(tether.__file__, encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    direct = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name != "_fit_counted":
            direct += [(node.name, c.lineno) for c in ast.walk(node)
                       if isinstance(c, ast.Call) and getattr(c.func, "attr", None)
                       == "_library_fit"]
    assert not direct, ("MF-L2: _library_fit called outside _fit_counted", direct)
    print("  MF-L2 every _library_fit call goes through _fit_counted")
    print("test_late_rows OK")


if __name__ == "__main__":
    main()
