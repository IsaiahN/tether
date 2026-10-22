"""F1b: ONE WORD PER ENDING (Isaiah 2026-10-15 08:30; the reviewer 08:27, 08:31). WRITTEN, NOT
RUN: it runs in the end-of-step-7 checklist. A game won is ledger.WIN ("game_win"), a level cleared
ledger.ADVANCE ("level_advance"); the bare words are read only through ledger.legacy_ending.

  W1   no git-tracked .py outside EXEMPT carries the quoted literal "advance" or "win".
  W2   legacy_ending: "win" -> game_win; ARC "advance" -> game_win, or the ambiguity in F1's era;
       any other world's "advance" -> level_advance; any other word unchanged.
  MF-W MUST-FAIL: the scanner over a source holding `return "advance"` reports it.

    python tests/test_ending_words.py
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import ledger  # noqa: E402

# EXEMPTIONS AS DATA, each with its reason (a table can be pinned; logic widens quietly)
EXEMPT = {
    "ledger.py": "legacy_ending reads the old words, never writes them",
    "contest_read.py": "a cell field named win, not an ending word",
    "contest_table.py": "a cell field named win, not an ending word",
    "tests/test_ending_words.py": "this check names the words it forbids",
    "tests/test_stream_win.py": "quotes the pre-F1b line as its must-fail target",
}
BARE = re.compile(r"""["'](advance|win)["']""")


def scan(name: str, text: str) -> list[str]:
    return [f"{name}:{i}: {ln.strip()}" for i, ln in enumerate(text.splitlines(), 1)
            if BARE.search(ln)]


def main() -> None:
    files = subprocess.run(["git", "ls-files", "*.py"], capture_output=True, text=True,
                           check=True, stdin=subprocess.DEVNULL).stdout.split()
    assert files, "no files listed: the scan would pass on nothing"
    hits = [h for f in files if f not in EXEMPT
            for h in scan(f, Path(f).read_text(encoding="utf-8"))]
    assert not hits, ("W1: a bare ending word", hits)
    print(f"  W1 {len(files) - len(EXEMPT)} files scanned, no bare ending word "
          f"({len(EXEMPT)} exempt, each with its reason)")
    lg = ledger.legacy_ending
    assert lg("win", None) == ledger.WIN
    assert lg("advance", "arc_world.ArcWorld") == ledger.WIN
    assert lg("advance", "arc_world.ArcWorld", f1_era=True) == ledger.LEGACY_AMBIGUOUS
    assert lg("advance", "snaps.Snap") == ledger.ADVANCE
    assert lg("advance", None) == ledger.ADVANCE
    assert lg("death", "arc_world.ArcWorld") == "death"
    print("  W2 legacy_ending maps the old words by provenance")
    mf = scan("planted.py", 'def terminal(self):\n    return "advance"\n')
    assert mf, "MF-W MUST-FAIL did not fail: the scanner missed a planted bare word"
    print(f"  MF-W must-fail fired: {mf[0]}")
    print("ending words: OK")


if __name__ == "__main__":
    main()
