"""BUILD 4 ITEM 15b, THE MET-GOAL CONFLICT READS 15a (TETHER_INTENT_WEIGH; the reviewer 2026-11-04
r1181; Fig 12 :126). Where the settled predictor on the met slot reads it, its verdict weighs the
conflict below the MIN_REPEAT bar; a refusal by prediction carries its support and is lifted when
settle demotes it (Fig 6 :44-45). Seconds: test_intent_predict's fixture (a gridworld agent stepped
twice, the conflict's inputs set by hand, ONE recorded undo).

MF-W1  a settled inc on the met slot predicts the press disturbs it: the route is refused
       "predicted_to_undo_met_goal" with support (inc, o0.row) after one undo; the decision row
       reads "weighed by prediction" and names the prediction
MF-W2  a settled idn predicts no change: no refusal, status "weighed by prediction: kept"
MF-W3  nothing settled reads the slot: no refusal, "conflict, not yet weighed" (MIN_REPEAT's rule)
MF-W4  the predicting term demoted, one real step (settle, then the lift): the route is open again,
       a route_lifted row, its _route_lifted entry reads "lifted"; a ground refusal stays
The red is behavioural, the arm OFF on this tree: TETHER_INTENT_WEIGH=0 fails MF-W1.

    python tests/test_intent_weigh.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import test_intent_predict as tp  # noqa: E402

S, WANT, PRESS = tp.S, tp.WANT, tp.PRESS


def agent(term: str | None):
    ag = tp.agent(met=True)
    if term is None:
        ag.gamma.is_settled = lambda *_a: False
    else:
        ag.bound[S] = term
        ag.gamma.is_settled = lambda n, s: (n, s) == (term, S)
    return ag


def decision(ag):
    got = tp.rows(ag, "decision")
    assert len(got) == 1, got
    return got[0]


def main():
    ag = agent("inc")
    ag._note_decision(WANT, PRESS)
    ref = {k: v for k, v in ag._route_refused.items() if k[0] == ag._route_said(WANT)}
    d = decision(ag)
    assert [v[0] for v in ref.values()] == ["predicted_to_undo_met_goal"] and \
        list(ref.values())[0][2] == ("inc", S) and d["status"].startswith(
            "weighed by prediction: route refused") and d["because"]["predicted"][
            "disturbs_met"] is True, ("MF-W1: the predicted disturbance did not weigh the "
                                      "conflict", ref, d)
    print(f"  MF-W1 one undo, refused {list(ref.values())[0]}; {d['status']!r}")
    ag2 = agent("idn")
    ag2._note_decision(WANT, PRESS)
    d2 = decision(ag2)
    assert not ag2._route_refused and d2["status"] == "weighed by prediction: kept" and \
        d2["because"]["predicted"]["read"] is True, ("MF-W2", ag2._route_refused, d2)
    print(f"  MF-W2 idn predicts no change: {d2['status']!r}, nothing refused")
    ag3 = agent(None)
    ag3._note_decision(WANT, PRESS)
    d3 = decision(ag3)
    assert not ag3._route_refused and d3["status"] == "conflict, not yet weighed", ("MF-W3", d3)
    print(f"  MF-W3 unread: {d3['status']!r}")
    route = next(iter(ref))
    ground = ("BECOME o9.row +", "ACTION2", None, route[3])
    ag._route_refused[ground] = ("undoes_met_goal", ag.cycle)
    ag.gamma.is_settled = lambda *_a: False             # settle demoted inc on o0.row
    ag.step()
    lifted = tp.rows(ag, "route_lifted")
    assert route not in ag._route_refused and ag._route_lifted.get(route, ("",))[0].startswith(
        "lifted: support inc demoted at") and [r["support"] for r in lifted] == ["inc"] and \
        ag._route_refused.get(ground, ("",))[0] == "undoes_met_goal", (
            "MF-W4: the demoted support did not lift its refusal", ag._route_refused,
            ag._route_lifted, lifted)
    print(f"  MF-W4 {ag._route_lifted[route][0]!r}; the ground refusal stays")
    print("test_intent_weigh OK")


if __name__ == "__main__":
    main()
