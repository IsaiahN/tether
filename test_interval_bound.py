"""THE INTERVAL BOUND (TETHER_INTERVAL_BOUND; the reviewer 2026-10-21 17:46). In-process, the real
ARC atoms (arc_atoms.three_spaces), objectives built as Agent._value_of builds them.

  (0) THE TABLE: every atom three_spaces builds has a VALUE_TURNS row of a known kind, and its
      function is registered with that kind.
  (R) EQUIVALENCE: 4,000 random objectives over the declared atoms (a first atom, an optional
      middle, a quantifier), random operands and groups, alphabets, currents (some outside the
      alphabet) and domains: _priced_hit ON equals OFF, and so do the choice-row calls.
      PRECONDITIONS: the bound answered > 500 calls, > 200 of them found nothing, > 50 found an
      unseen value.
  (a) MUST-FAIL, A WRONG DECLARATION: a parity atom (v % 2 == 0) declared "operand" -- under the
      CHECK the walk and the bound disagree (and without the CHECK the answer would differ).
  (b) AN UNDECLARED ATOM: the real "parity" (row "walk") and an atom with no row -> the walk,
      equal to OFF.
  (c) NOT_RESOLVED FROM CTX: an empty group, no operand, an unreadable operand, a non-int operand
      -> equal to OFF (a non-int breakpoint walks).
  (d) THE RING TIE: two satisfying unseen values at the nearest distance -> the same pick as the
      walk, by the draw key.
  (e) OFF identity and (f) the CHECK games are game runs, apart (vc33, then sp80).

    python test_interval_bound.py
"""
from __future__ import annotations

import os
import random
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import arc_atoms  # noqa: E402
import arc_predict  # noqa: E402
import gamma  # noqa: E402
import tether  # noqa: E402
from gamma import Atom, Ctx, Term  # noqa: E402

NR = tether.NOT_RESOLVED
ATOMS = {a.name: a for a in arc_atoms.three_spaces(arc_predict.predict())}
FIRST = ["same", "other", "above", "below", "rank_in", "count", "aligned", "all_same",
         "any_same", "none_same", "is_max", "is_min", "is_mode", "sum_group", "distinct", "sign",
         "holds", "negate", "idn", "both", "either"]
MIDDLE = [None, "negate", "both", "either", "other", "same", "below", "above"]
LAST = ["all", "any", "none"]


def sat_of(term: Term, ctx: Ctx):
    """Agent._value_of's objective, as it builds it."""
    def _sat(v: int):
        r = term.apply(v, ctx)
        return None if r is NR else bool(r)
    if tether._INTERVAL_BOUND:
        _sat.breaks = lambda: tether._value_breaks(term, ctx)
    return _sat


def dom_of(values, alpha, rows=None):
    d = tether._PricedDomain(values)
    d.alpha, d.key, d.seed = alpha, f"k{alpha}", "s"
    d.counts = dict.fromkeys(values, 1)
    d.note = (lambda *a: rows.append(repr(a))) if rows is not None else None
    return d


def hit(term, ctx, current, ordered, values, alpha, on, check=False):
    was = (tether._INTERVAL_BOUND, tether._INTERVAL_BOUND_CHECK)
    tether._INTERVAL_BOUND, tether._INTERVAL_BOUND_CHECK = on, check
    try:
        rows: list = []
        got = tether._priced_hit(sat_of(term, ctx), current, ordered, dom_of(values, alpha, rows))
        return got, rows
    finally:
        tether._INTERVAL_BOUND, tether._INTERVAL_BOUND_CHECK = was


def table() -> None:
    turns = arc_atoms.value_turns()
    missing = sorted(n for n in ATOMS if n not in turns)
    assert not missing, missing
    bad = sorted(n for n, (k, _why) in turns.items() if k not in gamma.TURN_KINDS)
    assert not bad, bad
    for n, a in ATOMS.items():
        assert gamma.VALUE_TURNS.get(a.fn) == turns[n][0], (n, gamma.VALUE_TURNS.get(a.fn))
    kinds = sorted({turns[n][0] for n in ATOMS})
    print(f"(0) the table: {len(ATOMS)} atoms, every one with a row and registered; kinds {kinds}")


