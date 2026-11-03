"""M1 + M2 THE THOUGHT RECORD (the reviewer 2026-11-02 r828 f): Agent._thought_note / _thought_of
and S2's cheap rank in Agent._topk, on a stub.
  M-a  a lookup's judged entries and the ones that offered are counted under a KIND-FORM key (the
       delta kind and the asked readings, no slot name): two slots with the same kind and readings
       share one key.
  M-b  the rank reads it: within a tier, the entry that paid under the key comes first, one tried
       and never paid comes after the untried -- a cut, never a verdict: it is still listed.
  M-c  the store's load sums two generations' thought_tried / thought_paid (lineage_store).
  MUST-FAIL: with the arm OFF the rank is S2's order, the record unread.

    python tests/test_thought_record.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import lineage_store  # noqa: E402
import tether  # noqa: E402
from test_topk import stub  # noqa: E402

A = tether.Agent


def rank(ag, lit, on=True):
    tether._THOUGHT_RECORD = on
    try:
        win, _n = A._topk(ag, lit, lit, {"T3": len(lit)}, {"o1.x": "colour"}, ("o1.x",),
                          ("o1.x", ("move",), (), (), ("o1.x",)))
        return [e for e, _w in win]
    finally:
        tether._THOUGHT_RECORD = True


def main():
    assert tether._THOUGHT_RECORD, "ON by default"
    k1, k2 = A._thought_key(("move",), {"colour"}), A._thought_key(("move",), {"colour", None})
    assert k1 == k2 and "o1" not in k1, ("M-a: kind form, no slot name", k1, k2)
    ag = stub()
    lit = [(f"e{i}", 0.0) for i in range(5)]
    A._thought_note(ag, k1, ["e0", "e1", "e2", "e3"], {"e3"})
    assert A._thought_of(ag, "tried", k1) == {"e0": 1, "e1": 1, "e2": 1, "e3": 1}
    assert A._thought_of(ag, "paid", k1) == {"e3": 1}, "M-a: paid counted"
    ag._thought_in["paid"][k1] = {"e3": 2}
    assert A._thought_of(ag, "paid", k1) == {"e3": 3}, "M-a: carried + this life"
    got = rank(ag, lit)
    assert got[0] == "e3" and got[1] == "e4" and got[2:] == ["e0", "e1", "e2"], (
        "M-b: paid first, untried next, tried-never-paid last, none dropped", got)
    assert rank(ag, lit, on=False) == [f"e{i}" for i in range(5)], "MUST-FAIL: OFF is S2's order"
    c: dict = {}
    for g in ({"thought_tried": {k1: {"e0": 2}}, "thought_paid": {k1: {"e3": 1}}},
              {"thought_tried": {k1: {"e0": 1, "e1": 1}}, "thought_paid": {k1: {"e3": 2}}}):
        lineage_store._counts_apply(c, g)
    assert c["thought_tried"][k1] == {"e0": 3, "e1": 1} and c["thought_paid"][k1] == {"e3": 3}, (
        "M-c: the store sums the generations", c)
    print(f"test_thought_record: key {k1}; ranked {got} (paid, untried, tried-unpaid); OFF "
          f"{rank(ag, lit, on=False)}; two generations summed {c['thought_tried'][k1]}")


if __name__ == "__main__":
    main()
