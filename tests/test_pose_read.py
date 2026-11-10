"""THE POSE, READABLE (TETHER_POSE_READ; the reviewer 2026-11-03 r915): under K1 an upright and a
turned L are one kind; `kind` (the shape label of the kind's first-seen member) and `turned` keep
the turn sayable without a new type. Game-free, about a second.

MF-P1 an upright L and a turned L on one board: the same `kind`, different `shape` (same kind 1,
      same as seen 0).
MF-P2 one tracked L turned a quarter between frames: turned 1; the same pose: turned 0; a 2x
      blow-up alone: grew 1, turned 0.
MF-P3 (must-stay) TETHER_POSE_READ=0 (a child process, K1 OFF): every other slot of the same two
      frames -- the shape labels and the pair readings included -- equals the ON run's; only
      `kind` and `turned` are absent.

    python tests/test_pose_read.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import numpy as np

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import arc_percept as ap  # noqa: E402

L = frozenset({(0, 0), (1, 0), (2, 0), (2, 1)})


def place(b, cells, r0, c0, colour):
    for r, c in cells:
        b[r0 + r, c0 + c] = colour
    return b


def name_of(obj, colour):
    got = [n for n, o in obj.tracked.items() if o["colour"] == colour]
    assert len(got) == 1, (colour, got)
    return got[0]


def two_frames(second) -> tuple[dict, str]:
    obj = ap.Objects()
    obj(place(np.zeros((12, 12), dtype=int), L, 2, 2, 3))
    s = obj(place(np.zeros((12, 12), dtype=int), second, 2, 2, 3))
    return s, name_of(obj, 3)


def frames_state() -> dict:
    b = place(place(np.zeros((12, 12), dtype=int), L, 1, 1, 3), ap._images(L)[1], 6, 6, 4)
    obj = ap.Objects()
    obj(b)
    s = obj(b)
    return {k: repr(v) for k, v in s.items()}


def main():
    if "--off" in sys.argv:
        assert not ap._POSE_READ, "the child runs OFF"
        print(json.dumps(frames_state()))
        return
    assert ap._POSE_READ, "TETHER_POSE_READ is ON by default"
    turned = ap._images(L)[1]
    b = place(place(np.zeros((12, 12), dtype=int), L, 1, 1, 3), turned, 6, 6, 4)
    obj = ap.Objects()
    s = obj(b)
    up, tn = name_of(obj, 3), name_of(obj, 4)
    same_kind = int(s[f"{up}.kind"] == s[f"{tn}.kind"])
    same_seen = int(s[f"{up}.shape"] == s[f"{tn}.shape"])
    assert (same_kind, same_seen) == (1, 0), ("MF-P1", same_kind, same_seen)
    s_t, n = two_frames(turned)
    s_s, m = two_frames(L)
    s_g, g = two_frames(frozenset((r * 2 + i, c * 2 + j) for r, c in L
                                  for i in range(2) for j in range(2)))
    got = (s_t.get(f"{n}.turned"), s_s.get(f"{m}.turned"), s_g.get(f"{g}.grew"),
           s_g.get(f"{g}.turned"))
    assert got == (1, 0, 1, 0), ("MF-P2 turned / same pose / grew alone", got)
    env = {**os.environ, "TETHER_POSE_READ": "0", "PYTHONDONTWRITEBYTECODE": "1"}
    out = subprocess.run([sys.executable, "-B", __file__, "--off"], env=env, capture_output=True,
                         text=True, timeout=60)
    assert out.returncode == 0, out.stderr[-2000:]
    off = json.loads(out.stdout.strip().splitlines()[-1])
    on = json.loads(json.dumps(frames_state()))
    extra = sorted(k for k in on if k not in off)
    assert {k.rsplit(".", 1)[-1] for k in extra} <= {"kind", "turned"} and extra and all(
        on[k] == off[k] for k in off), ("MF-P3", extra, [k for k in off if on.get(k) != off[k]])
    print(f"  MF-P1 upright and turned L: same kind {same_kind}, same as seen {same_seen}")
    print(f"  MF-P2 a quarter turn: turned {got[0]}; the same pose: {got[1]}; a 2x blow-up: "
          f"grew {got[2]}, turned {got[3]}")
    print(f"  MF-P3 OFF: {len(off)} slots equal to ON's; ON adds only {extra}")
    print("test_pose_read OK")


if __name__ == "__main__":
    main()
