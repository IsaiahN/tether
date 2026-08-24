"""The utterance grammar. Typed; ill-typed composition raises with its reason.

Terminals produce RECORDs, so precedence is type-checkable: BET's GROUND consumes a
PERCEIVE record, ACT's NEED consumes a BET record. That is the loop's dependency chain
enforced by the type system rather than by convention.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from enum import Enum
from typing import Any

sys.dont_write_bytecode = True


class T(Enum):
    OBJECT = "OBJECT"    # a slot's identity
    ATTR = "ATTR"        # an attribute value
    REGION = "REGION"    # an address
    PRED = "PRED"        # a relation that holds or not
    OBJ = "OBJ"          # a complete objective
    RECORD = "RECORD"    # a citable id
    PRICE = "PRICE"      # a cost claim with its evidence count, or an explicit null


class Ill(TypeError):
    """An ill-typed composition. Always raised with its reason, never silent."""


# the three check currencies a head can be paid in
EXECUTABLE = "executable"
LEDGER = "ledger"
COMPLETENESS = "completeness"


@dataclass(frozen=True)
class Prime:
    name: str
    category: str
    in_types: tuple[T, ...]
    out_type: T
    gloss: str = ""
    check: str | None = None
    star: int | None = None      # index of a repeating position, if any


def _p(*a: Any, **k: Any) -> Prime:
    return Prime(*a, **k)


PRIMES: dict[str, Prime] = {p.name: p for p in [
    _p("BE_AT", "Relation", (T.OBJECT, T.REGION), T.PRED, "an object is at a region"),
    _p("TOUCH", "Relation", (T.OBJECT, T.OBJECT), T.PRED, "two objects are in contact"),
    _p("BECOME", "Relation", (T.OBJECT, T.ATTR), T.PRED, "an object takes an attribute"),
    _p("BECAUSE", "Relation", (T.PRED, T.PRED), T.PRED, "one relation causes another"),
    _p("SAME", "Quality", (T.ATTR, T.ATTR), T.PRED, "two attributes are equal"),
    _p("OTHER", "Quality", (T.ATTR, T.ATTR), T.PRED, "two attributes differ"),
    _p("NOT", "Quality", (T.PRED,), T.PRED, "negation"),
    _p("EXIST", "Modality", (T.OBJECT,), T.PRED, "an object exists"),
    _p("CAN", "Modality", (T.PRED,), T.PRED, "a relation is achievable"),
    _p("ALL", "Quantity", (T.PRED,), T.OBJ, "holds for all in scope"),
    _p("SOME", "Quantity", (T.PRED,), T.OBJ, "holds for some in scope"),
    _p("ONE", "Quantity", (T.PRED,), T.OBJ, "holds for exactly one"),
    _p("NONE", "Quantity", (T.PRED,), T.OBJ, "holds for none"),
]}

SEE, CHANGED, SETTLE, STAND = "SEE", "CHANGED", "SETTLE", "STAND"
WANT, GROUND, DERIVE, PAY, NEED = "WANT", "GROUND", "DERIVE", "PAY", "NEED"

HEADS: dict[str, Prime] = {p.name: p for p in [
    _p(SEE, "Speech-act", (T.OBJECT, T.REGION, T.ATTR), T.PRED,
       "per-slot state claim", check=EXECUTABLE),
    _p(CHANGED, "Speech-act", (T.REGION, T.ATTR, T.ATTR), T.PRED,
       "a region went a -> b; the set asserts nothing else changed", check=COMPLETENESS),
    _p(SETTLE, "Speech-act", (T.RECORD, T.PRED), T.PRED,
       "the previous bet, by id: held or broke", check=EXECUTABLE),
    _p(STAND, "Speech-act", (T.RECORD, T.ATTR), T.PRED,
       "a held term strengthened, weakened or died", check=LEDGER),
    _p(WANT, "Speech-act", (T.OBJ,), T.PRED,
       "the objective; a typed hole here is a probe", check=EXECUTABLE),
    _p(GROUND, "Speech-act", (T.RECORD, T.RECORD), T.PRED,
       "pure citation: this step's perceive, then held terms", check=LEDGER, star=1),
    _p(DERIVE, "Speech-act", (T.PRED, T.RECORD, T.PRED), T.PRED,
       "cited records applied to the ground equal the bet", check=EXECUTABLE, star=1),
    _p(PAY, "Speech-act", (T.PRICE,), T.PRED,
       "the acknowledged cost with its evidence count, or an explicit null", check=LEDGER),
    _p(NEED, "Speech-act", (T.RECORD, T.ATTR), T.PRED,
       "this step's bet, by id, and the action it ran", check=LEDGER),
]}

PERCEIVE, BET, ACT = "PERCEIVE", "BET", "ACT"

TERMINALS: dict[str, Prime] = {p.name: p for p in [
    _p(PERCEIVE, "Terminal", (T.PRED,), T.RECORD, "SEE*, CHANGED*, SETTLE?, STAND*", star=0),
    _p(BET, "Terminal", (T.PRED, T.PRED, T.PRED, T.PRED), T.RECORD, "WANT, GROUND, DERIVE, PAY"),
    _p(ACT, "Terminal", (T.PRED,), T.RECORD, "NEED"),
]}

_PERCEIVE_HEADS = (SEE, CHANGED, SETTLE, STAND)
_BET_ORDER = (WANT, GROUND, DERIVE, PAY)


@dataclass(frozen=True)
class Leaf:
    type: T
    value: Any
    kind: str | None = None     # a RECORD's kind: perceive / bet / act / term
    tag: str | None = None


@dataclass(frozen=True)
class Term:
    head: str
    args: tuple = ()

    @property
    def type(self) -> T:
        return _prime(self.head).out_type

    def __repr__(self) -> str:
        return f"{self.head}({', '.join(map(_show, self.args))})"


def _show(x: Any) -> str:
    if isinstance(x, T):
        return f"<{x.value}>"
    if isinstance(x, Leaf):
        return repr(x.value)
    return repr(x)


def _prime(head: str) -> Prime:
    p = PRIMES.get(head) or HEADS.get(head) or TERMINALS.get(head)
    if p is None:
        raise Ill(f"unknown head '{head}'")
    return p


def is_hole(x: Any) -> bool:
    """A bare type as a leaf: a template without content. This is how a question is asked."""
    return isinstance(x, T)


def type_of(x: Any) -> T:
    if isinstance(x, Term):
        return x.type
    if isinstance(x, Leaf):
        return x.type
    if isinstance(x, T):
        return x
    raise Ill(f"not a typed value: {x!r}")


def _matches(sig: tuple[T, ...], star: int | None, got: tuple[T, ...]) -> bool:
    if star is None:
        return got == sig
    pre, rep, post = sig[:star], sig[star], sig[star + 1:]
    if len(got) < len(pre) + len(post):
        return False
    mid = got[len(pre):len(got) - len(post)] if post else got[len(pre):]
    tail_ok = got[len(got) - len(post):] == post if post else True
    return got[:len(pre)] == pre and tail_ok and all(t == rep for t in mid)


def compose(head: str, *args: Any) -> Term:
    """Type-checked composition. Raises Ill with its reason; never composes silently."""
    p = _prime(head)
    got = tuple(type_of(a) for a in args)
    if not _matches(p.in_types, p.star, got):
        want = tuple(t.value + ("*" if p.star == i else "") for i, t in enumerate(p.in_types))
        raise Ill(f"ill-typed: {head} expects {want} but got {tuple(t.value for t in got)}")
    if head in TERMINALS:
        _check_terminal(head, args)
    return Term(head, tuple(args))


def _check_terminal(head: str, args: tuple) -> None:
    heads = tuple(a.head if isinstance(a, Term) else None for a in args)
    if head == PERCEIVE:
        bad = [h for h in heads if h not in _PERCEIVE_HEADS]
        if bad:
            raise Ill(f"ill-typed: PERCEIVE admits {_PERCEIVE_HEADS}, got {bad[0]}")
        if heads.count(SETTLE) > 1:
            raise Ill("ill-typed: PERCEIVE settles at most one bet")
        return
    order = _BET_ORDER if head == BET else (NEED,)
    if heads != order:
        raise Ill(f"ill-typed: {head} is {order} in order, got {heads}")
    if head == BET:
        probe = is_hole(args[2].args[-1])
        if is_hole(args[0].args[0]) and not probe:
            raise Ill("ill-typed: DERIVE against a holed WANT composes with a probe only")
        if not probe and len(args[2].args) < 3:
            raise Ill("ill-typed: DERIVE cites no record and is not a probe")


def ref(record_id: Any, kind: str) -> Leaf:
    return Leaf(T.RECORD, str(record_id), kind=str(kind))


def price(value: float | None, n: int | None = None, reason: str | None = None) -> Leaf:
    """A number with its evidence count, or an explicit null with a reason.
    A number without evidence is representable here and refused at the gate."""
    return Leaf(T.PRICE, (value, n, reason))
