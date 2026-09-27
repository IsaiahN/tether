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
CARD_FILE = "runs/online_card_id.txt"
CLOSE_FILE = "runs/online_scorecard.json"


_CLOSED: dict = {}


def _close_direct(card_id: str, key: str, base: str) -> dict:
    """Close by the DOCUMENTED request rather than through the wrapper.

    `docs.arcprize.org`: POST /api/scorecard/close, `X-API-Key`, body {"card_id": ...}, and a
    scorecard is NOT tied to the session that opened it. The wrapper's own close 404s from a
    fresh Arcade where this succeeds, so the documented call is the one used.
    """
    import requests
    r = requests.post(f"{base}/api/scorecard/close",
                      headers={"X-API-Key": key, "Accept": "application/json"},
                      json={"card_id": card_id}, timeout=30)
    r.raise_for_status()
    out = r.json()
    _CLOSED[card_id] = out
    # PERSIST THE CLOSE RESPONSE IMMEDIATELY. The card itself becomes unreachable -- GET 404s
    # after the fact, and a card that was 200 seconds earlier 404s later -- so the close body is
    # the ONLY durable copy of the server's own record. Fetching it later is not an option.
    with open(CLOSE_FILE, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, default=str)
    print(f"scorecard {card_id} CLOSED -- server record saved to {CLOSE_FILE}")
    for e in out.get("environments", []):
        print(f"  SERVER {e.get('id')}: levels_completed={e.get('levels_completed')} "
              f"of level_count={e.get('level_count')} actions={e.get('actions')} "
              f"completed={e.get('completed')}")
    return out


def _load_env() -> None:
    """Read `.env` from the repo root (gitignored, untracked) if the var is not already set.

    THE KEY IS REFERENCED AND NEVER COPIED. Not printed, not written to any artifact, and passed
    to nothing but the Arcade constructor. A real environment variable still wins.
    """
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(p):
        return
    with open(p, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if k and not os.getenv(k):
                os.environ[k] = v


def _require_online():
    """Every reason this run could silently become local, checked before anything is made."""
    _load_env()
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

    # THE CARD ID IS WRITTEN THE MOMENT IT EXISTS, BEFORE A SINGLE CYCLE RUNS.
    # It lives only in this process's memory and the API has no list endpoint, so a run that
    # is interrupted leaves a card NOBODY CAN CLOSE -- not even by hand. Opening the card here
    # rather than letting make() do it is what makes the id recoverable.
    card_id = arc.open_scorecard(tags=["tether", "seat", game])
    arc._default_scorecard_id = card_id
    with open(CARD_FILE, "w", encoding="utf-8") as f:
        f.write(card_id)
    print(f"scorecard {card_id} OPEN -- id written to {CARD_FILE} before play starts")

    # CLOSED IN A finally: an interrupted run must still close its card. The recovery script
    # exists too, but a card that closes itself is one fewer thing to remember.
    t0 = time.time()
    try:
        report = arc_holdout.play(game, cycles=cycles, arc=arc, stop_on_end=True)
    finally:
        wall = time.time() - t0
        try:
            _close_direct(card_id, arc.arc_api_key, remote)
        except Exception as e:
            print(f"close failed: {type(e).__name__}: {e}")

    if not card_id:
        sys.exit("REFUSED TO REPORT: no scorecard id after play(), so nothing was ever posted. "
                 "The run happened; its result is NOT server-confirmed and is not printed as "
                 "though it were.")

    server = _CLOSED.get(card_id) or {}
    runs = []
    for e in server.get("environments", []):
        runs.append({"env": e.get("id"), "levels_completed": e.get("levels_completed"),
                     "level_count": e.get("level_count"), "actions": e.get("actions"),
                     "completed": e.get("completed"), "resets": e.get("resets")})

    result = {
        "game": game, "cycles": cycles, "mode": mode, "base_url": remote,
        "card_id": card_id, "wall_s": round(wall, 1),
        "server_score": server.get("score"),
        "server_runs": runs,
        # THE UNIT IS ACTIONS AND THE ENDING, NOT CYCLES. play() has no break on terminal --
        # after the first GAME_OVER every further cycle is a no-op -- so "one game" is read
        # off `endings`, and a run with no ending never finished the game.
        "endings": report.get("endings", {}),
        "actions": (report.get("budget") or {}).get("spent"),
        "game_ended": bool(report.get("endings")),
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
    print(f"  game_ended : {r['game_ended']}   endings: {r['endings']}")
    print(f"  actions    : {r['actions']}   cycles requested: {r['cycles']}")
    loc = r["local_report"]
    for k in ("levels",):
        if k in loc:
            print(f"  {k}: {loc[k]}")
    print()
    print("THE TWO ARE NOT SUMMED AND NOT AVERAGED. They are two readings of one session, and "
          "a disagreement between them is the finding.")


if __name__ == "__main__":
    g = sys.argv[1] if len(sys.argv) > 1 else "ls20"
    c = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    _print(run(g, c, out=f"runs/online_{g}.json"))
