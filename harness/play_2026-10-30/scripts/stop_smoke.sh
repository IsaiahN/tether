#!/bin/bash
sleep 2
cd /c/Users/Admin/Documents/GitHub/tether
S=/c/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad
export PYTHONDONTWRITEBYTECODE=1
for w in fake grid; do timeout 295 .venv/Scripts/python.exe -B $S/stop_smoke.py $w 24 > $S/stop_$w.out 2>&1; echo "$w rc $?" >> $S/stop_done.txt; done
echo done >> $S/stop_done.txt
