"""B3, TOWARD/AWAY, TETHER_RELATION_SET (the reviewer 2026-10-11 12:25 CDT): composition, no new
reading -- toward is the pair gap compared with its OWN earlier reading, below<a.dist_b~1>; away is
above<a.dist_b~1>. Needs the ~1 operand (TETHER_PREV_OFFER, or the window).

  t1 OFF: "o0.dist_o3 < o0.dist_o3~1" is refused (the must-fail: a pair reading is not stated);
  t2 ON: toward compiles to below<o0.dist_o3~1> on o0.dist_o3, away to above<...>;
  t3 on gridworld's own derived gaps, a step toward the partner: toward holds, away does not; a
     step away: the reverse;
  t4 reachability, PREV_OFFER on: the operand list of o0.dist_o3 holds o0.dist_o3~1, and below/
     above type-check on the gap with it as operand.

    python tests/test_relation_toward.py
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
import compile_term as C
from test_goal_condition import _agent
ag = _agent()
g = ag.env
atoms = {a.name: a for a in ag.gamma.atoms}
TOWARD, AWAY = "o0.dist_o3 < o0.dist_o3~1", "o0.dist_o3 > o0.dist_o3~1"
out = {}
ct, ca = (C.compile_candidate({"condition": t}, atoms) for t in (TOWARD, AWAY))
out["compiled"] = [(c.slot, [a.name for a in c.term.atoms], c.operand)
                   if isinstance(c, C.Compiled) else c.reason for c in (ct, ca)]
if isinstance(ct, C.Compiled):
    st = dict(g.state)
    r3, c3 = st["o3.row"], st["o3.col"]
    def gap(r, c):
        s = dict(st); s["o0.row"], s["o0.col"] = r, c
        return g.derive(s)["o0.dist_o3"]
    far, near = gap(r3, c3 + 4), gap(r3, c3 + 2)
    def frame(now, before):
        return {"o0.dist_o3": now, "o0.dist_o3~1": before}
    out["gaps"] = [far, near]
    out["toward_step"] = [C.run(ct, frame(near, far)), C.run(ca, frame(near, far))]
    out["away_step"] = [C.run(ct, frame(far, near)), C.run(ca, frame(far, near))]
    b = [x for x in ag._bindings("o0.dist_o3", []) if x]
    out["lag_offered"] = "o0.dist_o3~1" in b
    t = g.slot_types()["o0.dist_o3"]
    out["typed"] = [C._typed((atoms[n],), t, t) is None for n in ("below", "above")]
print(json.dumps(out))
'''


def _run(on: bool) -> dict:
    env = dict(os.environ, TETHER_RELATION_SET="1" if on else "0", TETHER_PREV_OFFER="1",
               PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, "-c", PROBE], capture_output=True, text=True, env=env,
                       cwd=_repo.ROOT, timeout=300)
    assert p.returncode == 0, p.stderr[-2500:]
    return json.loads(p.stdout.strip().splitlines()[-1])


if __name__ == "__main__":
    off = _run(False)
    assert all(isinstance(x, str) and "not a library reading" in x for x in off["compiled"]), off
    print(f"  t1 OFF: toward/away refused -- {off['compiled'][0]!r}")
    on = _run(True)
    assert on["compiled"] == [["o0.dist_o3", ["below"], "o0.dist_o3~1"],
                              ["o0.dist_o3", ["above"], "o0.dist_o3~1"]], on
    print("  t2 ON: toward -> below<o0.dist_o3~1>, away -> above<o0.dist_o3~1>")
    far, near = on["gaps"]
    assert near < far, on
    assert on["toward_step"] == [True, False] and on["away_step"] == [False, True], on
    print(f"  t3 gap {far} -> {near}: toward {on['toward_step']}; {near} -> {far}: away "
          f"{on['away_step']} (toward, away)")
    assert on["lag_offered"] and on["typed"] == [True, True], on
    print("  t4 PREV_OFFER on: o0.dist_o3~1 offered as an operand; below/above type-check")
    print("relation toward: OK")
