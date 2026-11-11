"""(A) THE WALK MEMO BY PATTERN (R1 finding F1; Isaiah 2026-11-10 16:12, the reviewer r1700, r1702,
r1704), arm TETHER_PATTERN_MEMO.

  M1  two walks with the same owner pattern share one entry, and every shared hit equals a fresh
      walk: TETHER_WALK_MEMO_CHECK on (each hit also walked fresh and compared), gridworld default
      seed 0, 12 steps, the purse off for volume -- pattern hits > 0, 0 disagreements
      MUST-FAIL: OFF (the instance key alone) checks fewer hits: the pattern hits are walks the
      instance key missed

    python tests/test_pattern_memo.py
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

BOOKS = ("pattern_memo_lookup", "pattern_memo_hit", "walk_memo_agree", "walk_memo_disagree")


def _run(on: bool) -> tuple[dict, int]:
    keep = (tether._PATTERN_MEMO, tether._WALK_MEMO_CHECK, tether._PURSE_OWN)
    tether._PATTERN_MEMO, tether._WALK_MEMO_CHECK, tether._PURSE_OWN = on, True, False
    try:
        env = world.bind(gridworld.family("default", 0))
        ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="pattern_memo"), tether.Config(),
                          ledger.Ledger())
        b0 = {k: ag.gamma.book.get(k, 0) for k in BOOKS}
        for _ in range(12):
            ag.step()
        bad = sum(1 for r in ag.led.rows() if r["event"] == "walk_memo_check")
        return {k: ag.gamma.book.get(k, 0) - b0[k] for k in BOOKS}, bad
    finally:
        tether._PATTERN_MEMO, tether._WALK_MEMO_CHECK, tether._PURSE_OWN = keep


def check_m1() -> None:
    on, bad_on = _run(True)
    off, bad_off = _run(False)
    assert on["pattern_memo_hit"] > 0, f"no walk shared an entry by pattern: {on}"
    assert on["walk_memo_disagree"] == 0 and bad_on == 0, f"a shared hit differed: {on}"
    assert off["pattern_memo_hit"] == 0 and off["walk_memo_disagree"] == 0 and bad_off == 0, off
    assert on["walk_memo_agree"] > off["walk_memo_agree"], \
        f"MUST-FAIL: the instance key alone checked as many hits: ON {on}, OFF {off}"
    print(f"  M1: ON {on['pattern_memo_hit']:,} of {on['pattern_memo_lookup']:,} pattern lookups "
          f"hit; {on['walk_memo_agree']:,} hits checked against a fresh walk, "
          f"{on['walk_memo_disagree']} differed; OFF (instance key alone) "
          f"{off['walk_memo_agree']:,} hits checked")


def main() -> int:
    check_m1()
    print("pattern_memo: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
