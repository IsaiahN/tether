"""E8 aggregates over real-game ledgers (read-only, background mode): per ledger,
  invent: rows, rows whose pick is not "none paid" (with their picks), park_verdict tally
  abduce: rows, rows with routed > 0, rows with new > 0, sum routed
  rehearsal: rows, sum rehearsed, sum compared, sum misses
  contradiction_diagnosed: every verdict
  accept: rows, their "term"/"origin" fields (first 5)
  intent_verdict / invention_carried / system0 / reuse_install: first detail (truncated)
argv: out_json ledger..."""
import collections
import ctypes
import json
import os
import sys

ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00100000)
EV = ('"invent"', '"abduce"', '"rehearsal"', '"contradiction_diagnosed"', '"accept"', '"intent_verdict"',
      '"invention_carried"', '"reuse_install"', '"system0"', '"termination"')
res = {}
for f in sys.argv[2:]:
    a = collections.defaultdict(collections.Counter)
    ex = collections.defaultdict(list)
    with open(f, encoding="utf-8") as fh:
        for ln in fh:
            if not any(k in ln for k in EV):
                continue
            r = json.loads(ln)
            e, d = r.get("event"), r.get("detail") or {}
            if e == "invent":
                a["invent"]["rows"] += 1
                a["invent_park"][str(d.get("park_verdict"))] += 1
                if d.get("pick") not in (None, "none paid"):
                    a["invent"]["picked"] += 1
                    if len(ex["invent_pick"]) < 5:
                        ex["invent_pick"].append({"cycle": r.get("cycle"), "slot": r.get("slot"), "pick": d.get("pick"),
                                                  "priced": d.get("priced")})
            elif e == "abduce":
                a["abduce"]["rows"] += 1
                a["abduce"]["routed_pos"] += int((d.get("routed") or 0) > 0)
                a["abduce"]["new_pos"] += int((d.get("new") or 0) > 0)
                a["abduce"]["routed_sum"] += d.get("routed") or 0
            elif e == "rehearsal":
                a["rehearsal"]["rows"] += 1
                for k in ("rehearsed", "compared", "misses", "links_held_misses"):
                    a["rehearsal"][k] += d.get(k) or 0
            elif e == "contradiction_diagnosed":
                a["diag_verdict"][str(d.get("verdict"))] += 1
            elif e in ("accept", "intent_verdict", "invention_carried", "reuse_install", "system0", "termination"):
                a["n"][e] += 1
                if len(ex[e]) < (5 if e == "accept" else 1):
                    ex[e].append({"cycle": r.get("cycle"), "slot": r.get("slot"), "step": r.get("step"),
                                  "detail": json.dumps(d, default=str)[:600]})
    tag = os.path.relpath(f, "C:/TETHER_RUNS").replace("\\", "/")
    res[tag] = {"agg": {k: dict(v) for k, v in a.items()}, "ex": dict(ex)}
    print(tag, json.dumps({k: dict(v) for k, v in a.items()}))
json.dump(res, open(sys.argv[1], "w", encoding="utf-8"), default=str)
