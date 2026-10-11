"""Sensor 3's feed (the reviewer 2026-10-11 12:49 CDT, ruled ungated): Agency.note is given the
slots whose VALUE changed, not the slots the agent was surprised by. One Agency fed through
Agent._moved, one through the old mass feed, on the same steps.

  f1 an avatar slot that moves on every press of A and never on B, PREDICTED PERFECTLY (mass 0),
     stays in contingent(); MUST-FAIL: under the mass feed it drops out;
  f2 a press predicted to move a slot that does not move (mass > 0) is not counted as moved;
     MUST-FAIL: the mass feed counts it.

    python test_agency_feed.py
"""
from __future__ import annotations

import sys
from types import SimpleNamespace

import instruments
import tether

sys.dont_write_bytecode = True


def main() -> int:
    slots = ["o0.row", "o1.row"]
    new, old = instruments.Agency(), instruments.Agency()
    row = 1
    # (action, o0 moves?, mass on o0.row, mass on o1.row): the avatar is predicted perfectly;
    # C is predicted to move o1.row and does not
    steps = [("A", True, 0, 0), ("B", False, 0, 0)] * 4 + [("C", False, 0, 2.0)]
    for action, moves, m0, m1 in steps:
        before = {"o0.row": row, "o1.row": 5}
        row += int(moves)
        after = {"o0.row": row, "o1.row": 5}
        res = {"o0.row": SimpleNamespace(mass=m0), "o1.row": SimpleNamespace(mass=m1)}
        new.note(action, tether.Agent._moved(res, before, after), slots)
        old.note(action, {s for s, r in res.items() if r.mass > 0}, slots)
    assert "o0.row" in new.contingent(), new.contingent()
    assert "o0.row" not in old.contingent(), old.contingent()
    print(f"  f1 predicted-perfectly avatar: contingent {new.contingent()} (mass feed: "
          f"{old.contingent()})")
    assert new.moved[("o1.row", "C")] == 0 and old.moved[("o1.row", "C")] == 1, (new, old)
    print("  f2 a predicted move that did not happen: moved 0 (mass feed: 1)")
    print("agency feed: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
