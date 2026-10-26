"""THE STEP CLOCK (TETHER_STEP_CLOCK; the reviewer 2026-10-26 r263 (b)): a ledger instrument the
agent never reads, on a stepped gridworld agent with a small closure budget (so mints park at
their bound and B1 defers: the park and step_mint rows have occasions).

  (a) ON: every REPEAT row carries wall_s {scope: s, other, total}, trace_len, wants_n and
      owed_import_n; total covers the scopes; some park row and some step_mint row carry wall_s;
  (b) MUST-FAIL: OFF writes none of these keys on any row;
  (c) the scopes are timed EXCLUSIVELY: a nested scope's time is its own, never its parent's too;
  (d) MUST-HOLD: ON with the new keys dropped equals OFF, row for row, each arm in its own fresh
      process, hash and agent seeds pinned (the arms header dropped; timings masked by
      conform/identity_mod_rows.TIMINGS, imported);
  (e) GUARD: no agent module reads a clock key; only the writers touch the clock's state; a planted
      read is caught (must-fail);
  (f) r264's counts: planted reuse stamps, one on the board and one off, and one non-reuse stamp.

    python tests/test_step_clock.py [check names]
"""
from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
import time

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
import gamma
import gridworld
import ledger
import tether
import world
from conform.identity_mod_rows import mask_timings

sys.dont_write_bytecode = True

NEW = {"repeat": ("wall_s", "trace_len", "wants_n", "owed_import_n", "gamma_reuse_live",
                  "gamma_reuse_on_board"),
       "park": ("wall_s",), "step_mint": ("wall_s",)}
KEYS = {"wall_s", "trace_len", "wants_n", "owed_import_n", "gamma_reuse_live",
        "gamma_reuse_on_board"}
WRITERS = {"_step_scope", "step", "_mint", "_mint_in_step", "_step_body", "_clock_row",
           "_clock_since"}


def _run(on: bool, steps: int = 8) -> list:
    keep = tether._STEP_CLOCK
    try:
        tether._STEP_CLOCK = on
        env = world.bind(gridworld.family("default", 0, 4))
        ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="step_clock_fixture"),
                          tether.Config(budget=40), ledger.Ledger())
        for _ in range(steps):
            ag.step()
        return ag.led.rows()
    finally:
        tether._STEP_CLOCK = keep


def _of(rows: list, event: str) -> list:
    return [r for r in rows if r.get("event") == event]


def check_a_on_rows_carry_the_clock() -> None:
    rows = _run(True)
    rep = _of(rows, "repeat")
    assert rep, "no REPEAT row: vacuous"
    for r in rep:
        d = r["detail"]
        assert all(k in d for k in NEW["repeat"]), sorted(d)
        w = d["wall_s"]
        assert {"other", "total"} <= set(w) and len(w) > 2, w
        parts = sum(v for k, v in w.items() if k != "total")
        assert abs(parts - w["total"]) <= 1e-3 * len(w), w        # rounding only
        assert all(v >= 0 for v in w.values()), w
        assert isinstance(d["trace_len"], int) and isinstance(d["wants_n"], int), d
        assert 0 <= d["gamma_reuse_on_board"] <= d["gamma_reuse_live"], d
    parks = _of(rows, "park")
    assert parks and all("wall_s" in r["detail"] for r in parks), len(parks)
    sm = _of(rows, "step_mint")
    assert sm and all("wall_s" in r["detail"] for r in sm), len(sm)
    print(f"     {len(rep)} REPEAT, {len(parks)} park, {len(sm)} step_mint rows; scopes "
          f"{sorted(set().union(*(r['detail']['wall_s'] for r in rep)) - {'other', 'total'})}")


def check_b_must_fail_off_writes_no_clock_key() -> None:
    rows = _run(False)
    assert _of(rows, "repeat") and _of(rows, "park"), "OFF had no REPEAT or park row: vacuous"
    hit = [(r["event"], k) for r in rows for k in NEW.get(r.get("event"), ())
           if k in (r.get("detail") or {})]
    assert not hit, hit[:5]


def check_c_scopes_are_exclusive() -> None:
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="step_clock_fixture"), tether.Config(),
                      ledger.Ledger())
    keep = tether._STEP_CLOCK
    try:
        tether._STEP_CLOCK = True
        ag._clk, ag._clk_stack, ag._clk_t0 = {}, [], time.perf_counter()
        with ag._step_scope("OUTER_T"):
            time.sleep(0.05)
            with ag._step_scope("INNER_T"):
                time.sleep(0.10)
            time.sleep(0.05)
        out, inn = ag._clk["OUTER_T"], ag._clk["INNER_T"]
        assert 0.09 <= out < 0.15 and 0.09 <= inn < 0.15, (out, inn)   # not 0.2 for the outer
        assert not ag._clk_stack, ag._clk_stack
    finally:
        tether._STEP_CLOCK = keep


def check_f_reuse_counts() -> None:
    """r264: gamma_reuse_live counts stamps whose residual starts reuse:; gamma_reuse_on_board
    counts those whose object ids are all on the current slots."""
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="step_clock_fixture"), tether.Config(),
                      ledger.Ledger())
    ag._clk, ag._clk_stack, ag._clk_t0 = {}, [], time.perf_counter()
    base = ag._clock_row()
    planted = {"t<o90001.row>": "reuse:o90001.row@1:closed",          # on board
               "t<o90001~o90002.bbox>": "reuse:o90001.row@1:partial",  # o90002 not on board
               "t<o90003.row>": "mint:o90003.row"}                     # not a reuse install
    for n, res in planted.items():
        ag.gamma.library[n] = None
        ag.gamma.stamps[n] = {"origin": "minted", "seq": 1, "residual": res, "admitted": None}
    ag.slots = list(ag.slots) + ["o90001.row"]
    got = ag._clock_row()
    assert got["gamma_reuse_live"] - base["gamma_reuse_live"] == 2, (base, got)
    assert got["gamma_reuse_on_board"] - base["gamma_reuse_on_board"] == 1, (base, got)


