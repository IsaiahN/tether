export PYTHONDONTWRITEBYTECODE=1
for v in $(env | grep ^TETHER_ | cut -d= -f1); do unset $v; done
R=C:/TETHER_RUNS/E4_2026-10-18
S=C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad
powershell -NoProfile -Command 'Get-Process python* -ErrorAction SilentlyContinue | Select-Object Id,@{n="MB";e={[math]::Round($_.PrivateMemorySize64/1MB)}},StartTime | Format-Table -AutoSize | Out-String' > $R/pre_e4a_processes.txt
powershell -NoProfile -Command '"free disk C GiB: " + [math]::Round((Get-PSDrive C).Free/1GB,1)' >> $R/pre_e4a_processes.txt
cd $S/e4
C:/Users/Admin/Documents/GitHub/tether/.venv/Scripts/python.exe -B $S/e4/e4_driver.py $S/wt_fix $R --part games > $R/driver_e4a.out 2>&1
