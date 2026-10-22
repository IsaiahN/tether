"""A D5 split is its slot's turn this cycle (F500; the reviewer 2026-10-11 22:59 CDT). The ALL-ON
fake of panel c05a4bd was refused by the gate (step-order, MINT after ACCEPT): the split slot never
left _turn_ahead, so a later mint's sweep in the same cycle reached it.

  (a) a split slot, then a later same-cycle sweep that would reach it: the slot is deferred
      (deferred:turn-done +1), no MINT row lands on it after its split row, step order holds;
  (b) two splits in one cycle: the first split's mint may sweep into the second slot before that
      slot's own split; both end bound to their incumbents, both turns closed, step order holds.
  (c) a part-B mint that accepts writes its ACCEPT row with detail.part (the reviewer 23:03 CDT),
      so a count of accepts per slot cannot read the part's accept as the slot's own; an
      ordinary accept (no split) carries no part.

Step order is read with gate._steps, not gate.check: a hand record carries no PERCEIVE bets, so the
full gate refuses it as 'park without bet', a cause unrelated to the turn.

    python tests/test_d5_turn.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
import gamma
import gate
import interface as IFace
import tether
from test_d5 import CLEAN, _hand

sys.dont_write_bytecode = True


def _idn(ag) -> gamma.Term:
    return gamma.Term(tuple(a for a in ag.gamma.atoms if a.name == "idn"))


def _after_split(ag, slot: str) -> list[dict]:
    rows = ag.led.rows()
    at = max(i for i, r in enumerate(rows) if r["event"] == "split"
             and r["detail"]["split_slot"] == slot)
    return [r for r in rows[at + 1:] if r["slot"] == slot and r["step"] == "MINT"]


def _ready(ag, slots: list[str]) -> None:
    cut = ag._d5_cut("x", "idn")
    assert cut is not None, "CLEAN must cut"
    ag._turn_ahead = set(slots) | {"y"}
    for s in slots:
        ag.bound[s] = "idn"
        ag.owed_import.add(s)
        ag._d5_pending[s] = (cut[0], cut[1], "idn")


def test_a_split_slot_is_not_swept_again_this_cycle():
    ag = _hand(CLEAN)
    _ready(ag, ["x"])
    assert ag._d5_splits() == {"x"}
    assert "x" not in ag._turn_ahead, ag._turn_ahead
    before = ag.chain.reuse_branch["deferred:turn-done"]
    ag.sweep(_idn(ag), "y")                        # a later mint's sweep, same cycle
    assert ag.chain.reuse_branch["deferred:turn-done"] == before + 1, ag.chain.reuse_branch
    assert not _after_split(ag, "x"), _after_split(ag, "x")
    assert gate._steps(ag.led.rows()) is None, gate._steps(ag.led.rows())


def test_two_splits_in_one_cycle_both_restore():
    ag = _hand(CLEAN)
    ag.slots = [*ag.slots, "z"]
    ag.alphabet["z"] = ag.alphabet["x"]
    ag._d5_rows["z"] = list(ag._d5_rows["x"])
    ag.trace = [({**b, "z": b["x"]}, a, {**f, "z": f["x"]}, k, at) for b, a, f, k, at in ag.trace]
    _ready(ag, ["x", "z"])
    assert ag._d5_splits() == {"x", "z"}
    assert ag.bound.get("x") == "idn" and ag.bound.get("z") == "idn", ag.bound
    assert ag._parts["x"]["A"] == "idn" and ag._parts["z"]["A"] == "idn", ag._parts
    assert not ({"x", "z"} & ag._turn_ahead), ag._turn_ahead
    assert gate._steps(ag.led.rows()) is None, gate._steps(ag.led.rows())


_T, _B = IFace.TOUCH, IFace.ELICIT
ROWS_C = [(_T, 1, 2), (_B, 3, 2), (_T, 2, 3), (_B, 5, 4), (_T, 4, 5), (_B, 6, 5),   # inc on TOUCH,
          (_T, 1, 2), (_B, 7, 6)]                                                   # dec off it


def test_a_part_b_accept_carries_its_part():
    t_ = IFace.TOUCH
    ag = _hand(ROWS_C, term="inc")
    cut = ag._d5_cut("x", "inc")
    ag.bound["x"] = "inc"
    ag._d5_split("x", cut[0], cut[1])
    acc = [r for r in ag.led.rows() if r["event"] == "accept" and r["slot"] == "x"]
    assert ag._parts["x"]["B"] and acc, (ag._parts, acc)          # non-vacuous: part B accepted
    assert all((r["detail"].get("part") or {}).get("part") == f"!{t_}" for r in acc), acc
    assert ag.bound.get("x") == "inc", ag.bound
    plain = _hand(ROWS_C, term="inc")                    # no split: an ordinary accept
    plain.mint("x")
    ordinary = [r for r in plain.led.rows() if r["event"] == "accept"]
    assert ordinary and not any("part" in r["detail"] for r in ordinary), ordinary


if __name__ == "__main__":
    tether._D5 = True
    test_a_split_slot_is_not_swept_again_this_cycle()
    print("  (a) the split slot leaves _turn_ahead; a later sweep defers it (+1), no MINT after "
          "its split row, step order holds")
    test_two_splits_in_one_cycle_both_restore()
    print("  (b) two splits in one cycle: both bound to their incumbent, both turns closed, step "
          "order holds")
    test_a_part_b_accept_carries_its_part()
    print("  (c) part B's accept carries its part; the slot keeps its incumbent")
    print("d5 turn: OK")
