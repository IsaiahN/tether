"""(C)'s EQUALITY CHECK AND BYTES PER ROW (the reviewer 2026-10-19 07:21 items 2-3). READ ONLY on two finished stores.
1. EVERY row of asked_tally, kind, kind_dk and pair in the text-key store against the integer-key store with each id
   decoded through sym: rows identical / rows compared, per table, both directions.
2. ABSENT keys: for each table, 2,000 keys drawn by random.Random(20261019) from the text store with the first key field
   suffixed "#absent" (a string no row holds); each looked up in both stores (the integer store through sym, where an
   absent string has no id): both must say "absent".
3. Bytes per row, an ESTIMATE (dbstat is not compiled into this SQLite build): the average record payload per table, a
   text column counted as its UTF-8 length and an integer as SQLite's stored width (0-8 bytes by magnitude); page and
   B-tree overhead not included.
argv: text_db int_db"""
import random
import sqlite3
import sys

TDB, IDB = sys.argv[1:3]
KEYS = {"asked_tally": ["entry", "role", "slot_class"], "kind": ["entry", "role", "kind_o", "kind_x"],
        "kind_dk": ["dk", "entry", "tgt"], "pair": ["kind_o", "kind_x"]}
ct, ci = sqlite3.connect(TDB), sqlite3.connect(IDB)
sym = dict(ci.execute("SELECT id, s FROM sym"))
rev = {s: i for i, s in sym.items()}
print("SYMBOLS", len(sym), sep="\t", flush=True)


def width(v) -> int:
    if isinstance(v, str):
        return len(v.encode("utf-8"))
    if v is None:
        return 0
    a = abs(int(v))
    for w, lim in ((0, 2), (1, 2 ** 7), (2, 2 ** 15), (3, 2 ** 23), (4, 2 ** 31), (6, 2 ** 47)):
        if a < lim:
            return w
    return 8


for t, keys in KEYS.items():
    cols = [r[1] for r in ct.execute(f"PRAGMA table_info({t})")]
    nk = len(keys)
    rows_t = {r[:nk]: r[nk:] for r in ct.execute(f"SELECT {', '.join(cols)} FROM {t}")}
    rows_i = {tuple(sym[x] for x in r[:nk]): r[nk:] for r in ci.execute(f"SELECT {', '.join(cols)} FROM {t}")}
    same = sum(1 for k, v in rows_t.items() if rows_i.get(k) == v)
    print("EQUAL", t, f"text->int {same}/{len(rows_t)}", f"int rows {len(rows_i)}",
          f"int->text {sum(1 for k, v in rows_i.items() if rows_t.get(k) == v)}/{len(rows_i)}", sep="\t", flush=True)
    rng = random.Random(20261019)
    sample = rng.sample(sorted(rows_t), min(2000, len(rows_t)))
    absent = [(k[0] + "#absent",) + k[1:] for k in sample]
    where = " AND ".join(f"{c}=?" for c in keys)
    a_t = sum(1 for k in absent if ct.execute(f"SELECT 1 FROM {t} WHERE {where}", k).fetchone() is None)
    a_i = sum(1 for k in absent if any(x not in rev for x in k) or ci.execute(
        f"SELECT 1 FROM {t} WHERE {where}", tuple(rev[x] for x in k)).fetchone() is None)
    print("ABSENT", t, f"text says absent {a_t}/{len(absent)}", f"int says absent {a_i}/{len(absent)}", sep="\t",
          flush=True)
    pt = sum(sum(width(x) for x in k) + sum(width(x) for x in v) for k, v in rows_t.items()) / max(1, len(rows_t))
    pi = sum(sum(width(x) for x in k) + sum(width(x) for x in v) for k, v in
             ((tuple(rev[x] for x in k), v) for k, v in rows_t.items())) / max(1, len(rows_t))
    print("PAYLOAD_EST", t, f"text {pt:.1f} B/row", f"int {pi:.1f} B/row", sep="\t", flush=True)
    del rows_t, rows_i
