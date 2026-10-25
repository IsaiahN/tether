"""H's set-aside on Windows (h_chain f2, 2026-10-19; the reviewer 17:58 items 3-4), on BOTH store
forms (step (5a); the reviewer 2026-10-25 00:43 (iv)): every check below runs once with
lineage_store (memory.db) and once with store_fold (learned.db), _heal given the module, as
lineage passes it.

  T1      a tiny store cut so header_ok reads it "unreadable": _heal sets the store aside (renamed
          .dead-<UTC>), the folder reads "no store", open_store builds a fresh one, header ok
  MF1     MUST-FAIL (memory.db only: it is lineage_store's 0319ae0 header_ok body): the
          connection closed on success only leaves a handle open, and the set-aside rename raises
          PermissionError
  MF2     MUST-FAIL: an open handle planted on the store: _heal's rename retries on its schedule
          (6 attempts counted), puts back what it moved, returns NOT ok ("set-aside failed"), and
          no exception escapes; the folder holds the store under its own name, nothing .dead-
  T2      the ROLLBACK (the reviewer 18:16 item 2): a handle planted on the -wal, a LATER file:
          the store's rename succeeds, the -wal's fails after 6 attempts, the store is renamed
          BACK; the folder's names and shas exactly as before; refused
  MF3     MUST-FAIL: _heal with the rename-back loop removed leaves <store>.dead-* and no store
  T3      the f4 shape at small scale (the reviewer 18:44 item 3): committed WAL frames and a lost
          page not among them; the checkpoint pads the file (size ok), quick_check is not "ok"
          (raises or reports), the store is refused and set aside, and NO checkpoint_failed
  T3b     a quick_check that raises (planted): NO checkpoint_failed, set aside
  T4      a checkpoint that itself raises (planted): checkpoint_failed is written and the store
          is still refused (set aside)
  G1      learned.db only (the reviewer 2026-10-25 00:43, G1): a DkSnapshotDb held open on the
          folder at the set-aside: _heal RAISES RuntimeError and every file keeps its own name

    python tests/test_store_heal.py      (Windows only: an open handle blocks a rename only there)
"""
from __future__ import annotations

import os
import sqlite3
import sys
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
assert os.name == "nt", "these checks need Windows: a POSIX rename succeeds on an open file"
import lineage  # noqa: E402
import lineage_store  # noqa: E402
import store_fold  # noqa: E402


def fill(m, con, rows: list) -> None:
    """Rows into the store's meta, in the module's own schema (several pages' worth)."""
    if m is lineage_store:
        con.executemany("INSERT INTO meta VALUES (?, ?)", rows)
    else:
        con.executemany("INSERT INTO learned VALUES ('meta', ?, ?)",
                        [(store_fold.j([k]), store_fold.j({"v": v})) for k, v in rows])


def cut_store(m) -> Path:
    """A store with enough rows for several pages, closed, then cut to its first 2 pages."""
    d = Path(tempfile.mkdtemp(prefix="heal_"))
    con = m.open_store(d)
    fill(m, con, [(f"k{i}", "x" * 200) for i in range(400)])
    m.sleep(con)
    con.close()
    with open(d / m.DB, "r+b") as fh:
        ps = int.from_bytes(fh.read(18)[16:18], "big")
        fh.truncate(2 * ps)
    return d


def header_ok_old(folder):
    """0319ae0's header_ok (lineage_store's), verbatim in its body: con.close() on success only."""
    p = lineage_store.path(folder)
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


