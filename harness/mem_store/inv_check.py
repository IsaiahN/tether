"""THE PAIR TABLE'S INVARIANT, checked (the seat 10:26). READ ONLY on one store, and optionally a second to compare.
(1) The invariant: for every pair, pair.n = SUM over its kind rows with in_landed = 1 of (n if has_n else 1), and
pair.last_seq = the MAX l_seq over those rows; computed by one aggregate over the kind table (a full scan -- a TEST,
never a load) and compared N/N with the pair table, decoded through sym. (2) With a second store: the kind table and
the pair table decoded through each store's sym, compared row for row.
argv: memory_db [other_memory_db]"""
import json
import sqlite3
import sys


def read(db):
    c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    sym = dict(c.execute("SELECT id, s FROM sym"))
    pair = {(sym[o], sym[x]): (n, last) for o, x, n, last in c.execute("SELECT kind_o, kind_x, n, last_seq FROM pair")}
    agg = {(sym[o], sym[x]): (n, last) for o, x, n, last in c.execute(
        "SELECT kind_o, kind_x, SUM(CASE WHEN has_n THEN n ELSE 1 END), MAX(l_seq) FROM kind WHERE in_landed=1 "
        "GROUP BY kind_o, kind_x")}
    kind = {(sym[e], sym[r], sym[o], sym[x]): rest for e, r, o, x, *rest in c.execute(
        "SELECT entry, role, kind_o, kind_x, in_landed, n, has_n, l_game, l_level, l_cycle, l_seq FROM kind")}
    c.close()
    return pair, agg, kind


p, a, k = read(sys.argv[1])
keys = set(p) | set(a)
bad = sorted(x for x in keys if p.get(x) != a.get(x))
print("INVARIANT", sys.argv[1], f"pairs {len(p)}", f"aggregate {len(a)}", f"identical {len(keys) - len(bad)}",
      f"DIFFER {len(bad)}", sep="\t", flush=True)
for x in bad[:10]:
    print("INV_DIFF", json.dumps(x)[:200], "pair", p.get(x), "aggregate", a.get(x), sep="\t")
if len(sys.argv) > 2:
    p2, _a2, k2 = read(sys.argv[2])
    kd = sum(1 for x in set(k) | set(k2) if k.get(x) != k2.get(x))
    pd = sum(1 for x in set(p) | set(p2) if p.get(x) != p2.get(x))
    print("COMPARE", f"kind rows {len(k)} vs {len(k2)}, differ {kd}", f"pair rows {len(p)} vs {len(p2)}, differ {pd}",
          sep="\t", flush=True)
