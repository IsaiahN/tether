"""R4 (c) read-only: the hypothesis rows of LS20/run, compact. argv: ledger path"""
import json
import sys

EV = {"goal_hypotheses", "goal_hypothesis_end", "hypothesis_hold", "hypothesis_test"}
with open(sys.argv[1], encoding="utf-8") as fh:
    for ln in fh:
        if '"event": "' not in ln:
            continue
        r = json.loads(ln)
        if r.get("event") not in EV:
            continue
        d = dict(r.get("detail") or {})
        for k in ("board", "counts"):
            d.pop(k, None)
        s = json.dumps(d, sort_keys=True)
        print(f"c{r.get('cycle')} {r.get('step')} {r.get('event')} {r.get('slot')} {s[:420]}")
