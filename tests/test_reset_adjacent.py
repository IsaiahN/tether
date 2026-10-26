"""RESET ADJACENCY, TETHER_RESET_ADJACENT (Isaiah 2026-09-29 "no consecutive resets"; the reviewer
2026-10-25 22:21, 22:46; PLAY11 round 2 c12-c13: a RESET,RESET chosen by Interface.undirected and
refused only by the platform's ResetGuard). The fake ARC game; each case ON and OFF, game-free.

  (a) undirected over (ACTION1, RESET) right after a RESET: ON never draws RESET; OFF does.
  (b) a RESET whose audit never ran (as on a seam step), then a realise over (RESET,): ON refuses
      (the flag came from the send); OFF realises RESET (the flag was only ever set in audit).
  (c) RESET, one other press, RESET: allowed under ON (the rule is adjacency only).
  (d) a bare routine step RESET right after a RESET: None under ON; RESET under OFF.
  (e) THE BACKSTOP: a planted exit returning RESET raw after a RESET: under ON no env.step(RESET)
      and one reset_adjacent_refused row naming the exit; under OFF it is sent.
  (f) a board offering only RESET: under ON the run ends by its cap (no hang), and every step after
      the first RESET proposes nothing, counted in the no_action rows. Under OFF (today's code) the
      same board RAISES in _explore ("the board advertises no actions"), because realise's old
      re-choose empties the offer: the occasion this arm closes.
  (h) the flag's start, seeded at wire_agent from the guard (the platform's last command): (h1) a
      fresh wrapper (its own reset done), a planted first RESET: ON not sent, an adjacency
      no_action; OFF the guard refuses it (refused_step 1); (h2) a wrapper with no construction
      reset: wire resets it, the flag starts set, a first RESET not sent; (h3) a guard passed in
      after ACTION1: the flag starts clear and a first RESET is sent.
  (ii) a planted exit returning None with the flag clear: the cause "the chooser returned nothing".
  ResetGuard's own strict RESET,RESET must-fail is tests/test_entry.py's, which drives the wrapper
  directly, so this arm cannot pre-empt it.

    python tests/test_reset_adjacent.py
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

from arcengine import GameAction  # noqa: E402

import arc_holdout  # noqa: E402
import interface as IFace  # noqa: E402
import tether  # noqa: E402
import tether_agent  # noqa: E402
from test_entry import FakeWrapper  # noqa: E402

RESET = IFace.RESET


def _agent():
    env, ag, *_ = arc_holdout.wire(FakeWrapper(script={}), "fake")
    env.observe()
    ag.step()
    return env, ag


def _arm(on: bool):
    IFace._RESET_ADJACENT = on


def case_a(on):
    _arm(on)
    _env, ag = _agent()
    ag.iface._last_was_reset = False
    ag.iface.note_sent(RESET)
    if not on:
        ag.iface._last_was_reset = True     # OFF: the flag as audit would set it after a RESET
    picks = [ag.iface.undirected(("ACTION1", RESET), c, env=ag.env).action for c in range(20)]
    return picks.count(RESET)


def case_b(on):
    _arm(on)
    _env, ag = _agent()
    ag.iface._last_was_reset = False
    ag.iface.note_sent(RESET)                # the press is sent; audit is NOT called (a seam)
    r = ag.iface.realise(IFace.Intent(IFace.ELICIT), (RESET,), (), None, ag.env)
    return None if r is None else r.action


def case_c():
    _arm(True)
    _env, ag = _agent()
    ag.iface.note_sent(RESET)
    ag.iface.note_sent("ACTION1")
    r = ag.iface.realise(IFace.Intent(IFace.ELICIT), (RESET,), (), None, ag.env)
    return RESET in ag.iface.adjacent(("ACTION1", RESET)), None if r is None else r.action


def case_d(on):
    _arm(on)
    _env, ag = _agent()
    ag.iface.note_sent(RESET)
    if not on:
        ag.iface._last_was_reset = True
    return ag._realise_step(RESET, {})


def case_e(on):
    _arm(on)
    _env, ag = _agent()
    ag.iface.note_sent(RESET)
    if not on:
        ag.iface._last_was_reset = True
    sent = []
    real_step = ag.env.step
    ag.env.step = lambda a, *xy: (sent.append(a), real_step(a, *xy))[1]
    ag.choose = lambda _before: (RESET, "planted")
    n0 = len(ag.led.rows())
    acted = ag.step()
    rows = [r for r in ag.led.rows()[n0:] if r["event"] == "reset_adjacent_refused"]
    return acted, sent, [r["detail"].get("by") for r in rows]


def case_f(on, n=8):
    _arm(on)
    led = os.path.join(tempfile.mkdtemp(prefix="radj_"), "f.jsonl")
    w = FakeWrapper(script={}, actions=())
    try:
        rep = tether_agent.run(w, "fake", max_actions=n, led_path=led)
    except RuntimeError as e:
        return f"raised: {e}"[:120], 0, w.calls
    with open(led, encoding="utf-8") as fh:
        rows = [json.loads(x) for x in fh if x.strip()]
    idle = [r for r in rows if r["event"] == "no_action"
            and "reset adjacency" in str(r["detail"].get("cause"))]
    return rep, len(idle), w.calls


class NoReset(FakeWrapper):
    """A wrapper that does NOT reset in its own __init__ (wire resets it, through the guard)."""

    def __init__(self):
        self.calls, self._last, self.script = [], None, {}
        self.actions, self.pos, self.n = [1, 2, 3, 4, 6], [30, 30], 0


def _plant(ag, pick):
    """A planted exit in choose's place (the step's per-step fields are reset by _step_body)."""
    ag.choose = lambda _before: (pick, "planted")


def _planted(w, on, pick=RESET):
    """(h): wire w, the agent's first choice planted; (sent to the wrapper, the guard's refused
    step(RESET) count, the step's no_action causes, the flag right after wire)."""
    _arm(on)
    env, ag, *_ = arc_holdout.wire(w, "fake")
    flag = ag.iface._last_was_reset
    env.observe()
    n0, c0 = len(ag.led.rows()), len(env.w.w.calls)
    _plant(ag, pick)
    ag.step()
    causes = [r["detail"].get("cause") for r in ag.led.rows()[n0:] if r["event"] == "no_action"]
    return env.w.w.calls[c0:], env.w.refused_step, causes, flag


