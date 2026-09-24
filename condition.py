"""The condition compiler -- Part 5.9.5, OPTION C.

A condition is **the AGENT's hypothesis in its runtime layer, approved BY THE GROUND** (ruling 5,
2026-09-22). The seed is never written. There is **no human gate**: used-and-held raises standing,
used-and-failed fades -- a human approving it would be the proctor deciding what the agent may
believe, which is the larger of the two errors the gate was avoiding.

    cond := cmp | cond ('and'|'or') cond | 'not' cond | '(' cond ')'
    cmp  := expr OP expr          OP in { == != < <= > >= }
    expr := INSTRUMENT '(' args ')' | SLOT | NUMBER

**TINY ON PURPOSE.** A grammar this small fails as a PARSE ERROR where a larger one would succeed
at reading the wrong thing -- and a wrong reading that parses is the failure mode that costs,
because it presents as a result.

**THREE-VALUED, AND THE THIRD VALUE IS THE POINT.** `True` / `False` / `None`, where `None` is
*I could not tell* -- an instrument that abstained, a slot that is not there. It is `NOT_RESOLVED`
carried through the logic instead of collapsing to `False`, because an unreadable condition and a
condition that does not hold are different facts and only one of them is evidence. `and`/`or` use
Kleene's rule: `False and None` is `False` (the answer is known whatever the unknown is), while
`True and None` is `None`.

**WHAT THIS MODULE DOES NOT DO: it does not decide whether a condition is TRUE OF THE CORPUS.** It
parses text into a checkable object and evaluates that object against a reading. Where the prose
carries no checkable condition the honest output is NOTHING -- an atom with no condition, which
therefore never confirms. **That is a real result and not a gap to be filled**; filling it would be
the seat authoring the agent's hypotheses.
"""
from __future__ import annotations

import re
import sys
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

sys.dont_write_bytecode = True

OPS: dict[str, Callable[[Any, Any], bool]] = {
    "==": lambda a, b: a == b, "!=": lambda a, b: a != b,
    "<": lambda a, b: a < b, "<=": lambda a, b: a <= b,
    ">": lambda a, b: a > b, ">=": lambda a, b: a >= b,
}

_TOKEN = re.compile(r"""
    \s*(?:
      (?P<op>==|!=|<=|>=|<|>)
    | (?P<lparen>\()
    | (?P<rparen>\))
    | (?P<comma>,)
    | (?P<num>-?\d+(?:\.\d+)?)
    | (?P<name>[A-Za-z_][A-Za-z_0-9]*(?:\.[A-Za-z_0-9]+)*)
    )""", re.X)


class ParseError(ValueError):
    """The text carries no condition this grammar can state. NOT a defect -- the expected
    outcome for prose, and the quantity the draftable-vs-blank census counts."""


def tokenize(text: str) -> list[tuple[str, str]]:
    out, i = [], 0
    while i < len(text):
        if text[i].isspace():
            i += 1
            continue
        m = _TOKEN.match(text, i)
        if not m or m.end() == i:
            raise ParseError(f"cannot tokenize at {text[i:i + 20]!r}")
        kind = m.lastgroup
        out.append((kind, m.group(kind)))
        i = m.end()
    return out


@dataclass(frozen=True)
class Cmp:
    op: str
    left: Any
    right: Any

    def __str__(self) -> str:
        return f"{self.left} {self.op} {self.right}"

    @property
    def size(self) -> int:
        return size(self)


@dataclass(frozen=True)
class Not:
    inner: Any

    def __str__(self) -> str:
        return f"not {self.inner}"

    @property
    def size(self) -> int:
        return size(self)


@dataclass(frozen=True)
class Bool:
    op: str          # "and" | "or"
    left: Any
    right: Any

    def __str__(self) -> str:
        return f"({self.left} {self.op} {self.right})"

    @property
    def size(self) -> int:
        return size(self)


@dataclass(frozen=True)
class Call:
    name: str
    args: tuple

    def __str__(self) -> str:
        return f"{self.name}({', '.join(str(a) for a in self.args)})"

    @property
    def size(self) -> int:
        return size(self)


@dataclass(frozen=True)
class Slot:
    name: str

    def __str__(self) -> str:
        return self.name

    @property
    def size(self) -> int:
        return size(self)


