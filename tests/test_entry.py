"""THE ENTRY SEAT -- the Kaggle path, offline, on a FAKE wrapper. No ARC board is touched.

The fake mirrors the real arc_agi wrappers where it matters here: it RESETS IN ITS OWN __init__
(both real ones do), holds the last frame as `observation_space`, and takes
`step(action, data=None, reasoning=None)`. Every command it receives is logged.

What this seat guards (the reviewer, 2026-10-06; Isaiah's 2026-09-29 ruling):
  1. `wire()` on a self-resetting wrapper issues EXACTLY ONE RESET -- F452/F454's fix, held;
  2. a planted RESET,RESET is REFUSED live (not sent, logged, counted);
  3. the same plant RAISES in strict mode -- the failure path is shown to fire;
  4. a RESET after a real action IS sent, and re-arms the guard -- so it refuses pairs, not resets.
"""
from __future__ import annotations

import logging
import pathlib
import sys

import numpy as np
from arcengine import FrameData, FrameDataRaw, GameAction, GameState

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
import arc_holdout

sys.dont_write_bytecode = True


class FakeWrapper:
    """A 64x64 board, one block the four directions move. `script` forces a state after N steps.
    At GAME_OVER or WIN it answers as the engine does (`perform_action`): any action but RESET
    returns a bare FrameData with an EMPTY stack and the state unchanged."""

    def __init__(self, script=None, actions=(1, 2, 3, 4, 6)):
        self.calls, self._last, self.script = [], None, dict(script or {})
        self.actions, self.pos, self.n = list(actions), [30, 30], 0
        self.reset()

    @property
    def observation_space(self):
        return self._last

    def _frame(self, state):
        g = np.zeros((64, 64), dtype=int)
        r, c = self.pos
        g[r:r + 4, c:c + 4] = 3
        g[5:9, 5:9] = 7
        f = FrameDataRaw(game_id="fake-0001", state=state, levels_completed=0, win_levels=2,
                         guid="g", available_actions=list(self.actions))
        f.frame = [g]
        self._last = f
        return f

    def reset(self):
        self.calls.append("RESET")
        self.pos = [30, 30]
        return self._frame(GameState.NOT_FINISHED)

    def step(self, action, data=None, reasoning=None):
        self.calls.append(action.name)
        self.last_data, self.last_reasoning = data, reasoning   # what a click actually carried
        ended = self._last.state in (GameState.GAME_OVER, GameState.WIN)
        if ended and action is not GameAction.RESET:
            self._last = FrameData(game_id="fake-0001", frame=[], state=self._last.state,
                                   available_actions=list(self.actions))
            return self._last
        if action is GameAction.RESET:
            self.pos = [30, 30]
            return self._frame(GameState.NOT_FINISHED)
        self.n += 1
        d = {1: (-2, 0), 2: (2, 0), 3: (0, -2), 4: (0, 2)}.get(action.value)
        if d:
            self.pos = [min(max(self.pos[0] + d[0], 0), 60), min(max(self.pos[1] + d[1], 0), 60)]
        return self._frame(self.script.get(self.n, GameState.NOT_FINISHED))


def check_wire_issues_one_reset():
    w = FakeWrapper()
    env = arc_holdout.wire(w, "fake")[0]
    assert w.calls == ["RESET"], f"construction sent {w.calls}; Isaiah: never RESET,RESET"
    assert isinstance(env.w, arc_holdout.ResetGuard), "ArcWorld is not behind the guard"


def check_planted_pair_is_refused_live():
    w = FakeWrapper()
    g = arc_holdout.ResetGuard(w)
    logging.disable(logging.ERROR)
    try:
        g.reset()
        g.step(GameAction.RESET)
    finally:
        logging.disable(logging.NOTSET)
    assert w.calls == ["RESET"], f"a second RESET reached the wrapper: {w.calls}"
    assert g.refused == 2, f"refusals not counted: {g.refused}"


def check_planted_pair_raises_in_strict_mode():
    g = arc_holdout.ResetGuard(FakeWrapper(), strict=True)
    try:
        g.reset()
    except RuntimeError:
        return
    raise AssertionError("strict mode let RESET,RESET through without raising")


def check_reset_after_an_action_is_sent_and_rearms():
    w = FakeWrapper()
    g = arc_holdout.ResetGuard(w, strict=True)
    g.step(GameAction.ACTION1)
    g.step(GameAction.RESET)
    assert w.calls == ["RESET", "ACTION1", "RESET"], f"a lawful RESET was not sent: {w.calls}"
    try:
        g.reset()
    except RuntimeError:
        return
    raise AssertionError("the guard did not re-arm after a sent RESET")


