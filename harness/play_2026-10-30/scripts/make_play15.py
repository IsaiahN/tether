"""Write PLAY15's chain and precheck from PLAY14's, each change asserted to land exactly once."""
import sys

src_dir, dst_dir = sys.argv[1], sys.argv[2]
G = "d7fd81d1682f114d3eb580d93cccd36576f86d06"
H = "ba01d98012863a21dd787db8a93cbccccd1f553f"


def edit(text, pairs):
    for old, new in pairs:
        assert text.count(old) == 1, (text.count(old), old[:80])
        text = text.replace(old, new)
    return text


common = [
    ('P="C:/TETHER_RUNS/S6_2026-10-19/PLAY14"', 'P="C:/TETHER_RUNS/S6_2026-10-19/PLAY15"'),
    ('T="C:/TETHER_RUNS/S6_2026-10-19/split/fresh_r19/arc-solver-agent"',
     'T="C:/TETHER_RUNS/S6_2026-10-19/split/fresh_r20/arc-solver-agent"'),
    ("G=ae028d6527124de0e05d6e98da9ee75dde49db93", f"G={G}"),
    ("H=9f77f70510c5c7454c0588778aa953b08691b346", f"H={H}"),
]

chain = open(f"{src_dir}/play_chain.sh", encoding="utf-8", newline="").read()
chain = edit(chain, common + [
    ("#!/bin/bash\n",
     "#!/bin/bash\n# PLAY15 = PLAY14 on the NEW tree: arc-solver-agent ba01d98 (general-agent d7fd81d, B1 whole mints per step:\n"
     "# TETHER_STEP_MINT, + README), a fresh clone split/fresh_r20 with M3 (the reviewer 2026-10-26 r252), with the same\n"
     "# E4B_SPY box; from 2c535e6f (PLAY14 r1's kept generation). Open-ended; the STOP file is the exit.\n"),
])
open(f"{dst_dir}/play_chain.sh", "w", encoding="utf-8", newline="").write(chain)

pre = open(f"{src_dir}/precheck.sh", encoding="utf-8", newline="").read()
pre = edit(pre, common + [
    ('[ "$(cat "$P/head.txt")" = "ce48227898899cc7" ] && say "GATE head.txt ce48227898899cc7" || say "GATE FAIL head.txt"',
     '[ "$(cat "$P/head.txt")" = "2c535e6f5e08e7d0" ] && say "GATE head.txt 2c535e6f5e08e7d0" || say "GATE FAIL head.txt"'),
])
open(f"{dst_dir}/precheck.sh", "w", encoding="utf-8", newline="").write(pre)
print("written")
