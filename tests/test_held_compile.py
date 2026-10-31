"""18 HELD_COMPILE_MEMO (TETHER_HELD_COMPILE_MEMO, default ON; the reviewer 2026-10-31 r512, r524).
Minimal gates, each in its own process.
  check_mustfail_compiles  six identical movers (r481's fixture), 20 steps: ON compiles each
                           distinct (signature, condition, subject) once; OFF compiles them
                           again per entry
  check_on_off_rows        ON = OFF row for row on the same fixture, timings masked; ON's repeat
                           rows carry reach_s within the step's total, OFF's none
  check_off_identity       TETHER_HELD_COMPILE_MEMO=0 (off_env) against 8e6efa5, fake, whole-run
    python tests/test_held_compile.py [check ...]
"""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile

from _batch import off_env  # noqa: E402  the batch's arms (r348)

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

BASE = "8e6efa5"        # wip/contact-tally, the tree before arm 18

FAKE = r'''
import json, sys
sys.dont_write_bytecode = True
tree = sys.argv[1]
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import arc_holdout
from test_entry import FakeWrapper
env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
for _ in range(24):
    ag.step()
ag.end_run("cap")
print(json.dumps({"rows": ag.led.rows()}, default=str))
'''

MOVERS = r'''
import json, sys
sys.dont_write_bytecode = True
tree = sys.argv[1]
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import numpy as np
import arc_holdout
import tether
from arcengine import FrameDataRaw
from test_entry import FakeWrapper
OFFS = [(0, 0), (0, 12), (12, 0), (12, 12), (24, 0), (24, 12)]
class Movers(FakeWrapper):
    def _frame(self, state):
        g = np.zeros((64, 64), dtype=int)
        r, c = self.pos
        for dr, dc in OFFS:
            g[r + dr:r + dr + 4, c + dc:c + dc + 4] = 3
        g[60:63, 60:63] = 7
        f = FrameDataRaw(game_id="fake-0001", state=state, levels_completed=0, win_levels=2,
                         guid="g", available_actions=list(self.actions))
        f.frame = [g]
        self._last = f
        return f
    def step(self, action, data=None, reasoning=None):
        out = super().step(action, data, reasoning)
        self.pos = [min(self.pos[0], 32), min(self.pos[1], 40)]
        return self._frame(out.state) if out.frame else out
env, ag, led, *_ = arc_holdout.wire(Movers(), "fake")
for _ in range(20):
    ag.step()
ag.end_run("cap")
print(json.dumps({"rows": ag.led.rows(), "compiles": tether._INDEX_N["held_compile"],
                  "memo": len(tether._HELD_COMPILE)}, default=str))
'''


def _child(probe: str, tree: str, extra: dict | None = None) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               **(extra or {}))
    out = subprocess.run([sys.executable, "-B", "-c", probe, tree], env=env,
                         capture_output=True, text=True, timeout=1800, cwd=str(_repo.ROOT),
                         stdin=subprocess.DEVNULL)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


def _norm(rows: list) -> list:
    sys.path.insert(0, os.path.join(str(_repo.ROOT), "conform"))
    from identity_mod_rows import mask_timings
    return [(r["cycle"], r["step"], r["slot"], r["event"],
             json.dumps(r["detail"], sort_keys=True, default=str))
            for r in mask_timings(json.loads(json.dumps(rows))) if r["event"] != "arms"]


def _diff(a: list, b: list) -> tuple:
    n = sum(1 for x, y in zip(a, b, strict=False) if x != y) + abs(len(a) - len(b))
    return n, next((i for i, (x, y) in enumerate(zip(a, b, strict=False)) if x != y), None)


def _route(rows: list) -> float:
    return sum(r["detail"]["wall_s"].get("ROUTE", 0.0) for r in rows
               if r["event"] == "repeat" and isinstance(r["detail"].get("wall_s"), dict))


def check_mustfail_compiles() -> None:
    root = str(_repo.ROOT)
    on = _child(MOVERS, root)
    off = _child(MOVERS, root, {"TETHER_HELD_COMPILE_MEMO": "0"})
    assert on["compiles"] > 0 and on["compiles"] == on["memo"], ("ON compiles", on["compiles"],
                                                                 on["memo"])
    assert off["memo"] == 0 and off["compiles"] > 10 * on["compiles"], (
        "MUST-FAIL: OFF compiles per entry", off["compiles"], on["compiles"])
    print(f"  held compiles on six movers, 20 steps: OFF {off['compiles']}, ON {on['compiles']} "
          f"(= the distinct keys); ROUTE sum OFF {_route(off['rows']):.2f} s, "
          f"ON {_route(on['rows']):.2f} s")


def check_on_off_rows() -> None:
    root = str(_repo.ROOT)
    on = _child(MOVERS, root)["rows"]
    off = _child(MOVERS, root, {"TETHER_HELD_COMPILE_MEMO": "0"})["rows"]
    rep_on = [r["detail"] for r in on if r["event"] == "repeat"]
    rep_off = [r["detail"] for r in off if r["event"] == "repeat"]
    assert rep_on and all("reach_s" in d and 0 <= d["reach_s"] <= d["wall_s"]["total"] + 1e-3
                          for d in rep_on), "ON: every repeat row carries reach_s within its total"
    assert not any("reach_s" in d for d in rep_off), "OFF writes reach_s"
    a, b = _norm(off), _norm(on)
    n, at = _diff(a, b)
    assert len(a) > 50 and n == 0, (len(a), len(b), at)
    print(f"  ON = OFF on six movers, 20 steps: {len(a)} rows, 0 differences; ON reach_s on "
          f"{len(rep_on)} repeat rows, sum {sum(d['reach_s'] for d in rep_on):.2f} s")


def check_off_identity() -> None:
    root = str(_repo.ROOT)
    with tempfile.TemporaryDirectory() as d:
        tar = subprocess.run(["git", "-C", root, "archive", BASE], capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(d, filter="data")
        base = _norm(_child(FAKE, d)["rows"])
    cur = _norm(_child(FAKE, root, off_env("TETHER_HELD_COMPILE_MEMO"))["rows"])
    n, at = _diff(base, cur)
    assert len(base) > 50 and n == 0, (len(base), len(cur), at)
    print(f"  OFF identity (TETHER_HELD_COMPILE_MEMO=0, fake): {len(base)} rows against {BASE}, "
          "0 differences")


def main() -> int:
    want = sys.argv[1:]
    names = [k for k in globals() if k.startswith("check_") and (not want or k in want)]
    assert not want or len(names) == len(want), ("unknown check name", sorted(want))
    if len(names) == 1:
        globals()[names[0]]()
        print("ok  ", names[0])
        return 0
    for n in names:
        r = subprocess.run([sys.executable, "-B", __file__, n], cwd=str(_repo.ROOT),
                           stdin=subprocess.DEVNULL)
        assert r.returncode == 0, n
    print(f"held_compile: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
