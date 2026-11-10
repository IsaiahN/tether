"""The goal-hypothesis route memo (the reviewer 2026-11-07 r1347, r1348): within one _hyp_propose
pass a FAILED route read is a function of (intent, withheld, actions, context, the state, the
RESET-adjacency flag), so a repeat is served from _route_memo and its unrealised record is REPLAYED
through the same writer (Interface._none): the interface's unrealised record and log, which the
REPEAT row drains, come out as without the memo. A success is never memoised. A forcing fixture: a
fresh gridworld agent, a planted ordered target on o0.row, the real Interface.realise, which cannot
route it (about 2 s).

check_replay   two reads in a pass: realise is called once, and unrealised / unrealised_log equal
               two reads with no memo. MUST-FAIL: a memo that does not replay leaves the log short
check_scope    outside a pass (_route_memo None) every read goes through realise

    python tests/test_route_memo.py [check ...]
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

SLOT = "o0.row"


def reads(memo, n: int = 2) -> tuple:
    """n route reads of the planted slot; (realise calls, the unrealised record, the log)."""
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="rm"), tether.Config(), ledger.Ledger())
    before = dict(env.observe())
    ag.slot_types[SLOT] = "POSITION"
    ag._goal_target = lambda slot, b: b[slot] + 3
    ag._rel_partner = lambda _s: None
    calls = [0]
    real = ag.iface.realise

    def counted(*a, **k):
        calls[0] += 1
        return real(*a, **k)
    ag.iface.realise = counted
    ag._route_memo = memo
    out = [ag._hyp_route(SLOT, before) for _ in range(n)]
    assert out == [None] * n, ("the fixture routes the slot", out)
    return calls[0], ag.iface.unrealised, list(ag.iface.unrealised_log)


class NoReplay(dict):
    """The must-fail: a hit finds the key and gets no stored record, so nothing is replayed."""

    def __getitem__(self, k):
        return None


def check_replay() -> None:
    on, off = reads({}), reads(None)
    assert on[0] == 1 and off[0] == 2, ("realise calls", on[0], off[0])
    assert on[1] is not None and on[1:] == off[1:], ("MF: the replay", on[1:], off[1:])
    bad = reads(NoReplay())
    assert bad[2] != off[2], "MUST-FAIL: a memo without the replay left the log unchanged"
    print(f"  memo: realise {on[0]} call for 2 reads, unrealised log {len(on[2])} entries = no "
          f"memo's ({off[0]} calls); without the replay the log has {len(bad[2])}")


def check_scope() -> None:
    assert reads(None, 3)[0] == 3, "outside a pass a read was served from a memo"
    print("  outside a pass: every read goes through realise")


def main() -> int:
    want = set(sys.argv[1:])
    for c in (check_replay, check_scope):
        if not want or c.__name__ in want:
            c()
            print("ok  ", c.__name__)
    print("test_route_memo OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
