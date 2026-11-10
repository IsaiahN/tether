"""(T)+(L)+(P): TIERS OF REACH AND THE KERNEL FLAG (the reviewer 2026-11-10 r1632, r1635; Isaiah
r1394, r1383), arms TETHER_REACH_TIER and TETHER_KERNEL. TIER_CAP is set to 3 here so a small
hand library crosses it.

  T1  inflow past the cap moves the lowest-reach unbound non-kernel term to tier 2, a reach_tier
      row; it stays in the library with every count (MF: the arm OFF moves nothing)
  T2  tier 2 is offered after tier 1 and only when nothing paid (MF: a payer holds it back)
  T3  a bound term never moves down, whatever its reach
  T4  a settled term can move down; its standing is untouched
  L1  a tier-2 term bound on a miss re-enters tier 1 with its entry cycle kept, and at the next
      inflow it falls before a fresher term (its reach is spread over its age)
  P1  a kernel term is never moved down nor crowded out (MF: the same term with the kernel arm
      OFF is moved, and is crowded out)
  P2  a kernel term is refuted like any other: refute and settle read no kernel flag (MF: a
      refute that skipped kernel terms is caught)

    python tests/test_tiers_kernel.py
"""
from __future__ import annotations

import os
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

PAIRS = [("inc", "dec"), ("inc", "inc"), ("dec", "dec"), ("dbl", "inc"), ("neg", "inc")]


def _hand(cap: int = 3) -> tether.Agent:
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="tiers"), tether.Config(),
                      ledger.Ledger())
    tether.TIER_CAP = cap
    ag.cycle = 0
    ag._reach_inflow()                   # the atoms enter at cycle 0 (all kernel)
    return ag


def _add(ag: tether.Agent, a: str, b: str) -> str:
    lib = ag.gamma.library
    return ag.gamma.accept(gamma.Term((lib[a].atoms[0], lib[b].atoms[0])), ag.cycle, "r").name


def _rows(ag: tether.Agent, ev: str) -> list:
    return [r["detail"] for r in ag.led.rows() if r["event"] == ev]


def _grow(ag: tether.Agent, pairs: list) -> list:
    names = []
    for a, b in pairs:
        ag.cycle += 1
        names.append(_add(ag, a, b))
        ag._reach_inflow()
    return names


def check_t1() -> None:
    ag = _hand()
    names = _grow(ag, PAIRS[:3])
    before = repr(ag.gamma.standing.get(names[0]))
    names += _grow(ag, PAIRS[3:4])
    moved = [d["term"] for d in _rows(ag, "reach_tier") if d["to"] == 2]
    assert moved == [names[0]], (moved, names)
    assert names[0] in ag.gamma.library and names[0] in ag._reach2
    assert repr(ag.gamma.standing.get(names[0])) == before
    keep, tether._REACH_TIER = tether._REACH_TIER, False
    try:
        assert list(ag._reach_pass(names, lambda: True)) == names, \
            "MF: the arm OFF still held tier 2 back"
    finally:
        tether._REACH_TIER = keep
    print(f"  T1: the fourth term past a cap of 3 moves the least-reached ({names[0]}) to tier 2; "
          f"still in the library, standing unchanged; OFF, nothing is held back")


def check_t2() -> None:
    ag = _hand()
    names = _grow(ag, PAIRS[:4])
    order = list(ag._reach_pass(names, lambda: False))
    assert order == names[1:] + names[:1], order
    assert _rows(ag, "reach_tier_second_pass")[-1]["offered"] == 1
    held = list(ag._reach_pass(names, lambda: True))
    assert held == names[1:], f"MF: tier 2 offered though tier 1 paid: {held}"
    print("  T2: tier 2 comes after tier 1 and only when nothing paid")


def check_t3() -> None:
    ag = _hand()
    first = _grow(ag, PAIRS[:3])
    ag.bound["x"] = first[0]
    nxt = _grow(ag, PAIRS[3:4])
    moved = [d["term"] for d in _rows(ag, "reach_tier") if d["to"] == 2]
    assert first[0] not in moved and moved == [first[1]], (moved, first, nxt)
    print(f"  T3: the bound {first[0]} stays; the next-least-reached {first[1]} moves")


