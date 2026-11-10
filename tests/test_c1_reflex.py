"""C1, THE REFLEX CARRY'S OTHER HALF (the reviewer 2026-11-09 r1592 3, r1600 Q3, r1602), arm
TETHER_REFLEX_CARRY_AGAINST.

  X1  MF: a reflex carried with 3 paid and 3 against does not start tilted: its first-read margin
      (1 + carried paid + paid - against) is a fresh reflex's (1); OFF it starts at 4
  X2  the carried against decays from the game's start on play's clock (cycle c: 3 * 0.5**(c/h))
  X3  the load keeps the latest write per key (3 then 1 reads 1), not a sum
  X4  a write carries each key's decayed against; OFF the record has no "against"

    python tests/test_c1_reflex.py
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

KEY = ("K",)


def _agent() -> tether.Agent:
    env = world.bind(gridworld.family("default", 0))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="c1_reflex"), tether.Config(),
                        ledger.Ledger())


def _carried(ag: tether.Agent, *against: float) -> None:
    ag._reinvent_carried([{"kind": "reflex", "name": f"x_reflex_{i}", "paid": [["walk", ["K"], 3]]
                           if i == 0 else [], "loss": [], "against": [["walk", ["K"], a]]}
                          for i, a in enumerate(against)])


def _arm(on: bool) -> bool:
    keep, tether._REFLEX_CARRY_AGAINST = tether._REFLEX_CARRY_AGAINST, on
    return keep


def _margin(ag: tether.Agent) -> float:
    st = ag._rf_standing("walk", KEY)
    return 1 + ag._rf_in("walk", KEY) + st["paid"] - st["against"]


def check_x1_x3() -> None:
    if not tether._REFLEX_CARRY:
        print("  X1-X3: skipped, TETHER_REFLEX_CARRY OFF")
        return
    keep = _arm(True)
    try:
        ag = _agent()
        _carried(ag, 3.0)
        m = _margin(ag)
        assert m == 1.0, f"MUST-FAIL: 3 paid / 3 against started tilted: margin {m}"
        ag2 = _agent()
        ag2.cycle = 4
        _carried(ag2, 3.0)
        a = ag2._rf_standing("walk", KEY)["against"]
        h = ag2.gamma.halflife or tether.REJECTION_HALFLIFE
        assert abs(a - 3.0 * 0.5 ** (4 / h)) < 1e-9, a
        ag3 = _agent()
        _carried(ag3, 3.0, 1.0)
        assert ag3._rf_against_in[("walk", KEY)] == 1.0, ag3._rf_against_in
        _arm(False)
        off = _agent()
        _carried(off, 3.0)
        assert _margin(off) == 4.0, _margin(off)
    finally:
        _arm(keep)
    print("  X1: 3 paid / 3 against carried starts at margin 1 (a fresh reflex's); OFF at 4")
    print(f"  X2: at cycle 4 the carried 3.0 reads {a:.4f} (= 3 * 0.5**(4/{h}))")
    print("  X3: two writes, 3 then 1: the load keeps 1")


def check_x4() -> None:
    keep = _arm(True)
    try:
        ag = _agent()
        ag._rf_standing("walk", KEY)["against"] = 2.0
        rec = ag._reflex_carry()
        _arm(False)
        ag_off = _agent()
        ag_off._rf_standing("walk", KEY)["against"] = 2.0
        rec_off = ag_off._reflex_carry()
    finally:
        _arm(keep)
    assert rec is not None and rec["against"] == [["walk", ["K"], 2.0]], rec
    assert rec_off is None or "against" not in rec_off, rec_off
    print(f"  X4: a write carries {rec['against']}; OFF the record carries no against")


def main() -> int:
    check_x1_x3()
    check_x4()
    print("c1_reflex: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