def checks(m) -> None:
    db, tag = m.DB, m.__name__
    d = cut_store(m)
    ok, why = m.header_ok(d)
    assert not ok and why.startswith("unreadable"), (tag, ok, why)
    ok, why, rep = lineage._heal(d, ok, why, m)
    sa = rep.get("set_aside")
    assert sa and sa["files"][0] == db and (ok, why) == (False, "no store"), (tag, ok, why, rep)
    assert (d / f"{db}{sa['suffix']}").exists() and not (d / db).exists()
    m.open_store(d).close()
    assert m.header_ok(d) == (True, "ok"), m.header_ok(d)
    print(f"[{tag}] T1 unreadable {db} set aside ({sa['files']}, attempts {sa['attempts']}); "
          "rebuilt; ok")

    if m is lineage_store:
        d1 = cut_store(m)
        got = header_ok_old(d1)
        assert got[0] is False and got[1].startswith("unreadable"), got
        try:
            (d1 / db).rename(d1 / f"{db}.dead-mf1")
        except PermissionError as e:
            print(f"[{tag}] MF1 the old body leaves a handle: the rename raises "
                  f"({type(e).__name__})")
        else:
            raise AssertionError("MF1: the old header_ok body did not block the rename")

    d2 = cut_store(m)
    ok, why = m.header_ok(d2)
    held = sqlite3.connect(f"file:{(d2 / db).as_posix()}?mode=ro", uri=True)   # the planted handle
    try:
        ok, why, rep = lineage._heal(d2, ok, why, m)
    finally:
        held.close()
    f = rep.get("set_aside_failed")
    assert f and not ok and why.startswith("set-aside failed"), (tag, ok, why, rep)
    assert f["attempts"][db] == 1 + len(lineage._RENAME_WAITS) == 6, f
    left = [x.name for x in d2.iterdir()]
    assert (d2 / db).exists() and not any(".dead-" in x for x in left), left
    print(f"[{tag}] MF2 a held file: refused after {f['attempts']} attempts, restored "
          f"{f['restored']}, {db} in place, nothing .dead-, no exception")
    for t, heal in (("T2", lineage._heal), ("MF3", heal_no_rollback())):
        d3 = cut_store(m)
        ok, why = m.header_ok(d3)       # leaves an empty -wal and a -shm: the later files
        before = {x.name: sha(x) for x in d3.iterdir()}
        assert f"{db}-wal" in before, (tag, before)
        with open(d3 / f"{db}-wal", "rb"):   # the planted holder of a LATER file
            ok, why, rep = heal(d3, ok, why, m)
        after = {x.name: sha(x) for x in d3.iterdir()}
        f = rep.get("set_aside_failed")
        assert f and not ok and f["file"] == f"{db}-wal", (tag, ok, why, rep)
        assert f["attempts"][f"{db}-wal"] == 6 and f["restored"] == [db], f
        if t == "T2":
            assert after == before, (before, after)
            print(f"[{tag}] T2 a later file held: {db} renamed BACK, restored {f['restored']}, "
                  "the folder's names and shas as before, refused, no exception")
        else:
            assert db not in after and any(x.startswith(f"{db}.dead-") for x in after), after
            print(f"[{tag}] MF3 the mutant without the rename-back leaves {db}.dead-* and no {db}")
    d4 = padded_case(m)
    ok, why = m.header_ok(d4)
    assert not ok and why.startswith("size "), (tag, ok, why)
    ok, why, rep = lineage._heal(d4, ok, why, m)
    qc = str(rep.get("quick_check"))
    assert rep.get("after_checkpoint") == "ok" and qc != "ok", (tag, rep)
    assert "checkpoint_failed" not in rep, rep
    assert rep.get("set_aside") and rep["set_aside"]["why"].startswith("quick_check"), rep
    print(f"[{tag}] T3 the f4 shape: the checkpoint pads the file (size ok), quick_check "
          f"{qc[:60]!r}, refused and set aside, NO checkpoint_failed")
    d6 = padded_case(m)
    ok, why = m.header_ok(d6)
    with planted(m, "open_store", lambda real: lambda *a, **k: QCRaises(real(*a, **k))):
        ok, why, rep = lineage._heal(d6, ok, why, m)
    assert "checkpoint_failed" not in rep, f"T3b: a raising quick_check read as a checkpoint {rep}"
    assert str(rep.get("quick_check")).startswith("error:") and rep.get("set_aside"), rep
    assert "quick_check error" in rep["set_aside"]["why"], rep
    print(f"[{tag}] T3b a quick_check that raises: quick_check {rep['quick_check']!r}, refused, "
          "NO checkpoint_failed")
    d5 = padded_case(m)
    ok, why = m.header_ok(d5)
    with planted(m, "checkpoint", lambda _real: boom):
        ok, why, rep = lineage._heal(d5, ok, why, m)
    assert "planted" in rep.get("checkpoint_failed", "") and rep.get("set_aside"), rep
    assert (ok, why) == (False, "no store"), (ok, why)
    print(f"[{tag}] T4 a checkpoint that raises: checkpoint_failed {rep['checkpoint_failed']!r}, "
          "refused and set aside")


def g1() -> None:
    """learned.db only: a held DkSnapshotDb at the set-aside RAISES, and no file is renamed."""
    d = Path(tempfile.mkdtemp(prefix="heal_g1_"))
    con = store_fold.open_store(d)
    fill(store_fold, con, [(f"k{i}", "x" * 200) for i in range(400)])
    store_fold.sleep(con)
    con.close()
    snap = lineage.DkSnapshotDb(d)      # the planted reader: open, its read transaction held
    before = sorted(x.name for x in d.iterdir())
    try:
        lineage._heal(d, False, "planted: a store refused at open", store_fold)
        got = None
    except RuntimeError as e:
        got = str(e)
    finally:
        snap.close()
    after = sorted(x.name for x in d.iterdir())
    assert got and "still open at the set-aside" in got, ("G1: the guard did not fire", got)
    assert after == before and store_fold.DB in after, (before, after)
    print(f"[store_fold] G1 a DkSnapshotDb held at the set-aside: RuntimeError {got!r}; every "
          f"file under its own name {after}")


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


def padded_case(m) -> Path:
    """The f4 shape at small scale: a store checkpointed, then more rows committed into its WAL
    only (open_store turns auto-checkpoint off), the files copied while the connection is still
    open, as a crash would leave them; then the file is cut so its largest b-tree page NOT among
    the WAL's frames is lost, with every later file page in the frames -- the checkpoint pads the
    file and the lost page reads as zeros."""
    import shutil
    import struct
    src, d = Path(tempfile.mkdtemp(prefix="pad_src_")), Path(tempfile.mkdtemp(prefix="pad_"))
    con = m.open_store(src)
    fill(m, con, [(f"a{i:05d}", "x" * 300) for i in range(600)])
    m.checkpoint(con)
    fill(m, con, [(f"b{i:05d}", "y" * 300) for i in range(300)])
    for n in (m.DB, f"{m.DB}-wal"):
        shutil.copyfile(src / n, d / n)
    con.close()
    w = (d / f"{m.DB}-wal").read_bytes()
    ps = struct.unpack(">I", w[8:12])[0]
    frames, off = set(), 32
    while off + 24 + ps <= len(w):
        frames.add(struct.unpack(">I", w[off:off + 4])[0])
        off += 24 + ps
    raw = (d / m.DB).read_bytes()
    n_file = len(raw) // ps
    p = next(q for q in range(n_file, 1, -1)
             if q not in frames and raw[(q - 1) * ps] in (2, 5, 10, 13))
    assert all(q in frames for q in range(p + 1, n_file + 1)), (p, n_file)
    with open(d / m.DB, "r+b") as fh:
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


def main() -> int:
    for m in (lineage_store, store_fold):
        checks(m)
    g1()
    print("store_heal: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
