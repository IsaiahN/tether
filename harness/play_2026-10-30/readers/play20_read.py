"""PLAY20 per-round read (r376 4): stop_read, remainder, goal_hypotheses compile_reads / not_admitted /
wall_s, ask / ask_none, owed rows, and acts and levels per game. Counts over the whole stream; zeros printed.
argv: round dir."""
import ast
import collections
import json
import os
import sys

sys.dont_write_bytecode = True
O = sys.argv[1]
EV = ("ask", "ask_none", "ask_unsplit", "split_aim_left", "stop_read", "stop_rule", "remainder",
      "goal_hypotheses", "owed_released", "owed_superseded")
n = collections.Counter()
stop_rule = collections.Counter()
sr = collections.Counter()
gh = {"rows": 0, "picks": 0, "phases": collections.Counter(), "compile_reads": 0, "not_admitted": 0,
      "wall_s": 0.0, "with_fields": 0}
rem_words = collections.Counter()
mint_by_cycle, rep_by_cycle = collections.Counter(), collections.Counter()   # r381: the share
ph_sum, ph_max = collections.Counter(), collections.defaultdict(lambda: (0.0, None))
s1, s1_max = collections.defaultdict(list), collections.defaultdict(lambda: (-1, None, None))
s1_cycles, s1_slots = set(), set()
by_tally = collections.Counter()
prog, prog_slots, ghe = [], set(), []
arms_n = collections.Counter()
with open(os.path.join(O, "stream.jsonl"), encoding="utf-8") as fh:
    for line in fh:
        r = json.loads(line)
        e = r.get("event")
        if e == "repeat" and isinstance((r.get("detail") or {}).get("wall_s"), dict):
            mint_by_cycle[r.get("cycle")] += r["detail"]["wall_s"].get("MINT", 0.0)
            by_tally[str(r["detail"].get("by"))] += 1          # r383 4: the chooser per act
            for ph, w in r["detail"]["wall_s"].items():      # r382 (a): every phase
                ph_sum[ph] += w
                if w > ph_max[ph][0]:
                    ph_max[ph] = (w, r.get("cycle"))
        if e in ("contact_first", "route_named", "goal_shelved", "goal_hypothesis_reopened",
                 "carry_w", "indistinct") or (e == "goal_hypothesis_end"):    # r405: PLAY21's arms
            d = r.get("detail") or {}
            if e == "contact_first":
                arms_n[f"contact_first:{d.get('why')}"] += 1
            elif e == "goal_shelved":
                arms_n["goal_shelved:progress" if (d.get("record") or {}).get("progress")
                       else "goal_shelved:won"] += 1
            elif e == "goal_hypothesis_end":
                if d.get("why") == "untested":
                    arms_n["goal_hypothesis_end:untested"] += 1
            else:
                arms_n[e] += 1
        if e == "progress":                                   # r391 1
            d = r.get("detail") or {}
            sw, cl = d.get("selected_want"), d.get("closer") or []
            prog.append((r.get("cycle"), sw is not None, sw is not None and sw in cl))
            prog_slots.update(cl)
        if e == "goal_hypothesis_end":                        # r391 2
            d = r.get("detail") or {}
            ghe.append((str(d.get("why")), not d.get("acted"), d.get("steps") == 0))
        if e in ("divide", "space_closed"):                   # r382 (b): the stored S1, 1a's rows
            s = (r.get("detail") or {}).get("survivors")
            if isinstance(s, int):
                s1[e].append(s)
                if e == "divide" and s >= 1:
                    s1_cycles.add(r.get("cycle"))
                    s1_slots.add(r.get("slot"))
                if s > s1_max[e][0]:
                    s1_max[e] = (s, r.get("cycle"), r.get("slot"))
        if e == "stop_read":
            rep_by_cycle[r.get("cycle")] += (r.get("detail") or {}).get("reprice_s", 0.0)
        if e not in EV:
            continue
        n[e] += 1
        d = r.get("detail") or {}
        if e == "stop_rule":
            stop_rule[str(d.get("rule") or d.get("verdict") or d.get("word") or "?")] += 1
        elif e == "stop_read":
            sr["spaces"] += d.get("spaces", 0)
            sr["reprice_hits"] += d.get("reprice_hits", 0)
            sr["repriced_cells"] += d.get("repriced_cells", 0)
            sr["repriced_rows"] += d.get("repriced_rows", 0)
            sr["reprice_s"] += d.get("reprice_s", 0.0)
        elif e == "remainder":
            rem_words[str(d.get("verdict") or d.get("word") or d.get("split") or "?")] += 1
        elif e == "goal_hypotheses":
            gh["rows"] += 1
            gh["picks"] += bool(d.get("pick"))
            if "compile_reads" in d:
                gh["with_fields"] += 1
                gh["phases"][d.get("phases")] += 1
                gh["compile_reads"] += d.get("compile_reads") or 0
                gh["not_admitted"] += d.get("not_admitted") or 0
                gh["wall_s"] += d.get("wall_s") or 0.0
