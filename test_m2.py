"""`M2_STANDARD`'s seven, each REINTRODUCING THE DEFECT it guards against.

The first version of this audit matched source text -- `"Rt.guards(r)" in src` -- which is the
corpus's own corollary inverted: *an exit code is a declaration where a pattern match over
stdout is a guess.* **A rename would have broken it silently, and a behaviour change would not
have broken it at all**, so it could pass while the mechanism was wrong.

`test_gate.py`'s form instead: **one defect per check, constructed, and the mechanism has to
catch it.** *Tests reach, not existence.*
"""

import math
import sys

import numpy as np
from arcengine import FrameDataRaw, GameState

import arc_atoms
import arc_percept
import arc_predict
import gamma
import routine as Rt
import tether
from arc_world import ArcWorld
from tether import YES, pays, term_bits

sys.dont_write_bytecode = True

SIDE, PALETTE = 14, 7


class _Two:
    """Two objects, one action that moves them. Enough state for a mint to be attempted."""

    def __init__(self) -> None:
        self.n = 0

    def _frame(self):
        f = FrameDataRaw(game_id="m2test", state=GameState.NOT_FINISHED, levels_completed=0,
                         win_levels=3, available_actions=[0, 1, 2, 3])
        b = np.zeros((SIDE, SIDE), dtype=int)
        b[2][self.n] = 3
        b[4][self.n + 1] = 5
        b[5][self.n + 1] = 5
        f.frame = [b]
        return f

    def reset(self):
        self.n = 0
        return self._frame()

    def step(self, *a, **_k):
        act = a[0] if a else None
        if "1" in getattr(act, "name", str(act)) and self.n < SIDE - 3:
            self.n += 1
        return self._frame()


def _agent(cycles: int = 25):
    env = ArcWorld(_Two(), arc_percept.Objects(),
                   arc_atoms.three_spaces(arc_predict.predict()), palette=PALETTE)
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="m2test"), tether.Config())
    for _ in range(cycles):
        ag.step()
    return ag


def _wide(ag, slot="o1.dcol"):
    """Widen only the SCOPE, which is the ceiling every fixture hit. Nothing else is touched."""
    real = ag._group
    ag._group = lambda s, st: (tuple(list(real(s, st)) + [7, 8, 9, 11]) if s == slot
                               else real(s, st))
    ag._disc[slot] = [3, 2, 1]
    ag.routine = ag.routine_for = None
    ag.refuted, ag.refuted_at = {}, {}
    return slot


def _mint(ag, state):
    n0 = len(ag.led.entries)
    ag._mint_routine(state)
    return [e for e in ag.led.entries[n0:] if "routine" in e.event]


def check_can_gates_until():
    """DEFECT: a NESTED guard nobody re-checked -- the durable contamination §3 names.

    The slot's own guard stays reachable, so the mint's first `CAN` passes and only the
    per-guard sweep can catch this. An earlier version patched `can` outright, which the
    SLOT-level check refused first -- so it passed with the per-guard sweep deleted.
    """
    ag = _agent()
    b = dict(ag.env.observe())
    slot = _wide(ag)
    assert ag.can(slot, b) == YES, "fixture: the slot's own guard must stay reachable"
    dead = Rt.Until("no.such.slot", Rt.Act(ag.actions[0]), 3)
    real_compose = Rt.compose
    Rt.compose = lambda *_a, **_k: [Rt.Until(slot, dead, 5)]   # every candidate carries it
    try:
        rows = _mint(ag, b)
    finally:
        Rt.compose = real_compose
    assert ag.can("no.such.slot", b) != YES, "fixture: the nested guard must be unreachable"
    assert ag.routine is None, "committed to a plan whose nested guard is unreachable"
    assert any(e.detail.get("reason", "").startswith("no candidate") for e in rows), (
        "refused, but not for the guard")


def check_trigger_is_the_residual_not_the_reward():
    """DEFECT: minting on the sparse reward channel, which is absent most of a run."""
    ag = _agent()
    b = dict(ag.env.observe())
    _wide(ag)
    _, degree = ag.env.objective()
    assert degree < 1.0, "fixture: the reward channel must be unsatisfied"
    ag.goal_residual = lambda _s, _st: 0.0    # nothing left on the DENSE channel
    _mint(ag, b)
    assert ag.routine is None, "minted with no goal residual -- the trigger is on the wrong channel"


def check_route_is_learned():
    """DEFECT: a routine naming an action the agent has no evidence for."""
    ag = _agent()
    b = dict(ag.env.observe())
    _wide(ag)
    _mint(ag, b)
    if ag.routine is not None:
        learned = ag._goal_split(b)
        assert set(Rt.actions(ag.routine)) == {learned}, (
            f"routine names {Rt.actions(ag.routine)}, learned route is {learned}")


