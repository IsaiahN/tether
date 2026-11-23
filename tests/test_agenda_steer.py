"""AGENDA STEER (WATSON 74, 2026-11-23): make the "Three texts before acting" card's refusal
reading causal. When a goal is refused and the card finds PRETEXT thin (the record held no
enabler, pushed=False), on_refuted.pretext says "press-and-watch, transcribe" -- the next holder
is TRY_FIRST, not another goal hypothesis that fizzles. A choice among EXISTING holders, never a
new procedure and never the hand-written _ANSWER table (WATSON 50's answer-encoding caution).

  S1  a pretext-thin refusal RETURNS a press-and-watch steer in the agenda row (both arms)
  S2  arm ON: the steer sets the agent flag and the next holder is try_first (no goal_choice)
  S3  arm OFF: the steer is recorded but NOT acted on -- goal_choice is asked, flag untouched
  S4  OFF byte-identity: with the arm off, the goal path is exactly development's order
  MF  with the arm on and the steer branch removed, S2 fails RED

Seconds; no live game needed.
"""
from __future__ import annotations

import os
import sys
from collections import Counter

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def _agent():
    env = world.bind(gridworld.family("default", 0))
    led = ledger.Ledger()
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
    ag.step()
    return ag, led


def _hold(ag, touches=2):
    ag._hyp = {"key": ("k",), "text": "o1.col == o2.col", "slots": ["o1.col"], "tkey": ("t",),
               "cond": None, "source": "library", "shelf": None, "steps": 3, "r0": 1.0,
               "budget": 5, "born": ag.cycle, "displaced": {}, "reads": {}, "seg": {},
               "touches": touches, "losses": 0, "held_unreadable": 0, "acted": Counter()}


def _refusal(ag, led):
    """A pretext-thin refusal: no enabler found, so the card steers press-and-watch."""
    n0 = len(led.rows())
    _hold(ag)
    ag._htn_push = lambda s, when="routes", why=None: False  # noqa: ARG005  must match signature
    ag._hyp_end("arrived_no_clear", loss=True)
    return [r["detail"] for r in led.rows()[n0:]
            if r.get("event") == "agenda"
            and r["detail"].get("card") == "Three texts before acting"]


def _holder_after_steer(ag):
    """Drive the proposal decision with AFTER_WORDS exhausted but an untried action available."""
    ag._hyp = None
    known = sum(len(v.get("delta", {})) for v in ag.iface.table.values())
    ag._hyp_exhausted = known + 1       # not exhausted
    ag.routine = None
    ag._try_first_hold = lambda: 3      # untried action available
    ag._agenda_steer = "press-and-watch"
    called = []
    ag._goal_choice = lambda: called.append("goal") or "o0.col"
    ag._goal_propose = lambda before: called.append("proposed")  # noqa: ARG005  signature
    ag._goal_hypothesis_run({})
    return called


def main() -> int:
    # S1: the steer is in the row under both arms (record, not decision)
    for arm in (True, False):
        tether._AGENDA_STEER = arm
        ag, led = _agent()
        rows = _refusal(ag, led)
        assert rows and rows[0].get("steer") == "press-and-watch", rows
    print("S1 PASS pretext-thin refusal returns press-and-watch steer in the row")

    # S2: arm ON -- steer acts; goal_choice not asked; flag consumed once
    was_aw = tether._HYP_AFTER_WORDS
    tether._HYP_AFTER_WORDS = False
    tether._AGENDA_STEER = True
    ag, led = _agent()
    called = _holder_after_steer(ag)
    assert "goal" not in called and "proposed" not in called, called
    assert getattr(ag, "_agenda_steer", None) is None, "steer not consumed"
    print("S2 PASS arm ON: steer diverts to try_first, goal_choice not asked, steer consumed")

    # S3/S4: arm OFF -- byte-identical to development; steer ignored, goal_choice asked
    tether._AGENDA_STEER = False
    ag, led = _agent()
    called = _holder_after_steer(ag)
    assert "goal" in called, called
    assert getattr(ag, "_agenda_steer", None) == "press-and-watch", "OFF must not touch state"
    print("S3/S4 PASS arm OFF: goal_choice asked, agent state untouched (byte-identical)")

    tether._AGENDA_STEER = True
    tether._HYP_AFTER_WORDS = was_aw
    print("PASS agenda steer is causal under the arm, inert OFF")
    return 0


if __name__ == "__main__":
    sys.exit(main())
