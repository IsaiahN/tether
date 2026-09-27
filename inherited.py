"""The INHERITED VOCABULARY -- what the agent can reach for, keyed by what its eyes report.

**NOT CALLED `library.py`, DELIBERATELY, AND THE REASON IS THIS SESSION'S OWN TALLY.** `library`
already names `Gamma.library` -- the terms the agent HOLDS, minted or imported and earned. This
is a different object: the 4,042 entries it can REACH FOR and has not earned. Five `A6i`
collisions were filed on 2026-09-27 alone, one of them in the plan that specified this module,
where `retrieve()`'s scan over `gamma.library` was mistaken for a scan over these files.
`retrieval.py` set the precedent with `Mechanics` over `Shape`.

    GAMMA.LIBRARY   what the agent holds.      small, earned, bet with
    THIS            what it can reach for.     4,042, inherited, not yet its own

THE KEY IS PERCEPTUAL BECAUSE THE AGENT HAS NO LEXICON -- Isaiah, 2026-09-27, overruling
§15.3's *you cannot ask for a primitive by name*. The overrule matters less than the reason:
**the agent does not think in words and is not an LLM**, so a name is an opaque string to it
and by-name lookup was never a temptation to forbid. What it has is visual acumen. It
distinguishes by attribute and by cue, so that is what it searches with.

WHICH INDEX, MEASURED RATHER THAN ASSUMED. `by_attribute` has 5,040 keys and they are
domain-scientific -- `ATPconcentration`, `BellInequality`, `DNAmethylation`. Of 23 names the
agent's perception actually emits, 13 exist, and the largest reaches 10 entries of 1,748. **The
tags are the surface**: 34 of them, 9,029 memberships, and `observer._MUT_ATTR` maps every
mutation the agent detects onto `position`/`extent`/`shape`/`colour` -- four of the thirty-four,
spelled the same. Nobody coordinated that; both are describing what an eye can distinguish.

ACCUMULATE, NEVER INTERSECT, AND THAT IS A MEASUREMENT TOO. The obvious design makes "position
changed" the query `POSITION+CHANGE`, which returns FOUR entries; in this corpus `CHANGE` pairs
with abstractions (`ACTION+CHANGE` 206) and not with visual attributes. A delta instead
DECOMPOSES, as `arc_atoms` already says of it -- *a DELTA IS SIGNED MOTION, its MAGNITUDE is an
extent and its DIRECTION is a sign* -- so one mutation lights `POSITION`, `MOTION`, `SPEED` and
`DIRECTION`, four healthy keys instead of one starved one.

**AND THE WEIGHTS ARE NOT THE SEAT'S.** 1,579 of 1,748 atoms carry `tags.scored`, a
`{tag, score, via}` list the library supplies. Inventing a weight here would be failure mode 4
wearing a retrieval's clothes.

ORDER, NEVER EXCLUDE -- kept even though §15.3 was overruled, because it was earned separately:
`_cannot_pay` filtered on what a term *ought to need* and LOST A CLOSING TERM. So `reach_tier`
ORDERS and never gates, and every name the query touches comes back.

NOTHING IS MATERIALISED. `retrieval.py`'s A1: a stored index over the closure would be a second
producer of reach. The four files are read once and the callables are built PER KEY ON DEMAND.
"""
from __future__ import annotations

import json
import sys
from functools import cache, lru_cache
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

ROOT = Path(__file__).parent / "library"

# THE CUE'S CLASSES TO THE LIBRARY'S TAGS, AND IT IS A TABLE RATHER THAN A RULE. `_CUE_ATTR` in
# `tether` is the same shape and says why: the observer's classes and the library's tags agree
# on four names by convergence, not by contract, so the mapping is DATA that can be pinned and
# moved -- `conform/lint.py`'s *exemptions as data, not logic*.
#
# THE DELTA ROW IS THE ONE THAT CARRIES WORK. A mutation is signed, and `sign`/`abs_delta`
# already exist as atoms, so a moved object reaches DIRECTION and SPEED as well as POSITION.
CUE_TAGS: dict[str, tuple[str, ...]] = {
    "position": ("POSITION", "MOTION"),
    "extent": ("EXTENT",),
    "shape": ("SHAPE", "STRUCTURE"),
    "colour": ("COLOUR",),
    "count": ("COUNT",),
    "contact": ("CONTACT",),
}

# A MUTATION ADDS THESE ON TOP OF ITS ATTRIBUTE'S TAGS. Kept separate from `CUE_TAGS` so that
# *what changed* and *that it changed* stay two facts -- the same split `observer` draws between
# `cue` and `mutations`, and the reason a blind frame and a still frame are different rows.
DELTA_TAGS: tuple[str, ...] = ("CHANGE", "DIRECTION", "SPEED")

