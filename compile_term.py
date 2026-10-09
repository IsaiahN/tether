"""compile_term: a library candidate's condition, compiled to a Term over the atoms Gamma holds
(M2, docs/cohesion/METAPROGRAMMING_DESIGN.md section 3; the reviewer 2026-10-08 21:08Z).

`compile_candidate(cand, atoms) -> Compiled | Refusal`. The library is REACH; nothing enters
Gamma's alphabet by being preloaded. A candidate becomes something the agent can bet with only as
a Term over the atoms it already has, so the 4,000 entries never become 4,000 functions.

THE TABLE IS DATA: each condition shape (operator, and what the right side is) names the atom
chain section 3 gives for it. EVERY chain then passes the SAME typing the mint applies
(`gamma.accepts_type`, chain links, operand types). A row whose chain fails it is REFUSED with
the typing reason, never compiled anyway: an ill-typed term the composer would never admit is
not a term the library may offer. The equivalence fixture checks every compiled row against
`condition.evaluate`, the independently written reference (Figure 10).

Works from the candidate's CONDITION TEXT, not its template label, so the term means what the
library wrote even where a label reads otherwise.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Any

import condition
import gamma

SAME = gamma.SAME_AS_TARGET

# (op, right side) -> (atom chain run on the target slot, operand side or None[, operand chain]).
# right side: "zero" / "one" for a constant, "slot" for another object's same reading.
# operand side: "x" -> the other object's slot is operand 0; "o" -> the chain runs on the OTHER
# object's slot with this object's as operand (the reversed binding, for "<"); "self" -> the
# target slot itself, transformed by the operand chain before it fills operand 0 (a tree).
TABLE: dict[tuple[str, str], tuple] = {
    (">", "zero"): (("sign",), None),               # up: a positive delta
    ("!=", "zero"): (("abs_delta", "sign"), None),  # moves: section 3's chain
    # down: "not positive AND non-zero" -- never the chain sign . holds . negate, which is "not
    # positive" and wrong at zero (the reviewer 2026-10-08 23:54Z)
    ("<", "zero"): (("sign", "holds", "negate", "both"), "self", ("abs_delta", "sign", "holds")),
    ("==", "one"): (("holds",), None),              # BOOL holds: the truth as a predicate
    ("==", "zero"): (("holds", "negate"), None),    # BOOL fails
    ("==", "slot"): (("same",), "x"),               # with / same / level / both
    ("!=", "slot"): (("other",), "x"),              # unlike / other
    (">", "slot"): (("above",), "x"),               # more / after
    ("<", "slot"): (("above",), "o"),               # less / before: the binding reversed
}
# A pair reading written as a call, and the pair atom that grounds it (the reviewer 2026-10-08
# 23:23Z): "== 1" -> the atom, "== 0" -> the atom then negate; it runs on the first object
# with the second as its operand. A pair call not listed here has no atom and is refused.
PAIR = {"touching": "touches"}
# Shapes that have no slot to run on, refused by name (section 3, section 7c).
NOT_SLOTS = {"frame": "events are not slots", "board": "the board is not an object slot"}


@dataclass(frozen=True)
class Compiled:
    slot: str                 # the slot the term runs on, e.g. "o1.drow"
    term: gamma.Term
    operand: str | None       # the slot that fills operand 0, if any


@dataclass(frozen=True)
class Refusal:
    reason: str


@cache
def readings() -> dict[str, dict]:
    p = Path(__file__).parent / "library" / "readings.json"
    return json.loads(p.read_text(encoding="utf-8"))["readings"]


def _split(slot: str) -> tuple[str, str]:
    obj, _, reading = slot.partition(".")
    return obj, reading


def _typed(chain: tuple[gamma.Atom, ...], slot_type: str, operand_type: str | None,
           op_chain: tuple[gamma.Atom, ...] = ()) -> str | None:
    """None when the chain is well-typed on a slot of `slot_type`, else the reason. An operand
    chain (a tree) must itself be well-typed on the operand slot and give what the reader
    of the operand wants."""
    if not gamma.accepts_type(chain[0], slot_type):
        return f"{chain[0].name} does not accept {slot_type}"
    for a, b in zip(chain, chain[1:], strict=False):
        if not gamma.accepts_type(b, a.out_type):
            return f"{a.name} gives {a.out_type}, which {b.name} does not accept"
    readers = [a for a in chain if a.reads_operand]
    if not readers:
        return (f"{chain[0].name} reads no operand and the condition names a second slot"
                if operand_type is not None else None)
    if operand_type is None:
        return f"{readers[0].name} reads an operand and the condition gives none"
    given = operand_type
    if op_chain:
        why = _typed(op_chain, operand_type, None)
        if why:
            return f"the operand chain: {why}"
        given = op_chain[-1].out_type
    for r in readers:
        want = slot_type if r.operand_type == SAME else r.operand_type
        if want is not None and given != want:
            return f"{r.name} wants a {want} operand, the condition gives {given}"
    return None


def compile_candidate(cand: dict, atoms: dict[str, gamma.Atom]) -> Compiled | Refusal:
    """One candidate (`{"condition": "o1.drow > 0", ...}`), compiled or refused with a reason."""
    try:
        node = condition.parse(cand["condition"])
    except condition.ParseError as e:
        return Refusal(f"the condition does not parse: {e}")
    if (isinstance(node, condition.Cmp) and isinstance(node.left, condition.Call)
            and node.left.name in PAIR):
        return _pair(node, atoms)
    if isinstance(node, condition.Cmp) and isinstance(node.left, condition.Call):
        # a pair reading names TWO objects; the atoms read one slot each (`touching` reads
        # whether its object touches ANY object), so no chain says "this pair"
        return Refusal(f"no pairwise atom: {node.left.name}(o, x) names two objects and no atom "
                       f"reads the pair")
    if not (isinstance(node, condition.Cmp) and isinstance(node.left, condition.Slot)):
        return Refusal("not a comparison of one slot")
    target = node.left.name
    obj, reading = _split(target)
    if obj in NOT_SLOTS:
        return Refusal(NOT_SLOTS[obj])
    rtype = (readings().get(reading) or {}).get("type")
    if rtype is None:
        return Refusal(f"{reading!r} is not a library reading")
    right = node.right
    if isinstance(right, condition.Slot):
        kind, other = "slot", right.name
        if _split(other)[1] != reading:
            return Refusal("the two sides read different quantities")
    elif right in (0, 1):
        kind, other = ("zero" if right == 0 else "one"), None
    else:
        return Refusal(f"no template compares {reading} with the constant {right}")
    row = TABLE.get((node.op, kind))
    if row is None:
        return Refusal(f"no template for {node.op} against a {kind}")
    names, side = row[0], row[1]
    op_names = row[2] if len(row) > 2 else ()
    missing = [n for n in (*names, *op_names) if n not in atoms]
    if missing:
        return Refusal(f"Gamma holds no atom {missing}")
    chain = tuple(atoms[n] for n in names)
    op_chain = tuple(atoms[n] for n in op_names)
    run_on, operand = target, None
    if side == "x":
        operand = other
    elif side == "o":
        run_on, operand = other, target
    elif side == "self":
        operand = target
    why = _typed(chain, rtype, rtype if operand else None, op_chain)
    if why:
        return Refusal(why)
    term = gamma.Term(chain, operand=operand,
                      operand_term=gamma.Term(op_chain) if op_chain else None)
    return Compiled(run_on, term, operand)


def _pair(node: Any, atoms: dict[str, gamma.Atom]) -> Compiled | Refusal:
    call = node.left
    if (len(call.args) != 2 or not all(isinstance(a, condition.Slot) for a in call.args)
            or node.op != "==" or node.right not in (0, 1)):
        return Refusal(f"no template for {call} {node.op} {node.right}")
    names = (PAIR[call.name],) if node.right == 1 else (PAIR[call.name], "negate")
    missing = [n for n in names if n not in atoms]
    if missing:
        return Refusal(f"Gamma holds no atom {missing}")
    chain = tuple(atoms[n] for n in names)
    why = _typed(chain, "OBJECT", "OBJECT")
    if why:
        return Refusal(why)
    first, second = (a.name for a in call.args)
    return Compiled(first, gamma.Term(chain, operand=second), second)


def run(c: Compiled, frame: dict[str, Any]) -> bool | None:
    """The compiled term on one frame (slot -> value): True / False, or None for could not tell."""
    from gamma import NOT_RESOLVED, Ctx
    if frame.get(c.slot) is None or (c.operand and frame.get(c.operand) is None):
        return None
    ops: tuple = ()
    if c.operand:
        o = frame[c.operand]
        if c.term.operand_term is not None:      # a tree: the operand is computed
            o = c.term.operand_term.apply(o, Ctx())
            if o is NOT_RESOLVED:
                return None
        ops = (o,)
    v = c.term.apply(frame[c.slot], Ctx(operands=ops))
    return None if v is NOT_RESOLVED else bool(v)
