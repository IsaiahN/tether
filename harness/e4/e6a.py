"""E6a ANALYSIS: E4b against E4a, PER GAME, never pooled (the reviewer 2026-10-18 14:24, 17:05 2d). READ ONLY;
the same row readers as collect.py (imported from beside this file), so E5.2 and E6a read one way.

Per game g, one row:
  order        g's position in the E4b stream (switch.tsv idx)
  EQUAL BUDGET E4a's state at 120 s of play (levels by then from level_changes times; steps whose cumulative
               step_s <= 120) beside E4b's slice (levels_in_slice, steps, wall incl. overrun)
  RECALL       terms born in E4a's g that were pulled / bound / settled in E4b's slice of g
  TRANSFER IN  terms born in OTHER units (E4a i != g, or an earlier E4b slice) used in E4b's slice of g
  TRANSFER OUT terms born in E4a's g used in E4b's OTHER slices
  SWITCH LAG   the first boundary row the agent wrote after the switch (e4_stream_check's DETECTION rule:
               event, how, steps after the slice began); none = it wrote none in the slice
argv: e4_dir out_dir"""
from __future__ import annotations

import collections
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
E4, OUT = sys.argv[1], sys.argv[2]
sys.argv = [sys.argv[0], E4, OUT]          # collect reads its own argv at import
import collect  # noqa: E402

BOUND = ("boundary", "ending", "restart", "restart_lineage")


def at_budget(res, budget=120.0):
    t, steps = 0.0, 0
    for s in res.get("step_s") or []:
        if t + s > budget:
            break
        t, steps = t + s, steps + 1
    # level_changes' FIRST entry is game_one's first READING (level 0), never a clear (the reviewer 23:21)
    levels = sum(1 for x in (res.get("level_changes") or [])[1:] if x and x[0] <= budget)
    return levels, steps


def switch_lag(led, rng):
    for r in collect.rows_of(led):
        c = r.get("cycle", 0)
        if rng[0] <= c < rng[1] and r.get("event") in BOUND:
            return f"{r.get('event')}:{(r.get('detail') or {}).get('how')}:{c - rng[0]}"
    return None


def main() -> int:
    us = collect.units()
    gens, born, _reborn = collect.generations()
    slices = [(name, rng) for ph, name, _l, rng, _r, _s in us if ph == "E4b"]
    e4a = {name: res for ph, name, _l, _rng, res, _s in us if ph == "E4a"}
    used_by = {}
    for ph, name, led, rng, _res, _sup in us:
        used_by[(ph, name)] = collect.read_unit(led, rng)[1]
    pair = collections.defaultdict(collections.Counter)
    for unit, used in used_by.items():
        for expr, how in used.items():
            src = collect.birth_unit(expr, born, slices)
            if src is not None and src != unit:
                for k in how:
                    pair[(src, unit)][k] += 1
    order = {name: i for i, (name, _rng) in enumerate(slices)}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "e6a.tsv"), "w", encoding="utf-8") as f:
        f.write("# per game, never pooled; recall / transfer columns are pulled/bound/settled; E4b has no per-slice "
                "level clock (switch.tsv cycle ranges)\ngame\torder\te4a_levels_at_120s\te4a_steps_at_120s\t"
                "e4b_levels\te4b_steps\te4b_wall_s\trecall\ttransfer_in\ttransfer_out\tswitch_lag\n")
        rows = {name: (led, rng, res) for ph, name, led, rng, res, _s in us if ph == "E4b"}
        for g in sorted(set(e4a) | set(rows)):
            lv, st = at_budget(e4a.get(g, {}))
            led, rng, res = rows.get(g, (None, None, {}))

            def fmt(c):
                return f"{c['pulled']}/{c['bound']}/{c['settled']}"
            rec = pair.get((("E4a", g), ("E4b", g)), collections.Counter())
            tin, tout = collections.Counter(), collections.Counter()
            for (s, u), c in pair.items():
                if u == ("E4b", g) and s != ("E4a", g):
                    tin.update(c)
                if s == ("E4a", g) and u[0] == "E4b" and u[1] != g:
                    tout.update(c)
            f.write(f"{g}\t{order.get(g)}\t{lv if g in e4a else None}\t{st if g in e4a else None}\t"
                    f"{res.get('levels_in_slice')}\t{res.get('actions')}\t{res.get('wall_s')}\t{fmt(rec)}\t"
                    f"{fmt(tin)}\t{fmt(tout)}\t{switch_lag(led, rng) if led else None}\n")
    with open(os.path.join(OUT, "e6a_pairs.tsv"), "w", encoding="utf-8") as f:
        f.write("# every ordered pair, both directions, never pooled\nborn\tused\tpulled\tbound\tsettled\n")
        for (s, u), c in sorted(pair.items()):
            f.write(f"{s[0]}:{s[1]}\t{u[0]}:{u[1]}\t{c['pulled']}\t{c['bound']}\t{c['settled']}\n")
    print("wrote", OUT, "games", len(set(e4a) | set(rows)), "pairs", len(pair))
    return 0


if __name__ == "__main__":
    sys.exit(main())
