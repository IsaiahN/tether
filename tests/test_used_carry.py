"""L1b, THE CODE'S WEIGHTS CROSS THE LINEAGE, TETHER_USED_CARRY (the reviewer 2026-10-17 19:06).

  C   process 1 plays the fake ARC game (12 actions, C-seed-X) into a lineage folder, notes 5
      closures on translate and 3 on recolour through Rank.note (the one writer), then writes the
      generation. Process 2 loads the folder: its carried Rank.used equals process 1's, unit for
      unit
  ONE every unit's code weight in process 2 is its carried used PLUS the paid 7i's replay put back
      in standing -- paid is counted once, in one place, never carried a second time (the
      reviewer 2026-10-17 19:33)
  MF  the same two processes with the arm OFF: process 2 carries no used; its code weight is the
      replayed paid alone
  H   the @run row names the alphabet in force: 80 on the fake (ARC atoms, arc_world imported)

    python tests/test_used_carry.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
HERE = _repo.ROOT

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
    out["used"], out["paid"], out["stated"] = ag.gamma.unit_weights()
    ag.end_run("cap")
    out["wrote"] = bool(lineage.write(d, ag, "fake"))
    hdr = [json.loads(x) for x in open(led, encoding="utf-8") if '"@run"' in x]
    out["alphabet"] = next(r["detail"].get("alphabet") for r in hdr if r["event"] == "arms")
else:
    c = ag.gamma.code()
    z = c.info["z"]
    out["carried"] = ag.gamma.carried_used
    out["paid"] = ag.gamma.unit_weights()[1]
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
    assert p1["wrote"] and p1["used"].get("translate", 0) >= 5, p1                        # pre
    p2 = child("p2", d, "1")
    assert p2["carried"] == p1["used"], (p1, p2)                                          # C
    print("C process 1 used (its own closures", p1["own"] or "none", "+ 5 translate + 3 recolour):",
          p1["used"], "; process 2 carries", p2["carried"])
    def one(r):
        return all(v == r["carried"].get(k, 0) + r["paid"].get(k, 0)
                   for k, v in r["code_w"].items())
    assert one(p2), (p2["code_w"], p2["carried"], p2["paid"])                            # ONE
    print("ONE every code weight = carried used + replayed paid; paid at process 1's write",
          p1["paid"], "replayed in process 2", p2["paid"])
    d0 = tempfile.mkdtemp()
    child("p1", d0, "0")
    q2 = child("p2", d0, "0")
    assert not q2["carried"] and one(q2), q2                                               # MF
    print("MF the arm off: process 2 carries no used; its code weights are the replayed paid",
          q2["paid"])
    assert p1["alphabet"] == 80, p1["alphabet"]                                            # H
    print("H the @run row names alphabet", p1["alphabet"])
    print("used_carry: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
