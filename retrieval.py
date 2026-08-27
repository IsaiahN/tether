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

sys.dont_write_bytecode = True


def characterise(robs: list, slot: str, slots: list[str]) -> dict:
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
    return {"arity": 1 + (1 if varies else 0), "varies": varies,
            "invariant": invariant, "n": len(robs)}


def key_of(term: Any) -> tuple:
    """A term's index key: its type signature and its arity. Both free to read off it."""
    return (term.in_type, term.out_type, 2 if term.reads_operand else 1)


def fits(term: Any, gap: dict, in_type: str, out_type: str) -> int:
    """How well one term's key fits the gap. Higher is better, and NOTHING is excluded.

    Two points for the type signature the slot actually needs, one for matching the gap's
    arity. **A zero score still comes back** -- ordering is the whole mechanism, and a term
    that scores nothing is tried last rather than not at all.
    """
    t_in, t_out, arity = key_of(term)
    return 2 * (t_in == in_type and t_out == out_type) + (arity == gap["arity"])


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
