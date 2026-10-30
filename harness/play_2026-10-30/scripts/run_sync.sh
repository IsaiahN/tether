#!/bin/bash
sleep 2
cd /c/Users/Admin/Documents/GitHub/tether
S=/c/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad
O=$S/run_sync.txt; echo "start $(date +%H:%M:%S) Idle" > $O
export PYTHONDONTWRITEBYTECODE=1
for c in check_ii_none_survive check_ii_unsynced check_ii_mustfail_unsynced; do s=$(date +%s); timeout 295 .venv/Scripts/python.exe -B tests/test_stop_rules.py $c > $S/sy_$c.out 2>&1; echo "$c rc $? $(( $(date +%s)-s )) s | $(grep -v '^ok ' $S/sy_$c.out | tail -1 | cut -c1-260)" >> $O; done
timeout 295 .venv/Scripts/python.exe -B $S/stop_smoke.py fake 24 > $S/stop4_fake.out 2>&1; echo "smoke fake rc $? | $(head -1 $S/stop4_fake.out | cut -c1-260)" >> $O
echo "end $(date +%H:%M:%S)" >> $O
