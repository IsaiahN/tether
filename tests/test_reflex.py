"""22 THE REFLEX TIER (TETHER_REFLEX, default ON; the reviewer 2026-11-05 r1242, r1243). gridworld
default seed 0, the agent seed pinned, 6 steps, then a planted read. Each check its own process; a
run with TETHER_REFLEX=0 in the environment turns every check red at its first line.
  check_r1_fires_first    a change with no own cause, no record: choose returns by="reflex"
                          ahead of a held routine; OFF the routine acts
  check_r2_ties_witness   one witness against: a tie, it fires (R2a); two: it does not and
                          deliberation acts (R2b); one row removed: it fires again
  check_r3_paused         the held routine is the same object after the reflex step, and its
                          next advance is its own first step
  check_r4_recovery       two witnesses, fewer ticks than one halflife: no fire; one halflife: fires
  check_r5_sensitize      a death with the guard met and no fire is paid: a situation that would
                          not fire then fires
  check_r6_no_identity    no game id and no family name is read at the reflex sites (AST)
  check_r7_habituates     a recurring unexplained change: two fires, two misses, then no fire
  check_freeze            a held routine whose next press is the death-voted kind: ON a
                          never-voted offer (by="reflex"); OFF the voted kind
    python tests/test_reflex.py [check ...]
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
    assert tether._REFLEX, "TETHER_REFLEX is OFF: the reflex tier is not read"
    tether._AGENT_SEED = False
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="g"), tether.Config(), ledger.Ledger())
    for _ in range(6):
        ag.step()
    return ag


def _plant_orient(ag, against: float = 0.0, paid: int = 0) -> tuple:
    """A slot whose outstanding grew since the last read, not credited to the last press."""
    slot = sorted(s for s in ag.slots if "." in s and not s.startswith("@"))[0]
    ag._rf_out = {s: v for s, v in ag._outstanding.items() if v > 0 and s != slot}
    ag._outstanding[slot] = ag._outstanding.get(slot, 0.0) + 5.0
    ag.iface.last_changed = ()
    ag._last_press_key = None
    ag._rf_pending = []
    situ = (ag._kind_key(slot), "orient")
    ag._reflexes["orient"]["standing"][situ] = {"paid": paid, "against": against,
                                                "tick": ag.cycle}
    return slot, situ


def _held(ag):
    import routine as Rt
    a = sorted(x for x in ag.actions if x != "RESET")[0]
    ag.routine = Rt.Seq(Rt.Act(a), Rt.Act(a))
    ag.routine_for, ag._routine_next = None, None
    return ag.routine, a


def _fires(ag) -> bool:
    before = ag.env.observe()
    return ag._reflex(before) is not None


def check_r1_fires_first() -> None:
    import tether
    ag = _agent()
    _plant_orient(ag)
    rt, a = _held(ag)
    act, by = ag.choose(ag.env.observe())
    assert by == "reflex" and ag.routine is rt, (by, act)
    row = [r["detail"] for r in ag.led.rows() if r["event"] == "reflex"][-1]
    assert row["fired"] and row["routine_paused"] and row["p"] == round(2 / 3, 3), row
    ag2 = _agent()
    _plant_orient(ag2)
    _held(ag2)
    tether._REFLEX = False                    # MUST-FAIL: the arm off, the routine acts
    act2, by2 = ag2.choose(ag2.env.observe())
    assert by2 == "routine" and act2 == a, (by2, act2)
    print(f"  ON by={by} ({act}), the routine held; OFF by={by2} ({act2})")


def check_r2_ties_witness() -> None:
    ag = _agent()
    _plant_orient(ag, against=1.0)
    assert _fires(ag), "R2a: one witness against is a tie and the wiring wins it"
    _plant_orient(ag, against=2.0)
    rt, a = _held(ag)
    assert not _fires(ag), "R2b: two witnesses outweigh the wiring"
    _plant_orient(ag, against=2.0)
    act, by = ag.choose(ag.env.observe())
    assert by == "routine" and act == a, (by, act)
    _plant_orient(ag, against=1.0)            # one witness row removed
    assert _fires(ag), "one row removed: it fires again"
    print(f"  one witness: fires (tie); two: no fire, by={by}; one removed: fires")


def check_r3_paused() -> None:
    import routine as Rt
    ag = _agent()
    _plant_orient(ag)
    rt, a = _held(ag)
    _act, by = ag.choose(ag.env.observe())
    assert by == "reflex" and ag.routine is rt, by
    emit, _rest = Rt.advance(ag.routine, ag._holds(ag.env.observe()), ag.routine_lib,
                             ag.routine_state)
    assert emit == a, emit
    print(f"  after the reflex step the routine is the same object; its next advance is {emit}")


def check_r4_recovery() -> None:
    import tether
    ag = _agent()
    hl = ag.gamma.halflife or tether.REJECTION_HALFLIFE
    _plant_orient(ag, against=2.0)
    c0 = ag.cycle
    _slot, situ = _plant_orient(ag, against=2.0)
    ag.cycle = c0 + int(hl) - 1
    assert not _fires(ag), "fewer ticks than one halflife: no fire"
    _slot, situ = _plant_orient(ag, against=2.0)
    ag._reflexes["orient"]["standing"][situ]["tick"] = c0
    ag.cycle = c0 + int(-(-hl // 1))
    assert _fires(ag), "one halflife: against <= 1, it fires (recovery)"
    print(f"  halflife {hl}: {int(hl) - 1} ticks no fire; {int(-(-hl // 1))} ticks fires")


def check_r5_sensitize() -> None:
    ag = _agent()
    _slot, situ = _plant_orient(ag, against=2.0)
    assert not _fires(ag)
    ag._rf_pending = [("orient", situ, _slot, 0.0, False)]
    ag._alive = False                         # a death followed the guard, with no fire
    ag._reflex_settle()
    st = ag._reflexes["orient"]["standing"][situ]
    assert st["paid"] == 1, st
    ag._alive = True
    _plant_orient(ag, against=2.0, paid=1)
    assert _fires(ag), "paid 1 against 2: 1 + 1 >= 2, it fires"
    print(f"  a death with the guard met, no fire: paid {st['paid']}; then it fires")


def check_r6_no_identity() -> None:
    import ast
    import inspect

    import tether
    fams = set(tether._DESC_SEED) | set(tether._DESC_SEED.values())
    for f in (tether.Agent._reflex, tether.Agent._reflex_settle, tether.Agent._rf_standing):
        tree = ast.parse(inspect.cleandoc("\n" + inspect.getsource(f)))
        for n in ast.walk(tree):
            if isinstance(n, ast.Constant) and isinstance(n.value, str):
                assert n.value not in fams, (f.__name__, n.value)
            name = n.attr if isinstance(n, ast.Attribute) else getattr(n, "id", "")
            assert "game" not in name.lower(), (f.__name__, name)
    print(f"  _reflex, _reflex_settle, _rf_standing: no game id, none of {len(fams)} family names")


def check_r7_habituates() -> None:
    ag = _agent()
    slot, situ = _plant_orient(ag)
    fires = []
    for _ in range(3):
        ag._rf_out = {s: v for s, v in ag._outstanding.items() if v > 0 and s != slot}
        ag._outstanding[slot] += 5.0          # recurring, never explained
        ag.iface.last_changed = ()
        ag._last_press_key = None
        ag._rf_pending = []
        fires.append(_fires(ag))
        ag.cycle += 1
        ag._outstanding[slot] += 1.0          # the consequence fails: not explained next step
        ag._reflex_settle()
    st = ag._reflexes["orient"]["standing"][situ]
    assert fires == [True, True, False], (fires, st)
    print(f"  fires {fires}; against {round(st['against'], 3)}, paid {st['paid']}")


def check_freeze() -> None:
    import routine as Rt
    import tether
    ag = _agent()
    k = ag._last_press_key
    assert k is not None, "PRECONDITION: no press key after 6 steps"
    ag._death_n[k] += 1
    ag._press_n[k] = max(ag._press_n[k], 1)
    ag._rf_out = {s: v for s, v in ag._outstanding.items() if v > 0}
    ag._rf_pending = []
    ag.routine = Rt.Seq(Rt.Act(k[1]), Rt.Act(k[1]))
    ag.routine_for, ag._routine_next = None, None
    act, by = ag.choose(ag.env.observe())
    assert by == "reflex" and act != k[1] and not ag._danger((k[0], act, k[2])), (by, act, k)
    ag2 = _agent()
    k2 = ag2._last_press_key
    ag2._death_n[k2] += 1
    ag2._press_n[k2] = max(ag2._press_n[k2], 1)
    ag2.routine = Rt.Seq(Rt.Act(k2[1]), Rt.Act(k2[1]))
    ag2.routine_for, ag2._routine_next = None, None
    tether._REFLEX = False                    # MUST-FAIL: the voted kind is pressed
    act2, by2 = ag2.choose(ag2.env.observe())
    assert by2 == "routine" and act2 == k2[1], (by2, act2)
    print(f"  voted {k[1]}: ON by={by} took {act}; OFF by={by2} pressed {act2}")


def main() -> int:
    want = sys.argv[1:]
    names = [k for k in globals() if k.startswith("check_") and (not want or k in want)]
    assert not want or len(names) == len(want), ("unknown check name", sorted(want))
    if len(names) == 1:
        globals()[names[0]]()
        print("ok  ", names[0])
        return 0
    bad = []
    for n in names:
        r = subprocess.run([sys.executable, "-B", __file__, n], cwd=str(_repo.ROOT),
                           stdin=subprocess.DEVNULL)
        if r.returncode:
            bad.append(n)
    assert not bad, bad
    print(f"reflex: {len(names)} checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
