"""9 CONTINGENT_ONE_PASS (TETHER_CONTINGENT_ONE_PASS, default ON; B3, the reviewer r427).
Minimal gates: one must-fail, one must-hold, each in its own process.
  check_mustfail_one_pass  an Agency whose tried counts its own iterations: ON iterates it once,
                           OFF once plus once per distinct slot; both return the same list; ON's
                           second call in a step does not re-scan, and one after note() does
  check_off_identity       MUST-HOLD: TETHER_CONTINGENT_ONE_PASS=0 (off_env) and the arm ON are
                           each byte-equal to e7a1c8e on the fake whole run; and on that run every
                           contingent() call returns the same list either way (calls > 0)
    python tests/test_contingent_one_pass.py [check ...]
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from collections import Counter

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
from test_contact_first import _child, _norm  # noqa: E402  the same probe and masks

sys.dont_write_bytecode = True

BASE = "e7a1c8e"        # wip/finish2 after 8 VIEW_HOLD_SAME_ROLE

SAME = r'''
import json, sys
sys.dont_write_bytecode = True
tree = sys.argv[1]
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
import arc_holdout
import instruments
from test_entry import FakeWrapper
n = {"calls": 0, "differ": 0, "tried_max": 0}
one = instruments.Agency.contingent
def both(self):
    instruments._CONTINGENT_ONE_PASS = True
    a = one(self)
    instruments._CONTINGENT_ONE_PASS = False
    b = one(self)
    instruments._CONTINGENT_ONE_PASS = True
    n["calls"] += 1
    n["differ"] += a != b
    n["tried_max"] = max(n["tried_max"], len(self.tried))
    return a
instruments.Agency.contingent = both
env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
for _ in range(24):
    ag.step()
print(json.dumps(n))
'''


class _Tried(Counter):
    def __init__(self, *a) -> None:
        super().__init__(*a)
        self.iters = 0

    def __iter__(self):
        self.iters += 1
        return super().__iter__()


def _agency(on: bool) -> tuple:
    import instruments
    instruments._CONTINGENT_ONE_PASS = on
    ag = instruments.Agency()
    ag.tried = _Tried()
    for s in ("o1.row", "o1.col", "o2.row", "o3.col"):
        for a in ("ACTION1", "ACTION2"):
            ag.tried[(s, a)] += 2
    ag.moved[("o1.row", "ACTION1")] = 2         # always under ACTION1, never under ACTION2
    ag.moved[("o2.row", "ACTION1")] = 1         # sometimes: not contingent
    ag.moved[("o3.col", "ACTION2")] = 2
    ag.moved[("o3.col", "ACTION1")] = 2         # always under both: not contingent
    ag.tried.iters = 0
    got = ag.contingent()
    return got, ag.tried.iters, ag


def check_mustfail_one_pass() -> None:
    on, it_on, ag = _agency(True)
    off, it_off, _ag = _agency(False)           # MUST-FAIL: off scans tried once per slot
    assert on == off == ["o1.row"], (on, off)
    assert it_on == 1 and it_off == 1 + 4, (it_on, it_off)
    import instruments
    instruments._CONTINGENT_ONE_PASS = True     # _agency(False) set it off for the module
    again = ag.contingent()                     # the same step: held, no second scan
    assert again == on and ag.tried.iters == 1, (again, ag.tried.iters)
    ag.note("ACTION2", set(), ["o1.row"])       # a write: the next call scans once more
    assert ag.contingent() == ["o1.row"] and ag.tried.iters == 2, ag.tried.iters
    print(f"  on: {on}, tried iterated {it_on}x, a second call in the step 0 more, after a "
          f"note 1 more; off: the same list, iterated {it_off}x")


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
    for name, extra in (("OFF", off_env("TETHER_CONTINGENT_ONE_PASS")), ("ON", {})):
        got = _norm(_child(root, extra))
        diff = sum(1 for x, y in zip(base, got, strict=False) if x != y) + abs(len(base) - len(got))
        assert len(base) > 50 and diff == 0, (name, len(base), len(got), next(
            (i for i, (x, y) in enumerate(zip(base, got, strict=False)) if x != y), None))
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")
    out = subprocess.run([sys.executable, "-B", "-c", SAME, root], env=env, capture_output=True,
                         text=True, timeout=900, cwd=root, stdin=subprocess.DEVNULL)
    assert out.returncode == 0, out.stderr[-3000:]
    n = json.loads(out.stdout.strip().splitlines()[-1])
    assert n["calls"] > 0 and n["differ"] == 0, ("occasion or a differing list", n)
    print(f"  OFF and ON (fake): {len(base)} rows against {BASE}, 0 differences each; "
          f"every contingent() call compared both ways: {n}")


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
    print(f"contingent_one_pass: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
