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
     demoted by one, and the split dissolved in the cycle it was made).

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
    print("ok")
