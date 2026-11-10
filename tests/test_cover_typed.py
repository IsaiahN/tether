"""THE COVER TYPES A DECLARED HEAD'S OPERAND BEFORE IT OFFERS (TETHER_COVER_TYPED; the reviewer
2026-11-04 r1166; r1103, r1142). The census's top re-offer was subtract<o2.add_n> at o2.col,
POSITION - EXTENT, refused by subtract's declared typing only at the bind. Now the cover applies
the bind's rule (gamma.target_operand) before it offers, and counts the refusal. Seconds:
test_lit_cover's fixture, its head atom `inc` declared POSITION -> DELTA for the test (restored
after).

MF-T1  the cover's inc . dec . neg at o1.z (POSITION) read from o1.row (EXTENT) is refused at the
       cover, counted "cover: inc takes DELTA at POSITION, not EXTENT", nothing offered
MF-T2  the same path with o1.row typed DELTA is offered
The red is behavioural, the arm OFF on this tree: TETHER_COVER_TYPED=0 fails MF-T1.

    python tests/test_cover_typed.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import composer  # noqa: E402
import gamma  # noqa: E402
import test_lit_cover as tl  # noqa: E402
import test_molecule_apply as tm  # noqa: E402

AGENT = tm.agent


def run(op_type):
    def agent():
        ag, led = AGENT()
        real = ag._molecule_pass

        def mp(*a, **k):
            ag.slot_types = {**ag.slot_types, "o1.z": "POSITION", "o1.row": op_type}
            return real(*a, **k)
        ag._molecule_pass = mp
        return ag, led
    whole = composer.Bonded(composer.UNKNOWN, composer.Bonded(composer.UNKNOWN, "inc", "dec"),
                            "neg")
    ag0, _l = AGENT()
    inc = next(a for a in ag0.gamma.atoms if a.name == "inc")
    keep = dict(gamma.TARGET_OPERAND.get(inc.fn) or {})
    had = inc.fn in gamma.TARGET_OPERAND
    tm.agent = agent
    try:
        gamma.TARGET_OPERAND[inc.fn] = {"POSITION": "DELTA"}
        order, row = tl.run(whole, tm.only({"→"}))
    finally:
        tm.agent = AGENT
        if had:
            gamma.TARGET_OPERAND[inc.fn] = keep
        else:
            gamma.TARGET_OPERAND.pop(inc.fn, None)
    return [p for p in order if p.get("lit")], row


def main():
    lit, row = run("EXTENT")
    why = row["not_offered"].get("cover: inc takes DELTA at POSITION, not EXTENT")
    assert not lit and why == 1 and row["lit_cover"].get("refused for typing") == 1, (
        "MF-T1: the cover offers a path its declared typing refuses", lit, row["not_offered"])
    print(f"  MF-T1 refused at the cover: {why} x 'cover: inc takes DELTA at POSITION, not EXTENT'")
    lit2, _row2 = run("DELTA")
    assert [(p["offer"], p["left"], p["right"]) for p in lit2] == [
        ("inc . dec . neg", "o1.row", "o1.z")], ("MF-T2", lit2)
    print("  MF-T2 the well-typed path is offered")
    print("test_cover_typed OK")


if __name__ == "__main__":
    main()
