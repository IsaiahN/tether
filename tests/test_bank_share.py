"""BANK SHARE (TETHER_BANK_SHARE, default ON; Isaiah 2026-11-16; the open 11-14 question r1970). A
step draws at most bank / (owed questions + 1) of the level's bank; the purse is untouched.
  B1  no owed question: the whole bank (a lone hard question gets it all)
  B2  three owed questions (two slots share one): bank / 3 -- distinct questions, not slots
  B3  another level's bank is never drawn (unchanged rule)
  MF-B1 TETHER_BANK_SHARE=0 -> the whole bank with questions waiting -> RED as required
Seconds.
    python tests/test_bank_share.py
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


def main() -> int:
    assert tether._BANK_SHARE is True, "the arm defaults ON"
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                      ledger.Ledger())
    ag.step()
    p = ag._purse()
    ag._bank, ag._bank_lvl = 1200, ag.level
    ag._owed_q = {}
    assert ag._allowance() == p + 1200, (ag._allowance(), p)
    print("B1 no owed question: the whole bank: GREEN")
    ag._owed_q = {"o1.row": 1, "o2.row": 1, "o3.col": 2}
    assert ag._allowance() == p + 1200 // 3, (ag._allowance(), p)
    print("B2 two distinct owed questions: bank / 3: GREEN")
    ag._bank_lvl = ag.level + 1
    assert ag._allowance() == p, "B3: another level's bank was drawn"
    print("B3 another level's bank is never drawn: GREEN")
    ag._bank_lvl = ag.level
    tether._BANK_SHARE = False
    whole = ag._allowance()
    tether._BANK_SHARE = True
    assert whole == p + 1200, whole
    print("MF-B1 the arm OFF: the whole bank with questions waiting -> RED (as required)")
    print("bank_share: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
