"""The stub-step edits to the must-fail draft (the reviewer 2026-10-22 10:14 (4)). argv: file"""
import sys
from pathlib import Path

p = Path(sys.argv[1])
s = p.read_text(encoding="utf-8")


def rep(old, new):
    global s
    assert s.count(old) == 1, (old, s.count(old))
    s = s.replace(old, new)


rep("harness/mem_store/e4_stream.py compared terminal() to \"win\", a word F1b (29d3f59) renamed to\n"
    "ledger.WIN, so a won game never ended its slice. This drives e4_stream's REAL loop (as\n"
    "tiers_timer.py does: the class patched, then the file run) in two children, one game, N agent\n"
    "steps, seed 00000000, with arc_world.ArcWorld.terminal answering ledger.WIN from the agent's K-th\n"
    "step on (so which game the seed puts first does not matter; switch.tsv names it):\n",
    "harness/mem_store/e4_stream.py compared terminal() to \"win\", a word F1b (29d3f59) renamed to\n"
    "ledger.WIN, so a won game never ended its slice. This drives e4_stream's REAL loop (as\n"
    "tiers_timer.py does: the class patched, then the file run) in two children, one game, N agent\n"
    "steps, seed 00000000, with arc_world.ArcWorld.terminal answering ledger.WIN from the agent's K-th\n"
    "step on (so which game the seed puts first does not matter; switch.tsv names it). The agent is\n"
    "real (a cold load through arc_holdout.wire) but its step is a STUB, patched in the child only:\n"
    "it counts and returns True, the real step's return on an acted turn (tether.Agent.step -> bool),\n"
    "which e4_stream.py:151 discards. A real step on a cold agent takes minutes (lf52, 2026-10-22), and\n"
    "this test's subject is the loop's end check; what it gives up: it does not show a REAL step\n"
    "reaching that check.\n")
rep("_step, _term = tether.Agent.step, arc_world.ArcWorld.terminal\n"
    "def step(self, *a, **kw):\n"
    "    r = _step(self, *a, **kw)\n"
    "    seen[\"steps\"] += 1\n"
    "    return r\n",
    "_term = arc_world.ArcWorld.terminal\n"
    "def step(self, *a, **kw):   # the stub: an acted turn, no deliberation (the test's subject is the loop)\n"
    "    seen[\"steps\"] += 1\n"
    "    return True\n")
p.write_text(s, encoding="utf-8", newline="\n")
print("ok")
