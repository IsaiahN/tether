"""BUILD 3, THE BOND TERMS (TETHER_BOND_TERMS; the reviewer 2026-11-04 r1052, r1055, r1059, r1060).
A settled ≡ / ⋛ / + junction is a CONDITION, routed to the mint's guard offer as a JUNCTION guard.
MECHANICS ONLY, NO GAME OCCASION YET: on the panels we have no ≡ / ⋛ junction settles (gridworld 0,
ls20 0) and every + has value-typed operands (r1057), so the fixture is a gridworld agent whose one
slot's history is set by hand. Seconds.

MF-B1'  a routed ≡ key joins the slot's guard offer where it separates R, and a JUNCTION-guarded
        term applies its chain where the junction holds and is the identity where it does not
MF-B2   wording: MOLECULE_APPLY's reason says "condition: routed to the guard offer for <y>";
        nsm.read_node says "a condition, routed to the guard offer" for ≡ / ⋛ / +, "not wired as a
        term" for ¬ (AGENT|negate), "has no atom" only where implemented_by is empty (− ⇒)
MF-B3   ≡ is ONE key whichever operand comes first, and its guard price is the same
MF-B4   routing never puts a term in _mol_offers: nothing PRED-typed is offered as a value predictor
MF-B5   a key that holds on every row of R and on every row outside it is NOT offered; G unchanged
MF-B6   a JUNCTION guard is priced over the junction-key count, an ACTED guard over len(sep)
        + between two value-typed readings is refused for typing, and no key is stored
        ⋛ stores both orders (two keys)

    python tests/test_bond_terms.py
"""
from __future__ import annotations

import math
import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import compile_term  # noqa: E402
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import nsm  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

Y, X = "o0.row", "o1.row"


def agent():
    env = world.bind(gridworld.family("default", 0))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                        ledger.Ledger())


def row(y, x):
    return ({Y: y, X: x}, "a", y, None, None)


