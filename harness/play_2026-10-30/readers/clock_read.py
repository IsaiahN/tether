"""Read-only (the reviewer r265 item 7): PLAY16's per-game clock columns from a finished round's stream.
Per game (switch.tsv order): the step's phase split (mean wall_s per scope over the game's REPEAT rows, and step
1's split), trace_len / wants_n / owed_import_n at the game's first and last REPEAT row, gamma_reuse_live /
gamma_reuse_on_board at its first; then Spearman of each against first action and against position, n stated.
argv: PLAY dir name, round dir name."""
import json
import sys

sys.dont_write_bytecode = True


def ranks(xs):    # pos_read.py's, copied: importing pos_read runs its main
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(x, y):
    rx, ry = ranks(x), ranks(y)
    n = len(x)
    mx, my = sum(rx) / n, sum(ry) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry, strict=True))
    vx = sum((a - mx) ** 2 for a in rx) ** 0.5
    vy = sum((b - my) ** 2 for b in ry) ** 0.5
    return cov / (vx * vy) if vx and vy else float("nan")


B = (sys.argv[1] if ":" in sys.argv[1] else f"C:/TETHER_RUNS/S6_2026-10-19/{sys.argv[1]}") + f"/{sys.argv[2]}"
KEYS = ("trace_len", "wants_n", "owed_import_n", "gamma_reuse_live", "gamma_reuse_on_board")
games = []
for ln in open(f"{B}/switch.tsv", encoding="utf-8"):
    f = ln.rstrip("\n").split("\t")
    if len(f) > 14 and f[0].isdigit():
        games.append({"pos": int(f[0]), "game": f[1], "c0": int(f[3]),
                      "first": None if f[14] == "None" else float(f[14])})
games.sort(key=lambda g: g["c0"])
for i, g in enumerate(games):
    g["c1"] = games[i + 1]["c0"] if i + 1 < len(games) else None
rep, sdr, dasked, dexh = [], [], {}, {}
fbreak, match1 = set(), {}
for ln in open(f"{B}/stream.jsonl", encoding="utf-8"):
    if not any(t in ln for t in ('"event": "repeat"', '"event": "step_derived"', '"event": "frame_break"',
                                 '"event": "matches"', '"event": "derived_asked"', '"event": "park"')):
        continue
    if '"event": "frame_break"' in ln or '"event": "matches"' in ln:
        try:
            r = json.loads(ln)
        except ValueError:
            continue
        if r.get("event") == "frame_break":
            fbreak.add(r["cycle"])
        elif r["cycle"] not in match1 or not match1[r["cycle"]].get("broke"):
            calls = (r.get("detail") or {}).get("calls") or []
            hit = next((c for c in calls if c.get("broke")), None)   # the call that broke, else the first
            if hit is not None or (calls and r["cycle"] not in match1):
                match1[r["cycle"]] = dict(hit or calls[0], calls_n=len(calls))
        continue
    try:
        r = json.loads(ln)
    except ValueError:
        continue
    d, e, c = r.get("detail") or {}, r.get("event"), r.get("cycle")
    if e == "repeat" and "wall_s" in d:
        rep.append((c, d))
    elif e == "step_derived":
        sdr.append((c, d))
    elif e == "derived_asked" and not d.get("echo"):
        dasked.setdefault(c, set()).add(r["slot"])
    elif e == "park" and r["slot"] in dasked.get(c, ()):
        dexh.setdefault(c, [0, 0])
        dexh[c][0] += 1
        dexh[c][1] += bool(d.get("budget_exhausted"))
print(f"REPEAT rows with clock fields: {len(rep)}")
if not rep:
    sys.exit("no clock rows: this round ran without TETHER_STEP_CLOCK (or no step ended)")
cols = {}
print("pos game first | steps | mean wall_s by scope (other, total) | step 1 split | start->end trace wants owed | "
      "reuse live/on_board at start")
for g in sorted(games, key=lambda g: g["pos"]):
    rows = [d for c, d in rep if c >= g["c0"] and (g["c1"] is None or c < g["c1"])]
    if not rows:
        print(f"{g['pos']:>2} {g['game']} {g['first']} | 0 REPEAT rows")
        continue
    scopes = sorted({k for d in rows for k in d["wall_s"]})
    mean = {k: round(sum(d["wall_s"].get(k, 0.0) for d in rows) / len(rows), 2) for k in scopes}
    s1 = {k: round(v, 2) for k, v in rows[0]["wall_s"].items()}
    a, z = rows[0], rows[-1]
    print(f"{g['pos']:>2} {g['game']} {g['first']} | {len(rows)} | {mean} | {s1} | "
          f"{a['trace_len']}->{z['trace_len']} {a['wants_n']}->{z['wants_n']} "
          f"{a['owed_import_n']}->{z['owed_import_n']} | {a['gamma_reuse_live']}/{a['gamma_reuse_on_board']}")
    inside = (lambda c: c >= g["c0"] and (g["c1"] is None or c < g["c1"]))
    gs = [d for c, d in sdr if inside(c)]
    ex = [v for c, v in dexh.items() if inside(c)]
    minted, exhausted = sum(v[0] for v in ex), sum(v[1] for v in ex)
    m1 = match1.get(g["c0"]) or {}
    s1d = next((d for c, d in sdr if c == g["c0"]), None)
    print(f"     switch: frame_break {'yes' if g['c0'] in fbreak else 'NO'}; matches call (the breaking one, "
          f"else the first, of {m1.get('calls_n')}) found "
          f"{m1.get('found')} claimed {m1.get('claimed')} median {m1.get('median')} colour_share "
          f"{m1.get('colour_share')} broke {m1.get('broke')}; step 1 B2: "
          + (f"run {s1d['derived_run']} deferred (owed after) {s1d['derived_deferred']} dropped "
             f"{s1d['owed_dropped']} stop_from_accept {s1d['stop_from_accept']}" if s1d else "no step_derived row"))
    print(f"     B2: derived_run {sum(d['derived_run'] for d in gs)} deferred "
          f"{sum(d['derived_deferred'] for d in gs)} owed_dropped {sum(d['owed_dropped'] for d in gs)}"
          f"; owed at game end {gs[-1]['derived_deferred'] if gs else 0}; derived mints exhausting "
          f"{exhausted}/{minted}")
    row = {f"start_{k}": a.get(k) for k in KEYS}
    row.update({f"mean_{k}": v for k, v in mean.items()})
    row.update({f"step1_{k}": v for k, v in s1.items()})
    for k, v in row.items():
        cols.setdefault(k, []).append((g["pos"], g["first"], v))
print("== Spearman per column; n = games with a value and a first action")
for k in sorted(cols):
    t = [(p, f, v) for p, f, v in cols[k] if isinstance(v, (int, float)) and f is not None]
    if len(t) < 5:
        print(f"  {k}: too few values ({len(t)})")
        continue
    vs = [v for _p, _f, v in t]
    print(f"  {k}: n {len(t)} min {min(vs)} max {max(vs)}; vs first action "
          f"{spearman(vs, [f for _p, f, _v in t]):+.2f}; vs position {spearman([p for p, _f, _v in t], vs):+.2f}")
