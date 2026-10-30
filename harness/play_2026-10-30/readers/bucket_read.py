"""The (C) bucket read (the reviewer 2026-10-20 23:24 item 2): the carried kind_dk rows by delta kind, by its type
(dk[0]) and by (type, sign), from the restore point's copy (immutable: nothing written). argv: memory.db"""
import collections
import json
import sqlite3
import sys

c = sqlite3.connect("file:" + sys.argv[1] + "?mode=ro&immutable=1", uri=True)
print(c.execute("select sql from sqlite_master where name='sym'").fetchone()[0])
cols = [r[1] for r in c.execute("pragma table_info(sym)")]
print("sym cols", cols, c.execute("select * from sym limit 2").fetchall())
ids = collections.Counter(dict(c.execute("select dk, count(*) from kind_dk group by dk")))
idcol, valcol = cols[0], cols[1]
sym = {i: v for i, v in c.execute(f"select {idcol}, {valcol} from sym where {idcol} in "
                                   f"({','.join(map(str, ids))})")}
def dec(v):
    try:
        return tuple(json.loads(v))
    except Exception:
        return (v,)
by_dk = {dec(sym[i]): n for i, n in ids.items()}
tot = sum(by_dk.values())
by_t, by_ts = collections.Counter(), collections.Counter()
for d, n in by_dk.items():
    by_t[d[0]] += n
    by_ts[d[:2]] += n
print(f"kind_dk rows {tot}; distinct delta kinds {len(by_dk)}; types {len(by_t)}; (type, sign) {len(by_ts)}")
print("by type:", by_t.most_common())
print("by (type, sign):", by_ts.most_common())
print("largest exact kinds:", sorted(by_dk.items(), key=lambda kv: -kv[1])[:12])
print("exact-kind sizes: max", max(by_dk.values()), "median", sorted(by_dk.values())[len(by_dk) // 2])
