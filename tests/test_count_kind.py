"""BUILD 5 ITEM 17 (iii), COUNT-OF-KIND (TETHER_COUNT_KIND; the reviewer 2026-11-05 r1203, r1205).
The completion offers "NONE of kind k remain" (count 0, the group row's guarded NONE) and
"count(kind a) == count(kind b)", over the kinds the agent HELD only (7l, recorded at perception).
Seconds:
test_group_row's agent; histories forced from its own state.

MF-C1  the objective held exactly when every member of the one held kind was gone: NONE of it is
       offered, is the cheapest that pays (errors 0), and the completion holds it, invented on
       came / gone, with no slot to want
MF-C2  a kind never held is not offered and reads None: with no kind held nothing is offered; a
       count over an unheld kind is None, never true
MF-C3  two kinds (the kinds forced): the objective held exactly when their counts were equal; the
       count-equal goal is offered and is the cheapest that pays (errors 0)
OFF: no count goal offered. The red is behavioural: TETHER_COUNT_KIND=0 fails MF-C1.

    python tests/test_count_kind.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import test_group_row as G  # noqa: E402

tether = G.tether


def main():
    ag, atoms, st = G.agent()
    kind = ag._kind("o0")
    members = [o for o in ag._owners(st) if ag._kind(o) == kind]
    gone = G.without(st, members)
    assert kind in ag._kinds_held and not ag._owners(gone), "the panel: one held kind, then none"

    rows = [((gone if i % 4 == 0 else G.without(st, members[: i % 4])), i % 4 == 0)
            for i in range(36)] + [(gone, True)]
    best, detail = ag._goal_candidates(rows)
    none_text = f"NONE of kind {'/'.join(kind)} remain"
    assert detail["offered"].get("count", 0) >= 1, ("MF-C1: no count goal offered", detail)
    assert best is not None and best[4] == none_text and best[3] == 0, (
        "MF-C1: NONE of the held kind is not the cheapest that pays", detail["cheapest"])
    ag._reach_hist = rows
    ag._goal_condition()
    row = [r for r in ag.led.rows() if r["event"] == "goal_condition"][-1]["detail"]
    assert row.get("pick") == none_text and row.get("key", "").startswith("AGENT-INVENTED|"), (
        "MF-C1: the completion does not hold it", row)
    assert row["link"] == {"linked": False, "why": "a count of a kind names no slot to want"}, row

    held = set(ag._kinds_held)
    ag._kinds_held = set()
    try:
        assert ag._goal_counts(rows) == [], "MF-C2: a count offered over a kind never held"
        assert ag._count_holds((kind,), gone) is None, "MF-C2: NONE of an unheld kind is not None"
    finally:
        ag._kinds_held = held
    assert ag._count_holds((kind, ("NEVER",)), st) is None, "MF-C2: an unheld side reads a count"

    a, b = ("A",), ("B",)
    real_kind = ag._kind
    ag._kind = lambda o: a if o in ("o0", "o1", "o2") else b if o in ("o3", "o4", "o5") \
        else real_kind(o)
    ag._kinds_held = {a, b}
    cases = [((), True), (("o0",), False), (("o0", "o3"), True), (("o3",), False)]
    rows2 = [(G.without(st, list(cases[i % 4][0])), cases[i % 4][1]) for i in range(36)]
    rows2.append((st, True))
    best2, detail2 = ag._goal_candidates(rows2)
    eq = "count(kind A) == count(kind B)"
    assert any(x["if"] == eq for x in detail2["cheapest"]), ("MF-C3: not offered", detail2)
    assert best2 is not None and best2[4] == eq and best2[3] == 0, (
        "MF-C3: count-equal is not the cheapest that pays", detail2["cheapest"])
    ag._kind = real_kind
    ag._kinds_held = held

    tether._COUNT_KIND = False
    try:
        _b, d_off = ag._goal_candidates(rows)
    finally:
        tether._COUNT_KIND = True
    assert "count" not in d_off["offered"] and not any(
        x["if"] == none_text for x in d_off["cheapest"]), ("OFF: a count goal offered", d_off)
    print(f"test_count_kind: pass (MF-C1 {none_text!r} cheapest that pays, held as {row['key']}, "
          f"no slot to want; MF-C2 unheld kinds not offered, None; MF-C3 {eq!r} cheapest that "
          f"pays of {detail2['conditions']}; OFF none offered)")


if __name__ == "__main__":
    main()
