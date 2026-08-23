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


@dataclass(frozen=True)
class Entry:
    seq: int
    cycle: int
    step: str
    slot: str
    event: str
    detail: dict[str, Any] = field(default_factory=dict)


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

    def record(self, cycle: int, step: str, slot: str, event: str, **detail: Any) -> Entry:
        if step not in STEPS:
            raise ValueError(f"entry names no loop step: {step!r}")
        e = Entry(len(self._entries), cycle, step, slot, event, detail)
        self._entries.append(e)
        if self._path is not None:
            with self._path.open("a", encoding="utf-8") as fh:
                row = {"mode": self.mode, **asdict(e)}
                fh.write(json.dumps(row, sort_keys=True, default=str) + "\n")
        return e

    @property
    def entries(self) -> list[Entry]:
        return list(self._entries)

    def rows(self) -> list[dict[str, Any]]:
        """What the gate reads. Plain data, no objects from this module."""
        return [{"mode": self.mode, **asdict(e)} for e in self._entries]

    def by_event(self, event: str) -> list[Entry]:
        return [e for e in self._entries if e.event == event]

    def origin_of(self, term: str) -> Entry | None:
        """Where a term entered the library. The question a reader actually asks."""
        for e in self._entries:
            if e.event == "accept" and e.detail.get("term") == term:
                return e
        return None
