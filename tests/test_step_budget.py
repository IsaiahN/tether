"""C1, THE PER-STEP BUDGET, TETHER_STEP_BUDGET (the reviewer 2026-10-17 15:36). The fake ARC game,
12 actions, C-seed-X.

  E     a budget above any step's work, TETHER_STEP_RANK=0: the ledger is the arm-OFF ledger row
        for row, the "@budget" rows aside (the budget never fires, so nothing changes; C1b's rank
        order, ffbdf14, reorders the step's lookups by design and is test_step_rank's). Both
        children pin item 25's chooser (TETHER_THINK_CHOOSER=0): it reads the purse by design
        (evals = budget - spent prices a think), so with it on a 10^12 budget is a different
        agent from OFF; E's subject is the budget alone, and the chooser's dependence on the purse
        is test_think_chooser's (the reviewer 2026-11-06 r1312). Both also pin A1's gate
        (TETHER_STEP_ACT=0): its deferrals write the owed queue in either arm, but route asks owed
        slots first only under the budget, so the budget-OFF arm reorders them (r1317; the
        ordering's move out of the budget branch is a fidelity item of its own)
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
from conform.identity_mod_rows import compare

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


def body(rows: list) -> list:
    # the header and the @run arms row are set by the children's arms (the budget, the pins), so
    # they are named out; every other row goes to identity_mod_rows.compare, which drops the
    # budget's own rows and maps every position field through the shift (r1318)
    return [r for r in rows if r.get("event") not in ("header", "arms")]


OWERS = ("budget_owed", "walk_cut", "lookup_deferred", "route_named")   # every _owed_q writer


def live_owed(rows: list, c: int) -> set:
    """The slots _owed_q holds at c+1's entry: written by a named writer (OWERS, the reviewer
    2026-11-06 r1323) at a cycle <= c, and not asked (route's lookup row) nor closed (owed_closed
    naming it) after that write and before c+1 (r1324: the LIVE set, so the check cannot go
    vacuous). Measured equal to the agent's own _owed_q at route's entry on this fixture."""
    live: dict = {}
    for r in rows:
        if r["cycle"] > c:
            continue
        ev, s = r.get("event"), r.get("slot")
        if ev in OWERS:
            live[s] = r["seq"]
        elif ev == "lookup":           # route's own ask (_lookup), which pops _owed_q
            live.pop(s, None)
        elif ev == "owed_closed":
            for m in r["detail"].get("unasked", ()):
                live.pop(m, None)
    return set(live)


def check_c(rows: list) -> list:
    """C: the owed slots are ASKED FIRST at c+1 -- route's rows at c+1 (written in its order; the
    "@" rows aside) open with every live owed slot route reaches, before any slot not owed. The
    owed slots' own fate there (looked up, held, deferred again) is not C's: an owed slot the
    gate defers again leaves no lookup, so "the first LOOKUP is owed" read the wrong row (r1324;
    the per-slot promise is A7's). Returns the (c, first routed slot at c+1) pairs; raises with the
    whole list otherwise."""
    routed: dict = {}
    for r in rows:
        if r.get("event") == "route" and not r["slot"].startswith("@"):
            routed.setdefault(r["cycle"], []).append(r["slot"])
    carried, bad = [], []
    for c in sorted({r["cycle"] for r in rows}):
        live = live_owed(rows, c)
        order = routed.get(c + 1, [])
        reached = [s for s in order if s in live]
        if not reached:
            continue
        carried.append((c, order[0]))
        if order[:len(reached)] != reached:
            bad.append((c, order[:len(reached) + 2], sorted(reached)[:6]))
    assert carried and not bad, ("C", carried, bad[:3])                                     # C
    return carried


def main() -> int:
    pin = {"TETHER_THINK_CHOOSER": "0",      # E's subject is the budget alone (docstring, r1312,
           "TETHER_STEP_ACT": "0",           # r1317)
           "TETHER_STEP_RANK": "0"}          # both arms: route's mint order reads it (r1556)
    off = child("-", {"TETHER_STEP_BUDGET": "0", **pin})
    assert not [r for r in off if r.get("event") in ("budget", "budget_owed")]           # MF
    big = child(str(10 ** 12), {"TETHER_STEP_RANK": "0", **pin})
    a = body(off)
    diff = compare(a, body(big), {"budget", "budget_owed"})
    assert not diff, diff[:3]                                                               # E
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
    carried = check_c(one)
    print("C cut partway:", [(r["cycle"], r["slot"], r["detail"]["question"]) for r in cut[:2]],
          "; owed slots routed first at the next step:", carried[:3])
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
    # every owed writer, as live_owed reads them: since c450e8d the question crosses on
    # lookup_deferred, not budget_owed (r1560)
    crossed = [r for r in n if r.get("event") in OWERS and r["cycle"] > bc
               and (r["detail"].get("question") or [nb + 1])[0] <= nb]
    assert crossed, "MF-D: no owed question crossed the boundary with the close removed"   # MF-D
    print("MF-D close removed:", len(crossed), "owed rows after the death carry a question from "
          "before it, e.g.", [(r["cycle"], r["event"], r["detail"]["question"])
                              for r in crossed[:2]])
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
