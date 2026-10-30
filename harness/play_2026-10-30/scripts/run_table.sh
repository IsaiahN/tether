#!/bin/bash
# r348 4: at the s1-reprice tip, EVERY batch arm's OFF identity against its own base (later arms off), at Idle
sleep 2
W=/c/Users/Admin/Documents/GitHub/tether-wt-s1reprice
S=/c/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad
cd $W
O=$S/run_table.txt; echo "start $(date +%H:%M:%S) Idle" > $O
export PYTHONDONTWRITEBYTECODE=1
for fc in "test_arrival_gap check_off_identity_plain" "test_arrival_gap check_off_identity_miss_a" "test_instance_retire check_off_identity" "test_kind_save check_off_identity" "test_settle_pred check_off_identity_fake" "test_settle_pred check_off_identity_gridworld" "test_divide check_off_identity_grid" "test_divide check_off_identity_fake" "test_divide check_credit_off_identity_grid" "test_divide check_credit_off_identity_fake" "test_owed_rejudge check_off_identity_grid" "test_owed_rejudge check_off_identity_fake"; do
  set -- $fc; s=$(date +%s); timeout 295 .venv/Scripts/python.exe -B tests/$1.py $2 > $S/tb_$1_$2.out 2>&1
  echo "$1 $2 rc $? $(( $(date +%s)-s )) s | $(grep -v '^ok ' $S/tb_$1_$2.out | tail -1 | cut -c1-220)" >> $O
done
echo "end $(date +%H:%M:%S)" >> $O
