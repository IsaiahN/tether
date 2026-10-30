#!/bin/bash
# r423 B: the r396 probe, unchanged, cold agent, lp85 and ft09, 5 steps each, at 7b9a90f (tether-wt-prof, before
# the six arms) and at a3ad3ef (tether-wt-mergeARC, code = e7a1c8e); interleaved one at a time so both trees run
# under the same contention beside PLAY22. Out: prof_r423/<tree>/<game>.*
export PYTHONDONTWRITEBYTECODE=1 TETHER_AGENT_SEED=0 OPERATION_MODE=offline
S=C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad
O=$S/prof_r423
[ ! -e $O ] || { echo "prof_r423 exists"; exit 2; }
mkdir -p $O/7b9a90f $O/a3ad3ef
A=C:/Users/Admin/Documents/GitHub/tether-wt-prof; B=C:/Users/Admin/Documents/GitHub/tether-wt-mergeARC
[ "$(git -C $A rev-parse --short HEAD)" = 7b9a90f ] && [ "$(git -C $B rev-parse --short HEAD)" = a3ad3ef ] || { echo heads > $O/run.log; exit 2; }
echo "START $(date +%H:%M:%S)" > $O/run.log
for g in lp85 ft09; do
  for t in 7b9a90f a3ad3ef; do
    T=$A; [ $t = a3ad3ef ] && T=$B
    ( cd $T && "$T/.venv/Scripts/python.exe" -B $S/prof_probe_r396.py $T $g 5 540 $O/$t > $O/$t/$g.out 2>&1; echo "$t $g rc $? $(date +%H:%M:%S)" >> $O/run.log )
  done
done
echo "END $(date +%H:%M:%S)" >> $O/run.log
