"""CONTACT IS A ROUTE (TETHER_CONTACT_ROUTE, default ON; the reviewer r1963; T0b: 8 count-reading
goals never met, ended parked/stalled/untested with no known lever; cards v4 (c)+(g)).
  K1  no action is known to move the goal's reading: _hyp_route returns the realised TOUCH of the
      goal's object, and a contact_route row is written (once per cycle and slot)
  K2  the object isn't on the board, or the touch can't be realised: no route (None)
  K3  an action IS known to move the reading: that action, not the touch
  MF-K1 TETHER_CONTACT_ROUTE OFF: no route, no row -> RED as required
  K4  gridworld 12 steps ON and OFF both pass the gate
Seconds.
    python tests/test_contact_route.py
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


def routed(ag, led, slot, known=None, touch_ok=True):
    def realise(intent, *_a, **_k):
        if intent.kind == IFace.TOUCH:
            return SimpleNamespace(action="ACTION_TOUCH", unmapped=False) if touch_ok else None
        return SimpleNamespace(action=known, unmapped=False) if known else None
    ag.iface.realise = realise
    ag._route_memo = None
    ag._rel_partner = lambda _s: None
    ag._goal_target = lambda s, before: 1 + (before.get(s) or 0)
    n0 = len(led.rows())
    a = ag._hyp_route(slot, ag.env.observe())
    rows = [r for r in led.rows()[n0:] if r.get("event") == "contact_route"]
    return a, rows


def main() -> int:
    assert tether._CONTACT_ROUTE is True, "the arm defaults ON"
    ag, led = agent()
    state = ag.env.observe()
    slot = next(k for k in sorted(state) if k.startswith("o") and k.endswith(".col"))
    a, rows = routed(ag, led, slot)
    assert a == "ACTION_TOUCH" and len(rows) == 1, (a, rows)
    assert rows[0]["detail"]["object"] == slot.split(".")[0]
    print(f"K1 no known lever for {slot}: route = touch {rows[0]['detail']['object']}, one "
          "contact_route row: GREEN")
    a, rows = routed(ag, led, slot)
    assert a == "ACTION_TOUCH" and not rows, "K1: the row is once per cycle and slot"

    a, _r = routed(ag, led, "o999.col")
    assert a is None, ("K2: an object not on the board", a)
    a, _r = routed(ag, led, slot, touch_ok=False)
    assert a is None, ("K2: an unrealisable touch", a)
    print("K2 object off the board, or the touch unrealisable: no route: GREEN")

    a, rows = routed(ag, led, slot, known="ACTION_KNOWN")
    assert a == "ACTION_KNOWN" and not rows, (a, rows)
    print("K3 a known lever: that action, not the touch: GREEN")

    tether._CONTACT_ROUTE = False
    ag2, led2 = agent()
    a, rows = routed(ag2, led2, slot)
    tether._CONTACT_ROUTE = True
    assert a is None and not rows, ("MF-K1: OFF should give no route", a)
    print("MF-K1 the arm OFF: no route, no row -> RED (as required)")

    for on in (True, False):
        tether._CONTACT_ROUTE = on
        env = world.bind(gridworld.family("default", 0))
        led3 = ledger.Ledger()
        ag3 = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                           led3)
        for _ in range(12):
            ag3.step()
        ag3.end_run("cap")
        v = gate.check(led3.rows())["verdict"]
        assert v == "pass", ("K4", on, v)
    tether._CONTACT_ROUTE = True
    print("K4 gridworld 12 steps ON and OFF: both pass the gate: GREEN")
    print("contact_route: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