def check_a_death_is_survived_by_the_agents_own_reset():
    """GAME_OVER (F478; Isaiah 2026-09-29): a death no longer ends the run. The ENTRY POINT
    never presses RESET -- every RESET past its one at construction is the AGENT's -- the agent
    is not stranded short of RESET, and no RESET,RESET pair reaches the wrapper."""
    import tether_agent
    w = FakeWrapper(script={2: GameState.GAME_OVER})
    out = tether_agent.run(w, "fake", max_actions=8)
    assert out["deaths"] == 1 and out["acted"] > 2, f"the run ended at the death: {out}"
    assert out["agent_resets"] >= 1 and out["end"] != "death", f"stranded after a death: {out}"
    assert w.calls.count("RESET") == 1 + out["agent_resets"], f"the entry point pressed: {w.calls}"
    assert ("RESET", "RESET") not in zip(w.calls[:-1], w.calls[1:], strict=True), (
        f"RESET,RESET sent: {w.calls}")


def check_a_press_after_a_death_keeps_the_board():
    """At GAME_OVER the engine answers a non-RESET press with an EMPTY stack. Read as "no
    board", the agent saw no slots and never acted again -- short of RESET. The world keeps the
    last board and takes only the state from the answer."""
    w = FakeWrapper(script={2: GameState.GAME_OVER})
    env = arc_holdout.wire(w, "fake")[0]
    env.step("ACTION1")
    env.step("ACTION2")
    board, levels = env.board(), env.levels()
    assert env.terminal() == "death" and board is not None, "no death to press after"
    env.step("ACTION3")
    assert w.observation_space.is_empty(), "the treatment: the engine's answer was not empty"
    assert env.board() is not None and (env.board() == board).all(), "the dead press lost the board"
    assert env.terminal() == "death" and env.levels() == levels, (env.terminal(), env.levels())
    assert env.observe(), "the dead press left no slots"
    # THE OTHER READING STAYS REACHABLE: an empty answer while the game is LIVE may be a dead
    # channel, so it still reads as no board -- never quietly as "nothing changed".
    live = FakeWrapper()
    env = arc_holdout.wire(live, "fake")[0]
    live.step = lambda *_a, **_k: FrameData(game_id="fake-0001", frame=[],
                                            state=GameState.NOT_FINISHED)
    env.step("ACTION1")
    assert env.board() is None, "an empty answer in a live game was read as nothing changed"

class TwinWrapper(FakeWrapper):
    """Two LOOK-ALIKE blocks (one shape, colour ignored by design) that BOTH move far enough to
    leave no overlap, so a RESET re-finds both by shape -- the case where names can swap."""

    def _frame(self, state):
        g = np.zeros((64, 64), dtype=int)
        r, c = self.pos
        g[r:r + 4, c:c + 4] = 3
        g[r + 20:r + 24, c:c + 4] = 3
        f = FrameDataRaw(game_id="twin-0001", state=state, levels_completed=0, win_levels=2,
                         guid="g", available_actions=list(self.actions))
        f.frame = [g]
        self._last = f
        return f


def _held_then_restarted(w, moves, how="death"):
    """A refutation filed on every tracked object's slot, a boundary of kind `how`, RESET, and the
    agent told the level restarted -- the order the entry loop produces."""
    import gamma
    env, ag = arc_holdout.wire(w, "fake")[:2]
    for a in moves:
        env.step(a)
    keys = [(f"{o}.row", (), ()) for o in sorted(env._decompose.tracked)]
    for k in keys:
        ag.refuted[k], ag.refuted_at[k] = gamma.Standing(last_tick=0), 1.0
    ag.retarget(env, env.levels()[0], how=how)
    env.step("RESET")
    ag.restarted(env)
    row = [e for e in ag.led.entries if e.event == "restart"]
    return env, ag, keys, (row[-1].detail if row else None)


