"""B1 WHOLE MINTS PER STEP (TETHER_STEP_MINT; the reviewer 2026-10-26 14:20, (b')), on a stepped
gridworld agent.

  (a) 3 MECHANISM slots whose mints each stop at a bound: the step runs 1 and owes 2
      (mint_deferred), and the next step mints an owed slot first;
  (b) with a small closure budget, at most one loop mint per step parks budget_exhausted, and some
      step deferred (occasions);
  (c) MUST-FAIL: OFF, as before -- no mint_deferred, and some step parks two or more exhausted;
  (d) MUST-HOLD: cfg.budget and work_budget 10**9 (nothing exhausts): the normalised ledger is
      identical ON and OFF, row for row, each arm in its own fresh process, hash seed pinned;
  (e) GUARD: every Agent method under @_in_step at ae028d6 still carries the same label.

    python tests/test_step_mint.py [check names]
"""
from __future__ import annotations

import ast
import collections
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
    # one temperament, as check_d's child pins it: the birth seed is OS entropy otherwise, and
    # check_c's occasion moved with it (the reviewer 2026-10-29 r316, r317)
    tether._AGENT_SEED = False
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


def _normalised(rows: list) -> list:
    """The ledger with B1's own record rows and the per-process fields taken out (the reviewer
    2026-10-26 14:35 item 3): row 0 (the header, naming the entry and the arm lists), seq,
    detail.wall_s, the step_mint rows, and completion_sweep's segment_rows (a row count)."""
    out = []
    for r in rows[1:]:
        if r.get("event") == "step_mint":
            continue
        r = {k: v for k, v in r.items() if k != "seq"}
        d = dict(r.get("detail") or {})
        d.pop("wall_s", None)
        if r.get("event") == "completion_sweep":
            d.pop("segment_rows", None)
        r["detail"] = d
        out.append(json.dumps(r, sort_keys=True, default=str))
    return out


def _ledger_rows(on: bool) -> list:
    tether._STEP_MINT = on
    ag = _agent(steps=6, budget=10 ** 9, work_budget=10 ** 9)
    return _normalised(ag.led.rows())


def check_d_must_hold_nothing_exhausts_on_equals_off() -> None:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")

    def run(arm: str) -> list:
        p = subprocess.run([sys.executable, __file__, "--ledger", arm], env=env,
                           capture_output=True, text=True, timeout=240)
        assert p.returncode == 0, (arm, p.returncode, p.stderr[-2000:])
        return json.loads(p.stdout.strip().splitlines()[-1])
    on, off = run("on"), run("off")
    assert len(on) == len(off), (len(on), len(off))
    diff = [i for i, (a, b) in enumerate(zip(on, off, strict=True)) if a != b]
    assert not diff, [(i, on[i][:300], off[i][:300]) for i in diff[:3]]
    assert len(on) > 0, "no rows: vacuous"


def _decorated(src: str) -> dict:
    """{method name: the _in_step label} for every Agent method under @_in_step("...")."""
    out = {}
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.ClassDef) and node.name == "Agent":
            for f in node.body:
                if not isinstance(f, ast.FunctionDef):
                    continue
                for dec in f.decorator_list:
                    if (isinstance(dec, ast.Call) and getattr(dec.func, "id", None) == "_in_step"
                            and dec.args and isinstance(dec.args[0], ast.Constant)):
                        out[f.name] = dec.args[0].value
    return out


def check_e_every_step_scope_decorator_kept() -> None:
    """GUARD (the reviewer 2026-10-26 14:35 item 1): a new method inserted between a decorator and
    its def moves the decorator. Twice today (route at ebd7743, mint at 47972ad). Every method
    decorated with @_in_step at ae028d6 still carries the same label here."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base = subprocess.run(["git", "-C", root, "show", "ae028d6:tether.py"], capture_output=True,
                          text=True, encoding="utf-8", timeout=60)
    assert base.returncode == 0, base.stderr[-500:]
    then = _decorated(base.stdout)
    with open(os.path.join(root, "tether.py"), encoding="utf-8") as fh:
        now = _decorated(fh.read())
    assert then, "no decorated method found at ae028d6: the reader is wrong"
    assert {"mint": "MINT", "route": "ROUTE"}.items() <= then.items(), then
    moved = {k: (v, now.get(k)) for k, v in then.items() if now.get(k) != v}
    assert not moved, moved


def main() -> int:
    if sys.argv[1:2] == ["--ledger"]:
        print(json.dumps(_ledger_rows(sys.argv[2] == "on")))
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
