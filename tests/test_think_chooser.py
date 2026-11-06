"""25 THE ONE THINK-VS-ACT CHOOSER (TETHER_THINK_CHOOSER, default ON; the reviewer 2026-11-05
r1261-r1265). gridworld default seed 0, the agent seed pinned, 6 steps; the timing PLANTED
(s_step, s_per_eval, the clocks, rho), never read live (tests/_repo.py). Each check its own process.
  check_c1_one_purse      what choose spends stays charged: the budget row's spent_choose is it,
                          and route does not reset the purse
  check_c2_runner_clocks  every runner sets the game's clock beside its loop; a run's think_choice
                          rows read actions_left = max_actions - taken
  check_c3_worked_step    the worked step (r1262): far, 48 vs 0.47 x 2.0 -> think; near, small
                          park 0.5 vs 0.1 x 2.0 -> think; 0.1 -> act
  check_c4_governor_inputs  closer_found zeroes the walk's gain; urgency raises the act side and
                          flips a choice; no fixed exit order left in the chooser (AST)
  check_c5_witness        a walk taken whose slot's outstanding fell is paid (think_settled, the
                          walk weight +1); a press preferred with no progress is one against
  check_c6_purse_fresh    the purse is fresh when choose (how_soon, look-ahead) reads it, though
                          the last step spent it out
  check_c7_wall_only      no turn count, a slice: displaced = think_s / s_step, never free
  check_c8_no_clock       no clock at all, or a turn count with no wall: displaced 0
  check_c9_no_identity    no game id and no family name at the chooser's sites (AST)
    python tests/test_think_chooser.py [check ...]
"""
from __future__ import annotations

import subprocess
import sys
import time

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True


def _agent(steps: int = 6):
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    assert tether._THINK_CHOOSER, "TETHER_THINK_CHOOSER is OFF"
    tether._AGENT_SEED = False
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    for _ in range(steps):
        ag.step()
    return ag


def _plant(ag, s_step=6.0, s_eval=0.00025, rho=2.0, need=1, urgency=1.0):
    ag._tc_rates = lambda: (s_step, s_eval)
    ag._tc_rho = lambda: rho
    ag._tc_act_side = lambda _kind, _slot: (need, urgency, {})
    ag.deadline = None


def _rows(ag, event):
    return [r["detail"] for r in ag.led.rows() if r["event"] == event]


def check_c1_one_purse() -> None:
    ag = _agent()
    orig = ag.choose

    def choose(before):
        ag._spent += 7
        return orig(before)
    ag.choose = choose
    n0 = len(_rows(ag, "budget"))
    ag.step()
    rows = _rows(ag, "budget")[n0:]
    assert rows and rows[-1].get("spent_choose", 0) >= 7, rows
    assert rows[-1]["spent"] == rows[-1]["spent_choose"] + rows[-1]["spent_route"], rows[-1]
    print(f"  spent_choose {rows[-1]['spent_choose']}, spent_route {rows[-1]['spent_route']}")


def check_c2_runner_clocks() -> None:
    import json
    import os
    import tempfile

    import tether
    import tether_agent
    from test_entry import FakeWrapper
    assert tether._THINK_CHOOSER, "TETHER_THINK_CHOOSER is OFF"
    for f, needle in (("tether_agent.py", "ag.actions_left, ag.actions_cap = max_actions - i_"),
                      ("arc_holdout.py", "ag.actions_left, ag.actions_cap = cycles - i_"),
                      ("kaggle/b_worker.py", "ag.slice_from, ag.slice_until = t_start, t_start"),
                      ("harness/mem_store/e4_stream.py", "ag.actions_left, ag.actions_cap = "
                                                         "n_steps - steps")):
        with open(os.path.join(_repo.ROOT, f), encoding="utf-8") as fh:
            assert needle in fh.read(), (f, needle)
    tether._AGENT_SEED = False
    led = os.path.join(tempfile.mkdtemp(), "c2.jsonl")
    tether_agent.run(FakeWrapper(script={}), "fake", max_actions=4, led_path=led)
    with open(led, encoding="utf-8") as fh:
        seen = {json.loads(x)["detail"]["clocks"]["actions_left"] for x in fh
                if '"think_choice"' in x}
    assert seen and seen <= {4, 3, 2, 1}, seen
    print(f"  four runners set their clock; actions_left read {sorted(seen)}")


