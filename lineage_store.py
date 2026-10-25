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
import codecs
import hashlib
import json
import os
import sqlite3
import time
import zlib
from pathlib import Path
from typing import Any

import armflag

DB = "memory.db"
SCHEMA = 4
SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY, v TEXT);
CREATE TABLE IF NOT EXISTS sym(id INTEGER PRIMARY KEY, s TEXT UNIQUE);
CREATE TABLE IF NOT EXISTS saves(h TEXT PRIMARY KEY, k INTEGER, parent TEXT);
CREATE TABLE IF NOT EXISTS blob(k TEXT PRIMARY KEY, v TEXT);
CREATE TABLE IF NOT EXISTS asked_tally(entry INTEGER, role INTEGER, slot_class INTEGER,
    n_variants INTEGER, n_asked INTEGER, n_landed INTEGER, first_save INTEGER,
    last_save INTEGER, n_saves_asked INTEGER, PRIMARY KEY(entry, role, slot_class)) WITHOUT ROWID;
CREATE TABLE IF NOT EXISTS ak_whole(entry TEXT, role TEXT, o TEXT, x TEXT,
    PRIMARY KEY(entry, role, o, x)) WITHOUT ROWID;
CREATE TABLE IF NOT EXISTS kind(entry INTEGER, role INTEGER, kind_o INTEGER, kind_x INTEGER,
    in_landed INTEGER, n INTEGER, has_n INTEGER, l_game TEXT, l_level INTEGER,
    l_cycle INTEGER, l_seq INTEGER, no_dk INTEGER,
    PRIMARY KEY(entry, role, kind_o, kind_x)) WITHOUT ROWID;
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
CREATE INDEX IF NOT EXISTS kind_dk_et ON kind_dk(entry, tgt);
CREATE INDEX IF NOT EXISTS kind_nocount ON kind(entry) WHERE has_n = 0 AND in_landed = 1;
CREATE INDEX IF NOT EXISTS kind_t2 ON kind(entry) WHERE no_dk = 1 AND in_landed = 1;
CREATE TABLE IF NOT EXISTS evidence(k INTEGER, i INTEGER, row TEXT, PRIMARY KEY(k, i))
    WITHOUT ROWID;
CREATE TABLE IF NOT EXISTS vindication(k INTEGER, i INTEGER, row TEXT, PRIMARY KEY(k, i))
    WITHOUT ROWID;
