"""C2 THE PURSE FIRST (R2's fired refuter; the reviewer r1707 2), arm TETHER_PURSE_FIRST.

  F1  at a spent purse the owed lookup (budget_owed) fits no library candidate: gridworld default
      seed 0, the allowance spent before route, 4 steps -- budget_owed rows > 0 and no
      _rebindings call inside ROUTE ON
      MUST-FAIL: OFF the candidate fit runs at the spent purse (_rebindings called inside ROUTE)

    python tests/test_purse_first.py
"""
from __future__ import annotations

import os
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def _run(on: bool) -> tuple[int, int]:
    keep = tether._PURSE_FIRST
    tether._PURSE_FIRST = on
    real = tether.Agent._rebindings
    calls = [0]
    try:
        env = world.bind(gridworld.family("default", 0))
        ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="purse_first"), tether.Config(),
                          ledger.Ledger())
        ag._allowance = lambda: 0        # the purse is spent before route, every step

        def spy(self, *a, **k):
            if self._running_step == "ROUTE":
                calls[0] += 1
            return real(self, *a, **k)
        tether.Agent._rebindings = spy
        for _ in range(4):
            ag.step()
        owed = sum(1 for r in ag.led.rows() if r["event"] == "budget_owed")
        return owed, calls[0]
    finally:
        tether.Agent._rebindings = real
        tether._PURSE_FIRST = keep


def check_f1() -> None:
    owed_on, reb_on = _run(True)
    owed_off, reb_off = _run(False)
    assert owed_on > 0 and owed_off > 0, ("no owed lookup to read", owed_on, owed_off)
    assert reb_on == 0, f"a candidate was fitted at a spent purse ON: {reb_on} _rebindings calls"
    assert reb_off > 0, ("MUST-FAIL: OFF fitted no candidate at the spent purse, so the check "
                         f"cannot fail: {reb_off}")
    print(f"  F1: spent purse, 4 steps: budget_owed ON {owed_on}, OFF {owed_off}; _rebindings "
          f"inside ROUTE ON {reb_on}, OFF {reb_off}")


def main() -> int:
    check_f1()
    print("purse_first: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
