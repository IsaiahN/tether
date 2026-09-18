"""Atoms as DETECTORS (Isaiah, `TRAINING_PLAN.md` §13; `ATTRIBUTES.md`): every closure atom carries
a boolean CONDITION that confirms it (`Movement` ⟺ position changed; `Solidity` ⟺ overlapArea==0).
`ATTRIBUTES.md` records these as PROSE ("they are written as prose and they are the quantity"); this
encodes them as PREDICATES over the mutation vector the observer/reverse_engineer already produce,
for the atoms the mapping targets. A mutation re-fires the conditions; the atoms whose condition
CONFIRMS are the lit ones -- a check against the board, not a lookup handed to the agent.

This makes `reverse_engineer`'s imperative statement-building declarative: a new atom is admitted by
NAMING its condition here, not by editing branching code. The condition and recipe are the closure's
own (`ATOMS.md`); nothing is invented.

§12.3 / CUE_BOUNDARY: a CUE module (it lights candidate atoms for retrieval), never imported by the
betting path -- enforced by conform/lint.py, which lists `detectors` among the cue modules.
"""

from __future__ import annotations

import sys

import sensors_heavy

sys.dont_write_bytecode = True

# Per-object change effect keys (reverse_engineer._match): drow dcol dh dw dcells recolour.
# Each atom's CONDITION is a predicate over one such effect; recipe is the ATOMS.md derivation.
# `_pos`/`_ext`/`_shp`/`_col` name which attribute changed, so the condition reads like the prose.

def _pos(e: dict) -> bool: return bool(e.get("drow") or e.get("dcol"))
def _ext(e: dict) -> bool: return bool(e.get("dh") or e.get("dw"))
def _shp(e: dict) -> bool: return bool(e.get("dcells")) or bool(e.get("dshape"))
def _col(e: dict) -> bool: return bool(e.get("recolour"))


# atom -> (recipe, condition). Order is checked-most-specific-first only where two could co-fire on
# one effect; independent attributes light independently (an object may translate AND recolour).
OBJECT_ATOMS = {
    "Translate": ("Ct + Co",              lambda e: _pos(e) and not (_ext(e) or _shp(e))),
    "Scale":     ("Frac + Scale",         _ext),
    "Deform":    ("Ge + Gs | Ge + Chirality", lambda e: _shp(e) and not _ext(e)),
    "Recolour":  ("Co + Featural identity", _col),
}

# Frame-level population atoms: the condition is over the appeared/vanished counts.
POPULATION_ATOMS = {
    "Construct": ("Rep + Bind",              lambda van, app: app and not van),
    "Erase":     ("Contact + Consumed",      lambda van, app: van and not app),
    "Separate":  ("Decompose + Co",          lambda van, app: van and app and app > van),
    "Merge":     ("Amalgamate + Med miscible", lambda van, app: van and app and van > app),
}


# Tier-1 PRIMITIVE detectors the heavy sensors now confirm -- the condition is the closure atom's
# OWN (ATOMS.md/ATTRIBUTES.md), wired to sensors_heavy, nothing invented. `To` "inside/outside/
# holes"; `Sym` "unchanged under reflection"; `Contain` "a thing held inside a boundary"; `Adj`
# "two things co-occurring in space"; `So` (frame-level, light_frame) "two cannot occupy one place".
def _symmetric(o: dict) -> bool:
    """Sym: a cell set unchanged under reflection across its own axis (the checkable case of
    'unchanged under reflection, rotation or translation')."""
    cells = {tuple(c) for c in o.get("cells", [])}
    if not cells:
        return False
    rs = [r for r, _ in cells]
    cs = [c for _, c in cells]
    r0, r1, c0, c1 = min(rs), max(rs), min(cs), max(cs)
    horiz = {(r0 + r1 - r, c) for r, c in cells}
    vert = {(r, c0 + c1 - c) for r, c in cells}
    return cells in (horiz, vert)


STATIC_ATOMS = {
    "Topology": ("To",      lambda o: sensors_heavy.scalar(o)["holes"] > 0),
    "Symmetry": ("Sym",     _symmetric),
}
RELATION_ATOMS = {
    "Contain":   ("To + So", lambda r: bool(r["contains"])),
    "Adjacency": ("Adj",     lambda r: r["contactPoints"] > 0),
}


def light_static(o: dict) -> list[dict]:
    """The per-object primitive atoms the heavy sensors confirm on one object (a topology carries
    holes) -- corpus-stated conditions wired to sensors_heavy."""
    return [{"atom": a, "recipe": r} for a, (r, cond) in STATIC_ATOMS.items() if cond(o)]


def light_relation(a: dict, b: dict) -> list[dict]:
    """The per-pair primitive atoms the heavy relation confirms (a holds b inside; a touches b)."""
    rel = sensors_heavy.relation(a, b)
    return [{"atom": at, "recipe": rc} for at, (rc, cond) in RELATION_ATOMS.items() if cond(rel)]


def light_frame(objs: list[dict]) -> list[dict]:
    """Frame-level primitive atoms: Solidity (So) holds when no two objects occupy one place --
    ATTRIBUTES.md's verbatim condition, `overlapArea == 0` for every pair."""
    for i, a in enumerate(objs):
        for b in objs[i + 1:]:
            if sensors_heavy.relation(a, b)["overlapArea"] > 0:
                return []
    return [{"atom": "Solidity", "recipe": "So"}]


def light_object(effect: dict) -> list[dict]:
    """The atoms whose per-object condition confirms on this change effect. Independent attributes
    light independently, so a compound change (move + recolour) lights both."""
    return [{"atom": a, "recipe": r} for a, (r, cond) in OBJECT_ATOMS.items() if cond(effect)]


def light_population(vanished: int, appeared: int) -> list[dict]:
    """The population atom the count direction confirms; empty for an equal exchange (ambiguous)."""
    return [{"atom": a, "recipe": r} for a, (r, cond) in POPULATION_ATOMS.items()
            if cond(vanished, appeared)]


def light(effects: list[dict], vanished: int = 0, appeared: int = 0) -> dict:
    """The full lit set for one frame->next: per-object atoms from each change effect, plus the
    population atom from the counts. The mutation directs the search; these are what it lights."""
    obj = []
    for e in effects:
        if e.get("kind") == "change":
            obj.extend(light_object(e))
    return {"object": obj, "population": light_population(vanished, appeared)}


if __name__ == "__main__":
    import json

    import arc_percept
    from reverse_engineer import _match, load_replay
    steps = load_replay("replays/ls20_human.ndjson")
    frames = [arc_percept.components(s["grid"]) for s in steps]
    hist: dict = {}
    for a, b in zip(frames, frames[1:], strict=False):
        effs = _match(a, b)
        van = sum(1 for e in effs if e["kind"] == "vanish")
        app = sum(1 for e in effs if e["kind"] == "appear")
        lit = light(effs, van, app)
        for d in lit["object"] + lit["population"]:
            hist[d["atom"]] = hist.get(d["atom"], 0) + 1
    print(json.dumps(hist, indent=1))
