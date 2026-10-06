"""THE KAGGLE ENTRY POINT'S LOOP (14a) -- harness-free, so it imports nothing from ARC-AGI-3-Agents.

The reference `Agent.main()` owns a push loop (`choose_action` returns an action and the harness
sends it); tether's loop is pull (`Agent.step()` acts on its world). The subclass the bundler
appends overrides `main()` and calls `run()` here, which drives tether one step at a time through
`arc_holdout.wire()` -- the SAME wiring `play` uses, so the two cannot drift. No threads, no
inversion, and it runs the same under Swarm's threads or under a runner of our own.

GAME_OVER: the entry point NEVER sends RESET (the who-presses rule). A death does NOT end the
run: the boundary is marked and play goes on, and the AGENT may choose the platform's RESET
(Isaiah 2026-09-29; F477, F478). Only a WIN, the step cap or the time allowance ends a game.
"""
from __future__ import annotations

import sys
import time

import arc_holdout

sys.dont_write_bytecode = True


def run(w, game: str, max_actions: int, *, on_action=None, library: str | None = None,
        cfg=None, led_path: str | None = None, deadline: float | None = None) -> dict:
    """Play one game on wrapper `w` until WIN, `max_actions` loop steps, or the deadline.

    `on_action(frame)` is called with the wrapper's frame after every step that acted -- the
    subclass uses it to keep `Agent.frames` and `action_counter` true. The step cap is the
    harness's own `MAX_ACTIONS`: a termination bound, never a prior.
    """
    env, ag, led, board, palette, loaded = arc_holdout.wire(w, game, cfg=cfg, led_path=led_path,
                                                            library=library)
    acted_n, was, end, deaths = 0, "", "", 0
    for _ in range(max_actions):
        # A WALL-CLOCK BOUND, like the step cap: the runner's per-game allowance, never a prior.
        if deadline is not None and time.time() >= deadline:
            end = end or "time"
            break
        env.observe()
        acted = ag.step()
        if acted:
            acted_n += 1
            if on_action is not None:
                on_action(w.observation_space)
        end = env.terminal()
        if end and end != was:
            ag.retarget(env, env.levels()[0], how=end)
            deaths += end == "death"
        was = end
        if end == "advance":    # WIN: the game is over and won. A death is not an end.
            break
    # THE GAME'S LIBRARY IS KEPT for the next game in this worker's sequence -- after WIN,
    # death or cap alike. No path, no save: a run with no sequence stays cold (F471).
    saved = ag.gamma.save(library) if library else None
    return {"game": game, "acted": acted_n, "cycles": ag.cycle, "end": end or "cap",
            "deaths": deaths, "agent_resets": ag._acts.get("RESET", 0),
            "levels": env.levels(), "refused_resets": getattr(env.w, "refused", 0),
            "loaded": loaded, "saved": saved}
