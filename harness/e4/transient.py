"""FIRST-SLICE TRANSIENT per E4a game (the reviewer 2026-10-18 23:55 item 4b; 2026-10-19 00:04 items 1-3): the commit
rise inside the window an E4b slice of the same game would cover, from each game's 10 s sampler, PER GAME, never
pooled. READ ONLY. ALL TIMES ARE SECONDS AFTER PLAY START, except play_start_s itself (seconds after module start).
  play_start_s  result.json's play_start_s; for a game with no result.json (a supervisor stop or an error) the last
                sampler row with 0 moves (the load is over by then, the first move in flight: a LATE start)
  base_mib      the sampler commit at play start (nearest row)
  slice_s       e4b_estimate's slice_replay_s: the end of the first move whose end is >= SL, E4a's moves replayed
  rise_mib      the largest sampler commit in [0, slice_s] minus base_mib, and in GiB (/1024)
  big_rise_mib  the game's largest in-move rise (load excluded); big_from_s the start of that move
  where         in_slice (it starts before slice_s) / NEAR (it starts 0-60 s after slice_s: a RISK line) / after
With --order SEED --start GIB --slope GIB the (b') table: position k in the seed's order, R(k) = start + (k-1) x
slope, R(k) + T(k) against 25.1 GiB, and R(k) + big_rise for each NEAR game (the risk lines); (a) R(25) <= 20.
argv: e4_dir [--slice S] [--order SEED --start GIB --slope GIB --games DIR]"""
import argparse
import contextlib
import glob
import io
import json
import os
import random
import sys

sys.dont_write_bytecode = True
ap = argparse.ArgumentParser()
ap.add_argument("e4")
ap.add_argument("--slice", type=float, default=120.0)
ap.add_argument("--order", default=None)
ap.add_argument("--start", type=float, default=None)
ap.add_argument("--slope", type=float, default=None)
ap.add_argument("--games", default=None)       # environment_files, for the order (e4_stream sorts its listing)
ap.add_argument("--near", type=float, default=60.0)
ap.add_argument("--line", type=float, default=25.1)
A = ap.parse_args()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = [sys.argv[0], A.e4, str(A.slice)]
with contextlib.redirect_stdout(io.StringIO()):
    import e4b_estimate as est  # noqa: E402  (it prints its own table at import)

rows = {}
print("idx\tgame\tplay_start_s\tstart_from\tbase_mib\tslice_s\trise_mib\trise_gib\tbig_rise_mib\tbig_rise_gib\t"
      "big_from_s\twhere\tkept_mib_at_slice_end")
for d in sorted(glob.glob(os.path.join(A.e4, "public", "[0-9][0-9]_*"))):
    idx, g = os.path.basename(d).split("_", 1)
    try:
        with open(os.path.join(d, f"{g}.commit.tsv"), encoding="utf-8") as fh:
            smp = [(float(a), int(b), int(c)) for a, b, c in
                   (ln.rstrip("\n").split("\t")[:3] for ln in fh if ln.strip())]
    except OSError:
        print(f"{idx}\t{g}\tNO SAMPLER")
        continue
    ps = None
    try:
        with open(os.path.join(d, f"{g}.result.json"), encoding="utf-8") as fh:
            ps = json.load(fh).get("play_start_s")
    except (OSError, ValueError):
        pass
    if ps is not None:
        start, src = float(ps), "play_start_s"
    else:
        start, src = max((t for t, _m, n in smp if n == 0), default=smp[0][0]), "last 0-move row"
    base = min(smp, key=lambda r: abs(r[0] - start))[1]
    moves, _ = est.moves_of(d, g)
    t, rep = 0.0, None
    for x in moves:
        t += x
        if t >= A.slice:
            rep = t
            break
    rep = rep if rep is not None else t
    win = [r for r in smp if start <= r[0] <= start + rep]
    rise = max(r[1] for r in win) - base if win else None
    kept = min(smp, key=lambda r: abs(r[0] - (start + rep)))[1] - base   # the sampler row nearest the slice end
    best, bt0, pm, m0, t0 = 0, None, None, None, None
    for tt, mm, nn in smp:
        if nn != pm:
            pm, m0, t0 = nn, mm, tt
        elif nn > 0 and mm - m0 > best:
            best, bt0 = mm - m0, t0
    frm = None if bt0 is None else round(bt0 - start, 1)
    if frm is None:
        where = None
    elif frm < rep:                      # a move that STARTS at the slice end is outside it
        where = "in_slice"
    elif frm - rep <= A.near:
        where = "NEAR"
    else:
        where = "after"
    rows[g] = (rise, best, where)
    print(f"{idx}\t{g}\t{round(start, 1)}\t{src}\t{base}\t{round(rep, 1)}\t{rise}\t"
          f"{round(rise / 1024, 2) if rise is not None else None}\t{best}\t{round(best / 1024, 2)}\t{frm}\t{where}\t"
          f"{kept}")
worst = max(((g, r[0]) for g, r in rows.items() if r[0] is not None), key=lambda x: x[1])
print(f"# slice {A.slice} s; worst first-slice rise: {worst[0]} {worst[1]} MiB = {round(worst[1] / 1024, 2)} GiB; "
      f"games {len(rows)}")

if A.order:
    games = sorted(os.listdir(A.games))
    assert len(games) == 25, games
    order = random.Random(A.order).sample(games, len(games))
    print(f"\n# (b') seed {A.order}, start {A.start} GiB, slope {A.slope} GiB per switch, line {A.line} GiB")
    print("k\tgame\tR_gib\tT_gib\tR+T\tpass\tnear_risk_R+big")
    tight = None
    for k, g in enumerate(order, 1):
        r = A.start + (k - 1) * A.slope
        rise, best, where = rows.get(g, (None, None, None))
        tt = rise / 1024 if rise is not None else None
        tot = r + tt if tt is not None else None
        risk = f"{round(r + best / 1024, 2)} ({'FAILS' if r + best / 1024 > A.line else 'ok'})" if where == "NEAR" else ""
        print(f"{k}\t{g}\t{round(r, 2)}\t{round(tt, 2) if tt is not None else None}\t"
              f"{round(tot, 2) if tot is not None else None}\t{None if tot is None else tot <= A.line}\t{risk}")
        if tot is not None and (tight is None or A.line - tot < tight[2]):
            tight = (k, g, A.line - tot)
    r25 = A.start + 24 * A.slope
    print(f"# tightest (b') row: k {tight[0]} {tight[1]}, margin {round(tight[2], 2)} GiB; "
          f"(a) R(25) = {round(r25, 2)} GiB, {'pass' if r25 <= 20 else 'FAILS'}")
