"""THE CAP ENDS A STEP BETWEEN LOOKUPS, TETHER_CAP_MIDSTEP (the reviewer 2026-10-17 10:47, 11:35).
gridworld_s2 (C-seed-X): an agent steps until its library route runs, then its deadline is set in
the past and it steps again.

  P1 the step ends between lookups: no exception escapes, one ROUTE "@cap" cap_mid_step row with
     its overrun_s (wall at the cap minus the deadline, >= 0), and no library row after the deadline
  P2 the record still flushes: lineage.write after the cap writes a generation carrying entry_use,
     and a fresh agent loads equal counts
  MF-P1 TETHER_CAP_MIDSTEP=0: the same deadline is ignored inside the step (no cap row, library
     rows written after it)

    python test_cap_midstep.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True

CHILD = r'''
import json, os, sys, tempfile
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.getcwd(), "conform"))
import gamma, ledger, lineage, panel, tether, world
g, seed = panel._gridworld("gridworld_s2")
env = world.bind(g)
d = tempfile.mkdtemp()
led = os.path.join(d, "gw.jsonl")
ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"gate_{seed}"), tether.Config(),
                  ledger.Ledger(path=led))
def rows():
    return [json.loads(x) for x in open(led, encoding="utf-8")]
n = 0
while n < 12 and not any(r.get("event") == "library" for r in rows()):
    ag.step(); n += 1
before = len(rows())
ag.deadline = 0.0
acted = None
for _ in range(4):
    acted = ag.step()
after = rows()[before:]
cap = [r for r in after if r.get("event") == "cap_mid_step"]
libs = [r for r in after if r.get("event") == "library"]
out = {"warm_steps": n, "cap_rows": len(cap), "lib_after": len(libs), "acted": acted,
       "overrun": [r["detail"].get("overrun_s") for r in cap],
       "cap_slot": cap[0]["slot"] if cap else None}
if tether._ENTRY_USE and tether._CAP_MIDSTEP:
    ld = os.path.join(d, "lin")
    lineage.write(ld, ag, "gw")
    gens = [f for f in os.listdir(ld) if f.startswith("gen_")]
    eu = json.loads(open(os.path.join(ld, gens[0]), encoding="utf-8").read()).get("entry_use", {})
    ag2 = tether.Agent(world.bind(panel._gridworld("gridworld_s2")[0]),
                       gamma.Gamma(env.atoms(), game=f"gate_{seed}"), tether.Config(),
                       ledger.Ledger(path=os.devnull))
    lineage.load(ld, ag2)
    out.update(written=len(eu), loaded=len(ag2._entry_use_in),
               equal=all(ag2._entry_use_in.get(k, {}).get(f) == v for k, c in ag._entry_use.items()
                         for f, v in c.items()))
print(json.dumps(out))
'''


def child(extra: dict) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", **extra})
    p = subprocess.run([sys.executable, "-B", "-c", CHILD], capture_output=True, text=True,
                       env=env, cwd=os.path.dirname(os.path.abspath(__file__)),
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-2000:]
    return json.loads(p.stdout.strip().splitlines()[-1])


def main() -> int:
    on = child({})
    assert on["cap_rows"] >= 1 and on["lib_after"] == 0 and on["cap_slot"] == "@cap", on   # P1
    assert all(isinstance(x, float) and x >= 0 for x in on["overrun"]), on["overrun"]
    assert on["written"] > 0 and on["loaded"] == on["written"] and on["equal"], on       # P2
    print("P1 cap row", on["cap_rows"], "library rows after the deadline", on["lib_after"],
          "; P2 entry_use written", on["written"], "loaded", on["loaded"], "equal", on["equal"])
    off = child({"TETHER_CAP_MIDSTEP": "0"})
    assert off["cap_rows"] == 0 and off["lib_after"] > 0, off                            # MF-P1
    print("MF-P1 OFF: cap rows", off["cap_rows"], "library rows after the deadline",
          off["lib_after"])
    print("cap_midstep: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
