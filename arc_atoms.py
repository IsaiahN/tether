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

import os
import sys
from typing import Any

from arc_percept import holes_of, perimeter_of
from gamma import SAME_AS_TARGET, Atom, Ctx
from sensors import (
    BOOL,
    CELL,
    CELLS,
    COLOUR,
    DELTA,
    EXTENT,
    NOT_RESOLVED,
    OBJECT,
    POSITION,
    SHAPE,
    Cells,
)

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

# THE ITERATION ARM, DEFAULT OFF -- `LIBRARY_RETRIEVAL` §12.2.1. Adds `cells`/`cell_row`/
# `cell_col`/`count_true`, which make a cell set WALKABLE for the first time. Off by default
# because it widens the closure the mint enumerates and that cost is measured before it is
# defaulted, per §12.12: a feature is priced in EPISODES FORGONE, not in per-cycle percent.
_ITERATE = bool(os.environ.get("TETHER_ITERATE"))

# THE ONE TABLE. An object record's key -> the §12.2 type its values inhabit. `_extract` reads
# it to type its atoms and `ArcWorld.slot_types` reads it to type its slots, and those are the
# same fact: a slot IS an object's attribute. Declared once so they cannot drift apart.
ATTRIBUTE_TYPE = {"colour": COLOUR, "row": POSITION, "col": POSITION,
                  "h": EXTENT, "w": EXTENT, "drow": DELTA, "dcol": DELTA,
                  "shape": SHAPE,
                  # THE RELATION SLOT -- observer item 4, arm `TETHER_OBSERVER`, default OFF.
                  # `a~b.contact` holds the SHARED-FACE COUNT, which is why it needs no new
                  # type: a categorical `point|edge|face` would have, and §12.2's set is
                  # closed. The count is already ordinal in the direction the subdivision
                  # means -- 0 corner, 1 edge, 2+ face, increasing constraint.
                  #
                  # **EXTENT AND NOT `COUNT`, AND THE REASON IS A GAP WORTH RECORDING.** §12.2
                  # names `COUNT` in its type set and `sensors` DOES NOT EXPORT ONE -- the
                  # importable set is BOOL COLOUR DELTA EXTENT OBJECT POSITION SHAPE. So the
                  # choice is among what exists, and EXTENT is the honest fit rather than a
                  # substitution: an ordered non-negative magnitude, exactly `h` and `w`'s
                  # shape, and *the extent of the contact* is what the quantity measures.
                  # Adding a `COUNT` type to close the gap would touch every consumer of the
                  # set and is not this arm's to do.
                  "contact": EXTENT,
                  # THE REST OF THE CHEAP MUTATION SET -- observer item 1, arm TETHER_OBSERVER.
                  # `observer._MUT_ATTR` names the frozen deltas as `drow dcol dh dw dcells
                  # recolour`; the tracker carried the first two. `dh`/`dw`/`dcells` are signed
                  # magnitudes, so DELTA like the two that were already here.
                  "dh": DELTA, "dw": DELTA, "dcells": DELTA,
                  # AND `colour_changed` IS BOOL, NOT DELTA, WHICH IS NOT COSMETIC. Colour is
                  # CATEGORICAL -- `arc_percept`'s own header says it is a SEPARATOR, comparable
                  # and never ordered -- so `new - old` on a hue is arithmetic over labels and
                  # means nothing. Publishing a colour DIFFERENCE would have invented a
                  # quantity; publishing *it changed* is the reading the corpus's set names.
                  "colour_changed": BOOL,
                  # THE BBOX OVERLAP SENSOR -- `RELATIONS.md` Part 6's first blocker, "a BUILD
                  # rather than a publish". An intersection AREA, so EXTENT like `contact`.
                  "bbox": EXTENT,
                  # THE SHAPE DELTAS -- arm `TETHER_SHAPE_DELTA`, default OFF. Signed changes
                  # in the two CELL-SET quantities, so DELTA like `dh`/`dw`/`dcells`. Admitted
                  # because no atom accepts `OBJECT_BEFORE`: the agent cannot reach the
                  # previous object, so it cannot compose these however long it searches.
                  # `arc_percept` carries the full reasoning and the seven that were refused.
                  "dholes": DELTA, "dperimeter": DELTA,
                  # THE OBJECT'S AGE -- arm `TETHER_INSTRUMENTS`, Part 12 item 3. Consecutive
                  # frames tracked, 0 at birth. EXTENT: an ordered non-negative magnitude, the
                  # same shape as `h`/`w`, and it is a COUNT the type set cannot express (the
                  # `contact` note records that gap and the reason EXTENT is the honest fit).
                  "age": EXTENT,
                  # DISPLACEMENT MAGNITUDE this frame, Chebyshev. EXTENT and not DELTA: a
                  # magnitude is non-negative and unsigned, where DELTA is signed and
                  # commensurable with POSITION. `speed` and `velocity` are ONE quantity here
                  # -- a slot holds one int, so a vector has nowhere to live -- and only one
                  # name is published. Direction stays in `drow`/`dcol`.
                  "speed": EXTENT,
                  # `inside` -- HOLE CONTAINMENT, per-pair, ruled 2026-09-23. The ONLY entry in
                  # `ADMITTED` that was never built: admitted 2026-09-08 with the batch's best
                  # reach number and absent from the registry for a fortnight. BOOL because it
                  # holds or it does not; the bare word `containment` is retired -- `arc_world`
                  # publishes BBOX overlap as `bbox` and refuses bbox containment separately.
                  "inside": BOOL}


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
    "area": "handed-2026-09-08: `h`/`w` are the BOUNDING BOX and nothing counted cells, so a "
            "sparse cross and its enclosing square were indistinguishable on every extent "
            "atom; not derivable -- `count` folds a peer group, not a cell set; `how big` is "
            "preschool. Sweep 38 priced it +18 at depth 3, which almost nothing else does",
    "centroid": "handed-2026-09-08: OBJECT-entry, one of only three candidates of 34 that both "
                "pay at depth 3 and can be built; row-mean of own cells; `middle` is preschool",
    "touching_n": "handed-2026-09-08: `touching` folded a POPULATION to a bit and Ctx.touching "
                  "already carried the names; HOW MANY neighbours, not whether any",
    # SEVEN ON THE `SHAPE` ARROWS. These entered on the DEPTH justification -- sweep 39's
    # leave-one-out priced each at +18 given all the others -- and NOT because the machinery
    # named them. That distinction is the whole reason the stamp exists: `rotate`, `reflect`,
    # `holes`, `parity` and `count` were named by `unexpressible()` or §12.4, and these were
    # named by a measurement I ran. **A future ablation must be able to tell those apart.**
    "bbox_area": "handed-2026-09-08 ON DEPTH: +18 leave-one-out; the box a shape occupies",
    "perimeter": "handed-2026-09-08 ON DEPTH: +18; exposed edges, correct on concave shapes",
    "corners": "handed-2026-09-08 ON DEPTH: +18; convex corner count",
    "orbit_size": "handed-2026-09-08 ON DEPTH: +18; |dihedral orbit|, 1 = fully symmetric",
    "canonical": "handed-2026-09-08 ON DEPTH: +15; least of the 8 dihedral images, which is "
                 "what makes two differently-oriented copies of one shape comparable",
    "symmetric": "handed-2026-09-08 ON DEPTH: +15; mirror symmetry as a predicate",
    "is_square": "handed-2026-09-08 ON DEPTH: +15; filled and equal-sided",
    # NINE MORE ON DEPTH. The four ORDERED ones are typed on `ORDERED` and not `COMPARABLE`
    # deliberately: `is_max` over colours would compare two arbitrary palette indices, which
    # is the `above(colour)` error the relate atoms already paid for once.
    "rank_in": "handed-2026-09-08 ON DEPTH; how many peers fall below this value",
    "is_max": "handed-2026-09-08 ON DEPTH; ORDERED only",
    "is_min": "handed-2026-09-08 ON DEPTH; ORDERED only",
    "sum_group": "handed-2026-09-08 ON DEPTH; the population total",
    "distinct": "handed-2026-09-08 ON DEPTH; how many values the population holds",
    "is_mode": "handed-2026-09-08 ON DEPTH; is this the commonest value",
    "aligned": "handed-2026-09-08 ON DEPTH; does any peer share this exact value",
    "abs_delta": "handed-2026-09-08 ON DEPTH; a delta's MAGNITUDE -- `moved 3 left` and `moved "
                 "3 right` shared no reading before it",
    "sign": "handed-2026-09-08 ON DEPTH; a delta's DIRECTION as a truth",
    # G1'S GAP, AND THE ONLY THREE HERE NAMED BY A STRUCTURAL ABSENCE RATHER THAN BY A PRICE:
    # the set held ∀, ∃ and ¬∃ and no connectives, so an objective was always ONE predicate
    # quantified. `both`/`either` are buildable only because §4's operand_term lets a COMPUTED
    # predicate fill operand 0 -- an operand was a slot's raw value until this pass.
    "negate": "handed-2026-09-08: PRED -> PRED; the set had quantifiers and no connectives",
    "both": "handed-2026-09-08: conjunction of two predicates; needs §4's computed operand",
    "either": "handed-2026-09-08: disjunction of two predicates; needs §4's computed operand",
    "holes": "handed-2026-09-08: §12.4's own INWARD example `holes(shape)`; SHAPE reached "
             "only SHAPE and PRED so no chain measured a shape; Isaiah's own preschool case, "
             "squares and pegs",
    "parity": "handed-2026-09-08: §12.4's own INWARD example `parity(position)`; no modulo "
              "exists anywhere in the atom set; odd-and-even precedes school",
    "inside": "handed-2026-09-08: named by Isaiah as the preschool case (pegs in holes) and "
              "NOT derivable from `touching` -- a ring touches its interior and its exterior "
              "identically. THE ONLY CANDIDATE THAT ADDS REACH AT max_depth=3: +15 chains "
              "where every other atom handed today adds none",
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


