import sqlite3
import sys

uri = "file:" + sys.argv[1] + "?mode=ro&immutable=1"   # immutable: no -shm / -wal is ever written
con = sqlite3.connect(uri, uri=True)
tabs = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")]
for t in tabs:
    n = con.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
    print(f"{t:14s} {n:>12,d}")
try:
    rows = con.execute("SELECT name, SUM(pgsize) FROM dbstat GROUP BY name ORDER BY 2 DESC").fetchall()
    print("bytes by table/index (dbstat):")
    for a, b in rows[:15]:
        print(f"  {a:30s} {b / 1e6:8.1f} MB")
except Exception as e:  # noqa: BLE001
    print("dbstat unavailable:", e)
