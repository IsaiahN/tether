"""C1b, THE STEP'S LOOKUPS IN RANK ORDER, TETHER_STEP_RANK (the reviewer 2026-10-17 17:07, 17:29,
17:30). The fake ARC game, 12 actions, C-seed-X.

  E   a budget above any step's work, rank ON vs OFF: per step the ROUTE rows are the same
      multiset, and every row outside ROUTE is the same in sequence (lookups reorder; no decision)
  C   a budget of 1 (one lookup per step), rank ON: in every step where a slot that CHANGED this
      step reaches a lookup point, the step's first lookup is a changed one; @budget per class
  MF  the same with the rank OFF: some step asks an unchanged slot first while a changed one waits

    python test_step_rank.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from collections import Counter

sys.dont_write_bytecode = True

CHILD = r'''
import json, os, sys, tempfile
sys.dont_write_bytecode = True
import tether, tether_agent
from test_entry import FakeWrapper
tether._AGENT_SEED = False
tether.STEP_BUDGET = int(sys.argv[1])
led = os.path.join(tempfile.mkdtemp(), "r.jsonl")
tether_agent.run(FakeWrapper(script={}), "fake", max_actions=12, led_path=led)
print(led)
'''


def child(budget: int, extra: dict | None = None) -> list:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", **(extra or {})})
    p = subprocess.run([sys.executable, "-B", "-c", CHILD, str(budget)], capture_output=True,
                       text=True, env=env, cwd=os.path.dirname(os.path.abspath(__file__)),
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-2000:]
    led = p.stdout.strip().splitlines()[-1]
    return [json.loads(x) for x in open(led, encoding="utf-8") if x.strip()]


def clean(r: dict) -> str:
    d = {k: v for k, v in (r.get("detail") or {}).items() if not k.endswith("seq")}
    return json.dumps({**{k: v for k, v in r.items() if k != "seq"}, "detail": d}, sort_keys=True)


def keep(rows: list) -> list:
    return [r for r in rows if r.get("slot") not in ("@budget", "@run")
            and r.get("event") not in ("header", "arms")]


def firsts(rows: list) -> list:
    """(cycle, first lookup's slot, changed slots at a lookup point) per step."""
    moved = {(r["cycle"], r["slot"]) for r in rows if r.get("event") == "bet"
             and r["detail"].get("actual") != r["detail"].get("from_value")}
    by: dict = {}
    for r in rows:
        if r.get("event") in ("reach", "budget_owed"):
            by.setdefault(r["cycle"], []).append(r["slot"])
    out = []
    for c, ss in sorted(by.items()):
        first = next((r["slot"] for r in rows if r.get("event") == "reach" and r["cycle"] == c),
                     None)
        out.append((c, first, sorted({s for s in ss if (c, s) in moved})))
    return out


def main() -> int:
    on = keep(child(10 ** 12))
    off = keep(child(10 ** 12, {"TETHER_STEP_RANK": "0"}))
    seq_on = [clean(r) for r in on if r.get("step") != "ROUTE"]
    seq_off = [clean(r) for r in off if r.get("step") != "ROUTE"]
    assert seq_on == seq_off, (len(seq_on), len(seq_off), next(
        ((i, a, b) for i, (a, b) in enumerate(zip(seq_on, seq_off, strict=False)) if a != b), None))
    cyc = {r["cycle"] for r in on} | {r["cycle"] for r in off}
    for c in sorted(cyc):
        a = Counter(clean(r) for r in on if r.get("step") == "ROUTE" and r["cycle"] == c)
        b = Counter(clean(r) for r in off if r.get("step") == "ROUTE" and r["cycle"] == c)
        assert a == b, (c, (a - b).most_common(2), (b - a).most_common(2))              # E
    print("E", len(seq_on), "non-ROUTE rows identical in sequence;", len(cyc),
          "steps' ROUTE rows identical as multisets")
    r1 = child(1)
    f1 = firsts(r1)
    bad = [(c, s, ch) for c, s, ch in f1 if ch and s not in ch]
    assert any(ch for _c, _s, ch in f1), "precondition: no changed slot reached a lookup point"
    assert not bad, bad                                                                  # C
    cls = [r["detail"].get("classes") for r in r1 if r.get("event") == "budget"
           and r["detail"].get("classes")]
    assert cls, "no per-class counts in @budget"
    print("C rank ON, budget 1: first lookup is a changed slot in every step that has one,",
          sum(1 for _c, _s, ch in f1 if ch), "steps; @budget classes e.g.", cls[1:3])
    r0 = child(1, {"TETHER_STEP_RANK": "0"})
    f0 = firsts(r0)
    worse = [(c, s, ch) for c, s, ch in f0 if ch and s not in ch]
    assert worse, "MF: with the rank off no step asked an unchanged slot first"          # MF
    print("MF rank OFF: an unchanged slot asked first while a changed one waited, e.g.", worse[:2])
    print("step_rank: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
