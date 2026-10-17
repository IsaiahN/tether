"""C1, THE PER-STEP BUDGET, TETHER_STEP_BUDGET (the reviewer 2026-10-17 15:36). The fake ARC game,
12 actions, C-seed-X.

  E     a budget above any step's work: the ledger is the arm-OFF ledger row for row, the "@budget"
        rows aside (the budget never fires, so nothing changes)
  C     a budget of 1 evaluation (one lookup per step, checked between lookups): a question cut
        partway -- one of its lookups run, another not asked -- carries its unasked member under
        the question's id ("budget_owed"), and the next step's first lookup is an owed one
  Q     every step with a lookup writes its "@budget" row (spent, asked, not asked, the owed
        queue in questions and lookups); under a budget of 1 no step asks more than one lookup
  D     a budget of 1 and a death at step 5: the boundary closes every owed question with one
        "owed_closed" row (its id and unasked members), and the first step after it carries none
  MF-D  the close removed: an owed question from before the death crosses the boundary
  MF    arm OFF: no budget row, no owed row

    python test_step_budget.py
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
from arcengine import GameState
from test_entry import FakeWrapper
tether._AGENT_SEED = False
if sys.argv[1] != "-":
    tether.STEP_BUDGET = int(sys.argv[1])
mode = sys.argv[2] if len(sys.argv) > 2 else ""
if mode == "noclose":
    tether.Agent._close_owed = lambda self, how: None
script = {5: GameState.GAME_OVER} if mode in ("death", "noclose") else {}
led = os.path.join(tempfile.mkdtemp(), "b.jsonl")
tether_agent.run(FakeWrapper(script=script), "fake", max_actions=12, led_path=led)
print(led)
'''


def child(budget: str, extra: dict | None = None, mode: str = "") -> list:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", **(extra or {})})
    p = subprocess.run([sys.executable, "-B", "-c", CHILD, budget, mode], capture_output=True,
                       text=True, env=env, cwd=os.path.dirname(os.path.abspath(__file__)),
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-2000:]
    led = p.stdout.strip().splitlines()[-1]
    return [json.loads(x) for x in open(led, encoding="utf-8") if x.strip()]


def strip(rows: list) -> list:
    # seq and the detail's seq pointers (signal_seq) shift by the inserted "@budget" rows
    keep = ("header", "arms")
    return [{**{k: v for k, v in r.items() if k != "seq"},
             "detail": {k: v for k, v in (r.get("detail") or {}).items()
                        if not k.endswith("seq")}}
            for r in rows if r.get("slot") != "@budget" and r.get("event") not in keep
            and r.get("slot") != "@run"]


def main() -> int:
    off = child("-", {"TETHER_STEP_BUDGET": "0"})
    assert not [r for r in off if r.get("event") in ("budget", "budget_owed")]           # MF
    big = child(str(10 ** 12))
    a, b = strip(big), strip(off)
    diff = [(i, x, y) for i, (x, y) in enumerate(zip(a, b, strict=False)) if x != y]
    assert len(a) == len(b) and not diff, (len(a), len(b), diff[:2])                       # E
    assert not [r for r in big if r.get("event") == "budget_owed"]
    print("E", len(a), "rows identical to OFF with the budget above any step's work; MF OFF: no "
          "budget rows")
    one = child("1")
    owed = [r for r in one if r.get("event") == "budget_owed"]
    libs = [r for r in one if r.get("event") == "library"]
    assert owed, "precondition: the budget of 1 left nothing unasked"
    # C: a question cut partway -- its object had a lookup run AND one not asked in one step
    cut = [r for r in owed if any(x["cycle"] == r["cycle"] and x["slot"] != r["slot"]
                                  and x["slot"].rsplit(".", 1)[0] == r["detail"]["question"][1]
                                  for x in libs)]
    assert cut, ("no question cut partway", [(r["cycle"], r["slot"]) for r in owed][:6])
    firsts = {}
    for r in libs:
        firsts.setdefault(r["cycle"], r["slot"])
    owed_by = {}
    for r in owed:
        owed_by.setdefault(r["cycle"], []).append(r["slot"])
    carried = [(c, firsts[c + 1]) for c in owed_by if c + 1 in firsts]
    assert carried and all(s in {x for c2, ss in owed_by.items() if c2 <= c for x in ss}
                           for c, s in carried), carried                                     # C
    print("C cut partway:", [(r["cycle"], r["slot"], r["detail"]["question"]) for r in cut[:2]],
          "; next step's first lookup is owed:", carried[:3])
    bud = [r for r in one if r.get("event") == "budget"]
    cycles = sorted({r["cycle"] for r in libs} | {r["cycle"] for r in owed})
    assert {r["cycle"] for r in bud} >= set(cycles), (cycles, [r["cycle"] for r in bud])
    q = [(r["cycle"], r["detail"]["asked"], r["detail"]["not_asked"],
          r["detail"]["owed_questions"], r["detail"]["owed_lookups"]) for r in bud]
    assert all(n == 1 for _c, n, *_ in q if n), q                                       # Q
    print("Q @budget rows (cycle, asked, not asked, owed questions, owed lookups):", q[:6])
    d = child("1", mode="death")
    closed = [r for r in d if r.get("event") == "owed_closed"]
    assert closed, "precondition: the death closed no owed question"
    bc = closed[0]["cycle"]
    after = sorted({r["cycle"] for r in d if r.get("event") == "budget" and r["cycle"] > bc})
    assert after, "precondition: no step after the death"
    first = [r for r in d if r.get("event") == "budget_owed" and r["cycle"] == after[0]]
    assert all(r["detail"]["question"][0] == after[0] for r in first), first[:3]          # D
    qs = {tuple(r["detail"]["question"]) for r in closed}
    assert len(qs) == len(closed), "one row per question"
    print("D death at cycle", bc, ": closed", len(closed), "questions, e.g.",
          [(r["detail"]["question"], r["detail"]["unasked"]) for r in closed[:2]],
          "; the first step after carries none:", [r["slot"] for r in first][:3])
    n = child("1", mode="noclose")
    nb = max(r["cycle"] for r in n if r.get("event") == "budget" and r["cycle"] <= bc)
    crossed = [r for r in n if r.get("event") == "budget_owed" and r["cycle"] > bc
               and r["detail"]["question"][0] <= nb]
    assert crossed, "MF-D: no owed question crossed the boundary with the close removed"   # MF-D
    print("MF-D close removed:", len(crossed), "owed rows after the death carry a question from "
          "before it, e.g.", [(r["cycle"], r["detail"]["question"]) for r in crossed[:2]])
    print("step_budget: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
