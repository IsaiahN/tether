"""THE PLAY RUN, ACROSS ROUNDS (the reviewer 2026-10-23 21:43, the 5 additions). Read only, harness side; nothing goes
back to the agent or its lineage.
  PER ROUND  load wall (load_report.json's mtime - launcher.txt's t_launch), the load report's dedup counts (library_n,
             loaded, already_held, deduped_onto_composition, store_merged_at_load, index installed), the stream's
             cycles / wall_s / written head / terms, the supervisor's rc and peak commit, and chain.log's compression line
             (names, lineage_bytes, store_bytes before and after)
  PER GAME   one row per game, one cell per round: position in that round's order : levels_in_slice / steps / acts /
             ending, from switch.tsv. A game that did not get a slice reads "-". Never pooled across games
argv: PLAY dir"""
import json
import os
import re
import sys

sys.dont_write_bytecode = True
P = sys.argv[1]
J = os.path.join


def load(p):
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as x:  # noqa: BLE001 -- a missing or partial file is the reading
        return {"__unreadable__": repr(x)}


rounds = sorted(d for d in os.listdir(P) if re.fullmatch(r"round_\d\d", d) and os.path.isdir(J(P, d)))
chain = open(J(P, "chain.log"), encoding="utf-8").read() if os.path.exists(J(P, "chain.log")) else ""
print(f"== rounds found: {len(rounds)} {rounds}")
games, cells = [], {}
for rd in rounds:
    O, n = J(P, rd), int(rd[-2:])
    lr = load(J(O, "load_report.json"))
    ll = lr.get("loaded_lineage") or {}
    try:   # launcher.txt is JSON followed by the supervisor's own line, so t_launch is read by pattern
        with open(J(O, "launcher.txt"), encoding="utf-8") as fh:
            tl = re.search(r'"t_launch": ([0-9.]+)', fh.read())
    except OSError:
        tl = None
    lw = (os.path.getmtime(J(O, "load_report.json")) - float(tl.group(1))
          if tl and os.path.exists(J(O, "load_report.json")) else None)
    res = load(J(O, "stream.result.json"))
    sup = load(J(O, "sup", "sup.json"))
    lin = res.get("lineage")
    print(f"== round {n}: load wall {None if lw is None else round(lw, 1)} s | library_n {lr.get('library_n')} "
          f"parent {lr.get('lineage_parent')} | loaded {ll.get('loaded')} already_held {ll.get('already_held')} "
          f"deduped_onto_composition {ll.get('deduped_onto_composition')} store_merged_at_load "
          f"{ll.get('store_merged_at_load')} index_installed {(ll.get('index') or {}).get('installed')}")
    print(f"   stream: cycles {res.get('cycles')} wall_s {res.get('wall_s')} end_path_s {res.get('end_path_s')} "
          f"budget_unreached {res.get('budget_unreached')} | lineage {str(lin)[:160]}")
    print(f"   sup: rc {sup.get('rc')} ending {sup.get('ending')} wall_s {sup.get('wall_s')} "
          f"peak_job_commit_gib {sup.get('peak_job_commit_gib')}")
    for tag in ("START", "WRITE_CHECK"):
        m = re.search(rf"ROUND {n} {tag} .*", chain)
        print(f"   chain {tag}: {m.group(0)[:300] if m else 'absent'}")
    try:
        with open(J(O, "switch.tsv"), encoding="utf-8") as fh:
            lines = [ln.rstrip("\n").split("\t") for ln in fh if ln.strip() and not ln.startswith("#")]
    except OSError:
        lines = []
    for r in lines:
        idx, g, steps, lv, end, acts = r[0], r[1], r[5], r[6], r[7], r[13]
        if g not in games:
            games.append(g)
        cells[(g, n)] = f"{idx}:{lv}/{steps}/{acts}/{end}"
print("== per game (cell = position:levels_in_slice/steps/acts/ending), one column per round")
print("   game  " + "  ".join(f"{r:>24s}" for r in rounds))
for g in sorted(games):
    print(f"   {g:5s} " + "  ".join(f"{cells.get((g, int(r[-2:])), '-'):>24s}" for r in rounds))
