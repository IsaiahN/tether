"""The compiler's equivalence fixture (M2; METAPROGRAMMING_DESIGN section 3, section 8).

Every candidate the library's own templates generate, over every reading it holds, is compiled.
Each compiled Term must give the SAME three-valued answer as `condition.evaluate` on 12 hand-built
frames: both objects, both signs, zero, equal. Every refusal must carry its reason. Must-fail:
the "less" row's reversed binding swapped back is caught. Run: python test_compile.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import arc_atoms  # noqa: E402
import arc_predict  # noqa: E402
import compile_term as C  # noqa: E402
import condition  # noqa: E402

sys.path.insert(0, "library")
import library_runtime  # noqa: E402

FRAMES = [(3, 1), (1, 3), (2, 2), (0, 0), (-1, 2), (2, -1), (-2, -2), (0, 5), (5, 0), (-3, 0),
          (0, -3), (1, 1)]


# A BOOL slot holds 0 or 1: its frames are its domain (the reviewer 2026-10-08 23:54Z). Integer
# frames on a BOOL reading produced disagreements no BOOL slot can show.
BOOL_FRAMES = [(0, 0), (0, 1), (1, 0), (1, 1)]


def _atoms() -> dict:
    return {a.name: a for a in arc_atoms.three_spaces(arc_predict.predict())}


def candidates() -> list[dict]:
    """Every (reading, template) the library's runtime would generate, on o1 against o2."""
    out = []
    for r, spec in C.readings().items():
        for label, tpl in library_runtime.TEMPLATES.get(spec.get("type"), []):
            out.append({"reading": r, "template": label,
                        "condition": tpl.format(o="o1", x="o2", r=r)})
    return out


def disagreements(atoms: dict) -> tuple[list[str], int, dict[str, int]]:
    """(disagreements, compiled count, refusals by reason)."""
    bad, n, refused = [], 0, {}
    for cand in candidates():
        c = C.compile_candidate(cand, atoms)
        if isinstance(c, C.Refusal):
            refused[c.reason] = refused.get(c.reason, 0) + 1
            continue
        n += 1
        node = condition.parse(cand["condition"])
        r = cand["reading"]
        if r in C.CHANGE_OF:                     # current and previous attribute, the flag agreeing
            attr = C.CHANGE_OF[r]
            for cur, prev in FRAMES:
                frame = {f"o1.{attr}": cur, f"o1.{attr}{C.PREV}": prev, f"o1.{r}": int(cur != prev)}
                want = condition.evaluate(node, lambda name, _args, f=frame: f.get(name))
                got = C.run(c, frame)
                if got != want:
                    bad.append(f"{cand['condition']} on {attr} {cur} after {prev}: term {got}, "
                               f"evaluate {want}")
            frame = {f"o1.{attr}": 1, f"o1.{r}": None}   # no earlier frame: could not tell
            if C.run(c, frame) is not None:
                bad.append(f"{cand['condition']} with no earlier frame: term told")
            continue
        domain = BOOL_FRAMES if C.readings()[r].get("type") == "BOOL" else FRAMES
        for a, b in domain:
            frame = {f"o1.{r}": a, f"o2.{r}": b}
            want = condition.evaluate(node, lambda name, _args, f=frame: f.get(name))
            got = C.run(c, frame)
            if got != want:
                bad.append(f"{cand['condition']} on o1={a} o2={b}: term {got}, evaluate {want}")
        frame = {f"o1.{r}": 1}                       # o2 unread: both must say "could not tell"
        want = condition.evaluate(node, lambda name, _args, f=frame: f.get(name))
        got = C.run(c, frame)
        if got != want:
            bad.append(f"{cand['condition']} with o2 unread: term {got}, evaluate {want}")
    return bad, n, refused


def test_every_compiled_row_agrees_with_evaluate():
    bad, n, refused = disagreements(_atoms())
    assert n, "nothing compiled"
    assert not bad, f"{len(bad)} disagreement(s), first: {bad[:3]}"
    assert all(reason for reason in refused), "a refusal without its reason"
    return n, refused