def equivalence() -> None:
    rnd = random.Random(11)
    before = dict(tether.INTERVAL_N)
    n = found_none = found_unseen = 0
    for _ in range(4000):
        names = [rnd.choice(FIRST)] + [m for m in [rnd.choice(MIDDLE)] if m] + [rnd.choice(LAST)]
        term = Term(tuple(ATOMS[x] for x in names))
        alpha = rnd.choice([12, 40, 200, 1025])
        ops = () if rnd.random() < 0.15 else (rnd.randrange(-3, alpha + 3),)
        grp = tuple(rnd.randrange(0, alpha) for _ in range(rnd.choice([0, 1, 3, 6])))
        ctx = Ctx(operands=ops, group=grp)
        current = rnd.randrange(-2, alpha + 2)
        values = {rnd.randrange(0, alpha) for _ in range(rnd.randint(1, 7))}
        ordered = rnd.random() < 0.8
        r = term.apply(current, ctx)
        if r is NR or bool(r):                       # objective_step answers before the walk
            continue
        n0 = tether.INTERVAL_N["bound"]
        on = hit(term, ctx, current, ordered, values, alpha, True)
        off = hit(term, ctx, current, ordered, values, alpha, False)
        assert on == off, (names, ops, grp, current, ordered, sorted(values), alpha, on, off)
        if tether.INTERVAL_N["bound"] > n0:
            n += 1
            walked = tether._walk_unseen(sat_of(term, ctx), current, ordered,
                                         dom_of(values, alpha),
                                         alpha if ordered else None,
                                         lambda v, a=alpha: tether.FR.draw_key(f"k{a}", v, "s"))
            found_none += walked is None
            found_unseen += walked is not None
    assert n > 500 and found_none > 200 and found_unseen > 50, (n, found_none, found_unseen)
    used = {k: tether.INTERVAL_N[k] - before[k] for k in before}
    print(f"(R) 4,000 objectives: ON equals OFF (the answer and the choice rows); the bound "
          f"answered {n} calls ({found_none} with nothing satisfying, {found_unseen} with an "
          f"unseen value); counters {used}")


def wrong_declaration() -> None:
    planted = Atom("planted_parity", lambda v, _c: int(v % 2 == 0), "POSITION", "PRED")
    gamma.declare_turns(planted, "operand")
    term = Term((planted, ATOMS["all"]))
    ctx = Ctx(operands=(5,))
    # current 3: the real nearest are 2 and 4; the wrong pieces' representatives (0 even, 1 odd,
    # 5 odd, 6 even) put the nearest satisfying ring at 3, values 0 and 6
    d0 = tether.INTERVAL_N["disagree"]
    got = hit(term, ctx, 3, True, {3}, 200, True, check=True)
    walk = hit(term, ctx, 3, True, {3}, 200, False)
    bound = hit(term, ctx, 3, True, {3}, 200, True)
    assert got == walk, (got, walk)                       # the check uses the walk's answer
    assert tether.INTERVAL_N["disagree"] > d0, "MF-a: the CHECK did not see a wrong declaration"
    assert bound != walk, ("MF-a: the plant was not consequential", bound, walk)
    print(f"(a) a parity declared 'operand': the CHECK disagrees (walk {walk[0]}, bound "
          f"{bound[0]}) and uses the walk's answer")


def undeclared() -> None:
    for term in (Term((ATOMS["parity"], ATOMS["holds"], ATOMS["all"])),
                 Term((Atom("no_row", lambda v, _c: int(v == 3), "POSITION", "PRED"),
                       ATOMS["all"]))):
        off = hit(term, Ctx(), 9, True, {9}, 300, False)
        w0, b0 = tether.INTERVAL_N["walk"], tether.INTERVAL_N["bound"]
        on = hit(term, Ctx(), 9, True, {9}, 300, True)
        assert on == off, (term, on, off)
        assert tether.INTERVAL_N["walk"] == w0 + 1 and tether.INTERVAL_N["bound"] == b0, (
            "MF-b: an undeclared atom was not walked", term)
    print("(b) the real 'parity' (row 'walk') and an atom with no row: walked, equal to OFF")


def not_resolved() -> None:
    cases = [("rank_in", Ctx(group=())), ("aligned", Ctx(group=())), ("below", Ctx()),
             ("both", Ctx(operands=(NR,))), ("below", Ctx(operands=((1, 2),))),
             ("aligned", Ctx(group=(3, "x")))]
    n = 0
    for first, ctx in cases:
        term = Term((ATOMS[first], ATOMS["all"]))
        for current in (0, 5, 299):
            n += 1
            try:
                off = hit(term, ctx, current, True, {current}, 300, False)
            except TypeError:                        # the walk itself cannot read it
                off = "raises"
            try:
                on = hit(term, ctx, current, True, {current}, 300, True)
            except TypeError:
                on = "raises"
            assert on == off, (first, ctx, current, on, off)
    assert n == 3 * len(cases), n
    print(f"(c) {len(cases)} ctx cases x 3 currents, _priced_hit called directly (empty "
          f"group, no operand, unreadable and non-int operands, a non-int group value): "
          f"equal to OFF")


