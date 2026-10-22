"""B, DIRECTION MOVABLE (the reviewer 2026-10-12 05:43, 05:47 CDT): synthetic steps fed straight to
_note_direction, one controlled owner (o0, by contingency), the agent's own pair slots present.
  m. a clock that moves +1 under every action reads NOT movable (refuter clause 2 has no world of
     ours that can fire it, so it is tested here);
  p. a distance that falls under one action and rises under another, in one ctx, reads movable;
  x. a slot seen both ways under each action (mixed cells only) reads NOT movable: abstention;
  c. KNOWN LIMITATION, asserted as today's behaviour: a mover that bounces +1/-1 by step while the
     agent alternates two actions reads MOVABLE, because purity can come from one observation per
     cell. contingent() has the same action-time confound (its always/never is read from whatever
     was observed). If a later change fixes it, this assertion is what flips, visibly;
  off. with the arm OFF the reading is today's (not movable: o5 is not contingent);
  scope. the type-scope note is written to the ledger once.
MUST-FAIL: mx1 (a mixed cell treated as pure) makes x read movable; mx2 (one pure nonzero cell
enough, no second action) makes m read movable. Both must be caught.
    python tests/test_direction_movable.py
"""
from __future__ import annotations

import os
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(_repo.ROOT, "conform"))
import panel  # noqa: E402

import gamma  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

CTX = {"o0.drow_o5": 1, "o0.dcol_o5": -1}


def _agent():
    g, seed = panel._gridworld("gridworld_s0")
    env = world.bind(g)
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game=f"dm_{seed}"), tether.Config(),
                      ledger.Ledger())
    for s in ("o5.clock", "o5.distance", "o5.noise", "o5.bounce"):
        ag.slot_types[s] = "EXTENT"
    ag.agency.tried[("o0.row", "up")] = ag.agency.moved[("o0.row", "up")] = 2
    ag.agency.tried[("o0.row", "left")] = 2                 # never moved: o0.row is contingent
    assert ag.agency.contingent() == ["o0.row"]
    return ag


def _step(ag, action, slot, frm, to):
    ag._note_direction(action, {**CTX, slot: frm}, {**CTX, slot: to}, [slot])


def _feed(ag):
    for a in ("up", "down", "left", "right", "up", "left"):
        _step(ag, a, "o5.clock", 3, 4)
    for _ in range(2):
        _step(ag, "left", "o5.distance", 5, 4)
        _step(ag, "right", "o5.distance", 4, 5)
    for a in ("left", "right"):
        _step(ag, a, "o5.noise", 2, 3)
        _step(ag, a, "o5.noise", 3, 2)
    for i in range(4):
        a, d = ("up", 1) if i % 2 == 0 else ("down", -1)
        _step(ag, a, "o5.bounce", 5, 5 + d)


def _readings(ag):
    return {s: ag._moves_by_direction(s) for s in ("o5.clock", "o5.distance", "o5.noise",
                                                   "o5.bounce")}


if __name__ == "__main__":
    tether._DIRECTION_MOVABLE = True
    ag = _agent()
    _feed(ag)
    r = _readings(ag)
    assert r["o5.clock"] is False, "m: a regardless-of-action changer read movable"
    assert r["o5.distance"] is True, "p: a second-order slot read not movable"
    assert r["o5.noise"] is False, "x: mixed cells did not abstain"
    assert r["o5.bounce"] is True, "c: the documented confound no longer reads movable -- if a " \
                                   "fix landed, update this assertion and the docstring"
    assert ag._movable_by("o5.distance") == "direction" and ag._moves_by_sources("o5.distance")
    rows = [x for x in ag.led.rows() if x["event"] == "direction_scope"]
    assert len(rows) == 1, f"scope: expected one note, got {len(rows)}"
    tether._DIRECTION_MOVABLE = False
    assert ag._moves_by_sources("o5.distance") is False, "off: the arm OFF changed the reading"
    tether._DIRECTION_MOVABLE = True
    real = tether.Agent._moves_by_direction

    def mx1(self, slot):                  # mutant: a mixed cell counts as if pure
        by_ctx: dict = {}
        for (_a, ctx), signs in self._dir.get(slot, {}).items():
            by_ctx.setdefault(ctx, set()).update(signs)
        return any(len(v) > 1 for v in by_ctx.values())

    def mx2(self, slot):                  # mutant: one pure nonzero cell is enough
        return any(len(s) == 1 and next(iter(s)) != 0 for s in self._dir.get(slot, {}).values())

    caught = []
    for name, fn, case, want in (("mx1", mx1, "o5.noise", False), ("mx2", mx2, "o5.clock", False)):
        tether.Agent._moves_by_direction = fn
        try:
            caught.append((name, ag._moves_by_direction(case) != want))
        finally:
            tether.Agent._moves_by_direction = real
    assert all(c for _n, c in caught), f"a mutant was not caught: {caught}"
    tether._DIRECTION_MOVABLE = False
    print(f"test_direction_movable: m, p, x hold; c (the confound) reads movable as documented; "
          f"off unchanged; scope noted once; mutants caught: {[n for n, c in caught if c]}")
