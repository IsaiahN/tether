"""THE CONSOLIDATED MEMORY (the reviewer 2026-10-19 06:13, 07:12, 07:19, 07:26, 07:31, 07:35;
Isaiah 06:12, 07:05, 07:19): one indexed store per memory folder (memory.db), DERIVED from the
memory saves (the archive, never edited) and rebuildable from them. Each save is merged in ONE
transaction after its archive files are written; the commit never checkpoints
(wal_autocheckpoint 0); the "sleep" (the checkpoint and a quick_check) runs off the play path.
Every repeated string is interned into sym, and the tables are keyed by integer tuples.

It holds what lineage.load builds from the chain: the fold's result, the carried counts summed
root to tip, the kind store (one row per key), the delta-kind store, the held index (the tip's
entry per key, with its file's signature), the asked record CONDENSED (n_variants per entry, role
and slot class) and its WHOLE pairs. A chain that is not linear, or anything the store cannot
answer exactly, is refused with a reason, and the caller loads from the archive as before."""
import hashlib
import json
import os
import sqlite3
import time
from pathlib import Path
from typing import Any

DB = "memory.db"
SCHEMA = 1
SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY, v TEXT);
CREATE TABLE IF NOT EXISTS sym(id INTEGER PRIMARY KEY, s TEXT UNIQUE);
CREATE TABLE IF NOT EXISTS saves(h TEXT PRIMARY KEY, k INTEGER, parent TEXT);
CREATE TABLE IF NOT EXISTS blob(k TEXT PRIMARY KEY, v TEXT);
CREATE TABLE IF NOT EXISTS asked_tally(entry INTEGER, role INTEGER, slot_class INTEGER,
    n_variants INTEGER, n_asked INTEGER, n_landed INTEGER, first_save INTEGER,
    last_save INTEGER, PRIMARY KEY(entry, role, slot_class)) WITHOUT ROWID;
CREATE TABLE IF NOT EXISTS ak_whole(entry TEXT, role TEXT, o TEXT, x TEXT,
    PRIMARY KEY(entry, role, o, x)) WITHOUT ROWID;
CREATE TABLE IF NOT EXISTS kind(entry INTEGER, role INTEGER, kind_o INTEGER, kind_x INTEGER,
    in_landed INTEGER, n INTEGER, has_n INTEGER, l_game TEXT, l_level INTEGER,
    l_cycle INTEGER, l_seq INTEGER, PRIMARY KEY(entry, role, kind_o, kind_x)) WITHOUT ROWID;
CREATE TABLE IF NOT EXISTS pair(kind_o INTEGER, kind_x INTEGER, n INTEGER, last_seq INTEGER,
    PRIMARY KEY(kind_o, kind_x)) WITHOUT ROWID;
CREATE TABLE IF NOT EXISTS kind_dk(dk INTEGER, entry INTEGER, tgt INTEGER, n INTEGER,
    l_game TEXT, l_level INTEGER, l_cycle INTEGER, l_seq INTEGER,
    PRIMARY KEY(dk, entry, tgt)) WITHOUT ROWID;
CREATE TABLE IF NOT EXISTS kind_off(dk INTEGER, entry INTEGER, ko INTEGER, n INTEGER,
    PRIMARY KEY(dk, entry, ko)) WITHOUT ROWID;
CREATE TABLE IF NOT EXISTS sig(id INTEGER PRIMARY KEY, arm TEXT, atoms TEXT, names TEXT,
    UNIQUE(arm, atoms, names));
CREATE TABLE IF NOT EXISTS held(key INTEGER, role INTEGER, gen TEXT, sig INTEGER, items TEXT,
    PRIMARY KEY(key, role)) WITHOUT ROWID;
