"""Read-only (the reviewer r279 (i)): m1 as far as the rows allow. Park rows keep counts and only the FIRST 12 cuts
(tether.py:15634 cuts[:12]), so the exact share of mint k's priced candidates that mint k-1 priced is NOT in the ledger.
What is: for consecutive parks of the SAME slot in one life, the overlap of their first-12 cut names (the cheapest end
of each search), and both mints' seen / tried counts. argv: rounds."""
import collections
import json
import sys

sys.dont_write_bytecode = True
P = "C:/TETHER_RUNS/S6_2026-10-19/PLAY16"
pairs = []
for n in sys.argv[1:]:
    last = {}
    for ln in open(f"{P}/round_{int(n):02d}/stream.jsonl", encoding="utf-8"):
        if '"event": "park"' not in ln:
            continue
        r = json.loads(ln)
        d = r.get("detail") or {}
        cuts = [c.get("name") for c in (d.get("cuts") or []) if isinstance(c, dict)]
        cur = (r["cycle"], set(cuts), d.get("candidates_seen"), d.get("candidates_tried"),
               bool(d.get("budget_exhausted")))
        s = r["slot"]
        if s in last and last[s][0] < cur[0] and cuts and last[s][1]:
            pairs.append((n, s, last[s], cur, len(cur[1] & last[s][1]) / len(cur[1])))
        last[s] = cur
print(f"consecutive same-slot park pairs (later cycle, both with cuts): {len(pairs)}")
if pairs:
    ov = [p[4] for p in pairs]
    hist = collections.Counter(round(x, 1) for x in ov)
    print(f"overlap of first-12 cuts (share of mint k's cut names already cut by mint k-1): "
          f"mean {sum(ov) / len(ov):.3f}; ==1.0 in {sum(1 for x in ov if x == 1.0)}; ==0 in "
          f"{sum(1 for x in ov if x == 0)}; histogram {dict(sorted(hist.items()))}")
    both_ex = [p for p in pairs if p[2][4] and p[3][4]]
    print(f"pairs where BOTH mints stopped at the bound: {len(both_ex)}; their mean overlap "
          f"{(sum(p[4] for p in both_ex) / len(both_ex)) if both_ex else float('nan'):.3f}")
    for p in pairs[:: max(1, len(pairs) // 8)][:8]:
        n, s, a, b, o = p
        print(f"  r{n} {s}: c{a[0]} seen {a[2]} tried {a[3]} ex {a[4]} -> c{b[0]} seen {b[2]} tried {b[3]} ex {b[4]}; "
              f"overlap {o:.2f}")
