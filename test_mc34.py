"""7a(8) MC3/MC4 (TETHER_MC34; R3 part 2; the reviewer 2026-10-10 22:33Z). MC3 appends the
ground's record of every ending; MC4 reads a plan's need against reserve_seen (the budget learned
by running out) and level_cost_seen (what cleared levels cost), kept apart.

  must-pass: a cleared ending and a run-ending cap are recorded; MC4 reads reserve_run_seen =
     actions at that cap minus actions used so far, and level_cost_seen = the cleared level's cost;
  1. MC3 is the ground's fields only: frame activity (book counts, bets) does not move it;
  2. a cap the WORLD holds is never read: with no cap ending, both reserves are "no record";
  3. the same word twice with no action between is one ending;
  5. a reset is cleared=False and stays out of level_cost_seen (the reviewer 22:47Z);
  6. AT ITS OWN SCOPE (the reviewer 23:18Z): a per-level budget of 60 exhausted on levels 1-3
     gives reserve_level_seen 60 (not 180), and a plan needing 50 at level 4 is not dropped;
  4. a real run (gridworld_arc_s1, 13 cycles, then end_run): OFF writes no ground_record row and
     no mc4 field; ON writes both on the real path (its first plan adoption is at c12).

    python test_mc34.py
"""
from __future__ import annotations

import sys

import gamma
import gridworld
import ledger
import routine as Rt
import tether
import world

sys.dont_write_bytecode = True
sys.path.insert(0, "conform")
import panel  # noqa: E402

PLAN = Rt.Until("o0.row", Rt.Act("ACTION1"), 6)


def _agent():
    env = world.bind(gridworld.family("default", 0, 4))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="mc34_fixture"), tether.Config(),
                        ledger.Ledger())


def _member(on: bool):
    was = tether._MC34
    tether._MC34 = on
    try:
        g, seed = panel._gridworld("gridworld_arc_s1")
        env = world.bind(g)
        ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"dt_default_{seed}"),
                          tether.Config(), ledger.Ledger())
        for _ in range(13):
            ag.step()
        ag.end_run("cap")
    finally:
        tether._MC34 = was
    rows = ag.led.rows()
    return ([r for r in rows if r["event"] == "ground_record"],
            [r for r in rows if r["event"] == "routine" and "mc4" in r["detail"]])


if __name__ == "__main__":
    tether._MC34 = True
    ag = _agent()
    assert ag._mc4(PLAN) == {"need": 6, "reserve_level_seen": "no record",
                             "reserve_run_seen": "no record", "level_cost_seen": "no record"}
    ag._run_actions, ag._attempt_actions = 14, 14
    ag._mc3_note("advance", "level")
    ag._attempt_actions = 0
    ag._run_actions = 30
    ag._mc3_note("cap", "run")
    ag._run_actions = 32
    m = ag._mc4(PLAN)
    assert m == {"need": 6, "reserve_level_seen": "no record", "reserve_run_seen": [-2],
                 "level_cost_seen": [14, 14]}, m
    print(f"  must-pass: {[e['how'] for e in ag._mc3]} recorded; MC4 {m}")
    before = [dict(e) for e in ag._mc3]
    ag.gamma.book["bargain_paid"] = ag.gamma.book.get("bargain_paid", 0) + 99
    assert ag._mc3 == before and set(before[0]) == {
        "how", "kind", "cleared", "level", "actions_this_level", "actions_this_run", "attempts",
        "scope"}
    print("  1: the record is the ground's fields only; frame activity does not move it")
    w = _agent()
    w.env.cap = w.env.max_actions = 50
    w._run_actions = 10
    w._mc3_note("advance", "level")
    assert w._mc4(PLAN)["reserve_level_seen"] == w._mc4(PLAN)["reserve_run_seen"] == "no record"
    print("  2: a world cap of 50, never reached by an ending, is not read: both reserves "
          "'no record'")
    d = _agent()
    d._mc3_note("death", "level")
    d._mc3_note("death", "level")
    assert len(d._mc3) == 1
    print("  3: the same word twice with no action between is one ending")
    r = _agent()
    r._attempt_actions = r._run_actions = 9
    r._mc3_note("reset", "level")
    r._mc3_note("mystery", "level")
    assert [(e["kind"], e["cleared"]) for e in r._mc3] == [("reset", False), ("mystery", False)]
    assert r._mc4(PLAN)["level_cost_seen"] == "no record", r._mc4(PLAN)
    print("  5: a reset (and an unknown word) is recorded as itself, never cleared; it does not "
          "enter level_cost_seen")
    lad = _agent()
    for _lv in (1, 2, 3):
        lad._attempt_actions = 60
        lad._run_actions += 60
        lad._mc3_note("cap", "level")
    lad._attempt_actions = 0                                          # level 4 begins
    m6 = lad._mc4(PLAN)
    assert m6["reserve_level_seen"] == [60, 60, 60] and m6["reserve_run_seen"] == "no record", m6
    assert not lad._cannot_finish(50) and lad._cannot_finish(61)
    print(f"  6: three level caps of 60 read reserve_level_seen {m6['reserve_level_seen']} (run "
          f"actions {lad._run_actions} are never the level's reserve); need 50 kept, 61 dropped")
    off_g, off_m = _member(False)
    on_g, on_m = _member(True)
    assert not off_g and not off_m, (len(off_g), len(off_m))
    assert on_g and on_m, (len(on_g), len(on_m))
    print(f"  4: OFF: 0 ground_record, 0 mc4; ON: {len(on_g)} ground_record "
          f"({on_g[-1]['detail']['how']}), {len(on_m)} adoption(s) carrying mc4 "
          f"{on_m[0]['detail']['mc4']}")
    print("ok")
