# The reviewer 23:02 item 3: when the driver's hung flag fires (it writes <game>/pyspy.txt with the first dump),
# take a SECOND py-spy dump of the same pids about 60 s later into <game>/pyspy2.txt, with the ledger bytes and
# commit MB at both moments. Read only on the game (py-spy dump attaches briefly, as the driver's own dump does).
# Bash, not python, so it adds no python process. Stops when E4a's header line count stops growing for 3 h.
R=C:/TETHER_RUNS/E4_2026-10-18
PYSPY="C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/2043231f-437e-4548-ac19-702f1efcfb71/scratchpad/spyenv/Scripts/py-spy.exe"
for i in $(seq 1 540); do
  for d in $R/public/*/; do
    d=${d%/}
    g=$(basename $d | cut -d_ -f2)
    if [ -f $d/pyspy.txt ] && [ ! -f $d/pyspy2.txt ]; then
      b1=$(stat -c %s $d/$g.jsonl 2>/dev/null); c1=$(tail -1 $d/$g.commit.tsv | cut -f2); t1=$(date +%H:%M:%S)
      sleep 60
      b2=$(stat -c %s $d/$g.jsonl 2>/dev/null); c2=$(tail -1 $d/$g.commit.tsv | cut -f2); t2=$(date +%H:%M:%S)
      {
        echo "second dump (the reviewer 23:02): first-check $t1 ledger_bytes $b1 commit_MB $c1 | second $t2 ledger_bytes $b2 commit_MB $c2"
        for q in $(grep -o "^--- py-spy dump --pid [0-9]*" $d/pyspy.txt | grep -o "[0-9]*$"); do
          echo "--- py-spy dump --pid $q"
          "$PYSPY" dump --pid $q 2>&1
        done
      } > $d/pyspy2.txt
    fi
  done
  sleep 20
done
