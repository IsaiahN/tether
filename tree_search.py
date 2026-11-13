"""10d STEP 2: A TREE IS SEARCHED TOP-DOWN, ONE TIER AT A TIME (the reviewer 2026-11-12;
Isaiah 12:41 "f(g(h(i(...))))", 12:51 necessity first, 15:15 "it can start now"; DESIGN_STEP10 10d).

The mint already holds tier 1: the flat chain and its depth-one trees, ordered by step 8 (source,
sense, shape of the gap). This module deepens them. A tree's open leaf -- the second slot a node
reads raw -- is replaced by a computed sub-tree over THAT slot, one tier down, and the result is
priced against the slot's history before anything below it is tried (Fig 4 :13-15, the round trip
per tier). Best-first by an optimistic bound, with the exact stop of step 8's P5 one level up: when
the least bound still waiting is at or over min(base, best total), nothing waiting can pay or beat
the best, so the walk ends (fail-first: Haralick & Elliott 1980).

Nothing here knows the agent. The caller hands in four callables:
  children(tree) -> the trees one tier deeper (ordered: the caller's order is the tiebreak)
  bound(tree)    -> a lower bound on any tree reached from it (its own cost: deeper only costs more)
  total(tree)    -> the bargain's whole price (cost + what it leaves unexplained)
  depth(tree)    -> the tree's tier
and gets back the best tree that beats `base` (or None) with per-tier stats. The order decides
which tree is seen first; it never refuses one the walk reaches (a cut is the budget's, counted).
"""
from __future__ import annotations

import heapq
import itertools
from collections.abc import Callable
from typing import Any


def deepen(roots: list, children: Callable[[Any], list], bound: Callable[[Any], float],
           total: Callable[[Any], float], depth: Callable[[Any], int], base: float,
           budget: int, max_tier: int | None = None) -> tuple[Any, dict]:
    """Best-first over the trees reached from `roots`, one tier per expansion.

    Returns (best tree with total < base, or None; stats). stats: priced (totals computed),
    expanded, per_tier {tier: priced}, tier_reached, frontier_stop (bool), budget_spent (bool).
    `budget` counts priced trees (the bargain's work); `max_tier` is a ceiling only (None: the
    purse and the stop decide)."""
    tie = itertools.count()
    heap: list = [(bound(r), next(tie), r) for r in roots]
    heapq.heapify(heap)
    best, best_total = None, base
    stats = {"priced": 0, "expanded": 0, "per_tier": {}, "tier_reached": 0,
             "frontier_stop": False, "budget_spent": False}
    while heap:
        b, _n, tree = heapq.heappop(heap)
        if b >= best_total:
            # EXACT: every tree still waiting has a bound >= this one, and deeper only costs
            # more, so none can pay (b >= base) or beat the best (b >= best_total)
            stats["frontier_stop"] = True
            break
        if stats["priced"] >= budget:
            stats["budget_spent"] = True
            break
        t = total(tree)
        d = depth(tree)
        stats["priced"] += 1
        stats["per_tier"][d] = stats["per_tier"].get(d, 0) + 1
        stats["tier_reached"] = max(stats["tier_reached"], d)
        if t < best_total:
            best, best_total = tree, t
        if max_tier is not None and d >= max_tier:
            continue
        kids = children(tree)
        if kids:
            stats["expanded"] += 1
        for k in kids:
            kb = bound(k)
            if kb < best_total:
                heapq.heappush(heap, (kb, next(tie), k))
    return best, stats


def term_depth(term: Any) -> int:
    """A gamma.Term's tier: 1 for a chain with no operand tree, +1 per nested operand_term."""
    d, t = 1, term
    while getattr(t, "operand_term", None) is not None:
        d, t = d + 1, t.operand_term
    return d


def open_leaf(term: Any) -> tuple[Any, ...]:
    """The path to a tree's deepest node that reads its second slot RAW (operand set, no
    operand_term): the leaf one tier down replaces. () when the tree has no such leaf."""
    path, t = [], term
    while t is not None:
        path.append(t)
        if t.operand_term is None:
            return tuple(path) if (len(path) > 1 and t.operand) else ()
        t = t.operand_term
    return ()


def replace_leaf(term: Any, sub: Any) -> Any:
    """The tree with its open leaf's raw second slot fed by `sub` (a one-atom term, unbound or
    naming a further slot): the leaf node L=(atoms, operand=b) becomes (atoms, operand=b,
    operand_term=sub). Rebuilt bottom-up so every node stays a frozen Term."""
    from gamma import Term
    path = open_leaf(term)
    if not path:
        return None
    leaf = path[-1]
    node = Term(leaf.atoms, origin=leaf.origin, operand=leaf.operand, guard=leaf.guard,
                guard_ref=leaf.guard_ref, operand_term=sub)
    for parent in reversed(path[:-1]):
        node = Term(parent.atoms, origin=parent.origin, operand=parent.operand,
                    guard=parent.guard, guard_ref=parent.guard_ref, operand_term=node)
    return node