"""
UPSERT_LAST = ("ON CONFLICT DO UPDATE SET l_game=excluded.l_game, l_level=excluded.l_level, "
               "l_cycle=excluded.l_cycle, l_seq=excluded.l_seq WHERE excluded.l_seq >= {t}.l_seq")


class Refused(Exception):
    """The store cannot answer this exactly; the caller loads from the archive."""


def path(folder: str | Path) -> Path:
    return Path(folder) / DB


def open_store(folder: str | Path, cache_kib: int = 262144,
               mmap_bytes: int = 1 << 30) -> sqlite3.Connection:
    con = sqlite3.connect(path(folder), isolation_level=None)
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA synchronous=NORMAL")
    con.execute("PRAGMA wal_autocheckpoint=0")    # never a checkpoint inside a merge's commit
    con.execute(f"PRAGMA cache_size=-{int(cache_kib)}")
    con.execute(f"PRAGMA mmap_size={int(mmap_bytes)}")
    con.executescript(SCHEMA_SQL)
    if con.execute("SELECT v FROM meta WHERE k='schema'").fetchone() is None:
        con.execute("INSERT INTO meta VALUES ('schema', ?)", (str(SCHEMA),))
    return con


def header_ok(folder: str | Path) -> tuple[bool, str]:
    """The CHEAP check at open (07:31 item 5): the file exists, its size covers page_count x
    page_size, the schema is this one, and last_merged names a memory save in the folder. The
    full quick_check runs at the sleep."""
    p = path(folder)
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
    if os.path.getsize(p) < pc * ps:
        return False, f"size {os.path.getsize(p)} < page_count x page_size {pc * ps}"
    if schema is None or schema[0] != str(SCHEMA):
        return False, f"schema {schema}"
    if last is not None and not (Path(folder) / f"gen_{last[0]}.json").exists():
        return False, f"last_merged {last[0]} is not in the archive"
    return True, "ok"


class Syms:
    def __init__(self, con: sqlite3.Connection):
        self.con = con
        self.ids = {s: i for i, s in con.execute("SELECT id, s FROM sym")}

    def __call__(self, s: str) -> int:
        i = self.ids.get(s)
        if i is None:
            i = self.ids[s] = len(self.ids) + 1
            self.con.execute("INSERT INTO sym VALUES (?,?)", (i, s))
        return i


def _j(x: Any) -> str:
    return json.dumps(x, sort_keys=True)


def _get_blob(con: sqlite3.Connection, k: str, default: Any) -> Any:
    r = con.execute("SELECT v FROM blob WHERE k=?", (k,)).fetchone()
    return json.loads(r[0]) if r else default


def _fold_apply(f: dict, h: str, g: dict) -> dict:
    """lineage.fold's loop body for ONE generation of a LINEAR chain (every status and keyed value
    has one head): the same rows in the same order. A merge generation, or a status for a row the
    store does not hold, is refused."""
    if g.get("merge") or len(g.get("parents", [])) > 1:
        raise Refused(f"generation {h} is a merge; the store holds linear chains only")
    rows = f.setdefault("rows", {})
    for r in g["terms"]:
        row = {**r, "born": h}
        rows[_j([row["born"], row.get("handle")])] = row
    for st in g["status"]:
        k = _j([st["born"], st["handle"]])
        if k not in rows:
            raise Refused(f"status for an unknown row {k}")
        rows[k]["admitted"] = st["admitted"]
    for fld in ("invented", "book"):
        f.setdefault(fld, {}).update(g[fld])
    f.setdefault("vindication", []).extend(g["vindication_tail"])
    f.setdefault("evidence", []).extend(g["evidence"])
    return f


def _add(into: dict, d: dict) -> None:
    for k, n in d.items():
        into[k] = into.get(k, 0) + n


def _counts_apply(c: dict, g: dict) -> dict:
    """lineage.load's root-to-tip sums for one generation, in the same order of first appearance."""
    _add(c.setdefault("unit_used", {}), g.get("unit_used") or {})
    for fld in ("line_grades", "root_grades", "kind_counts", "hazard_3a"):
        for k, d in g.get(fld, {}).items():
            _add(c.setdefault(fld, {}).setdefault(k, {}), d)
    _add(c.setdefault("cause_kinds", {}), g.get("cause_kinds", {}))
    for ek, du in g.get("entry_use", {}).items():
        into = c.setdefault("entry_use", {}).setdefault(ek, {})
        for fld, n in du.items():
            into[fld] = n if fld == "last" else into.get(fld, 0) + n
    c.setdefault("inventions", []).extend(g.get("inventions", ()))
    if g.get("seed"):
        c.setdefault("seeds", []).append(g["seed"])
    if "kinds_landed_n" not in g and g.get("kinds_landed"):
        c["kinds_set_form"] = c.get("kinds_set_form", 0) + len(g["kinds_landed"])
    return c


def _read_hashed(f: Path, prefix: str) -> dict:
    raw = f.read_bytes()
    if f.stem != f"{prefix}_{hashlib.sha256(raw).hexdigest()[:16]}":
        raise Refused(f"{f.name} does not hash to its name")
    return json.loads(raw)


