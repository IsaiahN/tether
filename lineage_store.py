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
import re
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


# THE 20 MB CAP (Isaiah 2026-10-25 05:31 "cap agent at 20mb memory cache of what it can store"; the
# reviewer 05:49, 06:06): ONE budget for all held from the store, every connection's page cache plus
# the store-derived structures. This connection: 8 MiB of pages and NO mmap, so every miss is read
# from memory.db (was 256 MiB + 1 GiB mapped); the load-time snapshot 2 MiB (lineage.DkSnapshot);
# _CARRIED and _LAZY answered from the held table (TETHER_CAP_HELD). Measured on the 33-save store:
# the load's working set was +116.5 MB before part (i) and +119.3 MB after it, so this connection
# was NOT most of it. The same rows come back from cache or disk, so no answer changes; only speed
# can.
def open_store(folder: str | Path, cache_kib: int = 8192,
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
    if g.get("aliases"):
        f.setdefault("aliases", []).extend(g["aliases"])     # (d), in chain order
    return f      # vindication and evidence are appended to their own tables (merge_save)


def _add(into: dict, d: dict) -> None:
    for k, n in d.items():
        into[k] = into.get(k, 0) + n


def _counts_apply(c: dict, g: dict, amap: dict | None = None, k: int = 0) -> dict:
    """lineage.load's root-to-tip sums for one generation, in the same order of first appearance.
    Under TETHER_KIND_ALIAS the routines carry their save index k (alias_routines), and under an
    alias map the action cells are read through it (alias_actions)."""
    if _ALIAS and g.get("routines_by_kind"):
        alias_routines(c, {r["key"]: r for r in g["routines_by_kind"]}, amap or {}, k)
        g = {x: v for x, v in g.items() if x != "routines_by_kind"}
    if amap and g.get("action_kinds"):
        alias_actions(c.setdefault("action_kinds", {}), g["action_kinds"], amap)
        g = {x: v for x, v in g.items() if x != "action_kinds"}
    if _AK_DELTA():
        add_action_increments(c.setdefault("action_kinds", {}), g.get("action_kinds_d"))
    _add(c.setdefault("unit_used", {}), g.get("unit_used") or {})
    for fld in ("line_grades", "root_grades", "kind_counts", "hazard_3a", "thought_tried",
                "thought_paid"):
        for k, d in g.get(fld, {}).items():
            _add(c.setdefault(fld, {}).setdefault(k, {}), d)
    _add(c.setdefault("cause_kinds", {}), g.get("cause_kinds", {}))
    _add(c.setdefault("stopped_at", {}), g.get("stopped_at", {}))
    for ek, du in g.get("entry_use", {}).items():
        into = c.setdefault("entry_use", {}).setdefault(ek, {})
        for fld, n in du.items():
            into[fld] = n if fld == "last" else into.get(fld, 0) + n
    c.setdefault("inventions", []).extend(g.get("inventions", ()))
    if g.get("routines_by_kind"):
        # (6c) THE FOLD, ONE ROW PER KIND FORM, the latest standing: load reads distinct kinds,
        # never lifetime (the reviewer 2026-10-26 06:32; Isaiah 10-19)
        c.setdefault("routines_by_kind", {}).update({r["key"]: r for r in g["routines_by_kind"]})
    if g.get("resolve_ok"):
        # r695 1: resolve verdicts per lineage, one row per (signature, entry, role), the latest
        c.setdefault("resolve_ok", {}).update(g["resolve_ok"])
    if g.get("action_kinds"):
        # r688 STORAGE: the action table by kind, one row per cell, the latest value kept
        c.setdefault("action_kinds", {}).update(g["action_kinds"])
    if "kinds_landed_n" not in g and g.get("kinds_landed"):
        c["kinds_set_form"] = c.get("kinds_set_form", 0) + len(g["kinds_landed"])
    return c


# K1's ALIAS GENERATION READ (the reviewer 2026-11-03 r886, r887, r902): a generation's
# "form_aliases" [[as_seen, canonical, pose]] joins the map in force (meta 'form_aliases'); the rows
# already stored are re-keyed there, and every later save's kinds and kind-keyed counts are read
# through it. Rows that meet are two sightings of one kind: n summed, the l_* of the greater l_seq,
# flags by max; an action cell's counts summed and its landed values united. The map is idempotent
# (lineage.alias_generation refuses one that is not), so a re-key at the alias generation and a
# translation on insert give one store. OFF: the field is ignored and every code stays as stored.
_ALIAS = armflag.arm("TETHER_KIND_ALIAS", default=True)
_FORM = re.compile(r"(?<![A-Za-z_])form=(\d+)")
_KIND_AT = {"kinds_landed": (2, 3), "kinds_landed_n": (2, 3), "kinds_last": (2, 3),
            "kinds_landed_dk": (0, 2), "kinds_dk_last": (0, 2), "kinds_offered_dk": (0, 2)}
_SUMMED2 = ("line_grades", "root_grades", "kind_counts", "hazard_3a", "thought_tried",
            "thought_paid")


def alias_add(amap: dict, pairs: Any) -> dict:
    """The map in force after one alias generation's pairs (as-seen -> canonical, ints)."""
    return {**amap, **{int(a): int(c) for a, c, *_pose in pairs}}


def alias_refusal(amap: dict, pairs: Any) -> str | None:
    """Why these pairs cannot join the map, or None (r903 2b, MF-K10, MF-K12): perception is
    deterministic, so an as-seen code with two canonicals is a defect; and the map stays
    idempotent (a canonical is the as-seen code of the canonical pose, so it maps to itself)."""
    have = dict(amap)
    for a, c, *_pose in pairs:
        a, c = int(a), int(c)
        if have.get(a, c) != c:
            return f"form {a} is aliased to {have[a]} and to {c}"
        have[a] = c
    onward = {a: c for a, c in have.items() if have.get(c, c) != c}
    if onward:
        a, c = sorted(onward.items())[0]
        return f"not idempotent: {a} -> {c} -> {have[c]} ({len(onward)} such)"
    return None


def alias_text(s: Any, amap: dict) -> Any:
    if not amap or not isinstance(s, str) or "form=" not in s:
        return s
    return _FORM.sub(lambda m: f"form={amap.get(int(m.group(1)), int(m.group(1)))}", s)


def _alias_val(x: Any, amap: dict) -> Any:
    if isinstance(x, str):
        return alias_text(x, amap)
    if isinstance(x, list | tuple):
        return [_alias_val(y, amap) for y in x]
    if isinstance(x, dict):
        return {alias_text(k, amap): _alias_val(v, amap) for k, v in x.items()}
    return x


def _sum_into(into: dict, d: dict, amap: dict) -> None:
    for k, n in d.items():
        k = alias_text(k, amap)
        into[k] = into.get(k, 0) + n


def _ak_meet(key: str, old: Any, new: Any) -> Any:
    import ast
    try:
        tab = ast.literal_eval(key)[1]
    except (ValueError, SyntaxError, IndexError, TypeError):
        return new
    if tab == "delta_kind":
        return [old[0] + new[0], old[1] + new[1]]
    return [json.loads(x) for x in sorted(set(map(_j, old)) | set(map(_j, new)))]


def alias_actions(into: dict, rows: dict, amap: dict) -> None:
    """The action cells through the map: a later save's cell replaces; two cells that meet in ONE
    re-key or ONE save are two sightings of one kind (_ak_meet: counts summed, landed values
    united)."""
    seen: dict = {}
    for k, v in rows.items():
        k2, v2 = alias_text(k, amap), _alias_val(v, amap)
        seen[k2] = _ak_meet(k2, seen[k2], v2) if k2 in seen else v2
    into.update(seen)


def _AK_DELTA() -> bool:
    import interface
    return interface._AK_DELTA


def add_action_increments(into: dict, rows: dict | None) -> None:
    """(7) TETHER_AK_DELTA: a save's action-cell increments added into the cells (_ak_meet: counts
    summed, landed values united); the keys are already read through the alias map (alias_gen)."""
    for key, v in (rows or {}).items():
        into[key] = _ak_meet(key, into[key], v) if key in into else v


def alias_routines(c: dict, rows: dict, amap: dict, k: int | None) -> None:
    """routines_by_kind through the map (the reviewer 2026-11-03 r904 1), with each key's save
    index in routines_k: `rows` from save k, or k None to re-key what `c` holds. Two pre-images that
    meet with different rows are a CONTEST, both kept in contested_routines; the read value is the
    later save's (then the greater text). Equal rows are no contest. A later save's row for a key
    replaces it, as before."""
    ks = c.setdefault("routines_k", {})
    if k is None:
        rows = c.get("routines_by_kind", {})
    seen: dict = {}
    seen_k: dict = {}
    for key, v in rows.items():
        k2 = alias_text(key, amap)
        v2 = {**_alias_val(v, amap), "key": k2}
        kv = ks.get(key, 0) if k is None else k
        if k2 in seen:
            pv, pk = seen[k2], seen_k[k2]
            if {x: y for x, y in pv.items() if x != "key"} != {
                    x: y for x, y in v2.items() if x != "key"}:
                rec = c.setdefault("contested_routines", {}).setdefault(k2, [])
                rec.extend(r for r in (pv, v2) if r not in rec)
            if (kv, _j(v2)) < (pk, _j(pv)):
                v2, kv = pv, pk
        seen[k2], seen_k[k2] = v2, kv
    if k is None:
        c["routines_by_kind"], c["routines_k"] = seen, seen_k
    else:
        c.setdefault("routines_by_kind", {}).update(seen)
        ks.update(seen_k)


def alias_counts(c: dict, amap: dict) -> dict:
    """The counts blob re-keyed through the map (at an alias generation)."""
    out = dict(c)
    for fld in _SUMMED2:
        if fld in c:
            new: dict = {}
            for k, d in c[fld].items():
                _sum_into(new.setdefault(alias_text(k, amap), {}), d, amap)
            out[fld] = new
    if "cause_kinds" in c:
        out["cause_kinds"] = {}
        _sum_into(out["cause_kinds"], c["cause_kinds"], amap)
    if "action_kinds" in c:
        out["action_kinds"] = {}
        alias_actions(out["action_kinds"], c["action_kinds"], amap)
    if "routines_by_kind" in c:
        alias_routines(out, {}, amap, None)
    return out


def alias_gen(g: dict, amap: dict) -> dict:
    """One save's kinds and kind-keyed counts read through the map (a shallow copy); the
    latest-wins fields are left to alias_actions and alias_routines."""
    if not amap:
        return g
    out = dict(g)
    for fld, at in _KIND_AT.items():
        if fld in g:
            out[fld] = [[_alias_val(x, amap) if i in at else x for i, x in enumerate(e)]
                        for e in g[fld]]
    for fld in _SUMMED2:
        if fld in g:
            new: dict = {}
            for k, d in g[fld].items():
                _sum_into(new.setdefault(alias_text(k, amap), {}), d, amap)
            out[fld] = new
    if "cause_kinds" in g:
        out["cause_kinds"] = {}
        _sum_into(out["cause_kinds"], g["cause_kinds"], amap)
    if g.get("action_kinds_d"):          # (7): increments meet by sum, as two sightings
        out["action_kinds_d"] = {}
        alias_actions(out["action_kinds_d"], g["action_kinds_d"], amap)
    return out


def alias_chain(chain: list) -> list:
    """lineage.load's archive read under the alias generations, giving the store's state: every
    save's kinds and summed counts through the whole map (sums do not depend on order), and the
    latest-wins fields folded in chain order with the re-key at each alias generation, placed on
    the last save. A chain with no alias generation, or OFF: unchanged."""
    if not _ALIAS or not any(g.get("form_aliases") for _h, g in chain):
        return chain
    full: dict = {}
    for _h, g in chain:
        full = alias_add(full, g.get("form_aliases", ()))
    run: dict = {}
    ak: dict = {}
    rk: dict = {}
    out = []
    for i, (h, g) in enumerate(chain):
        if g.get("form_aliases"):
            run = alias_add(run, g["form_aliases"])
            was, ak = ak, {}
            alias_actions(ak, was, run)
            alias_routines(rk, {}, run, None)
        if g.get("action_kinds"):
            if run:
                alias_actions(ak, g["action_kinds"], run)
            else:
                ak.update(g["action_kinds"])
        if g.get("routines_by_kind"):     # the store's save index: k = position + 1
            alias_routines(rk, {r["key"]: r for r in g["routines_by_kind"]}, run, i + 1)
        out.append((h, {k: v for k, v in alias_gen(g, full).items()
                        if k not in ("action_kinds", "routines_by_kind")}))
    h, g = out[-1]
    out[-1] = (h, {**g, "action_kinds": ak,
                   "routines_by_kind": list(rk.get("routines_by_kind", {}).values())})
    return out


def alias_map(con: sqlite3.Connection) -> dict:
    r = con.execute("SELECT v FROM meta WHERE k='form_aliases'").fetchone()
    return {int(a): c for a, c in json.loads(r[0]).items()} if r else {}


_REKEY_KIND = (
    "INSERT INTO kind SELECT entry, role, COALESCE(m1.new, kind_o), COALESCE(m2.new, kind_x), "
    "in_landed, n, has_n, l_game, l_level, l_cycle, l_seq, no_dk FROM temp.mv_kind "
    "LEFT JOIN temp.smap m1 ON m1.old = kind_o LEFT JOIN temp.smap m2 ON m2.old = kind_x "
    "WHERE 1 ORDER BY l_seq, entry, role, kind_o, kind_x ON CONFLICT DO UPDATE SET "
    "in_landed = max(in_landed, excluded.in_landed), n = n + excluded.n, "
    "has_n = max(has_n, excluded.has_n), "
    "l_game = CASE WHEN excluded.l_seq >= l_seq THEN excluded.l_game ELSE l_game END, "
    "l_level = CASE WHEN excluded.l_seq >= l_seq THEN excluded.l_level ELSE l_level END, "
    "l_cycle = CASE WHEN excluded.l_seq >= l_seq THEN excluded.l_cycle ELSE l_cycle END, "
    "l_seq = max(l_seq, excluded.l_seq)")
_REKEY_DK = (
    "INSERT INTO kind_dk SELECT COALESCE(m1.new, dk), entry, COALESCE(m2.new, tgt), n, l_game, "
    "l_level, l_cycle, l_seq FROM temp.mv_dk LEFT JOIN temp.smap m1 ON m1.old = dk "
    "LEFT JOIN temp.smap m2 ON m2.old = tgt WHERE 1 ORDER BY l_seq, dk, entry, tgt "
    "ON CONFLICT DO UPDATE SET n = n + excluded.n, "
    "l_game = CASE WHEN excluded.l_seq >= l_seq THEN excluded.l_game ELSE l_game END, "
    "l_level = CASE WHEN excluded.l_seq >= l_seq THEN excluded.l_level ELSE l_level END, "
    "l_cycle = CASE WHEN excluded.l_seq >= l_seq THEN excluded.l_cycle ELSE l_cycle END, "
    "l_seq = max(l_seq, excluded.l_seq)")
_REKEY_OFF = (
    "INSERT INTO kind_off SELECT COALESCE(m1.new, dk), entry, COALESCE(m2.new, ko), n "
    "FROM temp.mv_off LEFT JOIN temp.smap m1 ON m1.old = dk LEFT JOIN temp.smap m2 ON m2.old = ko "
    "WHERE 1 ORDER BY dk, entry, ko ON CONFLICT DO UPDATE SET n = n + excluded.n")


def _apply_aliases(con: sqlite3.Connection, s: "Syms", pairs: Any) -> dict:
    """An alias generation: the map in force grows by its pairs, and every stored kind row, delta
    row, offer row, pair and kind-keyed count is re-keyed through it. A pair's n is the sum of its
    landed kinds' contributions (what _merge_kinds accumulates, telescoped), so it is recomputed
    for every pair a re-keyed kind now names; kinds_known and no_dk likewise."""
    why = alias_refusal(alias_map(con), pairs)
    if why:
        raise Refused(f"form_aliases: {why}")
    amap = alias_add(alias_map(con), pairs)
    con.execute("INSERT OR REPLACE INTO meta VALUES ('form_aliases', ?)",
                (json.dumps({str(a): c for a, c in sorted(amap.items())}),))
    smap = {}
    for txt, sid in list(s.ids.items()):
        t2 = alias_text(txt, amap)
        if t2 != txt:
            smap[sid] = s(t2)
    con.execute("CREATE TEMP TABLE IF NOT EXISTS smap(old INTEGER PRIMARY KEY, new INTEGER)")
    con.execute("DELETE FROM temp.smap")
    con.executemany("INSERT INTO temp.smap VALUES (?,?)", sorted(smap.items()))
    if smap:
        known0 = con.execute("SELECT COUNT(*) FROM kind WHERE in_landed = 1").fetchone()[0]
        old = "(SELECT old FROM temp.smap)"
        for t, cols, sql in (("kind", ("kind_o", "kind_x"), _REKEY_KIND),
                             ("kind_dk", ("dk", "tgt"), _REKEY_DK),
                             ("kind_off", ("dk", "ko"), _REKEY_OFF)):
            where = " OR ".join(f"{c} IN {old}" for c in cols)
            mv = "mv_" + t.replace("kind_", "") if t != "kind" else "mv_kind"
            con.execute(f"DROP TABLE IF EXISTS temp.{mv}")
            con.execute(f"CREATE TEMP TABLE {mv} AS SELECT * FROM {t} WHERE {where}")
            con.execute(f"DELETE FROM {t} WHERE {where}")
            con.execute(sql)
            con.execute(f"DROP TABLE temp.{mv}")
        new = "(SELECT new FROM temp.smap)"
        con.execute(f"DELETE FROM pair WHERE kind_o IN {old} OR kind_x IN {old} "
                    f"OR kind_o IN {new} OR kind_x IN {new}")
        con.execute("INSERT INTO pair SELECT kind_o, kind_x, "
                    "SUM(CASE WHEN has_n THEN n ELSE 1 END), "
                    f"MAX(l_seq) FROM kind WHERE in_landed = 1 AND (kind_o IN {new} OR kind_x IN "
                    f"{new}) GROUP BY kind_o, kind_x")
        cause = s("CAUSE")
        con.execute("UPDATE kind SET no_dk = NOT EXISTS (SELECT 1 FROM kind_dk d WHERE "
                    "d.entry = kind.entry AND d.n > 0 AND d.tgt = CASE WHEN kind.role = ? "
                    f"THEN kind.kind_x ELSE kind.kind_o END) WHERE kind_o IN {new} OR "
                    f"kind_x IN {new}", (cause,))
        _meta_add(con, "kinds_known", con.execute(
            "SELECT COUNT(*) FROM kind WHERE in_landed = 1").fetchone()[0] - known0)
    con.execute("DELETE FROM temp.smap")
    return amap


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
        # once per row as written: two as-seen keys an alias joins count twice, as the load does
        many: dict = {}
        for e in g.get("kinds_landed", ()):
            many[kkey(e)] = many.get(kkey(e), 0) + 1
        con.executemany("UPDATE kind SET n = n + ?, has_n = 1 "
                        "WHERE entry=? AND role=? AND kind_o=? AND kind_x=?",
                        [(many[x], *x) for x in kl])
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


def merge_save(con: sqlite3.Connection, folder: str | Path, h: str, g: dict,
               state: Any = None) -> dict:
    """One memory save into the store, in ONE transaction: its gen_ body, its ak_ and idx_ files.
    Its parent must be the store's last_merged (a linear chain); in a rebuild or a continue
    (`state`, A2) every parent must already be merged. Returns the phase times."""
    p = Path(folder)
    t0 = time.perf_counter()
    if state is None:
        last = con.execute("SELECT v FROM meta WHERE k='last_merged'").fetchone()
        if (last[0] if last else None) != g.get("parent"):
            raise Refused(f"save {h}'s parent {g.get('parent')} is not last_merged {last}")
    else:
        have = {r[0] for r in con.execute("SELECT h FROM saves")}
        if not set(_parents(g)) <= have:
            raise Refused(f"save {h}'s parents {_parents(g)} are not all merged")
    k = (con.execute("SELECT max(k) FROM saves").fetchone()[0] or 0) + 1
    aks = [AkFile(f, f"ak_{h}") for f in sorted(p.glob(f"ak_{h}_*.json"))]
    for a in aks:
        a.verify()      # pass 1: refused before any write
    files = sorted(p.glob(f"idx_{h}_*.json"))
    idx = _read_hashed(files[0], f"idx_{h}") if len(files) == 1 else None
    t1 = time.perf_counter()
    con.execute("BEGIN")
    try:
        out = _merge_body(con, h, k, g, aks, idx, files, state)
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
                files: list, state: Any = None) -> dict:
    """merge_save's statements, inside its transaction."""
    s = Syms(con)
    amap: dict = {}
    if _ALIAS:
        if g.get("form_aliases"):
            amap = _apply_aliases(con, s, g["form_aliases"])
            con.execute("INSERT OR REPLACE INTO blob VALUES ('counts', ?)",
                        (json.dumps(alias_counts(_get_blob(con, "counts", {}), amap)),))
        else:
            amap = alias_map(con)
        g = alias_gen(g, amap)
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
    if state is None:
        f = _fold_apply(_get_blob(con, "fold", {}), h, g)
    else:
        state.step(h, g)
        f = _state_fold(state)
    c = _counts_apply(_get_blob(con, "counts", {}), g, amap, k)
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


