"""SCHEMA 3's CHECKS on one store (the reviewer 2026-10-19 10:45 item 2 (b) and the measures). TESTS ONLY: full scans.
The source store is opened READ ONLY; byte measures write only scratch copies (VACUUM INTO) in a given folder.
  PAIR     pair.n / last_seq = the aggregate over kind rows with in_landed = 1 of (n if has_n else 1) / MAX(l_seq)
  FLAG     no_dk = NOT EXISTS (kind_dk row, n > 0, same entry, tgt = kind_x for a CAUSE else kind_o), every kind row
  COUNTS   in_landed=1 rows; T2 candidates (in_landed=1 AND no_dk=1); known-with-no-count (in_landed=1 AND has_n=0)
  META     kinds_known = COUNT(in_landed=1); kind_seq_max = MAX(l_seq) over rows with a last (l_game NOT NULL)
  BYTES    the store VACUUMed as is, and once per new index with that index dropped: the difference is its bytes
argv: memory_db scratch_dir"""
import os
import sqlite3
import sys

DB, OUT = sys.argv[1:3]
c = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
cause = c.execute("SELECT id FROM sym WHERE s='CAUSE'").fetchone()
cause = cause[0] if cause else -1
pair = {(o, x): (n, last) for o, x, n, last in c.execute("SELECT kind_o, kind_x, n, last_seq FROM pair")}
agg = {(o, x): (n, last) for o, x, n, last in c.execute(
    "SELECT kind_o, kind_x, SUM(CASE WHEN has_n THEN n ELSE 1 END), MAX(l_seq) FROM kind WHERE in_landed=1 "
    "GROUP BY kind_o, kind_x")}
bad = sum(1 for k in set(pair) | set(agg) if pair.get(k) != agg.get(k))
print("PAIR", f"pairs {len(pair)}", f"aggregate {len(agg)}", f"DIFFER {bad}", sep="\t", flush=True)
rows, wrong, flagged = c.execute(
    "SELECT COUNT(*), SUM(no_dk IS NOT (NOT EXISTS (SELECT 1 FROM kind_dk d WHERE d.entry = k.entry AND d.n > 0 "
    "AND d.tgt = CASE WHEN k.role = ? THEN k.kind_x ELSE k.kind_o END))), SUM(no_dk) FROM kind k",
    (cause,)).fetchone()
print("FLAG", f"kind rows {rows}", f"no_dk WRONG {wrong}", f"no_dk set {flagged}", sep="\t", flush=True)
landed, cand, noc = c.execute("SELECT SUM(in_landed = 1), SUM(in_landed = 1 AND no_dk = 1), "
                              "SUM(in_landed = 1 AND has_n = 0) FROM kind").fetchone()
print("COUNTS", f"in_landed {landed}", f"T2 candidates {cand}", f"known with no count {noc}", sep="\t", flush=True)
meta = dict(c.execute("SELECT k, v FROM meta"))
mx = c.execute("SELECT MAX(l_seq) FROM kind WHERE l_game IS NOT NULL").fetchone()[0]
print("META", f"kinds_known {meta.get('kinds_known')} vs {landed}", f"kind_seq_max {meta.get('kind_seq_max')} vs {mx}",
      f"equal {str(meta.get('kinds_known')) == str(landed) and str(meta.get('kind_seq_max')) == str(mx)}",
      f"schema {meta.get('schema')}", sep="\t", flush=True)
c.close()
os.makedirs(OUT, exist_ok=True)


def vac(drop: str | None) -> int:
    dst = os.path.join(OUT, f"v_{drop or 'asis'}.db")
    assert not os.path.exists(dst), dst
    s = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    s.execute("VACUUM INTO ?", (dst,))
    s.close()
    if drop:
        t = sqlite3.connect(dst)
        t.execute(f"DROP INDEX {drop}")
        t.execute("VACUUM")
        t.close()
    return os.path.getsize(dst)


base = vac(None)
print("BYTES", "as is", base, sep="\t", flush=True)
for ix in ("kind_dk_et", "kind_nocount", "kind_t2"):
    print("BYTES", ix, base - vac(ix), sep="\t", flush=True)
