#!/bin/bash
# r349: the one-row-test refactor, at Idle, queued behind run_i2 (5976) and run_table (9544)
W=/c/Users/Admin/Documents/GitHub/tether-wt-s1r2
S=/c/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad
O=$S/run_r349.txt; echo "queued $(date +%H:%M:%S)" > $O
until ! tasklist //FI "PID eq 5976" | grep -q " 5976 " && ! tasklist //FI "PID eq 9544" | grep -q " 9544 "; do sleep 30; done
cd $W
echo "start $(date +%H:%M:%S) Idle, worktree $(git rev-parse --short HEAD) + (I2) + r349" >> $O
export PYTHONDONTWRITEBYTECODE=1
for w in fake grid; do s=$(date +%s); timeout 295 .venv/Scripts/python.exe -B $S/reprice_cost.py $W $w 24 > $S/r349cost_$w.out 2>&1; echo "cost $w rc $? $(( $(date +%s)-s )) s | $(head -1 $S/r349cost_$w.out | cut -c1-220)" >> $O; done
for f in test_ask test_divide; do
  for c in $(grep -o "^def check_[a-z0-9_]*" tests/$f.py | sed 's/def //'); do s=$(date +%s); timeout 295 .venv/Scripts/python.exe -B tests/$f.py $c > $S/r349_${f}_$c.out 2>&1; echo "$f $c rc $? $(( $(date +%s)-s )) s | $(grep -v '^ok ' $S/r349_${f}_$c.out | tail -1 | cut -c1-200)" >> $O; done
done
for fc in "test_arrival_gap check_off_identity_plain" "test_arrival_gap check_off_identity_miss_a" "test_instance_retire check_off_identity" "test_kind_save check_off_identity" "test_settle_pred check_off_identity_fake" "test_settle_pred check_off_identity_gridworld" "test_owed_rejudge check_off_identity_grid" "test_owed_rejudge check_off_identity_fake"; do
  set -- $fc; s=$(date +%s); timeout 295 .venv/Scripts/python.exe -B tests/$1.py $2 > $S/r349tb_$1_$2.out 2>&1
  echo "$1 $2 rc $? $(( $(date +%s)-s )) s | $(grep -v '^ok ' $S/r349tb_$1_$2.out | tail -1 | cut -c1-200)" >> $O
done
.venv/Scripts/python.exe -m ruff check . > /dev/null 2>&1; echo "ruff rc $?" >> $O
for t in tests/test_tripwire.py tests/test_arm_modules.py conform/arms.py tests/test_gate.py tests/test_gate_ledger.py; do s=$(date +%s); timeout 590 .venv/Scripts/python.exe -B $t > $S/r349_q.out 2>&1; echo "$t rc $? $(( $(date +%s)-s )) s | $(grep -v '^\s*TETHER_' $S/r349_q.out | tail -1 | cut -c1-160)" >> $O; done
echo "end $(date +%H:%M:%S)" >> $O
