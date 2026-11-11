"""PIECE 2, THE CONCEPT FOLD (TETHER_FOLD; the reviewer r1679, r1688, r1717; Isaiah 2026-11-10
13:05, 14:27). Each check is shown passing, then its must-fail (MF) is shown failing.

  F1   a fitting seen-once kind_dk row folds: the concept's n rises by one, the row is gone, one
       fold row (concept, folded 1, forms 1), book fold_total 1. The kind table the same
  F6   variation: a one-off form folds into its unformed concept. MF: an exact-key fit refuses it
  F2   a misfit (its concept holds 1 besides it) stays. MF: a fold with no fit test swallows it
  F3   a kernel entry, and a bound one, never folds. MF: a fold that skips no entry folds both
  F7   a missing part: a row whose type set lacks one of the concept's types stays. MF: an
       outcome-only fit (dk and entry, any target) folds it
  F8   isomer: a row whose dk differs in sign or cluster stays. MF: an ingredients-only fit (any
       dk) folds it
  F9   ingredient: a composite entry over a settled concept does not fold into it. MF: an
       any-shared-part entry match folds it
  F10  a recurring form (n == 2 in the series, or a stored row) never folds. MF: a fold keyed on
       the concept alone folds the stored one
  FW   a fold leaves W unchanged, and the next write still counts. MF: the clock's old base
       misses it. A row added after the last tick, then a fold of two others: W +1 (the fold
       ticks first, r1718). MF: reset before the tick gives 0
  F4   the fake game, three games on one lineage, fold ON: after each merge the store's concept
       counts equal those before plus the game's UNFOLDED landings. MF: a fold that also writes
       the row counts it twice
  F11  a fold touches only this game's rows: every row of the store before the game is still
       there with n at least as before. MF: a rows-anywhere fold (the store's seen-once rows)
       changes them
  F5   zero-is-off: TETHER_FOLD off (the module value lineage.write reads), no fold row and the
       game's seen-once rows written as they are
  F13  a run of 3 games with their own ids and ONE write at the end: game 1's one-offs fold
       (r1728: the candidate is "since the last write", whatever the game id). MF: the
       latest-sighting-this-game rule folds 0 of them
  F12  three one-offs of one unformed key with no stored concept fold into a NEW concept
       (concept_new True); two do not (r1721 2). MF: an exists-at-load-only fit folds none

    python tests/test_concept_fold.py
"""
from __future__ import annotations

import os
import sqlite3
import sys
import tempfile
from collections import Counter

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
sys.path.insert(0, _repo.ROOT)

import arc_holdout  # noqa: E402
import lineage  # noqa: E402
import lineage_store  # noqa: E402
import tether  # noqa: E402
from test_entry import FakeWrapper  # noqa: E402

tether._AGENT_SEED = False
DK, DKM, DKC = ("MOTION", "+", 1), ("MOTION", "-", 1), ("COLOUR", "+", 1)
E = "LIB|Alpha"
T1, T2 = ("POSITION", "SHAPE", "form=1"), ("POSITION", "SHAPE", "form=2")
U = ("POSITION", "SHAPE")


def fresh():
    """An agent with no lineage and empty kind stores (the in-memory reader), its game G."""
    env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake", lineage_dir=None)
    for m in (ag._kind_landed_dk, ag._kdk_last, ag._kind_known_dk, ag._kind_landed_n,
              ag._kind_last, ag._kind_landed, ag._kind_known, ag._kind_known_n):
        m.clear()
    ag._kdk_written, ag._kn_written = {}, {}
    rows: list = []
    real = ag.led.record

    def spy(c, s, sl, ev, **k):
        rows.append((ev, k))
        return real(c, s, sl, ev, **k)
    ag.led.record = spy
    return ag, rows


def land(ag, key, n=1, game=None):
    ag._kind_landed_dk[key] += n
    ag._kdk_last[key] = (ag.gamma.game if game is None else game, 0, 0, 1)


def folded(ag) -> int:
    return ag._concept_fold()["kind_dk"]


def patched(obj, name, val, fn):
    old = getattr(obj, name)
    setattr(obj, name, val)
    try:
        return fn()
    finally:
        setattr(obj, name, old)


def reader_of(fn):
    return lambda self, _table, _snap: (lambda key: fn(self, key))