# THE RAW PER-OBJECT READINGS, WHICH ARE NAMED DIFFERENTLY FROM THE MUTATION CLASSES. The
# observer publishes `row`/`col`/`h`/`w` per object and `position`/`extent` per mutation, so a
# still frame and a moved one speak two vocabularies for one thing.
#
# BUILT BY INVERTING `tether._CUE_ATTR` RATHER THAN AUTHORED, because that table already
# declares the same correspondence for attention and a second hand-written copy is two
# quantities under one intent -- the collision this module is named to avoid. The extra names
# are `sensors_heavy`'s, which the observer carries per object and `_CUE_ATTR` never needed.
RAW_TAGS: dict[str, tuple[str, ...]] = {
    "row": ("POSITION",), "col": ("POSITION",),
    "h": ("EXTENT",), "w": ("EXTENT",), "height": ("EXTENT",), "width": ("EXTENT",),
    "area": ("EXTENT",), "occupiedCells": ("EXTENT",), "perimeter": ("EXTENT",),
    "colour": ("COLOUR",),
    "shape": ("SHAPE", "STRUCTURE"), "density": ("STRUCTURE",), "solidity": ("STRUCTURE",),
    "orientation": ("DIRECTION",), "velocity": ("SPEED", "MOTION"),
}


@lru_cache(maxsize=1)
def load() -> dict[str, Any]:
    """The four files, read ONCE. Missing files are an empty vocabulary and never an exception:
    the agent must run without the inheritance, or the ablation clause has nothing to wipe."""
    out: dict[str, Any] = {"atoms": {}, "molecules": {}, "tags": {}, "domains": {}}
    for key, name, inner in (("atoms", "atoms.json", "atoms"),
                             ("molecules", "molecules.json", "molecules"),
                             ("tags", "tag_index.json", None),
                             ("domains", "domains.json", None)):
        path = ROOT / name
        if not path.exists():
            continue
        raw = json.loads(path.read_text(encoding="utf-8"))
        out[key] = raw.get(inner, raw) if inner else raw

    # THE AGENT'S OWN ATOMS JOIN THE VOCABULARY, IN THEIR OWN FILE -- Isaiah: *add your few
    # dozen atoms to it.* Kept separate on disk rather than merged into `atoms.json` because
    # GIVEN and BUILT must stay separable: the ablation partition is by WHICH CLAUSE ADMITTED A
    # THING and *cannot be reconstructed from a `prior` stamp afterwards*. A file boundary and
    # the `AGENT|` prefix are both cheap and neither can drift.
    agent = ROOT / "agent_atoms.json"
    if agent.exists():
        mine = json.loads(agent.read_text(encoding="utf-8")).get("atoms", {})
        out["atoms"] = {**out["atoms"], **mine}
        # AND THEY ARE INDEXED IN MEMORY, NEVER WRITTEN BACK. `tag_index.json` is the
        # reviewer's artefact; regenerating it here would make this module a second producer
        # of the index, which is the same defect `retrieval.py` refuses as a second producer
        # of reach. The extension costs one pass over 62 entries at load.
        by_tag = out["tags"].setdefault("by_tag", {})
        for key, e in mine.items():
            for tag in (e.get("tags") or {}).get("primary") or ():
                by_tag.setdefault(tag, {}).setdefault("atoms", []).append(key)
    return out


def entry(key: str) -> dict | None:
    """One entry by its `DOMAIN|Name` key, atom or molecule. THE SEAT MAY ASK BY NAME; the agent
    reaches by tag. Nothing here is on the agent's path -- `reach` is."""
    lib = load()
    return lib["atoms"].get(key) or lib["molecules"].get(key)


