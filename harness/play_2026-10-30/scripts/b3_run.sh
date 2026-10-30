#!/bin/bash
# r426 B3: b2_probe.py on a3ad3ef, one cold agent: sp80 (5 steps), 20 other games (4 steps each), sp80 again (5 steps,
# about cycle 85); the trace / window / bound / retargets logged at every boundary.
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TETHER_AGENT_SEED=0 OPERATION_MODE=offline
S=C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad
O=$S/b3_r426
[ ! -e $O ] || { echo "b3_r426 exists"; exit 2; }
mkdir -p $O
B=C:/Users/Admin/Documents/GitHub/tether-wt-mergeARC
[ "$(git -C $B rev-parse --short HEAD)" = a3ad3ef ] || { echo head > $O/run.log; exit 2; }
ORDER=sp80:5,sb26,su15,tn36,lf52,r11l,re86,ft09,vc33,m0r0,wa30,dc22,s5i5,cd82,ar25,lp85,sc25,ka59,cn04,ls20,g50t,sp80:5
echo "START $(date +%H:%M:%S) $ORDER" > $O/run.log
( cd $B && "$B/.venv/Scripts/python.exe" -B $S/b2_probe.py $B $O/a3ad3ef 4 $ORDER > $O/a3ad3ef.out 2>&1; echo "a3ad3ef rc $? $(date +%H:%M:%S)" >> $O/run.log )
echo "END $(date +%H:%M:%S)" >> $O/run.log
