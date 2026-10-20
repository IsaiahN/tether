"""E0, THE PERCEPT DECLARES WHAT IT DERIVES, TETHER_DERIVED_PERCEPT (the reviewer 2026-10-17 12:53,
12:59). Scripted ARC worlds, the agent playing a few actions in each.

  M     constant velocity (+3 cols per action, no own act): col's own term (an operand term reading
        the derived dcol) binds by the 5th step and predicts with residual 0 after; dcol and speed
        are not bet on (derived); no relational surprise (the derivation is exact on a one-frame
        response) -- momentum survives E0
  MF-M  the mover stops: a residual on col at the step it stops
  R     a resize in place (the object widens each action): residual on shape, none bet on w / h /
        dw / dcells, no relational surprise
  T     a mid-cascade change that reverts (two-frame responses, the object widens in the
        intermediate frame only): a relational_surprise row on a frame delta with its source
        (shape) held (derived_new under TETHER_DERIVED_SUBJECT, the same fields, never a residual)
  T-OFF TETHER_DERIVED_SUBJECT=0: the same case writes relational_surprise rows, and ON (above)
        derived_new rows only -- the test separates the DS arms
  OFF   TETHER_DERIVED_PERCEPT=0: dcol is bet on again (today's per-slot charge)
  E0b, the observer-item-4 pair slots a~b.contact / bbox / inside (the reviewer 14:12):
  X     derive() on each observed frame of a ring with a mover inside reproduces every published
        contact / bbox / inside value (the cells rebuilt as shape key + (row, col))
  P     the mover steps right inside the ring's hole until it touches the wall: residual on its
        col (and the undeclared add_* / rem_*) only; no bet on the pair's contact / bbox / inside;
        no relational surprise
  MF-P  TETHER_DERIVED_PERCEPT=0: the pair's inside / bbox are bet on again

    python test_derived_percept.py
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
import numpy as np
from arcengine import FrameDataRaw, GameState
import tether_agent
mode, N = sys.argv[1], int(sys.argv[2])
REL = ("relational_surprise", "derived_new")   # DS: derived_new carries the same fields

class W:
    def __init__(self):
        self.calls, self._last, self.t = [], None, 0
        self.reset()
    @property
    def observation_space(self):
        return self._last
    def board(self, t, mid=False):
        b = np.zeros((40, 64), dtype=int)
        b[2:6, 2:6] = 7                                       # S, still
        if mode in ("drift", "stop"):
            c = 6 + 3 * min(t, 5 if mode == "stop" else t)
            b[20:23, c:c + 3] = 3
        elif mode == "resize":
            b[20:23, 10:10 + 2 + t] = 3                       # widens one column per action
        elif mode == "transient":
            b[20:23, 10:13 + (1 if mid else 0)] = 3           # wider only mid-cascade
        elif mode in ("ring", "x"):
            b[2:6, 2:6] = 0
            b[12:19, 12:19] = 7                               # a ring, its hole 13-17 x 13-17
            b[13:18, 13:18] = 0
            b[15, 14 + min(t, 3)] = 3                         # touches the wall at col 18 from t=3
        return b
    def _f(self, frames):
        f = FrameDataRaw(game_id="derive", state=GameState.NOT_FINISHED, levels_completed=0,
                         win_levels=2, guid="g", available_actions=[1, 2])
        f.frame = frames
        self._last = f
        return f
    def reset(self):
        self.calls.append("RESET")
        return self._f([self.board(0)])
    def step(self, action, data=None, reasoning=None):
        self.calls.append(action.name)
        self.t += 1
        if mode == "transient":
            return self._f([self.board(self.t, mid=True), self.board(self.t)])
        return self._f([self.board(self.t)])

if mode == "x":
    import arc_atoms, arc_percept, arc_predict, gamma
    from arc_world import ArcWorld
    env = ArcWorld(W(), arc_percept.Objects(),
                   gamma.primitives_once(arc_atoms.three_spaces(arc_predict.predict())),
                   palette=10, name="x")
    acts = [a for a in env.actions()]
    out = {"frames": 0, "checked": 0, "wrong": [], "attrs": []}
    for i in range(N):
        d = env.observe()
        got = env.derive(d)
        keys = [k for k in d if "~" in k.rsplit(".", 1)[0]
                and k.rsplit(".", 1)[1] in ("contact", "bbox", "inside")]
        out["frames"] += 1
        out["checked"] += len(keys)
        out["attrs"] = sorted(set(out["attrs"]) | {k.rsplit(".", 1)[1] for k in keys})
        out["wrong"] += [(i, k, d[k], got.get(k)) for k in keys if got.get(k) != d[k]]
        env.step(acts[0])
    print(json.dumps(out))
    sys.exit()
led = os.path.join(tempfile.mkdtemp(), "d.jsonl")
tether_agent.run(W(), "derive", max_actions=N, led_path=led)
rows = [json.loads(x) for x in open(led, encoding="utf-8")]
bets = [r for r in rows if r.get("event") == "bet" and r["detail"].get("channel") == "transition"]
cols = {}
for r in bets:
    if r["slot"].endswith(".col"):
        cols.setdefault(r["slot"].rsplit(".", 1)[0], set()).add(r["detail"].get("actual"))
widths = {}
for r in rows:
    if r.get("event") == "bet" and r["slot"].endswith(".shape"):
        widths.setdefault(r["slot"].rsplit(".", 1)[0], set()).add(r["detail"].get("actual"))
mover = max(cols, key=lambda o: len(cols[o])) if mode in ("drift", "stop", "ring") else max(
    widths or cols, key=lambda o: len((widths or cols)[o]))
mine = [r for r in bets if r["slot"].rsplit(".", 1)[0] == mover]
out = {"mover": mover,
       "col": [(r["cycle"], r["detail"].get("bound"), round(r["detail"].get("mass", 0), 2))
               for r in mine if r["slot"].endswith(".col")],
       "massive": sorted({r["slot"].rsplit(".", 1)[1] for r in mine
                           if r["detail"].get("mass", 0) > 0}),
       "bet_attrs": sorted({r["slot"].rsplit(".", 1)[1] for r in mine}),
       "rel": [(r["slot"], r.get("of"), r["detail"].get("derived"),
                r["detail"].get("actual"), r["event"])
               for r in rows if r.get("event") in REL
               and r["slot"].rsplit(".", 1)[0] == mover]}
mine_pair = [r for r in bets if mover in r["slot"].rsplit(".", 1)[0].split("~")
             and "~" in r["slot"].rsplit(".", 1)[0]]
out["pair_bets"] = sorted({r["slot"].rsplit(".", 1)[1] for r in mine_pair})
out["pair_rel"] = [(r["slot"], r["detail"].get("derived"), r["detail"].get("actual"))
                   for r in rows if r.get("event") in REL
                   and "~" in r["slot"].rsplit(".", 1)[0]]
print(json.dumps(out))
'''


def child(mode: str, n: int, extra: dict | None = None) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update({"PYTHONDONTWRITEBYTECODE": "1", **(extra or {})})
    p = subprocess.run([sys.executable, "-B", "-c", CHILD, mode, str(n)], capture_output=True,
                       text=True, env=env, cwd=os.path.dirname(os.path.abspath(__file__)),
                       stdin=subprocess.DEVNULL)
    assert p.returncode == 0, p.stderr[-2000:]
    return json.loads(p.stdout.strip().splitlines()[-1])


def main() -> int:
    m = child("drift", 8)
    bound = {c: (b, ms) for c, b, ms in m["col"]}
    late = [bound[c] for c in sorted(bound) if c >= 4]
    assert late and all(b.startswith("translate<") and ms == 0 for b, ms in late), m["col"]   # M
    assert "dcol" not in m["bet_attrs"] and "speed" not in m["bet_attrs"], m["bet_attrs"]
    assert not m["rel"], m["rel"]
    print("M col from cycle 4:", late[0], "; dcol/speed bet on:", "dcol" in m["bet_attrs"],
          "; relational surprises", len(m["rel"]))
    s = child("stop", 9)
    stop = [(c, b, ms) for c, b, ms in s["col"] if c == 5]
    assert stop and stop[0][2] > 0, s["col"]                                            # MF-M
    print("MF-M the mover stops at cycle 5: col", stop[0])
    r = child("resize", 5)
    assert "shape" in r["massive"] and not ({"w", "h", "dw", "dcells"} & set(r["bet_attrs"])), r
    assert not r["rel"], r["rel"]                                                       # R
    print("R resize: residual on", r["massive"], "; w/h/dw/dcells bet on:",
          sorted({"w", "h", "dw", "dcells"} & set(r["bet_attrs"])), "; relational", len(r["rel"]))
    t = child("transient", 4)
    assert t["rel"] and all(any(x.endswith(".shape") for x in (src or ()))
                            for _s, src, _d, _a, _e in t["rel"]), t["rel"]              # T
    assert {e for *_x, e in t["rel"]} == {"derived_new"}, t["rel"]          # T under DS (ON)
    print("T transient: relational surprises", t["rel"][:3])
    toff = child("transient", 4, {"TETHER_DERIVED_SUBJECT": "0"})
    assert toff["rel"] and {e for *_x, e in toff["rel"]} == {"relational_surprise"}, toff  # T-OFF
    print("T-OFF (TETHER_DERIVED_SUBJECT=0): relational surprises", toff["rel"][:3])
    off = child("drift", 6, {"TETHER_DERIVED_PERCEPT": "0"})
    assert "dcol" in off["bet_attrs"], off["bet_attrs"]                                   # OFF
    print("OFF: dcol bet on again:", "dcol" in off["bet_attrs"])
    x = child("x", 5)
    assert x["checked"] and not x["wrong"] and set(x["attrs"]) == {"contact", "bbox", "inside"}, x
    print("X derive reproduces", x["checked"], "published pair readings over", x["frames"],
          "frames:", x["attrs"])                                                          # X
    p = child("ring", 6)
    # add_* / rem_* stay bet (identity-dependent, not declared; priced as B in E3)
    own = [a for a in p["massive"] if not a.startswith(("add_", "rem_"))]
    assert own == ["col"] and not p["pair_bets"] and not p["pair_rel"], p                  # P
    print("P ring: residual on", p["massive"], "; pair bets", p["pair_bets"], "; relational",
          len(p["pair_rel"]))
    poff = child("ring", 6, {"TETHER_DERIVED_PERCEPT": "0"})
    assert {"inside", "bbox"} <= set(poff["pair_bets"]), poff["pair_bets"]                # MF-P
    print("MF-P OFF: pair bets", poff["pair_bets"])
    print("derived_percept: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
