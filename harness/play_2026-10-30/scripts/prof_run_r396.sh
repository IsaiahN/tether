#!/bin/bash
export PYTHONDONTWRITEBYTECODE=1 TETHER_AGENT_SEED=0 OPERATION_MODE=offline
T=C:/Users/Admin/Documents/GitHub/tether-wt-prof
PY=$T/.venv/Scripts/python.exe
S=C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad
O=$S/prof_r396
mkdir -p $O
echo "START $(date +%H:%M:%S)" > $O/run.log
for g in ft09 lp85 sp80; do
  ( cd $T && "$PY" -B $S/prof_probe_r396.py $T $g 5 540 $O > $O/$g.out 2>&1; echo "$g rc $? $(date +%H:%M:%S)" >> $O/run.log ) &
done
wait
echo "END $(date +%H:%M:%S)" >> $O/run.log