def check_a_restart_carries_refutations_only_where_identity_is_sure():
    """F479 (the reviewer, 2026-10-06): a death's boundary HOLDS the slot-keyed refutations and a
    restart of the same level carries each back only where every object it names was re-found
    unambiguously. Twins re-found by shape may have swapped: never carried, and named."""
    env, ag, keys, row = _held_then_restarted(
        FakeWrapper(), ["ACTION2", "ACTION2", "ACTION4", "ACTION4", "ACTION4"])
    assert keys, "precondition: the tracker held no object, so no refutation was planted"
    assert all(k in ag.refuted for k in keys), f"a sure identity was not carried: {row}"
    assert row and sorted(row["carried"]) == sorted(k[0] for k in keys) and not row["not_carried"]
    # ACROSS AN ADVANCE NOTHING IS HELD: section 18.2's autoimmunity, unchanged.
    _e, ag2, k2, row2 = _held_then_restarted(FakeWrapper(), ["ACTION2"], how="level_advance")
    assert k2, "precondition: no refutation was planted before the ADVANCE"
    assert not ag2.refuted and row2 is None, "a refutation crossed an ADVANCE"
    # THE TWINS: both moved off their start, both re-found by shape -> neither carried, both named.
    env, ag, keys, row = _held_then_restarted(TwinWrapper(), ["ACTION4"] * 4)
    twins = sorted(o for o in env._decompose.tracked if env.identity(o) == "look-alike")
    assert len(twins) == 2, f"fixture: the twins were not both re-found by shape: {twins}"
    assert not any(k in ag.refuted for k in keys if k[0].split(".")[0] in twins), (
        "a refutation landed on a look-alike")
    assert sorted(row["not_carried"]) == sorted(f"{o}.row" for o in twins), row

def check_nothing_unknown_here_is_priced_by_the_agent():
    """DESIGN A (F480; the reviewer, 2026-10-06): when exploration has nothing left to learn in a
    context, the interface REPORTS each known effect and the AGENT prices and chooses -- a
    restart costs the actions spent since the level began (Fig 12), and only an effect that
    changes the board can reach a gap elsewhere (Fig 5). The interface presses nothing itself."""
    import interface as IF
    ag = arc_holdout.wire(FakeWrapper(), "fake")[1]
    move, dead, restart = IF.CHANGES, IF.NO_EFFECT, IF.RESTARTS
    ag._attempt_actions = 5
    assert ag._choose_known([(restart, 0), (move, 3), (dead, 0)])[0] == 1, "a restart beat a move"
    assert ag._choose_known([(dead, 0), (restart, 0)])[0] == 1, "dead presses beat a restart"
    assert ag._choose_known([(move, 4), (move, 1)])[0] == 1, "variety lost among equal moves"
    # THE INTERFACE: everything known here -> the agent's choice, named, and nothing else.
    iface, ctx = IF.Interface(), ("ctx",)
    iface.table = {"ACTION1": {"by_ctx": {ctx: {(("o0.row", 1),)}}, "n": 1, "delta": {}},
                   "RESET": {"by_ctx": {ctx: {(("o0.row", -1),)}}, "n": 1, "delta": {}}}
    iface.chooser = lambda known: (1, f"picked {known[1][0]}")
    r = iface.realise(IF.Intent(IF.ELICIT), ("ACTION1", "RESET"), ctx, {}, None)
    assert r.action == "RESET" and "nothing unknown here; picked restarts the level" in r.why, r

def check_shape_readings_are_keyed_on_the_cells():
    """F481: a shape reading is perceived once per (reading, cell set) per frame. Two shapes with
    the SAME cell count -- a line and an L -- must not share a reading, a recomputation must agree
    with the memo, and a new frame clears it."""
    import arc_atoms
    import arc_predict
    import gamma
    atoms = {a.name: a for a in arc_atoms.three_spaces(arc_predict.predict())}
    line = frozenset((0, c) for c in range(4))
    ell = frozenset({(0, 0), (1, 0), (2, 0), (2, 1)})
    ctx = gamma.Ctx()
    arc_atoms.new_frame()
    a = [atoms[n].fn(line, ctx) for n in ("corners", "orbit_size", "perimeter")]
    b = [atoms[n].fn(ell, ctx) for n in ("corners", "orbit_size", "perimeter")]
    assert a != b, f"a line and an L of equal size shared their readings: {a} {b}"
    arc_atoms.new_frame()
    assert [atoms[n].fn(ell, ctx) for n in ("corners", "orbit_size", "perimeter")] == b
    env = arc_holdout.wire(FakeWrapper(), "fake")[0]
    atoms["corners"].fn(line, ctx)
    assert arc_atoms._SHAPE_MEMO, "precondition: the corners reading left nothing to clear"
    env.step("ACTION1")
    assert not arc_atoms._SHAPE_MEMO, "a new frame kept the last frame's shape readings"

def check_a_win_ends_the_run():
    import tether_agent
    w = FakeWrapper(script={2: GameState.WIN})
    out = tether_agent.run(w, "fake", max_actions=6)
    assert out["end"] == "game_win", f"a WIN did not end the run: {out}"
    assert w.calls.count("RESET") == 1, f"RESET sent around a win: {w.calls}"


