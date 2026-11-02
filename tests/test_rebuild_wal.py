"""The store rebuild's WAL (the reviewer 2026-11-02 r794 3): every save in lineage_store._rebuild
rewrites the fold blob, and with no checkpoint the WAL grew with saves x blob (17.6 GB at about save
120 of 250 on the 3-way copy, 2026-11-02). Hand-written saves, a chain whose blob grows and a branch
joined by lineage.merge, rebuilt (the continue arm off) at N and 2N saves, the WAL read after each:
  RED    WAL_BOUND_BYTES None (no checkpoint): the WAL's peak grows with N (2N's well over N's);
  GREEN  the bound set small: the peak never passes the bound plus the largest one save (one
         save's own WAL grows with the blob), and the store equals the archive fold.

    python tests/test_rebuild_wal.py
"""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import lineage  # noqa: E402
import lineage_store  # noqa: E402

ROWS = 60           # rows each save adds, so the fold blob grows by about 6 KB a save
BOUND = 256 * 1024


def _put(d: Path, g: dict) -> str:
    raw = json.dumps(g, sort_keys=True, indent=1).encode("utf-8")
    h = hashlib.sha256(raw).hexdigest()[:16]
    (d / f"{lineage.PREFIX}{h}.json").write_bytes(raw)
    return h


def _gen(parent, tag):
    return {"lineage": 1, "parent": parent, "game": "wal", "status": [], "evidence": [],
            "vindication_tail": [], "book": {}, "invented": {}, "dormant": [],
            "dormant_refused": [],
            "terms": [{"handle": f"{tag}_{i}", "atoms": ["a", "b"], "admitted": "candidate"}
                      for i in range(ROWS)]}


def _rebuild_peak(d: Path, n: int, bound: int | None) -> tuple[int, int, int]:
    d.mkdir()
    root = _put(d, _gen(None, "r"))
    h = root
    for k in range(n):
        h = _put(d, _gen(h, f"a{k}"))
    _put(d, _gen(root, "b"))
    lineage.merge(d)
    seen, saved = [], lineage_store.merge_save

    def spy(con, folder, *a, **kw):
        out = saved(con, folder, *a, **kw)
        seen.append(lineage_store.wal_bytes(folder))
        return out
    lineage_store.merge_save, lineage_store.WAL_BOUND_BYTES = spy, bound
    lineage_store._CONTINUE = False
    con = lineage_store.open_store(d)
    try:
        paths = {x.get("dag") for x in lineage_store.catch_up(con, d)}
        fold = con.execute("SELECT v FROM blob WHERE k='fold'").fetchone()[0]
        rows = len(json.loads(fold)["rows"])
    finally:
        con.close()
        lineage_store.merge_save, lineage_store._CONTINUE = saved, True
    assert paths == {"rebuild"}, ("fixture: no rebuild ran", paths)
    _h, fa = lineage.head(d)
    assert rows == len(fa["terms"]), ("store != archive", rows, len(fa["terms"]))
    # one save's own WAL: its growth over the WAL before it (none after a checkpoint, which empties
    # it); from the second save on, since the first also holds the rebuild's emptying of the tables
    one = max(b - (a if a <= b else 0) for a, b in zip(seen, seen[1:], strict=False))
    return max(seen), rows, one


def main():
    kept = lineage_store.WAL_BOUND_BYTES
    tmp = Path(tempfile.mkdtemp(prefix="rebuild_wal_"))
    got = {}
    try:
        for bound in (None, BOUND):
            for n in (20, 40):
                got[(bound, n)] = _rebuild_peak(tmp / f"{bound}_{n}", n, bound)
    finally:
        lineage_store.WAL_BOUND_BYTES = kept
    (r20, _, _), (r40, rows, _) = got[(None, 20)], got[(None, 40)]
    (g20, _, o20), (g40, _, o40) = got[(BOUND, 20)], got[(BOUND, 40)]
    assert r40 > 1.6 * r20, ("RED: with no checkpoint the WAL's peak should grow with N", r20, r40)
    for g, one in ((g20, o20), (g40, o40)):
        assert g <= BOUND + one, ("GREEN: the peak passed the bound plus one save", g, BOUND, one)
    assert g40 < r40 / 3, ("GREEN: the bounded peak should be far below the unbounded", g40, r40)
    print(f"test_rebuild_wal: no bound, WAL peak {r20 // 1024} KB at N=20 -> {r40 // 1024} KB at "
          f"N=40 (grows with N); bound {BOUND // 1024} KB, peak {g20 // 1024} -> {g40 // 1024} KB, "
          f"each within the bound + one save ({o20 // 1024}, {o40 // 1024} KB); {rows} rows at "
          f"N=40, store = archive fold")


if __name__ == "__main__":
    main()
