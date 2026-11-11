"""ROADMAP STEP 4, THE RETRO-FOLD (r1717, r1721, r1734, r1736, r1761): Piece 2's rule applied once
to a lineage's memory store as it stands, written as ordinary archive saves that the normal load and
merge apply -- never an edit to memory.db. Outside the agent's step path.

A row folds iff its n == 1, it carries a shape form (tether._unformed changes it), its entry is not
a kernel term, and its concept (the key with the form dropped) holds n >= 2 without it. Decided on
the store before any fold. Each save carries, per folded row, -1 in kinds_landed_n / kinds_landed_dk
and the key in kinds_unknown / kinds_unknown_dk (lineage_store._FOLD_UNKNOWN); per concept, +rows in
the same fields, the key in kinds_landed, the folded rows' latest landing when it is newer than the
concept's own, and one audit record ("retro_fold", read by nothing). Saves are split by concept, so
each one keeps every concept's sum. The kernel is a freshly wired agent's (no bound terms offline).

    python conform/retro_fold.py <lineage dir>                 # count only, writes nothing
    python conform/retro_fold.py <lineage dir> --write [--rows N]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))

import lineage  # noqa: E402
import tether  # noqa: E402

RULE = "r1717/r1721/r1734/r1736/r1761"


def kernel() -> set:
    sys.path.insert(0, str(ROOT / "tests"))
    import arc_holdout
    from test_entry import FakeWrapper
    _env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake", lineage_dir=None)
    return set(ag.gamma.kernel)


def _plan(con: sqlite3.Connection, table: str, skip: set) -> dict:
    """One table's folds, in store ids: {concept: [rows, best_last]} and the concept's own last."""
    sym = {}

    def s(i):
        if i not in sym:
            sym[i] = con.execute("SELECT s FROM sym WHERE id = ?", (i,)).fetchone()[0]
        return sym[i]
    if table == "kind":
        cols, parts = "entry, role, kind_o, kind_x", (2, 3)
        kinds = "SELECT kind_o FROM kind UNION SELECT kind_x FROM kind"
    else:
        cols, parts = "dk, entry, tgt", (2,)
        kinds = "SELECT tgt FROM kind_dk"
    ent = 0 if table == "kind" else 1
    js = (2, 3) if table == "kind" else (0, 2)
    unf: dict = {}          # kind id -> (concept part, formed)
    ukey: dict = {}
    for (k,) in con.execute(kinds):
        t = tuple(json.loads(s(k)))
        u = tether._unformed(t)
        unf[k] = (ukey.setdefault(u, len(ukey)), u != t)
    skip_ids = {i for i, x in con.execute("SELECT id, s FROM sym") if x in skip}

    def concept(r):
        return tuple(unf[x][0] if i in parts else x for i, x in enumerate(r))
    conc: Counter = Counter()
    own_last: dict = {}
    q = f"SELECT {cols}, n, l_game, l_level, l_cycle, l_seq FROM {table}"
    for r in con.execute(q):
        key = r[:len(parts) + 2]
        c = concept(key)
        conc[c] += r[len(key)]
        if not any(unf[key[i]][1] for i in parts):
            own_last[c] = r[len(key) + 1:]
    fold: dict = {}
    kern_refused = 0
    for r in con.execute(q):
        key = r[:len(parts) + 2]
        n = r[len(key)]
        if n != 1 or not any(unf[key[i]][1] for i in parts):
            continue
        c = concept(key)
        if conc[c] - 1 < 2:
            continue
        if key[ent] in skip_ids:
            kern_refused += 1
            continue
        got = fold.setdefault(c, [[], None])
        got[0].append(key)
        lv = r[len(key) + 1:]
        if lv[0] is not None and (got[1] is None or lv[3] > got[1][3]):
            got[1] = lv
    back = {v: u for u, v in ukey.items()}
    return {"fold": fold, "own_last": own_last, "conc": conc, "s": s, "back": back,
            "parts": parts, "js": js, "kern_refused": kern_refused}


def _decode(p: dict, key: tuple, concept: bool = False) -> list:
    """Store ids as the save writes them: kinds and delta kinds as lists, names as text."""
    s = p["s"]
    return [list(p["back"][x]) if concept and i in p["parts"] else
            json.loads(s(x)) if i in p["js"] else s(x) for i, x in enumerate(key)]


def fields(table: str, p: dict, concepts: list) -> dict:
    """One save's kind fields for these concepts (each whole)."""
    dk = table == "kind_dk"
    n_rows, unknown, landed, last, recs = [], [], [], [], []
    for c in concepts:
        rows, best = p["fold"][c]
        cl = _decode(p, c, concept=True)
        for key in rows:
            k = _decode(p, key)
            n_rows.append([*k, -1])
            unknown.append(k)
        n_rows.append([*cl, len(rows)])
        landed.append(cl)
        own = p["own_last"].get(c)
        if best is not None and (own is None or own[0] is None or best[3] > own[3]):
            last.append([*cl, *best])
        recs.append([table, cl, len(rows), len({key[2:] for key in rows}), len(rows),
                     c not in p["own_last"]])
    if dk:
        return {"kinds_landed_dk": n_rows, "kinds_unknown_dk": unknown, "kinds_dk_last": last,
                "_recs": recs}
    return {"kinds_landed_n": n_rows, "kinds_unknown": unknown, "kinds_landed": landed,
            "kinds_last": last, "_recs": recs}