def check_a_click_carries_its_position():
    """Interface bug 3, on the path the entry point uses: ACTION6 with x, y reaches the wrapper
    as `data` -- `set_data` belongs to the GameAction-object path an overridden main() bypasses."""
    w = FakeWrapper()
    env = arc_holdout.wire(w, "fake")[0]
    env.step("ACTION6", 12, 34)
    assert w.calls[-1] == "ACTION6" and w.last_data == {"x": 12, "y": 34}, (
        f"the click arrived as {w.calls[-1]} {w.last_data}")


def check_run_saves_after_a_death_a_win_and_the_cap():
    """THE ENTRY POINT CARRIES (F471): with a library path, run() keeps the game's library
    whatever ended it -- a death, a win, or the cap. Without one it saves nothing."""
    import pathlib
    import tempfile

    import tether_agent
    with tempfile.TemporaryDirectory() as d:
        for i, script in enumerate(({2: GameState.GAME_OVER}, {2: GameState.WIN}, {})):
            path = str(pathlib.Path(d) / f"lib{i}.json")
            out = tether_agent.run(FakeWrapper(script=script), "fake", max_actions=4,
                                   library=path)
            # the planted ending happened (the save itself does not depend on it)
            assert (out["deaths"] >= 1, out["end"] == "game_win", out["end"] == "cap")[i], (i, out)
            assert out["saved"] and pathlib.Path(path).exists(), f"not kept after {out['end']}"
        out = tether_agent.run(FakeWrapper(), "fake", max_actions=2)
        assert out["saved"] is None, "a run with no library path saved something"


def check_a_save_killed_midway_leaves_the_previous_library_whole():
    """ATOMIC (F471): a save interrupted mid-write -- the platform's time limit -- must leave
    the library already on disk intact and loadable, never a half-written one."""
    import pathlib
    import tempfile

    import gamma
    inc = gamma.Atom("inc", lambda v, _c: v + 1, "val", "val")
    g = gamma.Gamma([inc], game="A")
    g.accept(gamma.Term(atoms=(inc, inc)), seq=0, residual="s@0")
    with tempfile.TemporaryDirectory() as d:
        path = str(pathlib.Path(d) / "lib.json")
        g.save(path)
        before = pathlib.Path(path).read_text(encoding="utf-8")
        real = pathlib.Path.write_text
        fired = []

        def dies(self, data, *a, **k):
            fired.append(1)
            real(self, data[: len(data) // 2], *a, **k)
            raise KeyboardInterrupt("killed mid-save")
        pathlib.Path.write_text = dies
        try:
            g.save(path)
        except KeyboardInterrupt:
            pass
        finally:
            pathlib.Path.write_text = real
        assert fired, "precondition: the save never called the killed write"
        assert pathlib.Path(path).read_text(encoding="utf-8") == before, "a kill tore the library"
        rep = gamma.Gamma([inc], game="B").load(path)
        assert rep.get("loaded") == 1 and not rep.get("cold"), rep


def check_an_unreadable_library_loads_cold_and_says_so():
    """A missing or unreadable library is a COLD start, reported -- never a crash (F471)."""
    import pathlib
    import tempfile

    import gamma
    inc = gamma.Atom("inc", lambda v, _c: v + 1, "val", "val")
    with tempfile.TemporaryDirectory() as d:
        path = pathlib.Path(d) / "lib.json"
        path.write_text('{"terms": [', encoding="utf-8")
        rep = gamma.Gamma([inc], game="A").load(str(path))
    assert rep.get("loaded") == 0 and rep.get("cold"), rep


def check_the_census_is_never_an_input():
    """13.3 (the reviewer 2026-10-16 14:49): the game-type census is a READING, never an input --
    no repository .py file but this check names its folder or file, so no agent code can load it."""
    here = pathlib.Path(_repo.ROOT)
    hits = [str(f.relative_to(here)) for f in here.rglob("*.py")
            if ".venv" not in f.parts and f.name != "test_entry.py"
            and any(t in f.read_text(encoding="utf-8", errors="replace")
                    for t in ("docs/census", r"docs\census", "GAME_TYPE_CENSUS"))]
    assert not hits, hits


if __name__ == "__main__":
    # C-seed-X, RESTORED 2026-10-15 19:42 (the reviewer 19:36): the per-commit smoke must be
    # deterministic, and two more checks are draw-dependent under the agent's own seed
    # (D-WIN-RESET, D-RESET-COUNT); 9355d51's and f72ce8f's smokes passed by the draw
    import tether
    tether._AGENT_SEED = False
    checks = [v for k, v in sorted(globals().items()) if k.startswith("check_")]
    for fn in checks:
        fn()
    print(f"entry: {len(checks)} checks passed")
