"""3 PROGRESS_SHELF (TETHER_PROGRESS_SHELF, default ON; the reviewer 2026-10-30 r392). Minimal
gates (r392): one must-fail, one must-hold, each in its own process.
  check_mustfail_shelves  on gridworld after 6 steps, a held condition naming a slot whose gap
                          shrank counts one progress at _note_progress, and a close without a
                          clear shelves it {won 0, lost 0, progress 1}; with the arm off nothing
                          is counted and the close drops it
  check_off_identity      TETHER_PROGRESS_SHELF=0 (off_env) against af6f0cd, fake, whole-run
    python tests/test_progress_shelf.py [check ...]
"""
from __future__ import annotations

import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
from test_contact_first import _child, _norm  # noqa: E402  the same probe and masks

sys.dont_write_bytecode = True

BASE = "af6f0cd"        # wip/finish after 2 ROUTE_NAMED
KEY = "progress_fixture"


def _held(on: bool) -> tuple:
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    tether._AGENT_SEED = False
    tether._PROGRESS_SHELF = on
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    for _ in range(6):
        ag.step()
    slot = sorted(s for s in ag.slots if "." in s and not s.startswith("@"))[0]
    ag._gap_delta.setdefault(slot, -1)           # the stub's "closer" needs a delta to row
    text = f"{slot} == 0"
    ag._goal_conds[KEY], ag._goal_text[KEY] = object(), text
    ag._goal_meta[KEY] = {"templates": ["{o}.col == 0"], "parts": [text], "level": ag.level}
    ag._goal_prog.clear()
    ag.improved = lambda s: s == slot
    n0 = len(ag.led.rows())
    ag._note_progress(dict(ag.trace[-1][0]) if ag.trace else {})
    prog = ag._goal_prog[KEY]
    ag._close_goals("end")
    shelved = [r["detail"] for r in ag.led.rows()[n0:] if r["event"] == "goal_shelved"]
    return slot, prog, ag._goal_shelf.get(KEY, {}).get("record"), shelved


def check_mustfail_shelves() -> None:
    slot, prog, rec, rows = _held(True)
    assert prog == 1, prog
    assert rec == {"won": 0, "lost": 0, "progress": 1}, rec
    assert rows and rows[-1]["record"] == rec, rows
    _s, prog_off, rec_off, rows_off = _held(False)   # MUST-FAIL: the arm off drops it
    assert prog_off == 0 and rec_off is None and not rows_off, (prog_off, rec_off, rows_off)
    print(f"  {slot}: one progress, shelved {rec}; off: nothing counted, nothing shelved")


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
    cur = _norm(_child(root, off_env("TETHER_PROGRESS_SHELF")))
    diff = sum(1 for x, y in zip(base, cur, strict=False) if x != y) + abs(len(base) - len(cur))
    assert len(base) > 50 and diff == 0, (len(base), len(cur), next(
        (i for i, (x, y) in enumerate(zip(base, cur, strict=False)) if x != y), None))
    print(f"  OFF identity (TETHER_PROGRESS_SHELF=0, fake): {len(base)} rows against {BASE}, "
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
    print(f"progress_shelf: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