def _owner() -> list[Atom]:
    """`val -> OBJECT`. **THE BRIDGE THAT MAKES THE 18 `OBJECT`-TYPED ATOMS REACHABLE** -- item 5,
    Isaiah: *the 18 become reachable; map/fold, not a bare re-type.*

    `F287` measured all eighteen `OBJECT`-typed atoms as NEVER CALLED -- a third of the registry
    -- and named the cause from `_extract`'s own docstring: `_decomposed` flattens every object
    to `name.attr -> int`, **so a term is handed a SCALAR and never an OBJECT.** The atoms were
    never broken and their values were never missing; **nothing in the composition space could
    PRODUCE an `OBJECT` for them to consume.**

    **THIS IS NOT A RE-TYPE AND IT INVENTS NOTHING.** `Ctx.obj` is already populated at every
    call site (`tether.py:1107`, `obj=self._record(slot, state)`), and `_record`'s own docstring
    says why that is sound: *the flattening scattered the object, it did not destroy it.* So the
    bridge is one atom that hands the composer a value the frame already holds.

    **TYPED `val` DELIBERATELY** -- the wildcard `idn` uses. Every slot is some attribute type,
    and an owner atom per type would be eighteen copies of one function selecting by a label,
    which is the type branching this project forbids.

    It abstains rather than guessing where no record arrived, so a frame that supplies neither
    the object nor the record reads NOT_RESOLVED and not a fabricated owner.
    """
    def _own(v: Any, c: Ctx) -> Any:
        rec = v if isinstance(v, dict) else getattr(c, "obj", None)
        return rec if isinstance(rec, dict) else NOT_RESOLVED
    return [Atom("owner", _own, VAL, OBJECT, reads_ctx=("obj",))]


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


