"""THE KAGGLE AGENT CLASS (14a) -- the one piece that imports the harness, so the repository never
does. `kaggle_bundle.py` appends this file to the one-file bundle as `my_agent.py`, the file the
notebook copies into `agents/templates/`; nothing in the repository imports it.

The reference `Agent.main()` owns a push loop; tether's is pull. So `main()` is OVERRIDDEN to call
`tether_agent.run()`, which drives tether one step at a time on `self.arc_env` through
`arc_holdout.wire()`. `on_action` keeps `self.frames` and `self.action_counter` true, so `is_done`,
`state`, `levels_completed`, the recorder and `cleanup()` read what actually happened.

`choose_action` exists only because the base class declares it abstract: with `main()` overridden
nothing calls it, and a call would mean the harness changed under us -- so it RAISES.
"""
from __future__ import annotations

import time

from agents.agent import Agent
from arcengine import FrameData, GameAction, GameState

import tether_agent

# PLACEHOLDER, NOT A RULING: the reviewer's 25 games x 500 actions. Actions per game is one of the
# numbers with Isaiah (F450). It is a termination bound -- `run()` ends sooner on WIN or a death.
# anchor: the reviewer's ceiling placeholder, 28,800 s / (25 games x 500 actions), 2026-10-05;
# Isaiah has the real actions-per-game. A termination bound, not a tuned value.
MAX_ACTIONS_PER_GAME = 500


class MyAgent(Agent):
    """tether, one game per instance."""

    MAX_ACTIONS = MAX_ACTIONS_PER_GAME

    def main(self) -> None:
        self.timer = time.time()

        def took(raw) -> None:
            if raw is not None:
                self.append_frame(self._convert_raw_frame_data(raw))
            self.action_counter += 1

        self.tether_report = tether_agent.run(self.arc_env, self.game_id, self.MAX_ACTIONS,
                                              on_action=took)
        self.cleanup()

    def is_done(self, frames: list[FrameData],  # noqa: ARG002 -- the base class's signature
                latest_frame: FrameData) -> bool:
        return latest_frame.state is GameState.WIN

    def choose_action(self, frames: list[FrameData], latest_frame: FrameData) -> GameAction:
        raise NotImplementedError("main() is overridden: tether drives the wrapper itself (14a)")
