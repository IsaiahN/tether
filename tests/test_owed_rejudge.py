"""1d OWED_REJUDGE (TETHER_OWED_REJUDGE, default ON; the reviewer 2026-10-28 r281, 2026-10-29 r326
Option A, r333). On B2's fixture: gridworld default seed 0 size 4, closure budget 40, echoes off,
birth seed pinned. Each check runs in its own process, under 5 minutes.
  check_a_sources_explained       an owed ask whose sources all carry no outstanding is released,
                                  "sources explained", and is not owed after
  check_a_mustfail_r281_guard     MUST-FAIL: r281's literal guard (the derived slot's OWN
                                  outstanding, 0 by construction) releases EVERY owed ask on its
                                  first re-judgment; the real guard releases none on the same frame
  check_b_newer_evidence          every owed_superseded row's newer transition is the one carried
                                  (or asked) that step, and was not already tried
  check_c_rank_first              the first mint of a step goes to the top of mint_rank where rank
                                  and code order differ
  check_c_mustfail_code_order     MUST-FAIL: _rank_mints as the identity (code order): the first
                                  mint of that step is code order's first
  check_d_mustfail_off            MUST-FAIL: OFF, the same explained frame releases nothing
  check_f_reraised                a released ask is raised again by a later frame's evidence
  check_g_tried_never_shrinks     no asked transition leaves the tried set across a step (r334)
  check_g_mustfail_prefix_supersede   MUST-FAIL: the supersede before its fix (carry the newest
                                  transition, tried or not) reopens settled transitions
  check_h_on_first_mint_by_rank   ON sibling of test_step_mint check_a: the next step's first mint
                                  is the top of mint_rank, ranks descending
  check_i_on_derived_a1_order     ON sibling of test_step_derived check_e: owed and fresh asks by
                                  A1 (fewer asks first, then draw_order "<cycle>:derived")
  check_tie_plain_first           r333: every plain candidate at rank 0 with derived asks pending:
                                  the plain mint takes the step's search, the derived asks are owed
                                  after it
  check_tie_control               the same, the plain mints skipped: the derived asks run
  check_off_identity_grid, check_off_identity_fake   TETHER_OWED_REJUDGE=0 against 2a8045c
    python tests/test_owed_rejudge.py [check ...]
"""
from __future__ import annotations

import collections
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

BASE = "2a8045c"      # wip/ask-stop after 1b, the tree before the arm


def _agent():
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    tether._AGENT_SEED = False
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="owed_rejudge_fixture"),
                      tether.Config(budget=40), ledger.Ledger())
    ag._ds_echo = lambda _d: []
    return env, ag


def _owed_state(max_steps: int = 6):
    env, ag = _agent()
    for _ in range(max_steps):
        ag.step()
        if ag._dw_owed:
            return env, ag
    raise AssertionError(("occasion: no owed derived ask", max_steps))


def _rejudge(ag) -> list:
    n0 = len(ag.led.rows())
    with ag._step_scope("MINT"):
        ag._derived_wants()
    return ag.led.rows()[n0:]


def _explain_sources(env, ag) -> None:
    der = env.derived()
    for d in ag._dw_owed:
        for s in der.get(d, ()):
            ag._outstanding[s] = 0.0


def check_a_sources_explained() -> None:
    env, ag = _owed_state()
    owed = sorted(ag._dw_owed)
    _explain_sources(env, ag)
    rel = [r for r in _rejudge(ag) if r["event"] == "owed_released"]
    assert sorted(r["slot"] for r in rel) == owed, (len(rel), len(owed))
    assert {r["detail"]["why"] for r in rel} == {"sources explained"}, rel[:2]
    assert not set(owed) & set(ag._dw_owed), "a released ask is still owed"
    print(f"  {len(owed)} owed asks, every source explained: {len(rel)} released 'sources "
          "explained', none owed after")


