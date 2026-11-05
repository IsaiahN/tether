"""BUILD 4 ITEM 15c, INTENT-LEVEL DISCRIMINATION (TETHER_INTENT_DISCRIMINATE; the reviewer
2026-11-04 r1184; Fig 2 :46). A slot's held rivals each predict the slot after the press each of its
intents realises to; the intent with the most distinct predictions (>= 2) enters 7h's exit contest
(read by the outstanding of the slot it aims at) and, when the contest picks it, is taken. Seconds:
test_intent_predict's fixture (a gridworld agent stepped twice), the rivals set by hand.

MF-D1  inc against idn on o0.row (a candidate), through choose, the contest taking the option when
       offered: the exit is discriminate:intent, a discriminate row, spread 2, the intent kept
MF-D2  two rivals that agree under every intent: nothing to offer
MF-D3  a settled slot off the held hypothesis: no rivals
MF-D4  the held hypothesis's own slot, its settled "stays" term (idn) against a Cause-guarded inc
       that holds only on ACTION2's press: the intent realised as ACTION2 (the second in order)
       is the one read, spread 2 (r1184; Fig 8 :39)
The red is behavioural, the arm OFF on this tree: TETHER_INTENT_DISCRIMINATE=0 fails MF-D1 (the
contest is never offered it).

    python tests/test_intent_discriminate.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import interface as IFace  # noqa: E402
import test_intent_predict as tp  # noqa: E402
import tether  # noqa: E402

S = tp.S
# two steps in, the delta table has not seen o0.row move, so nothing realises: the fixture hands
# each intent its press (as 15a's fixture hands its PRESS); 15c's choice is what is tested
PRESS = {"BECOME o0.row +": "ACTION1", "BECOME o0.row -": "ACTION2", "TOUCH o0": "ACTION3"}


def agent(settled: set, rv: dict | None = None):
    ag = tp.agent(met=False)
    ag.gamma.is_settled = lambda n, s=None: (n, s) in settled
    ag._hyp = None
    ag.iface.realise = (lambda w, *_a, **_k: IFace.Realisation(PRESS[w.says()], why="fixture")
                        if w.says() in PRESS else None)
    if rv is not None:
        real = ag._rivals
        ag._rivals = lambda s, hyp, guarded: rv if s == S else real(s, hyp, guarded)
    return ag


def main():
    ag = agent(set())
    lib = ag.gamma.library
    ag._rivals = (lambda s, hyp, guarded, real=ag._rivals:
                  {"inc": lib["inc"], "idn": lib["idn"]} if s == S else real(s, hyp, guarded))
    pick = ag._choice
    offered = []

    def choice(site, slot, opts, *a, **k):
        if site == "exit":
            offered.append([o[0] for o in opts])
            if any(o[0] == "discriminate" for o in opts):
                return "discriminate"
        return pick(site, slot, opts, *a, **k)
    ag._choice = choice
    act, by = ag.choose(ag.trace[-1][2])
    got = tp.rows(ag, "discriminate")
    assert by == "discriminate:intent" and len(got) == 1 and got[0]["spread"] == 2 and set(
        got[0]["rivals"]) == {"inc", "idn"} and ag._intent_now is not None, (
        "MF-D1: the rivals' disagreement was not offered or not taken", act, by, offered, got)
    print(f"  MF-D1 offered {offered}; {by}: {got[0]['intent']} as {act}, {got[0]['rivals']}")
    ag2 = agent(set(), {"inc": lib["inc"], "inc2": lib["inc"]})
    assert ag2._discrim_best(ag2.trace[-1][2]) is None, "MF-D2: rivals that agree offered"
    print("  MF-D2 rivals that agree: nothing offered")
    ag3 = agent({("inc", S)})
    ag3.bound[S] = "inc"
    assert ag3._rivals(S, set(), {S: ["idn"]}) == {}, "MF-D3: a settled slot has rivals"
    print("  MF-D3 a settled slot off the hypothesis: no rivals")
    ag4 = agent({("idn", S)})
    ag4.bound[S] = "idn"
    ag4._hyp = {"slots": [S]}
    key = "cause:test"
    ag4._invented[key] = tether.Cause("count", S, "ACTION2", 1)
    lib4 = ag4.gamma.library
    lib4["inc_on_a2"] = tether.Term(lib4["inc"].atoms, operand=lib4["inc"].operand,
                                    guard=tether.INVENTED_GUARD, guard_ref=key)
    best = ag4._discrim_best(ag4.trace[-1][2])
    assert best is not None and best[3].action == "ACTION2" and best[0] == 2 and set(
        best[4]) == {"idn", "inc_on_a2"}, (
        "MF-D4: the settled stays term was not tested against the held cause", best)
    print(f"  MF-D4 {best[2].says()} as {best[3].action}: {best[4]}, spread {best[0]}")
    print("test_intent_discriminate OK")


if __name__ == "__main__":
    main()
