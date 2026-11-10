"""BUILD 4 ITEM 14c, THE LANDING IN THOUGHT (TETHER_LA_LANDING; the reviewer 2026-11-05 r1189). A
look-ahead press reads its landing on the SIMULATED state from its realisation's coordinate; every
predictor on it is evaluated with that landing, and a held latch cause advances on it in thought.
Seconds: test_intent_predict's fixture (a gridworld agent stepped twice); a press aimed at o1's
cell (Interface._at), the real last landing set elsewhere (o9).

MF-L1  a held latch cause on o1 (14a): after one look-ahead press aimed at o1's cell, the cause
       holds on the NEXT simulated press (read from the chain, not the real trace)
MF-L2  a look-ahead press evaluates its predictor with the simulated landing o1, not the real
       last press's o9 (the evaluation context's landed, spied)
The red is behavioural, the arm OFF on this tree: TETHER_LA_LANDING=0 fails MF-L1.

    python tests/test_la_landing.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import test_intent_predict as tp  # noqa: E402
import tether  # noqa: E402

S = tp.S


def agent():
    ag = tp.agent(met=False)
    ag._last_landed = "o9"                       # the real last press landed elsewhere
    st = dict(ag.trace[-1][2])
    coord = ag.iface._at("o1", st, ag.iface.cell_of)
    assert coord is not None, "the fixture's o1 has no cell"
    return ag, st, coord


def main():
    ag, st, coord = agent()
    cause = tether.Cause("latch", S, "o1")
    act = ag.actions[0]
    out = ag._la_predict(st, act, [], set(), [0], coord)
    held = ag._cause_holds(cause, out, act, None)
    assert held, ("MF-L1: the latch did not advance on a press landed in thought",
                  ag._sim_parent.get(id(out)))
    print(f"  MF-L1 a look-ahead press at {coord} lands on o1 in thought: the latch on o1 holds "
          f"on the next simulated press")
    ag2, st2, coord2 = agent()
    seen = []
    real = ag2._eval_ctx

    def spy(*a, **k):
        seen.append(k.get("landed"))
        return real(*a, **k)
    ag2._eval_ctx = spy
    ag2._la_predict(st2, ag2.actions[0], [S], set(), [0], coord2)
    assert seen and seen[-1] == "o1", ("MF-L2: the predictor read the wrong press's landing",
                                       seen)
    print(f"  MF-L2 the predictor on the simulated press read landed {seen[-1]!r} (the real last "
          f"was 'o9')")
    print("test_la_landing OK")


if __name__ == "__main__":
    main()
