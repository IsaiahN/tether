"""THE FOUR CHECKS (the reviewer 2026-10-19 07:26 item 2). READ ONLY on the finished stores mem4t.db (text keys),
mem4i.db (integer keys) and mem3.db ((B)); one scratch copy for (iii).
(i) lookup cost WITH the encode: 20,000 held asked_tally keys asked by their strings, each encoded through the sym dict
    then looked up; the encode timed alone too.
(ii) ABSENT COMBINATIONS: per table, keys built by recombining fields of held keys (random.Random(20261019)), kept only
    when held in NEITHER store and every symbol IS known; 2,000 per table (fewer if the space runs out, said); looked
    up in both stores: N/N absent.
(iii) the 293.5 vs 365 MB text-file gap: (B)'s kind_dk carries a cluster column and its index, (C) does not. Measured
    by VACUUM INTO of a copy of mem3.db with and without that index dropped.
(iv) the dk family on the integer store: the largest cluster (by dk[0]) found through sym, its rows fetched by
    dk IN (its dk ids), timed (cold and warm); the same in mem4t by the equivalent query.
argv: bench_dir"""
import json
import os
import random
import sqlite3
import sys
import time

B = sys.argv[1]
ct, ci = sqlite3.connect(os.path.join(B, "mem4t.db")), sqlite3.connect(os.path.join(B, "mem4i.db"))
for c in (ct, ci):
    c.execute("PRAGMA cache_size=-262144")
    c.execute("PRAGMA mmap_size=1073741824")
sym = dict(ci.execute("SELECT id, s FROM sym"))
rev = {s: i for i, s in sym.items()}
KEYS = {"asked_tally": ["entry", "role", "slot_class"], "kind": ["entry", "role", "kind_o", "kind_x"],
        "kind_dk": ["dk", "entry", "tgt"], "pair": ["kind_o", "kind_x"]}

# (i)
held = ct.execute("SELECT entry, role, slot_class FROM asked_tally").fetchall()
q = random.Random(20261019).sample(held, 20000)
t0 = time.perf_counter()
enc = [(rev[a], rev[b], rev[c]) for a, b, c in q]
t_enc = (time.perf_counter() - t0) / len(q) * 1e6
t0 = time.perf_counter()
hit = sum(1 for k in q if ci.execute("SELECT 1 FROM asked_tally WHERE entry=? AND role=? AND slot_class=?",
                                     (rev[k[0]], rev[k[1]], rev[k[2]])).fetchone())
t_int = (time.perf_counter() - t0) / len(q) * 1e6
t0 = time.perf_counter()
hit_t = sum(1 for k in q if ct.execute("SELECT 1 FROM asked_tally WHERE entry=? AND role=? AND slot_class=?",
                                       k).fetchone())
t_txt = (time.perf_counter() - t0) / len(q) * 1e6
print("I_LOOKUP", f"encode alone {t_enc:.2f} us", f"int store with encode {t_int:.2f} us ({hit}/{len(q)} hit)",
      f"text store {t_txt:.2f} us ({hit_t}/{len(q)} hit)", sep="\t", flush=True)
del enc

# (ii)
for t, keys in KEYS.items():
    rows = ct.execute(f"SELECT {', '.join(keys)} FROM {t}").fetchall()
    have = set(rows)
    cols = [sorted({r[j] for r in rows}) for j in range(len(keys))]
    rng = random.Random(20261019)
    combos, tries = set(), 0
    while len(combos) < 2000 and tries < 200000:
        tries += 1
        k = tuple(rng.choice(cols[j]) for j in range(len(keys)))
        if k not in have:
            combos.add(k)
    where = " AND ".join(f"{c}=?" for c in keys)
    a_t = sum(1 for k in combos if ct.execute(f"SELECT 1 FROM {t} WHERE {where}", k).fetchone() is None)
    known = sum(1 for k in combos if all(x in rev for x in k))
    a_i = sum(1 for k in combos if ci.execute(f"SELECT 1 FROM {t} WHERE {where}",
                                               tuple(rev[x] for x in k)).fetchone() is None)
    print("II_ABSENT_COMBO", t, f"drawn {len(combos)} in {tries} tries", f"all symbols known {known}/{len(combos)}",
          f"text absent {a_t}/{len(combos)}", f"int absent {a_i}/{len(combos)}", sep="\t", flush=True)
    del rows, have, cols

# (iii)
c3 = sqlite3.connect(os.path.join(B, "mem3.db"))
size3 = os.path.getsize(os.path.join(B, "mem3.db"))
objs = c3.execute("SELECT type, name, tbl_name FROM sqlite_master ORDER BY name").fetchall()
c3.close()
for tag in ("asis", "noindex"):
    out = os.path.join(B, f"mem3_vacuum_{tag}.db")
    if os.path.exists(out):
        os.remove(out)
    src = os.path.join(B, "mem3_tmp.db")
    with open(os.path.join(B, "mem3.db"), "rb") as fi, open(src, "wb") as fo:
        fo.write(fi.read())
    c = sqlite3.connect(src)
    if tag == "noindex":
        c.execute("DROP INDEX kind_dk_cluster")
    c.execute("VACUUM INTO ?", (out,))
    c.close()
    os.remove(src)
    print("III_SIZE", tag, os.path.getsize(out), sep="\t", flush=True)
print("III_OBJECTS_mem3", json.dumps(objs), "file", size3, "mem4t file", os.path.getsize(os.path.join(B, "mem4t.db")),
      sep="\t", flush=True)

# (iv)
by_cluster: dict = {}
for i, s in sym.items():
    if s.startswith("["):
        try:
            d = json.loads(s)
        except ValueError:
            continue
        if isinstance(d, list) and len(d) == 3 and isinstance(d[0], str) and d[1] in ("+", "-", "0"):
            by_cluster.setdefault(d[0], []).append(i)
dk_ids = {r[0] for r in ci.execute("SELECT DISTINCT dk FROM kind_dk")}
by_cluster = {c: [i for i in ids if i in dk_ids] for c, ids in by_cluster.items()}
big = max(by_cluster, key=lambda c: ci.execute(
    f"SELECT count(*) FROM kind_dk WHERE dk IN ({','.join('?' * len(by_cluster[c]))})", by_cluster[c]).fetchone()[0])
ids = by_cluster[big]
for run in ("first", "second"):
    t0 = time.perf_counter()
    n = len(ci.execute(f"SELECT dk, entry, tgt, n FROM kind_dk WHERE dk IN ({','.join('?' * len(ids))})",
                       ids).fetchall())
    print("IV_DK_CLUSTER_INT", run, f"cluster {big!r}", f"dk ids {len(ids)}", f"rows {n}",
          f"s {time.perf_counter() - t0:.4f}", sep="\t", flush=True)
plan = ci.execute(f"EXPLAIN QUERY PLAN SELECT dk, entry, tgt, n FROM kind_dk WHERE dk IN "
                  f"({','.join('?' * len(ids))})", ids).fetchall()
print("IV_PLAN", " | ".join(r[-1] for r in plan), sep="\t", flush=True)
names = [sym[i] for i in ids]
t0 = time.perf_counter()
n = len(ct.execute(f"SELECT dk, entry, tgt, n FROM kind_dk WHERE dk IN ({','.join('?' * len(names))})",
                   names).fetchall())
print("IV_DK_CLUSTER_TEXT", f"rows {n}", f"s {time.perf_counter() - t0:.4f}", sep="\t", flush=True)
