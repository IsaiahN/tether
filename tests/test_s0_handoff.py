"""28 SYSTEM 0 HANDS OFF BY UNDERSTANDING (TETHER_S0_HANDOFF, default ON; the reviewer 2026-11-05
r1277, r1278). gridworld default seed 0, the agent seed pinned, 6 steps; the board's integral, the
outstanding and the drives PLANTED where a check is about the weighing. Each check its own process.
  check_z1_board_start      a new board reads unexplained 1.0 (the edge, said on the reading):
                            System 0 at full weight
  check_z2_explained_down   a mostly explained board weighs System 0 down to its unexplained share
  check_z3_exhausted_in     every drive exhausted: System 0 still aims (least-touched) and enters
                            the contest; OFF it is absent
  check_z4_open_but_known   one drive open, the board explained: weighed down, never at today's res
  check_z5_witness          stall, then a System 0 turn that finds a new contact, then a pay: paid;
                            a turn that finds nothing new: against
  check_z5b_await_closes    a kind awaiting a pay closes with NO verdict at a level end that did
                            not advance (r1279): "found new, no pay followed"
  check_z6_fallback         choose's fallback reads the contest's System 0 option (AST)
    python tests/test_s0_handoff.py [check ...]
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
    assert tether._S0_HANDOFF, "TETHER_S0_HANDOFF is OFF"
    tether._AGENT_SEED = False
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    for _ in range(6):
        ag.step()
    return ag


def _rows(ag, event):
    return [r["detail"] for r in ag.led.rows() if r["event"] == event]


def _obj(ag):
    return sorted({s.split(".")[0] for s in ag.slots if s[:1] == "o" and "~" not in s})[0]


def _plant_explained(ag, obj, share):
    """the board: 100 bits charged since its start, `share` of them still outstanding, all on
    `obj`'s slots."""
    for s in ag.slots:
        ag._outstanding[s] = 0.0
    mine = [s for s in ag.slots if s.split(".")[0] == obj]
    for s in mine:
        ag._outstanding[s] = 100.0 * share / len(mine)
    ag._s0_int0 = ag._integral - 100.0
    return mine


def check_z1_board_start() -> None:
    import tether
    ag = _agent()
    ag.retarget(ag.env, ag.level, how=tether.NEW_BOARD)
    un, how = ag._s0_unexplained()
    assert un == 1.0 and how.startswith("board start"), (un, how)
    print(f"  new board: unexplained {un} ('{how}')")


def check_z2_explained_down() -> None:
    ag = _agent()
    obj = _obj(ag)
    ag._contact_target = lambda _b: (obj, "planted")
    _plant_explained(ag, obj, 0.05)
    tw, w, r = ag._s0_weight(ag.env.observe())
    assert abs(r["unexplained"] - 0.05) < 1e-6 and w < r["aim"] * 0.06, (w, r)
    print(f"  5% unexplained: aim {r['aim']}, weight {w:.3f} (x {r['unexplained']} x p {r['p']})")


def check_z3_exhausted_in() -> None:
    ag = _agent()
    ag._contact_target = lambda _b: (None, "all-contacts-explored")
    ag._board_untried_n = lambda: 0
    ag._untouched_kinds = lambda _b: []
    ag.drive.covered = lambda _n: True
    ag._contact_keys = lambda _b: {}
    assert not ag._system0_active(), "precondition: every drive exhausted"
    before = ag.env.observe()
    tw, _w, r = ag._s0_weight(before)
    n0 = len(_rows(ag, "choice"))
    ag._exit_choice(before)
    rows = [x for x in _rows(ag, "choice")[n0:] if x.get("site") == "exit"]
    assert tw[0] is not None and tw[1] == "least-touched", tw
    assert rows and "s0" in rows[-1] and not any(r[k] for k in ("untried_action",
                                                               "untouched_kind",
                                                               "coverage_open", "contact_open"))
    print(f"  all drives exhausted: aims at {tw[0]} ({tw[1]}), in the contest")


def check_z4_open_but_known() -> None:
    ag = _agent()
    obj = _obj(ag)
    ag._contact_target = lambda _b: (obj, "planted")
    ag._board_untried_n = lambda: 1                     # one drive open
    _plant_explained(ag, obj, 0.1)
    tw, w, r = ag._s0_weight(ag.env.observe())
    assert r["untried_action"] and w < r["aim"], (w, r)
    print(f"  a drive open, 90% explained: weight {w:.3f} below today's res {r['aim']}")


def check_z5_witness() -> None:
    ag = _agent()
    obj = _obj(ag)
    kind = repr(ag._kind(obj))
    ag._s0_stall_at = ag.cycle
    ag._s0_take(obj)
    ag._contact_seen.add(("planted", "new contact"))
    ag.cycle += 1
    ag._s0_settle()
    assert kind in ag._s0_await, ag._s0_await
    ag._s0_pay()
    paid = ag._rf_standing("system0", (kind,))["paid"]
    ag._s0_take(obj)
    ag.cycle += 1
    ag._s0_settle()
    against = ag._rf_standing("system0", (kind,))["against"]
    assert paid == 1 and against >= 1 and _rows(ag, "s0_paid"), (paid, against)
    print(f"  stall -> new contact -> pay: paid {paid}; nothing new: against {against:.2f}")


def check_z5b_await_closes() -> None:
    import tether
    ag = _agent()
    kind = repr(ag._kind(_obj(ag)))
    ag._s0_await.add(kind)
    st0 = dict(ag._rf_standing("system0", (kind,)))
    ag.retarget(ag.env, ag.level, how=tether.NEW_BOARD)     # a level end with no pay
    st1 = ag._rf_standing("system0", (kind,))
    r = _rows(ag, "s0_await_closed")[-1]
    assert not ag._s0_await and r["reads"] == "found new, no pay followed", r
    assert st1["paid"] == st0["paid"] and st1["against"] <= st0["against"], (st0, st1)
    print(f"  a level end with no pay: closed ('{r['reads']}'), neither paid nor against")


def check_z6_fallback() -> None:
    import ast
    import inspect

    import tether
    assert tether._S0_HANDOFF, "TETHER_S0_HANDOFF is OFF"
    src = inspect.cleandoc("\n" + inspect.getsource(tether.Agent.choose))
    hits = [n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.If)
            and ast.unparse(n.test).startswith("_S0_HANDOFF and take is None")
            and "_s0_weight" in ast.unparse(n)]
    assert hits, "the fallback does not read the contest's System 0 option"
    print("  choose's fallback reads _s0_weight (the contest's option)")


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
    print(f"s0_handoff: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
