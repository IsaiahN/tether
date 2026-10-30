#!/bin/bash
# r361's re-run on the 1c tree + edit_r361, at Idle while round 3 plays
W=/c/Users/Admin/Documents/GitHub/tether
S=/c/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad
cd $W
O=$S/run_r361.txt; echo "start $(date +%H:%M:%S) Idle, $(git rev-parse --short HEAD) + 1c + r361 (diff $(git diff HEAD -- . ':!.claude' | sha256sum | cut -c1-16))" > $O
export PYTHONDONTWRITEBYTECODE=1
for c in check_s1_mustfail_reprice check_s1_reprice; do s=$(date +%s); timeout 295 .venv/Scripts/python.exe -B tests/test_ask.py $c > $S/r361_$c.out 2>&1; echo "test_ask $c rc $? $(( $(date +%s)-s )) s | $(grep -v '^ok ' $S/r361_$c.out | tail -1 | cut -c1-200)" >> $O; done
for c in $(grep -o "^def check_[a-z0-9_]*" tests/test_stop_rules.py | sed 's/def //'); do s=$(date +%s); timeout 295 .venv/Scripts/python.exe -B tests/test_stop_rules.py $c > $S/r361_sr_$c.out 2>&1; echo "test_stop_rules $c rc $? $(( $(date +%s)-s )) s | $(grep -v '^ok ' $S/r361_sr_$c.out | tail -1 | cut -c1-200)" >> $O; done
.venv/Scripts/python.exe -m ruff check . > /dev/null 2>&1; echo "ruff rc $? ." >> $O
for t in conform/arms.py tests/test_gate_ledger.py; do s=$(date +%s); timeout 590 .venv/Scripts/python.exe -B $t > $S/r361_q.out 2>&1; echo "$t rc $? $(( $(date +%s)-s )) s | $(grep -v '^\s*TETHER_' $S/r361_q.out | tail -1 | cut -c1-160)" >> $O; done
echo "end $(date +%H:%M:%S)" >> $O
