"""P2's boundary, pinned (the reviewer 2026-10-10 01:13Z): a promotion HELD when the level
changes is not granted on the old level's record. It waits for the term to settle in the NEW
level (R-D4: re-ground before a crossing counts), and is granted after that.

The panel cannot reach this (0 level ends on every member), so it is fixed here by hand:
  queue (sweep close, no settle) -> held -> retarget -> _promote: still held -> the term settles
  in the new level -> _promote: granted.

    python test_promote_across_levels.py
"""
from __future__ import annotations

import sys

import gamma
import gridworld
import ledger
import tether
import world

sys.dont_write_bytecode = True

SEQ = [0, 3, 5, 1, 6, 2, 7, 4] * 2          # y's next value is x's value now


def _agent() -> tether.Agent:
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="promote_levels_fixture"),
                      tether.Config(), ledger.Ledger())
    states = [{"x": SEQ[i], "y": SEQ[i - 1] if i else 7} for i in range(len(SEQ))]
    ag.trace = [(states[i], "A", states[i + 1], None, None) for i in range(len(SEQ) - 1)]
    ag._trace_pos = None
    ag.slots = [*ag.slots, "x", "y"]
    ag.alphabet["x"] = ag.alphabet["y"] = 8
    ag.bound = {}
    return ag


def _promoted(ag: tether.Agent) -> int:
    return sum(r["event"] == "promote" for r in ag.led.rows())


if __name__ == "__main__":
    ag = _agent()
    term = ag.gamma.build(("take",), operand="w")
    ag.gamma.accept(term, seq=len(ag.led), residual="fixture")
    ag.owed_import.add("y")
    ag.sweep(term, "w")
    assert ag._promotions, "the fixture did not queue a promotion"
    name = ag._promotions[0][0]
    ag._promote()
    held_before = (_promoted(ag), len(ag._promotions))

    ag.retarget(ag.env, ag.level + 1)
    ag._promote()
    held_across = (_promoted(ag), len(ag._promotions))

    slot = ag.slots[0]
    ag._carry(name)                        # bound on the new level: its candidacy wakes here
    ag.cycle += 1
    ag._pred_by = {slot: name}
    ag.settle({slot: tether.SlotResidual(slot, "transition", 1, 1, 0.0)})
    ag._promote()
    granted = (_promoted(ag), len(ag._promotions))

    print(f"  (promote rows, queued): held on the old level {held_before}; after the level change "
          f"{held_across}; after a settle in the new level {granted}")
    ok = held_before == (0, 1) and held_across == (0, 1) and granted == (1, 0)
    print("ok" if ok else "FAIL")
    sys.exit(0 if ok else 1)
