"""What a term has DONE, read from the ledger. **Nothing is accumulated; this is a query.**

`[I]` *"Step 5's outcome is written to the term, not accumulated on it. A term settles once and
is used many times. The settle is recorded; the using is not. So the library holds what a term
IS and nothing about how it has BEHAVED."*

**AND THE USING IS RECORDED AFTER ALL — every bet row carries `bound`, `mass` and `cause`, per
slot, per step.** So the four questions were answerable before this file existed and nothing
asked them. **Four counters on `Term` would have been a SECOND PRODUCER of a fact the ledger
already holds**, which is A1's shape at the level of a record and would have looked like a
feature.

**THE UNIT IS THE (TERM, SLOT) PAIR, RULED, and the reason is the hard rule.** The loop's event
is the slot-step; *R is indexed per object slot, and averaging is how a live signal
disappears*. **A term-level held/failed total is a sum over slots of readings of R** -- the
construction `sim_fidelity` was refused for and `_last_mass` was wrong for. So there is no
term-level count here, and **that is a limit on the reading rather than a loss of the
question.**

*(§14.7's `chunk reuse count` IS term-level and does not conflict: it counts how often a term
appears as a CONSTITUENT of a later mint -- a composition event, not a reading of R. The hard
rule is about R.)*

**THE FOURTH QUESTION NEEDS THE THIRD STATE, and the row already carries it.** *Applied and
wrong is a different state from did not apply.* `mass == 0` with `cause == genuine` is a term
that predicted and was right; `mass == 0` with `channel_closed` is **the slot owing and this
step reading zero** -- did-not-deliver, and counting it as a hold would be the two-state
collapse in the field that measures holding.

**AND `Standing` CANNOT ANSWER THIS, WHICH IS WHY THE LEDGER DOES.** `refute()` sets
`settled_at = None`, so *held then failed* and *never held here* are the same object in memory.
**The rows survive with their cycles**, so the arc is recoverable from the record even though
it is gone from the term.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass

sys.dont_write_bytecode = True

GENUINE = "genuine"


@dataclass
class Pair:
    """One (term, slot). **The four, and never summed with another pair's.**"""

    term: str
    slot: str
    called: int = 0
    held: int = 0
    failed: int = 0
    no_delivery: int = 0          # applied to a slot that owed and read zero
    settled_at: int | None = None
    demoted_at: int | None = None
    last_held: int | None = None
    last_failed: int | None = None

    @property
    def arc(self) -> int | None:
        """First settle to first failure. `None` while either end is missing."""
        if self.settled_at is None or self.demoted_at is None:
            return None
        return max(0, self.demoted_at - self.settled_at)

    def reading(self) -> str:
        """**The disposition, and it is the point of the four.**

        *Held whenever it applied* is a mechanism. *Held rarely* is a lucky fit. **Held
        consistently and then stopped is a term THE ROOM INVALIDATED** -- the staleness signal,
        and the reading nothing computed before. The failure is then a claim about the room
        rather than about the term.
        """
        if not self.called:
            return "never-called"
        if self.held and self.last_failed is not None and (
                self.last_held is None or self.last_failed > self.last_held):
            return "held-then-stopped" if self.held > 1 else "closed-once-then-failed"
        if self.held and not self.failed:
            return "holds"
        if self.failed and not self.held:
            return "never-held"
        return "mixed"


def read(rows: list[dict]) -> dict[tuple[str, str], Pair]:
    """One pass over the ledger. **Nothing here writes, and nothing sums across slots.**"""
    out: dict[tuple[str, str], Pair] = {}

    def pair(term: str, slot: str) -> Pair:
        return out.setdefault((term, slot), Pair(term=term, slot=slot))

    for r in rows:
        d = r.get("detail") or {}
        ev, slot, cyc = r.get("event"), r.get("slot"), r.get("cycle")
        if ev == "bet" and d.get("bound") and slot:
            p = pair(d["bound"], slot)
            p.called += 1
            mass = d.get("mass")
            if mass is None:
                continue
            if mass > 0:
                p.failed += 1
                p.last_failed = cyc
            elif d.get("cause") == GENUINE:
                p.held += 1
                p.last_held = cyc
            else:
                p.no_delivery += 1      # NOT a hold: the slot owed and read zero
        elif ev in ("settle", "demote"):
            asked = d.get("asked") or []
            term = d.get("term") or (asked[0] if asked else None)
            s = (asked[1] if len(asked) > 1 else slot)
            if not term or not s:
                continue
            p = pair(term, s)
            if ev == "settle" and p.settled_at is None:
                p.settled_at = cyc
            elif ev == "demote" and p.demoted_at is None:
                p.demoted_at = cyc
    return out


def report(rows: list[dict]) -> dict:
    """Dispositions, counted. **The count is over PAIRS, never over terms.**"""
    pairs = read(rows)
    kinds: dict[str, int] = {}
    for p in pairs.values():
        k = p.reading()
        kinds[k] = kinds.get(k, 0) + 1
    stale = [f"{p.term}@{p.slot}" for p in pairs.values()
             if p.reading() == "held-then-stopped"]
    return {"pairs": len(pairs), "dispositions": kinds,
            "arcs": {f"{p.term}@{p.slot}": p.arc
                     for p in pairs.values() if p.arc is not None},
            "room_invalidated": stale,
            "reads": ("per (term, slot); no term-level totals, because held and failed are "
                      "readings of R and R is indexed per slot. `held-then-stopped` is a "
                      "claim about the ROOM, not about the term")}
