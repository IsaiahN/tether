"""BUILD 5 ITEM 19 BOX 3, Q3 (i): THE GROUP ROW IN THE PROPOSER (TETHER_GROUP_PROPOSE; the
reviewer 2026-11-05 r1216, r1218). The goal proposer offers the group row's FORM (_group_form, the
one copy the completion also prices) over its own candidate texts, priced by bits, so an
ALL-of-a-kind goal is proposable before any win. Seconds: test_group_row's agent, no win, the
proposer's texts narrowed.

MF-P1  the single "o5.row == o1.row" (both 3, o5 has no route) is refused "route first"; its group
       "ALL kind(o5): o5.row == o1.row" does not hold (o0.row is 2): it is offered, picked and held,
       one want per member but its anchor (the route is stubbed, as test_goal_both_sides does: route
       knowledge is not what is tested)
MF-P2  OFF: the group is not offered and nothing is held
And the completion's own group path is unchanged (test_group_row green).
The red is behavioural: TETHER_GROUP_PROPOSE=0 fails MF-P1.

    python tests/test_group_propose.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import test_group_row as G  # noqa: E402

tether = G.tether
TEXT = "o5.row == o1.row"


def propose(on: bool | None):
    ag, _atoms, st = G.agent()
    before = ag.trace[-1][2]
    assert before["o5.row"] == before["o1.row"] != before["o0.row"], "the panel"
    ag.wants.clear()
    ag._hyp, ag._hyp_tried, ag._hyp_exhausted = None, {}, None
    ag._inv_conditions = lambda _b: [TEXT]
    ag._hyp_route = lambda *_a: "a route"
    # the two stubs must agree: _route_first_set is "A superset of the slots that route", the
    # invariant E's group skip rests on (r1419 E(a), r1429) -- o0.row (a member) has an entry;
    # o5.row and o1.row have none, so the single is still refused "route first"
    ag._route_first_set = lambda _b: {"o0.row"}
    was = tether._GROUP_PROPOSE
    tether._GROUP_PROPOSE = was if on is None else on
    try:
        ag._hyp_propose(before)
    finally:
        tether._GROUP_PROPOSE = was
    return ag, [r for r in ag.led.rows() if r["event"] == "goal_hypotheses"][-1]["detail"]


def main():
    ag, row = propose(None)
    want = f"ALL kind(o5): {TEXT}"
    assert row.get("pick") == want and isinstance(ag._hyp and ag._hyp.get("cond"),
                                                  tether._Group), ("MF-P1: not held", row)
    assert row.get("refused", {}).get("route first: no slot of it has an entry") == 1, (
        "MF-P1: the single", row)
    slots = ag._hyp["slots"]
    assert "o1.row" not in slots and {"o0.row", "o5.row"} <= set(slots) and all(
        s in ag.wants for s in slots), ("MF-P1: wants", slots)
    assert row.get("route"), ("MF-P1: no route", row)

    _off, row_off = propose(False)
    assert row_off.get("pick") is None and not any(
        str(x.get("if", "")).startswith("ALL kind") for x in row_off.get("ranked", [])), (
        "MF-P2: a group offered OFF", row_off)
    # MF-P3 (r1219): a PAIR reading's group binds the subject only -- the partner o2 held fixed and
    # never a member -- and the completion forms it as it did at 30746eb
    ag3, atoms3, _st3 = G.agent()
    st3 = dict(ag3.trace[-1][2])
    pair = "o0.touches_o2 == 1"
    c = tether.compile_term.compile_candidate({"condition": pair}, atoms3)
    formed = ag3._group_form(pair, c, st3, set())
    assert formed is not None, "MF-P3: no pair group formed"
    ptext, pgrp = formed
    assert ptext == f"ALL kind(o0): {pair}" and pgrp.group.exclude == ("o2",) and all(
        p.slot.endswith(".touches_o2") and not p.slot.startswith("o2.") for p in pgrp.parts), (
        "MF-P3: the partner is not held fixed", ptext, [p.slot for p in pgrp.parts])
    near = {**st3, **{f"{m}.touches_o2": 1 for m in ("o0", "o1", "o3", "o4", "o5")}}
    assert ag3._group_holds(pgrp.group, near, pgrp.kind) is True, "MF-P3: all touch o2, not held"
    assert ag3._group_holds(pgrp.group, {**near, "o3.touches_o2": 0}, pgrp.kind) is False, (
        "MF-P3: one member off, still held")
    rows = [(near, True)] * 3 + [({**near, "o3.touches_o2": 0}, False)] * 3
    single = (0, 0, 0, 0, pair, c)
    assert any(x[4] == ptext for x in ag3._goal_groups([single], rows)), (
        "MF-P3: the completion does not form the pair group")
    print(f"test_group_propose: pass (MF-P1 the single refused route-first; {want!r} held on "
          f"{len(slots)} member slots, route {row['route']!r}; MF-P2 OFF none; MF-P3 {ptext!r} "
          f"with o2 fixed and excluded, held / not per member, formed at the completion)")


if __name__ == "__main__":
    main()