def tags_of(cue: dict | None) -> dict[str, float]:
    """THE CUE, READ AS TAGS. `{tag: weight}` -- accumulation, never intersection.

    Takes `observer.Live.see()`'s output. A blind frame (`first`, or no cue) yields nothing,
    which is a REFUSAL and not an empty query: retrieving on no evidence would order the whole
    library by nothing and call the result a reading.
    """
    if not cue:
        return {}
    want: dict[str, float] = {}
    muts = (cue.get("mutations") or {}).get("attributes") or {}
    for attr in muts:
        for t in CUE_TAGS.get(attr, ()):
            want[t] = want.get(t, 0.0) + 1.0
        for t in DELTA_TAGS:
            want[t] = want.get(t, 0.0) + 0.5
    # THE STILL FRAME STILL SEES. An object that did not move still has a position and an
    # extent, so the attributes PRESENT contribute at a lower weight than the ones that MOVED --
    # surprise drives attention (`ARC_HUMAN_PRIORS`, Berlyne) and does not exhaust it.
    #
    # **TWO LEVELS DOWN, NOT ONE, AND THE FIRST VERSION READ THE WRONG ONE.** `cue["objects"]`
    # is `{object index: {attribute: value}}`, so iterating it yields INDICES -- `0`, `1` --
    # and every lookup missed silently. It did not fail; it contributed nothing, which is the
    # abstention an unreached mechanism always produces. Caught by an executes-check.
    for per_obj in ((cue.get("cue") or {}).get("objects") or {}).values():
        if not isinstance(per_obj, dict):
            continue
        for attr in per_obj:
            for t in RAW_TAGS.get(attr, ()):
                want[t] = want.get(t, 0.0) + 0.25
    return want


def reach(want: dict[str, float], kinds: tuple[str, ...] = ("atoms", "molecules")) -> list[str]:
    """ORDERED CANDIDATES FOR A TAG VECTOR. Every name the tags touch comes back.

    Keyed, never scanned: `by_tag` is a direct read per tag, so the cost is the number of tags
    the cue lit rather than the size of the library. That is the reviewer's ruling of
    2026-09-27 -- *indexing is not a cheaper search; same closure, same candidates, same
    results, reached by key rather than by enumeration.*

    THE SCORE IS THE LIBRARY'S OWN. Each entry's `tags.scored` gives `{tag, score}`; the weight
    the cue put on that tag multiplies it, and the products sum. An entry the cue lit twice
    outranks one it lit once, which is `_accumulate`'s shape: many weak contributions into one
    vector.

    `by_pair` IS A BONUS AND NEVER A GATE -- it was measured as a filter first and starves:
    `CHANGE+POSITION` holds 4 entries against `POSITION`'s 177.

    REACH TIER ORDERS AND DOES NOT EXCLUDE. 444 atoms are tier 0-1 and computable from a board
    today; 1,132 carry no tier at all. Dropping the untiered would be `_cannot_pay`'s lost
    closing term repeated at the vocabulary.
    """
    if not want:
        return []
    lib = load()
    by_tag = lib["tags"].get("by_tag") or {}
    score: dict[str, float] = {}
    for tag, weight in want.items():
        members = by_tag.get(tag) or {}
        for kind in kinds:
            for key in members.get(kind) or []:
                score[key] = score.get(key, 0.0) + weight * _tag_score(key, tag)
    # THE PAIR BONUS IS KEYED TOO, AND IT WAS NOT -- the reviewer, 2026-09-27. This iterated
    # ALL 477 `by_pair` entries on every call and tested each against the cue, which is a SCAN
    # inside the function whose whole purpose is that there is no scan. The cue lights a
    # handful of tags, so the pairs it can possibly match are a handful of keys: build them
    # and read them.
    #
    # SORTED, because that is how the index spells a pair (`ACTION+CHANGE`), and a lookup on
    # the unsorted spelling would MISS SILENTLY -- returning nothing and reading exactly like
    # a cue with no co-occurrence.
    by_pair = lib["tags"].get("by_pair") or {}
    lit = sorted(want)
    for i, a in enumerate(lit):
        for b in lit[i + 1:]:
            members = by_pair.get(f"{a}+{b}")
            if not members:
                continue
            bonus = min(want[a], want[b]) * 0.5
            for kind in kinds:
                for key in members.get(kind) or []:
                    if key in score:
                        score[key] += bonus
    return sorted(score, key=lambda k: (-score[k], _tier(k), k))


# THE AGENT'S OWN ATOMS, KEYED THE SAME WAY -- and the mapping is DERIVED, never authored.
# Four of the agent's attribute TYPES are library tags under the identical spelling, which is
# the least-invented mapping available: the type system already sorted its readings into the
# same perceptual categories the reviewer's clustering found.
#
# DELTA IS THE ONE THAT NEEDS A SENTENCE, AND `arc_atoms` SUPPLIES IT: *a DELTA IS SIGNED
# MOTION, its MAGNITUDE is an extent and its DIRECTION is a sign* -- so a delta-typed atom is
# reachable from CHANGE, DIRECTION and SPEED rather than from a tag of its own.
#
# BOOL/PRED/OBJ/OBJECT/val get NOTHING, deliberately. They are structural rather than
# perceptual, and giving them tags would make every atom match every cue -- a key that fires
# on everything is not a key, which `fits` already recorded happening once at 87.3%.
TYPE_TAGS: dict[str, tuple[str, ...]] = {
    "POSITION": ("POSITION",),
    "EXTENT": ("EXTENT",),
    "COLOUR": ("COLOUR",),
    "SHAPE": ("SHAPE",),
    "DELTA": ("CHANGE", "DIRECTION", "SPEED"),
}


