"""Read-only (r280 (ii)): the held-value failure share (held slots at c-1 not carried with the same value into c's bets)
on ORDINARY boundaries, the bar's population. argv: rounds; env PLAY."""
import json, os, sys
sys.dont_write_bytecode = True
P = os.environ.get("PLAY", "C:/TETHER_RUNS/S6_2026-10-19/PLAY16")
allv = []
for n in sys.argv[1:]:
    rd = f"{P}/round_{int(n):02d}"
    sw = set()
    for ln in open(f"{rd}/switch.tsv", encoding="utf-8"):
        f = ln.split("\t")
        if f[0].isdigit():
            sw.add(int(f[3]))
    act, frm = {}, {}
    for ln in open(f"{rd}/stream.jsonl", encoding="utf-8"):
        if '"event": "bet"' in ln:
            r = json.loads(ln); d = r["detail"]; c = r["cycle"]; s = r["slot"]
            if not s.startswith("o"):
                continue
            frm.setdefault(c, {})[s] = d.get("from_value")
            if "actual" in d and not d.get("vanished"):
                act.setdefault(c, {})[s] = d["actual"]
    for c in sorted(frm):
        if c in sw or c - 1 not in act:
            continue
        held = act[c - 1]
        fail = sum(1 for s, v in held.items() if s not in frm[c] or frm[c][s] != v)
        allv.append((fail / len(held), n, c, fail, len(held)))
allv.sort()
print(f"{P[-6:]} ordinary boundaries {len(allv)}; held-failure: zero in {sum(1 for x in allv if x[0] == 0)}; top 8: {[(round(x[0],3), 'r'+str(x[1]), 'c'+str(x[2]), x[3], x[4]) for x in allv[-8:]]}")
