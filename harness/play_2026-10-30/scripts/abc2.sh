#!/bin/bash
PY=/c/Users/Admin/Documents/GitHub/tether/.venv/Scripts/python.exe
RUN=C:/TETHER_RUNS/S6_2026-10-19/E4B_SPY/e4b_run.py
X=/c/TETHER_RUNS/S6_2026-10-19/split/six_umwelt
U=$(date -u +%Y%m%dT%H%M%SZ)
export PYTHONDONTWRITEBYTECODE=1
one() {  # label tree
  local lab=$1
  local tree=$2
  local dry=C:/TETHER_RUNS/S6_2026-10-19/E4B/dry_abc_${lab}_$U
  local out=C:/TETHER_RUNS/S6_2026-10-19/PLAY12/abc_${lab}_$U
  mkdir "$dry" || { echo "$lab STOP dry exists"; return; }
  local s=$(date +%s)
  timeout 300 $PY -B $RUN "$tree" "$dry" "$out" 120 60 00000006 60 60 1 > "$out.launch.txt" 2>&1; local rc=$?
  local row=$(awk -F'\t' '$1 ~ /^[0-9]+$/' "$out/switch.tsv" 2>/dev/null)
  local mint=$(grep -c '"step": "MINT"' "$out/stream.jsonl" 2>/dev/null)
  local route=$(grep -c '"step": "ROUTE"' "$out/stream.jsonl" 2>/dev/null)
  local reach=$(grep -c '"event": "reach"' "$out/stream.jsonl" 2>/dev/null)
  local faults=$(grep -cE '"event": ?"agent_fault"' "$out/stream.jsonl" 2>/dev/null)
  local peak=$(grep -o '"peak_job_commit_gib": [0-9.]*' "$out"/sup/*.json 2>/dev/null | head -1 | awk '{print $2}')
  echo "$lab tree=$(git -C "$tree" rev-parse --short HEAD) rc=$rc wall=$(( $(date +%s) - s ))s game=$(echo "$row" | cut -f2) steps=$(echo "$row" | cut -f6) first_act_s=$(echo "$row" | cut -f15) levels=$(echo "$row" | cut -f7) ending=$(echo "$row" | cut -f8) MINT=$mint ROUTE=$route reach=$reach faults=$faults peak_gib=$peak dry=$dry"
}
one C "$X"
git -C $X checkout -q --detach 68db0d7 && one A "$X"
git -C $X checkout -q --detach 29b85fe17ceb86c11fdc6101212e80b84ec03715
echo "six_umwelt back at $(git -C $X rev-parse --short HEAD); status $(git -C $X status --porcelain --untracked-files=no | wc -l)"
