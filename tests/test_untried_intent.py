"""BUILD 4 ITEM 16b, THE UNTRIED FORMED INTENT (TETHER_UNTRIED_INTENT; the reviewer 2026-11-05
r1189; Fig 8 :39). At a held hypothesis's slot with no residual and no rival, the first formed
intent (in the order formed) not yet pressed in this situation enters 7h's exit contest. Seconds:
test_intent_predict's fixture (a gridworld agent stepped twice), the record set through its door.

MF-U1  formed A (pressed here, through _note_formed) and B (formed, never pressed here): through
       choose, the contest offered "untried:goal" with B, and, taking it when offered, the exit is
       untried:goal, an untried_intent row naming B, B pressed
MF-U2  every formed intent pressed here: nothing offered, and "every formed intent tried here"
       said ONCE over two asks; a formed intent untried here that does not realise is NOT tried,
       so with one of those nothing is offered and nothing is said
MF-U3  the goal slot has a residual (not static): nothing offered
The red is behavioural, the arm OFF on this tree: TETHER_UNTRIED_INTENT=0 fails MF-U1.

    python tests/test_untried_intent.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import interface as IFace  # noqa: E402
import test_intent_predict as tp  # noqa: E402

S = tp.S
A = IFace.Intent(IFace.BECOME, S, "-")
B = IFace.Intent(IFace.TOUCH, object="o1")
PRESS = {"BECOME o0.row -": "up", "TOUCH o1": "right"}


def agent(static: bool = True):
    ag = tp.agent(met=False)
    ag.gamma.is_settled = lambda *_a: False              # the bound inc is a candidate: one rival
    ag.iface.realise = (lambda w, *_a, **_k: IFace.Realisation(PRESS[w.says()], why="fixture")
                        if w.says() in PRESS else None)
    ag._hyp = {"slots": [S], "acted": {}}
    ag._goal_static = {S} if static else set()
    ag._note_formed(A)                                   # A: formed and pressed in this situation
    ag._formed.setdefault(ag._route_said(B), (ag.cycle, B))   # B: formed, never pressed here
    return ag


def rows(ag):
    return tp.rows(ag, "untried_intent")


def main():
    ag = agent()
    pick, offered = ag._choice, []

    def choice(site, slot, opts, *a, **k):
        if site == "exit":
            offered.append([o[0] for o in opts])
            if any(o[0] == "untried:goal" for o in opts):
                return "untried:goal"
        return pick(site, slot, opts, *a, **k)
    ag._choice = choice
    act, by = ag.choose(ag.trace[-1][2])
    got = [r for r in rows(ag) if r.get("intent")]
    assert by == "untried:goal" and act == "right" and len(got) == 1 and \
        got[0]["intent"] == ag._route_said(B), (
            "MF-U1: the untried formed intent was not offered or not taken", by, act, offered, got)
    print(f"  MF-U1 offered {offered}; {by}: {got[0]['intent']} as {act}, formed at "
          f"{got[0]['formed_at']}")
    ag2 = agent()
    ag2._note_formed(B)
    before = ag2.trace[-1][2]
    # the fixture's two real steps formed an intent no stub realises: untried here, so NOT tried
    assert ag2._untried_ready(before) is None and not rows(ag2), (
        "MF-U2: an unrealised untried intent was said tried", rows(ag2))
    for _at, w in list(ag2._formed.values()):
        ag2._note_formed(w)
    assert ag2._untried_ready(before) is None and ag2._untried_ready(before) is None
    said = [r for r in rows(ag2) if r.get("intent") is None]
    assert len(said) == 1, ("MF-U2: 'every formed intent tried here' not said exactly once", said)
    print(f"  MF-U2 every formed intent tried here: nothing offered, said once "
          f"({said[0]['formed']}); an unrealised untried one is not 'tried'")
    ag3 = agent(static=False)
    assert ag3._untried_ready(ag3.trace[-1][2]) is None and not rows(ag3), "MF-U3"
    print("  MF-U3 the goal slot has a residual: nothing offered")
    print("test_untried_intent OK")


if __name__ == "__main__":
    main()
