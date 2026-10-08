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
        for a, b in FRAMES:
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
    for cond in ("o1.h > 0", "o1.drow != 0"):
        assert isinstance(C.compile_candidate({"condition": cond}, atoms), C.Compiled), cond
    for cond, reason in [("o1.drow < 0", "sign gives BOOL, which negate does not accept"),
                         ("o1.colour_changed == 1", "idn does not accept BOOL"),
                         ("o1.colour_changed == 0", "negate does not accept BOOL"),
                         ("touching(o1, o2) == 1", "no pairwise atom"),
                         ("frame.came > 0", "events are not slots"),
                         ("board.completed > 0", "not an object slot")]:
        got = C.compile_candidate({"condition": cond}, atoms)
        assert isinstance(got, C.Refusal) and reason in got.reason, (cond, got)


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


if __name__ == "__main__":
    n, refused = test_every_compiled_row_agrees_with_evaluate()
    test_each_named_refusal_is_refused_with_its_reason()
    caught = test_a_swapped_binding_is_caught()
    print(f"compile: {n} candidates compiled, each agreeing with condition.evaluate on "
          f"{len(FRAMES)} frames and on an unread operand; "
          f"{sum(refused.values())} refused by reason {dict(sorted(refused.items()))}; "
          f"the swapped binding caught on {len(caught)} frame(s)")
