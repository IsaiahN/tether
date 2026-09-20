"""The op -> closure derivation, with NO import path to any replay reader.

SPLIT OUT OF `mapping.py` (reviewer ruling, 2026-09-20). `mapping.py` held two kinds of thing
with different statuses: this generic half, which maps ANY described mutation to its closure
atom + recipe, and `map_answer_key` / `molecule_key`, which read a HUMAN REPLAY. `CUE_BOUNDARY`
blocked the module, so blocking the answer-key half also blocked the composer's own
cue->closure matching -- which is the design (`mapping not search`), not a shortcut.

THE FIREWALL IS NOW A FACT ABOUT THE IMPORT GRAPH RATHER THAN A PROPERTY SOMEONE REMEMBERS.
The reviewer refused a provenance-aware lint rule for exactly that reason: provenance of a
RUNTIME input cannot be checked statically, and *a firewall that only holds when the caller is
careful is a convention with a lint rule painted on it.* So the split does the work and
`CUE_BOUNDARY` keeps working as written.

THIS MODULE IMPORTS NOTHING. That is the property under test, and it is what makes it safe for
the betting path to reach: there is no route from here to a replay.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

# reverse_engineer's op -> the closure atom that expresses it, with its ATOMS.md recipe. The op is
# the agent's own perceived transformation; the closure atom is the library concept it instantiates.
# This is a VOCABULARY ALIGNMENT (two names for one concept), not a per-game answer -- the recipe is
# how the closure builds it, the provenance a projection cannot recover. The 1:1 ops resolve here;
# reshape and population BRANCH (below), because one op stands for several closure atoms.
OP_CLOSURE = {
    "recolour":   {"atom": "Recolour",  "recipe": "Co + Featural identity",  "op": "+"},
    "translate":  {"atom": "Translate", "recipe": "Ct + Co",                 "op": "+"},
    "rescale":    {"atom": "Scale",     "recipe": "Frac + Scale",            "op": "+"},
}

# reshape -> the Deform FAMILY. The precision pass (2026-09-17) traversing the atom recipes finds
# `Deform` was a coarse label for two atoms: Rotate = Ge + Gs, Reflect = Ge + Chirality. The
# reverse-engineered statement carries only attrs=["shape"], NOT the geometric signature, so the
# two cannot be SELECTED at map time -- both candidates are named and the selector is recorded as
# the signal the statement does not yet propagate. Naming a choice the signal cannot support would
# be a guess; naming the branch is honest.
DEFORM_FAMILY = {
    "atom": "Deform",
    "candidates": [{"atom": "Rotate",  "recipe": "Ge + Gs"},
                   {"atom": "Reflect", "recipe": "Ge + Chirality"}],
    "selector": "shape signature (rotation vs mirror) -- not propagated by the statement",
}

# population -> resolved by the vanished/appeared counts the statement ALREADY carries, so the
# finer closure atom follows from the DIRECTION of the count (no new signal invented): appear-only
# is Construct, vanish-only is Erase, one->several is Separate, several->one is Merge. An equal
# exchange is direction-ambiguous and keeps both candidates.
POPULATION = {
    "construct": {"atom": "Construct", "recipe": "Rep + Bind"},
    "erase":     {"atom": "Erase",     "recipe": "Contact + Consumed"},
    "separate":  {"atom": "Separate",  "recipe": "Decompose + Co"},
    "merge":     {"atom": "Merge",     "recipe": "Amalgamate + Med miscible"},
}


def _population(statement: dict) -> dict:
    van, app = statement.get("vanished", 0), statement.get("appeared", 0)
    key = ("construct" if app and not van else "erase" if van and not app
           else "separate" if app > van else "merge" if van > app else None)
    base = {"op": "population", "attrs": statement.get("attrs"),
            "vanished": van, "appeared": app, "mapping_gap": False}
    if key is None:  # equal exchange -- direction ambiguous
        return {**base, "closure_atom": "Population",
                "candidates": [POPULATION["separate"], POPULATION["merge"]],
                "selector": "equal vanish/appear -- direction ambiguous"}
    hit = POPULATION[key]
    return {**base, "closure_atom": hit["atom"], "recipe": hit["recipe"], "operator": "+"}


def to_closure(statement: dict) -> dict:
    """One reverse-engineered statement -> its closure derivation (atom + recipe + operator). An op
    with no closure counterpart is a MAPPING gap (the correspondence is incomplete), never an
    inexpressibility -- expressibility is closed over the exhaustive priors."""
    op = statement.get("op")
    if op == "reshape":
        return {"op": op, "attrs": statement.get("attrs"), "closure_atom": DEFORM_FAMILY["atom"],
                "candidates": DEFORM_FAMILY["candidates"], "selector": DEFORM_FAMILY["selector"],
                "mapping_gap": False}
    if op == "population":
        return _population(statement)
    hit = OP_CLOSURE.get(op)
    if hit is None:
        return {"op": op, "closure": None, "mapping_gap": True}
    return {"op": op, "attrs": statement.get("attrs"),
            "closure_atom": hit["atom"], "recipe": hit["recipe"], "operator": hit["op"],
            "mapping_gap": False}


def map_chunk(composition: dict) -> dict:
    """A chunk's reverse-engineered composition -> its statements' closure derivations, joined by
    the operator that composes them (conjunction of simultaneous effects)."""
    derivations = [to_closure(s) for s in composition.get("statements", [])]
    mapped = [d for d in derivations if not d["mapping_gap"]]
    return {"closure_derivation": " + ".join(d["closure_atom"] for d in mapped) or None,
            "derivations": derivations,
            "mapping_gaps": [d["op"] for d in derivations if d["mapping_gap"]]}

