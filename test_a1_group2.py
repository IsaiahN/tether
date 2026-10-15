"""C-A1-2, A1-CONVERT GROUP 2 (the reviewer 2026-10-15 09:05, 09:19, 14:23, 14:27). WRITTEN, NOT
RUN: it runs in the end-of-step-7 checklist.

  S4   _next_stream: an exact tie in spent goes to the recorded draw, the same pick whatever the
       list order. MF-S4: today's call (no key) takes the list's first.
  S6   _merge_by_depth: a depth-1 library chain with evidence is walked before the depth-1 closure
       chains, and a depth-3 one after the depth-2 closure chains. MF-S6: today's chain (library
       first) walks the depth-3 library chain first.
  S8   _lookup_order: a derived slot in contact comes before a plain slot not in contact (the
       residual gate first); within one gate and one action step, more evidence, then more
       distinct values. MF-S8: today's tuple puts the plain slot first.
  S9   objective_step / objective_gap over a _PricedDomain: the only satisfying value is UNSEEN and
       is aimed at (today: NOT_RESOLVED and None); with a shown value farther and an unseen value
       nearer, both are on the frontier and least-known picks the unseen. MF-S9: the plain set
       (today's domain) leaves the unseen-only case unresolved. F1: two satisfying values at one
       distance (unseen, and shown) go to the draw, never the lower value.
  ROWS on a 30-step fake game: at least one "stream" row (precondition); each names its site,
       winner_rank never past walked_total, and the stop counts are 0/1.

    python test_a1_group2.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from types import SimpleNamespace

sys.dont_write_bytecode = True

import frontier as FR  # noqa: E402
import tether  # noqa: E402


def s4() -> None:
    spent = {0: 2, 1: 2, 2: 2}
    key = "7:o1.x:stream_share"
    want = min(spent, key=lambda s: FR.draw_key(key, s))
    assert tether._next_stream([0, 1, 2], spent, True, key) == want
    assert tether._next_stream([2, 1, 0], spent, True, key) == want, "S4: the list order decided"
    assert tether._next_stream([2, 1, 0], spent, True) == 2, "MF-S4 did not show the list order"
    print(f"  S4 the tie goes to the draw ({want}), whatever the order; MF-S4: the list's first")


def _c(name, depth):
    return SimpleNamespace(name=name, atoms=tuple(range(depth)))


def s6() -> None:
    lib = [_c("L3", 3), _c("L1", 1)]
    clo = [_c("c1a", 1), _c("c1b", 1), _c("c2a", 2), _c("c2b", 2), _c("c3a", 3)]
    got = [c.name for c in tether._merge_by_depth(lib, iter(clo), {"L1": 2, "L3": 1}, "k")]
    assert got[0] == "L1" and got.index("L3") > got.index("c2b"), ("S6", got)
    today = [c.name for c in [*lib, *clo]]
    assert today[0] == "L3", "MF-S6 did not show library-first"
    print(f"  S6 merged by depth: {got}; MF-S6 today walks L3 first")


def s8() -> None:
    comp = {"plain_far": (1, False, 0, 3), "derived_near": (0, True, 0, 1),
            "ev": (1, False, 2, 1), "var": (1, False, 2, 4)}
    got = tether._lookup_order(list(comp), comp, "k")
    assert got[0] == "derived_near", ("S8: the gate is not first", got)
    assert got.index("var") < got.index("ev") < got.index("plain_far"), ("S8", got)
    today = sorted(comp, key=lambda s: (comp[s][1], comp[s][0], -comp[s][2], -comp[s][3], s))
    assert today[0] != "derived_near", "MF-S8 did not show the derived step first"
    print(f"  S8 {got}; MF-S8 today: {today}")


def _dom(values, alpha, counts):
    d = tether._PricedDomain(values)
    d.alpha, d.key, d.counts, d.note = alpha, "k", counts, None
    return d


def s9() -> None:
    only_unseen = lambda v: v == 7  # noqa: E731
    dom = _dom({2}, 10, {2: 1})
    assert tether.objective_step(only_unseen, 5, True, dom) == 6, "S9: the unseen not aimed at"
    assert tether.objective_gap(only_unseen, 5, True, dom) == 2
    assert tether.objective_step(only_unseen, 5, True, {2}) is tether.NOT_RESOLVED, "MF-S9"
    both = lambda v: v in (1, 4)  # noqa: E731
    dom2 = _dom({1}, 10, {1: 1})
    assert tether.objective_step(both, 5, True, dom2) == 4, "S9: least-known did not pick unseen"
    two = lambda v: v in (3, 7)  # noqa: E731
    want = min((3, 7), key=lambda v: FR.draw_key("k", v))
    assert tether._priced_hit(two, 5, True, _dom({0}, 10, {0: 1})) == want, "F1: unseen tie"
    assert tether._priced_hit(two, 5, True, _dom({7, 3}, 10, {3: 1, 7: 1})) == want, "F1: shown"
    print(f"  S9 the unseen-only value is aimed at (today unresolved); with both, the unseen "
          f"nearer; F1 a tie at one distance goes to the draw ({want})")


def rows() -> None:
    code = ("import json, sys; sys.dont_write_bytecode = True; import arc_holdout;"
            "from test_entry import FakeWrapper;"
            "env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), 'fake');"
            "[ag.step() for _ in range(30)];"
            "print('ROWS ' + json.dumps([r['detail'] for r in led.rows() "
            "if r['event'] == 'stream'], default=repr))")
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    r = subprocess.run([sys.executable, "-B", "-c", code], env=env, capture_output=True,
                       text=True, check=False, stdin=subprocess.DEVNULL)
    assert r.returncode == 0, r.stderr[-3000:]
    got = json.loads([ln for ln in r.stdout.splitlines() if ln.startswith("ROWS ")][-1][5:])
    assert got, "precondition: no stream row on the fake game"
    for d in got:
        assert d["site"] in ("library_merge", "lookup_order", "stream_share"), d
        assert d["winner_rank"] is None or d["winner_rank"] <= d["walked_total"], d
        assert set(d["stop"].values()) <= {0, 1}, d
    print(f"  ROWS {len(got)} stream rows, sites {sorted({d['site'] for d in got})}")


def main() -> None:
    s4()
    s6()
    s8()
    s9()
    rows()
    print("a1 group 2: OK")


if __name__ == "__main__":
    main()
