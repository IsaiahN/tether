"""7a(7) two readings at plan adoption (TETHER_TWO_READINGS; R3(a); the reviewer 2026-10-10
22:30Z). A plan reads bits (cost + left) and confirm (actions until it is seen to hold, Fig 12
:126); a dominated plan is dropped, the existing order (bits ascending) picks on the frontier.

  must-pass: Y and Z tie in bits, Z confirms in fewer actions: Y is dominated, Z is picked;
  1. NEVER THE SUM: Y (5 bits, 10 actions) and X (6 bits, 2 actions) are both on the frontier;
     the order picks Y, and a picker that summed the readings would pick X;
  2. a plan whose confirm cannot be counted is never dominated;
  3. arm OFF: a 10-cycle gridworld run never reaches _two_readings.

    python test_two_readings.py
"""
from __future__ import annotations

import sys

import gamma
import gridworld
import ledger
import routine as Rt
import tether
import world

sys.dont_write_bytecode = True


def _plan(n: int):
    return Rt.Until("o0.row", Rt.Act("ACTION1"), n)


def _agent():
    env = world.bind(gridworld.family("default", 0, 4))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="two_readings_fixture"),
                        tether.Config(), ledger.Ledger())


if __name__ == "__main__":
    ag = _agent()
    y, z = (5.0, 0.0, _plan(10)), (5.0, 0.0, _plan(2))
    pick = ag._two_readings("o0.row", [y, z], base=20.0)
    row = [r["detail"] for r in ag.led.rows() if r["event"] == "two_readings"][-1]
    assert pick is z and row["dominated"] == 1 and row["refute_min"] == 1, row
    print(f"  must-pass: Y dominated (tie in bits, 10 vs 2 actions); Z picked: {row['frontier']}")
    x = (6.0, 0.0, _plan(2))
    pick = ag._two_readings("o0.row", [y, x], base=20.0)
    row = [r["detail"] for r in ag.led.rows() if r["event"] == "two_readings"][-1]
    summed = min([y, x], key=lambda p: p[0] + p[1] + tether._confirm_actions(p[2]))
    assert pick is y and len(row["frontier"]) == 2 and summed is x, (row, summed)
    print("  1: Y (5 bits, 10 actions) and X (6 bits, 2 actions) both on the frontier; the order "
          "picks Y; the sum would pick X")
    odd = (5.0, 0.0, Rt.Choose("o0.row", Rt.Act("ACTION1"), Rt.Act("ACTION2")))
    assert tether._confirm_actions(odd[2]) is None
    ag._two_readings("o0.row", [y, odd, z], base=20.0)
    row = [r["detail"] for r in ag.led.rows() if r["event"] == "two_readings"][-1]
    assert any(f[2] is None for f in row["frontier"]), row
    print("  2: a plan whose confirm cannot be counted stays on the frontier")
    was = tether._TWO_READINGS
    tether._TWO_READINGS = False
    sys.path.insert(0, "conform")
    import panel  # the member exactly as the panel builds it
    g, seed = panel._gridworld("gridworld_arc_s1")
    env = world.bind(g)
    off = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"dt_default_{seed}"),
                       tether.Config(), ledger.Ledger())

    def _never(*_a, **_k):
        raise AssertionError("_two_readings ran with the arm OFF")
    off._two_readings = _never
    try:
        for _ in range(13):
            off.step()
    finally:
        tether._TWO_READINGS = was
    reached = [r["event"] for r in off.led.rows()
               if r["event"] in ("routine", "routine_cut")]
    assert reached, "fixture: the adoption path was never reached, so 3 would be vacuous"
    print(f"  3: arm OFF, 13 steps: _two_readings never ran, though the adoption path was "
          f"reached {len(reached)} times")
    print("ok")