def _as_shape(v: Any, c: Ctx) -> Any:
    """ARM I's decoder. The published SHAPE slot is an episode-local INT and every shape atom
    guards on a frozenset, so they read NOT_RESOLVED on every call (`F242`: 0 of 40).
    `Ctx.shapes` carries the decoder `arc_world.shapes()` already computed and nobody read.
    Returns the frozenset, or `v` unchanged when there is nothing to decode.

    **MODULE LEVEL BECAUSE `holes` COULD NOT REACH IT, AND `holes` IS THE ONE THAT MATTERED.**
    It lived inside `_shape_more()`, so the seven atoms there decoded and `_holes` -- defined in
    `_shape_facts()`, a different closure -- did not. Measured on `g50t`, 6 cycles, arm I ON:
    every other shape atom resolves on EVERY call (`bbox_area` 62,448/62,448, `canonical`
    59,062, `orbit_size` 44,236, `is_square` 37,452, `corners` 37,064, `perimeter` 21,124)
    **and `holes` reads 3,140 calls, 0 resolved, IDENTICAL with the arm off.**

    **AND IT IS THE ATOM THE CORPUS NAMES AS THE EXAMPLE** -- §12.4's own INWARD case
    `holes(shape)`, Isaiah's preschool squares-and-pegs. The one left out of the fix was the one
    the fix was described by. One producer now, so a future atom cannot be added to the wrong
    closure and silently miss it.
    """
    if isinstance(v, frozenset):
        return v
    m = getattr(c, "shapes", None) if c is not None else None
    return m.get(v, v) if isinstance(m, dict) else v