def _merge_kinds(con: sqlite3.Connection, s: "Syms", g: dict) -> None:
    def kkey(e):
        return (s(e[0]), s(e[1]), s(_j(e[2])), s(_j(e[3])))
    kl = sorted({kkey(e) for e in g.get("kinds_landed", ())})
    con.executemany("INSERT INTO kind VALUES (?,?,?,?,1,0,0,NULL,NULL,NULL,-1) "
                    "ON CONFLICT DO UPDATE SET in_landed=1", kl)
    con.executemany("INSERT INTO kind VALUES (?,?,?,?,0,?,1,NULL,NULL,NULL,-1) "
                    "ON CONFLICT DO UPDATE SET n = n + excluded.n, has_n = 1",
                    sorted((*kkey(e), e[4]) for e in g.get("kinds_landed_n", ())))
    if "kinds_landed_n" not in g:     # a set-form generation counts each key once (load, 545)
        con.executemany("UPDATE kind SET n = n + 1, has_n = 1 "
                        "WHERE entry=? AND role=? AND kind_o=? AND kind_x=?", kl)
    con.executemany("INSERT INTO kind VALUES (?,?,?,?,0,0,0,?,?,?,?) "
                    + UPSERT_LAST.format(t="kind"),
                    [(*kkey(e), *e[4:8]) for e in g.get("kinds_last", ())])
    con.executemany("INSERT INTO pair VALUES (?,?,?,-1) "
                    "ON CONFLICT DO UPDATE SET n = n + excluded.n",
                    [(s(_j(e[2])), s(_j(e[3])), e[4]) for e in g.get("kinds_landed_n", ())])
    con.executemany("UPDATE pair SET last_seq = max(last_seq, ?) WHERE kind_o=? AND kind_x=?",
                    [(e[7], s(_j(e[2])), s(_j(e[3]))) for e in g.get("kinds_last", ())])
    con.executemany("INSERT INTO kind_dk VALUES (?,?,?,?,NULL,NULL,NULL,-1) "
                    "ON CONFLICT DO UPDATE SET n = n + excluded.n",
                    sorted((s(_j(e[0])), s(e[1]), s(_j(e[2])), e[3])
                           for e in g.get("kinds_landed_dk", ())))
    con.executemany("INSERT INTO kind_dk VALUES (?,?,?,0,?,?,?,?) "
                    + UPSERT_LAST.format(t="kind_dk"),
                    [(s(_j(e[0])), s(e[1]), s(_j(e[2])), *e[3:7])
                     for e in g.get("kinds_dk_last", ())])
    con.executemany("INSERT INTO kind_off VALUES (?,?,?,?) "
                    "ON CONFLICT DO UPDATE SET n = n + excluded.n",
                    sorted((s(_j(e[0])), s(e[1]), s(_j(e[2])), e[3])
                           for e in g.get("kinds_offered_dk", ())))


def _merge_asked(con: sqlite3.Connection, s: "Syms", k: int, bodies: list) -> None:
    for body in bodies:
        tally: dict = {}
        for e in body["entries"]:
            if e["slot"] is None:
                con.execute("INSERT OR IGNORE INTO ak_whole VALUES (?,?,?,?)",
                            (e["key"], e["role"], e["o"], e["x"]))
            key = (e["key"], e["role"], (e["slot"] or "").split(".", 1)[-1])
            tally[key] = tally.get(key, 0) + e.get("n", 1)
        con.executemany("INSERT INTO asked_tally VALUES (?,?,?,?,0,0,?,?) ON CONFLICT DO UPDATE "
                        "SET n_variants = n_variants + excluded.n_variants, "
                        "last_save = excluded.last_save",
                        sorted((s(a), s(b), s(c), n, k, k) for (a, b, c), n in tally.items()))


def _merge_held(con: sqlite3.Connection, s: "Syms", h: str, idx: dict) -> None:
    sig = (_j(idx["sig_arm"]), _j(sorted(idx["sig_atoms"])), _j(sorted(idx.get("sig_names", []))))
    con.execute("INSERT OR IGNORE INTO sig(arm, atoms, names) VALUES (?,?,?)", sig)
    sid = con.execute("SELECT id FROM sig WHERE arm=? AND atoms=? AND names=?", sig).fetchone()[0]
    con.executemany("INSERT INTO held VALUES (?,?,?,?,?) ON CONFLICT DO UPDATE SET "
                    "gen=excluded.gen, sig=excluded.sig, items=excluded.items",
                    [(s(e["key"]), s(e["role"]), h, sid, _j(e["items"])) for e in idx["entries"]])


