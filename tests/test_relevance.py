"""PIECE 3, LIBRARY RELEVANCE (TETHER_RELEVANCE; the reviewer r1679, r1720; spec 5.10.8). Each check
is shown passing, then its must-fail (MF) is shown failing.

  R1  a term unused for many writes ranks below an equal-confidence term in use. MF: with no fade
      the two tie, and the tie goes by name
  R2  an untried term does not outrank one proven 10 times and in use. MF: read as used (fade 1,
      the never-used rule removed), it outranks
  R3  confidence values are unchanged: track_of before and after the relevance reads, and with the
      switch off, are equal
  R4  a used kernel term never loses rank to the fade: it keeps its no-fade relevance and stays
      level with an equal term in use. MF: out of the kernel, it drops below one in use
  R5  zero-is-off: TETHER_RELEVANCE off, note_use stamps nothing and retrieve is passed no relevance
  RC  the carry: a settle and a refute stamp term_w at the clock; replayed into a fresh Gamma, the
      evidence rows rebuild term_w equal to the writer's, an innate row included

    python tests/test_relevance.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
sys.path.insert(0, _repo.ROOT)

import gamma  # noqa: E402
import gridworld  # noqa: E402
import retrieval  # noqa: E402
import world  # noqa: E402

GAP = {"varies": [], "arity": 1, "varies_types": ()}


def fresh(w_now=1000, h=0.5):
    env = world.bind(gridworld.family("default", 0))
    g = gamma.Gamma(env.atoms(), game="g")
    at = {a.name: a for a in g.atoms}
    names = []
    for pair in (("inc", "dbl"), ("dbl", "inc")):
        t = gamma.Term((at[pair[0]], at[pair[1]]))
        g._install(t, seq=0, residual=None)
        names.append(t.name)
    g.book["store_writes"] = w_now
    g.store_seed = h
    return g, names


def lib(g, names):
    return {n: g.library[n] for n in names}


def order(g, names, rel=True):
    return retrieval.retrieve(lib(g, names), GAP, track=g.track_of, youth=g.youth_of,
                              relevance=g.relevance_of if rel else None)


def main() -> int:
    assert gamma._RELEVANCE, "precondition: TETHER_RELEVANCE on (its default)"
    # R1
    g, (a, b) = fresh()
    assert retrieval.fits(g.library[a], GAP, "val", "val") == retrieval.fits(
        g.library[b], GAP, "val", "val"), "precondition: equal fit"
    for n in (a, b):
        g.standing[n].confirmations = 3
    g.term_w[a], g.term_w[b] = 100, 1000         # a: used 900 writes ago; b: in use
    ra, rb = g.relevance_of(a), g.relevance_of(b)
    got = order(g, [a, b])
    assert ra < rb and got == [b, a], (ra, rb, got)
    nofade = sorted([a, b])
    assert order(g, [a, b], rel=False) == nofade and g.track_of(a) == g.track_of(b)
    print(f"R1 equal confidence {g.track_of(a):.3f}: the term in use {rb:.3f} ranks before the one "
          f"unused for 900 of 1000 writes {ra:.3f}; MF no fade: a tie, broken by name ({nofade})")

    # R2
    g, (p, u) = fresh()
    g.standing[p].confirmations = 10
    g.term_w[p] = 1000
    rp, ru = g.relevance_of(p), g.relevance_of(u)
    assert order(g, [p, u]) == [p, u] and rp > ru, (rp, ru)
    g.term_w[u] = 1000                           # the defect: the untried term read as used
    mf = g.relevance_of(u)
    assert order(g, [p, u]) == [u, p] and mf > rp, (mf, rp)
    print(f"R2 proven x10 in use {rp:.3f} ranks before untried {ru:.3f} (youth only); MF read as "
          f"used, the untried term reads {mf:.3f} and outranks it")

    # R3
    g, (a, b) = fresh()
    g.standing[a].confirmations, g.standing[a].refusals = 4, 1
    g.term_w[a] = 500
    before = (g.track_of(a), g.track_of(b))
    for n in (a, b):
        g.relevance_of(n)
    after = (g.track_of(a), g.track_of(b))
    was = gamma._RELEVANCE
    gamma._RELEVANCE = False
    try:
        off = (g.track_of(a), g.track_of(b))
    finally:
        gamma._RELEVANCE = was
    assert before == after == off, (before, after, off)
    print(f"R3 confidence unchanged: {before[0]:.4f}, {before[1]:.4f} before, after the relevance "
          f"reads, and with the switch off")

    # R4
    def kernel_case(exempt):
        g, (k, n) = fresh()
        for x in (k, n):
            g.standing[x].confirmations = 3
        g.term_w[k], g.term_w[n] = 100, 1000     # k used long ago, n in use
        if exempt:
            g.kernel[k] = "inherited"
        return g.relevance_of(k), g.relevance_of(n), g.track_of(k) + g.youth_of(k), \
            order(g, [k, n])
    rk, rn, full, got = kernel_case(True)
    rk2, rn2, _f, got2 = kernel_case(False)
    assert rk == full == rn and rk2 < rn2 and got2[0] != got2[1], (rk, full, rn, rk2, rn2, got2)
    print(f"R4 a kernel term used 900 writes ago keeps its no-fade relevance {rk:.3f} = "
          f"confidence + youth, level with the same term in use {rn:.3f}; MF out of the kernel: "
          f"{rk2:.3f}, below {rn2:.3f}")

    # R5
    was = gamma._RELEVANCE
    gamma._RELEVANCE = False
    try:
        g, (a, _b) = fresh()
        g.note_use(a)
        g.settle(a)
        stamped = dict(g.term_w)
    finally:
        gamma._RELEVANCE = was
    import tether
    assert stamped == {} and tether.G_RELEVANCE is True, stamped
    print("R5 switch off: note_use and a settle stamp nothing (tether passes relevance only under "
          "G_RELEVANCE, read at import; gw12 identity with TETHER_RELEVANCE=0 is the run check)")

    # RC
    g1, (a, b) = fresh(w_now=200)
    g1.keep_evidence = True
    g1.settle(a)
    g1.book["store_writes"] = 350
    g1.refute(b)
    g1.book["store_writes"] = 420
    g1.settle(b)
    inn = next(iter(g1.innate)) if g1.innate else None
    if inn is not None:
        g1.book["store_writes"] = 450
        g1.refute(inn)                           # an innate term: a contradiction row
    want = dict(g1.term_w)
    g2, _n = fresh(w_now=900)
    g2.replay(list(g1.evidence))
    keys = [a, b] + ([inn] if inn is not None else [])
    assert {k: g2.term_w.get(k) for k in keys} == {k: want[k] for k in keys}, (g2.term_w, want)
    g3, _n = fresh(w_now=900)
    g3.replay([r[:-1] for r in g1.evidence])     # MF: rows with no clock reading
    assert any(g3.term_w.get(k) != want[k] for k in keys), "MF-RC: rows without w read the same"
    print(f"RC term_w rebuilt by replay equals the writer's: {a[:24]}.. {want[a]}, {b[:24]}.. "
          f"{want[b]}" + (f", innate {inn} {want[inn]}" if inn is not None else "")
          + "; MF rows stripped of their w: the stamps differ")
    print("relevance: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
