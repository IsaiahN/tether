#!/bin/bash
# after the release-row edits (@_in_step MINT; end/level releases on "@owed") and r335 (a): the checks they touch
sleep 2   # Start-Process sets Idle on this bash before any child starts; children inherit it
cd /c/Users/Admin/Documents/GitHub/tether
S=/c/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad
O=$S/run_1d_b.txt; echo "start $(date +%H:%M:%S)" > $O
export PYTHONDONTWRITEBYTECODE=1
for c in check_a_sources_explained check_a_mustfail_r281_guard check_d_mustfail_off check_f_reraised check_g_tried_never_shrinks; do s=$(date +%s); timeout 295 .venv/Scripts/python.exe -B tests/test_owed_rejudge.py $c > $S/rb_$c.out 2>&1; echo "$c rc $? $(( $(date +%s)-s )) s | $(grep -v '^ok ' $S/rb_$c.out | tail -1 | cut -c1-240)" >> $O; done
for t in "tests/test_step_mint.py check_e_every_step_scope_decorator_kept" tests/test_tripwire.py tests/test_gate.py conform/arms.py; do s=$(date +%s); timeout 295 .venv/Scripts/python.exe -B $t > $S/rb_q.out 2>&1; echo "$t rc $? $(( $(date +%s)-s )) s | $(grep -v '^\s*TETHER_' $S/rb_q.out | tail -1 | cut -c1-160)" >> $O; done
.venv/Scripts/python.exe -m ruff check . > /dev/null 2>&1; echo "ruff rc $?" >> $O
echo "end $(date +%H:%M:%S)" >> $O
