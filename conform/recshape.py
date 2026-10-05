"""recshape: every consumer of a history/trace record unpacks it at the RECORD'S OWN WIDTH.

THE DEFECT, 2026-10-04. `history()` returns `(before, action, after-value, intent, landed)`
and `self.trace` rows are the same width. **Consumers disagreed at FOUR widths -- 2, 3, 4 and
5 -- across fifteen unpack sites, EIGHT of them hiding the tail behind `*_`.** Two cost
something measurable:

    `_invent`      unpacked THREE and raised `ValueError` on its first call. `_INVENT` is
                   default-OFF, so the arm had never executed since `history()` widened --
                   every "`_INVENT` off" reading was also "`_INVENT` could not run"
    `bears_on`     unpacked `state, action, _actual, *_` and threw `landed` away, so the
                   field `?ACTED_SELF` needs was NOT IN SCOPE TO SUPPLY. On `click_only`
                   that refused all 23 perfect guarded candidates per seed, 0 admitted

**AND THE TOLERANCE IS WHAT MADE BOTH INVISIBLE.** `*_` accepts any row at least as wide as
the names before it, so a consumer could drift from the producer for weeks and nothing would
fail. It also hid a STALE FIXTURE: the M2 spectator check hand-built a 3-tuple history and
passed, because `*_` did not care. **The repair is not "be careful with unpacks" -- it is that
a widening must break a TEST rather than a RUN**, which is this seat.

A LEADING STAR IS REFUSED TOO, AND THAT IS THE SUBTLE HALF. `for *_, land in hist` reads the
last field by position and looks explicit. Append a field and `land` silently becomes the new
one -- a wrong value rather than a crash, which is the worse failure. Both `_guards` counters
were written that way.

WIDTH IS WHAT THIS CHECKS, AND IT IS DELIBERATELY NOT TYPES. `self.trace`'s third element is
the after-STATE and `history()`'s is the slot's VALUE -- two record types of the same width,
and conflating them would be the `A6i` this project keeps paying for. The seat asserts the
ARITY every consumer agrees to; what each field MEANS is the caller's business.
"""
from __future__ import annotations

import ast
import pathlib
import sys

sys.dont_write_bytecode = True

ROOT = pathlib.Path(__file__).resolve().parent.parent
TARGET = ROOT / "tether.py"

# The names that hold a history/trace-shaped sequence. DATA, not logic -- a table can be
# pinned and read, a condition widens quietly.
SOURCES = {"hist", "robs", "obs", "trace"}


def _width_of_record(tree) -> int | None:
    """THE CANONICAL WIDTH, TAKEN FROM THE PRODUCER AND NEVER TYPED IN HERE.

    `history()` returns a list comprehension of one tuple; its length IS the record width.
    A number written into this file would be the next thing to go stale, which is the exact
    failure the seat exists to stop -- one level up.
    """
    for n in ast.walk(tree):
        if isinstance(n, ast.FunctionDef) and n.name == "history":
            for c in ast.walk(n):
                if isinstance(c, ast.ListComp) and isinstance(c.elt, ast.Tuple):
                    return len(c.elt.elts)
    return None


def _owner(fns, ln):
    c = [f for f in fns if f[0] <= ln <= f[1]]
    return min(c, key=lambda f: f[1] - f[0])[2] if c else "?"


def _sites(src: str):
    tree = ast.parse(src)
    fns = [(n.lineno, n.end_lineno, n.name) for n in ast.walk(tree)
           if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    found = []

    def names(node):
        out = set()
        for n in ast.walk(node):
            if isinstance(n, ast.Name):
                out.add(n.id)
            if isinstance(n, ast.Attribute):
                out.add(n.attr)
        return out

    def add(ln, tgt, itr):
        if not isinstance(tgt, ast.Tuple) or not (names(itr) & SOURCES):
            return
        star = any(isinstance(e, ast.Starred) for e in tgt.elts)
        found.append((ln, _owner(fns, ln), len(tgt.elts), star))

    for n in ast.walk(tree):
        # COMPREHENSIONS TOO. The first census of this class walked only `For` nodes and
        # MISSED THREE SITES, one of them a starred dict comprehension over `self.trace`.
        if isinstance(n, ast.For):
            add(n.lineno, n.target, n.iter)
        elif isinstance(n, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            for g in n.generators:
                add(n.lineno, g.target, g.iter)
        elif isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Tuple):
            add(n.lineno, n.targets[0], n.value)
    return tree, sorted(set(found))


def _bad(src: str):
    tree, sites = _sites(src)
    want = _width_of_record(tree)
    out = []
    if want is None:
        return ["`history()`'s record could not be read, so no width can be asserted."], 0, []
    for ln, fn, w, star in sites:
        if star:
            out.append(f"tether.py:{ln} in `{fn}` unpacks a record with `*`. A star hides a "
                       f"widening; a LEADING star rebinds the named field to a new one "
                       f"silently. Name all {want} fields.")
        elif w != want:
            out.append(f"tether.py:{ln} in `{fn}` unpacks {w} fields from a {want}-field "
                       f"record. `_invent` did this and raised on its first call.")
    return out, want, sites


def _self_test(src: str) -> list[str]:
    """REINTRODUCE THE DEFECT, NEVER DISABLE THE CHECK. Both shapes, because they fail
    differently: a short unpack CRASHES and a starred one returns a WRONG VALUE."""
    out = []
    for name, hurt in (
        # anchored on a live unpack; the first anchor sat in `_invent`, removed 2026-10-05 (F439)
        ("short", src.replace("        for state, action, actual, intent, landed in hist:",
                              "        for state, action, actual in hist:", 1)),
        ("starred", src.replace("        for st, _a, _v, _intent, _landed in robs:",
                                "        for st, _a, _v, *_ in robs:", 1)),
    ):
        if hurt == src:
            out.append(f"self-test could not reintroduce the {name} defect -- anchor missing")
        elif not _bad(hurt)[0]:
            out.append(f"SELF-TEST FAILED: a {name} unpack was not flagged. This seat "
                       f"cannot fail, so its green says nothing.")
    return out


def main() -> int:
    src = TARGET.read_text(encoding="utf-8")
    bad, want, sites = _bad(src)
    bad = _self_test(src) + bad
    if not bad:
        print(f"  recshape ok -- {len(sites)} record unpacks, all {want} fields, no star")
        return 0
    for b in bad:
        print(f"  recshape: {b}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
