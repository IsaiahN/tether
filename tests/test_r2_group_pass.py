"""R2 (the reviewer 2026-11-06 r1297): the proposer's group pass reads the owners of its state once
(F1), and skips a text before compiling it when its (kind, template) key was already taken by a
text that FORMED (F2) -- `seen` is still marked only inside _group_form. Pure: the same candidates
out. test_group_row's agent (seconds), the proposer's texts planted.

  R2a IDENTITY: over a planted pool (every slot equal to every slot of the same reading, so many
      texts share a key), _group_cands' full output -- rank tuples, texts, members, keys, in
      order -- equals the same pass with the F2 skip and the F1 read-once both patched off
  R2b FORCING: the first text of a key fails to form (its compile planted as a refusal) and a
      later text with the same key forms: the later one still comes out. CONTROL: the same pool
      with the key marked before the pass loses it -- what marking "seen" before compiling does

    python tests/test_r2_group_pass.py [check ...]
"""
from __future__ import annotations

import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import test_group_row as G  # noqa: E402

tether = G.tether


def _fresh():
    ag, atoms, _st = G.agent()
    before = ag.trace[-1][2]
    ag._hyp, ag._hyp_tried, ag._hyp_exhausted = None, {}, None
    return ag, atoms, before


def _rows(out):
    return [(k, t, tuple(p.slot for p in g.parts), tk, s) for k, t, g, tk, s in out]


def check_r2a_identity() -> None:
    ag, atoms, before = _fresh()
    slots = sorted(s for s in before if s.count(".") == 1 and s.startswith("o")
                   and "~" not in s and "@" not in s)
    by_reading: dict = {}
    for s in slots:
        by_reading.setdefault(s.split(".", 1)[1], []).append(s)
    items = {f"{a} == {b}": "pool" for sl in by_reading.values() for a in sl for b in sl if a != b}
    assert len(items) > 50, len(items)
    keys = {ag._group_key(t) for t in items}
    assert len(keys) < len(items), "the pool has no shared keys: F2 has nothing to skip"
    new = _rows(ag._group_cands(items, before, atoms))
    ag._compile_cache.clear()
    raw = tether.Agent._owners
    try:
        tether.Agent._group_key = lambda _self, _t: None
        ag._own_pass = None
        tether.Agent._owners = lambda _self, st: sorted(
            {k.split(".", 1)[0] for k in st if "." in k and "~" not in k.split(".", 1)[0]
             and "@" not in k})
        tether.Agent._group_cands = lambda self, it, b, at: self._group_cands_pass(
            it, b, at, [], set())
        old = _rows(ag._group_cands(items, before, atoms))
    finally:
        tether.Agent._owners = raw
    assert new and new == old, (len(new), len(old))
    print(f"  {len(items)} texts, {len(keys)} keys: {len(new)} group candidates, the same list "
          f"with F1 and F2 off")


def check_r2b_forcing() -> None:
    ag, atoms, before = _fresh()
    first, later = "o0.row == o1.row", "o5.row == o1.row"
    assert ag._kind("o0") == ag._kind("o5"), "the panel: o0 and o5 share a kind"
    assert ag._group_key(first) == ag._group_key(later), "one key"
    ag._compile_cache[first] = G.C.Refusal("planted: the first text does not form")
    items = {first: "pool", later: "pool"}
    out = [t for _k, t, _g, _tk, _s in ag._group_cands(items, before, atoms)]
    assert out == [f"ALL kind(o5): {later}"], out
    marked = [t for _k, t, _g, _tk, _s in ag._group_cands_pass(
        items, before, atoms, [], {ag._group_key(first)})]
    assert marked == [], marked
    print(f"  the first text refused, the later one forms: {out}; marked early: {marked}")


def main() -> int:
    want = sys.argv[1:]
    names = [k for k in globals() if k.startswith("check_") and (not want or k in want)]
    if len(names) == 1:
        globals()[names[0]]()
        print("ok  ", names[0])
        return 0
    bad = [n for n in names if subprocess.run([sys.executable, "-B", __file__, n],
                                              cwd=str(_repo.ROOT),
                                              stdin=subprocess.DEVNULL).returncode]
    assert not bad, bad
    print(f"r2_group_pass: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
