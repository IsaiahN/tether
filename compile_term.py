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
import re
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Any

import armflag
import condition
import gamma
import relations

SAME = gamma.SAME_AS_TARGET
# B3 (the reviewer 2026-10-11 12:25 CDT): under the arm a pair reading (`dist_o3`) is typed by its
# relation, and a slot may be compared with its OWN earlier reading (`slot~1`) -- toward is
# "o0.dist_o3 < o0.dist_o3~1", away the converse. OFF; reason in conform/arms.py.
_RELATION_SET = armflag.arm("TETHER_RELATION_SET")

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
# B1 (TETHER_RELATION_SET): where Gamma holds `below`, "<" against a slot keeps the LEFT party
# the subject instead of reversing the binding. Read off the atom set, so it follows the arm.
CONVERSE: dict[tuple[str, str], tuple] = {("<", "slot"): (("below",), "x")}
# BOTH SPELLINGS (TETHER_RELATION_SET; the reviewer 2026-10-11): a one-atom comparison of two
# slots says the same thing run on either party -- above(a, b) is below(b, a); same and other
# are symmetric. The atom that reads it from the other side.
SWAP = {"above": "below", "below": "above", "same": "same", "other": "other"}
# A pair reading written as a call, and the pair atom that grounds it (the reviewer 2026-10-08
# 23:23Z): "== 1" -> the atom, "== 0" -> the atom then negate; it runs on the first object
# with the second as its operand. A pair call not listed here has no atom and is refused.
PAIR = {"touching": "touches"}
# A CHANGE reading and the agent attribute it is a change OF (the reviewer 2026-10-09 01:03Z row,
# its map declared as data at 02:18): "== 1" -> other<attr~1>, "== 0" -> same<attr~1>, run on the
# attribute slot with its own previous value as operand. A change reading not listed is refused.
CHANGE_OF = {"colour_changed": "colour"}
# THE FACE COUNT (the reviewer 2026-10-11 14:17 CDT, under TETHER_RELATION_SET): the library's
# contact(o, x) counts shared cell FACES (0 corner, 1 edge, 2+ face). Its presence and absence
# are the face-level atom `touches` -- never the box slot touches_x, whose gap 0 counts corners.
# Any other value needs the count itself, whose pair part is held back (TETHER_OBSERVER).
FACE_COUNT = {"contact": "touches"}
FACE_PRESENT = {(">", 0): False, ("!=", 0): False, ("==", 0): True}     # -> negate?
# "== 0" on an EXTENT (14:17 CDT, under the arm): an extent is never negative, so "is zero" is
# "not nonzero" -- sign (nonzero, on an EXTENT, not a direction) . holds . negate.
EXTENT_ZERO = (("sign", "holds", "negate"), None)
# THE OBSERVER PAIR CALLS (6, 7; the reviewer 2026-10-11 14:17, 14:31 CDT): inside(o, x) is HOLE
# containment, the observer's directed `x~o.inside` (x~o = o inside x), NEVER the box slot
# inside_x; bbox(o, x) is the box overlap area, `a~b.bbox` named in sorted order. (op, right) ->
# the chain; anything else is refused.
OBSERVER_PAIR = {"inside": {("==", 1): ("holds",), ("==", 0): ("holds", "negate")},
                 "bbox": {(">", 0): ("sign", "holds"), ("!=", 0): ("sign", "holds"),
                          ("==", 0): ("sign", "holds", "negate")}}
PREV = "~1"                  # tether.PREV, pinned by test_compile
# Shapes that have no slot to run on, refused by name (section 3, section 7c).
NOT_SLOTS = {"frame": "events are not slots", "board": "the board is not an object slot",
             # the world's progress marker (world.GOAL_SLOT; the library's `board`), named
             # with an '@' the condition grammar cannot tokenize, so it is refused BEFORE the parse
             "@goal": "@goal is the board's progress marker (the library's board), not an "
                      "object slot"}


@dataclass(frozen=True)
class Compiled:
    slot: str                 # the slot the term runs on, e.g. "o1.drow"
    term: gamma.Term
    operand: str | None       # the slot that fills operand 0, if any
    # A SPARSE PAIR SLOT (6/7): the two objects it relates, and its value when they are both
    # present and the slot is absent (relations.SPARSE_PAIR). Empty / None everywhere else.
    parties: tuple = ()
    absent: Any = None


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


# A RULE candidate holds of EVERY object in scope; one slot's chain says nothing about the group
# (the reviewer 2026-10-09 00:42Z: refused until a group row -- all_same / all_of -- is ruled)
QUANTIFIED = "quantified over the group: needs a group row (not ruled)"


