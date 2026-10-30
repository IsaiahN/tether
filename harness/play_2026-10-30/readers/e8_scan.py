"""E8's one pass over real-game ledgers (read-only, Windows background mode): per ledger, the count of each event
named in WANT (a line is parsed only if it contains one of the names), and the FIRST full row of each, kept to a
JSON file for quoting. Also the header row (seq 0) and the last row. argv: out_json ledger..."""
import collections
import ctypes
import json
import os
import sys

ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00100000)
WANT = ["contradiction", "contradiction_routed", "contradiction_diagnosed", "recurse_parts", "invent",
        "rehearsal", "abduce", "intent_verdict", "intent_graded", "inherited_lit", "reuse_install",
        "invention_carried", "termination", "utterance", "system0", "hypothesis_test", "demote", "promote",
        "compete", "rebind", "accept", "pull", "ending", "boundary", "goal_hypotheses", "quit", "veto",
        "two_readings", "library_explained", "miss_while_settled", "store_refused", "load", "lineage"]
keys = [f'"{w}"' for w in WANT]
out = {}
for f in sys.argv[2:]:
    c, first, head, last = collections.Counter(), {}, None, None
    with open(f, encoding="utf-8") as fh:
        for i, ln in enumerate(fh):
            last = ln
            if i == 0:
                head = json.loads(ln)
            if not any(k in ln for k in keys):
                continue
            r = json.loads(ln)
            e = r.get("event")
            if e in WANT:
                c[e] += 1
                first.setdefault(e, r)
    tag = os.path.relpath(f, "C:/TETHER_RUNS").replace("\\", "/")
    out[tag] = {"counts": dict(c), "first": first, "head": head,
                "last": json.loads(last) if last else None, "rows": i + 1}
    print(tag, i + 1, dict(sorted(c.items())))
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), default=str)
