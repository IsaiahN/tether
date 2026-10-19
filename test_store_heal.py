"""H's set-aside on Windows (h_chain f2, 2026-10-19; the reviewer 17:58 items 3-4).

  T1      a tiny store cut so header_ok reads it "unreadable": _heal sets memory.db aside (renamed
          .dead-<UTC>), the folder reads "no store", open_store builds a fresh one, header ok
  MF1     MUST-FAIL: header_ok's OLD body (0319ae0: the connection closed on success only) on the
          same cut store leaves a handle open, and the set-aside rename raises PermissionError
  MF2     MUST-FAIL: an open handle planted on memory.db: _heal's rename retries on its schedule
          (6 attempts counted), puts back what it moved, returns NOT ok ("set-aside failed"), and
          no exception escapes; the folder holds memory.db under its own name, nothing .dead-
  T2      the ROLLBACK (the reviewer 18:16 item 2): a handle planted on the -wal, a LATER file:
          memory.db's rename succeeds, the -wal's fails after 6 attempts, memory.db is renamed
          BACK (restored [memory.db]); the folder's names and shas exactly as before; refused
  MF3     MUST-FAIL: _heal with the rename-back loop removed leaves memory.db.dead-* and no
          memory.db on the same plant
  T3      the f4 shape at small scale (the reviewer 18:44 item 3): committed WAL frames and a lost
          page not among them; the checkpoint pads the file (size ok), quick_check is not "ok"
          (raises or reports), the store is refused and set aside, and NO checkpoint_failed is
          written (8defe20's single try wrote it whenever quick_check raised)
  T4      a checkpoint that itself raises (planted): checkpoint_failed is written and the store
          is still refused (set aside)

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
    files = {}
    for tag, heal in (("T2", lineage._heal), ("MF3", heal_no_rollback())):
        d3 = cut_store()
        ok, why = ls.header_ok(d3)       # leaves an empty -wal and a -shm: the later files
        files[tag] = before = {x.name: sha(x) for x in d3.iterdir()}
        assert f"{ls.DB}-wal" in before, before
        with open(d3 / f"{ls.DB}-wal", "rb"):   # the planted holder of a LATER file
            ok, why, rep = heal(d3, ok, why)
        after = {x.name: sha(x) for x in d3.iterdir()}
        f = rep.get("set_aside_failed")
        assert f and not ok and f["file"] == f"{ls.DB}-wal", (ok, why, rep)
        assert f["attempts"][f"{ls.DB}-wal"] == 6 and f["restored"] == [ls.DB], f
        if tag == "T2":
            assert after == before, (before, after)
            print(f"T2 a later file held: memory.db renamed BACK, restored {f['restored']}, "
                  "the folder's names and shas as before, refused, no exception")
        else:
            assert ls.DB not in after and any(x.startswith(f"{ls.DB}.dead-") for x in after), after
            print("MF3 the mutant without the rename-back leaves memory.db.dead-* and no memory.db")
    d4 = padded_case()
    ok, why = ls.header_ok(d4)
    assert not ok and why.startswith("size "), (ok, why)
    ok, why, rep = lineage._heal(d4, ok, why)
    qc = str(rep.get("quick_check"))
    assert rep.get("after_checkpoint") == "ok" and qc != "ok", rep
    assert "checkpoint_failed" not in rep, rep
    assert rep.get("set_aside") and rep["set_aside"]["why"].startswith("quick_check"), rep
    print(f"T3 the f4 shape: the checkpoint pads the file (size ok), quick_check {qc[:60]!r}, "
          "refused and set aside, NO checkpoint_failed")

    # T3b: the real f4 store's quick_check RAISED; a small store reports instead, so the raise is
    # planted (a connection whose quick_check raises). 8defe20's single try labels it a failed
    # checkpoint: this is the check that fails there
    d6 = padded_case()
    ok, why = ls.header_ok(d6)
    with planted(ls, "open_store", lambda real: lambda *a, **k: QCRaises(real(*a, **k))):
        ok, why, rep = lineage._heal(d6, ok, why)
    assert "checkpoint_failed" not in rep, f"T3b: a raising quick_check read as a checkpoint {rep}"
    assert str(rep.get("quick_check")).startswith("error:") and rep.get("set_aside"), rep
    assert "quick_check error" in rep["set_aside"]["why"], rep
    print(f"T3b a quick_check that raises: quick_check {rep['quick_check']!r}, why "
          f"{rep['set_aside']['why']!r}, refused, NO checkpoint_failed")

    d5 = padded_case()
    ok, why = ls.header_ok(d5)
    with planted(ls, "checkpoint", lambda _real: boom):
        ok, why, rep = lineage._heal(d5, ok, why)
    assert "planted" in rep.get("checkpoint_failed", "") and rep.get("set_aside"), rep
    assert (ok, why) == (False, "no store"), (ok, why)
    print(f"T4 a checkpoint that raises: checkpoint_failed {rep['checkpoint_failed']!r}, refused "
          "and set aside")
    print("store_heal: OK")
    return 0


def boom(_con):
    raise sqlite3.OperationalError("planted: the checkpoint fails")


class QCRaises:
    """A store connection whose PRAGMA quick_check raises, as the real f4 store's did."""
    def __init__(self, con):
        self.con = con

    def execute(self, sql, *a):
        if "quick_check" in sql:
            raise sqlite3.DatabaseError("planted: database disk image is malformed")
        return self.con.execute(sql, *a)

    def close(self):
        self.con.close()


