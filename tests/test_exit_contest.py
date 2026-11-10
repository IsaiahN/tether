"""C3 THE EXIT CONTEST (the reviewer 2026-11-10 r1638, r1640, r1641), arm TETHER_EXIT_CONTEST.

  X1  the gate's record beats a higher prior: an exit with a settled return outbids one whose
      prior (A1's outstanding at its aim) is larger; its source is "record:level"
  X2  no record: the bid is the prior, source "prior"; the level's record goes before the series'
  X3  the gate reads only its own record: an exit's own claim is never read (MF: a prior pushed up
      for an exit that has a record does not move its bid)
  X4  the cost filter: an exit whose median demand is over the allowance leaves the room; a filter
      that would empty the room is not applied, and says so
  X5  the record is the ground's: _ex_settle credits the bits explained since the act to the exit
      that took it, at its level and in the series
  X6  OFF: the contest reads A1's outstanding at the aim, as before (no bids on the row)
  X7  touch-move (r1644): a held routine at its checkpoint PROPOSES. MF: losing the contest leaves
      routine_state byte-equal, the routine object and its acts unchanged, with a routine_rebid
      row won=false; winning commits it (the routine advances, the act goes out as "routine")
  X8  discriminate:goal and lookahead bid as offers; each is committed (_goal_split /
      _lookahead_act run) only when it wins (MF: a losing offer never runs its commit); a winner
      with no act hands the turn to the rest of the contest
  X9  r1645: an exact reach-tier tie is split by the seeded draw, never the name, and the
      reach_tier row lists the tied names

    python tests/test_exit_contest.py
"""
from __future__ import annotations

import os
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")

import copy  # noqa: E402

import gamma  # noqa: E402
import gridworld  # noqa: E402
import interface as IFace  # noqa: E402
import ledger  # noqa: E402
import routine as Rt  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def _agent() -> tether.Agent:
    env = world.bind(gridworld.family("default", 0))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="contest"), tether.Config(),
                        ledger.Ledger())


def check_x1_x2_x3() -> None:
    ag = _agent()
    lk = ag._lk()
    ag._ex_rec[(lk, "distinguish")] = [2, 3.0]          # 1.5 bits per act at this level
    ag._ex_rec["goal"] = [1, 0.4]                       # the series' only
    prior = {"distinguish": 0.2, "goal": 5.0, "system0": 9.0}
    gain, bids = ag._ex_bids(["distinguish", "goal", "system0"], prior)
    assert bids["distinguish"]["source"] == "record:level" and gain["distinguish"] == 1.5
    assert bids["goal"]["source"] == "record:series" and gain["goal"] == 0.4
    assert bids["system0"]["source"] == "prior" and gain["system0"] == 9.0
    assert gain["distinguish"] > gain["goal"], "MF: the prior beat the record"
    pushed = dict(prior, distinguish=1e9)
    g2, _b = ag._ex_bids(["distinguish", "goal", "system0"], pushed)
    assert g2["distinguish"] == 1.5, "MF: a claimed number moved a recorded bid"
    print("  X1-X3: record 1.5 (level) and 0.4 (series) replace their priors 0.2 and 5.0; "
          "no record -> prior 9.0; a pushed claim leaves the recorded bid at 1.5")


def check_x4() -> None:
    ag = _agent()
    a = ag._allowance()
    ag._ex_cost["goal"] = [a * 3, a * 3, a * 3]
    gain, bids = ag._ex_bids(["goal", "distinguish"], {"goal": 5.0, "distinguish": 1.0})
    assert bids["_room"] == ["distinguish"] and not bids["goal"]["affordable"], bids
    ag._ex_cost["distinguish"] = [a * 2]
    _g, bids = ag._ex_bids(["goal", "distinguish"], {"goal": 5.0, "distinguish": 1.0})
    assert bids["_room"] == ["goal", "distinguish"] and bids["_filter"].startswith("not applied")
    print(f"  X4: median demand {a * 3} over the allowance {a} leaves the room; a filter that "
          f"would empty it is not applied")


def check_x5() -> None:
    ag = _agent()
    ag._integral, ag._outstanding = 10.0, {"x": 6.0}
    ag._ex_last = (ag._lk(), "distinguish", ag.pe_integral() - ag.outstanding(), ag.cycle)
    ag._outstanding = {"x": 2.5}                        # the next frame explained 3.5 bits
    ag._ex_settle()
    assert ag._ex_rec[(ag._lk(), "distinguish")] == [1, 3.5], ag._ex_rec
    assert ag._ex_rec["distinguish"] == [1, 3.5] and ag._ex_last is None
    print("  X5: 3.5 bits explained after the act, credited to (level, distinguish) and the series")