def _normalised(rows: list) -> tuple:
    out, carried = [], 0
    for r in mask_timings(json.loads(json.dumps(rows[1:], default=str))):
        if r.get("slot") == "@run" and r.get("event") == "arms":
            continue
        d = r.get("detail") or {}
        for k in NEW.get(r.get("event"), ()):
            if k in d:
                carried += 1
                d.pop(k)
        out.append(json.dumps(r, sort_keys=True, default=str))
    return out, carried


def check_d_must_hold_on_minus_new_keys_equals_off() -> None:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")

    def run(arm: str) -> dict:
        p = subprocess.run([sys.executable, __file__, "--ledger", arm], env=env,
                           capture_output=True, text=True, timeout=240)
        assert p.returncode == 0, (arm, p.returncode, p.stderr[-2000:])
        return json.loads(p.stdout.strip().splitlines()[-1])
    on, off = run("on"), run("off")
    assert on["carried"] > 0, "ON carried no clock key: the treatment did not run"
    assert off["carried"] == 0, off["carried"]
    a, b = on["rows"], off["rows"]
    assert len(a) == len(b) and a, (len(a), len(b))
    diff = [i for i, (x, y) in enumerate(zip(a, b, strict=True)) if x != y]
    assert not diff, [(i, a[i][:300], b[i][:300]) for i in diff[:3]]
    print(f"     {len(a)} rows equal; ON carried {on['carried']} clock keys")


def _violations(src: str) -> list:
    """Reads of a clock key (subscript load, .get/.pop/.setdefault) outside WRITERS, and any touch
    of the clock's state (_clk, _clk_stack, _clk_t0, _clk0, _clock_row, _clock_since, _STEP_CLOCK)
    outside WRITERS."""
    bad = []
    state = {"_clk", "_clk_stack", "_clk_t0", "_clk0", "_clock_row", "_clock_since", "_STEP_CLOCK"}

    def visit(node, fn):
        for ch in ast.iter_child_nodes(node):
            f = ch.name if isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef)) else fn
            inside = f in WRITERS
            if (isinstance(ch, ast.Subscript) and isinstance(ch.ctx, ast.Load)
                    and isinstance(ch.slice, ast.Constant) and ch.slice.value in KEYS
                    and not inside):
                bad.append((ch.lineno, f, "reads " + ch.slice.value))
            if (isinstance(ch, ast.Call) and isinstance(ch.func, ast.Attribute)
                    and ch.func.attr in ("get", "pop", "setdefault") and ch.args
                    and isinstance(ch.args[0], ast.Constant) and ch.args[0].value in KEYS
                    and not inside):
                bad.append((ch.lineno, f, f"{ch.func.attr}({ch.args[0].value!r})"))
            name = (ch.attr if isinstance(ch, ast.Attribute)
                    else ch.id if isinstance(ch, ast.Name) else None)
            if name in state and fn is not None and not inside:
                bad.append((ch.lineno, f, "touches " + name))
            visit(ch, f)
    visit(ast.parse(src), None)
    return bad


def _agent_modules() -> list:
    """Every repo module the agent imports (tether's import graph), never tests or conform."""
    root = os.path.normcase(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    out = []
    for m in list(sys.modules.values()):
        f = getattr(m, "__file__", None)
        if not f:
            continue
        f = os.path.normcase(os.path.abspath(f))
        rel = os.path.relpath(f, root)
        if (f.startswith(root) and not rel.startswith(("tests", "conform", ".venv", ".."))
                and f.endswith(".py")):
            out.append(f)
    return sorted(set(out))


def check_e_guard_no_agent_read_and_planted_read_caught() -> None:
    mods = _agent_modules()
    assert any(m.endswith("tether.py") for m in mods), mods
    bad = {}
    for m in mods:
        with open(m, encoding="utf-8") as fh:
            v = _violations(fh.read())
        if v:
            bad[os.path.basename(m)] = v
    assert not bad, bad
    with open(tether.__file__, encoding="utf-8") as fh:
        src = fh.read()
    planted = src.replace("    def _clock_row(self) -> dict:",
                          "    def _planted(self, r):\n        return r['detail']['trace_len']\n\n"
                          "    def _sneak(self):\n        return self._clk\n\n"
                          "    def _clock_row(self) -> dict:", 1)
    assert planted != src, "the plant site is gone: the must-fail is vacuous"
    got = {(f, why) for _ln, f, why in _violations(planted)}
    assert {("_planted", "reads trace_len"), ("_sneak", "touches _clk")} <= got, got
    print(f"     {len(mods)} agent modules clean; planted read and touch caught")


def main() -> int:
    if sys.argv[1:2] == ["--ledger"]:
        rows, carried = _normalised(_run(sys.argv[2] == "on"))
        print(json.dumps({"rows": rows, "carried": carried}))
        return 0
    want = set(sys.argv[1:])
    checks = [v for k, v in globals().items() if k.startswith("check_")
              and (not want or k in want)]
    assert not want or len(checks) == len(want), ("unknown check name", sorted(want))
    for c in checks:
        c()
        print("ok  ", c.__name__)
    print(f"test_step_clock: {len(checks)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