class planted:
    """Replaces mod.name with make(original) inside the block, and restores it after."""
    def __init__(self, mod, name, make):
        self.mod, self.name, self.make = mod, name, make

    def __enter__(self):
        self.real = getattr(self.mod, self.name)
        setattr(self.mod, self.name, self.make(self.real))

    def __exit__(self, *exc):
        setattr(self.mod, self.name, self.real)


def padded_case() -> Path:
    """The f4 shape at small scale: a store checkpointed, then more rows committed into its WAL
    only (open_store turns auto-checkpoint off), the files copied while the connection is still
    open, as a crash would leave them; then the file is cut so its largest b-tree page NOT among
    the WAL's frames is lost, with every later file page in the frames -- the checkpoint pads the
    file and the lost page reads as zeros."""
    import shutil
    import struct
    src, d = Path(tempfile.mkdtemp(prefix="pad_src_")), Path(tempfile.mkdtemp(prefix="pad_"))
    con = ls.open_store(src)
    ins = "INSERT INTO meta VALUES (?, ?)"
    con.executemany(ins, [(f"a{i:05d}", "x" * 300) for i in range(600)])
    ls.checkpoint(con)
    con.executemany(ins, [(f"b{i:05d}", "y" * 300) for i in range(300)])
    for n in (ls.DB, f"{ls.DB}-wal"):
        shutil.copyfile(src / n, d / n)
    con.close()
    w = (d / f"{ls.DB}-wal").read_bytes()
    ps = struct.unpack(">I", w[8:12])[0]
    frames, off = set(), 32
    while off + 24 + ps <= len(w):
        frames.add(struct.unpack(">I", w[off:off + 4])[0])
        off += 24 + ps
    raw = (d / ls.DB).read_bytes()
    n_file = len(raw) // ps
    p = next(q for q in range(n_file, 1, -1)
             if q not in frames and raw[(q - 1) * ps] in (2, 5, 10, 13))
    assert all(q in frames for q in range(p + 1, n_file + 1)), (p, n_file)
    with open(d / ls.DB, "r+b") as fh:
        fh.truncate((p - 1) * ps)
    return d


def sha(f: Path) -> str:
    import hashlib
    return hashlib.sha256(f.read_bytes()).hexdigest()[:16]


def heal_no_rollback():
    """MF3's mutant: _heal's source with the rename-back loop removed (asserted once), compiled in
    lineage's globals."""
    import inspect
    src = inspect.getsource(lineage._heal)
    cut = ("            for m in moved:\n"
           "                (p / f\"{m}.dead-{stamp}\").rename(p / m)\n")
    assert src.count(cut) == 1, "the rename-back loop is not in _heal as expected"
    ns: dict = {}
    exec(compile(src.replace(cut, ""), "_heal(no rollback)", "exec"), dict(vars(lineage)), ns)  # noqa: S102
    return ns["_heal"]


if __name__ == "__main__":
    sys.exit(main())
