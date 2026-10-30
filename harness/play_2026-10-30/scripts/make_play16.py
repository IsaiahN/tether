"""Write PLAY16's chain and precheck from PLAY15's, each change asserted to land exactly once.
argv: PLAY15 dir, PLAY16 dir, the 16-hex head PLAY16 starts from, a short note naming that head."""
import sys

src_dir, dst_dir, head, note = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
assert len(head) == 16 and all(c in "0123456789abcdef" for c in head), head
G = "d12c74e004fb124c111d249089589b6464ff9822"
H = "f5453c38d92119c441968e9fd8920f0cd8355941"


def edit(text, pairs):
    for old, new in pairs:
        assert text.count(old) == 1, (text.count(old), old[:80])
        text = text.replace(old, new)
    return text


common = [
    ('P="C:/TETHER_RUNS/S6_2026-10-19/PLAY15"', 'P="C:/TETHER_RUNS/S6_2026-10-19/PLAY16"'),
    ('T="C:/TETHER_RUNS/S6_2026-10-19/split/fresh_r20/arc-solver-agent"',
     'T="C:/TETHER_RUNS/S6_2026-10-19/split/fresh_r22/arc-solver-agent"'),
    ("G=d7fd81d1682f114d3eb580d93cccd36576f86d06", f"G={G}"),
    ("H=ba01d98012863a21dd787db8a93cbccccd1f553f", f"H={H}"),
]

chain = open(f"{src_dir}/play_chain.sh", encoding="utf-8", newline="").read()
chain = edit(chain, common + [
    ("#!/bin/bash\n",
     "#!/bin/bash\n# PLAY16 = PLAY15 on the NEW tree: arc-solver-agent f5453c3 (general-agent d12c74e, the step clock\n"
     "# TETHER_STEP_CLOCK + B2 TETHER_STEP_DERIVED, + README), a fresh clone split/fresh_r22 with M3 (the reviewer r265, r273),\n"
     f"# with the same E4B_SPY box; from {head[:8]} ({note}). Open-ended; the STOP file is the exit.\n"),
])
open(f"{dst_dir}/play_chain.sh", "w", encoding="utf-8", newline="").write(chain)

pre = open(f"{src_dir}/precheck.sh", encoding="utf-8", newline="").read()
pre = edit(pre, common + [
    ('[ "$(cat "$P/head.txt")" = "2c535e6f5e08e7d0" ] && say "GATE head.txt 2c535e6f5e08e7d0" || say "GATE FAIL head.txt"',
     f'[ "$(cat "$P/head.txt")" = "{head}" ] && say "GATE head.txt {head}" || say "GATE FAIL head.txt"'),
])
open(f"{dst_dir}/precheck.sh", "w", encoding="utf-8", newline="").write(pre)
print("written")
