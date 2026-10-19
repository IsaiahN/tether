"""THE STORE'S SPLIT IN BYTES (the reviewer 2026-10-19 07:57 item 5 iii; this SQLite build has no dbstat). The source
memory.db is opened READ ONLY. Each table, with its own CREATE statement and any index on it, is copied ALONE into a
fresh scratch database (page size as the source), the scratch file is VACUUMed, and its size less an empty database's
is that table's bytes. The scratch files are removed after each reading; the source is never written.
argv: memory_db scratch_dir"""
import os
import sqlite3
import sys

DB, OUT = sys.argv[1:3]
os.makedirs(OUT, exist_ok=True)
src = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
page = src.execute("PRAGMA page_size").fetchone()[0]
objs = src.execute("SELECT type, name, tbl_name, sql FROM sqlite_master WHERE sql IS NOT NULL").fetchall()
tables = [(n, s) for t, n, _tb, s in objs if t == "table"]
src.close()


def size_of(name: str | None, create: str | None, idx: list) -> int:
    f = os.path.join(OUT, "one.db")
    if os.path.exists(f):
        os.remove(f)
    c = sqlite3.connect(f"file:{f}", uri=True)
    c.execute(f"PRAGMA page_size={page}")
    if name:
        c.execute(create)
        for s in idx:
            c.execute(s)
        c.execute("ATTACH ? AS s", (f"file:{DB}?mode=ro",))
        c.execute(f"INSERT INTO main.{name} SELECT * FROM s.{name}")
        c.commit()
        c.execute("DETACH s")
    c.execute("VACUUM")
    c.close()
    n = os.path.getsize(f)
    os.remove(f)
    return n


base = size_of(None, None, [])
tot = 0
for name, create in tables:
    idx = [s for t, _n, tb, s in objs if t == "index" and tb == name]
    b = size_of(name, create, idx) - base
    tot += b
    print("III_BYTES", name, f"bytes {b}", f"indexes {len(idx)}", sep="\t", flush=True)
print("III_TOTAL", f"bytes {tot}", f"source file {os.path.getsize(DB)}", f"empty db {base}", sep="\t", flush=True)
