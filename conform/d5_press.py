"""7a D5's optional reading (the reviewer 2026-10-10 16:41Z): for each `not_split` row, would the
REALISED PRESS have separated the term's right rows from its wrong rows? A READING for the seats,
offline, from the ledger alone; nothing in the agent reads it, and a press is never a guard
(Isaiah 2026-09-29: guards name intents). Per ledger, never pooled (Fig 1 :22).

Rows: the slot's bet rows bound to the term, in the not_split row's level, up to its cycle; right
means mass 0. The press is the same cycle's REPEAT action (a bet at cycle c settles c's action).
The reader's right/wrong counts are printed beside the agent's, so a mismatch shows the pairing
or the window is wrong rather than passing silently.

    python conform/d5_press.py runs/x/*.jsonl
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.dont_write_bytecode = True


def read(path: Path) -> list[dict]:
    rows = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
    press, level = {}, {}
    for r in rows:
        if r.get("event") == "repeat":
            d = r.get("detail") or {}
            press[r["cycle"]] = d.get("action")
            level[r["cycle"]] = d.get("level")
    out = []
    for ns in (r for r in rows if r.get("event") == "not_split"):
        d, c = ns["detail"], ns["cycle"]
        by = defaultdict(lambda: [0, 0])          # press -> [right, wrong]
        for b in rows:
            bd = b.get("detail") or {}
            if (b.get("event") != "bet" or b["slot"] != d["split_slot"]
                    or bd.get("bound") != d["term"]
                    or b["cycle"] > c or level.get(b["cycle"]) != level.get(c)):
                continue
            by[press.get(b["cycle"])][0 if bd.get("mass", 0.0) == 0.0 else 1] += 1
        right = sum(v[0] for v in by.values())
        wrong = sum(v[1] for v in by.values())
        pure = all(min(v) == 0 for v in by.values())
        out.append({"cycle": c, "slot": d["split_slot"], "term": d["term"],
                    "agent": (d["right"], d["wrong"]), "reader": (right, wrong),
                    "by_press": {k: tuple(v) for k, v in sorted(by.items(), key=str)},
                    "press_separates": pure and right >= 2 and wrong >= 2})
    return out


if __name__ == "__main__":
    for p in sys.argv[1:]:
        res = read(Path(p))
        print(f"{Path(p).name}: not_split {len(res)}, the press would separate "
              f"{sum(r['press_separates'] for r in res)}")
        for r in res:
            flag = "" if r["agent"] == r["reader"] else "  COUNT MISMATCH"
            print(f"  c{r['cycle']} {r['slot']} {r['term']}: agent {r['agent']} reader "
                  f"{r['reader']}{flag}; by press (right, wrong) {r['by_press']}; "
                  f"separates {r['press_separates']}")
