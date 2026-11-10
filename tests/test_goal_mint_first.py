"""BUILD 4 ITEM 13, THE GOAL'S SLOT MINTS FIRST (TETHER_GOAL_MINT_FIRST; the reviewer 2026-11-04
r1161, r1162). FIN5E B1: at the slots look-ahead stopped on, 48 mints were deferred behind non-goal
slots and 0 were made; nothing in the mint order read the held hypothesis. Now its slots routed
MECHANISM / REFUTED-with-no-fit go first, the rest keep their order. Seconds: a gridworld agent,
the step's routed list given, _goal_first called as the step calls it.

MF-G1  two routed MECHANISM slots, the hypothesis's subject second -> it is first, the other after
MF-G2  a hypothesis slot with no residual route is counted (no_residual), never made a site
MF-G3  no hypothesis held: the order is unchanged and no row is written
The red is behavioural, the arm OFF on this tree: TETHER_GOAL_MINT_FIRST=0 fails MF-G1.

    python tests/test_goal_mint_first.py
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

M, R, H = tether.MECHANISM, tether.REFUTED, tether.HELD


def agent():
    env = world.bind(gridworld.family("default", 0))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                        ledger.Ledger())


def order(ag, routed):
    n0 = len(ag.led.rows())
    out = ag._goal_first(routed) if tether._GOAL_MINT_FIRST else routed
    rows = [r["detail"] for r in ag.led.rows()[n0:] if r.get("event") == "goal_mint_first"]
    return [r[0] for r in out], rows


def main():
    routed = [("o1.col", M, None, ""), ("o0.row", H, None, ""), ("o2.row", M, None, ""),
              ("o3.row", R, "inc", "")]
    ag = agent()
    ag._hyp = {"slots": ["o2.row", "o3.row", "o4.row"]}
    got, rows = order(ag, routed)
    assert got == ["o2.row", "o1.col", "o0.row", "o3.row"], (
        "MF-G1: the goal's MECHANISM slot does not mint first", got)
    print(f"  MF-G1 {[r[0] for r in routed]} -> {got}")
    assert rows and rows[0]["first"] == ["o2.row"] and rows[0]["no_residual"] == [
        "o3.row", "o4.row"], ("MF-G2", rows)
    print(f"  MF-G2 no residual (counted, never a site): {rows[0]['no_residual']}")
    ag2 = agent()
    ag2._hyp = None
    got2, rows2 = order(ag2, routed)
    assert got2 == [r[0] for r in routed] and not rows2, ("MF-G3", got2, rows2)
    print("  MF-G3 no hypothesis: the order is unchanged, no row")
    print("test_goal_mint_first OK")


if __name__ == "__main__":
    main()
