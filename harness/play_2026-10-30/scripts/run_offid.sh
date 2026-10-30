#!/bin/bash
sleep 2
cd /c/Users/Admin/Documents/GitHub/tether
S=/c/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad
O=$S/run_offid.txt; echo "start $(date +%H:%M:%S) Idle" > $O
export PYTHONDONTWRITEBYTECODE=1
for fc in "test_ask check_off_identity_grid" "test_ask check_off_identity_fake"; do set -- $fc; s=$(date +%s); timeout 295 .venv/Scripts/python.exe -B tests/$1.py $2 > $S/oi_$1_$2.out 2>&1; echo "$1 $2 rc $? $(( $(date +%s)-s )) s | $(grep -v '^ok ' $S/oi_$1_$2.out | tail -1 | cut -c1-200)" >> $O; done
echo "end $(date +%H:%M:%S)" >> $O
