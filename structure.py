"""The STRUCTURE HASH: one stable string naming a term's FORM, never its occasion.

This is the primitive the library system names but never built
(`docs/03-DESIGN/02-LIBRARY_RETRIEVAL.md`, CONFLICTS b: *"NO STRUCTURE HASH EXISTS ...
the single largest unbuilt prerequisite in the document"*). Rulings 7, 8 and 9 and
§5.10 all key cross-game memory on it. It is built here as a **pure, callable,
unwired** function: adding a consumer is a separate design decision (Isaiah's),
not part of this module.

DERIVATION FROM THE FIGURES
--------------------------
* **Figure 9** describes a residual by *"arity · symmetry · scale"* and says
  *"describe it before you go looking, or any frame you pick will seem to fit"* and
  *"you get a kind of thing, never the answer itself"*. So what is hashed is the
  FORM — atom names in composition order, the operand-tree's shape, the guard's
  kind, and the type signature. No slot name, object id, game id or cycle number
  enters: those are the occasion, not the arity or scale.
* **Figure 13**: *"The set is closed. The arrangements are not."* and *"composition
  only ever rearranges the kinds already held"*. Two chains over the same atoms in
  a different order are different arrangements and must hash differently; the
  atoms themselves are the closed set and are named by their vocabulary names.
* **Figure 4**: *"Only methods cross up. Only head starts come down."* and *"A
  recording carried upward looks like knowledge and is a description of one
  occasion."* The atom names and typing are the permanent vocabulary (the
  kernel); `Term.operand`, `Term.guard_ref` and `Term.origin` are per-board
  bindings and provenance — transient instances — so only their PRESENCE (for
  the bindings) is structural, never their value.

`hashlib.sha256` over a canonical JSON encoding is used, never Python's `hash()`:
the key must be identical across runs, processes and machines, and `hash()`
is salted per process. `origin` is deliberately excluded (ruling 7 makes it a
status, not structure), so a term carries the same structure hash no matter
where it was minted or which game it was later pulled into.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any


def _atom_struct(atom: Any) -> tuple:
    """The structural face of one atom: its vocabulary name and declared typing.

    The function object, its source, its admission clause and any identity are
    excluded — those are provenance or implementation, not the atom's form.
    """
    name = getattr(atom, "name", atom)
    return (
        str(name),
        str(getattr(atom, "in_type", "") or ""),
        str(getattr(atom, "out_type", "") or ""),
        tuple(getattr(atom, "also_accepts", ()) or ()),
        str(getattr(atom, "operand_type", "") or ""),
        tuple(getattr(atom, "reads_ctx", ()) or ()),
        bool(getattr(atom, "reads_operand", False)),
        bool(getattr(atom, "polymorphic", False)),
        str(getattr(atom, "elem_type", "") or ""),
    )


def _term_struct(term: Any) -> dict:
    """A canonical, order-preserving description of a term's structure only.

    `operand` and `guard_ref` contribute a presence bit, never their value: a slot
    or object name is an instance and would not mean anything on the next board.
    `origin` is not read at all. A nested `operand_term` is described recursively,
    so the operand-TREE (not merely its root) is part of the key.
    """
    atoms = tuple(getattr(term, "atoms", ()) or ())
    operand_term = getattr(term, "operand_term", None)
    return {
        "atoms": [_atom_struct(a) for a in atoms],
        "types": [
            str(getattr(term, "in_type", "") or ""),
            str(getattr(term, "out_type", "") or ""),
            str(getattr(term, "operand_type", "") or ""),
        ],
        # PRESENCE, not the slot name (an instance).
        "has_operand": getattr(term, "operand", None) is not None,
        # The recursively described operand tree, or None.
        "operand_term": _term_struct(operand_term) if operand_term is not None else None,
        # The guard KIND is structural; the referent is a per-board binding, so
        # only whether one exists is structural, never the name it holds.
        "guard": str(getattr(term, "guard", None) or ""),
        "has_guard_ref": getattr(term, "guard_ref", None) is not None,
    }


def structure_hash(term: Any) -> str:
    """Return a stable hex SHA-256 of the TERM'S STRUCTURE.

    Atom names in composition order, their declared typing, the operand-tree's
    shape (including operand presence), and the guard kind/referent presence are
    the whole input. Slot names, object ids, game ids, cycle numbers, provenance
    and every other instance are excluded. Two structurally identical terms on
    different boards therefore share a hash; two chains differing only by atom
    order, operand presence or guard structure do not.

    Accepts a `gamma.Term` (or any object with the same structural fields), so it
    stays domain-agnostic and import-free. Nothing imports this module from the
    agent path; a consumer is a separate decision.
    """
    canonical = json.dumps(
        _term_struct(term), sort_keys=True, separators=(",", ":"), ensure_ascii=True
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