def test_each_named_refusal_is_refused_with_its_reason():
    atoms = _atoms()
    # 7a: "present" (EXTENT > 0) and "moves" (!= 0) compile since sign accepts EXTENT
    # 7a and 7b: these compile now (present, moves; down as the tree; BOOL holds / fails)
    for cond in ("o1.h > 0", "o1.drow != 0", "o1.drow < 0", "o1.colour_changed == 1",
                 "o1.colour_changed == 0"):
        assert isinstance(C.compile_candidate({"condition": cond}, atoms), C.Compiled), cond
    for cond, reason in [
                         ("contact(o1, o2) == 1", "no pairwise atom"),
                         ("frame.came > 0", "events are not slots"),
                         ("board.completed > 0", "not an object slot"),
                         ("@goal.row < o2.row", "@goal is the board's progress marker"),
                         ("o1.row > @goal.row", "@goal is the board's progress marker")]:
        got = C.compile_candidate({"condition": cond}, atoms)
        assert isinstance(got, C.Refusal) and reason in got.reason, (cond, got)


def test_a_rule_candidate_is_refused_as_quantified():
    """A RULE candidate from the library's own view is refused as quantified over the group;
    MUST-FAIL: the same candidate without its quantifier compiles, so the quantifier is what
    refuses it."""
    atoms = _atoms()
    lib = library_runtime.Library("library").load()
    for key in lib.seed:
        for cand in lib.view(key, "RULE"):
            bare = {k: v for k, v in cand.items() if k not in ("quantifier", "scope")}
            if isinstance(C.compile_candidate(bare, atoms), C.Compiled):
                got = C.compile_candidate(cand, atoms)
                assert isinstance(got, C.Refusal) and got.reason == C.QUANTIFIED, (cand, got)
                return cand["condition"]
    raise AssertionError("no RULE candidate in the library compiles without its quantifier")


def test_a_change_reading_compiles_on_its_attribute():
    """The 01:03Z row: a change reading compiles on the attribute it is a change OF, against that
    attribute one frame earlier. MUST-FAIL: same/other swapped is caught by the frames."""
    import tether
    assert C.PREV == tether.PREV, "compile_term.PREV drifted from tether.PREV"
    atoms = _atoms()
    yes = C.compile_candidate({"condition": "o1.colour_changed == 1"}, atoms)
    no = C.compile_candidate({"condition": "o1.colour_changed == 0"}, atoms)
    assert isinstance(yes, C.Compiled) and isinstance(no, C.Compiled), (yes, no)
    assert (yes.slot, yes.term.name, yes.operand) == ("o1.colour", "other<o1.colour~1>",
                                                      "o1.colour~1"), yes
    assert no.term.name == "same<o1.colour~1>", no
    real = C._change

    def swapped(obj, reading, op, right, atoms):
        return real(obj, reading, op, 1 - right if right in (0, 1) else right, atoms)
    C._change = swapped
    try:
        bad, _n, _r = disagreements(atoms)
    finally:
        C._change = real
    caught = [b for b in bad if "colour_changed" in b]
    assert caught, "same/other swapped in the change row was not caught"
    return len(caught)


def test_down_as_the_plain_chain_is_caught_at_zero():
    """MUST-FAIL: "down" compiled as sign . holds . negate means "not positive" and is wrong
    at zero; the equivalence catches it. The ruled form is the tree."""
    atoms = _atoms()
    keep = C.TABLE[("<", "zero")]
    C.TABLE[("<", "zero")] = (("sign", "holds", "negate"), None)
    try:
        bad, _n, _r = disagreements(atoms)
    finally:
        C.TABLE[("<", "zero")] = keep
    at_zero = [b for b in bad if "< 0 on o1=0 " in b]
    assert at_zero, "down as the plain chain was not caught at zero"
    return at_zero


def test_a_swapped_binding_is_caught():
    """MUST-FAIL: "less" compiled with the binding NOT reversed means "more"; it must disagree."""
    atoms = _atoms()
    keep = C.TABLE[("<", "slot")]
    C.TABLE[("<", "slot")] = (("above",), "x")
    try:
        bad, _n, _r = disagreements(atoms)
    finally:
        C.TABLE[("<", "slot")] = keep
    assert bad, "the swapped binding in the 'less' row was not caught"
    return bad


def _rec(r, c, cells):
    return {"row": r, "col": c, "structure": frozenset(cells)}


