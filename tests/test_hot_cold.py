"""S4, HOT/COLD (the reviewer 2026-11-02 r811, r816): lineage.DkSnapshot over a store holding one
kind's three kind_dk rows -- n 5 and n 2 (hot), n 1 (cold, a past life's single sighting).
  MF-HC1  the kind's enumeration returns the hot rows only (2 of 3); with the arm OFF, all 3.
  MF-HC2  a cold row's keyed read (DkSnapshot.cold) returns its stored n (1); a hot row's, 0.
  MF-HC3  the per-type totals count the hot rows (7), the full totals every row (8); nothing is
          deleted (the table still holds 3 rows).

    python tests/test_hot_cold.py
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import lineage  # noqa: E402
import lineage_store  # noqa: E402

D = ("drow", "+", 1)
T = ("o", "x")


def fixture() -> Path:
    d = Path(tempfile.mkdtemp(prefix="hot_cold_"))
    con = lineage_store.open_store(d)
    try:
        syms = {1: json.dumps(list(D)), 2: json.dumps(list(T)), 3: "a", 4: "b", 5: "c"}
        con.executemany("INSERT INTO sym VALUES (?, ?)", list(syms.items()))
        con.executemany("INSERT INTO kind_dk VALUES (?,?,?,?,NULL,NULL,NULL,-1)",
                        [(1, 3, 2, 5), (1, 4, 2, 2), (1, 5, 2, 1)])
        con.commit()
    finally:
        con.close()
    return d


def main():
    assert lineage._HOT_COLD, "the arm is ON by default"
    d = fixture()
    snap = lineage.DkSnapshot(d)
    hot = snap.rows(D)
    assert sorted(k for _d, k, _t in hot) == ["a", "b"], ("MF-HC1 hot only", hot)
    assert snap.cold((D, "c", T)) == 1 and snap.cold((D, "a", T)) == 0, "MF-HC2"
    assert snap.tot_t["drow"]["a"] + snap.tot_t["drow"]["b"] == 7 and "c" not in snap.tot_t["drow"]
    assert sum(snap.tot_t_all["drow"].values()) == 8, ("MF-HC3", snap.tot_t_all)
    assert len(snap.rows(D, hot=False)) == 3, "nothing deleted"
    snap.close() if hasattr(snap, "close") else None
    lineage._HOT_COLD = False
    try:
        off = lineage.DkSnapshot(d)
        assert len(off.rows(D)) == 3 and off.cold((D, "c", T)) == 0, "MUST-FAIL: OFF reads all"
    finally:
        lineage._HOT_COLD = True
    print("test_hot_cold: a kind's 3 rows (n 5, 2, 1) -> 2 hot enumerated, the n == 1 row read by "
          "key (1); per-type total 7 hot / 8 all; the table keeps all 3; OFF enumerates all 3")


if __name__ == "__main__":
    main()