class _P:
    def __init__(self, toks: list[tuple[str, str]]) -> None:
        self.t, self.i = toks, 0

    def peek(self) -> tuple[str, str] | None:
        return self.t[self.i] if self.i < len(self.t) else None

    def take(self) -> tuple[str, str]:
        if self.i >= len(self.t):
            raise ParseError("ended early")
        self.i += 1
        return self.t[self.i - 1]

    def cond(self) -> Any:
        node = self.and_()
        while (p := self.peek()) and p[0] == "name" and p[1] == "or":
            self.take()
            node = Bool("or", node, self.and_())
        return node

    def and_(self) -> Any:
        node = self.not_()
        while (p := self.peek()) and p[0] == "name" and p[1] == "and":
            self.take()
            node = Bool("and", node, self.not_())
        return node

    def not_(self) -> Any:
        p = self.peek()
        if p and p[0] == "name" and p[1] == "not":
            self.take()
            return Not(self.not_())
        return self.cmp()

    def cmp(self) -> Any:
        if (p := self.peek()) and p[0] == "lparen":
            # only a parenthesised CONDITION starts here; an expression's parens follow a name
            self.take()
            node = self.cond()
            if not (self.peek() and self.peek()[0] == "rparen"):
                raise ParseError("unclosed (")
            self.take()
            return node
        left = self.expr()
        p = self.peek()
        if not p or p[0] != "op":
            # A BARE EXPRESSION IS NOT A CONDITION. `holes(o1)` is a reading, not a claim, and
            # accepting it would silently make "nonzero" the comparison nobody wrote.
            raise ParseError("a condition needs a comparison operator")
        op = self.take()[1]
        return Cmp(op, left, self.expr())

    def expr(self) -> Any:
        kind, val = self.take()
        if kind == "num":
            return float(val) if "." in val else int(val)
        if kind != "name":
            raise ParseError(f"expected a value, got {val!r}")
        if (p := self.peek()) and p[0] == "lparen":
            self.take()
            args: list = []
            if self.peek() and self.peek()[0] != "rparen":
                args.append(self.expr())
                while self.peek() and self.peek()[0] == "comma":
                    self.take()
                    args.append(self.expr())
            if not (self.peek() and self.peek()[0] == "rparen"):
                raise ParseError("unclosed ( in call")
            self.take()
            return Call(val, tuple(args))
        return Slot(val)


def parse(text: str) -> Any:
    """text -> a condition object, or `ParseError` if this grammar cannot state it."""
    p = _P(tokenize(text))
    node = p.cond()
    if p.peek() is not None:
        raise ParseError(f"trailing {p.peek()[1]!r}")
    return node


UNKNOWN = None


def size(node: Any) -> int:
    """How many nodes the condition is made of. **The thing a bargain can charge for.**

    **A GUARD WAS FREE, AND A FREE GUARD IS A FREE LUNCH.** `routine.length` counts
    constructors and never looked inside a guard, which is correct while every guard is one
    slot name and wrong the moment they can be combined: `or` is easier to satisfy than either
    side, so a routine could loosen its own termination condition at no cost and win the
    bargain by saying less. **That is precisely the term that explains everything by saying
    nothing** -- the thing `pays` exists to refuse -- and it would have arrived through the one
    part of the object nobody was pricing.

    A LEAF IS 1. Anything without a size is a leaf, which is what keeps a bare slot-name string
    at the price it has always had.
    """
    if isinstance(node, (Not,)):
        return 1 + size(node.inner)
    if isinstance(node, (Bool, Cmp)):
        return 1 + size(node.left) + size(node.right)
    if isinstance(node, Call):
        return 1 + sum(size(a) for a in node.args)
    return 1


def evaluate(node: Any, read: Callable[[str, tuple], Any]) -> bool | None:
    """`read(name, args)` returns a value, or `None` for *could not tell*.

    `None` PROPAGATES rather than collapsing to False -- Kleene, so a known answer survives an
    unknown operand and an unknown one is never reported as a refutation."""
    if isinstance(node, (int, float)):
        return node
    if isinstance(node, Slot):
        return read(node.name, ())
    if isinstance(node, Call):
        args = tuple(evaluate(a, read) for a in node.args)
        return UNKNOWN if any(a is None for a in args) else read(node.name, args)
    if isinstance(node, Not):
        v = evaluate(node.inner, read)
        return UNKNOWN if v is None else (not v)
    if isinstance(node, Cmp):
        a = evaluate(node.left, read)
        b = evaluate(node.right, read)
        if a is None or b is None:
            return UNKNOWN
        try:
            return bool(OPS[node.op](a, b))
        except TypeError:
            # `row < shape` type-checks in Python for some pairs and means nothing. An
            # incomparable pair is NOT a refutation.
            return UNKNOWN
    if isinstance(node, Bool):
        a = evaluate(node.left, read)
        b = evaluate(node.right, read)
        if node.op == "and":
            if a is False or b is False:
                return False
            return UNKNOWN if (a is None or b is None) else True
        if a is True or b is True:
            return True
        return UNKNOWN if (a is None or b is None) else False
    raise ParseError(f"cannot evaluate {node!r}")


