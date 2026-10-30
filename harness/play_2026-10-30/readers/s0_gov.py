"""r356 read, PLAY19 round 1: per game, step 1's governor verdicts (lookup_deferred why, and the in-mint
extension rows that carry a think-or-act why) beside step 1's MINT wall. argv: round dir."""
import json
import sys
from collections import Counter

sys.dont_write_bytecode = True
R = sys.argv[1]
rows = [json.loads(x) for x in open(f"{R}/stream.jsonl", encoding="utf-8")]
hdr, games = None, []
for line in open(f"{R}/switch.tsv", encoding="utf-8"):
    if line.startswith("# idx"):
        hdr = line[2:].rstrip("\n").split("\t")
    elif not line.startswith("#") and line.strip():
        games.append(dict(zip(hdr, line.rstrip("\n").split("\t"), strict=True)))
WHYS = {"closer_found", "urgent", "urgent_declined", "probe_first", "probe_declined", "ok"}
for g in games:
    sp, s1 = int(g["seqP"]), int(g["seq1"])
    step1 = [r for r in rows if sp <= r.get("seq", -1) < s1]
    rep = next((r for r in step1 if r["event"] == "repeat"), None)
    deferred = Counter(r["detail"].get("why") for r in step1 if r["event"] == "lookup_deferred")
    gov = Counter()
    for r in step1:
        d = r.get("detail") or {}
        for k in ("why", "governor", "think_or_act"):
            v = d.get(k)
            if isinstance(v, str) and v in WHYS:
                gov[(r["step"], r["event"], v)] += 1
    mint = rep["detail"]["wall_s"].get("MINT") if rep else None
    print(g["game"], "steps", g["steps"], "acts", g["acts"], "| step1 MINT s", mint,
          "| lookup_deferred", dict(deferred), "| governor rows", dict(gov.most_common(6)))
