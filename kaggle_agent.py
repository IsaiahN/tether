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


# ---- THE RUNNER ENTRY (F473): `python -m agents.templates.my_agent`, run where main.py runs. ----
# Environment and ROOT_URL exactly as the kit's main.py builds them, so the gateway sees the same
# client; the orchestration itself is tether_runner.serve(), harness-free and tested offline.

def _root_url() -> str:
    import os
    scheme, host, port = (os.environ.get("SCHEME", "http"), os.environ.get("HOST", "localhost"),
                          os.environ.get("PORT", 8001))
    if (scheme == "http" and str(port) == "80") or (scheme == "https" and str(port) == "443"):
        return f"{scheme}://{host}"
    return f"{scheme}://{host}:{port}"


def make_env(game: str, card: str):
    """Module-level, so a worker PROCESS can take it: each process builds its OWN client."""
    from arc_agi import Arcade
    return Arcade().make(game, scorecard_id=card)


def runner_main(lib_dir: str = "/kaggle/working/tether_libs") -> dict:
    import json
    import os

    import requests
    from arc_agi import Arcade
    from dotenv import load_dotenv

    import tether_runner
    load_dotenv(dotenv_path=".env.example")
    load_dotenv(dotenv_path=".env", override=True)
    root = _root_url()
    headers = {"X-API-Key": os.getenv("ARC_API_KEY", ""), "Accept": "application/json"}
    arc = Arcade()

    def games():
        r = requests.get(f"{root}/api/games", headers=headers, timeout=10)
        r.raise_for_status()
        return [g["game_id"] for g in r.json()]

    rec = tether_runner.serve(games, lambda: arc.open_scorecard(tags=["agent", "tether"]),
                              arc.close_scorecard, make_env, lib_dir)
    with open(os.path.join(lib_dir, "run_record.json"), "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1, default=str)
    return rec


if __name__ == "__main__":
    runner_main()