def check_a_mustfail_r281_guard() -> None:
    env, ag = _owed_state()
    n = len(ag._dw_owed)
    der = env.derived()
    live = sum(1 for d in ag._dw_owed if any(ag.outstanding(s) > 0 for s in der[d]))
    assert live == n, ("occasion: every owed ask has a source with outstanding > 0", live, n)

    def literal(d, der_):                      # r281 as written: the derived slot's own surprise
        if d not in der_:
            return "not derived"
        if d in ag.wants:
            return "wants"
        return None if ag.outstanding(d) > 0 else "sources explained"
    ag._owed_why = literal
    rel = [r for r in _rejudge(ag) if r["event"] == "owed_released"]
    assert len(rel) == n, ("MUST-FAIL: r281's literal guard releases every owed ask", len(rel), n)
    env2, ag2 = _owed_state()
    rel2 = [r for r in _rejudge(ag2) if r["event"] == "owed_released"]
    assert not rel2, ("the real guard on the same frame", len(rel2))
    print(f"  MUST-FAIL: r281's literal guard releases all {n} owed asks at the first re-judgment; "
          "the sources' guard releases 0 on the same frame")


def _run(steps: int, probe=None, ag_hook=None):
    env, ag = _agent()
    if ag_hook is not None:
        ag_hook(ag)
    for _ in range(steps):
        n0 = len(ag.led.rows())
        ag.step()
        if probe is not None:
            probe(ag, ag.led.rows()[n0:])
    return env, ag


def check_b_newer_evidence() -> None:
    seen = {"superseded": 0}

    def probe(ag, new):
        asked = {r["slot"] for r in new if r["event"] == "derived_asked"
                 and "owed_since" in r["detail"]}
        for r in new:
            if r["event"] != "owed_superseded":
                continue
            d, now = r["slot"], tuple(r["detail"]["now"])
            assert now != tuple(r["detail"]["was"]), r
            assert d in asked or ag._dw_owed.get(d, (None, None))[1] == now, (d, now)
            seen["superseded"] += 1
    _run(8, probe)
    assert seen["superseded"], "occasion: no owed ask was superseded"
    print(f"  {seen['superseded']} supersedes, each newer transition carried or asked")


def _first_mints(rank_identity: bool):
    calls = collections.defaultdict(list)

    def hook(ag):
        m0 = ag._mint_in_step

        def spy(slot, b):
            calls[ag.cycle].append(slot)
            return m0(slot, b)
        ag._mint_in_step = spy
        if rank_identity:
            ag._rank_mints = lambda routed, _split: routed
    _env, ag = _run(8, ag_hook=hook)
    return calls, ag


def _rank_occasion():
    _calls, ag = _first_mints(False)
    for r in ag.led.rows():
        d = r["detail"] if r["event"] == "mint_rank" else None
        if d and d["order"][0] != d["was"][0] and d["rank"][0] > d["rank"][
                d["order"].index(d["was"][0])]:          # decided by rank, not by an A1 tie
            return r["cycle"], d
    raise AssertionError("occasion: no step where a strictly higher rank overtakes code order")


def check_c_rank_first() -> None:
    c, d = _rank_occasion()
    calls, _ag = _first_mints(False)
    assert calls[c][0] == d["order"][0], (c, calls[c], d)
    print(f"  cycle {c}: rank {d['order']} {d['rank']}, code order {d['was']}: first mint "
          f"{calls[c][0]}")


def check_c_mustfail_code_order() -> None:
    c, d = _rank_occasion()
    calls, _ag = _first_mints(True)
    assert calls[c][0] == d["was"][0] != d["order"][0], ("MUST-FAIL: code order", c, calls[c], d)
    print(f"  MUST-FAIL: code order at cycle {c} mints {calls[c][0]} first, not {d['order'][0]}")


def check_d_mustfail_off() -> None:
    import tether
    env, ag = _owed_state()
    n = len(ag._dw_owed)
    _explain_sources(env, ag)
    tether._OWED_REJUDGE = False
    new = _rejudge(ag)
    rel = [r for r in new if r["event"] == "owed_released"]
    kept = sum(1 for r in new if r["event"] in ("derived_asked", "derived_deferred")
               and ("owed_since" in r["detail"] or r["event"] == "derived_deferred"))
    assert not rel and kept >= n, ("MUST-FAIL: OFF keeps every owed ask", len(rel), kept, n)
    print(f"  MUST-FAIL: OFF, every source explained: 0 released, {n} owed asks carried on")


def check_f_reraised() -> None:
    env, ag = _owed_state()
    _explain_sources(env, ag)
    rel = {r["slot"] for r in _rejudge(ag) if r["event"] == "owed_released"}
    assert rel, "occasion: nothing released"
    back = set()
    for _ in range(6):
        n0 = len(ag.led.rows())
        ag.step()
        back |= {r["slot"] for r in ag.led.rows()[n0:]
                 if r["event"] in ("derived_asked", "derived_deferred") and r["slot"] in rel}
        if back:
            break
    assert back, ("a released ask raised again by a later frame", len(rel))
    print(f"  {len(rel)} released; {len(back)} raised again by a later frame, e.g. "
          f"{sorted(back)[0]}")


