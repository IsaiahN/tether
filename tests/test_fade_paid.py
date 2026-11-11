"""r1661 (A), POSITIVES FADE TOO (Isaiah 2026-11-10 11:41, 11:47; the reviewer r1661), arm
TETHER_FADE_PAID; r1663 (C) TETHER_FADE_FAILURES; r1665 the master, TETHER_GENERAL.

  F1  MF: a weight paid 3 times then unused reads 3 * 0.5**(gap / (4 h)), falling toward 0 (the
      seed p); OFF it reads 3 whatever the gap
  F2  one more pay restores the full count (4); an against since the last read restores it too
  F3  the raw count never fades: the record read (_pa) and the carry write read 3, and `against`
      decays exactly as OFF
  C1  with TETHER_FADE_FAILURES OFF a refusal, a rejection and an against left alone keep their
      full weight; MF: ON fades them
  G1  TETHER_GENERAL=0 forces FADE_FAILURES and FADE_PAID OFF; MF: unset, they read ON

    python tests/test_fade_paid.py
"""
from __future__ import annotations

import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")
# Piece 1: these checks read the CYCLE clock (TETHER_FADE_BY_STORE=0, r1677); the store clock is
# tests/test_store_clock.py
os.environ.setdefault("TETHER_FADE_BY_STORE", "0")

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

KEY = ("K",)


def _agent() -> tether.Agent:
    env = world.bind(gridworld.family("default", 0))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="fade_paid"), tether.Config(),
                        ledger.Ledger())


def _arm(on: bool) -> bool:
    keep, tether._FADE_PAID = tether._FADE_PAID, on
    return keep


def _paid3(on: bool) -> tuple:
    """Three pays at cycle 0, then reads at gaps of 4 h and 40 h."""
    keep = _arm(on)
    try:
        ag = _agent()
        h = ag.gamma.halflife or tether.REJECTION_HALFLIFE
        ag._rf_standing("walk", KEY)["paid"] += 3
        p0 = ag._rf_standing("walk", KEY)["paid"]
        ag.cycle = int(4 * h)
        p1 = ag._rf_standing("walk", KEY)["paid"]
        ag.cycle = int(40 * h)
        p2 = ag._rf_standing("walk", KEY)["paid"]
        return ag, h, (p0, p1, p2)
    finally:
        _arm(keep)


def check_f1() -> None:
    ag, h, (p0, p1, p2) = _paid3(True)
    want = 3 * 0.5 ** (int(4 * h) / (4 * h))
    assert p0 == 3, p0
    assert p1 < 3, f"MUST-FAIL: a weight unused for 4 h still reads {p1}"
    assert abs(p1 - want) < 1e-5, (p1, want)
    assert p2 < 0.01, p2
    _ag, _h, off = _paid3(False)
    assert off == (3, 3, 3), off
    print(f"  F1: paid 3, unused: {p0} -> {p1:.4f} at 4 h -> {p2:.6f} at 40 h (h = {h}); "
          f"OFF {off}")


def check_f2_f3() -> None:
    keep = _arm(True)
    try:
        ag, h, _ = _paid3(True)
        tether._FADE_PAID = True
        st = ag._rf_standing("walk", KEY)
        st["paid"] += 1
        back = ag._rf_standing("walk", KEY)["paid"]
        assert back == 4, f"one pay did not restore the count: {back}"
        ag.cycle += int(4 * h)
        faded = ag._rf_standing("walk", KEY)["paid"]
        ag._rf_standing("walk", KEY)["against"] += 1
        by_against = ag._rf_standing("walk", KEY)["paid"]
        assert faded < 4 and by_against == 4, (faded, by_against)
        rec = ag._reflex_carry()
        pa = tether._pa(ag._reflexes["walk"], KEY)
        assert pa[0] == 4, pa
        assert rec is not None and ["walk", ["K"], 4] in rec["paid"], rec
        on = _agent()
        on._rf_standing("walk", KEY)["against"] += 2
        on.cycle = 7
        a_on = on._rf_standing("walk", KEY)["against"]
        tether._FADE_PAID = False
        off = _agent()
        off._rf_standing("walk", KEY)["against"] += 2
        off.cycle = 7
        a_off = off._rf_standing("walk", KEY)["against"]
        assert a_on == a_off, (a_on, a_off)
    finally:
        _arm(keep)
    print(f"  F2: one pay restores 4; unused again {faded:.4f}, one against restores {by_against}")
    print(f"  F3: _pa reads {pa}; the carry writes {rec['paid']}; against at cycle 7 "
          f"{a_on:.4f} ON = {a_off:.4f} OFF")


def _fail_arm(on: bool) -> tuple:
    keep = (gamma._FADE_FAILURES, tether.G_FADE_FAILURES)
    gamma._FADE_FAILURES = tether.G_FADE_FAILURES = on
    return keep


def _failures_left(on: bool) -> tuple:
    """A refusal and an against taken at cycle 0, read after 4 h of nothing."""
    keep = _fail_arm(on)
    try:
        ag = _agent()
        h = ag.gamma.halflife or tether.REJECTION_HALFLIFE
        st = gamma.Standing(last_tick=0)
        st.refusals = st.rejections = 2.0
        st.decay(int(4 * h), h)
        ag._rf_standing("walk", KEY)["against"] += 2
        ag.cycle = int(4 * h)
        return st.refusals, st.rejections, ag._rf_standing("walk", KEY)["against"]
    finally:
        gamma._FADE_FAILURES, tether.G_FADE_FAILURES = keep


def check_c1() -> None:
    specialist = _failures_left(False)
    assert specialist == (2.0, 2.0, 2), \
        f"TETHER_FADE_FAILURES OFF still faded a failure: {specialist}"
    general = _failures_left(True)
    assert all(v < 2 for v in general), f"MUST-FAIL: ON left a failure unfaded: {general}"
    print(f"  C1: refusals, rejections, against left alone 4 h: OFF {specialist}; "
          f"ON {tuple(round(v, 4) for v in general)}")


PROBE = ("import _repo, gamma, tether; "
         "print(int(gamma._GENERAL), int(gamma._FADE_FAILURES), int(tether._FADE_PAID))")


def _probe(general: str | None) -> str:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    if general is not None:
        env["TETHER_GENERAL"] = general
    p = subprocess.run([sys.executable, "-c", PROBE], capture_output=True, text=True, env=env,
                       cwd=os.path.dirname(os.path.abspath(__file__)), timeout=300)
    assert p.returncode == 0, p.stderr[-2000:]
    return p.stdout.strip().splitlines()[-1]


def check_g1() -> None:
    specialist = _probe("0")
    assert specialist == "0 0 0", f"TETHER_GENERAL=0 left a fade switch ON: {specialist}"
    general = _probe(None)
    assert general == "1 1 1", f"MUST-FAIL: without the master the fades read {general}"
    print(f"  G1: TETHER_GENERAL=0 reads GENERAL, FADE_FAILURES, FADE_PAID = {specialist}; "
          f"unset {general}")


def main() -> int:
    check_f1()
    check_f2_f3()
    check_c1()
    check_g1()
    print("fade_paid: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