def _parents(g: dict) -> list:
    """lineage._parents: a merge generation names several ("parents"), every other one or none."""
    if "parents" in g:
        return list(g["parents"])
    return [g["parent"]] if g.get("parent") else []


def _state_fold(state: Any) -> dict:
    """A2: the store's fold blob from lineage.FoldState -- the same rows in the same order, keyed
    as _fold_apply keys them, with the contested records fold keeps."""
    out = state.result()
    f = {"rows": {_j([r["born"], r.get("handle")]): r for r in out["terms"]},
         "invented": out["invented"], "book": out["book"]}
    for k in ("aliases", "contested_invented", "contested_book"):
        if out.get(k):
            f[k] = out[k]
    return f


# A2 THE STORE READS A BRANCHED LINEAGE (the reviewer 2026-11-02 r784, Isaiah 06:31): a lineage
# joined by lineage.merge was refused here ("linear chains only") and every load and save then
# refolded the whole archive (the 47 GB path, 2026-10-31). ON: when the unmerged saves do not
# continue the store's chain one by one, the store is REBUILT from the saves in lineage._topo
# order, one save parsed at a time, through lineage.FoldState -- fold's own rule for contested
# statuses and keys -- so the store and the archive read one DAG alike. Later saves continue the
# merge generation linearly, as before. OFF: refused, as before.
_DAG = armflag.arm("TETHER_STORE_DAG", default=True)
_TABLES = ("sym", "saves", "blob", "asked_tally", "ak_whole", "kind", "pair", "kind_dk", "kind_off",
           "sig", "held", "evidence", "vindication", "seeds")


