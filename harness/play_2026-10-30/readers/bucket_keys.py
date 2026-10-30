"""(C) sizing: distinct entries per exact delta kind and per type, and rows per exact kind (immutable read of the point)."""
import collections
import json
import sqlite3
import sys

c = sqlite3.connect("file:" + sys.argv[1] + "?mode=ro&immutable=1", uri=True)
sym = dict(c.execute("select id, s from sym"))
rows = c.execute("select dk, entry, tgt, n from kind_dk").fetchall()
dk_of = {i: tuple(json.loads(sym[i])) for i in {r[0] for r in rows}}
per_dk_entries = collections.defaultdict(set)
per_t_entries = collections.defaultdict(set)
per_dk_rows = collections.Counter()
zero = 0
for d, e, t, n in rows:
    k = dk_of[d]
    per_dk_entries[k].add(e)
    per_t_entries[k[0]].add(e)
    per_dk_rows[k] += 1
    zero += n <= 0
print("rows", len(rows), "rows with n<=0", zero, "library-ish distinct entries", len({r[1] for r in rows}))
print("distinct (dk, entry):", sum(len(v) for v in per_dk_entries.values()), "| distinct (type, entry):",
      sum(len(v) for v in per_t_entries.values()))
print("per type distinct entries:", {t: len(v) for t, v in sorted(per_t_entries.items())})
print("per exact kind rows max", max(per_dk_rows.values()), "| distinct entries per exact kind max",
      max(len(v) for v in per_dk_entries.values()))
