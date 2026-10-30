#!/bin/bash
# 1d's remaining checks, each in its own process; then the B1/B2 files whole, the quick set and test_gate_ledger
cd /c/Users/Admin/Documents/GitHub/tether
S=/c/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad
O=$S/run_1d.txt; : > $O
export PYTHONDONTWRITEBYTECODE=1
one() { s=$(date +%s); timeout 295 .venv/Scripts/python.exe -B "$@" > $S/r1d_$(basename $1 .py)_${2:-all}.out 2>&1; rc=$?; echo "$1 ${2:-all} rc $rc $(( $(date +%s)-s )) s | $(grep -v '^ok ' $S/r1d_$(basename $1 .py)_${2:-all}.out | tail -1 | cut -c1-240)" >> $O; }
for c in check_g_tried_never_shrinks check_g_mustfail_prefix_supersede check_h_on_first_mint_by_rank check_i_on_derived_a1_order check_c_rank_first check_c_mustfail_code_order check_tie_plain_first check_off_identity_grid check_off_identity_fake; do one tests/test_owed_rejudge.py $c; done
for c in $(grep -o "^def check_[a-z0-9_]*" tests/test_step_mint.py | sed 's/def //'); do one tests/test_step_mint.py $c; done
for c in $(grep -o "^def check_[a-z0-9_]*" tests/test_step_derived.py | sed 's/def //'); do one tests/test_step_derived.py $c; done
.venv/Scripts/python.exe -m ruff check . > $S/r1d_ruff.out 2>&1; echo "ruff rc $?" >> $O
for t in tests/test_tripwire.py tests/test_arm_modules.py conform/arms.py tests/test_gate.py tests/test_gate_ledger.py; do s=$(date +%s); timeout 590 .venv/Scripts/python.exe -B $t > $S/r1d_q_$(basename $t .py).out 2>&1; echo "$t rc $? $(( $(date +%s)-s )) s | $(grep -v '^\s*TETHER_' $S/r1d_q_$(basename $t .py).out | tail -1 | cut -c1-160)" >> $O; done
head -1 $S/r1d_q_arms.out >> $O
echo done >> $O