SQ, DOT, ELL = [(0, 0), (0, 1), (1, 0), (1, 1)], [(0, 0)], [(0, 0), (1, 0), (2, 0), (2, 1)]
PAIR_FRAMES = [  # (o1, o2): right, left, below, above, apart, diagonal, dots, an L against a dot
    (_rec(0, 0, SQ), _rec(0, 2, SQ)), (_rec(0, 2, SQ), _rec(0, 0, SQ)),
    (_rec(0, 0, SQ), _rec(2, 0, SQ)), (_rec(2, 0, SQ), _rec(0, 0, SQ)),
    (_rec(0, 0, SQ), _rec(0, 3, SQ)), (_rec(0, 0, SQ), _rec(2, 2, SQ)),
    (_rec(5, 5, DOT), _rec(5, 6, DOT)), (_rec(5, 5, DOT), _rec(6, 6, DOT)),
    (_rec(0, 0, ELL), _rec(1, 1, DOT)), (_rec(0, 0, ELL), _rec(0, 2, DOT)),
]


def _adjacent(a: dict, b: dict) -> int:
    """An independent reader: every pair of cells, at grid distance exactly one."""
    ca = [(a["row"] + r, a["col"] + c) for r, c in a["structure"]]
    cb = [(b["row"] + r, b["col"] + c) for r, c in b["structure"]]
    return int(any(abs(r1 - r2) + abs(c1 - c2) == 1 for r1, c1 in ca for r2, c2 in cb))


def pair_disagreements(atoms: dict, rebind_self: bool = False) -> list[str]:
    bad = []
    for cond in ("touching(o1, o2) == 1", "touching(o1, o2) == 0"):
        c = C.compile_candidate({"condition": cond}, atoms)
        assert isinstance(c, C.Compiled), (cond, c)
        if rebind_self:                       # the planted defect: the operand is o1 itself
            c = C.Compiled(c.slot, C.gamma.Term(c.term.atoms, operand="o1"), "o1")
        node = condition.parse(cond)
        for a, b in PAIR_FRAMES:
            frame = {"o1": a, "o2": b}

            def read(name, args, f=frame):
                return _adjacent(*args) if name == "touching" else f.get(name)
            want, got = condition.evaluate(node, read), C.run(c, frame)
            if got != want:
                bad.append(f"{cond} on {a} / {b}: term {got}, evaluate {want}")
        frame = {"o1": PAIR_FRAMES[0][0]}       # o2 unread
        want = condition.evaluate(node, lambda n, args, f=frame: _adjacent(*args)
                                  if n == "touching" else f.get(n))
        if C.run(c, frame) != want:
            bad.append(f"{cond} with o2 unread: term {C.run(c, frame)}, evaluate {want}")
    return bad


def test_the_pair_atom_agrees_with_an_independent_reading():
    """touches<x> (the reviewer 2026-10-08 23:23Z): touching(o, x) == 1 / == 0 compile to
    touches<x> and touches . negate<x>, and agree with an independently written adjacency on
    ten record pairs (face contact each way, apart, diagonal only, single cells, an L) and on an
    unread operand. MUST-FAIL: the operand bound to the object itself is caught."""
    atoms = _atoms()
    bad = pair_disagreements(atoms)
    assert not bad, bad[:3]
    caught = pair_disagreements(atoms, rebind_self=True)
    assert caught, "an operand bound to the object itself was not caught"
    return len(caught)


if __name__ == "__main__":
    n, refused = test_every_compiled_row_agrees_with_evaluate()
    test_each_named_refusal_is_refused_with_its_reason()
    caught = test_a_swapped_binding_is_caught()
    down_caught = test_down_as_the_plain_chain_is_caught_at_zero()
    rule = test_a_rule_candidate_is_refused_as_quantified()
    change_caught = test_a_change_reading_compiles_on_its_attribute()
    self_bound = test_the_pair_atom_agrees_with_an_independent_reading()
    print(f"compile: {n} candidates compiled, each agreeing with condition.evaluate on "
          f"{len(FRAMES)} frames and on an unread operand; "
          f"{sum(refused.values())} refused by reason {dict(sorted(refused.items()))}; "
          f"the swapped binding caught on {len(caught)} frame(s); touches<x> agrees on "
          f"{len(PAIR_FRAMES)} pairs and an unread operand, its self-bound operand caught on "
          f"{self_bound}; down as the plain chain caught on {len(down_caught)} zero frame(s); "
          f"the RULE candidate {rule!r} refused as quantified, and compiles without it; "
          f"colour_changed compiles on colour~1, same/other swapped caught on {change_caught}")
