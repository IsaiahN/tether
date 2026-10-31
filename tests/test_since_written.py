"""ledger.since_written as a bisect over this step's tallied repeats (the reviewer 2026-10-31
r571 3; the r567 profile: 6.1% of own time, a scan of _tev on every _judge). Byte-equal by
construction: _tev is appended in `written` order, so its tail from w0 is a bisect, not a scan.
  S     on a ledger of appended rows and tallied repeats mixed over several steps,
        since_written(w0) equals the old scan's list for every w0 from 0 to written
  MF-S  the old scan with its filter dropped (every repeat of the step) differs from it, so S
        can fail
    python tests/test_since_written.py
"""
from __future__ import annotations

import bisect
import random
import sys

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)
import ledger

sys.dont_write_bytecode = True


def old_scan(led: ledger.Ledger, w0: int, keep_filter: bool = True) -> list:
    """since_written as it was before (1e9d4d5), kept here as the reference."""
    i = bisect.bisect_left(led._wat, w0)
    out = [(led._wat[j], led._row(led._entries[j])) for j in range(i, len(led._entries))]
    if led._tev:
        out += [(w, dict(r)) for w, r in led._tev if (w >= w0 or not keep_filter)]
        out.sort(key=lambda p: p[0])
    return [r for _w, r in out]


def build(seed: int):
    """A ledger at several moments: rows, tallied repeats (the objective_domain choice row, same
    fields), and flush_tally at each step's end. Yields the ledger after each record call."""
    rnd = random.Random(seed)
    led = ledger.Ledger()
    for cycle in range(6):
        for _ in range(rnd.randint(5, 25)):
            if rnd.random() < 0.6:
                led.record(cycle, "PLAN", "@goal", "choice", site=ledger.TALLY_SITE,
                           options=rnd.randint(0, 2), frontier=None, pick="p", by="b", root=None,
                           residual=None, seen=None)
            else:
                led.record(cycle, "ROUTE", f"o{rnd.randint(0, 3)}.row", "route", bin="held")
            yield led
        led.flush_tally(cycle)


def check_s() -> int:
    n = 0
    for seed in range(4):
        for led in build(seed):
            for w0 in range(0, led.written + 1):
                assert led.since_written(w0) == old_scan(led, w0), (seed, led.written, w0)
                n += 1
    return n


def check_mf() -> bool:
    for seed in range(4):
        for led in build(seed):
            if not led._tev:
                continue
            w0 = led._tev[-1][0]          # past every repeat but the last
            if led.since_written(w0) != old_scan(led, w0, keep_filter=False):
                return True
    return False


def main() -> int:
    n = check_s()
    print(f"  S: since_written == the old scan for {n} (ledger state, w0) pairs")
    assert check_mf(), "MF-S: the filter dropped and S still passed: S cannot fail"
    print("  MF-S: the scan without its filter differs, so S can fail")
    print("since_written: 2 checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
