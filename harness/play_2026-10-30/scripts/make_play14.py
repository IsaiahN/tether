"""Write PLAY14's chain and precheck from PLAY13's, each change asserted to land exactly once."""
import sys

src_dir, dst_dir = sys.argv[1], sys.argv[2]
G = "ae028d6527124de0e05d6e98da9ee75dde49db93"
H = "9f77f70510c5c7454c0588778aa953b08691b346"


def edit(text, pairs):
    for old, new in pairs:
        assert text.count(old) == 1, (text.count(old), old[:80])
        text = text.replace(old, new)
    return text


common = [
    ('P="C:/TETHER_RUNS/S6_2026-10-19/PLAY13"', 'P="C:/TETHER_RUNS/S6_2026-10-19/PLAY14"'),
    ('T="C:/TETHER_RUNS/S6_2026-10-19/split/fresh_r18/arc-solver-agent"',
     'T="C:/TETHER_RUNS/S6_2026-10-19/split/fresh_r19/arc-solver-agent"'),
    ("G=0b027bad045c8d75923c7c33813224e179a71e3c", f"G={G}"),
    ("H=8dae023fabb11b1eaa5d292e168bac5e2ef4c421", f"H={H}"),
]

chain = open(f"{src_dir}/play_chain.sh", encoding="utf-8", newline="").read()
chain = edit(chain, common + [
    ("#!/bin/bash\n",
     "#!/bin/bash\n# PLAY14 = PLAY13 on the NEW tree: arc-solver-agent 9f77f70 (general-agent ae028d6, think-or-act at the step: A1\n"
     "# TETHER_STEP_ACT, A2 TETHER_WALK_BUDGET, + README), a fresh clone split/fresh_r19 (the reviewer 2026-10-26 13:01 CDT), with\n"
     "# the same E4B_SPY box; from ce482278 (PLAY13 r1's kept generation). Open-ended; the STOP file is the exit.\n"),
])
open(f"{dst_dir}/play_chain.sh", "w", encoding="utf-8", newline="").write(chain)

pre = open(f"{src_dir}/precheck.sh", encoding="utf-8", newline="").read()
pre = edit(pre, common + [
    ('[ "$(cat "$P/head.txt")" = "467ff7e8f846469b" ] && say "GATE head.txt 467ff7e8f846469b" || say "GATE FAIL head.txt"',
     '[ "$(cat "$P/head.txt")" = "ce48227898899cc7" ] && say "GATE head.txt ce48227898899cc7" || say "GATE FAIL head.txt"'),
])
open(f"{dst_dir}/precheck.sh", "w", encoding="utf-8", newline="").write(pre)
print("written")
