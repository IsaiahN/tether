"""STEP (5a), THE SAVE MERGE ON THE LEARNED STORE'S ROWS (the reviewer 2026-10-24 20:00, option
(B)): one save -- its gen_ body, its ak_ files' entries, its idx_ -- merged into the db form's
(section, key, body) rows, the arithmetic of lineage_store.merge_save ported table by table, over
the TOUCHED keys only (and the kind rows whose no_dk flag a new kind_dk row moves, B1). Keys and
bodies are written exactly as harness/migrate_learned.table_rows decodes the old tables, so a
merged store equals a migrated one (X1). Shared with the old merge, unchanged:
lineage_store._fold_apply, _counts_apply (pure arithmetic on the two blobs), AkFile (reading an
ak_ file) and _j.

Each section's manifest digest is ADDITIVE: the sum mod 2^256 of sha256(key \\t body) per row, so
a save updates it in O(touched) (B2), never by re-reading the section."""
from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from pathlib import Path
from typing import Any

import lineage_store as ls

MOD = 1 << 256
PERCEPTION = frozenset({"kind", "kind_dk", "kind_off", "pair"})
CHUNK = 500
# the kind rows a kind_dk row bears on (no_dk's EXISTS, B1): by entry and the target column
DEP_INDEXES = (
    "CREATE INDEX IF NOT EXISTS kind_entry_o ON perception(json_extract(key, '$[0]'), "
    "json_extract(key, '$[2]')) WHERE section = 'kind'",
    "CREATE INDEX IF NOT EXISTS kind_entry_x ON perception(json_extract(key, '$[0]'), "
    "json_extract(key, '$[3]')) WHERE section = 'kind'",
    "CREATE INDEX IF NOT EXISTS kind_dk_et ON perception(json_extract(key, '$[1]'), "
    "json_extract(key, '$[2]')) WHERE section = 'kind_dk'")


