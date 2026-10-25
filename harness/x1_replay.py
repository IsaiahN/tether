"""X1, REPLAY IDENTITY (the reviewer 2026-10-24 20:00, with B1-B3): the live lineage's saves, root
to tip, merged by BOTH merges -- lineage_store.merge_save into a scratch memory.db (today's code,
the independent side) and store_fold.merge_save into a scratch learned.db (the port) -- and
compared after EACH save:
  every key the port touched, its decoded body against the old table's row (B3: canonical, both
  as table_rows decodes); every section's row count; and at saves 1, 8, 16, 24, 33 every section
  whole (additive digest).
B2: per save, the touched keys, both merges' seconds and the store's rows before. Runs in chunks
under the cap (START..END; the scratch state carries on). The live folder is only read (its saves
copied once).
    python x1_replay.py LIVE SCRATCH START END"""
from __future__ import annotations

import json
import shutil
import sqlite3
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT), str(ROOT / "harness")]
import migrate_learned as ml  # noqa: E402

import lineage_store as ls  # noqa: E402
import store_fold as sf  # noqa: E402

FULL = {1, 8, 16, 24, 33}


def old_row(con, tb, key_vals, inv) -> str | None:
    """The old table's row for one decoded key, decoded as table_rows does (None if absent)."""
    cols, keys = ml.columns(con, tb)
    sc = ml.SYM_COLS.get(tb, ())
    args = []
    for c, v in zip(keys, key_vals, strict=True):
        if c in sc:
            if v not in inv:
                return None
            v = inv[v]
        args.append(v)
    r = con.execute(f"SELECT {', '.join(cols)} FROM {tb} WHERE "
                    + " AND ".join(f"{c} = ?" for c in keys), args).fetchone()
    if r is None:
        return None
    d = dict(zip(cols, r, strict=True))
    sym = {i: s for s, i in inv.items()}
    for c in sc:
        d[c] = sym[d[c]]
    return ml.j({c: d[c] for c in cols if c not in keys})


def main() -> int:
    live, scr = Path(sys.argv[1]), Path(sys.argv[2])
    start, end = int(sys.argv[3]), int(sys.argv[4])
    old_dir, new_db = scr / "old", scr / "new" / "learned.db"
    if start == 1:
        assert not scr.exists(), scr
        old_dir.mkdir(parents=True)
        new_db.parent.mkdir(parents=True)
        for f in live.iterdir():
            if f.name != "memory.db":
                shutil.copyfile(f, old_dir / f.name)
    chain = [h for (h,) in sqlite3.connect(
        f"file:{(live / 'memory.db').as_posix()}?mode=ro&immutable=1", uri=True).execute(
        "SELECT h FROM saves ORDER BY k")]
    co = ls.open_store(old_dir)
    cn = sf.open_new(new_db)
    bad = 0
    for k in range(start, end + 1):
        h = chain[k - 1]
        g = json.loads(ls.file_bytes(old_dir / f"gen_{h}.json"))
        rows_before = sum(r[0] for r in cn.execute("SELECT n FROM manifest"))
        t = time.perf_counter()
        ls.merge_save(co, old_dir, h, g)
        t_old = time.perf_counter() - t
        aks = [ls.AkFile(f, f"ak_{h}") for f in sorted(old_dir.glob(f"ak_{h}_*.json"))]
        files = sorted(old_dir.glob(f"idx_{h}_*.json"))
        idx = ls._read_hashed(files[0], f"idx_{h}") if len(files) == 1 else None
        m = sf.merge_save(cn, h, g, aks, idx, len(files))
        inv = {s: i for i, s in co.execute("SELECT id, s FROM sym")}
        diff = []
        for sec, key in m["keys"]:
            new = cn.execute(f"SELECT body FROM {sf.Rows(cn).part(sec)} WHERE section = ? AND "
                             "key = ?", (sec, key)).fetchone()
            old = old_row(co, sec, json.loads(key), inv)
            if (new[0] if new else None) != old:
                diff.append((sec, key, old, new[0] if new else None))
        counts = {}
        for tb in ml.tables(co):
            n_old = co.execute(f"SELECT count(*) FROM {tb}").fetchone()[0]
            r = cn.execute("SELECT n FROM manifest WHERE section = ?", (tb,)).fetchone()
            if n_old != (r[0] if r else 0):
                counts[tb] = (n_old, r[0] if r else 0)
        line = (f"save {k:2} {h}: touched {m['touched']:,}, port {m['s']:.1f} s, "
                f"old {t_old:.1f} s, store rows before {rows_before:,}; q {m.get('q')}; "
                f"touched-key diffs {len(diff)}; count diffs {counts}")
        if k in FULL:
            sym = dict(co.execute("SELECT id, s FROM sym"))
            whole = []
            for tb in ml.tables(co):
                want = ml.table_rows(co, tb, sym)
                part = "perception" if tb in sf.PERCEPTION else "learned"
                have = dict(cn.execute(f"SELECT key, body FROM {part} WHERE section = ?", (tb,)))
                if sf.additive_digest(want) != sf.additive_digest(have):
                    first = next((x for x in sorted(set(want) | set(have))
                                  if want.get(x) != have.get(x)), None)
                    whole.append((tb, first, want.get(first), have.get(first)))
            line += f"; WHOLE compare: {len(whole)} sections differ"
            for tb, x, a, b in whole[:4]:
                print(f"  WHOLE {tb} first key {x}\n    old {a}\n    new {b}")
            bad += len(whole)
        print(line, flush=True)
        for sec, key, a, b in diff[:3]:
            print(f"  DIFF {sec} {key}\n    old {a}\n    new {b}", flush=True)
        bad += len(diff) + len(counts)
        if bad:
            print(f"X1 RED at save {k}")
            return 1
    co.close()
    cn.close()
    print(f"X1 {start}..{end}: green")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
