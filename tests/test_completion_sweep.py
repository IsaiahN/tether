"""Objective build 1, the completion sweep (TETHER_COMPLETION_SWEEP; ARC_AGENT 21.3; the reviewer
2026-10-11 02:19Z). When the WORLD's objective degree reaches 1.0, the segment since the last
completion is re-examined and recorded. Record only.

  must-pass: gridworld_s0, 15 cycles ON: one sweep row per world 0 -> 1 flip of the goal (s0
     reaches it at c11), carrying what was live, settled and closed in the segment;
  a. the WORLD's verdict only: on every cycle where the agent's own bet PREDICTED the goal
     complete and the world said not, no sweep row (and such cycles exist on this run);
  b. nothing retargeted, no binding dropped, no trace cleared: a snapshot either side of each
     sweep call is unchanged;
  c. a run with no completion writes no sweep row (the world's degree held at 0);
  OFF: the sweep never runs.

    python tests/test_completion_sweep.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
import gamma
import ledger
import tether
import world

sys.dont_write_bytecode = True
sys.path.insert(0, "conform")
import panel  # noqa: E402

real = tether.Agent._completion_sweep
calls: list = []


def _checked(self, degree):
    before = (dict(self.bound), len(self.trace), self.level, set(self.owed_import))
    real(self, degree)
    assert (dict(self.bound), len(self.trace), self.level, set(self.owed_import)) == before, \
        "b: a sweep changed a live structure"
    calls.append(degree)


def _agent(member="gridworld_s0"):
    g, seed = panel._gridworld(member)
    env = world.bind(g)
    return tether.Agent(env, gamma.Gamma(env.atoms(), game=f"dt_default_{seed}"),
                        tether.Config(), ledger.Ledger())


def _run(n, on=True, stub=None):
    was = tether._COMPLETION_SWEEP
    tether._COMPLETION_SWEEP = on
    try:
        ag = _agent()
        if stub is not None:
            ag.env.objective = stub
        for _ in range(n):
            ag.step()
    finally:
        tether._COMPLETION_SWEEP = was
    return ag.led.rows()


if __name__ == "__main__":
    # C-seed-X (2026-10-20): the must-pass needs gridworld_s0 to reach its goal within 15 cycles,
    # which depends on the per-process birth seed (2 of 7 unpinned runs did not); one temperament
    tether._AGENT_SEED = False
    tether.Agent._completion_sweep = _checked
    rows = _run(15)
    goal = {r["cycle"]: r["detail"] for r in rows
            if r["event"] == "bet" and r["slot"] == "@goal.completed"}
    flips = [c for c in sorted(goal) if goal[c].get("actual") == 1
             and goal[c].get("from_value") == 0]
    sweeps = [r for r in rows if r["event"] == "completion_sweep"]
    assert flips and len(sweeps) == len(flips), (flips, [r["cycle"] for r in sweeps])
    d = sweeps[0]["detail"]
    print(f"  must-pass: world flips at {flips}; sweep rows at {[r['cycle'] for r in sweeps]}; "
          f"first: segment from c{d['segment_from_cycle']}, {len(d['live'])} live, settled "
          f"{len(d['settled_in_segment'])}, closed {len(d['closed_in_segment'])}, still owed "
          f"{len(d['still_owed'])}")
    agent_only = [c for c, x in goal.items() if x.get("predicted") == 1 and x.get("actual") == 0]
    sweep_cycles = {r["cycle"] for r in sweeps}
    assert agent_only, "fixture: the agent never predicted completion alone, so a is vacuous"
    assert not sweep_cycles & set(agent_only)
    print(f"  a: the agent alone predicted completion on {len(agent_only)} cycles; no sweep on any")
    print(f"  b: {len(calls)} sweep calls, bound / trace / level / owed unchanged across each")
    none = _run(10, stub=lambda: ("BECOME(o0, target)", 0.0))
    assert not [r for r in none if r["event"] == "completion_sweep"]
    print("  c: the world's degree held at 0 for 10 steps: no sweep row")
    tether.Agent._completion_sweep = real

    def _never(*_a, **_k):
        raise AssertionError("the sweep ran with the arm OFF")
    tether.Agent._completion_sweep = _never
    off = _run(15, on=False)
    tether.Agent._completion_sweep = real
    assert not [r for r in off if r["event"] == "completion_sweep"]
    print("  OFF: 15 steps, the sweep never ran")
    print("ok")