def _shape_facts() -> list[Atom]:
    """`SHAPE → EXTENT`, and the first arrow that takes a shape to a QUANTITY.

    `rotate`/`reflect` map SHAPE to SHAPE and the COMPARABLE relations map it to PRED, so a
    shape could be transformed or compared and never MEASURED. §12.4's own INWARD example is
    `holes(shape)`.

    BOTH READ THE CELL SET, which is what makes them atoms rather than sensors: a shape IS
    `frozenset((r - r0, c - c0) for r, c in cells)`, so the interior and the boundary are both
    already in hand and neither needs the board.
    """
    def _holes(v: Any, _c: Ctx) -> Any:
        # THE BODY MOVED TO `arc_percept.holes_of` -- ONE implementation, because there were
        # two and they disagreed 56 times of 263. The atom keeps the DECODE and the GUARD,
        # which are the atom's business; the geometry is perception's.
        v = _as_shape(v, _c)        # ARM I, which this atom was omitted from -- see `_as_shape`
        if not isinstance(v, frozenset) or not v:
            return NOT_RESOLVED
        return holes_of(v)

    def _parity(v: Any, _c: Ctx) -> Any:
        return NOT_RESOLVED if not isinstance(v, int) else bool(v % 2)

    def _centroid(o: Any, c: Ctx) -> Any:
        """Mean ROW of the object's own cells. **One coordinate, because a slot holds one.**

        `_group` is a single attribute column, so a two-coordinate centroid has nowhere to
        live -- and returning the row half is a reading rather than a stand-in for the pair.
        """
        rec = o if isinstance(o, dict) else getattr(c, "obj", None)
        if not isinstance(rec, dict) or not rec.get("structure"):
            return NOT_RESOLVED
        # `structure` IS OFFSETS FROM THE TOP-LEFT, so the mean of them is the mean offset and
        # the absolute row is that plus the object's own `row`. Reading it as an absolute
        # coordinate would put every object's centroid near the origin.
        rows = [r for r, _ in rec["structure"]]
        base = rec.get("row")
        if not isinstance(base, int):
            return NOT_RESOLVED
        return sum(rows) // len(rows) + base

    def _touch_n(o: Any, c: Ctx) -> Any:
        """HOW MANY are in contact, where `touching` said only WHETHER any were.

        `Ctx.touching` is a tuple of slot NAMES, so the population is already there and the
        existing atom was folding it to a bit.
        """
        rec = o if isinstance(o, dict) else getattr(c, "obj", None)
        if not isinstance(rec, dict) or c.touching is None:
            return NOT_RESOLVED
        return len(c.touching)

    def _area(o: Any, c: Ctx) -> Any:
        """Filled CELL COUNT, which is what `h`/`w` cannot give -- see the admitting note.

        **IT READ `rec["cells"]` AND THE RECORD HAS NO SUCH KEY.** `_record` publishes the
        offset frozenset under `structure` -- *"the structure BESIDE the label, never in place
        of it"* -- so this and `_centroid` were the only two readers of a key nothing writes,
        and both returned NOT_RESOLVED on every call. `A6i` at a record boundary: one quantity,
        two names, and the site that wrote it checked its consumers for MUTATION rather than
        for reading the right key.

        **AND THE ATOM WAS HANDED FOR EXACTLY THIS READING** -- *"`h`/`w` are the BOUNDING BOX
        and nothing counted cells, so a sparse cross and its enclosing square were
        indistinguishable on every extent atom"*. The atom admitted to count cells could not.

        `len(structure) == len(cells)`: the offsets are a bijection with the cells.
        """
        rec = o if isinstance(o, dict) else getattr(c, "obj", None)
        if not isinstance(rec, dict) or not rec.get("structure"):
            return NOT_RESOLVED
        return len(rec["structure"])

    return [Atom("holes", _holes, SHAPE, EXTENT),
            Atom("parity", _parity, POSITION, BOOL),
            # `h` AND `w` ARE THE BOUNDING BOX. Nothing counted the CELLS, so a sparse cross
            # and the solid square that encloses it read identically on every extent atom the
            # set had -- and *how big* is the first quantity a child compares.
            #
            # AND IT ENTERS AT `OBJECT`, WHICH IS WHY IT PAYS NOW. Sweep 38 priced 34
            # candidates: the depth-3 payers are exactly the `OBJECT`-entry atoms, because a
            # chain starting one arrow in cannot reach `OBJ` inside three. +18 at depth 3
            # where every atom handed before it added none.
            Atom("area", _area, OBJECT, EXTENT, reads_ctx=("obj",)),
            # THE OTHER TWO `OBJECT`-ENTRY ATOMS, and entry is what makes them pay at depth 3:
            # sweep 39 found seven candidates paying there and only three buildable.
            Atom("centroid", _centroid, OBJECT, POSITION, reads_ctx=("obj",)),
            Atom("touching_n", _touch_n, OBJECT, EXTENT, reads_ctx=("obj", "touching"))]


