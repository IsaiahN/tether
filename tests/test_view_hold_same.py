"""7 VIEW_HOLD_SAME (TETHER_VIEW_HOLD_SAME, default ON; the reviewer 2026-10-30 r414, r415).
Minimal gates: one must-fail, one must-hold, each in its own process.
  check_mustfail_holds  a stub library with o == x: ON makes one lib.view call (under "{o}", "{o}")
                        for two asks and restores the name; OFF makes two named calls
  check_off_identity    MUST-HOLD: TETHER_VIEW_HOLD_SAME=0 (off_env) against 3ebbab0, fake,
                        whole-run; and ON with TETHER_VIEW_HOLD_SAME_CHECK=1 on the same run: every
                        served "same" view equal to a fresh lib.view (0 mismatches, served > 0)
    python tests/test_view_hold_same.py [check ...]
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
from test_contact_first import _child, _norm  # noqa: E402  the same probe and masks

sys.dont_write_bytecode = True

BASE = "3ebbab0"        # general-agent after wip/finish

COUNTS = r'''
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
print(json.dumps(dict(ag._view_hold_n)))
'''


class _Lib:
    def __init__(self) -> None:
        self.calls: list = []

    def view(self, key: str, role: str, o: str, x: str) -> list:
        self.calls.append((key, role, o, x))
        return [{"condition": f"{o}.col == {x}.col", "template": "same", "reading": "col"},
                {"condition": f"{o}.row > 0", "template": "holds", "reading": "row"}]


def _asks(on: bool) -> tuple:
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    tether._AGENT_SEED = False
    tether._VIEW_HOLD_SAME = on
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    lib = _Lib()
    a = ag._lib_view(lib, "entry", "STATE", "o5", "o5")
    b = ag._lib_view(lib, "entry", "STATE", "o7", "o7")
    return lib.calls, a, b, dict(ag._view_hold_n)


def check_mustfail_holds() -> None:
    calls, a, b, n = _asks(True)
    assert calls == [("entry", "STATE", "{o}", "{o}")], calls
    assert a[0]["condition"] == "o5.col == o5.col", a
    assert b[0]["condition"] == "o7.col == o7.col", b
    assert n.get("held_same") == 1 and n.get("served_same") == 2, n
    calls_off, a_off, b_off, _n = _asks(False)   # MUST-FAIL: off, two named views
    assert calls_off == [("entry", "STATE", "o5", "o5"), ("entry", "STATE", "o7", "o7")], calls_off
    assert a_off == a and b_off == b, (a_off, b_off)
    print(f"  on: 1 lib.view for 2 asks (held under one placeholder), names restored; off: 2; {n}")


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
    off = _norm(_child(root, off_env("TETHER_VIEW_HOLD_SAME")))
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
    assert n.get("served_same", 0) > 0, ("occasion: no 'same' view served on the fake run", n)
    # 8 (e7a1c8e) serves MEASURE / RELATION o == x views from its own hold and the one check
    # counts both (tether.py same_checked); as test_view_hold_same_role.py:80 (r452 B1)
    served = n["served_same"] + n.get("served_same_role", 0)
    assert n.get("same_checked", 0) == served and n.get("same_mismatch", 0) == 0, n
    print(f"  OFF identity (TETHER_VIEW_HOLD_SAME=0, fake): {len(base)} rows against {BASE}, 0 "
          f"differences; ON with the check: {n}")


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
    print(f"view_hold_same: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
