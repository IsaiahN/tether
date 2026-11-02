"""N1 / N2, THE LIVE NARRATOR (the reviewer 2026-11-02 14:38 plan, r822): ledger.Ledger says its key
rows aloud through narrate.Narrator.
  MF-N1  a mint row then a settle row print MINT then SETTLE, in order, and narrate.log holds them.
  MF-N2  the ledger file is byte-identical with the narrator ON and OFF.
  MF-N3  OFF prints nothing and writes no narrate.log.
  MF-N4  2,500 mint rows in one cycle print ONE MINT line and, at the next cycle, "+2499 more".
  MF-N5  end_game prints "stopped at link perception" for a game with no bet, "vocabulary" for
         bets and no term, and "plan" for a closer with no level.
  MF-N6  a console that raises on write (an injected UnicodeEncodeError) never reaches play: the
         rows are all written, the narrator turns itself off and counts 1 fault.
  MF-N7  a second end_game with no row since the last says nothing.

    python tests/test_narrate.py
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
    led.record(1, "PERCEIVE", "o1.x", "bet", channel="transition")
    led.record(1, "MINT", "o1.x", "mint", term="t1", reads="o1.x moves by one")
    led.record(2, "SETTLE", "o1.x", "settle", term="t1", status="accepted")


def run(on: bool, d: Path, fill=rows) -> tuple[str, Path]:
    narrate._NARRATE = on
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            led = ledger.Ledger(d / "run.jsonl")
            fill(led)
            led.close()
    finally:
        narrate._NARRATE = True
    return out.getvalue(), d / "run.jsonl"


def main():
    assert narrate._NARRATE, "the arm is ON by default"
    a, b = Path(tempfile.mkdtemp(prefix="narr_on_")), Path(tempfile.mkdtemp(prefix="narr_off_"))
    said, led_on = run(True, a)
    lines = said.splitlines()
    assert [ln.split()[1] for ln in lines] == ["MINT", "SETTLE"], ("MF-N1", lines)
    assert lines[0].startswith("c1 MINT o1.x: t1") and "accepted" in lines[1], ("MF-N1", lines)
    assert (a / "narrate.log").read_text(encoding="utf-8").splitlines() == lines, "MF-N1 log"
    quiet, led_off = run(False, b)
    assert led_on.read_bytes() == led_off.read_bytes(), "MF-N2: the ledger moved with the narrator"
    assert quiet == "" and not (b / "narrate.log").exists(), ("MF-N3", quiet)

    def burst(led):
        for i in range(2500):
            led.record(5, "MINT", f"o{i}.x", "mint", term=f"t{i}")
        led.record(6, "PERCEIVE", "*", "progress", closer=("o1.x",), selected_want=None)
    said, _ = run(True, Path(tempfile.mkdtemp(prefix="narr_cap_")), burst)
    lines = said.splitlines()
    assert sum(ln.split()[1] == "MINT" for ln in lines) == 1, ("MF-N4", lines[:4])
    assert "c5 +2499 more: MINT 2499" in lines, ("MF-N4", lines)

    def games(led):
        led.end_game(0, "g0")
        led.record(1, "PERCEIVE", "o1.x", "bet", channel="transition")
        led.end_game(1, "g1")
        led.record(2, "PERCEIVE", "o1.x", "bet", channel="transition")
        led.record(2, "MINT", "o1.x", "mint", term="t1")
        led.record(3, "PERCEIVE", "*", "progress", closer=("o1.x",), selected_want=None)
        led.end_game(3, "g2")
    said, _ = run(True, Path(tempfile.mkdtemp(prefix="narr_game_")), games)
    links = [ln.split("stopped at link ")[1].split()[0] for ln in said.splitlines() if "GAME" in ln]
    assert links == ["perception", "vocabulary", "plan"], ("MF-N5", said)

    def again(led):                      # MF-N7: a second end with nothing since says nothing
        games(led)
        led.end_game(4, "end cap")
    said, _ = run(True, Path(tempfile.mkdtemp(prefix="narr_end_")), again)
    assert sum("GAME" in ln for ln in said.splitlines()) == 3, ("MF-N7", said)

    class Broken(io.StringIO):           # MF-N6: a console that raises on every write
        def write(self, s):
            raise UnicodeEncodeError("cp1252", s, 0, 1, "injected")
    d = Path(tempfile.mkdtemp(prefix="narr_err_"))
    led = ledger.Ledger(d / "run.jsonl")
    saved, sys.stdout = sys.stdout, Broken()
    try:
        rows(led)                        # RED before the guard: the error reaches play here
        led.end_game(2, "g")
    finally:
        sys.stdout = saved
    led.close()
    n = len((d / "run.jsonl").read_text(encoding="utf-8").splitlines())
    nar = led.narrator
    assert n == 3 and not nar.on and nar.faults == 1, ("MF-N6", n, nar.fault)
    print("test_narrate: MINT then SETTLE said in order and logged; the ledger byte-identical "
          "ON/OFF; OFF says nothing; 2,500 mints in a cycle -> 1 line + '+2499 more'; games "
          f"stop at {links}; an empty second end says nothing; a raising console turns it off "
          "(1 fault), never into play")


if __name__ == "__main__":
    main()
