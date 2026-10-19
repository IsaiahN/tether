"""S1/S2: the migration = lineage_store.catch_up from an empty store, on a lineage COPY; then the sleep and
the cheap header check, each timed. argv: repo lineage_copy"""
import os
import sys
import time

sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])
import lineage_store as ls  # noqa: E402

d = sys.argv[2]
assert not os.path.exists(os.path.join(d, ls.DB)), "a store already exists in this copy"
t0 = time.perf_counter()
con = ls.open_store(d)
rows = ls.catch_up(con, d)
t1 = time.perf_counter()
for r in rows:
    print("MERGE", r["k"], r["save"], r["s_read"], r["s_statements"], r["s_commit"], sep="\t", flush=True)
sl = ls.sleep(con)
con.close()
t2 = time.perf_counter()
ok = ls.header_ok(d)
t3 = time.perf_counter()
print("TOTAL_MERGE_S", round(t1 - t0, 1), "SLEEP", sl, "HEADER", ok, round(t3 - t2, 4),
      "DB_BYTES", os.path.getsize(os.path.join(d, ls.DB)), sep="\t", flush=True)
