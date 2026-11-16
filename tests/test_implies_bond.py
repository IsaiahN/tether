"""O1, ⇒ WIRED (TETHER_IMPLIES_BOND, default ON; BUILD_SEQUENCE_FUTURE_STATE §5 "O1: ⇒ wired";
Operators Table :35-40). A settled ⇒ junction between two truth-typed readings is a CONDITION
routed to the guard offer, like + and ∥, but ORDERED. MECHANICS ONLY, modelled on the retired
test_bond_terms.py: a gridworld agent whose slot types and history are set by hand. Seconds.

  I1  between two PRED readings the key ⇒:a|b is routed to b's guard offer, _jc_holds gives
      (not a) or b on the four truth combinations, and it is offered where it separates R
  I2  direction matters: a⇒b and b⇒a are two keys, routed to different readings, and they differ
      on a state where a holds and b does not
  I3  refused for typing between value readings; no key stored
  I5  nsm.read_node says ⇒ is a condition routed to the guard offer (a listed reason)
  MF-I1 tether._IMPLIES_BOND = False -> the ⇒ key is not routed ("has no atom") -> RED as required
  I4  gridworld 12 steps ON and OFF both pass the gate

    python tests/test_implies_bond.py
"""
from __future__ import annotations

import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import compile_term  # noqa: E402
import gamma  # noqa: E402
import gate  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import nsm  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

Y, X = "o0.row", "o1.row"
ROUTED = f"condition: routed to the guard offer for {Y}"


def agent(pred=True):
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                      ledger.Ledger())
    if pred:
        ag.slot_types = {**ag.slot_types, X: "PRED", Y: "PRED"}
    return ag


def row(y, x):
    return ({Y: y, X: x}, "a", y, None, None)


def main() -> int:
    assert tether._IMPLIES_BOND is True and nsm._IMPLIES_BOND is True, "the arm defaults ON"
    # I1: X ⇒ Y routed to Y's offer, material implication on the four combinations
    ag = agent()
    why = ag._route_junction("⇒", X, Y)
    key = f"⇒:{X}|{Y}"
    assert why == ROUTED and ag._junction_of.get(Y) == {key}, ("I1 routed", why, ag._junction_of)
    table = {(u, v): ag._jc_holds(key, {X: u, Y: v}) for u in (False, True) for v in (False, True)}
    assert table == {(False, False): True, (False, True): True, (True, False): False,
                     (True, True): True}, ("I1 (not a) or b", table)
    # offered where it separates R: holds on R (rows 1-2), false outside (x true, y false)
    hist = [row(1, 1), row(0, 0), row(0, 1), row(0, 1)]
    ag.history = lambda slot: hist if slot == Y else []
    off = ag._guards_once(hist[:2], Y, [])
    assert off[6] == [key] and off[1][-1] == gamma.JUNCTION_GUARD, ("I1 offered", off)
    print(f"I1 {key} routed to {Y}; holds {table}; offered where it separates R: GREEN")

    # I2: the other direction is another key, on X's offer, and reads differently
    why2 = ag._route_junction("⇒", Y, X)
    rkey = f"⇒:{Y}|{X}"
    assert why2 == f"condition: routed to the guard offer for {X}", ("I2", why2)
    assert set(ag._junction_conds) == {key, rkey} and ag._junction_of.get(X) == {rkey}, \
        ("I2 two keys", sorted(ag._junction_conds), ag._junction_of)
    s = {X: True, Y: False}
    assert ag._jc_holds(key, s) is False and ag._jc_holds(rkey, s) is True, ("I2 direction", s)
    print(f"I2 {key} and {rkey} are two keys; on {s}: {key} False, {rkey} True: GREEN")

    # I3: value readings refused for typing, nothing stored
    ag3 = agent(pred=False)
    r3 = ag3._route_junction("⇒", X, Y)
    assert "not conditions (typing)" in r3 and not ag3._junction_of \
        and not ag3._junction_conds, ("I3 typing", r3)
    print(f"I3 value-typed: {r3!r}, no key: GREEN")

    # I5: the translator's wording
    atoms = {a.name: a for a in ag.gamma.atoms}
    inc = next(a for a in ag.gamma.atoms if a.in_type == a.out_type and a.name != "idn")
    st = nsm.say_term(gamma.Term((inc,)))
    got = nsm.read_node(f"([{st}] ⇒ [{st}])", atoms)
    assert isinstance(got, compile_term.Refusal) and nsm.listed(got.reason) \
        and "a condition, routed to the guard offer" in got.reason \
        and "has no atom" not in got.reason, ("I5 nsm", got)
    print(f"I5 nsm.read_node: {got.reason!r}: GREEN")

    # MF-I1: the arm OFF -> not routed
    tether._IMPLIES_BOND = nsm._IMPLIES_BOND = False
    try:
        ag4 = agent()
        r4 = ag4._route_junction("⇒", X, Y)
        got4 = nsm.read_node(f"([{st}] ⇒ [{st}])", atoms)
    finally:
        tether._IMPLIES_BOND = nsm._IMPLIES_BOND = True
    assert r4 == "⇒: bond has no atom (r896)" and not ag4._junction_of, ("MF-I1", r4)
    assert "has no atom" in got4.reason, ("MF-I1 nsm", got4)
    print(f"MF-I1 the arm OFF: {r4!r}, no key; nsm {got4.reason!r} -> RED as required")

    # I4: gridworld 12 steps ON and OFF both pass the gate
    for on in (True, False):
        tether._IMPLIES_BOND = nsm._IMPLIES_BOND = on
        env = world.bind(gridworld.family("default", 0))
        led = ledger.Ledger()
        ag5 = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                           led)
        for _ in range(12):
            ag5.step()
        ag5.end_run("cap")
        v = gate.check(led.rows())["verdict"]
        assert v == "pass", ("I4: the gate refused", on, v)
    tether._IMPLIES_BOND = nsm._IMPLIES_BOND = True
    print("I4 gridworld 12 steps ON and OFF: both pass the gate: GREEN")
    print("test_implies_bond OK")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
