"""8 VIEW_HOLD_SAME_ROLE (TETHER_VIEW_HOLD_SAME_ROLE, default ON; the reviewer 2026-10-30 r417).
Minimal gates: one must-fail, one must-hold, each in its own process.
  check_mustfail_holds  a stub library, RELATION with o == x: ON makes one lib.view call (under
                        "{o}", "{o}") for two asks and restores the name; OFF makes two named calls
  check_off_identity    MUST-HOLD: TETHER_VIEW_HOLD_SAME_ROLE=0 (off_env) against c1075e4, fake,
                        whole-run; and ON with TETHER_VIEW_HOLD_SAME_CHECK=1 on the same run: every
                        served view equal to a fresh lib.view (0 mismatches, served_same_role > 0)
    python tests/test_view_hold_same_role.py [check ...]
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
from test_contact_first import _child, _norm  # noqa: E402  the same probe and masks
from test_view_hold_same import COUNTS, _Lib  # noqa: E402  the same stub and run-counts probe

sys.dont_write_bytecode = True

BASE = "c1075e4"        # wip/finish2 after 7 VIEW_HOLD_SAME


def _asks(on: bool) -> tuple:
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    tether._AGENT_SEED = False
    tether._VIEW_HOLD_SAME_ROLE = on
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    lib = _Lib()
    a = ag._lib_view(lib, "entry", "RELATION", "o5", "o5")
    b = ag._lib_view(lib, "entry", "RELATION", "o7", "o7")
    return lib.calls, a, b, dict(ag._view_hold_n)


def check_mustfail_holds() -> None:
    calls, a, b, n = _asks(True)
    assert calls == [("entry", "RELATION", "{o}", "{o}")], calls
    assert a[0]["condition"] == "o5.col == o5.col", a
    assert b[0]["condition"] == "o7.col == o7.col", b
    assert n.get("held_same_role") == 1 and n.get("served_same_role") == 2, n
    calls_off, a_off, b_off, _n = _asks(False)   # MUST-FAIL: off, two named views
    assert calls_off == [("entry", "RELATION", "o5", "o5"),
                         ("entry", "RELATION", "o7", "o7")], calls_off
    assert a_off == a and b_off == b, (a_off, b_off)
    print(f"  on: 1 lib.view for 2 RELATION asks under one placeholder, names restored; off: 2; "
          f"{n}")


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
    off = _norm(_child(root, off_env("TETHER_VIEW_HOLD_SAME_ROLE")))
    diff = sum(1 for x, y in zip(base, off, strict=False) if x != y) + abs(len(base) - len(off))
    assert len(base) > 50 and diff == 0, (len(base), len(off), next(
        (i for i, (x, y) in enumerate(zip(base, off, strict=False)) if x != y), None))
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               TETHER_VIEW_HOLD_SAME_CHECK="1")
    out = subprocess.run([sys.executable, "-B", "-c", COUNTS, root], env=env, capture_output=True,
                         text=True, timeout=900, cwd=root, stdin=subprocess.DEVNULL)
    assert out.returncode == 0, out.stderr[-3000:]
    n = json.loads(out.stdout.strip().splitlines()[-1])
    assert n.get("served_same_role", 0) > 0, ("occasion: no MEASURE/RELATION o == x view", n)
    served = n.get("served_same", 0) + n["served_same_role"]
    assert n.get("same_checked", 0) == served and n.get("same_mismatch", 0) == 0, n
    print(f"  OFF identity (TETHER_VIEW_HOLD_SAME_ROLE=0, fake): {len(base)} rows against {BASE}, "
          f"0 differences; ON with the check: {n}")


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
    print(f"view_hold_same_role: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
