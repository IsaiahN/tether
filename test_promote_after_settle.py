"""P2's fixture: a sweep's promotion to primitive waits for the term's first settle in THIS level
(the reviewer 2026-10-09 23:01Z, 2026-10-10 00:37Z: nothing is trusted before it settles).

A term the sweep closes a residual with is queued for promotion. Before P2 `_promote` made it a
primitive at once, with no settle anywhere. With the module flag off and on:
MUST-FAIL: a sweep-closed term that has never settled is NOT promoted; after its first settle in
this level it IS; the queue keeps it until then (held, not dropped).

    python test_promote_after_settle.py
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
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="promote_fixture"),
                      tether.Config(), ledger.Ledger())
    states = [{"x": SEQ[i], "y": SEQ[i - 1] if i else 7} for i in range(len(SEQ))]
    ag.trace = [(states[i], "A", states[i + 1], None, None) for i in range(len(SEQ) - 1)]
    ag._trace_pos = None
    ag.slots = [*ag.slots, "x", "y"]
    ag.alphabet["x"] = ag.alphabet["y"] = 8
    ag.bound = {}
    return ag


def _run(flag: bool) -> tuple[int, int, int]:
    tether._PROMOTE_AFTER_SETTLE = flag
    try:
        ag = _agent()
        term = ag.gamma.build(("take",), operand="w")
        ag.gamma.accept(term, seq=len(ag.led), residual="fixture")
        ag.owed_import.add("y")
        ag.sweep(term, "w")
        assert ag._promotions, "the fixture did not queue a promotion"
        name = ag._promotions[0][0]
        ag._promote()
        before = sum(r["event"] == "promote" for r in ag.led.rows())
        held = len(ag._promotions)
        ag.cycle += 1
        ag._pred_by = {"y": name}
        ag.settle({"y": tether.SlotResidual("y", "transition", 1, 1, 0.0)})
        ag._promote()
        after = sum(r["event"] == "promote" for r in ag.led.rows())
        return before, held, after
    finally:
        tether._PROMOTE_AFTER_SETTLE = True


if __name__ == "__main__":
    off, on = _run(False), _run(True)
    print(f"  (promoted before a settle, held in the queue, promoted after it): "
          f"without P2 {off}; with it {on}")
    ok = off[0] == 1 and on == (0, 1, 1)
    print("ok" if ok else "FAIL")
    sys.exit(0 if ok else 1)
