"""evalctx: every Ctx a TERM IS EVALUATED IN goes through `Agent._eval_ctx`, and nothing else.

THE DEFECT THIS REINTRODUCES, 2026-10-04, `F431.3`. `Ctx.acted_self` defaults `False`, and an
AST census found it set at **3 of 11 constructions -- and the three were the PRICING
functions**. So a term guarded on `ACTED_SELF` evaluated as IDENTITY wherever it was JUDGED.
Measured on `click_only` seeds 3 and 5: **23 candidates per seed explain every frame at
`left == 0.0`, all 23 pay the bargain, and `bears_on` refuses all 23. Zero admitted.** The slot
went to a term wrong on two frames at twice the price, while `inc?ACTED_SELF` -- the literal
rule of that world -- sat refused at the cheapest price on the board.

**AND THE ROOT WAS THE UNPACK, NOT THE CONSTRUCTOR, which is why this seat checks a SHAPE
rather than a keyword.** `bears_on` looped `for state, action, _actual, *_ in robs` and threw
`landed` away: the field was not in scope to supply, so no amount of care at the `Ctx(` call
could have reached it. A keyword-presence check would have passed on a site that had nothing
to pass. Routing every construction through one function is what makes the omission
impossible rather than merely discouraged.

NOT NAMED `census`. `census.py` is the SPLIT GUARD and means branch accounting; two quantities
under one word is `A6i`, and this file would have been the fourth instance in a week.

THE EXEMPTION IS DATA AND IT CARRIES ITS OWN EXPIRY. `_ops` builds `Ctx(operands=(value,))` to
apply an `operand_term`, and that is exempt ON A CHECKABLE FACT rather than on judgement:
`_branches` constructs `Term((a,))` with NO `guard=`, so an operand_term is always unguarded
and `acted_self` is never read there. **The seat asserts that fact.** The moment a branch is
built with a guard the exemption fails loudly instead of silently covering a blind site.

WHAT THIS SEAT DOES NOT CLAIM, and the distinction is the reviewer's: routing a site is not
fixing it. The LIVE callers -- `_predict`, `_discrepancy`, `goal_residual`, `_goal_target` --
have `_last_action` and no `_last_landed`, so they pass `landed=None` and read `acted_self`
False exactly as before. They are routed so the next guarded caller is not blind. **A green
seat here means no site can omit the field, NOT that every site can supply it.**
"""
from __future__ import annotations

import ast
import pathlib
import sys

sys.dont_write_bytecode = True

ROOT = pathlib.Path(__file__).resolve().parent.parent
TARGET = ROOT / "tether.py"

# EXEMPTIONS AS DATA, NEVER AS LOGIC -- a table can be pinned and read; a condition widens
# quietly. One entry, and it expires on the fact asserted in `_branch_fact`.
EXEMPT = {"_ops": "applies an operand_term, which `_branches` builds unguarded"}
CONSTRUCTOR = "_eval_ctx"


def _owner(fns, ln):
    c = [f for f in fns if f[0] <= ln <= f[1]]
    return min(c, key=lambda f: f[1] - f[0])[2] if c else "?"


def _sites(src: str):
    """Every direct `Ctx(` construction, as (line, enclosing function)."""
    tree = ast.parse(src)
    fns = [(n.lineno, n.end_lineno, n.name) for n in ast.walk(tree)
           if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    return [(n.lineno, _owner(fns, n.lineno)) for n in ast.walk(tree)
            if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "Ctx"]


def _stray(src: str):
    """Constructions outside the one constructor and outside the exemption table."""
    return [(ln, fn) for ln, fn in _sites(src)
            if fn != CONSTRUCTOR and fn not in EXEMPT]


def _branch_fact(src: str) -> list[str]:
    """THE EXEMPTION'S EXPIRY. `_branches` must build its terms WITHOUT a guard.

    If a branch ever carries one, `_ops`' bare `Ctx` becomes a blind site and the exemption
    above is covering it. Checked rather than remembered.
    """
    tree = ast.parse(src)
    for n in ast.walk(tree):
        if isinstance(n, ast.FunctionDef) and n.name == "_branches":
            for c in ast.walk(n):
                if (isinstance(c, ast.Call) and getattr(c.func, "id", None) == "Term"
                        and any(k.arg == "guard" for k in c.keywords)):
                    return [f"`_branches` builds a GUARDED Term at line {c.lineno}: the "
                            f"`_ops` exemption is now covering a blind site and must go."]
            return []
    return ["`_branches` not found -- the `_ops` exemption rests on a fact nobody can check."]


def _self_test(src: str) -> list[str]:
    """REINTRODUCE THE DEFECT, NEVER DISABLE THE CHECK.

    A guard whose failure path is never exercised is indistinguishable from one that cannot
    fail -- which is how the focus seat stayed green since installation. So the seat proves
    it goes RED on a direct construction before its green is worth anything.
    """
    out = []
    hurt = src.replace("    def bears_on(self",
                       "    def _reintroduced(self, slot, state):\n"
                       "        return Ctx(action=None, operands=())\n\n"
                       "    def bears_on(self", 1)
    if hurt == src:
        out.append("self-test could not reintroduce the defect -- anchor missing")
    elif not any(fn == "_reintroduced" for _, fn in _stray(hurt)):
        out.append("SELF-TEST FAILED: a direct `Ctx(` construction was not flagged. "
                   "This seat cannot fail, so its green says nothing.")
    return out


def main() -> int:
    src = TARGET.read_text(encoding="utf-8")
    bad = _self_test(src) + _branch_fact(src)
    for ln, fn in _stray(src):
        bad.append(f"tether.py:{ln} builds a `Ctx` directly in `{fn}` -- route it through "
                   f"`Agent.{CONSTRUCTOR}`, which supplies `acted_self`. A term guarded on "
                   f"ACTED_SELF reads as IDENTITY in a Ctx that omits it.")
    sites = _sites(src)
    if not bad:
        print(f"  evalctx ok -- {len(sites)} Ctx constructions, "
              f"{len([1 for _, f in sites if f == CONSTRUCTOR])} in the constructor, "
              f"{len([1 for _, f in sites if f in EXEMPT])} exempt ({', '.join(EXEMPT)})")
        return 0
    for b in bad:
        print(f"  evalctx: {b}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
