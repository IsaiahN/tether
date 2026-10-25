"""THE ONE DOOR to the agent's knowledge (Isaiah 2026-10-24 08:30: "one service that fetches and
stores data based on the conditional efficiently"; the reviewer 08:49, 08:56, 08:58). Every read of
a library file and every load or save of the learned store goes through here.

STEP 1, A THIN FACADE: today's code does the work, unchanged, behind each function -- lineage.py,
lineage_store.py and gamma's save / load are the learned backends, folded in here at steps 4-5, when
the json|db conditional joins. Same arguments, same results; conform/door.py (M7) checks that no
other module opens a knowledge file.

At the repo root, not in library/: the library-ABSENT ablation (TETHER_LIBRARY_REQUIRED=0) still
loads and saves a learned store, and a door inside library/ would vanish with it."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

LIBRARY = Path(__file__).parent / "library"


def _lineage():
    """lineage, imported at first use: `import store` costs nothing, so the library readers
    (inherited, compile_term) import it without pulling in the learned backend."""
    import lineage
    return lineage


# ---------------------------------------------------------------- the library's files
def library_files(names) -> dict:
    """The GIVEN library's old file shapes, by old name (store step 3): served from given.json /
    frame.json / index.json by library_runtime.old_files, fresh per call. {} when library/ is
    absent (the ablation: library_runtime itself lives there)."""
    if not LIBRARY.is_dir():
        return {}
    import sys
    if str(LIBRARY) not in sys.path:
        sys.path.insert(0, str(LIBRARY))
    import library_runtime
    return library_runtime.old_files(LIBRARY, names)


def read_json(path: str | Path) -> Any:
    """A knowledge file's parsed JSON, or None when it is absent (the library ablation)."""
    p = Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def read_text(path: str | Path) -> str:
    """A knowledge file's text; raises as Path.read_text does."""
    return Path(path).read_text(encoding="utf-8")


def read_bytes(path: str | Path) -> bytes:
    """A knowledge file's bytes; raises as Path.read_bytes does."""
    return Path(path).read_bytes()


def write_text(path: str | Path, text: str) -> None:
    """A knowledge file written whole (feeder's atoms-only control library)."""
    Path(path).write_text(text, encoding="utf-8")


def copy(src: str | Path, dst: str | Path) -> None:
    """A library= save copied (feeder's probe works on a copy, never the training path)."""
    import shutil
    shutil.copyfile(src, dst)


def remove(path: str | Path) -> None:
    """A copy made by copy() removed (absent is fine)."""
    Path(path).unlink(missing_ok=True)


# ---------------------------------------------------------------- the learned store
def lineage_load(d: str | Path, ag: Any) -> dict:
    return _lineage().load(d, ag)


def lineage_write(d: str | Path, ag: Any, game: str, sleep: bool = True) -> dict:
    return _lineage().write(d, ag, game, sleep=sleep)


def lineage_boundary(d: str | Path | None, ag: Any, game: str, how: str) -> dict | None:
    return _lineage().boundary(d, ag, game, how)


def library_load(g: Any, path: str, **kw: Any) -> dict:
    """A library= save into Gamma g (gamma.Gamma.load)."""
    return g.load(path, **kw)


def library_save(g: Any, path: str, header: dict | None = None) -> dict:
    """Gamma g written to a library= save (gamma.Gamma.save)."""
    return g.save(path, header=header)


def replace(src: str | Path, dst: str | Path) -> None:
    """A checked save's temporary file moved over the save (os.replace)."""
    os.replace(src, dst)


# ---------------------------------------------------------------- reads during play
def resolve(ag: Any, lib: Any, key: str, role: str, sig: tuple) -> list | None:
    return _lineage().resolve(ag, lib, key, role, sig)


def resolve_memo(ag: Any, lib: Any, mkey: tuple, atoms: dict) -> tuple | None:
    return _lineage().resolve_memo(ag, lib, mkey, atoms)


def resolve_bs(ag: Any, lib: Any, skey: tuple, atoms: dict) -> tuple | None:
    return _lineage().resolve_bs(ag, lib, skey, atoms)


def recorded_whole(mkey: tuple) -> bool:
    return _lineage().recorded_whole(mkey)


