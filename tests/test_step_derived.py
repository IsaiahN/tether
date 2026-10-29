"""B2 ONE STOP PER STEP FOR EVERY MINT KIND (TETHER_STEP_DERIVED; the reviewer 2026-10-26 r270), on
a stepped gridworld agent (its pair slots are declared derived).

  (a) with a small closure budget: no step runs two derived mints that stop at their bound, and some
      step defers derived asks after one (occasions);
  (b) a step whose ACCEPT loop already stopped at a bound runs no derived mint: every derived ask
      that would mint is owed (occasions);
  (c) MUST-FAIL: OFF, as before -- no derived_deferred row, and some step runs two or more derived
      mints that stop at their bound;
  (d) MUST-HOLD: cfg.budget and work_budget 10**9 (nothing exhausts): the normalised ledger is
      identical ON and OFF, row for row, each arm in its own fresh process, hash seed pinned;
  (e) the next step asks an owed derived slot before any fresh one (owed_since rows first);
  (f) an owed slot's transition is not in _dw_tried while it is owed, and is once its mint runs.

    python tests/test_step_derived.py [check names]
"""
from __future__ import annotations

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
from conform.identity_mod_rows import mask_timings

sys.dont_write_bytecode = True
STEPS = 8


def _agent(**cfg) -> tether.Agent:
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="step_derived_fixture"),
                      tether.Config(**cfg), ledger.Ledger())
    # gridworld's derived asks are all echoes (a source missed), which never mint; bp35's were not.
    # No source missed, so each derived ask mints, as on bp35 (both arms, every check)
    ag._ds_echo = lambda _d: []
    return ag


def _derived_exhausting(rows: list) -> dict:
    """Per cycle: the derived asks whose want-only mint parked stopped at a bound."""
    asked = collections.defaultdict(set)
    out = collections.defaultdict(list)
    for r in rows:
        e, d = r.get("event"), r.get("detail") or {}
        if e == "derived_asked":
            asked[r["cycle"]].add(r["slot"])
        elif e == "park" and d.get("budget_exhausted") and r["slot"] in asked[r["cycle"]]:
            out[r["cycle"]].append(r["slot"])
    return out


def _run(on: bool, steps: int = STEPS, probe=None, **cfg) -> tether.Agent:
    keep = tether._STEP_DERIVED
    try:
        tether._STEP_DERIVED = on
        ag = _agent(**cfg)
        for _ in range(steps):
            ag.step()
            if probe is not None:
                probe(ag)
        return ag
    finally:
        tether._STEP_DERIVED = keep


def _of(rows: list, event: str) -> list:
    return [r for r in rows if r.get("event") == event]


def check_a_at_most_one_exhausting_derived_mint_per_step() -> None:
    rows = _run(True, budget=40).led.rows()
    ex = _derived_exhausting(rows)
    assert all(len(s) <= 1 for s in ex.values()), dict(ex)
    dfr = _of(rows, "derived_deferred")
    assert dfr, ("no derived ask was deferred: vacuous", dict(ex))
    print(f"     {len(dfr)} derived_deferred rows; exhausting derived mints per step "
          f"{sorted((c, len(s)) for c, s in ex.items())}")


def check_b_accept_stop_owes_every_derived_ask() -> None:
    rows = _run(True, budget=40).led.rows()
    sd = [r["detail"] for r in _of(rows, "step_derived") if r["detail"].get("stop_from_accept")]
    hits = [d for d in sd if d["derived_deferred"]]
    assert hits, ("no step with an ACCEPT stop deferred a derived ask: vacuous", sd)
    assert all(d["derived_run"] == 0 for d in sd), sd
    print(f"     {len(sd)} steps with an ACCEPT stop; derived run 0 in each; deferred "
          f"{[d['derived_deferred'] for d in sd]}")


def check_c_must_fail_off_runs_every_derived_mint() -> None:
    rows = _run(False, budget=40).led.rows()
    assert not _of(rows, "derived_deferred") and not _of(rows, "step_derived")
    ex = _derived_exhausting(rows)
    assert any(len(s) >= 2 for s in ex.values()), ("OFF never exhausted twice in a step", dict(ex))


def _normalised(rows: list) -> list:
    """B2's own rows and the per-process fields out: row 0 (the header), seq, the TIMINGS
    (imported), step_mint and step_derived rows, completion_sweep's segment_rows."""
    out = []
    for r in mask_timings(json.loads(json.dumps(rows[1:], default=str))):
        if r.get("event") in ("step_mint", "step_derived"):
            continue
        r.pop("seq", None)
        d = r.get("detail") or {}
        d.pop("wall_s", None)
        if r.get("event") == "completion_sweep":
            d.pop("segment_rows", None)
        out.append(json.dumps(r, sort_keys=True, default=str))
    return out


