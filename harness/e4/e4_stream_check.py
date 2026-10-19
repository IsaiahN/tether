"""The stream's boundary check (the reviewer 2026-10-18 11:40 point 4, 13:02 (B)). The guarantee is structural: the
driver calls no agent method at a switch. Per switch (idx > 0) the switch.tsv row carries three ledger marks:
seq0 (before the switch), seqP (after the MF plant, if any; before the new game's first step), seq1 (after that step).

  LEAK       ANY row in [seq0, seqP): written AT the switch, between
             steps, by the harness. By design there is none; --mf plants ag.restarted(env) there, and the check
             must catch it (--expect-fail).
  DETECTION  a boundary row from the slice's first step on: the game's own event as play() handles it (a
             GAME_OVER, a level edge) -- reported with its event, how and lag in steps, NEVER a failure.
Also no @consolidate fold with trigger game_start after the run's birth. argv: out_dir [--expect-fail]"""
import json
import os
import sys

out = sys.argv[1]
expect_fail = "--expect-fail" in sys.argv
BOUND = ("boundary", "ending", "restart", "restart_lineage")
slices = []
for ln in open(os.path.join(out, "switch.tsv"), encoding="utf-8"):
    if ln.startswith("#") or not ln.strip():
        continue
    f = ln.rstrip("\n").split("\t")
    s1 = int(f[-1]) if f[-1] not in ("None", "") else None
    slices.append({"idx": int(f[0]), "game": f[1], "cycle0": int(f[3]), "seq0": int(f[-3]), "seqP": int(f[-2]),
                   "seq1": s1})
rows = [json.loads(x) for x in open(os.path.join(out, "stream.jsonl"), encoding="utf-8") if x.strip()]
leaks, detect = [], []
for k, sl in enumerate(slices):
    if sl["idx"] == 0:
        continue
    # ANY row at the switch is a leak: the driver writes nothing between steps (a planted restarted()
    # shows as a consolidate fold, not only as a restart row, so the event list alone would miss it)
    at = [r for r in rows if sl["seq0"] <= r.get("seq", -1) < sl["seqP"]]
    if at:
        leaks.append((sl["idx"], sl["game"], [(r.get("event"), (r.get("detail") or {}).get("how")
                                               or (r.get("detail") or {}).get("trigger")) for r in at[:3]]))
    end = slices[k + 1]["seq0"] if k + 1 < len(slices) else 10 ** 12
    first = next((r for r in rows if sl["seqP"] <= r.get("seq", -1) < end and r.get("event") in BOUND), None)
    if first is not None:
        detect.append({"idx": sl["idx"], "game": sl["game"], "event": first.get("event"),
                       "how": (first.get("detail") or {}).get("how"), "lag_steps": first.get("cycle", 0) - sl["cycle0"]})
folds = [r for r in rows if r.get("event") == "consolidate"
         and (r.get("detail") or {}).get("trigger") == "game_start" and r.get("cycle", 0) > 0]
bad = bool(leaks or folds)
print(json.dumps({"switches": sum(1 for s in slices if s["idx"] > 0), "leaked_switches": len(leaks),
                  "first_leaks": leaks[:3], "game_start_folds_after_birth": len(folds),
                  "detections": detect, "verdict": "LEAK" if bad else "CLEAN"}))
if expect_fail:
    sys.exit(0 if bad else "MUST-FAIL did not fail: the planted boundary at the switch was not caught")
sys.exit(1 if bad else 0)
