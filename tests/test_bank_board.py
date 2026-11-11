"""C2 BANK PER BOARD (R1 finding F3, 2026-11-10), arm TETHER_BANK_PER_BOARD.

  B1  MF: a bank saved on one board is empty after the agent's own new-board boundary
      (retarget NEW_BOARD) at the same level number, so the next board's allowance is its purse;
      OFF it carries over
  B2  a level change still empties it, ON and OFF (U4's rule, unchanged)

    python tests/test_bank_board.py
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


def _agent() -> tuple:
    env = world.bind(gridworld.family("default", 0))
    return env, tether.Agent(env, gamma.Gamma(env.atoms(), game="bank"), tether.Config(),
                             ledger.Ledger())


def _bank_after(how: str, on: bool, level_step: int = 0) -> tuple:
    keep, tether._BANK_PER_BOARD = tether._BANK_PER_BOARD, on
    try:
        env, ag = _agent()
        ag._bank, ag._bank_lvl = 5_000_000, ag.level
        ag.retarget(env, ag.level + level_step, how=how)
        live = ag._bank if ag._bank_lvl == ag.level else 0
        return live, ag._allowance() - ag._purse()
    finally:
        tether._BANK_PER_BOARD = keep


def check_b1() -> None:
    on = _bank_after(tether.NEW_BOARD, True)
    off = _bank_after(tether.NEW_BOARD, False)
    assert on == (0, 0), f"MUST-FAIL: a new board kept the last board's bank: {on}"
    assert off == (5_000_000, 5_000_000), off
    print(f"  B1: new board at the same level: bank, allowance - purse ON {on}; OFF {off}")


def check_b2() -> None:
    on = _bank_after(tether.ADVANCE, True, 1)
    off = _bank_after(tether.ADVANCE, False, 1)
    assert on[1] == 0 and off[1] == 0, (on, off)
    print(f"  B2: a level change empties it, ON {on[1]}, OFF {off[1]} (allowance - purse)")


def main() -> int:
    check_b1()
    check_b2()
    print("bank_board: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
