"""THE ROUND'S DRAW IS ROWED "explore" (the reviewer 2026-11-08 r1485, r1486 (3); record only). The
round rank breaks a subject's equal-checked candidates by the draw position, so a pick separated
from the next only by the round, the two the same subject at equal checked counts, was the draw's.
The agent's own _b1_decided and _b1_tied on hand-made key groups; key = (class, ttb, parked,
turnable, round, subject tried, checked, draw position).

R1  same subject, equal checked: decided_by "explore", draw_in "round", tie 2, tied [[0,0],[0,0]],
    least [0,0]; a third such candidate makes the tie 3
R2  same subject, the next checked once more: "round" stays
R3  the next a different subject: "round" stays
MF  the old label (the first differing tier only) reads R1 as "round": the case this repairs

    python tests/test_hyp_label.py
"""
from __future__ import annotations

import sys
from types import SimpleNamespace

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import tether  # noqa: E402

TIERS = ("class", "ttb", "parked", "turnable", "round", "subject_tried", "checked", "explore")
A = tether.Agent


def group(*rows):
    """rows: (text, subject, round, subject tried, checked, draw position)."""
    by_text, kk = {}, {}
    for text, subj, rr, st, ck, dp in rows:
        x = (None, text, SimpleNamespace(slot=subj), text)
        by_text[text] = x
        kk[id(x)] = ("S0", (), 0, False, rr, st, ck, dp)

    def key(x):
        return kk[id(x)]
    order = [x[1] for x in sorted(by_text.values(), key=key)]
    return by_text, order, key


def label(by_text, order, key):
    dec = A._b1_decided(by_text, order, 1, TIERS, key, ())
    if dec.get("decided_by") == "explore":
        dec.update(A._b1_tied(by_text, order, 1, key, dec.get("draw_in")))
    return dec


def main():
    g1 = group(("a1", "o1.x", 0, 0, 0, 0), ("a2", "o1.x", 1, 0, 0, 1))
    r1 = label(*g1)
    got = (r1["decided_by"], r1.get("draw_in"), r1.get("tie"))
    assert got == ("explore", "round", 2), ("R1", r1)
    assert r1["tied"] == [[0, 0], [0, 0]] and r1["least"] == [0, 0], ("R1 tied", r1)
    r1b = label(*group(("a1", "o1.x", 0, 0, 0, 0), ("a2", "o1.x", 1, 0, 0, 1),
                       ("a3", "o1.x", 2, 0, 0, 2)))
    assert r1b.get("tie") == 3 and len(r1b["tied"]) == 3, ("R1: three equal, tie 3", r1b)
    r2 = label(*group(("a1", "o1.x", 0, 0, 0, 0), ("a2", "o1.x", 1, 0, 1, 1)))
    assert r2["decided_by"] == "round" and "draw_in" not in r2, ("R2", r2)
    r3 = label(*group(("a1", "o1.x", 0, 0, 0, 1), ("b1", "o2.y", 1, 0, 0, 0)))
    assert r3["decided_by"] == "round" and "draw_in" not in r3, ("R3", r3)
    by_text, order, key = g1
    a, b = key(by_text[order[0]]), key(by_text[order[1]])
    old = TIERS[next(j for j in range(len(TIERS)) if a[j] != b[j])]
    assert old == "round", ("MF: the old label reads R1 as the round", old)
    print(f"hyp_label: R1 same subject at equal counts rows {r1['decided_by']} (draw_in "
          f"{r1['draw_in']}, tie {r1['tie']}, tied {r1['tied']}, least {r1['least']}), three such "
          f"tie {r1b['tie']}; R2 unequal counts {r2['decided_by']}; R3 another subject "
          f"{r3['decided_by']}; MF the old label read R1 as {old}: 4 of 4, 1 must-fail")


if __name__ == "__main__":
    main()
