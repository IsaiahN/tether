"""8b CLOSED (the reviewer 2026-11-04 r1135, r1138): a pair offset (o.dcol_oN, o.drow_oN, ...) gets
no term of its own -- the base's motion term is not borrowed (object dcol is motion across frames,
pair dcol_oN is separation in one frame: A6i), and no instrument in Gamma composes a two-source
offset (o.col = x.col - d needs a held atom whose result is another POSITION's value and a
DELTA negation; recolour takes a COLOUR operand, negate is PRED -> PRED). The 806 stay counted,
and the record says why. Seconds.

MF-P1  a termless pair reading among the slots: the reason names the pair offset and both rulings
MF-P2  a termless non-pair reading: the reason is unchanged (today's text)

    python tests/test_pair_no_term.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import tether  # noqa: E402


def main():
    why = tether._no_term_why("a leaf slot has no term", ["o1.dcol_o2"])
    assert why.startswith("a leaf slot has no term -- pair offset: no term of its own") \
        and "A6i, r1135" in why and "r1138" in why, ("MF-P1", why)
    plain = tether._no_term_why("lookup: a reading has no term", ["o1.col"])
    assert plain == "lookup: a reading has no term", ("MF-P2", plain)
    print(f"  MF-P1 {why!r}")
    print(f"  MF-P2 {plain!r}")
    print("test_pair_no_term OK")


if __name__ == "__main__":
    main()
