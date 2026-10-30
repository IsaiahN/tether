#!/bin/bash
# r429's outstanding re-run: b2_probe.py on the committed arm 9 tree (wip/finish3, main checkout, clean), one cold
# agent: sp80 (5 steps) + 10 fillers (4 steps each); at every boundary len / on-board share of _outstanding and of
# agency.tried, beside trace / window / bound / retargets.
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TETHER_AGENT_SEED=0 OPERATION_MODE=offline
S=C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad
O=$S/b4_r429
[ ! -e $O ] || { echo "b4_r429 exists"; exit 2; }
mkdir -p $O
B=C:/Users/Admin/Documents/GitHub/tether
[ "$(git -C $B rev-parse --abbrev-ref HEAD)" = wip/finish3 ] && [ -z "$(git -C $B status --porcelain --untracked-files=no | grep -v settings.json)" ] || { echo "tree" > $O/run.log; exit 2; }
ORDER=sp80:5,sb26,su15,tn36,lf52,r11l,re86,ft09,vc33,m0r0,wa30
echo "START $(date +%H:%M:%S) $(git -C $B rev-parse --short HEAD) $ORDER" > $O/run.log
( cd $B && "$B/.venv/Scripts/python.exe" -B $S/b2_probe.py $B $O/tree 4 $ORDER > $O/tree.out 2>&1; echo "rc $? $(date +%H:%M:%S)" >> $O/run.log )
echo "END $(date +%H:%M:%S)" >> $O/run.log
