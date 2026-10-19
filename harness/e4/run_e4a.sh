export PYTHONDONTWRITEBYTECODE=1
for v in $(env | grep ^TETHER_ | cut -d= -f1); do unset $v; done
until grep -q "^# E4 end" C:/TETHER_RUNS/E4_2026-10-18/results.tsv; do sleep 15; done
powershell -NoProfile -Command "Get-Process python* -ErrorAction SilentlyContinue | Select-Object Id,@{n='MB';e={[math]::Round(\.PrivateMemorySize64/1MB)}},StartTime | Format-Table -AutoSize | Out-String" > C:/TETHER_RUNS/E4_2026-10-18/pre_e4a_processes.txt
powershell -NoProfile -Command "'free disk C GiB: ' + [math]::Round((Get-PSDrive C).Free/1GB,1)" >> C:/TETHER_RUNS/E4_2026-10-18/pre_e4a_processes.txt
cd C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad/e4
C:/Users/Admin/Documents/GitHub/tether/.venv/Scripts/python.exe -B C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad/e4/e4_driver.py C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad/wt_fix C:/TETHER_RUNS/E4_2026-10-18 --part games > C:/TETHER_RUNS/E4_2026-10-18/driver_e4a.out 2>&1
