#!/bin/bash
# Read-only round summary for PLAY16 (the reviewer r278: light posts). argv: round number (two digits), previous (two digits).
N=$1; PREV=$2
S=/c/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad
P=/c/Users/Admin/Documents/GitHub/tether/.venv/Scripts/python.exe
D=/c/TETHER_RUNS/S6_2026-10-19/PLAY16/round_$N
export PYTHONDONTWRITEBYTECODE=1
cd $S
$P -B r16_read.py round_$N > r16_r${N}_line.txt 2>&1 || echo "line rc $?"
$P -B clock_read.py PLAY16 round_$N > r16_r${N}_clock.txt 2>&1 || echo "clock rc $?"
$P -B pos_read.py PLAY16 round_$PREV round_$N > r16_r${N}_pos.txt 2>&1 || echo "pos rc $?"
R=$D/stream.jsonl
echo "games $(awk -F'\t' '$1 ~ /^[0-9]+$/' $D/switch.tsv | wc -l); steps $(awk -F'\t' '$1 ~ /^[0-9]+$/ {s+=$6} END {print s}' $D/switch.tsv)"
for e in settle mint reuse_install frame_break level_up; do printf "%s %s | " $e $(grep -c "\"event\": \"$e\"" $R); done; echo
echo "faults+caps $(grep -c '"agent_fault"\|"cap_unminted"' $R)"
grep TOTALS r16_r${N}_line.txt
grep Spearman r16_r${N}_pos.txt | tail -1; grep paired r16_r${N}_pos.txt | head -1
echo "slowest: $(awk -F'\t' '$1 ~ /^[0-9]+$/ {print $1"-"$2, $15}' $D/switch.tsv | sort -k2 -n -r | head -5 | tr '\n' '|')"
echo "missed switches (pos game first):"; grep -B1 "frame_break NO" r16_r${N}_clock.txt | grep -o "^ *[0-9]* [a-z0-9]* [0-9.]*"
grep -A1 "frame_break NO" r16_r${N}_clock.txt | grep "switch:" | sed 's/.*matches call[^)]*)//' | cut -c1-220
echo "max owed at game end: $(grep 'owed at game end' r16_r${N}_clock.txt | sed 's/.*owed at game end \([0-9]*\).*/\1/' | sort -n | tail -1)"
grep "B2:" r16_r${N}_clock.txt | awk '{r+=$3; d+=$5; o+=$7} END {print "B2 run",r,"deferred",d,"dropped",o}'
grep "derived mints exhausting" r16_r${N}_clock.txt | sed 's/.*exhausting \([0-9]*\)\/\([0-9]*\).*/\1 \2/' | awk '{e+=$1; m+=$2} END {print "derived exhausting", e, "of", m}'
grep "step1_MINT\|step1_PLAN\|step1_PERCEIVE\|step1_other\|step1_total" r16_r${N}_clock.txt
c=$(awk -F'\t' '$2=="bp35" {print $4}' $D/switch.tsv)
[ -n "$c" ] && grep "\"cycle\": $c," $R | grep '"event": "goal_hypotheses"' | $P -B -c "
import json,sys
ln=sys.stdin.readline()
if ln:
    d=json.loads(ln)['detail']; print('bp35 c$c hyp', {k:d.get(k) for k in ('wall_s','open','checked')})"
grep "^ *[0-9]* bp35 " r16_r${N}_clock.txt | sed 's/ | {/\n   {/' | head -2 | cut -c1-200
