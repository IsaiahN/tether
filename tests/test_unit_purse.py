"""C2 THE PURSE INSIDE EVERY UNIT (R1 finding F2; Isaiah 2026-11-10 16:12, the reviewer r1700), arm
TETHER_UNIT_PURSE.

  P1  MF: a planted unit of N heads over the allowance stops at the allowance (cap.PurseCut at the
      limit); with no limit set it runs all N; a held unit is never stopped inside
  P2  a real step whose allowance is far below its demand writes ONE unit_purse_cut row, its
      demand censored, and runs on to its choice (r1703): a step cut inside ROUTE still writes its
      step_act and REPEAT rows, and every cut step its REPEAT row (MF: 796b600, where the cut
      unwound the whole step); thinking is NOT ended: the next step runs; OFF the step runs past
      the allowance and writes no such row
  P3  a step under the allowance is unchanged: the same rows ON and OFF
  P4  (r1705 (i), r1707 3) a cut inside the goal hypotheses' candidate building: the pass offers
      none, stops at its own purse check ("unreached at this budget: the purse"), and the step
      still writes its REPEAT row (MF: OFF the building runs whole past the allowance, no cut)
  P5  (r1715 2) the allowance spent at the proposer's entry: the conditions, phase 0's candidates
      and the group forms are skipped (the building never called), the pass ends with its own
      "unreached at this budget" row and the step writes its REPEAT row (MF: 240afa1 runs the
      building whole at the spent purse)
  P6  (r1715 2, NO STARVATION) a proposer costing about 8x the newborn allowance completes within
      a few steps, because the skipped or cut step counts as cut and PURSE_RISE doubles the purse
      (MF: with the rise off it never completes in 10 steps)

    python tests/test_unit_purse.py
"""
from __future__ import annotations

import os
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")

import cap  # noqa: E402
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def _unit(n: int) -> int:
    done = 0
    for _ in range(n):
        cap.head()
        done += 1
    return done


def _planted(limit: int | None, n: int, held: bool = False) -> tuple:
    start = cap.HEADS

    def on_limit():
        raise cap.PurseCut
    cap.LIMIT, cap.ON_LIMIT = (None, None) if limit is None else (start + limit, on_limit)
    done = 0
    try:
        if held:
            with cap.hold():
                done = _unit(n)
        else:
            done = _unit(n)
        stopped = False
    except cap.PurseCut:
        stopped, done = True, cap.HEADS - start
    finally:
        cap.LIMIT = cap.ON_LIMIT = None
    return stopped, done


def check_p1() -> None:
    on = _planted(1000, 50_000)
    off = _planted(None, 50_000)
    held = _planted(1000, 50_000, held=True)
    assert on == (True, 1000), f"MUST-FAIL: a unit over the allowance was not stopped at it: {on}"
    assert off == (False, 50_000), off
    assert held == (False, 50_000), held
    # r1701 3: a cut due inside a hold waits for the hold to exit, then fires at the next head
    start = cap.HEADS

    def on_limit():
        raise cap.PurseCut
    cap.LIMIT, cap.ON_LIMIT = start + 1000, on_limit
    after = None
    try:
        with cap.hold():
            _unit(5_000)
        inside = cap.HEADS - start
        try:
            cap.head()
            after = "no cut"
        except cap.PurseCut:
            after = "cut at the first head after the hold"
    finally:
        cap.LIMIT = cap.ON_LIMIT = None
    assert inside == 5_000 and after == "cut at the first head after the hold", (inside, after)
    print(f"  P1: 50,000-head unit, allowance 1,000: ON stopped {on}; no limit {off}; held {held}; "
          f"a cut due inside a hold: the held unit ran {inside:,} heads, then {after}")


def _agent() -> tether.Agent:
    env = world.bind(gridworld.family("default", 0))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="unit_purse"), tether.Config(),
                        ledger.Ledger())


