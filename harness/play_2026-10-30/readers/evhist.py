"""Event histogram per ledger: (step, event) -> count, for the given ledgers; background I/O mode.
argv: out_tsv ledger..."""
import collections
import ctypes
import json
import os
import sys

ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00100000)
out = open(sys.argv[1], "w", encoding="utf-8")
for f in sys.argv[2:]:
    c = collections.Counter()
    n = 0
    with open(f, encoding="utf-8") as fh:
        for ln in fh:
            n += 1
            try:
                r = json.loads(ln)
            except ValueError:
                c[("?", "unparsed")] += 1
                continue
            c[(r.get("step"), r.get("event"))] += 1
    tag = os.path.relpath(f, "C:/TETHER_RUNS").replace("\\", "/")
    for (s, e), k in sorted(c.items(), key=lambda x: (-x[1], str(x[0]))):
        out.write(f"{tag}\t{s}\t{e}\t{k}\n")
    print(tag, "rows", n, "kinds", len(c))
