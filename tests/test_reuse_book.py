"""8c, THE REUSE BOOK (reuse.py; TETHER_REUSE_BOOK; the reviewer 2026-11-12 r1835/r1838,
DESIGN_STEP8 P6; Isaiah 11-11 07:20-07:30). Pure data, under a second.

  RB1     THE AGE WINDOW: with window 3, a head's uses stop counting after its 3rd chance in a
          context, the same window for every head; payments are still recorded.
  MF-RB1  with no window the uses keep counting past the 3rd chance (RED for RB1).
  RB2     GENERAL AFTER 2 CONTEXTS: a head paid in one context is not general; paid in a second
          (here by a musing re-test, source="muse") it is.
  RB3     RESIDENCY: kernel, then general, then reused, then one-offs, then unused.
  RB4     PERSISTENCE: drain() increments summed over two saves and load() give the same counts
          as one book that saw everything; the second-use point survives.
  RB5     AUTHORITY: a chain built from a general head outranks one built from a one-off (order
          only), and derive_window reads the median chances-to-second-use.

    python tests/test_reuse_book.py
"""
from __future__ import annotations

import sys
from types import SimpleNamespace

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import reuse  # noqa: E402


def sum_saves(*ds: dict) -> dict:
    """lineage_store._counts_apply's rule for a {key: {sub: n}} field: summed root to tip."""
    out: dict = {}
    for d in ds:
        for k, sub in d.items():
            into = out.setdefault(k, {})
            for s, n in sub.items():
                into[s] = into.get(s, 0) + n
    return out


def main() -> int:
    a, b = ("SELF", "o39", "MOTION"), ("WORLD", "o12", "COLOUR")

    # RB1 / MF-RB1
    for window, expect in ((3, 3), (None, 5)):
        bk = reuse.ReuseBook(window=window)
        for _ in range(5):
            bk.note_chance(a, "AGENT|translate")
            bk.note_use(a, "AGENT|translate", paid=True)
        got = bk.uses[(reuse._ck(a), "AGENT|translate")]
        assert got == expect, (window, got)
        assert bk.paid[(reuse._ck(a), "AGENT|translate")] == 5
    print("  RB1: window 3 counts 3 uses of 5 chances, payments all kept; "
          "MF-RB1: no window counts 5 (RED for RB1)")

    # RB2
    bk = reuse.ReuseBook()
    bk.note_chance(a, "h")
    bk.note_use(a, "h", paid=True)
    assert bk.tier("h") != "general", bk.tier("h")
    bk.note_chance(b, "h")
    bk.note_use(b, "h", paid=True, source="muse")
    assert bk.tier("h") == "general", bk.tier("h")
    print("  RB2: paid in one context -> not general; a paid musing re-test in a second -> general")

    # RB3
    bk = reuse.ReuseBook(kernel={"k"})
    for h, uses in (("g", 0), ("r", 2), ("o", 1)):
        for _ in range(uses):
            bk.note_chance(a, h)
            bk.note_use(a, h, paid=False)
    for ctx in (a, b):
        bk.note_chance(ctx, "g")
        bk.note_use(ctx, "g", paid=True)
    order = bk.residency(["u", "o", "r", "g", "k"])
    assert order == ["k", "g", "r", "o", "u"], order
    print(f"  RB3: residency {order}")

    # RB4
    one, s1 = reuse.ReuseBook(), reuse.ReuseBook()
    for bkk in (one, s1):
        for _ in range(2):
            bkk.note_chance(a, "h")
            bkk.note_use(a, "h", paid=True)
    d1 = s1.drain()
    for bkk in (one, s1):
        bkk.note_chance(b, "h")
        bkk.note_use(b, "h", paid=False)
    d2 = s1.drain()
    back = reuse.ReuseBook()
    back.load(sum_saves(d1, d2))
    for fld in ("chances", "uses", "paid", "second_use_at"):
        assert dict(getattr(back, fld)) == dict(getattr(one, fld)), (fld, getattr(back, fld))
    assert s1.drain() == {}, "a drain with nothing new must be empty"
    print("  RB4: two saves' increments, summed and loaded, equal one book's counts")

    # RB5
    bk = reuse.ReuseBook()
    for ctx in (a, b):
        bk.note_chance(ctx, "gen")
        bk.note_use(ctx, "gen", paid=True)
    bk.note_chance(a, "one")
    bk.note_use(a, "one", paid=True)
    auth = bk.authority()
    atom = SimpleNamespace
    hi, lo = auth((atom(name="gen"),)), auth((atom(name="one"),))
    assert hi > lo, (hi, lo)
    w = reuse.derive_window(one)
    assert w == 2, w
    print(f"  RB5: authority general {hi} > one-off {lo}; derive_window = {w} "
          "(median chances to a second use)")
    print("reuse_book: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
