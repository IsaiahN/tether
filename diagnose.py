"""3a DIAGNOSE (Isaiah 2026-10-17 03:37 "the design of step 3a (contradiction scenario) is settled",
04:59 "per spot, per kind and per actor ... several things around the board at once"; the reviewer's
PART 2c and 05:00/05:01 amendments). When a settled or innate expectation is contradicted, the agent
does not blame its reading by reflex: it asks, in order, whether there is a fact here (noise), when
the term last held (recall), whether its own act slipped, whether the world changed in the gap (or
the thing simply moved), whether its own acts in a different order explain it, and only then
whether the reading was weak. Each verdict is a recorded, reversible row; nothing is removed.

Pure: the agent hands in its rows and readers; this module holds no agent state. `Hazard` is the
learned prior -- world changes per SPOT, per KIND and per ACTOR, and own slips/orders per spot and
kind, each kept apart and never averaged (Fig 1 :19, :22). It reads only the agent's own verdicts,
never a game tag.
"""
from __future__ import annotations

import sys
from collections import Counter
from collections.abc import Callable

sys.dont_write_bytecode = True

UNSEEN = "unseen"          # the hidden hand: a change with no candidate actor (Saxe et al. 2005)


class Hazard:
    """The three world-change counts and the own-act counts, kept apart, plus actor trust."""

    def __init__(self) -> None:
        self.world = {"spot": Counter(), "kind": Counter(), "actor": Counter()}
        self.own = {"spot": Counter(), "kind": Counter()}
        self.near: Counter = Counter()   # unexplained changes with the actor in the gap
        self.away: Counter = Counter()   # unexplained changes with the actor absent

    def credited(self, actor: str, min_repeat: int) -> bool:
        """Trusted as a cause only after MIN_REPEAT co-occurring unexplained changes AND more of
        them near it than without it (the reviewer 05:01): a bystander is never blamed for one
        coincidence. Before that it is a candidate, ranked and reversible (Fig 9 :41)."""
        return self.near[actor] >= min_repeat and self.near[actor] > self.away[actor]

    def world_first(self, spot: str, kind: str, actors) -> bool:
        """D3 before D2 when this object's HIGHEST world count passes its slip+order count: the
        opponent end of the range; at zero the own-act checks run first (the cube end)."""
        hw = max(self.world["spot"][spot], self.world["kind"][kind],
                 max((self.world["actor"][a] for a in actors), default=0))
        return hw > self.own["spot"][spot] + self.own["kind"][kind]


