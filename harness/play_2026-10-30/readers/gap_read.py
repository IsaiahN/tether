"""Read-only (r280 (ii)): per cycle, the share of bets whose prediction failed (predicted != actual), switch frames marked.
argv: round numbers. Bets are PERCEIVE rows: the prediction held for this frame against what arrived."""
import collections, json, re, sys
sys.dont_write_bytecode = True
P = "C:/TETHER_RUNS/S6_2026-10-19/PLAY16"
for n in sys.argv[1:]:
    rd = f"{P}/round_{int(n):02d}"
    sw = {}
    for ln in open(f"{rd}/switch.tsv", encoding="utf-8"):
        f = ln.split("\t")
        if f[0].isdigit():
            sw[int(f[3])] = (int(f[0]), f[1])
    tot, bad, fields = collections.Counter(), collections.Counter(), collections.Counter()
    fb = {}
    for ln in open(f"{rd}/stream.jsonl", encoding="utf-8"):
        if '"event": "bet"' in ln:
            r = json.loads(ln); d = r["detail"]; c = r["cycle"]
            if "predicted" not in d or "actual" not in d:
                fields["no_pred"] += 1; continue
            tot[c] += 1; bad[c] += d["predicted"] != d["actual"]
        elif '"event": "frame_break"' in ln:
            r = json.loads(ln); fb[r["cycle"]] = r["detail"].get("broke")
    print(f"round {n}: cycles {len(tot)}, bets {sum(tot.values())}, bets without predicted/actual {fields['no_pred']}")
    ordinary = [bad[c] / tot[c] for c in tot if c not in sw and tot[c]]
    ordinary.sort()
    q = lambda p: ordinary[min(len(ordinary) - 1, int(p * len(ordinary)))]
    print(f"  ordinary frames {len(ordinary)}: failure share min {ordinary[0]:.2f} q50 {q(.5):.2f} q90 {q(.9):.2f} max {ordinary[-1]:.2f}")
    for c in sorted(sw):
        if c == 0:
            continue
        s = bad[c] / tot[c] if tot[c] else float("nan")
        rank = sum(1 for x in ordinary if x >= s) if tot[c] else -1
        print(f"  switch {sw[c][1]}@{sw[c][0]} c{c}: bets {tot[c]} failed {bad[c]} share {s:.2f} | ordinary frames at or above: {rank} | fb {fb.get(c)}")
