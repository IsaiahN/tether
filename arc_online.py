"""ONE SESSION, ONE GAME, ONLINE -- the scorecard the SERVER keeps, not the one we compute.

SEAT-SIDE. The agent does not import this, exactly as it does not import `arc_holdout`.

WHY IT IS SEPARATE. `arc_holdout` is OFFLINE by default, and its own header records that the
scorecard has been LOCAL in every mode it has ever run under: *"the `session.post` path is
`ONLINE`/`COMPETITION` only. Nothing was ever posted."* So every `levels_completed` this project
has read came off a frame the LOCAL wrapper produced. This asks `https://three.arcprize.org`
instead, and reports the two side by side.

IT REFUSES RATHER THAN FALLS BACK, AND THAT IS THE POINT. A LOCAL scorecard reported as an
ONLINE one is worse than no reading: it is a check that passes because of something it does not
control, and it would make a zero look confirmed by an independent party when nothing
independent happened. Every precondition is asserted BEFORE the game is made, and the run dies
rather than degrade.

SLOW BY CONSTRUCTION. Every step is a network call where OFFLINE was ~2,420/s. One session, one
game; this is not a sweep and must not become one.
"""
from __future__ import annotations

import json
import os
import sys
import time

REMOTE = "https://three.arcprize.org"


def _require_online():
    """Every reason this run could silently become local, checked before anything is made."""
    key = os.getenv("ARC_API_KEY", "").strip()
    if not key:
        sys.exit("REFUSED: ARC_API_KEY is not set. ONLINE needs it, and falling back to a "
                 "LOCAL scorecard would report a number nothing independent produced.")
    mode = os.getenv("OPERATION_MODE", "").strip().lower()
    if mode not in ("online", "competition"):
        sys.exit(f"REFUSED: OPERATION_MODE is {mode or '<unset>'!r}; it must be 'online' "
                 f"(or 'competition'). Under any other mode the scorecard is LOCAL.")
    return key, mode


def run(game: str = "ls20", cycles: int = 40, out: str | None = None) -> dict:
    key, mode = _require_online()
    from arc_agi import Arcade, OperationMode

    arc = Arcade(operation_mode=OperationMode(mode), arc_api_key=key)

    # POSITIVE proof of remoteness, not an absence of evidence of localness.
    assert arc.operation_mode in (OperationMode.ONLINE, OperationMode.COMPETITION), \
        f"constructed mode is {arc.operation_mode}"
    assert arc.arc_base_url.startswith("https://"), f"base url is {arc.arc_base_url!r}"
    assert arc.arc_api_key, "the Arcade carries no api key"
    remote = arc.arc_base_url

    import arc_holdout

    t0 = time.time()
    report = arc_holdout.play(game, cycles=cycles, arc=arc)
    wall = time.time() - t0

    # make() creates the default scorecard on the Arcade it is called on -- which is ours.
    card_id = getattr(arc, "_default_scorecard_id", None)
    if not card_id:
        sys.exit("REFUSED TO REPORT: no scorecard id after play(), so nothing was ever posted. "
                 "The run happened; its result is NOT server-confirmed and is not printed as "
                 "though it were.")

    closed = arc.close_scorecard(card_id)
    fetched = None
    try:
        fetched = arc.get_scorecard(card_id)
    except Exception as e:                       # a closed card may refuse a GET; not fatal
        fetched = f"get_scorecard raised {type(e).__name__}: {e}"

    server = closed if closed is not None else fetched
    runs = []
    if hasattr(server, "environments"):
        for envlist in server.environments:
            for r in envlist.runs:
                runs.append({"guid": getattr(r, "guid", None), "score": r.score,
                             "levels_completed": r.levels_completed, "actions": r.actions,
                             "state": str(getattr(r, "state", None)),
                             "number_of_levels": getattr(r, "number_of_levels", None)})

    result = {
        "game": game, "cycles": cycles, "mode": mode, "base_url": remote,
        "card_id": card_id, "wall_s": round(wall, 1),
        "server_score": getattr(server, "score", None),
        "server_runs": runs,
        "local_report": report,
    }
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=1, default=str)
    return result


def _print(r: dict) -> None:
    print(f"game {r['game']}  cycles {r['cycles']}  mode {r['mode']}  {r['base_url']}")
    print(f"card {r['card_id']}  wall {r['wall_s']}s")
    print()
    print("SERVER (independent of anything this repo computes)")
    print(f"  scorecard score : {r['server_score']}")
    for x in r["server_runs"]:
        print(f"  run {x['guid']}: levels_completed={x['levels_completed']} "
              f"score={x['score']} actions={x['actions']} state={x['state']} "
              f"of {x['number_of_levels']} levels")
    if not r["server_runs"]:
        print("  (no runs on the card)")
    print()
    print("LOCAL (what this repo has been reading all along)")
    loc = r["local_report"]
    for k in ("levels", "levels_completed", "stopped", "cycles"):
        if k in loc:
            print(f"  {k}: {loc[k]}")
    print()
    print("THE TWO ARE NOT SUMMED AND NOT AVERAGED. They are two readings of one session, and "
          "a disagreement between them is the finding.")


if __name__ == "__main__":
    g = sys.argv[1] if len(sys.argv) > 1 else "ls20"
    c = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    _print(run(g, c, out=f"runs/online_{g}.json"))
