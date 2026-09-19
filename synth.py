"""Composition -> board synthesizer: the inverse of the detector pipeline. Given target tier-1
primitives, place objects over a background field (larger than them, so `_actors` keeps them) so the
forward pipeline reads the target back. This is the durable form of the round-trip that caught six
perception bugs this session (see memory generator-roundtrip-audit) -- proctor-side, CUE-side,
lint-guarded out of the betting path.

It generates from the GENERAL library, never toward a public/private board. The CURRICULUM that
samples, orders and anneals compositions into a training schedule is a separate design
(TRAINING_PLAN 14, Isaiah's hunches) and is deliberately NOT decided here -- this is only the core
that any such curriculum would need.
"""

from __future__ import annotations

import sys

import arc_percept
import detectors
from reverse_engineer import _actors

sys.dont_write_bytecode = True

FIELD = 1  # the background field colour -- the largest component, which _actors drops


def _blank(h: int, w: int) -> list:
    return [[FIELD] * w for _ in range(h)]


def synthesize(targets: set) -> list:
    """A board whose non-field objects carry `targets` (static primitives). Incidental primitives
    may also fire -- a container is symmetric and holed -- which is honest, not a miss. `roundtrip`
    is how a caller checks the target is actually present."""
    g = _blank(6, 9)
    if "Contain" in targets or "Topology" in targets:
        for dr in range(3):  # a 3x3 ring at (1,1): Topology (a hole) + Symmetry
            for dc in range(3):
                if (dr, dc) != (1, 1):
                    g[1 + dr][1 + dc] = 2
        if "Contain" in targets:
            g[2][2] = 3  # a cell in the ring's hole
    if "Adjacency" in targets:
        g[1][6] = 4  # two 4-adjacent cells of different colour
        g[2][6] = 5
    if targets & {"Symmetry"} and not targets & {"Contain", "Topology", "Adjacency"}:
        g[1][4] = 2
        g[1][5] = 2  # a 1x2 block: symmetric, isolated
    return g


def roundtrip(targets: set) -> set:
    """Synthesize `targets`, run the forward pipeline (dropping the field as `_actors` does), and
    return the primitives that actually light. A caller asserts `targets <= roundtrip(targets)`."""
    objs = _actors(arc_percept.components(synthesize(targets)))
    got = {d["atom"] for d in detectors.light_frame(objs)}
    for o in objs:
        got |= {d["atom"] for d in detectors.light_static(o)}
    for a in objs:
        for b in objs:
            if a is not b:
                got |= {d["atom"] for d in detectors.light_relation(a, b)}
    return got


def synthesize_pair(target: str) -> tuple:
    """A (before, after) frame-pair whose ONE object exhibits `target` -- a mutation primitive
    (Translate/Scale/Recolour). The object stays small so it is never the largest component and the
    field is what `_match` drops; a Scale stays within SIZE_KEEP so the pair still matches."""
    before, after = _blank(6, 9), _blank(6, 9)
    for dr in range(2):  # a 2x2 block, colour 2, at (1,1) in both frames unless moved
        for dc in range(2):
            before[1 + dr][1 + dc] = 2
    if target == "Translate":
        for dr in range(2):
            for dc in range(2):
                after[1 + dr][4 + dc] = 2  # same block, moved right
    elif target == "Scale":
        for dr in range(2):
            for dc in range(3):
                after[1 + dr][1 + dc] = 2  # 2x2 -> 2x3 (ratio 4/6 >= SIZE_KEEP 0.5)
    elif target == "Recolour":
        for dr in range(2):
            for dc in range(2):
                after[1 + dr][1 + dc] = 6  # same block, colour 2 -> 6
    else:
        raise ValueError(f"no pair recipe for {target}")
    return before, after


def roundtrip_pair(target: str) -> set:
    """Synthesize the pair, run `_match` + the per-object detectors, return what lit."""
    from reverse_engineer import _match
    before, after = synthesize_pair(target)
    effs = _match(arc_percept.components(before), arc_percept.components(after))
    got: set = set()
    for e in effs:
        if e.get("kind") == "change":
            got |= {d["atom"] for d in detectors.light_object(e)}
    return got


if __name__ == "__main__":
    for tgt in ({"Topology"}, {"Contain"}, {"Adjacency"}, {"Symmetry"}, {"Contain", "Adjacency"}):
        got = roundtrip(tgt)
        print(f"{'ok ' if tgt <= got else 'MISS'} static {sorted(tgt)} -> {sorted(got)}")
    for t in ("Translate", "Scale", "Recolour"):
        got = roundtrip_pair(t)
        print(f"{'ok ' if t in got else 'MISS'} mutation target={t} -> lit={sorted(got)}")
