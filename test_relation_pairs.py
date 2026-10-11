"""B2, TETHER_RELATION_SET (the reviewer 2026-10-11 14:19Z, 14:33Z): pair relations as slots on
gridworld, every ordered pair, `{a}.{rel}_{b}`. The arm is read at import: each half runs alone.

  OFF: no pair slot in observe(), slots(), alphabet() or relational_slots().
  ON:  6 x 5 x 5 = 150 pair slots; each value equals the relation computed by hand from the two
       objects' cells (box gap, offset, containment, contact); every one has an owner (the
       subject), an alphabet, a type, and is declared relational.

    python test_relation_pairs.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
import gridworld
from conform import panel
g, _seed = panel._gridworld("gridworld_s0")
obs, slots, alpha = g.observe(), g.slots(), g.alphabet()
pairs = sorted(k for k in obs if "_" in k.split(".", 1)[1] and k.split(".", 1)[1].split("_")[0]
               in ("dist", "drow", "dcol", "inside", "touches"))
own, types, rel = g.slot_owner(), g.slot_types(), set(g.relational_slots())
bad = []
for k in pairs:
    a, attr = k.split(".", 1)
    r, b = attr.split("_", 1)
    ra, rb = (g.state[a + ".row"], g.state[a + ".col"]), (g.state[b + ".row"], g.state[b + ".col"])
    gap = max(0, abs(ra[0] - rb[0]) - 1, abs(ra[1] - rb[1]) - 1)
    want = {"dist": gap, "drow": rb[0] - ra[0], "dcol": rb[1] - ra[1],
            "inside": int(ra == rb), "touches": int(gap == 0)}[r]
    if obs[k] != want:
        bad.append([k, obs[k], want])
    if own.get(k) != a or k not in alpha or k not in types or attr not in rel or k not in slots:
        bad.append([k, "contract"])
print(json.dumps({"n": len(pairs), "bad": bad[:10], "nbad": len(bad)}))
'''


def _run(on: bool) -> dict:
    env = dict(os.environ, TETHER_RELATION_SET="1" if on else "0", PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, "-c", PROBE], capture_output=True, text=True, env=env,
                       cwd=os.path.dirname(os.path.abspath(__file__)), timeout=240)
    assert p.returncode == 0, p.stderr[-2000:]
    return json.loads(p.stdout.strip().splitlines()[-1])


if __name__ == "__main__":
    off = _run(False)
    assert off["n"] == 0, off
    print("  OFF: no pair slots")
    on = _run(True)
    assert on["n"] == 150 and on["nbad"] == 0, on
    print(f"  ON: {on['n']} pair slots, every value equal to the hand-computed relation, every one "
          f"owned, typed, sized and declared relational")
    print("relation pairs: OK")
