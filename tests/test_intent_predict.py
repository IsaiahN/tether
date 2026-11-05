"""BUILD 4 ITEM 15a, INTENT-LEVEL PREDICTION (TETHER_INTENT_PREDICT; the reviewer 2026-11-04 r1177;
Isaiah 09-29). (before, intent, after): the intent's press through the settled per-slot predictors,
computed only where the plan is already weighing an intent -- the met-goal conflict in
_note_decision -- and recorded there. Seconds: a gridworld agent stepped twice; o0.row bound to a
settled inc; the conflict's inputs (an undone count, a met objective) set by hand.

MF-I1  the weighed intent BECOME o0.row +, pressed as ACTION1 with a met objective on o0.row it
       has undone before: one intent_predict row, action ACTION1, o0.row predicted v -> v+1,
       disturbs_met True, its ms on the row
MF-I2  the same press with no live conflict (the objective not met): no intent_predict row
MF-I3  an intent with no realisation predicts None
The red is behavioural, the arm OFF on this tree: TETHER_INTENT_PREDICT=0 fails MF-I1.

    python tests/test_intent_predict.py
"""
from __future__ import annotations

import os
import sys
from types import SimpleNamespace

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gridworld  # noqa: E402
import interface as IFace  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

S = "o0.row"
WANT = IFace.Intent(IFace.BECOME, S, "+")
PRESS = SimpleNamespace(action="ACTION1", coord=None, unmapped=False)


def agent(met: bool):
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                      ledger.Ledger())
    ag.step()
    ag.step()
    ag.bound[S] = "inc"
    ag.gamma.is_settled = lambda n, s: (n, s) == ("inc", S)
    ag._undone = {(None, WANT.says(), S, None): 1}
    ag._res[S] = [0] * tether.MIN_REPEAT if met else [1]
    return ag


def rows(ag, event):
    return [r["detail"] for r in ag.led.rows() if r.get("event") == event]


def main():
    ag = agent(met=True)
    v = ag.trace[-1][2][S]
    ag._note_decision(WANT, PRESS)
    got = rows(ag, "intent_predict")
    want = (v + 1) % ag.alphabet[S]
    assert len(got) == 1 and got[0]["action"] == "ACTION1" and got[0]["changed"] == {
        S: [v, want]} and got[0]["disturbs_met"] is True and got[0]["ms"] >= 0, (
        "MF-I1: the weighed intent is not predicted", got)
    print(f"  MF-I1 {got[0]['intent']} as {got[0]['action']}: {got[0]['changed']}, "
          f"disturbs_met {got[0]['disturbs_met']}, {got[0]['ms']} ms")
    ag2 = agent(met=False)
    ag2._note_decision(WANT, PRESS)
    assert not rows(ag2, "intent_predict"), ("MF-I2: a row where nothing is weighed",
                                             rows(ag2, "intent_predict"))
    print("  MF-I2 no live conflict: no intent_predict row")
    ag2.iface = SimpleNamespace(realise=lambda *_a, **_k: None)
    assert ag2._intent_predict(ag2.trace[-1][2], WANT) is None, "MF-I3"
    print("  MF-I3 an unrealisable intent predicts None")
    print("test_intent_predict OK")


if __name__ == "__main__":
    main()
