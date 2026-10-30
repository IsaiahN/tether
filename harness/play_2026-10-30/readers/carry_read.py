"""Read-only (r280 (ii)): across each step boundary c-1 -> c, for slot ids with a scored bet at c-1 (actual) and a bet at c
(from_value), the share whose value changed BETWEEN steps (actual(c-1) != from_value(c)). Nothing acts between steps, so
on an ordinary boundary this is the persistence expectation's failure with no press; at an arrival it is the held frame
failing on the arrived one. Also: frame_break rows' action field (None = arrival). argv: rounds."""
import json, sys
sys.dont_write_bytecode = True
import os
P = os.environ.get("PLAY", "C:/TETHER_RUNS/S6_2026-10-19/PLAY16")
for n in sys.argv[1:]:
    rd = f"{P}/round_{int(n):02d}"
    sw = {}
    for ln in open(f"{rd}/switch.tsv", encoding="utf-8"):
        f = ln.split("\t")
        if f[0].isdigit():
            sw[int(f[3])] = (int(f[0]), f[1])
    act, frm, fb = {}, {}, {}
    for ln in open(f"{rd}/stream.jsonl", encoding="utf-8"):
        if '"event": "bet"' in ln:
            r = json.loads(ln); d = r["detail"]; c = r["cycle"]; s = r["slot"]
            if not s.startswith("o"):
                continue
            frm.setdefault(c, {})[s] = d.get("from_value")
            if "actual" in d and not d.get("vanished"):
                act.setdefault(c, {})[s] = d["actual"]
        elif '"event": "frame_break"' in ln:
            r = json.loads(ln); d = r["detail"]
            fb[r["cycle"]] = (d.get("action"), d.get("found"), d.get("claimed"), d.get("median"), d.get("colour_share"), d.get("broke"))
    rows = []
    for c in sorted(frm):
        if c - 1 not in act:
            continue
        common = [s for s in frm[c] if s in act[c - 1]]
        ch = sum(1 for s in common if frm[c][s] != act[c - 1][s])
        rows.append((c, len(common), ch, len(frm[c]), len(act[c - 1])))
    ordn = sorted(ch / k for c, k, ch, _, _ in rows if c not in sw and k)
    zero = sum(1 for x in ordn if x == 0)
    print(f"round {n}: ordinary boundaries {len(ordn)}; changed-between-steps share: zero in {zero}, max {ordn[-1] if ordn else None:.3f}, "
          f"nonzero values {[round(x,3) for x in ordn if x][:12]}")
    for c, k, ch, nf, na in rows:
        if c in sw and c:
            g = sw[c]
            b = fb.get(c)
            tag = "BROKE" if b and b[5] else "MISSED"
            print(f"  {tag:6s} {g[1]}@{g[0]} c{c}: ids carried {k} of {nf} (prev {na}), changed {ch} share {ch/k if k else float('nan'):.3f}"
                  + (f" | break row action={b[0]} found={b[1]} claimed={b[2]} median={b[3]} colour={b[4]}" if b else " | no break row"))
    extra = [c for c in fb if c not in sw]
    print(f"  break rows off a switch cycle: {extra}; break rows with an action: {[c for c in fb if fb[c][0] is not None]}")
