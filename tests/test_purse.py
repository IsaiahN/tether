"""C2 THE PURSE (the reviewer r1392, r1395, r1399, r1610), arms TETHER_PURSE_OWN (P1-P2) and
TETHER_PURSE_DEADLINE (P3).

  U1  the product-limit median: observed demand gives its median; over half the mass censored
      above what was seen gives none (MF r1399: a spend median over the same censored steps would
      lower the purse; the purse holds its prior)
  U2  the newborn: before any demand the purse is STEP_BUDGET in heads (the innate prior), a fresh
      agent's step 0 is cut at it with a purse_cut row; with MIN_REPEAT observed steps at the level
      the purse is the level's own median
  U3  owed work booked back: a payment "for" an earlier cycle adds its heads to that step's demand
      and closes the question; the step is observed once nothing is owed
  U4  the bank: a step under the purse saves the rest; a heavy step draws, never past what is
      banked; a new level starts it empty
  U5  a spent purse is "unreached at this budget", never a value nor "none": the unseen walk
      returns PURSE_CUT and the objective reads NOT_RESOLVED, not a negative (Fig 9 :60)
  U6  OFF: the gates read STEP_BUDGET's evaluation count, as before
  U7  P3: offline a think of h heads displaces h / purse presses; OFF (PURSE_DEADLINE) nothing
  U8  the purse names its source: "innate prior (STEP_BUDGET, heads)" for a newborn, "level
      median" once the level has MIN_REPEAT observed steps (r1644)
  U9  the overshoot: the first check past the allowance records where the step crossed it, with
      the heads spent then; MF: under the allowance, nothing is recorded (r1644)
  U10 RISE (r1646): a level whose every step is cut raises the purse x PURSE_RISE each step, its
      source "censored: over half cut; rising until half finish"
  U11 once half finish, the level median rules again: observed evidence can lower the purse;
      censored evidence never lowers it
  U12 OFF (TETHER_PURSE_RISE): the last purse holds

    python tests/test_purse.py
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
from sensors import NOT_RESOLVED  # noqa: E402

KM = tether.Agent._km_median


def _agent() -> tether.Agent:
    env = world.bind(gridworld.family("default", 0))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="purse"), tether.Config(),
                        ledger.Ledger())


def _rec(ag: tether.Agent, cyc: int, think: int, opened=()) -> None:
    ag._pd_at[cyc] = len(ag._pd)
    ag._pd.append({"cyc": cyc, "lvl": ag.level, "think": think, "extra": 0, "open": set(opened)})
    ag._pd_ver += 1


def check_u1() -> None:
    assert KM([(10, True), (20, True), (30, True)]) == 20
    cens = [(10, True)] + [(5000, False)] * 3
    assert KM(cens) is None, KM(cens)
    ag = _agent()
    for i, (v, seen) in enumerate(cens):
        _rec(ag, i, v, () if seen else {("cut", i)})
    spend = sorted(v for v, _ in cens)[len(cens) // 2]
    assert spend < tether.STEP_BUDGET and ag._purse() == tether.STEP_BUDGET, ag._purse()
    print(f"  U1: KM median 20 on three observed; undefined when censored; the purse holds "
          f"{ag._purse()} where a spend median would read {spend}")


def check_u2() -> None:
    ag = _agent()
    assert ag._purse() == tether.STEP_BUDGET
    ag.step()
    # TETHER_UNIT_PURSE (r1700): the newborn's step may now be stopped inside a unit first
    cut = [r for r in ag.led.rows() if r["event"] in ("purse_cut", "unit_purse_cut")
           or r["detail"].get("after") == "the purse"]
    assert cut and all("unreached at this budget" in r["detail"]["reads"] for r in cut), cut[:1]
    assert ag._pd[-1]["open"] == {("cut", 0)}, "MF: a cut step's demand was read as observed"
    ag2 = _agent()
    for i in range(tether.MIN_REPEAT):
        _rec(ag2, i, 1000 * (i + 1))
    want = KM([(1000 * (i + 1), True) for i in range(tether.MIN_REPEAT)])
    assert ag2._purse() == want, (ag2._purse(), want)
    print(f"  U2: newborn purse {tether.STEP_BUDGET} (innate prior), step 0 cut with "
          f"{len(cut)} rows naming the purse; {tether.MIN_REPEAT} observed steps -> the level's "
          f"median {want}")


def check_u3() -> None:
    ag = _agent()
    _rec(ag, 0, 400, {(0, "o0")})
    assert ag._pd[0]["open"]
    ag._clk_hs, ag._clk_h, ag._clk_h0, ag._clk_stack = [], {}, tether.cap.HEADS, []
    ag._dem_paid = [{"for": 0, "q": [0, "o0"], "slot": "o0.row", "heads": 250}]
    ag._owed_q = {}
    ag._purse_close_step(1)
    r = ag._pd[0]
    assert r["extra"] == 250 and not r["open"], r
    print("  U3: an owed lookup paid at cycle 1 adds 250 heads to cycle 0's demand and closes it")


def check_u4() -> None:
    ag = _agent()
    ag._clk_hs, ag._clk_h, ag._clk_stack = [], {}, []
    ag._owed_q, ag._dem_paid = {}, []
    p = ag._purse()
    ag._clk_h0 = tether.cap.HEADS - (p - 100)
    ag._purse_close_step(0)
    assert ag._bank == 100 and ag._bank_last == (100, 0), (ag._bank, ag._bank_last)
    ag._clk_h0 = tether.cap.HEADS - (p + 500)
    ag._purse_close_step(1)
    assert ag._bank == 0 and ag._bank_last == (0, 100), "MF: drew past what was banked"
    ag._bank = 70
    ag.level += 1
    p2 = ag._purse()                # read first: the median counts its own heads
    ag._clk_h0 = tether.cap.HEADS - (p2 - 10)
    ag._purse_close_step(2)
    assert ag._bank == 10, ("MF: the bank carried across the level", ag._bank)
    print("  U4: saved 100, a heavy step drew 100 (not 500), a new level started the bank empty")


def check_u5() -> None:
    dom = tether._PricedDomain({3})
    dom.alpha, dom.key, dom.seed, dom.counts = 10, "k", None, {3: 1}
    dom.note = lambda *_a: None
    noted = []
    dom.purse = lambda _d: True
    dom.purse_note = noted.append
    got = tether._walk_unseen(lambda v: v == 7, 5, True, dom, 10, lambda v: v)
    assert got is tether.PURSE_CUT
    hit = tether._priced_hit(lambda v: v == 7, 5, True, dom)
    assert hit is NOT_RESOLVED and noted == [None], (hit, noted)
    dom.purse = lambda _d: False
    assert tether._priced_hit(lambda v: v == 7, 5, True, dom) == 7
    print("  U5: the walk stops with PURSE_CUT; the objective reads NOT_RESOLVED, never none; "
          "uncut it finds 7")


def check_u6() -> None:
    ag = _agent()
    keep, tether._PURSE_OWN = tether._PURSE_OWN, False
    try:
        ag._spent = tether.STEP_BUDGET - 1
        assert not ag._purse_out() and ag._purse_affords(1) and not ag._purse_affords(2)
        ag._spent = tether.STEP_BUDGET
        assert ag._purse_out() and not ag._purse_cut(), "OFF: a purse cut"
    finally:
        tether._PURSE_OWN = keep
    print("  U6: OFF, the gates read STEP_BUDGET's evaluation count; no purse cut")


def check_u7() -> None:
    ag = _agent()
    p = ag._purse()
    c = ag._tc_clock_now()
    assert c["s_per_press"] == p and c["unit"] == "heads", c
    assert abs(ag._tc_displaced(p // 2, c) - 0.5) < 1e-9
    keep, tether._PURSE_DEADLINE = tether._PURSE_DEADLINE, False
    try:
        c0 = ag._tc_clock_now()
        assert ag._tc_displaced(p // 2, c0) == 0.0, c0
    finally:
        tether._PURSE_DEADLINE = keep
    print(f"  U7: offline a think of {p // 2} heads displaces 0.5 presses at purse {p}; "
          f"OFF it displaces 0")


def check_u8() -> None:
    ag = _agent()
    ag._purse()
    assert ag._purse_src == "innate prior (STEP_BUDGET, heads)", ag._purse_src
    for i in range(tether.MIN_REPEAT):
        _rec(ag, i, 100 * (i + 1))
    ag._purse()
    assert ag._purse_src == "level median", ag._purse_src
    print("  U8: newborn: innate prior (STEP_BUDGET, heads); then the level median")


def check_u9() -> None:
    ag = _agent()
    ag._clk_hs, ag._clk_h, ag._clk_stack = [], {}, [("route", 0.0)]
    a = ag._allowance()
    ag._clk_h0 = tether.cap.HEADS - (a - 10)
    assert not ag._purse_out() and ag._p_cross is None, "MF: a crossing under the allowance"
    ag._clk_h0 = tether.cap.HEADS - (a + 7)
    assert ag._purse_out()
    c = ag._p_cross
    assert c["at"] == "route" and c["spent"] >= a + 7 and c["allowance"] == a, c
    print(f"  U9: crossed in 'route' at {c['spent']} heads against {a}; nothing under it")


def check_u10_u11() -> None:
    ag = _agent()
    seen = [ag._purse()]
    for i in range(3):
        _rec(ag, i, 60000, {("cut", i)})
        seen.append(ag._purse())
    k = tether.PURSE_RISE
    assert seen == [tether.STEP_BUDGET * k ** j for j in range(4)], seen
    assert ag._purse_src == "censored: over half cut; rising until half finish"
    top = seen[-1]
    for i in range(3, 7):
        _rec(ag, i, 1000)
    got = ag._purse()
    assert got == 1000 and ag._purse_src == "level median", (got, ag._purse_src)
    ag2 = _agent()
    ag2._purse()
    for i in range(3):
        _rec(ag2, i, 1, {("cut", i)})            # censored lower bounds far below the purse
        assert ag2._purse() >= tether.STEP_BUDGET, "MF: censored evidence lowered the purse"
    print(f"  U10-U11: every step cut: {seen}; then four observed at 1000 -> the level median "
          f"{got} (from {top}); censored lower bounds never lowered it")


def check_u12() -> None:
    keep, tether._PURSE_RISE = tether._PURSE_RISE, False
    try:
        ag = _agent()
        ag._purse()
        _rec(ag, 0, 60000, {("cut", 0)})
        assert ag._purse() == tether.STEP_BUDGET and ag._purse_src == "last purse"
    finally:
        tether._PURSE_RISE = keep
    print("  U12: OFF, the last purse holds")


if __name__ == "__main__":
    for c in (check_u1, check_u2, check_u3, check_u4, check_u5, check_u6, check_u7, check_u8,
              check_u9, check_u10_u11, check_u12):
        c()
    print("purse: OK")
