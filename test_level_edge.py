"""C-level-1, F1: THE AGENT PERCEIVES A LEVEL CLEAR (the reviewer 2026-10-15 07:32, 07:42, 07:55).
WRITTEN, NOT RUN: it runs in the end-of-step-7 checklist. Each case is its own process, its arms set
in the environment at start. The world is test_entry's FakeWrapper with levels_completed raised
from 0 to 1 at step CLEAR and no WIN: a level clear the terminal edge never reports.

  E1   tether_agent.run, TETHER_LEVEL_EDGE ON: exactly one "ending" row with
       how="level_advance" at the clear; Agent.level 0 -> 1; one @credit row; every @signal
       resolution at the clear has kind "level".
  E2   arc_holdout.play on the same wrapper (handed in through arc.make): the same ending row
       and Agent.level 1.
  E3   with TETHER_LINEAGE_HOLD also ON: the dormant carry fires at the clear (ag._dormant grows).
  E4   with TETHER_LINEAGE_BOUNDARY and TETHER_LINEAGE_CARRY also ON, a lineage folder: exactly one
       generation for the clear, how "level", agent_level 1 (written AFTER the retarget).
  MF-E MUST-FAIL: TETHER_LEVEL_EDGE OFF on the same wrapper: no ending row, Agent.level stays 0,
       so E1's check goes red.

    python test_level_edge.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

import arc_holdout  # noqa: E402
import tether  # noqa: E402
import tether_agent  # noqa: E402
from test_entry import FakeWrapper  # noqa: E402

CLEAR, STEPS = 6, 14


class LevelWrapper(FakeWrapper):
    """levels_completed 1 from step CLEAR on, never a WIN: one level clear mid-game."""

    def _frame(self, state):
        f = super()._frame(state)
        f.levels_completed = 1 if self.n >= CLEAR else 0
        return f


def _endings(ag):
    return [e for e in ag.led.entries if e.event == "ending"]


def role(case, d):
    w = LevelWrapper()
    seen = {}
    real = tether.Agent.retarget

    def spy(self, env, level, how=tether.ADVANCE):
        seen.setdefault("dormant_before", len(getattr(self, "_dormant", [])))
        real(self, env, level, how)
        seen["dormant_after"] = len(getattr(self, "_dormant", []))
        seen["ag"] = self
    tether.Agent.retarget = spy
    try:
        if case == "play":
            class _Arc:     # play builds its wrapper through arc.make (arc_holdout 287)
                def make(self, _game):
                    return w
            rep = arc_holdout.play("fake", STEPS, arc=_Arc(), lineage_dir=d or None)
            rep = {**rep, "lineage_bounds": rep["persistence"]["lineage_bounds"]}
        else:
            rep = tether_agent.run(w, "fake", STEPS, lineage_dir=d or None)
    finally:
        tether.Agent.retarget = real
    ag = seen.get("ag")
    out = {"level_edge": tether._LEVEL_EDGE, "retargets": 0 if ag is None else 1}
    if ag is not None:
        ends = _endings(ag)
        out.update(endings=[e.detail.get("how") for e in ends], level=ag.level,
                   credit=sum(1 for e in ag.led.entries if e.slot == "@credit"),
                   kinds=sorted({e.detail.get("kind") for e in ag.led.entries
                                 if e.slot == "@signal" and e.event == "resolution"}),
                   dormant=[seen["dormant_before"], seen["dormant_after"]])
    out["bounds"] = [{k: b.get(k) for k in ("how", "agent_level")} for b in
                     rep.get("lineage_bounds") or [] if b]
    print("CASE " + json.dumps(out), flush=True)


def _child(case, arms, d=""):
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(arms)
    r = subprocess.run([sys.executable, "-B", __file__, "--role", case, d], env=env,
                       stdin=subprocess.DEVNULL, capture_output=True, text=True, check=False)
    assert r.returncode == 0, (case, arms, r.stderr[-3000:])
    return json.loads(next(ln for ln in r.stdout.splitlines() if ln.startswith("CASE "))[5:])


def main():
    e1 = _child("run", {"TETHER_LEVEL_EDGE": "1"})
    assert e1["endings"] == ["level_advance"] and e1["level"] == 1 and e1["credit"] == 1, ("E1", e1)
    assert e1["kinds"] in ([], ["level"]), ("E1 kinds", e1)
    print(f"  E1 one advance ending at the clear, Agent.level 1, one @credit; kinds {e1['kinds']}")
    e2 = _child("play", {"TETHER_LEVEL_EDGE": "1"})
    assert e2["endings"] == e1["endings"] and e2["level"] == 1, ("E2 differs from E1", e1, e2)
    print("  E2 arc_holdout.play: the same advance ending and Agent.level 1")
    e3 = _child("run", {"TETHER_LEVEL_EDGE": "1", "TETHER_LINEAGE_HOLD": "1"})
    assert e3["dormant"][1] > e3["dormant"][0], ("E3: no dormant carry at the clear", e3)
    print(f"  E3 the dormant carry fired at the clear: {e3['dormant']}")
    d = tempfile.mkdtemp(prefix="edge_")
    e4 = _child("run", {"TETHER_LEVEL_EDGE": "1", "TETHER_LINEAGE_BOUNDARY": "1",
                        "TETHER_LINEAGE_CARRY": "1"}, d)
    assert e4["bounds"] == [{"how": "level", "agent_level": 1}], ("E4", e4)
    print("  E4 one generation for the clear, how level, written after the retarget")
    mf = _child("run", {"TETHER_LEVEL_EDGE": "0"})
    assert mf["retargets"] == 0, ("MF-E MUST-FAIL did not fail: a retarget with the arm OFF", mf)
    print("  MF-E must-fail fired: with the arm OFF the clear is not perceived (no retarget)")
    print("level edge: OK")


if __name__ == "__main__":
    if "--role" in sys.argv:
        a = sys.argv[sys.argv.index("--role") + 1:]
        role(a[0], a[1] if len(a) > 1 else "")
    else:
        main()
