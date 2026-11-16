"""A LEVER BY KIND (TETHER_KIND_LEVER, default ON; the reviewer r1965; r1963 4's pre-named next
step: contact routes taken, count goals still never met).
  L1  no action is known to move the goal's reading here, but the delta table saw one move the
      same reading on ANOTHER object the wanted way: CONTACT_ROUTE realises that move (not the
      touch), and a kind_lever_route row names the other slot, the action and the direction
  L2  the delta table's moves go the wrong way, or only on the goal's own object, or on another
      reading: no kind lever; the touch, as before
  L3  of two kind levers, the one seen move the reading more often is tried first
  MF-L1 TETHER_KIND_LEVER OFF: the touch, no kind_lever_route row -> RED as required
  L4  gridworld 12 steps ON and OFF both pass the gate
Seconds.
    python tests/test_kind_lever.py
"""
from __future__ import annotations

import os
import sys
from types import SimpleNamespace

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gate  # noqa: E402
import gridworld  # noqa: E402
import interface as IFace  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def agent():
    env = world.bind(gridworld.family("default", 0))
    led = ledger.Ledger()
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
    ag.step()
    return ag, led


def routed(ag, led, slot, before, delta):
    """`delta`: action -> {(ctx, slot, rel): (n, total)}. BECOME on a slot the table moved is
    realised as the action that moved it; BECOME on the goal's own slot is never known."""
    asked = []

    def realise(intent, *_a, **_k):
        asked.append(intent)
        if intent.kind == IFace.TOUCH:
            return SimpleNamespace(action="ACTION_TOUCH", unmapped=False)
        if intent.kind == IFace.BECOME and intent.subject != slot:
            for a, d in delta.items():
                if any(k == intent.subject for (_c, k, _r) in d):
                    return SimpleNamespace(action=a, unmapped=False)
        return None
    ag.iface.realise = realise
    ag.iface.table = {a: {"delta": d} for a, d in delta.items()}
    ag._route_memo = None
    ag._rel_partner = lambda _s: None
    ag._goal_target = lambda s, b: b[s] + 1
    ag.env.observe = lambda: dict(before)
    n0 = len(led.rows())
    a = ag._hyp_route(slot, dict(before))
    rows = led.rows()[n0:]
    return (a, [r for r in rows if r.get("event") == "kind_lever_route"],
            [r for r in rows if r.get("event") == "contact_route"], asked)


def main() -> int:
    assert tether._KIND_LEVER is True and tether._CONTACT_ROUTE is True, "the arms default ON"
    ag, led = agent()
    before = {"o1.rem_n": 2, "o2.rem_n": 5, "o3.rem_n": 1, "o1.row": 3, "o2.row": 4}
    acts = tuple(ag.env.actions())
    assert len(acts) >= 2, acts
    a1, a2 = acts[0], acts[1]
    good = {a1: {((), "o2.rem_n", "OTHER"): (3, 3)}}
    a, kl, cr, _asked = routed(ag, led, "o1.rem_n", before, good)
    assert a == a1 and len(kl) == 1 and not cr, (a, kl, cr)
    d = kl[0]["detail"]
    assert d["other"] == "o2.rem_n" and d["action"] == a1 and d["direction"] == "+", d
    print(f"L1 no lever for o1.rem_n; {a1} moved o2.rem_n up 3 times: kind lever {a1}, one "
          "kind_lever_route row, no touch: GREEN")

    for name, delta in (("the wrong way", {a1: {((), "o2.rem_n", "OTHER"): (3, -3)}}),
                        ("its own object", {a1: {((), "o1.rem_n", "SELF"): (3, 3)}}),
                        ("another reading", {a1: {((), "o2.row", "OTHER"): (3, 3)}})):
        ag, led = agent()
        a, kl, cr, _asked = routed(ag, led, "o1.rem_n", before, delta)
        assert a == "ACTION_TOUCH" and not kl and cr, (name, a, kl, cr)
    print("L2 moves the wrong way, on its own object, or on another reading: no kind lever, the "
          "touch: GREEN")

    ag, led = agent()
    two = {a1: {((), "o3.rem_n", "OTHER"): (1, 1)}, a2: {((), "o2.rem_n", "OTHER"): (4, 6)}}
    a, kl, _cr, _asked = routed(ag, led, "o1.rem_n", before, two)
    assert a == a2 and kl[0]["detail"]["other"] == "o2.rem_n", (a, kl)
    print(f"L3 two kind levers: the one seen more often ({a2}, 4 times over 1) first: GREEN")

    tether._KIND_LEVER = False
    ag, led = agent()
    a, kl, cr, _asked = routed(ag, led, "o1.rem_n", before, good)
    tether._KIND_LEVER = True
    assert a == "ACTION_TOUCH" and not kl and cr, ("MF-L1", a, kl)
    print("MF-L1 the arm OFF: the touch, no kind_lever_route row -> RED (as required)")

    for on in (True, False):
        tether._KIND_LEVER = on
        env = world.bind(gridworld.family("default", 0))
        led3 = ledger.Ledger()
        ag3 = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                           led3)
        for _ in range(12):
            ag3.step()
        ag3.end_run("cap")
        v = gate.check(led3.rows())["verdict"]
        assert v == "pass", ("L4", on, v)
    tether._KIND_LEVER = True
    print("L4 gridworld 12 steps ON and OFF: both pass the gate: GREEN")
    print("kind_lever: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