CREATE TABLE IF NOT EXISTS seeds(k INTEGER PRIMARY KEY, seed TEXT);
"""
UPSERT_LAST = ("ON CONFLICT DO UPDATE SET l_game=excluded.l_game, l_level=excluded.l_level, "
               "l_cycle=excluded.l_cycle, l_seq=excluded.l_seq WHERE excluded.l_seq >= {t}.l_seq")


class Refused(Exception):
    """The store cannot answer this exactly; the caller loads from the archive."""


def path(folder: str | Path) -> Path:
    return Path(folder) / DB


# THE 20 MB CAP, part (i) (Isaiah 2026-10-25 05:31 "cap agent at 20mb memory cache of what it can
# store"; the reviewer 05:49): the store connection's page cache at 20 MiB and NO mmap, so its pages
# come only through the capped cache and every miss is read from memory.db. Was 256 MiB + 1 GiB
# mapped (the load's +116.5 MB working set, about 100 MB of it this connection). The same rows come
# back from cache or disk, so no answer changes; only speed can.
def open_store(folder: str | Path, cache_kib: int = 20480,
               mmap_bytes: int = 0) -> sqlite3.Connection:
    con = sqlite3.connect(path(folder), isolation_level=None)
    try:        # on any failure the connection is closed before the error leaves (no handle held)
        con.execute("PRAGMA journal_mode=WAL")
        con.execute("PRAGMA synchronous=NORMAL")
        con.execute("PRAGMA wal_autocheckpoint=0")    # never a checkpoint inside a merge's commit
        con.execute(f"PRAGMA cache_size=-{int(cache_kib)}")
        con.execute(f"PRAGMA mmap_size={int(mmap_bytes)}")
        con.executescript(SCHEMA_SQL)
        got = con.execute("SELECT v FROM meta WHERE k='schema'").fetchone()
        if got is None:
            con.execute("INSERT INTO meta VALUES ('schema', ?)", (str(SCHEMA),))
        elif got[0] != str(SCHEMA):
            raise Refused(f"store schema {got[0]}, this code writes {SCHEMA}")
    except BaseException:
        con.close()
        raise
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
    except sqlite3.DatabaseError as e:
        return False, f"unreadable: {e}"
    # closed on EVERY path: a handle left open on "unreadable" blocked H's set-aside rename on
    # Windows and crashed the load (h_chain f2, 2026-10-19)
    try:
        pc = con.execute("PRAGMA page_count").fetchone()[0]
        ps = con.execute("PRAGMA page_size").fetchone()[0]
        schema = con.execute("SELECT v FROM meta WHERE k='schema'").fetchone()
        last = con.execute("SELECT v FROM meta WHERE k='last_merged'").fetchone()
    except sqlite3.DatabaseError as e:
        return False, f"unreadable: {e}"
    finally:
        con.close()
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


# W1 (S2V; the reviewer 2026-10-21 15:38): _merge_kinds encoded the same few kind values with
# json.dumps once per row (607,920 key builds at one sp80 boundary). One merge keeps each value's
# string, keyed on repr(value): 1, True and 1.0 compare and hash alike and encode apart, and their
# reprs differ; a value of another top-level type is encoded fresh. OFF: _j per row (23a9077)
_KEY_MEMO = armflag.arm("TETHER_STORE_KEY_MEMO", default=True)
# W1's check run: every reuse also encodes fresh and compares; the fresh string is used. OFF: none
_KEY_MEMO_CHECK = armflag.arm("TETHER_STORE_KEY_MEMO_CHECK")
KEY_MEMO_N: dict = {"hit": 0, "bypass": 0, "agree": 0, "disagree": 0}
_MEMO_TYPES = (list, tuple, str, int, float, bool)


def _key_memo():
    """_j for one merge, remembering each value's string (W1)."""
    if not _KEY_MEMO:
        return _j
    memo: dict = {}

    def j(x: Any) -> str:
        if type(x) not in _MEMO_TYPES:
            KEY_MEMO_N["bypass"] += 1
            return _j(x)
        k = repr(x)
        out = memo.get(k)
        if out is None:
            out = memo[k] = _j(x)
            return out
        KEY_MEMO_N["hit"] += 1
        if _KEY_MEMO_CHECK:
            fresh = _j(x)
            KEY_MEMO_N["agree" if fresh == out else "disagree"] += 1
            out = fresh
        return out
    return j


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
    return f      # vindication and evidence are appended to their own tables (merge_save)


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
    if "kinds_landed_n" not in g and g.get("kinds_landed"):
        c["kinds_set_form"] = c.get("kinds_set_form", 0) + len(g["kinds_landed"])
    return c


def file_bytes(f: Path) -> bytes:
    """L2 (TETHER_COMPRESS, the reviewer 2026-10-20 11:06): a save file's own bytes. Every
    lineage file is JSON and opens with '{', never 0x78, so a first byte 0x78 is a zlib stream;
    anything else is read as written. Names and hashes are those of the uncompressed bytes."""
    raw = f.read_bytes()
    return zlib.decompress(raw) if raw[:1] == b"\x78" else raw


def file_chunks(f: Path, size: int):
    """file_bytes as a stream of at most about `size`-byte reads, decompressed as they are read."""
    with open(f, "rb") as fh:
        b = fh.read(size)
        if b[:1] != b"\x78":
            while b:
                yield b
                b = fh.read(size)
            return
        d = zlib.decompressobj()
        while b:
            out = d.decompress(b)
            if out:
                yield out
            b = fh.read(size)
        tail = d.flush()
        if tail:
            yield tail
        if not d.eof:
            raise Refused(f"{f.name}: a truncated compressed file")


def _read_hashed(f: Path, prefix: str) -> dict:
    raw = file_bytes(f)
    if f.stem != f"{prefix}_{hashlib.sha256(raw).hexdigest()[:16]}":
        raise Refused(f"{f.name} does not hash to its name")
    return json.loads(raw)


# M (the reviewer 2026-10-19 17:53, 19:21): an ak_ file is READ STREAMED, never parsed whole. On
# bp35's 216.5 MB ak_ the whole parse was 1,630 MiB of the save's 1,746 MiB in-merge rise; the
# streamed read peaked at 62 MiB with the same sha and tally (m_parse2, 4 real files)
AK_HEAD = '{"entries":['
AK_READ = 8 << 20      # bytes per read
AK_MARGIN = 1 << 20    # characters kept ahead of the decoder (an entry is far smaller)
AK_BATCH = 10_000      # ak_whole rows per executemany, in file order


