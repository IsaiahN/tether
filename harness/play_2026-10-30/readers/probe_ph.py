"""A read: does each of P0/P6/P11's entries fire in the fake game within 20 steps, and where does the cut land?"""
import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True
REPO = sys.argv[1]
CHILD = r'''
import json, os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
sys.path.insert(1, os.path.join(sys.argv[1], "tests"))
import arc_holdout, cap, tether
from test_entry import FakeWrapper
tether._AGENT_SEED = False
env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake")
fn = sys.argv[2]
calls, fired = [], []
real = getattr(tether.Agent, fn)
def hooked(self, *a, **k):
    calls.append(self.cycle)
    return real(self, *a, **k)
setattr(tether.Agent, fn, hooked)
for _ in range(20):
    env.observe()
    ag.step()
print(json.dumps({"fn": fn, "calls": calls[:10], "n": len(calls)}))
'''
env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")
for fn in ("_size_fold", "_respell_goals", "_intent_root", "_utter", "_flush_probe"):
    p = subprocess.run([sys.executable, "-B", "-c", CHILD, REPO, fn], capture_output=True, text=True,
                       env=env, cwd=REPO, stdin=subprocess.DEVNULL, timeout=900)
    print(p.stdout.strip().splitlines()[-1] if p.returncode == 0 else ("ERR", fn, p.stderr[-500:]))
