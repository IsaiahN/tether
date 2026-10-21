"""GQ2's ONE build (the reviewer 2026-10-20 17:34 CDT): the stall reads the trend, an unreadable
frame holds the series, a held routable hypothesis acts before System 0, a clock is not a subject.
gridworld_arc_s1, the agent seed pinned, one process; each check on a fresh agent stepped until a
hypothesis is held, the arm toggled at the call (each flag is read where it is used).

  T1 TREND (TETHER_GOAL_HYPOTHESES): readings with no new low over MIN_REPEAT + 1 end the held
     hypothesis "stalled" by the trend ON, and it holds OFF (inside its budget); readings that keep
     falling are not ended early ON.
  T2 HOLD (TETHER_ARRIVAL): one operand-unreadable frame keeps the series' length ON (and counts a
     held cycle on the hypothesis), and restarts it OFF.
  T3 ORDER (TETHER_GOAL_HYPOTHESES): with System 0 forced active, the hypothesis's route is taken
     ON (discriminate:goal) and System 0 acts OFF.
  T4 CLOCK (TETHER_GOAL_HYPOTHESES): a slot moved by -2 under every action is refused as
     self-moving ON and accepted OFF; a slot moved only under one action is accepted ON.
  T5 THE CLICK BOARD (19:54 (c)): one positioned action and the platform's RESET, never pressed: a
     +1-every-click slot is self-moving after clicks landing in two places, not after one; a slot
     moved only where the click lands on one object is not.

    python test_hyp_trend.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
tree = sys.argv[1]
sys.path = ([tree, tree + "/conform"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import gamma, ledger, panel, tether, world

W = tether.MIN_REPEAT + 1


def fresh():
    env = world.bind(panel._gridworld("gridworld_arc_s1")[0])
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="hyptrend"), tether.Config(),
                      ledger.Ledger())
    for _ in range(40):
        ag.step()
        if ag._hyp is not None:
            return ag
    raise SystemExit("no hypothesis held in 40 steps")


def ends(ag):
    return [r["detail"] for r in ag.led.rows() if r["event"] == "goal_hypothesis_end"]


def trend(on, reads):
    ag = fresh()
    h, sl = ag._hyp, ag._hyp["slots"][0]
    n0 = len(ends(ag))
    h.update(steps=0, budget=99, reads={s: list(reads) for s in h["slots"]}, seg={})
    for s in h["slots"]:
        ag._res[s] = [reads[-1]]            # open: neither touched nor confirmed
    tether._GOAL_HYP = on
    try:
        ag._hyp_check()
    finally:
        tether._GOAL_HYP = True
    new = ends(ag)[n0:]
    return {"held": ag._hyp is not None, "end": [(e["why"], e.get("by")) for e in new]}


def hold(on):
    ag = fresh()
    h, sl = ag._hyp, ag._hyp["slots"][0]
    ag._res[sl] = [0.5, 0.4]
    orig = ag.goal_residual

    def gr(slot, state, counts=None, why=None):
        if slot == sl:
            if why is not None:
                why["exit"] = "operand-unreadable"
            return None
        return orig(slot, state, counts, why)
    ag.goal_residual = gr
    tether._ARRIVAL = on
    try:
        ag.note_goals(ag.env.observe())
    finally:
        tether._ARRIVAL = True
    return {"len": len(ag._res.get(sl) or ()), "held_unreadable": h["held_unreadable"]}


def order(on):
    ag = fresh()
    before = ag.env.observe()
    sl = ag._hyp["slots"][0]
    ag._res[sl] = [0.6, 0.5]
    route = ag._hyp_route(sl, before)
    ag.routine, ag._routine_next = None, None
    ag._system0_active = lambda: True
    ag._exit_choice = lambda b: ("system0", None, None)
    tether._GOAL_HYP = on
    try:
        act, by = ag.choose(before)
    finally:
        tether._GOAL_HYP = True
    return {"route": route, "act": act, "by": by}


def clock(on):
    ag = fresh()
    ag._hyp_end("lost")
    before = ag.env.observe()
    acts = list(ag.actions)
    planted = []                       # the agent's own transitions: one press of each action
    for a in acts:
        b, af = dict(before), dict(before)
        af["o0.col"] = b["o0.col"] - 2
        af["o0.row"] = b["o0.row"] + (1 if a == acts[-1] else 0)
        planted.append((b, a, af, None, None))
    ag.trace = planted
    tether._GOAL_HYP = on
    try:
        out = {"col": ag._self_moving("o0.col"), "row": ag._self_moving("o0.row")}
        ag._hyp_tried = {}
        ag._hyp_propose(before)
    finally:
        tether._GOAL_HYP = True
    row = [r["detail"] for r in ag.led.rows() if r["event"] == "goal_hypotheses"][-1]
    out["refused"] = row["refused"].get("self-moving subject", 0)
    out["open"] = row["open"]
    return out


def click():
    # a one-action click board (19:54 (c)): ACTION6 and the platform's RESET, never pressed
    ag = fresh()
    ag.actions = ["ACTION6", "RESET"]
    ag.env.provenance = lambda a: "platform-universal" if a == "RESET" else "declared"
    b0 = ag.env.observe()

    def press(land, drow):
        b, af = dict(b0), dict(b0)
        af["o0.col"] = b["o0.col"] + 1          # +1 on every click, wherever it lands
        af["o0.row"] = b["o0.row"] + drow       # moved only where the click lands on o1
        return (b, "ACTION6", af, None, land)
    ag.trace = [press("o1", 1)]
    one = ag._self_moving("o0.col")
    ag.trace = [press("o1", 1), press("o2", 0), press("o1", 1)]
    return {"one_place": one, "two_places": ag._self_moving("o0.col"),
            "mover_at_one_place": ag._self_moving("o0.row")}


print(json.dumps({
    "t1_flat_on": trend(True, [0.5] * W), "t1_flat_off": trend(False, [0.5] * W),
    "t1_fall_on": trend(True, [0.5 - 0.1 * i for i in range(W)]),
    "t2_on": hold(True), "t2_off": hold(False),
    "t3_on": order(True), "t3_off": order(False),
    "t4_on": clock(True), "t4_off": clock(False), "t5": click()}, default=str))
'''


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", TETHER_AGENT_SEED="0")
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, here], env=env, capture_output=True,
                         text=True, timeout=900, cwd=here)
    assert out.returncode == 0, out.stderr[-3000:]
    r = json.loads(out.stdout.strip().splitlines()[-1])
    assert not r["t1_flat_on"]["held"] and r["t1_flat_on"]["end"] == [["stalled", "trend"]], r
    assert r["t1_flat_off"]["held"] and not r["t1_flat_off"]["end"], r
    assert r["t1_fall_on"]["held"] and not r["t1_fall_on"]["end"], r
    assert r["t2_on"] == {"len": 2, "held_unreadable": 1}, r["t2_on"]
    assert r["t2_off"]["len"] == 0 and r["t2_off"]["held_unreadable"] == 0, r["t2_off"]
    assert r["t3_on"]["by"] == "discriminate:goal" and r["t3_on"]["act"] == r["t3_on"]["route"], r
    assert r["t3_off"]["by"] == "system0", r["t3_off"]
    assert r["t4_on"]["col"] is True and r["t4_on"]["row"] is False and r["t4_on"]["refused"], r
    assert not r["t4_off"]["refused"], r
    assert r["t4_off"]["open"] > r["t4_on"]["open"], (r["t4_on"], r["t4_off"])
    assert r["t5"] == {"one_place": False, "two_places": True, "mover_at_one_place": False}, r["t5"]
    print(f"test_hyp_trend: pass (T1 flat ON {r['t1_flat_on']['end']}, OFF held, falling ON held; "
          f"T2 series ON {r['t2_on']}, OFF {r['t2_off']}; T3 ON {r['t3_on']}, OFF {r['t3_off']}; "
          f"T4 ON {r['t4_on']}, OFF {r['t4_off']}; T5 click board {r['t5']})")


if __name__ == "__main__":
    main()
