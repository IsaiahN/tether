"""§16.5 — habitat enumeration, and it EMITS RESIDUALS rather than goals.

Figure 11, quoted because the procedure is the specification:

    List everything in contact with the residual, then what is in contact with those, and
    outward until the cascade stops mattering. **You do not invent the list. You read it off
    the world**, and what you cannot perceive or measure yet is the residual.

**THE POINT IS THE LAST CLAUSE.** A residual reaches the loop by one route today -- something
was bet on and the bet was wrong -- so the only gaps it can work on are gaps in things it
already models. **A relation is not a slot**, so `contains`, `touches`, `blocks` cannot be bet
on, cannot be wrong, and cannot produce a residual. **This opens that door from the other
side: not by making relations bettable, but by making the INABILITY TO REPRESENT THEM the
thing that gets recorded.**

**ITS FALSIFIER IS §16.7's TRAP, AND IT IS STATED BEFORE THE FIRST RUN.** *Building a case for
what it believes to be true about its purpose* is objective abduction, and the measured history
is `abduced=[]` on most games. The corpus's fix: *discovering the objective = minting the φ
that explains the residual*, on Figure 3's ordering -- perception, then vocabulary, then
objective -- and ***a module that jumps to the third is a reading taken below the break.***

> **This emits residuals or it stops.** Nothing here returns a goal, a target, a preference or
> a ranking of outcomes. If it ever does, it is objective abduction wearing a perception
> layer's name.

**ONE RELATION OF THE FOUR, AND THE OTHERS ARE REPORTED RATHER THAN SUBSTITUTED.** §16.5's
relations column names contact, containment, precondition, and correlate-with-my-action:

    contact                   BUILT -- sensor 8, Tier 1
    containment               TIER 2. §12.3: `inside` composes from position and extent, and
                              *they are Tier 2 and the agent should have to reach for them*.
                              Hardcoding it here would delete the evidence the composition
                              system works, which is the same rule that forbids loading it
    precondition              loop-side -- §16.1's lattice, not perception's to compute
    correlate-with-my-action  loop-side -- needs the action history

**THE STOPPING RULE IS PRAGMATIC AND SAYS SO.** Ruled: *no new relation type in the next
ring.* `PHILOSOPHY` §16 -- *the enumeration runs outward until the cascade stops mattering,
**which is a pragmatic bound and says so***; `THE_FORMULA` -- ***never a completeness claim***;
step 8 -- *the loop has no convergence criterion by construction.* **A rule that LOOKED
principled would be the more dangerous choice**, because it invites exactly the completeness
reading the corpus forbids.

**AND IT LEAVES A TRACE, which is what the type-novelty rule lacked on its own.** The report
carries the relation TYPES seen and the RING at which the set stopped growing, so the stop is
auditable from the record rather than only correct in the moment.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Any

import arc_percept as P

sys.dont_write_bytecode = True

PRAGMATIC = ("a pragmatic bound, never a completeness claim: the cascade stopped adding "
             "relation TYPES, which is not a statement that nothing further exists")


@dataclass
class Habitat:
    """What was read off the world. **No goals, no targets, no preferences.**"""

    seed: str
    rings: list[list[str]] = field(default_factory=list)
    relations: list[tuple[str, str, str]] = field(default_factory=list)
    types_seen: list[str] = field(default_factory=list)
    stopped_at: int = 0
    stop_reason: str = ""

    def residuals(self) -> list[dict]:
        """**EVERY RELATION IS A RESIDUAL, because no relation has a slot.**

        This is the direction clause made mechanical -- *what you cannot perceive or measure
        yet is the residual*. The agent can SEE that these hold and has no way to represent
        them, so each is recorded as unexplained rather than discarded as unmodellable.
        """
        return [{"kind": k, "between": (a, b), "representable": False,
                 "why": "a relation is not a slot, so it cannot be bet on or be wrong"}
                for k, a, b in self.relations]

    def report(self) -> dict:
        return {"seed": self.seed, "rings": len(self.rings),
                "actors": sum(len(r) for r in self.rings),
                "relations": len(self.relations), "types": self.types_seen,
                "stopped_at_ring": self.stopped_at, "stop_reason": self.stop_reason,
                "residuals_emitted": len(self.relations), "goals_emitted": 0,
                "bound": PRAGMATIC}


def _rtype(obj: dict, aff: Any) -> str:
    """A relation's TYPE: contact, qualified by the contacted object's affordance profile.

    §16.5's actors column is *objects, **with affordance profiles** (§16.4)*, so the profile
    is part of the habitat rather than an addition to it. **Read by behaviour under contact,
    never by substance** -- §16.4 is explicit that a taxonomy of blob-kinds is the archetype
    trap wearing a perception costume.

    **THREE STATES, NOT TWO, AND THE FIRST VERSION CONFLATED THE LAST TWO.** `Affordances`
    keeps `None` distinct from `False` *for the same reason `unreached` is kept distinct from
    `unreachable`*, and a type function that collapses them throws that away one layer up:

        `contact`              NO READER WIRED -- a fact about the build
        `contact:unobserved`   reader present, this kind never seen in contact yet
        `contact:inert`        READ, and it affords nothing
        `contact:blocks,...`   read, and these are what it affords

    **A sparse type set means different things in each case**, and only the first is a wiring
    defect. The second is the honest early state of a learned reading and resolves with play.
    """
    if aff is None:
        return "contact"                       # NO READER -- a WIRING state
    prof = aff.profile(obj)
    if all(v is None for v in prof.values()):
        return "contact:unobserved"            # reader present, never seen in contact
    on = sorted(k for k, v in prof.items() if v)
    return "contact:" + (",".join(on) if on else "inert")   # READ, and affords nothing


def enumerate_from(objects: dict[str, dict], seed: str, aff: Any = None) -> Habitat:
    """Outward from the seed along CONTACT, stopping when a ring adds no new relation type.

    Terminates without a cap because the object set is finite -- **a maximum-rings parameter
    would be the invented number the ruling ruled out**, and it is not needed.
    """
    h = Habitat(seed=seed)
    if seed not in objects:
        h.stop_reason = "seed not among the tracked objects"
        return h

    seen = {seed}
    ring = [seed]
    h.rings.append(ring)
    types: list[str] = []

    while ring:
        nxt: list[str] = []
        fresh = False
        for a in ring:
            for b, ob in sorted(objects.items()):
                if b in seen or not P.touching(objects[a], ob):
                    continue
                t = _rtype(ob, aff)
                h.relations.append((t, a, b))
                if t not in types:
                    types.append(t)
                    fresh = True
                seen.add(b)
                nxt.append(b)
        h.stopped_at = len(h.rings)
        if not nxt:
            h.stop_reason = "the cascade reached every object in contact"
            break
        if not fresh:
            # THE RULED STOP. The ring is discarded, not kept: it added no new TYPE, which
            # is the whole criterion -- keeping it would make the rule a formality.
            h.stop_reason = f"no new relation type in ring {len(h.rings) + 1}"
            break
        h.rings.append(nxt)
        ring = nxt

    h.types_seen = types
    return h
