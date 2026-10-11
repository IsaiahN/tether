"""The cell tier (TETHER_REALISE_CELL; the reviewer 2026-10-11 09:53Z): a direction intent reads
each action's effect FROM THE CELL THE SLOT IS IN -- `lands` keyed (ctx, slot, before) -- before
today's mean-delta tiers. Data: o0.col's cell evidence rebuilt from run (C)'s ledger, c0-97
(gridworld_arc_s1, a wrapping board, 5 columns), as tests/fixtures/realise_cell_c97.json.

  m1: (C)'s c98 state (o0.col 2, want +) must NOT choose left; it is reported which it chooses
      and from which tier. The delta table carries left's wrap samples, so today's tiers
      reproduce c98's wrong press;
  m2: from column 0, want +, the chosen press moves o0.col in the + sign from 0 (a wrap is a
      legitimate +);
  m3: no cell evidence at the current value: ON and OFF pick the same;
  m4: a cell holding two values gives no direction from that cell;
  expected_move is unchanged by the arm (cell=False there, scope of the ruling).

    python test_realise_cell.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import interface as IFace

sys.dont_write_bytecode = True
CTX = ()
SLOT = "o0.col"
OFFERED = ("up", "down", "left", "right")
CELLS = json.loads((Path(__file__).parent / "tests" / "fixtures" / "realise_cell_c97.json")
                   .read_text(encoding="utf-8"))


def _iface(cells, delta):
    f = IFace.Interface()
    for key, vals in cells.items():
        a, before = key.split("|")
        e = f.table.setdefault(a, {})
        e.setdefault("lands", {})[(CTX, SLOT, int(before))] = set(vals)
    for a, (n, tot) in delta.items():
        f.table.setdefault(a, {}).setdefault("delta", {})[(CTX, SLOT, IFace.SELF)] = (n, tot)
    return f


def _pick(f, now, sign, on):
    was = IFace._REALISE_CELL
    IFace._REALISE_CELL = on
    try:
        r = f.realise(IFace.Intent(IFace.BECOME, SLOT, sign), OFFERED, CTX, {SLOT: now}, None)
    finally:
        IFace._REALISE_CELL = was
    return (r.action, r.why) if r else (None, None)


if __name__ == "__main__":
    # same-context deltas as the wraps leave them: left +4 x2 against -1 x1, right +1 against -4
    delta = {"left": (3, 4 + 4 - 1), "right": (2, 1 - 4)}
    f = _iface(CELLS, delta)
    off = _pick(f, 2, "+", False)
    on = _pick(f, 2, "+", True)
    assert off[0] == "left", off
    assert on[0] != "left" and on[0] == "right", on
    print(f"  m1: c98 (o0.col 2, want +): OFF picks {off[0]} ({off[1]}); ON picks {on[0]} "
          f"({on[1]})")
    a, why = _pick(f, 0, "+", True)
    after = CELLS[f"{a}|0"][0]
    assert after > 0, (a, after)
    print(f"  m2: from column 0, want +: ON picks {a} -> {after} ({why}), a + move from 0")
    for now in (7,):
        assert _pick(f, now, "+", True) == _pick(f, now, "+", False)
    print(f"  m3: no cell evidence at o0.col 7: ON == OFF {_pick(f, 7, '+', True)}")
    two = dict(CELLS, **{"right|2": [3, 1]})
    g = _iface(two, {})
    assert _pick(g, 2, "+", True) == (None, None), _pick(g, 2, "+", True)
    print("  m4: right's cell at 2 holds {1, 3}: no direction from it; with no other "
          "evidence the pick is None")
    em = []
    for on_ in (False, True):
        was = IFace._REALISE_CELL
        IFace._REALISE_CELL = on_
        try:
            em.append(f.expected_move(IFace.Intent(IFace.BECOME, SLOT, "+"), OFFERED, CTX,
                                      {SLOT: 2}, None))
        finally:
            IFace._REALISE_CELL = was
    assert em[0] == em[1], em
    print(f"  expected_move unchanged by the arm: {em[0]} == {em[1]}")
    print("ok")
