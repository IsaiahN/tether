"""Every row mentioning an AGENT-INVENTED term, by (step, event) and by status/verdict fields, across ledgers;
background mode. argv: ledger..."""
import collections
import ctypes
import json
import sys

ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00100000)
c, st, ex = collections.Counter(), collections.Counter(), {}
for f in sys.argv[1:]:
    with open(f, encoding="utf-8") as fh:
        for ln in fh:
            if "AGENT-INVENTED" not in ln:
                continue
            r = json.loads(ln)
            k = (r.get("step"), r.get("event"))
            c[k] += 1
            d = r.get("detail") or {}
            for fld in ("status", "verdict", "outcome", "result", "settled"):
                if fld in d:
                    st[(k, fld, str(d[fld])[:40])] += 1
            ex.setdefault(k, json.dumps(r)[:350])
for k, v in c.most_common():
    print(v, k)
print("--- status/verdict fields")
for k, v in st.most_common(25):
    print(v, k)
print("--- one example per kind (settle/promote/import only)")
for k, s in ex.items():
    if k[0] in ("SETTLE", "PROMOTE", "IMPORT"):
        print(k, s)
