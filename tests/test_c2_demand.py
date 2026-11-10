"""C2 P0: THE DEMAND RECORD (the reviewer 2026-11-09 r1399, r1610), record only, no arm. Each step's
@body heads line carries its thinking heads, the questions it left owed, and owed work it ran for an
earlier step, booked back to that step.

  E1  MF: an owed question planted at cycle 1 and asked later is booked "for" cycle 1, never for
      the step that ran it, with heads > 0
  E2  "deferred" names only questions first owed THIS step (a re-deferral keeps its first cycle)
  E3  think = total less the idle scopes' heads

    python tests/test_c2_demand.py
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def _heads(path: str) -> list:
    with open(f"{path}.body.jsonl", encoding="utf-8") as fh:
        return [b for b in map(json.loads, fh) if b.get("event") == "heads"]


def main() -> int:
    keep = (tether._STEP_ACT, tether._ROUTE_NAMED)
    tether._STEP_ACT, tether._ROUTE_NAMED = False, False    # the lookups run, so owed work is asked
    try:
        # mkdtemp: the ledger holds its file open, and Windows won't remove the directory
        path = os.path.join(tempfile.mkdtemp(prefix="c2_demand_"), "l.jsonl")
        env = world.bind(gridworld.family("default", 0))
        ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="c2_demand"), tether.Config(),
                          ledger.Ledger(path))
        for _ in range(3):
            ag.step()
        ag._owed_q.update({s: (1, s) for s in ag.slots})
        for _ in range(3):
            ag.step()
        lines = _heads(path)
    finally:
        tether._STEP_ACT, tether._ROUTE_NAMED = keep
    paid = [(b["cycle"], p) for b in lines for p in b["paid"]]
    assert paid, "no planted owed question was asked in 3 steps: the occasion is missing"
    for c, p in paid:
        assert p["for"] == 1 and p["for"] != c and p["heads"] > 0, \
            f"MUST-FAIL: owed work at c{c} booked for {p['for']}, not the step that owed it: {p}"
    for b in lines:
        assert all(q[0] == b["cycle"] for q in b["deferred"]), b["deferred"]
        idle = sum(b["scopes"].get(k, 0) for k in tether._TC_IDLE_SCOPES)
        assert b["think"] == b["total"] - idle, b
    ran = sorted({c for c, _ in paid})
    print(f"  E1: {len(paid)} owed lookups planted at c1 and run at c{ran} booked for c1 "
          f"({sum(p['heads'] for _, p in paid)} heads)")
    print("  E2: deferred names only questions first owed that step")
    print("  E3: think = total less the idle scopes")
    print("c2_demand: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
