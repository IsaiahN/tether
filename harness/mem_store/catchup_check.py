"""S4's CATCH_UP vs INCREMENTAL CHECK (the reviewer 2026-10-19 08:26 item 3, the added refuter). The incremental
store is the one a run built (its migration plus write()'s merge of the run's save). A second store is built by
catch_up alone from the SAME archive: every *.json of the lineage folder hard-linked (never copied, never written)
into an empty scratch folder, then lineage_store.open_store + catch_up there. The incremental store is opened READ
ONLY. asked_tally is compared decoded through each store's own sym table, on keys, n_variants, n_asked, n_landed,
first_save, last_save, n_saves_asked, N/N; also meta n_variants_frozen_from, saves, and ak_whole.
argv: repo lineage_dir scratch_dir"""
import os
import sqlite3
import sys

REPO, LIN, OUT = sys.argv[1:4]
sys.path = [p for p in sys.path if "scratchpad" not in p]
sys.path.insert(0, REPO)
import lineage_store as ls  # noqa: E402

assert not os.path.exists(OUT), "the scratch folder must not exist"
os.makedirs(OUT)
n = 0
for f in sorted(os.listdir(LIN)):
    if f.endswith(".json"):
        os.link(os.path.join(LIN, f), os.path.join(OUT, f))
        n += 1
con = ls.open_store(OUT)
merged = ls.catch_up(con, OUT)
con.close()
print("BUILT", f"json linked {n}", f"saves merged {len(merged)}", sep="\t", flush=True)


def read(db):
    c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    sym = dict(c.execute("SELECT id, s FROM sym"))
    t = {(sym[a], sym[b], sym[cl]): rest for a, b, cl, *rest in c.execute(
        "SELECT entry, role, slot_class, n_variants, n_asked, n_landed, first_save, last_save, n_saves_asked "
        "FROM asked_tally")}
    meta = dict(c.execute("SELECT k, v FROM meta"))
    saves = sorted(c.execute("SELECT h, k, parent FROM saves"))
    whole = sorted(c.execute("SELECT * FROM ak_whole"))
    c.close()
    return t, meta, saves, whole


ti, mi, si, wi = read(os.path.join(LIN, ls.DB))
tc, mc, sc, wc = read(os.path.join(OUT, ls.DB))
same = sum(1 for k in ti if tc.get(k) == ti[k])
print("ASKED_TALLY", f"incremental {len(ti)}", f"catch_up {len(tc)}", f"identical {same}",
      f"keys only incremental {len(set(ti) - set(tc))}", f"keys only catch_up {len(set(tc) - set(ti))}", sep="\t")
for k in sorted((k for k in ti if tc.get(k) != ti[k]), key=repr)[:10]:
    print("DIFF", k, ti[k], tc.get(k), sep="\t")
print("SUMS (n_variants, n_asked, n_saves_asked)", [sum(v[i] for v in ti.values()) for i in (0, 1, 5)],
      [sum(v[i] for v in tc.values()) for i in (0, 1, 5)], sep="\t")
print("META", mi, mc, f"equal {mi == mc}", sep="\t")
print("SAVES", f"equal {si == sc}", len(si), len(sc), sep="\t")
print("AK_WHOLE", f"equal {wi == wc}", len(wi), len(wc), sep="\t")
