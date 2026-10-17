"""E1 OWN CLOCK, TETHER_OWN_CLOCK (the reviewer 2026-10-17 10:05): the slots the agent's own
perception writes by its own rule (age, stability) are predicted by that rule when the frames
arrive. A scripted ARC world answers every action with a TWO-frame stack (an intermediate, then the
settled board) over three objects: S stays still, M moves (in both frames), R moves in the
intermediate frame and is back by the settled one.

  O1 F, the tracker advances one action took, is READ: 2 here
  O2 age on a continuing track: the expectation equals the reading (residual 0)
  O3 stability, M moved: expected 0 and read 0 (residual 0); the change sits on M's row
  O4 stability, R's mid-cascade change that reverted: expectation != reading, R's row unchanged
  O5 no expectation at birth (an object first seen this action)
  A1 agent ON: no age/stability bet on a still board carries mass, every such row says own_clock
  MF-A1 agent OFF: the same board refuses no_change on every object's age (today's refusals)

    python test_own_clock.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True

WORLD = r'''
import json, sys
sys.dont_write_bytecode = True
import numpy as np
from arcengine import FrameDataRaw, GameState
import arc_atoms, arc_percept, arc_predict
from arc_world import ArcWorld

def board(m_row, r_row, born=False):
    b = np.zeros((40, 40), dtype=int)
    b[2:6, 2:6] = 7                    # S
    b[m_row:m_row + 4, 15:19] = 3      # M
    b[r_row:r_row + 4, 30:34] = 4      # R
    if born:
        b[34:37, 2:5] = 5              # N, first seen on the settled frame
    return b

class W:
    def __init__(self, mode):
        self.mode, self.calls = mode, 0
    def _f(self, stack):
        f = FrameDataRaw(game_id="ownclock", state=GameState.NOT_FINISHED, levels_completed=0,
                         win_levels=3, available_actions=[1, 2])
        f.frame = stack
        return f
    def reset(self):
        return self._f([board(10, 10)])
    def step(self, *a, **k):
        self.calls += 1
        if self.mode == "still":
            return self._f([board(10, 10), board(10, 10)])
        return self._f([board(12, 12), board(14, 10, born=True)])

mode = sys.argv[1]
w = W(mode)
env = ArcWorld(w, arc_percept.Objects(), arc_atoms.three_spaces(arc_predict.predict()),
               palette=8, platform=())
env._frame = w.reset()
before = env.observe()
tr = env._decompose.tracked
at = {(o["row"], o["col"]): n for n, o in tr.items()}
S, M, R = at[(2, 2)], at[(10, 15)], at[(10, 30)]
env.step("ACTION1")
after = env.observe()
oe = env.own_expected()
born = [n for n in env._decompose.tracked if n not in tr]
print(json.dumps({"F": env._own[1], "S": S, "M": M, "R": R, "born": born,
                  "before": before, "after": after, "oe": oe}))
'''

AGENT = r'''
import json, sys
sys.dont_write_bytecode = True
import numpy as np
from arcengine import FrameDataRaw, FrameData, GameState, GameAction
import tether_agent

class Still:
    def __init__(self):
        self.calls, self._last = [], None
        self.reset()
    @property
    def observation_space(self):
        return self._last
    def _f(self, n):
        b = np.zeros((40, 40), dtype=int)
        b[2:6, 2:6] = 7
        b[20:24, 20:24] = 3
        f = FrameDataRaw(game_id="ownclock-agent", state=GameState.NOT_FINISHED,
                         levels_completed=0, win_levels=2, guid="g", available_actions=[1, 2])
        f.frame = [b] * n
        self._last = f
        return f
    def reset(self):
        self.calls.append("RESET")
        return self._f(1)
    def step(self, action, data=None, reasoning=None):
        self.calls.append(action.name)
        return self._f(2)

led = sys.argv[1]
tether_agent.run(Still(), "ownclock", max_actions=4, led_path=led)
rows = [json.loads(x) for x in open(led, encoding="utf-8")]
bets = [r for r in rows if r.get("event") == "bet"
        and r["slot"].rsplit(".", 1)[-1] in ("age", "stability")]
print(json.dumps({"n": len(bets),
                  "massive": sum(1 for r in bets if r["detail"].get("mass", 0) > 0),
                  "own_clock": sum(1 for r in bets if r["detail"].get("bound") == "own_clock"),
                  "age_refused": sum(1 for r in bets if r["slot"].endswith(".age")
                                     and r["detail"].get("mass", 0) > 0)}))
'''


def child(code: str, *argv: str, extra: dict | None = None) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", **(extra or {})})
    p = subprocess.run([sys.executable, "-B", "-c", code, *argv], capture_output=True, text=True,
                       env=env, cwd=os.path.dirname(os.path.abspath(__file__)),
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-2000:]
    return json.loads(p.stdout.strip().splitlines()[-1])


def main() -> int:
    still = child(WORLD, "still")
    assert still["F"] == 2, still["F"]                                          # O1
    S = still["S"]
    for s in (f"{S}.age", f"{S}.stability"):
        assert still["oe"][s] == still["after"][s], (s, still["oe"], still["after"])   # O2
    print("O1 F read:", still["F"], "; O2 still S age/stability expected == read:",
          still["after"][f"{S}.age"], still["after"][f"{S}.stability"])

    mv = child(WORLD, "move")
    M, R = mv["M"], mv["R"]
    assert mv["oe"][f"{M}.stability"] == 0 == mv["after"][f"{M}.stability"], mv["oe"]   # O3
    assert mv["after"][f"{M}.row"] != mv["before"][f"{M}.row"]
    assert mv["oe"][f"{M}.age"] == mv["after"][f"{M}.age"]
    assert mv["oe"][f"{R}.stability"] != mv["after"][f"{R}.stability"], (mv["oe"], mv["after"])
    assert mv["after"][f"{R}.row"] == mv["before"][f"{R}.row"]                  # O4
    assert mv["born"] and not any(k.startswith(mv["born"][0] + ".") for k in mv["oe"])  # O5
    print("O3 M moved: stability expected 0, read 0, row", mv["before"][f"{M}.row"], "->",
          mv["after"][f"{M}.row"], "; O4 R reverted mid-cascade: stability expected",
          mv["oe"][f"{R}.stability"], "read", mv["after"][f"{R}.stability"],
          "; O5 newborn", mv["born"], "has no expectation")

    led = os.path.join(os.environ.get("TEMP", "."), "own_clock_on.jsonl")
    on = child(AGENT, led, extra={"TETHER_OWN_CLOCK": "1"})
    assert on["n"] > 0 and on["massive"] == 0 and on["own_clock"] == on["n"], on     # A1
    off = child(AGENT, led.replace("_on", "_off"), extra={"TETHER_OWN_CLOCK": "0"})
    assert off["age_refused"] > 0 and off["own_clock"] == 0, off                    # MF-A1
    print("A1 ON:", on, "; MF-A1 OFF:", off)
    print("own_clock: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
