"""(iv) corrected: the dk ids taken from kind_dk itself (not detected by shape), decoded through sym, grouped by dk[0];
the largest cluster's rows fetched by dk IN (...) on mem4i, and by the cluster in mem3 (B), timed. argv: bench_dir"""
import collections
import json
import os
import sqlite3
import sys
import time

B = sys.argv[1]
ci = sqlite3.connect(os.path.join(B, "mem4i.db"))
ci.execute("PRAGMA cache_size=-262144")
ci.execute("PRAGMA mmap_size=1073741824")
sym = dict(ci.execute("SELECT id, s FROM sym"))
dk_rows = collections.Counter(dict(ci.execute("SELECT dk, count(*) FROM kind_dk GROUP BY dk")))
clusters: dict = collections.defaultdict(list)
for i in dk_rows:
    clusters[json.loads(sym[i])[0]].append(i)
sizes = sorted(((sum(dk_rows[i] for i in ids), c, len(ids)) for c, ids in clusters.items()), reverse=True)
print("CLUSTERS", len(clusters), "dk ids", len(dk_rows), "top", sizes[:5], sep="\t", flush=True)
n_big, big, _ = sizes[0]
ids = clusters[big]
for run in ("first", "second"):
    t0 = time.perf_counter()
    n = len(ci.execute(f"SELECT dk, entry, tgt, n FROM kind_dk WHERE dk IN ({','.join('?' * len(ids))})",
                       ids).fetchall())
    print("IV_INT", run, big, f"dk ids {len(ids)}", f"rows {n}", f"s {time.perf_counter() - t0:.4f}", sep="\t",
          flush=True)
c3 = sqlite3.connect(os.path.join(B, "mem3.db"))
c3.execute("PRAGMA cache_size=-262144")
t0 = time.perf_counter()
n3 = len(c3.execute("SELECT dk, entry, tgt, n FROM kind_dk WHERE cluster=?", (json.dumps(big),)).fetchall())
print("IV_B_CLUSTER_INDEX", big, f"rows {n3}", f"s {time.perf_counter() - t0:.4f}", sep="\t", flush=True)
