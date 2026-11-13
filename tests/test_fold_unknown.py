"""THE RETRO-FOLD'S UNKNOWN KEYS (TETHER_FOLD_UNKNOWN; the reviewer r1761 3, r1762 1-2) and
conform/retro_fold.py. Each check is shown passing, then its must-fail (MF) failing.

  U1  a hand lineage, the tool's fold saves merged: the folded kind and dk keys are not known on
      either load path (archive: absent from _kind_known / _kind_known_n / _kind_last /
      _kind_known_dk / _kdk_last; store: in_landed 0, no l_*, n 0), their concepts hold the sum.
      MF: the arm OFF leaves them known on both paths
  U2  gap (i): a pair whose only landed row folds has no store row, and the store's pairs equal
      the archive's _pair_counts. MF: no recount leaves the row (n 0)
  U3  gap (ii): a dk row that falls 1 -> 0 sets its target's no_dk back to 1. MF: no re-read
      leaves it 0
  U4  the tool's refusals: a recurring formed row (n 2) and a kernel entry stay. MF: the same
      row at n 1 folds; with no kernel skip the kernel rows fold
  U5  parity with Piece 2: the fake game played once with the live fold ON, against the same game
      fold OFF then the retro-fold: the same _kind_known, _kind_pairs, n, lasts, on both paths
  U7  the one-scan pair recount equals the per-pair one it replaced (b48babb's, which scanned kind
      once per pair: ~10 h on central, r1771), pair table for pair table, on pairs emptied (F2, F3),
      partly folded (F1: W, another entry's recurring row, stays) and untouched. MF: a recount that
      skips the emptied pairs' DELETE differs
  U6  a delta kind's third element is an int on some keys and a str on others (lineage._ksorted):
      the fixture folds one of each, and the dk save's kinds_dk_last is written in the writer's
      total order. MF: plain sorted() of those rows raises (the 2026-11-11 10:45 red)

    python tests/test_fold_unknown.py
"""
from __future__ import annotations

import hashlib
import sqlite3
import sys
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
sys.path.insert(0, _repo.ROOT)
sys.path.insert(0, str(Path(_repo.ROOT) / "conform"))

import retro_fold  # noqa: E402

import arc_holdout  # noqa: E402
import lineage  # noqa: E402
import lineage_store  # noqa: E402
import tether  # noqa: E402
from test_entry import FakeWrapper  # noqa: E402

tether._AGENT_SEED = False
E, E2 = "LIB|Alpha", "LIB|Beta"
P, C = "PROCESS", "CAUSE"
DK = ["MOTION", "+", 1]
DX = ["MOTION", "+", "x"]
U = ["POSITION", "SHAPE"]


def F(i):
    return [*U, f"form={i}"]


def put(d: Path, parent, **f) -> str:
    g = {"lineage": 1, "game": None, "terms": [], "status": [], "evidence": [],
         "vindication_tail": [], "book": {}, "invented": {}, "dormant": [], "dormant_refused": [],
         **({"parent": parent} if parent else {}), **f}
    raw = lineage._dumps(g)
    h = hashlib.sha256(raw).hexdigest()[:16]
    (d / f"{lineage.PREFIX}{h}.json").write_bytes(lineage._store_bytes(raw))
    return h


def merged(d: Path) -> None:
    con = lineage_store.open_store(d)
    try:
        lineage_store.catch_up(con, d)
    finally:
        con.close()


