"""6 INDIST_ON_CHANGE (TETHER_INDIST_ON_CHANGE, default ON; the reviewer 2026-10-30 r400). Minimal
gates: one must-fail, one must-hold, each in its own process.
  check_mustfail_once   on gridworld after 6 steps, with the last grouping cleared, the trigger
                        computes once and returns None at a second read with nothing changed; with
                        the arm off it computes both times
  check_off_identity    MUST-HOLD: TETHER_INDIST_ON_CHANGE=0 (off_env) against afe1a82, fake,
                        whole-run; and ON against OFF on the same run, every row but "indistinct"
                        identical -- no decision moved, pure cost
    python tests/test_indist_on_change.py [check ...]
"""
from __future__ import annotations

import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
from test_contact_first import _child, _norm  # noqa: E402  the same probe and masks

sys.dont_write_bytecode = True

BASE = "afe1a82"        # wip/finish after 5 CARRY_W
# fields that hold a LEDGER POSITION: fewer "indistinct" rows shift them, no decision does (read
# on the fake whole run, 2026-10-30: these four were the only differences, 744 rows)
POSITIONAL = {"choice_tally": ("ref",), "accept": ("seq",), "resolution": ("signal_seq",)}


def _unpos(rows: list) -> list:
    import json
    out = []
    for c, step, slot, ev, d in rows:
        if ev == "indistinct":
            continue
        dd = json.loads(d)
        for k in POSITIONAL.get(ev, ()):
            dd.pop(k, None)
        if ev == "promote" and isinstance(dd.get("shadow"), dict):
            dd["shadow"] = {k: v for k, v in dd["shadow"].items() if k != "recorded_before"}
        out.append((c, step, slot, ev, json.dumps(dd, sort_keys=True)))
    return out


def _twice(on: bool) -> tuple:
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    tether._AGENT_SEED = False
    tether._INDIST_ON_CHANGE = on
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    for _ in range(6):
        ag.step()
    ag._indist_key = None
    return ag.indistinguishable(), ag.indistinguishable()


def check_mustfail_once() -> None:
    a, b = _twice(True)
    assert a is not None and b is None, (a, b)
    a_off, b_off = _twice(False)                 # MUST-FAIL: the arm off computes both times
    assert a_off is not None and b_off is not None and a_off == b_off == a, (a_off, b_off, a)
    print(f"  on: computed once ({len(a)} groups), then None; off: computed twice")


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
    off = _norm(_child(root, off_env("TETHER_INDIST_ON_CHANGE")))
    diff = sum(1 for x, y in zip(base, off, strict=False) if x != y) + abs(len(base) - len(off))
    assert len(base) > 50 and diff == 0, (len(base), len(off), next(
        (i for i, (x, y) in enumerate(zip(base, off, strict=False)) if x != y), None))
    on = _norm(_child(root))
    keep_on, keep_off = _unpos(on), _unpos(off)
    d2 = sum(1 for x, y in zip(keep_on, keep_off, strict=False) if x != y) + abs(
        len(keep_on) - len(keep_off))
    assert d2 == 0, ("ON moved a decision", len(keep_on), len(keep_off), next(
        (i for i, (x, y) in enumerate(zip(keep_on, keep_off, strict=False)) if x != y), None))
    n_on = sum(1 for r in on if r[3] == "indistinct")
    n_off = sum(1 for r in off if r[3] == "indistinct")
    print(f"  OFF identity (TETHER_INDIST_ON_CHANGE=0, fake): {len(base)} rows against {BASE}, 0 "
          f"differences; ON vs OFF: {len(keep_on)} non-indistinct rows identical but for ledger "
          f"positions ({POSITIONAL}, promote.shadow.recorded_before); indistinct rows ON {n_on}, "
          f"OFF {n_off}")


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
    print(f"indist_on_change: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
