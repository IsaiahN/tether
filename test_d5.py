"""7a D5, split a slot's residual on strain (Fig 9 :4-5, :54-58; the reviewer 2026-10-10 15:58Z,
16:24Z). The cut reads every row on which THIS term predicted the slot in the current level.

  must-pass (hand record): a term right on every TOUCH row and wrong on every other, 2 a side,
     is split on TOUCH, and the split pays;
  fake (40 actions, TETHER_D5 on): o2.drow's recolour<o0.colour> is right on TOUCH steps and on
     three earlier BECOME steps of the same level, wrong on the later BECOME steps. No held
     predicate separates that, so it is NOT split, the reason is recorded once, and the full gate
     passes (the reviewer 16:24Z: a real finding, not a failure);
  2. a term wrong on both sides of every held predicate is not split;
  3. one wrong row (fewer than 2 a side) does not fire;
  4. credit: after a split, a not-P step is predicted by part B (or nothing), never charged to the
     incumbent;
  5. part B's search writes rows carrying its part, and the slot's park state is restored;
  6. the incumbent's shadow right on a not-P step reverts the split, with its row;
  7. right on a not-P row earlier in the SAME level, then demoted and rebound, then wrong on
     not-P: NOT split. A cut keyed on the binding (the rows since the rebind) would fire;
  8. the step between the cut (found at settle) and the split (run in route, after the bet): on
     a not-P step the incumbent is a shadow, never the predictor, and on a P step it predicts.
     Before this, gridworld_s1 ON charged the incumbent for not-P rows on 3 of 4 splits (c30:
     demoted by one, and the split dissolved in the cycle it was made);
  9. a cut found at settle is a CANDIDATE (the reviewer 18:46Z, Fig 9 :60): a cut_candidate row,
     nothing pending, the incumbent still bound -- and the step that found it is not its witness;
 10. a P step does not witness: the candidate waits;
 11. the first not-P step with the incumbent RIGHT refutes it: cut_refuted, no split, no pending;
 12. the first not-P step with the incumbent WRONG confirms it: cut_confirmed, and the split is
     pending for the next perceive;
 13. WITHDRAWN NEVER STANDS IN FOR A REFUTATION (the reviewer 20:30Z): the incumbent WRONG on a P
     step refutes the cut (side P) -- and when that same miss demotes it, the rows are
     cut_refuted and no cut_withdrawn;
 14. withdrawn only where no witness can arrive: the level ends (retarget), or another term
     predicts the slot; each row says so and carries no verdict on the cut;
 15. every candidate leaves by exactly one of confirmed / refuted / withdrawn.

    python test_d5.py
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

import gamma
import gate
import gridworld
import interface as IFace
import ledger
import test_entry
import tether
import tether_agent
import world

sys.dont_write_bytecode = True


def _fake() -> list[dict]:
    path = os.path.join(tempfile.mkdtemp(), "fake.jsonl")
    tether_agent.run(test_entry.FakeWrapper(), "fake", max_actions=40, led_path=path)
    with open(path, encoding="utf-8") as fh:
        return [json.loads(x) for x in fh if x.strip()]


def _hand(rows: list[tuple], term: str = "idn") -> tether.Agent:
    """A gridworld agent with a hand trace on slot x: (intent kind, x before, x after,
    predictor). The predictor defaults to `term`; None marks a step it did not predict."""
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="d5_fixture"), tether.Config(),
                      ledger.Ledger())
    ag.trace = [({"x": r[1]}, "A", {"x": r[2]}, r[0], None) for r in rows]
    ag._trace_pos = None
    ag.slots = [*ag.slots, "x"]
    ag.alphabet["x"] = 8
    ag._d5_rows["x"] = [(i, r[3] if len(r) > 3 else term) for i, r in enumerate(rows)]
    return ag


T, B = IFace.TOUCH, IFace.ELICIT        # two intent kinds: "TOUCH" and "BECOME OTHER"
CLEAN = [(T, 1, 1), (B, 1, 3), (T, 2, 2), (B, 2, 5)]          # idn right on TOUCH only


if __name__ == "__main__":
    tether._D5 = True
    cut = _hand(CLEAN)._d5_cut("x", "idn")
    assert cut is not None and cut[0] == T and cut[1]["incumbent_miss_bits_off_p"] > 0, cut
    print(f"  must-pass (hand): split on {cut[0]}, {cut[1]}")
    # fake: the earlier right BECOME rows are on the same level
    rows = _fake()
    assert not [r for r in rows if r["slot"] == "@d5" and r["event"] == "split"]
    ns = [r["detail"] for r in rows if r["event"] == "not_split"
          and r["detail"]["split_slot"] == "o2.drow"]
    assert len(ns) == 1 and ns[0]["right"] >= 2 and ns[0]["wrong"] >= 2, ns
    assert gate.check(rows)["verdict"] == gate.PASS
    print(f"  fake: o2.drow NOT split ({ns[0]['right']} right, {ns[0]['wrong']} wrong in the "
          f"level; predicates {ns[0]['predicates']}); reason recorded once; full gate passes")
    # 2, 3
    mixed = [(T, 1, 1), (B, 1, 3), (T, 2, 4), (B, 2, 5), (T, 3, 3)]
    assert _hand(mixed)._d5_cut("x", "idn") is None
    print("  2: a term wrong on both sides of TOUCH is not split")
    assert _hand([(T, 1, 1), (T, 2, 2), (B, 2, 5), (T, 3, 3)])._d5_cut("x", "idn") is None
    print("  3: one wrong row (fewer than 2 a side) does not fire")
    # 7: same level, right on not-P early; a demote/rebind (predictor None) between
    seven = [(T, 1, 1), (B, 1, 1), (B, 2, 4, None), (T, 2, 2), (B, 2, 6), (T, 3, 3), (B, 3, 7)]
    ag7 = _hand(seven)
    assert ag7._d5_cut("x", "idn") is None
    ag7._d5_rows["x"] = [(i, "idn") for i in range(3, len(seven))]   # the binding-keyed window
    assert ag7._d5_cut("x", "idn") is not None
    print("  7: right on a not-P row earlier in the level, then rebound: NOT split (a window "
          "keyed on the binding would split it)")
    # 5: a real split on the hand record; part B's search rows carry its part
    ag = _hand(CLEAN)
    ag.bound["x"] = "idn"
    owed_before = "x" in ag.owed_import
    ag._d5_split("x", cut[0], cut[1])
    part_rows = [r for r in ag.led.rows() if (r["detail"] or {}).get("part")]
    split_rows = [r for r in ag.led.rows() if r["event"] == "split"]
    assert split_rows and all(r["detail"]["part"]["part"] == f"!{T}" for r in part_rows)
    assert ag.bound.get("x") == "idn" and ("x" in ag.owed_import) == owed_before
    assert ag._parts["x"]["A"] == "idn"
    print(f"  5: split row written; part B's {len(part_rows)} search row(s) carry !{T}; the "
          f"slot's binding and owed state restored; part B = {ag._parts['x']['B']}")
    # 4: a not-P step predicts by part B (or nothing), never by the incumbent
    ag._intent_now = IFace.Intent(IFace.ELICIT)
    ag._last_landed = None
    ag._d5_select(["x"], {"x": 4}, "A")
    assert ag.bound.get("x") != "idn" and "x" in ag._shadow
    print(f"  4: on a not-P step the slot's predictor is {ag.bound.get('x')} (not the incumbent); "
          f"the incumbent's shadow is kept ({ag._shadow['x']})")
    # 6
    ag6 = _hand(CLEAN)
    ag6._parts["x"] = {"P": T, "A": "idn", "B": None}
    ag6._shadow["x"] = 4
    ag6._pred_by = {"x": None}
    ag6.settle({"x": tether.SlotResidual("x", "transition", 4, 4, 0.0)})
    broke = [r for r in ag6.led.rows() if r["event"] == "partition_broken"]
    assert broke and "x" not in ag6._parts and ag6.bound.get("x") == "idn", (broke, ag6._parts)
    print("  6: the incumbent's shadow right on a not-P step reverts the split, with its row")
    # 8
    ag8 = _hand(CLEAN)
    ag8.bound["x"] = "idn"
    ag8._d5_pending["x"] = (T, cut[1], "idn")
    ag8._last_landed = None
    ag8._intent_now = IFace.Intent(IFace.TOUCH)
    ag8._d5_select(["x"], {"x": 4}, "A")
    assert ag8.bound.get("x") == "idn" and "x" not in ag8._shadow
    ag8._intent_now = IFace.Intent(IFace.ELICIT)
    ag8._d5_select(["x"], {"x": 4}, "A")
    assert ag8.bound.get("x") is None and "x" in ag8._shadow, (ag8.bound, ag8._shadow)
    ag8._d5_split("x", *ag8._d5_pending.pop("x"))
    assert ag8.bound.get("x") == "idn" and ag8._parts["x"]["A"] == "idn", ag8._parts
    print("  8: between the cut and the split, the incumbent predicts a P step and is only a "
          "shadow on a not-P step; the split then restores it as part A")
    # 9-12: candidacy, driven through settle
    def _cand():
        a = _hand(CLEAN)
        a.bound["x"] = "idn"
        a._pred_by = {"x": "idn"}
        a._last_landed = None
        return a
    ag9 = _cand()
    ag9._intent_now = IFace.Intent(IFace.ELICIT)                  # not-P, and a miss: the trigger
    ag9.settle({"x": tether.SlotResidual("x", "transition", 2, 5, 3.0)})
    ev9 = [r["event"] for r in ag9.led.rows() if r["slot"] == "@d5"]
    assert ev9 == ["cut_candidate"] and "x" in ag9._d5_candidates, ev9
    assert "x" not in ag9._d5_pending and "x" not in ag9._parts, (ag9._d5_pending, ag9._parts)
    print("  9: the cut is a candidate (row written, nothing pending, no parts); the step that "
          "found it did not witness it")
    ag9._intent_now = IFace.Intent(IFace.TOUCH)
    ag9.settle({"x": tether.SlotResidual("x", "transition", 3, 3, 0.0)})
    assert "x" in ag9._d5_candidates and [r["event"] for r in ag9.led.rows()
                                          if r["slot"] == "@d5"] == ["cut_candidate"]
    print(" 10: a P step does not witness; the candidate waits")
    ag11 = _cand()
    ag11._d5_candidates["x"] = (T, cut[1], "idn")
    ag11._intent_now = IFace.Intent(IFace.ELICIT)
    ag11.settle({"x": tether.SlotResidual("x", "transition", 4, 4, 0.0)})
    ev11 = [r["event"] for r in ag11.led.rows() if r["slot"] == "@d5"]
    assert ev11 == ["cut_refuted"] and not ag11._d5_candidates and not ag11._d5_pending, ev11
    assert ag11.bound.get("x") == "idn" and not ag11._parts
    print(" 11: the incumbent right on the first not-P step refutes the cut: no split, nothing "
          "pending, the incumbent keeps the slot")
    ag12 = _cand()
    ag12._d5_candidates["x"] = (T, cut[1], "idn")
    ag12._intent_now = IFace.Intent(IFace.ELICIT)
    ag12.settle({"x": tether.SlotResidual("x", "transition", 4, 6, 3.0)})
    ev12 = [r["event"] for r in ag12.led.rows() if r["slot"] == "@d5"]
    assert ev12[0] == "cut_confirmed" and "x" in ag12._d5_pending, (ev12, ag12._d5_pending)
    print(f" 12: the incumbent wrong on the first not-P step confirms the cut; the split is "
          f"pending for the next perceive (rows {ev12})")
    # 13: a P-step miss refutes, even when it demotes the incumbent
    ag13 = _cand()
    ag13._d5_candidates["x"] = (T, cut[1], "idn")
    ag13._intent_now = IFace.Intent(T)
    ag13.gamma.refute = lambda *_a, **_k: True               # force the demote branch
    ag13.settle({"x": tether.SlotResidual("x", "transition", 3, 5, 3.0)})
    ev13 = [r for r in ag13.led.rows() if r["slot"] == "@d5"]
    assert [r["event"] for r in ev13] == ["cut_refuted"], [r["event"] for r in ev13]
    assert ev13[0]["detail"]["side"] == "P" and ag13.bound.get("x") is None, ev13
    print(" 13: the incumbent wrong on a P step refutes the cut (side P); the same miss demoted "
          "it, and the rows are cut_refuted only -- no cut_withdrawn")
    # 14a: the level ends with a candidate outstanding
    ag14 = _cand()
    ag14._d5_candidates["x"] = (T, cut[1], "idn")
    ag14.retarget(ag14.env, 1)
    ev14 = [r for r in ag14.led.rows() if r["slot"] == "@d5"]
    assert [r["event"] for r in ev14] == ["cut_withdrawn"], ev14
    d14 = ev14[0]["detail"]
    assert d14["verdict_on_the_cut"] is None and "level" in d14["reason"], d14
    # 14b: another term predicts the slot
    ag14b = _cand()
    ag14b._d5_candidates["x"] = (T, cut[1], "idn")
    ag14b._pred_by = {"x": "inc"}
    ag14b.bound["x"] = "inc"
    ag14b._intent_now = IFace.Intent(IFace.ELICIT)
    ag14b.settle({"x": tether.SlotResidual("x", "transition", 4, 4, 0.0)})
    ev14b = [r["detail"]["reason"] for r in ag14b.led.rows() if r["event"] == "cut_withdrawn"]
    assert len(ev14b) == 1 and "another term" in ev14b[0], ev14b
    print(" 14: withdrawn only where no witness can arrive (the level ended; another term "
          "predicts the slot), each with no verdict on the cut")
    # 15: each candidate leaves by exactly one terminal row
    ends = {"cut_confirmed", "cut_refuted", "cut_withdrawn"}
    for a in (ag11, ag12, ag13, ag14, ag14b):                # ag9 is left waiting by design
        n = sum(1 for r in a.led.rows() if r["event"] in ends)
        assert n == 1 and not a._d5_candidates, (n, a._d5_candidates)
    print(" 15: every candidate driven here left by exactly one of confirmed / refuted / withdrawn")
    print("ok")
