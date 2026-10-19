export PYTHONDONTWRITEBYTECODE=1
for v in $(env | grep ^TETHER_ | cut -d= -f1); do unset $v; done
PY=C:/Users/Admin/Documents/GitHub/tether/.venv/Scripts/python.exe
O=C:/TETHER_RUNS/E4_2026-10-18/stream_mftest; mkdir -p $O
cd C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad/wt_stream
for mode in mf plain; do
  flag=""; [ $mode = mf ] && flag="--mf"
  $PY -B harness/supervise.py --out $O/$mode/sup --watch-pid 5168 --max-s 1500 -- $PY -B C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad/e4/e4_stream.py C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad/wt_stream $O/$mode --seed mftest01 --slice-s 60 --n-games 2 $flag > /dev/null 2>&1
  echo "$mode sup $(grep -o '"rc": [^,]*, "ending": "[A-Z_]*"' $O/$mode/sup/sup.json)" >> $O/summary.txt
done
$PY -B C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad/e4/e4_stream_check.py $O/mf --expect-fail >> $O/summary.txt 2>&1; echo "mf check rc=$?" >> $O/summary.txt
$PY -B C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad/e4/e4_stream_check.py $O/plain >> $O/summary.txt 2>&1; echo "plain check rc=$?" >> $O/summary.txt
echo END >> $O/summary.txt
