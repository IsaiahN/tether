"""Read-only (r280 (ii)): every tracker call on the matches rows. Arrival call at a switch = the broke call, else the
call with the lowest median (the new board's first decomposition). Ordinary calls = every call at a non-switch cycle."""
import json, subprocess, sys
sys.dont_write_bytecode = True
import os
P = os.environ.get("PLAY", "C:/TETHER_RUNS/S6_2026-10-19/PLAY16")
ordm, ordc, brk, miss = [], [], [], []
for n in range(1, int(os.environ.get("LAST", "42")) + 1):
    rd = f"{P}/round_{n:02d}"
    sw = {}
    for ln in open(f"{rd}/switch.tsv", encoding="utf-8"):
        f = ln.split("\t")
        if f[0].isdigit():
            sw[int(f[3])] = (int(f[0]), f[1])
    out = subprocess.run(["grep", '"event": "matches"', f"{rd}/stream.jsonl"], capture_output=True, text=True).stdout
    for ln in out.splitlines():
        r = json.loads(ln); c = r["cycle"]; d = r["detail"]; calls = d.get("calls") or []
        if c in sw and c:
            if not calls:
                miss.append((n, sw[c], c, None, d.get("routes"))); continue
            k = next((x for x in calls if x.get("broke")), None) or min(calls, key=lambda x: x.get("median", 1))
            row = (n, sw[c], c, {q: k.get(q) for q in ("found", "claimed", "median", "colour_share", "broke")}, d.get("routes"))
            (brk if k.get("broke") else miss).append(row)
        elif c not in sw:
            for x in calls:
                ordm.append(x.get("median")); ordc.append(x.get("colour_share"))
def qs(v):
    v = sorted(x for x in v if x is not None); g = lambda p: v[min(len(v) - 1, int(p * len(v)))]
    return f"n {len(v)} min {v[0]:.4f} q01 {g(.01):.4f} q05 {g(.05):.4f} q50 {g(.5):.4f} q95 {g(.95):.4f} max {v[-1]:.4f}"
print("ORDINARY calls median:", qs(ordm)); print("ORDINARY calls colour_share:", qs(ordc))
print("ORDINARY calls with median < 0.71:", sum(1 for x in ordm if x is not None and x < .71), " with colour_share > 0.42:", sum(1 for x in ordc if x is not None and x > .42),
      " both:", sum(1 for a, b in zip(ordm, ordc) if a is not None and b is not None and a < .71 and b > .42))
print("BROKE arrival calls median:", qs([r[3]["median"] for r in brk])); print("BROKE arrival calls colour_share:", qs([r[3]["colour_share"] for r in brk]))
for r in miss:
    print("MISSED", f"r{r[0]} {r[1][1]}@{r[1][0]} c{r[2]}", r[3], "routes", r[4])
