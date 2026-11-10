"""TETHER_DERIVE_AS_JUDGED (the reviewer 2026-11-10 r1625): derive() reads each bet slot's value as
the settle judged it (the code), never the raw value -- one prediction, one decoding.

  j0 treatment: o0.col's predicted state carries the code ON and the raw value OFF;
  j1 (a) MUST-FAIL: a wrapped source (raw = code - alphabet, held) fires NO relational_surprise ON,
     and does OFF -- the echo;
  j2 (b) a genuinely surprising relation (sources held, its board value differs from derive on the
     judged values) still fires ON, exactly once, so the arm silences only the echo.

    python tests/test_derive_judged.py
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
ag.alphabet = ag._alphabets(env)
before = dict(g.state)
derived = g.derived()
s = "o0.col"
code = before[s]
raw = code - ag.alphabet[s]
ps = ag._derive_sources(before, [s], {s: code}, {s: raw})
dpred = {k: v for k, v in ag._derive(ps, before).items() if k in derived}
after = dict(before)
after.update({k: v for k, v in ag._derive(dict(before), before).items() if k in derived})
S = tether.SlotResidual
srcs = {x for v in derived.values() for x in v}
def surprises(aft):
    ag._rel_subjects = set()
    res = {x: S(x, tether.TRANSITION, before[x], before[x], 0.0) for x in srcs}
    n0 = len(ag.led.rows())
    ag._relational_surprise(derived, dpred, res, aft, before)
    return [r["slot"] for r in ag.led.rows()[n0:] if r["event"] == "relational_surprise"]
out = {"j0": [ps[s], code, raw], "j1": surprises(after)}
k = sorted(k for k in derived if k in dpred and s not in derived[k])[0]
bent = dict(after)
bent[k] = dpred[k] + 1
out["j2"] = [k, surprises(bent)]
print(json.dumps(out))
'''


def _run(on: bool) -> dict:
    env = dict(os.environ, TETHER_RELATION_SET="1", TETHER_DERIVE_AS_JUDGED="1" if on else "0",
               PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, "-c", PROBE], capture_output=True, text=True, env=env,
                       cwd=_repo.ROOT, timeout=600)
    assert p.returncode == 0, p.stderr[-2500:]
    return json.loads(p.stdout.strip().splitlines()[-1])


if __name__ == "__main__":
    on, off = _run(True), _run(False)
    assert on["j0"][0] == on["j0"][1] and off["j0"][0] == off["j0"][2], (on, off)
    print(f"  j0 o0.col into derive: ON {on['j0'][0]} (the code), OFF {off['j0'][0]} (raw)")
    assert on["j1"] == [], on
    assert off["j1"], off
    print(f"  j1 wrapped source held: ON {len(on['j1'])} surprises; OFF {len(off['j1'])} "
          f"(MUST-FAIL: the echo, e.g. {off['j1'][:3]})")
    assert on["j2"][1] == [on["j2"][0]], on
    print(f"  j2 a genuine relational surprise on {on['j2'][0]} still fires ON: {on['j2'][1]}")
    print("derive as judged: OK")
