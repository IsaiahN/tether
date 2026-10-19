"""H's set-aside on Windows (h_chain f2, 2026-10-19; the reviewer 17:58 items 3-4).

  T1      a tiny store cut so header_ok reads it "unreadable": _heal sets memory.db aside (renamed
          .dead-<UTC>), the folder reads "no store", open_store builds a fresh one, header ok
  MF1     MUST-FAIL: header_ok's OLD body (0319ae0: the connection closed on success only) on the
          same cut store leaves a handle open, and the set-aside rename raises PermissionError
  MF2     MUST-FAIL: an open handle planted on memory.db: _heal's rename retries on its schedule
          (6 attempts counted), puts back what it moved, returns NOT ok ("set-aside failed"), and
          no exception escapes; the folder holds memory.db under its own name, nothing .dead-

    python test_store_heal.py      (Windows only: an open handle blocks a rename only there)
"""
from __future__ import annotations

import os
import sqlite3
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
assert os.name == "nt", "these checks need Windows: a POSIX rename succeeds on an open file"
import lineage  # noqa: E402
import lineage_store as ls  # noqa: E402


def cut_store() -> Path:
    """A store with enough rows for several pages, closed, then cut to its first 2 pages."""
    d = Path(tempfile.mkdtemp(prefix="heal_"))
    con = ls.open_store(d)
    con.executemany("INSERT INTO meta VALUES (?, ?)", [(f"k{i}", "x" * 200) for i in range(400)])
    ls.sleep(con)
    con.close()
    with open(d / ls.DB, "r+b") as fh:
        ps = int.from_bytes(fh.read(18)[16:18], "big")
        fh.truncate(2 * ps)
    return d


def header_ok_old(folder):
    """0319ae0's header_ok, verbatim in its body: con.close() on the success path only."""
    p = ls.path(folder)
    if not p.exists():
        return False, "no store"
    try:
        con = sqlite3.connect(f"file:{p.as_posix()}?mode=ro", uri=True)
        pc = con.execute("PRAGMA page_count").fetchone()[0]
        ps = con.execute("PRAGMA page_size").fetchone()[0]
        schema = con.execute("SELECT v FROM meta WHERE k='schema'").fetchone()
        last = con.execute("SELECT v FROM meta WHERE k='last_merged'").fetchone()
        con.close()
    except sqlite3.DatabaseError as e:
        return False, f"unreadable: {e}"
    return pc, ps, schema, last


def main() -> int:
    d = cut_store()
    ok, why = ls.header_ok(d)
    assert not ok and why.startswith("unreadable"), (ok, why)
    ok, why, rep = lineage._heal(d, ok, why)
    sa = rep.get("set_aside")
    assert sa and sa["files"][0] == ls.DB and (ok, why) == (False, "no store"), (ok, why, rep)
    assert (d / f"{ls.DB}{sa['suffix']}").exists() and not (d / ls.DB).exists()
    ls.open_store(d).close()
    assert ls.header_ok(d) == (True, "ok"), ls.header_ok(d)
    print(f"T1 unreadable store set aside ({sa['files']}, attempts {sa['attempts']}); rebuilt; ok")

    d1 = cut_store()
    got = header_ok_old(d1)
    assert got[0] is False and got[1].startswith("unreadable"), got
    try:
        (d1 / ls.DB).rename(d1 / f"{ls.DB}.dead-mf1")
    except PermissionError as e:
        print(f"MF1 the old body leaves a handle: the rename raises ({type(e).__name__})")
    else:
        raise AssertionError("MF1: the old header_ok body did not block the rename")

    d2 = cut_store()
    ok, why = ls.header_ok(d2)
    # the planted handle
    held = sqlite3.connect(f"file:{(d2 / ls.DB).as_posix()}?mode=ro", uri=True)
    try:
        ok, why, rep = lineage._heal(d2, ok, why)
    finally:
        held.close()
    f = rep.get("set_aside_failed")
    assert f and not ok and why.startswith("set-aside failed"), (ok, why, rep)
    assert f["attempts"][ls.DB] == 1 + len(lineage._RENAME_WAITS) == 6, f
    left = [x.name for x in d2.iterdir()]
    assert (d2 / ls.DB).exists() and not any(".dead-" in x for x in left), left
    print(f"MF2 a held file: refused after {f['attempts']} attempts, restored {f['restored']}, "
          "memory.db in place, nothing .dead-, no exception")
    print("store_heal: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
