"""THE COVER'S IDENTICAL OFFERS COLLAPSED (TETHER_COVER_DEDUPE; the reviewer 2026-11-04 r1163 FIX 2;
Fig 12 :126 "Bits price the description"). The end-of-Build-3 A/B's census on ls20: one step's
cover made 1,709,313 offers, 75,871 distinct (slot, term, operand), one repeated 822 times -- the
same chain from paths that differ only in a middle leaf whose slots carry the same term. Seconds:
test_lit_cover's fixture with the middle leaf `dec` read on two slots of o1 (o1.col, o1.h).

MF-D1  the two paths with the same (slot, term, operand) are ONE offer, copies 2, lit_cover
       collapsed 1; a distinct offer (operand o1.w, inc read twice) is still offered; OFF: every
       copy (4 offers)
The red is behavioural, the arm OFF on this tree: TETHER_COVER_DEDUPE=0 fails MF-D1.

    python tests/test_cover_dedupe.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import composer  # noqa: E402
import test_lit_cover as tl  # noqa: E402
import test_molecule_apply as tm  # noqa: E402

AGENT = tm.agent


def agent():
    ag, led = AGENT()
    real = ag._molecule_pass

    def mp(*a, **k):
        ag.bound.update({"o1.h": "dec", "o1.w": "inc"})   # dec twice on o1; inc twice on o1
        return real(*a, **k)
    ag._molecule_pass = mp
    return ag, led


def main():
    whole = composer.Bonded(composer.UNKNOWN, composer.Bonded(composer.UNKNOWN, "inc", "dec"),
                            "neg")
    tm.agent = agent
    try:
        order, row = tl.run(whole, tm.only({"→"}))
    finally:
        tm.agent = AGENT
    lit = sorted((p["offer"], p["left"], p["right"], p.get("copies")) for p in order
                 if p.get("lit"))
    want = [("inc . dec . neg", "o1.row", "o1.z", 2), ("inc . dec . neg", "o1.w", "o1.z", 2)]
    assert lit == want and row["lit_cover"].get("collapsed") == 2, (
        "MF-D1: identical cover offers are not collapsed", lit, row.get("lit_cover"))
    print(f"  MF-D1 {lit}; lit_cover {row['lit_cover']}")
    print("test_cover_dedupe OK")


if __name__ == "__main__":
    main()
