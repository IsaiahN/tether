"""E8 Q16-Q21, one pass per ledger (background mode). Per ledger: counts of the events that mark each Fig 3 link;
the consecutive-RESET count (from the "action" field of any row that carries one, in seq order); quit/termination
rows; and the abstention verdict denominators. argv: out_json ledger..."""
import collections
import ctypes
import json
import os
import sys

ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00100000)
LINK = {
    "1 perception": ("bet",),
    "2 vocabulary": ("pull", "reuse_install", "lookup", "library"),
    "3 objective": ("want", "g1_want", "echo_want", "want_only", "goal_choice", "goal_hypotheses", "derived_new"),
    "4 planning": ("routine", "routine_end", "routine_cut", "routine_inert", "intent", "decision"),
    "5 learn+carry": ("settle", "promote", "hold", "cite", "invention_carried"),
}
EV = {e for v in LINK.values() for e in v} | {"termination", "quit", "ending", "choice", "system0", "route"}
res = {}
for f in sys.argv[2:]:
    c = collections.Counter()
    acts, ends = [], []
    with open(f, encoding="utf-8") as fh:
        for ln in fh:
            r = None
            if '"action"' in ln:
                r = json.loads(ln)
                a = (r.get("detail") or {}).get("action")
                if isinstance(a, str) and r.get("event") in ("decision", "choice", "system0", "act", "bet"):
                    acts.append((r.get("cycle"), a))
            if not any(f'"{e}"' in ln for e in EV):
                continue
            r = r or json.loads(ln)
            e = r.get("event")
            if e in EV:
                c[e] += 1
                if e in ("termination", "quit", "ending"):
                    d = r.get("detail") or {}
                    ends.append({k: d.get(k) for k in ("how", "class", "why", "reads") if k in d})
    seen, rr = {}, 0
    for cyc, a in acts:
        seen.setdefault(cyc, a)
    seq = [seen[k] for k in sorted(seen)]
    rr = sum(1 for x, y in zip(seq, seq[1:]) if x == y == "RESET")
    tag = os.path.relpath(f, "C:/TETHER_RUNS").replace("\\", "/")
    links = {k: sum(c[e] for e in v) for k, v in LINK.items()}
    res[tag] = {"links": links, "counts": dict(c), "reset_reset": rr, "acts": len(seq),
                "resets": seq.count("RESET"), "ends": ends[:4]}
    print(tag.split("/")[-1], json.dumps(links), "acts", len(seq), "RESET", seq.count("RESET"), "RESET,RESET", rr)
json.dump(res, open(sys.argv[1], "w", encoding="utf-8"), default=str)
