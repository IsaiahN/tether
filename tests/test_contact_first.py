"""1 CONTACT_FIRST (TETHER_CONTACT_FIRST, default ON; the reviewer 2026-10-30 r392, r393). Minimal
gates (r392): one must-fail, one must-hold, each in its own process.
  check_mustfail_owes   on gridworld after 6 steps, a slot walked once is owed (same_rows) at a
                        second ask with no new row, and a named act owes an unwalked slot for this
                        step only; with the arm off every ask walks
  check_off_identity    TETHER_CONTACT_FIRST=0 (off_env) against 9133034, fake, whole-run
    python tests/test_contact_first.py [check ...]
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

BASE = "9133034"        # general-agent, the tree before wip/finish

PROBE = r'''
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


def _child(tree: str, extra: dict | None = None) -> list:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               **(extra or {}))
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, tree], env=env,
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


def check_mustfail_owes() -> None:
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    tether._AGENT_SEED = False
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    for _ in range(6):
        ag.step()
    s1, s2 = sorted(ag.alphabet)[:2]
    calls = []
    ag.mint = calls.append
    ag._sm, ag._act_named = None, None
    ag._cf_rows.clear()                           # the 6 steps' own walks are not this occasion
    ag._cf_owed.clear()
    n0 = len(ag.led.rows())                       # rows the 6 real steps wrote are not counted
    real = sum(1 for r in ag.led.rows() if r["event"] == "contact_first")
    ag._mint_in_step(s1, tether.MECHANISM)       # walked: its rows are kept
    ag._mint_in_step(s1, tether.MECHANISM)       # the same rows: owed
    ag._act_named = ag.cycle
    ag._mint_in_step(s2, tether.MECHANISM)       # a named act: owed for this step
    ag._mint_in_step(s2, tether.MECHANISM)       # already owed for it: walks
    rows = [(r["slot"], r["detail"]["why"]) for r in ag.led.rows()[n0:]
            if r["event"] == "contact_first"]
    assert calls == [s1, s2], calls
    assert rows == [(s1, "same_rows"), (s2, "named")], rows
    assert s1 in ag.owed_import and s2 in ag.owed_import
    tether._CONTACT_FIRST = False                # MUST-FAIL: without the arm every ask walks
    calls.clear()
    for s in (s1, s1, s2, s2):
        ag._mint_in_step(s, tether.MECHANISM)
    assert calls == [s1, s1, s2, s2], ("MUST-FAIL: the arm off walks every ask", calls)
    print(f"  {s1}: walked then owed (same_rows); {s2}: owed (named) then walked; off: 4 walks; "
          f"the 6 real steps wrote {real} contact_first rows of their own")


def check_off_identity() -> None:
    root = str(_repo.ROOT)
    with tempfile.TemporaryDirectory() as d:
        tar = subprocess.run(["git", "-C", root, "archive", BASE], capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(d, filter="data")
        base = _norm(_child(d))
    cur = _norm(_child(root, off_env("TETHER_CONTACT_FIRST")))
    diff = sum(1 for x, y in zip(base, cur, strict=False) if x != y) + abs(len(base) - len(cur))
    assert len(base) > 50 and diff == 0, (len(base), len(cur), next(
        (i for i, (x, y) in enumerate(zip(base, cur, strict=False)) if x != y), None))
    print(f"  OFF identity (TETHER_CONTACT_FIRST=0, fake): {len(base)} rows against {BASE}, "
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
    print(f"contact_first: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
