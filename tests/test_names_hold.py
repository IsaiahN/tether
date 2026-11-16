"""NAMES THAT HOLD (TETHER_NAMES_HOLD, default ON; the reviewer 2026-11-13 r1948/r1949;
design docs/04-PLANS_AHEAD/02-BUILD_SEQUENCE_FUTURE_STATE.md item 1b). Each case asserts its
occasion before its verdict, and each must-fail runs the same frames with the arm OFF.
  N1  rule 2, the nearest same-shape name: two same-shaped cells A (left) and B (right); A vanishes
      and B moves two cells. ON: B's piece keeps B's name. MF-N1 OFF: it takes A's name (the first
      by name), the defect.
  N2  rule 2, a tie is no identity: one cell vanishes and two same-shaped cells appear at the
      same distance from it. ON: both born, the old name in maybe_same for both, never reissued.
      MF-N2 OFF: one of them takes the old name.
  N3  rule 1, unchanged means same (guaranteed by overlap, no code): an untouched cell keeps its
      name across 20 frames while others move, and through a frame break.
  N4  rule 3, a reset: X is born at home, moves, then a frame break (distractors moved and
      recoloured) lands with X back on its home cells. ON: X's name comes back (route
      "home", unsure).
      MF-N4 OFF: X is born under a new name.
  N5  the counter only goes up: no birth name is ever one issued before.
    python tests/test_names_hold.py
"""
from __future__ import annotations

import sys

import numpy as np

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import arc_percept  # noqa: E402


def name_at(o, cells) -> str | None:
    cells = frozenset(cells)
    return next((n for n, ob in o.tracked.items() if ob["cells"] == cells), None)


def run(frames):
    o = arc_percept.Objects()
    for g in frames:
        o(g)
    return o


def n1(on: bool) -> str | None:
    arc_percept._NAMES_HOLD = on
    f1 = np.zeros((3, 15), dtype=int)
    f1[1, 0] = 2
    f1[1, 10] = 2
    f2 = np.zeros((3, 15), dtype=int)
    f2[1, 12] = 2
    o = arc_percept.Objects()
    o(f1)
    a, b = name_at(o, [(1, 0)]), name_at(o, [(1, 10)])
    assert a and b and a < b, ("N1 occasion: A named before B", a, b)
    o(f2)
    got = name_at(o, [(1, 12)])
    return {a: "A", b: "B"}.get(got, got)


def n2(on: bool):
    arc_percept._NAMES_HOLD = on
    f1 = np.zeros((5, 9), dtype=int)
    f1[2, 4] = 2
    f2 = np.zeros((5, 9), dtype=int)
    f2[2, 2] = 2
    f2[2, 6] = 2
    o = arc_percept.Objects()
    o(f1)
    old = name_at(o, [(2, 4)])
    o(f2)
    p, q = name_at(o, [(2, 2)]), name_at(o, [(2, 6)])
    return old, p, q, dict(getattr(o, "maybe_same", {}))


def n4(on: bool):
    arc_percept._NAMES_HOLD = on
    f1 = np.zeros((8, 12), dtype=int)
    f1[0, 0] = 3                        # X, home (0, 0)
    for r in (3, 5, 7):
        f1[r, 1:3] = 6                  # three dominoes, colour 6
    f2 = f1.copy()
    f2[0, 0] = 0
    f2[0, 3] = 3                        # X moves (shape match)
    f3 = np.full((8, 12), 0)
    f3[0, 0] = 3                        # X back home
    for r in (3, 5, 7):
        f3[r, 8:10] = 7                 # dominoes moved and recoloured: a frame break
    o = arc_percept.Objects()
    o(f1)
    x = name_at(o, [(0, 0)])
    o(f2)
    assert name_at(o, [(0, 3)]) == x, ("N4 occasion: X tracked across its move", o.matches)
    o(f3)
    return x, name_at(o, [(0, 0)]), o.matches.get(name_at(o, [(0, 0)])), list(o.breaks)


def main() -> None:
    assert arc_percept._NAMES_HOLD is True, "the arm defaults ON"
    got = n1(True)
    assert got == "B", ("N1: the mover did not keep its name", got)
    print("  N1 ON: B moved two cells with A gone; B keeps its name (nearest same shape)")
    got = n1(False)
    assert got == "A", ("MF-N1: OFF should hand B's piece A's name (first by name)", got)
    print("  MF-N1 OFF: B's piece takes A's name -> RED (as required)")

    old, p, q, maybe = n2(True)
    assert old not in (p, q), ("N2: a tied piece took the old name", old, p, q)
    assert maybe.get(p) == [old] and maybe.get(q) == [old], ("N2: the tie not recorded", maybe)
    print(f"  N2 ON: two pieces tied at distance 2 from {old}: both born ({p}, {q}), "
          f"maybe_same records {old} for each")
    old, p, q, _m = n2(False)
    assert old in (p, q), ("MF-N2: OFF should reissue the old name to one tied piece", old, p, q)
    print("  MF-N2 OFF: one tied piece takes the old name -> RED (as required)")

    for on in (True, False):
        arc_percept._NAMES_HOLD = on
        frames = []
        for k in range(20):
            g = np.zeros((6, 12), dtype=int)
            g[0, 0] = 4                                  # untouched
            g[3, k % 10] = 2                             # a mover
            frames.append(g)
        stripes = np.zeros((6, 12), dtype=int)
        stripes[:, 4:8] = 1
        stripes[:, 8:] = 5
        stripes[0, 0] = 4                                # still untouched, through a break
        o = arc_percept.Objects()
        o(frames[0])
        keep = name_at(o, [(0, 0)])
        for g in frames[1:] + [stripes]:
            o(g)
            assert name_at(o, [(0, 0)]) == keep, ("N3: the untouched cell was renamed", on)
    print("  N3: an untouched cell keeps one name across 20 frames and a break, ON and OFF")

    x, back, how, brks = n4(True)
    assert brks and brks[-1].get("broke"), ("N4 occasion: no frame break", brks)
    assert back == x and how and how[0] == "home", ("N4: the home name did not come back",
                                                   x, back, how)
    print(f"  N4 ON: a break, X back on its home cells takes {x} back (route home)")
    x, back, how, brks = n4(False)
    assert brks and brks[-1].get("broke"), ("MF-N4 occasion: no frame break", brks)
    assert back != x, ("MF-N4: OFF should name X anew", x, back)
    print(f"  MF-N4 OFF: X born as {back}, not {x} -> RED (as required)")

    arc_percept._NAMES_HOLD = True
    seen: set = set()
    o = arc_percept.Objects()
    rng = np.random.default_rng(7)
    for _ in range(40):
        g = np.zeros((8, 8), dtype=int)
        for _k in range(3):
            g[rng.integers(0, 8), rng.integers(0, 8)] = int(rng.integers(1, 4))
        o(g)
        for n, (route, _s) in o.matches.items():
            if route == "birth":
                assert n not in seen, ("N5: a birth reused a name", n)
            seen.add(n)
    print(f"  N5: 40 random frames, {len(seen)} names, no birth reused one")
    print("names_hold: OK")


if __name__ == "__main__":
    main()