class AkFile:
    """One ak_ file for _merge_asked. verify() (pass 1, before BEGIN): its sha256, in AK_READ
    reads, against its name. entries() (pass 2, inside the transaction): the entries decoded one
    at a time from a bounded buffer, hashing the same bytes as they are read; then the body's tail
    into .tail, and the digest must again equal the name's -- else Refused, and the merge rolls
    back. A file not opening with AK_HEAD is parsed whole and says so (.whole)."""

    def __init__(self, f: Path, prefix: str):
        self.f, self.prefix, self.chunk = f, prefix, AK_READ
        self.tail: dict = {}
        self.whole = False

    def verify(self) -> None:
        h = hashlib.sha256()
        for b in file_chunks(self.f, self.chunk):
            h.update(b)
        if self.f.stem != f"{self.prefix}_{h.hexdigest()[:16]}":
            raise Refused(f"{self.f.name} does not hash to its name")

    def entries(self):
        head = b""
        for c in file_chunks(self.f, 1 << 16):
            head += c
            if len(head) >= len(AK_HEAD):
                break
        head = head[:len(AK_HEAD)]
        if head != AK_HEAD.encode():
            self.whole = True
            body = _read_hashed(self.f, self.prefix)
            self.tail = {k: v for k, v in body.items() if k != "entries"}
            yield from body["entries"]
            return
        sha, dec = hashlib.sha256(), json.JSONDecoder()
        u8 = codecs.getincrementaldecoder("utf-8")()   # a read can split a character
        chunks = file_chunks(self.f, self.chunk)
        if True:
            buf, pos, done = "", 0, False

            def fill(need: int) -> None:
                nonlocal buf, pos, done
                while not done and len(buf) - pos < need:
                    b = next(chunks, b"")
                    sha.update(b)
                    done = not b
                    buf = buf[pos:] + u8.decode(b, final=done)
                    pos = 0
            fill(len(AK_HEAD))
            pos = len(AK_HEAD)
            while True:
                fill(AK_MARGIN)
                while pos < len(buf) and buf[pos] in ", \n":
                    pos += 1
                    fill(AK_MARGIN)
                if buf[pos] == "]":
                    break
                try:
                    e, end = dec.raw_decode(buf, pos)
                except ValueError:
                    if done:
                        raise
                    fill(len(buf) - pos + self.chunk)   # an entry longer than the margin
                    continue
                pos = end
                yield e
            fill(1 << 62)                                 # the rest: the tail, hashed too
            self.tail = json.loads("{" + buf[pos + 1:].lstrip(","))
        if self.f.stem != f"{self.prefix}_{sha.hexdigest()[:16]}":
            raise Refused(f"{self.f.name} changed between its check and its merge")


# THE PAIR TABLE'S INVARIANT (the reviewer 10:13 item 3; the seat 10:26): pair.n is the sum over the
# pair's kind rows of in_landed * (n if has_n else 1), and pair.last_seq the latest l_seq of those
# rows -- what _pair_counts reads off the old load (every known key: its summed n, else 1). The
# merge keeps it by the change in the touched rows' contribution, read before and after.
_PAIR_CONTRIB = ("SELECT k.kind_o, k.kind_x, SUM(CASE WHEN k.has_n THEN k.n ELSE 1 END), "
                 "MAX(k.l_seq) FROM temp.touched t JOIN kind k ON k.entry=t.entry AND "
                 "k.role=t.role AND k.kind_o=t.kind_o AND k.kind_x=t.kind_x WHERE k.in_landed=1 "
                 "GROUP BY k.kind_o, k.kind_x")
_KNOWN_TOUCHED = ("SELECT COUNT(*) FROM temp.touched t JOIN kind k ON k.entry=t.entry AND "
                  "k.role=t.role AND k.kind_o=t.kind_o AND k.kind_x=t.kind_x WHERE k.in_landed=1")


def _meta_add(con: sqlite3.Connection, k: str, d: int) -> None:
    v = con.execute("SELECT v FROM meta WHERE k=?", (k,)).fetchone()
    con.execute("INSERT OR REPLACE INTO meta VALUES (?, ?)", (k, str(int(v[0] if v else 0) + d)))


def _meta_max(con: sqlite3.Connection, k: str, x: int) -> None:
    v = con.execute("SELECT v FROM meta WHERE k=?", (k,)).fetchone()
    con.execute("INSERT OR REPLACE INTO meta VALUES (?, ?)",
                (k, str(max(int(v[0]) if v else x, x))))


