"""r423 A: a READ of a round's existing rows (no run). Per step, the repeat row's wall_s by phase, split by
whether that cycle carries a contact_first row (by why) / a route_named row, and per game. Means per step,
with the step counts printed. argv: round dir."""
import ast
import collections
import json
import os
import sys

sys.dont_write_bytecode = True
O = sys.argv[1]
PH = ("total", "MINT", "ROUTE", "PERCEIVE", "other", "PLAN")
wall, cf, rn, ind = {}, collections.defaultdict(set), collections.Counter(), collections.Counter()
with open(os.path.join(O, "stream.jsonl"), encoding="utf-8") as fh:
    for line in fh:
        r = json.loads(line)
        e, c = r.get("event"), r.get("cycle")
        if e == "repeat" and isinstance((r.get("detail") or {}).get("wall_s"), dict):
            assert c not in wall, ("two repeat rows on one cycle", c)
            wall[c] = r["detail"]["wall_s"]
        elif e == "contact_first":
            cf[c].add((r.get("detail") or {}).get("why"))
        elif e == "route_named":
            rn[c] += 1
        elif e == "indistinct":
            ind[c] += 1
starts = []
with open(os.path.join(O, "read.out"), encoding="utf-8") as fh:
    for line in fh:
        if line.startswith("SLICE {"):
            s = ast.literal_eval(line[6:].strip())
            starts.append((int(s["cycle_start"]), s["game"]))


def game_of(c):
    g = None
    for c0, gg in sorted(starts):
        if c >= c0:
            g = gg
    return g


def row(name, cs):
    cs = list(cs)
    if not cs:
        print(f"  {name:34s} steps   0")
        return
    m = {p: sum(wall[c].get(p, 0.0) for c in cs) / len(cs) for p in PH}
    print(f"  {name:34s} steps {len(cs):3d}  " + "  ".join(f"{p} {m[p]:6.1f}" for p in PH))


cs = sorted(wall)
print(f"STEPS {len(cs)} (repeat rows with wall_s); contact_first cycles {len(cf)}, route_named cycles {len(rn)}, "
      f"indistinct cycles {len(ind)}")
first = {c0 for c0, _g in starts}
print("PER STEP MEANS, s:")
row("all", cs)
row("contact_first any", [c for c in cs if c in cf])
row("contact_first named", [c for c in cs if "named" in cf.get(c, ())])
row("contact_first same_rows", [c for c in cs if "same_rows" in cf.get(c, ())])
row("no contact_first", [c for c in cs if c not in cf])
row("route_named", [c for c in cs if c in rn])
row("no route_named", [c for c in cs if c not in rn])
row("both", [c for c in cs if c in cf and c in rn])
row("neither", [c for c in cs if c not in cf and c not in rn])
row("a game's first step", [c for c in cs if c in first])
row("not a game's first step", [c for c in cs if c not in first])
row("not first, no cf, no rn", [c for c in cs if c not in first and c not in cf and c not in rn])
row("not first, cf or rn", [c for c in cs if c not in first and (c in cf or c in rn)])
print("PER GAME (steps; per step means; cf / rn steps):")
by = collections.defaultdict(list)
for c in cs:
    by[game_of(c)].append(c)
for g, gcs in by.items():
    m = {p: sum(wall[c].get(p, 0.0) for c in gcs) / len(gcs) for p in PH}
    print(f"  {g} steps {len(gcs):2d}  " + "  ".join(f"{p} {m[p]:6.1f}" for p in PH)
          + f"  cf {sum(c in cf for c in gcs)} rn {sum(c in rn for c in gcs)}")
