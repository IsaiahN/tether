"""Read-only: the park and divide rows of named (cycle, slot) pairs in a stream.jsonl, every key but the long
lists, so it shows what the record holds of enumerate_closure's own stats. argv: stream, cycle:slot,..."""
import json
import sys

sys.dont_write_bytecode = True
want = {(int(c), s) for c, s in (x.split(":", 1) for x in sys.argv[2].split(","))}
cyc = {c for c, _ in want}
for ln in open(sys.argv[1], encoding="utf-8"):
    if not any(f'"cycle": {c},' in ln for c in cyc):
        continue
    r = json.loads(ln)
    if (r.get("cycle"), r.get("slot")) not in want or r.get("event") not in ("park", "divide", "mint"):
        continue
    d = r.get("detail") or {}
    keep = {k: v for k, v in d.items() if k not in ("reads", "cuts", "code", "contest")}
    print(r["cycle"], r["slot"], r["event"], json.dumps(keep)[:900])
