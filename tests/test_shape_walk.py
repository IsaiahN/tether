"""STEP 8b-2: THE ORDERED WALK (Gamma.ordered_closure + shape_order; TETHER_SHAPE_WALK; the reviewer
2026-11-12 r1838, DESIGN_STEP8 B4/B5). Over the ARC atom set, under ten minutes (Isaiah 11-12).

  SW1     NOTHING IS REFUSED: with no budget and no stop, ordered_closure yields exactly the set
          enumerate_closure yields, on several type pairs at depth 3 and 4.
  SW2     THE SHAPE COMES FIRST: with the key for a gap on `col`, the yields come out in
          non-increasing E (wanted readings touched), and the first yield touches the gap.
  MF-SW2  enumerate_closure's shortest-first order breaks SW2's ordering on the same pair
          (the order this piece replaces).
  SW3     THE FRONTIER STOP IS EXACT: with bound = atom count and stop at 2, every one-atom
          term is still yielded, the walk ends by `frontier_stop`, and it yields fewer terms
          than the walk without a stop.
  MF-SW3  with the stop ignored, the walk does not end early (yields everything).

    python tests/test_shape_walk.py
"""
from __future__ import annotations

import json
import os
import sys
import time

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
sys.path.insert(0, _repo.ROOT)

import arc_atoms  # noqa: E402
import arc_predict  # noqa: E402
import gamma  # noqa: E402
import shape_order  # noqa: E402
from gamma import Gamma  # noqa: E402

PAIRS = (("OBJECT", "POSITION", 4), ("POSITION", "PRED", 3), ("val", "val", 3))


def names(it) -> list[str]:
    return [t.name for t in it]


def main() -> int:
    t0 = time.time()
    g = Gamma(gamma.primitives_once(arc_atoms.three_spaces(arc_predict.predict())))
    with open(os.path.join(_repo.ROOT, "library", "given.json"), encoding="utf-8") as f:
        lib = json.load(f)["entries"]
    readings = shape_order.declared_readings(lib)

    # SW1: the same set, every pair
    for i, o, d in PAIRS:
        a = names(g.enumerate_closure(i, o, d, 10**9))
        b = names(g.ordered_closure(i, o, d, 10**9))
        assert sorted(a) == sorted(b), (i, o, d, len(a), len(b))
        assert len(set(b)) == len(b), ("duplicate yield", i, o)
        print(f"  SW1: {i}->{o} depth {d}: the same {len(a):,} terms, none refused")

    # SW2: E non-increasing, first yield touches the gap
    want = shape_order.wanted("col")
    key = shape_order.make_order_key(want, readings)

    def e_of(name: str) -> int:
        touched: set = set()
        for a in name.split(" . "):
            touched |= readings.get(a, frozenset()) & want
        return len(touched)

    i, o, d = PAIRS[0]
    es = [e_of(n) for n in names(g.ordered_closure(i, o, d, 10**9, order_key=key))]
    assert es and es[0] > 0, ("SW2: the first yield does not touch the gap", es[:5])
    in_order = all(x >= y for x, y in zip(es, es[1:], strict=False))
    assert in_order, "SW2: yields not in non-increasing E"
    print(f"  SW2: {len(es):,} yields in non-increasing E (first E={es[0]}, last E={es[-1]})")
    old = [e_of(n) for n in names(g.enumerate_closure(i, o, d, 10**9))]
    assert not all(x >= y for x, y in zip(old, old[1:], strict=False)), "MF-SW2 did not fail"
    print("  MF-SW2: shortest-first is not in E order on the same pair (RED as required)")

    # SW3: the frontier stop
    full = names(g.ordered_closure(i, o, d, 10**9, order_key=key))
    st: dict = {}
    got = names(g.ordered_closure(i, o, d, 10**9, stats=st, order_key=key,
                                  bound_of=lambda ch: float(len(ch)), stop=lambda m: m >= 2))
    singles = {n for n in full if " . " not in n}
    assert singles <= set(got), ("SW3: a one-atom term below the stop was lost",
                                 sorted(singles - set(got))[:3])
    assert st.get("frontier_stop") and st.get("depth_exhausted"), st
    assert len(got) < len(full), (len(got), len(full))
    print(f"  SW3: stop at bound 2 kept all {len(singles)} one-atom terms, yielded "
          f"{len(got):,} of {len(full):,}, frontier_stop={st['frontier_stop']}")
    ign = names(g.ordered_closure(i, o, d, 10**9, order_key=key,
                                  bound_of=lambda ch: float(len(ch)), stop=lambda _m: False))
    assert len(ign) == len(full), "MF-SW3 did not fail"
    print("  MF-SW3: with the stop ignored the walk yields everything (RED as required)")
    print(f"shape_walk: OK ({time.time() - t0:.1f} s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
