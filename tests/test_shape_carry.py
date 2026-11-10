"""BUILD 5 ITEM 20, A SHAPE CARRIES AS ITS METHOD (TETHER_SHAPE_CARRY; the reviewer 2026-11-05
r1231, r1232, r1233; Fig 4 :22-24). A held completion goal's parts are shelved as their METHOD
form through the ONE M7 path (_goal_templates -> _shelve_one -> _inv_carry), with the reads a
form's text does not name (_goal_reads), re-invented on load by _reinvent_carried, and a carried
group is rebuilt BY FORM in the proposer. Seconds: test_group_row's agent and its private library;
a second, fresh agent loads what the first shelved.

MF-C1  RED FIRST: a group "ALL kind(o5): o5.row == o1.row", an order "o0.row == o4.row then
       o0.col == o4.col" and a count "NONE of kind EXTENT remain" (reads came/gone) each shelve a
       METHOD form ("ALL kind({o}): {o}.row == {x}.row", ...) and each re-invents on a fresh agent,
       none refused. OFF: no template, nothing carried
MF-C8  the CONTACT shape "o0.touches_o2 == 1": the library's own template keeps the partner
       ("{o}.touches_o2 == 1", a recording), so the method form is shelved instead,
       "{o}.touches_{x} == 1", with reads [touching]; it re-invents on the fresh agent
MF-C2  the fresh agent's proposer instantiates the carried group, which the compiler refuses, and
       rebuilds it BY FORM (_carried_groups -> _group_form): a _Group is held. OFF (the rebuild
       arm off on the same agent): no group held
MF-C4  a constant "o3.colour == 2" is refused by carry_check: no template, it stays in-game
(Connected is not carried yet: "connected" is no library reading, so carry_check refuses its form.)
The red is behavioural: TETHER_SHAPE_CARRY=0 fails MF-C1.

    python tests/test_shape_carry.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import test_group_row as G  # noqa: E402

tether = G.tether
SHAPES = [("ALL kind(o5): o5.row == o1.row", "ALL kind({o}): {o}.row == {x}.row", None),
          ("o0.row == o4.row then o0.col == o4.col",
           "{o}.row == {x}.row then {o}.col == {x}.col", None),
          ("NONE of kind EXTENT remain", "NONE of kind EXTENT remain", ["came", "gone"])]
CONTACT = ("o0.touches_o2 == 1", "{o}.touches_{x} == 1")
CONSTANT = "o3.colour == 2"


def shelve(ag, text: str, reads: list | None, n: int, tpl: dict | None = None) -> list:
    """The write path a completion takes: _goal_templates and _goal_reads, then _shelve_one."""
    lib = ag._inv_library()
    key = f"t_goal_{n}"
    ag._goal_text[key] = text
    ag._goal_meta[key] = {"met_state": "after", "level": ag.level, "parts": [text],
                          "templates": ag._goal_templates([text], tpl or {}, lib), "affects": []}
    rd = reads or (ag._goal_reads(None, text, lib) if tether._SHAPE_CARRY else None)
    if rd and tether._SHAPE_CARRY:
        ag._goal_meta[key]["reads"] = rd
    k0 = len(ag._inv_carry)
    ag._shelve_one(key, "test", {"won": 1, "lost": 0}, "test")
    return ag._inv_carry[k0:]


def propose(ag, on: bool) -> dict:
    before = ag.trace[-1][2]
    ag.wants.clear()
    ag._hyp, ag._hyp_exhausted, ag._hyp_tried = None, None, {}
    ag._inv_conditions = lambda _b, **_k: []
    ag._hyp_route = lambda *_a: "a route"
    ag._route_first_set = lambda _b: None
    was = tether._SHAPE_CARRY, tether._GROUP_PROPOSE
    tether._SHAPE_CARRY, tether._GROUP_PROPOSE = on, False
    try:
        ag._hyp_propose(before)
    finally:
        tether._SHAPE_CARRY, tether._GROUP_PROPOSE = was
    return [r for r in ag.led.rows() if r["event"] == "goal_hypotheses"][-1]["detail"]


def carry(on: bool | None) -> tuple:
    was = tether._SHAPE_CARRY
    tether._SHAPE_CARRY = was if on is None else on
    try:
        ag, _atoms, _st = G.agent()
        rows = [r for i, (t, _f, rd) in enumerate(SHAPES) for r in shelve(ag, t, rd, i)]
        contact = shelve(ag, CONTACT[0], None, 7, {CONTACT[0]: "{o}.touches_o2 == 1"})
        const = shelve(ag, CONSTANT, None, 9)
        ag2, _a2, _s2 = G.agent()
        got = (ag2._reinvent_carried(rows + contact) if rows + contact
               else {"reinvented": 0, "refused": 0})
        last = [r for r in ag2.led.rows() if r["event"] == "invention_carried"]
        return rows, contact, const, got, (last[-1]["detail"] if last else {}), ag2
    finally:
        tether._SHAPE_CARRY = was


def main():
    off, _ct, _c, _g, _d, _a = carry(False)
    assert off == [], ("MF-C1 (red first): OFF carried", off)

    rows, contact, const, got, detail, _ag2 = carry(None)
    forms = [r["template"] for r in rows]
    assert forms == [f for _t, f, _r in SHAPES], ("MF-C1: the method forms", forms)
    assert rows[2].get("reads") == ["came", "gone"], ("MF-C1: the count's reads", rows[2])
    names = [r["name"] for r in rows + contact]
    assert detail.get("refused") == [] and set(names) <= set(detail.get("reinvented", [])), (
        "MF-C1/C8: not re-invented", detail)
    assert [r["template"] for r in contact] == [CONTACT[1]] and "touching" in contact[0].get(
        "reads", []), ("MF-C8: the contact form", contact)
    assert const == [], ("MF-C4: a constant carried", const)

    ag3, _a3, _s3 = G.agent()          # the carried group alone on a fresh agent's shelf
    ag3._reinvent_carried([rows[0]])
    off2 = propose(ag3, on=False)
    assert not str(off2.get("pick") or "").startswith("ALL kind("), ("MF-C2: OFF held", off2)
    on2 = propose(ag3, on=True)
    assert str(on2.get("pick") or "").startswith("ALL kind(") and isinstance(
        ag3._hyp and ag3._hyp.get("cond"), tether._Group), ("MF-C2: no group held", on2)
    print(f"test_shape_carry: pass (MF-C1 OFF none; ON {forms} shelved and re-invented "
          f"{got['reinvented']} (axis forms included), refused {detail.get('refused')}; MF-C8 "
          f"{contact[0]['template']!r} reads {contact[0]['reads']}; MF-C2 carried group rebuilt "
          f"and held {on2['pick']!r} (OFF: {off2.get('pick')!r}); MF-C4 {CONSTANT!r} not carried)")


if __name__ == "__main__":
    main()
