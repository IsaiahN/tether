"""Write PLAY13's chain and precheck from PLAY12's, each change asserted to land exactly once."""
import sys

src_dir, dst_dir = sys.argv[1], sys.argv[2]
G = "0b027bad045c8d75923c7c33813224e179a71e3c"
H = "8dae023fabb11b1eaa5d292e168bac5e2ef4c421"


def edit(text, pairs):
    for old, new in pairs:
        assert text.count(old) == 1, (text.count(old), old[:80])
        text = text.replace(old, new)
    return text


common = [
    ('P="C:/TETHER_RUNS/S6_2026-10-19/PLAY12"', 'P="C:/TETHER_RUNS/S6_2026-10-19/PLAY13"'),
    ('T="C:/TETHER_RUNS/S6_2026-10-19/split/fresh_r17/arc-solver-agent"',
     'T="C:/TETHER_RUNS/S6_2026-10-19/split/fresh_r18/arc-solver-agent"'),
    ("G=8314ed61f7cdf9c100dc0d152c4657e01db8bc6c", f"G={G}"),
    ("H=2e77f1696ccd246e6affff1c466bf1331f20d78e", f"H={H}"),
]

chain = open(f"{src_dir}/play_chain.sh", encoding="utf-8", newline="").read()
chain = edit(chain, common + [
    ("#!/bin/bash\n",
     "#!/bin/bash\n# PLAY13 = PLAY12 on the NEW tree: arc-solver-agent 8dae023 (general-agent 0b027ba, the limbs, + README), a fresh clone\n"
     "# split/fresh_r18 (the reviewer 2026-10-26 10:33 CDT), with the same E4B_SPY box; from 467ff7e8 (PLAY12 r1 restored). THE\n"
     "# chain.log FIX, BOTH (the reviewer 10:20): a fresh chain.log per launch (refused if one exists), the seed lookup takes\n"
     "# the last match, and exactly one SEED line per round is asserted before round 1.\n"),
    ('WANT="$(cat "$P/play_chain.want")"',
     '[ ! -s "$L" ] || { echo "STOP $L exists: a fresh chain.log per launch (the reviewer 2026-10-26 10:20)"; exit 2; }\n'
     'WANT="$(cat "$P/play_chain.want")"'),
    ("U0=20261026T131047Z   # the first launch's, so the relaunch keeps its seeds (r1 9a2ede8f; the reviewer 2026-10-26 08:23)",
     "U0=$(date -u +%Y%m%dT%H%M%SZ)"),
    ('echo "$(date +%H:%M:%S) seeds fixed; waiting 180 s before round 1" >> "$L"',
     '[ -z "$(grep \'^SEED round \' "$L" | awk \'{print $3}\' | sort | uniq -d)" ] || { echo "STOP a round holds more than one SEED line" >> "$L"; exit 2; }\n'
     'echo "$(date +%H:%M:%S) seeds fixed; one SEED line per round; waiting 180 s before round 1" >> "$L"'),
    ("""seed=$(grep "^SEED round $r " "$L" | awk '{print $4}')""",
     """seed=$(grep "^SEED round $r " "$L" | awk '{print $4}' | tail -1)"""),
])
open(f"{dst_dir}/play_chain.sh", "w", encoding="utf-8", newline="").write(chain)

pre = open(f"{src_dir}/precheck.sh", encoding="utf-8", newline="").read()
pre = edit(pre, common + [
    ('[ ! -e "$T/lineage" ] && say "GATE no lineage folder in the clone" || say "GATE FAIL lineage folder"',
     '[ ! -e "$T/lineage" ] && say "GATE no lineage folder in the clone" || say "GATE FAIL lineage folder"\n'
     '[ ! -e "$P/chain.log" ] && say "GATE no chain.log yet (a fresh log per launch)" || say "GATE FAIL chain.log exists"\n'
     '[ "$(cat "$P/head.txt")" = "467ff7e8f846469b" ] && say "GATE head.txt 467ff7e8f846469b" || say "GATE FAIL head.txt"\n'
     '[ "$(grep -c "uniq -d" "$P/play_chain.sh")" = "1" ] && [ "$(grep -c "| tail -1)" "$P/play_chain.sh")" = "1" ] '
     '&& say "GATE the chain asserts one SEED line per round and takes the last match" || say "GATE FAIL the SEED checks"\n'
     '[ ! -e "$P/STOP" ] && say "GATE no STOP file" || say "GATE FAIL a STOP file is present"'),
])
open(f"{dst_dir}/precheck.sh", "w", encoding="utf-8", newline="").write(pre)
print("written")
