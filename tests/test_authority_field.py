"""F4, H7'S AUTHORITY ON THE MINT'S ROW (the reviewer r1898 F4, r1900): the reuse authority that
orders the shape walk's chains (P6 H7) was read by no row. Record-only: the mint's detail carries
"authority" -- chains scored, how many scored above 0 (only those can move an order), the highest,
and the book's paid (context, head) pairs -- while the reuse book is on.

  A1  _tally_authority returns each score unchanged and counts it. MF-A1: a tally that returns
      score + 1 (one that would move the order) is caught by the same check (RED).
  A2  gridworld default 0, 12 steps: every mint/park row that walked the shape order carries the
      field with its four keys, scored >= nonzero. MF-A2: the reuse book off -> no row carries it.

    python tests/test_authority_field.py
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
import reuse  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

KEYS = {"scored", "nonzero", "max", "book_paid"}
CHAINS = [("a",), ("a", "b"), ("c",), ("b", "c")]


def _scores(tally) -> tuple[bool, dict]:
    base = {("a",): 0.0, ("a", "b"): 2.0, ("c",): 0.0, ("b", "c"): 3.0}
    into: dict = {}
    f = tally(base.__getitem__, into, 7)
    return all(f(c) == base[c] for c in CHAINS), into


def _rows(on: bool) -> list:
    real = reuse.ON
    reuse.ON = on
    try:
        env = world.bind(gridworld.family("default", 0))
        ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="authority_field"), tether.Config(),
                          ledger.Ledger())
        for _ in range(12):
            ag.step()
    finally:
        reuse.ON = real
    return [r["detail"] for r in ag.led.rows() if r["event"] in ("mint", "park")]


def main() -> int:
    same, into = _scores(tether._tally_authority)
    print(f"   scores unchanged {same}; counted {into}")
    ok = same and into == {"scored": 4, "nonzero": 2, "max": 3.0, "book_paid": 7}
    print("A1 the tally changes no score and counts it: " + ("GREEN" if ok else "RED"))
    assert ok

    def plant(score, into, heads):
        f = tether._tally_authority(score, into, heads)
        return lambda c: f(c) + 1.0
    moved, _ = _scores(plant)
    print("MF-A1 a tally that moves the score: " + ("RED" if not moved
                                                    else "GREEN (the plant went unseen)"))
    assert not moved
    on = _rows(True)
    got = [d["authority"] for d in on if "authority" in d]
    print(f"   reuse book on: {len(on)} mint/park rows, {len(got)} with the field; first {got[:2]}")
    ok2 = got and all(set(a) == KEYS and a["scored"] >= a["nonzero"] for a in got)
    print("A2 the mint's row carries H7's authority: " + ("GREEN" if ok2 else "RED"))
    assert ok2
    off = [d for d in _rows(False) if "authority" in d]
    print("MF-A2 the reuse book off writes no field: " + ("RED" if not off
                                                         else f"GREEN? {len(off)} rows carry it"))
    assert not off
    print("authority_field: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
