"""THE STORE'S SPLIT (the reviewer 2026-10-19 07:57 item 5 ii/iii). READ ONLY (uri mode=ro) on a finished memory.db.
(iii) per table and index: pages and bytes from dbstat (falls back to row count x average payload if dbstat is absent).
(ii) the blobs: each blob row's bytes, and the fold blob's parts (rows, vindication, evidence, book, invented) each as
its json length and its item count -- the parts that grow with every save versus with the library.
argv: memory_db"""
import json
import sqlite3
import sys

DB = sys.argv[1]
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
try:
    rows = con.execute("SELECT name, count(*), sum(pgsize), sum(payload) FROM dbstat GROUP BY name "
                       "ORDER BY sum(pgsize) DESC").fetchall()
    tot = sum(r[2] for r in rows)
    for name, pages, size, payload in rows:
        print("III_DBSTAT", name, f"pages {pages}", f"bytes {size}", f"payload {payload}",
              f"share {size / tot:.3f}", sep="\t")
    print("III_DBSTAT_TOTAL", f"bytes {tot}", sep="\t")
except sqlite3.OperationalError as e:
    print("III_NO_DBSTAT", e, sep="\t")
    for (t,) in con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall():
        print("III_ROWS", t, con.execute(f"SELECT count(*) FROM {t}").fetchone()[0], sep="\t")
for k, v in con.execute("SELECT k, v FROM blob ORDER BY k"):
    print("II_BLOB", k, f"bytes {len(v)}", sep="\t")
    d = json.loads(v)
    for part, x in sorted(d.items()):
        print("II_PART", k, part, f"json_bytes {len(json.dumps(x))}",
              f"items {len(x) if hasattr(x, '__len__') else 'scalar'}", sep="\t")
print("II_SAVES", con.execute("SELECT count(*) FROM saves").fetchone()[0], sep="\t")
