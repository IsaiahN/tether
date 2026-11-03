"""TF_PASS (the reviewer 2026-11-02 r849 2): the try-first sweep is one pass over the board's own
untouched kinds before the novelty release may fire. Game-free stubs (test_p2_hold's board / touch).
  MF-TF1  6 kinds, only the 6th touch moves anything: the hold stays open through the 5 empty
          touches and the 6th touch registers the actuator. OFF (b8cca33): released after 2
          empty touches, 4 kinds never touched.
  MF-TF2  N kinds whose keys churn (touching never empties the list), none pays: released after
          exactly N empty touches, one try_first_released row -- the old never-release hang
          cannot return.
  MF-TF3  after that release the count grows by m: the re-opened pass is m touches, not N + m.
  MF-TF4  OFF: the release at MIN_REPEAT empty touches, as before (test_p2_hold runs OFF).
  MF-TF5  (r850) N untouched kinds and no offered action can be aimed at an object: the kinds hold
          nothing (the hold reads the untried actions only, here 0, so try_first refuses no
          split), one try_first_no_touch row. OFF (b8cca33): the hold reads N on every step and
          never releases -- RED there.

    python tests/test_tf_pass.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import tether  # noqa: E402
from test_p2_hold import board, touch  # noqa: E402

A = tether.Agent


def arm(on: bool):
    tether._TF_PASS = on


def fresh(kinds: int, aim: bool = True):
    ag = board(kinds)
    ag._tf_len = ag._tf_left = ag._tf_rel_u = None
    ag.actions = ("A1", "A2")
    ag._running_step = "PLAN"
    ag.iface.can_touch = lambda _offered: aim
    return ag


def mf5(on: bool) -> tuple:
    arm(on)
    try:
        ag = fresh(4, aim=False)
        seen = [A._try_first_open(ag) for _ in range(3)]
        return seen, [r["detail"] for r in ag.led.rows() if r["event"] == "try_first_no_touch"]
    finally:
        arm(True)


def churn(ag, n: int):
    """kind keys that churn: the untouched list is n kinds however many were touched."""
    ag._untouched_kinds = lambda _before: [[f"k{i}"] for i in range(ag._n)]
    ag._n = n


def released(ag) -> list:
    return [r["detail"] for r in ag.led.rows() if r["event"] == "try_first_released"]


def mf1(on: bool) -> tuple:
    arm(on)
    try:
        ag = fresh(6)
        seen = [A._try_first_open(ag)]
        for i in range(6):
            if seen[-1] == 0:
                break                              # released: System 0 touches no more kinds
            touch(ag, f"o{i}", ("o9.x",) if i == 5 else ())
            seen.append(A._try_first_open(ag))
        return seen, "o5" in ag._actuators
    finally:
        arm(True)


def mf2_3(n: int, m: int) -> tuple:
    ag = fresh(n)
    churn(ag, n)
    seen = [A._try_first_open(ag)]
    for i in range(n):
        touch(ag, f"o{i}")
        seen.append(A._try_first_open(ag))
    ag._n = n + m                                  # the board shows m more kinds
    again = [A._try_first_open(ag)]
    for i in range(m):
        touch(ag, f"p{i}")
        again.append(A._try_first_open(ag))
    return seen, again, released(ag)


def main():
    assert tether._TF_PASS and tether._TRY_FIRST_PAYS, "ON by default, inside TRY_FIRST_PAYS"
    on, act_on = mf1(True)
    off, act_off = mf1(False)
    assert on == [6, 5, 4, 3, 2, 1, 0] and act_on, ("MF-TF1: one full pass, the 6th found", on)
    assert off == [6, 5, 0] and not act_off, ("MF-TF1 OFF: released after 2, 6th never", off)
    seen, again, rel = mf2_3(5, 3)
    assert seen == [5, 5, 5, 5, 5, 0], ("MF-TF2: released after exactly N empty touches", seen)
    assert again == [8, 8, 8, 0], ("MF-TF3: the re-opened pass is the growth only", again)
    assert [r["pass_len"] for r in rel] == [5, 3], ("one row per release", rel)
    no, no_rows = mf5(True)
    no_off, _ = mf5(False)
    assert no == [0, 0, 0] and len(no_rows) == 1, ("MF-TF5: nothing can touch, kinds hold none",
                                                   no, no_rows)
    assert no_off == [4, 4, 4], ("MF-TF5 OFF: the kinds hold forever (b8cca33)", no_off)
    print(f"test_tf_pass: 6 kinds, the 6th pays: ON {on} (actuator {act_on}), OFF {off} (actuator "
          f"{act_off}); churning 5, none pays: {seen}; grown by 3: {again}; released rows "
          f"pass_len {[r['pass_len'] for r in rel]}; no aimable action: ON {no} ({len(no_rows)} "
          f"row), OFF {no_off}")


if __name__ == "__main__":
    main()
