"""C1 (B): THE NULL'S MISSES IN D5'S CONDITION SEARCH, ORIENTATION, AND THE THREE-VALUED KNOWN
EFFECT (the reviewer 2026-11-10 r1612, r1614, r1615), arms TETHER_D5_NULL, TETHER_D5_EITHER_SIDE,
TETHER_KNOWN_CORE.

  N1  (c) known_split: a form every signature moved HOLDS, one none moved FAILS, one some moved is
      UNDECIDED; a context never seen is undecided for every form
  N2  MF (c), the c48 shape generalised: a level whose only blocking row is in a context never
      seen cuts with the arm ON (decided 4, undecided 1) and not with it OFF
  N3  MF (b): a P on exactly the wrong rows splits as "UNLESS P"; OFF it does not; the price is the
      doubled offered set's
  N4  MF (a), the PATH through settle: a null miss on a slot bet with nothing bound reaches the cut
      (a cut_candidate on "@null"); OFF it does not; idn's standing is byte-equal and no refute,
      demote or miss row names idn
  N5  MF (a): a null split mints part B and leaves the slot unbound (part A "@null"); its shadow,
      right on a not-P row, reverts the split; idn's standing byte-equal after both

    python tests/test_c1_nullsearch.py
"""
from __future__ import annotations

import os
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

KE = tether.KNOWN_EFFECT
COL = (("o0.col", -1), ("o0.dcol_o1", 1))           # a left press: col down, the pair moves
ROW = (("o0.row", 1),)                               # a down press: row up


def _agent(steps: int = 4) -> tether.Agent:
    env = world.bind(gridworld.family("default", 0, 4))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="c1_nullsearch"), tether.Config(),
                      ledger.Ledger())
    for _ in range(steps):
        ag.step()
    return ag


def _arms(null: bool, either: bool, core: bool):
    keep = (tether._D5_NULL, tether._D5_EITHER_SIDE, tether._KNOWN_CORE, tether._D5_ACTION,
            tether._D5)
    (tether._D5_NULL, tether._D5_EITHER_SIDE, tether._KNOWN_CORE, tether._D5_ACTION,
     tether._D5) = null, either, core, True, True
    return keep


def _restore(keep) -> None:
    (tether._D5_NULL, tether._D5_EITHER_SIDE, tether._KNOWN_CORE, tether._D5_ACTION,
     tether._D5) = keep


def _idn(ag) -> str:
    return repr(ag.gamma.standing.get(tether.IDN))


def _hand(ag, rows: list, known: dict) -> None:
    """Rows on slot x, the null predicting (no change); known[i] = (holds, union) for a row whose
    press was seen in its context, absent for one never seen. The rows are the null's."""
    ag.trace = [({"x": b}, "A", {"x": a}, None, None) for b, a in rows]
    ag._trace_pos = None
    ag.slots = [*ag.slots, "x"]
    ag.alphabet["x"] = 8
    ag._d5_rows["x"] = [(i, tether.NULL_MAKER) for i in range(len(rows))]
    ag._kn3 = {id(ag.trace[i][0]): v for i, v in known.items()}
    ag._kn_eff = {id(ag.trace[i][0]): v[0] for i, v in known.items() if v[0]}


# c48 generalised: the null right where the col form holds, wrong where it fails; row 4 unseen
ROWS = [(1, 1), (1, 3), (2, 2), (2, 5), (3, 3)]
SEEN_COL = (frozenset({"?.col", "?.col-"}), frozenset({"?.col", "?.col-", "?.dcol_o1"}))
SEEN_ROW = (frozenset({"?.row", "?.row+"}), frozenset({"?.row", "?.row+"}))
KNOWN = {0: SEEN_COL, 1: SEEN_ROW, 2: SEEN_COL, 3: SEEN_ROW}


def check_n1() -> None:
    ag = _agent(0)
    ctx = (("orthogonal", 3),)
    ag.iface.table["left"] = {**ag.iface.table.get("left", {}),
                              "by_ctx": {ctx: {COL, (*COL, ("o0.dist_o2", -1)),
                                               (("o0.col", -1),)}}}
    seen, holds, union = ag.iface.known_split("left", ctx)
    assert seen and "?.col-" in holds and "?.dcol_o1" not in holds and "?.dcol_o1" in union
    assert "?.row" not in union, union
    assert ag.iface.known_split("left", (("orthogonal", 9),)) == (False, frozenset(), frozenset())
    print("  N1: every signature -> holds (?.col-); some -> undecided (?.dcol_o1); none -> fails "
          "(?.row); a context never seen -> undecided")