# ---------------------------------------------------------------- the learned store (step 4)
# Rows are (section, key, body), key and body JSON text (C4; the reviewer 2026-10-24 08:49, 16:19).
# Two forms, one schema: json (learned.jsonl.gz + perception.jsonl.gz, gzip mtime 0, level 6) and
# db (learned.db). Each section carries its row count and the sha256 of its rows in key order,
# checked at load. Step 4 builds and checks it; nothing in play reads it until step 5.
PERCEPTION = frozenset({"kind", "kind_dk", "kind_off", "pair"})
PARTS = ("learned", "perception")
JSON_FILES = {"learned": "learned.jsonl.gz", "perception": "perception.jsonl.gz"}
DB_FILE = "learned.db"


class StoreError(Exception):
    """A learned store that is missing, empty or fails a digest: named, never read as empty."""


# THE DB'S SEARCHES (the census Q-s; the reviewer 2026-10-24 16:57): each expression is written
# once, here, and both its index and its query are built from it, so the two cannot drift.
DK = "json_extract(key, '$[0]')"
LANDED = "json_extract(body, '$.in_landed') = 1"
KIND_FILTERS = {"nocount": f"json_extract(body, '$.has_n') = 0 AND {LANDED}",
                "t2": f"json_extract(body, '$.no_dk') = 1 AND {LANDED}"}
INDEXES = {
    "perception_dk": (f"CREATE INDEX perception_dk ON perception({DK}, key) "
                      "WHERE section = 'kind_dk'"),
    **{f"kind_{f}": (f"CREATE INDEX kind_{f} ON perception(key, body) "   # covering
                     f"WHERE section = 'kind' AND {w}") for f, w in KIND_FILTERS.items()}}
# INDEXED BY (the reviewer 17:48): a forced index fails loudly ("no such index") where a planner's
# choice would slow silently when the statistics change (empty partial indexes read as unknown).
SEARCHES = {        # name -> (query, the index that must answer it)
    "S-1": ("SELECT key, body FROM perception INDEXED BY perception_dk WHERE section = 'kind_dk' "
            f"AND {DK} = ? AND json_extract(body, '$.n') != 0 ORDER BY key", "perception_dk"),
    "S-2": ("SELECT body FROM learned WHERE section = 'held' AND key = ?", "PRIMARY KEY"),
    **{f"C-{f}": (f"SELECT key, body FROM perception INDEXED BY kind_{f} WHERE section = 'kind' "
                  f"AND {w} ORDER BY key", f"kind_{f}") for f, w in KIND_FILTERS.items()}}


def db_search(d: str | Path, name: str, *args: Any) -> list:
    """One of the census's searches on the db form: [(key, body)] or [(body,)], as SQLite gives."""
    import sqlite3
    p = Path(d) / DB_FILE
    if not p.exists():
        raise StoreError(f"{p} is absent")
    con = sqlite3.connect(f"file:{p.as_posix()}?mode=ro", uri=True)
    try:
        return con.execute(SEARCHES[name][0], args).fetchall()
    finally:
        con.close()


def part_of(section: str) -> str:
    return "perception" if section in PERCEPTION else "learned"


def section_digest(rows: dict) -> list:
    import hashlib
    h = hashlib.sha256()
    for k in sorted(rows):
        h.update(f"{k}\t{rows[k]}\n".encode())
    return [len(rows), h.hexdigest()]


def _checked(where: str, man: dict, store: dict, verify: bool) -> dict:
    if not man or not any(n for n, _ in man.values()):
        raise StoreError(f"{where}: the learned store is empty")
    if set(man) != set(store):
        raise StoreError(f"{where}: sections {sorted(set(man) ^ set(store))} are in only one of "
                         "the manifest and the rows")
    for s, want in man.items():
        got = section_digest(store[s]) if verify else [len(store[s]), want[1]]
        if got != list(want):
            raise StoreError(f"{where}: section {s} fails its digest ({got[0]} rows read, "
                             f"{want[0]} written)")
    return store


def _json_write(d: Path, man: dict, store: dict, suffix: str) -> None:
    import gzip
    for part in PARTS:
        secs = [s for s in sorted(man) if part_of(s) == part]
        with open(d / (JSON_FILES[part] + suffix), "wb") as fh:
            with gzip.GzipFile(filename="", mode="wb", fileobj=fh, compresslevel=6, mtime=0) as z:
                z.write((json.dumps({"manifest": {s: man[s] for s in secs}}) + "\n").encode())
                for s in secs:
                    for k in sorted(store[s]):
                        z.write((json.dumps([s, k, store[s][k]], ensure_ascii=False)
                                 + "\n").encode())
            fh.flush()
            os.fsync(fh.fileno())


