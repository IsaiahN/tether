"""F2's fallback (TETHER_WANT_TARGET_SUBJECT; the reviewer 2026-10-11 07:20Z): the target reads a
retained want ONLY where `_want_scope` names it (a goal-condition want); every own want keeps
the masked lookup. The data is the recorded gridworld_arc_s1 history at c89, the pair linked.

  1. both arms OFF: today's lookup -- a want under a bound val predictor is masked;
  2. SUBJECT ON: an own (non-goal-condition) want on a val-bound slot is still masked
     (target None, _term_of names the bound predictor);
  3. SUBJECT ON: the subject-scoped want on o0.col yields o3's column; _term_of kind "want";
  4. both ON = TETHER_WANT_TARGET's behaviour.

    python tests/test_want_target_subject.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
import tether
from test_goal_pair import ROWS
from test_gt_which import _linked

sys.dont_write_bytecode = True
PRED = "translate"      # a library atom, out_type val: a predictor, not an objective


def _read(ag, slot, st, full, subject):
    was = (tether._WANT_TARGET, tether._WANT_TARGET_SUBJECT)
    tether._WANT_TARGET, tether._WANT_TARGET_SUBJECT = full, subject
    try:
        return ag._goal_target(slot, st), ag._term_of(slot)
    finally:
        tether._WANT_TARGET, tether._WANT_TARGET_SUBJECT = was


if __name__ == "__main__":
    ag = _linked()
    away = next(st for st, hit in ROWS if not hit and st["o0.col"] != st["o3.col"])
    own = ag._want_terms["o0.col"]
    # an OWN want: the same OBJ term placed as o2.col's want, NOT subject-scoped
    ag.wants["o2.col"], ag._want_terms["o2.col"] = own.name, own
    for sl in ("o0.col", "o2.col"):
        ag.bound[sl] = PRED
    assert "o2.col" not in ag._want_scope and ag._want_scope["o0.col"] == ag.wants["o0.col"]
    t, k = _read(ag, "o0.col", away, False, False)
    assert t is None and k["kind"] == "bound" and k["name"] == PRED, (t, k)
    print(f"  1: both OFF: o0.col target {t}, _term_of {k['kind']} {k['name']} (masked, as today)")
    t, k = _read(ag, "o2.col", away, False, True)
    assert t is None and k["kind"] == "bound" and k["name"] == PRED, (t, k)
    print(f"  2: SUBJECT ON, own want on o2.col under {PRED}: target {t}, _term_of {k['kind']} "
          f"{k['name']} -- still masked")
    t, k = _read(ag, "o0.col", away, False, True)
    assert t == away["o3.col"] and k["kind"] == "want", (t, k)
    print(f"  3: SUBJECT ON, subject-scoped want on o0.col: target {t} (o3's column), _term_of "
          f"kind {k['kind']}")
    for sl in ("o0.col", "o2.col"):
        assert _read(ag, sl, away, True, True) == _read(ag, sl, away, True, False), sl
    print(f"  4: both ON == WANT_TARGET alone on o0.col and o2.col (o2.col target "
          f"{_read(ag, 'o2.col', away, True, True)[0]})")
    print("ok")
