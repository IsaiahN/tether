"""NOTHING SILENT: a narrator's first fault is on the record, and one bad row does not kill
the rest of the run.   MF is the old self-disabling guard, reintroduced in the test.

    python tests/test_nsm_fault.py
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

os.environ["TETHER_NSM_SPEAK"] = "1"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import ledger  # noqa: E402
import nsm  # noqa: E402


def _pair(root: str):
    led = ledger.Ledger(Path(root) / "led.jsonl")
    return led, led.speaker, Path(root) / "nsm.log"


def check_fault_is_recorded_and_the_trace_lives() -> None:
    assert nsm._NSM, "fixture: the narrator arm is off"
    with tempfile.TemporaryDirectory() as root:
        led, sp, log = _pair(root)
        try:
            # a malformed row: say_row calls d.get on None, which raises INSIDE nsm.py
            sp.see(1, 0, "PLAN", "o1", "mint", None)
            assert sp.faults == 1 and sp.skipped == 1 and sp.on, (sp.faults, sp.skipped, sp.on)
            faults = [r for r in led.rows() if r["event"] == "nsm_fault"]
            assert len(faults) == 1, led.rows()
            d = faults[0]["detail"]
            assert d["exception"] == "AttributeError" and d["source"].startswith("nsm.py:"), d
            assert d["where"] == "nsm.Speaker.see" and d["message"], d

            # the NEXT good row is still spoken; the bad one cost one counted row, not the run
            sp.see(2, 0, "PLAN", "o1", "mint", {"term": "x"})
            text = log.read_text(encoding="utf-8")
            assert "MINT" in text and "`x`" in text, text
            assert sp.faults == 1 and sp.skipped == 1 and sp.on, (sp.faults, sp.skipped, sp.on)
            print(f"  F1: fault on the record at {d['source']} ({d['exception']}); the next good "
                  f"row was spoken; faults {sp.faults}, skipped {sp.skipped}: GREEN")
        finally:
            led.close()                          # R2: release the held handle before cleanup


def check_the_old_silence_is_red() -> None:
    """MF: put the self-disabling guard back; the fault is invisible and the run goes quiet."""
    old = nsm.Speaker.see

    def silent(self, seq, cycle, step, slot, event, d):
        if not self.on:
            return
        try:
            self._see(seq, cycle, step, slot, event, d)
        except Exception as e:                     # the defect: on=False, no record
            self.on = False
            self.faults += 1
            self.fault = repr(e)[:200]

    nsm.Speaker.see = silent
    try:
        with tempfile.TemporaryDirectory() as root:
            led, sp, log = _pair(root)
            try:
                sp.see(1, 0, "PLAN", "o1", "mint", None)
                sp.see(2, 0, "PLAN", "o1", "mint", {"term": "y"})
                assert not sp.on and sp.faults == 1
                assert not [r for r in led.rows() if r["event"] == "nsm_fault"], led.rows()
                assert "`y`" not in log.read_text(encoding="utf-8"), "the bad row did not kill it"
                print("  MF: with the old guard, no fault row and the next good row is silent -- "
                      "RED as required")
            finally:
                led.close()
    finally:
        nsm.Speaker.see = old


if __name__ == "__main__":
    check_fault_is_recorded_and_the_trace_lives()
    check_the_old_silence_is_red()
    print("nsm_fault: OK")
