"""WHY DOES FIXTURE B SETTLE NOTHING? The whole book, not the four keys I happened to capture.

The panel reported `bargain_paid 0 / settled 0` on all three `click_only` seeds and I said I
had not traced the cause. **The panel could not trace it: it captured four book keys chosen
for a different question.** `gamma.book` carries the stage counts that say WHERE candidates
die -- `mint_no_residual`, the gap buckets, the arrival-depth histogram -- and reading all of
them costs one short run.

**NO HYPOTHESIS IS ENCODED HERE.** It prints every key both arms hold, and the difference.
A probe that only printed the key I suspect would confirm me by construction.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, r"C:\Users\Admin\Documents\GitHub\tether")

import gamma as G  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

CYCLES = 60   # anchor: the panel's population, so this book is that run's book
SEED = 0      # anchor: the panel's first seed


def run(arm: str) -> dict:
    env = world.bind(gridworld.family(arm, SEED, CYCLES))
    ag = tether.Agent(env, G.Gamma(env.atoms()), tether.Config(max_depth=2), ledger.Ledger())
    err = ""
    try:
        for _ in range(CYCLES):
            ag.step()
    except Exception as exc:                                  # noqa: BLE001
        err = f"{type(exc).__name__}: {exc}"
    return {"arm": arm, "error": err, "book": dict(ag.gamma.book),
            "actions": list(env.actions()), "slots": len(env.slots())}


def main() -> int:
    arm = sys.argv[1] if len(sys.argv) > 1 else "click_only"
    r = run(arm)
    Path(__file__).with_name(f"book_{arm}.json").write_text(
        json.dumps(r, indent=1, sort_keys=True), encoding="utf-8")
    print(f"WORLD gridworld {arm} seed {SEED}, {CYCLES} cycles, no ARC board.")
    print(f"actions={r['actions']}  slots={r['slots']}  error={r['error']!r}")
    print("  THE WHOLE BOOK (every key, zeros included -- a missing key and a zero key")
    print("  are different readings and only one of them is a measurement):")
    for k in sorted(r["book"]):
        print(f"    {k:28} {r['book'][k]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