def check_t4() -> None:
    ag = _hand()
    first = _grow(ag, PAIRS[:3])
    for _ in range(4):
        ag.gamma.settle(first[0], where=0, slot="x")
    st = ag.gamma.standing[first[0]]
    before = (st.settled_at, st.confirmations, st.misses, st.rejections)
    for n in first[1:]:
        ag._reach_uses[n] = 20          # the others bound often: the settled one is least reached
    nxt = _grow(ag, PAIRS[3:4])
    moved = [d["term"] for d in _rows(ag, "reach_tier") if d["to"] == 2]
    assert moved == [first[0]], (moved, first, nxt)
    st = ag.gamma.standing[first[0]]
    assert (st.settled_at, st.confirmations, st.misses, st.rejections) == before
    print(f"  T4: {first[0]} (settled_at {before[0]}, confirmations {before[1]}) moves down; its "
          f"standing is unchanged")


def check_l1() -> None:
    ag = _hand()
    names = _grow(ag, PAIRS[:4])
    old = names[0]
    born = ag._reach_born[old]
    ag.cycle += 10
    fresh = _grow(ag, [("dbl", "dec")])           # moves one more down, then the recall
    cand = ag.gamma.library[old]
    ag._take_pull(old, cand, "x")
    assert old not in ag._reach2 and ag._reach_born[old] == born
    assert [d for d in _rows(ag, "reach_tier") if d["term"] == old and d["to"] == 1]
    conf = ag.gamma.standing[old].confirmations
    ag._reach_inflow()                  # the recall is this cycle's intake: it does not move
    assert old not in ag._reach2
    ag._reach_uses[names[3]] = 20       # the one older term still in tier 1, bound often
    assert ag._reach_of(old) < ag._reach_of(fresh[0])
    ag.cycle += 1
    _grow(ag, [("neg", "dec")])
    moved = [d["term"] for d in _rows(ag, "reach_tier") if d["to"] == 2]
    assert moved[-1] == old, (moved, old, fresh)
    assert ag.gamma.standing[old].confirmations == conf
    print(f"  L1: {old} recalled keeps its entry cycle ({born}); at the next inflow it falls "
          f"before the fresher {fresh[0]}")


def check_p1() -> None:
    ag = _hand(cap=0)
    ag.cycle += 1
    _add(ag, "inc", "dec")
    ag._reach_inflow()
    moved = {d["term"] for d in _rows(ag, "reach_tier") if d["to"] == 2}
    assert not moved & set(ag.gamma.kernel), moved
    ag._crowd[("x", "inc")] = (ag.level, len(ag.gamma.library), tether.IDN, 0.0)
    ag.bound["x"] = tether.IDN
    assert not ag._crowd_blocked("x", "inc"), "a kernel claim was crowded out"
    keep, tether._KERNEL = tether._KERNEL, False
    try:
        off = _hand(cap=0)
        off.cycle += 1
        _add(off, "inc", "dec")
        off._reach_inflow()
        assert {d["term"] for d in _rows(off, "reach_tier") if d["to"] == 2}, \
            "MF: with the kernel arm OFF an atom should move"
        off._crowd[("x", "inc")] = (off.level, len(off.gamma.library), tether.IDN, 0.0)
        off.bound["x"] = tether.IDN
        assert off._crowd_blocked("x", "inc"), "MF: OFF, the atom should be held out"
    finally:
        tether._KERNEL = keep
    print("  P1: at a cap of 0 no kernel atom moves and none is crowded out; OFF, both happen")


def check_p2() -> None:
    import inspect
    ag = _hand()
    assert "inc" in ag.gamma.kernel
    ag.gamma.settle("inc", where=0, slot="x")
    hit = ag.gamma.refute("inc", where=1, slot="x")
    st = ag.gamma.standing["inc"]
    assert st.misses > 0 or st.rejections > 0 or hit, st
    for f in (gamma.Gamma.settle, gamma.Gamma.refute):
        assert ".kernel" not in inspect.getsource(f), f"{f.__name__} reads the kernel flag"
    real = gamma.Gamma.refute

    def skips(self, name, where=None, slot=None):
        return False if name in self.kernel else real(self, name, where, slot)
    gamma.Gamma.refute = skips
    try:
        g2 = _hand().gamma
        g2.settle("inc", where=0, slot="x")
        g2.refute("inc", where=1, slot="x")
        s2 = g2.standing["inc"]
        assert (s2.misses, s2.rejections) != (st.misses, st.rejections), \
            "MF: a refute that skips the kernel went unseen"
    finally:
        gamma.Gamma.refute = real
    print(f"  P2: the kernel atom inc is refuted (misses {st.misses}, rejections {st.rejections}); "
          f"settle and refute read no kernel flag")


if __name__ == "__main__":
    cap = tether.TIER_CAP
    try:
        for c in (check_t1, check_t2, check_t3, check_t4, check_l1, check_p1, check_p2):
            c()
    finally:
        tether.TIER_CAP = cap
    print("tiers_kernel: OK")
