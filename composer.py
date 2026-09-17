"""Lit atoms -> candidate molecules via the RECIPES (F162: the recipes, not the domain adjacency
graph, are the atom->molecule composition). Parses ATOMS.md's recipe tables into {molecule ->
ingredients} and, given the atoms a mutation lit (detectors.py), returns the molecules whose recipe
those atoms COVER -- the composition the lit cues map to. Nothing invented: every molecule and its
recipe is the closure's own; this only reads them.

The layer above detectors: detectors light the ARC-level atoms (Translate, Rotate...), each itself a
recipe in ATOMS.md; the composer finds the molecules those compose into (Orbit = Rotate+Translate).
An ingredient the board never lights (Lev, Su...) simply keeps its molecule off the candidate list,
so the closure filters itself to what the game supports -- no ARC judgement here.

§12.3 / CUE_BOUNDARY: a CUE module (retrieval), never imported by the betting path -- enforced by
conform/lint.py, which lists `composer` among the cue modules.
"""

from __future__ import annotations

import functools
import re
import sys

sys.dont_write_bytecode = True

_ATOMS_MD = "docs/library-closure/ATOMS.md"


@functools.lru_cache(maxsize=2)
def recipes(path: str = _ATOMS_MD) -> dict:
    """{molecule -> frozenset(ingredients)} from ATOMS.md's `| name | a + b | ... |` recipe rows.
    A row with no `+` in the recipe column is an atom (or separator) and carries no composition."""
    out: dict = {}
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            m = re.match(r"\s*\|(.+?)\|(.+?)\|(.+?)\|\s*$", ln)
            if not m:
                continue
            name = m.group(1).strip().strip("*").strip()
            recipe = m.group(2).strip().strip("*").strip()
            if "+" not in recipe:
                continue
            comps = frozenset(c.strip().strip("*").strip() for c in recipe.split("+"))
            if name and all(comps):
                out[name] = comps
    return out


def candidates(lit: set, path: str = _ATOMS_MD) -> list[dict]:
    """Molecules whose recipe ingredients are ALL among the lit atoms -- the compositions the lit
    cues fully support. Ranked by recipe size: a longer covered recipe is a more specific match."""
    lit = set(lit)
    hits = [{"molecule": n, "recipe": sorted(ing), "size": len(ing)}
            for n, ing in recipes(path).items() if ing <= lit]
    return sorted(hits, key=lambda d: (-d["size"], d["molecule"]))


if __name__ == "__main__":
    import json
    for lit in ({"Rotate", "Translate"}, {"Rotate", "Translate", "Scale"}, {"Recolour"}):
        print(sorted(lit), "->", json.dumps([c["molecule"] for c in candidates(lit)]))
