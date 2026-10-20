"""GQ1, A LEVEL CLEAR COUNTS (TETHER_LEVEL_GOAL; the reviewer 2026-10-20 14:27 CDT). Each arm in its
own process (the flag resolves at import), the agent seed pinned (TETHER_AGENT_SEED=0).

  L1  test_level_edge's LevelWrapper (fake ARC: levels_completed 0 -> 1 at step 6 of 14, win_levels
      2, never a win), tether_agent.run: ON -> a completion_sweep row at degree 0.5 and a
      goal_condition row naming its met_state, the clearing step's after and before states both
      priced; MUST-FAIL OFF -> no sweep row, no goal_condition row (degree never reaches 1.0).
  L2  two clears, one goal each (test_goal_condition's gridworld_arc_s1 fixture, o0.col == o1.col
      exactly on the met steps): ON -> the second goal is named _goal_2 and held; MUST-FAIL OFF ->
      it is named _goal_1 again and refused at creation (the name-collision bug).
  L3  the shelf and the carry: ON -> at retarget(ADVANCE) a goal_shelved row, a shelf entry with
      (game, level), and an M7-INV record of kind "goal" holding the METHOD (a template with {o}
      / {x}); written by lineage.write and loaded by lineage.load into a fresh agent's shelf,
      carried; OFF -> no shelf, no goal record carried.

    python test_level_goal.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True

PROBE = r'''
import json, sys, tempfile
sys.dont_write_bytecode = True
tree = sys.argv[1]
sys.path = ([tree, tree + "/conform"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import gamma, ledger, lineage, panel, tether, tether_agent, world
from test_level_edge import LevelWrapper, STEPS
from test_goal_condition import _agent, _hist

out = {"arm": tether._LEVEL_GOAL}
# L1
seen = {}
real = tether.Agent.retarget
def spy(self, env, level, how=tether.ADVANCE):
    seen["ag"] = self
    real(self, env, level, how)
tether.Agent.retarget = spy
try:
    tether_agent.run(LevelWrapper(), "fake", STEPS)
finally:
    tether.Agent.retarget = real
ag = seen.get("ag")
rows = [] if ag is None else ag.led.rows()
out["L1"] = {"retargeted": ag is not None,
             "sweeps": [r["detail"].get("degree") for r in rows
                        if r.get("event") == "completion_sweep"],
             "goal_conditions": [
                 {k: r["detail"].get(k) for k in ("pick", "met_state", "steps", "reached")}
                 | {"other": (r["detail"].get("other_state") or {}).get("met_state")}
                 for r in rows if r.get("event") == "goal_condition"]}
# L2 + L3
ag = _agent()
for _ in range(5):              # the fixture steps once; a transition must exist for _hist
    if ag.trace:
        break
    ag.step()
assert ag.trace, "fixture: no transition in 6 steps"
tether._GOAL_CONDITION = tether._GOAL_PAIR = tether._GOAL_LINK = True
picks = []
H = _hist(ag)                    # built once: retarget clears the trace _hist reads
for level in (0, 1):
    ag._reach_hist = list(H)
    ag._goal_condition()
    gc = [r for r in ag.led.rows() if r.get("event") == "goal_condition"][-1]["detail"]
    picks.append({k: gc.get(k) for k in ("pick", "key", "why")})
    if level == 0:
        ag.retarget(ag.env, 1, how=tether.ADVANCE)
        shelved = [r["detail"] for r in ag.led.rows() if r.get("event") == "goal_shelved"]
        goal_recs = [r for r in ag._inv_carry if r.get("kind") == "goal"]
        out["L3"] = {"shelf": {k: {"game": v.get("game"), "level": v.get("level")}
                               for k, v in ag._goal_shelf.items()},
                     "shelved_rows": len(shelved),
                     "carry": [{k: r.get(k) for k in ("name", "template", "level", "kind")}
                               for r in goal_recs]}
out["L2"] = picks
d = tempfile.mkdtemp(prefix="lvlgoal_")
lineage.write(d, ag, "default")
g, seed = panel._gridworld("gridworld_arc_s1")
env = world.bind(g)
ag2 = tether.Agent(env, gamma.Gamma(env.atoms(), game="lvlgoal_load"), tether.Config(),
                   ledger.Ledger())
lineage.load(d, ag2)
out["L3"] = dict(out.get("L3", {}),
                 loaded={k: {"carried": v.get("carried"), "level": v.get("level")}
                                            for k, v in ag2._goal_shelf.items()})
print(json.dumps(out, default=str))
'''


def _run(arm: str) -> dict:
    here = os.path.dirname(os.path.abspath(__file__))
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", TETHER_LEVEL_GOAL=arm, TETHER_AGENT_SEED="0")
    out = subprocess.run([sys.executable, "-c", PROBE, here], env=env, capture_output=True,
                         text=True, timeout=1200, cwd=here)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def _on_holds(r: dict) -> list[str]:
    bad = []

    def chk(ok, what):
        if not ok:
            bad.append(what)
    l1, l2, l3 = r["L1"], r["L2"], r.get("L3", {})
    chk(l1["retargeted"], "L1 the clear retargeted (the level edge)")
    chk(0.5 in l1["sweeps"], "L1 a sweep at degree 0.5")
    chk(any(g["met_state"] in ("after", "before") and g["other"] in ("after", "before")
            for g in l1["goal_conditions"]), "L1 a goal_condition row, both states priced")
    chk(l2[0]["key"] and l2[1]["key"] and l2[0]["key"] != l2[1]["key"]
        and l2[1]["pick"] != "refused at creation", "L2 the second goal held under a new name")
    chk(l3.get("shelved_rows", 0) >= 1
        and any(v["level"] == 0 for v in l3.get("shelf", {}).values()),
        "L3 shelved at ADVANCE with its level")
    chk(any("{o}" in (c["template"] or "") or "{x}" in (c["template"] or "")
            for c in l3.get("carry", [])), "L3 carried as a METHOD (a template)")
    chk(any(v.get("carried") for v in l3.get("loaded", {}).values()),
        "L3 loaded into a fresh agent's shelf, carried")
    return bad


def main() -> None:
    on, off = _run("1"), _run("0")
    assert on["arm"] is True and off["arm"] is False, (on["arm"], off["arm"])
    bad_on = _on_holds(on)
    assert not bad_on, f"ON: {bad_on}\n{json.dumps(on, indent=1)}"
    bad_off = _on_holds(off)
    assert len(bad_off) >= 5, f"MUST-FAIL OFF: only {bad_off} failed\n{json.dumps(off, indent=1)}"
    msg = (f"test_level_goal: pass (ON: sweeps {on['L1']['sweeps']}, goal_condition "
           f"{on['L1']['goal_conditions']}, names {[p['key'] for p in on['L2']]}, shelf "
           f"{on['L3']['shelf']}, loaded {on['L3']['loaded']}; MUST-FAIL OFF: {len(bad_off)} "
           f"fail -- {bad_off}; OFF L2 {off['L2']})")
    print(msg.encode("ascii", "backslashreplace").decode())     # a refusal text carries U+2261


if __name__ == "__main__":
    main()
