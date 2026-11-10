"""(7) THE STORE CONTINUE's WAL (TETHER_CONTINUE_WAL; Build 1 ride-along, REPORT FIN5E §8: the WAL
reached 2.14 GB in a continue on 2026-11-03): every save rewrites the fold blob, and _continue had
no bound where _rebuild had one (r794 3). Hand-written saves: a linear store, then a branch, a merge
and N children of the merge arriving together (the continue path), the WAL read after each save:
  RED    TETHER_CONTINUE_WAL off: the WAL's peak grows with N (2N's well over N's);
  GREEN  ON, the bound set small: the peak never passes the bound plus the largest one save, and
         the store equals the archive fold.

    python tests/test_continue_wal.py
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

ROWS = 60
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


def _continue_peak(d: Path, n: int, on: bool) -> tuple[int, int, int]:
    d.mkdir()
    root = _put(d, _gen(None, "r"))
    a = _put(d, _gen(root, "a"))
    con = lineage_store.open_store(d)
    try:
        lineage_store.catch_up(con, d)             # the store's chain: root, a (linear)
    finally:
        con.close()
    _put(d, _gen(root, "b"))
    h = lineage.merge(d)["hash"]
    for k in range(n):
        h = _put(d, _gen(h, f"c{k}"))
    assert a
    seen, saved = [], lineage_store.merge_save

    def spy(con, folder, *x, **kw):
        out = saved(con, folder, *x, **kw)
        seen.append(lineage_store.wal_bytes(folder))
        return out
    lineage_store.merge_save, lineage_store.WAL_BOUND_BYTES = spy, BOUND
    lineage_store._CONTINUE_WAL = on
    con = lineage_store.open_store(d)
    try:
        paths = {x.get("dag") for x in lineage_store.catch_up(con, d)}
        fold = con.execute("SELECT v FROM blob WHERE k='fold'").fetchone()[0]
        rows = len(json.loads(fold)["rows"])
    finally:
        con.close()
        lineage_store.merge_save = saved
    assert paths == {"continue"}, ("fixture: the continue did not run", paths)
    _h, fa = lineage.head(d)
    assert rows == len(fa["terms"]), ("store != archive", rows, len(fa["terms"]))
    one = max(y - (x if x <= y else 0) for x, y in zip(seen, seen[1:], strict=False))
    return max(seen), rows, one


def main():
    kept = lineage_store.WAL_BOUND_BYTES, lineage_store._CONTINUE_WAL
    assert kept[1], "TETHER_CONTINUE_WAL is ON by default"
    tmp = Path(tempfile.mkdtemp(prefix="continue_wal_"))
    got = {}
    try:
        for on in (False, True):
            for n in (20, 40):
                got[(on, n)] = _continue_peak(tmp / f"{on}_{n}", n, on)
    finally:
        lineage_store.WAL_BOUND_BYTES, lineage_store._CONTINUE_WAL = kept
    (r20, _, _), (r40, rows, _) = got[(False, 20)], got[(False, 40)]
    (g20, _, o20), (g40, _, o40) = got[(True, 20)], got[(True, 40)]
    assert r40 > 1.6 * r20, ("RED: with no bound the continue's WAL peak should grow with N",
                             r20, r40)
    for g, one in ((g20, o20), (g40, o40)):
        assert g <= BOUND + one, ("GREEN: the peak passed the bound plus one save", g, BOUND, one)
    assert g40 < r40 / 3, ("GREEN: the bounded peak should be far below the unbounded", g40, r40)
    print(f"test_continue_wal: OFF, WAL peak {r20 // 1024} KB at N=20 -> {r40 // 1024} KB at N=40; "
          f"ON (bound {BOUND // 1024} KB) {g20 // 1024} -> {g40 // 1024} KB, each within the bound "
          f"+ one save ({o20 // 1024}, {o40 // 1024} KB); {rows} rows, store = archive fold")


if __name__ == "__main__":
    main()