def _shape_more() -> list[Atom]:
    """Six more readings of a cell set. **All measured on the shape itself, none on the board.**

    `holes` opened `SHAPE -> EXTENT` and these ride it. Sweep 39's leave-one-out priced each at
    `+18` GIVEN all the others -- they do not share, because the closure counts CHAINS and two
    atoms on one arrow are two chains. My own note calling them *semantics on an arrow that
    already exists, worth nothing structurally* was wrong, and measured so.
    """
    _shape = _as_shape          # the module-level decoder; see its note on `holes`

    def _bbox(v: Any, _c: Ctx) -> Any:
        v = _shape(v, _c)
        if not isinstance(v, frozenset) or not v:
            return NOT_RESOLVED
        rs = [r for r, _ in v]
        cs = [c for _, c in v]
        return (max(rs) - min(rs) + 1) * (max(cs) - min(cs) + 1)

    def _perimeter(v: Any, _c: Ctx) -> Any:
        # Body in `arc_percept.perimeter_of` -- same one-implementation reason as `_holes`.
        v = _shape(v, _c)
        if not isinstance(v, frozenset) or not v:
            return NOT_RESOLVED
        return perimeter_of(v)

    def _corners(v: Any, _c: Ctx) -> Any:
        v = _shape(v, _c)
        # A CONVEX CORNER is a cell with two orthogonal neighbours missing.
        if not isinstance(v, frozenset) or not v:
            return NOT_RESOLVED
        n = 0
        for r, c in v:
            up, dn = (r-1, c) in v, (r+1, c) in v
            lf, rt = (r, c-1) in v, (r, c+1) in v
            n += sum(1 for a, b in ((up, lf), (up, rt), (dn, lf), (dn, rt)) if not a and not b)
        return n

    def _dihedral(v: frozenset) -> list:
        out, cur = [], v
        for _ in range(4):
            m = max(r for r, _ in cur)
            cur = frozenset((c, m - r) for r, c in cur)
            out.append(cur)
            mc = max(c for _, c in cur)
            out.append(frozenset((r, mc - c) for r, c in cur))
        return out

    def _canonical(v: Any, _c: Ctx) -> Any:
        v = _shape(v, _c)
        # THE LEAST OF THE EIGHT DIHEDRAL IMAGES -- a shape's identity under rotate/reflect,
        # which is what makes two differently-oriented copies comparable at all.
        if not isinstance(v, frozenset) or not v:
            return NOT_RESOLVED
        return min(_dihedral(v), key=lambda f: sorted(f))

    def _orbit(v: Any, _c: Ctx) -> Any:
        v = _shape(v, _c)
        if not isinstance(v, frozenset) or not v:
            return NOT_RESOLVED
        return len(set(_dihedral(v)))

    def _symmetric(v: Any, _c: Ctx) -> Any:
        v = _shape(v, _c)
        if not isinstance(v, frozenset) or not v:
            return NOT_RESOLVED
        m = max(c for _, c in v)
        return frozenset((r, m - c) for r, c in v) == v

    def _is_square(v: Any, _c: Ctx) -> Any:
        v = _shape(v, _c)
        if not isinstance(v, frozenset) or not v:
            return NOT_RESOLVED
        rs = [r for r, _ in v]
        cs = [c for _, c in v]
        h = max(rs) - min(rs) + 1
        w = max(cs) - min(cs) + 1
        return h == w and len(v) == h * w

    return [Atom("bbox_area", _bbox, SHAPE, EXTENT),
            Atom("perimeter", _perimeter, SHAPE, EXTENT),
            Atom("corners", _corners, SHAPE, EXTENT),
            Atom("orbit_size", _orbit, SHAPE, EXTENT),
            Atom("canonical", _canonical, SHAPE, SHAPE),
            Atom("symmetric", _symmetric, SHAPE, BOOL),
            Atom("is_square", _is_square, SHAPE, BOOL)]


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


