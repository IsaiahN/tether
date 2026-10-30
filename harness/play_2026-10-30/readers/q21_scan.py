"""Q6/Q21: 'leave' rows (with their unbundled field), recurse_parts rows, and every row whose text carries
'unreachable at this budget', 'undiagnosed', 'abstain' or 'unreached' -- counted by (event, phrase), first example
of leave kept; background mode. argv: ledger..."""
import collections
import ctypes
import json
import sys

ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00100000)
PH = ("unreachable at this budget", "undiagnosed", "abstain", "unreached")
c, ex = collections.Counter(), {}
for f in sys.argv[1:]:
    with open(f, encoding="utf-8") as fh:
        for ln in fh:
            hit = [p for p in PH if p in ln]
            if not hit and '"leave"' not in ln and "recurse_parts" not in ln:
                continue
            r = json.loads(ln)
            e = r.get("event")
            if e in ("leave", "recurse_parts"):
                d = r.get("detail") or {}
                c[(e, "unbundled" if d.get("unbundled") else "plain")] += 1
                ex.setdefault(e, json.dumps(r)[:600])
            for p in hit:
                c[(e, p)] += 1
for k, v in c.most_common(40):
    print(v, k)
for e, s in ex.items():
    print("EXAMPLE", s)
