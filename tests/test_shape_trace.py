"""BUILD 5 ITEM 21, THE INSTRUMENT (TETHER_SHAPE_TRACE; the reviewer 2026-11-05 r1234). Record-only
fields (family, board, per-slot trend) on goal_hypotheses / goal_hypothesis_end, read per board by
shape_trace.py. Seconds: test_desc_demote's played gridworld agent.

MF-T4  RED FIRST: with the arm OFF the rows carry no board, and the reader prints "no shape trace"
       -- it never invents a hold
MF-T1  ON: X "o0.row == o4.row" stalls flat, then Y "o1.colour == o3.colour" is held, on ONE
       board: the reader prints X's span, family navigate, trend fell=False, the switch line
       "switch +k cycles -> 'o1.colour == o3.colour'" and the family_demoted row under X
MF-T2  the same holds with the board counter moved between them print under TWO boards
MF-T5  (r1239) the proposer's turn held by a routine writes ONE proposal_gated row (holder
       routine, its routine rendered; a second call with the same holder writes none), and the
       reader prints it under the board
MF-T6  (r1239) the family counts: a proposal over a navigate X2 and a contact C lists contact
       with its cheapest text C and its price -- read, never inferred
The red is behavioural: TETHER_SHAPE_TRACE=0 fails MF-T1.

    python tests/test_shape_trace.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import routine as Rt  # noqa: E402
import shape_trace  # noqa: E402
import test_board_desc as B  # noqa: E402
import test_desc_demote as D  # noqa: E402

tether = B.tether
X, Y = "o0.row == o4.row", "o1.colour == o3.colour"


def run(on: bool | None, new_board: bool = False) -> list:
    was = tether._SHAPE_TRACE
    tether._SHAPE_TRACE = was if on is None else on
    try:
        ag = B.played()
        assert D.propose(ag, [X]).get("pick") == X, "the hold of X"
        B.stall(ag)
        if new_board:
            ag.iface.board_n += 1
        ag.cycle += 3
        assert D.propose(ag, [Y]).get("pick") == Y, "the hold of Y"
        return shape_trace.trace(ag.led.rows())
    finally:
        tether._SHAPE_TRACE = was


def section(lines: list, text: str) -> list:
    """The lines of the board one of whose HOLD lines names `text` (never its family counts)."""
    out, cur = {}, None
    for ln in lines:
        if ln.startswith("board "):
            cur = ln
            out[cur] = []
        elif cur:
            out[cur].append(ln)
    return [ln for b, ls in out.items() if any(text in x and " family=" in x for x in ls)
            for ln in [b, *ls]]


def main():
    assert run(False) == ["no shape trace"], "MF-T4 (red first): OFF invented a trace"

    lines = run(None)
    sec = section(lines, repr(Y))
    x_line = next((ln for ln in sec if repr(X) in ln and "family=navigate" in ln), None)
    assert x_line and "ended stalled" in x_line, ("MF-T1: X's hold", sec)
    assert any("fell=False" in ln for ln in sec), ("MF-T1: the flat trend", sec)
    assert any(ln.strip().startswith("switch +") and repr(Y) in ln for ln in sec), (
        "MF-T1: the switch", sec)
    assert any("family_demoted" in ln for ln in sec), ("MF-T1: the demotion row", sec)

    two = run(None, new_board=True)
    bx = [ln for ln in section(two, repr(X)) if ln.startswith("board ")]
    by = [ln for ln in section(two, repr(Y)) if ln.startswith("board ")]
    assert bx and by and bx[0] != by[0], ("MF-T2: one board", two)

    ag = B.played()
    ag._hyp, ag._hyp_exhausted = None, None
    ag.routine = Rt.Act("a held routine")
    g0 = len([r for r in ag.led.rows() if r["event"] == "proposal_gated"])
    ag._goal_hypothesis_run(ag.trace[-1][2])
    ag._goal_hypothesis_run(ag.trace[-1][2])
    gated = [r["detail"] for r in ag.led.rows() if r["event"] == "proposal_gated"][g0:]
    assert len(gated) == 1 and gated[0]["holder"] == "routine" and "a held routine" in str(
        gated[0]["what"]), ("MF-T5: the gated row", gated)
    ag.routine = None
    t5 = shape_trace.trace(ag.led.rows())
    assert any("proposal_gated" in ln and "'holder': 'routine'" in ln for ln in t5), (
        "MF-T5: the reader", t5)

    ag2 = B.played()
    c = D.propose(ag2, [D.X2, D.C])
    fams = c.get("families") or {}
    assert fams.get("contact", {}).get("cheapest") == D.C and "bits" in fams["contact"] and (
        "navigate" in fams), ("MF-T6: the families", fams)
    print("test_shape_trace: pass (MF-T4 OFF: 'no shape trace'; MF-T1 one board:\n  "
          + "\n  ".join(sec) + f"\n MF-T2 X on {bx[0]!r}, Y on {by[0]!r}; MF-T5 {gated[0]}; "
          f"MF-T6 {fams})")


if __name__ == "__main__":
    main()