def _group_more() -> list[Atom]:
    """Seven more folds over the outer stream, and two readings of a delta.

    **THE TYPE SPLIT IS THE POINT.** `distinct`, `is_mode` and `aligned` need only EQUALITY, so
    they take `COMPARABLE`. `rank_in`, `is_max`, `is_min` and `sum_group` need ORDER, so they
    take `ORDERED` -- and declaring them on `COMPARABLE` would let `is_max` compare two colours,
    which is the `above(colour)` error the relate atoms already paid for once.
    """
    def _g(c: Ctx) -> tuple:
        return getattr(c, "group", ()) or ()

    def _rank(v: Any, c: Ctx) -> Any:
        g = _g(c)
        return NOT_RESOLVED if not g else sum(1 for x in g if x < v)

    def _distinct(_v: Any, c: Ctx) -> Any:
        g = _g(c)
        return NOT_RESOLVED if not g else len(set(g))

    def _is_mode(v: Any, c: Ctx) -> Any:
        g = _g(c)
        if not g:
            return NOT_RESOLVED
        return sum(1 for x in g if x == v) >= max(sum(1 for x in g if x == y) for y in set(g))

    def _is_max(v: Any, c: Ctx) -> Any:
        g = _g(c)
        return NOT_RESOLVED if not g else v >= max(g)

    def _is_min(v: Any, c: Ctx) -> Any:
        g = _g(c)
        return NOT_RESOLVED if not g else v <= min(g)

    def _sum(_v: Any, c: Ctx) -> Any:
        g = _g(c)
        return NOT_RESOLVED if not g else sum(g)

    def _aligned(v: Any, c: Ctx) -> Any:
        g = _g(c)
        return NOT_RESOLVED if not g else v in g

    def _abs(v: Any, _c: Ctx) -> Any:
        return NOT_RESOLVED if not isinstance(v, int) else abs(v)

    def _sign(v: Any, _c: Ctx) -> Any:
        return NOT_RESOLVED if not isinstance(v, int) else v > 0

    return [Atom("rank_in", _rank, ORDERED[0], EXTENT,
                 also_accepts=ORDERED[1:], reads_ctx=("group",)),
            Atom("is_max", _is_max, ORDERED[0], BOOL,
                 also_accepts=ORDERED[1:], reads_ctx=("group",)),
            Atom("is_min", _is_min, ORDERED[0], BOOL,
                 also_accepts=ORDERED[1:], reads_ctx=("group",)),
            Atom("sum_group", _sum, ORDERED[0], EXTENT,
                 also_accepts=ORDERED[1:], reads_ctx=("group",)),
            Atom("distinct", _distinct, COMPARABLE[0], EXTENT,
                 also_accepts=COMPARABLE[1:], reads_ctx=("group",)),
            Atom("is_mode", _is_mode, COMPARABLE[0], BOOL,
                 also_accepts=COMPARABLE[1:], reads_ctx=("group",)),
            Atom("aligned", _aligned, COMPARABLE[0], BOOL,
                 also_accepts=COMPARABLE[1:], reads_ctx=("group",)),
            # A DELTA IS SIGNED MOTION. Its MAGNITUDE is an extent and its DIRECTION is a
            # truth, and neither was reachable: `drow` handed a signed int to atoms that
            # compare it, so `moved 3 left` and `moved 3 right` shared no reading.
            Atom("abs_delta", _abs, DELTA, EXTENT),
            Atom("sign", _sign, DELTA, BOOL)]


