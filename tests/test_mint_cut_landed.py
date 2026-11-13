"""SHIP 1, THE MINT CUT AFTER ITS MINT LANDED (the reviewer r1869), arm TETHER_MINT_CUT_LANDED.

  L1  a mint unit cut AFTER the slot's mint and ACCEPT rows were written inside the unit: no
      purse_cut row and the slot is not owed (ON). MF-L1: OFF, the owed row is written for a slot
      whose term was just accepted -> RED for the claim.
  L2  a mint unit cut BEFORE anything landed is owed as before, ON and OFF.
  The real must-fail is the demo's gate on a fresh export (ON pass, OFF "ladder: MINT after
  ACCEPT"); this is the unit half.

    python tests/test_mint_cut_landed.py
"""
from __future__ import annotations

import os
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")

import cap  # noqa: E402
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def _cut_mint(on: bool, land: bool) -> tuple:
    """mint() on a real agent whose _mint writes the slot's mint + ACCEPT rows (land) and then
    raises cap.PurseCut. (purse_cut rows on the slot, slot owed)."""
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="mint_cut"), tether.Config(),
                      ledger.Ledger())
    slot = sorted(ag.alphabet)[0]

    def fake(s: str):
        if land:
            ag.led.record(ag.cycle, "MINT", s, "mint", of=(s,))
            ag.led.record(ag.cycle, "ACCEPT", s, "accept", term="x")
        raise cap.PurseCut
    ag._mint = fake
    real_on, real_lim = tether._MINT_CUT_LANDED, cap.LIMIT
    tether._MINT_CUT_LANDED = on
    cap.LIMIT = cap.HEADS + 10**12          # a limit set: _unit's cut path runs
    try:
        ag.mint(slot)
    finally:
        tether._MINT_CUT_LANDED, cap.LIMIT = real_on, real_lim
    cuts = [r for r in ag.led.rows() if r["event"] == "purse_cut" and r["slot"] == slot]
    return len(cuts), slot in ag._owed_q


def main() -> int:
    on = _cut_mint(True, True)
    off = _cut_mint(False, True)
    print(f"   landed then cut: ON (purse_cut rows, owed) {on}; OFF {off}")
    ok = on == (0, False)
    print("L1 a cut after the mint landed owes nothing: " + ("GREEN" if ok else "RED"))
    assert ok
    print("MF-L1 OFF owes the landed slot: " + ("RED" if off == (1, True)
                                               else "GREEN (the plant went unseen)"))
    assert off == (1, True)
    early_on, early_off = _cut_mint(True, False), _cut_mint(False, False)
    print(f"   cut before anything landed: ON {early_on}; OFF {early_off}")
    ok2 = early_on == early_off == (1, True)
    print("L2 a cut before the mint landed is owed, ON and OFF: " + ("GREEN" if ok2 else "RED"))
    assert ok2
    print("mint_cut_landed: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