def _steps(on: bool, allowance: int | None, n: int = 3) -> tuple:
    """`allowance` heads past what the step had spent when its first unit began (so the cut lands
    inside that unit, not before it), unlimited until then; None: the agent's own."""
    keep = tether._UNIT_PURSE
    tether._UNIT_PURSE = on
    try:
        ag = _agent()
        box = [None]
        if allowance is not None:
            unit = ag._unit

            def first_unit(on_cut, fn, *a, **k):
                if box[0] is None:
                    box[0] = ag._purse_spent() + allowance
                return unit(on_cut, fn, *a, **k)
            ag._unit = first_unit
            ag._allowance = lambda: 10 ** 15 if box[0] is None else box[0]
        per = []
        for _ in range(n):
            c0, r0 = ag.cycle, len(ag.led.rows())
            box[0] = None
            ag.step()
            rows = ag.led.rows()[r0:]
            per.append((c0, ag.cycle, [r["event"] for r in rows]))
        return ag, per
    finally:
        tether._UNIT_PURSE = keep


def check_p2() -> None:
    ag, per = _steps(True, 2_000)
    for c0, c1, evs in per:
        assert evs.count("unit_purse_cut") <= 1, evs.count("unit_purse_cut")
        assert c1 == c0 + 1, (c0, c1)
    rows = ag.led.rows()
    cuts = {r["cycle"]: r["detail"] for r in rows if r["event"] == "unit_purse_cut"}
    assert cuts, "MUST-FAIL: no unit cut at 2,000 heads"
    in_route = [c for c, d in cuts.items() if d["at"] == "ROUTE"]
    assert in_route, f"no cut inside ROUTE to read: {cuts}"
    have = {(r["cycle"], r["event"]) for r in rows if r["event"] in ("step_act", "repeat")}
    lost = [(c, e) for c in cuts for e in ("repeat",) + (("step_act",) if c in in_route else ())
            if (c, e) not in have]
    assert not lost, f"MUST-FAIL (796b600): a cut step lost its choice rows: {lost}"
    assert not ag._cut, "a purse cut ended thinking (only a deadline does)"
    assert any(("cut", c) in r["open"] for r in ag._pd for c in [r["cyc"]]), "demand not censored"
    _off, per_off = _steps(False, 2_000)
    assert all("unit_purse_cut" not in evs for _c0, _c1, evs in per_off), per_off
    d = cuts[in_route[0]]
    print(f"  P2: allowance 2,000 heads past the first unit: {len(cuts)} of {len(per)} steps cut "
          f"inside a unit (in "
          f"ROUTE at cycle {in_route[0]}: {d['site']}, spent {d['spent']:,}); every cut step "
          f"wrote its REPEAT row and the ROUTE-cut ones their step_act; the next step ran; OFF "
          f"none")


def check_p3() -> None:
    _a, on = _steps(True, None, 2)
    _b, off = _steps(False, None, 2)
    if any("unit_purse_cut" in evs for _c0, _c1, evs in on):
        print("  P3: the default allowance is crossed inside a unit on gridworld; compared by gw12 "
              "instead")
        return
    assert on == off, (on, off)
    n = sum(len(e) for *_x, e in on)
    print(f"  P3: under the allowance, the rows are the same ON and OFF ({n} rows over 2 steps)")


def _p4(on: bool) -> tuple:
    """the first step whose goal hypotheses build group candidates, with the allowance one head
    past what the step had spent when that building began"""
    keep = tether._UNIT_PURSE
    tether._UNIT_PURSE = on
    try:
        ag = _agent()
        box = [None]
        unit = ag._unit

        def at_building(on_cut, fn, *a, **k):
            if box[0] is None and "_group_cands" in fn.__code__.co_names:
                box[0] = ag._purse_spent() + 1
            return unit(on_cut, fn, *a, **k)
        ag._unit = at_building
        ag._allowance = lambda: 10 ** 15 if box[0] is None else box[0]
        for _ in range(12):
            box[0], c0 = None, ag.cycle
            ag.step()
            if box[0] is not None:
                rows = [r for r in ag.led.rows() if r["cycle"] == c0]
                return c0, rows
        return None, []
    finally:
        tether._UNIT_PURSE = keep


