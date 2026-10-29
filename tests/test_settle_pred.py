"""THE SETTLE ROW CARRIES ITS OWN PREDICTION, RECORD ONLY (TETHER_SETTLE_PRED, default ON; the
reviewer 2026-10-29 r288, r294; harvest item 6). Two fixtures, so both outcomes have an occasion:
the fake ARC game (16 steps; its bound terms settle on predicted CHANGES) and gridworld default
seed 0 (30 steps; its settles agree with persistence). Each check runs in its own process.
  check_on            every settle row carries predicted_code, actual_code, from_value,
                      from_code, risky; the prediction equals the actual in code space on every
                      row (a settle is a held prediction, so the bet-row join's "contradicted"
                      cannot occur); risky == (predicted_code != from_code); risky True occurs
                      (fake) and False occurs (gridworld)
  check_off           MUST-FAIL OFF: no settle row carries the fields
  check_off_identity  the arm OFF writes the same ledger as d1c64f0 on both fixtures, arms rows
                      aside and wall timings masked
    python tests/test_settle_pred.py [check ...]
"""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

BASE = "d1c64f0"      # the tree before the arm
FIELDS = ("predicted_code", "actual_code", "from_value", "from_code", "risky")

PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
tree, which = sys.argv[1], sys.argv[2]
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
if which == "fake":
    import arc_holdout
    from test_entry import FakeWrapper
    env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
    n = 16
else:
    import gamma, gridworld, ledger, tether, world
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    n = 30
for _ in range(n):
    ag.step()
print(json.dumps({"rows": ag.led.rows()}, default=str))
'''


def child(tree: str, which: str, extra: dict | None = None) -> list:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               **(extra or {}))
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, tree, which], env=env,
                         capture_output=True, text=True, timeout=900, cwd=str(_repo.ROOT),
                         stdin=subprocess.DEVNULL)
    assert out.returncode == 0, out.stderr[-3000:]
    return json.loads(out.stdout.strip().splitlines()[-1])["rows"]


def settles(rows: list) -> list:
    return [r["detail"] for r in rows if r["event"] == "settle"]


def check_on() -> None:
    root = str(_repo.ROOT)
    got = {w: settles(child(root, w)) for w in ("fake", "gridworld")}
    for w, ds in got.items():
        assert ds, ("occasion: no settle row", w)
        for d in ds:
            assert all(k in d for k in FIELDS), ("a settle row lacks the fields", w, d)
            assert d["actual_code"] == d["predicted_code"], ("held, yet differs in code", w, d)
            assert d["risky"] == (d["predicted_code"] != d["from_code"]), ("risky", w, d)
    risky = {w: sum(1 for d in ds if d["risky"]) for w, ds in got.items()}
    assert risky["fake"] > 0, ("occasion: no risky settle on the fake", got["fake"][:2])
    assert risky["gridworld"] < len(got["gridworld"]), ("occasion: no null-agreeing settle",
                                                        got["gridworld"][:2])
    ex = next(d for d in got["fake"] if d["risky"])
    print(f"  ON: fake {len(got['fake'])} settles ({risky['fake']} risky, e.g. {ex['term']} "
          f"predicted {ex['predicted_code']} from {ex['from_code']}, held); gridworld "
          f"{len(got['gridworld'])} settles ({risky['gridworld']} risky); every row's prediction "
          "equals its actual in code space (0 contradicted)")


def check_off() -> None:
    root = str(_repo.ROOT)
    for w in ("fake", "gridworld"):
        ds = settles(child(root, w, {"TETHER_SETTLE_PRED": "0"}))
        assert ds, ("MUST-FAIL occasion: no settle row", w)
        assert not any(k in d for d in ds for k in FIELDS), ("OFF wrote a field", w, ds[0])
    print("  MUST-FAIL OFF: settle rows on both fixtures carry none of the fields")


def check_off_identity() -> None:
    root = str(_repo.ROOT)
    sys.path.insert(0, os.path.join(root, "conform"))
    from identity_mod_rows import mask_timings

    def norm(rows):
        return [(r["cycle"], r["step"], r["slot"], r["event"],
                 json.dumps(r["detail"], sort_keys=True, default=str))
                for r in mask_timings(json.loads(json.dumps(rows))) if r["event"] != "arms"]
    with tempfile.TemporaryDirectory() as d:
        tar = subprocess.run(["git", "-C", root, "archive", BASE], capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(d, filter="data")
        for w in ("fake", "gridworld"):
            base = norm(child(d, w))
            cur = norm(child(root, w, {"TETHER_SETTLE_PRED": "0"}))
            diff = sum(1 for x, y in zip(base, cur, strict=False) if x != y) + abs(len(base)
                                                                                  - len(cur))
            assert len(base) > 50 and diff == 0, ("OFF identity", w, len(base), len(cur),
                                                 next((i for i, (x, y) in enumerate(
                                                     zip(base, cur, strict=False)) if x != y),
                                                     None))
            print(f"  OFF identity ({w}): {len(base)} rows against {BASE}, 0 differences")


def main() -> int:
    want = set(sys.argv[1:])
    checks = [v for k, v in globals().items() if k.startswith("check_")
              and (not want or k in want)]
    assert not want or len(checks) == len(want), ("unknown check name", sorted(want))
    for c in checks:
        c()
        print("ok  ", c.__name__)
    print(f"settle_pred: {len(checks)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