def main():
    tether._AGENT_SEED = False
    on_a, off_a = case_a(True), case_a(False)
    assert on_a == 0 and off_a > 0, ("(a)", on_a, off_a)
    print(f"  (a) undirected after a RESET, 20 draws over (ACTION1, RESET): RESET drawn ON {on_a}, "
          f"OFF {off_a}")
    on_b, off_b = case_b(True), case_b(False)
    assert on_b is None and off_b == RESET, ("(b)", on_b, off_b)
    print(f"  (b) a RESET sent with no audit (a seam), then realise over (RESET,): ON {on_b}, "
          f"OFF {off_b}")
    kept, c_r = case_c()
    assert kept and c_r == RESET, ("(c)", kept, c_r)
    print(f"  (c) RESET, ACTION1, then: RESET offered {kept}, realised {c_r}")
    on_d, off_d = case_d(True), case_d(False)
    assert on_d is None and off_d == RESET, ("(d)", on_d, off_d)
    print(f"  (d) a bare routine RESET right after a RESET: ON {on_d}, OFF {off_d}")
    on_e, off_e = case_e(True), case_e(False)
    assert on_e[0] is False and RESET not in on_e[1] and on_e[2] == ["planted"], ("(e) ON", on_e)
    assert RESET in off_e[1] and not off_e[2], ("(e) OFF", off_e)
    print(f"  (e) the backstop, a planted raw RESET after a RESET: ON acted {on_e[0]}, sent "
          f"{on_e[1]}, refused rows by {on_e[2]}; OFF sent {off_e[1]}")
    rep, idle, calls = case_f(True)
    assert isinstance(rep, dict) and idle >= 7, ("(f) ON", rep, idle)
    print(f"  (f) a RESET-only board, 8 actions, ON: the run returned (no hang); no_action "
          f"(reset adjacency) {idle}; wrapper calls {calls}")
    rep, idle, calls = case_f(False)
    assert isinstance(rep, str) and "no actions" in rep, ("(f) OFF: no raise", rep)
    print(f"  (f) the same board OFF (today's code): {rep}")
    # (h) the flag's start, read from the guard at wire_agent (the reviewer 2026-10-25 23:04)
    sent, ref, causes, flag = _planted(FakeWrapper(script={}), True)
    assert flag and "RESET" not in sent and ref == 0, ("(h1) ON", sent, ref, flag)
    assert causes == ["reset adjacency: the last press was RESET"], ("(h1) ON cause", causes)
    print(f"  (h1) a fresh wrapper (its own reset done), first choice RESET, ON: flag {flag}, "
          f"sent {sent}, guard refused {ref}, cause {causes}")
    sent, ref, causes, flag = _planted(FakeWrapper(script={}), False)
    assert not flag and ref == 1 and not causes, ("(h1) OFF", sent, ref, flag)
    print(f"  (h1) the same OFF: flag {flag}, the guard refused {ref} (not sent: {sent})")
    w = NoReset()
    sent, ref, causes, flag = _planted(w, True)
    assert w.calls[0] == "RESET" and flag and "RESET" not in sent and ref == 0, ("(h2)", w.calls)
    print(f"  (h2) a wrapper with no construction reset: wire's reset {w.calls[:1]}, flag {flag}, "
          f"first RESET not sent")
    g = arc_holdout.ResetGuard(FakeWrapper(script={}))
    g.step(GameAction.ACTION1)
    sent, ref, causes, flag = _planted(g, True)
    assert not flag and sent == ["RESET"] and ref == 0 and not causes, ("(h3)", sent, ref, flag)
    print(f"  (h3) a guard passed in after ACTION1: flag {flag}, first RESET sent {sent}")
    # (ii) a true cause: a None from a planted non-RESET exit, the flag clear
    _arm(True)
    _env, ag = _agent()
    ag.iface.note_sent("ACTION1")
    _plant(ag, None)
    n0 = len(ag.led.rows())
    ag.step()
    causes = [r["detail"].get("cause") for r in ag.led.rows()[n0:] if r["event"] == "no_action"]
    assert causes == ["the chooser returned nothing"], ("(ii)", causes)
    print(f"  (ii) a planted exit returning None, the last press ACTION1: cause {causes}")
    _arm(True)
    print("reset_adjacent: OK")


if __name__ == "__main__":
    main()
