"""P7: WEIGHT AND SENSE LINES (TETHER_NARRATE_WEIGHT; the reviewer 2026-11-12 r1835/r1838,
DESIGN_STEP8 item 6; Isaiah 11-06 "when a weight changes mid-game log that event and console it").

  NW1     a standing_freed row and a reflex_settled row print WEIGHT lines naming the form, the side
          it crossed to and its counts; a sense_pick row prints "src ... -> sense .../role,
          expecting ..."; a sense_note row prints held / missed.
  NW2     the ledger file is byte-identical with the arm ON and OFF (say-only).
  MF-NW1  with the arm OFF the same rows print no WEIGHT and no SENSE line (RED for NW1).

    python tests/test_narrate_weight.py
"""
from __future__ import annotations

import contextlib
import io
import sys
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import ledger  # noqa: E402
import narrate  # noqa: E402


def rows(led: ledger.Ledger) -> None:
    led.record(3, "ROUTE", "@weight", "standing_freed", form="muse_test", situation=["k", "s"],
               to="under", by="witnesses", against=2.5, against_before=1.0, paid=0,
               carried=0, halflife=8, reads="the weight crossed")
    led.record(4, "ROUTE", "o2.x", "reflex_settled", form="orient", situation=["k"], fired=True,
               held=True, paid=3, against=0.5, reads="orients")
    led.record(5, "MINT", "o39.col", "sense_pick", src="SELF", subj=["col", "row"],
               head="AGENT|translate", role="PROCESS", pred=["MOTION", 1, "s"])
    led.record(6, "SETTLE", "o39.col", "sense_note", head="AGENT|translate", outcome="paid",
               src="SELF")


def run(on: bool, d: Path) -> tuple[str, Path]:
    narrate._NARRATE_WEIGHT = on
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            led = ledger.Ledger(d / "run.jsonl")
            rows(led)
            led.close()
    finally:
        narrate._NARRATE_WEIGHT = True
    return out.getvalue(), d / "run.jsonl"


def main() -> int:
    assert narrate._NARRATE and narrate._NARRATE_WEIGHT, "both arms are ON by default"
    a, b = Path(tempfile.mkdtemp(prefix="nw_on_")), Path(tempfile.mkdtemp(prefix="nw_off_"))
    said, led_on = run(True, a)
    lines = said.splitlines()
    kinds = [ln.split()[1] for ln in lines]
    assert kinds == ["WEIGHT", "WEIGHT", "SENSE", "SENSE"], ("NW1", lines)
    assert "muse_test" in lines[0] and "-> under by witnesses" in lines[0], ("NW1", lines[0])
    assert "orient paid" in lines[1], ("NW1", lines[1])
    assert "src SELF on" in lines[2], ("NW1", lines[2])
    assert "-> sense AGENT|translate/PROCESS, expecting" in lines[2], ("NW1", lines[2])
    assert "AGENT|translate held under SELF" in lines[3], ("NW1", lines[3])
    print("  NW1: " + "\n        ".join(lines))
    quiet, led_off = run(False, b)
    assert led_on.read_bytes() == led_off.read_bytes(), "NW2: the ledger moved with the arm"
    print("  NW2: the ledger is byte-identical ON and OFF")
    off_kinds = [ln.split()[1] for ln in quiet.splitlines()]
    assert "WEIGHT" not in off_kinds and "SENSE" not in off_kinds, ("MF-NW1 did not fail", quiet)
    print("  MF-NW1: OFF prints no WEIGHT / SENSE line (RED for NW1, as required)")
    print("narrate_weight: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