def ring_tie() -> None:
    dk = lambda v: tether.FR.draw_key("k300", v, "s")  # noqa: E731
    seen = 0
    for c in range(20, 280, 7):
        ctx = Ctx(group=(c - 5, c + 5))
        term = Term((ATOMS["aligned"], ATOMS["all"]))
        on = hit(term, ctx, c, True, {c}, 300, True)
        off = hit(term, ctx, c, True, {c}, 300, False)
        assert on == off == (min((c - 5, c + 5), key=dk), []), (c, on, off)
        seen += 1
    print(f"(d) {seen} ring ties (c-5 and c+5 both satisfy): the bound picks the walk's value "
          f"by the draw key")


def zero_one() -> None:
    # (i) holds turns at 0 AND 1: on an ordered slot whose shown values miss both, the nearest
    # satisfying value is 0 or 1 -- the bound must find the walk's
    term = Term((ATOMS["holds"], ATOMS["all"]))
    assert tether._value_breaks(term, Ctx()) == {0, 1}, tether._value_breaks(term, Ctx())
    for current in (2, 5, 40, 150):
        on = hit(term, Ctx(), current, True, {current, current + 3}, 200, True, check=True)
        off = hit(term, Ctx(), current, True, {current, current + 3}, 200, False)
        assert on == off and on[0] == 1, (current, on, off)
    print("(i) holds (zero_one): B = {0, 1}; from 2, 5, 40, 150 the bound and the walk both "
          "reach 1")


def unordered() -> None:
    # (ii) the walk's unordered pick is min(ring, key=dk) over every v in range(alpha), v !=
    # current, v not in dom, evaluate(v); the bound lists the true pieces' values in the same
    # ascending order. Two true pieces: below 40 and above 160 (either . all over below/above)
    d0, a0, b0 = (tether.INTERVAL_N[k] for k in ("disagree", "agree", "bound"))
    for first, o in (("below", 40), ("above", 160), ("other", 77), ("same", 77)):
        term = Term((ATOMS[first], ATOMS["all"]))
        for current in (0, 77, 100, 199):
            for values in ({current}, {current, 3, 170}):
                on = hit(term, Ctx(operands=(o,)), current, False, values, 200, True, check=True)
                off = hit(term, Ctx(operands=(o,)), current, False, values, 200, False)
                assert on == off, (first, o, current, values, on, off)
    two = Term((ATOMS["rank_in"], ATOMS["other"], ATOMS["all"]))
    ctx2 = Ctx(operands=(1,), group=(50, 120))
    for current in (10, 80, 190):
        on = hit(two, ctx2, current, False, {current}, 200, True, check=True)
        off = hit(two, ctx2, current, False, {current}, 200, False)
        assert on == off, (current, on, off)
    # a satisfying SHOWN value returns before the unseen branch, so not every case reaches it
    n = tether.INTERVAL_N["bound"] - b0
    assert n >= 15 and tether.INTERVAL_N["disagree"] == d0, (n, tether.INTERVAL_N)
    assert tether.INTERVAL_N["agree"] - a0 == n, ("a bound call the CHECK did not compare", n)
    print(f"(ii) unordered: {n} bound calls, two true pieces included (rank_in.other with the "
          f"group at 50 and 120: true below 51 and above 120), the CHECK 0 disagree, equal to OFF")


def run_end() -> None:
    # (iii) the nearest true value is the END of a run, not a breakpoint: below 30 from 100 is 29
    term = Term((ATOMS["below"], ATOMS["all"]))
    for current, values, want in ((100, {100}, 29), (100, {100, 150}, 29), (100, {100, 29, 28}, 29),
                                  (2, {2}, 1)):
        on = hit(term, Ctx(operands=(30,)), current, True, values, 200, True, check=True)
        off = hit(term, Ctx(operands=(30,)), current, True, values, 200, False)
        assert on == off and on[0] == want, (current, values, on, off)
    print("(iii) below 30: from 100 -> 29 (a run's end, unseen; also with 150 shown), with 29 "
          "shown -> the shown 29, from 2 -> 1; equal to the walk")


if __name__ == "__main__":
    table()
    equivalence()
    wrong_declaration()
    undeclared()
    not_resolved()
    ring_tie()
    zero_one()
    unordered()
    run_end()
    print("test_interval_bound: pass")
