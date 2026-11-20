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

# The PARAMETER names that may hold a history/trace-shaped sequence. 2026-11-19: this
# table used to be read as "any mention of one of these names anywhere in an iterable is
# a record", which flagged a 2-field unpack of `obs` where `obs` was the fifth field of
# a `contact` tuple (tether.py:3678) and a deliberate trailing-star discard (8029). A
# name alone is not evidence of a record: it must be a parameter with one of these names
# or be ASSIGNED from a producer below. DATA, not logic -- a table can be pinned.
SOURCES = {"hist", "robs", "obs", "trace"}


def _names(node) -> set[str]:
    out: set[str] = set()
    for n in ast.walk(node):
        if isinstance(n, ast.Name):
            out.add(n.id)
        elif isinstance(n, ast.Attribute):
            out.add(n.attr)
    return out


def _record_names(fn, want: int | None) -> set[str]:
    """Names in ONE function that provably hold a history/trace record.

    A parameter named in SOURCES is a record by the function's own contract. A local is
    one only when assigned from `history()`, `_residual_obs`, `self.trace`, or an
    expression already built from a record (a filtered/derived list). An ordinary local
    named `obs` is NOT a record -- that name collision was 26 false findings.
    """
    rec = {a.arg for a in (*fn.args.args, *fn.args.kwonlyargs, *fn.args.posonlyargs)
           if a.arg in SOURCES}
    for n in ast.walk(fn):
        if not isinstance(n, ast.Assign) or len(n.targets) != 1:
            continue
        tgt, val = n.targets[0], n.value
        if not isinstance(tgt, ast.Name):
            continue
        produced = (isinstance(val, ast.Call) and isinstance(val.func, ast.Attribute)
                    and val.func.attr in ("history", "_residual_obs"))
        produced = produced or (isinstance(val, ast.Attribute) and val.attr == "trace")
        # A filtered/derived list of records is itself a record -- but ONLY through a
        # comprehension over a known record. A broad "mentions a record anywhere"
        # rule made ordinary 2- and 4-tuples (`r`, `_v`, `best`) look like history rows.
        if isinstance(val, (ast.ListComp, ast.SetComp, ast.GeneratorExp)):
            over_record = any(
                (isinstance(g.iter, ast.Name) and g.iter.id in rec)
                or (isinstance(g.iter, ast.Attribute) and g.iter.attr == "trace")
                for g in val.generators)
            # A projection to a DIFFERENT tuple shape is a new record with its own
            # contract, not a history row: `_unbundle` builds 3-tuples from trace rows.
            preserves = isinstance(val.elt, ast.Name) or (
                isinstance(val.elt, ast.Tuple) and len(val.elt.elts) == want)
            produced = produced or (over_record and preserves)
        if produced:
            rec.add(tgt.id)
    return rec


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
    fns = [(n.lineno, n.end_lineno, n.name, n) for n in ast.walk(tree)
           if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    found = []
    _rec_cache: dict[int, set[str]] = {}

    def is_record(itr, ln) -> bool:
        owner = next((f for f in fns if f[0] <= ln <= f[1]), None)
        if owner is None:
            return False
        if owner[3] not in _rec_cache:
            _rec_cache[owner[3]] = _record_names(owner[3], want)
        rec = _rec_cache[owner[3]]
        # The iterable must BE a record name, not merely mention one in a subscript,
        # a field unpack, or a nested expression. `self.trace` is a record directly.
        if isinstance(itr, ast.Name):
            return itr.id in rec
        if isinstance(itr, ast.Attribute):
            return itr.attr == "trace"
        return False

    want = _width_of_record(tree)

    def add(ln, tgt, itr):
        if not isinstance(tgt, ast.Tuple) or not is_record(itr, ln):
            return
        elts = tgt.elts
        # A TRAILING star (`first, *_rest`) anchors the named field to element 0 and
        # discards the tail -- safe under a widening, so it is not a finding unless the
        # named prefix already exceeds the record's width. A LEADING or MIDDLE star
        # (`*_head, last`) shifts every name after it onto a different field, which is
        # the silent rebind this seat exists to catch.
        trailing = bool(elts) and isinstance(elts[-1], ast.Starred)
        star = any(isinstance(e, ast.Starred) for e in elts[:-1])
        named = len(elts) - 1 if trailing else len(elts)
        if trailing and not star and want is not None and named <= want:
            return
        found.append((ln, _owner(fns, ln), named, star))

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
                                "        for *_head, _landed in robs:", 1)),
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
