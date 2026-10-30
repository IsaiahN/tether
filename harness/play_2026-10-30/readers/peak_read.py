"""r442 (a READ): WHEN a round's memory peak lands. sup/mem.tsv (10 s samples of each process's private MB, from the
supervisor's start) -> the sample with the largest private MB, the game playing then (switch.tsv wall_start_s, which
counts from the stream's start: the offset is read from sup.log's start and switch.tsv's '# stream start'), whether it
is before or after a fault_recovered row, and dormant_held from the last arrival_alias row in or before that game. Also
the per-game peak, so a late-round rise is told from one game's spike. argv: round dir."""
import datetime as dt
import json
import os
import re
import sys

sys.dont_write_bytecode = True
O = sys.argv[1]
mem = [ln.split("\t") for ln in open(os.path.join(O, "sup", "mem.tsv"), encoding="utf-8").read().splitlines()[1:]]
mem = [(int(t), int(p), int(m)) for t, p, m, *_ in mem if m.strip().isdigit()]
sup0 = re.search(r"^(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) start", open(os.path.join(O, "sup", "sup.log"), encoding="utf-8").read(),
                 re.M).group(1)
sw = open(os.path.join(O, "switch.tsv"), encoding="utf-8").read().splitlines()
st0 = re.search(r"stream start (\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)", sw[0]).group(1)
off = (dt.datetime.fromisoformat(st0) - dt.datetime.fromisoformat(sup0)).total_seconds()
games = []
for ln in sw:
    if ln.startswith("#"):
        continue
    f = ln.split("\t")
    games.append((f[1], float(f[2]) + off, float(f[2]) + float(f[4]) + off, int(f[3]), int(f[3]) + int(f[5]) - 1))
aa, rec = [], None
for ln in open(os.path.join(O, "stream.jsonl"), encoding="utf-8"):
    if '"arrival_alias"' in ln or '"fault_recovered"' in ln:
        r = json.loads(ln)
        if r["event"] == "arrival_alias":
            aa.append((r["cycle"], r["detail"].get("dormant_held"), r["detail"].get("held")))
        elif r["event"] == "fault_recovered" and rec is None:
            rec = r["cycle"]


def game_at(t):
    return next((g for g in games if g[1] <= t <= g[2]), None)


t, pid, mb = max(mem, key=lambda x: x[2])
g = game_at(t)
dh = [a for a in aa if g and a[0] <= g[4]]
print(f"== {O}: peak private {mb} MB ({mb / 1024:.2f} GiB) at t={t} s (pid {pid}); game {g[0] if g else None} "
      f"(cycles {g[3] if g else '?'}-{g[4] if g else '?'}); fault_recovered at cycle {rec} -> peak "
      f"{'after' if rec is not None and g and g[3] >= rec else 'before' if rec is not None else 'no recovery'}; "
      f"dormant_held then {dh[-1][1] if dh else None} (row c{dh[-1][0] if dh else None}, held {dh[-1][2] if dh else None})")
print("  per game peak private MB: " + " ".join(
    f"{g[0]}:{max((m for tt, _p, m in mem if g[1] <= tt <= g[2]), default=0)}" for g in games))