def main():
    # no arm assert here: with TETHER_BOND_TERMS=0 this test must fail BY BEHAVIOUR at B1'
    # (no JUNCTION guard offered), the red for a new arm (the reviewer r1064)
    ag = agent()
    # R: the rows where o0.row equals o1.row; outside R they differ, so ≡ separates R
    hist = [row(1, 1), row(2, 2), row(3, 5), row(4, 7)]
    robs = hist[:2]
    ag.history = lambda slot: hist if slot == Y else []
    before = ag._guards_once(robs, Y, [])
    g0 = len(before[1])
    assert not before[6] and gamma.JUNCTION_GUARD not in before[1], ("no key before routing",
                                                                    before[1])
    offers0 = {k: list(v) for k, v in ag._mol_offers.items()}
    why = ag._route_junction("≡", X, Y)
    assert why == f"condition: routed to the guard offer for {Y}", ("MF-B2 row", why)
    key = f"≡:{X}|{Y}" if X < Y else f"≡:{Y}|{X}"
    assert ag._junction_of[Y] == {key}, ("MF-B1' routed", ag._junction_of)
    after = ag._guards_once(robs, Y, [])
    assert after[6] == [key] and after[1][-1] == gamma.JUNCTION_GUARD, ("MF-B1' offered", after)
    g1 = len(after[1])
    assert g1 == g0 + 1, ("G", g0, g1)
    # the guarded term, through the agent's own context: holds -> the chain, else identity
    inc = next(a for a in ag.gamma.atoms if a.in_type == a.out_type and a.name != "idn")
    t = gamma.Term((inc,), guard=gamma.JUNCTION_GUARD, guard_ref=key)
    v_hold = t.apply(1, ag._eval_ctx(Y, {Y: 1, X: 1}, action="a", operands=(),
                                     guard_ref=key))
    v_not = t.apply(1, ag._eval_ctx(Y, {Y: 1, X: 9}, action="a", operands=(),
                                    guard_ref=key))
    plain = gamma.Term((inc,)).apply(1, ag._eval_ctx(Y, {Y: 1, X: 1}, action="a", operands=()))
    assert v_hold == plain and v_not == 1 and plain != 1, ("MF-B1' guard", inc.name, v_hold,
                                                           v_not, plain)
    # B3: the other order is the same one key, the same price
    ag._route_junction("≡", Y, X)        # the same junction spelled the other way round
    assert set(ag._junction_conds) == {key}, ("MF-B3 one key", sorted(ag._junction_conds))
    again = ag._guards_once(robs, Y, [])
    p1 = tether._guard_bits(gamma.JUNCTION_GUARD, g1 - 1, len(after[6]))
    p2 = tether._guard_bits(gamma.JUNCTION_GUARD, len(again[1]) - 1, len(again[6]))
    assert again[6] == [key] and p1 == p2, ("MF-B3 price", again[6], p1, p2)
    # B4: routing offers no value predictor
    assert {k: list(v) for k, v in ag._mol_offers.items()} == offers0, "MF-B4 _mol_offers moved"
    # B5: a key true on every row, inside R and out, does not separate; G unchanged
    ag3 = agent()
    flat = [row(1, 1), row(2, 2), row(3, 3), row(4, 4)]
    ag3.history = lambda slot: flat if slot == Y else []
    g_flat0 = len(ag3._guards_once(flat[:2], Y, [])[1])
    ag3._route_junction("≡", X, Y)
    after3 = ag3._guards_once(flat[:2], Y, [])
    assert not after3[6] and len(after3[1]) == g_flat0, ("MF-B5", after3[6], g_flat0)
    # B6: per-kind referent counts
    jb = tether._guard_bits(gamma.JUNCTION_GUARD, g1 - 1, len(after[6]))
    assert math.isclose(jb, math.log2(g1) + math.log2(len(after[6]) + 1)), ("MF-B6 J", jb)
    ab = tether._guard_bits(gamma.ACTED_SELF, g1 - 1, 3)
    assert math.isclose(ab, math.log2(g1) + math.log2(4)) and ab != jb, ("MF-B6 ACTED", ab, jb)
    # + between value-typed readings: refused for typing, nothing stored
    ag4 = agent()
    r4 = ag4._route_junction("+", X, Y)
    assert "not conditions (typing)" in r4 and not ag4._junction_of, ("+ typing", r4)
    # ⋛: both orders
    ag5 = agent()
    ag5._route_junction("⋛", X, Y)
    assert ag5._junction_of[Y] == {f"⋛:{X}|{Y}", f"⋛:{Y}|{X}"}, ("⋛ two keys", ag5._junction_of)
    # ∥ (r1073; mechanics only, no game occasion yet): a condition only between two truth-typed
    # readings, canonical (one key either order), offered where it separates R
    ag6 = agent()
    ag6.slot_types = {**ag6.slot_types, X: "PRED", Y: "PRED"}
    phist = [row(0, 0), row(0, 0), row(1, 0), row(0, 1)]
    ag6.history = lambda slot: phist if slot == Y else []
    r6 = ag6._route_junction("∥", X, Y)
    ag6._route_junction("∥", Y, X)
    pk = f"∥:{min(X, Y)}|{max(X, Y)}"
    assert r6 == f"condition: routed to the guard offer for {Y}" and \
        set(ag6._junction_conds) == {pk}, ("∥ routed, one key", r6, ag6._junction_conds)
    off6 = ag6._guards_once(phist[:2], Y, [])
    # ∥ is false on R here, so under TETHER_NEGATE_GUARD its negation is offered in its place
    want6 = ["¬" + pk] if tether._NEGATE_GUARD else [pk]
    assert off6[6] == want6 and off6[1][-1] == gamma.JUNCTION_GUARD, ("∥ offered", off6)
    ag7 = agent()
    r7 = ag7._route_junction("∥", X, Y)
    assert "not conditions (typing)" in r7 and not ag7._junction_of, ("∥ typing", r7)
    # B2: the translator's wording
    atoms = {a.name: a for a in ag.gamma.atoms}
    st = nsm.say_term(gamma.Term((inc,)))
    reasons = {}
    for bond in ("≡", "⋛", "+", "∥", "¬", "−", "⇒"):
        # the bond's symbol as the word: ¬ and − share the NSM word NOT, and ¬ is unary
        got = nsm.read_node(f"([{st}] {bond} [{st}])", atoms)
        assert isinstance(got, compile_term.Refusal), (bond, got)
        reasons[bond] = got.reason
        assert nsm.listed(got.reason), ("MF-B2 unlisted", bond, got.reason)
    assert all("a condition, routed to the guard offer" in reasons[b]
               for b in ("≡", "⋛", "+", "∥"))
    assert ("a negated condition, routed to the guard offer" if tether._NEGATE_GUARD
            else "not wired as a term") in reasons["¬"], reasons["¬"]   # r1055: ¬ wired
    assert "has no atom" in reasons["⇒"], reasons
    # r1160: − is implemented_by AGENT|subtract while TETHER_SUBTRACT is on (685b015)
    r_sub = reasons["−"]
    assert (r_sub.startswith("−: implemented_by AGENT|subtract") and
            r_sub.endswith("not wired as a term")) if nsm._SUBTRACT else \
        "− has no atom" in r_sub, r_sub
    assert not any("has no atom" in reasons[b] for b in ("≡", "⋛", "+", "¬")), reasons
    print(f"  MF-B1' {key} routed to {Y}; offered where it separates R: G {g0} -> {g1}; "
          f"JUNCTION-guarded {inc.name}: holds -> {v_hold}, not -> {v_not} (identity)")
    print(f"  MF-B2 row {why!r}; translator {reasons}")
    print(f"  MF-B3 ≡ either order -> one key {key}, price {p1:.4f} both ways")
    print("  MF-B4 routing left _mol_offers unchanged (no PRED-typed value predictor)")
    print(f"  MF-B5 a key true on every row is not offered: G {g_flat0} unchanged")
    print(f"  MF-B6 JUNCTION {jb:.4f} = log2(G) + log2(k+1) over {len(after[6])} key; "
          f"ACTED {ab:.4f} over its own 3 refs")
    print(f"  + value-typed: {r4!r}; ⋛ two keys {sorted(ag5._junction_of[Y])}")
    print(f"  ∥ between PRED readings: one key {pk} either order, offered where it separates R; "
          f"value-typed: {r7!r}")
    print("test_bond_terms OK")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
