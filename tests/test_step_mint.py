"""B1 WHOLE MINTS PER STEP (TETHER_STEP_MINT; the reviewer 2026-10-26 14:20, (b')), on a stepped
gridworld agent.

  (a) 3 MECHANISM slots whose mints each stop at a bound: the step runs 1 and owes 2
      (mint_deferred), and the next step mints an owed slot first;
  (b) with a small closure budget, at most one loop mint per step parks budget_exhausted, and some
      step deferred (occasions);
  (c) MUST-FAIL: OFF, as before -- no mint_deferred, and some step parks two or more exhausted;
  (d) MUST-HOLD: cfg.budget and work_budget 10**9 (nothing exhausts): the ledger is byte-identical
      ON and OFF, each arm in its own fresh process, hash seed pinned.

    python tests/test_step_mint.py [check names]
"""
from __future__ import annotations

import collections
import hashlib
import json
import os
import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
import gamma
import gridworld
import ledger
import tether
import world

sys.dont_write_bytecode = True


def _agent(steps: int = 3, **cfg) -> tether.Agent:
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="step_mint_fixture"),
                      tether.Config(**cfg), ledger.Ledger())
    for _ in range(steps):
        ag.step()
    return ag


def _rows(ag: tether.Agent, n0: int, event: str) -> list:
    return [r for r in ag.led.rows()[n0:] if r.get("event") == event]


def check_a_one_exhausting_mint_then_owed_first() -> None:
    ag = _agent()
    three = [s for s in sorted(ag.slots) if s not in getattr(ag, "_own_now", ())][:3]
    assert len(three) == 3, three
    calls: list = []

    def fake_mint(slot):
        calls.append((ag.cycle, slot))
        ag._mint_exhausted = True                  # every mint stops at its bound
    ag.mint = fake_mint
    ag.route = lambda _res: [(s, tether.MECHANISM, None, "test") for s in three]
    keep = tether._STEP_MINT
    try:
        tether._STEP_MINT = True
        c0, n0 = ag.cycle, len(ag.led.rows())
        ag.step()
        first = [s for c, s in calls if c == c0 and s in three]
        assert first == [three[0]], first                       # one mint ran
        dfr = [r["slot"] for r in _rows(ag, n0, "mint_deferred")]
        assert dfr == three[1:], dfr                            # two owed
        assert all(s in ag.owed_import for s in three[1:]), three
        sm = _rows(ag, n0, "step_mint")
        d = sm[-1]["detail"] if sm else {}
        assert (d.get("mints_run"), d.get("mints_deferred"), d.get("stop")) == (1, 2, three[0]), sm
        c1 = ag.cycle
        ag.step()
        second = [s for c, s in calls if c == c1 and s in three]
        assert second and second[0] in three[1:], second      # an owed slot is minted first
    finally:
        tether._STEP_MINT = keep


def _loop_exhausted(ag: tether.Agent, n0: int) -> dict:
    """Per cycle: the slots whose park (outside the derived-want asks) stopped at a bound."""
    asked = collections.defaultdict(set)
    ex = collections.defaultdict(set)
    for r in ag.led.rows()[n0:]:
        e, d = r.get("event"), r.get("detail") or {}
        if e == "derived_asked":
            asked[r["cycle"]].add(r["slot"])
        elif e == "park" and d.get("budget_exhausted"):
            ex[r["cycle"]].add(r["slot"])
    return {c: s - asked[c] for c, s in ex.items()}


def _small_budget_run(on: bool) -> tuple:
    keep = tether._STEP_MINT
    try:
        tether._STEP_MINT = on
        ag = _agent(steps=0, budget=40)
        n0 = len(ag.led.rows())
        for _ in range(8):
            ag.step()
        return _loop_exhausted(ag, n0), len(_rows(ag, n0, "mint_deferred"))
    finally:
        tether._STEP_MINT = keep


def check_b_at_most_one_exhausting_loop_mint_per_step() -> None:
    ex, deferred = _small_budget_run(True)
    assert all(len(s) <= 1 for s in ex.values()), ex
    assert deferred >= 1, ("no step deferred a mint: vacuous", ex)


def check_c_must_fail_off_runs_every_mint() -> None:
    ex, deferred = _small_budget_run(False)
    assert deferred == 0, deferred
    assert any(len(s) >= 2 for s in ex.values()), ("OFF never exhausted twice in a step", ex)


def _ledger_sha(on: bool) -> str:
    tether._STEP_MINT = on
    ag = _agent(steps=6, budget=10 ** 9, work_budget=10 ** 9)
    rows = json.dumps(ag.led.rows(), sort_keys=True, default=str)
    return f"{hashlib.sha256(rows.encode('utf-8')).hexdigest()} {len(ag.led.rows())}"


def check_d_must_hold_nothing_exhausts_on_equals_off() -> None:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")

    def run(arm: str) -> str:
        p = subprocess.run([sys.executable, __file__, "--ledger", arm], env=env,
                           capture_output=True, text=True, timeout=240)
        assert p.returncode == 0, (arm, p.returncode, p.stderr[-2000:])
        return p.stdout.strip().splitlines()[-1]
    on, off = run("on"), run("off")
    assert on == off, (on, off)
    assert int(on.split()[1]) > 0, on


def main() -> int:
    if sys.argv[1:2] == ["--ledger"]:
        print(_ledger_sha(sys.argv[2] == "on"))
        return 0
    want = set(sys.argv[1:])
    checks = [v for k, v in globals().items() if k.startswith("check_")
              and (not want or k in want)]
    assert not want or len(checks) == len(want), ("unknown check name", sorted(want))
    for c in checks:
        c()
        print("ok  ", c.__name__)
    print(f"test_step_mint: {len(checks)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
