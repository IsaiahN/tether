"""22 INCREMENTAL_JUDGE (TETHER_INCREMENTAL_JUDGE, default ON; the reviewer 2026-10-31 r571).
Minimal gates, each in its own process.
  check_identity_and_long_life
                      THE MUST-HOLD: six movers (r481's fixture), 60 steps: the ON and OFF ledgers
                      identical row for row, the timing fields and the arms row aside; THE
                      MUST-FAIL, the same runs: the history rows _left walks and ROUTE's seconds
                      per step, OFF vs ON, as series; ON walks fewer in all and in the second half
  check_off_identity  TETHER_INCREMENTAL_JUDGE=0 (off_env) against 2d0df39, fake, whole-run
    python tests/test_incremental_judge.py [check ...]
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

BASE = "2d0df39"        # wip/incremental-judge before arm 22 (arm 20 + since_written)

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
rows_walked = [0]
real_left = tether.Agent._left
def left(self, term, slot, hist, ceiling=None, offset=0.0, start=0, total=0.0):
    rows_walked[0] += len(hist) - start
    return real_left(self, term, slot, hist, ceiling=ceiling, offset=offset, start=start,
                     total=total)
tether.Agent._left = left
env, ag, led, *_ = arc_holdout.wire(Movers(), "fake")
series = []
for _ in range(60):
    r0 = rows_walked[0]
    ag.step()
    series.append(rows_walked[0] - r0)
ag.end_run("cap")
print(json.dumps({"rows": ag.led.rows(), "series": series}, default=str))
'''


def _child(probe: str, tree: str, extra: dict | None = None) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               **(extra or {}))
    out = subprocess.run([sys.executable, "-B", "-c", probe, tree], env=env,
                         capture_output=True, text=True, timeout=3600, cwd=str(_repo.ROOT),
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


def _pair() -> tuple:
    root = str(_repo.ROOT)
    return _child(MOVERS, root), _child(MOVERS, root, {"TETHER_INCREMENTAL_JUDGE": "0"})


def _route(rows: list) -> list:
    return [round(r["detail"]["wall_s"].get("ROUTE", 0.0), 2) for r in rows
            if r["event"] == "repeat" and isinstance(r["detail"].get("wall_s"), dict)]


def check_identity_and_long_life() -> None:
    """The must-hold and the must-fail read off the same pair of runs."""
    on, off = _pair()
    a, b = _norm(off["rows"]), _norm(on["rows"])
    n, at = _diff(a, b)
    print(f"  ON vs OFF, six movers, 60 steps: {len(a)} rows OFF, {len(b)} ON, {n} differences"
          + (f", first at {at}: OFF {a[at][:4]} ON {b[at][:4]}" if at is not None else ""))
    assert len(a) > 100 and n == 0, ("STOP: ON is not OFF row for row", n, at)
    s_on, s_off = on["series"], off["series"]
    half = len(s_off) // 2
    print(f"  rows _left walked per step OFF: {s_off}")
    print(f"  rows _left walked per step ON:  {s_on}")
    print(f"  totals OFF {sum(s_off)}, ON {sum(s_on)}; second half OFF {sum(s_off[half:])}, ON "
          f"{sum(s_on[half:])}")
    r_off, r_on = _route(off["rows"]), _route(on["rows"])
    print(f"  ROUTE s per step OFF: {r_off}")
    print(f"  ROUTE s per step ON:  {r_on}")
    print(f"  ROUTE sum OFF {sum(r_off):.1f} s, ON {sum(r_on):.1f} s")
    assert sum(s_off) > 0, "the fixture walks no history OFF: the arm cannot be read"
    assert sum(s_on) < sum(s_off) and sum(s_on[half:]) < sum(s_off[half:]), (
        "STOP: ON walks no fewer rows", sum(s_on), sum(s_off))


def check_off_identity() -> None:
    root = str(_repo.ROOT)
    with tempfile.TemporaryDirectory() as d:
        tar = subprocess.run(["git", "-C", root, "archive", BASE], capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(d, filter="data")
        base = _norm(_child(FAKE, d)["rows"])
    cur = _norm(_child(FAKE, root, off_env("TETHER_INCREMENTAL_JUDGE"))["rows"])
    n, at = _diff(base, cur)
    assert len(base) > 50 and n == 0, (len(base), len(cur), at)
    print(f"  OFF identity (TETHER_INCREMENTAL_JUDGE=0, fake): {len(base)} rows against {BASE}, "
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
    print(f"incremental_judge: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
