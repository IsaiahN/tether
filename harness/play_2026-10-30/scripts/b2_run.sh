#!/bin/bash
# r424 B2: b2_probe.py on 7b9a90f then a3ad3ef, one cold agent through sp80,cd82,ar25,lp85, 5 steps each.
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TETHER_AGENT_SEED=0 OPERATION_MODE=offline
S=C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad
O=$S/b2_r424
[ ! -e $O ] || { echo "b2_r424 exists"; exit 2; }
mkdir -p $O
A=C:/Users/Admin/Documents/GitHub/tether-wt-prof; B=C:/Users/Admin/Documents/GitHub/tether-wt-mergeARC
[ "$(git -C $A rev-parse --short HEAD)" = 7b9a90f ] && [ "$(git -C $B rev-parse --short HEAD)" = a3ad3ef ] || { echo heads > $O/run.log; exit 2; }
echo "START $(date +%H:%M:%S)" > $O/run.log
for t in 7b9a90f a3ad3ef; do
  T=$A; [ $t = a3ad3ef ] && T=$B
  ( cd $T && "$T/.venv/Scripts/python.exe" -B $S/b2_probe.py $T $O/$t 5 sp80,cd82,ar25,lp85 > $O/$t.out 2>&1; echo "$t rc $? $(date +%H:%M:%S)" >> $O/run.log )
done
echo "END $(date +%H:%M:%S)" >> $O/run.log
