"""S6 (v), THE FACTORED PRICING, TETHER_INV_FACTOR (the reviewer 2026-10-19 15:35 item 3).

  B   every (condition, then-term) pair's cost from _inv_pairs is BIT-EQUAL (float.hex) to
      _inv_cost(f, [c], units), on a real Gamma under a planted code whose sums are order-sensitive
  K   _inv_pick equals sorting every pair and slicing: priced, the cheapest five, and every pair
      at the least total (a planted exact tie), in order
  MF  the same pair folded in a DIFFERENT order (the condition's values first) differs from
      _inv_cost on the planted case -- so B's bit equality can see an order change
  MF-L  the condition's truth vector dropped from the left cache's key (_inv_truth_key -> ())
      breaks bit-equality on the planted case -- so the key is what keeps the cache exact
  C   the code moving while the pairs are priced raises
(The real-firing check, pair by pair on life 18's first firing, is the (v) run's probe.)

    python tests/test_inv_factor.py
"""
from __future__ import annotations

import math
import os
import sys
from types import SimpleNamespace

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True


def main() -> int:
    sys.path.insert(0, os.path.join(_repo.ROOT, "conform"))
    import panel

    import gamma
    import tether
    import world
    assert tether.G_PRIOR_CODE and tether._INV_FACTOR, "run with the arms at their defaults (ON)"
    a = world.bind(panel._gridworld("gridworld_s2")[0]).atoms()
    g = gamma.Gamma(a, game="inv_factor")
    # a planted code: 1e16 then two small values sums differently left to right and right to left
    cost = {(x,): 1.0 for x in a}
    cost[(a[0],)] = 1e16
    cost[(a[1],)] = 0.1
    cost[(a[2],)] = 0.2
    planted = gamma.Code(cost, 0.3, 7.0, {})
    g.code = lambda: planted
    agent = SimpleNamespace(gamma=g)
    agent._bits = lambda *parts: tether.Agent._bits(agent, *parts)
    agent._inv_pairs = lambda *x: tether.Agent._inv_pairs(agent, *x)
    agent._inv_truth_key = tether.Agent._inv_truth_key
    units = tuple(gamma.Term((x,)) for x in a)
    fs = [(gamma.Term((a[0],)), [0.0, 1.0, 2.0]), (gamma.Term((a[1], a[2])), [0.5, 0.0, 0.25]),
          (gamma.Term((a[3],)), [0.0, 0.0, 0.0]), (gamma.Term((a[2], a[1], a[3])), [1.0, 1.0, 0.0])]
    # c0 and c4 are one term with one truth, all-true against f2's zero row: their two pairs with
    # f2 are the cheapest and tie exactly (K needs a real tie); every other pair pays an idb row
    plan = [((4, 5), [True, True, True]), ((5, 4), [True, False, True]),
            ((1,), [False, True, True]), ((2, 1), [True, True, False]),
            ((4, 5), [True, True, True])]
    conds = [(f"c{i}", SimpleNamespace(term=gamma.Term(tuple(a[j] for j in js))), truth)
             for i, (js, truth) in enumerate(plan)]
    idb = [3.0, 2.0, 5.0]
    hist = [None, None, None]
    flat = []
    for text, c, truth in conds:
        for f, fb in fs:
            left = sum(fb[i] if truth[i] else idb[i] for i in range(len(hist)))
            cst = tether.Agent._inv_cost(agent, f, [c], units)
            flat.append((cst + left, cst, left, text, c, f))
    pairs = list(tether.Agent._inv_pairs(agent, conds, fs, idb, units, hist))
    assert len(pairs) == len(flat) == len(conds) * len(fs)
    for (ci, fi, total, cst, left), x in zip(pairs, flat, strict=True):
        got = (total.hex(), cst.hex(), left.hex())
        assert got == (x[0].hex(), x[1].hex(), x[2].hex()), (ci, fi, x)
        assert conds[ci][0] == x[3] and fs[fi][0] is x[5]
    print("B", len(pairs), "pairs bit-equal to _inv_cost (float.hex)")                      # B
    flat_order = list(flat)
    flat.sort(key=lambda x: (x[0], x[1], x[3], x[5].name))
    priced, top, tied = tether.Agent._inv_pick(agent, conds, fs, idb, units, hist)
    want_tied = [x for x in flat if x[0] == flat[0][0]]
    assert priced == len(flat) and top == flat[:5] and tied == want_tied, (priced, top, tied)
    assert len(tied) >= 2, "K: the planted case must hold an exact tie at the least total"
    print("K the pick equals sort-and-slice: priced", priced, "cheapest 5 equal, tie set",
          len(tied))                                                                        # K
    bond = math.log2(max(tether.BONDS, 1))
    f, c = fs[0][0], conds[0][1]
    vf = [planted.cost[s] for s in gamma.Gamma.symbols(f, units)]
    vc = [planted.cost[s] for s in gamma.Gamma.symbols(c.term, ())]
    b = 0.0
    for v in vc + vf:          # the wrong order: the condition's values first
        b += v
    wrong = (b + planted.end) + (len(vf) + len(vc) - 1) * bond
    right = tether.Agent._inv_cost(agent, f, [c], units)
    assert wrong.hex() != right.hex(), ("MF: the planted case does not separate", wrong, right)
    print("MF the other summation order differs on the planted case:", right, "vs", wrong)  # MF
    agent._inv_truth_key = lambda _truth: ()         # the truth vector dropped from the key
    again = tether.Agent._inv_pairs(agent, conds, fs, idb, units, hist)
    broke = [(ci, fi) for (ci, fi, total, _c, _l), x in zip(again, flat_order, strict=True)
             if total.hex() != x[0].hex()]
    agent._inv_truth_key = tether.Agent._inv_truth_key
    assert broke, "MF-L: dropping the truth vector from left's key did not break bit-equality"
    print("MF-L the truth vector dropped from the left cache's key: bit-equality breaks on",
          len(broke), "pairs")                                                            # MF-L
    moved = gamma.Code(dict(cost), 0.3, 7.0, {})
    seq = iter([planted] + [moved] * 10)
    g.code = lambda: next(seq)
    try:
        list(tether.Agent._inv_pairs(agent, conds, fs, idb, units, hist))
    except RuntimeError as e:
        print("C the code moving mid-pricing raises:", e)                                   # C
    else:
        raise AssertionError("C: the moved code was not caught")
    print("inv_factor: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
