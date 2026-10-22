"""C1, THE PER-STEP BUDGET, TETHER_STEP_BUDGET (the reviewer 2026-10-17 15:36). The fake ARC game,
12 actions, C-seed-X.

  E     a budget above any step's work, TETHER_STEP_RANK=0: the ledger is the arm-OFF ledger row
        for row, the "@budget" rows aside (the budget never fires, so nothing changes; C1b's rank
        order, ffbdf14, reorders the step's lookups by design and is test_step_rank's)
  C     a budget of 1 evaluation (one lookup per step, checked between lookups), TETHER_STEP_RANK=0:
        a question cut partway -- one of its lookups run, another not asked -- carries its unasked
        member under the question's id ("budget_owed"), and the next step's first lookup is an
        owed one (the unranked path; C1b's ranked ORDER is test_step_rank's -- the reviewer
        2026-10-18 01:28 (i))
  C-RANK the same budget on the DEFAULT (ranked) path: no owed question vanishes -- each owed
        (step k, slot) is asked at a later step, closed by an owed_closed row, or still in the
        queue at the run's end: the slots left number at most the last @budget row's
        owed_lookups (the reviewer 01:28)
  Q     every step with a lookup writes its "@budget" row (spent, asked, not asked, the owed
        queue in questions and lookups); under a budget of 1 no step asks more than one lookup
  D     a budget of 1 and a death at step 5: the boundary closes every owed question with one
        "owed_closed" row (its id and unasked members), and the first step after it carries none
  MF-D  the close removed: an owed question from before the death crosses the boundary
  D2    a budget of 1 and a level ADVANCE at step 5 (levels_completed 0 -> 1, no terminal state):
        retarget(advance) closes every owed question with one row, and the next level's first step
        carries none (the reviewer 16:06); the edge reaches retarget under TETHER_LEVEL_EDGE (F1,
        default ON since 2026-10-15), and the boundary's ending row precedes the owed_closed rows
  MF-D2 TETHER_LEVEL_EDGE=0: no retarget at the advance, so the owed questions cross the level
  MF    arm OFF: no budget row, no owed row

    python tests/test_step_budget.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

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


class Advance(FakeWrapper):
    def _frame(self, state):
        f = super()._frame(state)
        if self.n >= 5:
            f.levels_completed = 1
        return f


d = tempfile.mkdtemp()
led = os.path.join(d, "b.jsonl")
w = Advance() if mode == "level_advance" else FakeWrapper(script=script)
tether_agent.run(w, "fake", max_actions=12, led_path=led, lineage_dir=d)
print(led)
'''


def child(budget: str, extra: dict | None = None, mode: str = "") -> list:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", **(extra or {})})
    p = subprocess.run([sys.executable, "-B", "-c", CHILD, budget, mode], capture_output=True,
                       text=True, env=env, cwd=_repo.ROOT,
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
    big = child(str(10 ** 12), {"TETHER_STEP_RANK": "0"})
    a, b = strip(big), strip(off)
    diff = [(i, x, y) for i, (x, y) in enumerate(zip(a, b, strict=False)) if x != y]
    assert len(a) == len(b) and not diff, (len(a), len(b), diff[:2])                       # E
    assert not [r for r in big if r.get("event") == "budget_owed"]
    print("E", len(a), "rows identical to OFF with the budget above any step's work; MF OFF: no "
          "budget rows")
    one = child("1", {"TETHER_STEP_RANK": "0"})
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
    rk = child("1")
    ro = [r for r in rk if r.get("event") == "budget_owed"]
    q_end = [r for r in rk if r.get("event") == "budget"][-1]["detail"]["owed_lookups"]
    asked = {(r["cycle"], r["slot"]) for r in rk if r.get("event") == "library"}
    shut = {tuple(r["detail"]["question"]) for r in rk if r.get("event") == "owed_closed"}
    held = {r["slot"] for r in ro if not any(c > r["cycle"] and s_ == r["slot"] for c, s_ in asked)
            and tuple(r["detail"]["question"]) not in shut}
    # an owed slot leaves the queue only when asked or closed, and one no longer routed writes no
    # row: the rest must all still be IN the queue at the end (its count, the last @budget row)
    assert ro and len(held) <= q_end, ("C-RANK: an owed question vanished", len(held), q_end)
    print("C-RANK default path:", len(ro), "owed rows; the", len(held), "slots never asked later "
          "nor closed are all still queued at the end (owed_lookups", q_end, ")")       # C-RANK
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
    print("D death at cycle", bc, ": closed", len(closed), "questions (how:",
          sorted({r["detail"]["how"] for r in closed}), "), e.g.",
          [(r["detail"]["question"], r["detail"]["unasked"]) for r in closed[:2]],
          "; the first step after carries none:", [r["slot"] for r in first][:3])
    n = child("1", mode="noclose")
    nb = max(r["cycle"] for r in n if r.get("event") == "budget" and r["cycle"] <= bc)
    crossed = [r for r in n if r.get("event") == "budget_owed" and r["cycle"] > bc
               and r["detail"]["question"][0] <= nb]
    assert crossed, "MF-D: no owed question crossed the boundary with the close removed"   # MF-D
    print("MF-D close removed:", len(crossed), "owed rows after the death carry a question from "
          "before it, e.g.", [(r["cycle"], r["detail"]["question"]) for r in crossed[:2]])
    v = child("1", mode="level_advance")
    vc = [r for r in v if r.get("event") == "owed_closed"]
    hows = {r["detail"]["how"] for r in vc}
    assert vc and hows == {"level_advance"}, [r["detail"] for r in vc][:2]
    vb = vc[0]["cycle"]
    nxt = sorted({r["cycle"] for r in v if r.get("event") == "budget" and r["cycle"] > vb})
    assert nxt, "precondition: no step after the advance"
    vf = [r for r in v if r.get("event") == "budget_owed" and r["cycle"] == nxt[0]]
    assert all(r["detail"]["question"][0] == nxt[0] for r in vf), vf[:3]                  # D2
    assert len({tuple(r["detail"]["question"]) for r in vc}) == len(vc), "one row per question"
    end_seq = [r["seq"] for r in v if r.get("event") == "ending"
               and r["detail"].get("how") == "level_advance"]
    assert end_seq and end_seq[0] < min(r["seq"] for r in vc), (end_seq, vc[0]["seq"])
    vo = child("1", {"TETHER_LEVEL_EDGE": "0"}, mode="level_advance")
    assert not [r for r in vo if r.get("event") == "owed_closed"]
    vx = [r for r in vo if r.get("event") == "budget_owed" and r["cycle"] > vb
          and r["detail"]["question"][0] <= vb]
    assert vx, "MF-D2: with the edge off, no owed question crossed the level"            # MF-D2
    print("MF-D2 TETHER_LEVEL_EDGE=0: no owed_closed row;", len(vx), "owed rows after the advance "
          "carry a question from before it, e.g.", [(r["cycle"], r["detail"]["question"])
                                                     for r in vx[:2]])
    print("D2 advance at cycle", vb, ": closed", len(vc), "questions (how level_advance); the next "
          "level's first step carries none:", [r["slot"] for r in vf][:3])
    print("step_budget: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
