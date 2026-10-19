"""FOLLOW-UP (V4-V6): the auto-checkpoint and mmap, plans and row counts skipped.
WHY A SMALL LATE MERGE IS SLOW (Isaiah 2026-10-19 07:05; the reviewer 07:06 items 1, 2, 4, 7). On COPIES of (B)'s
finished store (bench/mem3.db, 18 saves merged): (1) EXPLAIN QUERY PLAN for every merge statement and the load reads;
(2) memory save 13's delta (3,947 ask rows, 7,977 kind rows, 8,033 dk rows) merged again, statement by statement,
with the COMMIT and the WAL bytes it wrote timed apart, under three variants, each on its own fresh copy:
  V1 as (B): unsorted batches, synchronous NORMAL;   V2 each batch SORTED by its primary key, synchronous NORMAL;
  V3 sorted, synchronous OFF (to see what the fsync costs; not a proposal).
Every row of the re-merge is already in the store, so every upsert takes the ON CONFLICT path (stated, not hidden).
argv: lineage_dir store_db work_dir"""
import collections
import json
import os
import shutil
import sqlite3
import sys
import time

D, SRC, W = sys.argv[1:4]
H = "faa69c6a4e5c7e2a"     # memory save 13
CACHE_KIB, MMAP_B = 262144, 1073741824
STMT = {
    "asked_tally": "INSERT INTO asked_tally VALUES (?,?,?,?,?,?) ON CONFLICT DO UPDATE SET "
                   "n_rows = n_rows + excluded.n_rows, last_save = excluded.last_save",
    "kind": "INSERT INTO kind VALUES (?,?,?,?,?,0) ON CONFLICT DO UPDATE SET n = n + excluded.n",
    "kind_last": "UPDATE kind SET last_seq = max(last_seq, ?) WHERE entry=? AND role=? AND kind_o=? AND kind_x=?",
    "kind_dk": "INSERT INTO kind_dk VALUES (?,?,?,?,?,0) ON CONFLICT DO UPDATE SET n = n + excluded.n",
    "pair": "INSERT INTO pair VALUES (?,?,?,0) ON CONFLICT DO UPDATE SET n = n + excluded.n",
    "pair_last": "UPDATE pair SET last_seq = max(last_seq, ?) WHERE kind_o=? AND kind_x=?",
    "meta": "INSERT OR REPLACE INTO meta VALUES ('last_merged', ?)",
}
LOADS = {"load_pairs": "SELECT kind_o, kind_x, n, last_seq FROM pair",
         "load_meta": "SELECT v FROM meta WHERE k='last_merged'",
         "load_maxseq": "SELECT max(last_seq) FROM kind",
         "dk_cluster": "SELECT dk, entry, tgt, n FROM kind_dk WHERE cluster=?",
         "count_tally": "SELECT count(*) FROM asked_tally"}

with open(os.path.join(D, f"gen_{H}.json"), "rb") as fh:
    g = json.loads(fh.read())
ak = [f for f in os.listdir(D) if f.startswith(f"ak_{H}_")]
with open(os.path.join(D, ak[0]), "rb") as fh:
    es = json.loads(fh.read())["entries"]
cnt = collections.Counter((e["key"], e["role"], e["slot"].split(".", 1)[-1]) for e in es)
kn, kl, dk = g.get("kinds_landed_n", ()), g.get("kinds_last", ()), g.get("kinds_landed_dk", ())
BATCH = {
    "asked_tally": [(a, b, c, n, 13, 13) for (a, b, c), n in cnt.items()],
    "kind": [(e[0], e[1], json.dumps(e[2]), json.dumps(e[3]), e[4]) for e in kn],
    "kind_last": [(e[7], e[0], e[1], json.dumps(e[2]), json.dumps(e[3])) for e in kl],
    "kind_dk": [(json.dumps(e[0][0]), json.dumps(e[0]), e[1], json.dumps(e[2]), e[3]) for e in dk],
    "pair": [(json.dumps(e[2]), json.dumps(e[3]), e[4]) for e in kn],
    "pair_last": [(e[7], json.dumps(e[2]), json.dumps(e[3])) for e in kl],
    "meta": [(H,)],
}
SORTKEY = {"asked_tally": lambda r: r[:3], "kind": lambda r: r[:4], "kind_last": lambda r: r[1:],
           "kind_dk": lambda r: r[1:4], "pair": lambda r: r[:2], "pair_last": lambda r: r[1:], "meta": lambda r: r}
print("BATCH", *[f"{k}={len(v)}" for k, v in BATCH.items()], sep="\t", flush=True)

con = sqlite3.connect(SRC)
for name, sql in ():
    plan = con.execute("EXPLAIN QUERY PLAN " + sql, tuple([None] * sql.count("?"))).fetchall()
    print("PLAN", name, " | ".join(r[-1] for r in plan) or "(no table access: a direct insert)", sep="\t", flush=True)
for t in ("asked_tally", "kind", "kind_dk", "pair"):
    n = con.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
    print("ROWS", t, n, sep="\t", flush=True)
con.close()

for vname, sort, sync, autock, mmap in (("V4", True, "NORMAL", 0, MMAP_B), ("V5", True, "NORMAL", 0, 0),
                                       ("V6", True, "NORMAL", 1000, 0)):
    db = os.path.join(W, f"probe_{vname}.db")
    for ext in ("", "-wal", "-shm"):
        if os.path.exists(db + ext):
            os.remove(db + ext)
    shutil.copyfile(SRC, db)
    c = sqlite3.connect(db)
    c.execute("PRAGMA journal_mode=WAL")
    c.execute(f"PRAGMA synchronous={sync}")
    c.execute(f"PRAGMA cache_size=-{CACHE_KIB}")
    c.execute(f"PRAGMA mmap_size={mmap}")
    c.execute(f"PRAGMA wal_autocheckpoint={autock}")
    times = {}
    c.execute("BEGIN")
    for name, sql in STMT.items():
        rows = sorted(BATCH[name], key=SORTKEY[name]) if sort else BATCH[name]
        t0 = time.perf_counter()
        c.executemany(sql, rows)
        times[name] = round(time.perf_counter() - t0, 3)
    t0 = time.perf_counter()
    c.execute("COMMIT")
    t_commit = round(time.perf_counter() - t0, 3)
    wal = os.path.getsize(db + "-wal") if os.path.exists(db + "-wal") else 0
    t0 = time.perf_counter()
    c.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    t_ckpt = round(time.perf_counter() - t0, 3)
    c.close()
    print("VARIANT", vname, f"sorted={sort}", f"sync={sync}", f"autocheckpoint={autock}", f"mmap={mmap}",
          *[f"{k}={v}" for k, v in times.items()],
          f"commit={t_commit}", f"wal_bytes={wal}", f"wal_pages={wal // 4120}", f"checkpoint={t_ckpt}",
          sep="\t", flush=True)
