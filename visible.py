"""3a. THE VISIBLE SET — a TERM may be visible without being held.

**THE RULING, 2026-08-27.** All possible priors exist already; a frame is a slice of one. An
organism does not compose its priors — it inherits them and expresses what the environment
triggers. So the seed needs **access** to everything possible, because the terrain, the actors
and the selection pressure are all unknown and reactivity is the whole point.

> **But access is not possession**, and that distinction is what §11 and §23.2 were both
> reaching for with one word.

**§11 IS UNTOUCHED.** Nothing enters Γ except under *the loop cannot run without it* or *the
agent minted a crude version first and we are promoting it*. At start neither applies to a
TERM, **so no TERM enters.** §23.2's *load generously* becomes **populate the visible set
generously**. Visibility is not entry, so there is no third clause and the entry rule is not
weakened.

**NOT CALLED A CATALOGUE, AND THE NAME MATTERS.** §14.7 uses `catalogue` for the FAILURE:
*a library that grows and is never reused is a catalogue, and a catalogue is what "the agent
is composing" looks like when it is not.* **This is the structural opposite** — that one is
HELD BUT NEVER USED, inside Γ; this one is VISIBLE BUT NEVER HELD, outside it. Naming it
`catalogue` would have made the ruling read as the failure mode described approvingly.

**WHAT AN ENTRY CONTAINS, AND WHAT IT DELIBERATELY OMITS.** `never content` is the clause that
keeps this from being seeding under another name:

    kind                 what family of thing this is
    affordance           what it WOULD do, as predicates -- aimable, not executable
    provenance           a summary: where it came from, not how it works
    holders              how many agents earned it -- a population fact, not a hint

    NEVER: the composition, the atom chain, the parameters, the implementation.
           An entry says a capability EXISTS and what it would achieve. It does not say how.

**AIMING** is adopting an entry's affordance predicates as a goal hypothesis. The agent sees
that a capability exists and what it would do, **and cannot execute it.**

**EARNING** is regenerating the entry's mastery pattern under ablation. Only then does it
enter that agent's Γ — **under §11 clause two, promoted from a crude version the agent minted
first**, which `gamma`'s admitting-clause field already records.

**AND THE COMPOSITION CLAIM SURVIVES EXACTLY.** Every term the agent holds, it built or
promoted. An entry it never earned was never held, **so there is nothing to wipe and nothing
to distinguish** — the ablation problem shrinks rather than being managed.

UNVERIFIED AGAINST ITS SOURCE. The four fields are the ruling's. The earlier architecture
material that specifies this structure is **not in `docs/` and was not read**, so anything it
adds beyond these four is unchecked here rather than contradicted.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass

sys.dont_write_bytecode = True


@dataclass(frozen=True)
class Entry:
    """Visible, never held. **No field carries the composition.**"""

    name: str
    kind: str
    affordance: tuple[str, ...]     # what it WOULD do. Aimable, not executable.
    provenance: str
    holders: int = 0

    def aim(self) -> dict:
        """Adopt the affordance predicates as a goal hypothesis. Returns no mechanism."""
        return {"aiming_at": self.name, "kind": self.kind,
                "predicts": list(self.affordance), "holds": False,
                "reads": "a goal hypothesis, not a term -- nothing here can be applied"}


class VisibleSet:
    """Populated generously. **Nothing here is in Γ, and nothing here can be executed.**"""

    def __init__(self, entries: list[Entry] | None = None) -> None:
        self._e: dict[str, Entry] = {}
        for e in entries or []:
            self._e[e.name] = e
        self.earned: set[str] = set()

    def add(self, e: Entry) -> None:
        self._e[e.name] = e

    def visible(self) -> list[str]:
        return sorted(self._e)

    def aimable(self, kind: str | None = None) -> list[Entry]:
        return [e for e in self._e.values() if kind is None or e.kind == kind]

    def earn(self, name: str) -> dict:
        """The agent regenerated this entry's pattern. **Now it may enter Γ, under clause
        two** — and the caller does the entering, because this object never holds terms."""
        e = self._e.get(name)
        if e is None:
            return {"earned": False, "why": "not visible"}
        self.earned.add(name)
        return {"earned": True, "name": name, "admit_under": "promoted",
                "reads": "regenerated under ablation, so it enters as a promotion of what "
                         "the agent minted crudely -- never as a load"}

    def report(self) -> dict:
        return {"visible": len(self._e), "earned": len(self.earned),
                "held_without_earning": 0,
                "reads": "visible is not held; an unearned entry was never in Gamma, so "
                         "the ablation has nothing to distinguish"}


def seed_from(priors: dict) -> VisibleSet:
    """Every loadable row, made VISIBLE rather than held.

    The affordance is the catalogue's own operational statement — **what it would do** — and
    the composition that would achieve it is exactly what is not here.
    """
    out = VisibleSet()
    for shape, rows in priors.items():
        for p in rows:
            out.add(Entry(p.name, shape, (p.statement,), p.citation))
    return out