def check_n2() -> None:
    keep = _arms(True, False, True)
    try:
        ag = _agent()
        _hand(ag, ROWS, KNOWN)
        cut = ag._d5_cut("x", tether.NULL_MAKER)
        _restore(keep)
        keep = _arms(True, False, False)
        off = _agent()
        _hand(off, ROWS, KNOWN)
        cut_off = off._d5_cut("x", tether.NULL_MAKER)
    finally:
        _restore(keep)
    assert cut is not None and cut[0] == f"{KE} ?.col", cut
    assert cut[1]["decided"] == 4 and cut[1]["undecided"] == 1, cut
    assert cut_off is None, f"MUST-FAIL: OFF the unseen row did not block the cut: {cut_off}"
    print(f"  N2: ON cuts on {cut[0]!r} (decided 4, undecided 1, guard_bits "
          f"{cut[1]['guard_bits']}); OFF the unseen row reads as not-P and blocks it")


def check_n3() -> None:
    # the null RIGHT on the rows where "?.row" is unknown-free and false; P marks the WRONG rows
    known = {0: SEEN_COL, 1: SEEN_ROW, 2: SEEN_COL, 3: SEEN_ROW}
    rows = [(1, 1), (1, 3), (2, 2), (2, 5)]
    keep = _arms(True, True, True)
    try:
        ag = _agent()
        _hand(ag, rows, {i: (v[0] - {"?.col", "?.col-"}, v[1]) for i, v in known.items()})
        cut = ag._d5_cut("x", tether.NULL_MAKER)
        _restore(keep)
        keep = _arms(True, False, True)
        one = _agent()
        _hand(one, rows, {i: (v[0] - {"?.col", "?.col-"}, v[1]) for i, v in known.items()})
        cut_one = one._d5_cut("x", tether.NULL_MAKER)
    finally:
        _restore(keep)
    assert cut is not None and cut[0].startswith(f"{tether.UNLESS} {KE} ?.row"), cut
    assert cut_one is None, f"MUST-FAIL: one-sided D5 split on the wrong rows: {cut_one}"
    n = len({f"{KE} {f}" for v in known.values() for f in v[0] - {"?.col", "?.col-"}})
    n += 1 if tether._ACTED_GUARD else 0             # ACTED_SELF is offered beside the forms
    base = cut[0].split(" ", 1)[1]
    assert cut[1]["guard_bits"] == round(tether._guard_bits(base, 2 * n), 3), (cut, n)
    assert cut[1]["guard_bits"] > round(tether._guard_bits(base, n), 3)
    print(f"  N3: {cut[0]!r} splits (part A where ?.row fails); one-sided it does not; priced over "
          f"{2 * n} offered")


def check_n4() -> None:
    for on in (True, False):
        keep = _arms(on, False, True)
        try:
            ag = _agent()
            _hand(ag, ROWS[:4], {i: KNOWN[i] for i in range(4)})
            ag._d5_rows["x"] = ag._d5_rows["x"][:3]          # settle appends the fourth
            ag._null_bet = frozenset({"x"})
            ag._pred_by["x"] = None
            ag.bound.pop("x", None)
            before = _idn(ag)
            n0 = len(ag.led.rows())
            ag.settle({"x": tether.SlotResidual("x", "transition", 2, 5, 3.0)})
            new = ag.led.rows()[n0:]
        finally:
            _restore(keep)
        cand = [r for r in new if r["event"] == "cut_candidate"]
        blame = [r for r in new if r["event"] in ("refute", "demote", "miss_while_settled")
                 and r["detail"].get("term") == tether.IDN]
        assert _idn(ag) == before and not blame, (before, _idn(ag), blame)
        if on:
            assert cand and cand[0]["detail"]["incumbent"] == tether.NULL_MAKER, new
        else:
            assert not cand, f"MUST-FAIL: OFF a null miss reached the cut: {cand}"
    print("  N4: through settle, a null miss reaches the cut (cut_candidate, incumbent @null); OFF "
          "it does not; idn's standing byte-equal, no row blames idn")


