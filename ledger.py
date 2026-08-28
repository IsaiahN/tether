"""The record. Append-only; every entry names its loop step.

The ledger is a reification: the loop's own state made available as data. That is why a
checker can read it without reading the machine, and why the checker can be domain-blind.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

# the eight loop steps. An entry that cannot name one is a defect, not a log line.
STEPS = ("PERCEIVE", "ROUTE", "MINT", "ACCEPT", "SETTLE", "PROMOTE", "IMPORT", "REPEAT")

# the three modes. Every run declares one.
GENERAL, SPECIFIED, GROUNDED = "general", "specified", "grounded"

# THE THREE CAUSES OF A LOW READING, and only two of them are about R stopping. The
# third is the permanent condition and its remedy is step 7 INWARD, so a zero that means
# "nothing to explain" and a zero that means "I could not see it" must not arrive as the
# same row.
#
# The checker declares these too, and that is not the double-loaded registry: a
# conformance checker and its subject are supposed to state the vocabulary separately,
# or the check is reading its own definition back. If either side renames one, A4 goes
# red, which is the drift being caught rather than prevented.
GENUINE, CHANNEL_CLOSED, SLICE_TOO_SMALL = "genuine", "channel_closed", "slice_too_small"

# WHAT A BET RESTS ON WHEN NOTHING IS BOUND. `idn` is a TERM -- an atom with a cost and a
# provenance; having no term is not, and writing the second as the first made a default look
# like a choice. `DOCTRINE_AUDIT` 8 named the defect before the reader hit it: *an unbound
# slot is predicted to not change -- a PERSISTENCE PRIOR, one of the six loadable shapes,
# applied invisibly: not stamped `prior`, not recorded as a choice, not falsifiable.*
#
# THE PREDICTION STILL FALLS BACK TO `idn` AND MUST. The loop has to predict something. What
# changes is the RECORD: the prediction needs a default, the record needs the difference.
NO_CHANGE = "no_change"

# 2e. THE FIVE ENDINGS, distinguished -- and the distinction is §19's episode half.
#
#   *"I ran out" is not "I was wrong" -- the same bug in two places.* The MINT half was fixed
#   at Phase 0d, splitting one `UNREACHED` into `no_support` / `not_novel` / `budget_spent` /
#   `depth_exhausted`. The EPISODE half is this: a run ending meant both *I hit the action
#   cap* and *the world killed me*. **In both cases a resource exhaustion was being reported
#   as a verdict about the world**, which is Figure 9's rule broken in the loop's own
#   reporting: never let a filter hand you a verdict.
WIN, DEATH, RESET, ADVANCE, CAP = "win", "death", "reset", "advance", "cap"

# §21.5: RESET and ADVANCE produce the SAME residual spike and mean OPPOSITE things, and the
# frame carries `full_reset` and `levels_completed` so the discriminator survives even where
# COMPETITION collapses the two events in the API's semantics.
ENDING_READS = {
    WIN: "the objective was met",
    DEATH: "the world ended the episode -- evidence about the world",
    RESET: "the next board is KNOWN, so a residual spike means THE MODEL IS WRONG. On a "
           "board already modelled a residual has no excuse",
    ADVANCE: "the next board is UNKNOWN by design, so a residual spike means NOTHING YET. "
             "Demoting here punishes the terms that carried the last level",
    CAP: "the seat's budget ran out. NOT a verdict about the world -- §19's episode half",
}


@dataclass(frozen=True)
class Entry:
    seq: int
    cycle: int
    step: str
    slot: str
    event: str
    detail: dict[str, Any] = field(default_factory=dict)
    # WHICH SLOTS A MAGNITUDE ON THIS ROW WAS DERIVED FROM. R is indexed per slot and
    # averaging across slots is how a live signal disappears, so a row carrying a
    # quantity has to say what the quantity is of -- and a row that says nothing cannot
    # be asked. Absent, not None, when the row carries no magnitude: the two readings
    # are `this row makes no claim` and `this row claims and will not say`.
    of: tuple[str, ...] | None = None


class Ledger:
    def __init__(self, path: str | Path | None = None, mode: str = SPECIFIED) -> None:
        if mode not in (GENERAL, SPECIFIED, GROUNDED):
            raise ValueError(f"unknown mode: {mode}")
        self.mode = mode
        self._entries: list[Entry] = []
        self._path = Path(path) if path else None
        if self._path is not None:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.write_text("", encoding="utf-8")

    def __len__(self) -> int:
        return len(self._entries)

    def record(self, cycle: int, step: str, slot: str, event: str,
               of: tuple[str, ...] | None = None, **detail: Any) -> Entry:
        if step not in STEPS:
            raise ValueError(f"entry names no loop step: {step!r}")
        e = Entry(len(self._entries), cycle, step, slot, event, detail, of)
        self._entries.append(e)
        if self._path is not None:
            with self._path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(self._row(e), sort_keys=True, default=str) + "\n")
        return e

    def _row(self, e: Entry) -> dict[str, Any]:
        d = {"mode": self.mode, **asdict(e)}
        if d.get("of") is None:
            d.pop("of", None)          # absent means "carries no magnitude", not "None"
        return d

    @property
    def entries(self) -> list[Entry]:
        return list(self._entries)

    def rows(self) -> list[dict[str, Any]]:
        """What the gate reads. Plain data, no objects from this module."""
        return [self._row(e) for e in self._entries]

    def by_event(self, event: str) -> list[Entry]:
        return [e for e in self._entries if e.event == event]
