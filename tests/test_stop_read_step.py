"""12 STOP_READ_STEP (TETHER_STOP_READ_STEP, default ON; the reviewer r462, r463).
Minimal gates: one must-fail, one must-hold, each in its own process.
  check_mustfail_step_order  demo.py replayed on draw c2377d1e (its seed only, in
                             tests/fixtures/demo_draw_c2377d1e.jsonl): OFF, gate.py refuses its
                             ledger on check "steps" (a slot MINT after ACCEPT); ON, no "steps"
                             refusal, and the 1c rows say ACCEPT
  check_off_identity         MUST-HOLD: TETHER_STOP_READ_STEP=0 (off_env) byte-equal to cba1dd5 on
                             the fake whole run; ON's run is compared too
    python tests/test_stop_read_step.py [check ...]
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

BASE = "cba1dd5"        # general-agent's release, before 12
DRAW = os.path.join(str(_repo.ROOT), "tests", "fixtures", "demo_draw_c2377d1e.jsonl")
FOUR = ("stop_rule", "stop_read", "split_aim_left", "remainder")


def _demo(arm: str) -> tuple[dict, list]:
    """demo.py on the pinned draw with the arm set; gate.py's verdict on its ledger; its rows."""
    root = str(_repo.ROOT)
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", TETHER_SEED_FROM=DRAW, TETHER_STOP_READ_STEP=arm)
    subprocess.run([sys.executable, "-B", "demo.py"], cwd=root, env=env, capture_output=True,
                   text=True, timeout=600, stdin=subprocess.DEVNULL)
    led = os.path.join(root, "runs", "demo.jsonl")
    g = subprocess.run([sys.executable, "-B", "gate.py", led], cwd=root, capture_output=True,
                       text=True, timeout=600)
    with open(led, encoding="utf-8") as fh:
        rows = [json.loads(x) for x in fh if x.strip()]
    return json.loads(g.stdout), rows


def check_mustfail_step_order() -> None:
    off, off_rows = _demo("0")
    assert off["check"] == "steps" and "MINT after ACCEPT" in off.get("note", ""), off
    on, on_rows = _demo("1")
    assert on["check"] != "steps", on
    steps = {r["step"] for r in on_rows if r["event"] in FOUR}
    assert steps == {"ACCEPT"}, steps
    n = sum(1 for r in on_rows if r["event"] in FOUR)
    print(f"  OFF: gate refuses on 'steps' ({off['note']}); ON: no 'steps' refusal (gate: "
          f"{on['check'] or 'pass'}), {n} 1c rows all ACCEPT; rows OFF {len(off_rows)} ON "
          f"{len(on_rows)}")


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
    off = _norm(_child(root, off_env("TETHER_STOP_READ_STEP")))
    diff = sum(1 for x, y in zip(base, off, strict=False) if x != y) + abs(len(base) - len(off))
    assert len(base) > 50 and diff == 0, ("OFF", len(base), len(off), next(
        (i for i, (x, y) in enumerate(zip(base, off, strict=False)) if x != y), None))
    on_rows = _child(root)
    on = _norm(on_rows)
    n4 = sum(1 for r in on_rows if r["event"] in FOUR)
    on_diff = sum(1 for x, y in zip(base, on, strict=False) if x != y) + abs(len(base) - len(on))
    assert n4 > 0 or on_diff == 0, ("ON differs with no 1c row", on_diff)
    print(f"  OFF (TETHER_STOP_READ_STEP=0, fake): {len(base)} rows against {BASE}, 0 differences; "
          f"ON: {n4} 1c rows, {on_diff} rows differ")


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
    print(f"stop_read_step: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
