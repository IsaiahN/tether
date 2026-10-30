#!/bin/bash
# 1c's checks at Idle, each in its own process; then the smoke on the r338 code, the quick set, test_gate_ledger
sleep 2
cd /c/Users/Admin/Documents/GitHub/tether
S=/c/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad
O=$S/run_1c2.txt; echo "start $(date +%H:%M:%S)" > $O
export PYTHONDONTWRITEBYTECODE=1
for c in check_i_held check_i_mustfail_not_risky check_i_mustfail_old_key check_ii_none_survive check_ii_mustfail_stale_key check_ii_bar_only check_ii_mustfail_bar_only check_ii_small_rise check_ii_mustfail_small_rise check_ii_stale_cells check_iii_split_refused check_iii_mustfail_off check_iii_owner_read_anew check_iii_spent check_iii_mustfail_no_spend check_bound_fake check_off_identity_grid check_off_identity_fake; do s=$(date +%s); timeout 295 .venv/Scripts/python.exe -B tests/test_stop_rules.py $c > $S/sr_$c.out 2>&1; echo "$c rc $? $(( $(date +%s)-s )) s | $(grep -v '^ok ' $S/sr_$c.out | tail -1 | cut -c1-260)" >> $O; done
for w in fake grid; do timeout 295 .venv/Scripts/python.exe -B $S/stop_smoke.py $w 24 > $S/stop3_$w.out 2>&1; echo "smoke $w rc $? | $(head -1 $S/stop3_$w.out | cut -c1-260)" >> $O; done
.venv/Scripts/python.exe -m ruff check . > /dev/null 2>&1; echo "ruff rc $?" >> $O
for t in tests/test_tripwire.py tests/test_arm_modules.py conform/arms.py tests/test_gate.py "tests/test_step_mint.py check_e_every_step_scope_decorator_kept" tests/test_gate_ledger.py; do s=$(date +%s); timeout 590 .venv/Scripts/python.exe -B $t > $S/sr_q.out 2>&1; echo "$t rc $? $(( $(date +%s)-s )) s | $(grep -v '^\s*TETHER_' $S/sr_q.out | tail -1 | cut -c1-200)" >> $O; done
echo "end $(date +%H:%M:%S)" >> $O
