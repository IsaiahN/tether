"""Item 2's fixture, the history window (the reviewer 2026-10-09 14:52Z, 15:26Z, 18:10Z, 18:15Z).

A term maps a slot's before-value x_t to its outcome x_(t+1), so the operand `slot~j` reads
x_(t-j): j+1 frames before the outcome. The reviewer's lags are outcome lags: "x_t = x_(t-3)" is
read by `~2`, "x_t = x_(t-2)+1" by `~1`.

Checked on a synthetic trace (so each law is exactly the one named), through the agent's own
`_lag_evidence` and `_window_lags`:
  - the rota of 3 has evidence at ~2 and not at ~1;
  - x_t = x_(t-2)+1 (mod 3) has evidence at ~1 once a value has recurred;
  - MUST-FAIL: a lag at which no earlier value recurs gets NO evidence (the test could not fail);
  - the offer ranks evidence lags first, nearest first, then the rest, nearest first;
  - GUARD-D3: the window reaches only as far back as the trace holds.

    python test_window.py
"""
from __future__ import annotations

import sys

import gamma
import gridworld
import ledger
import tether
import world

sys.dont_write_bytecode = True

SLOT = "x"


def _agent() -> tether.Agent:
    env = world.bind(gridworld.family("default", 0, 4))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="window_fixture"),
                        tether.Config(), ledger.Ledger())


def _with_trace(ag: tether.Agent, seq: list[int]) -> list:
    """The trace a slot following `seq` leaves, and its history rows (before, action, outcome)."""
    states = [{SLOT: v} for v in seq]
    ag.trace = [(states[i], "A", states[i + 1], None, None) for i in range(len(seq) - 1)]
    ag._trace_pos = None
    return [(states[i], "A", seq[i + 1], None, None) for i in range(len(seq) - 1)]


def _evidence(ag: tether.Agent, rows: list) -> dict[int, bool]:
    return {j: ag._lag_evidence(SLOT, rows, j)["evidence"] for j in range(1, len(ag.trace))}


def check_the_rota_of_3_has_evidence_at_2_not_1() -> None:
    ag = _agent()
    ev = _evidence(ag, _with_trace(ag, [4, 4, 7] * 5))
    assert ev[2] and not ev[1], ev


def check_x_t_from_x_t_minus_2_plus_1_has_evidence_at_1() -> None:
    ag = _agent()
    seq = [0, 0]
    for _ in range(12):
        seq.append((seq[-2] + 1) % 3)
    ev = _evidence(ag, _with_trace(ag, seq))
    assert ev[1], ev


def check_no_recurrence_no_evidence() -> None:
    ag = _agent()
    rows = _with_trace(ag, [1, 2, 3, 4, 5, 6])
    recs = [ag._lag_evidence(SLOT, rows, j) for j in range(1, len(ag.trace))]
    assert all(r["recurred"] == 0 and not r["evidence"] for r in recs), recs


def check_the_offer_ranks_evidence_first_then_nearest() -> None:
    ag = _agent()
    rows = _with_trace(ag, [4, 4, 7] * 5)
    ev = _evidence(ag, rows)
    got = [int(b.rsplit("~", 1)[1]) for b in ag._window_lags(SLOT, rows)]
    want = [j for j in sorted(ev) if ev[j]] + [j for j in sorted(ev) if not ev[j]]
    assert got == want, (got, want)
    assert ag._window_info[SLOT]["offered"] == len(got)


def check_the_window_reaches_only_what_the_trace_holds() -> None:
    ag = _agent()
    rows = _with_trace(ag, [1, 2, 1])
    got = ag._window_lags(SLOT, rows)
    assert got == [f"{SLOT}~1"], got
    ag.trace = []
    ag._trace_pos = None
    assert ag._window_lags(SLOT, []) == []


def check_non_lag_bindings_keep_order_and_position() -> None:
    """The reviewer 18:15Z: only lag bindings move. On a stepped agent, every slot's binding list
    with the window ON is the OFF list with lags appended after it, never interleaved."""
    ag = _agent()
    for _ in range(12):
        ag.step()
    keep = tether._WINDOW, tether._PREV_OFFER
    try:
        tether._PREV_OFFER = False
        seen = 0
        for slot in ag.slots:
            robs = ag._residual_obs(slot, ag.gamma.library[ag.bound.get(slot, tether.IDN)],
                                    ag.history(slot))
            tether._WINDOW = False
            off = ag._bindings(slot, robs)
            tether._WINDOW = True
            on = ag._bindings(slot, robs)
            assert on[:len(off)] == off, (slot, off, on)
            assert all(tether.lag_of(b) for b in on[len(off):]), (slot, on[len(off):])
            seen += len(on) > len(off)
        assert seen, "no slot was offered a lag: the guard checked nothing"
    finally:
        tether._WINDOW, tether._PREV_OFFER = keep


def _mint_window(seq: list[int], budget: int) -> tuple[dict, str]:
    """One real mint on a stepped gridworld agent whose first slot follows `seq`, under the window,
    at `budget`; returns the mint's window record and the slot."""
    ag = _agent()
    ag.step()
    slot = max(sorted(ag.slots), key=lambda s: ag.alphabet.get(s, 0))   # room for the values
    base = dict(ag.trace[-1][0])
    states = [{**base, slot: v} for v in seq]
    ag.trace = [(states[i], "A", states[i + 1], tether.NO_INTENT, None)
                for i in range(len(seq) - 1)]
    ag._trace_pos = None
    ag.bound.pop(slot, None)
    ag.cfg.work_budget = budget
    keep = tether._WINDOW
    try:
        tether._WINDOW = True
        ag.mint(slot)
    finally:
        tether._WINDOW = keep
    rows = [r for r in ag.led.rows() if r.get("step") == "MINT" and r.get("slot") == slot
            and "window" in (r.get("detail") or {})]
    return (rows[-1]["detail"]["window"] if rows else {}), slot


