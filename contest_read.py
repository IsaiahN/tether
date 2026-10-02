"""Both readings of a `contest_table.py` panel, fixed BEFORE the panel finished.

**WHY THIS IS A SEPARATE FILE AND NOT A FLAG ON THE INSTRUMENT.** The panel is running and
its child processes are spawned fresh per arm, so editing `contest_table.py` mid-run would
give later arms different code from earlier ones -- the two-builds error that produced three
reversals this morning. The instrument is untouched; this reads its printed output.

**AND IT IS COMMITTED BEFORE THE TABLE EXISTS**, which is the whole point: the reviewer fixed
the reading at 13:46 with three rows seen, and a reading written after the data is not a
reading, it is a choice.

TWO READINGS, the reviewer 2026-10-02 13:46:

  1. THE PRE-REGISTERED VERDICT, exactly as written in `contest_table.py`: on informative
     slot-rows, contest ON must end with MORE slots settled-and-correct than OFF in BOTH
     ?ACTED arms and never fewer in either.

  2. A ROBUSTNESS READING, LABELLED AS SUCH AND NOT A REPLACEMENT: the same comparison
     restricted to slot-rows where EVERY ARM'S denominator is >= 2 -- the floor from 00:16
     this morning, which retired a PASS I had reported on a denominator of one. Too thin to
     read -> INSUFFICIENT.

  3. THE CHANGE PROCEEDS ONLY IF BOTH SAY PROCEED. A WEAK BAR CAN STOP A CHANGE, IT CANNOT
     LICENSE ONE: pre-registered PROCEEDS with robustness INSUFFICIENT is NOT a proceed, and
     pre-registered DOES-NOT-PROCEED settles it regardless.

`win` is reported with its denominator everywhere, because a W on 2/2 is not a W on 35/35 and
the tally alone cannot tell them apart.

    .venv/Scripts/python.exe contest_read.py <panel output file>
"""

from __future__ import annotations

import re
import sys

sys.dont_write_bytecode = True

ARMS = [(0, 0), (1, 0), (0, 1), (1, 1)]
MIN_DENOM = 2          # anchor: the 00:16 floor, borrowed and not chosen here
CELL = re.compile(r"(\d)(\d):\s*([W.])(\d+)/(\d+)")
ROW = re.compile(r"^\s+(\S+):(\d+)\s+(\S+)\s+(.*)$")


def parse(path: str) -> list[dict]:
    rows = []
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()
    for line in lines:
        m = ROW.match(line.rstrip("\n"))
        if not m or "UNAVAILABLE" in line:
            continue
        cells = CELL.findall(m.group(4))
        if len(cells) != len(ARMS):
            continue
        rows.append({"world": m.group(1), "seed": int(m.group(2)), "slot": m.group(3),
                     "cells": {(int(a), int(c)): {"win": w == "W", "ok": int(n), "tot": int(d)}
                               for a, c, w, n, d in cells}})
    return rows


def verdict(rows: list[dict], label: str, floor: int | None) -> tuple[str, dict]:
    use = rows
    if floor is not None:
        use = [r for r in rows if all(c["tot"] >= floor for c in r["cells"].values())]
    tally = {k: sum(1 for r in use if r["cells"][k]["win"]) for k in ARMS}
    n = len(use)
    print(f"\n  {label}   slot-rows {n}" + (f" (of {len(rows)}, floor {floor})" if floor else ""))
    for k in ARMS:
        wins = [f"{r['cells'][k]['ok']}/{r['cells'][k]['tot']}"
                for r in use if r["cells"][k]["win"]]
        print(f"    acted={k[0]} contest={k[1]}   {tally[k]}/{n}"
              + (f"   W denominators {wins}" if wins else ""))
    if n == 0:
        print("    -> INSUFFICIENT: no slot-row meets the floor on every arm")
        return "INSUFFICIENT", tally
    on0, off0, on1, off1 = tally[(0, 1)], tally[(0, 0)], tally[(1, 1)], tally[(1, 0)]
    out = "PROCEEDS" if (on0 > off0 and on1 > off1) else "DOES NOT PROCEED"
    print(f"    acted=0  ON {on0} vs OFF {off0}      acted=1  ON {on1} vs OFF {off1}")
    print(f"    -> {out}")
    return out, tally


def main() -> int:
    rows = parse(sys.argv[1])
    print(f"  parsed {len(rows)} informative slot-rows from {sys.argv[1]}")
    a, _ = verdict(rows, "1. PRE-REGISTERED, as written", None)
    b, _ = verdict(rows, f"2. ROBUSTNESS (labelled), every arm's denominator >= {MIN_DENOM}",
                   MIN_DENOM)
    both = a == "PROCEEDS" and b == "PROCEEDS"
    print(f"\n  PRE-REGISTERED {a}   ROBUSTNESS {b}")
    print(f"  -> THE CONTEST CHANGE {'PROCEEDS' if both else 'DOES NOT PROCEED'}"
          + ("" if both else "   (a weak bar can stop a change, it cannot license one)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