@cache
def atom_tags(name: str, in_type: str, out_type: str) -> frozenset[str]:
    """An agent atom's tags, from its TYPES plus `observer._MUT_ATTR`.

    The types alone lose which delta is which -- `drow` and `dh` are both `OBJECT -> DELTA` --
    and the observer already drew that split for perception (`drow` is position, `dh` is
    extent). Read off that table rather than off the atom's name, so a `d`-prefix convention
    is never parsed.
    """
    out: set[str] = set()
    for t in (in_type, out_type):
        out.update(TYPE_TAGS.get(str(t), ()))
    try:
        import observer
        attr = observer._MUT_ATTR.get(name) or observer._HEAVY_MUT.get(name)
    except Exception:
        attr = None
    if attr:
        out.update(CUE_TAGS.get(attr, ()))
    return frozenset(out)


def affinity(tags: frozenset[str], want: dict[str, float]) -> float:
    """HOW MUCH THE CUE FAVOURS AN ATOM, IN `[0, 1)` -- A TIE-BREAK AND NEVER A REORDERING.

    **THE BOUND IS DERIVED, NOT CHOSEN.** `retrieval.fits` returns an INTEGER in 0..5, so the
    smallest gap between two distinct fits is 1; anything strictly below 1 can therefore only
    separate candidates that `fits` scored EQUAL. That matters because `fits` is degenerate
    most of the time -- its own docstring records the key collapsing onto arity at 87.3% -- so
    the ties are where nearly all the ordering actually happens, and today they are broken by
    registry order, which `enumerate_closure` calls *an accident*.

    `x / (1 + x)` is monotone and bounded by construction, so no cutoff is picked.

    IT CANNOT EXCLUDE. `enumerate_closure` orders its start set and admits everything; an atom
    the cue never mentions scores 0.0 and is tried last rather than not at all.
    """
    if not tags or not want:
        return 0.0
    x = sum(w for t, w in want.items() if t in tags)
    return x / (1.0 + x)


def term_affinity(term: Any, want: dict[str, float]) -> float:
    """`affinity` over a whole chain -- the UNION of its atoms' tags, not the sum.

    Union rather than sum because a longer chain would otherwise outscore a shorter one for
    being longer, which is a length preference wearing a relevance score's clothes. The
    bargain already prices length, and pricing it twice in opposite directions is how a
    mechanism ends up arguing with itself.
    """
    tags: set[str] = set()
    for a in getattr(term, "atoms", ()) or ():
        tags |= atom_tags(a.name, str(a.in_type), str(a.out_type))
    return affinity(frozenset(tags), want)


def _tag_score(key: str, tag: str) -> float:
    """The entry's OWN WEIGHT for this tag, or a neutral 0.5 where it declares none.

    **`weight`, NEVER `score` -- the reviewer's ruling of 2026-09-27 and this file read the
    wrong field first.** The README: *order by `weight`, not `score`: raw scores grow with how
    many attributes an entry was written with.* A raw score therefore ranks VERBOSE entries
    above apt ones, which is a property of how the corpus was authored rather than of the
    board. `weight` is `score / (1 + the entry's total)`, bounded in [0,1) and comparable
    across entries -- the same squashing `affinity` below arrived at independently.

    THE DEFAULT IS 0.5 AND NOT 1.0, because weights are now bounded by 1. Under the old raw
    scores a default of 1.0 was unremarkable; against weights it would rank every UNSCORED
    entry above almost every scored one. **Changing the field without changing the default
    would have silently inverted the ranking** -- 169 of 1,748 atoms carry no `scored` list.
    0.5 is the midpoint of the bounded range: present, unranked, neither favoured nor dropped.
    """
    e = entry(key) or {}
    for row in (e.get("tags") or {}).get("scored") or ():
        if row.get("tag") == tag:
            w = row.get("weight")
            return float(w) if w is not None else 0.5
    return 0.5


def _tier(key: str) -> int:
    """Tier as a TIE-BREAK, so what the agent can actually compute today comes first among
    equals. Untiered sorts last and is still returned."""
    t = (entry(key) or {}).get("reach_tier")
    return int(t) if isinstance(t, (int, str)) and str(t).isdigit() else 9