def _json_read(d: Path, verify: bool, suffix: str = "") -> dict:
    import gzip
    man: dict = {}
    store: dict = {}
    for part in PARTS:
        p = d / (JSON_FILES[part] + suffix)
        if not p.exists():
            raise StoreError(f"{p} is absent")
        with gzip.open(p, "rb") as z:
            head = z.readline()
            if not head:
                raise StoreError(f"{p} is empty")
            m = json.loads(head)["manifest"]
            man.update(m)
            for s in m:     # a section with 0 rows has no row line
                store.setdefault(s, {})
            for line in z:
                s, k, b = json.loads(line)
                store.setdefault(s, {})[k] = b
    return _checked(str(d), man, store, verify)


def _db_write(p: Path, man: dict, store: dict) -> None:
    import sqlite3
    con = sqlite3.connect(p)
    try:
        for t in (*PARTS, "manifest"):
            con.execute(f"DROP TABLE IF EXISTS {t}")
        for part in PARTS:
            con.execute(f"CREATE TABLE {part}(section TEXT, key TEXT, body TEXT, "
                        "PRIMARY KEY(section, key)) WITHOUT ROWID")
        con.execute("CREATE TABLE manifest(section TEXT PRIMARY KEY, n INTEGER, sha TEXT)")
        for s in sorted(man):
            con.executemany(f"INSERT INTO {part_of(s)} VALUES (?, ?, ?)",
                            ((s, k, store[s][k]) for k in sorted(store[s])))
        con.executemany("INSERT INTO manifest VALUES (?, ?, ?)",
                        ((s, n, h) for s, (n, h) in sorted(man.items())))
        for sql in INDEXES.values():
            con.execute(sql)
        con.execute("ANALYZE")     # the planner's statistics: without them it prefers the PK
        con.commit()
    finally:
        con.close()
    with open(p, "rb+") as fh:
        os.fsync(fh.fileno())


def _db_read(p: Path, verify: bool) -> dict:
    import sqlite3
    if not p.exists():
        raise StoreError(f"{p} is absent")
    con = sqlite3.connect(f"file:{p.as_posix()}?mode=ro", uri=True)
    try:
        names = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if not {*PARTS, "manifest"} <= names:
            raise StoreError(f"{p}: tables {sorted({*PARTS, 'manifest'} - names)} are absent")
        man = {s: [n, h] for s, n, h in con.execute("SELECT section, n, sha FROM manifest")}
        store: dict = {s: {} for s in man}
        for part in PARTS:
            for s, k, b in con.execute(f"SELECT section, key, body FROM {part} "
                                       "ORDER BY section, key"):
                store.setdefault(s, {})[k] = b
    finally:
        con.close()
    return _checked(str(p), man, store, verify)


def learned_save(fmt: str, d: str | Path, store: dict) -> dict:
    """Every section of `store` ({section: {key: body}}) written whole and atomically: temporary
    files, fsync, read back and verified, then renamed over the old. Returns the manifest."""
    d = Path(d)
    d.mkdir(parents=True, exist_ok=True)
    man = {s: section_digest(r) for s, r in sorted(store.items())}
    if fmt == "json":
        _json_write(d, man, store, ".tmp")
        _json_read(d, True, ".tmp")
        for part in PARTS:
            os.replace(d / (JSON_FILES[part] + ".tmp"), d / JSON_FILES[part])
    elif fmt == "db":
        tmp = d / (DB_FILE + ".tmp")
        _db_write(tmp, man, store)
        _db_read(tmp, True)
        os.replace(tmp, d / DB_FILE)
    else:
        raise StoreError(f"unknown store format {fmt!r} (json | db)")
    return man


def learned_load(fmt: str, d: str | Path, verify: bool = True) -> dict:
    """The whole learned store, {section: {key: body}}, each section checked against its digest
    (verify=False skips the recomputation: B6's timing only). Missing or empty: StoreError."""
    if fmt == "json":
        return _json_read(Path(d), verify)
    if fmt == "db":
        return _db_read(Path(d) / DB_FILE, verify)
    raise StoreError(f"unknown store format {fmt!r} (json | db)")
