"""(b'-l) PHASE 1, THE LINEAGE HOLD (the reviewer 2026-10-14 16:29, 16:34, 16:38, 16:43, 17:02,
17:06). Real Agents through __init__ on the fake ARC world; the arm is set in the ENVIRONMENT of a
child process at start (never toggled at runtime). Child 1: the arm alone. Child 2 (given --env
FILE): every TETHER_ line of FILE plus the arm -- the flipped ARC state. Each prints its header.

  RL-1   nothing deleted: every store, the trace included, each copied by its own type, is in
         _dormant after the boundary, at an ADVANCE and at a DEATH; not_carried entries stay.
  RL-2   no slot-name reach: after an ADVANCE the live stores start empty. (That nothing outside
         _carry_lineage reads _dormant is a code read.)
  RL-2b  REGRESSION GUARD, not a new reach: paths (the _gap_key form) already survives an advance
         at HEAD (2026-2032); the arm must not break it. New reach-by-kind is phase 2's.
  RL-3   runner parity: play() (an injected arc) and tether_agent.run on the same fake world
         write the same restart_lineage row, and at least one count in it is > 0.
  RL-4   colour kind only: the attempt row names no slot (a colour value cannot enter its two
         fields by construction: action names and str(_gap_key) -- a code read).
  RL-5   per-entry refusal rows exist at HEAD (3259) and are unchanged; the arm adds one count
         row per store at every boundary. MUST-FAIL: HEAD writes no boundary count rows.
  RL-6   one attempt row per boundary, with the ending and no "refuted" anywhere in it.
  A2     the trace is dormant (a list) and is not carried.
  A3     actions_tried is read from THIS attempt's own trace: after a carry, an attempt that
         tries nothing reports it empty, and one that re-tries a carried action reports it.
  F2     carried VALUES land: a sure object's reach_tested entry with its value, the
         object-free want, and the sure-object Drive pair are back after the restart.
  TWIN   an ambiguous twin's entries are not carried and stay dormant.
  C3     a pair-keyed refutation (o_a~o_b) with one twin is not carried under the arm.
RL-0 (arm OFF, ledgers identical to HEAD) is a lane, not this fixture.

    python test_lineage_hold.py [--env FILE]
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from arcengine import GameState  # noqa: E402

import arc_holdout  # noqa: E402
import gamma  # noqa: E402
import tether  # noqa: E402
import tether_agent  # noqa: E402
from test_entry import FakeWrapper, TwinWrapper  # noqa: E402

MOVES = ["ACTION2", "ACTION2", "ACTION4", "ACTION4", "ACTION4"]
KIND = (("KIND",), (), ())


def _seed(env, ag):
    """Every store non-empty: one entry per tracked object, one object-free want, a trace step."""
    objs = sorted(env._decompose.tracked)
    for o in objs:
        k, s = (f"{o}.row", (), ()), f"{o}.row"
        ag.refuted[k], ag.refuted_at[k] = gamma.Standing(last_tick=0), 1.0
        ag._reach_tested[k] = "tested_no"
        ag.wants[s], ag._want_terms[s] = "t", None
        ag._undone[(("ctx",), "said", s, 1.0)] = 1
        ag._undone_across[("said", s)] = 1
        ag._prev_gap[s], ag._gap_delta[s] = 1, 0
        ag._refuted_slot[s] = "t"
        # the real shapes: a cut is (*_d5_cut, incumbent) (tether 9935), read as c[0] and c[2] by
        # _d5_level_end; a split is {"P", "A", "B"} (tether 5407)
        ag._d5_candidates[s] = ag._d5_pending[s] = ("P", "Q", "t")
        ag._parts[s] = {"P": "P", "A": "t", "B": "u"}
    ag.trace.append(({}, "ACTION2", {}))
    ag.drive.tried.setdefault("ACTION2", set()).add(tuple((f"{o}.row", 1) for o in objs))
    ag.wants["board"] = "t"           # names no object: carried vacuously (restarted's rule)
    ag.paths[KIND] = {"failed": 1, "first_cycle": 0, "last_cycle": ag.cycle}
    return objs


def _sizes(ag):
    s = {nm: len(getattr(ag, at)) for nm, at in tether._LINEAGE_STORES}
    s["drive_tried"] = len(ag.drive.tried)
    return s


def _boundary(w, how, moves=MOVES):
    env, ag = arc_holdout.wire(w, "fake")[:2]
    for a in moves:
        env.step(a)
    objs = _seed(env, ag)
    before = _sizes(ag)
    assert all(before.values()), ("fixture: a store was not seeded", before)
    ag.retarget(env, env.levels()[0], how=how)
    return env, ag, objs, before


def _header(ag):
    h = next(e.detail for e in ag.led.by_event("arms") if e.slot == "@run")
    on = [f for f in h["on"] if f.endswith(("._LINEAGE_HOLD", "._RELATION_SET"))]
    return (f"env {os.environ.get('LINEAGE_ENV')}; header on {len(h['on'])} "
            f"off {len(h['off'])}; {on}")


def on_checks():
    assert tether._LINEAGE_HOLD, "the child must be started with TETHER_LINEAGE_HOLD=1"
    # ADVANCE: RL-1 (types, trace), RL-5, RL-6, RL-4, RL-2, RL-2b.
    env, ag, objs, before = _boundary(FakeWrapper(), "level_advance")
    print(f"  HEADER: {_header(ag)}", flush=True)
    rec = ag._dormant[-1]
    for nm, at in tether._LINEAGE_STORES:
        assert type(rec["stores"][nm]) is type(getattr(ag, at)), ("RL-1 type", nm)
    for nm, n in before.items():
        assert len(rec["stores"][nm]) == n, ("RL-1", nm, n, len(rec["stores"][nm]))
    rows = [e.detail for e in ag.led.entries if e.event == "dormant"]
    assert {r["store"]: r["count"] for r in rows} == before, ("RL-5", rows)
    att = [e.detail for e in ag.led.entries if e.event == "attempt_end"]
    assert len(att) == 1 and att[0]["ending"] == "level_advance", ("RL-6", att)
    assert "refuted" not in repr(att[0]), ("RL-6 a verdict in the attempt row", att[0])
    named = repr(att[0]["actions_tried"]) + repr(att[0]["gap_kinds"])
    assert not any(o in named for o in objs), ("RL-4 a slot name in the attempt row", att[0])
    assert not ag._reach_tested and not ag.wants and not ag.trace, "RL-2 a store crossed by name"
    assert KIND in ag.paths and str(KIND[0]) in att[0]["gap_kinds"], (
        "RL-2b the kind form did not cross", att[0]["gap_kinds"])
    print(f"  ADVANCE: {len(before)} stores dormant by type; counts {before}", flush=True)
    # DEATH + same-level restart: RL-1 death clause, A2, F2, A3.
    env, ag, objs, before = _boundary(FakeWrapper(), "death")
    env.step("RESET")
    ag.restarted(env)
    row = [e.detail for e in ag.led.entries if e.event == "restart_lineage"]
    assert row and sum(row[-1]["carried"].values()) > 0, ("carry exercised", row)
    assert all(len(ag._dormant[-1]["stores"][nm]) == n for nm, n in before.items()), "RL-1 death"
    assert ({}, "ACTION2", {}) not in ag.trace and ag._dormant[-1]["stores"]["trace"], "A2 trace"
    sure = [o for o in objs if env.identity(o) in ("overlap", "unique-shape")]
    assert sure, ("fixture: no sure object", {o: env.identity(o) for o in objs})
    assert ag._reach_tested.get((f"{sure[0]}.row", (), ())) == "tested_no", "F2 reach_tested"
    assert ag.wants.get("board") == "t", "F2 the object-free want"
    pair = tuple((f"{o}.row", 1) for o in objs)
    all_sure = set(objs) <= set(sure)
    back = pair in ag.drive.tried.get("ACTION2", set())
    assert back == all_sure, ("F2 the Drive pair", all_sure, back)
    print(f"  RESTART: carried {row[-1]['carried']} / not {row[-1]['not_carried']}", flush=True)
    ag.retarget(env, env.levels()[0], how="death")      # A3: nothing new tried since the carry
    att = [e.detail for e in ag.led.entries if e.event == "attempt_end"]
    assert att[-1]["actions_tried"] == [], ("A3 carried actions counted as tried", att[-1])
    # A3 the re-try: after a carry, the attempt takes a carried action AGAIN (a trace step, as the
    # step loop writes at tether 4418) -> it is counted as tried.
    env, ag, objs, before = _boundary(FakeWrapper(), "death")
    env.step("RESET")
    ag.restarted(env)
    assert "ACTION2" in ag.drive.tried, ("fixture: the carried pair is not back", ag.drive.tried)
    ag.trace.append(({}, "ACTION2", {}, None, None))
    ag.retarget(env, env.levels()[0], how="death")
    att = [e.detail for e in ag.led.entries if e.event == "attempt_end"]
    assert att[-1]["actions_tried"] == ["ACTION2"], ("A3 a re-try was not counted", att[-1])
    # TWIN + C3. The twins read "look-alike" only once a RESET has re-found them by shape
    # (test_entry 172-186, 201-202), so every ordered pair gets a pair-keyed refutation BEFORE the
    # boundary and the twins are read AFTER the restart.
    env, ag = arc_holdout.wire(TwinWrapper(), "fake")[:2]
    for a in ["ACTION4"] * 4:
        env.step(a)
    objs = _seed(env, ag)
    for a in objs:
        for b in objs:
            if a != b:
                pk = (f"{a}~{b}.bbox", (), ())
                ag.refuted[pk], ag.refuted_at[pk] = gamma.Standing(last_tick=0), 1.0
    ag.retarget(env, env.levels()[0], how="death")
    env.step("RESET")
    ag.restarted(env)
    twins = sorted(o for o in env._decompose.tracked if env.identity(o) == "look-alike")
    others = [o for o in objs if o not in twins]
    assert len(twins) == 2 and set(twins) <= set(objs) and others, (
        "fixture: twins and a third object", twins, objs)
    pk = (f"{others[0]}~{twins[0]}.bbox", (), ())
    named = tether.Agent._objs_named      # the carry's own rule: exact objects, never a substring
    assert not any(t in named(k) for t in twins for k in ag._reach_tested), "TWIN carried"
    assert any(t in named(k) for t in twins for k in ag._dormant[-1]["stores"]["reach_tested"]), (
        "TWIN dropped from the dormant record")
    assert pk not in ag.refuted, ("C3 a pair-keyed refutation with a twin was carried", pk)
    print(f"  TWIN {twins} and C3 {pk[0]}: not carried, still dormant", flush=True)
    # RL-3 runner parity, non-vacuous (F1).
    a, b = _restart_row(_by_tether_agent), _restart_row(_by_play)
    assert a is not None and b is not None, ("RL-3 unexercised: no death in the run", a, b)
    assert sum(sum(r.values()) for r in (a["carried"], a["not_carried"])) > 0, ("RL-3 vacuous", a)
    assert a == b, ("RL-3", a, b)
    print(f"  RL-3 parity: {a}", flush=True)


# The record's own death case (test_entry 119-126): GAME_OVER at the second action, 8 actions.
DEATH = {2: GameState.GAME_OVER}


def _by_tether_agent():
    tether_agent.run(FakeWrapper(script=DEATH), "fake", 8)


def _by_play():
    class Arc:
        def make(self, _game):
            return FakeWrapper(script=DEATH)
    arc_holdout.play("fake", 8, arc=Arc())


def _restart_row(drive):
    rows = []
    real = tether.Agent.restarted

    def spy(self, env):
        real(self, env)
        rows.extend(e.detail for e in self.led.entries if e.event == "restart_lineage")
    tether.Agent.restarted = spy
    try:
        drive()
    finally:
        tether.Agent.restarted = real
    return {k: rows[0][k] for k in ("carried", "not_carried")} if rows else None


def _child(extra: dict, label: str) -> None:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(extra, TETHER_LINEAGE_HOLD="1", LINEAGE_ENV=label)
    r = subprocess.run([sys.executable, "-B", __file__, "--on"], cwd=os.getcwd(), env=env,
                       stdin=subprocess.DEVNULL, capture_output=True, text=True, check=False)
    sys.stdout.write(r.stdout)
    assert r.returncode == 0, f"--on ({label}) failed:\n{r.stderr[-3000:]}"


def main():
    _child({}, "the arm alone")
    if "--env" in sys.argv:
        path = sys.argv[sys.argv.index("--env") + 1]
        lines = Path(path).read_text(encoding="utf-8").splitlines()
        extra = dict(ln.strip().split("=", 1) for ln in lines
                     if ln.strip().startswith("TETHER_") and "=" in ln)
        _child(extra, path)
    print("lineage hold: OK")


if __name__ == "__main__":
    (on_checks if "--on" in sys.argv else main)()