def _chunks(p: dict, rows_per: int) -> list[list]:
    out, cur, n = [], [], 0
    for c in sorted(p["fold"], key=repr):
        k = len(p["fold"][c][0])
        if cur and n + k > rows_per:
            out.append(cur)
            cur, n = [], 0
        cur.append(c)
        n += k
    if cur:
        out.append(cur)
    return out


def _gen(parent: str, f: dict, part: int, of: int, tool: str, kernel_n: int) -> dict:
    recs = f.pop("_recs")
    tot: dict = {}
    for t, _c, rows, _forms, _n, new in recs:
        x = tot.setdefault(t, {"rows_folded": 0, "concepts": 0, "concepts_new": 0})
        x["rows_folded"] += rows
        x["concepts"] += 1
        x["concepts_new"] += int(new)
    for k in list(f):
        f[k] = lineage._ksorted(f[k]) if k.endswith("_dk") else sorted(f[k])
    return {"lineage": 1, "parent": parent, "game": None, "terms": [], "status": [],
            "evidence": [], "vindication_tail": [], "book": {}, "invented": {}, "dormant": [],
            "dormant_refused": [], **f,
            "retro_fold": {"rule": RULE, "kernel_only": True, "kernel_terms": kernel_n,
                           "part": [part, of], "tool": tool,
                           "records": [[t, c, r, fm, n] for t, c, r, fm, n, _new in recs],
                           "concept_new": [[t, c] for t, c, *_x, new in recs if new],
                           "totals": tot}}


def run(d: Path, rows_per: int = 200_000, write: bool = False, kern: set | None = None,
        say=print) -> dict:
    """Plan the fold of the store in `d` and, with `write`, write its saves on the store's last
    merged save. Every save in the folder must be merged and the last merged must be a tip (a
    lineage may carry dead-end tips the store merged as a DAG; central has seven, r1763 3)."""
    t0 = time.perf_counter()
    gens = lineage._scan(d)
    tips = lineage._tips(gens)
    con = sqlite3.connect(f"file:{(d / 'memory.db').as_posix()}?mode=ro", uri=True)
    try:
        last = con.execute("SELECT v FROM meta WHERE k='last_merged'").fetchone()
        merged = {h for (h,) in con.execute("SELECT h FROM saves")}
        if not last or set(gens) != merged or last[0] not in tips:
            say(f"REFUSED: tips {tips}, store last_merged {last and last[0]}, saves not merged "
                f"{len(set(gens) - merged)}: merge the store first")
            return {"refused": True}
        kern = kernel() if kern is None else kern
        tool = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()[:16]
        plans = {t: _plan(con, t, kern) for t in ("kind", "kind_dk")}
        out = {"tables": {}, "saves": []}
        for t, p in plans.items():
            rows = sum(len(v[0]) for v in p["fold"].values())
            out["tables"][t] = x = {
                "rows": con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0],
                "n_is_1": con.execute(f"SELECT COUNT(*) FROM {t} WHERE n = 1").fetchone()[0],
                "folded": rows, "concepts": len(p["fold"]),
                "concepts_new": sum(1 for c in p["fold"] if c not in p["own_last"]),
                "kernel_refused": p["kern_refused"]}
            say(f"{t}: {x}")
        chunks = [(t, c) for t in ("kind", "kind_dk") for c in _chunks(plans[t], rows_per)]
        say(f"saves {len(chunks)} (at most {rows_per} folded rows each); planned in "
            f"{time.perf_counter() - t0:.0f} s; kernel {len(kern)} terms; parent {last[0]}")
        if not write:
            return out
        parent = last[0]
        for i, (t, cs) in enumerate(chunks, 1):
            g = _gen(parent, fields(t, plans[t], cs), i, len(chunks), tool, len(kern))
            raw = lineage._dumps(g)
            h = hashlib.sha256(raw).hexdigest()[:16]
            stored = lineage._store_bytes(raw)
            with open(d / f"{lineage.PREFIX}{h}.json", "xb") as fh:
                fh.write(stored)
                fh.flush()
                os.fsync(fh.fileno())
            out["saves"].append({"h": h, "table": t, "raw": len(raw), "stored": len(stored),
                                 "rows": sum(len(plans[t]["fold"][c][0]) for c in cs)})
            say(f"wrote {lineage.PREFIX}{h}.json part {i}/{len(chunks)}: {out['saves'][-1]}")
            parent = h
        say(f"tip {parent}; {time.perf_counter() - t0:.0f} s")
        out["tip"] = parent
        return out
    finally:
        con.close()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("lineage")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--rows", type=int, default=200_000, help="folded rows per save at most")
    a = ap.parse_args()
    return 2 if run(Path(a.lineage), a.rows, a.write).get("refused") else 0


if __name__ == "__main__":
    sys.exit(main())