def check_c3_worked_step() -> None:
    import tether
    ag = _agent()
    _plant(ag)
    slot = sorted(s for s in ag.slots if "." in s and not s.startswith("@"))[0]
    ag._spent = tether.STEP_BUDGET - 20000              # the muse's 20000 evaluations: 5.0 s
    ag.actions_left, ag.actions_cap = 40, 200
    ag.slice_until = time.time() + 300.0
    c = ag._tc_clocks()
    d = ag._tc_displaced(20000, c)
    assert abs(d - 3.5 / 7.5) < 1e-2, d
    far = ag._tc_choose("muse", slot, "k", 48.0, None)
    ag.actions_left, ag.slice_until = 2, time.time() + 20.0
    dn = ag._tc_displaced(20000, ag._tc_clocks())
    assert abs(dn - 0.1) < 1e-2, dn
    near = ag._tc_choose("muse", slot, "k", 0.5, None)
    small = ag._tc_choose("muse", slot, "k", 0.1, None)
    rows = _rows(ag, "think_choice")[-3:]
    assert (far, near, small) == (True, True, False), rows
    print(f"  far displaced {d:.3f}: think; near {dn:.3f}: 0.5 think, 0.1 act "
          f"(costs {[r['cost'] for r in rows]})")


def check_c4_governor_inputs() -> None:
    import ast
    import inspect

    import tether
    ag = _agent()
    _plant(ag)
    slot = max((s for s in ag.slots if not s.startswith("@")), key=ag.outstanding)
    ag._outstanding[slot] = 10.0
    walk, why = ag._think_or_act(slot, closer=True)
    assert (walk, why) == (False, "closer_found"), (walk, why)
    ag._spent = tether.STEP_BUDGET - 20000
    ag.actions_left, ag.slice_until = None, time.time() + 300.0     # wall only: 0.833 displaced
    calm = ag._tc_choose("walk", slot, "k", 3.0, None)               # cost 0.833 x 2 = 1.67
    _plant(ag, urgency=4.0)
    urgent = ag._tc_choose("walk", slot, "k", 3.0, None)             # cost 6.67
    assert (calm, urgent) == (True, False), (calm, urgent)
    for f in (tether.Agent._tc_walk, tether.Agent._tc_choose, tether.Agent._tc_act_side):
        for n in ast.walk(ast.parse(inspect.cleandoc("\n" + inspect.getsource(f)))):
            if isinstance(n, ast.Constant) and isinstance(n.value, str):
                assert n.value not in ("urgent", "urgent_declined", "probe_first",
                                       "probe_declined"), (f.__name__, n.value)
    print(f"  closer -> {why}; gain 3.0: urgency 1 think, urgency 4 act; no exit order left")


def check_c5_witness() -> None:
    ag = _agent()
    _plant(ag)
    slot = max((s for s in ag.slots if not s.startswith("@")), key=ag.outstanding)
    ag._outstanding[slot] = 10.0
    ag._tc_pending = []
    ag._tc_choose("walk", slot, ag._kind_key(slot), 5.0, None)
    ag._tc_choose("muse", None, "mk", 0.0, None)        # an act preferred over a muse
    ag._last_progress = ag._last_commit = -1
    p0 = ag._rf_standing("walk", (ag._kind_key(slot),))["paid"]
    ag.cycle += 1
    ag._outstanding[slot] = 4.0
    ag._tc_settle()
    rows = _rows(ag, "think_settled")[-2:]
    walk = [r for r in rows if r["option"] == "walk"][0]
    act = [r for r in rows if r["option"] == "muse"][0]
    assert walk["paid"] and walk["weight_paid"] == p0 + 1, walk
    assert act["chosen"] == "act" and not act["paid"] and act["weight_against"] >= 1, act
    print(f"  walk paid (weight {walk['weight_paid']}); press over the muse unpaid "
          f"(against {act['weight_against']})")


def check_c6_purse_fresh() -> None:
    import tether
    ag = _agent()
    seen = []
    orig = ag.choose

    def choose(before):
        seen.append(ag._spent)
        return orig(before)
    ag.choose = choose
    ag._spent = tether.STEP_BUDGET                      # the last step spent it out
    ag.step()
    assert seen == [0], seen
    print(f"  choose read the purse at {seen[0]} after a spent-out step")


