"""10d STEP 2, THE TIERED TREE SEARCH (tree_search.deepen; the reviewer 2026-11-12; DESIGN_STEP10
10d). A planted history where the target moves by X - (Y - Z): no depth-one tree explains it, the
depth-two tree does. deepen starts from the depth-one trees (tier 1, the mint's own), opens the raw
leaf one tier down, prices each tree against the history, and stops exactly.

TS1  deepen returns translate<subtract<X>(subtract<Y>(Z))> (zero residual), priced below base
TS2  EXACT: the same best as pricing every tree to tier 3 by brute force, with fewer priced
TS3  the frontier stop fires once the best is found (frontier_stop True, budget not spent)
MF-TS1 the tier ceiling held at 2 (no deepening) -> no tree pays -> TS1 RED (asserted)
Seconds: synthetic frames, the real _ops, no game.

    python tests/test_tree_search.py
"""
from __future__ import annotations

import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import arc_predict  # noqa: E402
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import tree_search  # noqa: E402
import world  # noqa: E402
from gamma import Ctx, Term  # noqa: E402

M, SLOTS = "o0.m", ("o1.a", "o2.b", "o3.c", "o4.d")
X, Y, Z = SLOTS[0], SLOTS[1], SLOTS[2]
VALS = [(9, 4, 1, 3), (7, 7, 3, 0), (2, 5, 8, 6), (6, 1, 2, 9), (4, 8, 5, 2), (8, 3, 6, 4)]
MISS_BITS = 8.0         # the price of one frame the tree predicts wrong (the bargain's unit here)


def build():
    held = {a.name: a for a in arc_predict.predict()}
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma([*env.atoms(), held["translate"], held["subtract"]],
                                       game="fam_default_0"), tether.Config(), ledger.Ledger())
    ag._memo = None
    return ag, held["translate"], held["subtract"]


def main() -> int:
    ag, tr, sb = build()
    frames = []
    m = 0
    for a, b, c, d in VALS:
        st = {M: m, X: a, Y: b, Z: c, SLOTS[3]: d}
        nxt = m + (a - (b - c))
        frames.append((st, nxt))
        m = nxt

    def total(t):
        miss = 0
        for st, nxt in frames:
            ops = ag._ops(t, st)
            got = None if ops is None else t.apply(st[M], Ctx(operands=ops))
            miss += got != nxt
        return gamma.Gamma.length(t) + MISS_BITS * miss

    def bound(t):
        return gamma.Gamma.length(t)

    def children(t):
        if not tree_search.open_leaf(t):
            return []
        leaf_slot = tree_search.open_leaf(t)[-1].operand
        return [k for k in (tree_search.replace_leaf(t, Term((sb,), operand=s))
                            for s in SLOTS if s != leaf_slot) if k is not None]

    roots = [Term((tr,), operand=X, operand_term=Term((sb,), operand=s))
             for s in SLOTS if s != X]
    base = MISS_BITS * len(frames)          # explaining nothing: every frame missed
    best, st = tree_search.deepen(roots, children, bound, total, tree_search.term_depth,
                                  base, budget=500)
    want = tree_search.replace_leaf(roots[0], Term((sb,), operand=Z))
    print(f"  best: {best.name if best else None} total {total(best) if best else None}"
          f" (base {base}); stats {st}")
    ok1 = best == want and total(best) < base
    print(f"TS1 the depth-two tree is found and pays: {'GREEN' if ok1 else 'RED'}")
    # brute force to tier 3
    every = list(roots) + [k for r in roots for k in children(r)]
    bf = min(every, key=lambda t: (total(t), t.name))
    ok2 = total(bf) == total(best) and st["priced"] <= len(every)
    print(f"TS2 exact: brute force best {bf.name} total {total(bf)}; deepen priced"
          f" {st['priced']} of {len(every)}: {'GREEN' if ok2 else 'RED'}")
    ok3 = st["frontier_stop"] and not st["budget_spent"]
    print(f"TS3 the frontier stop ends the walk: {'GREEN' if ok3 else 'RED'}")
    flat, st2 = tree_search.deepen(roots, children, bound, total, tree_search.term_depth,
                                   base, budget=500, max_tier=2)
    red = flat is None or total(flat) >= total(want) + MISS_BITS
    print(f"  ceiling 2: best {flat.name if flat else None}; stats {st2}")
    print(f"MF-TS1 no deepening (tier ceiling 2): {'RED (as required)' if red else 'GREEN'}")
    assert ok1 and ok2 and ok3 and red
    print("tree_search: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
