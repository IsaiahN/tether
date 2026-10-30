"""Write PLAY18's chain and precheck from PLAY17's, each change asserted to land exactly once.
argv: PLAY17 dir, PLAY18 dir, the 16-hex head PLAY18 starts from, a short note naming that head."""
import sys

src_dir, dst_dir, head, note = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
assert len(head) == 16 and all(c in "0123456789abcdef" for c in head), head
G = "549f403e220cbaadb392c4639ffe7887c6ef2575"
H = "45234bab4f23bbedd3ee79bcea0fd56c5a3793af"


def edit(text, pairs):
    for old, new in pairs:
        assert text.count(old) == 1, (text.count(old), old[:80])
        text = text.replace(old, new)
    return text


common = [
    ('P="C:/TETHER_RUNS/S6_2026-10-19/PLAY17"', 'P="C:/TETHER_RUNS/S6_2026-10-19/PLAY18"'),
    ('T="C:/TETHER_RUNS/S6_2026-10-19/split/fresh_r23/arc-solver-agent"',
     'T="C:/TETHER_RUNS/S6_2026-10-19/split/fresh_r24/arc-solver-agent"'),
    ("G=6c04c56a0043548e6411e8f528bff00c3f9dfb04", f"G={G}"),
    ("H=5153347457d4d081dc0ebdd45dfd7b4d916c2d30", f"H={H}"),
    # r305 step 4: the modules decisions 2+3 changed, hashed by name beside the head check
    ('"$T/conform/arms.py" | cut -c1-16',
     '"$T/conform/arms.py" "$T/gamma.py" "$T/lineage.py" | cut -c1-16'),
]

chain = open(f"{src_dir}/play_chain.sh", encoding="utf-8", newline="").read()
chain = edit(chain, common + [
    ("#!/bin/bash\n",
     "#!/bin/bash\n# PLAY18 = PLAY17 on the NEW tree: arc-solver-agent 45234ba (general-agent 549f403, decisions\n"
     "# 2+3: TETHER_INSTANCE_RETIRE, TETHER_KIND_SAVE, TETHER_SETTLE_PRED, + README), a fresh clone\n"
     f"# split/fresh_r24 with M3 (the reviewer r305), the same E4B_SPY box; from {head[:8]} ({note}).\n"
     "# Open-ended; the STOP file is the exit.\n"),
])
open(f"{dst_dir}/play_chain.sh", "w", encoding="utf-8", newline="").write(chain)

pre = open(f"{src_dir}/precheck.sh", encoding="utf-8", newline="").read()
pre = edit(pre, common + [
    ('[ "$(cat "$P/head.txt")" = "fa086387e04eee9e" ] && say "GATE head.txt fa086387e04eee9e" || say "GATE FAIL head.txt"',
     f'[ "$(cat "$P/head.txt")" = "{head}" ] && say "GATE head.txt {head}" || say "GATE FAIL head.txt"'),
])
open(f"{dst_dir}/precheck.sh", "w", encoding="utf-8", newline="").write(pre)
print("written")
