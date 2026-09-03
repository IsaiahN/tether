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
from sensors import BOOL, COLOUR, DELTA, EXTENT, NOT_RESOLVED, OBJECT, POSITION, SHAPE

sys.dont_write_bytecode = True

# OBJECT AND OBJ ARE DIFFERENT NODES, AND ONE CONSTANT USED TO BE BOTH.
# `_extract` takes OBJECT -- a thing on the board. `_quantify` yields OBJ -- a complete
# objective, which is `grammar.T.OBJ`'s own gloss. Under one name the type graph had a node
# that was two things, and the closure composed across it: 225 pipelines at depth 4, the
# first being `colour . same . all . colour` -- quantify to an objective, then read a colour
# OFF the objective. Well-typed, meaningless, and refusing that is what the type system is
# for. `grammar.py` had kept them apart all along as OBJECT and OBJ.
OBJ = "OBJ"          # `OBJECT` is imported from `sensors`; this one is the objective
# `ATTR` IS A SPACE, NOT A TYPE, AND THE CODE MADE IT A TYPE. §11.2's table names
# `ATTR x ATTR -> PRED` as one of THREE COMPOSITION SPACES; §12.3's table names the types
# inside it -- `OBJ -> COLOUR`, `OBJ -> POSITION`, `OBJ -> EXTENT`, `OBJ -> SHAPE`. `_relate`
# cited §11.2 and typed on the space's name, which is correct about the space and wrong about
# the type: it made `above` -- an ORDER -- apply to a colour, 4 of the 60 terms in
# `OBJECT -> {PRED, OBJ}` at depth 3. Well-typed and meaningless, and the colour ruling is why:
# a colour is a LABEL that permutes on refresh, so `>` on it compares two arbitrary indices.
# IMPORTED, NOT REDECLARED. `sensors.py` already carried §12.2's nine attribute types, and
# the ATTR split declared four of them here a commit later -- two producers of one fact, with
# identical strings, which is harmless exactly until one side changes.
COMPARABLE = (COLOUR, POSITION, EXTENT, DELTA, SHAPE)   # equality is meaningful on all
ORDERED = (POSITION, EXTENT, DELTA)       # order is meaningful only on these
PRED, QUANT, VAL = "PRED", "QUANT", "val"

# THE ONE TABLE. An object record's key -> the §12.2 type its values inhabit. `_extract` reads
# it to type its atoms and `ArcWorld.slot_types` reads it to type its slots, and those are the
# same fact: a slot IS an object's attribute. Declared once so they cannot drift apart.
ATTRIBUTE_TYPE = {"colour": COLOUR, "row": POSITION, "col": POSITION,
                  "h": EXTENT, "w": EXTENT, "drow": DELTA, "dcol": DELTA,
                  "shape": SHAPE}


def _extract() -> list[Atom]:
    """`OBJECT → COLOUR | POSITION | EXTENT | DELTA | SHAPE`, one per key 2b computes.

    **EIGHT, NOT FIVE, AND THE OLD WARNING CAME TRUE.** It said *which five these are was never
    decided ... the ceiling on what can be represented is an encoding accident, and the next
    reader will assume five was chosen.* `shape` and the two DELTA keys were published later
    and the count moved by exactly that route. **The warning was right and outlived its own
    number**, which is why it is restated rather than deleted: the ceiling is still whatever
    `_decomposed` happens to emit, and nothing here decides it.

    **AND THESE ATOMS CANNOT EXTRACT IN THE LIVE LOOP -- MEASURED, NOT ARGUED.** `_decomposed`
    already extracts, flattening every object to `name.attr -> int`, so a term is handed a
    SCALAR and never an OBJECT. All eight were identity on a bare int; now all eight abstain
    there, which is §12.2's rule and not a repair of this. **The gap is that §11.2's EXTRACT
    space runs BEFORE the loop at a vocabulary the seat fixed** -- the agent cannot reach for
    an attribute because attributes are computed on the way in.
    """
    def pick(key: str):
        def fn(o: Any, _c: Ctx) -> Any:
            # §12.2: *a value or NOT_RESOLVED. Never a guess, never a default.* Both branches
            # were guesses -- `o.get(key, 0)` asserted the attribute is zero, and returning a
            # non-dict unchanged asserted the scalar IS the attribute.
            if not isinstance(o, dict):
                return NOT_RESOLVED
            return o.get(key, NOT_RESOLVED)
        return fn
    return [Atom(k, pick(k), OBJECT, t) for k, t in ATTRIBUTE_TYPE.items()]


def _contact() -> list[Atom]:
    """§12.3 sensor 8 as an atom: `OBJECT → BOOL`, second operand from `Ctx`.

    **THE TWO-PLACE CASE, WHICH `_extract` DID NOT COVER.** `touching(a, b)` is `OBJ x OBJ ->
    BOOL` and an atom receives ONE value, so the second operand arrives through `Ctx.touching`
    -- resolved per slot by the caller, exactly as `operands` is. The one-place sensors were
    wrapped eight times and this shape had no answer until it was ruled.

    **THE PRICE IS A RE-MEASUREMENT, NOT A LINE.** The atom COUNT moves `space_estimate`,
    `coverage`, `λ` and `V`, and every number on the panel was taken under the previous set --
    the false-mint rate, the exponent, chunk reuse, the transfer curve. **They are stale from
    this commit**, and saying so here is the point of saying it at all.

    It abstains on a non-OBJECT for the same reason `pick` does: the loop hands a SCALAR, and
    a reading taken from the wrong kind of thing is a guess.
    """
    def touching(o: Any, c: Ctx) -> Any:
        if not isinstance(o, dict):
            return NOT_RESOLVED
        return int(bool(c.touching))
    return [Atom("touching", touching, OBJECT, BOOL)]


def _relate() -> list[Atom]:
    """`ATTR → PRED`, reading a second ATTR as an operand.

    `same` and `other` are EQUALITY and hold on every attribute; `above` is ORDER and holds
    only on `POSITION` and `EXTENT`. That is the whole of the split -- one atom refused three
    compositions, and it is refused by TYPE rather than by a rule naming `colour`.

    §11.2 types this `ATTR × ATTR → PRED`. The operand's type is not checked -- see the
    module note -- so the arity is real and the typing of the second argument is not.
    """
    def same(v: Any, c: Ctx) -> Any:
        return int(bool(c.operands) and v == c.operands[0])

    def other(v: Any, c: Ctx) -> Any:
        return int(bool(c.operands) and v != c.operands[0])

    def above(v: Any, c: Ctx) -> Any:
        return int(bool(c.operands) and v > c.operands[0])

    return [Atom("same", same, COMPARABLE[0], PRED, reads_operand=True,
                 also_accepts=COMPARABLE[1:]),
            Atom("other", other, COMPARABLE[0], PRED, reads_operand=True,
                 also_accepts=COMPARABLE[1:]),
            Atom("above", above, ORDERED[0], PRED, reads_operand=True,
                 also_accepts=ORDERED[1:])]


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
    return list(predict) + _extract() + _contact() + _relate() + _quantify()
