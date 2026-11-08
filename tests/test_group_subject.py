"""G1, THE GROUP'S SUBJECTS (TETHER_GROUP_SUBJECT; the reviewer 2026-11-08 r1460, r1464, r1465): a
group row wants every member, so each PART's subject passes the singles' two subject checks -- the
self-moving check and the own clock -- or the whole row is refused. test_group_propose's panel: the
single "o5.row == o1.row" is refused route first and its group "ALL kind(o5): o5.row == o1.row" is
offered and picked (one want per member: o0.row, o5.row, ...).

G0   the arm ON with no clock: the group is picked, as test_group_propose's MF-P1
G1   a member's subject (o0.row) read self-moving: the row is refused "group: self-moving subject"
     and no group is picked
G2   a member's subject (o0.row) in the own clock: the row is refused
     "group: the own clock moves it"
MF1  G1 with the guard not consulted (the arm OFF): the group is picked again
MF2  G2 with the guard not consulted: the group is picked again

    python tests/test_group_subject.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import test_group_row as G  # noqa: E402

tether = G.tether
TEXT = "o5.row == o1.row"
WANT = f"ALL kind(o5): {TEXT}"


def propose(on: bool, moving=(), clock=()):
    ag, _atoms, _st = G.agent()
    before = ag.trace[-1][2]
    assert before["o5.row"] == before["o1.row"] != before["o0.row"], "the panel"
    ag.wants.clear()
    ag._hyp, ag._hyp_tried, ag._hyp_exhausted = None, {}, None
    ag._inv_conditions = lambda _b, **_k: [TEXT]
    ag._hyp_route = lambda *_a: "a route"
    ag._route_first_set = lambda _b: {"o0.row"}
    real_sm = ag._self_moving
    ag._self_moving = lambda sl, *a, **k: sl in moving or real_sm(sl, *a, **k)
    if clock:
        ag._own_clock_keys = lambda: frozenset(clock)
    was = tether._GROUP_SUBJECT
    tether._GROUP_SUBJECT = on
    try:
        ag._hyp_propose(before)
    finally:
        tether._GROUP_SUBJECT = was
    return [r for r in ag.led.rows() if r["event"] == "goal_hypotheses"][-1]["detail"]


def checks():
    out = {}
    r0 = propose(True)
    out["G0"] = (r0.get("pick") == WANT, r0)
    r1 = propose(True, moving=("o0.row",))
    out["G1"] = (r1.get("pick") != WANT
                 and r1["refused"].get("group: self-moving subject", 0) >= 1, r1)
    r2 = propose(True, clock=("o0.row",))
    out["G2"] = (r2.get("pick") != WANT
                 and r2["refused"].get("group: the own clock moves it", 0) >= 1, r2)
    return out


def main():
    out = checks()
    bad = {k: v[1] for k, v in out.items() if not v[0]}
    assert not bad, bad
    m1 = propose(False, moving=("o0.row",))
    assert m1.get("pick") == WANT, ("MF1: the self-moving guard is consulted with the arm OFF", m1)
    m2 = propose(False, clock=("o0.row",))
    assert m2.get("pick") == WANT, ("MF2: the own-clock guard is consulted with the arm OFF", m2)
    print(f"G0  the arm ON, no clock: {WANT!r} picked")
    n1 = out['G1'][1]['refused'].get('group: self-moving subject')
    print(f"G1  o0.row self-moving: refused {n1} 'group: self-moving subject', not picked")
    print(f"G2  o0.row in the own clock: refused "
          f"{out['G2'][1]['refused'].get('group: the own clock moves it')} "
          "'group: the own clock moves it', not picked")
    print("MF1 / MF2  the arm OFF: the group is picked under each stub")
    print("group_subject: 3 of 3, 2 must-fails")


if __name__ == "__main__":
    main()