def _connect() -> list[Atom]:
    """`PRED → PRED`. **G1's gap: the set had quantifiers and no connectives.**

    `all`/`any`/`none` are the QUANTIFIERS -- ∀, ∃, ¬∃ -- and they close a predicate into an
    objective. Nothing joined two predicates, so **an objective was always ONE predicate
    quantified** and *all objects are red AND square* had no form at all.

    **AND `both`/`either` ARE BUILDABLE ONLY BECAUSE OF §4's TREE.** They read a SECOND
    predicate, and until this pass an operand was a slot's raw VALUE -- so a computed predicate
    could not arrive. `Term.operand_term` is exactly what lets one fill operand 0. The largest
    structural item on the board became reachable through a change made for another reason.

    NOT_RESOLVED PROPAGATES rather than being coerced: an unreadable half makes the conjunction
    unreadable, because *this instrument cannot see it* is not *this is false*.
    """
    def _negate(v: Any, _c: Ctx) -> Any:
        return NOT_RESOLVED if v is NOT_RESOLVED else int(not v)

    def _both(v: Any, c: Ctx) -> Any:
        if v is NOT_RESOLVED or not c.operands:
            return NOT_RESOLVED if v is NOT_RESOLVED else v
        o = c.operands[0]
        return NOT_RESOLVED if o is NOT_RESOLVED else int(bool(v) and bool(o))

    def _either(v: Any, c: Ctx) -> Any:
        if v is NOT_RESOLVED or not c.operands:
            return NOT_RESOLVED if v is NOT_RESOLVED else v
        o = c.operands[0]
        return NOT_RESOLVED if o is NOT_RESOLVED else int(bool(v) or bool(o))

    return [Atom("negate", _negate, PRED, PRED),
            Atom("both", _both, PRED, PRED, reads_operand=True,
                 operand_type=PRED, reads_ctx=("operands",)),
            Atom("either", _either, PRED, PRED, reads_operand=True,
                 operand_type=PRED, reads_ctx=("operands",))]


def _quantify() -> list[Atom]:
    """`PRED → OBJ`. What closes a statement back into something bettable."""
    return [Atom("all", lambda v, _c: int(bool(v)), PRED, OBJ),
            Atom("any", lambda v, _c: int(bool(v)), PRED, OBJ),
            Atom("none", lambda v, _c: int(not v), PRED, OBJ)]


