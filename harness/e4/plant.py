"""Fixture control for collect.py's transfer table: plant ONE pull row in the fixture's stream copy, naming a
term expression the fixture's lineage holds (born in ar25), at a cycle inside the stream's first slice.
argv: fixture_dir"""
import glob
import json
import os
import sys

F = sys.argv[1]
with open(glob.glob(os.path.join(F, "lineage", "gen_*.json"))[0], encoding="utf-8") as fh:
    gen = json.load(fh)
was = next(t["was"] for t in gen["terms"] if t.get("was"))
with open(os.path.join(F, "stream", "switch.tsv"), encoding="utf-8") as fh:
    sw = [x.split("\t") for x in fh.read().splitlines() if x and not x.startswith("#")]
cyc = int(sw[0][3])
row = {"cycle": cyc, "detail": {"term": was, "origin": "minted", "planted": True}, "event": "pull",
       "seq": 10 ** 9, "slot": "o0.x", "step": "ROUTE"}
with open(os.path.join(F, "stream", "stream.jsonl"), "a", encoding="utf-8") as fh:
    fh.write(json.dumps(row) + "\n")
print("planted", was, "born", gen.get("game"), "into slice", sw[0][1], "at cycle", cyc)
