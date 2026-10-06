"""THE KAGGLE ENTRY POINT'S LOOP (14a) -- harness-free, so it imports nothing from ARC-AGI-3-Agents.

The reference `Agent.main()` owns a push loop (`choose_action` returns an action and the harness
sends it); tether's loop is pull (`Agent.step()` acts on its world). The subclass the bundler
appends overrides `main()` and calls `run()` here, which drives tether one step at a time through
`arc_holdout.wire()` -- the SAME wiring `play` uses, so the two cannot drift. No threads, no
inversion, and it runs the same under Swarm's threads or under a runner of our own.

GAME_OVER: the entry point NEVER sends RESET (the who-presses rule, INDEX "ResetGate AS A STATE
CONDITION"; the reviewer, 2026-10-06). Whether the AGENT may choose RESET after a death is with
Isaiah (F450). Until he rules, a death ENDS the run -- `ON_GAME_OVER = "stop"`.
"""
from __future__ import annotations

import sys

import arc_holdout

sys.dont_write_bytecode = True

ON_GAME_OVER = "stop"   # the only value until Isaiah rules on offering RESET to the agent (F450)


def run(w, game: str, max_actions: int, *, on_action=None, library: str | None = None,
        cfg=None, led_path: str | None = None) -> dict:
    """Play one game on wrapper `w` until WIN, the first death, or `max_actions` loop steps.

    `on_action(frame)` is called with the wrapper's frame after every step that acted -- the
    subclass uses it to keep `Agent.frames` and `action_counter` true. The step cap is the
    harness's own `MAX_ACTIONS`: a termination bound, never a prior.
    """
    if ON_GAME_OVER != "stop":
        raise ValueError(f"ON_GAME_OVER={ON_GAME_OVER!r} has no ruling behind it (F450)")
    env, ag, led, board, palette, loaded = arc_holdout.wire(w, game, cfg=cfg, led_path=led_path,
                                                            library=library)
    acted_n, was, end = 0, "", ""
    for _ in range(max_actions):
        env.observe()
        acted = ag.step()
        if acted:
            acted_n += 1
            if on_action is not None:
                on_action(w.observation_space)
        end = env.terminal()
        if end and end != was:
            ag.retarget(env, env.levels()[0], how=end)
        was = end
        if end:
            break
    return {"game": game, "acted": acted_n, "cycles": ag.cycle, "end": end or "cap",
            "levels": env.levels(), "refused_resets": getattr(env.w, "refused", 0)}
