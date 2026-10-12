"""A D5 split is its slot's turn this cycle (F500; the reviewer 2026-10-11 22:59 CDT). The ALL-ON
fake of panel c05a4bd was refused by the gate (step-order, MINT after ACCEPT): the split slot never
left _turn_ahead, so a later mint's sweep in the same cycle reached it.

  (a) a split slot, then a later same-cycle sweep that would reach it: the slot is deferred
      (deferred:turn-done +1), no MINT row lands on it after its split row, step order holds;
  (b) two splits in one cycle: the first split's mint may sweep into the second slot before that
      slot's own split; both end bound to their incumbents, both turns closed, step order holds.

Step order is read with gate._steps, not gate.check: a hand record carries no PERCEIVE bets, so the
full gate refuses it as 'park without bet', a cause unrelated to the turn.

    python test_d5_turn.py
"""
from __future__ import annotations

import sys

import gamma
import gate
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


if __name__ == "__main__":
    tether._D5 = True
    test_a_split_slot_is_not_swept_again_this_cycle()
    print("  (a) the split slot leaves _turn_ahead; a later sweep defers it (+1), no MINT after "
          "its split row, step order holds")
    test_two_splits_in_one_cycle_both_restore()
    print("  (b) two splits in one cycle: both bound to their incumbent, both turns closed, step "
          "order holds")
    print("d5 turn: OK")
