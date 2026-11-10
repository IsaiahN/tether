"""step_order_scan: every gate.py _steps violation in a ledger, not only the first.

The reviewer 2026-11-09 r1559, r1560. gate.py refuses at the first row whose step falls below the
highest step already written on its (cycle, slot); this reads the same rule over every row and
lists each violation by (cycle, key, the step pair, the event pair), so one run shows them all.
It imports gate.STEPS read-only and never changes gate.py.

Every witness on a real game reports "step-order violations: base N / change M", plus any new
key; a change that adds a violation stops and comes back (r1560).

    python conform/step_order_scan.py ledger.jsonl [base.jsonl]

With a base, it prints both counts and the keys only the change has; rc 1 if the change adds any.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from gate import STEPS  # noqa: E402


def violations(path: str) -> list[tuple]:
    """(cycle, slot, step, event, high step, high event) for every row below its key's high mark."""
    hi: dict = {}
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            k, i = (r.get("cycle", 0), r.get("slot")), STEPS.index(r["step"])
            if k in hi and i < hi[k][0]:
                out.append((*k, r["step"], r["event"], STEPS[hi[k][0]], hi[k][1]))
            else:
                hi[k] = (i, r["event"])
    return out


def _report(name: str, v: list) -> None:
    print(f"{name}: {len(v)} violations on {len({(c, s) for c, s, *_ in v})} keys")
    kind = Counter((st, ev, hst, hev, s if str(s).startswith("@") else "real slot")
                   for _c, s, st, ev, hst, hev in v)
    for (st, ev, hst, hev, sk), n in kind.most_common():
        print(f"  {n:5d}  {st} {ev} after {hst} {hev}  on {sk}")


def main(argv: list[str]) -> int:
    new = violations(argv[0])
    _report(argv[0], new)
    if len(argv) < 2:
        return 0
    base = violations(argv[1])
    _report(argv[1], base)
    keys = {(c, s) for c, s, *_ in new} - {(c, s) for c, s, *_ in base}
    print(f"step-order violations: base {len(base)} / change {len(new)}; keys only in the "
          f"change: {sorted(keys)[:10]}")
    return 1 if len(new) > len(base) or keys else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
