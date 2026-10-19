# DEPLOY 7c77689 at a natural batch end (Isaiah 21:28 yes; the reviewer 21:29). Run ONLY when no E4a batch runs.
# Steps: fast-forward e1-reach-exact (wt_fix) --ff-only; the checks on the merged tree; the driver header patch.
# It does not relaunch: the relaunch (run_e4a4.sh wt_fix N) follows only if every check passes.
set -e
export PYTHONDONTWRITEBYTECODE=1
for v in $(env | grep ^TETHER_ | cut -d= -f1); do unset $v; done
S=C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad
PY=C:/Users/Admin/Documents/GitHub/tether/.venv/Scripts/python.exe
n=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process -Filter \"Name like 'python%'\" | Where-Object { \$_.CommandLine -like '*e4_driver.py*' } | Measure-Object).Count")
test "$n" = "0" || { echo "REFUSED: a driver is running ($n)"; exit 1; }
cd $S/wt_fix
test "$(git rev-parse --short HEAD)" = "38b2daa" || { echo "REFUSED: wt_fix not at 38b2daa"; exit 1; }
git merge --ff-only 7c77689
echo "HEAD $(git rev-parse HEAD)"
$PY -B -m ruff check . | tail -1
$PY -B test_alpha_last.py </dev/null 2>&1 | tail -4
$PY -B test_game_one_deadline.py </dev/null 2>&1 | tail -3
$PY -B test_gate.py </dev/null 2>&1 | tail -1
$PY -B $S/e4/pending_header_patch.py $S/e4/e4_driver.py
$PY -B -c "import ast,sys; ast.parse(open(sys.argv[1],encoding='utf-8').read()); print('driver parse ok')" $S/e4/e4_driver.py
echo DEPLOY-CHECKS-DONE