def _rebuild(con: sqlite3.Connection, folder: str | Path, read: Any) -> list:
    """A2: the store emptied and refilled from every save in the folder, in lineage._topo order.
    The store is derived from the saves, so emptying it loses nothing; a rebuild cut short is
    caught by the next catch_up and run again."""
    import lineage
    p = Path(folder)
    gens = {f.stem[4:]: {"parents": _parents(read(f.stem[4:]))} for f in p.glob("gen_*.json")}
    order = lineage._topo(gens)
    con.execute("BEGIN")
    try:
        for t in _TABLES:
            con.execute(f"DELETE FROM {t}")
        con.execute("DELETE FROM meta WHERE k <> 'schema'")
    except BaseException:
        con.execute("ROLLBACK")
        raise
    con.execute("COMMIT")
    state = lineage.FoldState(lists=False)
    out = []
    for h in order:
        out.append({**merge_save(con, folder, h, read(h), state), "dag": "rebuild"})
        # the save path's WAL bound (r794 3): every save rewrites the fold blob, so a rebuild with
        # no checkpoint grew the WAL with saves x blob (17.6 GB at about save 120 of 250, 11-02)
        if WAL_BOUND_BYTES is not None and wal_bytes(folder) > WAL_BOUND_BYTES:
            out[-1]["wal_bound"] = {"wal_bytes": wal_bytes(folder), **checkpoint(con)}
    return out


