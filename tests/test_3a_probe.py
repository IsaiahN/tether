"""BUILD 4 ITEM 16, 3a-PROBE (TETHER_3A_PROBE; the reviewer 2026-11-04 r1184; Fig 5 :12). 3a's named
probe acted on once per (slot, diagnosis). Seconds: test_intent_predict's fixture (a gridworld agent
stepped twice), a diagnosis handed to the queue by hand.

MF-P1  a slip ("repeat the intended act", the object meant o1): one real step, the exit contest
       taking the option when offered -- the exit is probe:3a, TOUCH o1 pressed (as "right"), a
       probe_taken row, and after settle a probe_result row naming where the press landed (none
       on gridworld: "not read")
MF-P2  "watch the actor; re-observe what it reached" on o0.row: one real step -- a probe_attend row,
       no press of its own, the queue emptied
MF-P3  "the outward/mint route" (model_too_small): probe_queued how routed, nothing queued
MF-P4  the same diagnosis twice: queued once
The red is behavioural, the arm OFF on this tree: TETHER_3A_PROBE=0 fails MF-P1 (the contest is
never offered it).

    python tests/test_3a_probe.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import interface as IFace  # noqa: E402
import test_intent_predict as tp  # noqa: E402

S = tp.S
SLIP = {"verdict": "slip", "next_probe": "repeat the intended act", "rows": [0], "t_last": 1}


def agent():
    ag = tp.agent(met=False)
    ag.gamma.is_settled = lambda n, s=None: (n, s) == ("inc", S)   # a real step asks with no slot
    real = ag.iface.realise
    ag.iface.realise = (lambda w, *a, **k: IFace.Realisation("right", why="fixture")
                        if w.says() == "TOUCH o1" else real(w, *a, **k))
    return ag


def main():
    ag = agent()
    ag._3a_aim[(ag._trace_epoch, 0)] = "o1"
    ag._probe_queue(S, SLIP)
    pick, offered = ag._choice, []

    def choice(site, slot, opts, *a, **k):
        if site == "exit":
            offered.append([o[0] for o in opts])
            if any(o[0] == "probe:3a" for o in opts):
                return "probe:3a"
        return pick(site, slot, opts, *a, **k)
    ag._choice = choice
    ag.step()
    taken, res = tp.rows(ag, "probe_taken"), tp.rows(ag, "probe_result")
    assert len(taken) == 1 and taken[0]["action"] == "right" and taken[0]["aim"] == "o1" and \
        len(res) == 1 and "landed" in res[0], ("MF-P1: the slip's named probe was not acted on",
                                               offered, taken, res)
    print(f"  MF-P1 offered {offered}; {taken[0]['probe']!r} as {taken[0]['action']} at "
          f"{taken[0]['aim']}; result: landed {res[0]['landed']!r}, {res[0]['outcome']!r}")
    ag2 = agent()
    ag2._probe_queue(S, {"verdict": "world_changed", "t_last": 1,
                         "next_probe": "watch the actor; re-observe what it reached"})
    ag2.step()
    att = tp.rows(ag2, "probe_attend")
    assert att and not ag2._3a_probes and not tp.rows(ag2, "probe_taken"), (
        "MF-P2: the re-observation was not attended to", att, ag2._3a_probes)
    print(f"  MF-P2 attended to {S}: {att[0]['probe']!r}, no press of its own")
    ag3 = agent()
    ag3._probe_queue(S, {"verdict": "model_too_small", "t_last": 1,
                         "next_probe": "the outward/mint route"})
    q = tp.rows(ag3, "probe_queued")
    assert len(q) == 1 and q[0]["how"] == "routed" and not ag3._3a_probes, ("MF-P3", q)
    print(f"  MF-P3 {q[0]['probe']!r}: how {q[0]['how']}, nothing queued")
    ag4 = agent()
    ag4._3a_aim[(ag4._trace_epoch, 0)] = "o1"
    ag4._probe_queue(S, SLIP)
    ag4._probe_queue(S, SLIP)
    assert len(ag4._3a_probes) == 1, ("MF-P4: queued twice", ag4._3a_probes)
    print("  MF-P4 the same diagnosis twice: queued once")
    print("test_3a_probe OK")


if __name__ == "__main__":
    main()
