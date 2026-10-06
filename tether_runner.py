"""THE K-WORKER RUNNER -- the sequence that lets a library carry (decision 3; F471-F472).

The kit's Swarm (`agents/swarm.py`) starts every game's thread at once, so under it there is no
"next game" and nothing can carry. Here K worker PROCESSES each play an ordered list of games and
carry ITS OWN library file from one to the next. Every worker starts from the same frontloaded
priors (an empty library over the same atoms); libraries are never shared or merged.

NOTHING ON THE SCORE PATH IS A GUESSED NUMBER -- each is read live:
  K        os.sched_getaffinity(0), else os.cpu_count()
  games    the list the gateway serves (GET /api/games), assigned by ORDER, never by identity
  time     CEILING_S below, from ARC's own sample notebook; each game's allowance is computed live
           as (time left before the ceiling - MARGIN_S) / (games this worker has left)

Scored through the official calls, as Swarm does: one card opened here, each game made with
`make(game, scorecard_id=card)` in its worker, the card closed after every worker joins.
"""
from __future__ import annotations

import json
import multiprocessing as mp
import os
import sys
import time

import tether_agent

sys.dont_write_bytecode = True

# SOURCE: docs/example/arc3-sample-submission-stochastic-goose.ipynb -- "Check if 8 hours have
# elapsed since start." `(time.time() - self.start_time) >= 8 * 3600 - 5 * 60`. That sample times
# PER AGENT (one per game, all concurrent); our workers are sequential, so it is applied RUN-WIDE
# from the runner's start -- the safe reading.
CEILING_S = 8 * 3600 - 5 * 60
# anchor: a declared margin for saving and closing the card before the ceiling, not a tuned value.
MARGIN_S = 120
# anchor: a loop bound only -- the live time allowance ends a game, never this number.
MAX_ACTIONS_PER_GAME = 10_000_000


def cores() -> int:
    try:
        return len(os.sched_getaffinity(0))
    except AttributeError:
        return os.cpu_count() or 1


def assign(games: list[str], k: int) -> list[list[str]]:
    """Round-robin BY ORDER: worker i plays games i, i+k, i+2k ... -- never by a game's identity."""
    return [games[i::k] for i in range(k)]


def worker(i: int, games: list[str], card: str, lib_dir: str, deadline: float, make, out: str,
           margin_s: float = MARGIN_S):
    """One worker: its games in order, its own library carried from each game to the next."""
    lib = os.path.join(lib_dir, f"worker{i}.json")
    rows = []
    for n, game in enumerate(games):
        left = deadline - margin_s - time.time()
        if left <= 0:
            rows.append({"game": game, "end": "unplayed: ceiling reached", "loaded": False})
            continue
        allowance = left / (len(games) - n)
        rep = tether_agent.run(make(game, card), game, MAX_ACTIONS_PER_GAME, library=lib,
                               deadline=time.time() + allowance)
        rows.append({k: rep[k] for k in ("game", "end", "acted", "cycles", "levels")}
                    | {"allowance_s": round(allowance, 1), "loaded": bool(rep.get("loaded"))})
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"worker": i, "library": lib, "games": rows}, fh, indent=1)


def run(games: list[str], card: str, make, lib_dir: str, k: int | None = None,
        start: float | None = None, processes: bool = True, ceiling_s: float = CEILING_S,
        margin_s: float = MARGIN_S) -> dict:
    """Assign, start K workers, join them, return the run record. `make(game, card)` builds a
    game's wrapper inside the worker; it must be module-level so a process can take it."""
    k = k or cores()
    start = time.time() if start is None else start
    deadline = start + ceiling_s
    os.makedirs(lib_dir, exist_ok=True)
    parts = assign(games, min(k, len(games)) or 1)
    outs = [os.path.join(lib_dir, f"worker{i}.record.json") for i in range(len(parts))]
    if processes:
        procs = [mp.Process(target=worker,
                            args=(i, g, card, lib_dir, deadline, make, o, margin_s))
                 for i, (g, o) in enumerate(zip(parts, outs, strict=True))]
        for p in procs:
            p.start()
        for p in procs:
            p.join()
    else:
        for i, (g, o) in enumerate(zip(parts, outs, strict=True)):
            worker(i, g, card, lib_dir, deadline, make, o, margin_s)
    records = []
    for o in outs:
        try:
            with open(o, encoding="utf-8") as fh:
                records.append(json.load(fh))
        except (OSError, ValueError) as e:
            records.append({"record": o, "missing": f"{type(e).__name__}: {e}"[:200]})
    return {"k": k, "workers": len(parts), "games": len(games), "ceiling_s": ceiling_s,
            "margin_s": margin_s, "records": records}


def serve(fetch_games, open_card, close_card, make, lib_dir: str, **kw) -> dict:
    """The official scoring path, as Swarm does it: the games the gateway serves, ONE card opened,
    every game made with it in the workers, the card closed once after they all join -- closed
    even if a worker fails, so the gateway is never left holding an open card."""
    games = list(fetch_games())
    card = open_card()
    try:
        rec = run(games, card, make, lib_dir, **kw)
    finally:
        closed = close_card(card)
    return rec | {"card": card, "closed": closed is not False}
