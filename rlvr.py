"""§13 step 4: did the agent ACHIEVE each chunk's effect?

SEAT-SIDE. The agent does not import this, exactly as it does not import `arc_holdout`.

WHAT THIS IS AND IS NOT. §13 step 4 is *"run the real agent across all levels of that one game,
rigorous RLVR: reward = did it achieve each chunk's effect (ground-checkable), never did it
reproduce the actions."* The answer key and the runner both existed; nothing joined them, which
is what `F159` found. This is the join and nothing more.

`KEY_BOUNDARY` IS SATISFIED BY PLACEMENT, NOT BY CARE. The key is read AFTER the run, by the seat,
to score a trajectory the agent already produced. Nothing here reaches the betting path and the
agent's own decisions are taken before this module opens anything. Post-hoc verification is
permitted; pre-hoc selection is the encoded answer.

THE COMPARISON USES THE KEY'S OWN FUNCTION, WHICH IS THE POINT. `reverse_engineer._signature` is
*"the chunk's net effect as one compact, ground-checkable signature in frozen attributes"*, and it
is applied to BOTH sides -- the human chunk and the agent's own window. So the score carries no
metric invented here, and a change to what an effect means moves both sides together.

FRAMES ARE NOT IN THE LEDGER. `detail.frames` is a COUNT, so an archived run cannot be scored and
the capture has to be live -- `ArcWorld.on_frame`, attached for the duration of one run.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import arc_holdout
import arc_percept
import framepair
import reverse_engineer

sys.dont_write_bytecode = True


def _boards(game: str, cycles: int) -> tuple[list, dict]:
    """Run the agent and keep every board it saw, in order."""
    seen: list = []

    def tap(was, _action, now):
        if not seen and was is not None:
            seen.append(was)
        if now is not None:
            seen.append(now)

    report = arc_holdout.play(game=game, cycles=cycles, on_frame=tap)
    return seen, report


def _windows(objs: list, span: int) -> list:
    """Every span-long window of the agent's trajectory, as effect signatures.

    The agent is not following the human's cut, so the chunk boundary is not a place in ITS
    trajectory -- the question is whether the effect occurred anywhere, which is what makes this
    an effect check rather than an action check.
    """
    out = []
    for i in range(len(objs) - span):
        out.append(reverse_engineer._signature(framepair.match(objs[i], objs[i + span])))
    return out


def _rate(objs: list, key: dict) -> tuple[int, int, list]:
    """Non-trivial chunks achieved, over non-trivial chunks. The all-zero signature is dropped
    from both sides -- an inert agent matches it for free, and ls20's key contains one."""
    per: dict[int, list] = {}
    hit = tot = 0
    rows = []
    for c in key["chunks"]:
        s = c["signature"]
        if not (s["moved"] or s["resized"] or s["recoloured"] or s["vanished"] or s["appeared"]):
            continue
        span = max(1, int(c["frames"][1]) - int(c["frames"][0]))
        if span not in per:
            per[span] = _windows(objs, span) if span < len(objs) else []
        tot += 1
        got = s in per[span]
        hit += got
        rows.append({"level": c["level"], "frames": c["frames"], "span": span,
                     "achieved": got, "windows_searched": len(per[span])})
    return hit, tot, rows


# A DECLARED PANEL, not a chosen one: five games spanning the alphabet, fixed here so the null
# sample cannot be picked per reading. The seat authors it and the reviewer moves it.
NULL_PANEL = ("ar25", "dc22", "ls20", "sk48", "wa30")

# THE POOLED CEILING, AND IT IS NOT RECOMPUTED PER CALL -- F179. A per-call ceiling from five
# draws is a LOCAL MAXIMUM PRESENTED AS A BOUND: the first version of this returned 0.7% and
# passed `ls20`, one tick after 24 draws had measured the null reaching 4.2%. A control's samples
# are cumulative evidence about one distribution, so the bound is the max over EVERY draw taken,
# recorded here and raised only by a run that beats it.
#   37 draws, 7 nonzero.  max = 3/71 on m0r0's trajectory against the ls20 key.
POOLED_NULL_CEILING = 3 / 71


def against_null(game: str = "ls20", cycles: int = 25, others=NULL_PANEL) -> dict:
    """The reading and its base-rate DISTRIBUTION, because a scalar null hides its own variance.

    THE NULL IS CROSS-GAME: the same trajectory scored against ANOTHER game's key. The signature
    counts HOW MANY objects moved, not which or where, so collisions are cheap -- and the only way
    to know whether a hit means anything is to ask how often this trajectory hits a key it has no
    business hitting. Per game, never pooled.

    AND IT IS SAMPLED SEVERAL TIMES, WHICH F178 COST. One null draw read 0/71 and the word
    *nearly zero* went into a published claim; twenty-four draws later the null reached 3/71 and
    two of the three boards called scorers were at or below it. **A null quoted as one number is a
    distribution with its variance hidden, and it reads as more authoritative than the signal
    because it is supposed to be boring.** So this returns every draw and the MAX, and the verdict
    is against the max rather than the mean -- the ceiling is what a claim has to clear.
    """
    boards, report = _boards(game, cycles)
    objs = [arc_percept.components(b) for b in boards]

    def key_for(g: str) -> dict:
        p = Path(f"replays/{g}_answer_key.json")
        return (json.loads(p.read_text(encoding="utf-8")) if p.exists()
                else reverse_engineer.answer_key(f"replays/{g}_human.ndjson"))

    hit, tot, rows = _rate(objs, key_for(game))
    nulls = {g: _rate(objs, key_for(g))[:2] for g in others if g != game}
    rates = {g: (h / t if t else 0.0) for g, (h, t) in nulls.items()}
    # the bound is the POOLED max, never this call's -- see POOLED_NULL_CEILING
    ceiling = max([POOLED_NULL_CEILING, *rates.values()])
    mine = hit / tot if tot else 0.0
    return {"game": game, "cycles": cycles, "agent_frames": len(boards),
            "achieved": f"{hit}/{tot}", "rate": round(100 * mine, 1),
            "null_draws": {g: f"{h}/{t}" for g, (h, t) in nulls.items()},
            "this_call_max_pct": round(100 * max(rates.values(), default=0.0), 1),
            "pooled_ceiling_pct": round(100 * ceiling, 1),
            "clears_null": mine > ceiling,
            "levels_completed": report.get("levels_completed"),
            "reads": ("EXACT signature match against every same-span window of the agent's own "
                      "trajectory, all-zero chunks dropped from both sides. The null is the SAME "
                      "trajectory against another game's key -- the signature counts how many "
                      "objects moved, not which, so collisions are cheap and a bare rate is "
                      "unreadable"),
            "rows": rows}


if __name__ == "__main__":
    g = sys.argv[1] if len(sys.argv) > 1 else "ls20"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 25
    r = against_null(g, n)
    print(json.dumps({k: v for k, v in r.items() if k != "rows"}, indent=1))
    print(f'  VERDICT: {r["rate"]}% against a POOLED null ceiling of {r["pooled_ceiling_pct"]}% '
          f'(this run of {len(r["null_draws"])} draws maxed at {r["this_call_max_pct"]}%) -- '
          f'{"CLEARS" if r["clears_null"] else "DOES NOT CLEAR"}')
    for row in [x for x in r["rows"] if x["achieved"]]:
        print("  ACHIEVED", row)
