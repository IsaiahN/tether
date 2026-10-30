"""5 CARRY_W (TETHER_CARRY_W, default ON; the reviewer 2026-10-30 r392, r397). Minimal gates
(r392): one must-fail, one must-hold, each in its own process.
  check_mustfail_mixes  a stub carried LEARNED term (inc.dbl) reads today's track_of before any
                        outcome; after one settle and one refusal its kind's w is 0.5 and its
                        track_of is 0.5 * Laplace(as loaded) + 0.5 * Laplace(this life); the arm
                        off reads today's formula and logs nothing
  check_off_identity    TETHER_CARRY_W=0 (off_env) against 10cbfae, fake, whole-run
    python tests/test_carry_w.py [check ...]
"""
from __future__ import annotations

import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
from test_contact_first import _child, _norm  # noqa: E402  the same probe and masks

sys.dont_write_bytecode = True

BASE = "10cbfae"        # wip/finish after 4 UNTESTED_KEEP


def _run(on: bool) -> tuple:
    import gamma
    import gridworld
    import world
    gamma._CARRY_W = on
    env = world.bind(gridworld.family("default", 0))
    g = gamma.Gamma(env.atoms(), game="g")
    at = {a.name: a for a in g.atoms}
    t = gamma.Term((at["inc"], at["dbl"]))
    g._install(t, seq=0, residual=None)
    g.carried[t.name] = {"from": "earlier", "handle": None}
    g.learn(t.name)
    g.replay([["settle", t.name, None, None, g.tick]] * 3)   # carried evidence, not this life's
    st = g.standing[t.name]
    base = (st.confirmations, st.refusals)
    before = g.track_of(t.name)
    g.settle(t.name)
    g.refute(t.name)                              # settled, so a refusal
    after = g.track_of(t.name)
    st = g.standing[t.name]
    today = (st.confirmations + 1.0) / (st.confirmations + st.refusals + 2.0)
    return base, before, after, today, list(g.carry_w_log)


def check_mustfail_mixes() -> None:
    base, before, after, today, log = _run(True)
    c0, r0 = base
    lap0 = (c0 + 1.0) / (c0 + r0 + 2.0)
    assert before == lap0, ("at birth: today's track_of", before, lap0)
    want = 0.5 * lap0 + 0.5 * (1.0 + 1.0) / (1.0 + 1.0 + 2.0)
    assert abs(after - want) < 1e-12, (after, want)
    assert [x[1:] for x in log] == [(1, 0, 1.0), (1, 1, 0.5)], log
    _b, before_off, after_off, today_off, log_off = _run(False)   # MUST-FAIL: off, today's formula
    assert before_off == before and after_off == today_off and not log_off, (after_off, today_off)
    assert after != after_off, ("MUST-FAIL: the arm must move the carried term's track", after)
    print(f"  carried inc.dbl: at birth {before:.6f} (today's); after 1 held + 1 failed, w 0.5, "
          f"track {after:.6f}; off {after_off:.6f}; carry_w log {[x[1:] for x in log]}")


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
    cur = _norm(_child(root, off_env("TETHER_CARRY_W")))
    diff = sum(1 for x, y in zip(base, cur, strict=False) if x != y) + abs(len(base) - len(cur))
    assert len(base) > 50 and diff == 0, (len(base), len(cur), next(
        (i for i, (x, y) in enumerate(zip(base, cur, strict=False)) if x != y), None))
    print(f"  OFF identity (TETHER_CARRY_W=0, fake): {len(base)} rows against {BASE}, "
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
    print(f"carry_w: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
