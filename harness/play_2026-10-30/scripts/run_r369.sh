#!/bin/bash
W=/c/Users/Admin/Documents/GitHub/tether
S=/c/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad
cd $W
O=$S/run_r369.txt; echo "start $(date +%H:%M:%S) Idle, $(git rev-parse --short HEAD) + 1e + r369 (diff $(git diff HEAD -- . ':!.claude' | sha256sum | cut -c1-16), test_remainder $(sha256sum tests/test_remainder.py | cut -c1-16))" > $O
export PYTHONDONTWRITEBYTECODE=1
for fc in "test_divide check_credit_flip_identity_grid" "test_divide check_credit_flip_identity_fake" "test_remainder check_c_age"; do
  set -- $fc; s=$(date +%s); timeout 295 .venv/Scripts/python.exe -B tests/$1.py $2 > $S/r369_$1_$2.out 2>&1
  echo "$1 $2 rc $? $(( $(date +%s)-s )) s | $(grep -v '^ok ' $S/r369_$1_$2.out | tail -1 | cut -c1-220)" >> $O
done
.venv/Scripts/python.exe -m ruff check . > /dev/null 2>&1; echo "ruff rc $? ." >> $O
echo "end $(date +%H:%M:%S)" >> $O