def diagnose(rows: list, slot: str, owner: str, *, persists: bool,
             predicts: Callable[[tuple], bool],
             predicts_with: Callable[[tuple, str], bool],
             alt_predicts: Callable[[tuple], bool],
             changed_of: Callable[[int], set], touching_now: set, kind: str,
             kind_of: Callable[[str], str], moved_to: Callable[[object], str | None],
             hazard: Hazard, min_repeat: int, gap_cap: int = 8,
             own_reach: Callable[[int], bool] = lambda _i: False,
             own_owners: Callable[[int], set] = lambda _i: set(),
             owner_moved: Callable[[int], bool] = lambda _i: False) -> dict:
    """One contradiction on `slot` (owned by `owner`), diagnosed. `rows`: the slot's trace rows in
    order, each (i, before, action, after, aim, landed) -- aim the object the act was meant for,
    landed the one the press landed on (None where unknown). Readers: `predicts(row)` the
    contradicted term was right on that row; `predicts_with(row, action)` the same with another
    action; `alt_predicts(row)` some other held term was right; `changed_of(i)` the owners that
    changed in transition i; `moved_to(value)` another object of the same canonical form now
    holding the remembered value on the same attribute, or None. `own_reach(i)`: the own act of
    transition i reached the slot without aiming at its owner -- through a relation to something
    the act moved (Fig 11 :43, the contact cascade); `own_owners(i)`: what the own act moved in
    transition i (the agent's body and what derives from it), never an actor candidate (Fig 5 :12,
    mis-attached: our own act through a relation is not another actor); `owner_moved(i)`: the
    slot's owner changed its own non-derived slots in transition i (it moved itself). Own reach
    makes our act a candidate that cannot be ruled out, never a bar on the world (Fig 9 :60): a
    reached row where the owner also moved itself is a COMPOUND, credited to both (the reviewer
    09:20; Isaiah 04:59). Returns the verdict row."""
    out = {"at": slot, "kind": kind}      # "at": the ledger's own `slot` is the row's key
    if not persists:                                                     # D0 NOISE
        return {**out, "verdict": "noise", "next_probe": None,
                "evidence": "the miss does not persist: one observation is a coincidence"}
    held = [k for k, r in enumerate(rows) if predicts(r)]                # D1 RECALL
    if not held:
        return {**out, "verdict": "never_held", "next_probe": "the existing route",
                "evidence": "no row where the term predicted right"}
    k_last = held[-1]
    gap = rows[k_last + 1:][-gap_cap:]
    if not gap:
        return {**out, "verdict": "undiagnosed", "next_probe": None,
                "evidence": "the term held on the latest row: no gap to read"}
    reached = [r[0] for r in gap if owner not in (r[4], r[5]) and own_reach(r[0])]
    aimed = [r for r in gap if owner in (r[4], r[5])]
    own_rows = aimed + [r for r in gap if r[0] in reached]
    compound = [i for i in reached if owner_moved(i)]
    # actor candidates: the objects that CHANGED in the gap (moved, recoloured, ...), the agent's
    # own targets aside; a motionless bystander is never one, whatever it touches (an enabling
    # condition is part 2's constant, not an actor). Contact is recorded beside them, not counted
    cands = set()
    for r in gap:
        cands |= changed_of(r[0]) - own_owners(r[0])
    cands -= {owner} | {r[5] for r in gap if r[5]} | {r[4] for r in gap if r[4]}
    if compound:
        cands.add(owner)      # it moved itself: the actor of its own relational change
    actors = sorted({kind_of(c) for c in cands}) or [UNSEEN]
    order = ("D3", "D2") if hazard.world_first(slot, kind, actors) else ("D2", "D3")
    changed_in_gap = any(r[1].get(slot) != r[3].get(slot) for r in gap)
    out.update(t_last=rows[k_last][0], gap=len(gap), order="".join(order), actors=actors,
               near=sorted(kind_of(c) for c in cands & set(touching_now)))
    if reached:
        out["own_reach"] = reached     # own rows through a relation, not by aim
    for d in order:
        if d == "D2":                                                    # D2 OWN ACT (slip)
            slip = [r[0] for r in gap
                    if r[4] is not None and r[5] != r[4] and owner in (r[4], r[5])]
            if slip:
                hazard.own["spot"][slot] += 1
                hazard.own["kind"][kind] += 1
                return {**out, "verdict": "slip", "rows": slip,
                        "next_probe": "repeat the intended act",
                        "evidence": "right intention, wrong execution: the press landed elsewhere"}
        elif not aimed and (not reached or compound) and changed_in_gap:  # D3 WORLD CHANGE
            for a in actors:
                hazard.near[a] += 1
            for a in list(hazard.near):
                if a not in actors:
                    hazard.away[a] += 1
            credited = [a for a in actors if a != UNSEEN and hazard.credited(a, min_repeat)]
            hazard.world["spot"][slot] += 1
            hazard.world["kind"][kind] += 1
            for a in credited or [UNSEEN]:
                hazard.world["actor"][a] += 1
            scopes = ["spot", "kind"] + (["actor"] if credited else [])
            if compound:                     # own act through the relation AND the world
                hazard.own["spot"][slot] += 1
                hazard.own["kind"][kind] += 1
                return {**out, "verdict": "compound", "rows": compound, "scopes": scopes,
                        "credited": credited, "stale": True, "closed_at": rows[k_last][0],
                        "next_probe": ("watch the actor; re-observe what it reached" if credited
                                       else "re-observe the slot before betting on memory"),
                        "evidence": "the own act reached the slot through a relation and its "
                                    "owner moved itself: credited to both"}
            to = moved_to(rows[k_last][3].get(slot))
            if to is not None:
                return {**out, "verdict": "moved", "from": owner, "to": to, "scopes": scopes,
                        "credited": credited, "stale": True,
                        "next_probe": "re-observe what the actor reached" if credited
                        else "re-observe the slot before betting on memory",
                        "evidence": "an object of the same canonical form now holds the value"}
            return {**out, "verdict": "world_changed", "scopes": scopes, "credited": credited,
                    "stale": True, "closed_at": rows[k_last][0],
                    "next_probe": ("watch the actor; re-observe what it reached" if credited
                                   else "re-observe the slot before betting on memory"),
                    "evidence": "the value changed in the gap and no own act touched it"}
    if own_rows:                                                         # D4 REPLAY
        if predicts(gap[-1]):
            return {**out, "verdict": "stale_expectation", "next_probe": "refresh and bet again",
                    "evidence": "the term holds on the latest board: the expectation was old"}
        if len(gap) >= 2 and predicts_with(gap[-1], gap[-2][2]) and predicts_with(gap[-2],
                                                                                  gap[-1][2]):
            hazard.own["spot"][slot] += 1
            hazard.own["kind"][kind] += 1
            return {**out, "verdict": "order", "swap": [gap[-2][0], gap[-1][0]],
                    "next_probe": "repeat the intended acts in their order",
                    "evidence": "the last two acts, swapped, are what the term predicts"}
        failing = [r for r in gap if not predicts(r)]
        if failing and all(alt_predicts(r) for r in failing):
            return {**out, "verdict": "scope", "next_probe": "split the scope (two scopes)",
                    "evidence": "another known term holds where this one failed"}
        if failing and not any(alt_predicts(r) for r in failing):
            return {**out, "verdict": "model_too_small", "next_probe": "the outward/mint route",
                    "evidence": "no known term reaches what was observed"}
    if any(r[1].get(slot) is None for r in gap):                         # D5 READING
        return {**out, "verdict": "reading", "next_probe": "perception's remedy (resolve)",
                "evidence": "the reading was weak in the gap"}
    return {**out, "verdict": "undiagnosed", "next_probe": None,
            "evidence": "D0-D5 leave it unexplained: kept as a residual, never a guess"}
