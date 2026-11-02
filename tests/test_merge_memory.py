"""lineage.merge's MEMORY (the reviewer 2026-11-02 r788 1, r790 2): merge reads the tips through
lineage._scan, one generation at a time, after _read -- which parses and holds every generation at
once -- ran a merge on the 1.6 GB copy out of memory (MemoryError, 07:42). N hand-written
generations of the same size, at two values of N:
  RED    the old path, lineage._read: its traced peak grows with N (2N's peak well over N's);
  GREEN  lineage._scan: its peak stays near one generation's, the same at N and 2N, and the tips
         it gives lineage.merge equal _read's.
Peaks by tracemalloc, in this process (each fixture is a few MB).

    python tests/test_merge_memory.py
"""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import tracemalloc
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import lineage  # noqa: E402

ROWS = 4000    # term rows per generation: about 0.5 MB of JSON each


def _fixture(d: Path, n: int) -> None:
    parent = None
    for k in range(n):
        g = {"lineage": 1, "game": "mem", "status": [], "evidence": [], "vindication_tail": [],
             "book": {}, "invented": {}, "dormant": [], "dormant_refused": [],
             "terms": [{"handle": f"g{k}_{i}", "atoms": ["a", "b"], "admitted": "x"}
                       for i in range(ROWS)]}
        if parent:
            g["parent"] = parent
        raw = json.dumps(g, sort_keys=True).encode()
        parent = hashlib.sha256(raw).hexdigest()[:16]
        (d / f"{lineage.PREFIX}{parent}.json").write_bytes(raw)


def _peak(fn, d: Path) -> tuple[float, object]:
    tracemalloc.start()
    out = fn(d)
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    return peak / 2**20, out


def main():
    tmp = Path(tempfile.mkdtemp(prefix="merge_mem_"))
    got = {}
    for n in (8, 16):
        d = tmp / f"n{n}"
        d.mkdir()
        _fixture(d, n)
        read_mb, gens = _peak(lineage._read, d)
        scan_mb, scanned = _peak(lineage._scan, d)
        assert lineage._tips(gens) == lineage._tips(scanned), ("the tips differ", n)
        got[n] = (read_mb, scan_mb)
    (r8, s8), (r16, s16) = got[8], got[16]
    assert r16 > 1.6 * r8, ("RED: the old read's peak should grow with N", r8, r16)
    assert s16 < 1.3 * s8 and s16 < r16 / 4, ("GREEN: the scan's peak should stay near one "
                                              "generation", s8, s16)
    print(f"test_merge_memory: _read peak {r8:.1f} MB at N=8 -> {r16:.1f} MB at N=16 (grows "
          f"with N); _scan peak {s8:.1f} -> {s16:.1f} MB (one generation); tips equal")


if __name__ == "__main__":
    main()