print("EVENTS", {e: n[e] for e in EV})
print("STOP_READ sums", {k: round(v, 2) if isinstance(v, float) else v for k, v in sr.items()})
ms, rs = sum(mint_by_cycle.values()), sum(rep_by_cycle.values())
mmax = max(mint_by_cycle.items(), key=lambda kv: kv[1], default=(None, 0.0))
rmax = max(rep_by_cycle.items(), key=lambda kv: kv[1], default=(None, 0.0))
shares = [rep_by_cycle[c] / mint_by_cycle[c] for c in rep_by_cycle if mint_by_cycle.get(c)]
print(f"MINT WALL (repeat rows' wall_s.MINT) steps {len(mint_by_cycle)} sum {ms:.1f} s, largest {mmax[1]:.1f} s "
      f"(cycle {mmax[0]}) | REPRICE (stop_read reprice_s) steps {len(rep_by_cycle)} sum {rs:.2f} s, "
      f"largest {rmax[1]:.2f} s (cycle {rmax[0]}) | share of MINT: round {rs / ms if ms else 0:.4f}, "
      f"largest per step {max(shares, default=0):.4f}")
tot = ph_sum.get("total", 0.0)
print(f"STEP CLOCK (repeat rows' wall_s, {len(mint_by_cycle)} steps; share of the summed 'total' {tot:.1f} s):")
for ph in sorted(ph_sum, key=lambda p: -ph_sum[p]):
    print(f"  {ph:9} sum {ph_sum[ph]:8.1f} s  largest {ph_max[ph][0]:7.1f} s (cycle {ph_max[ph][1]})  "
          f"share {ph_sum[ph] / tot if tot else 0:.3f}")
print("STORED S1 as 1b reads it (valid cells with bound < bar, _space_bounds 'stale' + _s1_of): "
      "not recorded -- no row carries it but 'ask' (0 rows here); NOT the count below")
for e in ("divide", "space_closed"):
    v = s1[e]
    if not v:
        print(f"UNELIMINATED ({e}.survivors, cells with v[2] None): 0 rows")
        continue
    hist = collections.Counter(min(x, 3) for x in v)
    print(f"UNELIMINATED ({e}.survivors, cells with v[2] None): rows {len(v)}, largest {s1_max[e][0]} "
          f"(cycle {s1_max[e][1]}, slot {s1_max[e][2]}), rows with 0 / 1 / 2 / >=3: "
          f"{hist[0]} / {hist[1]} / {hist[2]} / {hist[3]}")
print(f"UNELIMINATED >= 1 after a mint (divide rows): steps {len(s1_cycles)}, gaps {len(s1_slots)}")
print(f"BY (repeat rows' chooser, {sum(by_tally.values())} steps): {dict(by_tally.most_common())} | "
      f"_ask called on >= {by_tally['distinguish']} cycles ('distinguish' returns only after :12457)")
print("STOP_RULE by verdict", dict(stop_rule))
print("REMAINDER by verdict", dict(rem_words))
print("GOAL_HYPOTHESES", {k: (dict(v) if isinstance(v, collections.Counter) else round(v, 1)
                              if isinstance(v, float) else v) for k, v in gh.items()})
acts, lv, starts = {}, {}, []
with open(os.path.join(O, "read.out"), encoding="utf-8") as fh:
    for line in fh:
        if line.startswith("SLICE {"):
            s = ast.literal_eval(line[6:].strip())
            g = s["game"]
            acts[g] = acts.get(g, 0) + int(s["acts"])
            lv[g] = lv.get(g, 0) + int(s["levels_in_slice"])
            starts.append((int(s["cycle_start"]), g))


def game_of(c):
    g = None
    for c0, gg in sorted(starts):
        if c is not None and c >= c0:
            g = gg
    return g


pg = collections.defaultdict(lambda: [0, 0, 0])
for c, has_sw, on_aim in prog:
    v = pg[game_of(c)]
    v[0] += 1
    v[1] += has_sw
    v[2] += on_aim
print(f"PROGRESS (r391 1; selected_want is a slot string, matched by membership in closer): rows {len(prog)}, "
      f"selected_want set {sum(p[1] for p in prog)}, closer on the selected want {sum(p[2] for p in prog)}, "
      f"distinct slots in closer {len(prog_slots)}")
print("  per game rows/with_want/on_aim:", " ".join(f"{g}:{v[0]}/{v[1]}/{v[2]}" for g, v in pg.items()))
by_why = collections.defaultdict(lambda: [0, 0, 0])
for why, no_act, zero in ghe:
    by_why[why][0] += 1
    by_why[why][1] += no_act
    by_why[why][2] += zero
print(f"GOAL_HYPOTHESIS_END (r391 2): ends {len(ghe)}, acted empty {sum(x[1] for x in ghe)}, steps == 0 "
      f"{sum(x[2] for x in ghe)}; by why (ends/acted-empty/steps0): "
      + " ".join(f"{w}:{v[0]}/{v[1]}/{v[2]}" for w, v in by_why.items()))
print("PER GAME acts/levels", " ".join(f"{g}:{acts[g]}/{lv[g]}" for g in acts))
print("TOTAL acts", sum(acts.values()), "levels", sum(lv.values()), "games", len(acts))
keys = ("contact_first:named", "contact_first:same_rows", "route_named", "goal_shelved:progress",
        "goal_shelved:won", "goal_hypothesis_end:untested", "goal_hypothesis_reopened", "carry_w",
        "indistinct")
print("NEW ARMS (r405) rows:", {k: arms_n[k] for k in keys})
sup = None
with open(os.path.join(O, "read.out"), encoding="utf-8") as fh:
    for line in fh:
        if line.startswith("SUP {"):
            sup = ast.literal_eval(line[4:].strip())
if sup:
    print(f"PACE acts {sum(acts.values())} / wall {sup['wall_s']} s = "
          f"{3600 * sum(acts.values()) / sup['wall_s']:.1f} acts/hour; peak "
          f"{sup['peak_process_commit_gib']} GiB")
