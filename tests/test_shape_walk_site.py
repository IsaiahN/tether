"""P5, 8b-2: the call site (TETHER_SHAPE_WALK; the reviewer's patch, r1838; DESIGN_STEP8 B4/B5).
gridworld default 0, 12 steps.

  SS1   ON: the mint walks gamma.ordered_closure (and never enumerate_closure's by-fit walk), and
        the frontier stop is ASKED (a walk with residual rows passes its per-stream bound). Whether
        it fires is printed, not asserted: on gw12 and dc22 c0-9 the caller's own cut ends every
        walk first (P5 commit post).
  MF-SS1 the call site with no stop (the plant): the stop is never asked -> RED.
  SS2   OFF: the by-fit enumerate_closure walk, and ordered_closure is never called.
  gw12's OFF identity against the parent is the commit's check, not this file's.

    python tests/test_shape_walk_site.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
HERE = _repo.ROOT

CHILD = r'''
import json, os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.getcwd())
import gamma, gridworld, ledger, tether, world
G = gamma.Gamma
OUT = {"ordered": 0, "by_fit": 0, "stats": [], "asks": 0}
_oc, _ec = G.ordered_closure, G.enumerate_closure
def oc(self, *a, **k):
    OUT["ordered"] += 1
    if os.environ.get("PLANT_NO_STOP"):
        k["stop"] = None
    s0 = k.get("stop")
    if s0 is not None:
        def s1(m, _s=s0):
            OUT["asks"] += 1
            return _s(m)
        k["stop"] = s1
    st = a[4] if len(a) > 4 else k.get("stats")
    if st is not None:
        OUT["stats"].append(st)
    return _oc(self, *a, **k)
def ec(self, *a, **k):
    if k.get("order") is not None:
        OUT["by_fit"] += 1
    return _ec(self, *a, **k)
G.ordered_closure, G.enumerate_closure = oc, ec
env = world.bind(gridworld.family("default", 0))
ag = tether.Agent(env, G(env.atoms(), game="fam_default_0"), tether.Config(), ledger.Ledger())
for _ in range(12):
    ag.step()
stops = sum(1 for s in OUT["stats"] if s.get("frontier_stop"))
print("SITE " + json.dumps({"ordered": OUT["ordered"], "by_fit": OUT["by_fit"], "stops": stops,
                            "asks": OUT["asks"],
                            "pops": sum(s.get("pops", 0) for s in OUT["stats"])}))
'''


def run(arm: bool, plant: bool = False) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               TETHER_SHAPE_WALK="1" if arm else "0")
    if plant:
        env["PLANT_NO_STOP"] = "1"
    p = subprocess.run([sys.executable, "-B", "-c", CHILD], capture_output=True, text=True,
                       env=env, cwd=HERE, stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    return next(json.loads(x[5:]) for x in p.stdout.splitlines() if x.startswith("SITE "))


def main() -> int:
    on = run(True)
    print(f"   ON: {on}")
    ok1 = on["ordered"] > 0 and on["by_fit"] == 0 and on["asks"] > 0
    print("SS1 the mint walks ordered_closure and asks the frontier stop: "
          + ("GREEN" if ok1 else "RED"))
    assert ok1, on
    pl = run(True, plant=True)
    print(f"   the plant (no stop): {pl}")
    print("MF-SS1 no stop at the call site: " + ("RED" if pl["asks"] == 0
                                                  else "GREEN (the plant went unseen)"))
    assert pl["asks"] == 0, pl
    off = run(False)
    print(f"   OFF: {off}")
    ok2 = off["ordered"] == 0 and off["by_fit"] > 0
    print("SS2 OFF walks the by-fit enumerate_closure only: " + ("GREEN" if ok2 else "RED"))
    assert ok2, off
    print("shape_walk_site: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