def _tried_shrinks(prefix: bool) -> tuple:
    """Per step: (slot, transition) pairs in _dw_tried before the step and gone after it."""
    gone, steps, skipped = [], 0, 0
    env, ag = _agent()
    if prefix:                      # the supersede before the fix: newest transition, tried or not
        ag._supersedes = lambda _d, ct, t_new: t_new != ct[1]
    for _ in range(8):
        was = {d: set(ts) for d, ts in ag._dw_tried.items()}
        n0 = len(ag.led.rows())
        ag.step()
        if any(r["event"] == "boundary" for r in ag.led.rows()[n0:]):
            skipped += 1             # retarget's own row: it clears the tried set with the names
            continue
        steps += 1
        gone += [(d, t) for d, ts in was.items() for t in ts - ag._dw_tried.get(d, set())]
    return gone, steps, skipped, ag


def check_g_tried_never_shrinks() -> None:
    gone, steps, skipped, ag = _tried_shrinks(False)
    sup = sum(1 for r in ag.led.rows() if r["event"] == "owed_superseded")
    assert steps and sup, ("occasion: steps and supersedes", steps, sup)
    assert not gone, ("a settled transition was reopened", gone[:3])
    print(f"  {steps} steps read, {skipped} skipped at a boundary row, {sup} supersedes: no asked "
          "transition left the tried set")


def check_g_mustfail_prefix_supersede() -> None:
    gone, steps, _skipped, _ag = _tried_shrinks(True)
    assert gone, ("MUST-FAIL: the pre-fix supersede reopens a settled transition", steps)
    print(f"  MUST-FAIL: the pre-fix supersede reopens {len(gone)} asked transitions, e.g. "
          f"{gone[0]}")


def _three_mechanism(on: bool):
    """test_step_mint check_a's fixture (three MECHANISM slots, every mint stops at its bound)."""
    import tether
    _env, ag = _agent()
    for _ in range(3):
        ag.step()
    three = [s for s in sorted(ag.slots) if s not in getattr(ag, "_own_now", ())][:3]
    calls: list = []

    def fake_mint(slot):
        calls.append((ag.cycle, slot))
        ag._mint_exhausted = True
    ag.mint = fake_mint
    ag.route = lambda _res: [(s, tether.MECHANISM, None, "test") for s in three]
    tether._OWED_REJUDGE = on
    c0, n0 = ag.cycle, len(ag.led.rows())
    ag.step()
    c1, n1 = ag.cycle, len(ag.led.rows())
    ag.step()
    return three, calls, c0, c1, ag.led.rows()[n0:n1], ag.led.rows()[n1:]


def check_h_on_first_mint_by_rank() -> None:
    three, calls, c0, c1, _r0, r1 = _three_mechanism(True)
    mr = [r["detail"] for r in r1 if r["event"] == "mint_rank"]
    assert mr, "occasion: no mint_rank row in the second step"
    d = mr[0]
    assert d["rank"] == sorted(d["rank"], reverse=True), d
    second = [s for c, s in calls if c == c1 and s in three]
    assert second and second[0] == d["order"][0], (second, d)
    print(f"  ON sibling of test_step_mint check_a: the next step's first mint is {second[0]} "
          f"(order {d['order']}, rank {d['rank']}, was {d['was']})")


def check_i_on_derived_a1_order() -> None:
    import frontier as FR
    env, ag = _agent()
    seen_steps = 0
    for _ in range(8):
        before = collections.Counter(ag._dw_seen)
        n0 = len(ag.led.rows())
        ag.step()
        asked = [r["slot"] for r in ag.led.rows()[n0:] if r["event"] == "derived_asked"]
        if len(asked) < 2:
            continue
        der = sorted(env.derived())
        drawn = {s: i for i, s in enumerate(FR.draw_order(der, f"{ag.cycle - 1}:derived",
                                                          ag.draw_seed))}
        want = sorted(asked, key=lambda s: (before[s], drawn[s]))
        assert asked == want, (ag.cycle - 1, asked[:6], want[:6])
        seen_steps += 1
    assert seen_steps, "occasion: no step with two or more derived asks"
    print(f"  ON sibling of test_step_derived check_e: {seen_steps} steps ask owed and fresh "
          "alike by A1 (fewer asks first, then the draw)")


