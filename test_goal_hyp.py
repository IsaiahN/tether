"""GQ2, GOAL HYPOTHESES (TETHER_GOAL_HYPOTHESES; the reviewer 2026-10-20 14:27 CDT).
gridworld_arc_s1 (the panel world with the ARC atoms), 25 steps, each arm its own process, the
agent seed pinned.

  H1 ON: hypotheses are PROPOSED from the board (a goal_hypotheses row with a pick, its subject,
     its route from the agent's own delta table, and the ranked head printed); while nothing is
     routable (the delta table empty at the start) the row says System 0 and a proposal comes back
     once an effect is learned.
  H2 ON: a held hypothesis is a SUBJECT-scoped want on its slot, and it ENDS (arrived_no_clear or
     stalled), and the NEXT one differs in (condition, subject).
  H3 ON: the routine path is reached past CAN (a routine row past the gate: routine /
     routine_inert / routine_cut) -- the never-met goal is reachable from the delta table.
  MUST-FAIL OFF: no goal_hypotheses row, no hypothesis end, no routine past the gate.

    python test_goal_hyp.py
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

env = world.bind(panel._gridworld("gridworld_arc_s1")[0])
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="goalhyp"), tether.Config(), ledger.Ledger())
scoped = []
for _ in range(25):
    ag.step()
    if ag._hyp is not None:
        scoped += [ag._want_scope.get(sl) == ag.wants.get(sl) is not None
                   for sl in ag._hyp["slots"]]
rows = ag.led.rows()
hyp = [r for r in rows if r["event"] == "goal_hypotheses"]
print(json.dumps({
    "arm": tether._GOAL_HYP,
    "proposals": [{"c": r["cycle"], "pick": r["detail"].get("pick"), "slot": r["slot"],
                   "route": r["detail"].get("route"), "ranked": len(r["detail"].get("ranked", ())),
                   "why": r["detail"].get("why")} for r in hyp],
    "ends": [{"c": r["cycle"], "why": r["detail"].get("why"), "text": r["detail"].get("text")}
             for r in rows if r["event"] == "goal_hypothesis_end"],
    "past_gate": sum(1 for r in rows if r["event"] in ("routine", "routine_inert", "routine_cut")),
    "scoped": scoped}, default=str))
'''


def _run(arm: str) -> dict:
    here = os.path.dirname(os.path.abspath(__file__))
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", TETHER_GOAL_HYPOTHESES=arm, TETHER_AGENT_SEED="0")
    out = subprocess.run([sys.executable, "-c", PROBE, here], env=env, capture_output=True,
                         text=True, timeout=600, cwd=here)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def _on_holds(r: dict) -> list[str]:
    bad = []

    def chk(ok, what):
        if not ok:
            bad.append(what)
    picks = [p for p in r["proposals"] if p["pick"]]
    chk(picks and all(p["route"] and p["ranked"] for p in picks),
        "H1 a proposal with a pick, a route and its ranked head")
    first = r["proposals"][0] if r["proposals"] else None
    chk(first is None or first["pick"] or "System 0" in str(first["why"]),
        "H1 an unroutable start says System 0")
    chk(r["scoped"] and all(r["scoped"]), "H2 the held hypothesis is a subject-scoped want")
    chk(r["ends"] and all(e["why"] in ("arrived_no_clear", "stalled", "lost") for e in r["ends"]),
        "H2 a hypothesis ended (arrived without a clear, or stalled)")
    seq = [(p["pick"], p["slot"]) for p in picks]
    chk(len(seq) >= 2 and all(a != b for a, b in zip(seq, seq[1:], strict=False)),
        "H2 the next hypothesis differs")
    chk(r["past_gate"] >= 1, "H3 a routine reached past the CAN gate")
    return bad


def main() -> None:
    on, off = _run("1"), _run("0")
    assert on["arm"] is True and off["arm"] is False, (on["arm"], off["arm"])
    bad_on = _on_holds(on)
    assert not bad_on, f"ON: {bad_on}\n{json.dumps(on, indent=1)}"
    bad_off = _on_holds(off)
    assert len(bad_off) >= 4 and not off["proposals"] and not off["ends"], \
        f"MUST-FAIL OFF: {bad_off}\n{json.dumps(off, indent=1)}"
    msg = (f"test_goal_hyp: pass (ON: {len([p for p in on['proposals'] if p['pick']])} picks "
           f"{[(p['c'], p['pick'], p['route']) for p in on['proposals'] if p['pick']]}, ends "
           f"{[(e['c'], e['why']) for e in on['ends']]}, past the gate {on['past_gate']}; "
           f"MUST-FAIL OFF: {len(bad_off)} fail, past the gate {off['past_gate']})")
    print(msg.encode("ascii", "backslashreplace").decode())


if __name__ == "__main__":
    main()
