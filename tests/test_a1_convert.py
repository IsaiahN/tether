"""C-A1-1, A1-CONVERT GROUP 1 (the reviewer 2026-10-15 09:12, 09:19, 09:33, 09:38; Isaiah 09:11,
09:27). WRITTEN, NOT RUN: it runs in the end-of-step-7 checklist.

  P1   frontier_pick's five steps, each the one that decides on a case built for it: gate, frontier
       (an axis no option reads is not an axis; None neither beats nor is beaten), residual,
       learning, draw; and the draw replays for the same key and options.
  P2   test_entry 217-219's properties under the agent's known-effect pick (the 10-06 test).
  A2   on a fake game with every A1 arm ON, every "choice" row names a site, a `by` in BY, and a
       pick consistent with its recorded readings: `gate` = the only option with residual > 0;
       `frontier` = a frontier of one; `residual` = the unique frontier maximum; `learning` = the
       unique least-seen among the residual ties; `draw` = a frontier member.
  MF-P MUST-FAIL: frontier_pick replaced by "the first option" (our order) fails P1.
  MF-A MUST-FAIL: with TETHER_A1_TIES=0 the interface's band pick is our index again
       (pick_by stays empty where P1's draw case would have recorded).

    python tests/test_a1_convert.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import frontier as FR  # noqa: E402


def p1(pick=FR.frontier_pick) -> None:
    # an empty list is refused by name, never reaches the draw's modulo (the reviewer 09:53 F2)
    try:
        pick([], None, None, "k")
    except ValueError as e:
        assert "no options" in str(e), e
    else:
        raise AssertionError("P1: frontier_pick([]) did not refuse")
    # gate: only one option bears on the open residual
    assert pick([("a", None, 1), ("b", None, 6)], {"a": 0, "b": 3}, None, "k")[:2] == ("b", "gate")
    # frontier: one option beats the other on the axis both read
    assert pick([("a", None, 1), ("b", None, 6)], None, None, "k")[:2] == ("a", "frontier")
    # an axis no option reads is not an axis; None neither beats nor is beaten
    n, by, front = pick([("a", None, None), ("b", None, 2)], None, {"a": 1, "b": 0}, "k")
    assert sorted(front) == ["a", "b"] and (n, by) == ("b", "learning"), (n, by, front)
    # residual: the frontier's larger residual reading
    assert pick([("a", 1, 1), ("b", 1, 1)], {"a": 1, "b": 2}, None, "k")[:2] == ("b", "residual")
    # draw: equal on everything; the same key and options replay the same pick
    d1 = pick([("a", None, None), ("b", None, None)], None, None, "k1")
    d2 = pick([("b", None, None), ("a", None, None)], None, None, "k1")
    assert d1[1] == "draw" and d1[0] == d2[0], (d1, d2)


def p2() -> None:
    import arc_holdout
    import interface as IF
    from test_entry import FakeWrapper
    ag = arc_holdout.wire(FakeWrapper(), "fake")[1]
    move, dead, restart = IF.CHANGES, IF.NO_EFFECT, IF.RESTARTS
    ag._attempt_actions = 5
    assert ag._choose_known([(restart, 0), (move, 3), (dead, 0)])[0] == 1
    assert ag._choose_known([(dead, 0), (restart, 0)])[0] == 1
    assert ag._choose_known([(move, 4), (move, 1)])[0] == 1
    # F3 (the reviewer 2026-10-15 10:42): a restart with nothing to throw away reaches nothing
    ag._attempt_actions = 0
    assert ag._choose_known([(restart, 0), (move, 0)])[0] == 1, "F3: a restart at the start won"


def a2(rows: list) -> int:
    seen = 0
    for r in rows:
        if r["event"] != "choice":
            continue
        d, seen = r["detail"], seen + 1
        assert d["by"] in FR.BY and d["site"], d
        front = [f[0] for f in d["frontier"]]
        res = d["residual"] or {}
        if d["by"] == "gate":
            assert [n for n, v in res.items() if v > 0] == [d["pick"]], d
        else:
            assert d["pick"] in front, d
        if d["by"] == "frontier":
            assert front == [d["pick"]], d
        if d["by"] in ("residual", "learning", "draw") and d["residual"] is not None:
            top = max(res[n] for n in front)
            tops = [n for n in front if res[n] == top]
            if d["by"] == "residual":
                assert tops == [d["pick"]], d
            else:
                assert d["pick"] in tops and len(tops) > 1, d
        if d["by"] in ("learning", "draw") and d["seen"] is not None:
            pool = ([n for n in front if res[n] == max(res[m] for m in front)]
                    if d["residual"] is not None else front)
            low = min(d["seen"][n] for n in pool)
            lows = [n for n in pool if d["seen"][n] == low]
            assert (lows == [d["pick"]]) if d["by"] == "learning" else (d["pick"] in lows), d
    return seen


def _child(arms: dict) -> list:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(arms)
    code = ("import json, sys; sys.dont_write_bytecode = True; import arc_holdout, tether_agent;"
            "from test_entry import FakeWrapper;"
            "env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), 'fake');"
            "[ag.step() for _ in range(30)];"
            "print('ROWS ' + json.dumps(led.rows(), default=repr));"
            "print('PICKBY ' + json.dumps(dict(ag.iface.pick_by)))")
    r = subprocess.run([sys.executable, "-B", "-c", code], env=env, capture_output=True,
                       text=True, check=False, stdin=subprocess.DEVNULL)
    assert r.returncode == 0, r.stderr[-3000:]
    out = dict(ln.split(" ", 1) for ln in r.stdout.splitlines() if ln[:5] in ("ROWS ", "PICKB"))
    return json.loads(out["ROWS"]), json.loads(out["PICKBY"])


def _our_order(opts, _res, _seen, _key):
    """MF-P's planted pick: the first option, our order. It refuses an empty list as
    frontier_pick does, so the must-fail reaches the cases it was written to fail (the reviewer
    2026-10-16 08:29: the bare lambda raised IndexError on p1's empty-list case first)."""
    if not opts:
        raise ValueError("no options")
    return opts[0][0], "frontier", [opts[0][0]]


def main() -> None:
    p1()
    print("  P1 the five steps each decide their case; the draw replays")
    p2()
    print("  P2 test_entry 217-219's properties hold under the agent's pick")
    rows, by = _child({})
    # THE PANEL PRECONDITION: MF-A below can only fire if the ON run had a tie for the interface
    # to pick; a run with none would make MF-A pass on nothing
    assert by, "precondition: no interface tie on this panel, so MF-A cannot discriminate"
    n = a2(rows)
    print(f"  A2 {n} choice rows consistent with their readings; interface pick_by {by}")
    try:
        p1(_our_order)
    except AssertionError:
        print("  MF-P must-fail fired: our order fails P1")
    else:
        raise AssertionError("MF-P MUST-FAIL did not fail")
    _rows, by_off = _child({"TETHER_A1_TIES": "0"})
    assert not by_off, ("MF-A MUST-FAIL did not fail: the interface still picked by frontier",
                        by_off)
    print("  MF-A must-fail fired: with A1_TIES OFF the interface records no frontier pick")
    print("a1 convert: OK")


if __name__ == "__main__":
    main()
