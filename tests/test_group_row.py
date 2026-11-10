"""BUILD 5 ITEM 17 (i), THE GROUP ROW (TETHER_GROUP_ROW; the reviewer 2026-11-05 r1200; Fig 11 :48,
Fig 8 :39, Fig 6 :46). A quantified candidate compiles to a Group over the members of a kind the
agent holds (7l), evaluated per member. Seconds: a gridworld agent stepped twice, with ARC's
comparison atoms so a POSITION equality compiles (as test_goal_both_sides); the states are the
agent's own, edited to force each case.

MF-G1  "o0.row == o1.row" for ALL of o0's kind compiles to a Group and is evaluated per member:
       true when every member's row is o1's, false when one member's is not. OFF: QUANTIFIED
MF-G2  NONE (presence alone) of a held kind whose members are gone holds; of a kind never held it
       is NOT_RESOLVED (None), never satisfied; with members present it is false; NONE of a
       member condition with one member unreadable and none true is None, not true (r1201)
MF-G3  ALL of a kind with no members is NOT_RESOLVED (None), never a vacuous true
MF-G4  (B, reach) a history where the objective held exactly when every member was level: the
       completion offers group goals, reads them through holds(), the exact one is the cheapest
       that pays and links one want per member but its anchor. OFF: no group offered
The red is behavioural: TETHER_GROUP_ROW=0 refuses the compile, and every MF fails.

    python tests/test_group_row.py
"""
from __future__ import annotations

import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import arc_atoms  # noqa: E402
import arc_predict  # noqa: E402
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

C = tether.compile_term
RULE = "ALL objects, every frame"        # the library's RULE view writes this quantifier


def agent():
    env = world.bind(gridworld.family("default", 0))
    atoms = {a.name: a for a in env.atoms()}
    atoms.update({a.name: a for a in arc_atoms.three_spaces(arc_predict.predict())})
    ag = tether.Agent(env, gamma.Gamma(list(atoms.values()), game="fam_default_0"),
                      tether.Config(), ledger.Ledger())
    ag.step()
    ag.step()
    return ag, atoms, dict(ag.trace[-1][2])


def without(state: dict, owners: list[str]) -> dict:
    return {k: v for k, v in state.items()
            if not any(k.startswith(o + ".") or f"~{o}." in k for o in owners)}


def main():
    ag, atoms, st = agent()
    kind = ag._kind("o0")
    members = [o for o in ag._owners(st) if ag._kind(o) == kind]
    assert len(members) >= 3, ("the panel: o0's kind needs members", members)

    g = C.compile_candidate({"condition": "o0.row == o1.row", "quantifier": RULE, "scope": "o0"},
                            atoms)
    assert isinstance(g, C.Group) and g.quant == "ALL", ("MF-G1: no group row", g)
    level = {**st, **{f"{o}.row": st["o1.row"] for o in members}}
    assert ag._group_holds(g, level) is True, "MF-G1: every member level, ALL false"
    odd = next(o for o in members if o not in ("o0", "o1"))
    assert ag._group_holds(g, {**level, f"{odd}.row": st["o1.row"] + 1}) is False, (
        "MF-G1: one member off the row, ALL still true -- not evaluated per member")
    C._GROUP_ROW = False
    try:
        off = C.compile_candidate({"condition": "o0.row == o1.row", "quantifier": RULE,
                                   "scope": "o0"}, atoms)
    finally:
        C._GROUP_ROW = True
    assert isinstance(off, C.Refusal) and off.reason == C.QUANTIFIED, ("MF-G1 OFF", off)

    none = C.compile_candidate({"quantifier": "none", "scope": "o0"}, atoms)
    assert isinstance(none, C.Group) and none.member is None, ("MF-G2: no NONE row", none)
    assert kind in ag._kinds_held, ("MF-G2: the kind was never recorded at perception", kind)
    gone = without(st, members)
    assert ag._group_holds(none, gone, kind=kind) is True, (
        "MF-G2: a held kind gone to zero, NONE does not hold")
    assert ag._group_holds(none, st, kind=kind) is False, "MF-G2: members present, NONE holds"
    never = ("NEVER-HELD",)
    assert never not in ag._kinds_held
    assert ag._group_holds(none, gone, kind=never) is None, (
        "MF-G2: a kind never held reads satisfied, not NOT_RESOLVED")
    above = C.compile_candidate({"condition": "o0.row > o1.row", "quantifier": "none",
                                 "scope": "o0"}, atoms)
    assert ag._group_holds(above, level) is True, "MF-G2: no member above o1, NONE false"
    blind = {k: v for k, v in level.items() if k != f"{odd}.row"}
    assert ag._group_holds(above, blind) is None, (
        "MF-G2 (r1201): one member unreadable and none true reads NONE satisfied, not None")

    assert ag._group_holds(g, gone, kind=kind) is None, "MF-G3: ALL of no members is not None"
    assert ag._group_holds(g, st, kind=never) is None, "MF-G3: ALL of an empty kind is not None"
    # MF-G4 (r1201, reach): a history where the objective held exactly when every member was
    # level with o1; the single "o0.row == o1.row" also holds where another member is off
    rows = []
    for i in range(36):
        off = [o for o in members if o not in ("o0", "o1")][i % 4] if i % 3 else None
        s = dict(level) if off is None else {**level, f"{off}.row": st["o1.row"] + 1}
        rows.append((s, off is None))
    rows.append((dict(level), True))
    calls = []
    real = tether._Group.holds

    def spy(self, state):
        calls.append(1)
        return real(self, state)
    tether._Group.holds = spy
    try:
        best, detail = ag._goal_candidates(rows)
    finally:
        tether._Group.holds = real
    assert detail["offered"].get("group", 0) >= 1 and calls, ("MF-G4: no group goal offered "
                                                             "or never checked", detail["offered"])
    assert best is not None and isinstance(best[5], tether._Group) and best[3] == 0, (
        "MF-G4: the exact group goal is not the cheapest that pays", detail["cheapest"])
    link = ag._link_goal("@group", best[5])
    assert link["linked"] and len(link["slots"]) == len(members) - 1, (   # the anchor is not
        "MF-G4: not wanted per member", link)                              # wanted on itself
    C._GROUP_ROW = False
    try:
        b_off, d_off = ag._goal_candidates(rows)
    finally:
        C._GROUP_ROW = True
    assert "group" not in d_off["offered"] and not isinstance((b_off or [None] * 6)[5],
                                                              tether._Group), ("MF-G4 OFF", d_off)
    print(f"test_group_row: pass (MF-G1 ALL per member over {len(members)} of kind {kind}, OFF "
          f"QUANTIFIED; MF-G2 NONE held-and-gone True, never-held None, present False, one "
          f"unreadable None; MF-G3 ALL of none None; MF-G4 {best[4]!r} the cheapest that pays, "
          f"{detail['offered']['group']} group(s) offered, holds() read {len(calls)}x, wanted on "
          f"{len(link['slots'])} slots; OFF none)")


if __name__ == "__main__":
    main()