def merge_save(con: sqlite3.Connection, folder: str | Path, h: str, g: dict) -> dict:
    """One memory save into the store, in ONE transaction: its gen_ body, its ak_ and idx_ files.
    Its parent must be the store's last_merged (a linear chain). Returns the phase times."""
    p = Path(folder)
    t0 = time.perf_counter()
    last = con.execute("SELECT v FROM meta WHERE k='last_merged'").fetchone()
    if (last[0] if last else None) != g.get("parent"):
        raise Refused(f"save {h}'s parent {g.get('parent')} is not last_merged {last}")
    k = (con.execute("SELECT max(k) FROM saves").fetchone()[0] or 0) + 1
    aks = [_read_hashed(f, f"ak_{h}") for f in sorted(p.glob(f"ak_{h}_*.json"))]
    files = sorted(p.glob(f"idx_{h}_*.json"))
    idx = _read_hashed(files[0], f"idx_{h}") if len(files) == 1 else None
    t1 = time.perf_counter()
    con.execute("BEGIN")
    s = Syms(con)
    _merge_asked(con, s, k, aks)
    _merge_kinds(con, s, g)
    if idx is not None:
        _merge_held(con, s, h, idx)
    else:
        con.execute("INSERT OR REPLACE INTO meta VALUES ('idx_gap', ?)",
                    (_j([h, f"{len(files)} index files"]),))
    f = _fold_apply(_get_blob(con, "fold", {}), h, g)
    c = _counts_apply(_get_blob(con, "counts", {}), g)
    c["n_saves"] = k
    con.execute("INSERT OR REPLACE INTO blob VALUES ('fold', ?)", (json.dumps(f),))
    con.execute("INSERT OR REPLACE INTO blob VALUES ('counts', ?)", (json.dumps(c),))
    con.execute("INSERT INTO saves VALUES (?,?,?)", (h, k, g.get("parent")))
    con.execute("INSERT OR REPLACE INTO meta VALUES ('last_merged', ?)", (h,))
    t2 = time.perf_counter()
    con.execute("COMMIT")
    t3 = time.perf_counter()
    return {"save": h, "k": k, "s_read": round(t1 - t0, 3), "s_statements": round(t2 - t1, 3),
            "s_commit": round(t3 - t2, 3)}


def sleep(con: sqlite3.Connection) -> dict:
    """The "sleep" (07:12 b): the checkpoint and the full quick_check, OFF the play path."""
    t0 = time.perf_counter()
    con.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    t1 = time.perf_counter()
    ok = con.execute("PRAGMA quick_check").fetchone()[0]
    t2 = time.perf_counter()
    return {"s_checkpoint": round(t1 - t0, 3), "s_quick_check": round(t2 - t1, 3),
            "quick_check": ok}


def unmerged(con: sqlite3.Connection, folder: str | Path) -> list:
    """The memory saves in the folder the store has not merged, by file name alone."""
    have = {r[0] for r in con.execute("SELECT h FROM saves")}
    return sorted(f.stem[4:] for f in Path(folder).glob("gen_*.json") if f.stem[4:] not in have)


def catch_up(con: sqlite3.Connection, folder: str | Path) -> list:
    """Merge every unmerged memory save, parent before child; each hash-checked against its
    name. ONE save's parse in memory at a time (the parents are read first, then each save is
    read again for its merge). The migration is this from an empty store."""
    def read(h: str) -> dict:
        raw = (Path(folder) / f"gen_{h}.json").read_bytes()
        if hashlib.sha256(raw).hexdigest()[:16] != h:
            raise Refused(f"gen_{h}.json does not hash to its name")
        return json.loads(raw)
    parent = {h: read(h).get("parent") for h in unmerged(con, folder)}
    out = []
    while parent:
        last = con.execute("SELECT v FROM meta WHERE k='last_merged'").fetchone()
        nxt = [h for h, q in parent.items() if q == (last[0] if last else None)]
        if len(nxt) != 1:
            raise Refused(f"{len(nxt)} saves continue the store's chain; {len(parent)} unmerged")
        del parent[nxt[0]]
        out.append(merge_save(con, folder, nxt[0], read(nxt[0])))
    return out
