"""B2, TAKE THE BEST OVER CONTACT KINDS (TETHER_HYP_LEARN; the reviewer 2026-11-08 r1479, r1480;
Isaiah 10:13). A real agent; the agent's own cue order (_b2_cues), key (_b2_ttb_key) and ending
credit (_b2_credit).

L1  no history: every validity 0.5, so the cue order IS Isaiah's levels, and an L1 candidate goes
    before an L3a one
L2  own history L3a paid 4 of 10, L1 paid 0 of 10: L3a goes before L1 (validity moved the order)
L3  two candidates sharing L1, one with L3a and one without: L3a decides only once L1 (and every
    earlier cue) fails to discriminate -- a candidate with L2 instead beats the L3a one
LW  r1480: an inherited record calls L3a "pays" (at or above the mean inherited validity); five
    own L3a holds all fail; w_L3a falls to 0 and L3a moves below L1 within the game series
L0  r1481 (1): no history, an L0 candidate (about the subject itself) before an L1 one; L0 paid 0
    of 5 against L1's 2 of 5, L1 first
TH  r1481 (2): one failed L1 hold, L1 keeps its level's slot; three failed L1 holds against L3a's
    1 of 3 paid, L3a before L1. MF-TH: the threshold removed, one failure sinks L1 below the
    untried kinds
MF  a TALLY (count of kinds) puts a three-weak-kind candidate (L3c, L4, L5+) ahead of a one-strong
    one (L1); Take The Best puts L1 first, and the test catches the tally

    python tests/test_hyp_learn.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import test_group_row as G  # noqa: E402

tether = G.tether


def fresh():
    ag, _atoms, _st = G.agent()
    for d in (ag._b2_kinds, ag._b2_cells, ag._b2_kinds_inh, ag._b2_cells_inh, ag._b2_wk):
        d.clear()
    return ag


def first(ag, a, b):
    """Which of two has-sets Take The Best puts first, under the agent's current cue order."""
    cues = ag._b2_cues()
    return "a" if ag._b2_ttb_key(a, cues) < ag._b2_ttb_key(b, cues) else "b"


def main():
    ag = fresh()
    assert ag._b2_cues() == tether._B2_CUES, ("L1: no history, the levels", ag._b2_cues())
    assert first(ag, {"L1"}, {"L3a"}) == "a", "L1: L1 before L3a"

    ag = fresh()
    for i in range(10):
        ag._b2_credit([("n", "L3a")], i < 4, "parked")
        ag._b2_credit([("n", "L1")], False, "parked")
    cues = ag._b2_cues()
    assert cues.index("L3a") < cues.index("L1") and first(ag, {"L3a"}, {"L1"}) == "a", (
        "L2: L3a 4/10 before L1 0/10", cues)

    ag = fresh()
    assert first(ag, {"L1", "L3a"}, {"L1"}) == "a", "L3: L1 ties, L3a decides"
    assert first(ag, {"L1", "L3a"}, {"L1", "L2"}) == "b", "L3: L2 discriminates first"

    ag = fresh()
    ag._b2_kinds_inh.update({"L3a": [10, 0, 0, 6], "L1": [10, 0, 0, 1]})
    c0 = ag._b2_cues()
    assert c0.index("L3a") < c0.index("L1"), ("LW: inherited L3a above L1", c0)
    for _ in range(5):
        ag._b2_credit([("n", "L3a")], False, "stalled")
    c1, wl = ag._b2_cues(), list(ag._b2_wk["L3a"])
    assert wl == [0, 5] and c1.index("L3a") > c1.index("L1"), (
        "LW: the call failed five times, L3a falls below L1", wl, c1)

    ag = fresh()                        # r1481 (1): L0, about the subject itself, leads
    assert first(ag, {"L0"}, {"L1"}) == "a", "L0: no history, L0 before L1"
    for i in range(5):
        ag._b2_credit([("n", "L0")], False, "parked")
        ag._b2_credit([("n", "L1")], i < 2, "parked")
    assert first(ag, {"L0"}, {"L1"}) == "b", ("L0: 0/5 against 2/5, L1 first", ag._b2_cues())

    ag = fresh()                        # r1481 (2): one ending does not overturn the levels
    ag._b2_credit([("n", "L1")], False, "parked")
    one = ag._b2_cues()
    assert one.index("L1") == 1, ("TH: one failed L1 hold, L1 holds its slot", one)
    saved = tether._B2_MIN_EVIDENCE
    tether._B2_MIN_EVIDENCE = 0
    try:
        mf_th = ag._b2_cues()
    finally:
        tether._B2_MIN_EVIDENCE = saved
    assert mf_th.index("L1") > mf_th.index("L1b"), ("MF-TH: no threshold, L1 sinks", mf_th)
    for _ in range(2):
        ag._b2_credit([("n", "L1")], False, "parked")
    for i in range(3):
        ag._b2_credit([("n", "L3a")], i < 1, "parked")
    three = ag._b2_cues()
    assert three.index("L3a") < three.index("L1"), ("TH: L1 0/3 against L3a 1/3", three)

    ag = fresh()
    weak, strong = {"L3c", "L4", "L5+"}, {"L1"}
    tally = sorted([("weak", weak), ("strong", strong)], key=lambda p: -len(p[1]))[0][0]
    assert tally == "weak", "MF: the tally's own order (the case a tally gets wrong)"
    assert first(ag, strong, weak) == "a", ("MF: Take The Best puts the one strong kind first",
                                            tally)
    print(f"hyp_learn: L1 levels {list(tether._B2_CUES[:3])}... L1 before L3a; L2 cue order after "
          f"history {list(cues[-3:])} (L3a before L1); L3 L3a decides only after L1 ties, L2 "
          f"before it; LW the call held/failed {wl} -> L3a {c0.index('L3a')} -> "
          f"{c1.index('L3a')} in the cue order; L0 leads with no history, yields to L1 on "
          f"history; TH one failed L1 keeps slot {one.index('L1')}, three put L3a "
          f"({three.index('L3a')}) before L1 ({three.index('L1')}); MF-TH no threshold sinks L1 to "
          f"{mf_th.index('L1')}; MF a tally puts the three-weak candidate first, Take The Best the "
          "strong one: 7 of 7, 2 must-fails")


if __name__ == "__main__":
    main()
