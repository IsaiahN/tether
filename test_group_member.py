"""GQ2b, F-a + F-b (TETHER_GROUP_MEMBER; the reviewer 2026-10-20 14:27 (b)). gridworld_arc_s1 after
three steps, each arm its own process, the agent seed pinned. A group-scoped (view) objective is
planted on o0.row and read over planted rows o0..o5.

  G1 ON: aligned . holds . all reads a REAL fraction -- rows [1,1,1,2,3,4] -> 0.5, [1,1,1,2,3,1]
     -> 1/3 (it moves when one member moves), all 5 -> 0.0; none_same . all reads 0.5 / 2/3 / 1.0;
     the scope is the whole family (6, the subject included).
  G2 ON (F-b): symmetric . holds . all on o0.shape resolves (the goal sites read shapes; the decoder
     is planted, since gridworld publishes none -- only ArcWorld does).
  MUST-FAIL OFF: aligned reads 0.0 on all three boards and none_same 1.0 (each peer judged with the
     subject's context, whose group contains it), the scope 5; symmetric does not resolve.

    python test_group_member.py
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
from gamma import Term

env = world.bind(panel._gridworld("gridworld_arc_s1")[0])
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="gm"), tether.Config(), ledger.Ledger())
for _ in range(3):
    ag.step()
st = dict(ag.trace[-1][0])
A = {a.name: a for a in ag.gamma.atoms}
out = {"arm": tether._GROUP_MEMBER}


def plant(slot, chain):
    t = Term(chain)
    ag.wants[slot], ag._want_terms[slot] = t.name, t
    ag._want_scope.pop(slot, None)


for name in ("aligned", "none_same"):
    chain = (A[name], A["holds"], A["all"]) if A[name].out_type == "BOOL" else (A[name], A["all"])
    plant("o0.row", chain)
    got = []
    for rows in ([1, 1, 1, 2, 3, 4], [1, 1, 1, 2, 3, 1], [5, 5, 5, 5, 5, 5]):
        c = {}
        r = ag.goal_residual("o0.row", dict(st, **{f"o{i}.row": v for i, v in enumerate(rows)}), c)
        got.append([None if r is None else round(r, 4), c.get("scope")])
    out[name] = got
# (a) the routine's unsat follows rg and the member count (the reviewer 17:17 3 (a))
plant("o0.row", (A["aligned"], A["holds"], A["all"]))
board = dict(st, **{f"o{i}.row": v for i, v in enumerate([1, 1, 1, 2, 3, 4])})
rg = ag.goal_residual("o0.row", board)
n = ag._scope_n("o0.row", board)
out["unsat"] = [round(rg, 4), n, round(rg * n, 4)]
# (d) the cost of one group goal_residual (6 members here), measured, not optimised
import time
t0 = time.perf_counter()
for _ in range(50):
    ag._memo = None
    ag.goal_residual("o0.row", board)
out["us_per_call"] = round((time.perf_counter() - t0) / 50 * 1e6, 1)
# (b) MUST NOT CHANGE: a subject-scoped want (a GQ1 link) and every bet read the same ON and OFF
from test_goal_condition import _compiled
ag.wants.pop("o0.col", None)
ag._want_terms.pop("o0.col", None)
link = ag._link_goal("test_subject", _compiled(ag, "o0.col == o3.col"))
out["subject_link"] = link.get("slots")
out["subject_rg"] = ag.goal_residual("o0.col", st)
act = ag._last_action or ag.actions[0]
out["bets"] = {s: ag._predict(s, st, act) for s in sorted(ag.slots) if s in st}
plant("o0.shape", (A["symmetric"], A["holds"], A["all"]))
# gridworld publishes no shapes() (only ArcWorld does), so the decoder is planted for o0's shape
# id: a two-cell, mirror-symmetric shape. The wiring is what is tested: the goal site passes it
ag._shapes_now = lambda: {st["o0.shape"]: frozenset({(0, 0), (0, 1)})}
ag._memo = None                       # no cached Ctx built before the plant
why = {}
out["symmetric"] = ag.goal_residual("o0.shape", st, why=why)
out["symmetric_exit"] = why.get("exit")
print(json.dumps(out))
'''


def _run(arm: str) -> dict:
    here = os.path.dirname(os.path.abspath(__file__))
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", TETHER_GROUP_MEMBER=arm, TETHER_AGENT_SEED="0")
    out = subprocess.run([sys.executable, "-c", PROBE, here], env=env, capture_output=True,
                         text=True, timeout=600, cwd=here)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def main() -> None:
    on, off = _run("1"), _run("0")
    assert on["arm"] is True and off["arm"] is False
    assert on["aligned"] == [[0.5, 6], [0.3333, 6], [0.0, 6]], on["aligned"]
    assert on["none_same"] == [[0.5, 6], [0.6667, 6], [1.0, 6]], on["none_same"]
    assert on["symmetric"] is not None, on
    assert [v for v, _n in off["aligned"]] == [0.0, 0.0, 0.0], off["aligned"]
    assert [v for v, _n in off["none_same"]] == [1.0, 1.0, 1.0], off["none_same"]
    assert all(n == 5 for _v, n in off["aligned"]), off["aligned"]
    assert off["symmetric"] is None, off
    # (a) the routine's unsat moves with the fix: rg x members
    assert on["unsat"] == [0.5, 6, 3.0] and off["unsat"] == [0.0, 5, 0.0], \
        (on["unsat"], off["unsat"])
    # (b) the subject-scoped path and every bet are identical ON and OFF
    assert on["subject_link"] == off["subject_link"] and on["subject_rg"] == off["subject_rg"], \
        (on["subject_rg"], off["subject_rg"])
    assert on["bets"] == off["bets"], "a bet changed with the arm"
    print(f"test_group_member: pass (ON: aligned {on['aligned']}, none_same {on['none_same']}, "
          f"symmetric {on['symmetric']}, unsat {on['unsat']}; MUST-FAIL OFF: aligned "
          f"{off['aligned']}, none_same {off['none_same']}, symmetric None "
          f"({off['symmetric_exit']}), unsat {off['unsat']}; MUST NOT CHANGE: subject R "
          f"{on['subject_rg']} both, {len(on['bets'])} bets identical; COST per group "
          f"goal_residual (6 members): ON {on['us_per_call']} us, OFF {off['us_per_call']} us)")


if __name__ == "__main__":
    main()
