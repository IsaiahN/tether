#!/bin/bash
# after the 8th cell field (r345): every 1c check, the 1a/1b/1d files, the OFF identities, the quick set, test_gate_ledger -- at Idle
sleep 2
cd /c/Users/Admin/Documents/GitHub/tether
S=/c/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad
O=$S/run_full.txt; echo "start $(date +%H:%M:%S) Idle" > $O
export PYTHONDONTWRITEBYTECODE=1
for f in test_stop_rules test_ask test_divide test_owed_rejudge; do
  for c in $(grep -o "^def check_[a-z0-9_]*" tests/$f.py | sed 's/def //'); do
    s=$(date +%s); timeout 295 .venv/Scripts/python.exe -B tests/$f.py $c > $S/fu_${f}_$c.out 2>&1
    echo "$f $c rc $? $(( $(date +%s)-s )) s | $(grep -v '^ok ' $S/fu_${f}_$c.out | tail -1 | cut -c1-200)" >> $O
  done
done
.venv/Scripts/python.exe -m ruff check . > /dev/null 2>&1; echo "ruff rc $?" >> $O
for t in tests/test_tripwire.py tests/test_arm_modules.py conform/arms.py tests/test_gate.py tests/test_gate_ledger.py; do s=$(date +%s); timeout 590 .venv/Scripts/python.exe -B $t > $S/fu_q.out 2>&1; echo "$t rc $? $(( $(date +%s)-s )) s | $(grep -v '^\s*TETHER_' $S/fu_q.out | tail -1 | cut -c1-160)" >> $O; done
echo "end $(date +%H:%M:%S)" >> $O