def _one_lag_budget(seq: list[int]) -> tuple[dict, int]:
    """The smallest budget at which the mint reaches exactly one lag (found, not set)."""
    lo, hi = 1, 1 << 16                       # lags reached rises with the budget: bisect it
    if _mint_window(seq, hi)[0].get("reached", 0) < 1:
        raise AssertionError("no budget reached a lag")
    while lo < hi:
        mid = (lo + hi) // 2
        if _mint_window(seq, mid)[0].get("reached", 0) >= 1:
            hi = mid
        else:
            lo = mid + 1
    w, _ = _mint_window(seq, lo)
    assert w["reached"] == 1, (lo, w)
    return w, lo


def check_mf_d4_the_rank_decides_the_cut() -> None:
    """The reviewer 18:25Z, item 4: before the rota's lag (~2) has recurred it has no evidence, so
    a budget reaching one lag reaches ~1 and counts ~2 beyond bound (no evidence); once it
    recurs it has evidence, ranks first, and is the lag reached."""
    # a distinct opening, so the residual clears the floor before the rota's lag recurs
    rota = [1, 2, 3, 5, 6] + [4, 4, 7] * 8
    # the first record on which the MINT'S OWN residual gives ~2 evidence (an unbounded budget)
    n = next(k for k in range(6, len(rota) + 1)
             if any(e["j"] == 2 for e in _mint_window(rota[:k], 10 ** 6)[0].get("evidence", ())))
    before, b0 = _one_lag_budget(rota[:n - 1])
    assert not any(e["j"] == 2 for e in before["evidence"]), before
    assert before["beyond_bound"]["no_evidence"] >= 1, before          # ~2 among them
    after, b1 = _one_lag_budget(rota[:n])
    assert any(e["j"] == 2 for e in after["evidence"]), after
    assert after["beyond_bound"]["evidence"] == len(after["evidence"]) - 1, after
    assert after["beyond_bound"]["no_evidence"] == after["offered"] - len(after["evidence"]), after


def _walk(seq: list[int], window: bool, two_pass: bool, budget: int = 10 ** 6):
    """The (chain, binding) pairs one real mint walks, in order, and its record (item 2b)."""
    ag = _agent()
    ag.step()
    slot = max(sorted(ag.slots), key=lambda s: ag.alphabet.get(s, 0))
    base = dict(ag.trace[-1][0])
    states = [{**base, slot: v} for v in seq]
    ag.trace = [(states[i], "A", states[i + 1], tether.NO_INTENT, None)
                for i in range(len(seq) - 1)]
    ag._trace_pos = None
    ag.bound.pop(slot, None)
    ag.cfg.work_budget = budget
    walked: list = []
    orig = ag._operand_fits

    def spy(cand, s, x):
        if s == slot:
            walked.append((cand.name, x))
        return orig(cand, s, x)
    ag._operand_fits = spy
    keep = tether._WINDOW, tether._TWO_PASS
    try:
        tether._WINDOW, tether._TWO_PASS = window, two_pass
        ag.mint(slot)
    finally:
        tether._WINDOW, tether._TWO_PASS = keep
    rows = [r for r in ag.led.rows() if r.get("step") == "MINT" and r.get("slot") == slot]
    return walked, (rows[-1] if rows else {})


def check_2b_a_pass_1_is_the_off_walk_when_no_lag_has_evidence() -> None:
    """Must-fail (a), the reviewer 19:45Z: on a record where no lag has evidence and the budget is
    not reached, the two-pass walk begins with exactly the window-OFF walk, then only lags."""
    seq = [1, 2, 3, 5, 6, 8, 9, 0]                      # no earlier value recurs at any lag
    off, _ = _walk(seq, window=False, two_pass=True)
    on, rec = _walk(seq, window=True, two_pass=True)
    assert not rec["detail"]["window"]["evidence"], rec["detail"]["window"]
    assert off and on[:len(off)] == off, (len(off), len(on))
    assert all(tether.lag_of(x) for _c, x in on[len(off):]), on[len(off):][:5]


def check_2b_d_one_and_two_pass_price_the_same_set_ties_counted() -> None:
    """Guard (d), the reviewer 19:45Z: with the budget unreached, one-pass and two-pass price the
    same (chain, binding) set; their winners agree, or the totals tie (counted, expected 0)."""
    seq = [1, 2, 3, 5, 6] + [4, 4, 7] * 5
    one, r1 = _walk(seq, window=True, two_pass=False)
    two, r2 = _walk(seq, window=True, two_pass=True)
    assert set(one) == set(two), (len(set(one) ^ set(two)))
    d1, d2 = r1.get("detail") or {}, r2.get("detail") or {}
    if d1.get("term") != d2.get("term"):
        t1 = (d1.get("term_bits") or 0) + (d1.get("left_bits") or 0)
        t2 = (d2.get("term_bits") or 0) + (d2.get("left_bits") or 0)
        assert abs(t1 - t2) < 1e-9, ("winner differs and is NOT a tie", d1.get("term"), t1,
                                     d2.get("term"), t2)
        print("     TIE recorded:", d1.get("term"), d2.get("term"), t1)


def main() -> int:
    checks = [v for k, v in globals().items() if k.startswith("check_")]
    for c in checks:
        c()
        print("ok  ", c.__name__)
    print(f"test_window: {len(checks)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
