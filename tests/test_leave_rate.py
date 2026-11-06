"""26 THE LEAVE RULE (TETHER_LEAVE_RATE, default ON; the reviewer 2026-11-05 r1268, r1269).
gridworld default seed 0, the agent seed pinned, 6 steps; rho and the rates PLANTED, never read
live (tests/_repo.py). A planted goal hypothesis goes through the real _hyp_check; its end is
captured. Each check its own process.
  check_l1_left_under_rho   rho > 0, the line's rate under it: left ("stalled" by "rate"), tagged
                            LEFT, a line_choice row kept False. OFF: no rate leave
  check_l2_seed_ceiling     rho == 0: the ceiling ends it, as today (the seed)
  check_l3_kept_over_rho    past the ceiling with its rate over rho: kept, the ceiling a reading
                            on the row. OFF: the ceiling ends it
  check_l4_routine_verdict  a routine's divergence still abandons it; its rate is a reading on
                            the row and the line is tagged LEFT
  check_l5_7f_unchanged     7f's exhaustion leave is unchanged: item 26 only tags it (AST)
  check_l6_wrong_leave      a left mint line that reopens and pays, and a left routine that is
                            DONE, each write wrong_leave and lower their leave weight
  check_l7_inside_chooser   the leave is a reading inside the chooser: no new exit (AST)
    python tests/test_leave_rate.py [check ...]
"""
from __future__ import annotations

import subprocess
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True


def _agent():
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    assert tether._LEAVE_RATE, "TETHER_LEAVE_RATE is OFF"
    tether._AGENT_SEED = False
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    for _ in range(6):
        ag.step()
    return ag


def _rows(ag, event):
    return [r["detail"] for r in ag.led.rows() if r["event"] == event]


def _hyp(ag, steps: int, budget: int, fell: float):
    """A held hypothesis on one slot, `steps` own presses so far, the slot's outstanding fallen
    by `fell` bits since birth; its end captured."""
    import tether
    slot = max((s for s in ag.slots if not s.startswith("@")), key=ag.outstanding)
    ag._outstanding[slot] = 20.0
    key = ("planted",)
    ag._goal_links[key] = ()
    ag._hyp = {"key": key, "tkey": ("planted-t",), "slots": [slot], "steps": steps,
               "budget": budget, "reads": {}, "seg": {}, "own_last": True, "touches": 0,
               "r0": 1.0, "out0": {slot: 20.0 + fell}, "text": "planted"}
    ended = []
    ag._hyp_end = lambda why, **k: ended.append((why, k.get("by")))
    ag._res = {}
    assert tether._GOAL_HYP, "precondition: TETHER_GOAL_HYPOTHESES"
    return slot, ended


def check_l1_left_under_rho() -> None:
    import tether
    ag = _agent()
    ag._tc_rho = lambda: 2.0
    _slot, ended = _hyp(ag, tether.MIN_REPEAT + 1, 100, fell=1.0)   # rate 1.0 / (MR+2) < 2.0
    ag._hyp_check()
    row = _rows(ag, "line_choice")[-1]
    assert ended == [("stalled", "rate")] and not row["kept"], (ended, row)
    assert ("hyp", ("planted-t",)) in ag._lr_left, ag._lr_left
    print(f"  rate {row['rate']} < rho {row['rho']}: left {ended}, tagged LEFT")


def check_l2_seed_ceiling() -> None:
    ag = _agent()
    ag._tc_rho = lambda: 0.0
    _slot, ended = _hyp(ag, 5, 5, fell=50.0)                       # steps -> 6 > budget 5
    ag._hyp_check()
    assert ended == [("stalled", "ceiling")], ended
    assert not _rows(ag, "line_choice"), "a line_choice row while rho is 0"
    print(f"  rho 0: {ended} (the ceiling, the seed)")


