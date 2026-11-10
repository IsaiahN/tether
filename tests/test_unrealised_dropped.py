"""unrealised_dropped (the reviewer 2026-11-07 r1431, r1432): the interface's unrealised_log keeps
its 256 cap, and a reason the cap refuses is COUNTED, not lost silently. The REPEAT row writes
"unrealised_dropped" beside "unrealised" only when > 0; absent means 0 dropped. Record only, no arm.
A fresh gridworld agent; 257 reasons planted through the one writer (Interface._none).

D1  257 planted: the row's log holds 256 and unrealised_dropped is 1
D2  the drain zeroes it: the next row has no unrealised_dropped and an empty log
MF  256 planted (the cap exactly): no unrealised_dropped -- the field cannot appear without a drop

    python tests/test_unrealised_dropped.py
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


def agent():
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="ud"), tether.Config(), ledger.Ledger())
    ag._last_real = None                # set at each cycle's start; no cycle has run
    return ag


def plant(ag, n: int) -> None:
    for i in range(n):
        ag.iface._none("no way", f"planted {i}", "test")


def main() -> int:
    assert tether.IFace._UNREALISED_WHY, "TETHER_UNREALISED_WHY is off: nothing is recorded"
    ag = agent()
    plant(ag, 257)
    row = ag._r4_repeat()
    assert len(row["unrealised"]) == 256 and row.get("unrealised_dropped") == 1, (
        "D1", len(row["unrealised"]), row.get("unrealised_dropped"))
    row2 = ag._r4_repeat()
    assert "unrealised_dropped" not in row2 and row2["unrealised"] == [], ("D2", row2)
    mf = agent()
    plant(mf, 256)
    row3 = mf._r4_repeat()
    assert len(row3["unrealised"]) == 256 and "unrealised_dropped" not in row3, ("MF", row3)
    print("D1  257 planted: log 256, unrealised_dropped 1")
    print("D2  drained: the next row has no unrealised_dropped and an empty log")
    print("MF  256 planted: no unrealised_dropped")
    print("unrealised_dropped: 3 of 3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