def check_d_must_hold_nothing_exhausts_on_equals_off() -> None:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0")

    def run(arm: str) -> dict:
        p = subprocess.run([sys.executable, __file__, "--ledger", arm], env=env,
                           capture_output=True, text=True, timeout=240)
        assert p.returncode == 0, (arm, p.returncode, p.stderr[-2000:])
        return json.loads(p.stdout.strip().splitlines()[-1])
    on, off = run("on"), run("off")
    assert on["asked"] > 0, "no derived ask ran: vacuous"
    assert on["deferred"] == 0 == off["deferred"], (on["deferred"], off["deferred"])
    a, b = on["rows"], off["rows"]
    assert len(a) == len(b) and a, (len(a), len(b))
    diff = [i for i, (x, y) in enumerate(zip(a, b, strict=True)) if x != y]
    assert not diff, [(i, a[i][:300], b[i][:300]) for i in diff[:3]]
    print(f"     {len(a)} rows equal; {on['asked']} derived asks")


def check_e_owed_derived_slot_asked_first_next_step() -> None:
    """OFF path: owed first, 1d OFF (TETHER_OWED_REJUDGE=0). ON, owed and fresh asks go by
    A1: test_owed_rejudge check_i_on_derived_a1_order."""
    keep = tether._OWED_REJUDGE
    tether._OWED_REJUDGE = False     # B2's owed-first order; 1d (r281) replaces it by A1
    try:
        rows = _run(True, budget=40).led.rows()
    finally:
        tether._OWED_REJUDGE = keep
    dfr = {(r["cycle"], r["slot"]) for r in _of(rows, "derived_deferred")}
    by_c = collections.defaultdict(list)
    for r in _of(rows, "derived_asked"):
        by_c[r["cycle"]].append("owed_since" in (r.get("detail") or {}))
    for c, flags in by_c.items():
        assert flags == sorted(flags, reverse=True), (c, flags)     # owed asks before fresh ones
    owed_asked = sum(sum(f) for f in by_c.values())
    dropped = sum(r["detail"]["owed_dropped"] for r in _of(rows, "step_derived"))
    assert owed_asked > 0, ("no owed derived ask was asked: vacuous", len(dfr), dropped)
    print(f"     {owed_asked} owed asks asked first; {dropped} owed dropped (no longer due)")


def check_f_owed_transition_not_tried_until_minted() -> None:
    seen = {"owed": 0, "minted": 0}
    prev: dict = {}

    def probe(ag: tether.Agent) -> None:
        for d, (_c0, t) in ag._dw_owed.items():
            assert t not in ag._dw_tried.get(d, set()), (d, t)
            seen["owed"] += 1
        last = [r for r in ag.led.rows() if r.get("cycle") == ag.cycle - 1]
        asked_owed = {r["slot"] for r in last if r.get("event") == "derived_asked"
                      and "owed_since" in (r.get("detail") or {})}
        # 1d (TETHER_OWED_REJUDGE): an owed ask whose slot moved again carries the newer transition
        now = {r["slot"]: tuple(r["detail"]["now"]) for r in last
               if r.get("event") == "owed_superseded"}
        for d, (_c0, t) in prev.items():
            t = now.get(d, t)
            if d in asked_owed and d not in ag._dw_owed:
                assert t in ag._dw_tried.get(d, set()), (d, t)       # tried once its mint ran
                seen["minted"] += 1
        prev.clear()
        prev.update(ag._dw_owed)
    _run(True, budget=40, probe=probe)
    assert seen["owed"] and seen["minted"], ("no owed slot, or none minted: vacuous", seen)
    print(f"     owed transitions held out of tried {seen['owed']} times; {seen['minted']} "
          "minted and then tried")


def main() -> int:
    if sys.argv[1:2] == ["--ledger"]:
        ag = _run(sys.argv[2] == "on", budget=10 ** 9, work_budget=10 ** 9)
        rows = ag.led.rows()
        print(json.dumps({"rows": _normalised(rows), "asked": len(_of(rows, "derived_asked")),
                          "deferred": len(_of(rows, "derived_deferred"))}))
        return 0
    want = set(sys.argv[1:])
    checks = [v for k, v in globals().items() if k.startswith("check_")
              and (not want or k in want)]
    assert not want or len(checks) == len(want), ("unknown check name", sorted(want))
    for c in checks:
        c()
        print("ok  ", c.__name__)
    print(f"test_step_derived: {len(checks)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
