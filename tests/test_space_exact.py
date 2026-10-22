"""SPACE_EXACT COUNTS WHAT THE CLOSURE EMITS (the reviewer 2026-10-21 22:10, 23:27; S3M). Its
docstring names the check: "enumerate with an unbounded budget and the two numbers must agree
exactly". Over the ARC atom set (TETHER_ITERATE ON, so cells and the element walk exist), every
(in type, out type) pair at depth 4, the ARC search depth.

  SX    Gamma.space_exact == the number of terms enumerate_closure yields with no budget, on
        every pair.
  MF-SX the old count (by out-type alone, never through _iter_step; kept here as the defect
        reintroduced) disagrees with the enumeration on at least one pair -- it held chains
        _iter_step refuses (owner . shape . cells . {quantifier}).

    python tests/test_space_exact.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
sys.path.insert(0, _repo.ROOT)

import arc_atoms  # noqa: E402
import arc_predict  # noqa: E402
import gamma  # noqa: E402
from gamma import IDN_NAME, Gamma, accepts_type  # noqa: E402

DEPTH = 4


def old_count(units, in_type: str, out_type: str, max_depth: int) -> int:
    """The count before the fix: by out-type alone."""
    free = [u for u in units if not any(a.name == IDN_NAME for a in u.atoms)]
    total = sum(1 for u in units if accepts_type(u, in_type) and u.out_type == out_type)
    live: dict[str, int] = {}
    for u in free:
        if accepts_type(u, in_type):
            live[u.out_type] = live.get(u.out_type, 0) + 1
    for _ in range(2, max_depth + 1):
        nxt: dict[str, int] = {}
        for t, n in live.items():
            for u in free:
                if accepts_type(u, t):
                    nxt[u.out_type] = nxt.get(u.out_type, 0) + n
        live = nxt
        total += live.get(out_type, 0)
    return total


def main() -> int:
    assert arc_atoms._ITERATE, "PRECONDITION: TETHER_ITERATE off, so there is no element walk"
    g = Gamma(gamma.primitives_once(arc_atoms.three_spaces(arc_predict.predict())))
    units = g.units()
    ins = sorted({t for u in units if not u.atoms[0].polymorphic for t in u.atoms[0].accepts})
    outs = sorted({u.out_type for u in units})
    pairs, old_bad, yielded = 0, [], 0
    for i in ins:
        for o in outs:
            n = sum(1 for _ in g.enumerate_closure(i, o, DEPTH, budget=10**9))
            assert Gamma.space_exact(units, i, o, DEPTH) == n, (i, o, n)
            if old_count(units, i, o, DEPTH) != n:
                old_bad.append((i, o))
            pairs, yielded = pairs + 1, yielded + n
    print(f"  SX: space_exact == the unbudgeted enumeration on all {pairs} type pairs at depth "
          f"{DEPTH} ({len(units)} units, {yielded:,} terms yielded)")
    assert old_bad, "MF-SX did not fail: the old out-type count agreed everywhere"
    print(f"  MF-SX: the old out-type count disagrees on {len(old_bad)} of {pairs} pairs "
          f"(e.g. {old_bad[0][0]} -> {old_bad[0][1]})")
    print("space_exact: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
