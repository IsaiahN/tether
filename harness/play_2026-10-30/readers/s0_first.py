"""r356 read, PLAY19 round 1 (no new run): per game, what the agent did before and at its FIRST action.
From switch.tsv (the slice windows) and stream.jsonl. argv: round dir."""
import json
import sys
from collections import Counter

sys.dont_write_bytecode = True
R = sys.argv[1]
rows = [json.loads(x) for x in open(f"{R}/stream.jsonl", encoding="utf-8")]
by_seq = {r["seq"]: i for i, r in enumerate(rows) if "seq" in r}
hdr, games = None, []
for line in open(f"{R}/switch.tsv", encoding="utf-8"):
    if line.startswith("# idx"):
        hdr = line[2:].rstrip("\n").split("\t")
    elif not line.startswith("#") and line.strip():
        games.append(dict(zip(hdr, line.rstrip("\n").split("\t"), strict=True)))
print("rows", len(rows), "games", len(games))
print("game  steps acts first_act_s slice_s | pre-step rows (events) | step-1 exit (by) fixed_would s0_defer "
      "| step-1 REPEAT wall_s by phase | MINT rows in step 1 | first step_mint wall_s seen in slice (cycle)")
for g in games:
    s0, sp, s1 = int(g["seq0"]), int(g["seqP"]), int(g["seq1"])
    win = [r for r in rows if s0 <= r.get("seq", -1) < s1]
    pre = [r for r in win if r["seq"] < sp]
    step1 = [r for r in win if r["seq"] >= sp]
    rep = next((r for r in step1 if r["event"] == "repeat"), None)
    ch = next((r for r in step1 if r["event"] == "choice" and r["detail"].get("site") == "exit"), None)
    mints = sum(1 for r in step1 if r["step"] == "MINT")
    # the whole slice: step_mint rows, for the first wall seen
    slice_rows = [r for r in rows if r.get("seq", -1) >= sp and r.get("detail", {}).get("game", g["game"])]
    sm = [r for r in win if r["event"] == "step_mint"]
    print(g["game"], g["steps"], g["acts"], g["first_act_s"], g["wall_s"], "|",
          len(pre), dict(Counter(r["event"] for r in pre).most_common(4)), "|",
          rep["detail"].get("by") if rep else None,
          ch["detail"].get("fixed_would") if ch else None, ch["detail"].get("s0_defer") if ch else None, "|",
          rep["detail"].get("wall_s") if rep else None, "|", mints, "|",
          [(r["cycle"], r["detail"].get("wall_s")) for r in sm][:2])