def check_n5() -> None:
    keep = _arms(True, False, True)
    try:
        ag = _agent()
        _hand(ag, ROWS, KNOWN)
        before = _idn(ag)
        ag._d5_split("x", f"{KE} ?.col", {}, tether.NULL_MAKER)
        part = dict(ag._parts.get("x", {}))
        unbound = "x" not in ag.bound
        ag._shadow["x"] = 3
        ag.settle({"x": tether.SlotResidual("x", "transition", 3, 3, 0.0)})
        broke = [r for r in ag.led.rows() if r["event"] == "partition_broken"]
    finally:
        _restore(keep)
    assert part.get("A") == tether.NULL_MAKER and unbound, (part, ag.bound.get("x"))
    assert broke and "x" not in ag._parts and "x" not in ag.bound, (broke, ag.bound.get("x"))
    assert _idn(ag) == before, "MUST-FAIL: the null split or its revert moved idn's standing"
    print(f"  N5: the null split leaves x unbound (part A @null, part B {part.get('B')!r}); its "
          f"shadow right on a not-P row reverts it; idn's standing byte-equal")


def _left(ag, slot: str) -> None:
    """slot's mint line LEFT by 7f, with every transition already seen: _may_mint skips it."""
    seen = {(b.get(slot), a, af.get(slot)) for b, a, af, *_ in ag.trace}
    ag._leave_held[slot] = {"level": ag.level, "root": ag._root_id, "cycle": 2,
                            "slots": set(ag.slots), "skipped": 0, "seen": seen,
                            "upto": len(ag.trace)}


def _split_rows(on: bool, left: bool) -> tuple[list, dict]:
    keep = _arms(on, False, True)
    try:
        ag = _agent()
        _hand(ag, ROWS, KNOWN)
        if left:
            _left(ag, "x")
        n0 = len(ag.led)
        ag._d5_split("x", f"{KE} ?.col", {}, tether.NULL_MAKER)
        new = ag.led.rows(n0)
    finally:
        _restore(keep)
    split = next(r for r in new if r["event"] == "split")
    return new, split


def _part_rows(new: list) -> list:
    return [r for r in new if (r["detail"].get("part") or {}).get("part") == f"!{KE} ?.col"]


def check_n6() -> None:
    """r1619 (a), (b): a left slot's confirmed null cut REOPENS the line with a row and part B's
    mint runs; OFF (TETHER_D5_NULL off) the line stays left and the split row says so."""
    new, split = _split_rows(True, True)
    reopen = [r for r in new if r["event"] == "reopen"]
    assert reopen and reopen[0]["detail"]["reopen_by"] == "split", new
    assert reopen[0]["detail"]["split_P"] == f"{KE} ?.col"
    parts = _part_rows(new)
    assert parts and parts[0]["seq"] > reopen[0]["seq"], "MUST-FAIL (a): part B's mint never ran"
    assert not split["detail"]["part_b"].startswith("not searched"), split["detail"]
    off, split_off = _split_rows(False, True)
    assert not [r for r in off if r["event"] == "reopen"] and not _part_rows(off), off
    said = split_off["detail"]["part_b"]
    assert said == "not searched: the line was left at c2", \
        f"MUST-FAIL (b): a split whose part mint did not run said {said!r}"
    print(f"  N6: left line reopened (reopen_by split), part B's mint ran ({len(parts)} part rows; "
          f"part_b {split['detail']['part_b']!r}); OFF: {said!r}")


def check_n7() -> None:
    """r1619 (c): a split whose part mint parked names the park row; never 'parked' without one."""
    new, split = _split_rows(True, False)
    said = split["detail"]["part_b"]
    parks = [r for r in _part_rows(new) if r["event"] == "park"]
    if parks:
        assert said == f"searched: parked (seq {parks[0]['seq']})", \
            f"MUST-FAIL (c): the park row is not named: {said!r}"
    else:
        assert "parked" not in said, f"MUST-FAIL (c): 'parked' with no park row: {said!r}"
    print(f"  N7: part_b {said!r} ({len(parks)} park row(s) carrying the part)")


def main() -> int:
    check_n1()
    check_n2()
    check_n3()
    check_n4()
    check_n5()
    check_n6()
    check_n7()
    print("c1_nullsearch: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
