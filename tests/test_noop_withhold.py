"""23 NOOP_WITHHOLD (TETHER_NOOP_WITHHOLD, default ON; the reviewer 2026-10-31 r571).
Minimal gates, each in its own process, on test_entry's FakeWrapper (one block the four directions
move; the click and a move into the edge change nothing), 40 steps.
  check_no_repeat     THE MUST-FAIL: a press (board, action, coordinate) whose earlier press on that
                      identical board changed nothing is repeated under OFF; under ON it is repeated
                      only where every option was withheld (the lift)
  check_rows          ON writes PLAN @noop withheld rows, OFF none; no step goes without a press
                      that OFF made one on
  check_off_identity  TETHER_NOOP_WITHHOLD=0 (off_env) against 1e9d4d5, fake, whole-run
    python tests/test_noop_withhold.py [check ...]
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

BASE = "1e9d4d5"        # general-agent, the tree before arm 23

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

PRESSES = r'''
import hashlib, json, sys
sys.dont_write_bytecode = True
tree = sys.argv[1]
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import numpy as np
import arc_holdout
from test_entry import FakeWrapper
presses = []
class Spy(FakeWrapper):
    def step(self, action, data=None, reasoning=None):
        before = hashlib.sha1(np.asarray(self._last.frame[-1]).tobytes()).hexdigest() \
            if self._last is not None and len(self._last.frame) else None
        out = super().step(action, data, reasoning)
        after = hashlib.sha1(np.asarray(out.frame[-1]).tobytes()).hexdigest() \
            if len(out.frame) else before
        presses.append([before, action.name, json.dumps(data, sort_keys=True), before == after])
        return out
env, ag, led, *_ = arc_holdout.wire(Spy(), "fake")
for _ in range(40):
    ag.step()
ag.end_run("cap")
print(json.dumps({"rows": ag.led.rows(), "presses": presses}, default=str))
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


def _repeats(presses: list) -> tuple:
    """(presses, no-op presses, repeats of a press that changed nothing on that identical board)."""
    dead, rep, nop = set(), 0, 0
    for before, act, data, same in presses:
        key = (before, act, data)
        rep += key in dead
        if same:
            nop += 1
            dead.add(key)
    return len(presses), nop, rep


def _pair() -> tuple:
    root = str(_repo.ROOT)
    return _child(PRESSES, root), _child(PRESSES, root, {"TETHER_NOOP_WITHHOLD": "0"})


def check_no_repeat() -> None:
    on, off = _pair()
    n_on, nop_on, rep_on = _repeats(on["presses"])
    n_off, nop_off, rep_off = _repeats(off["presses"])
    lifted = sum(1 for r in on["rows"] if "every option vetoed" in json.dumps(r["detail"]))
    print(f"  OFF: presses {n_off}, no-op presses {nop_off}, repeats of a known no-op on the same "
          f"board {rep_off}")
    print(f"  ON: presses {n_on}, no-op presses {nop_on}, repeats {rep_on}; rows naming the lift "
          f"(every option vetoed) {lifted}")
    assert rep_off > 0, "the fixture never repeats a no-op OFF: the arm cannot be read"
    assert rep_on <= lifted, ("STOP: ON repeated a known no-op without the lift", rep_on, lifted)


def check_rows() -> None:
    on, off = _pair()
    n_on = sum(1 for r in on["rows"] if r["event"] == "withheld" and r["slot"] == "@noop")
    n_off = sum(1 for r in off["rows"] if r["event"] == "withheld" and r["slot"] == "@noop")
    print(f"  @noop withheld rows ON {n_on}, OFF {n_off}; presses ON {len(on['presses'])}, OFF "
          f"{len(off['presses'])}")
    assert n_on and not n_off, (n_on, n_off)
    assert len(on["presses"]) >= len(off["presses"]), "ON pressed less often than OFF"


def check_off_identity() -> None:
    root = str(_repo.ROOT)
    with tempfile.TemporaryDirectory() as d:
        tar = subprocess.run(["git", "-C", root, "archive", BASE], capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(d, filter="data")
        base = _norm(_child(FAKE, d)["rows"])
    cur = _norm(_child(FAKE, root, off_env("TETHER_NOOP_WITHHOLD"))["rows"])
    n, at = _diff(base, cur)
    assert len(base) > 50 and n == 0, (len(base), len(cur), at)
    print(f"  OFF identity (TETHER_NOOP_WITHHOLD=0, fake): {len(base)} rows against {BASE}, "
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
    print(f"noop_withhold: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