def main() -> int:
    # F1 / F6: fit and variation
    ag, rows = fresh()
    ag._kind_known_dk[(DK, E, T2)] = 3
    land(ag, (DK, E, T1))
    n = folded(ag)
    fr = [k for ev, k in rows if ev == "fold"]
    assert n == 1 and (DK, E, T1) not in ag._kind_landed_dk and ag._kind_landed_dk[(DK, E, U)] == 1
    assert fr == [fr[0]] and fr[0]["concept"] == [DK, E, U] and fr[0]["folded"] == 1 \
        and fr[0]["forms"] == 1 and ag.gamma.book["fold_total"] == 1, (fr, ag.gamma.book)
    after = ag._kind_known_dk[(DK, E, T2)] + ag._kind_landed_dk[(DK, E, U)]
    ag2, _ = fresh()
    ag2._kind_known_dk[(DK, E, T2)] = 3
    land(ag2, (DK, E, T1))
    mf = patched(tether, "_unformed", lambda k: k, lambda: folded(ag2))
    assert mf == 0, "MF-F6: an exact-key fit should refuse the one-off form"
    # the kind table
    agk, rk = fresh()
    KO, KX = ("COLOUR", "SHAPE", "form=7"), ("COLOUR", "SHAPE", "form=8")
    UO = ("COLOUR", "SHAPE")
    agk._kind_known_n[(E, "CAUSE", ("COLOUR", "SHAPE", "form=9"), UO)] = 2
    agk._kind_known.add((E, "CAUSE", ("COLOUR", "SHAPE", "form=9"), UO))
    e = (E, "CAUSE", KO, KX)
    agk._kind_landed_n[e] = 1
    agk._kind_landed.add(e)
    agk._kind_last[e] = (agk.gamma.game, 0, 0, 1)
    nk = agk._concept_fold()["kind"]
    uk = (E, "CAUSE", UO, UO)
    assert nk == 1 and e not in agk._kind_landed_n and agk._kind_landed_n[uk] == 1 \
        and e not in agk._kind_landed and uk in agk._kind_landed and (UO, UO) in agk._kind_pairs
    print(f"F1 kind_dk: the one-off row folded, concept n 3 -> {after}; fold row "
          f"{fr[0]['concept']} folded {fr[0]['folded']} forms {fr[0]['forms']}; fold_total "
          f"{ag.gamma.book['fold_total']}. The kind table: {e[2]}/{e[3]} -> {uk[2]}/{uk[3]}, "
          f"landed and pairs moved")
    print("F6 variation folds; MF an exact-key fit: folded 0")

    # F2: misfit
    ag, _ = fresh()
    ag._kind_known_dk[(DK, E, T2)] = 1
    land(ag, (DK, E, T1))
    assert folded(ag) == 0 and ag._kind_landed_dk[(DK, E, T1)] == 1
    ag, _ = fresh()
    ag._kind_known_dk[(DK, E, T2)] = 1
    land(ag, (DK, E, T1))
    mf = patched(tether.Agent, "_fold_reader", reader_of(lambda _s, _k: (0, 99)),
                 lambda: folded(ag))
    assert mf == 1, "MF-F2: a fold with no fit test should swallow the misfit"
    print("F2 a misfit (concept 1 besides it) stays; MF no fit test: folded 1")

    # F3: kernel and bound
    out = []
    for how in ("kernel", "bound"):
        for defect in (False, True):
            ag, _ = fresh()
            ag._kind_known_dk[(DK, E, T2)] = 3
            land(ag, (DK, E, T1))
            if how == "kernel":
                ag.gamma.kernel[E] = "inherited"
            else:
                ag.bound["o1.x"] = E
            if defect:
                real = tether.Agent._fold_rows
                n = patched(tether.Agent, "_fold_rows",
                            lambda self, *a, r=real: r(self, *a[:6], set(), a[7]),
                            lambda a_=ag: folded(a_))
            else:
                n = folded(ag)
            out.append((how, defect, n))
    assert out == [("kernel", False, 0), ("kernel", True, 1), ("bound", False, 0),
                   ("bound", True, 1)], out
    print("F3 a kernel entry and a bound entry stay; MF skipping no entry: both fold")

    # F7: missing part
    ag, _ = fresh()
    ag._kind_known_dk[(DK, E, ("EXTENT", "POSITION", "SHAPE", "form=2"))] = 3
    land(ag, (DK, E, T1))
    assert folded(ag) == 0
    ag, _ = fresh()
    ag._kind_known_dk[(DK, E, ("EXTENT", "POSITION", "SHAPE", "form=2"))] = 3
    land(ag, (DK, E, T1))
    mf = patched(tether, "_unformed", lambda k: () if isinstance(k, tuple) and k and k[0] in
                 ("EXTENT", "POSITION") else k, lambda: folded(ag))
    assert mf == 1, "MF-F7: an outcome-only fit should fold the row missing a part"
    print("F7 a row lacking the concept's EXTENT stays; MF outcome-only fit: folded 1")

    # F8: isomer (another sign, another cluster)
    def isomer(defect):
        ag, _ = fresh()
        ag._kind_known_dk[(DKM, E, T2)] = 3
        ag._kind_known_dk[(DKC, E, T2)] = 3
        land(ag, (DK, E, T1))
        if not defect:
            return folded(ag)

        def any_dk(self, key):
            return 0, sum(n for k, n in self._kind_known_dk.items()
                          if k[1] == key[1] and tether._unformed(k[2]) == tether._unformed(key[2]))
        return patched(tether.Agent, "_fold_reader", reader_of(any_dk), lambda: folded(ag))
    assert isomer(False) == 0 and isomer(True) == 1
    print("F8 a row under (MOTION, +) beside (MOTION, -) and (COLOUR, +) concepts stays; MF "
          "ingredients-only fit: folded 1")

    # F9: ingredient
    comp = "LIB|Alpha+LIB|Beta"

    def ingredient(defect):
        ag, _ = fresh()
        ag._kind_known_dk[(DK, E, T2)] = 3
        land(ag, (DK, comp, T1))
        if not defect:
            return folded(ag)

        def shared(self, key):
            return 0, sum(n for k, n in self._kind_known_dk.items()
                          if k[0] == key[0] and set(k[1].split("+")) & set(key[1].split("+")))
        return patched(tether.Agent, "_fold_reader", reader_of(shared), lambda: folded(ag))
    assert ingredient(False) == 0 and ingredient(True) == 1
    print(f"F9 the composite entry {comp} over the settled {E} concept stays; MF any-shared-part "
          "match: folded 1")

    # F10: a recurring form
    ag, _ = fresh()
    ag._kind_known_dk[(DK, E, T2)] = 3
    land(ag, (DK, E, T1), n=2)
    a = folded(ag)
    ag, _ = fresh()
    ag._kind_known_dk[(DK, E, T2)] = 3
    ag._kind_known_dk[(DK, E, T1)] = 1
    land(ag, (DK, E, T1))
    b = folded(ag)
    ag, _ = fresh()
    ag._kind_known_dk[(DK, E, T2)] = 3
    ag._kind_known_dk[(DK, E, T1)] = 1
    land(ag, (DK, E, T1))
    mf = patched(tether.Agent, "_fold_reader", reader_of(
        lambda s, _k: (0, s._kind_known_dk[(DK, E, T2)] + s._kind_known_dk[(DK, E, T1)])),
        lambda: folded(ag))
    assert (a, b, mf) == (0, 0, 1), (a, b, mf)
    print("F10 a form seen twice this series, and one already stored, stay; MF the concept alone: "
          "the stored one folds")

    # F13: per-game ids, one write at the end
    def per_game(defect=False):
        ag, _ = fresh()
        ag._kind_known_dk[(DK, E, T2)] = 3
        for i, gid in enumerate(("game1", "game2", "game3")):
            land(ag, (DK, E, ("POSITION", "SHAPE", f"form={40 + i}")), game=gid)
        ag.gamma.game = "game3"                  # the one write happens in the last game
        if not defect:
            return folded(ag), ag._kind_landed_dk[(DK, E, U)]
        real = tether.Agent._fold_candidate

        def this_game(self, e, *a):
            return real(self, e, *a) and self._kdk_last.get(e, (None,))[0] == self.gamma.game
        return patched(tether.Agent, "_fold_candidate", this_game, lambda: folded(ag)), None
    (n13, conc13), (mf13, _) = per_game(), per_game(defect=True)
    assert n13 == 3 and conc13 == 3 and mf13 == 1, (n13, conc13, mf13)
    print(f"F13 three games with their own ids, one write: all {n13} one-offs folded (game 1's "
          f"included), concept holds {conc13}; MF the this-game rule: {mf13} (only game 3's)")

    # F12: a concept formed by this game's one-offs alone
    def new_concept(k, defect=False):
        ag, rows = fresh()
        for i in range(k):
            land(ag, (DK, E, ("POSITION", "SHAPE", f"form={30 + i}")))
        if defect:
            return patched(tether.Agent, "_fold_fits",
                           lambda _self, s, sc, _h: s == 0 and sc >= 2, lambda: folded(ag))
        n = folded(ag)
        return n, [k_["concept_new"] for ev, k_ in rows if ev == "fold"]
    three, two, mf12 = new_concept(3), new_concept(2), new_concept(3, defect=True)
    assert three == (3, [True]) and two == (0, []) and mf12 == 0, (three, two, mf12)
    print(f"F12 three one-offs, no stored concept: folded {three[0]} into a new concept "
          f"(concept_new {three[1][0]}); two: folded {two[0]}; MF an exists-at-load-only fit: "
          f"folded {mf12}")

    # FW: W unchanged by a fold, and the next write still counts
    def w_case(defect, new_row):
        ag, _ = fresh()
        ag._kind_known_dk[(DK, E, T2)] = 3
        for i in range(5):
            land(ag, (DK, E, ("POSITION", "SHAPE", f"form={10 + i}")))
        ag._store_tick()
        w0 = ag.gamma.book["store_writes"]
        prev = dict(ag._store_prev)
        folded(ag)
        if defect:
            ag._store_prev = prev
        if new_row:
            land(ag, (DKM, E, ("BOOL",)))
        ag._store_tick()
        return ag.gamma.book["store_writes"] - w0
    got = (w_case(False, False), w_case(False, True), w_case(True, True))
    assert got == (0, 1, 0), got

    def w_between(defect):      # r1718: a row added after the last tick, then a fold of two
        ag, _ = fresh()
        ag._kind_known_dk[(DK, E, T2)] = 3
        land(ag, (DK, E, ("POSITION", "SHAPE", "form=21")))
        land(ag, (DK, E, ("POSITION", "SHAPE", "form=22")))
        ag._store_tick()
        w0 = ag.gamma.book["store_writes"]
        land(ag, (DKM, E, ("BOOL",)))
        if defect:      # reset before tick: the fold's own tick does not run
            patched(tether.Agent, "_store_tick", lambda _s: None, lambda: folded(ag))
        else:
            folded(ag)
        return ag.gamma.book["store_writes"] - w0
    between = (w_between(False), w_between(True))
    assert between == (1, 0), between
    print(f"FW 5 rows folded into 1: W moves {got[0]}; with one new row after the fold "
          f"{got[1]}; MF the clock's old base: {got[2]}. A row added after the last tick, then "
          f"two rows folded: W +{between[0]}; MF reset before the tick: +{between[1]}")

    # F4 / F11 / F5: the fake game on a lineage, three games, fold ON / OFF
    def play(fold, games=3, steps=8, defect=None, keep=None):
        d = tempfile.mkdtemp()
        snaps, want = [], []
        for _g in range(games):
            env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake", lineage_dir=d)
            for _ in range(steps):
                env.observe()
                ag.step()
            ag.end_run("cap")
            rows = []
            real = ag.led.record
            ag.led.record = (lambda c, s, sl, ev, rows_=rows, real_=real, **k:
                             (rows_.append(ev), real_(c, s, sl, ev, **k))[1])
            snaps.append(table(d))
            want.append(unfolded(ag))
            old = tether._CONCEPT_FOLD
            tether._CONCEPT_FOLD = fold
            try:
                if defect:
                    defect(ag)
                lineage.write(d, ag, "fake")
            finally:
                tether._CONCEPT_FOLD = old
            if keep is not None:
                keep.append(rows.count("fold"))
        return d, snaps, table(d), want

    def table(d):
        p = lineage_store.path(d)
        if not p.exists():
            return {}
        con = sqlite3.connect(f"file:{p.as_posix()}?mode=ro", uri=True)
        sym = dict(con.execute("SELECT id, s FROM sym"))
        out = {("dk", sym[a], sym[b], sym[c]): n
               for a, b, c, n in con.execute("SELECT dk, entry, tgt, n FROM kind_dk WHERE n != 0")}
        out.update({("k", sym[a], sym[b], sym[c], sym[x]): n for a, b, c, x, n in con.execute(
            "SELECT entry, role, kind_o, kind_x, CASE WHEN has_n THEN n ELSE 1 END FROM kind "
            "WHERE in_landed = 1")})
        con.close()
        return out

    import json

    def unfolded(ag):
        """This write's landings as the store keys them, before any fold, by concept."""
        out = Counter()
        wd, wn = getattr(ag, "_kdk_written", {}), getattr(ag, "_kn_written", {})
        for (dk, en, t), n in ag._kind_landed_dk.items():
            if n > wd.get((dk, en, t), 0):
                out[("dk", json.dumps(list(dk)), en, json.dumps(list(t)))] += n - wd.get(
                    (dk, en, t), 0)
        for (en, r, o, x), n in ag._kind_landed_n.items():
            if n > wn.get((en, r, o, x), 0):
                out[("k", en, r, json.dumps(list(o)), json.dumps(list(x)))] += n - wn.get(
                    (en, r, o, x), 0)
        return concepts(out)

    def concepts(t):
        c = Counter()
        for k, n in t.items():
            parts = (3,) if k[0] == "dk" else (3, 4)
            c[tuple(json.dumps(tether._unformed(tuple(json.loads(x)))) if i in parts else x
                    for i, x in enumerate(k))] += n
        return c

    nf_on: list = []
    d_on, snaps_on, on, want = play(True, keep=nf_on)
    assert sum(nf_on) > 0, "precondition: the fold ON run folded nothing"
    bad = [i for i, (b, a, w) in enumerate(zip(snaps_on, snaps_on[1:] + [on], want, strict=True))
           if concepts(a) != concepts(b) + w]
    assert not bad, bad

    def twice(ag):      # the defect: the folded row is written as well
        real = tether.Agent._fold_rows

        def keep_rows(self, table, landed, *a):
            before = Counter(landed)
            n = real(self, table, landed, *a)
            for e, c in before.items():
                if e not in landed:
                    landed[e] = c
            return n
        ag._fold_rows = keep_rows.__get__(ag)
    _d, s_mf, mf, w_mf = play(True, defect=twice)
    assert any(concepts(a) != concepts(b) + w
               for b, a, w in zip(s_mf, s_mf[1:] + [mf], w_mf, strict=True)), "MF-F4: the same sums"
    print(f"F4 3 games, fold ON: after each merge the store's concept counts = before + the "
          f"game's UNFOLDED landings ({len(concepts(on))} concepts, {len(on)} rows), fold rows "
          f"per game {nf_on}; MF writing the row too: the sums differ")

    def kept(before, after):
        return [k for k, n in before.items() if after.get(k, 0) < n]
    lost = [kept(snaps_on[i], snaps_on[i + 1] if i + 1 < len(snaps_on) else on)
            for i in range(1, len(snaps_on))]
    assert not any(lost), lost
    retro = dict(snaps_on[-1])
    for k in [k for k, n in retro.items() if n == 1 and "form=" in "".join(map(str, k))][:5]:
        del retro[k]
    assert kept(snaps_on[-1], retro), "MF-F11: a rows-anywhere fold should change a stored row"
    print(f"F11 every row stored before games 2 and 3 kept with n at least as before "
          f"({len(snaps_on[1])} and {len(snaps_on[2])} rows); MF a rows-anywhere fold of the "
          f"store's seen-once rows: {len(kept(snaps_on[-1], retro))} changed")

    nf_off: list = []
    _d, _s, off, _w = play(False, games=1, keep=nf_off)
    once_off = [k for k, n in off.items() if n == 1 and "form=" in "".join(map(str, k))]
    assert nf_off == [0] and once_off, (nf_off, len(once_off))
    print(f"F5 TETHER_FOLD off: no fold row; {len(once_off)} seen-once formed rows written")
    print("concept_fold: OK")
    return 0


if __name__ == "__main__":
    os.environ.setdefault("PYTHONHASHSEED", "0")
    raise SystemExit(main())
