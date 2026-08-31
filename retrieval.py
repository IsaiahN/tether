"""3c. Retrieval keyed by the characterised residual -- and it materialises nothing.

§15.3: *the whole library is present and reachable. **What you cannot do is ask for a
primitive by name** -- you get it by describing the gap it fits.* Figure 9's procedure:

    R, described: arity · symmetry · scale -> the frame whose closure predicts it -> one
    lookup. R's own predicates name the habitat that holds phi. **Matching is a one-pass
    check, not a search.**

NOTHING IS MATERIALISED, AND THAT IS A1. `closure(Γ)` is GENERATED and never stored -- the
REACH rule exists to keep one producer of reach -- so this indexes the LIBRARY, which is
stored anyway, and keys it by a function computed on demand. **A stored index over the
closure would be a second producer of reach**, which is the design the corpus never asked for
and the check was written to catch.

AND IT DOES NOT GATE. §15.3 is explicit that the full library stays reachable: retrieval
ORDERS the candidates by how well their key fits the gap, and returns all of them. **Filtering
is what `_cannot_pay`'s docstring records as having LOST A CLOSING TERM** -- *that reasons
about what a term ought to need*. Same lesson as contact ranking: order, never exclude.

WHAT IS KEYED AND WHAT IS NOT, stated because the gap matters. §15.3 lists four keys: type
signature, arity, what varies against what is invariant, and effect shape. **The first two are
properties of a term and are keyed here. The last two are properties of a term's BEHAVIOUR**,
which needs the term applied to the residual's own frames -- so they are left to the bargain,
which already evaluates every candidate. Keying on what is free and evaluating what is not is
the one-pass check; keying on all four would be the search §15.3 says this replaces.
"""
from __future__ import annotations

import sys
from typing import Any

from gamma import SAME_AS_TARGET

sys.dont_write_bytecode = True


def characterise(robs: list, slot: str, slots: list[str],
                 types: dict[str, str] | None = None) -> dict:
    """THE GAP, DESCRIBED. `R`'s own structure, computed from the residual and nothing else.

    `arity` is how many slots the gap involves: a residual whose frames all hold one slot's
    value constant cannot need that slot, and one where another slot varies with the miss
    might. **Counted, never inferred from what a term would like to read** -- which is the
    version `_cannot_pay` records as having lost a closing term.
    """
    if not robs:
        return {"arity": 1, "varies": (), "invariant": (), "n": 0}
    others = [s for s in slots if s != slot]
    varies = tuple(s for s in others
                   if len({st.get(s) for st, _, _ in robs if s in st}) > 1)
    invariant = tuple(s for s in others if s not in varies)
    # WHICH TYPES VARIED, NOT WHICH SLOTS -- and this is the key that CROSSES. A slot name is
    # an instance: `o11.col` does not exist on the next board, so a key holding one can only
    # ever match at home. *Vocabulary permanent, instances transient*, applied to the
    # RETRIEVAL KEY -- the one place the ruling had not reached, though the stored term has
    # obeyed it since `save` dropped the binding. Figure 9's form: arity and scale, no ids.
    tv = tuple(sorted(types[s] for s in varies if s in types)) if types else ()
    return {"arity": 1 + (1 if varies else 0), "varies": varies, "varies_types": tv,
            "target_type": (types or {}).get(slot),
            "invariant": invariant, "n": len(robs)}


def key_of(term: Any) -> tuple:
    """A term's index key: signature, arity, and **the slot it can read**. All free.

    **THE THIRD IS §15.3's THIRD KEY, AND THE BLOCKER SAID IT WAS NOT FREE.** The recorded
    reason was *needs the term applied to the residual's frames*, filed beside `effect shape`
    under *properties of its BEHAVIOUR*. **The grouping is what was wrong, not the reasoning
    about cost** -- `effect shape` genuinely requires running it; this does not.

    **`Ctx` HAS TWO FIELDS.** An atom is `fn(v, c)` and `c` carries `action` and `operands` and
    nothing else, so a term's dependency set is bounded at CONSTRUCTION: its own slot, its
    operand slot, the action. **It cannot vary with a slot it has no accessor for**, and
    `reads_operand` is *declared at construction, never inferred*. So the INVARIANT half is
    read off the term in O(1) and the *would consume the work it exists to save* argument does
    not reach it.

    **SOUND ONE WAY AND NOT THE OTHER, WHICH IS WHY IT IS A KEY AND NOT A PROOF.** Invariance
    is exact -- no accessor, no dependence. *Varies* is an upper bound: a term that reads its
    operand may still ignore it. **`fits` orders and excludes nothing, so an over-approximation
    is the right shape**; a gate would need the exact set and would have to run the term.
    """
    # `operand_type` AND NOT `operand`. The first is declared at construction and is a TYPE,
    # so it survives `save` dropping the binding; the second is a slot name and does not. An
    # imported term keyed on `operand` scored as if unary on every gap, which is the shape of
    # the transfer column having no subject.
    return (term.in_type, term.out_type, 2 if term.reads_operand else 1, term.operand_type)


def fits(term: Any, gap: dict, in_type: str, out_type: str) -> int:
    """How well one term's key fits the gap. Higher is better, and NOTHING is excluded.

    Two points for the type signature the slot actually needs, one for matching the gap's
    arity. **A zero score still comes back** -- ordering is the whole mechanism, and a term
    that scores nothing is tried last rather than not at all.

    **THE THIRD KEY SCORES LIKE ARITY**, which is the other free one: *aimed at a slot that
    actually moved* is one point, and a term reading a slot the residual held still gets
    nothing for it. **A unary term is invariant to every other slot**, so it scores where the
    gap has nothing else varying -- an invariance claim rather than an absence of one.
    """
    t_in, t_out, arity, reads = key_of(term)
    if reads is None:
        aimed = not gap["varies"]
    elif reads == SAME_AS_TARGET:
        # THE TARGET'S TYPE, NOT "ANYTHING MOVED". The first version asked `bool(varies)` and
        # measured as a CONSTANT the moment `delta` published 42 slots that vary every step:
        # 154 of 154 gaps had something moving, and the key collapsed onto arity at 87.3%.
        # `SAME_AS_TARGET` says the operand HAS THE TARGET'S TYPE, so the question is whether
        # that type is among the ones that moved -- discriminating, and still instance-free.
        aimed = gap.get("target_type") in gap.get("varies_types", ())
    else:
        aimed = reads in gap.get("varies_types", ())
    return (2 * (t_in == in_type and t_out == out_type)
            + (arity == gap["arity"]) + bool(aimed))


def retrieve(library: dict, gap: dict, in_type: str = "val",
             out_type: str = "val") -> list[str]:
    """ONE PASS over the library, ordered by fit. Every name comes back.

    Not a search: no composition, no enumeration, no closure walked. The library is what is
    stored, this reads it once, and the ordering is what makes a big library an asset rather
    than a liability -- §23.5's *an asset when you look things up by the shape of your gap and
    a liability when you walk it in registry order.*

    LENGTH IS THE TIE-BREAK, AND THAT IS DELIBERATE. Within one habitat the shorter term still
    wins, so MDL's preference is not overturned -- it is **restricted to the habitat first**.
    Ordering by length alone is the registry walk; ordering by fit alone would throw away the
    one preference the bargain is built on.
    """
    scored = [(-fits(t, gap, in_type, out_type), len(t), n) for n, t in library.items()]
    return [n for _, _, n in sorted(scored)]
