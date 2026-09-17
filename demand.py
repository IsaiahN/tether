"""The demand-ranked perception log, MEASURED (TRAINING_PLAN.md perceptual-reach gate; DEMAND_LOG).

Reads every game's answer-key gaps and ranks them by GAME COUNT (never chunk count), the gap (the
evidence, ranked on) separated from the fix (a per-instance hypothesis, tallied but never ranked
on). Seat-side evidence for whether a perception change is earned by cross-game demand -- never fed
to the agent. Replaces DEMAND_LOG.md's hand-maintained placeholder with the measured tally, so the
'how many games demand this' count is computed, not asserted.

Post-redirect (expressibility-closed, F165): these are AGENT-PERCEPTION gaps -- what the frozen 8 +
touching cannot state though the CLOSURE can. Never a reason to add perception here; the ranked list
is only the later build-queue, and one game never earns a change.
"""

from __future__ import annotations

import collections
import glob
import os
import sys

import reverse_engineer

sys.dont_write_bytecode = True


def demand(pattern: str = "replays/*_human.ndjson") -> list[dict]:
    """Every game's inexpressibility gaps aggregated by gap SHAPE, ranked by how many distinct GAMES
    demand it. `chunks` sizes the demand; `games` earns a change. `fixes` is the per-instance fix
    hypotheses tallied for later re-derivation -- carried, never ranked on."""
    by_shape: dict[str, dict] = collections.defaultdict(
        lambda: {"games": set(), "chunks": 0, "fixes": collections.Counter()})
    for p in sorted(glob.glob(pattern)):
        if os.path.getsize(p) < 100:
            continue
        g = os.path.basename(p).split("_")[0]
        try:
            ak = reverse_engineer.answer_key(p)
        except Exception:
            continue
        for gap in ak["gaps"]:
            rec = by_shape[gap.get("gap", "?")]
            rec["chunks"] += 1
            rec["games"].add(g)
            fix = gap.get("fix?")
            if fix:
                rec["fixes"][fix] += 1
    ranked = sorted(by_shape.items(), key=lambda kv: (-len(kv[1]["games"]), -kv[1]["chunks"]))
    return [{"gap": s, "games": len(r["games"]), "chunks": r["chunks"], "fixes": dict(r["fixes"])}
            for s, r in ranked]


if __name__ == "__main__":
    import json
    for d in demand():
        print(f"[{d['games']} games / {d['chunks']} chunks] {d['gap'][:80]}")
        for fix, n in d["fixes"].items():
            print(f"    fix?x{n}: {fix[:80]}")
    print(json.dumps({"gap_shapes": len(demand())}, indent=1))
