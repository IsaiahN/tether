import os, pstats, sys
st = pstats.Stats(sys.argv[1])
rows = []
for (f, ln, fn), (cc, nc, tt, ct, _callers) in st.stats.items():
    rows.append((fn, f"{os.path.basename(f)}:{ln}", nc, tt, ct))
total = max(r[4] for r in rows)
print(f"total cumulative (top) {total:.1f} s; functions {len(rows)}")
for key, name in ((4, "CUMULATIVE"), (3, "TOTTIME")):
    print(f"== top 25 by {name}: name file:line ncalls tottime cumtime")
    for r in sorted(rows, key=lambda r: -r[key])[:25]:
        print(f"  {r[0]} {r[1]} {r[2]} {r[3]:.2f} {r[4]:.2f}")
want = ("_reafferent", "aim_cell", "_acted", "_held_by", "_mover", "action_kinds", "_kind_of_action", "_kinds")
print("== the named sites anywhere in the profile (name file:line ncalls tottime cumtime):")
for r in sorted(rows, key=lambda r: -r[4]):
    if any(w in r[0] for w in want):
        print(f"  {r[0]} {r[1]} {r[2]} {r[3]:.3f} {r[4]:.3f}")