def _iterate() -> list[Atom]:
    """ITERATION -- `LIBRARY_RETRIEVAL` §12.2.1, arm `TETHER_ITERATE`, default OFF.

    Cells were REACHABLE and never ITERABLE: `SHAPE` holds the offset frozenset, so the agent
    could hold a cell set and had no way to walk it. The ten cell-level folds in this file --
    `holes`, `perimeter`, `corners`, `bbox_area` ... -- are handwritten Python, and §12.0 rules
    that the MEANS to iterate is inheritance where a SOLVED CASE would be an answer.

    THREE ATOMS AND NO FOURTH. `cells` opens, a `CELL`-typed atom is mapped by `Term.apply`, a
    `CELLS`-typed atom closes. **`map` is absent because a chain already applies atoms in
    sequence -- elementwise transformation is what a chain IS, and a second spelling of it is
    not robustness.**

    WHAT THIS DELIBERATELY DOES NOT DO: carry an accumulator across cells. A stateful reducer
    needs a body, a body is not in the atom sequence, and `units()` rebuilds a promoted term
    from the atom sequence ALONE -- so two folds differing only in body would collapse into one
    unit and execute as each other. That is CHUNK IDENTITY and it is a declared item, not a gap
    in this one.
    """
    def _cells(v: Any, c: Ctx) -> Any:
        v = _as_shape(v, c)
        if not isinstance(v, frozenset) or not v:
            return NOT_RESOLVED
        # RASTER ORDER, so position in the collection means something. An unordered collection
        # would make "the longest unbroken run" unstatable for a reason unrelated to iteration.
        return Cells(tuple(sorted(v)))

    def _cell_row(v: Any, _c: Ctx) -> Any:
        return v[0] if isinstance(v, tuple) and len(v) == 2 else NOT_RESOLVED

    def _cell_col(v: Any, _c: Ctx) -> Any:
        return v[1] if isinstance(v, tuple) and len(v) == 2 else NOT_RESOLVED

    def _count_true(v: Any, _c: Ctx) -> Any:
        """CLOSES the iteration by counting what HELD. The only reducer, and it is the one a
        predicate map needs -- `cells . <per-cell reads> . <predicate> . count_true`.

        REFUSES A NON-BOOLEAN COLLECTION, and that is not fussiness. The first version counted
        TRUTHY, so `cells . cell_col . count_true` over cells at columns 0,1,2,4 returned 3 --
        it dropped column ZERO as falsy and printed a number that looked like an answer. §12.2:
        a reading or an explicit non-reading, never a guess. `CELLS` does not carry an ELEMENT
        type, so the guard has to be here rather than in the type graph -- recorded because
        that gap is where the next wrong number comes from.
        """
        if not isinstance(v, Cells) or not len(v):
            return NOT_RESOLVED
        if not all(isinstance(x, bool) for x in v):
            return NOT_RESOLVED
        return sum(1 for x in v if x)

    return [Atom("cells", _cells, SHAPE, CELLS),
            Atom("cell_row", _cell_row, CELL, POSITION),
            Atom("cell_col", _cell_col, CELL, POSITION),
            Atom("count_true", _count_true, CELLS, EXTENT)]


def three_spaces(predict: list[Atom]) -> list[Atom]:
    """EXTRACT + RELATE + QUANTIFY, joined to whatever PREDICT the domain supplies.

    PREDICT is passed in rather than built: it is the domain's atom set -- grid transforms at
    3d -- and inventing one here would be this file choosing what the agent may bet on.
    """
    out = (list(predict) + _owner() + _extract() + _transform() + _shape_facts() + _shape_more()
           + _contact() + _relate() + _over_group() + _group_more() + _connect()
           + _quantify() + (_iterate() if _ITERATE else []))
    # ONE NAME, ONE ATOM -- and this is `A6i` in the one place it can be made mechanical.
    # `recolour` was TWO atoms for part of 2026-09-22: `arc_predict:104`'s `val -> val` grid
    # transform (the corpus files it under OPERATION) and an `OBJECT -> BOOL` extractor
    # auto-generated when `recolour` was added to `ATTRIBUTE_TYPE` while widening perception.
    # NOTHING FAILED. Term names are built from atom names, so `translate . recolour` simply
    # became ambiguous -- the collision presents as nothing, which is why the rule that
    # catches it has to fire at construction rather than be remembered at the callsite.
    # ADDING AN `ATTRIBUTE_TYPE` KEY MINTS AN ATOM; check the name against this list first.
    seen: dict[str, Atom] = {}
    for a in out:
        if a.name in seen:
            o = seen[a.name]
            raise ValueError(
                f"two atoms named {a.name!r} in one registry: "
                f"{o.in_type}->{o.out_type} and {a.in_type}->{a.out_type}. "
                f"One name, one atom -- rename the newer one.")
        seen[a.name] = a
    return out
