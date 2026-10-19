# The hung rule for census run 1 (the reviewer 2026-10-19 03:14 item 4): every 60 s, read the ledger's and census.tsv's
# sizes and the last commit row. If NEITHER file has grown for 300 s, take two py-spy dumps of the child (pid PID),
# about 60 s apart, with the sizes and commit at each, into census_run1/hung_<n>_a.txt and _b.txt. READ ONLY: it never
# kills or signals anything; the verdict is mine, posted, by the ruled rule. At most one pair per 15 min. Ends when
# sup.json exists. argv: run_dir pid
D=$1; PID=$2
PYSPY="C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/2043231f-437e-4548-ac19-702f1efcfb71/scratchpad/spyenv/Scripts/py-spy.exe"
last=""; quiet=0; n=0; cool=0
while [ ! -f $D/sup/sup.json ]; do
    now="$(stat -c %s $D/stream.jsonl 2>/dev/null) $(stat -c %s $D/census.tsv 2>/dev/null)"
    if [ "$now" = "$last" ]; then quiet=$((quiet+60)); else quiet=0; last="$now"; fi
    [ $cool -gt 0 ] && cool=$((cool-60))
    if [ $quiet -ge 300 ] && [ $cool -le 0 ]; then
        n=$((n+1))
        for s in a b; do
            f=$D/hung_${n}_$s.txt
            { date '+%Y-%m-%d %H:%M:%S'; echo "sizes $(stat -c %s $D/stream.jsonl) $(stat -c %s $D/census.tsv)"; \
              echo "mem $(tail -1 $D/sup/mem.tsv)"; timeout 60 "$PYSPY" dump --pid $PID; } > $f 2>&1
            [ $s = a ] && sleep 60
        done
        cool=900; quiet=0
    fi
    sleep 60
done
echo "census_watch ended $(date '+%H:%M:%S')"
