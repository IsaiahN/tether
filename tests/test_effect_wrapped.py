"""TETHER_EFFECT_WRAPPED (the reviewer 2026-11-10 r1627 (E)): a press's effect is signed by the
minimal difference mod the slot's alphabet, so a one-cell wrap reads as the step the bet reads.

  w1 (a) MUST-FAIL: 0 -> 4 on n = 5 signs "?.row-" ON and "?.row+" OFF;
  w2 (b) a step that does not wrap (2 -> 1) signs "?.row-" both ways;
  w3 (c) MUST-FAIL: a press stepping the same way in and out of the wrap (3 -> 2, then 0 -> 4)
     books ONE signature in its context ON and two OFF (the false remap);
  w4 a step of exactly n/2 (0 -> 2 on n = 4) keeps the raw sign and is recorded as a tie, ON;
  w5 MUST-FAIL (r1629): the delta table takes the same step -- the 0 -> 4 press adds -1 to its
     running total ON and +4 OFF;
  w6 MUST-FAIL (r1630): Agent.can() -- with up seen to move o0.row 3 -> 2 and 2 -> 1, dec bound,
     the row at 0 and its target one wrapped cell away (4) is reachable ON ("yes") and not
     OFF (the raw direction reads the step as the wrong way).

    python tests/test_effect_wrapped.py
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
import interface as IF
ctx = ("ctx",)
def press(f, a, b, n=5, act="up"):
    f.audit(IF.Realisation(act), {"o0.row": a}, {"o0.row": b}, ctx, alphabet={"o0.row": n})
    return f
out = {}
out["w1"] = sorted(press(IF.Interface(), 0, 4).known_forms("up", ctx))
out["w2"] = sorted(press(IF.Interface(), 2, 1).known_forms("up", ctx))
f = press(press(IF.Interface(), 3, 2), 0, 4)
out["w3"] = len(f.table["up"]["by_ctx"][ctx])
f = press(IF.Interface(), 0, 2, n=4)
out["w4"] = [sorted(f.known_forms("up", ctx)), f.effect_ties]
f = press(IF.Interface(), 0, 4)
out["w5"] = sum(t for (c, k, _r), (_n, t) in f.table["up"]["delta"].items() if k == "o0.row")
print(json.dumps(out))
'''

CAN = r'''
import json, sys
sys.dont_write_bytecode = True
import gamma, ledger, tether, world
from conform import panel
S = "o0.row"
g, seed = panel._gridworld("gridworld_s0")
env = world.bind(g)
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"t_{seed}"), tether.Config(),
                  ledger.Ledger())
ag.step()
def row(a, b):
    x = dict(g.state)
    x[S] = a
    y = dict(x)
    y[S] = b
    return (x, "up", y, None, None)
ag.trace = [row(3, 2), row(2, 1)]
ag.bound[S] = "dec"
ag._hyp, ag._disc = None, {}
ag._discrepancy = lambda s, st: 1
st = dict(g.state)
st[S] = 0
print(json.dumps({"w6": str(ag.can(S, st)), "wanted": ag._predict(S, st, "up")}))
'''


def _run(on: bool, probe: str = PROBE) -> dict:
    env = dict(os.environ, TETHER_EFFECT_WRAPPED="1" if on else "0", PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, "-c", probe], capture_output=True, text=True, env=env,
                       cwd=_repo.ROOT, timeout=300)
    assert p.returncode == 0, p.stderr[-2500:]
    return json.loads(p.stdout.strip().splitlines()[-1])


if __name__ == "__main__":
    on, off = _run(True), _run(False)
    assert "?.row-" in on["w1"] and "?.row+" not in on["w1"], on
    assert "?.row+" in off["w1"], off
    print(f"  w1 0 -> 4 on n = 5: ON {on['w1']}, OFF {off['w1']} (MUST-FAIL)")
    assert "?.row-" in on["w2"] and on["w2"] == off["w2"], (on, off)
    print(f"  w2 2 -> 1: {on['w2']} both ways")
    assert on["w3"] == 1 and off["w3"] == 2, (on, off)
    print(f"  w3 up in and out of the wrap: ON {on['w3']} signature, OFF {off['w3']} (MUST-FAIL)")
    assert "?.row+" in on["w4"][0] and on["w4"][1] == ["o0.row"], on
    print(f"  w4 0 -> 2 on n = 4 (a tie): {on['w4'][0]}, tie recorded on {on['w4'][1]}")
    assert on["w5"] == -1 and off["w5"] == 4, (on, off)
    print(f"  w5 the delta table on 0 -> 4: ON {on['w5']}, OFF {off['w5']} (MUST-FAIL)")
    con, coff = _run(True, CAN), _run(False, CAN)
    assert con["wanted"] == 4 and con["w6"] == "yes" and coff["w6"] != "yes", (con, coff)
    print(f"  w6 can(): target 4 from row 0 under dec: ON {con['w6']}, OFF {coff['w6']} "
          f"(MUST-FAIL)")
    print("effect wrapped: OK")
