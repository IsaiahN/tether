"""THE HEADS COUNTER (the reviewer 2026-11-07 r1398, r1404 1): cap.HEADS counts every loop head,
the deadline unset included; each step's heads by scope go to the @body side file, never a row.
The fake ARC game, C-seed-X.

  H1  cap.head() counts with AT None, held, and with a deadline not yet reached
  H2  a run writes one @body "heads" line per step: total = unscoped + the scopes' sum, some step
      counts heads; no ledger row is a heads line

    python tests/test_heads.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
HERE = _repo.ROOT
sys.path.insert(0, HERE)

CHILD = r'''
import os, sys, tempfile
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
sys.path.insert(1, os.path.join(sys.argv[1], "tests"))
import tether, tether_agent
from test_entry import FakeWrapper
tether._AGENT_SEED = False
led = os.path.join(tempfile.mkdtemp(), "r.jsonl")
tether_agent.run(FakeWrapper(script={}), "fake", max_actions=int(sys.argv[2]), led_path=led)
print(led)
'''


def h1() -> None:
    import cap
    at, hold = cap.AT, cap._HOLD
    try:
        cap.AT, n0 = None, cap.HEADS
        for _ in range(7):
            cap.head()
        assert cap.HEADS - n0 == 7, (cap.HEADS, n0)
        cap._HOLD = 1
        cap.head()
        assert cap.HEADS - n0 == 8, "a held head is not counted"
        cap._HOLD, cap.AT = 0, time.time() + 3600
        cap.head()
        assert cap.HEADS - n0 == 9, "a head under a far deadline is not counted"
    finally:
        cap.AT, cap._HOLD = at, hold
    print("H1  cap.head() counts with AT None, held, and under a deadline: 9 of 9")


def h2(n: int = 6) -> None:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")
    p = subprocess.run([sys.executable, "-B", "-c", CHILD, HERE, str(n)], capture_output=True,
                       text=True, env=env, cwd=HERE, stdin=subprocess.DEVNULL, timeout=600)
    assert p.returncode == 0, p.stderr[-2000:]
    led = p.stdout.strip().splitlines()[-1]
    with open(led, encoding="utf-8") as fh:
        rows = [json.loads(x) for x in fh if x.strip()]
    assert os.path.exists(led + ".body.jsonl"), "no @body side file"
    with open(led + ".body.jsonl", encoding="utf-8") as fh:
        body = [json.loads(x) for x in fh if x.strip()]
    heads = [b for b in body if b.get("event") == "heads"]
    assert heads, "no heads line in @body"
    for b in heads:
        assert b["total"] == b["unscoped"] + sum(b["scopes"].values()), b
    assert any(b["total"] > 0 for b in heads), "no step counted a head"
    cyc = [b["cycle"] for b in heads]
    assert cyc == sorted(cyc), cyc
    assert not [r for r in rows if r.get("event") == "heads"], "a heads line reached the ledger"
    print(f"H2  {len(heads)} @body heads lines over {n} actions, {sum(b['total'] for b in heads)} "
          f"heads; each total = unscoped + scopes; no ledger row")


def main() -> int:
    h1()
    h2()
    print("heads: 2 of 2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
