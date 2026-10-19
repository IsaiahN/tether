"""DEADLINE AFTER LOAD (the reviewer 2026-10-18 20:24): game_one's cap counts PLAY, from the
agent's first step, so wiring the agent and loading the lineage fall outside it. Offline ARC
game ar25 (environment_files).

  DL   a planted 40 s load (arc_holdout.wire delayed) and a 30 s cap: play (wall less
       play_start_s) >= 29 s, at least one step, and play_start_s >= 40
  MF   the same plant on 4268b04's game_one (the deadline from module start): 0 steps,
       censored at once

Scaled from the reviewer's 90 s load / 590 s play to keep the test under 5 minutes.

    python test_game_one_deadline.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
LOAD_S, CAP_S = 40.0, 30.0

WRAP = r'''
import runpy, sys, time
repo, script, load_s = sys.argv[1], sys.argv[2], float(sys.argv[3])
sys.argv = [script] + sys.argv[4:]
sys.path.insert(0, repo)
import arc_holdout
_wire = arc_holdout.wire
def slow(*a, **k):
    time.sleep(load_s)          # the planted load, inside play(), as the lineage load is
    return _wire(*a, **k)
arc_holdout.wire = slow
runpy.run_path(script, run_name="__main__")
'''


def run(script: str) -> dict:
    out = tempfile.mkdtemp(prefix="dl_")
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    # the real interpreter path: a worktree's .venv junction would put "scratchpad" in its
    # site-packages path, which game_one strips from sys.path
    py = os.path.realpath(sys.executable)
    p = subprocess.run([py, "-B", "-c", WRAP, HERE, script, str(LOAD_S), "--repo", HERE,
                        "--game", "ar25", "--cap-s", str(CAP_S), "--out", out],
                       capture_output=True, text=True, env=env, cwd=HERE,
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-2000:]
    with open(os.path.join(out, "ar25.result.json"), encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    new = run(os.path.join(HERE, "harness", "game_one.py"))
    ps = new.get("play_start_s")
    assert new.get("deadline_after_load") is True and ps is not None, new
    play = new["wall_s"] - ps
    assert ps >= LOAD_S, ("the planted load did not run before the first step", ps)
    assert new["agent_steps"] >= 1 and play >= CAP_S - 1, (new["agent_steps"], play)
    print(f"  DL: planted load {LOAD_S:.0f} s, cap {CAP_S:.0f} s: play_start_s {ps}, "
          f"play {play:.1f} s, {new['agent_steps']} steps")
    old_src = subprocess.run(["git", "-C", HERE, "show", "4268b04:harness/game_one.py"],
                             capture_output=True, text=True, check=True).stdout
    old = os.path.join(tempfile.mkdtemp(prefix="dl_old_"), "game_one_4268b04.py")
    with open(old, "w", encoding="utf-8") as fh:
        fh.write(old_src)
    o = run(old)
    assert o["agent_steps"] == 0 and o["censored"], ("MF did not fail", o["agent_steps"],
                                                    o["censored"])
    print(f"  MF: 4268b04's game_one under the same plant: {o['agent_steps']} steps, "
          f"censored {o['censored']}")
    print("game_one_deadline: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
