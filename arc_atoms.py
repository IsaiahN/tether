"""3b. The three composition spaces, typed -- and `λ` starts reporting something.

§11.2: **there are three composition spaces and we have one and a half.**

    PREDICT   slot × action → slot        built -- `gamma.py`'s atoms
    RELATE    ATTR × ATTR → PRED → OBJ    `grammar.py` composes utterances, and the MINT
                                          enumerates `gamma`'s closure only -- so it is
                                          wired for SPEAKING and not for SEARCHING
    EXTRACT   grid × object → ATTR        the extractors exist as 2b's sensors; the TYPING
                                          does not

**The machinery needed nothing new.** `enumerate_closure(in_type, out_type, ...)` is already
type-directed and `Atom` already carries `in_type`/`out_type` -- what was missing is an atom
set whose types are not all `val → val`. §11.3: *the Stage 1 falsifier fired in the toy world,
`λ = V = 7`, because every atom was `val → val` and the type graph was a single node ... **the
instrument was working; it just had nothing to measure.***

AND THE EXTRACTORS ARE 2b's SENSORS, WRAPPED RATHER THAN REWRITTEN. `colour`, `row`, `col`,
`h`, `w` come off the component dict `arc_percept.components` already builds. A second
implementation of `position` would be the reinvention no grep can see.

WHAT THIS DOES NOT DO. Operand TYPING is `0a`'s and is parked: `gamma` types an atom's input
and output and not its operand, so `ATTR × ATTR → PRED` is expressed here as `ATTR → PRED`
with an operand-reading atom. **The type GRAPH is what `λ` is computed over, and the graph is
sparse either way** -- but the second argument's type is unchecked, and saying so is cheaper
than discovering it at 3c.
"""
from __future__ import annotations

import sys
from typing import Any

from gamma import Atom, Ctx

sys.dont_write_bytecode = True

# OBJECT AND OBJ ARE DIFFERENT NODES, AND ONE CONSTANT USED TO BE BOTH.
# `_extract` takes OBJECT -- a thing on the board. `_quantify` yields OBJ -- a complete
# objective, which is `grammar.T.OBJ`'s own gloss. Under one name the type graph had a node
# that was two things, and the closure composed across it: 225 pipelines at depth 4, the
# first being `colour . same . all . colour` -- quantify to an objective, then read a colour
# OFF the objective. Well-typed, meaningless, and refusing that is what the type system is
# for. `grammar.py` had kept them apart all along as OBJECT and OBJ.
OBJECT, OBJ = "OBJECT", "OBJ"
ATTR, PRED, QUANT, VAL = "ATTR", "PRED", "QUANT", "val"


def _extract() -> list[Atom]:
    """`OBJECT → ATTR`. One per sensor 2b already computes, wrapped and not rewritten."""
    def pick(key: str):
        def fn(o: Any, _c: Ctx) -> Any:
            return o.get(key, 0) if isinstance(o, dict) else o
        return fn
    return [Atom(k, pick(k), OBJECT, ATTR) for k in ("colour", "row", "col", "h", "w")]


def _relate() -> list[Atom]:
    """`ATTR → PRED`, reading a second ATTR as an operand.

    §11.2 types this `ATTR × ATTR → PRED`. The operand's type is not checked -- see the
    module note -- so the arity is real and the typing of the second argument is not.
    """
    def same(v: Any, c: Ctx) -> Any:
        return int(bool(c.operands) and v == c.operands[0])

    def other(v: Any, c: Ctx) -> Any:
        return int(bool(c.operands) and v != c.operands[0])

    def above(v: Any, c: Ctx) -> Any:
        return int(bool(c.operands) and v > c.operands[0])

    return [Atom("same", same, ATTR, PRED, reads_operand=True),
            Atom("other", other, ATTR, PRED, reads_operand=True),
            Atom("above", above, ATTR, PRED, reads_operand=True)]


def _quantify() -> list[Atom]:
    """`PRED → OBJ`. What closes a statement back into something bettable."""
    return [Atom("all", lambda v, _c: int(bool(v)), PRED, OBJ),
            Atom("any", lambda v, _c: int(bool(v)), PRED, OBJ),
            Atom("none", lambda v, _c: int(not v), PRED, OBJ)]


def three_spaces(predict: list[Atom]) -> list[Atom]:
    """EXTRACT + RELATE + QUANTIFY, joined to whatever PREDICT the domain supplies.

    PREDICT is passed in rather than built: it is the domain's atom set -- grid transforms at
    3d -- and inventing one here would be this file choosing what the agent may bet on.
    """
    return list(predict) + _extract() + _relate() + _quantify()
