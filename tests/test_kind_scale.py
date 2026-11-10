"""Build 1 (5), SCALE (TETHER_KIND_SCALE; Isaiah 2026-11-03 14:29 "the same kind at a different
size"; the reviewer r911): a k-fold blow-up of a shape is that shape's kind at scale k. Game-free,
about a second.

MF-S1 an L blown up 2x has the L's kind (kind_code, and form_code under K1) and scale 2; the 3x
      one scale 3.
MF-S2 (must-stay) a 1x3 bar and a 1x5 bar stay different kinds, each at scale 1.
MF-S3 a one-colour 2x2 block is one object of the dot's kind at scale 2; a two-colour 2x2 checker
      is never one object (components() is one hue per object), so nothing descales from it.
MF-S4 one tracked object, 2x2 -> 4x4: scale 2 -> 4, grew 1 shrank 0, the same name; 4x4 -> 2x2:
      shrank 1 grew 0; 2x2 -> 2x2: neither.
MF-S5 OFF (TETHER_KIND_SCALE=0, a child process): the 2x L is a different kind from the L, kind_code
      equals the hash of the L's own canonical form (the code before this part), and the tracker
      and the atom types publish no scale, grew or shrank.

    python tests/test_kind_scale.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import numpy as np

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import arc_atoms  # noqa: E402
import arc_percept as ap  # noqa: E402

L = frozenset({(0, 0), (1, 0), (2, 0), (2, 1)})


def up(cells, k):
    return frozenset((r * k + i, c * k + j) for r, c in cells for i in range(k) for j in range(k))


def board(blocks, n=12):
    b = np.zeros((n, n), dtype=int)
    for r0, c0, size, colour in blocks:
        b[r0:r0 + size, c0:c0 + size] = colour
    return b


def frames(a, b):
    """One tracked object across two boards: (its readings after the second, same name)."""
    obj = ap.Objects()

    def block():
        got = [n for n, o in obj.tracked.items() if o["colour"] == 3]
        assert len(got) == 1, ("one object of the block's colour", got)
        return got[0]
    obj(board([(2, 2, a, 3)]))
    n1 = block()
    s2 = obj(board([(2, 2, b, 3)]))
    n2 = block()
    return {x: s2.get(f"{n2}.{x}") for x in ("scale", "grew", "shrank")}, n1 == n2


def off() -> dict:
    out = {"same_kind": ap.kind_code(up(L, 2)) == ap.kind_code(L),
           "code_before": ap.kind_code(up(L, 2)) == ap._hash(ap._canon(up(L, 2))[0]),
           "types": sorted(k for k in ("scale", "grew", "shrank") if k in arc_atoms.ATTRIBUTE_TYPE)}
    obj = ap.Objects()
    obj(board([(2, 2, 2, 3)]))
    s = obj(board([(2, 2, 4, 3)]))
    out["slots"] = sorted(k for k in s if k.rsplit(".", 1)[-1] in ("scale", "grew", "shrank"))
    return out


def main():
    if "--off" in sys.argv:
        assert not ap._KIND_SCALE, "the child runs OFF"
        print(json.dumps(off()))
        return
    assert ap._KIND_SCALE, "TETHER_KIND_SCALE is ON by default"
    was = ap._KIND_CANON
    try:
        ap._KIND_CANON = True
        s1 = (ap.form_code(up(L, 2)) == ap.form_code(L) == ap.kind_code(up(L, 3)))
    finally:
        ap._KIND_CANON = was
    sc = [ap._entry(up(L, k))[4] for k in (1, 2, 3)]
    assert s1 and ap.kind_code(up(L, 2)) == ap.kind_code(L) and sc == [1, 2, 3], (
        "MF-S1 an L blown up is the L's kind", sc)
    b3, b5 = frozenset((0, c) for c in range(3)), frozenset((0, c) for c in range(5))
    assert ap.kind_code(b3) != ap.kind_code(b5) and ap._entry(b3)[4] == ap._entry(b5)[4] == 1, (
        "MF-S2 bars of different lengths stay different kinds")
    dot = ap.kind_code(frozenset({(0, 0)}))
    solid = [o for o in ap.components(board([(2, 2, 2, 3)])) if len(o["shape"]) == 4]
    checker = board([])
    checker[2:4, 2:4] = [[3, 5], [5, 3]]
    parts = [o for o in ap.components(checker) if o["colour"] in (3, 5)]
    assert len(solid) == 1 and ap.kind_code(solid[0]["shape"]) == dot and \
        ap._entry(solid[0]["shape"])[4] == 2, ("MF-S3 a one-colour 2x2 is a dot at scale 2", solid)
    assert parts and all(len(o["shape"]) < 4 for o in parts), (
        "MF-S3 a two-colour checker was one object", [sorted(o["shape"]) for o in parts])
    grew, same1 = frames(2, 4)
    shrank, same2 = frames(4, 2)
    still, same3 = frames(2, 2)
    assert grew == {"scale": 4, "grew": 1, "shrank": 0} and same1, ("MF-S4 grew", grew, same1)
    assert shrank == {"scale": 2, "grew": 0, "shrank": 1} and same2, ("MF-S4 shrank", shrank)
    assert still == {"scale": 2, "grew": 0, "shrank": 0} and same3, ("MF-S4 neither", still)
    env = {**os.environ, "TETHER_KIND_SCALE": "0", "PYTHONDONTWRITEBYTECODE": "1"}
    out = subprocess.run([sys.executable, "-B", __file__, "--off"], env=env, capture_output=True,
                         text=True, timeout=60)
    assert out.returncode == 0, out.stderr[-2000:]
    o = json.loads(out.stdout.strip().splitlines()[-1])
    assert o == {"same_kind": False, "code_before": True, "types": [], "slots": []}, ("MF-S5", o)
    print(f"  MF-S1 the L at x1, x2, x3: one kind, scales {sc}")
    print("  MF-S2 bars of 3 and 5: two kinds, each at scale 1")
    print(f"  MF-S3 a one-colour 2x2 is the dot's kind at scale 2; the checker is {len(parts)} "
          f"objects, none of 4 cells")
    print(f"  MF-S4 2x2 -> 4x4 {grew}; 4x4 -> 2x2 {shrank}; 2x2 -> 2x2 {still}; one name each")
    print(f"  MF-S5 OFF: {o}")
    print("test_kind_scale OK")


if __name__ == "__main__":
    main()