def check_p4() -> None:
    c, rows = _p4(True)
    assert c is not None, "precondition: no step built group candidates in 12 steps"
    cut = [r["detail"] for r in rows if r["event"] == "unit_purse_cut"]
    assert cut and cut[0]["at"] == "PLAN", f"MUST-FAIL: no PLAN cut inside the building: {cut}"
    hyp = [r["detail"].get("why") for r in rows if r["event"] == "goal_hypotheses"]
    assert any(w and w.startswith("unreached at this budget") for w in hyp), hyp
    assert any(r["event"] == "repeat" for r in rows), "the cut step lost its REPEAT row"
    c_off, rows_off = _p4(False)
    assert c_off == c and not [r for r in rows_off if r["event"] == "unit_purse_cut"], \
        "OFF cut inside the building"
    print(f"  P4: cycle {c}: cut in PLAN at {cut[0]['site']}; the pass ended '{hyp[-1]}'; REPEAT "
          f"written; OFF no cut")


def check_p5() -> None:
    ag = _agent()
    box, built = [None], [0]
    body, gc = ag._hyp_propose_body, ag._group_cands

    def spent_at_entry(before):
        box[0] = ag._purse_spent()                  # the allowance is all spent from here on
        return body(before)

    def counted(*a, **k):
        built[0] += 1
        return gc(*a, **k)
    ag._hyp_propose_body, ag._group_cands = spent_at_entry, counted
    ag._allowance = lambda: 10 ** 15 if box[0] is None else box[0]
    for _ in range(12):
        box[0], c0 = None, ag.cycle
        ag.step()
        if box[0] is not None:
            break
    assert box[0] is not None, "precondition: the proposer never ran in 12 steps"
    rows = [r for r in ag.led.rows() if r["cycle"] == c0]
    hyp = [r["detail"].get("why") for r in rows if r["event"] == "goal_hypotheses"]
    assert built[0] == 0, f"MUST-FAIL (240afa1): the building ran at a spent purse, {built[0]} x"
    assert any(w and w.startswith("unreached at this budget") for w in hyp), hyp
    assert any(r["event"] == "repeat" for r in rows), "the step lost its REPEAT row"
    print(f"  P5: cycle {c0}: allowance spent at the proposer's entry: the building called "
          f"{built[0]} times; the pass ended '{hyp[-1]}'; REPEAT written")


def _p6(rise: bool, n: int) -> int | None:
    keep = tether._PURSE_RISE
    tether._PURSE_RISE = rise
    try:
        ag = _agent()
        cond = ag._inv_conditions

        def dear(*a, **k):                          # a proposer about 8 newborn allowances deep
            for _ in range(8 * tether.STEP_BUDGET):
                cap.head()
            return cond(*a, **k)
        ag._inv_conditions = dear
        for _ in range(n):
            c0 = ag.cycle
            ag.step()
            hyp = [r["detail"] for r in ag.led.rows()
                   if r["cycle"] == c0 and r["event"] == "goal_hypotheses"]
            if hyp and not str(hyp[-1].get("why", "")).startswith("unreached at this budget"):
                return c0 + 1
        return None
    finally:
        tether._PURSE_RISE = keep


def check_p6() -> None:
    on = _p6(True, 10)
    off = _p6(False, 10)
    assert on is not None and on <= 6, f"starved with the rise on: {on}"
    assert off is None, f"MUST-FAIL: with the rise off it completed at step {off}"
    print(f"  P6: a proposer 8 allowances deep completes at step {on} with PURSE_RISE; never in "
          f"10 steps without it")


def main() -> int:
    check_p1()
    check_p2()
    check_p3()
    check_p4()
    check_p5()
    check_p6()
    print("unit_purse: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
