"""TETHER_SWEEP_STAMP (the reviewer 2026-11-10 r1626 (S)): a sweep's _reach rescan of a parked
record that finds nothing is not re-run until the unit set grows again.

  s1 ON: two sweeps with no unit growth run _reach ONCE on the record;
  s2 ON: unit growth between the two sweeps runs it twice;
  s3 MUST-FAIL, OFF: two sweeps with no unit growth run it twice, as before.

    python tests/test_sweep_stamp.py
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
import gamma, ledger, tether, world
from conform import panel
g, seed = panel._gridworld("gridworld_s0")
env = world.bind(g)
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"t_{seed}"), tether.Config(), ledger.Ledger())
for _ in range(4):
    ag.step()
slot = next(s for s in ("o0.col", "o0.row") if len({v for _, _, v, _, _ in ag.history(s)}) > 1)
calls = []
ag._reach = lambda s, h, sl: calls.append(s) or None
ag._turn_ahead = None
ag.owed_import = set()
units = [5]
ag.gamma.units = lambda: [0] * units[0]
ag.parked = {"k": {"slot": slot, "hist": ag.history(slot), "slots": list(ag.slots),
                   "verdict": "budget_spent", "units_then": 1}}
term = ag.gamma.library[tether.IDN]
def two(grow):
    calls.clear()
    ag.parked["k"].pop("rescan_units", None)
    ag.sweep(term, "@none")
    if grow:
        units[0] += 1
    ag.sweep(term, "@none")
    return calls.count(slot)
print(json.dumps({"slot": slot, "flat": two(False), "grow": two(True)}))
'''


def _run(on: bool) -> dict:
    env = dict(os.environ, TETHER_SWEEP_STAMP="1" if on else "0", PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, "-c", PROBE], capture_output=True, text=True, env=env,
                       cwd=_repo.ROOT, timeout=600)
    assert p.returncode == 0, p.stderr[-2500:]
    return json.loads(p.stdout.strip().splitlines()[-1])


if __name__ == "__main__":
    on, off = _run(True), _run(False)
    assert on["flat"] == 1, on
    print(f"  s1 ON, no unit growth: _reach on {on['slot']} {on['flat']} time over two sweeps")
    assert on["grow"] == 2, on
    print(f"  s2 ON, units grew between: {on['grow']} times")
    assert off["flat"] == 2, off
    print(f"  s3 OFF, no unit growth: {off['flat']} times (MUST-FAIL: every sweep re-runs it)")
    print("sweep stamp: OK")
