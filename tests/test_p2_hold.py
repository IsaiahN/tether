"""P2', THE TRY-FIRST HOLD BY ITS OWN RECORD (the reviewer 2026-11-02 r830, r832): the agent's own
methods on stubs holding only the state they read.
  P2'-a  10 untouched kinds, no untried action: MIN_REPEAT kind touches that change nothing (the
         contact row's felt change empty) release the kinds' hold -- _try_first_open 10 -> 0, so
         the mint and the split are no longer held. OFF (today): 10 after every touch.
  P2'-a2 kind touches that all move the SAME slot (a change the board has already shown) do not
         pay: after the first, MIN_REPEAT of them release the hold. OFF (and before the novelty
         rule): every one "changed something" and the hold stays.
  P2'-b  a kind touch that moves a slot new to the board keeps the hold (the unpaid run restarts);
         a kind newly on the board re-opens a released hold.
  P2'-c  a held goal hypothesis whose presses are System 0's is not aged (steps 0) and is never
         ended "stalled" on them: past its budget with no press of its own it ends "untested" by
         "elsewhere" (r834), kept on the shelf by UNTESTED_KEEP. On its own presses it ends at
         its budget.
         OFF (today): System 0's presses age it and end it "stalled" by the ceiling.
  P2'-a/a2/b test the novelty release alone, so they run with TF_PASS OFF (the one-pass budget
  is test_tf_pass's).

    python tests/test_p2_hold.py
"""
from __future__ import annotations

import sys
from collections import Counter
from types import SimpleNamespace

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import ledger  # noqa: E402
import tether  # noqa: E402

A = tether.Agent


def board(kinds: int) -> SimpleNamespace:
    objs = [f"o{i}" for i in range(kinds)]
    ag = SimpleNamespace(_kind_unpaid=0, _kinds_open=0, _board_touched=set(),
                         _tf_len=None, _tf_left=None, _tf_rel_u=None, _running_step="PLAN",
                         _board_moved=set(),
                         _seam_now=False, _last_landed=None, _actuators={}, _contact_pending=None,
                         led=ledger.Ledger(None), iface=SimpleNamespace(last_changed=()),
                         env=SimpleNamespace(observe=lambda: {}), cycle=0,
                         _objs_named=A._objs_named)
    ag.objs = objs
    ag._board_untried_n = lambda: 0
    ag._kind = lambda o: ("k", o)                         # one object per kind
    ag._untouched_kinds = lambda _before: [[o] for o in ag.objs if o not in ag._board_touched]
    return ag


def touch(ag, o: str, changed: tuple = ()) -> None:
    ag._board_touched.add(o)
    ag.iface.last_changed = changed
    ag._moved_before = frozenset(ag._board_moved)   # as the step does, before it adds this press
    ag._board_moved.update(changed)
    ag._contact_pending = (("kind-touch", o), (o,))
    A._contact_felt(ag)


def held_after(on: bool, changes: list) -> list:
    tether._TRY_FIRST_PAYS, tether._TF_PASS = on, False
    try:
        ag = board(10)
        seen = [A._try_first_open(ag)]
        for i, ch in enumerate(changes):
            touch(ag, f"o{i}", ch)
            seen.append(A._try_first_open(ag))
        return seen, ag
    finally:
        tether._TRY_FIRST_PAYS, tether._TF_PASS = True, True


def hyp_ends(on: bool, own: bool, cycles: int = 4) -> tuple:
    tether._HYP_OWN_PRESS = on
    ended = []
    try:
        h = {"key": "g", "slots": ["o1.x"], "steps": 0, "budget": 2, "reads": {}, "seg": {},
             "r0": 5, "acted": Counter()}
        ag = SimpleNamespace(_hyp=h, wants={"o1.x": "w"}, _goal_links={"g": (("o1.x", "w"),)},
                             _res={})
        ag._hyp_end = lambda why, **k: (ended.append((why, k.get("by"))), setattr(ag, "_hyp", None))
        for _ in range(cycles):
            if ag._hyp is None:
                break
            h["own_last"] = own
            A._hyp_check(ag)
        return h["steps"], ended
    finally:
        tether._HYP_OWN_PRESS = True


def main():
    assert tether._TRY_FIRST_PAYS and tether._HYP_OWN_PRESS, "both arms ON by default"
    m = tether.MIN_REPEAT
    on, _ = held_after(True, [()] * m)
    off, _ = held_after(False, [()] * m)
    assert on[0] == 10 and on[-1] == 0, ("P2'-a: unpaid touches release the hold", on)
    assert off[-1] == 10 - m, ("P2'-a MUST-FAIL: OFF the kinds still hold", off)
    paid, ag = held_after(True, [("o5.x",)] + [()] * (m - 1))
    assert paid[-1] == 10 - m and ag._kind_unpaid == m - 1, ("P2'-b: a paying touch keeps it", paid)
    same, _ = held_after(True, [("o5.x",)] * (m + 1))
    assert same[-1] == 0, ("P2'-a2: a change already shown does not pay", same)
    rel, ag = held_after(True, [()] * m)
    ag.objs = ag.objs + ["o99"]                           # a kind newly on the board
    tether._TF_PASS = False
    try:
        assert A._try_first_open(ag) == 10 - m + 1, "P2'-b: a new kind re-opens the hold"
    finally:
        tether._TF_PASS = True
    s_on, e_on = hyp_ends(True, own=False)
    s_off, e_off = hyp_ends(False, own=False)
    s_own, e_own = hyp_ends(True, own=True)
    assert s_on == 0 and e_on == [("untested", "elsewhere")], ("P2'-c: not aged; ended "
                                                               "untested", s_on, e_on)
    assert e_off == [("stalled", "ceiling")], ("P2'-c MUST-FAIL: OFF it is ended", e_off)
    assert e_own == [("stalled", "ceiling")], ("P2'-c: on its own presses it ends", e_own)
    own = set(tether._HYP_OWN_BY)                   # the exits that press FOR the held hypothesis
    assert {"routine", "hold", "actuator", "discriminate:goal"} <= own \
        and not own & {"system0", "probe", "draw", "distinguish"}, ("P2'-c: its own presses", own)
    print(f"test_p2_hold: 10 kinds, {m} unpaid touches -> hold {on[0]} -> {on[-1]} (OFF "
          f"{off[-1]}); a paying touch keeps it ({paid[-1]}); a new kind re-opens it; a hypothesis "
          f"on System 0's presses: steps {s_on}, ended by {e_on[0][1]} (OFF {e_off[0][1]}); on "
          f"its own: ended {e_own[0][0]}")


if __name__ == "__main__":
    main()
