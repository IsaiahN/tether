"""E4b's expected wall from E4a's measured moves, PER GAME (the reviewer 14:24; 17:04: over 2 h comes first;
18:03 the floor max(120 s, first move); 18:12 the seat's estimate is THE estimate; 23:02: price the in-flight
overrun from each game's MOVE-LENGTH distribution, p50 / p90 / max). Read only.

E4b's driver steps while (now - slice start) < SL and never cuts a move, so a slice ends at the end of the
first move that STARTS at or after SL... precisely: it ends when a move ends at or after SL. Replaying a game's
E4a move list from its own start gives that game's slice:
  slice_replay_s  the cumulative end of the first move whose end is >= SL (the moves as E4a played them)
  floor_s         max(SL, first move) (the reviewer's floor)
Moves per game: result.json step_s; for a game the supervisor stopped (no result.json), the move ENDS read from
its 10 s commit sampler, the last move counted as running to the stop (a lower bound on its length).
E4b's one life loads no chain per game, so no load term (stated, not measured).
argv: e4_dir [slice_s]"""
import glob
import json
import os
import sys

E4 = sys.argv[1]
SL = float(sys.argv[2]) if len(sys.argv) > 2 else 120.0


def moves_of(d, g):
    try:
        with open(os.path.join(d, f"{g}.result.json"), encoding="utf-8") as fh:
            return [x for x in json.load(fh).get("step_s") or [] if x], "result.json"
    except (OSError, ValueError):
        pass
    try:
        with open(os.path.join(d, f"{g}.commit.tsv"), encoding="utf-8") as fh:
            rows = [ln.split("\t") for ln in fh]
    except OSError:
        return [], "none"
    rows = [(float(r[0]), int(r[2])) for r in rows if len(r) >= 3]
    t0 = max((t for t, m in rows if m == 0), default=0.0)       # the load ends near here
    ends, seen = [], 0
    for t, m in rows:
        while seen < m:
            ends.append(t)
            seen += 1
    last_t = rows[-1][0] if rows else t0
    out, prev = [], t0
    for e in ends:
        out.append(max(0.1, e - prev))
        prev = e
    out.append(max(0.1, last_t - prev))         # the move in flight at the stop, to the stop
    return out, "sampler (supervisor stop; last move to the stop)"


def pct(xs, q):
    s = sorted(xs)
    return s[min(len(s) - 1, int(q * len(s)))]


rows, tot_r, tot_f = [], 0.0, 0.0
for d in sorted(glob.glob(os.path.join(E4, "public", "[0-9][0-9]_*"))):
    g = os.path.basename(d).split("_", 1)[1]
    s, src = moves_of(d, g)
    if not s:
        rows.append((g, None, None, None, None, None, src))
        continue
    t, rep = 0.0, None
    for x in s:
        t += x
        if t >= SL:
            rep = t
            break
    rep = rep if rep is not None else t
    flo = max(SL, s[0])
    tot_r, tot_f = tot_r + rep, tot_f + flo
    rows.append((g, round(pct(s, 0.5), 1), round(pct(s, 0.9), 1), round(max(s), 1), round(rep, 1), round(flo, 1),
                 src))
print("game\tmove_p50_s\tmove_p90_s\tmove_max_s\tslice_replay_s\tfloor_s\tsource")
for r in rows:
    print("\t".join(str(x) for x in r))
n = sum(1 for r in rows if r[4] is not None)
print(f"# games: {n} of {len(rows)}. E4b wall, replay of E4a's moves: {round(tot_r)} s = {round(tot_r / 3600, 2)} h; "
      f"the reviewer's floor: {round(tot_f)} s = {round(tot_f / 3600, 2)} h (slice {SL} s)")
