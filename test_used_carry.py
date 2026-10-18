"""L1b, THE CODE'S WEIGHTS CROSS THE LINEAGE, TETHER_USED_CARRY (the reviewer 2026-10-17 19:06).

  C   process 1 plays the fake ARC game (12 actions, C-seed-X) into a lineage folder; its own
      closures there are none, so it notes 5 on translate and 3 on recolour through Rank.note
      (the one writer), then writes the generation. Process 2 loads the folder: its carried weights
      equal process 1's unit weights at the write, key for key, and its code's weight on each of
      those units is that count
  MF  the same two processes with the arm OFF: process 2 carries nothing and its code is flat
  H   the @run row names the alphabet in force: 80 on the fake (ARC atoms, arc_world imported)

    python test_used_carry.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))

CHILD = r'''
import json, os, sys, tempfile
sys.dont_write_bytecode = True
import arc_holdout, gamma, lineage, tether
from test_entry import FakeWrapper
tether._AGENT_SEED = False
mode, d = sys.argv[1], sys.argv[2]
led = os.path.join(tempfile.mkdtemp(), "u.jsonl")
env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake", led_path=led, lineage_dir=d)
out = {}
if mode == "p1":
    for _ in range(12):
        env.observe()
        ag.step()
        if env.terminal():
            break
    out["own"] = dict(ag.gamma.unit_weights()[0])
    for name, n in (("translate", 5), ("recolour", 3)):
        for _ in range(n):
            ag.rank.note(name, ag.cycle)
    out["weights"], out["stated"] = ag.gamma.unit_weights()
    ag.end_run("cap")
    out["wrote"] = bool(lineage.write(d, ag, "fake"))
    hdr = [json.loads(x) for x in open(led, encoding="utf-8") if '"@run"' in x]
    out["alphabet"] = next(r["detail"].get("alphabet") for r in hdr if r["event"] == "arms")
else:
    c = ag.gamma.code()
    z = c.info["z"]
    out["carried"], out["carried_stated"] = ag.gamma.carried_weights, ag.gamma.carried_stated
    out["code_w"] = {gamma.unit_key(k): round(z * 2 ** -v - 1, 6) for k, v in c.cost.items()}
print("RESULT", json.dumps(out))
'''


def child(mode: str, d: str, arm: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "TETHER_USED_CARRY": arm})
    p = subprocess.run([sys.executable, "-B", "-c", CHILD, mode, d], capture_output=True,
                       text=True, env=env, cwd=HERE, stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-3000:]
    line = next(x for x in p.stdout.splitlines() if x.startswith("RESULT "))
    return json.loads(line[len("RESULT "):])


def main() -> int:
    d = tempfile.mkdtemp()
    p1 = child("p1", d, "1")
    assert p1["wrote"] and p1["weights"].get("translate") == 5, p1                        # pre
    p2 = child("p2", d, "1")
    assert p2["carried"] == p1["weights"] and p2["carried_stated"] == p1["stated"], (p1, p2)  # C
    assert all(p2["code_w"][k] == n for k, n in p1["weights"].items()), (p1, p2)
    print("C process 1 (own closures on the fake:", p1["own"] or "none", ") noted 5 on translate "
          "and 3 on recolour and wrote; process 2 carries", p2["carried"], "and its code weighs",
          {k: p2["code_w"][k] for k in p1["weights"]})
    d0 = tempfile.mkdtemp()
    child("p1", d0, "0")
    q2 = child("p2", d0, "0")
    assert not q2["carried"] and all(v == 0 for v in q2["code_w"].values()), q2           # MF
    print("MF the arm off: process 2 carries nothing; every unit's code weight is 0")
    assert p1["alphabet"] == 80, p1["alphabet"]                                            # H
    print("H the @run row names alphabet", p1["alphabet"])
    print("used_carry: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
