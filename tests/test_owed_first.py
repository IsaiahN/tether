"""(2b) (the reviewer 2026-11-06 r1317, r1323): "owed, asked first next step" holds in every arm.
The governor (A1) and the walk budget (A2) write _owed_q whether or not the step budget is on, but
route's owed-first order sat inside the budget branch, so with TETHER_STEP_BUDGET=0 a deferred slot
kept its old place. A stepped gridworld agent, seed pinned; seconds.

MF-2b   budget OFF: a slot in _owed_q, last in the residual's order, is routed FIRST. RED at f0576c8
CONTROL budget ON, TETHER_STEP_RANK off: the same (the budget's own owed-first branch, unchanged)
CONTROL budget OFF, nothing owed: today's order, untouched

    python tests/test_owed_first.py
"""
from __future__ import annotations

import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def _order(budget: bool, owed: bool) -> tuple:
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="owed_first"), tether.Config(),
                      ledger.Ledger())
    for _ in range(3):
        ag.step()
    slots = sorted(s for s in ag.slots if not s.startswith("@"))[:4]
    last = slots[-1]
    ag._owed_q = {last: (ag.cycle - 1, "o_prior")} if owed else {}
    ag._library_fit = lambda _s, _ex: None
    keep = tether._STEP_BUDGET, tether._STEP_RANK
    tether._STEP_BUDGET, tether._STEP_RANK = budget, False
    try:
        ag.route({s: tether.SlotResidual(s, "x", 0, 10 ** 6, 1.0) for s in slots})
    finally:
        tether._STEP_BUDGET, tether._STEP_RANK = keep
    return slots, last, list(ag._route_order)


def main() -> int:
    slots, last, order = _order(budget=False, owed=True)
    assert order[0] == last, ("MF-2b: budget OFF, the owed slot was not asked first", order)
    _s, last_on, order_on = _order(budget=True, owed=True)
    assert order_on[0] == last_on, ("CONTROL: budget ON lost owed-first", order_on)
    s0, _l, order0 = _order(budget=False, owed=False)
    assert order0 == s0, ("CONTROL: nothing owed, the order moved", order0)
    print(f"  MF-2b budget OFF: {last} (owed, last in the residual) routed first: {order[:3]}")
    print(f"  CONTROL budget ON: {order_on[:3]}; nothing owed: today's order kept")
    print("test_owed_first OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
