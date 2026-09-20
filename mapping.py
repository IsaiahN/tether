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

import arc_percept
import composer
import detectors
import reverse_engineer

# THE GENERIC HALF LIVES IN `closure_map.py` (reviewer ruling, 2026-09-20). It imports nothing,
# so there is no route from it to a replay reader -- which is what lets the betting path reach
# it while THIS module stays blocked by `CUE_BOUNDARY`. The split is the firewall; the rule did
# not have to get smarter.
from closure_map import DEFORM_FAMILY, OP_CLOSURE, POPULATION, map_chunk, to_closure

sys.dont_write_bytecode = True


__all__ = ['DEFORM_FAMILY', 'OP_CLOSURE', 'POPULATION', 'map_chunk', 'to_closure',
           'map_answer_key', 'molecule_key']


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


def molecule_key(path: str) -> dict:
    """The end-to-end cue->closure chain, PER OBJECT: the mutation (reverse_engineer._match, first
    -> last frame) LIGHTS each object's atoms (detectors), and those atoms COMPOSE into a named
    molecule only when they form an emergent composite (composer, via recipes) -- one object
    rotating AND translating is `Orbit`. Composition is per object, never the chunk union: `Orbit`
    is one
    object's Rotate+Translate, not two objects doing unrelated things.

    An empty `molecules` is CORRECT, not a gap: most co-occurrences (Recolour+Translate) are a
    CONJUNCTION of independent atoms, fully stated by the atom list -- not every pair is a molecule.
    The composer's job is to name the emergent composite where one exists and stay silent otherwise.
    """
    steps = reverse_engineer.load_replay(path)
    chunks = reverse_engineer.chunk_replay(steps)
    perceived = [arc_percept.components(s["grid"]) for s in steps]
    out = []
    for c in chunks:
        i0, i1 = c["idx"][0], c["idx"][-1]
        eff = reverse_engineer._match(perceived[i0], perceived[i1])
        objs = []
        for e in eff:
            if e.get("kind") == "change":
                atoms = sorted(d["atom"] for d in detectors.light_object(e))
                objs.append({"atoms": atoms,
                             "molecules": [m["molecule"] for m in composer.candidates(set(atoms))]})
        van = sum(1 for x in eff if x["kind"] == "vanish")
        app = sum(1 for x in eff if x["kind"] == "appear")
        out.append({"level": c["level"], "frames": [i0, i1], "objects": objs,
                    "population": [d["atom"] for d in detectors.light_population(van, app)]})
    return {"game": path, "n_chunks": len(chunks), "chunks": out}


if __name__ == "__main__":
    import json
    import sys as _s
    path = _s.argv[1] if len(_s.argv) > 1 else "replays/ls20_human.ndjson"
    if "--molecules" in _s.argv:
        mk = molecule_key(path)
        for c in mk["chunks"][:8]:
            named = [(o["atoms"], o["molecules"]) for o in c["objects"] if o["molecules"]]
            print(f"  L{c['level']} {c['frames']}: {len(c['objects'])} objs, "
                  f"pop={c['population']}, molecules={named}")
        raise SystemExit
    r = map_answer_key(path)
    print(json.dumps({k: r[k] for k in ("game", "n_chunks", "mapped_chunks", "mapping_gap_ops")},
                     indent=1))
    for c in r["chunks"][:6]:
        print(f"  L{c['level']} {c['frames']}: {c['closure']['closure_derivation']}")
