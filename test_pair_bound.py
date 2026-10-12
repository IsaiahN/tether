"""Commit A, A-EXACT: the pair bound's NECESSITY with the budget removed (the reviewer 2026-10-12
04:46 and 04:56 CDT). On one recorded gridworld cycle, every term reaching pays() -- chain
instances AND operand trees -- is collected with the arm off and on, with `work_budget` unbounded
so every instance is priced. Necessary means the two paying sets are IDENTICAL.
  a. arm ON in check mode: the real `_cannot_pay` agrees on every pair-refused instance;
  b. the paying set, trees included, is identical arm off vs on;
  m1. MUST FAIL: a pair holding a paying chain instance is forced into the refused set;
  m2. MUST FAIL: a refused pair's trees are skipped too (Isaiah 2026-09-24: a tree keeps its own
      bound). Each mutant needs material -- a paying instance (m1), a paying tree under a refused
      pair (m2) -- and the fixture fails loudly when the cycle has none.
    python test_pair_bound.py [member] [cycle]
"""
from __future__ import annotations

import copy
import inspect
import os
import sys
import time

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "conform"))
import panel  # noqa: E402

import gamma  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

MEMBER = sys.argv[1] if len(sys.argv) > 1 else "gridworld_s1"
# cycle 10 of gridworld_s1 (default arms): it has paying instances AND a tree paying under a
# refused instance, so both mutants have material; cycle 12 has no paying tree.
CYCLE = int(sys.argv[2]) if len(sys.argv) > 2 else 10
_SRC, _FIRST = inspect.getsourcelines(tether.Agent._mint)
TREE_LINES = {_FIRST + i for i, line in enumerate(_SRC) if "pays(bcost, bleft, base)" in line}
_pays0 = tether.pays


def _snapshot():
    g, seed = panel._gridworld(MEMBER)
    env = world.bind(g)
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"dt_default_{seed}"), tether.Config(),
                      ledger.Ledger())
    for _ in range(CYCLE):
        ag.step()
    return ag


def _parse(name: str):
    """gamma.Term.name: f"{atoms}<{operand}>?{guard}<{guard_ref}>", operand and guard optional."""
    base, _q, gpart = name.rpartition("?") if "?" in name else (name, "", "")
    g = gpart.split("<", 1)[0] or None
    r = gpart[:-1].split("<", 1)[1] if gpart.endswith(">") and "<" in gpart else None
    return base.split("<", 1)[0], g, r


def _paying(snap, arm: bool, check: bool = False, extra=None, skip_trees: bool = False):
    """One cycle stepped from a copy of `snap`, budget removed; the terms that paid."""
    ag = copy.deepcopy(snap)
    ag.cfg.work_budget = 10 ** 12
    tether._PAIR_BOUND, tether._PAIR_BOUND_CHECK = arm, check
    paid, refused_g = set(), set()
    real_pr, real_trees = tether.Agent._pair_refused, tether.Agent._trees

    def pays(cost, left, base):
        r = _pays0(cost, left, base)
        fr = sys._getframe(1)
        if r and fr.f_code.co_name == "_mint":
            tree = fr.f_lineno in TREE_LINES
            t = fr.f_locals["bt" if tree else "term"]
            paid.add((fr.f_locals.get("slot"), "tree" if tree else "inst", t.name))
        return r

    def pair_refused(self, cand, *a, **k):
        out = real_pr(self, cand, *a, **k)
        if extra is not None and cand.name == extra[0]:
            out = set(out) | {extra[1]}
        refused_g.update((cand.name, g) for g, _r in out)
        return out

    def trees(self, cand, bind, g, slot):
        if skip_trees and (cand.name, g) in refused_g:
            return []
        return real_trees(self, cand, bind, g, slot)

    tether.pays, tether.Agent._pair_refused, tether.Agent._trees = pays, pair_refused, trees
    try:
        ag.step()
    finally:
        tether.pays, tether.Agent._pair_refused, tether.Agent._trees = _pays0, real_pr, real_trees
        tether._PAIR_BOUND, tether._PAIR_BOUND_CHECK = False, False
    return paid, refused_g


if __name__ == "__main__":
    assert len(TREE_LINES) == 2, f"expected the two tree pays() sites, found {TREE_LINES}"
    t0 = time.perf_counter()
    snap = _snapshot()
    t1 = time.perf_counter()
    base, _ = _paying(snap, arm=False)
    on, refused_g = _paying(snap, arm=True, check=True)          # a: the assert mode runs here
    t2 = time.perf_counter()
    assert on == base, f"b: paying sets differ: lost {sorted(base - on)[:4]}, " \
                       f"gained {sorted(on - base)[:4]}"
    insts = sorted(p for p in base if p[1] == "inst")
    trees_paid = [p for p in base if p[1] == "tree"]
    assert refused_g, "no pair was refused on this cycle: the arm had nothing to do"
    assert insts, "m1 has no material: no chain instance paid on this cycle"
    assert trees_paid, "m2 has no material: no tree paid on this cycle"
    _slot, _kind, name = insts[0]
    atoms, g, r = _parse(name)
    m1, _ = _paying(snap, arm=True, extra=(atoms, (g, r)))
    assert (_slot, "inst", name) not in m1, \
        f"m1 MUST FAIL: forcing ({atoms}, {g}, {r}) refused did not lose {name}"
    m2, _ = _paying(snap, arm=True, skip_trees=True)
    lost_trees = {p for p in base - m2 if p[1] == "tree"}
    assert lost_trees, "m2 MUST FAIL: skipping a refused pair's trees lost no paying tree"
    t3 = time.perf_counter()
    print(f"test_pair_bound: {MEMBER} cycle {CYCLE}: paying {len(base)} ({len(insts)} instances, "
          f"{len(trees_paid)} trees); refused (chain, guard) {len(refused_g)}; a and b hold; "
          f"m1 lost {len(base - m1)} incl {name}; m2 lost {len(lost_trees)} trees. "
          f"snapshot {t1 - t0:.0f}s, a+b {t2 - t1:.0f}s, mutants {t3 - t2:.0f}s")
