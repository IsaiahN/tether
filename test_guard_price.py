"""F408, every named guard priced (TETHER_GUARD_PRICE; Fig 12 :99-102; the reviewer 2026-10-10
21:31Z). A guard is a choice among the G on offer, so it costs log2(G+1); no guard is the +1 slot.

  must-pass: ON, an intent guard and "no intent" cost log2(G+1); unguarded costs 0; ACTED_* is
     unchanged (its referent term stays, the reviewer 2026-10-04);
  1. OFF, every intent guard costs 0, as before F408;
  2. one function: every cost site in tether.py calls _guard_bits (no inline guard price), and a
     short ON run charges intent guards through it.

    python test_guard_price.py
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

import gamma
import gridworld
import interface as IFace
import ledger
import tether
import world

sys.dont_write_bytecode = True

CYCLES = 10   # anchor: the 5-minute per-item budget (Isaiah 2026-10-10 16:22 CDT)


if __name__ == "__main__":
    was = tether._GUARD_PRICE
    tether._GUARD_PRICE = True
    for g in (IFace.TOUCH, IFace.ELICIT, tether.NO_INTENT):
        for n in (1, 3):
            assert tether._guard_bits(g, n) == math.log2(n + 1), (g, n)
    assert tether._guard_bits(None, 3) == 0.0
    acted = tether._guard_bits(tether.ACTED_SELF, 3, 2)
    assert acted == math.log2(4) + math.log2(3), acted
    print("  must-pass: ON, intent guards and 'no intent' cost log2(G+1); unguarded 0; ACTED_* "
          "unchanged")
    tether._GUARD_PRICE = False
    intents = (IFace.TOUCH, IFace.ELICIT, tether.NO_INTENT)
    assert all(tether._guard_bits(g, 3) == 0.0 for g in intents)
    assert tether._guard_bits(tether.ACTED_SELF, 3, 2) == acted
    print("  1: OFF, every intent guard costs 0, as before F408")
    src = Path(tether.__file__).read_text(encoding="utf-8")
    calls = len(re.findall(r"_guard_bits\(", src)) - 1                  # minus the def
    assert calls >= 5 and "log2(len(_gs)" not in src, calls
    tether._GUARD_PRICE = True
    charged, real = [], tether._guard_bits

    def spy(guard, offered, refs=0):
        out = real(guard, offered, refs)
        if guard not in (None, tether.ACTED_SELF, tether.ACTED_ON) and out > 0:
            charged.append(guard)
        return out
    tether._guard_bits = spy
    try:
        env = world.bind(gridworld.family("default", 1, CYCLES))
        ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="guard_price_fixture"),
                          tether.Config(), ledger.Ledger())
        for _ in range(CYCLES):
            ag.step()
    finally:
        tether._guard_bits = real
        tether._GUARD_PRICE = was
    assert charged, "fixture: no intent guard was priced in the run"
    kinds = sorted(set(map(str, charged)))
    print(f"  2: {calls} cost sites call _guard_bits and none prices inline; a {CYCLES}-cycle "
          f"ON run charged {len(charged)} intent-guard prices through it ({kinds})")
    print("ok")