def check_x6() -> None:
    ag = _agent()
    keep, tether._EXIT_CONTEST = tether._EXIT_CONTEST, False
    try:
        for _ in range(3):
            ag.step()
    finally:
        tether._EXIT_CONTEST = keep
    rows = [r["detail"] for r in ag.led.rows()
            if r["event"] == "choice" and r["detail"].get("site") == "exit"]
    assert all("bids" not in d for d in rows), "OFF: bids on the row"
    on = _agent()
    for _ in range(3):
        on.step()
    on_rows = [r["detail"] for r in on.led.rows()
               if r["event"] == "choice" and r["detail"].get("site") == "exit"]
    assert all("bids" in d for d in on_rows), "ON: an exit choice without its bids"
    print(f"  X6: OFF {len(rows)} exit choices with no bids; ON {len(on_rows)}, each with its bids")


def _held(ag: tether.Agent) -> None:
    elicit = IFace.Intent(IFace.ELICIT)
    ag.routine = Rt.Expect("o0.col", Rt.Seq(Rt.Act(elicit), Rt.Act(elicit)))   # it claims
    ag.routine_for, ag.routine_state, ag._routine_next = "o0.col", {"mark": [1, 2]}, None


def check_x7() -> None:
    ag = _agent()
    ag.step()
    _held(ag)
    lk = ag._lk()
    ag._ex_rec[(lk, "routine")] = [1, -5.0]           # the record says the routine does not pay
    for e in ("probe", "system0", "distinguish", "goal"):
        ag._ex_rec[(lk, e)] = [1, 50.0]
    before_rs, before_rt, acts = copy.deepcopy(ag.routine_state), ag.routine, ag._routine_acts
    act, by = ag.choose(dict(ag.trace[-1][2]))
    rows = [r["detail"] for r in ag.led.rows() if r["event"] == "routine_rebid"]
    assert rows and rows[-1]["won"] is False and by != "routine", (rows, by)
    assert ag.routine_state == before_rs and repr(ag.routine_state) == repr(before_rs), \
        "MF: a losing re-bid changed routine_state"
    assert ag.routine is before_rt and ag._routine_acts == acts, "MF: a losing re-bid committed"
    win = _agent()
    win.step()
    _held(win)
    win._ex_rec[(win._lk(), "routine")] = [1, 1e6]
    rt0 = win.routine
    act2, by2 = win.choose(dict(win.trace[-1][2]))
    assert by2 == "routine" and act2 is not None and win.routine is not rt0, (by2, act2)
    print(f"  X7: the routine lost to {by}: state byte-equal, not advanced; when it wins it "
          f"commits ({act2})")


def check_x8() -> None:
    ag = _agent()
    ag.step()
    ran = []
    ag._goal_split = lambda _before, commit=True: ran.append(("goal", commit)) or "up"
    ag._lookahead_act = lambda _before: ran.append("lookahead") or None
    ag._c3_offer = {"discriminate:goal": {"aim": "o0.col"}, "lookahead": {"aim": "o0.col"}}
    lk = ag._lk()
    ag._ex_rec[(lk, "lookahead")] = [1, 1e6]
    ag._ex_rec[(lk, "discriminate:goal")] = [1, 1e5]
    take, _t, _d = ag._exit_choice(dict(ag.trace[-1][2]))
    assert take == "lookahead", take
    got = ag._c3_commit(take, dict(ag.trace[-1][2]))
    assert got is None and ran == ["lookahead"], ("MF: a losing offer committed", ran)
    got2 = ag._c3_commit("discriminate:goal", dict(ag.trace[-1][2]))
    assert got2 == "up" and ("goal", True) in ran
    print("  X8: both offered; the winner alone committed; a winner with no act hands the turn on")


def check_x9() -> None:
    ag = _agent()
    tether.TIER_CAP, keep = 1, tether.TIER_CAP
    try:
        lib = ag.gamma.library
        ag.cycle = 0
        ag._reach_inflow()
        ag.cycle = 1
        names = [ag.gamma.accept(gamma.Term((lib[a].atoms[0], lib[b].atoms[0])), 1, "r").name
                 for a, b in (("inc", "dec"), ("dec", "inc"), ("inc", "inc"))]
        ag._reach_inflow()
        ag.cycle = 2
        ag.gamma.accept(gamma.Term((lib["dbl"].atoms[0], lib["inc"].atoms[0])), 2, "r")
        ag._reach_inflow()
    finally:
        tether.TIER_CAP = keep
    rows = [r["detail"] for r in ag.led.rows() if r["event"] == "reach_tier"]
    tied = [d for d in rows if d.get("tied")]
    assert tied and set(tied[-1]["tied"]) <= set(names) and tied[-1]["by"] == "draw", rows
    print(f"  X9: {len(tied[-1]['tied'])} terms tied in reach and entry; the draw chose, the row "
          f"lists them")


if __name__ == "__main__":
    for c in (check_x1_x2_x3, check_x4, check_x5, check_x6, check_x7, check_x8, check_x9):
        c()
    print("exit_contest: OK")
