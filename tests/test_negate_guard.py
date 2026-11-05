"""BUILD 3, ¬ WIRED (TETHER_NEGATE_GUARD; the reviewer 2026-11-04 r1055 "negate over a PRED term";
Operators Table :58 "a refutation is a negation"). A routed junction key k is a PRED; ¬k holds where
k is resolved and false. MECHANICS ONLY, NO GAME OCCASION YET: composer.window_test never settles ¬,
and no ≡ / ⋛ junction settles on our panels, so the fixture is test_bond_terms' gridworld agent with
one slot's history set by hand. Seconds.

MF-N1  R is where o0.row and o1.row DIFFER: the routed ≡ key is false on R, so ¬≡ is offered on the
       guard, and a ¬-guarded term applies its chain where they differ, the identity where they are
       the same, and the identity where a reading is unresolved (an unknown is not a negation)
MF-N2  R is where they are the SAME: ≡ itself is offered and ¬≡ is not
MF-N3  nsm.read_node says "a negated condition, routed to the guard offer" for ¬, a listed reason
MF-N4  (r1160) in MF-N1's case ≡ is false on R, so ¬≡ is offered IN PLACE of ≡, and ≡ is recorded
       on a ROUTE "polarity" row ("false on R -> offered as ¬k"), not offered
The red is behavioural, the arm OFF on this tree: TETHER_NEGATE_GUARD=0 fails MF-N1.

    python tests/test_negate_guard.py
"""
from __future__ import annotations

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
KEY = f"≡:{min(X, Y)}|{max(X, Y)}"


def agent(hist):
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                      ledger.Ledger())
    ag.history = lambda slot: hist if slot == Y else []
    ag._route_junction("≡", X, Y)
    return ag


def row(y, x):
    return ({Y: y, X: x}, "a", y, None, None)


def main():
    hist = [row(1, 3), row(2, 5), row(3, 3), row(4, 4)]
    ag = agent(hist)
    off = ag._guards_once(hist[:2], Y, [])
    assert "¬" + KEY in off[6] and off[1][-1] == gamma.JUNCTION_GUARD, (
        "MF-N1: the ¬ key is not offered", off[6])
    pol = [e.detail for e in ag.led._entries if e.event == "polarity"]
    assert off[6] == ["¬" + KEY] and [(d["key"], d["offered"]) for d in pol] == [
        (KEY, "¬" + KEY)], ("MF-N4: k is offered beside ¬k, or not recorded", off[6], pol)
    inc = next(a for a in ag.gamma.atoms if a.in_type == a.out_type and a.name != "idn")
    t = gamma.Term((inc,), guard=gamma.JUNCTION_GUARD, guard_ref="¬" + KEY)

    def run(state):
        return t.apply(1, ag._eval_ctx(Y, state, action="a", operands=(), guard_ref="¬" + KEY))
    plain = gamma.Term((inc,)).apply(1, ag._eval_ctx(Y, {Y: 1, X: 3}, action="a", operands=()))
    differ, same, unknown = run({Y: 1, X: 3}), run({Y: 1, X: 1}), run({Y: 1})
    assert differ == plain != 1 and same == 1 and unknown == 1, (
        "MF-N1 guard", differ, same, unknown, plain)
    print(f"  MF-N1 R where they differ: offered {off[6]}; ¬-guarded {inc.name}: differ -> "
          f"{differ}, same -> {same}, unresolved -> {unknown} (identity)")
    hist2 = [row(1, 1), row(2, 2), row(3, 5), row(4, 7)]
    on = agent(hist2)._guards_once(hist2[:2], Y, [])
    assert on[6] == [KEY], ("MF-N2", on[6])
    print(f"  MF-N2 R where they are the same: offered {on[6]} only")
    print(f"  MF-N4 ≡ false on R: offered {off[6]} in its place; recorded {pol[0]['reads']!r}")
    atoms = {a.name: a for a in ag.gamma.atoms}
    st = nsm.say_term(gamma.Term((inc,)))
    got = nsm.read_node(f"([{st}] ¬ [{st}])", atoms)
    assert isinstance(got, compile_term.Refusal) and nsm.listed(got.reason) and \
        "a negated condition, routed to the guard offer" in got.reason, ("MF-N3", got)
    print(f"  MF-N3 translator: {got.reason!r}")
    print("test_negate_guard OK")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
