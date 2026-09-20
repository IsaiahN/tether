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


def against_null(game: str = "ls20", cycles: int = 25, others=("vc33", "tn36")) -> dict:
    """The reading and its base rate in one call, because the reading is unreadable alone.

    THE NULL IS CROSS-GAME: the same trajectory scored against ANOTHER game's key. The signature
    counts HOW MANY objects moved, not which or where, so collisions are cheap -- and the only way
    to know whether a hit means anything is to ask how often this trajectory hits a key it has no
    business hitting. Per game, never pooled.
    """
    boards, report = _boards(game, cycles)
    objs = [arc_percept.components(b) for b in boards]

    def key_for(g: str) -> dict:
        p = Path(f"replays/{g}_answer_key.json")
        return (json.loads(p.read_text(encoding="utf-8")) if p.exists()
                else reverse_engineer.answer_key(f"replays/{g}_human.ndjson"))

    hit, tot, rows = _rate(objs, key_for(game))
    nulls = {g: _rate(objs, key_for(g))[:2] for g in others if g != game}
    return {"game": game, "cycles": cycles, "agent_frames": len(boards),
            "achieved": f"{hit}/{tot}", "null": {g: f"{h}/{t}" for g, (h, t) in nulls.items()},
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
    for row in [x for x in r["rows"] if x["achieved"]]:
        print("  ACHIEVED", row)
