"""4 UNTESTED_KEEP (TETHER_UNTESTED_KEEP, default ON; the reviewer 2026-10-30 r392, r397). Minimal
gates (r392): one must-fail, one must-hold, each in its own process.
  check_mustfail_keeps  on gridworld after 6 steps, a held hypothesis ended with steps 0 and touches
                        0 ends "untested" (ended_by kept) and stays off _hyp_tried; with the arm off
                        it enters _hyp_tried with the check's own why
  check_off_identity    TETHER_UNTESTED_KEEP=0 (off_env) against 5cb5e78, fake, whole-run
    python tests/test_untested_keep.py [check ...]
"""
from __future__ import annotations

import subprocess
import sys
from collections import Counter

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
from test_contact_first import _child, _norm  # noqa: E402  the same probe and masks

sys.dont_write_bytecode = True

BASE = "5cb5e78"        # wip/finish after 3 PROGRESS_SHELF
TKEY = ("{o}.col == 0", "fixture.col", None)


def _end(on: bool) -> tuple:
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    tether._AGENT_SEED = False
    tether._UNTESTED_KEEP = on
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    for _ in range(6):
        ag.step()
    ag._hyp = {"key": "untested_fixture", "text": "fixture.col == 0", "slots": ["fixture.col"],
               "tkey": TKEY, "cond": None, "source": "library", "shelf": None, "steps": 0,
               "touches": 0, "losses": 0, "held_unreadable": 0, "reads": {}, "seg": {},
               "displaced": {}, "acted": Counter({"system0": 1})}
    n0 = len(ag.led.rows())
    ag._hyp_end("no object of its kind")
    rows = [r["detail"] for r in ag.led.rows()[n0:] if r["event"] == "goal_hypothesis_end"]
    return rows[-1], TKEY in ag._hyp_tried, TKEY in ag._untested


def check_mustfail_keeps() -> None:
    row, tried, kept = _end(True)
    assert row["why"] == "untested" and row["ended_by"] == "no object of its kind", row
    assert not tried and kept, (tried, kept)
    row_off, tried_off, kept_off = _end(False)  # MUST-FAIL: the arm off marks it tried
    assert row_off["why"] == "no object of its kind" and "ended_by" not in row_off, row_off
    assert tried_off and not kept_off, (tried_off, kept_off)
    print("  steps 0, touches 0: ends 'untested' (ended_by 'no object of its kind'), not tried; "
          "off: tried")


def check_off_identity() -> None:
    import io
    import tarfile
    import tempfile

    from _batch import off_env
    root = str(_repo.ROOT)
    with tempfile.TemporaryDirectory() as d:
        tar = subprocess.run(["git", "-C", root, "archive", BASE], capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(d, filter="data")
        base = _norm(_child(d))
    cur = _norm(_child(root, off_env("TETHER_UNTESTED_KEEP")))
    diff = sum(1 for x, y in zip(base, cur, strict=False) if x != y) + abs(len(base) - len(cur))
    assert len(base) > 50 and diff == 0, (len(base), len(cur), next(
        (i for i, (x, y) in enumerate(zip(base, cur, strict=False)) if x != y), None))
    print(f"  OFF identity (TETHER_UNTESTED_KEEP=0, fake): {len(base)} rows against {BASE}, "
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
    print(f"untested_keep: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
