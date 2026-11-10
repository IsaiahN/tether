"""C1 PART 5, THE KNOWN-EFFECT CONDITION (the reviewer 2026-11-09 r1592 (a)-(e); Isaiah 09-29
ruling 1 kept: a guard names an intent, not a button).

  K1  Interface.known_forms offers a press's attribute forms only when ONE effect is known in the
      context: an unseen press, and a press with two effects there, offer nothing (MF (a))
  K2  a hand trace on slot x: idn right on the rows whose press was known to move ?.row (up on one,
      down on the other) and wrong on the ?.col rows, 2 a side: D5 splits on "KNOWN_EFFECT ?.row",
      priced by _guard_bits (c); the signed forms alone separate nothing. A CUT-LOGIC witness: it
      calls _d5_cut directly, and the live loop names no maker for an unbound slot, so its entry
      through settle is test_c1_nullsearch N4 (the reviewer 2026-11-10 r1612 (3))
  K3  MF (b): the same rows with button names ("ACTION1", "left", "o0.row+") in place of forms:
      refused by shape, no split
  K4  MF (d): forms that do not separate the right rows from the wrong ones: no split
  K5  the arm OFF: the separating forms are not offered, no split
  K6  a gridworld run with the arm ON fills the side map per step, every form attribute-shaped,
      and the first step's press offers nothing (no effect was known before it)

    python tests/test_c1_action.py
"""
from __future__ import annotations

import os
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True
os.environ.setdefault("TETHER_AGENT_SEED", "0")

import gamma  # noqa: E402
import gridworld  # noqa: E402
import interface as IFace  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def _agent() -> tether.Agent:
    env = world.bind(gridworld.family("default", 0, 4))
    return tether.Agent(env, gamma.Gamma(env.atoms(), game="c1_action"), tether.Config(),
                        ledger.Ledger())


def _hand(rows: list[tuple]) -> tether.Agent:
    """Slot x, one intent kind on every row (so no intent cut), idn predicting each:
    (x before, x after, the forms the press was known to move)."""
    ag = _agent()
    ag.trace = [({"x": b}, "A", {"x": a}, IFace.TOUCH, None) for b, a, _ in rows]
    ag._trace_pos = None
    ag.slots = [*ag.slots, "x"]
    ag.alphabet["x"] = 8
    ag._d5_rows["x"] = [(i, "idn") for i in range(len(rows))]
    ag._kn_eff = {id(t[0]): frozenset(f) for t, (_, _, f) in zip(ag.trace, rows, strict=True)}
    # TETHER_KNOWN_CORE (default ON, r1633) reads the three-valued table: one known effect per
    # press here, so holds = union = its forms (the same meaning as _kn_eff)
    ag._kn3 = {k: (v, v) for k, v in ag._kn_eff.items()}
    return ag


ROW_UP, ROW_DN = {"?.row", "?.row+"}, {"?.row", "?.row-"}
COL_UP, COL_DN = {"?.col", "?.col+"}, {"?.col", "?.col-"}
SEPARATES = [(1, 1, ROW_UP), (1, 3, COL_UP), (2, 2, ROW_DN), (2, 5, COL_DN)]


def check_k1() -> None:
    ag = _agent()
    ctx = ("c",)
    ag.iface.table = {"A": {"by_ctx": {ctx: {(("o0.row", 1),)}}, "n": 1, "delta": {}},
                      "B": {"by_ctx": {ctx: {(("o0.row", 1),), (("o0.col", -1),)}}, "n": 2,
                            "delta": {}}}
    assert ag.iface.known_forms("A", ctx) == {"?.row", "?.row+"}, ag.iface.known_forms("A", ctx)
    assert ag.iface.known_forms("A", ("other",)) == frozenset(), "MUST-FAIL (a): unseen context"
    assert ag.iface.known_forms("C", ctx) == frozenset(), "MUST-FAIL (a): unseen press"
    assert ag.iface.known_forms("B", ctx) == frozenset(), "MUST-FAIL (a): two effects known"
    print("  K1: one known effect offers {?.row, ?.row+}; an unseen press, an unseen context and "
          "two effects offer nothing")


def check_k2_k5() -> None:
    keep = tether._D5_ACTION
    try:
        tether._D5_ACTION = True
        cut = _hand(SEPARATES)._d5_cut("x", "idn")
        assert cut is not None and cut[0] == f"{tether.KNOWN_EFFECT} ?.row", cut
        assert cut[1]["guard_bits"] > 0 and cut[1]["right_on_p"] == 2, cut
        print(f"  K2: split on {cut[0]!r}, {cut[1]}")
        planted = [(1, 1, {"ACTION1", "left"}), (1, 3, {"ACTION2", "o0.row+"}),
                   (2, 2, {"ACTION1", "left"}), (2, 5, {"ACTION2", "o0.row+"})]
        assert _hand(planted)._d5_cut("x", "idn") is None, "MUST-FAIL (b): a button name split"
        print("  K3: button names in the side map are refused by shape: no split")
        mixed = [(1, 1, ROW_UP), (1, 3, ROW_DN), (2, 2, COL_UP), (2, 5, COL_DN)]
        assert _hand(mixed)._d5_cut("x", "idn") is None, "MUST-FAIL (d): split on no separation"
        print("  K4: forms that do not separate right from wrong: no split")
        tether._D5_ACTION = False
        assert _hand(SEPARATES)._d5_cut("x", "idn") is None, "the arm is OFF and it split"
        print("  K5: arm OFF: the separating forms are not offered, no split")
    finally:
        tether._D5_ACTION = keep


def check_k6() -> None:
    keep = tether._D5_ACTION
    try:
        tether._D5_ACTION = True
        ag = _agent()
        ag.step()
        first = ag._kn_eff_now
        for _ in range(29):
            ag.step()
    finally:
        tether._D5_ACTION = keep
    forms = [f for v in ag._kn_eff.values() for f in v]
    assert first == frozenset(), first
    assert forms, "occasion: no known effect in 30 gridworld steps"
    assert all(tether._KNOWN_FORM.fullmatch(f) for f in forms), forms
    assert all(ag._kn_eff.values()), "an empty effect was stored"
    print(f"  K6: gridworld, 30 steps ON: {len(ag._kn_eff)} of 30 states with a known effect "
          f"in the side map, every form "
          f"attribute-shaped ({sorted(set(forms))}); the first press offered nothing")


def main() -> int:
    check_k1()
    check_k2_k5()
    check_k6()
    print("c1_action: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
