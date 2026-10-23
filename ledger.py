"""The record. Append-only; every entry names its loop step.

The ledger is a reification: the loop's own state made available as data. That is why a
checker can read it without reading the machine, and why the checker can be domain-blind.
"""

from __future__ import annotations

import atexit
import bisect
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
# THE CHOICE TALLY (Isaiah 2026-10-23 09:12 "these should be deduped and tallied"; the reviewer
# 09:13, 10:40): an objective_domain "choice" row whose KEY was already written in this life is
# not appended; it adds to a per-step count, flushed as one "choice_tally" row per key at the
# step's end (flush_tally). E4b: 636,386 such rows, 3,001 keys. The key is every decision field;
# only cycle, seq and mode are out. `written` counts appended rows AND tallied repeats, and
# since_written() returns both in call order, so a reader that captures and replays rows
# (_library_fit's dedup) replays the repeats too. CHECK: each repeat's FULL key is counted beside
# its tally key, and a flush asserts one full key per tally key and equal counts. OFF: every row
# appended, as before.
_CHOICE_TALLY = armflag.arm("TETHER_CHOICE_TALLY", default=True)
_CHOICE_TALLY_CHECK = armflag.arm("TETHER_CHOICE_TALLY_CHECK")
# THE ORDER GUARD (the reviewer 2026-10-23 11:21, 11:25, 11:32): a repeat is tallied only where
# writing it in full could change no check gate.py makes on the file: the latest row appended in its
# (cycle, slot) carries the same step (so gate._steps, gate.py:86-103, would neither refuse it nor
# move its "last"); its detail has no field outside the key; its mode equals its first row's (_mode).
# Otherwise it is appended in full, counted per condition. OFF: tally ignores order (c2ddc5a).
_CHOICE_TALLY_ORDER = armflag.arm("TETHER_CHOICE_TALLY_ORDER", default=True)
TALLY_SITE = "objective_domain"
TALLY_FIELDS = ("site", "options", "frontier", "pick", "by", "root", "residual", "seen")


def _tally_key(slot: str, step: str, detail: dict, fields: tuple) -> str:
    return json.dumps([slot, step, [detail.get(f) for f in fields]], sort_keys=True, default=str)


def _full_key(slot: str, step: str, detail: dict) -> str:
    """CHECK's key: the WHOLE detail, so a tally key that drops a field is caught."""
    return json.dumps([slot, step, detail], sort_keys=True, default=str)

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
        self.written = 0                      # appended rows + tallied repeats, in call order
        self._wat: list[int] = []             # each appended entry's `written` index
        self._tkeys: dict[str, int] = {}      # tally key -> the seq of its full row
        self._tstep: dict[str, list] = {}     # this step: key -> [ref, n, first_cycle, last_cycle]
        self._tev: list[tuple[int, dict]] = []   # this step's tallied repeats, (written, row)
        self._tchk: dict[str, set] = {}       # CHECK: tally key -> its full keys (first + repeats)
        self._tfull: dict[str, str] = {}      # CHECK: tally key -> the full key of its first row
        self._tchk_n: dict[str, int] = {}     # CHECK: full key -> repeats this step
        self._tmode: dict[str, str] = {}      # ORDER: tally key -> its first row's mode
        self._last_step: dict[tuple, str] = {}   # ORDER: (cycle, slot) -> its latest appended step
        self._last_cyc: int | None = None     # ORDER: the highest cycle appended (prunes the above)
        self.tally_full = {"step": 0, "field": 0, "mode": 0}   # ORDER: repeats appended in full
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
        if _CHOICE_TALLY and event == "choice" and detail.get("site") == TALLY_SITE:
            k = _tally_key(slot, step, detail, TALLY_FIELDS)
            ref = self._tkeys.get(k)
            if ref is not None and _CHOICE_TALLY_ORDER:
                why = ("step" if self._last_step.get((cycle, slot)) != step
                       else "field" if any(f not in TALLY_FIELDS for f in detail)
                       else "mode" if self._tmode.get(k) != self.mode else None)
                if why is not None:
                    ref = None
                    self.tally_full[why] += 1
            if ref is not None:
                t = self._tstep.setdefault(k, [ref, 0, cycle, cycle])
                t[1] += 1
                t[3] = cycle
                row = {"mode": self.mode, "cycle": cycle, "step": step, "slot": slot,
                       "event": event, "detail": detail}
                if of is not None:
                    row["of"] = of
                self._tev.append((self.written, row))
                self.written += 1
                if _CHOICE_TALLY_CHECK:
                    fk = _full_key(slot, step, detail)
                    self._tchk.setdefault(k, {self._tfull[k]}).add(fk)
                    self._tchk_n[fk] = self._tchk_n.get(fk, 0) + 1
                return self._entries[ref]
            if k not in self._tkeys:
                self._tkeys[k] = len(self._entries)
                self._tmode[k] = self.mode
                if _CHOICE_TALLY_CHECK:
                    self._tfull[k] = _full_key(slot, step, detail)
        e = Entry(len(self._entries), cycle, step, slot, event, detail, of)
        self._entries.append(e)
        if _CHOICE_TALLY and _CHOICE_TALLY_ORDER:
            if self._last_cyc is None or cycle > self._last_cyc:
                if self._last_cyc is not None:     # a missing key appends in full: pruning is safe
                    self._last_step = {kk: v for kk, v in self._last_step.items()
                                       if kk[0] >= cycle - 1}
                self._last_cyc = cycle
            self._last_step[(cycle, slot)] = step
        self._wat.append(self.written)
        self.written += 1
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

    def since_written(self, w0: int) -> list[dict[str, Any]]:
        """Every record() call from `written` index w0 on, in call order: the appended rows and this
        step's tallied repeats. OFF (no repeats): exactly rows(i) where i is w0's entry."""
        i = bisect.bisect_left(self._wat, w0)
        out = [(self._wat[j], self._row(self._entries[j])) for j in range(i, len(self._entries))]
        if self._tev:
            out += [(w, dict(r)) for w, r in self._tev if w >= w0]
            out.sort(key=lambda p: p[0])
        return [r for _w, r in out]

    def flush_tally(self, cycle: int) -> None:
        """The step's end: one "choice_tally" row per key repeated in it (ref, n, first and last
        cycle), then the per-step state clears. CHECK: one full key per tally key, equal counts."""
        if not self._tstep:
            self._tev.clear()
            return
        if _CHOICE_TALLY_CHECK:
            for k, (_ref, n, _f, _l) in self._tstep.items():
                fks = self._tchk.get(k, set())
                if len(fks) != 1 or self._tchk_n.get(next(iter(fks)), 0) != n:
                    raise AssertionError(("CHOICE_TALLY CHECK", k[:200], n,
                                          {f[:120]: self._tchk_n.get(f) for f in fks}))
            self._tchk.clear()
            self._tchk_n.clear()
        pend, self._tstep = self._tstep, {}
        self._tev.clear()
        for ref, n, first, last in pend.values():
            self.record(cycle, "SETTLE", "@tally", "choice_tally", ref=ref, n=n,
                        first_cycle=first, last_cycle=last)


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
