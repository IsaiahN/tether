"""BUILD 4 ITEM 12: TETHER_WANT_TARGET_SUBJECT DEFAULT ON (the reviewer 2026-11-04 r1152). Off since
10-11 "pending a reading"; read: every caller of Agent._target_lookup sits behind "if _WANT_TARGET
else", and TETHER_WANT_TARGET is default ON, so the arm is the dormant fallback for the day the full
unmask is off. Seconds: a gridworld agent, one slot, the lookup called directly.

MF-T1  with TETHER_WANT_TARGET forced OFF, a slot holding a bound val predictor (inc) AND a
       subject-scoped want: the arm ON reads the want through _objective_of; forced OFF, the
       bound predictor masks it
MF-T2  an OWN want (not subject-scoped) stays masked with the arm on
MF-T3  with TETHER_WANT_TARGET on, _goal_target never calls _target_lookup (subsumed)
The red is behavioural, the arm OFF on this tree: TETHER_WANT_TARGET_SUBJECT=0 fails MF-T1.

    python tests/test_want_subject_default.py
"""
from __future__ import annotations

import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402
from gamma import Term  # noqa: E402

SLOT, WANT = "o0.row", "want_o0_row"


def agent(scoped: bool):
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                      ledger.Ledger())
    dec = next(a for a in ag.gamma.atoms if a.name == "dec")
    ag.bound = {SLOT: "inc"}
    ag.wants = {SLOT: WANT}
    ag._want_terms = {SLOT: Term((dec,))}
    ag._want_scope = {SLOT: WANT} if scoped else {}
    return ag


def main():
    keep = (tether._WANT_TARGET, tether._WANT_TARGET_SUBJECT)
    try:
        tether._WANT_TARGET = False
        on = agent(True)._target_lookup(SLOT)
        tether._WANT_TARGET_SUBJECT = False
        off = agent(True)._target_lookup(SLOT)
        tether._WANT_TARGET_SUBJECT = keep[1]
        own = agent(False)._target_lookup(SLOT)
    finally:
        tether._WANT_TARGET, tether._WANT_TARGET_SUBJECT = keep
    assert on[0] == WANT and off[0] == "inc", (
        "MF-T1: the subject-scoped want is not read", on, off)
    assert own[0] == "inc", ("MF-T2: an own want was unmasked", own)
    print(f"  MF-T1 WANT_TARGET off: arm ON reads {on[0]!r}, OFF reads the masking {off[0]!r}")
    print(f"  MF-T2 an own want stays masked: {own[0]!r}")
    ag = agent(True)
    calls = []
    real = ag._target_lookup
    ag._target_lookup = lambda s: calls.append(s) or real(s)
    ag._goal_target(SLOT, {SLOT: 3})
    assert tether._WANT_TARGET and not calls, ("MF-T3: _target_lookup reached with WANT_TARGET on",
                                               calls)
    print("  MF-T3 WANT_TARGET on: _goal_target never calls _target_lookup (subsumed)")
    print("test_want_subject_default OK")


if __name__ == "__main__":
    main()
