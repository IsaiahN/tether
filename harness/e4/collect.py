"""E5.2 DATA COLLECTION (the reviewer 2026-10-18 16:48; readings from 11:19 (iii), the 11:17 list item 8, and
14:24's E5.2 / E6a / additions 3-4). READ ONLY: it opens the E4 folder's files and writes one output folder.
It never imports the agent. Run only after E4b has ended (it refuses a folder whose stream has no end line).

Units, never pooled: an E4a GAME (public/NN_<game>/) and an E4b SLICE (stream/, cut by switch.tsv's
cycle ranges). Every table names its row source in its header comment.

  ground.tsv       the ground: levels, the time of each level change, won / censored, actions, wall,
                   step mean, peak commit (result.json, sup.json)
  agent.tsv        per unit: consolidation folds by trigger, asked_kept bytes, kinds by class, Q1/Q2,
                   K1 lookups left unasked, mints (real) apart from want_only and derived_asked, G1
                   questions / formed / no_new_state / wants, routines adopted, routine_refused by
                   reason, goal hypotheses held per step, first-want cycle per level (ledger rows)
  generations.tsv  per generation: game, parent, term rows vs distinct compositions (L3) (lineage/gen_*)
  transfer.tsv     per ORDERED pair (born-in i -> used-in j, i != j): terms born in i that were PULLED,
                   BOUND (accept / rebind) and SETTLED in j (term handles + lineage term.game)
  library.tsv      the snapshots by phase: files, bytes, and the change between phases (snapshots/*)
  unmapped.txt     every listed reading this script could not tie to a row, with the nearest row

argv: e4_dir out_dir [--parse-check]   (--parse-check: parse every file and print row counts only)"""
from __future__ import annotations

import collections
import glob
import json
import os
import sys

E4, OUT = sys.argv[1], sys.argv[2]
PARSE_ONLY = "--parse-check" in sys.argv


def rows_of(path):
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            if ln.strip():
                yield json.loads(ln)


def load_json(path, default=None):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return default