def _merge_kinds(con: sqlite3.Connection, s: "Syms", g: dict) -> None:
    _j = _key_memo()

    def kkey(e):
        return (s(e[0]), s(e[1]), s(_j(e[2])), s(_j(e[3])))
    kl = sorted({kkey(e) for e in g.get("kinds_landed", ())})
    con.execute("CREATE TEMP TABLE IF NOT EXISTS touched(entry INTEGER, role INTEGER, "
                "kind_o INTEGER, kind_x INTEGER, PRIMARY KEY(entry, role, kind_o, kind_x)) "
                "WITHOUT ROWID")
    con.execute("DELETE FROM temp.touched")
    con.executemany("INSERT OR IGNORE INTO temp.touched VALUES (?,?,?,?)",
                    [*kl, *(kkey(e) for e in g.get("kinds_landed_n", ())),
                     *(kkey(e) for e in g.get("kinds_last", ()))])
    before = {(o, x): n for o, x, n, _l in con.execute(_PAIR_CONTRIB)}
    known0 = con.execute(_KNOWN_TOUCHED).fetchone()[0]
    con.executemany("INSERT INTO kind VALUES (?,?,?,?,1,0,0,NULL,NULL,NULL,-1,0) "
                    "ON CONFLICT DO UPDATE SET in_landed=1", kl)
    con.executemany("INSERT INTO kind VALUES (?,?,?,?,0,?,1,NULL,NULL,NULL,-1,0) "
                    "ON CONFLICT DO UPDATE SET n = n + excluded.n, has_n = 1",
                    sorted((*kkey(e), e[4]) for e in g.get("kinds_landed_n", ())))
    if "kinds_landed_n" not in g:     # a set-form generation counts each key once (load, 545)
        con.executemany("UPDATE kind SET n = n + 1, has_n = 1 "
                        "WHERE entry=? AND role=? AND kind_o=? AND kind_x=?", kl)
    con.executemany("INSERT INTO kind VALUES (?,?,?,?,0,0,0,?,?,?,?,0) "
                    + UPSERT_LAST.format(t="kind"),
                    [(*kkey(e), *e[4:8]) for e in g.get("kinds_last", ())])
    after = con.execute(_PAIR_CONTRIB).fetchall()
    con.executemany("INSERT INTO pair VALUES (?,?,?,?) ON CONFLICT DO UPDATE SET "
                    "n = n + excluded.n, last_seq = max(last_seq, excluded.last_seq)",
                    sorted((o, x, n - before.get((o, x), 0), last) for o, x, n, last in after))
    _meta_add(con, "kinds_known", con.execute(_KNOWN_TOUCHED).fetchone()[0] - known0)
    seqs = [e[7] for e in g.get("kinds_last", ())]
    if seqs:
        _meta_max(con, "kind_seq_max", max(seqs))
    con.executemany("INSERT INTO kind_dk VALUES (?,?,?,?,NULL,NULL,NULL,-1) "
                    "ON CONFLICT DO UPDATE SET n = n + excluded.n",
                    sorted((s(_j(e[0])), s(e[1]), s(_j(e[2])), e[3])
                           for e in g.get("kinds_landed_dk", ())))
    con.executemany("INSERT INTO kind_dk VALUES (?,?,?,0,?,?,?,?) "
                    + UPSERT_LAST.format(t="kind_dk"),
                    [(s(_j(e[0])), s(e[1]), s(_j(e[2])), *e[3:7])
                     for e in g.get("kinds_dk_last", ())])
    # T2's CANDIDATE FLAG (the reviewer 10:45 item 2): no_dk = 1 iff no kind_dk row with n > 0
    # exists for (entry, target), target = kind_x for a CAUSE, kind_o otherwise -- the old T2's
    # rule (tether.py _tiers) over the old load's kind_known_dk (summed n > 0 only)
    cause = s("CAUSE")
    con.execute("UPDATE kind SET no_dk = NOT EXISTS (SELECT 1 FROM kind_dk d WHERE "
                "d.entry = kind.entry AND d.n > 0 AND d.tgt = CASE WHEN kind.role = ? "
                "THEN kind.kind_x ELSE kind.kind_o END) WHERE (entry, role, kind_o, kind_x) "
                "IN (SELECT entry, role, kind_o, kind_x FROM temp.touched)", (cause,))
    con.executemany("UPDATE kind SET no_dk = 0 WHERE entry = ? AND no_dk = 1 AND "
                    "((role = ? AND kind_x = ?) OR (role <> ? AND kind_o = ?))",
                    sorted({(s(e[1]), cause, s(_j(e[2])), cause, s(_j(e[2])))
                            for e in g.get("kinds_landed_dk", ()) if e[3] > 0}))
    con.execute("DELETE FROM temp.touched")
    con.executemany("INSERT INTO kind_off VALUES (?,?,?,?) "
                    "ON CONFLICT DO UPDATE SET n = n + excluded.n",
                    sorted((s(_j(e[0])), s(e[1]), s(_j(e[2])), e[3])
                           for e in g.get("kinds_offered_dk", ())))