def corpus_glosses() -> dict:
    """`{lowercased atom name: (prose gloss, source:line)}` from the READ-ONLY seed.

    The seed is never written -- this reads it and nothing else. `ATOMS.md` rows are
    `| Name | Recipe | prose gloss |`, and the gloss is informal English by design.
    """
    out: dict[str, tuple[str, str]] = {}
    for rel in ("docs/library-closure/ATOMS.md", "docs/library-closure/ATTRIBUTES.md"):
        try:
            with open(rel, encoding="utf-8") as fh:
                lines = fh.read().splitlines()
        except OSError:
            continue
        for n, ln in enumerate(lines, 1):
            if not ln.startswith("|"):
                continue
            cells = [c.strip().strip("*`").strip() for c in ln.strip("|").split("|")]
            if len(cells) < 3 or not cells[0] or cells[0].lower() in ("atom", "element"):
                continue
            key = cells[0].lower().replace(" ", "_")
            out.setdefault(key, (cells[-1], f"{rel}:{n}"))
    return out


def census(names: list[str]) -> str:
    """DRAFTABLE vs BLANK over a SCOPED atom set. The reviewer's first deliverable.

    **A BLANK IS A RESULT, NOT A GAP.** Isaiah, via the reviewer: *where a prose condition
    cannot be parsed, the honest outcome is an atom with no condition, which therefore never
    confirms.* Filling one would be the seat authoring the agent's hypotheses, which is the
    thing the human gate was removed to prevent.
    """
    gl = corpus_glosses()
    draft, blank, absent = [], [], []
    for nm in sorted(set(names)):
        hit = gl.get(nm.lower())
        if hit is None:
            absent.append(nm)
            continue
        text, src = hit
        try:
            parse(text)
            draft.append((nm, text, src))
        except ParseError as e:
            blank.append((nm, str(e)[:38], src))
    tot = len(draft) + len(blank) + len(absent)
    out = [f"  CONDITION CENSUS over {tot} scoped atoms",
           f"    DRAFTABLE  {len(draft)}   a condition this grammar can state",
           f"    BLANK      {len(blank)}   named in the seed, prose carries no checkable claim",
           f"    ABSENT     {len(absent)}  no row in the seed at all"]
    for nm, text, src in draft:
        out.append(f"      DRAFTABLE  {nm:14s} {text[:48]}   [{src}]")
    if blank:
        out.append("    BLANK (the expected outcome for prose, and a real result):")
        out += [f"      {nm:14s} {why}" for nm, why, _s in blank[:8]]
        if len(blank) > 8:
            out.append(f"      ... and {len(blank) - 8} more")
    if absent:
        out.append(f"    ABSENT: {', '.join(absent[:14])}"
                   + (f" ... +{len(absent) - 14}" if len(absent) > 14 else ""))
    return "\n".join(out)


def _selftest() -> int:
    bad = 0

    def chk(text: str, reads: dict, want: Any) -> None:
        nonlocal bad
        got = evaluate(parse(text), lambda n, a: reads.get((n, a), reads.get(n)))
        if got is not want:
            print(f"condition: {text!r} -> {got!r}, wanted {want!r}")
            bad += 1

    chk("holes(o1) > 0", {("holes", ("o1",)): 2, "o1": "o1"}, True)
    chk("o1.row == o2.row", {"o1.row": 3, "o2.row": 3}, True)
    chk("o1.row == o2.row", {"o1.row": 3, "o2.row": 4}, False)
    chk("not o1.row == o2.row", {"o1.row": 3, "o2.row": 4}, True)
    chk("o1.row < o2.row and o1.col < o2.col",
        {"o1.row": 1, "o2.row": 2, "o1.col": 1, "o2.col": 2}, True)

    # THE THIRD VALUE. An unreadable operand is UNKNOWN, never False.
    chk("o1.row == o2.row", {"o1.row": None, "o2.row": 3}, None)
    # Kleene: a known False survives an unknown
    chk("o1.row == 9 and o2.row == 9", {"o1.row": 1, "o2.row": None}, False)
    chk("o1.row == 1 or o2.row == 9", {"o1.row": 1, "o2.row": None}, True)
    chk("o1.row == 9 or o2.row == 9", {"o1.row": 1, "o2.row": None}, None)

    # WHAT MUST NOT PARSE -- each is a way prose would slip through as a reading
    for text in ("holes(o1)",                       # a reading, not a claim
                 "two objects meeting become one",  # actual corpus prose
                 "o1.row ==",                       # truncated
                 "o1.row == = 3",                   # malformed
                 "(o1.row == 3"):                   # unclosed
        try:
            parse(text)
            print(f"condition: {text!r} PARSED and must not")
            bad += 1
        except ParseError:
            pass

    print("condition: ok" if not bad else f"condition: {bad} FAILED")
    return 1 if bad else 0


if __name__ == "__main__":
    if "--census" in sys.argv:
        import arc_atoms
        import arc_predict
        print(census([a.name for a in
                      arc_atoms.three_spaces(arc_predict.predict())]))
        raise SystemExit(0)
    raise SystemExit(_selftest())