def hand(kern: str, n_y: int = 2) -> Path:
    """X1-X3 seen once (concept new), Y recurring, W another entry's recurring row on X1's pair, Z
    a CAUSE row on F1 (no_dk 0 by D1), K1-K3 a
    kernel entry's one-offs; D1-D3 dk one-offs, and D4-D6 the same with a str-sized delta kind."""
    d = Path(tempfile.mkdtemp())
    rows = [[E, P, F(1), F(1), 1], [E, P, F(2), F(2), 1], [E, P, F(3), F(3), 1],
            [E, P, F(4), F(4), n_y], [E2, P, F(1), F(1), 2], [E, C, U, F(1), 2],
            [kern, P, F(5), F(5), 1], [kern, P, F(6), F(6), 1], [kern, P, F(7), F(7), 1]]
    last = [[*r[:4], "g0", 0, 1, 10 + i] for i, r in enumerate(rows)]
    dks = [[k, E, F(i), 1] for k in (DK, DX) for i in (1, 2, 3)]
    put(d, None, kinds_landed=sorted(r[:4] for r in rows), kinds_landed_n=sorted(rows),
        kinds_last=sorted(last), kinds_landed_dk=lineage._ksorted(dks),
        kinds_dk_last=lineage._ksorted([[*k[:3], "g0", 0, 1, 30 + i] for i, k in enumerate(dks)]))
    merged(d)
    return d


def load(d: Path, store: bool):
    old = lineage._MEMORY_STORE
    lineage._MEMORY_STORE = store
    try:
        _env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake", lineage_dir=str(d))
    finally:
        lineage._MEMORY_STORE = old
    return ag


def kinds(d: Path) -> dict:
    con = sqlite3.connect(f"file:{lineage_store.path(d).as_posix()}?mode=ro", uri=True)
    sym = dict(con.execute("SELECT id, s FROM sym"))
    out = {"kind": {(sym[a], sym[b], sym[c], sym[x]): (n, il, nd, ls) for a, b, c, x, n, il, nd, ls
                    in con.execute("SELECT entry, role, kind_o, kind_x, n, in_landed, no_dk, "
                                   "l_seq FROM kind")},
           "pair": {(sym[o], sym[x]): (n, ls) for o, x, n, ls in
                    con.execute("SELECT kind_o, kind_x, n, last_seq FROM pair")}}
    con.close()
    return out


def j(k):
    return lineage_store._j(tuple(k))


def fold(d: Path, kern: set) -> dict:
    out = retro_fold.run(d, write=True, kern=kern, say=lambda *_a: None)
    merged(d)
    return out


