"""O2, NESTING WITH A BUDGET (TETHER_GUARD_NEST, default ON; BUILD_SEQUENCE_FUTURE_STATE §5 "O2:
nesting with a budget and a guard on nesting depth"; the reviewer 2026-11-14 "guards that hold
combined conditions (guard-join pricing lands with O2)"). A guard condition may be a junction of two
CONDITIONS (routed junction keys), read recursively; nothing deeper than GUARD_NEST_DEPTH is built
or read. MECHANICS ONLY, in the style of test_implies_bond.py: a gridworld agent whose slot types
and history are set by hand. Seconds.

  N1  the truth table of +:((⇒:a|b))|((∥:c|c)) on all eight truth combinations of a, b, c is
      ((not a) or b) and c; an unresolved reading reads False for the key AND for its ¬
  N2  a depth-3 combination is refused with the counted reason "nesting depth", nothing stored,
      and a hand-inserted depth-3 key reads False (nothing past the budget is read)
  N3  a combined key is offered only where it sorts R strictly better than each part (states
      counted), and its price is at least the sum of its parts' descriptions plus a bond
  MF-N1 tether._GUARD_NEST = False -> no combined key is built, offered or read -> RED as required
  N4  gridworld 12 steps ON and OFF both pass the gate

    python tests/test_guard_nest.py
"""
from __future__ import annotations

import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import itertools  # noqa: E402
import math  # noqa: E402

import gamma  # noqa: E402
import gate  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

A, B, C, Y = "o0.row", "o1.row", "o2.row", "o3.row"


def agent():
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                      ledger.Ledger())
    ag.slot_types = {**ag.slot_types, A: "PRED", B: "PRED", C: "PRED", Y: "PRED"}
    return ag