def compile_candidate(cand: dict, atoms: dict[str, gamma.Atom]) -> Compiled | Refusal:
    """One candidate (`{"condition": "o1.drow > 0", ...}`), compiled or refused with a reason."""
    if "quantifier" in cand:
        return Refusal(QUANTIFIED)
    for name, why in NOT_SLOTS.items():
        if name.startswith("@") and re.search(re.escape(name) + r"\b", cand["condition"]):
            return Refusal(why)
    try:
        node = condition.parse(cand["condition"])
    except condition.ParseError as e:
        return Refusal(f"the condition does not parse: {e}")
    if (isinstance(node, condition.Cmp) and isinstance(node.left, condition.Call)
            and node.left.name in PAIR):
        return _pair(node, atoms)
    if (_RELATION_SET and isinstance(node, condition.Cmp) and isinstance(node.left, condition.Call)
            and node.left.name in FACE_COUNT):
        return _face(node, atoms)
    if (_RELATION_SET and isinstance(node, condition.Cmp) and isinstance(node.left, condition.Call)
            and node.left.name in OBSERVER_PAIR):
        return _observer_pair(node, atoms)
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
    rel = relations.pair_attr(reading) if _RELATION_SET else None
    if rtype is None and rel is not None:
        rtype = relations.PAIR_RELATIONS[rel]
    if rtype is None:
        return Refusal(f"{reading!r} is not a library reading")
    right = node.right
    if reading in CHANGE_OF:
        return _change(obj, reading, node.op, right, atoms)
    if isinstance(right, condition.Slot):
        kind, other = "slot", right.name
        if "~" in other and not (_RELATION_SET and other == target + PREV):
            return Refusal("an earlier reading is compared only with its own slot, under the arm")
        oreading = _split(other)[1].split("~", 1)[0]
        # THE GOAL-PAIR REPAIR (the reviewer 2026-10-11 13:40 CDT): two pair slots read the same
        # quantity when they carry the same RELATION (dist_o3 vs dist_o4), as the mint already
        # takes them; pair vs non-pair and two different relations stay refused.
        same_rel = (_RELATION_SET and rel is not None
                    and relations.pair_attr(oreading) == rel)
        if oreading != reading and not same_rel:
            return Refusal("the two sides read different quantities")
    elif right in (0, 1):
        kind, other = ("zero" if right == 0 else "one"), None
    else:
        return Refusal(f"no template compares {reading} with the constant {right}")
    row = TABLE.get((node.op, kind))
    if _RELATION_SET and rtype == "EXTENT" and (node.op, kind) == ("==", "zero"):
        row = EXTENT_ZERO
    if (node.op, kind) in CONVERSE and all(n in atoms for n in CONVERSE[(node.op, kind)][0]):
        row = CONVERSE[(node.op, kind)]
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


def converse(c: Compiled, atoms: dict[str, gamma.Atom]) -> Compiled | None:
    """The same comparison spelled on the OTHER party: run on the operand slot with the first
    slot as operand, through the swapped atom. None where it has no other spelling here (a
    multi-atom chain, an operand tree, a constant, or an atom Gamma does not hold)."""
    if (len(c.term.atoms) != 1 or c.operand is None or c.term.operand_term is not None
            or PREV in c.operand):
        return None
    name = SWAP.get(c.term.atoms[0].name)
    if name is None or name not in atoms:
        return None
    return Compiled(c.operand, gamma.Term((atoms[name],), operand=c.slot), c.slot)


def _change(obj: str, reading: str, op: str, right: Any,
            atoms: dict[str, gamma.Atom]) -> Compiled | Refusal:
    if isinstance(right, condition.Slot):
        return Refusal("a change reading compared across objects reads no slot")
    if op != "==" or right not in (0, 1):
        return Refusal(f"no template for a change reading {op} {right}")
    name = "other" if right == 1 else "same"
    if name not in atoms:
        return Refusal(f"Gamma holds no atom {[name]}")
    attr = CHANGE_OF[reading]
    atype = (readings().get(attr) or {}).get("type")
    chain = (atoms[name],)
    why = _typed(chain, atype, atype)
    if why:
        return Refusal(why)
    slot, operand = f"{obj}.{attr}", f"{obj}.{attr}{PREV}"
    return Compiled(slot, gamma.Term(chain, operand=operand), operand)


def _observer_pair(node: Any, atoms: dict[str, gamma.Atom]) -> Compiled | Refusal:
    """inside(o, x) / bbox(o, x) onto the observer's sparse pair slot, carrying its parties and
    the declared absent value so run() reads an absent pair as 0 when both objects are present."""
    call = node.left
    if len(call.args) != 2 or not all(isinstance(a, condition.Slot) for a in call.args):
        return Refusal(f"no template for {call} {node.op} {node.right}")
    names = OBSERVER_PAIR[call.name].get((node.op, node.right))
    if names is None:
        return Refusal(f"no template for the observer pair {call.name} {node.op} {node.right}")
    missing = [n for n in names if n not in atoms]
    if missing:
        return Refusal(f"Gamma holds no atom {missing}")
    o, x = (a.name for a in call.args)
    if call.name == "inside":
        slot, rtype = f"{x}~{o}.inside", "BOOL"
    else:
        a, b = sorted((o, x))
        slot, rtype = f"{a}~{b}.bbox", "EXTENT"
    chain = tuple(atoms[n] for n in names)
    why = _typed(chain, rtype, None)
    if why:
        return Refusal(why)
    return Compiled(slot, gamma.Term(chain), None, parties=(o, x),
                    absent=relations.SPARSE_PAIR[call.name])


def _face(node: Any, atoms: dict[str, gamma.Atom]) -> Compiled | Refusal:
    """contact(o, x) > 0 / != 0 / == 0 through the face atom; any other value is refused."""
    call = node.left
    if len(call.args) != 2 or not all(isinstance(a, condition.Slot) for a in call.args):
        return Refusal(f"no template for {call} {node.op} {node.right}")
    neg = FACE_PRESENT.get((node.op, node.right))
    if neg is None:
        return Refusal("the face count's pair part is held back (TETHER_OBSERVER)")
    names = (FACE_COUNT[call.name], "negate") if neg else (FACE_COUNT[call.name],)
    missing = [n for n in names if n not in atoms]
    if missing:
        return Refusal(f"Gamma holds no atom {missing}")
    chain = tuple(atoms[n] for n in names)
    why = _typed(chain, "OBJECT", "OBJECT")
    if why:
        return Refusal(why)
    first, second = (a.name for a in call.args)
    return Compiled(first, gamma.Term(chain, operand=second), second)


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
    if frame.get(c.slot) is None and c.absent is not None and c.parties and all(
            any(k.startswith(p + ".") for k in frame) for p in c.parties):
        frame = {**frame, c.slot: c.absent}      # a sparse pair, both objects present: absent IS 0
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
