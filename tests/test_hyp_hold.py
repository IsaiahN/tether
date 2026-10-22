"""THE TOUCH HOLD (TETHER_GOAL_HYPOTHESES; the reviewer 2026-10-20 18:40 CDT). gridworld_arc_s1,
the agent seed pinned, one process, each check on a fresh agent stepped until a hypothesis is
held, System 0 forced active in both arms (so OFF is System 0), the arm toggled at the call.

  H1 a planted touch: the held hypothesis's residual reads 0 exactly while its subject and its
     other party keep the values they had at the touch. ON: the touched cycle's act is a "hold"
     with an action the delta table never saw move either, both values are unchanged after it,
     and the next reading at 0 CONFIRMS (the hypothesis ends arrived_no_clear). OFF: System 0.
  H2 no holding action known, and one action planted as the platform's (provenance
     platform-universal) and left untried -- vc33's RESET at c4: ON it is withheld (System 0
     acts with another) and the repeat row says why; OFF System 0 takes it (untried first).

    python tests/test_hyp_hold.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
tree = sys.argv[1]
sys.path = ([tree, tree + "/conform"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import gamma, ledger, panel, tether, world


def fresh():
    env = world.bind(panel._gridworld("gridworld_arc_s1")[0])
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="hyphold"), tether.Config(),
                      ledger.Ledger())
    for _ in range(40):
        ag.step()
        if ag._hyp is not None and all(ag.iface.table.get(a, {}).get("n") for a in ag.actions):
            ag._system0_active = lambda: True
            ag._exit_choice = lambda b: ("system0", None, None)
            ag.routine, ag._routine_next = None, None
            return ag
    raise SystemExit("no hypothesis held with every action taken in 40 steps")


def plant_touch(ag):
    h = ag._hyp
    sl = h["slots"][0]
    op = next(s for s in (h["cond"].slot, h["cond"].operand) if s != sl)   # the other party
    st = ag.env.observe()
    vals = (st.get(sl), st.get(op))
    orig = ag.goal_residual

    def gr(slot, state, counts=None, why=None):
        if slot == sl:
            return 0.0 if (state.get(sl), state.get(op)) == vals else 0.5
        return orig(slot, state, counts, why)
    ag.goal_residual = gr
    ag._res[sl] = [0.5]
    return sl, op, vals


def last_repeat(ag):
    return [r["detail"] for r in ag.led.rows() if r["event"] == "repeat"][-1]


def h1(on):
    ag = fresh()
    sl, op, vals = plant_touch(ag)
    tether._GOAL_HYP = on
    try:
        ag.step()                      # the touched cycle
        rep = last_repeat(ag)
        after = ag.env.observe()
        out = {"slot": sl, "operand": op, "by": rep.get("by"), "action": rep.get("action"),
               "why": rep.get("hyp_why"), "kept": (after.get(sl), after.get(op)) == vals}
        if on:
            ag.step()                  # the confirming reading
            ends = [r["detail"] for r in ag.led.rows() if r["event"] == "goal_hypothesis_end"]
            out["end"] = ends[-1]["why"] if ends else None
    finally:
        tether._GOAL_HYP = True
    return out


def h2(on):
    ag = fresh()
    sl, op, _vals = plant_touch(ag)
    plat = ag.actions[-1]
    ag.env.provenance = lambda a: "platform-universal" if a == plat else None
    ag.iface.table.pop(plat, None)                     # untried, as RESET was on vc33
    for a in ag.actions:                               # no action is known to keep the subject
        if a != plat:
            e = ag.iface.table[a]
            e["delta"][((), sl, "x")] = (1, 1)
    tether._GOAL_HYP = on
    try:
        ag.step()
        rep = last_repeat(ag)
    finally:
        tether._GOAL_HYP = True
    return {"platform": plat, "by": rep.get("by"), "action": rep.get("action"),
            "why": rep.get("hyp_why")}


print(json.dumps({"h1_on": h1(True), "h1_off": h1(False), "h2_on": h2(True), "h2_off": h2(False)},
                 default=str))
'''


def main() -> None:
    here = _repo.ROOT
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", TETHER_AGENT_SEED="0")
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, here], env=env, capture_output=True,
                         text=True, timeout=1200, cwd=here)
    assert out.returncode == 0, out.stderr[-3000:]
    r = json.loads(out.stdout.strip().splitlines()[-1])
    on, off = r["h1_on"], r["h1_off"]
    assert on["by"] == "hold" and on["kept"] and on["end"] == "arrived_no_clear", on
    assert on["why"] and on["why"].startswith("touched: held with"), on
    assert off["by"] == "system0" and off["why"] is None, off
    p_on, p_off = r["h2_on"], r["h2_off"]
    assert p_off["action"] == p_off["platform"], p_off
    assert p_on["action"] != p_on["platform"] and p_on["by"] == "system0", p_on
    assert p_on["why"] and "withheld" in p_on["why"], p_on
    print(f"test_hyp_hold: pass (H1 ON hold {on['action']} on {on['slot']}/{on['operand']}, "
          f"kept, then {on['end']}; OFF {off['by']} {off['action']} (kept {off['kept']}); "
          f"H2 ON {p_on['action']} with {p_on['platform']} withheld ({p_on['why']!r}); "
          f"OFF {p_off['action']})")


if __name__ == "__main__":
    main()
