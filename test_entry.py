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
import sys

import numpy as np
from arcengine import FrameDataRaw, GameAction, GameState

import arc_holdout

sys.dont_write_bytecode = True


class FakeWrapper:
    """A 64x64 board, one block the four directions move. `script` forces a state after N steps."""

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



def check_a_death_ends_the_run_with_one_reset():
    """GAME_OVER: the entry point never sends RESET (who-presses rule); until Isaiah rules on
    offering RESET to the agent (F450), a death ENDS the run."""
    import tether_agent
    w = FakeWrapper(script={2: GameState.GAME_OVER})
    out = tether_agent.run(w, "fake", max_actions=6)
    assert out["end"] == "death", f"a death did not end the run: {out}"
    assert w.calls.count("RESET") == 1, f"RESET sent around a death: {w.calls}"
    assert out["acted"] == 2, f"acted past the death: {out}"


def check_a_win_ends_the_run():
    import tether_agent
    w = FakeWrapper(script={2: GameState.WIN})
    out = tether_agent.run(w, "fake", max_actions=6)
    assert out["end"] == "advance", f"a WIN did not end the run: {out}"
    assert w.calls.count("RESET") == 1, f"RESET sent around a win: {w.calls}"


def check_a_click_carries_its_position():
    """Interface bug 3, on the path the entry point uses: ACTION6 with x, y reaches the wrapper
    as `data` -- `set_data` belongs to the GameAction-object path an overridden main() bypasses."""
    w = FakeWrapper()
    env = arc_holdout.wire(w, "fake")[0]
    env.step("ACTION6", 12, 34)
    assert w.calls[-1] == "ACTION6" and w.last_data == {"x": 12, "y": 34}, (
        f"the click arrived as {w.calls[-1]} {w.last_data}")


if __name__ == "__main__":
    checks = [v for k, v in sorted(globals().items()) if k.startswith("check_")]
    for fn in checks:
        fn()
    print(f"entry: {len(checks)} checks passed")
