"""A STORE BUILT BY catch_up ALONE, timed per save (the reviewer 2026-10-19 10:27 item 3: the merge fix's cost). Every
*.json of a lineage copy hard-linked (never copied, never written) into an empty scratch folder, then REPO's
lineage_store.open_store + catch_up; each save's merge phases (s_read, s_statements, s_commit) printed with its kind
rows touched (kinds_landed + kinds_landed_n + kinds_last of that save). Run once with each tree's lineage_store.
argv: repo lineage_copy out_dir"""
import json
import os
import sys
import time

REPO, LIN, OUT = sys.argv[1:4]
sys.path = [p for p in sys.path if "scratchpad" not in p]
sys.path.insert(0, REPO)
import lineage_store as ls  # noqa: E402

print("LINEAGE_STORE", ls.__file__, flush=True)
assert not os.path.exists(OUT), "the scratch folder must not exist"
os.makedirs(OUT)
for f in sorted(os.listdir(LIN)):
    if f.endswith(".json"):
        os.link(os.path.join(LIN, f), os.path.join(OUT, f))
con = ls.open_store(OUT)
t0 = time.perf_counter()
out = ls.catch_up(con, OUT)
wall = time.perf_counter() - t0
con.close()
tot = {"s_read": 0.0, "s_statements": 0.0, "s_commit": 0.0}
for r in out:
    with open(os.path.join(OUT, f"gen_{r['save']}.json"), encoding="utf-8") as fh:
        g = json.load(fh)
    touched = sum(len(g.get(k, ())) for k in ("kinds_landed", "kinds_landed_n", "kinds_last"))
    del g
    for k in tot:
        tot[k] += r[k]
    print("SAVE", r["k"], r["save"], f"touched {touched}", f"s_read {r['s_read']}",
          f"s_statements {r['s_statements']}", f"s_commit {r['s_commit']}", sep="\t", flush=True)
print("TOTAL", f"saves {len(out)}", f"wall {wall:.1f}", json.dumps({k: round(v, 3) for k, v in tot.items()}),
      sep="\t", flush=True)
