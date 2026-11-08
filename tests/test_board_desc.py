"""BUILD 5 ITEM 18, THE BOARD'S DESCRIPTION (TETHER_BOARD_DESC; the reviewer 2026-11-05 r1221,
r1222, r1223). The agent's own per-level readings of what its acting does, a board_desc row when
they change, feeding only the proposer's price as a prior in bits. Seconds: test_group_row's agent.

MF-B1  RED FIRST, NAMED: on gridworld the lifetime mode() reads "coupled" for the two-axis mover
       o0 (it counts SLOTS); the description reads avatar owners ["o0"] (it counts OWNERS)
MF-B2  only positioned actions moved something: click-only; an unpositioned one moved: not
MF-B3  an owner gone at the press where the steered owner touched it: collect, by its kind; an
       owner gone with no touch: not
MF-B4  one press moved three owners besides the self: toggle 3; the self's press that also moved
       one other owner: not toggle (the self, _desc_self, is what two or more actions move)
MF-B5  the prior: silent, every family the same price; avatar holding, navigate cheapest, every
       family finite (reachable)
MF-B6  AST GUARD: no test (if / elif / ternary / comprehension filter / while) in tether.py names a
       description reading or the seed table -- the description feeds only the price; a planted
       `if reads["avatar"]:` is caught
MF-B7  (r1238) ls20's shape: every press moves the avatar o0 and, through derivation, three
       other owners' pair slots relative to o0 (and one derived slot only up/down move): toggle
       does not hold and avatar reads [o0] -- an owner moves only by its OWN slots. RED FIRST in
       the same test: with the derived slots not excluded, toggle reads 3 and avatar takes the
       derived slot's owner too
MF-18a (r1221) the description (avatar o0) ranks X "o0.row == o4.row" (navigate) over Y
       "o1.colour == o3.colour" (placement), both moved this board (one G tier), same bits: X is
       held; X's goal residual reads flat, _hyp_check ends it "stalled" by the trend, and the next
       proposal holds Y -- the switch is the residual's
MF-18b (r1221) the description silent (a fresh level, no press): every family one price, and the
       agent still reaches Y, the first pick or after the other stalls
MF-18c (r1223) with a record that placement PAID under "avatar" (two wins), Y's prior beats the
       seed's X and Y is held first
(Route knowledge is stubbed as test_group_propose does; the readings are planted at _hyp_check.)
The red is behavioural: TETHER_BOARD_DESC=0 writes no board_desc row and fails MF-B1.

    python tests/test_board_desc.py
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import test_group_row as G  # noqa: E402

tether = G.tether
READINGS = ("avatar", "click_only", "collect", "toggle")


def guard(src: str) -> list[int]:
    """MF-B6: the lines where a test names a reading or the seed table."""
    bad = []
    for node in ast.walk(ast.parse(src)):
        tests = ([node.test] if isinstance(node, (ast.If, ast.IfExp, ast.While)) else
                 list(node.ifs) if isinstance(node, ast.comprehension) else [])
        for t in tests:
            for n in ast.walk(t):
                if ((isinstance(n, ast.Constant) and n.value in READINGS)
                        or (isinstance(n, ast.Name) and n.id == "_DESC_SEED")):
                    bad.append(t.lineno)
    return bad


X, Y = "o0.row == o4.row", "o1.colour == o3.colour"


def played():
    was = tether._HYP_ORDER
    tether._HYP_ORDER = False   # the panel's board is the one the draw's walk leaves (B1 moves it)
    try:
        ag, _atoms, _st = G.agent()
        for _ in range(10):
            ag.step()
    finally:
        tether._HYP_ORDER = was
    if hasattr(ag, "_desc_board"):
        ag._desc_board()    # item 19: the board's own stalls cleared; the description alone
    return ag


def propose(ag) -> dict:
    before = ag.trace[-1][2]
    ag.wants.clear()
    ag._hyp, ag._hyp_exhausted = None, None
    ag._inv_conditions = lambda _b, **_k: [X, Y]
    ag._hyp_route = lambda *_a: "a route"
    ag._route_first_set = lambda _b: None
    was = tether._GROUP_PROPOSE
    tether._GROUP_PROPOSE = False
    try:
        ag._hyp_propose(before)
    finally:
        tether._GROUP_PROPOSE = was
    return [r for r in ag.led.rows() if r["event"] == "goal_hypotheses"][-1]["detail"]


def stall(ag) -> None:
    """The held hypothesis's goal residual reads flat; _hyp_check ends it by the trend."""
    h = ag._hyp
    h["own_last"] = True
    for sl in h["slots"]:
        h["reads"][sl] = [3] * (tether.MIN_REPEAT + 2)
    ag._hyp_check()
    end = [r for r in ag.led.rows() if r["event"] == "goal_hypothesis_end"][-1]["detail"]
    assert ag._hyp is None and end["why"] == "stalled", ("the stall", end)


def evidence():
    ag = played()
    b = ag.trace[-1][2]
    assert b["o0.row"] != b["o4.row"] and b["o1.colour"] != b["o3.colour"], "the panel"
    a = propose(ag)
    assert a.get("pick") == X and a["desc"]["holding"] == ["avatar"], ("MF-18a: X first", a)
    stall(ag)
    a2 = propose(ag)
    assert a2.get("pick") == Y and a2["refused"].get("tried this level") == 1, ("MF-18a", a2)

    ag = played()
    ag._desc_level()
    b = propose(ag)
    assert b["desc"]["holding"] == [] and len(set(b["desc"]["prior"].values())) == 1, ("18b", b)
    if b.get("pick") != Y:
        stall(ag)
        b = propose(ag)
    assert b.get("pick") == Y, ("MF-18b: Y not reached", b)

    ag = played()
    ag._desc_paid[("avatar", "placement")] = 2
    c = propose(ag)
    assert c.get("pick") == Y and c["desc"]["prior"]["placement"] < c["desc"]["prior"][
        "navigate"], ("MF-18c: the record does not outweigh the seed", c)
    return a, b, c


