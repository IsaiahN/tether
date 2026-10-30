#!/bin/bash
# The reviewer 2026-10-26 10:41 item 4: ONE cProfile run of the merged code on cn04 (seed 00000006), its own NEW empty dry
# lineage, about 60 s of play, through the box (e4b_box.py, the spy installed) run directly under cProfile.
PY=/c/Users/Admin/Documents/GitHub/tether/.venv/Scripts/python.exe
T=C:/TETHER_RUNS/S6_2026-10-19/split/fresh_r18/arc-solver-agent
U=$(date -u +%Y%m%dT%H%M%SZ)
DRY=C:/TETHER_RUNS/S6_2026-10-19/E4B/dry_prof_$U; OUT=C:/TETHER_RUNS/S6_2026-10-19/PLAY13/prof_$U
mkdir "$DRY" || exit 2
for v in $(env | grep -o '^TETHER_[A-Z_0-9]*'); do unset $v; done
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1
s=$(date +%s); dl=$(( s + 60 ))
timeout 150 $PY -B -m cProfile -o "$OUT.prof" C:/TETHER_RUNS/S6_2026-10-19/E4B_SPY/e4b_box.py "$T" "$OUT" --seed 00000006 --lineage "$DRY" --slice-min-s 60 --slice-max-s 60 --deadline-at $dl --n-games 1 > "$OUT.log" 2>&1
echo "rc $? wall $(( $(date +%s) - s ))s prof $OUT.prof"
awk -F'\t' '$1 ~ /^[0-9]+$/ {print "game", $2, "steps", $6, "first_act_s", $15, "ending", $8}' "$OUT/switch.tsv"
