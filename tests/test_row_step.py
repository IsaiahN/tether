"""SHIP 1, THE MINT'S PRE-SCOPE READS NAME THEIR STEP (the reviewer r1871): _mint_in_step's
contact read (CONTACT_FIRST) and reach-gate read run before the mint's step opens, under the step
that called it (ACCEPT); a purse cut inside them wrote ACCEPT rows on the slot, and its MINT rows
followed -- the demo's gate refused ("MINT after ACCEPT"). _row_step labels their rows MINT and
moves no clock.

  RS1  every row on the slot from one _mint_in_step called under ACCEPT is labelled MINT.
       MF-RS1: the old order (no relabel) writes ACCEPT rows first -> RED.
  RS2  the purse spent and the step clock's heads are what the old order gives.
       MF-RS2: _step_scope("MINT") in its place moves the clock (ACCEPT is an idle scope, MINT is
       charged) -> RED.

    python tests/test_row_step.py
"""
from __future__ import annotations

import contextlib
import os
import sys
import time

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")

import cap  # noqa: E402
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

HEADS = 1000


def _call(plant: str | None) -> tuple:
    """one _mint_in_step under ACCEPT, the clock open on ACCEPT; the two reads each spend HEADS
    and write a cut row labelled by the running step. (steps of the slot's rows, spent, clk_h)."""
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="row_step"), tether.Config(),
                      ledger.Ledger())
    slot = sorted(ag.alphabet)[0]

    def read(*_a):
        for _ in range(HEADS):
            cap.head()
        ag.led.record(ag.cycle, ag._running_step, slot, "purse_cut", site="unseen_walk")

    ag._contact_fp = read
    ag._out_of_reach = lambda _s: read() or False
    ag._try_first_hold = lambda: 0
    ag.mint = lambda s: ag.led.record(ag.cycle, "MINT", s, "mint", of=(s,))
    if plant == "old":
        ag._row_step = lambda _step: contextlib.nullcontext()
    elif plant == "scope":
        ag._row_step = ag._step_scope
    ag._running_step = "ACCEPT"
    ag._clk_stack, ag._clk_hs, ag._clk_h = [("ACCEPT", time.perf_counter())], [cap.HEADS], {}
    ag._clk_h0 = cap.HEADS
    ag._mint_in_step(slot, "mechanism")
    steps = [r["step"] for r in ag.led.rows() if r["slot"] == slot]
    return steps, ag._purse_spent(), dict(ag._clk_h)


def main() -> int:
    new, old, scope = _call(None), _call("old"), _call("scope")
    print(f"   new: steps {new[0]}, spent {new[1]}, clk_h {new[2]}")
    print(f"   old order: steps {old[0]}, spent {old[1]}, clk_h {old[2]}")
    print(f"   _step_scope instead: steps {scope[0]}, spent {scope[1]}, clk_h {scope[2]}")
    ok = new[0] == ["MINT"] * 3
    print("RS1 the pre-scope reads' rows are MINT rows: " + ("GREEN" if ok else "RED"))
    assert ok
    print("MF-RS1 the old order writes ACCEPT first: " + ("RED" if old[0][0] == "ACCEPT"
                                                         else "GREEN (the plant went unseen)"))
    assert old[0][0] == "ACCEPT"
    ok2 = new[1:] == old[1:]
    print("RS2 the purse and the clock are the old order's: " + ("GREEN" if ok2 else "RED"))
    assert ok2
    print("MF-RS2 _step_scope moves the clock: " + ("RED" if scope[1:] != old[1:]
                                                    else "GREEN (the plant went unseen)"))
    assert scope[1:] != old[1:]
    print("row_step: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
