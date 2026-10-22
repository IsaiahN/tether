"""ITEM 2, A TOUCH-LOSS STARTS A NEW APPROACH (TETHER_GOAL_HYPOTHESES; the reviewer
2026-10-20 19:11 CDT). gridworld_arc_s1, the agent seed pinned; a fresh agent stepped until a
hypothesis is held, then its subject's readings planted through note_goals and _hyp_check, the
path a step takes:

    0.5, 0.0 (touch, k), 0.0635 (lost, k+1), 0.0317, 0.0159 -- falling again

  ON (this tree): the stall reads shrinking() over the readings since the last touch-loss
     ([0.0635, 0.0317, 0.0159], shrinking), so the hypothesis is HELD through k+3; touches 1,
     losses 1 on its row.
  OFF: 6fe24e2's rule (no new low against every reading since the hold) stalls at k+3 -- read by
     passing another tree as argv[1] (the main checkout at 89c1ee9 carries that rule).

    python tests/test_hyp_segment.py [tree]
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

env = world.bind(panel._gridworld("gridworld_arc_s1")[0])
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="hypseg"), tether.Config(), ledger.Ledger())
for _ in range(40):
    ag.step()
    if ag._hyp is not None:
        break
h = ag._hyp
sl = h["slots"][0]
queue = []
orig = ag.goal_residual


def gr(slot, state, counts=None, why=None):
    if slot == sl and queue:
        return queue[0]
    return orig(slot, state, counts, why)


ag.goal_residual = gr
ag._res.pop(sl, None)
h.update(steps=0, budget=99, reads={})
if "seg" in h:
    h.update(seg={}, touches=0, losses=0)
held = []
for v in (0.5, 0.0, 0.0635, 0.0317, 0.0159):
    queue[:] = [v]
    ag.note_goals(ag.env.observe())
    if ag._hyp is not None:
        ag._hyp_check()
    held.append(ag._hyp is not None)
    if ag._hyp is None:
        break
ends = [r["detail"] for r in ag.led.rows() if r["event"] == "goal_hypothesis_end"]
print(json.dumps({"held": held, "end": ends[-1] if ends and not held[-1] else None,
                  "touches": h.get("touches"), "losses": h.get("losses"),
                  "seg": h.get("seg", {}).get(sl)}, default=str))
'''


def _run(tree: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", TETHER_AGENT_SEED="0")
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, tree], env=env, capture_output=True,
                         text=True, timeout=900, cwd=tree)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def main() -> None:
    here = _repo.ROOT
    if len(sys.argv) > 1:
        r = _run(sys.argv[1])
        print(f"test_hyp_segment, other tree {sys.argv[1]}: held {r['held']}, end "
              f"{(r['end'] or {}).get('why')} by {(r['end'] or {}).get('by')}")
        return
    r = _run(here)
    assert r["held"] == [True] * 5, r
    assert r["touches"] == 1 and r["losses"] == 1 and r["seg"] == 2, r
    print(f"test_hyp_segment: pass (ON held through k+3 {r['held']}; touches {r['touches']}, "
          f"losses {r['losses']}, the approach reopened at reading {r['seg']})")


if __name__ == "__main__":
    main()
