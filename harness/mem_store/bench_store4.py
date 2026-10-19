"""THE STORE AS RULED (the reviewer 2026-10-19 07:12): the asked record CONDENSED (asked_tally), the kind tables, the
pair totals kept from each save's delta, wal_autocheckpoint 0 so no checkpoint runs inside a merge's commit, and the
"sleep" (an explicit checkpoint after each save) timed APART. ONE FLAG (--intkeys): text keys as (B), or every repeated
string interned into a symbol table and the big tables keyed by integer tuples (the reviewer 07:06 item 5). READ ONLY on
the lineage copy; writes one scratch SQLite file. Per save (rows already in the store: as (B), the same data and order):
the statements' seconds, the commit, the sleep. At the end: each table's rows, pages and bytes per row (dbstat
if the build has it), lookups per call, the load read.
argv: lineage_dir db_path out_tsv cache_kib mmap_bytes [--intkeys]"""
import collections
import glob
import json
import os
import random
import sqlite3
import sys
import time

D, DB, OUT = sys.argv[1:4]
CACHE_KIB, MMAP_B = int(sys.argv[4]), int(sys.argv[5])
INT = "--intkeys" in sys.argv[6:]
assert not os.path.exists(DB), "the scratch store must not exist yet"
rows_out = []


def row(*f) -> None:
    rows_out.append("\t".join(str(x) for x in f))
    print(*f, sep="\t", flush=True)


def chain(d: str) -> list:
    gens = {}
    for f in glob.glob(os.path.join(d, "gen_*.json")):
        with open(f, "rb") as fh:
            g = json.loads(fh.read())
        gens[os.path.basename(f)[4:-5]] = g.get("parent")
        del g
    kids = {p: h for h, p in gens.items()}
    out, h = [], kids.get(None)
    while h:
        out.append(h)
        h = kids.get(h)
    assert len(out) == len(gens), (len(out), len(gens))
    return out


K = "INTEGER" if INT else "TEXT"
con = sqlite3.connect(DB)
con.execute("PRAGMA journal_mode=WAL")
con.execute("PRAGMA synchronous=NORMAL")
con.execute(f"PRAGMA cache_size=-{CACHE_KIB}")
con.execute(f"PRAGMA mmap_size={MMAP_B}")
con.execute("PRAGMA wal_autocheckpoint=0")     # no checkpoint inside a merge's commit (the reviewer 07:12 (a))
con.executescript(f"""
CREATE TABLE meta(k TEXT PRIMARY KEY, v TEXT);
CREATE TABLE sym(id INTEGER PRIMARY KEY, s TEXT UNIQUE);
CREATE TABLE asked_tally(entry {K}, role {K}, slot_class {K}, n_rows INTEGER, first_save INTEGER, last_save INTEGER,
                         PRIMARY KEY(entry, role, slot_class)) WITHOUT ROWID;
CREATE TABLE kind(entry {K}, role {K}, kind_o {K}, kind_x {K}, n INTEGER, last_seq INTEGER,
                  PRIMARY KEY(entry, role, kind_o, kind_x)) WITHOUT ROWID;
CREATE TABLE kind_dk(dk {K}, entry {K}, tgt {K}, n INTEGER, last_seq INTEGER,
                     PRIMARY KEY(dk, entry, tgt)) WITHOUT ROWID;
CREATE TABLE pair(kind_o {K}, kind_x {K}, n INTEGER, last_seq INTEGER, PRIMARY KEY(kind_o, kind_x)) WITHOUT ROWID;
""")
row("META", "intkeys", INT, "cache_kib", CACHE_KIB, "mmap", MMAP_B, "sqlite", sqlite3.sqlite_version,
    "page_size", con.execute("PRAGMA page_size").fetchone()[0])
SYM: dict = {}


def s(x: str):
    """The key as stored: the text itself, or its interned integer (new symbols inserted in the same transaction)."""
    if not INT:
        return x
    i = SYM.get(x)
    if i is None:
        i = SYM[x] = len(SYM) + 1
        con.execute("INSERT INTO sym VALUES (?,?)", (i, x))
    return i


order = chain(D)
row("KIND", "save_k", "ak_rows", "kind_rows", "dk_rows", "s_parse", "s_statements",
    "s_commit", "s_sleep", "wal_pages", "db_bytes")
