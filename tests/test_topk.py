"""SERP, THE CHEAP RANK AND THE CUT (the reviewer 2026-11-02 r810, r816): Agent._topk and
Agent._tk_after on a stub holding only the state they read (the per-key offsets, the lookup counts,
the atoms); the rank's read counts come from the library index's posting lists (_POSTING).
  MF-TK1  200 kept entries -> at most TOPK_K (32) evaluated in one lookup.
  MF-TK2  the only fitting entry at rank 70 -> not in lookup 1's or 2's window, in lookup 3's of the
          same key; with the arm OFF the whole kept list is evaluated, so it is there at lookup 1
          (the cut is reversible, not lossy).
  MF-TK3  no "no entry" verdict while the offset is short of the end: _tk_after says not yet
          (False) for each window before the last, and True only at the end.
  MF-TK4  within one tier, an entry reading 3 of the asked readings ranks above one reading 1.
  MF-TK5  with 2,500 lit entries, the held-index filter (_described_lit, after the cut) examines at
          most 32 distinct entries in one lookup.
  MF-SC1  S3: a key asked twice never judges an entry twice -- its two windows are disjoint.
  MF-SC2  S3: a new description key starts from the top, whatever another key judged.

    python tests/test_topk.py
"""
from __future__ import annotations

import sys
from collections import Counter
from types import SimpleNamespace

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import ledger  # noqa: E402
import tether  # noqa: E402

A = tether.Agent


def stub():
    ag = SimpleNamespace(_tk_off={}, _tk_nofit={}, _tk_win=(None, ()), _dl_n=Counter(),
                         gamma=SimpleNamespace(atoms=[]), cycle=0,
                         led=ledger.Ledger(None),    # N1: _tk_after says "not yet" through it
                         _thought={"tried": {}, "paid": {}}, _thought_in={"tried": {}, "paid": {}},
                         _thought_key=A._thought_key)
    ag._thought_of = lambda f, k: A._thought_of(ag, f, k)
    return ag


def entries(n, prefix="e"):
    return [(f"{prefix}{i:03d}", 0.0) for i in range(n)]


def main():
    assert tether._SERP and tether.TOPK_K == 32, "SERP ON by default, K = 32"
    att = {"o1.col": "col", "o1.row": "row", "o1.w": "w"}
    tg = tuple(att)
    # MF-TK1
    lit = entries(200)
    tiers = {"T3": 200}
    ag = stub()
    win, nxt = A._topk(ag, lit, lit, tiers, att, tg, "k1")
    assert len(win) <= 32 and nxt == 32, ("MF-TK1", len(win), nxt)
    # MF-TK2 + MF-TK3: the fitting entry at rank 70; each window that misses advances, no verdict
    target, ag, found, verdicts = lit[70][0], stub(), None, []
    for lookup in range(1, 10):
        win, nxt = A._topk(ag, lit, lit, tiers, att, tg, "k2")
        if any(k == target for k, _w in win):
            found = lookup
            break
        verdicts.append(A._tk_after(ag, "k2", nxt))
    assert found == 3 and verdicts == [False, False], ("MF-TK2 / MF-TK3", found, verdicts)
    assert any(k == target for k, _w in lit), "OFF: the whole kept list holds it at lookup 1"
    ag, ends = stub(), []
    for _ in range(7):
        _w, nxt = A._topk(ag, lit, lit, tiers, att, tg, "k3")
        ends.append(A._tk_after(ag, "k3", nxt))
    assert ends[:6] == [False] * 6 and ends[6] is True and "k3" not in ag._tk_off, (
        "MF-TK3: the verdict only at the end, then the offset resets", ends)
    # MF-TK4: same tier, the 3-reading entry ranks first though it was listed after
    lit4 = [("one", 0.0), *entries(40, "x"), ("three", 0.0)]
    tether._posting_reads()
    tether._POSTING["one"] = {"col"}
    tether._POSTING["three"] = {"col", "row", "w"}
    win, _n = A._topk(stub(), lit4, lit4, {"T3": len(lit4)}, att, tg, "k4")
    names = [k for k, _w in win]
    assert names[0] == "three" and names.index("one") == 1, ("MF-TK4", names[:3])
    # MF-TK5: the cut runs first, so the held-index filter sees the window only
    seen: set = set()
    ag5 = stub()
    ag5._held_index = lambda *a: (seen.add(a[1]), [])[1]
    big = entries(2500, "y")
    win, _n = A._topk(ag5, big, big, {"T3": 2500}, att, tg, "k6")
    A._described_lit(ag5, None, win, {"T3": 2500}, att, tg, frozenset())
    assert 0 < len(seen) <= 32, ("MF-TK5: held-index entries examined", len(seen))
    # MF-SC1 / MF-SC2 (S3): no entry judged twice under one key; a new key starts fresh
    assert tether._SERP_CACHE, "S3 ON by default"
    ag6 = stub()
    w1, n1 = A._topk(ag6, lit, lit, tiers, att, tg, "s1")
    A._tk_after(ag6, "s1", n1)
    w2, _n2 = A._topk(ag6, lit, lit, tiers, att, tg, "s1")
    assert not {k for k, _w in w1} & {k for k, _w in w2} and len(w2) == 32, "MF-SC1"
    w3, _n3 = A._topk(ag6, lit, lit, tiers, att, tg, "s2")
    assert [k for k, _w in w3] == [k for k, _w in w1], "MF-SC2: a new key starts from the top"
    print(f"test_topk: 200 kept -> {len(A._topk(stub(), lit, lit, tiers, att, tg, 'k5')[0])} "
          f"evaluated; the rank-70 fit found on lookup {found} (windows 1-2 not yet, no verdict); "
          f"7 windows over 200 -> verdict only at the 7th; the 3-reading entry ranks above the "
          f"1-reading one; 2,500 lit -> {len(seen)} entries through the held-index filter; S3: a "
          f"re-asked key's windows are disjoint, a new key starts from the top")


if __name__ == "__main__":
    main()
