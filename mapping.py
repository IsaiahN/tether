"""The cue -> closure mapping (Isaiah, 2026-09-15): a chunk's mutations map to the CLOSURE atoms and
their recipes that express the intent -- so the answer key names library derivations (composable via
`OPERATORS.md`), not ad-hoc ops. This is the MAPPING job: match, do not search. Every target is
reachable/findable in the closure (`docs/library-closure/ATOMS.md`); nothing invented.

The route is the RECIPE structure, validated against ATOMS.md (2026-09-15): the ARC-level
transformations have direct closure entries with recipes -- Recolour = Co + Featural identity,
Translate = Ct + Co, Rotate = Ge + Gs -- so a mutation maps to its closure atom + recipe + operator,
carrying the composition PROVENANCE the projection cannot recover.

§12.3 / CUE_BOUNDARY: a CUE module. It produces the answer key's closure derivations (proctor-side,
retrieval/mapping); it is never imported by the betting path (enforced by conform/lint.py).
The atoms it names are what the agent must REACH for, never terms handed to it.
"""

from __future__ import annotations

import sys

import reverse_engineer

sys.dont_write_bytecode = True

# reverse_engineer's op -> the closure atom that expresses it, with its ATOMS.md recipe. The op is
# the agent's own perceived transformation; the closure atom is the library concept it instantiates.
# This is a VOCABULARY ALIGNMENT (two names for one concept), not a per-game answer -- the recipe is
# how the closure builds it, the provenance a projection cannot recover.
OP_CLOSURE = {
    "recolour":   {"atom": "Recolour",  "recipe": "Co + Featural identity",  "op": "+"},
    "translate":  {"atom": "Translate", "recipe": "Ct + Co",                 "op": "+"},
    "rescale":    {"atom": "Scale",     "recipe": "Frac + Scale",            "op": "+"},
    "reshape":    {"atom": "Deform",    "recipe": "Ge + Featural change",    "op": "+"},
    "population":  {"atom": "Population", "recipe": "Spawn | Merge | Separate", "op": "|"},
}


def to_closure(statement: dict) -> dict:
    """One reverse-engineered statement -> its closure derivation (atom + recipe + operator). An op
    with no closure counterpart is a MAPPING gap (the correspondence is incomplete), never an
    inexpressibility -- expressibility is closed over the exhaustive priors."""
    op = statement.get("op")
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


def map_answer_key(path: str) -> dict:
    """A game's human-panel replay -> the closure-mapped answer key: every chunk's intent as a
    library composition, with provenance and any mapping gaps. Consumes reverse_engineer's chunking
    and effect layer; adds the closure derivation layer."""
    ak = reverse_engineer.answer_key(path)
    chunks = [{"level": c["level"], "frames": c["frames"],
               "closure": map_chunk(c["composition"])} for c in ak["chunks"]]
    all_gaps = [g for c in chunks for g in c["closure"]["mapping_gaps"]]
    mapped = sum(1 for c in chunks if c["closure"]["closure_derivation"])
    return {"game": ak["game"], "n_chunks": ak["n_chunks"], "mapped_chunks": mapped,
            "mapping_gap_ops": sorted(set(all_gaps)), "chunks": chunks}


if __name__ == "__main__":
    import json
    import sys as _s
    path = _s.argv[1] if len(_s.argv) > 1 else "replays/ls20_human.ndjson"
    r = map_answer_key(path)
    print(json.dumps({k: r[k] for k in ("game", "n_chunks", "mapped_chunks", "mapping_gap_ops")},
                     indent=1))
    for c in r["chunks"][:6]:
        print(f"  L{c['level']} {c['frames']}: {c['closure']['closure_derivation']}")
