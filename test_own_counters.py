"""STABILITY / AGE, THE NARROW ARM (B) (TETHER_OWN_COUNTERS_DERIVED; the reviewer 2026-10-21 21:52,
2026-10-22 02:13). The slots the world's own clock writes (env.own_counted()) are counters of our
own bookkeeping: never minted for or bound, their misses never charged, still bet and recorded.

  OC1  ON: a planted step where an own-counted slot misses beside a source slot charges the
       integral and outstanding ONCE (the source's miss only); OFF charges both.
  OC2  ON: a slot the world declares own-counted (gridworld's o0.col, which OFF mints for in
       these steps) gets an "own_counter_unminted" row and no MINT row; OFF mints for it.
  OC3  ON: the fake ARC game's own-clock bet rows on age / stability are still written, the
       same rows as OFF.
  ID   OFF (both arms of the merge off): the fake ARC game's ledger on this tree equals the main
       checkout's, read by conform/identity_mod_rows.compare past the @run header. Read against
       116481a at the merge, before the main checkout moved; after it, a determinism check.

    python test_own_counters.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import gamma
import gridworld
import ledger
import tether
import world

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
MAIN = "C:/Users/Admin/Documents/GitHub/tether"
sys.path.insert(0, os.path.join(HERE, "conform"))
from identity_mod_rows import compare  # noqa: E402  the one identity reader, imported

CHILD = r'''
import json, os, sys, tempfile
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
import tether, tether_agent
from test_entry import FakeWrapper
tether._AGENT_SEED = False
for _a in ("_OWN_COUNTERS_DERIVED", "_LIBRARY_EXPLAINS"):
    if hasattr(tether, _a):
        setattr(tether, _a, sys.argv[2] == "on")
led = os.path.join(tempfile.mkdtemp(), "r.jsonl")
tether_agent.run(FakeWrapper(script={}), "fake", max_actions=12, led_path=led)
print(led)
'''


def _fake(tree: str, arm: str) -> list[dict]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")
    p = subprocess.run([sys.executable, "-B", "-c", CHILD, tree, arm], capture_output=True,
                       text=True, env=env, cwd=tree, stdin=subprocess.DEVNULL, timeout=600)
    assert p.returncode == 0, p.stderr[-2000:]
    with open(p.stdout.strip().splitlines()[-1], encoding="utf-8") as fh:
        return [json.loads(x) for x in fh if x.strip()]


def _gw(arm: bool, steps: int = 4) -> tether.Agent:
    tether._OWN_COUNTERS_DERIVED = arm
    try:
        env = world.bind(gridworld.family("default", 0, 4))
        env.own_counted = lambda: frozenset({"o0.col"})   # the world's declaration, planted
        ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="own_counters"), tether.Config(),
                          ledger.Ledger())
        for _ in range(steps):
            ag.step()
        return ag
    finally:
        tether._OWN_COUNTERS_DERIVED = False


def _charge(arm: bool) -> tuple[float, float, float]:
    tether._OWN_COUNTERS_DERIVED = arm
    try:
        env = world.bind(gridworld.family("default", 0, 4))
        env.own_counted = lambda: frozenset({"o0.stability"})
        ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="own_counters"), tether.Config(),
                          ledger.Ledger())
        i0 = ag._integral
        ag._charge({"o0.shape": tether.SlotResidual("o0.shape", "transition", 1, 2, 3.0),
                    "o0.stability": tether.SlotResidual("o0.stability", "transition", 4, 0, 2.0)})
        return ag._integral - i0, ag.outstanding("o0.shape"), ag.outstanding("o0.stability")
    finally:
        tether._OWN_COUNTERS_DERIVED = False


def main() -> int:
    tether._AGENT_SEED = False     # C-seed-X: separately born agents compared, one temperament
    on, off = _charge(True), _charge(False)
    assert on == (3.0, 3.0, 0.0) and off == (5.0, 3.0, 2.0), (on, off)
    print(f"  OC1: a stability miss (2.0) beside a shape miss (3.0): ON charges the integral "
          f"{on[0]} (once), stability outstanding {on[2]}; OFF {off[0]}, {off[2]}")
    g_off, g_on = _gw(False), _gw(True)
    mint = ("mint", "park")
    m_off = [r for r in g_off.led.rows() if r["slot"] == "o0.col" and r["event"] in mint]
    m_on = [r for r in g_on.led.rows() if r["slot"] == "o0.col" and r["event"] in mint]
    un = [r for r in g_on.led.rows() if r["event"] == "own_counter_unminted"]
    assert m_off, "PRECONDITION: OFF minted nothing for o0.col in these steps"
    assert not m_on and un and all(r["slot"] == "o0.col" for r in un), (len(m_on), len(un))
    assert "o0.col" not in g_on.bound, g_on.bound.get("o0.col")
    print(f"  OC2: o0.col declared own-counted: OFF {len(m_off)} mint rows; ON 0, unbound, and "
          f"{len(un)} own_counter_unminted rows")
    f_on, f_off = _fake(HERE, "on"), _fake(HERE, "off")

    def own_bets(rows: list[dict]) -> list:
        return [(r["cycle"], r["slot"], r["detail"].get("bound"), r["detail"].get("mass"))
                for r in rows if r["event"] == "bet"
                and str(r["slot"]).rsplit(".", 1)[-1] in ("age", "stability")]
    b_on, b_off = own_bets(f_on), own_bets(f_off)
    assert b_on and b_on == b_off and {b[2] for b in b_on} == {tether.OWN_CLOCK}, (
        len(b_on), len(b_off))
    print(f"  OC3: the fake ARC game's own-clock bets on age / stability: ON {len(b_on)} rows "
          f"= OFF's")
    base = _fake(MAIN, "off")
    a, b = ([r for r in rs if not (r["event"] == "arms" and r["slot"] == "@run")]
            for rs in (base, f_off))
    bad = compare(a, b, set())
    assert not bad, bad[:3]
    print(f"  ID: OFF on this tree = 116481a's ledger ({MAIN}): {len(b)} rows past the header "
          f"(compare())")
    print("own_counters: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