def main():
    ag, _atoms, st = G.agent()
    for _ in range(10):
        ag.step()
    rows = [r["detail"] for r in ag.led.rows() if r["event"] == "board_desc"]
    assert rows, "MF-B1: no board_desc row"
    assert ag.agency.mode() == "coupled" and set(ag.agency.contingent()) >= {"o0.row", "o0.col"}, (
        "MF-B1 (red first): the lifetime mode()", ag.agency.mode(), ag.agency.contingent())
    last = rows[-1]
    assert last["reads"]["avatar"]["owners"] == ["o0"] and "avatar" in last["holding"] and (
        last["scope"]["level"] == ag.level), ("MF-B1: not one owner", last)

    ag._desc_level()
    ag.actions = ("ACTION6", "ACTION7")
    ag._desc_note("ACTION6", {"o3.colour"}, ["o3.colour", "o4.colour"])
    ag._desc_note("ACTION7", set(), ["o3.colour", "o4.colour"])
    assert ag._board_desc()["reads"]["click_only"] is True, "MF-B2: click-only"
    ag.actions = ("ACTION6", "up")
    ag._desc_note("up", {"o4.colour"}, ["o3.colour", "o4.colour"])
    assert ag._board_desc()["reads"]["click_only"] is False, "MF-B2: an unpositioned mover"

    ag._desc_level()
    ag.actions = ("up", "down", "left")
    for a, m in (("up", {"o0.row"}), ("down", {"o0.row"}), ("left", set())):
        ag._desc_note(a, m, ["o0.row", "o1.row"])
    gone3 = [s for s in ag.slots if s.startswith("o3.")]
    gone4 = [s for s in ag.slots if s.startswith("o4.")]
    now = tuple(s for s in ag.slots if not s.startswith(("o3.", "o4.")))
    ag._desc_collect(gone3 + gone4, now, {**st, "o0.touches_o3": 1, "o0.touches_o4": 0,
                                          "o4.touches_o0": 0})
    want = {",".join(ag._kind("o3")): 1}
    assert ag._board_desc()["reads"]["collect"] == want, ("MF-B3", ag._board_desc()["reads"])

    ag._desc_level()
    ag.actions = ("up", "down", "left")
    for a, m in (("up", {"o0.row", "o5.row"}), ("down", {"o0.row"}),
                 ("left", {"o1.colour", "o2.colour", "o3.colour"})):
        ag._desc_note(a, m, ["o0.row", "o5.row", "o1.colour", "o2.colour", "o3.colour"])
    tog = ag._board_desc()["reads"]["toggle"]
    assert tog == {"left": 3}, ("MF-B4", tog, ag._lv_breadth)

    der = sorted(s for s in ag._derived_slots() if s.endswith("_o0") and not s.startswith("o0."))
    owners = list(dict.fromkeys(s.split(".", 1)[0] for s in der))
    assert len(owners) >= 4, ("the panel: derived slots of four owners relative to o0", der)
    d3 = [next(s for s in der if s.startswith(o + ".")) for o in owners[:3]]
    dc = next(s for s in der if s.startswith(owners[3] + "."))

    def b7(own_only: bool) -> dict:
        ag._desc_level()
        ag.actions = ("up", "down", "left")
        was = ag._derived_slots
        if not own_only:
            ag._derived_slots = set       # the red: derived slots counted as an owner's own
        try:
            for a, m in (("up", {"o0.row", *d3, dc}), ("down", {"o0.row", *d3, dc}),
                         ("left", {"o0.col", *d3})):
                ag._desc_note(a, m, ["o0.row", "o0.col", *d3, dc])
            return ag._board_desc()["reads"]
        finally:
            ag._derived_slots = was

    red = b7(False)
    assert red["toggle"] and owners[3] in (red["avatar"] or {}).get("owners", []), (
        "MF-B7 (red first): the derived-slot artifact", red)
    b7r = b7(True)
    assert b7r["toggle"] is None and b7r["avatar"]["owners"] == ["o0"], ("MF-B7", b7r)

    silent = ag._desc_prior([])
    assert len(set(silent.values())) == 1, ("MF-B5: silent is not uniform", silent)
    av = ag._desc_prior(["avatar"])
    assert min(av, key=av.get) == "navigate" and all(v < 10 for v in av.values()), ("MF-B5", av)

    src = Path(tether.__file__).read_text(encoding="utf-8")
    assert guard(src) == [], ("MF-B6: a description reading in a test", guard(src))
    assert guard('if reads["avatar"]:\n    hold = "navigate"\n') == [1], "MF-B6: guard blind"
    a, b, c = evidence()
    print(f"  MF-18a X held by the prior {a['desc']['prior']}, stalled, Y held; MF-18b silent "
          f"{b['desc']['prior']['navigate']} bits each, Y reached; MF-18c record -> "
          f"{c['desc']['prior']}, Y first")
    print(f"test_board_desc: pass (MF-B1 mode() {ag.agency.mode()!r}, description avatar owners "
          f"['o0']; B2 click-only True/False; B3 collect {want}; B4 toggle {tog}; B5 silent "
          f"{silent['navigate']} bits each, avatar {av}; B6 no test names a reading)")


if __name__ == "__main__":
    main()
