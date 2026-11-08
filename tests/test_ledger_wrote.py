"""Ledger.wrote (the reviewer 2026-11-07 r1442 (a), r1449): whether a row on a slot under a step was
written in a given cycle -- what the "@derived" key reads before moving E0-W's deferral note.

W1  an ACCEPT on d in cycle c-1, a tail-booked row of c-1 after it, then cycle c rows with no ACCEPT
    on d: wrote(c, "ACCEPT", d) is False, so the note stays on d
W2  an ACCEPT on d in cycle c: wrote(c, "ACCEPT", d) is True, so the note goes on "@derived"
W3  a cycle c-1 row written after cycle c rows does not cut the scan short: the c ACCEPT before it
    is found
MF  a scan that matches any cycle >= c - 1 (not exactly c) reports W1's c-1 ACCEPT: W1 catches it

    python tests/test_ledger_wrote.py
"""
from __future__ import annotations

import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import ledger  # noqa: E402

D, C = "o0.dcol_o30", 17


def w1() -> ledger.Ledger:
    led = ledger.Ledger()
    led.record(C - 1, "ACCEPT", D, "rebind")
    led.record(C - 1, "PERCEIVE", "@vector", "unseen_withdrawn", at=D)   # the tail, booked c-1
    led.record(C - 1, "REPEAT", "@loop", "repeat")
    led.record(C, "PLAN", D, "reflex")
    led.record(C, "ROUTE", D, "route")
    return led


def main() -> int:
    led = w1()
    assert led.wrote(C, "ACCEPT", D) is False, "W1: a c-1 ACCEPT counted as this cycle's"
    led.record(C, "ACCEPT", D, "rebind")
    assert led.wrote(C, "ACCEPT", D) is True, "W2: this cycle's ACCEPT not found"
    led3 = ledger.Ledger()
    led3.record(C, "ACCEPT", D, "rebind")
    led3.record(C - 1, "PERCEIVE", "@vector", "probe_queued", at=D)      # a c-1 row after c rows
    led3.record(C, "MINT", D, "mint")
    assert led3.wrote(C, "ACCEPT", D) is True, "W3: a c-1 row cut the scan short"
    real = ledger.Ledger.wrote

    def loose(self, cycle, step, slot):
        for e in reversed(self._entries):
            if e.cycle < cycle - 1:
                return False
            if e.step == step and e.slot == slot:      # the planted defect: any cycle >= c - 1
                return True
        return False
    ledger.Ledger.wrote = loose
    try:
        caught = w1().wrote(C, "ACCEPT", D) is True
    finally:
        ledger.Ledger.wrote = real
    assert caught, "MF: the loose scan was not caught by W1"
    print("W1  a c-1 ACCEPT (tail row between) does not count: the note stays on d")
    print("W2  this cycle's ACCEPT is found: the note goes on @derived")
    print("W3  a c-1 row written after cycle c rows does not cut the scan short")
    print("MF  a scan matching any cycle >= c-1 reports W1's c-1 ACCEPT")
    print("ledger_wrote: 3 of 3, 1 must-fail")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
