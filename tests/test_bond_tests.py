"""BUILD 2 item 1, THE BOND TESTS OVER A WINDOW (TETHER_BOND_TEST; the reviewer 2026-11-03 r897; the
Operators Table's tests). composer.window_test reads two operands' per-frame values; each test
decides only where the window discriminates. Game-free except the last check (a gridworld agent).

MF-B+  both move on every occasion -> True; one moves alone -> False; the same values -> None (TEST)
MF-B→  A moves, then B -> True; B moves before A ever has -> False; always together -> None
MF-B⇒  B absent until A fires, then comes -> True; B present before A fires -> False; B never
       comes -> None (FIELD)
MF-B−  A moves while B is absent -> True; A moves while B is present (B absent elsewhere) -> False;
       B never absent -> None
MF-B⋛  values that merely differ -> None (TEST); ∥ -> None (TEST, settled at the bargain)
MF-Bmixed  one occasion for and one against -> None, never a soft false
MF-Brow  a gridworld agent's end_run writes one bond_tests row whose tally covers every tested
       junction once per bond

    python tests/test_bond_tests.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import composer  # noqa: E402


def w(*xs):
    """a window of one-slot operand values."""
    return [(x,) for x in xs]


def test(bond, a, b, still=True, skip=()):
    """(verdict, kind); `still` True: another bound slot stayed on every frame (specific)."""
    r = composer.window_test(bond, w(*a), w(*b), [still] * len(a), skip)
    return (r[0], r[2])


def main():
    assert composer._BOND_TEST, "TETHER_BOND_TEST is ON by default"
    got = {
        "+ both": test("+", [0, 1, 2], [5, 6, 7]),
        "+ alone": test("+", [0, 1, 1], [5, 5, 5]),
        "+ same": test("+", [0, 1, 2], [0, 1, 2]),
        "→ then": test("→", [0, 1, 1], [5, 5, 6]),
        "→ before": test("→", [0, 0, 1], [5, 6, 6]),
        "→ together": test("→", [0, 1, 2], [5, 6, 7]),
        "⇒ produces": test("⇒", [0, 1, 1], [None, None, 3]),
        "⇒ before": test("⇒", [0, 0, 1, 1], [4, None, None, 3]),
        "⇒ never": test("⇒", [0, 1, 2], [4, 4, 4]),
        "− absent": test("−", [0, 1, 2], [None, None, None]),
        "− present": test("−", [0, 1, 2, 2], [4, 4, 4, None]),
        "− never": test("−", [0, 1, 2], [4, 4, 4]),
        "⋛ differ": test("⋛", [3, 4, 5], [1, 1, 1]),
        "∥": test("∥", [0, 1, 2], [5, 6, 7]),
        "mixed": test("+", [0, 1, 1, 2], [5, 6, 7, 8]),
        "+ not specific": test("+", [0, 1, 2], [5, 6, 7], still=False),
        "→ not specific": test("→", [0, 1, 1], [5, 5, 6], still=False),
        "+ reset skipped": test("+", [0, 1, 1], [5, 6, 5], skip=(2,)),
    }
    want = {
        "+ both": (True, ""), "+ alone": (False, ""), "+ same": (None, "TEST"),
        "→ then": (True, ""), "→ before": (False, ""), "→ together": (None, "TEST"),
        "⇒ produces": (True, ""), "⇒ before": (False, ""), "⇒ never": (None, "FIELD"),
        "− absent": (True, ""), "− present": (False, ""), "− never": (None, "TEST"),
        "⋛ differ": (None, "TEST"), "∥": (None, "TEST"), "mixed": (None, "TEST"),
        "+ not specific": (None, "TEST"), "→ not specific": (None, "TEST"),
        "+ reset skipped": (True, ""),
    }
    bad = {k: (got[k], want[k]) for k in want if got[k] != want[k]}
    assert not bad, ("MF-B the window tests", bad)
    # r934 b: a junction where + and → both read True stays UNKNOWN, ambiguous; one True settles
    a, b = w(0, 1, 2, 3), w(5, 6, 7, 8)
    both = {bond: composer.window_test(bond, a, b, [True] * 4) for bond in composer.WINDOW_BONDS}
    both["→"] = (True, "", "", {})
    amb = composer.junction_verdict(both)
    one = composer.junction_verdict({**both, "+": (None, "", "TEST", {}), "→": (True, "", "", {})})
    assert amb == (None, "ambiguous: +, →") and one == ("→", "settled: →"), ("MF-Bamb", amb, one)
    ev = composer.window_test("+", w(0, 1, 2), w(5, 6, 7), [False, True, False])[3]
    assert ev == {"occasions": 2, "deciding": [1, 2], "specific": [1]}, ("MF-Bev evidence", ev)
    import gamma
    import gridworld
    import ledger
    import tether
    import world
    env = world.bind(gridworld.family("default", 0))
    led = ledger.Ledger()
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
    for _ in range(12):
        ag.step()
    ag.end_run("cap")
    rows = [r for r in led.rows() if r.get("event") == "bond_tests"]
    assert len(rows) == 1, ("MF-Brow one bond_tests row", len(rows))
    d = rows[0]["detail"] if "detail" in rows[0] else rows[0]
    per = {b: sum(v.values()) for b, v in d["tally"].items()}
    assert all(n == d["tested"] for n in per.values()), ("MF-Brow tally", per, d["tested"])
    side = d["unbound_by_side"]
    assert side["names_no_atom"] + side["atom_bound_nowhere"] == d["unbound"], ("MF-Brow sides", d)
    print(f"  MF-B {len(want)} windows: conjunction / sequence / production / subtraction decide "
          f"where the window discriminates, None otherwise; comparison and disjunction None "
          f"(settled at the bargain); mixed None; not specific None; a reset frame skipped")
    print("  MF-Bamb conjunction and sequence both True -> UNKNOWN, ambiguous; one -> settled; "
          "MF-Bev the row's evidence: occasions, deciding frames, the specific ones")
    print(f"  MF-Brow gridworld 12 steps: {d['junctions']} junctions, {d['tested']} tested, "
          f"{d['unbound']} untestable {d['unbound_by_side']}; outcome {d['junction_outcome']}")
    print("test_bond_tests OK")


if __name__ == "__main__":
    main()
