"""Build 1 (4), THE canon() MEMO (TETHER_CANON_MEMO; the reviewer 2026-11-03 r909): each cell set's
canonical form, pose and both codes are computed once per game. Game-free, under a second.

MF-K15 (a) a cell set read twice, as a list and as a frozenset, computes its 8 images once (twice
       for the canonical form's pose), not again; canon_reset empties the memo and the next read
       computes again.
       (b) the values equal the unmemoised ones (TETHER_CANON_MEMO=0, a child process) for all
       8 images of three shapes: canon, kind_code, form_code under K1 OFF and ON, code_pair.

    python tests/test_canon_memo.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import arc_percept as ap  # noqa: E402

SHAPES = [{(0, 0), (1, 0), (2, 0), (2, 1)}, {(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)},
          {(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)}]


def values() -> list:
    out = []
    was = ap._KIND_CANON
    try:
        for s in SHAPES:
            for img in ap._images(s):
                cells = sorted(img)
                ap._KIND_CANON = False
                off = ap.form_code(cells)
                ap._KIND_CANON = True
                on = ap.form_code(cells)
                best, pose = ap.canon(cells)
                out.append([sorted(best), pose, ap.kind_code(cells), off, on,
                            list(ap.code_pair(cells))])
    finally:
        ap._KIND_CANON = was
    return out


def main():
    if "--values" in sys.argv:
        print(json.dumps(values()))
        return
    assert ap._CANON_MEMO, "TETHER_CANON_MEMO is ON by default"
    calls = [0]
    real = ap._images

    def spy(cells):
        calls[0] += 1
        return real(cells)
    ap._images = spy
    try:
        ap.canon_reset()
        cells = [[0, 0], [1, 0], [2, 0], [2, 1]]
        first = ap.canon(cells)
        n1 = calls[0]
        again = (ap.canon(cells), ap.canon(frozenset(map(tuple, cells))), ap.kind_code(cells),
                 ap.code_pair(cells))
        n2 = calls[0]
        ap.canon_reset()
        ap.canon(cells)
        n3 = calls[0]
    finally:
        ap._images = real
    assert n1 == 2 and n2 == n1, ("MF-K15a a cell set read again computed its images again",
                                  n1, n2)
    assert again[0] == again[1] == first and n3 == n1 + 2, ("MF-K15a reset", n3)
    env = {**os.environ, "TETHER_CANON_MEMO": "0", "PYTHONDONTWRITEBYTECODE": "1"}
    out = subprocess.run([sys.executable, "-B", __file__, "--values"], env=env,
                         capture_output=True, text=True, timeout=60)
    assert out.returncode == 0, out.stderr[-2000:]
    off = json.loads(out.stdout.strip().splitlines()[-1])
    on = json.loads(json.dumps(values()))
    assert on == off, ("MF-K15b memo ON values != OFF", next(
        (a, b) for a, b in zip(on, off, strict=True) if a != b))
    print(f"  MF-K15a images computed {n1} times for the first read, 0 for 4 more reads "
          f"(list, frozenset, kind_code, code_pair), {n3 - n1} after canon_reset")
    print(f"  MF-K15b {len(on)} images of {len(SHAPES)} shapes: canon, kind_code, form_code K1 "
          f"OFF / ON and code_pair equal to TETHER_CANON_MEMO=0")
    print("test_canon_memo OK")


if __name__ == "__main__":
    main()
