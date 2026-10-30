"""Read-only (the reviewer r280 item 1): PLAY16's across-round table, one row per finished round, from chain.log,
each round's switch.tsv and one pass over its stream.jsonl. Prints a TSV table then trend lines. argv: first last."""
import json
import re
import sys

sys.dont_write_bytecode = True
import os
P = os.environ.get("PLAY", "C:/TETHER_RUNS/S6_2026-10-19/PLAY16")
first, last = int(sys.argv[1]), int(sys.argv[2])
chain = open(f"{P}/chain.log", encoding="utf-8").read().splitlines()


def line(pat):
    return next((ln for ln in chain if re.search(pat, ln)), "")


EV = re.compile(r'"event": "(level_up|mint|settle|reuse_install|frame_break|step_mint|mint_deferred|step_derived)"')
rows = []
for n in range(first, last + 1):
    rd = f"{P}/round_{n:02d}"
    st = line(rf"ROUND {n} START ")
    run = line(rf"ROUND {n} RUN rc ")
    wc = line(rf"ROUND {n} WRITE_CHECK ")
    end = line(rf"ROUND {n} END ")
    if not end:
        continue
    seed = re.search(r"seed (\w+)", st).group(1)
    wall = int(re.search(r"wall (\d+) s", run).group(1))
    rc = re.search(r"RUN rc (\S+)", run).group(1)
    names = int(re.search(r"names (\d+)", wc).group(1))
    lbytes = int(re.search(r"lineage_bytes (\d+)", wc).group(1))
    faults = int(re.search(r"agent_fault events (\d+)", end).group(1))
    games = []
    for ln in open(f"{rd}/switch.tsv", encoding="utf-8"):
        f = ln.rstrip("\n").split("\t")
        if len(f) > 14 and f[0].isdigit():
            games.append({"pos": int(f[0]), "game": f[1], "c0": int(f[3]), "steps": int(f[5]),
                          "levels": int(f[6]), "first": None if f[14] == "None" else float(f[14])})
    games.sort(key=lambda g: g["c0"])
    c0s = [g["c0"] for g in games]

    def game_at(c):
        k = None
        for i, c0 in enumerate(c0s):
            if c >= c0:
                k = i
        return k
    cnt = {k: 0 for k in ("level_up", "mint", "settle", "reuse_install", "step_mint", "mint_deferred")}
    fb_cycles, lvl_games, sd_last = set(), set(), {}
    for ln in open(f"{rd}/stream.jsonl", encoding="utf-8"):
        m = EV.search(ln)
        if not m:
            continue
        e = m.group(1)
        if e in cnt:
            cnt[e] += 1
        if e in ("frame_break", "level_up", "step_derived"):
            try:
                r = json.loads(ln)
            except ValueError:
                continue
            c = r.get("cycle")
            if e == "frame_break":
                fb_cycles.add(c)
            elif e == "level_up":
                gi = game_at(c)
                if gi is not None:
                    lvl_games.add(games[gi]["game"])
            else:
                gi = game_at(c)
                if gi is not None:
                    sd_last[gi] = (r.get("detail") or {}).get("derived_deferred", 0)
    switches = [g for g in games if g["pos"] != min(x["pos"] for x in games)]
    missed = [f"{g['game']}@{g['pos']}" for g in switches if g["c0"] not in fb_cycles]
    bp = next((g for g in games if g["game"] == "bp35"), None)
    steps = sum(g["steps"] for g in games)
    lv_tsv = sum(g["levels"] for g in games)
    owed_max = max(sd_last.values()) if sd_last else 0
    owed_game = games[max(sd_last, key=sd_last.get)]["game"] if sd_last else "-"
    rows.append(dict(n=n, seed=seed, rc=rc, wall=wall, games=len(games), steps=steps,
                     spm=round(steps / (wall / 60), 2), lvl_up=cnt["level_up"], lvl_tsv=lv_tsv,
                     lvl_games=",".join(sorted(lvl_games)) or "-", mints=cnt["mint"], settle=cnt["settle"],
                     reuse=cnt["reuse_install"], names=names, lbytes=lbytes,
                     fb=f"{len(switches) - len(missed)}/{len(switches)}", missed=",".join(missed) or "-",
                     bp35=f"{bp['first']}@{bp['pos']}" if bp else "-",
                     sm=cnt["step_mint"], md=cnt["mint_deferred"], owed=f"{owed_max}({owed_game})", faults=faults))
    print(f"# scanned round {n}", file=sys.stderr, flush=True)
cols = ["n", "seed", "rc", "wall", "games", "steps", "spm", "lvl_up", "lvl_tsv", "lvl_games", "mints", "settle", "reuse",
        "names", "lbytes", "fb", "missed", "bp35", "sm", "md", "owed", "faults"]
print("\t".join(cols))
for r in rows:
    print("\t".join(str(r[c]) for c in cols))
