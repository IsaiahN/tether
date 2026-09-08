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

from gamma import SAME_AS_TARGET, Atom, Ctx
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
# BOOL IS THE PUREST MEMBER, NOT A STRANGER. Equality is meaningful on a truth -- do two
# objects agree on contact -- and order is not: neither truth is MORE. That is exactly
# `COLOUR`'s and `SHAPE`'s slot, so `BOOL` sits in `COMPARABLE` and out of `ORDERED`.
#
# **AND IT DOES NOT OPEN LINK 2, WHICH IS WHY IT IS SAID HERE.** It admits 15 chains, all
# beginning `touching`, all typed `OBJECT -> OBJ` -- and the loop's objective query starts at
# the SLOT'S OWN type, so it never asks for them. Measured: `POSITION -> OBJ` and
# `COLOUR -> OBJ` gain ZERO. And `touching` abstains anyway: it is `OBJECT -> BOOL`, the loop
# hands a scalar, and `touching(0, ctx)` is `NOT_RESOLVED` -- the SAME flattening that makes
# the eight extract atoms abstain. **The relational vocabulary and the extract space are
# blocked by one cause, not two.**
COMPARABLE = (COLOUR, POSITION, EXTENT, DELTA, SHAPE, BOOL)   # equality is meaningful on all
ORDERED = (POSITION, EXTENT, DELTA)       # order is meaningful only on these
PRED, QUANT, VAL = "PRED", "QUANT", "val"

# THE ONE TABLE. An object record's key -> the §12.2 type its values inhabit. `_extract` reads
# it to type its atoms and `ArcWorld.slot_types` reads it to type its slots, and those are the
# same fact: a slot IS an object's attribute. Declared once so they cannot drift apart.
ATTRIBUTE_TYPE = {"colour": COLOUR, "row": POSITION, "col": POSITION,
                  "h": EXTENT, "w": EXTENT, "drow": DELTA, "dcol": DELTA,
                  "shape": SHAPE}


# THE ADMITTING CLAUSE, PER ATOM, RECORDED WHERE THE ATOM IS DECLARED.
#
# `CLAUDE.md`'s entry rule had two clauses -- *the loop cannot run without it*, or *the agent
# minted a crude version and we are promoting it* -- and neither admits a primitive the loop
# RUNS without and cannot EXPRESS. Isaiah ruled a third, 2026-09-08: an atom may be handed
# when the agent's own machinery perceived and named the gap, when the primitive is
# fundamental enough that no in-run derivation is plausible, and when a human competitor
# would arrive already holding it.
#
# **THE STAMP IS WHAT PRESERVES THE COMPOSITION CLAIM UNDER THE CONCESSION.** The claim is not
# that the agent invented `rotate`; it is that the agent COMPOSED WITH `rotate`. Those are
# different claims and only a record of which atoms were handed keeps them separable -- the
# ablation partitions by WHICH CLAUSE ADMITTED A THING, and that cannot be reconstructed from
# an origin stamp afterwards, because `prior` marks every atom alike.
ADMITTED = {
    "rotate": "handed-2026-09-08: named by `arc_predict.unexpressible()` as `couples row and "
              "col`; no chain of the 21 yields it; mental rotation is preschool",
    "reflect": "handed-2026-09-08: named by `arc_predict.unexpressible()` as `needs the board "
               "extent`; no chain of the 21 yields it; mirror symmetry is preschool",
    "count": "handed-2026-09-08: named by §12.4's own INWARD example "
             "`ratio(count(colour=a), count(colour=b))`; every group fold ends at PRED so no "
             "chain yields a cardinality; counting precedes school",
}


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
        def fn(o: Any, c: Ctx) -> Any:
            # §12.2: *a value or NOT_RESOLVED. Never a guess, never a default.* Both branches
            # were guesses -- `o.get(key, 0)` asserted the attribute is zero, and returning a
            # non-dict unchanged asserted the scalar IS the attribute.
            #
            # THE SCALAR CASE IS NO LONGER AN ABSTENTION. The docstring above records that all
            # eight abstained in the live loop because `_decomposed` hands a SCALAR -- and the
            # record is reassembled from that same state and arrives on `Ctx`, so the extract
            # space can finally run. The abstention stays for a frame that supplies neither.
            rec = o if isinstance(o, dict) else getattr(c, "obj", None)
            if not isinstance(rec, dict):
                return NOT_RESOLVED
            return rec.get(key, NOT_RESOLVED)
        return fn
    # `obj` -- the record carries EVERY attribute of the owner, so an extract atom varies
    # with its owner's other slots and may not claim invariance to them.
    return [Atom(k, pick(k), OBJECT, t, reads_ctx=("obj",))
            for k, t in ATTRIBUTE_TYPE.items()]


