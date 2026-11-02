"""K1, ONE KIND PER SHAPE (the reviewer 2026-11-02 r797; Isaiah 10:12): arc_percept.form_code over
the least of a shape's 8 rotations and mirrors (TETHER_KIND_CANON, default OFF until the legacy
read, r808), and K3a, the tracker matching a turned object by kind (TETHER_TURN_TRACK, ON).
  MF-K1  an L moved, rotated 90 / 180 / 270 and mirrored reads ONE code (colour is never in the
         cells); RED with the arm OFF, where a turn is a different code.
  MF-K2  different shapes of one size stay apart: an L, a T and an S of four cells; a 2x3 bar and
         a 3x3 square.
  POSE   canon's pose maps the canonical form back onto each image, and differs between them.
  MF-K3  an object that turns 90 degrees and moves with no overlap keeps its name through the
         tracker's shape route (Objects), with the published code left as-seen (K1 OFF); RED
         with TETHER_TURN_TRACK OFF, where it is a birth.

    python tests/test_kind_canon.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import numpy as np  # noqa: E402

import arc_percept as ap  # noqa: E402

L = frozenset({(0, 0), (1, 0), (2, 0), (2, 1)})
T = frozenset({(0, 0), (0, 1), (0, 2), (1, 1)})
S = frozenset({(0, 1), (0, 2), (1, 0), (1, 1)})
BAR = frozenset((r, c) for r in range(2) for c in range(3))
SQUARE = frozenset((r, c) for r in range(3) for c in range(3))


def variants(cells: frozenset) -> list:
    moved = frozenset((r + 5, c + 7) for r, c in cells)
    return [cells, moved, *ap._images(cells)[1:4], ap._images(cells)[4]]


def _turned() -> tuple[str, str, str]:
    """An L at (2, 2), then the same L turned a quarter and moved to (20, 20): (the first name,
    the name at the new place, its match route)."""
    b1, b2 = np.zeros((30, 30), dtype=int), np.zeros((30, 30), dtype=int)
    for r, c in L:
        b1[2 + r, 2 + c] = 3
    for r, c in ap._images(L)[1]:
        b2[20 + r, 20 + c] = 3
    obj = ap.Objects()
    obj(b1)
    first = next(n for n, o in obj.tracked.items() if o["row"] == 2 and o["col"] == 2)
    obj(b2)
    now = next(n for n, o in obj.tracked.items() if o["row"] == 20 and o["col"] == 20)
    return first, now, obj.matches.get(now, (None,))[0]


def main():
    assert not ap._KIND_CANON and ap._TURN_TRACK, "defaults: K1 OFF (r808), K3a ON"
    first, now, route = _turned()
    ap._KIND_CANON = True
    assert now == first and route == "shape", ("MF-K3: a turned object keeps its name",
                                               first, now, route)
    codes = {ap.form_code(v) for v in variants(L)}
    assert len(codes) == 1, ("MF-K1: one kind across moves, turns and a mirror", len(codes))
    poses = {ap.canon(v)[1] for v in ap._images(L)}
    for v in ap._images(L):
        best, pose = ap.canon(v)
        assert ap._images(best)[pose] == ap._norm(v), ("POSE maps canon onto the object", pose)
    assert len(poses) == 8, ("an L's 8 images read 8 poses", sorted(poses))
    apart = [ap.form_code(x) for x in (L, T, S)]
    assert len(set(apart)) == 3, "MF-K2: L, T and S are three kinds"
    assert ap.form_code(BAR) != ap.form_code(SQUARE), "MF-K2: a 2x3 bar is not a 3x3 square"
    ap._KIND_CANON = ap._TURN_TRACK = False
    try:
        off = {ap.form_code(v) for v in variants(L)}
        f_off, n_off, r_off = _turned()
    finally:
        ap._TURN_TRACK = True
    assert len(off) > 1, ("MUST-FAIL: OFF, a turn reads a different code", len(off))
    assert n_off != f_off, ("MUST-FAIL: OFF, the turned object is a birth", f_off, n_off, r_off)
    print(f"test_kind_canon: an L moved, turned 90/180/270 and mirrored -> 1 code ON, {len(off)} "
          f"codes OFF; 8 poses, each mapping the canonical form back; L / T / S -> 3 kinds; "
          f"2x3 bar != 3x3 square; an L turned and moved keeps its name {first} (route {route}), "
          f"OFF it is born as {n_off} ({r_off})")


if __name__ == "__main__":
    main()
