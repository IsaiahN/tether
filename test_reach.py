"""reach's fixtures (M4 step 2a): the CAUSE test over frames, its => order, and the ~1 gate.

    python test_reach.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import compile_term as C  # noqa: E402
import reach  # noqa: E402
from test_compile import _atoms  # noqa: E402

SQ = [(0, 0), (0, 1), (1, 0), (1, 1)]


def _rec(r, c):
    return {"row": r, "col": c, "structure": frozenset(SQ)}


def _frames(states):
    """(o1 col, o2 colour) per frame -> frames as reach.frames builds them from a trace."""
    trace = [({"o1.col": c1, "o2.colour": col}, "x", {}, None, None) for c1, col in states]

    def records(before):
        return {"o1": _rec(0, before["o1.col"]), "o2": _rec(0, 5)}
    return reach.frames(trace, records)


CAUSE = {"if": "touching(o1, o2) == 1", "then": "o2.colour_changed == 1"}
# o1 apart, o1 moves to touch o2 (cols 3-4 against 5-6), then o2 recolours to a third colour
CONTAGION = [(0, 3), (3, 3), (3, 7)]
# o2 recolours while o1 is still apart, before any touch: B before A, so => is not supported
EARLY = [(0, 3), (0, 7), (3, 7), (3, 9)]


def test_the_contagion_is_supported():
    if_c, then_c = reach.compile_cause(CAUSE, _atoms())
    v = reach.cause(if_c, then_c, _frames(CONTAGION))
    assert v["supported"] and v["held"] == 1 and v["refuted"] == 0, v
    assert v["if_now"] is True, v
    return v


def test_a_recolour_before_the_touch_is_not_supported():
    """MUST-FAIL: with =>'s order check removed (B counted wherever it happens), the early
    recolour reads supported -- and the fixture says so."""
    if_c, then_c = reach.compile_cause(CAUSE, _atoms())
    v = reach.cause(if_c, then_c, _frames(EARLY))
    assert not v["supported"] and v["refuted"] >= 1, v
    real = reach.composer.holds
    reach.composer.holds = lambda _bond, _a, b: tuple(y for y in b)
    try:
        blind = reach.cause(if_c, then_c, _frames(EARLY))
    finally:
        reach.composer.holds = real
    assert blind["supported"], "the => order check was removed and the early recolour still failed"
    return v


def test_a_term_reading_prev_is_withheld_while_the_arm_is_off():
    """The ~1 gate (the reviewer 07:23Z): the then-side reads o2.colour~1, so with the arm OFF it
    is kept and recorded, never offered. MUST-FAIL: with the gate's test removed it is offered."""
    _if, then_c = reach.compile_cause(CAUSE, _atoms())
    assert then_c.operand == "o2.colour" + C.PREV, then_c
    assert reach.offer_or_withhold(then_c, prev_offer=False) == (False, reach.PREV_OFF)
    assert reach.offer_or_withhold(then_c, prev_offer=True) == (True, None)
    real = reach.reads_prev
    reach.reads_prev = lambda _c: False
    try:
        leaked = reach.offer_or_withhold(then_c, prev_offer=False)
    finally:
        reach.reads_prev = real
    assert leaked == (True, None), "the gate was removed and the ~1 term was still withheld"


def test_no_earlier_frame_cannot_tell():
    """The first frame has no o2.colour~1, so the then-side is None there, never False."""
    _if, then_c = reach.compile_cause(CAUSE, _atoms())
    assert C.run(then_c, _frames(CONTAGION)[0]) is None


if __name__ == "__main__":
    good = test_the_contagion_is_supported()
    early = test_a_recolour_before_the_touch_is_not_supported()
    test_a_term_reading_prev_is_withheld_while_the_arm_is_off()
    test_no_earlier_frame_cannot_tell()
    print(f"reach: contagion supported (held {good['held']}, refuted {good['refuted']}, if now "
          f"{good['if_now']}); recolour before touch not supported (refuted {early['refuted']}), "
          f"and caught with the => order removed; the ~1 then-side withheld with the arm OFF, "
          f"offered ON, leaked with the gate removed; no earlier frame cannot tell")