def j(x: Any) -> str:
    return json.dumps(x, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def row_hash(key: str, body: str) -> int:
    return int.from_bytes(hashlib.sha256(f"{key}\t{body}\n".encode()).digest(), "big")


def additive_digest(rows: dict) -> list:
    return [len(rows), format(sum(row_hash(k, b) for k, b in rows.items()) % MOD, "064x")]


class Rows:
    """The touched rows of one save: fetched by key on first use, changed in memory, flushed in the
    save's transaction. Remembers each row's body as it was, for the manifest's additive update."""

    def __init__(self, con: sqlite3.Connection):
        self.con, self.cur, self.orig, self.dirty, self.pending = con, {}, {}, set(), set()

    def part(self, s: str) -> str:
        return "perception" if s in PERCEPTION else "learned"

    def fetch(self, s: str, keys) -> None:
        need = [k for k in dict.fromkeys(keys) if (s, k) not in self.cur]
        for i in range(0, len(need), CHUNK):
            chunk = need[i:i + CHUNK]
            got = dict(self.con.execute(
                f"SELECT key, body FROM {self.part(s)} WHERE section = ? AND key IN "
                f"({','.join('?' * len(chunk))})", (s, *chunk)))
            for k in chunk:
                b = got.get(k)
                self.orig[(s, k)] = b
                self.cur[(s, k)] = json.loads(b) if b is not None else None

    def get(self, s: str, k: str) -> dict | None:
        if (s, k) not in self.cur:
            self.fetch(s, [k])
        return self.cur[(s, k)]

    def put(self, s: str, k: str, body: dict) -> None:
        if (s, k) not in self.cur:
            self.fetch(s, [k])
        self.cur[(s, k)] = body
        self.dirty.add((s, k))
        self.pending.add((s, k))

    def flush(self) -> None:
        """Writes the rows changed since the last flush, in key order (B-tree locality)."""
        enc = self.__dict__.setdefault("enc", {})
        for sk in self.pending:
            enc[sk] = j(self.cur[sk])
        for p in ("learned", "perception"):
            rows = sorted((s, k, enc[(s, k)]) for (s, k) in self.pending if self.part(s) == p)
            # an UPSERT changes only body, so the indexes on key expressions are left alone
            self.con.executemany(f"INSERT INTO {p} VALUES (?, ?, ?) ON CONFLICT(section, key) "
                                 "DO UPDATE SET body = excluded.body", rows)
        self.pending = set()

    def manifest(self) -> dict:
        """(section -> (rows added, digest delta)) over every row this save changed (after the
        final flush, so each body's text is the one written)."""
        assert not self.pending, "manifest before the final flush"
        out: dict = {}
        for (s, k) in self.dirty:
            new, old = self.enc[(s, k)], self.orig[(s, k)]
            n, d = out.get(s, (0, 0))
            d += row_hash(k, new) - (row_hash(k, old) if old is not None else 0)
            out[s] = (n + (old is None), d)
        return out


class Syms:
    """lineage_store.Syms on the sym section: a new string gets id len + 1, in first-call order."""

    def __init__(self, rows: Rows):
        self.rows = rows
        self.ids = {json.loads(b)["s"]: json.loads(k)[0] for k, b in
                    rows.con.execute("SELECT key, body FROM learned WHERE section = 'sym'")}

    def __call__(self, s: str) -> int:
        i = self.ids.get(s)
        if i is None:
            i = self.ids[s] = len(self.ids) + 1
            self.rows.put("sym", j([i]), {"s": s})
        return i


def meta_get(rows: Rows, k: str) -> str | None:
    b = rows.get("meta", j([k]))
    return b["v"] if b else None


def meta_set(rows: Rows, k: str, v: str) -> None:
    rows.put("meta", j([k]), {"v": v})


def meta_add(rows: Rows, k: str, d: int) -> None:
    v = meta_get(rows, k)
    meta_set(rows, k, str(int(v if v is not None else 0) + d))


def meta_max(rows: Rows, k: str, x: int) -> None:
    v = meta_get(rows, k)
    meta_set(rows, k, str(max(int(v) if v is not None else x, x)))


def merge_kinds(rows: Rows, s: Syms, g: dict) -> None:
    """lineage_store._merge_kinds, ported: kind, pair, kind_dk, kind_off and the two kind metas.
    The kind values are encoded once per merge (lineage_store._key_memo, the old code's own
    memo)."""
    jj = ls._key_memo()
    kl, kn, klast = g.get("kinds_landed", ()), g.get("kinds_landed_n", ()), g.get("kinds_last", ())
    parts: dict = {}               # key -> (entry, role, kind_o, kind_x), decoded once

    def kkey(e) -> str:
        p = (e[0], e[1], jj(e[2]), jj(e[3]))
        s(p[0]), s(p[1]), s(p[2]), s(p[3])       # the sym calls, in the old code's order
        k = j(list(p))
        parts[k] = p
        return k
    kl_k = [kkey(e) for e in kl]
    kn_k = [kkey(e) for e in kn]
    klast_k = [kkey(e) for e in klast]
    touched = list(dict.fromkeys((*kl_k, *kn_k, *klast_k)))
    rows.fetch("kind", touched)

    def contrib() -> dict:      # _PAIR_CONTRIB over the touched rows
        out: dict = {}
        for k in touched:
            b = rows.get("kind", k)
            if b and b["in_landed"] == 1:
                key = parts[k][2:4]
                n, last = out.get(key, (0, None))
                v = b["l_seq"]
                out[key] = (n + (b["n"] if b["has_n"] else 1), v if last is None else max(last, v))
        return out

    def known() -> int:
        return sum(1 for k in touched if (rows.get("kind", k) or {}).get("in_landed") == 1)

    before, known0 = contrib(), known()
    blank = {"in_landed": 0, "n": 0, "has_n": 0, "l_game": None, "l_level": None, "l_cycle": None,
             "l_seq": -1, "no_dk": 0}
    for k in dict.fromkeys(kl_k):
        b = rows.get("kind", k)
        rows.put("kind", k, {**blank, "in_landed": 1} if b is None else {**b, "in_landed": 1})
    for e, k in zip(kn, kn_k, strict=True):
        b = rows.get("kind", k)
        rows.put("kind", k, {**blank, "n": e[4], "has_n": 1} if b is None
                 else {**b, "n": b["n"] + e[4], "has_n": 1})
    if "kinds_landed_n" not in g:
        for k in dict.fromkeys(kl_k):
            b = rows.get("kind", k)
            rows.put("kind", k, {**b, "n": b["n"] + 1, "has_n": 1})
    for e, k in zip(klast, klast_k, strict=True):   # UPSERT_LAST: the save's order; a tie: later
        b = rows.get("kind", k)
        lv = dict(zip(("l_game", "l_level", "l_cycle", "l_seq"), e[4:8], strict=True))
        if b is None:
            rows.put("kind", k, {**blank, **lv})
        elif lv["l_seq"] >= b["l_seq"]:
            rows.put("kind", k, {**b, **lv})
    after = contrib()
    for (o, x), (n, last) in sorted(after.items()):
        pk = j([o, x])
        b = rows.get("pair", pk)
        dn = n - before.get((o, x), (0, None))[0]
        rows.put("pair", pk, {"n": dn, "last_seq": last} if b is None else
                 {"n": b["n"] + dn, "last_seq": max(b["last_seq"], last)})
    meta_add(rows, "kinds_known", known() - known0)
    seqs = [e[7] for e in klast]
    if seqs:
        meta_max(rows, "kind_seq_max", max(seqs))
    dk_new, dk_last = g.get("kinds_landed_dk", ()), g.get("kinds_dk_last", ())

    def dkey(e) -> str:
        p = (jj(e[0]), e[1], jj(e[2]))
        s(p[0]), s(p[1]), s(p[2])
        return j(list(p))
    dk_new_k = [dkey(e) for e in dk_new]
    rows.fetch("kind_dk", dk_new_k)
    for e, k in zip(dk_new, dk_new_k, strict=True):
        b = rows.get("kind_dk", k)
        rows.put("kind_dk", k, {"n": e[3], "l_game": None, "l_level": None, "l_cycle": None,
                                "l_seq": -1} if b is None else {**b, "n": b["n"] + e[3]})
    dk_last_k = [dkey(e) for e in dk_last]
    rows.fetch("kind_dk", dk_last_k)
    for e, k in zip(dk_last, dk_last_k, strict=True):
        b = rows.get("kind_dk", k)
        lv = dict(zip(("l_game", "l_level", "l_cycle", "l_seq"), e[3:7], strict=True))
        if b is None:
            rows.put("kind_dk", k, {"n": 0, **lv})
        elif lv["l_seq"] >= b["l_seq"]:
            rows.put("kind_dk", k, {**b, **lv})
    s("CAUSE")
    rows.flush()     # the EXISTS below reads kind_dk as this save leaves it
    # no_dk on the touched kind rows: EXISTS once per DISTINCT (entry, target), each a parameterised
    # indexed SEARCH (a correlated or joined form over a temp table plans as a SCAN of the
    # expression index: measured 2026-10-24, 5x slower). Both columns bound, so a read is bounded by
    # its matches; one query per entry read all the entry's rows, a per-save cost growing with the
    # store (X1 B2, 2026-10-24)
    tgt_of = {k: (p[0], p[3] if p[1] == "CAUSE" else p[2]) for k, p in parts.items()}
    con = rows.con
    q = rows.__dict__.setdefault("q", {})
    q_has = ("SELECT 1 FROM perception INDEXED BY kind_dk_et WHERE section = 'kind_dk' AND "
             "json_extract(key, '$[1]') = ? AND json_extract(key, '$[2]') = ? AND "
             "json_extract(body, '$.n') > 0 LIMIT 1")
    want_pairs = sorted(set(tgt_of.values()))
    has = {p for p in want_pairs if con.execute(q_has, p).fetchone() is not None}
    q["entries"], q["nodk_pairs"], q["kind_touched"] = (len({p[0] for p in want_pairs}),
                                                        len(want_pairs), len(touched))
    for k in touched:
        b = rows.get("kind", k)
        want = 0 if tgt_of[k] in has else 1
        if b is not None and b["no_dk"] != want:
            rows.put("kind", k, {**b, "no_dk": want})
    # B1: kind rows NOT in this save, whose (entry, target) a new kind_dk row (n > 0) now covers
    # (the old second UPDATE), per distinct pair and target column
    dep = []
    pairs = sorted({(e[1], jj(e[2])) for e in dk_new if e[3] > 0})
    q["b1_pairs"] = len(pairs)
    for ent, tgt in pairs:
        for col, ix, cause in (("$[2]", "kind_entry_o", False), ("$[3]", "kind_entry_x", True)):
            for (k,) in con.execute(f"SELECT key FROM perception INDEXED BY {ix} WHERE "
                                    "section = 'kind' AND json_extract(key, '$[0]') = ? AND "
                                    f"json_extract(key, '{col}') = ?", (ent, tgt)):
                if (json.loads(k)[1] == "CAUSE") == cause:
                    dep.append(k)
    rows.fetch("kind", dep)
    for k in dep:
        b = rows.get("kind", k)
        if b["no_dk"] == 1:
            rows.put("kind", k, {**b, "no_dk": 0})
    off = g.get("kinds_offered_dk", ())
    off_k = [dkey(e) for e in off]
    rows.fetch("kind_off", off_k)
    for e, k in zip(off, off_k, strict=True):
        b = rows.get("kind_off", k)
        rows.put("kind_off", k, {"n": e[3]} if b is None else {"n": b["n"] + e[3]})


def merge_asked(rows: Rows, s: Syms, k: int, h: str, bodies: list) -> None:
    """lineage_store._merge_asked, ported (the tallies from each ak_ file, read by its AkFile)."""
    for a in bodies:
        tally_n: dict = {}
        tally_1: dict = {}
        no_n = 0
        for e in a.entries():
            if "sc" in e:
                key = (e["key"], e["role"], e["sc"])
                tally_1[key] = tally_1.get(key, 0) + e["v"]
                tally_n[key] = tally_n.get(key, 0) + e["n"]
                continue
            if e.get("w"):
                wk = j([e["key"], e["role"], e["o"], e["x"]])
                if rows.get("ak_whole", wk) is None:
                    rows.put("ak_whole", wk, {})
                continue
            if e["slot"] is None:
                wk = j([e["key"], e["role"], e["o"], e["x"]])
                if rows.get("ak_whole", wk) is None:
                    rows.put("ak_whole", wk, {})
            key = (e["key"], e["role"], (e["slot"] or "").split(".", 1)[-1])
            tally_1[key] = tally_1.get(key, 0) + 1
            if "n" in e:
                tally_n[key] = tally_n.get(key, 0) + e["n"]
            else:
                no_n += 1
        new = a.tail.get("form") in (2, 3)
        if new and no_n:
            raise KeyError(f"n: {no_n} form-2 rows without n in {a.f.name}")
        tally = tally_n if new else tally_1
        for (x, y, z) in tally:   # the old generator's order: insertion, sorted only afterwards
            s(x), s(y), s(z)
        rows.fetch("asked_tally", [j(list(t)) for t in tally])
        if not new:
            for (x, y, z), n in sorted(tally.items()):
                tk = j([x, y, z])
                b = rows.get("asked_tally", tk)
                rows.put("asked_tally", tk, {"n_variants": n, "n_asked": 0, "n_landed": 0,
                                             "first_save": k, "last_save": k, "n_saves_asked": 0}
                         if b is None else {**b, "n_variants": b["n_variants"] + n, "last_save": k})
            continue
        if meta_get(rows, "n_variants_frozen_from") is None:
            meta_set(rows, "n_variants_frozen_from", h)
        for (x, y, z), n in sorted(tally.items()):
            tk = j([x, y, z])
            b = rows.get("asked_tally", tk)
            rows.put("asked_tally", tk, {"n_variants": 0, "n_asked": n, "n_landed": 0,
                                         "first_save": k, "last_save": k, "n_saves_asked": 1}
                     if b is None else
                     {**b, "n_asked": b["n_asked"] + n, "n_saves_asked": b["n_saves_asked"] + 1,
                      "last_save": k})


def merge_held(rows: Rows, s: Syms, h: str, idx: dict) -> None:
    """lineage_store._merge_held, ported: the signature row (INSERT OR IGNORE; id = max + 1), then
    each entry's held row replaced whole."""
    sig = (ls._j(idx["sig_arm"]), ls._j(sorted(idx["sig_atoms"])),
           ls._j(sorted(idx.get("sig_names", []))))
    sigs = {(json.loads(b)["arm"], json.loads(b)["atoms"], json.loads(b)["names"]): json.loads(k)[0]
            for k, b in rows.con.execute("SELECT key, body FROM learned WHERE section = 'sig'")}
    sigs.update({(b["arm"], b["atoms"], b["names"]): json.loads(k)[0]
                 for (sec, k), b in rows.cur.items() if sec == "sig" and b is not None})
    sid = sigs.get(sig)
    if sid is None:
        sid = max(sigs.values(), default=0) + 1
        rows.put("sig", j([sid]), {"arm": sig[0], "atoms": sig[1], "names": sig[2]})
    for e in idx["entries"]:
        s(e["key"]), s(e["role"])
    rows.fetch("held", [j([e["key"], e["role"]]) for e in idx["entries"]])
    for e in idx["entries"]:
        rows.put("held", j([e["key"], e["role"]]),
                 {"gen": h, "sig": sid, "items": ls._j(e["items"])})


def merge_save(con: sqlite3.Connection, h: str, g: dict, aks: list, idx: dict | None,
               n_idx_files: int) -> dict:
    """lineage_store.merge_save on the store's rows, in ONE transaction: refused unless the save's
    parent is the store's last_merged. Returns the phase times and the touched-key count (B2)."""
    t0 = time.perf_counter()
    for a in aks:
        a.verify()
    con.execute("BEGIN")
    try:
        rows = Rows(con)
        last = meta_get(rows, "last_merged")
        if last != g.get("parent"):
            raise ls.Refused(f"save {h}'s parent {g.get('parent')} is not last_merged {last}")
        k = (con.execute("SELECT max(CAST(json_extract(body, '$.k') AS INTEGER)) FROM learned "
                         "WHERE section = 'saves'").fetchone()[0] or 0) + 1
        s = Syms(rows)
        merge_asked(rows, s, k, h, aks)
        merge_kinds(rows, s, g)
        if idx is not None:
            merge_held(rows, s, h, idx)
        else:
            meta_set(rows, "idx_gap", ls._j([h, f"{n_idx_files} index files"]))
        rows.fetch("evidence", [j([k, i]) for i in range(len(g["evidence"]))])
        for i, e in enumerate(g["evidence"]):
            rows.put("evidence", j([k, i]), {"row": json.dumps(e)})
        rows.fetch("vindication", [j([k, i]) for i in range(len(g["vindication_tail"]))])
        for i, e in enumerate(g["vindication_tail"]):
            rows.put("vindication", j([k, i]), {"row": json.dumps(e)})
        meta_add(rows, "n_vindication", len(g["vindication_tail"]))
        if g.get("seed"):
            rows.put("seeds", j([k]), {"seed": json.dumps(g["seed"])})

        def blob(name):
            b = rows.get("blob", j([name]))
            return json.loads(b["v"]) if b else {}
        f = ls._fold_apply(blob("fold"), h, g)
        c = ls._counts_apply(blob("counts"), g)
        c["n_saves"] = k
        rows.put("blob", j(["fold"]), {"v": json.dumps(f)})
        rows.put("blob", j(["counts"]), {"v": json.dumps(c)})
        rows.put("saves", j([h]), {"k": k, "parent": g.get("parent")})
        meta_set(rows, "last_merged", h)
        if g.get("ended"):
            meta_set(rows, "ended",
                     json.dumps({"h": h, "ended": g["ended"], "error": g.get("error")}))
        rows.flush()
        update_manifest(con, rows.manifest())
        con.execute("COMMIT")
    except BaseException:
        if con.in_transaction:
            con.execute("ROLLBACK")
        raise
    s_merge = round(time.perf_counter() - t0, 3)
    # the checkpoint at the save boundary, never inside the commit and never deferred across saves
    # (the reviewer 2026-10-24 21:24): the WAL holds one save; its cost is its own number
    wal = Path(con.execute("PRAGMA database_list").fetchone()[2] + "-wal")
    wal_bytes = wal.stat().st_size if wal.exists() else 0
    t1 = time.perf_counter()
    con.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    return {"save": h, "k": k, "touched": len(rows.dirty), "s": s_merge,
            "s_checkpoint": round(time.perf_counter() - t1, 3), "wal_bytes": wal_bytes,
            "keys": sorted(rows.dirty), "q": rows.__dict__.get("q", {})}


def update_manifest(con: sqlite3.Connection, delta: dict) -> None:
    for sec, (dn, dd) in delta.items():
        r = con.execute("SELECT n, sha FROM manifest WHERE section = ?", (sec,)).fetchone()
        n, d = (r[0], int(r[1], 16)) if r else (0, 0)
        con.execute("INSERT OR REPLACE INTO manifest VALUES (?, ?, ?)",
                    (sec, n + dn, format((d + dd) % MOD, "064x")))


def open_new(path) -> sqlite3.Connection:
    """An empty db-form store with the step (4) tables, its indexes and the dependent-key
    indexes."""
    import store
    con = sqlite3.connect(path, isolation_level=None)
    con.execute("PRAGMA journal_mode=WAL")       # lineage_store.open_store's settings
    con.execute("PRAGMA synchronous=NORMAL")
    con.execute("PRAGMA wal_autocheckpoint=0")    # merge_save checkpoints at the save boundary
    con.execute("PRAGMA cache_size=-262144")
    for part in store.PARTS:
        con.execute(f"CREATE TABLE IF NOT EXISTS {part}(section TEXT, key TEXT, body TEXT, "
                    "PRIMARY KEY(section, key)) WITHOUT ROWID")
    con.execute("CREATE TABLE IF NOT EXISTS manifest(section TEXT PRIMARY KEY, n INTEGER, "
                "sha TEXT)")
    for sql in (*store.INDEXES.values(), *DEP_INDEXES):
        con.execute(sql.replace("CREATE INDEX ", "CREATE INDEX IF NOT EXISTS ", 1)
                    if "IF NOT EXISTS" not in sql else sql)
    if con.execute("SELECT 1 FROM learned WHERE section = 'meta' AND key = ?",
                   (j(["schema"]),)).fetchone() is None:
        con.execute("BEGIN")
        rows = Rows(con)
        meta_set(rows, "schema", str(ls.SCHEMA))
        rows.flush()
        update_manifest(con, rows.manifest())
        con.execute("COMMIT")
    return con
