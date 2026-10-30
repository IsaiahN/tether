#!/bin/bash
export PYTHONDONTWRITEBYTECODE=1
cd /c/Users/Admin/Documents/GitHub/tether
PY=.venv/Scripts/python.exe
L=C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad/run_cw.txt
: > $L
run() { n=$1; shift; s=$(date +%s); "$@" > "$L.$n" 2>&1; rc=$?; echo "$n rc $rc $(( $(date +%s)-s )) s | $(tail -1 "$L.$n" | cut -c1-200)" >> $L; }
run ruff $PY -m ruff check .
run arms $PY -B conform/arms.py
run arm_modules $PY -B tests/test_arm_modules.py
run mustfail $PY -B tests/test_carry_w.py check_mustfail_mixes
run off_identity $PY -B tests/test_carry_w.py check_off_identity
echo END >> $L