def check_l3_kept_over_rho() -> None:
    ag = _agent()
    ag._tc_rho = lambda: 2.0
    _slot, ended = _hyp(ag, 5, 5, fell=50.0)                       # rate 50 / 6 > 2.0
    ag._hyp_check()
    row = _rows(ag, "line_choice")[-1] if _rows(ag, "line_choice") else None
    assert not ended and row and row["kept"] and "ceiling" in row["readings"], (ended, row)
    print(f"  past the ceiling, rate {row['rate']} > rho {row['rho']}: kept; readings "
          f"{row['readings']}")


def check_l4_routine_verdict() -> None:
    import routine as Rt
    ag = _agent()
    before = ag.env.observe()
    slot = next(s for s in sorted(before) if not s.startswith("@"))
    ag.routine = Rt.Act("x")
    ag._expect = (slot, before[slot], 0)
    ag._lr_rt0 = (ag.outstanding() + 5.0, ag._tc_presses - 2, "planted-form")
    done = ag._check_expectation(before, step="SETTLE")
    row = _rows(ag, "routine_abandoned")[-1]
    assert done and row["line_rate"] == 2.5 and row["line_presses"] == 2, row
    assert ("routine", "planted-form") in ag._lr_left
    print(f"  abandoned on divergence (the verdict kept); line_rate {row['line_rate']}, tagged")


def check_l5_7f_unchanged() -> None:
    import ast
    import inspect

    import tether
    assert tether._LEAVE_RATE, "TETHER_LEAVE_RATE is OFF"
    src = inspect.cleandoc("\n" + inspect.getsource(tether.Agent._leave_check))
    assert "unreachable at this budget" in src
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.If) and "_LEAVE_RATE" in ast.unparse(n.test):
            body = ast.unparse(ast.Module(body=n.body, type_ignores=[]))
            assert "_lr_left" in body or "_tc_wrong_leave" in body, body
            assert "return" not in body and "_leave_held" not in body, body
    print("  7f's verdict is untouched: item 26 only tags its leave and its later pay")


def check_l6_wrong_leave() -> None:
    import routine as Rt
    ag = _agent()
    slot = max((s for s in ag.slots if not s.startswith("@")), key=ag.outstanding)
    kind = ag._kind_key(slot)
    ag._lr_left[("mint", slot)] = ag.cycle - 3
    ag._leave_line[slot] = {"key": (ag.level, ag._root_id), "first": 10.0, "mints": 1}
    ag._outstanding[slot] = 5.0
    ag.bound.pop(slot, None)
    a0 = ag._rf_standing("leave", ("mint", kind))["against"]
    ag._leave_check(slot, 10.0)
    ag._lr_rt0 = (ag.outstanding(), ag._tc_presses, "planted-form")
    ag._lr_left[("routine", "planted-form")] = ag.cycle - 2
    ag._lr_routine_end(Rt.DONE)
    rows = _rows(ag, "wrong_leave")
    assert [r["line"] for r in rows[-2:]] == ["mint", "routine"], rows
    assert ag._rf_standing("leave", ("mint", kind))["against"] > a0
    assert ("mint", slot) not in ag._lr_left and ("routine", "planted-form") not in ag._lr_left
    print(f"  wrong_leave on a reopened mint line that paid and a left routine DONE; mint weight "
          f"against {rows[-2]['weight_against']}")


def check_l7_inside_chooser() -> None:
    import ast
    import inspect

    import tether
    assert tether._LEAVE_RATE, "TETHER_LEAVE_RATE is OFF"
    line = ast.parse(inspect.cleandoc("\n" + inspect.getsource(tether.Agent._tc_line)))
    rets = [n for n in ast.walk(line) if isinstance(n, ast.Return)]
    assert len(rets) == 1, "the line reading has one exit"
    walk = ast.parse(inspect.cleandoc("\n" + inspect.getsource(tether.Agent._tc_walk)))
    for n in ast.walk(walk):
        if isinstance(n, ast.If) and "_tc_line" in ast.unparse(n.test):
            assert all(isinstance(b, ast.Assign) for b in n.body), ast.unparse(n)
    print("  _tc_line: one exit; in the walk a line under rho only replaces the gain")


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
    print(f"leave_rate: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
