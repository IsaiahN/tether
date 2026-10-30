#!/bin/bash
sleep 2
W=/c/Users/Admin/Documents/GitHub/tether-wt-s1reprice
S=/c/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad
cd $W
O=$S/run_i2.txt; echo "start $(date +%H:%M:%S) Idle, worktree $(git rev-parse --short HEAD) + (I2)" > $O
export PYTHONDONTWRITEBYTECODE=1
for w in fake grid; do s=$(date +%s); timeout 295 .venv/Scripts/python.exe -B $S/reprice_cost.py $W $w 24 > $S/i2cost_$w.out 2>&1; echo "cost $w rc $? $(( $(date +%s)-s )) s | $(head -1 $S/i2cost_$w.out | cut -c1-220)" >> $O; done
for c in $(grep -o "^def check_[a-z0-9_]*" tests/test_ask.py | sed 's/def //'); do s=$(date +%s); timeout 295 .venv/Scripts/python.exe -B tests/test_ask.py $c > $S/i2_$c.out 2>&1; echo "$c rc $? $(( $(date +%s)-s )) s | $(grep -v '^ok ' $S/i2_$c.out | tail -1 | cut -c1-220)" >> $O; done
.venv/Scripts/python.exe -m ruff check . > /dev/null 2>&1; echo "ruff rc $?" >> $O
for t in tests/test_tripwire.py tests/test_arm_modules.py conform/arms.py tests/test_gate.py tests/test_gate_ledger.py; do s=$(date +%s); timeout 590 .venv/Scripts/python.exe -B $t > $S/i2_q.out 2>&1; echo "$t rc $? $(( $(date +%s)-s )) s | $(grep -v '^\s*TETHER_' $S/i2_q.out | tail -1 | cut -c1-160)" >> $O; done
echo "end $(date +%H:%M:%S)" >> $O
