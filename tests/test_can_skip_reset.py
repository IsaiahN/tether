"""F5, TETHER_CAN_SKIP_RESET (the reviewer r1898 F5, r1900): why no crossing was ever "opened".
can_ledger calls a crossing "opened" only from BLOCKED; the one BLOCKED reason a board can lift is
"no route; every action tried", and the can lists counted RESET (never in the interface table) as
untried, so that reason was never read: 0 opened of 198 crossings on the step 10 retest.

  S1  every action but RESET in the table: untried 0 (ON). MF-S1: OFF counts RESET -> 1 (RED).
      Not alive, RESET is untried ON too (interface.untried_here's test, r1901).
  S2  on that reading a slot with no route is BLOCKED ("every action tried"); when its route
      appears the crossing reads "opened". MF-S2: OFF it stays NOT_FOUND and the crossing reads
      "discovered" (RED for the claim).

    python tests/test_can_skip_reset.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import can_ledger  # noqa: E402
import gamma  # noqa: E402
import gridworld  # noqa: E402
import interface as IFace  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def _untried(on: bool, alive: bool = True) -> tuple[int, list]:
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="can_skip_reset"), tether.Config(),
                      ledger.Ledger())
    ag.actions = [*[a for a in ag.actions if a != IFace.RESET], IFace.RESET]
    table = {a: {"delta": {}} for a in ag.actions if a != IFace.RESET}
    ag.iface.alive = alive
    real = tether._CAN_SKIP_RESET
    tether._CAN_SKIP_RESET = on
    try:
        return ag._can_untried(table), ag.actions
    finally:
        tether._CAN_SKIP_RESET = real


def _crossing(untried: int) -> str:
    """The slot o.x with no route on that reading, then routable on the next."""
    prev = can_ledger.classify(["o.x"], {"o.x"}, set(), set(), untried, set())
    now = can_ledger.classify(["o.x"], {"o.x"}, {"o.x"}, set(), untried, set())
    cross, _ = can_ledger.crossings(prev, now, True)
    return cross[0]["kind"]


def main() -> int:
    on, acts = _untried(True)
    off, _ = _untried(False)
    print(f"   actions {acts}; every action but RESET in the table: untried ON {on}, OFF {off}")
    print("S1 RESET is not counted untried: " + ("GREEN" if on == 0 else "RED"))
    assert on == 0
    print("MF-S1 OFF counts RESET: " + ("RED" if off == 1 else "GREEN (the plant went unseen)"))
    assert off == 1
    dead, _ = _untried(True, alive=False)
    print(f"   not alive: untried ON {dead} (RESET counted, as interface.untried_here)")
    assert dead == 1
    k_on, k_off = _crossing(on), _crossing(off)
    print(f"   a route appears for a slot that had none: ON {k_on!r}, OFF {k_off!r}")
    print("S2 the crossing reads opened: " + ("GREEN" if k_on == "opened" else "RED"))
    assert k_on == "opened"
    print("MF-S2 OFF never opens: " + ("RED" if k_off == "discovered"
                                       else "GREEN (the plant went unseen)"))
    assert k_off == "discovered"
    print("can_skip_reset: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
