"""Write PLAY17's chain and precheck from PLAY16's, each change asserted to land exactly once.
argv: PLAY16 dir, PLAY17 dir, the 16-hex head PLAY17 starts from, a short note naming that head."""
import sys

src_dir, dst_dir, head, note = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
assert len(head) == 16 and all(c in "0123456789abcdef" for c in head), head
G = "6c04c56a0043548e6411e8f528bff00c3f9dfb04"
H = "5153347457d4d081dc0ebdd45dfd7b4d916c2d30"


def edit(text, pairs):
    for old, new in pairs:
        assert text.count(old) == 1, (text.count(old), old[:80])
        text = text.replace(old, new)
    return text


common = [
    ('P="C:/TETHER_RUNS/S6_2026-10-19/PLAY16"', 'P="C:/TETHER_RUNS/S6_2026-10-19/PLAY17"'),
    ('T="C:/TETHER_RUNS/S6_2026-10-19/split/fresh_r22/arc-solver-agent"',
     'T="C:/TETHER_RUNS/S6_2026-10-19/split/fresh_r23/arc-solver-agent"'),
    ("G=d12c74e004fb124c111d249089589b6464ff9822", f"G={G}"),
    ("H=f5453c38d92119c441968e9fd8920f0cd8355941", f"H={H}"),
    # r288 (b): the modules decision 5 reads, hashed by name beside the head check
    ('"$P/play_across.py" | cut -c1-16',
     '"$P/play_across.py" "$T/arc_percept.py" "$T/arc_world.py" "$T/conform/arms.py" | cut -c1-16'),
]

chain = open(f"{src_dir}/play_chain.sh", encoding="utf-8", newline="").read()
chain = edit(chain, common + [
    ("#!/bin/bash\n",
     "#!/bin/bash\n# PLAY17 = PLAY16 on the NEW tree: arc-solver-agent 5153347 (general-agent 6c04c56, decision 5\n"
     "# TETHER_ARRIVAL_GAP + the step_derived TIMINGS fix, + README), a fresh clone split/fresh_r23 with M3 (the reviewer\n"
     f"# r286, r287), with the same E4B_SPY box; from {head[:8]} ({note}). Open-ended; the STOP file is the exit.\n"),
])
open(f"{dst_dir}/play_chain.sh", "w", encoding="utf-8", newline="").write(chain)

pre = open(f"{src_dir}/precheck.sh", encoding="utf-8", newline="").read()
pre = edit(pre, common + [
    ('[ "$(cat "$P/head.txt")" = "5526aed57fa6f38e" ] && say "GATE head.txt 5526aed57fa6f38e" || say "GATE FAIL head.txt"',
     f'[ "$(cat "$P/head.txt")" = "{head}" ] && say "GATE head.txt {head}" || say "GATE FAIL head.txt"'),
])
open(f"{dst_dir}/precheck.sh", "w", encoding="utf-8", newline="").write(pre)
print("written")
