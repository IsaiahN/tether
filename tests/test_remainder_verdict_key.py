"""14 REMAINDER_VERDICT_KEY (TETHER_REMAINDER_VERDICT_KEY, default ON; the reviewer r466 1(b)).
Minimal gates, each in its own process.
  check_mustfail_gate  demo.py replayed on the three draws (their seeds only, tests/fixtures/
                       demo_draw_*.jsonl), with 12 ON: OFF, gate.py refuses each ledger on check
                       "unreached" (the remainder row's copied "verdict" read as a park with no
                       coverage); ON, gate.py passes all three
  check_keys_only      MUST-HOLD: on each draw the ON and OFF ledgers are equal once the remainder
                       rows' two keys are named back (timings and the arms row masked)
  check_off_identity   MUST-HOLD: TETHER_REMAINDER_VERDICT_KEY=0 (off_env) byte-equal to 9eb4012
                       on the fake whole run
    python tests/test_remainder_verdict_key.py [check ...]
"""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
from test_contact_first import _child, _norm  # noqa: E402  the same probe and masks

sys.dont_write_bytecode = True

BASE = "9eb4012"        # 12 STOP_READ_STEP, before 14
DRAWS = ("c36f0f02", "838dce71", "c2377d1e")
KEYS = {"mint_verdict": "verdict", "mint_verdict_cycle": "verdict_cycle"}


def _demo(draw: str, arm: str) -> tuple[int, dict, list]:
    """demo.py on the pinned draw with 14 set (12 at its default, ON); gate.py's rc and verdict on
    its ledger; its rows."""
    root = str(_repo.ROOT)
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", TETHER_REMAINDER_VERDICT_KEY=arm,
               TETHER_SEED_FROM=os.path.join(root, "tests", "fixtures", f"demo_draw_{draw}.jsonl"))
    subprocess.run([sys.executable, "-B", "demo.py"], cwd=root, env=env, capture_output=True,
                   text=True, timeout=600, stdin=subprocess.DEVNULL)
    led = os.path.join(root, "runs", "demo.jsonl")
    g = subprocess.run([sys.executable, "-B", "gate.py", led], cwd=root, capture_output=True,
                       text=True, timeout=600)
    with open(led, encoding="utf-8") as fh:
        rows = [json.loads(x) for x in fh if x.strip()]
    return g.returncode, json.loads(g.stdout), rows


def check_mustfail_gate() -> None:
    for d in DRAWS:
        orc, off, off_rows = _demo(d, "0")
        assert orc != 0 and off["check"] == "unreached", (
            "MUST-FAIL: OFF should be refused", d, off)
        n = sum(1 for r in off_rows if r["event"] == "remainder")
        assert n > 0, ("occasion: no remainder row", d)
        nrc, on, _on_rows = _demo(d, "1")
        assert nrc == 0, ("ON should pass the gate", d, on)
        print(f"  {d}: OFF gate rc {orc} on '{off['check']}' ({n} remainder rows); "
              f"ON gate rc {nrc}")


def check_keys_only() -> None:
    for d in DRAWS:
        _rc, _v, off_rows = _demo(d, "0")
        _rc, _v, on_rows = _demo(d, "1")
        named = [{**r, "detail": {KEYS.get(k, k): v for k, v in r["detail"].items()}}
                 if r["event"] == "remainder" else r for r in on_rows]
        off, on = _norm(off_rows), _norm(named)
        diff = sum(1 for x, y in zip(off, on, strict=False) if x != y) + abs(len(off) - len(on))
        n = sum(1 for r in on_rows if r["event"] == "remainder")
        assert n > 0 and diff == 0, ("ON and OFF differ beyond the two keys", d, diff, next(
            (i for i, (x, y) in enumerate(zip(off, on, strict=False)) if x != y), None))
        print(f"  {d}: {len(on)} rows, {n} remainder rows; equal once the two keys are named back")


def check_off_identity() -> None:
    import tarfile
    import tempfile

    from _batch import off_env
    root = str(_repo.ROOT)
    with tempfile.TemporaryDirectory() as d:
        tar = subprocess.run(["git", "-C", root, "archive", BASE], capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(d, filter="data")
        base = _norm(_child(d))
    off = _norm(_child(root, off_env("TETHER_REMAINDER_VERDICT_KEY")))
    diff = sum(1 for x, y in zip(base, off, strict=False) if x != y) + abs(len(base) - len(off))
    assert len(base) > 50 and diff == 0, ("OFF", len(base), len(off), next(
        (i for i, (x, y) in enumerate(zip(base, off, strict=False)) if x != y), None))
    print(f"  OFF (TETHER_REMAINDER_VERDICT_KEY=0, fake): {len(base)} rows against {BASE}, "
          f"0 differences")


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
    print(f"remainder_verdict_key: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