def main() -> int:
    assert tether._GUARD_NEST is True and tether.GUARD_NEST_DEPTH == 2, "the arm defaults ON"
    # N1: +((a⇒b))|(c), c the condition ∥:c|c (c either c: c itself, as a key)
    ag = agent()
    ag._route_junction("⇒", A, B)
    ag._route_junction("∥", C, C)
    kab, kc = f"⇒:{A}|{B}", f"∥:{C}|{C}"
    key = ag._jk_combine("+", kab, kc)
    assert key == f"+:({kab})|({kc})" and ag._jk_depth(key) == 2, ("N1 built", key)
    table = {(a, b, c): ag._jc_holds(key, {A: a, B: b, C: c})
             for a, b, c in itertools.product((False, True), repeat=3)}
    want = {(a, b, c): ((not a) or b) and c for a, b, c in table}
    assert table == want, ("N1 truth table", table)
    s_un = {A: True, B: tether.NOT_RESOLVED, C: True}
    assert ag._jc_holds(key, s_un) is False and ag._jc_holds("¬" + key, s_un) is False, \
        ("N1 unresolved is not a negation", s_un)
    print(f"N1 {key}: {sum(table.values())}/8 true, exactly ((not a) or b) and c; "
          "unresolved reads False for k and ¬k: GREEN")

    # N2: depth 3 refused, counted; a forced depth-3 key reads nothing
    ag._route_junction("+", A, C)
    kac = f"+:{A}|{C}"
    n0 = ag._guard_nest_why["nesting depth"]
    d3 = ag._jk_combine("∥", key, kac)
    deep = f"∥:({key})|({kac})"
    assert d3 is None and deep not in ag._junction_conds \
        and ag._guard_nest_why["nesting depth"] == n0 + 1, ("N2 refused", d3,
                                                             dict(ag._guard_nest_why))
    ag._junction_conds[deep] = ("∥", key, kac)          # forced past the budget by hand
    s_t = {A: True, B: True, C: True}
    assert ag._jc_holds(key, s_t) is True and ag._jc_holds(kac, s_t) is True \
        and ag._jc_holds(deep, s_t) is False, ("N2 nothing past the budget is read",)
    del ag._junction_conds[deep]
    print(f"N2 depth {1 + ag._jk_depth(key)} refused: reasons {dict(ag._guard_nest_why)}; "
          "a forced depth-3 key reads False: GREEN")

    # N3: offered only where it separates R strictly better than each part.
    # Y's two routed keys k1 = ≡:a|y-ish? -- use two truth junctions routed to Y.
    ag3 = agent()
    ag3._route_junction("+", A, Y)        # k1 = +:o0.row|o3.row   (a and y)
    ag3._route_junction("∥", B, Y)        # k2 = ∥:o1.row|o3.row   (b or y)
    k1, k2 = f"+:{A}|{Y}", f"∥:{B}|{Y}"
    assert ag3._junction_of.get(Y) == {k1, k2}, ag3._junction_of

    def row(a, b, y):
        return ({A: a, B: b, Y: y}, "a", y, None, None)
    # R: (a, b, y) = (1,0,1) and (1,0,1). Outside: (0,0,1) (k1 F, k2 T) and (1,1,0) (k1 F, k2 T)
    # and (0,1,1). k1 = a and y holds on R. A part alone sorts some states wrongly; check counts.
    robs = [row(True, False, True), row(True, False, True)]
    outside = [row(False, True, True), row(True, True, False)]
    hist = robs + outside
    ag3.history = lambda slot: hist if slot == Y else []
    off = ag3._jk_offer(robs, Y)
    sc = {k: ag3._jc_score(hist, robs, [ag3._jc_value(k, s) for s, *_ in hist],
                           [ag3._jc_value(k, s) for s, *_ in robs]) for k in (k1, k2)}
    nest = [k for k in off if ag3._jk_nested(k)]
    # k1 (a and y) already sorts all four (R true; outside (0,1,1) F, (1,1,0) F) -> nothing
    # combined can be strictly better than k1: no combined key may be offered
    assert sc[k1] == len(hist) and not nest, ("N3 not strictly better -> not offered", sc, off)
    print(f"N3a k1 already sorts {sc[k1]}/{len(hist)}: combined keys offered {nest}: GREEN")
    # now a history where neither part alone sorts everything but a+b combination does:
    # k1 = a and y, k2 = b or y. R: (1,1,1). outside: (1,0,1) (k1 T, k2 T) and (0,1,1) (k1 F,
    # k2 T) and (1,1,0) (k1 F, k2 T). k1 4-of-... -> use k2' = b and y instead.
    ag4 = agent()
    ag4._route_junction("+", A, Y)        # k1 = a and y
    ag4._route_junction("+", B, Y)        # k3 = b and y
    k3 = f"+:{B}|{Y}"
    robs4 = [row(True, True, True), row(True, True, True)]
    outside4 = [row(True, False, True), row(False, True, True)]
    hist4 = robs4 + outside4
    ag4.history = lambda slot: hist4 if slot == Y else []
    sc4 = {k: ag4._jc_score(hist4, robs4, [ag4._jc_value(k, s) for s, *_ in hist4],
                            [ag4._jc_value(k, s) for s, *_ in robs4]) for k in (k1, k3)}
    off4 = ag4._jk_offer(robs4, Y)
    ck = f"+:({k1})|({k3})"
    assert ck in off4 and ag4._jk_nested(ck), ("N3b offered", off4, sc4)
    cs = ag4._jc_score(hist4, robs4, [ag4._jc_value(ck, s) for s, *_ in hist4],
                       [ag4._jc_value(ck, s) for s, *_ in robs4])
    assert cs > max(sc4.values()), ("N3b strictly better", cs, sc4)
    # the ∥ and ⇒ joins of the same parts do not sort better, so they are not offered
    assert f"∥:({k1})|({k3})" not in off4 and f"⇒:({k1})|({k3})" not in off4, off4
    # pricing: the combined key's description >= sum of its parts' + one bond (term_bits' term)
    refs = len(off4)
    parts = ag4._jk_bits(k1, refs) + ag4._jk_bits(k3, refs)
    bond = tether.term_bits(2, 0, 3) - tether.term_bits(1, 0, 3)
    assert math.isclose(ag4._jk_bits(ck, refs), parts + bond) and bond > 0, ("N3 price",)
    g = gamma.JUNCTION_GUARD
    whole = tether._guard_bits(g, 1, refs) + ag4._jk_nest_bits(g, ck, refs)
    each = tether._guard_bits(g, 1, refs) + ag4._jk_nest_bits(g, k1, refs)
    assert ag4._jk_nest_bits(g, k1, refs) == 0.0 and whole >= each + ag4._jk_bits(k3, refs), \
        ("N3 guard price", whole, each)
    print(f"N3b parts sort {sc4}, {ck} sorts {cs}/{len(hist4)}: offered {off4}; price "
          f"{whole:.3f} bits >= part {each:.3f} + {ag4._jk_bits(k3, refs):.3f}: GREEN")
    # a third pass: the offered combined key is in the pool, and joining it again is depth 3
    n4 = ag4._guard_nest_why["nesting depth"]
    ag4._jk_offer(robs4, Y)
    assert ag4._guard_nest_why["nesting depth"] > n4, ("N2 in the offer path", ag4._guard_nest_why)
    print(f"N2b in the offer path: 'nesting depth' counted "
          f"{ag4._guard_nest_why['nesting depth'] - n4} times on re-offer: GREEN")

    # MF-N1: the arm OFF -> nothing built, offered or read
    tether._GUARD_NEST = False
    try:
        ag5 = agent()
        ag5._route_junction("+", A, Y)
        ag5._route_junction("+", B, Y)
        ag5.history = lambda slot: hist4 if slot == Y else []
        off5 = ag5._jk_offer(robs4, Y)
        built = ag5._jk_combine("+", k1, k3)
        ag5._junction_conds[ck] = ("+", k1, k3)          # forced: still not read as nested
        read5 = ag5._jc_holds(ck, {A: True, B: True, Y: True})
    finally:
        tether._GUARD_NEST = True
    assert not any(ag5._jk_nested(k) for k in off5) and built is None and read5 is False, \
        ("MF-N1", off5, built, read5)
    print(f"MF-N1 the arm OFF: offer {off5}, combine -> {built}, forced key reads {read5} "
          "-> RED as required")

    # N4: gridworld 12 steps ON and OFF both pass the gate
    for on in (True, False):
        tether._GUARD_NEST = on
        env = world.bind(gridworld.family("default", 0))
        led = ledger.Ledger()
        ag6 = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                           led)
        for _ in range(12):
            ag6.step()
        ag6.end_run("cap")
        v = gate.check(led.rows())["verdict"]
        assert v == "pass", ("N4: the gate refused", on, v)
    tether._GUARD_NEST = True
    print("N4 gridworld 12 steps ON and OFF: both pass the gate: GREEN")
    print("test_guard_nest OK")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
