"""C4 RECALL-FIRST GOAL PROPOSER (the reviewer 2026-11-10 r1638, r1640), arm TETHER_PROPOSE_RECALL.

  R1  the stages: a shelf template with a won record is RECALL, one without is COMPOSE, the
      library's grammar is ENUMERATE, in that order; the row names the stage it ended in, the
      stages it reached and what it checked of what
  R2  MF: a pass that picks in recall never reaches enumerate (stages_left keeps it)
  R3  a spent purse stops the pass before enumeration: "unreached at this budget", never
      System 0's "nothing open"
  R4  OFF: no stage on the row
  R5  G4 (r1640, r1647): MF every staged row records what was compared (checked N of M), the
      readings it ranked by, shelf_n, and why the winner won (None only when nothing was picked)

    python tests/test_propose_recall.py
"""
from __future__ import annotations

import os
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def _agent(shelf: dict | None = None) -> tether.Agent:
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="recall"), tether.Config(),
                      ledger.Ledger())
    for k, v in (shelf or {}).items():
        ag._goal_shelf[k] = v
    return ag


def _hyp_rows(ag: tether.Agent) -> list:
    return [r["detail"] for r in ag.led.rows() if r["event"] == "goal_hypotheses"]


SHELF = {"won_col": {"template": "{o}.col > 0", "record": {"won": 1, "lost": 0, "progress": 0}},
         "new_row": {"template": "{o}.row > 0", "record": {"won": 0, "lost": 0, "progress": 0}}}


def check_r1_r2() -> None:
    ag = _agent(SHELF)
    for _ in range(3):
        ag.step()
    rows = [d for d in _hyp_rows(ag) if "stage" in d]
    assert rows, "occasion: no proposal pass"
    for d in rows:
        order = d["stages"] + d["stages_left"]
        assert order == [s for s in ("recall", "compose", "enumerate") if s in order], order
        assert order[0] == "recall", order
        assert d["checked_of"][0] <= d["checked_of"][1], d
        assert "ranked" in d and d["shelf_n"] == len(SHELF), "MF: a row without its readings"
        assert (d["why_won"] is None) == (d.get("pick") is None), "MF: a pick without its why"
        if d.get("pick") is not None and d["stage"] == "recall":
            assert "enumerate" in d["stages_left"], "MF: a recall pick reached enumeration"
    print(f"  R1-R2: {len(rows)} passes, each recall -> compose -> enumerate; "
          f"ended in {sorted({d['stage'] for d in rows})}; checked_of e.g. {rows[0]['checked_of']}")


def check_r3() -> None:
    keep = tether.STEP_BUDGET
    tether.STEP_BUDGET = 1
    try:
        ag = _agent(SHELF)
        ag.step()
    finally:
        tether.STEP_BUDGET = keep
    rows = _hyp_rows(ag)
    cut = [d for d in rows if d.get("purse_cut")]
    assert cut, ("occasion: no proposal was cut at a purse of 1", rows[:1])
    assert all(d["why"] == "unreached at this budget: the purse" for d in cut
               if d.get("pick") is None), cut
    assert all("System 0" not in (d.get("why") or "") for d in cut)
    print(f"  R3: purse 1: {len(cut)} passes cut, stages_left {cut[0].get('stages_left')}, "
          f"'unreached at this budget'")


def check_r4() -> None:
    keep, tether._PROPOSE_RECALL = tether._PROPOSE_RECALL, False
    try:
        ag = _agent(SHELF)
        ag.step()
    finally:
        tether._PROPOSE_RECALL = keep
    assert all("stage" not in d for d in _hyp_rows(ag)), "OFF: a stage on the row"
    print("  R4: OFF, no stage on the row")


if __name__ == "__main__":
    for c in (check_r1_r2, check_r3, check_r4):
        c()
    print("propose_recall: OK")