sample = []
t_all = time.time()
for k, h in enumerate(order, 1):
    t0 = time.time()
    with open(os.path.join(D, f"gen_{h}.json"), "rb") as fh:
        g = json.loads(fh.read())
    aks = []
    for f in glob.glob(os.path.join(D, f"ak_{h}_*.json")):
        with open(f, "rb") as fh:
            aks.append(json.loads(fh.read())["entries"])
    t1 = time.time()
    n_ak = sum(len(es) for es in aks)
    con.execute("BEGIN")
    for es in aks:
        cnt = collections.Counter((e["key"], e["role"], e["slot"].split(".", 1)[-1]) for e in es)
        batch = sorted((s(a), s(b), s(c), n, k, k) for (a, b, c), n in cnt.items())
        con.executemany("INSERT INTO asked_tally VALUES (?,?,?,?,?,?) ON CONFLICT DO UPDATE SET "
                        "n_rows = n_rows + excluded.n_rows, last_save = excluded.last_save", batch)
        if len(sample) < 20000:
            sample += random.Random(k).sample([r[:3] for r in batch], min(2000, len(batch)))
    kn, kl, dk = g.get("kinds_landed_n", ()), g.get("kinds_last", ()), g.get("kinds_landed_dk", ())
    kb = sorted((s(e[0]), s(e[1]), s(json.dumps(e[2])), s(json.dumps(e[3])), e[4]) for e in kn)
    con.executemany("INSERT INTO kind VALUES (?,?,?,?,?,0) ON CONFLICT DO UPDATE SET n = n + excluded.n", kb)
    con.executemany("UPDATE kind SET last_seq = max(last_seq, ?) WHERE entry=? AND role=? AND kind_o=? AND kind_x=?",
                    sorted((e[7], s(e[0]), s(e[1]), s(json.dumps(e[2])), s(json.dumps(e[3]))) for e in kl))
    con.executemany("INSERT INTO kind_dk VALUES (?,?,?,?,0) ON CONFLICT DO UPDATE SET n = n + excluded.n",
                    sorted((s(json.dumps(e[0])), s(e[1]), s(json.dumps(e[2])), e[3]) for e in dk))
    con.executemany("INSERT INTO pair VALUES (?,?,?,0) ON CONFLICT DO UPDATE SET n = n + excluded.n",
                    sorted((s(json.dumps(e[2])), s(json.dumps(e[3])), e[4]) for e in kn))
    con.executemany("UPDATE pair SET last_seq = max(last_seq, ?) WHERE kind_o=? AND kind_x=?",
                    sorted((e[7], s(json.dumps(e[2])), s(json.dumps(e[3]))) for e in kl))
    con.execute("INSERT OR REPLACE INTO meta VALUES ('last_merged', ?)", (h,))
    t2 = time.time()
    con.execute("COMMIT")
    t3 = time.time()
    wal = os.path.getsize(DB + "-wal") if os.path.exists(DB + "-wal") else 0
    con.execute("PRAGMA wal_checkpoint(TRUNCATE)")     # the "sleep", timed apart (off the play path in the design)
    t4 = time.time()
    row("MERGE", k, n_ak, len(kn), len(dk), round(t1 - t0, 2), round(t2 - t1, 2),
        round(t3 - t2, 3), round(t4 - t3, 2), wal // 4120, os.path.getsize(DB))
    del g, aks, kn, kl, dk
counts = {t: con.execute(f"SELECT count(*) FROM {t}").fetchone()[0] for t in ("asked_tally", "kind", "kind_dk", "pair")}
row("TOTAL_S", round(time.time() - t_all, 1), "counts", json.dumps(counts), "symbols", len(SYM))
try:
    for name, n_pages, n_bytes in con.execute("SELECT name, count(*), sum(pgsize) FROM dbstat GROUP BY name"):
        n = counts.get(name) or (len(SYM) if name == "sym" else None)
        row("TABLE_PAGES", name, n_pages, n_bytes, n, round(n_bytes / n, 1) if n else "")
except sqlite3.OperationalError as e:
    row("TABLE_PAGES", "dbstat unavailable", str(e))
pres = random.Random(99).sample(sample, min(20000, len(sample)))
t5 = time.perf_counter()
hit = sum(1 for q in pres if con.execute(
    "SELECT 1 FROM asked_tally WHERE entry=? AND role=? AND slot_class=?", q).fetchone())
row("LOOKUP", "present", len(pres), hit, round((time.perf_counter() - t5) / len(pres) * 1e6, 2))
con.close()
t6 = time.perf_counter()
c2 = sqlite3.connect(DB)
pairs = c2.execute("SELECT kind_o, kind_x, n, last_seq FROM pair").fetchall()
meta = dict(c2.execute("SELECT k, v FROM meta").fetchall())
syms = c2.execute("SELECT count(*) FROM sym").fetchone()[0]
row("LOAD", "pairs", len(pairs), "meta", meta.get("last_merged"), "symbols", syms,
    "s", round(time.perf_counter() - t6, 3))
c2.close()
row("DB_BYTES", os.path.getsize(DB))
with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(rows_out) + "\n")