def _transform() -> list[Atom]:
    """`SHAPE → SHAPE`, and the build named these two gaps itself.

    `arc_predict.unexpressible()` reports *the four the signature cannot carry, with the
    reason* -- and two of the four are these, by name:

        rotate    "couples row and col; an atom returns one slot's value"
        reflect   "needs the board extent; `Ctx` has no accessor and the board is not a slot"

    **BOTH REASONS ARE ABOUT `val -> val` AND BOTH DISSOLVE AT `SHAPE`.** A shape IS the cell
    set -- `frozenset((r - r0, c - c0) for r, c in cells)` -- so it carries both coordinates
    and there is nothing to couple, and it is already normalised to its own origin so no
    board extent is needed. **The obstacle the build recorded is the obstacle at the
    signature it recorded it for.**

    AND THEY ARE THE FIRST `SHAPE -> SHAPE` ATOMS, so the OBJECT component of the type graph
    gains its first cycle: `rotate . reflect . rotate` is a chain, and `max_depth` binds on
    something for the first time rather than matching the graph exactly.
    """
    def _rot(v: Any, _c: Ctx) -> Any:
        if not isinstance(v, frozenset) or not v:
            return NOT_RESOLVED
        m = max(r for r, _ in v)
        return frozenset((c, m - r) for r, c in v)

    def _ref(v: Any, _c: Ctx) -> Any:
        if not isinstance(v, frozenset) or not v:
            return NOT_RESOLVED
        m = max(c for _, c in v)
        return frozenset((r, m - c) for r, c in v)

    return [Atom("rotate", _rot, SHAPE, SHAPE),
            Atom("reflect", _ref, SHAPE, SHAPE)]


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
        rec = o if isinstance(o, dict) else getattr(c, "obj", None)
        if not isinstance(rec, dict):
            return NOT_RESOLVED
        # UNKNOWN IS NOT EMPTY. Contact is computed from cells, the state carries none, so a
        # replayed frame cannot say what touched what -- and `()` there would assert *nothing
        # was touching* on evidence nobody has.
        if c.touching is None:
            return NOT_RESOLVED
        return int(bool(c.touching))
    return [Atom("touching", touching, OBJECT, BOOL, reads_ctx=("obj", "touching"))]


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

    # `0a`'s TYPING HALF, APPLIED HERE AT LAST. `gamma.Atom.operand_type` and
    # `_operand_fits` were built after these three and never reached them, and *an undeclared
    # type ADMITS* -- so `above` took ORDERED as its INPUT and ANY type as its OPERAND. That
    # is the `ATTR` split's own hazard one argument over: `above(col:POSITION, colour:COLOUR)`
    # was well-typed and meaningless. Measured before declaring: of 240 ordered (target,
    # operand) pairs on a 16-slot board, 168 (70%) are cross-type and are refused, and every
    # refused pair compares two different attribute types.
    #
    # OPEN, AND SMALLER THAN THIS FIX. `SAME_AS_TARGET` inherits `COMMENSURABLE`, whose
    # warrant is `translate`'s AFFINE operation -- *a position plus its own displacement* --
    # and equality is not addition. 32 pairs (13%) ride in on a table justified for a
    # different operator. Recorded rather than edited: the table is a pinned exemption, and
    # narrowing it from here would be logic widening what data should hold.
    return [Atom("same", same, COMPARABLE[0], PRED, reads_operand=True,
                 also_accepts=COMPARABLE[1:], operand_type=SAME_AS_TARGET,
                 reads_ctx=("operands",)),
            Atom("other", other, COMPARABLE[0], PRED, reads_operand=True,
                 also_accepts=COMPARABLE[1:], operand_type=SAME_AS_TARGET,
                 reads_ctx=("operands",)),
            Atom("above", above, ORDERED[0], PRED, reads_operand=True,
                 also_accepts=ORDERED[1:], operand_type=SAME_AS_TARGET,
                 reads_ctx=("operands",))]


