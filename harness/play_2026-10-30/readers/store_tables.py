"""Read-only: each table's row count in a lineage BACKUP's memory.db, opened immutable=1 (never the live store).
argv: the backup folder."""
import sqlite3
import sys

sys.dont_write_bytecode = True
db = f"file:{sys.argv[1]}/memory.db?mode=ro&immutable=1"
con = sqlite3.connect(db, uri=True)
tabs = [r[0] for r in con.execute("select name from sqlite_master where type='table' order by name")]
for t in tabs:
    n = con.execute(f'select count(*) from "{t}"').fetchone()[0]
    cols = [r[1] for r in con.execute(f'pragma table_info("{t}")')]
    print(f"{t}\t{n}\t{','.join(cols)[:160]}")
con.close()
