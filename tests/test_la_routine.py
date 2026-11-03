"""P4 LA_ROUTINE (the reviewer 2026-11-02 r832 d): Agent._la_routine on a stub board.
  P-d   a gap closed by look-ahead's BECOME presses settles ONE routine whose kind form names no
        action and no coordinate -- intents over kind keys only; a trail holding a TOUCH with no
        subject has no kind form and is NOT formed (routine_not_formed, its reason).
  P-b'  the form binds back (_bind_form) on another board whose slots have the same kinds under
        other names: the method carries, not the presses. (Fewer steps on the second occurrence
        is Series B's reading, not a fixture's.)
  MUST-FAIL: a hypothesis that ends "stalled" forms nothing; with the arm OFF nothing forms.

    python tests/test_la_routine.py
"""
from __future__ import annotations

import json
import sys
from types import SimpleNamespace

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import interface as IFace  # noqa: E402
import ledger  # noqa: E402
import routine as Rt  # noqa: E402
import tether  # noqa: E402

A = tether.Agent


def board(names: tuple) -> SimpleNamespace:
    ag = SimpleNamespace(slots=[f"{o}.{a}" for o in names for a in ("x", "y")], routines=[],
                         led=ledger.Ledger(None), cycle=3, _la_trail=None,
                         _objs_named=A._objs_named)
    ag._kind_key = lambda s: "K." + s.split(".", 1)[1]
    ag._kind = lambda o: ("obj", o[-1])
    ag._routine_form = lambda r: A._routine_form(ag, r)
    ag._bind_form = lambda x, slots, objs: A._bind_form(ag, x, slots, objs)
    return ag


def end(trail: list, why: str, on: bool = True) -> SimpleNamespace:
    tether._LA_ROUTINE = on
    try:
        ag = board(("o1", "o2"))
        ag._la_trail = ("h", trail)
        A._la_routine(ag, {"key": "h", "slots": ["o1.x"]}, why)
        return ag
    finally:
        tether._LA_ROUTINE = True


def main():
    assert tether._LA_ROUTINE, "ON by default"
    up = [IFace.Intent(IFace.BECOME, "o1.x", "+"), IFace.Intent(IFace.BECOME, "o1.x", "+"),
          IFace.Intent(IFace.BECOME, "o2.y", "-")]
    ag = end(up, "arrived_no_clear")
    assert len(ag.routines) == 1, ("P-d: the closing presses settle one routine", ag.routines)
    row = [r for r in ag.led.rows() if r["event"] == "routine_formed"][0]["detail"]
    form = json.loads(row["form"])
    text = row["form"]
    assert "ACTION" not in text and "coord" not in text and "K.x" in text, ("P-d: kinds only",
                                                                           text)
    touch = end([IFace.Intent(IFace.TOUCH, object="o2")], "level_cleared")
    nf = [r["detail"]["reason"] for r in touch.led.rows() if r["event"] == "routine_not_formed"]
    assert not touch.routines and nf and "no kind form" in nf[0], ("P-d: no subject, no form", nf)
    other = board(("o7", "o9"))
    back = A._bind_form(other, form, {"K.x": "o7.x", "K.y": "o9.y"}, {})
    first = back.first.action
    assert isinstance(back, Rt.Seq) and first.subject == "o7.x" and first.object == "+", (
        "P-b': binds back by kind on another board", back)
    assert not end(up, "stalled").routines, "MUST-FAIL: a stalled end forms nothing"
    assert not end(up, "arrived_no_clear", on=False).routines, "MUST-FAIL: OFF forms nothing"
    print(f"test_la_routine: 3 closing presses -> 1 routine {row['routine']}; its form names kinds"
          f" only; a subjectless TOUCH is not formed ({nf[0]}); bound back on o7/o9 as "
          f"{Rt.render(back)}; stalled / OFF form nothing")


if __name__ == "__main__":
    main()
