export PYTHONDONTWRITEBYTECODE=1
for v in $(env | grep ^TETHER_ | cut -d= -f1); do unset $v; done
R=C:/TETHER_RUNS/E4_2026-10-18
S=C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad
START=${1:-2}
cd $S/e4
C:/Users/Admin/Documents/GitHub/tether/.venv/Scripts/python.exe -B $S/e4/e4_driver.py $S/wt_fix $R --part games --start $START > $R/driver_e4a_from$START.out 2>&1