def _tie(skip_plain: bool) -> tuple:
    out = {"occasion": 0, "deferred_after_plain": 0, "derived_run_after_skip": 0, "ranks": []}

    def hook(ag):
        ag._understanding = lambda _s: 0.0           # every candidate at rank 0, as a derived ask
        if skip_plain:
            ag._mint_in_step = lambda _slot, _b: None

    def probe(_ag, new):
        ranks = [r["detail"]["rank"] for r in new if r["event"] == "mint_rank"]
        out["ranks"] += [v for rk in ranks for v in rk]
        plain = {s for r in new if r["event"] == "mint_rank" for s in r["detail"]["order"]}
        sd = [r["detail"] for r in new if r["event"] == "step_derived"]
        pending = sum(x["derived_run"] + x["derived_deferred"] for x in sd)
        if ranks and all(v == 0 for rk in ranks for v in rk) and pending:
            out["occasion"] += 1
            out["deferred_after_plain"] += sum(
                1 for r in new
                if r["event"] == "derived_deferred" and r["detail"]["after"] in plain)
            out["derived_run_after_skip"] += sum(x["derived_run"] for x in sd)
    _run(8, probe, ag_hook=hook)
    return out


def check_tie_plain_first() -> None:
    # r334's guard: plain-first IS the (rank, kind_order) order only while every plain rank is
    # >= 0 (a derived ask's is 0). Read on a run with the real _understanding.
    _env, ag = _run(8)
    real = [v for r in ag.led.rows() if r["event"] == "mint_rank" for v in r["detail"]["rank"]]
    assert real and min(real) >= 0, ("a plain rank below 0 breaks plain-first", real)
    o = _tie(False)
    assert o["occasion"], ("occasion: a step with plain candidates and derived asks at rank 0", o)
    assert o["deferred_after_plain"], ("the plain mint took the step's search", o)
    print(f"  r333 tie: {o['occasion']} steps with both at rank 0; {o['deferred_after_plain']} "
          "derived asks owed after a plain candidate's stop")


def check_tie_control() -> None:
    o = _tie(True)
    assert o["occasion"] and o["derived_run_after_skip"], ("control: the derived asks run", o)
    print(f"  control, the plain mints skipped: {o['derived_run_after_skip']} derived asks run")


PROBE = r'''
import json, sys
sys.dont_write_bytecode = True
tree, which = sys.argv[1], sys.argv[2]
sys.path = ([tree, tree + "/tests"]
            + [p for p in sys.path if "scratchpad" not in p.replace("\\", "/")])
if which == "fake":
    import arc_holdout
    from test_entry import FakeWrapper
    env, ag, led, *_ = arc_holdout.wire(FakeWrapper(), "fake")
    n = 16
else:
    import gamma, gridworld, ledger, tether, world
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(budget=40),
                      ledger.Ledger())
    n = 8
for _ in range(n):
    ag.step()
ag.end_run("cap")
print(json.dumps({"rows": ag.led.rows()}, default=str))
'''


def _child(tree: str, which: str, extra: dict | None = None) -> list:
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",
               **(extra or {}))
    out = subprocess.run([sys.executable, "-B", "-c", PROBE, tree, which], env=env,
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


def _off_identity(w: str) -> None:
    root = str(_repo.ROOT)
    with tempfile.TemporaryDirectory() as d:
        tar = subprocess.run(["git", "-C", root, "archive", BASE], capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
            tf.extractall(d, filter="data")
        base = _norm(_child(d, w))
    cur = _norm(_child(root, w, off_env("TETHER_OWED_REJUDGE")))
    diff = sum(1 for x, y in zip(base, cur, strict=False) if x != y) + abs(len(base) - len(cur))
    assert len(base) > 50 and diff == 0, (w, len(base), len(cur), next(
        (i for i, (x, y) in enumerate(zip(base, cur, strict=False)) if x != y), None))
    print(f"  OFF identity (TETHER_OWED_REJUDGE=0, {w}): {len(base)} rows against {BASE}, "
          "0 differences")


def check_off_identity_grid() -> None:
    _off_identity("grid")


def check_off_identity_fake() -> None:
    _off_identity("fake")


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
    print(f"owed_rejudge: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
