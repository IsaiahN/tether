#!/bin/bash
# r434: ON and OFF twins of the committed alias tree (wip/arrival-alias eadee1a), one cold agent each,
# sp80 -> cd82 -> ar25, 3 steps each, in parallel at Idle; per step: contingent count, mode, Agency's integer totals.
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TETHER_AGENT_SEED=0 OPERATION_MODE=offline
S=C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad
O=$S/b6_twins
[ ! -e $O ] || { echo "b6_twins exists"; exit 2; }
mkdir -p $O
B=C:/Users/Admin/Documents/GitHub/tether-wt-alias
[ "$(git -C $B rev-parse --short HEAD)" = eadee1a ] && [ -z "$(git -C $B status --porcelain --untracked-files=no)" ] || { echo tree > $O/run.log; exit 2; }
echo "START $(date +%H:%M:%S)" > $O/run.log
( cd $B && "$B/.venv/Scripts/python.exe" -B $S/b2_probe.py $B $O/on 3 sp80,cd82,ar25 > $O/on.out 2>&1; echo "on rc $? $(date +%H:%M:%S)" >> $O/run.log ) &
( cd $B && TETHER_ARRIVAL_ALIAS=0 "$B/.venv/Scripts/python.exe" -B $S/b2_probe.py $B $O/off 3 sp80,cd82,ar25 > $O/off.out 2>&1; echo "off rc $? $(date +%H:%M:%S)" >> $O/run.log ) &
wait
echo "END $(date +%H:%M:%S)" >> $O/run.log
