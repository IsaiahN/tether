"""2 ROUTE_NAMED (TETHER_ROUTE_NAMED, default ON; the reviewer 2026-10-30 r392, r393). Minimal
gates (r392): one must-fail, one must-hold, each in its own process.
  check_mustfail_owes   on gridworld after 6 steps, with this cycle's act named, a slot's lookup is
                        owed (route_named) at its first ask and walks at its second; with the arm
                        off no ask is owed for a named act
  check_off_identity    TETHER_ROUTE_NAMED=0 (off_env) against 82308d8, fake, whole-run
    python tests/test_route_named.py [check ...]
"""
from __future__ import annotations

import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
from test_contact_first import _child, _norm  # noqa: E402  the same probe and masks

sys.dont_write_bytecode = True

BASE = "82308d8"        # wip/finish after 1 CONTACT_FIRST


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
    slot = sorted(ag.alphabet)[0]
    ag._rn_owed.clear()
    ag._act_named = ag.cycle
    n0 = len(ag.led.rows())
    first, second = ag._defer_lookup(slot), ag._defer_lookup(slot)
    rows = [r["slot"] for r in ag.led.rows()[n0:] if r["event"] == "route_named"]
    assert first == "named" and second != "named", (first, second)
    assert rows == [slot] and slot in ag.owed_import, rows
    tether._ROUTE_NAMED = False                  # MUST-FAIL: without the arm nothing owes for it
    ag._rn_owed.clear()
    n1 = len(ag.led.rows())
    got = ag._defer_lookup(slot)
    assert got != "named" and not [r for r in ag.led.rows()[n1:]
                                   if r["event"] == "route_named"], got
    print(f"  {slot}: owed (named) then asked ({second!r}); off: {got!r}, no route_named row")


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
    cur = _norm(_child(root, off_env("TETHER_ROUTE_NAMED")))
    diff = sum(1 for x, y in zip(base, cur, strict=False) if x != y) + abs(len(base) - len(cur))
    assert len(base) > 50 and diff == 0, (len(base), len(cur), next(
        (i for i, (x, y) in enumerate(zip(base, cur, strict=False)) if x != y), None))
    print(f"  OFF identity (TETHER_ROUTE_NAMED=0, fake): {len(base)} rows against {BASE}, "
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
    print(f"route_named: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
