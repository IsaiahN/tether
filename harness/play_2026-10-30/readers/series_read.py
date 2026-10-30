"""Read-only (the reviewer r267 item 3): each game's first action and position across rounds, routed slots at step 1
(from the stream's first-step ROUTE rows is not needed: switch.tsv's position and first only), and which games rise
in every round-to-round pair. argv: PLAY dir name, rounds (in order)."""
import sys

sys.dont_write_bytecode = True
P = f"C:/TETHER_RUNS/S6_2026-10-19/{sys.argv[1]}"
rounds = sys.argv[2:]
ser: dict = {}
for rnd in rounds:
    for ln in open(f"{P}/{rnd}/switch.tsv", encoding="utf-8"):
        f = ln.rstrip("\n").split("\t")
        if len(f) > 14 and f[0].isdigit():
            ser.setdefault(f[1], {})[rnd] = (int(f[0]), None if f[14] == "None" else float(f[14]))
full = {g: s for g, s in ser.items() if all(r in s and s[r][1] is not None for r in rounds)}
print(f"games in every round with a first action: {len(full)} of {len(ser)}")
rise = []
for g in sorted(full, key=lambda g: -full[g][rounds[-1]][1]):
    s = full[g]
    fs = [s[r][1] for r in rounds]
    up = all(b > a for a, b in zip(fs, fs[1:], strict=False))
    rise += [g] if up else []
    print(f"  {g}: " + " | ".join(f"{r[-2:]} pos {s[r][0]:>2} first {s[r][1]:>6}" for r in rounds)
          + ("   RISES EVERY ROUND" if up else ""))
print(f"rise in every round-to-round pair: {len(rise)} of {len(full)}: {rise}")
missing = sorted(set(ser) - set(full))
print(f"not in every round (yet): {missing}")
