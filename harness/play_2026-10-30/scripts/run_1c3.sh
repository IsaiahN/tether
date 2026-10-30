#!/bin/bash
# 1c rebased on 2855932 (main checkout, uncommitted), the standard gates only (r354), at Idle while round 3 plays
W=/c/Users/Admin/Documents/GitHub/tether
S=/c/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad
cd $W
O=$S/run_1c3.txt; echo "start $(date +%H:%M:%S) Idle, $(git rev-parse --short HEAD) + 1c (diff $(git diff HEAD -- . ':!.claude' | sha256sum | cut -c1-16))" > $O
export PYTHONDONTWRITEBYTECODE=1
for f in test_stop_rules test_ask; do
  for c in $(grep -o "^def check_[a-z0-9_]*" tests/$f.py | sed 's/def //'); do s=$(date +%s); timeout 295 .venv/Scripts/python.exe -B tests/$f.py $c > $S/c3_${f}_$c.out 2>&1; echo "$f $c rc $? $(( $(date +%s)-s )) s | $(grep -v '^ok ' $S/c3_${f}_$c.out | tail -1 | cut -c1-200)" >> $O; done
done
for fc in "test_arrival_gap check_off_identity_plain" "test_arrival_gap check_off_identity_miss_a" "test_instance_retire check_off_identity" "test_kind_save check_off_identity" "test_settle_pred check_off_identity_fake" "test_settle_pred check_off_identity_gridworld" "test_divide check_off_identity_grid" "test_divide check_off_identity_fake" "test_divide check_credit_off_identity_grid" "test_divide check_credit_off_identity_fake" "test_owed_rejudge check_off_identity_grid" "test_owed_rejudge check_off_identity_fake"; do
  set -- $fc; s=$(date +%s); timeout 295 .venv/Scripts/python.exe -B tests/$1.py $2 > $S/c3tb_$1_$2.out 2>&1
  echo "$1 $2 rc $? $(( $(date +%s)-s )) s | $(grep -v '^ok ' $S/c3tb_$1_$2.out | tail -1 | cut -c1-200)" >> $O
done
.venv/Scripts/python.exe -m ruff check . > /dev/null 2>&1; echo "ruff rc $?" >> $O
for t in tests/test_tripwire.py tests/test_arm_modules.py conform/arms.py tests/test_gate.py tests/test_gate_ledger.py; do s=$(date +%s); timeout 590 .venv/Scripts/python.exe -B $t > $S/c3_q.out 2>&1; echo "$t rc $? $(( $(date +%s)-s )) s | $(grep -v '^\s*TETHER_' $S/c3_q.out | tail -1 | cut -c1-160)" >> $O; done
echo "end $(date +%H:%M:%S)" >> $O