# A2c CONTINUE (the reviewer 2026-11-02 r792): when fold's _topo order is the store's merged chain
# followed by exactly the new saves, the new saves are appended in that order through the rebuild's
# own body, its lineage.FoldState seeded by stepping the store's chain from the saves in memory
# (nothing written): the same fold blob as the rebuild, contested statuses and book keys included
# (two branches that both played contest every counter both moved), and every other table appended
# in the rebuild's order. Minutes instead of hours. Otherwise None, and the full rebuild runs.
# OFF: always the rebuild.
_CONTINUE = armflag.arm("TETHER_STORE_CONTINUE", default=True)
_CONTINUE_WAL = armflag.arm("TETHER_CONTINUE_WAL", default=True)


def _continue(con: sqlite3.Connection, folder: str | Path, read: Any, ps: dict) -> list | None:
    """A2c: the unmerged saves (`ps`, their parents) in _topo order when they follow the store's
    chain, else None."""
    import lineage
    merged = [r[0] for r in con.execute("SELECT h FROM saves ORDER BY k")]
    gens: dict[str, dict] = {}
    for h, p in con.execute("SELECT h, parent FROM saves"):
        # a root and a merge save both store no single parent: their own file names theirs
        gens[h] = {"parents": [p] if p else _parents(read(h))}
    gens.update({h: {"parents": q} for h, q in ps.items()})
    order = lineage._topo(gens)
    new = order[len(merged):]
    if order[:len(merged)] != merged or set(new) != set(ps):
        return None
    state = lineage.FoldState(lists=False)
    for h in merged:
        state.step(h, read(h))
    out = []
    for h in new:
        out.append({**merge_save(con, folder, h, read(h), state), "dag": "continue"})
        # the rebuild's WAL bound (r794 3), here too: a continue of many saves grew the WAL to
        # 2.14 GB on 2026-11-03 (REPORT FIN5E §8). OFF (TETHER_CONTINUE_WAL): no bound, as before
        if (_CONTINUE_WAL and WAL_BOUND_BYTES is not None
                and wal_bytes(folder) > WAL_BOUND_BYTES):
            out[-1]["wal_bound"] = {"wal_bytes": wal_bytes(folder), **checkpoint(con)}
    return out


