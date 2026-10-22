"""The record. Append-only; every entry names its loop step.

The ledger is a reification: the loop's own state made available as data. That is why a
checker can read it without reading the machine, and why the checker can be domain-blind.
"""

from __future__ import annotations

import atexit
import json
import sys
import weakref
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import armflag

sys.dont_write_bytecode = True

# R2, ONE HELD HANDLE (the reviewer 2026-10-17 17:58, 18:04): each row opened and closed the file
# (~12% of samples on lf52 with the asdict it drives). Now the path is opened once, at the first
# row, and FLUSHED after every row, so the loss window stays one row; closed at end_run and at
# exit; a write after a close reopens it. OFF: opened per row (011c8c8)
_LEDGER_HANDLE = armflag.arm("TETHER_LEDGER_HANDLE", default=True)
_OPEN: weakref.WeakSet = weakref.WeakSet()   # ledgers holding a handle, closed at exit

# the eight loop steps. An entry that cannot name one is a defect, not a log line.
# `PLAN` IS FIRST, AND THE WRITE ORDER DECIDED IT RATHER THAN A VIEW ABOUT COGNITION. The
# routine rows are emitted inside `choose`, which runs BEFORE `_utter` writes the bet's PERCEIVE
# row for the same slot -- and `gate.py` enforces non-decreasing step order per (cycle, slot).
# Any later position makes a real board fail the gate the first time a routine mints.
#
# It also reads correctly: the plan is formed from what is understood so far, the bet is the
# claim about what the planned action will do, and the residual comes back after it is taken.
STEPS = ("PLAN", "PERCEIVE", "ROUTE", "MINT", "ACCEPT", "SETTLE", "PROMOTE", "IMPORT", "REPEAT")

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
# THE TWO CLEARING WORDS NAME THEIR EVENT (Isaiah 2026-10-15 08:30; the reviewer 08:31): a game won
# is "game_win", a level cleared "level_advance". Before F1b they were the bare words "win" and
# "advance", and ARC wrote "advance" for a game WIN; old ledgers are read through legacy_ending.
WIN, DEATH, RESET, ADVANCE, CAP = "game_win", "death", "reset", "level_advance", "cap"
# item 4 (2026-10-22): the game ended because the agent's own code raised, never the world
AGENT_FAULT = "agent_fault"

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

# OLD RECORDS, NEVER REWRITTEN (Isaiah 2026-10-15 08:30; the reviewer 08:31): a ledger written
# before F1b carries the bare words. "win" was always a game won. "advance" was a level step in
# snaps and in tests calling retarget; on ARC it was the GAME WIN (arc_world terminal()), and
# from 446e7f6 (F1, a level clear through retarget) until F1b it was ALSO the level clear, which no
# word on the row separates. Readers of old ledgers (the recovery read, panel readers) map here.
LEGACY_AMBIGUOUS = "level_advance or game_win"


def legacy_ending(word: str, world: str | None, f1_era: bool = False) -> str:
    """An old ledger's ending word, by PROVENANCE. `world` is the run header's world class
    ("arc_world.ArcWorld" on ARC; from provenance where the header predates 0c841dd); `f1_era` is
    True for an ARC run at or after 446e7f6 and before F1b. Never rewrites a file."""
    if word == "win":
        return WIN
    if word != "advance":
        return word
    if world is not None and world.startswith("arc_world."):
        return LEGACY_AMBIGUOUS if f1_era else WIN
    return ADVANCE


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
        self._fh = None
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
            line = json.dumps(self._row(e), sort_keys=True, default=str) + "\n"
            if _LEDGER_HANDLE:
                if self._fh is None:
                    self._fh = self._path.open("a", encoding="utf-8")
                    _OPEN.add(self)
                self._fh.write(line)
                self._fh.flush()
            else:
                with self._path.open("a", encoding="utf-8") as fh:
                    fh.write(line)
        return e

    def close(self) -> None:
        """R2: close the held handle (end_run, and at exit); a later row reopens it."""
        if self._fh is not None:
            self._fh.close()
            self._fh = None
            _OPEN.discard(self)

    def _row(self, e: Entry) -> dict[str, Any]:
        d = {"mode": self.mode, **asdict(e)}
        if d.get("of") is None:
            d.pop("of", None)          # absent means "carries no magnitude", not "None"
        return d

    @property
    def entries(self) -> list[Entry]:
        return list(self._entries)

    def rows(self, start: int = 0) -> list[dict[str, Any]]:
        """What the gate reads. Plain data, no objects from this module. R2: from `start` on only,
        so a reader of the tail no longer converts the whole ledger."""
        return [self._row(e) for e in self._entries[start:]]

    def by_event(self, event: str) -> list[Entry]:
        return [e for e in self._entries if e.event == event]


@atexit.register
def _close_all() -> None:
    for led in list(_OPEN):
        led.close()


def signal_sign(row: dict[str, Any]) -> str | None:
    """MC1 (7a(4); the reviewer 2026-10-10 07:57Z): the sign of the ground's answer to a bet, read
    from the bet row and nothing else (Fig 1). None if the row is not a signal -- only a
    TRANSITION bet the ground answered is one; the @objective and @bracket rows are not. Paid iff
    not vanished and mass == 0; a vanished slot is failed whatever its mass (missing is charged,
    never skipped)."""
    d = row.get("detail") or {}
    if (row.get("step") != "PERCEIVE" or row.get("event") != "bet"
            or d.get("channel") != "transition" or d.get("suspended")):
        return None
    return "paid" if not d.get("vanished") and d.get("mass") == 0 else "failed"