# ---- the units -------------------------------------------------------------------------------------------
def units():
    """(phase, unit, ledger path, cycle range or None, result dict, sup dict) per E4a game and E4b slice."""
    out = []
    for d in sorted(glob.glob(os.path.join(E4, "public", "[0-9][0-9]_*"))):
        g = os.path.basename(d).split("_", 1)[1]
        out.append(("E4a", g, os.path.join(d, f"{g}.jsonl"), None,
                    load_json(os.path.join(d, f"{g}.result.json"), {}), load_json(os.path.join(d, "sup.json"), {})))
    sw = os.path.join(E4, "stream", "switch.tsv")
    if os.path.exists(sw):
        with open(sw, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        assert any(x.startswith("# stream end") for x in lines), "E4b has not ended: no '# stream end' line"
        sl = [x.split("\t") for x in lines if x and not x.startswith("#")]
        led = os.path.join(E4, "stream", "stream.jsonl")
        for k, f in enumerate(sl):
            c0 = int(f[3])
            c1 = int(sl[k + 1][3]) if k + 1 < len(sl) else 10 ** 12
            res = {"wall_s": float(f[4]), "actions": int(f[5]), "levels_in_slice": int(f[6]), "ending": f[7],
                   "endings": f[8], "order": int(f[0])}
            out.append(("E4b", f[1], led, (c0, c1), res, {}))
    return out


def load_window(game_dir, game, res):
    """E4a only: game start -> first step, as a window (the reviewer 17:40). game_one's clock T0 starts BEFORE
    play() wires the agent and loads the lineage (game_one.py:54-55, arc_holdout.py:205-206), so the cap
    includes the load. Its sampler writes (t, commit MB, actions) every 10 s from T0; with t0 the last sample
    at 0 actions, t1 the first at >= 1, and s0 the first step's own time, the first step began in
    (t0 - s0, t1 - s0]. Returns "lo..hi" seconds, or None."""
    s = res.get("step_s") or []
    if not s:
        return None
    t0, t1 = 0.0, None
    try:
        with open(os.path.join(game_dir, f"{game}.commit.tsv"), encoding="utf-8") as fh:
            for ln in fh:
                f = ln.split("\t")
                if len(f) < 3:
                    continue
                t, acts = float(f[0]), int(f[2])
                if acts == 0:
                    t0 = t
                elif t1 is None:
                    t1 = t
                    break
    except (OSError, ValueError):
        return None
    if t1 is None:
        return None
    return f"{max(0.0, round(t0 - s[0], 1))}..{round(t1 - s[0], 1)}"


# ---- per-unit readings from the ledger ---------------------------------------------------------------------
def read_unit(path, rng):
    t = collections.Counter()
    folds = collections.Counter()
    refused = collections.Counter()
    last = {}
    wants_held, first_want, level_cycles = [], {}, [0]
    used = collections.defaultdict(set)           # handle -> {"pulled", "bound", "settled"}
    n = 0
    for r in rows_of(path):
        cyc = r.get("cycle", 0)
        if rng and not (rng[0] <= cyc < rng[1]):
            continue
        n += 1
        e, step, d = r.get("event"), r.get("step"), r.get("detail") or {}
        t[(step, e)] += 1
        if e == "consolidate":
            folds[str(d.get("trigger"))] += 1
            last["consolidate"] = d
        elif e == "memo_sizes":
            last["memo_sizes"] = d
        elif e == "routine_refused":
            refused[str(d.get("reason"))[:60]] += 1
        elif e == "budget" and r.get("slot") == "@budget":
            t["k1_late_not_asked"] += int(d.get("late_not_asked") or 0)
            t["k1_not_asked"] += int(d.get("not_asked") or 0)
        elif e == "lookup" and step == "ROUTE":           # cost readings under their own row names (17:16 1)
            t["lookup_rows"] += 1
            t["lookup_held_n"] += int(d.get("held_n") or 0)
        elif e == "lookup_tiers":
            t["lookup_tiers_rows"] += 1
            t["lookup_tiers_deferred"] += int(d.get("deferred") or 0)
            for k, v in (d.get("listed") or {}).items():
                t[f"lookup_tiers_listed_{k}"] += int(v or 0)
        elif e in ("goal_choice", "progress") and d.get("wants_held") is not None:
            wants_held.append(d.get("wants_held") if isinstance(d.get("wants_held"), int) else len(d["wants_held"]))
        elif e == "g1":
            t["g1_formed"] += d.get("formed") is not None      # formed: the slot a want formed on, or null
            t["g1_no_new_state"] += bool(d.get("no_new_state"))
        elif e == "ground_record" and d.get("how") not in (None, "cap"):     # a cap is no level edge
            level_cycles.append(cyc)
        if d.get("want") and (step, e) != ("MINT", "derived_asked"):
            lv = sum(1 for c in level_cycles if c <= cyc) - 1
            first_want.setdefault(lv, cyc - (rng[0] if rng else 0))
        h = d.get("term")
        if isinstance(h, str):
            if e == "pull":
                used[h].add("pulled")
            elif e in ("accept", "rebind"):
                used[h].add("bound")
            elif e == "settle":
                used[h].add("settled")
    con, memo = last.get("consolidate") or {}, last.get("memo_sizes") or {}
    ex, hits = memo.get("exempt") or {}, memo.get("hits") or {}     # tether.py:3111-3116, the agent's own hits
    agent = {
        "rows": n,
        "mints_real": t[("MINT", "mint")],
        "want_only": t[("MINT", "want_only")],
        "derived_asked": t[("MINT", "derived_asked")],
        "g1_questions": t[("MINT", "g1")], "g1_formed": t["g1_formed"], "g1_no_new_state": t["g1_no_new_state"],
        "g1_wants": t[("MINT", "g1_want")],
        "routines_adopted": t[("PLAN", "routine")],
        "routine_refused": dict(refused.most_common()),
        "folds_by_trigger": dict(folds),
        "asked_kept": con.get("asked_kept"), "asked_kept_total": con.get("asked_kept_total"),
        "kinds_by_class": con.get("kinds_by_class"),
        "Q1_bound_slot_hit_derived": hits.get("bound_slot_hit_derived"),
        "Q2_bound_slot_landed": ex.get("bound_slot_landed"),
        # the carried-hit reading: hits on entries the lineage carried in, beside all hits (memo_sizes.hits)
        "slot_hit": hits.get("bound_slot_hit"), "slot_hit_carried": hits.get("bound_slot_hit_carried"),
        "slot_from_carry": hits.get("bound_slot_from_carry"),
        "whole_hit": hits.get("bound_whole_hit"), "whole_hit_carried": hits.get("bound_whole_hit_carried"),
        "k1_late_not_asked": t["k1_late_not_asked"], "k1_not_asked": t["k1_not_asked"],
        "lookup_rows": t["lookup_rows"], "lookup_held_n": t["lookup_held_n"],
        "lookup_tiers_rows": t["lookup_tiers_rows"], "lookup_tiers_deferred": t["lookup_tiers_deferred"],
        "lookup_tiers_listed": {k[len("lookup_tiers_listed_"):]: v for k, v in t.items()
                                if isinstance(k, str) and k.startswith("lookup_tiers_listed_")},
        "wants_held_mean": round(sum(wants_held) / len(wants_held), 2) if wants_held else None,
        "first_want_cycle_by_level": first_want,
    }
    return agent, used


# ---- generations and term birth ----------------------------------------------------------------------------
def generations():
    """The generations in CHAIN order (root first, by parent links; file names are hashes), and each term
    EXPRESSION's first birth. Ledger rows name a term by its expression (detail.term, e.g.
    "recolour<o10.colour>"); a generation's term row carries that expression as `was`. An expression born in
    two games keeps its first birth and is counted in `reborn`."""
    by_hash = {}
    for p in glob.glob(os.path.join(E4, "lineage", "gen_*.json")):
        g = load_json(p, {})
        by_hash[os.path.basename(p)[4:-5]] = (os.path.basename(p), g)
    kids = collections.defaultdict(list)
    for h, (_f, g) in by_hash.items():
        kids[g.get("parent")].append(h)
    order, todo = [], sorted(kids.get(None, []))
    while todo:
        h = todo.pop(0)
        order.append(h)
        todo = sorted(kids.get(h, [])) + todo
    born, gens, reborn = {}, [], collections.Counter()
    for h in order:
        f, g = by_hash[h]
        terms = g.get("terms") or []
        comp = {json.dumps([x.get("atoms"), x.get("operand"), x.get("guard"), x.get("operand_term")],
                           sort_keys=True) for x in terms}
        ns = sorted((int(x[4]) for x in g.get("kinds_landed_n") or () if len(x) > 4), reverse=True)
        gens.append({"file": f, "game": g.get("game"), "parent": g.get("parent"),
                     "term_rows": len(terms), "distinct_compositions": len(comp),
                     "top10_landings": f"{sum(ns[:10])}/{sum(ns)}"})     # 17:16 2: count / denominator
        for x in terms:
            w = x.get("was")
            if not w:
                continue
            if w in born and born[w][0] != x.get("game"):
                reborn[w] += 1
            born.setdefault(w, (x.get("game"), x.get("residual")))
    if len(order) != len(by_hash):
        print("WARNING: generations off the chain:", len(by_hash) - len(order))
    return gens, born, reborn


def birth_unit(expr, born, slices):
    """The unit a term was born in: its lineage game; for a term born in the stream, the slice whose cycle
    range holds its residual's @cycle. None for an expression no generation holds (a library entry)."""
    if expr not in born:
        return None
    g, res = born[expr]
    if g != "stream":
        return ("E4a", g)
    try:
        cyc = int(str(res).rsplit("@", 1)[1].split(":")[0])
    except (IndexError, ValueError):
        return ("E4b", "?")
    for name, (c0, c1) in slices:
        if c0 <= cyc < c1:
            return ("E4b", name)
    return ("E4b", "?")


def library():
    rows = []
    for d in sorted(glob.glob(os.path.join(E4, "snapshots", "*"))):
        files = [f for f in glob.glob(os.path.join(d, "**", "*"), recursive=True) if os.path.isfile(f)
                 and not f.endswith("MANIFEST.tsv")]
        rows.append({"phase": os.path.basename(d), "files": len(files),
                     "bytes": sum(os.path.getsize(f) for f in files)})
    return rows


UNMAPPED = {   # the reviewer 2026-10-18 17:16 ruled each
    "full index walks": "name dropped; ROUTE lookup held_n and lookup_tiers rows are reported under their own "
                        "names in agent.tsv, no derived 'walks' figure",
    "top-10 share of landings": "computed from kinds_landed_n per generation (generations.tsv, count/denominator)",
    "kind-entry hits at the next level / next game":
        "left unread: the carried bound-slot / whole hits are read (memo_sizes.hits *_carried); lookup_tiers "
        "T1a-T1d is printed under its own name and no meaning is claimed",
    "level-start wall": "E4a only (result.json level_changes times); E4b has no per-slice level clock, only "
                        "switch.tsv's cycle ranges",
}


def main() -> int:
    us = units()
    os.makedirs(OUT, exist_ok=True)
    if PARSE_ONLY:
        for ph, name, led, rng, res, _sup in us:
            n = sum(1 for r in rows_of(led) if not rng or rng[0] <= r.get("cycle", 0) < rng[1])
            print(ph, name, "rows", n, "result keys", len(res))
        print("generations", len(generations()[0]), "snapshots", len(library()))
        return 0
    slices = [(name, rng) for ph, name, _l, rng, _r, _s in us if ph == "E4b"]
    gens, born, reborn = generations()
    with open(os.path.join(OUT, "ground.tsv"), "w", encoding="utf-8") as g, \
            open(os.path.join(OUT, "agent.tsv"), "w", encoding="utf-8") as a:
        g.write("# result.json / sup.json (E4a); switch.tsv (E4b). load_s: game start -> first step, a window from "
                "the 10 s commit sampler; the E4a cap INCLUDES it. levels_cleared: game_one's level_changes LESS its "
                "first entry, which is the first READING (level 0 at the first action), never a clear (the reviewer "
                "23:21)\nphase\tunit\tlevels_cleared\tlevel_readings_first_included\twon\tcensored"
                "\tactions\twall_s\ts_per_step_mean\tpeak_commit_gib\tending\tload_s\n")
        a.write("# the unit's ledger rows (E4b: the slice's cycle range)\nphase\tunit\treadings_json\n")
        pairs = collections.defaultdict(lambda: collections.Counter())
        for ph, name, led, rng, res, sup in us:
            lc = res.get("level_changes") or []
            g.write(f"{ph}\t{name}\t{max(0, len(lc) - 1) if ph == 'E4a' else res.get('levels_in_slice')}\t"
                    f"{json.dumps(lc)}\t"
                    f"{res.get('won', res.get('ending') == 'win')}\t{res.get('censored')}\t"
                    f"{res.get('actions', res.get('agent_steps'))}\t{res.get('wall_s')}\t{res.get('s_per_step_mean')}\t"
                    f"{sup.get('peak_process_commit_gib')}\t{sup.get('ending', res.get('ending'))}\t"
                    f"{load_window(os.path.dirname(led), name, res) if ph == 'E4a' else None}\n")
            agent, used = read_unit(led, rng)
            a.write(f"{ph}\t{name}\t{json.dumps(agent, sort_keys=True, default=str)}\n")
            for h, how in used.items():
                src = birth_unit(h, born, slices)
                if src is not None and src != (ph, name):
                    for k in how:
                        pairs[(src, (ph, name))][k] += 1
    with open(os.path.join(OUT, "transfer.tsv"), "w", encoding="utf-8") as f:
        f.write("# per ordered pair, never pooled: terms born in i (lineage term.game; a stream term by its "
                "residual's cycle) that were pulled / bound / settled in j\nborn_phase\tborn_unit\tused_phase\t"
                "used_unit\tpulled\tbound\tsettled\n")
        f.writelines(f"{s[0]}\t{s[1]}\t{u[0]}\t{u[1]}\t{c['pulled']}\t{c['bound']}\t{c['settled']}\n" for (s, u), c in sorted(pairs.items()))
    with open(os.path.join(OUT, "generations.tsv"), "w", encoding="utf-8") as f:
        f.write("# lineage/gen_*.json in chain order; top10_landings = the 10 largest kinds_landed_n counts over "
                "their total\nfile\tgame\tparent\tterm_rows\tdistinct_compositions\ttop10_landings\n")
        f.writelines(f"{x['file']}\t{x['game']}\t{x['parent']}\t{x['term_rows']}\t{x['distinct_compositions']}\t"
                    f"{x['top10_landings']}\n" for x in gens)
    with open(os.path.join(OUT, "library.tsv"), "w", encoding="utf-8") as f:
        f.write("# snapshots/<phase>/ (copied, never moved)\nphase\tfiles\tbytes\n")
        f.writelines(f"{x['phase']}\t{x['files']}\t{x['bytes']}\n" for x in library())
    with open(os.path.join(OUT, "unmapped.txt"), "w", encoding="utf-8") as f:
        for k, v in UNMAPPED.items():
            f.write(f"{k}: {v}\n")
        f.write(f"expressions born in more than one game (first birth kept): {len(reborn)}\n")
    print("wrote", OUT, "units", len(us), "generations", len(gens), "pairs", len(pairs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
