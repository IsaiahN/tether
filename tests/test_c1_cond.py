"""C1 PART 6(c): THE CARRY OF FOUND CONDITIONS (the reviewer 2026-11-09 r1604 (A)), arm
TETHER_CONDITION_CARRY.

  D1  MF: a split's record, written through the real lineage write and read back, holds no
      "o<digit>": a KNOWN_EFFECT pair form's partner instance is its kind
  D2  the load: a held split ranks 0, one that ended partition_broken ranks 1 (a failed method)
  D3  the order: with TOUCH and "KNOWN_EFFECT ?.row" both separating, the carried one is found
      first; the offered set and its guard_bits price are unchanged
  D4  MF: a carried condition that does not separate here fires nothing
  D5  a carried cut is still a candidate: _d5_cut finds it, nothing is split by it
  D6  OFF: the order is today's (TOUCH first), even with conditions held

    python tests/test_c1_cond.py
"""
from __future__ import annotations

import json
import os
import re
import sys
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")

import gamma  # noqa: E402
import gridworld  # noqa: E402
import interface as IFace  # noqa: E402
import ledger  # noqa: E402
import lineage  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

T, B = IFace.TOUCH, IFace.ELICIT
CLEAN = [(T, 1, 1), (B, 1, 3), (T, 2, 2), (B, 2, 5)]          # idn right on TOUCH only
INSTANCE = re.compile(r"(?<![A-Za-z0-9])o\d+")


def _agent(steps: int = 0) -> tether.Agent:
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="c1_cond"), tether.Config(),
                      ledger.Ledger())
    for _ in range(steps):
        ag.step()
    return ag


def _arms(cond: bool, action: bool = True):
    keep = (tether._CONDITION_CARRY, tether._D5_ACTION, tether._D5)
    tether._CONDITION_CARRY, tether._D5_ACTION, tether._D5 = cond, action, True
    return keep


def _restore(keep) -> None:
    tether._CONDITION_CARRY, tether._D5_ACTION, tether._D5 = keep


def _hand(rows: list, row_forms: dict | None = None) -> tether.Agent:
    ag = _agent()
    ag.trace = [({"x": r[1]}, "A", {"x": r[2]}, r[0], None) for r in rows]
    ag._trace_pos = None
    ag.slots = [*ag.slots, "x"]
    ag.alphabet["x"] = 8
    ag._d5_rows["x"] = [(i, "idn") for i in range(len(rows))]
    ag._kn_eff = {id(t[0]): frozenset(row_forms.get(i, ())) for i, t in enumerate(ag.trace)} \
        if row_forms else {}
    return ag


def check_d1() -> None:
    keep = _arms(True)
    try:
        ag = _agent(4)
        slot = next(s for s in ag.slots if s.startswith("o0."))
        ag._cond_write(slot, f"{tether.KNOWN_EFFECT} ?.dcol_o3+", "idn", None,
                       {"right_on_p": 2, "wrong_off_p": 2})
        ag._cond_end(slot, "partition_broken")
        with tempfile.TemporaryDirectory() as d:
            lineage._write(d, ag, "g", False, [])
            gens = lineage._read(Path(d))
        recs = [r for g in gens.values() for r in g.get("inventions", ())
                if r.get("kind") in ("condition", "condition_end")]
    finally:
        _restore(keep)
    assert len(recs) == 2, recs
    text = json.dumps(recs)
    assert not INSTANCE.search(text), f"MUST-FAIL: an instance name crossed the save: {text}"
    assert recs[0]["P"].startswith(f"{tether.KNOWN_EFFECT} ?.dcol_("), recs[0]["P"]
    print(f"  D1: the record read back holds no o<digit>; P {recs[0]['P']!r}; slot kind "
          f"{recs[0]['slot_kind']!r}")
    return recs


def check_d2(recs: list) -> None:
    keep = _arms(True)
    try:
        ag = _agent()
        ag._reinvent_carried(json.loads(json.dumps(recs)))
        held = {**recs[0], "name": "g_cond_9", "term": "g_cond_9", "P": "TOUCH"}
        ag._reinvent_carried([held])
    finally:
        _restore(keep)
    k_broken = (recs[0]["slot_kind"], recs[0]["P"])
    assert ag._cond_in[k_broken] == 1, ag._cond_in
    assert ag._cond_in[(recs[0]["slot_kind"], "TOUCH")] == 0, ag._cond_in
    print("  D2: loaded: the broken split ranks 1, a held one 0")


def check_d3_d6() -> None:
    forms = {0: {"?.row"}, 2: {"?.row"}}           # the TOUCH rows are the rows moving the row
    keep = _arms(True)
    try:
        plain = _hand(CLEAN, forms)._d5_cut("x", "idn")
        ag = _hand(CLEAN, forms)
        ag._cond_in = {(ag._kind_key("x"), f"{tether.KNOWN_EFFECT} ?.row"): 0}
        carried = ag._d5_cut("x", "idn")
        assert not ag._parts, "D5: a carried cut split the slot without its witness"
        _restore(keep)
        keep = _arms(False)
        off = _hand(CLEAN, forms)
        off._cond_in = dict(ag._cond_in)
        cut_off = off._d5_cut("x", "idn")
    finally:
        _restore(keep)
    assert plain[0] == T and cut_off[0] == T, (plain, cut_off)
    assert carried[0] == f"{tether.KNOWN_EFFECT} ?.row", carried
    assert carried[1]["guard_bits"] == plain[1]["guard_bits"], (carried, plain)
    print(f"  D3: carried {carried[0]!r} found first (today {plain[0]!r}); guard_bits "
          f"{carried[1]['guard_bits']} both ways")
    print("  D5: a candidate only, nothing split")
    print(f"  D6: OFF the order is today's ({cut_off[0]!r})")


def check_d4() -> None:
    mixed = [(T, 1, 1), (B, 1, 3), (T, 2, 4), (B, 2, 5), (T, 3, 3)]
    keep = _arms(True)
    try:
        ag = _hand(mixed)
        ag._cond_in = {(ag._kind_key("x"), T): 0}
        cut = ag._d5_cut("x", "idn")
    finally:
        _restore(keep)
    assert cut is None, f"MUST-FAIL: a carried condition fired where it does not separate: {cut}"
    print("  D4: a carried TOUCH that does not separate here fires nothing")


def main() -> int:
    recs = check_d1()
    check_d2(recs)
    check_d3_d6()
    check_d4()
    print("c1_cond: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
