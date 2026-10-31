"""16 CONTACT_LIGHT (TETHER_CONTACT_LIGHT, default ON; the reviewer 2026-10-31 r483, r490, r491).
Minimal gates, each in its own process.
  check_mustfail_resume  on gridworld after 8 steps, a second lookup for a slot with no new row
                         scores no row of a val-typed candidate and returns the same totals; with
                         the arm off it scores every row again
  check_on_off_rows      ON = OFF row for row on six identical movers (r481's fixture), 20 steps
  check_off_identity     TETHER_CONTACT_LIGHT=0 (off_env) against 3813c79, fake, whole-run
    python tests/test_contact_light.py [check ...]
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

BASE = "3813c79"        # general-agent, the tree before arm 16

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
print(json.dumps({"rows": ag.led.rows()}, default=str))
'''


def _child(probe: str, tree: str, extra: dict | None = None) -> list:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               **(extra or {}))
    out = subprocess.run([sys.executable, "-B", "-c", probe, tree], env=env,
                         capture_output=True, text=True, timeout=900, cwd=str(_repo.ROOT),
                         stdin=subprocess.DEVNULL)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])["rows"]


def _norm(rows: list) -> list:
    sys.path.insert(0, os.path.join(str(_repo.ROOT), "conform"))
    from identity_mod_rows import mask_timings
    return [(r["cycle"], r["step"], r["slot"], r["event"],
             json.dumps(r["detail"], sort_keys=True, default=str))
            for r in mask_timings(json.loads(json.dumps(rows))) if r["event"] != "arms"]


def _diff(a: list, b: list) -> tuple:
    n = sum(1 for x, y in zip(a, b, strict=False) if x != y) + abs(len(a) - len(b))
    return n, next((i for i, (x, y) in enumerate(zip(a, b, strict=False)) if x != y), None)


def check_mustfail_resume() -> None:
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    tether._AGENT_SEED = False
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    for _ in range(8):
        ag.step()
    slot = sorted(ag.alphabet)[0]
    held = ag.gamma.library[ag.bound.get(slot, tether.IDN)]
    hist = ag.history(slot)
    vals = [t for t in ag.gamma.library.values() if getattr(t, "out_type", "val") != tether.OBJ_TYPE]
    assert len(hist) > 3 and len(vals) > 3, (len(hist), len(vals))
    rows = [0]
    real = type(ag)._left

    def spy(self, term, s, h, *a, start=0, **k):
        rows[0] += len(h) - start
        return real(self, term, s, h, *a, start=start, **k)

    type(ag)._left = spy
    cells = ag._cl_cells_for(slot, held)
    first = [ag._cl_left(t, slot, hist, cells) for t in vals]
    rows[0] = 0
    second = [ag._cl_left(t, slot, hist, ag._cl_cells_for(slot, held)) for t in vals]
    resumed = rows[0]
    rows[0] = 0
    walked = [ag._cl_left(t, slot, hist, None) for t in vals]   # MUST-FAIL: the arm off
    assert first == second == walked, "the totals moved"
    assert resumed == 0, ("a second lookup with no new row scored rows", resumed)
    assert rows[0] == len(vals) * len(hist), ("MUST-FAIL: off scores every row", rows[0])
    print(f"  {slot}: {len(vals)} val-typed candidates x {len(hist)} rows; second lookup scored 0 "
          f"rows, off scored {rows[0]}; totals equal")


def check_on_off_rows() -> None:
    root = str(_repo.ROOT)
    on = _norm(_child(MOVERS, root))
    off = _norm(_child(MOVERS, root, {"TETHER_CONTACT_LIGHT": "0"}))
    n, at = _diff(off, on)
    assert len(off) > 50 and n == 0, (len(off), len(on), at)
    print(f"  ON = OFF on six movers, 20 steps: {len(off)} rows, 0 differences")


def check_off_identity() -> None:
    root = str(_repo.ROOT)
    with tempfile.TemporaryDirectory() as d:
        tar = subprocess.run(["git", "-C", root, "archive", BASE], capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(d, filter="data")
        base = _norm(_child(FAKE, d))
    cur = _norm(_child(FAKE, root, off_env("TETHER_CONTACT_LIGHT")))
    n, at = _diff(base, cur)
    assert len(base) > 50 and n == 0, (len(base), len(cur), at)
    print(f"  OFF identity (TETHER_CONTACT_LIGHT=0, fake): {len(base)} rows against {BASE}, "
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
    print(f"contact_light: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