def _count(v: Any, c: Ctx) -> Any:
    """How many peers share this value. **A cardinality, not a truth.**

    `NOT_RESOLVED` WHERE THERE IS NO POPULATION, never 0: an empty group is *I cannot see the
    others*, and returning zero would make a missing reading indistinguishable from a real
    count of none -- §12.2's rule at the one place a fold is tempted to default.
    """
    g = getattr(c, "group", ())
    if not g:
        return NOT_RESOLVED
    return sum(1 for x in g if x == v)


def _over_group() -> list[Atom]:
    """`ATTR → PRED`, quantified over the OUTER STREAM -- the same attribute on every other
    object.

    **THIS IS THE PER-MEMBER FOLD, WHICH `_relate` CANNOT DO.** `same` compares one value to
    ONE bound operand; these compare it to EVERY member of a population and fold the results.
    `ALL x . x == v` is a different claim from `x0 == v`, and it is the claim the group
    question needs: *do the objects all agree on this attribute, or does each differ.*

    **AN EMPTY POPULATION IS `NOT_RESOLVED`, NOT TRUE.** Vacuous truth would make `all_same`
    hold on a board with one object, which is an absence read as a reading -- the same rule
    as a locus with no changed cells getting no entry.

    **AND NEITHER POLE IS PUBLISHED.** The population arrives through `Ctx` and the fold is an
    ATOM, so the agent composes the group claim rather than reading one off a sensor -- which
    is §12.3's requirement that alignment and counting be REACHED.
    """
    def fold(q):
        def fn(v: Any, c: Ctx) -> Any:
            if not c.group:
                return NOT_RESOLVED
            return int(q(x == v for x in c.group))
        return fn

    # `group` -- every peer's value for this attribute. These vary with EVERY peer slot,
    # which is the invariance `key_of` was claiming they had.
    return [Atom("all_same", fold(all), COMPARABLE[0], PRED,
                 also_accepts=COMPARABLE[1:], reads_ctx=("group",)),
            Atom("any_same", fold(any), COMPARABLE[0], PRED,
                 also_accepts=COMPARABLE[1:], reads_ctx=("group",)),
            Atom("none_same", fold(lambda g: not any(g)), COMPARABLE[0], PRED,
                 also_accepts=COMPARABLE[1:], reads_ctx=("group",)),
            # THE FIRST GROUP FOLD THAT DOES NOT END AT `PRED`, and that is the point of it.
            # The three above collapse a population to a truth, so everything a group knows
            # arrives as one bit and the group is gone. `count` returns HOW MANY, which is
            # the `group -> value` arrow whose absence explained four separate gaps at once:
            # no ranking, no cardinality, no ratio, no aggregate.
            #
            # §12.4's own INWARD example is `ratio(count(colour=a), count(colour=b))` -- the
            # one of its three worked examples that needed TWO primitives existing nowhere.
            # This is the first of them.
            Atom("count", _count, COMPARABLE[0], EXTENT,
                 also_accepts=COMPARABLE[1:], reads_ctx=("group",))]


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
    return (list(predict) + _extract() + _transform() + _contact() + _relate()
            + _over_group() + _quantify())
