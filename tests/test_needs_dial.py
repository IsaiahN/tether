"""C7 THE NEEDS DIAL (the reviewer 2026-11-10 r1638, r1640, r1641; Isaiah 11-06 answer 8), arm
TETHER_NEEDS_DIAL.

  N1  the even head start: with no outcomes, progress and explore weigh 1/2 each (w sums to 1)
  N2  learned per state: where progress paid near ruin, exploration's share falls when PRESSED;
      where exploring paid at ease, it rises when COMFORTABLE (MF: one state's outcomes do not
      move the other's weights)
  N3  the state is read off the record: a game loss this level, or most of its steps cut by the
      purse, is PRESSED; otherwise COMFORTABLE
  N4  the outcome books on the (state, need) the turn was taken in, paid only when bits were
      explained
  N5  the guard: the dial sets weights on the contested exits only; OFF it sets none
  N7  r1649 (TETHER_DIAL_RATE): the weight reads the RATE, never the paid count. MF explore 10
      paid of 100 turns against progress 2 of 2 gives progress the higher weight; OFF (017b282)
      the paid count backs explore
  N6  r1647: the risk reading per need is the lowest standing p of a line taken for it in this
      state, None before any; MF a line taken in the other state does not count; G4: the record
      says what it compared and why

    python tests/test_needs_dial.py
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

OPTS = ["goal", "distinguish", "system0"]


def _agent() -> tether.Agent:
    env = world.bind(gridworld.family("default", 0))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="dial"), tether.Config(),
                        ledger.Ledger())


def check_n1() -> None:
    d = _agent()._dial_weights(OPTS)
    assert d["w"] == {"progress": 0.5, "explore": 0.5}, d
    print("  N1: no outcomes: progress 0.5, explore 0.5")


def check_n2_n3() -> None:
    ag = _agent()
    assert ag._dial_state() == "comfortable"
    ag._dial[("pressed", "progress")] = [3, 3]
    ag._dial[("comfortable", "explore")] = [3, 4]
    calm = ag._dial_weights(OPTS)
    r_e, r_p = 4 / 6, 1 / 2                         # explore 3 of 4, progress unseen (even prior)
    assert calm["state"] == "comfortable" and calm["w"]["explore"] == round(r_e / (r_e + r_p), 4)
    assert ag._ex_need["distinguish"] > 0.5 > ag._ex_need["goal"], ag._ex_need
    ag._dial_lost[ag._lk()] += 1
    hard = ag._dial_weights(OPTS)
    r_p2, r_e2 = 4 / 5, 1 / 2                       # pressed: progress 3 of 3, explore unseen
    assert hard["state"] == "pressed" and hard["w"]["explore"] == round(r_e2 / (r_e2 + r_p2), 4)
    ag2 = _agent()
    for i in range(3):
        ag2._pd.append({"cyc": i, "lvl": ag2.level, "think": 1, "extra": 0,
                        "open": {("cut", i)} if i else set()})
    assert ag2._dial_state() == "pressed", "most steps cut by the purse is pressed"
    print(f"  N2-N3: comfortable -> explore {calm['w']['explore']}; after a game loss, pressed -> "
          f"explore {hard['w']['explore']}; two of three steps cut is pressed")


def check_n4() -> None:
    ag = _agent()
    ag._integral, ag._outstanding = 5.0, {"x": 5.0}
    ag._dial_last = ("comfortable", "explore")
    ag._ex_last = (ag._lk(), "distinguish", ag.pe_integral() - ag.outstanding(), ag.cycle)
    ag._outstanding = {"x": 4.0}
    ag._ex_settle()
    ag._dial_last = ("comfortable", "progress")
    ag._ex_last = (ag._lk(), "goal", ag.pe_integral() - ag.outstanding(), ag.cycle)
    ag._ex_settle()
    assert ag._dial[("comfortable", "explore")] == [1, 1], ag._dial
    assert ag._dial[("comfortable", "progress")] == [0, 1], "MF: an unpaid turn booked as paid"
    print("  N4: a turn that explained 1 bit books paid; one that explained none books a turn only")


def check_n5() -> None:
    ag = _agent()
    ag._dial_weights(["goal"])
    assert set(ag._ex_need) == {"goal"}, ag._ex_need
    keep, tether._NEEDS_DIAL = tether._NEEDS_DIAL, False
    try:
        off = _agent()
        for _ in range(3):
            off.step()
    finally:
        tether._NEEDS_DIAL = keep
    rows = [r["detail"] for r in off.led.rows()
            if r["event"] == "choice" and r["detail"].get("site") == "exit"]
    assert rows and not off._ex_need and all("_dial" not in d["bids"] for d in rows), rows[:1]
    print("  N5: the dial weighs the contested exits only; OFF it sets no weight")


def check_n6() -> None:
    ag = _agent()
    d0 = ag._dial_weights(OPTS)
    assert d0["risk"] == {"progress": None, "explore": None}, d0
    ag._dial_ex[("comfortable", "goal")] = [1, 4]
    ag._dial_ex[("comfortable", "probe:3a")] = [3, 4]
    ag._dial_ex[("comfortable", "distinguish")] = [2, 2]
    ag._dial_ex[("pressed", "goal")] = [0, 5]
    d = ag._dial_weights(OPTS)
    assert d["risk"] == {"progress": 0.25, "explore": 1.0}, "MF: " + repr(d["risk"])
    assert d["checked"] == "2 of 2 needs" and d["why"], d
    print(f"  N6: risk comfortable {d['risk']} (the pressed goal line at 0.0 not counted); the "
          f"record says what it compared and why")


def check_n7() -> None:
    ag = _agent()
    ag._dial[("comfortable", "explore")] = [10, 100]
    ag._dial[("comfortable", "progress")] = [2, 2]
    d = ag._dial_weights(OPTS)
    assert d["w"]["progress"] > d["w"]["explore"], "MF: the paid count backed the worse line"
    assert d["rate"] == {"progress": 0.75, "explore": round(11 / 102, 4)}, d["rate"]
    keep, tether._DIAL_RATE = tether._DIAL_RATE, False
    try:
        off = ag._dial_weights(OPTS)
    finally:
        tether._DIAL_RATE = keep
    assert off["w"]["explore"] > off["w"]["progress"] and "rate" not in off, off
    print(f"  N7: explore 10/100 vs progress 2/2: ON w {d['w']} (the rate); OFF w {off['w']} "
          f"(the paid count, 017b282)")


if __name__ == "__main__":
    for c in (check_n1, check_n2_n3, check_n4, check_n5, check_n6, check_n7):
        c()
    print("needs_dial: OK")
