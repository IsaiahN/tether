#!/bin/bash
# The alias arm's smallest real occasion: b2_probe.py on tether-wt-alias (uncommitted ARRIVAL_ALIAS, ON by default),
# one cold agent, sp80 -> cd82 -> ar25, 3 steps each; then the arrival_alias rows are read.
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TETHER_AGENT_SEED=0 OPERATION_MODE=offline
S=C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad
O=$S/b5_alias
[ ! -e $O ] || { echo "b5_alias exists"; exit 2; }
mkdir -p $O
B=C:/Users/Admin/Documents/GitHub/tether-wt-alias
echo "START $(date +%H:%M:%S)" > $O/run.log
( cd $B && "$B/.venv/Scripts/python.exe" -B $S/b2_probe.py $B $O/tree 3 sp80,cd82,ar25 > $O/tree.out 2>&1; echo "rc $? $(date +%H:%M:%S)" >> $O/run.log )
echo "END $(date +%H:%M:%S)" >> $O/run.log
