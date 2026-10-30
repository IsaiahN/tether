#!/bin/bash
export PYTHONDONTWRITEBYTECODE=1
PY=C:/Users/Admin/Documents/GitHub/tether/.venv/Scripts/python.exe
W=C:/TETHER_RUNS/S6_2026-10-19/wt_ivv
M=C:/Users/Admin/Documents/GitHub/tether
S=C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad
O=$S/set_fd.txt
: > $O
cd $W
$PY -B -m ruff check tether.py conform/arms.py test_fit_dedup.py >> $O 2>&1; echo "ruff rc $?" >> $O
for t in test_gate.py test_entry.py test_k1.py conform/arms.py test_consolidate.py test_fit_units.py test_fit_tier0.py test_tiers_index.py test_tiers_draw.py; do
  t0=$(date +%s); $PY -B $t > $S/set_fd_one.txt 2>&1; rc=$?
  echo "$t rc $rc $(( $(date +%s)-t0 ))s | $(tail -1 $S/set_fd_one.txt)" >> $O
  [ $rc -ne 0 ] && cp $S/set_fd_one.txt $S/set_fd_fail_$(basename $t .py).txt
done
mkdir -p $S/fd_ident
(unset $(env | grep -o '^TETHER_[A-Z_0-9]*'); export PYTHONHASHSEED=0 TETHER_AGENT_SEED=0; $PY -B C:/TETHER_RUNS/S6_2026-10-19/S0/ident_run.py $M $S/fd_ident/ref.jsonl 15 > /dev/null 2>&1; echo "ref rc $?" >> $O
 TETHER_FIT_DEDUP=0 $PY -B C:/TETHER_RUNS/S6_2026-10-19/S0/ident_run.py $W $S/fd_ident/off.jsonl 15 > /dev/null 2>&1; echo "off rc $?" >> $O
 $PY -B C:/TETHER_RUNS/S6_2026-10-19/S0/ident_mask.py $W $S/fd_ident/ref.jsonl $S/fd_ident/off.jsonl >> $O 2>&1; echo "ident rc $?" >> $O)
echo END >> $O