def _merge_asked(con: sqlite3.Connection, s: "Syms", k: int, h: str, bodies: list) -> None:
    # bodies: AkFile objects, each read once, streamed (M)
    """The OLD form (each row a variant's first appearance over the life) adds to n_variants. The
    NEW form (form 2, S4: the rows asked since the last save, each with n = times asked) adds n to
    n_asked and 1 to n_saves_asked (the memory saves the class was asked in; not counts' n_saves,
    the saves merged), and leaves n_variants frozen (the reviewer 08:26 item 3): a new-form row
    cannot tell a new variant from a repeat without a per-variant table."""
    for a in bodies:
        # the form sits after the entries in the file, so both tallies are kept until the tail
        tally_n: dict = {}
        tally_1: dict = {}
        no_n, batch = 0, []
        for e in a.entries():
            if "sc" in e:          # L1 form 3: a tally row, already summed by (key, role, class)
                key = (e["key"], e["role"], e["sc"])
                tally_1[key] = tally_1.get(key, 0) + e["v"]
                tally_n[key] = tally_n.get(key, 0) + e["n"]
                continue
            if e.get("w"):         # L1 form 3: a whole row, read by ak_whole only
                batch.append((e["key"], e["role"], e["o"], e["x"]))
                if len(batch) >= AK_BATCH:
                    con.executemany("INSERT OR IGNORE INTO ak_whole VALUES (?,?,?,?)", batch)
                    batch = []
                continue
            if e["slot"] is None:
                batch.append((e["key"], e["role"], e["o"], e["x"]))
                if len(batch) >= AK_BATCH:
                    con.executemany("INSERT OR IGNORE INTO ak_whole VALUES (?,?,?,?)", batch)
                    batch = []
            key = (e["key"], e["role"], (e["slot"] or "").split(".", 1)[-1])
            tally_1[key] = tally_1.get(key, 0) + 1
            if "n" in e:
                tally_n[key] = tally_n.get(key, 0) + e["n"]
            else:
                no_n += 1
        if batch:
            con.executemany("INSERT OR IGNORE INTO ak_whole VALUES (?,?,?,?)", batch)
        new = a.tail.get("form") in (2, 3)    # "3-from-1" (a migrated old-form file) adds variants
        if new and no_n:
            raise KeyError(f"n: {no_n} form-2 rows without n in {a.f.name}")
        tally = tally_n if new else tally_1
        if not new:
            con.executemany("INSERT INTO asked_tally VALUES (?,?,?,?,0,0,?,?,0) ON CONFLICT "
                            "DO UPDATE SET n_variants = n_variants + excluded.n_variants, "
                            "last_save = excluded.last_save",
                            sorted((s(a), s(b), s(c), n, k, k) for (a, b, c), n in tally.items()))
            continue
        con.execute("INSERT OR IGNORE INTO meta VALUES ('n_variants_frozen_from', ?)", (h,))
        con.executemany("INSERT INTO asked_tally VALUES (?,?,?,0,?,0,?,?,1) ON CONFLICT DO UPDATE "
                        "SET n_asked = n_asked + excluded.n_asked, "
                        "n_saves_asked = n_saves_asked + 1, last_save = excluded.last_save",
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
    aks = [AkFile(f, f"ak_{h}") for f in sorted(p.glob(f"ak_{h}_*.json"))]
    for a in aks:
        a.verify()      # pass 1: refused before any write
    files = sorted(p.glob(f"idx_{h}_*.json"))
    idx = _read_hashed(files[0], f"idx_{h}") if len(files) == 1 else None
    t1 = time.perf_counter()
    con.execute("BEGIN")
    try:
        out = _merge_body(con, h, k, g, aks, idx, files)
    except BaseException:
        if con.in_transaction:      # pass 2's re-hash, or any error: nothing of the save lands
            con.execute("ROLLBACK")
        raise
    t2 = time.perf_counter()
    con.execute("COMMIT")
    t3 = time.perf_counter()
    return {"save": h, "k": k, "s_read": round(t1 - t0, 3), "s_statements": round(t2 - t1, 3),
            "s_commit": round(t3 - t2, 3), **out}


def _merge_body(con: sqlite3.Connection, h: str, k: int, g: dict, aks: list, idx: dict | None,
                files: list) -> dict:
    """merge_save's statements, inside its transaction."""
    s = Syms(con)
    _merge_asked(con, s, k, h, aks)
    _merge_kinds(con, s, g)
    if idx is not None:
        _merge_held(con, s, h, idx)
    else:
        con.execute("INSERT OR REPLACE INTO meta VALUES ('idx_gap', ?)",
                    (_j([h, f"{len(files)} index files"]),))
    # the O(life) parts, APPENDED (the reviewer 08:17 3a, 11:27): never rewritten, never removed
    con.executemany("INSERT INTO evidence VALUES (?,?,?)",
                    [(k, i, json.dumps(e)) for i, e in enumerate(g["evidence"])])
    con.executemany("INSERT INTO vindication VALUES (?,?,?)",
                    [(k, i, json.dumps(e)) for i, e in enumerate(g["vindication_tail"])])
    _meta_add(con, "n_vindication", len(g["vindication_tail"]))
    if g.get("seed"):
        con.execute("INSERT INTO seeds VALUES (?,?)", (k, json.dumps(g["seed"])))
    f = _fold_apply(_get_blob(con, "fold", {}), h, g)
    c = _counts_apply(_get_blob(con, "counts", {}), g)
    c["n_saves"] = k
    con.execute("INSERT OR REPLACE INTO blob VALUES ('fold', ?)", (json.dumps(f),))
    con.execute("INSERT OR REPLACE INTO blob VALUES ('counts', ?)", (json.dumps(c),))
    con.execute("INSERT INTO saves VALUES (?,?,?)", (h, k, g.get("parent")))
    con.execute("INSERT OR REPLACE INTO meta VALUES ('last_merged', ?)", (h,))
    if g.get("ended"):  # item 4 (C3): read by the next load only while h is the tip
        con.execute("INSERT OR REPLACE INTO meta VALUES ('ended', ?)",
                    (json.dumps({"h": h, "ended": g["ended"], "error": g.get("error")}),))
    whole = [a.f.name for a in aks if a.whole]
    return {"ak_whole_parse": whole} if whole else {}


# THE WAL's SIZE BOUND (the reviewer 07:12 c, 07:19 3, 08:03 3b; ruled 10:08): a SIZE, never a time
# or an SSD assumption. Measured by T5b (wal_probe.py c318adaa, lineage_cnt's 19 saves, no
# checkpoint): point lookups and cluster reads FLAT from 101 MB to 555 MB of WAL, the -shm about
# 2 KB per MB, private bytes unchanged, so neither B nor read cost binds there. The bound is the
# EDGE OF WHAT WAS MEASURED; above it needs a new curve. Refuter: lookups rising with the WAL
# inside it, or the -shm growing faster than linear. A save that leaves the WAL above it
# checkpoints at that boundary (about 10.6 s on this HDD), reported as a play-path cost.
WAL_BOUND_BYTES: int | None = 555_137_072


def wal_bytes(folder: str | Path) -> int:
    w = Path(folder) / f"{DB}-wal"
    return w.stat().st_size if w.exists() else 0


def checkpoint(con: sqlite3.Connection) -> dict:
    """The WAL bound's checkpoint alone, at a boundary: no quick_check (that stays in the sleep)."""
    t0 = time.perf_counter()
    con.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    return {"s_checkpoint": round(time.perf_counter() - t0, 3)}


def note_end_path(con: sqlite3.Connection, wall_s: float, sleep_s: float) -> dict:
    """C1 (A)'s reserve (the reviewer 2026-10-22 14:27): the end path's measured wall and its
    sleep part, written after the sleep so the next life's load reads its predecessor's."""
    out = {"s": round(wall_s, 3), "sleep_s": round(sleep_s, 3)}
    con.execute("INSERT OR REPLACE INTO meta VALUES ('end_path', ?)", (json.dumps(out),))
    con.commit()
    return out


def read_end_path(con: sqlite3.Connection) -> dict | None:
    """The last end path's measured wall (note_end_path), or None when never measured."""
    v = con.execute("SELECT v FROM meta WHERE k='end_path'").fetchone()
    return json.loads(v[0]) if v else None


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
        raw = file_bytes(Path(folder) / f"gen_{h}.json")
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