def check_shelf_must_be_runnable_here():
    """DEFECT: composing over a settled routine whose action this level does not advertise."""
    ag = _agent()
    b = dict(ag.env.observe())
    slot = _wide(ag)
    ag.routines = [Rt.Until(slot, Rt.Act("ACTION9"), 3)]
    rows = _mint(ag, b)
    # THE ROW, NOT THE OUTCOME. Asserting on what got minted passes vacuously whenever the
    # bargain happens to prefer a valid candidate on price -- which it did, so the earlier
    # version of this check survived the filter being deleted.
    row = next((e.detail for e in rows if e.event in ("routine", "routine_cut")), None)
    assert row is not None and row["shelf"] == 0, (
        f"an unrunnable shelf routine entered the candidate set: shelf={row and row['shelf']}")
    ag2 = _agent()
    b2 = dict(ag2.env.observe())
    s2 = _wide(ag2)
    ag2.routines = [Rt.Until(s2, Rt.Act(ag2.actions[0]), 3)]
    row2 = next((e.detail for e in _mint(ag2, b2)
                 if e.event in ("routine", "routine_cut")), None)
    assert row2 is not None and row2["shelf"] == 1, "a runnable shelf routine was excluded"


def check_one_bargain():
    """DEFECT: a routine bought when it does not pay -- or priced by a second currency."""
    ag = _agent()
    b = dict(ag.env.observe())
    _wide(ag)
    ag.goal_residual = lambda _s, _st: 0.02   # a real residual, too small to buy a plan
    rows = _mint(ag, b)
    assert ag.routine is None, "bought a plan the bargain could not afford"
    assert any(e.detail.get("reason") == "does-not-pay" for e in rows), "wrong reason"


def check_until_terminates():
    """DEFECT: `Until` on a guard that never holds, running forever."""
    out, cur = [], Rt.Until("never", Rt.Act("A"), 4)
    for _ in range(50):
        emit, rest = Rt.advance(cur, lambda _g: False)
        if emit in (Rt.DONE, Rt.BLOCKED, Rt.EXHAUSTED):
            break
        out.append(emit)
        cur = rest
    assert emit == Rt.EXHAUSTED, f"ended {emit}, not exhausted"
    assert len(out) == 4, f"ran {len(out)} steps against a budget of 4"


def check_endings_stay_apart():
    """DEFECT: an unreadable guard reported as a satisfied one."""
    assert Rt.advance(Rt.Until("g", Rt.Act("A"), 3), lambda _g: None)[0] == Rt.BLOCKED
    assert Rt.advance(Rt.When("g", Rt.Act("A")), lambda _g: None)[0] == Rt.BLOCKED
    assert Rt.advance(Rt.When("g", Rt.Act("A")), lambda _g: False)[0] == Rt.DONE


def check_chunking_reaches_the_bargain():
    """DEFECT: chunking that shortens a number without changing what can be afforded."""
    nav = Rt.Until("g1", Rt.Act("A"), 8)
    plan = Rt.Seq(nav, Rt.Seq(Rt.Act("B"), Rt.Until("g2", Rt.Act("A"), 8)))
    assert Rt.length(plan, (nav,)) < Rt.length(plan), "a settled routine did not count as one unit"
    n, base = 3, 9 * math.log2(3)
    assert not pays(term_bits(Rt.length(plan), n), 0.0, base)
    assert pays(term_bits(Rt.length(plan, (nav,)), n), 0.0, base), (
        "chunking changed the length and not what the bargain affords")


def check_only_a_trial_refutes():
    """DEFECT: `I could not read the guard` recorded as `this plan does not work`."""
    ag = _agent()
    b = dict(ag.env.observe())
    slot = _wide(ag)
    ag.routine = Rt.Until(slot, Rt.Act("NOT_ADVERTISED"), 3)
    ag.routine_for = slot
    ag.choose(b)                              # ends `unadvertised` -- a non-trial
    assert not ag.refuted, "a non-trial was recorded as a refutation"


def check_refutations_do_not_cross_a_boundary():
    """DEFECT: rejecting a routine on a new level for what happened to a dead slot."""
    ag = _agent()
    slot = "o1.dcol"
    k = ag._reject_key(slot, Rt.Until(slot, Rt.Act("ACTION2"), 3))
    ag.refuted[k] = gamma.Standing(last_tick=0)
    ag.refuted[k].refute(0)
    ag.refuted_at[k] = 0.5
    ag.retarget(ag.env, ag.level + 1)
    assert not ag.refuted, "a refutation keyed on a dead slot name survived a boundary"


CHECKS = [v for k, v in sorted(globals().items()) if k.startswith("check_")]

if __name__ == "__main__":
    bad = []
    for fn in CHECKS:
        try:
            fn()
        except AssertionError as exc:
            bad.append(f"{fn.__name__}: {exc}")
    for line in bad:
        print("  FAIL", line)
    print(f"\n  {len(CHECKS) - len(bad)}/{len(CHECKS)} M2 checks pass")
    sys.exit(1 if bad else 0)
