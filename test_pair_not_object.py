"""C1a, A PAIR OWNER IS NOT AN OBJECT NAME, TETHER_PAIR_NOT_OBJECT (the reviewer 2026-10-17 14:24).
The fake ARC game, 12 actions, C-seed-X, the arm ON and OFF.

  P1    the two ledgers are the same row for row, the refusal counts (library, abduce) aside: every
        offer, landing, bet and mint is unchanged (exact)
  P2    ON refuses pairings under "a pair owner is not an object name", and no parse refusal
        names a pair owner
  MF-P  OFF: the same pairings refuse per candidate at parse ("cannot tokenize at '~...")

    python test_pair_not_object.py
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
import tether, tether_agent
from test_entry import FakeWrapper
tether._AGENT_SEED = False
led = os.path.join(tempfile.mkdtemp(), "p.jsonl")
tether_agent.run(FakeWrapper(script={}), "fake", max_actions=12, led_path=led)
print(led)
'''
NOT_OBJECT = "a pair owner is not an object name"


def child(extra: dict) -> list:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", **extra})
    p = subprocess.run([sys.executable, "-B", "-c", CHILD], capture_output=True, text=True,
                       env=env, cwd=os.path.dirname(os.path.abspath(__file__)),
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-2000:]
    led = p.stdout.strip().splitlines()[-1]
    return [json.loads(x) for x in open(led, encoding="utf-8") if x.strip()]


def strip(rows: list) -> list:
    out = []
    for r in rows:
        r = {k: v for k, v in r.items() if k not in ("seq", "t", "wall")}
        if r.get("event") in ("library", "abduce"):    # abduce carries the refusal total
            r = {**r, "detail": {k: v for k, v in r["detail"].items() if k != "refused"}}
        if r.get("event") in ("header", "arms") or r.get("slot") == "@run":
            continue
        out.append(r)
    return out


def refused(rows: list) -> dict:
    tot: dict = {}
    for r in rows:
        if r.get("event") == "library":
            for k, v in (r["detail"].get("refused") or {}).items():
                tot[k] = tot.get(k, 0) + v
    return tot


def main() -> int:
    on, off = child({}), child({"TETHER_PAIR_NOT_OBJECT": "0"})
    a, b = strip(on), strip(off)
    diff = [(i, x, y) for i, (x, y) in enumerate(zip(a, b, strict=False)) if x != y]
    assert len(a) == len(b) and not diff, (len(a), len(b), diff[:2])                     # P1
    print("P1", len(a), "rows identical ON vs OFF (library refusal counts aside)")
    r_on, r_off = refused(on), refused(off)
    tilde = lambda r: sum(v for k, v in r.items() if "does not parse" in k and "~" in k)  # noqa: E731
    assert r_on.get(NOT_OBJECT, 0) > 0 and tilde(r_on) == 0, (r_on.get(NOT_OBJECT), tilde(r_on))
    print("P2 ON: pairings refused as not an object name", r_on[NOT_OBJECT],
          "; parse refusals naming a pair owner", tilde(r_on))                            # P2
    assert tilde(r_off) > 0 and NOT_OBJECT not in r_off, (tilde(r_off), r_off.get(NOT_OBJECT))
    print("MF-P OFF: parse refusals naming a pair owner", tilde(r_off),
          "; evaluations ON", sum(r_on.values()), "OFF", sum(r_off.values()))           # MF-P
    print("pair_not_object: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