def check_c7_wall_only() -> None:
    ag = _agent()
    _plant(ag)
    ag.actions_left, ag.slice_until = None, time.time() + 300.0
    d = ag._tc_displaced(20000, ag._tc_clocks())
    assert abs(d - 5.0 / 6.0) < 1e-3, d
    print(f"  wall only: displaced {d:.4f} = 5.0 s / 6.0 s")


def check_c8_no_clock() -> None:
    ag = _agent()
    _plant(ag)
    ag.actions_left = ag.slice_until = None
    none = ag._tc_displaced(20000, ag._tc_clocks())
    ag.actions_left, ag.actions_cap = 40, 200
    count = ag._tc_displaced(20000, ag._tc_clocks())
    assert none == 0.0 and count == 0.0, (none, count)
    print("  no clock: 0; a turn count with no wall: 0")


def check_c9_no_identity() -> None:
    import ast
    import inspect

    import tether
    assert tether._THINK_CHOOSER, "TETHER_THINK_CHOOSER is OFF"
    fams = set(tether._DESC_SEED) | set(tether._DESC_SEED.values())
    fs = (tether.Agent._tc_note_step, tether.Agent._tc_rates, tether.Agent._tc_clocks,
          tether.Agent._tc_displaced, tether.Agent._tc_rho, tether.Agent._tc_need,
          tether.Agent._tc_act_side, tether.Agent._tc_choose, tether.Agent._tc_walk,
          tether.Agent._tc_muse, tether.Agent._tc_settle)
    for f in fs:
        for n in ast.walk(ast.parse(inspect.cleandoc("\n" + inspect.getsource(f)))):
            if isinstance(n, ast.Constant) and isinstance(n.value, str):
                assert n.value not in fams, (f.__name__, n.value)
            name = n.attr if isinstance(n, ast.Attribute) else getattr(n, "id", "")
            assert "game" not in name.lower(), (f.__name__, name)
    print(f"  {len(fs)} sites: no game id, none of {len(fams)} family names")


def check_c10_walk_binds() -> None:
    ag = _agent()
    _plant(ag)
    slot = max((s for s in ag.slots if not s.startswith("@")), key=ag.outstanding)
    ag._outstanding[slot] = 10.0
    ag._tc_pending = []
    ag._tc_choose("walk", slot, ag._kind_key(slot), 5.0, None)
    ag.bound[slot] = "a new bound term"                   # the mint bound it; nothing fell yet
    other = next(s for s in ag.slots if s != slot and not s.startswith("@"))
    ag._outstanding[other] = 10.0
    ag._tc_choose("walk", other, ag._kind_key(other), 5.0, None)   # neither: one settle, against
    ag.cycle += 1
    ag._tc_settle()
    rows = {r["option"] + ":" + str(r["paid"]) for r in _rows(ag, "think_settled")[-2:]}
    assert rows == {"walk:True", "walk:False"}, rows
    print("  a walk that bound its slot, outstanding not yet fallen: paid; one with neither: "
          "against at its window")


def check_c11_press_refutes() -> None:
    ag = _agent()
    _plant(ag)
    ag._tc_pending = []
    ag._tc_choose("muse", None, "mk", 0.0, None)          # a press preferred over a muse
    c0 = ag.cycle
    ag._last_progress = ag._last_commit = -1               # no progress
    ag._tc_refuted_at = c0 + 1                             # its press refuted a bound term
    ag.cycle += 1
    ag._tc_settle()
    r = _rows(ag, "think_settled")[-1]
    assert r["chosen"] == "act" and r["paid"] and r["weight_paid"] >= 1, r
    print(f"  a press that refuted and made no progress: paid (act weight {r['weight_paid']})")


def main() -> int:
    want = sys.argv[1:]
    names = [k for k in globals() if k.startswith("check_") and (not want or k in want)]
    if len(names) == 1:
        globals()[names[0]]()
        print("ok  ", names[0])
        return 0
    bad = [n for n in names if subprocess.run([sys.executable, "-B", __file__, n],
                                              cwd=str(_repo.ROOT),
                                              stdin=subprocess.DEVNULL).returncode]
    assert not bad, bad
    print(f"think_chooser: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