def main() -> int:
    kern = retro_fold.kernel()
    kname = sorted(kern)[0]
    folded = [(E, P, tuple(F(i)), tuple(F(i))) for i in (1, 2, 3)]
    dfold = [(tuple(k), E, tuple(F(i))) for k in (DK, DX) for i in (1, 2, 3)]

    # U1 / U4
    d = hand(kname)
    out = fold(d, kern)
    assert out["tables"]["kind"]["folded"] == 3 and out["tables"]["kind_dk"]["folded"] == 6, out
    assert out["tables"]["kind"]["kernel_refused"] == 3, out
    st = kinds(d)["kind"]
    for e in folded:
        assert st[(e[0], e[1], j(e[2]), j(e[3]))][:2] == (0, 0), st
    assert st[(E, P, j(U), j(U))][:2] == (3, 1) and st[(E, P, j(F(4)), j(F(4)))][:2] == (2, 1)
    for store in (False, True):
        ag = load(d, store)
        if not store:
            assert not set(folded) & ag._kind_known and not set(folded) & set(ag._kind_known_n)
            assert not set(folded) & set(ag._kind_last), ag._kind_last
            assert ag._kind_known_n[(E, P, tuple(U), tuple(U))] == 3
        assert not set(dfold) & set(ag._kind_known_dk) and not set(dfold) & set(ag._kdk_last)
        for k in (DK, DX):
            assert ag._kind_known_dk[(tuple(k), E, tuple(U))] == 3 or store, ag._kind_known_dk
    old = lineage_store._FOLD_UNKNOWN
    lineage_store._FOLD_UNKNOWN = False
    try:
        d_mf = hand(kname)
        fold(d_mf, kern)
        ag_mf = load(d_mf, False)
        st_mf = kinds(d_mf)["kind"]
    finally:
        lineage_store._FOLD_UNKNOWN = old
    assert set(folded) <= ag_mf._kind_known, "MF-U1: the arm OFF should leave the keys known"
    assert all(st_mf[(e[0], e[1], j(e[2]), j(e[3]))][1] == 1 for e in folded), "MF-U1 store"
    print("U1 the folded kind and dk keys are not known on either path; concept n 3 (new); "
          "MF arm OFF: known on both paths")
    d_n1 = hand(kname, n_y=1)
    n1 = fold(d_n1, kern)["tables"]["kind"]["folded"]
    no_skip = retro_fold.run(hand(kname), kern=set(), say=lambda *_a: None)
    assert n1 == 4 and no_skip["tables"]["kind"]["folded"] == 6, (n1, no_skip)
    print("U4 the recurring row (n 2) and the kernel entry's 3 rows stay; MF the row at n 1 "
          "folds (4), no kernel skip folds the kernel rows (6)")

    # U2: the pair (F2, F2) loses its only landed row; (F1, F1) keeps W's
    pr = kinds(d)["pair"]
    assert (j(F(2)), j(F(2))) not in pr and pr[(j(F(1)), j(F(1)))][0] == 2, pr
    ag_a = load(d, False)
    arch = {(j(o), j(x)): v for (o, x), v in ag_a._pair_counts().items()}
    assert {k: v[0] for k, v in pr.items()} == {k: v[0] for k, v in arch.items()}, (pr, arch)
    real = lineage_store._recount_pairs
    lineage_store._recount_pairs = lambda *_a: None
    try:
        d2 = hand(kname)
        fold(d2, kern)
    finally:
        lineage_store._recount_pairs = real
    assert kinds(d2)["pair"].get((j(F(2)), j(F(2)))) is not None, "MF-U2: the row should stay"
    print(f"U2 the pair whose only row folded is gone; store pairs = archive _pair_counts "
          f"({len(pr)} pairs); MF no recount: the row stays at n "
          f"{kinds(d2)['pair'][(j(F(2)), j(F(2)))][0]}")

    # U7: the one scan == the per-pair recount it replaced, on emptied, partly folded and untouched
    def per_pair(con, pairs, delete=True):
        for o, x in sorted(pairs):
            n, last, rows = con.execute(
                "SELECT SUM(CASE WHEN has_n THEN n ELSE 1 END), MAX(l_seq), COUNT(*) FROM kind "
                "WHERE in_landed = 1 AND kind_o = ? AND kind_x = ?", (o, x)).fetchone()
            if rows:
                con.execute("UPDATE pair SET n = ?, last_seq = ? WHERE kind_o = ? AND kind_x = ?",
                            (n, last, o, x))
            elif delete:
                con.execute("DELETE FROM pair WHERE kind_o = ? AND kind_x = ?", (o, x))

    def with_recount(fn):
        real = lineage_store._recount_pairs
        lineage_store._recount_pairs = fn
        try:
            dd = hand(kname)
            fold(dd, kern)
        finally:
            lineage_store._recount_pairs = real
        return kinds(dd)["pair"]
    ref = with_recount(per_pair)
    assert pr == ref, (pr, ref)
    mf = with_recount(lambda con, pairs: per_pair(con, pairs, delete=False))
    assert mf != pr, "MF-U7: a recount without the DELETE should leave the emptied pairs"
    print(f"U7 the one-scan recount == the per-pair recount it replaced ({len(pr)} pairs: emptied "
          f"F2/F3, partly folded F1 at n {pr[(j(F(1)), j(F(1)))][0]}); MF no DELETE: "
          f"{len(set(mf) - set(pr))} emptied pairs left")

    # U3: Z (CAUSE, target F1) had D1; D1 falls 1 -> 0
    z = (E, C, j(U), j(F(1)))
    assert kinds(d)["kind"][z][2] == 1, kinds(d)["kind"][z]
    real = lineage_store._reread_no_dk
    lineage_store._reread_no_dk = lambda *_a: None
    try:
        d3 = hand(kname)
        fold(d3, kern)
    finally:
        lineage_store._reread_no_dk = real
    assert kinds(d3)["kind"][z][2] == 0, "MF-U3: no re-read should leave no_dk 0"
    print("U3 the CAUSE row on F1: no_dk 0 -> 1 when D1 falls to 0; MF no re-read: stays 0")

    # U5: parity with Piece 2
    def game(fold_on: bool, retro: bool):
        dd = Path(tempfile.mkdtemp())
        env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake", lineage_dir=str(dd))
        for _ in range(8):
            env.observe()
            ag.step()
        ag.end_run("cap")
        old = tether._CONCEPT_FOLD
        tether._CONCEPT_FOLD = fold_on
        try:
            lineage.write(dd, ag, "fake")
        finally:
            tether._CONCEPT_FOLD = old
        n = ag.gamma.book.get("fold_total", 0)
        if retro:
            merged(dd)
            t = fold(dd, kern | set(ag.bound.values()))["tables"]
            n = t["kind"]["folded"] + t["kind_dk"]["folded"]
        return dd, n

    def state(dd, store):
        ag = load(dd, store)
        out = {"pairs": ag._pair_counts(), "kind_pairs": set(ag._kind_pairs),
               "kdk_last": dict(ag._kdk_last), "kind_seq": ag._kind_seq}
        if store:
            con = sqlite3.connect(f"file:{lineage_store.path(dd).as_posix()}?mode=ro", uri=True)
            sym = dict(con.execute("SELECT id, s FROM sym"))
            out["kind"] = {tuple(sym[x] for x in r[:4]): r[4:] for r in con.execute(
                "SELECT entry, role, kind_o, kind_x, n, l_seq, no_dk FROM kind "
                "WHERE in_landed = 1")}
            out["kind_dk"] = {tuple(sym[x] for x in r[:3]): r[3:] for r in con.execute(
                "SELECT dk, entry, tgt, n, l_seq FROM kind_dk WHERE n != 0")}
            out["meta"] = dict(con.execute("SELECT k, v FROM meta WHERE k IN "
                                           "('kinds_known', 'kind_seq_max')"))
            con.close()
        else:
            out.update(known=set(ag._kind_known),
                       n={k: v for k, v in ag._kind_known_n.items() if v},
                       dk={k: v for k, v in ag._kind_known_dk.items() if v},
                       last=dict(ag._kind_last))
        return out
    (live, n_live), (retro, n_retro) = game(True, False), game(False, True)
    assert n_live > 0 and n_live == n_retro, ("precondition: the same rows fold", n_live, n_retro)
    diffs = {}
    for store in (False, True):
        a, b = state(live, store), state(retro, store)
        diffs[store] = [k for k in a if a[k] != b[k]]
    assert not any(diffs.values()), diffs
    print(f"U5 live fold vs retro-fold of the same game ({n_live} rows folded each): the same "
          f"known keys, n, dk, lasts and pairs on the archive path; the same kind / kind_dk "
          f"rows, pairs, meta and lasts on the store path")

    # U6: the dk save of U1's lineage holds a kinds_dk_last for the int-sized and the str-sized
    # delta kind; the tool wrote it in the writer's total order
    dk_save = [s for s in out["saves"] if s["table"] == "kind_dk"]
    g = lineage._read(d)[dk_save[0]["h"]]
    rows = g["kinds_dk_last"]
    assert {type(r[0][2]) for r in rows} == {int, str} and rows == lineage._ksorted(rows), rows
    try:
        sorted(rows)
        mf = None
    except TypeError as e:
        mf = str(e)
    assert mf, "MF-U6: plain sorted() of int- and str-sized delta kinds should raise"
    print(f"U6 the dk save's kinds_dk_last ({len(rows)} rows, delta kinds sized int and str) is in "
          f"the writer's total order; MF plain sorted(): {mf}")
    print("fold_unknown: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
