"""RDL Piece 2: rdl_release (C4 release schedule, the release base layer, codified reach). Spec:
docs/03-DESIGN/RDL_BUILD_SPEC_2026-11-16.md "Piece 2". Synthetic preloads (types.SimpleNamespace),
no agent, no rdl_store import.
  R1  tier 1 released at birth (the base layer); tier 2 not until tier-1 settled >= MIN_SETTLED,
      then released (age never releases)
  R2  unusable preloads (C2: no bond or no attach) are never released; a passed `usable` is used
  R3  stats_from_rows counts offered / settled / refused per (corpus, tier)
  R4  reach_policy orders by validity desc, ties by tried desc, then the cue's text; priority
      follows the policy rank
  R5  merge_stats sums increments and mutates neither input
  MF-R1 inherited_settled=False -> tier 1 NOT released at birth -> RED as required (the base layer
      is what releases it)
Seconds.
    python tests/test_rdl_release.py
"""
from __future__ import annotations

import sys
from types import SimpleNamespace

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import rdl_release as R  # noqa: E402


def pre(pid, tier, corpus="wordnet", bonds=(("of", "a", "b"),), attaches=("e1",), cluster=None):
    src = {"corpus": corpus}
    if cluster:
        src["cluster"] = cluster
    return SimpleNamespace(pid=pid, tier=tier, stage=("instance", "regularity", "abstraction",
                                                      "core_rule")[tier - 1],
                           source=src, bonds=tuple(bonds), attaches=tuple(attaches))


def row(event, pid, tier, corpus="wordnet", cluster="SHAPE", cycle=0):
    return {"event": event, "detail": {"pid": pid, "tier": tier, "corpus": corpus,
                                       "cluster": cluster}, "cycle": cycle, "slot": None}


def main() -> int:
    assert R.MIN_SETTLED == 2, "MIN_SETTLED is the project's MIN_REPEAT, reused"
    ps = [pre("t1a", 1), pre("t1b", 1, corpus="cards"), pre("t2a", 2), pre("t3a", 3)]

    # R1: the base layer releases tier 1 at birth; tier 2 waits for tier-1 settles
    assert R.released(ps, {}) == {"t1a", "t1b"}, R.released(ps, {})
    one = {("wordnet", 1): {"offered": 3, "settled": 1, "refused": 0}}
    assert R.released(ps, one) == {"t1a", "t1b"}, "one settle is a coincidence"
    two = {("wordnet", 1): {"offered": 3, "settled": 1, "refused": 0},
           ("cards", 1): {"offered": 1, "settled": 1, "refused": 0}}
    assert R.released(ps, two) == {"t1a", "t1b", "t2a"}, "summed over sources"
    assert "t3a" not in R.released(ps, two), "tier 3 waits on tier-2 settles"
    print("R1 tier 1 at birth (base layer); tier 2 at tier-1 settled >= 2: GREEN")

    # R2: C2 -- no bond or no attach is recorded, never offered
    bad = [pre("nob", 1, bonds=()), pre("noa", 1, attaches=()), pre("ok", 1)]
    assert R.released(bad, {}) == {"ok"}, R.released(bad, {})
    assert R.released(bad, {}, usable=lambda p: p.pid == "nob") == {"nob"}, "usable passed in"
    print("R2 unusable preloads never released: GREEN")

    # R3: stats_from_rows
    rows = [row("rdl_offer", "t1a", 1), row("rdl_settle", "t1a", 1), row("rdl_settle", "t1a", 1),
            row("rdl_refuse", "t1a", 1), row("rdl_offer", "t1b", 1, corpus="cards"),
            row("rdl_refuse", "t2a", 2), {"event": "mint", "detail": {"tier": 1}, "cycle": 0}]
    st = R.stats_from_rows(rows)
    assert st == {("wordnet", 1): {"offered": 1, "settled": 2, "refused": 1},
                  ("cards", 1): {"offered": 1, "settled": 0, "refused": 0},
                  ("wordnet", 2): {"offered": 0, "settled": 0, "refused": 1}}, st
    assert R.released(ps, st) == {"t1a", "t1b", "t2a"}, "rows feed the release"
    print("R3 stats_from_rows counts: GREEN")

    # R4: reach_policy -- validity desc, tried desc, cue text
    rr = ([row("rdl_settle", "a", 1, cluster="A")] * 3 + [row("rdl_refuse", "a", 1, cluster="A")]
          + [row("rdl_settle", "b", 1, cluster="B"), row("rdl_refuse", "b", 1, cluster="B")]
          + [row("rdl_settle", "d", 1, cluster="AB"), row("rdl_refuse", "d", 1, cluster="AB")]
          + [row("rdl_offer", "c", 1, cluster="C")]
          + [row("rdl_refuse", "e", 1, cluster="E")] * 2)
    pol = R.reach_policy(rr)
    got = [(e[0][2], e[1], e[2]) for e in pol]
    want = [("A", 4, 3), ("AB", 2, 1), ("B", 2, 1), ("C", 0, 0), ("E", 2, 0)]
    assert got == want, got
    assert [e[3] for e in pol] == [4 / 6, 0.5, 0.5, 0.5, 0.25], [e[3] for e in pol]
    assert pol == R.reach_policy(list(reversed(rr))), "order independent of row order"
    pa, pb, pn = pre("pa", 1, cluster="A"), pre("pb", 1, cluster="B"), pre("pn", 1, cluster="Z")
    assert R.priority(pa, pol, 0) < R.priority(pb, pol, 0) < R.priority(pn, pol, 0)
    assert R.priority(pn, pol, 5) == (len(pol), 1, -5, "pn")
    o1, o2 = pre("x", 1, cluster="Z"), pre("y", 1, cluster="Z")
    assert R.priority(o2, pol, 9) < R.priority(o1, pol, 1), "age only breaks ties, older first"
    print("R4 reach_policy order (validity, tried, text) and priority: GREEN")

    # R5: merge_stats
    a = {("wordnet", 1): {"offered": 1, "settled": 2, "refused": 0}}
    b = {("wordnet", 1): {"offered": 1, "settled": 1, "refused": 3},
         ("cards", 4): {"offered": 2, "settled": 0, "refused": 0}}
    m = R.merge_stats(a, b)
    assert m == {("wordnet", 1): {"offered": 2, "settled": 3, "refused": 3},
                 ("cards", 4): {"offered": 2, "settled": 0, "refused": 0}}, m
    assert a == {("wordnet", 1): {"offered": 1, "settled": 2, "refused": 0}}, "a mutated"
    assert R.merge_stats(None, b) == b and R.merge_stats(a, {}) == a
    print("R5 merge_stats sums: GREEN")

    # MF-R1: without the base layer tier 1 is not released at birth
    off = R.released(ps, {}, inherited_settled=False)
    assert "t1a" not in off and not off, off
    print("MF-R1 inherited_settled=False: tier 1 NOT released at birth -> RED as required")
    print("rdl_release: OK")
    return 0


def test_rdl_release():
    assert main() == 0


if __name__ == "__main__":
    sys.exit(main())
