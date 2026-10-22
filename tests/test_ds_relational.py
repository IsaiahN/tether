"""DS (3), THE RELATIONAL GAP UNDER BOTH ARMS (the reviewer 2026-10-20 10:11, P1):
test_relation_derived's three cases on gridworld_s0's first derived slot, calling
_relational_surprise directly, each recorded as [k in res, relational_surprise rows, derived_new
rows]:

  m1 held          the derived prediction holds, every source held      OFF [F,0,0]   ON [F,0,0]
  m2 blocked       every source held, the observed relation differs      OFF [T,1,0]   ON [F,0,1]
  m3 source missed a source's own residual carries it                    OFF [F,0,0]   ON [F,0,0]
  MF  each arm's result read against the OTHER arm's expectation differs on m2 and on nothing else

    python tests/test_ds_relational.py
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
S = tether.SlotResidual
k = sorted(g.derived())[0]
srcs = g.derived()[k]
ag.alphabet = ag._alphabets(env)
def case(src_bits, after_k, dpred_k):
    res = {s: S(s, tether.TRANSITION, 1, 1, src_bits) for s in srcs}
    n0 = len(ag.led.rows())
    ag._relational_surprise({k: srcs}, {k: dpred_k}, res, {k: after_k}, {k: dpred_k})
    rows = [r["event"] for r in ag.led.rows()[n0:]]
    return [k in res, rows.count("relational_surprise"), rows.count("derived_new")]
print(json.dumps({"arm": tether._DERIVED_SUBJECT, "slot": k, "m1": case(0, 2, 2),
                  "m2": case(0, 3, 2), "m3": case(1.0, 3, 2)}))
'''
WANT = {False: {"m1": [False, 0, 0], "m2": [True, 1, 0], "m3": [False, 0, 0]},
        True: {"m1": [False, 0, 0], "m2": [False, 0, 1], "m3": [False, 0, 0]}}


def run(arm: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", TETHER_RELATION_SET="1", TETHER_DERIVED_SUBJECT=arm)
    here = _repo.ROOT
    p = subprocess.run([sys.executable, "-B", "-c", PROBE], capture_output=True, text=True, env=env,
                       cwd=here, stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-2000:]
    return json.loads(p.stdout.strip().splitlines()[-1])


def misses(got: dict, want: dict) -> list:
    return [m for m in ("m1", "m2", "m3") if got[m] != want[m]]


def main() -> int:
    off, on = run("0"), run("1")
    assert off["arm"] is False and on["arm"] is True, (off, on)
    print("OFF", off["slot"], {m: off[m] for m in ("m1", "m2", "m3")})
    print("ON ", on["slot"], {m: on[m] for m in ("m1", "m2", "m3")})
    assert misses(off, WANT[False]) == [], off                                        # OFF
    assert misses(on, WANT[True]) == [], on                                           # ON
    mf = (misses(off, WANT[True]), misses(on, WANT[False]))
    assert mf == (["m2"], ["m2"]), mf                                                 # MF
    print("MF each arm against the other's expectation differs on:", mf)
    print("ds_relational: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
