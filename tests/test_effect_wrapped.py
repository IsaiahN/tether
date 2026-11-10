"""TETHER_EFFECT_WRAPPED (the reviewer 2026-11-10 r1627 (E)): a press's effect is signed by the
minimal difference mod the slot's alphabet, so a one-cell wrap reads as the step the bet reads.

  w1 (a) MUST-FAIL: 0 -> 4 on n = 5 signs "?.row-" ON and "?.row+" OFF;
  w2 (b) a step that does not wrap (2 -> 1) signs "?.row-" both ways;
  w3 (c) MUST-FAIL: a press stepping the same way in and out of the wrap (3 -> 2, then 0 -> 4)
     books ONE signature in its context ON and two OFF (the false remap);
  w4 a step of exactly n/2 (0 -> 2 on n = 4) keeps the raw sign and is recorded as a tie, ON;
  w5 MUST-FAIL (r1629): the delta table takes the same step -- the 0 -> 4 press adds -1 to its
     running total ON and +4 OFF.

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


def _run(on: bool) -> dict:
    env = dict(os.environ, TETHER_EFFECT_WRAPPED="1" if on else "0", PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, "-c", PROBE], capture_output=True, text=True, env=env,
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
    print("effect wrapped: OK")