def catch_up(con: sqlite3.Connection, folder: str | Path) -> list:
    """Merge every unmerged memory save, parent before child; each hash-checked against its
    name. ONE save's parse in memory at a time (the parents are read first, then each save is
    read again for its merge). The migration is this from an empty store."""
    def read(h: str) -> dict:
        raw = file_bytes(Path(folder) / f"gen_{h}.json")
        if hashlib.sha256(raw).hexdigest()[:16] != h:
            raise Refused(f"gen_{h}.json does not hash to its name")
        return json.loads(raw)
    ps = {h: _parents(read(h)) for h in unmerged(con, folder)}
    if _DAG and any(len(q) > 1 for q in ps.values()):
        return (_CONTINUE and _continue(con, folder, read, ps)) or _rebuild(con, folder, read)
    parent = {h: (q[0] if len(q) == 1 else None) for h, q in ps.items()}
    out = []
    while parent:
        last = con.execute("SELECT v FROM meta WHERE k='last_merged'").fetchone()
        nxt = [h for h, q in parent.items() if q == (last[0] if last else None)]
        if len(nxt) != 1:
            if _DAG:
                rest = {h: ps[h] for h in parent}
                return out + ((_CONTINUE and _continue(con, folder, read, rest))
                              or _rebuild(con, folder, read))
            raise Refused(f"{len(nxt)} saves continue the store's chain; {len(parent)} unmerged")
        del parent[nxt[0]]
        out.append(merge_save(con, folder, nxt[0], read(nxt[0])))
    return out
