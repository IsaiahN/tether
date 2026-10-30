#!/bin/bash
# wip/act: the dry box smoke at 6d0ed2b, then the cn04 speed line 0b027bad vs 6d0ed2b (the reviewer
# 2026-10-26 11:52 item 5, 12:12). One at a time, each on its own new empty dry lineage.
PY=/c/Users/Admin/Documents/GitHub/tether/.venv/Scripts/python.exe
RUN=C:/TETHER_RUNS/S6_2026-10-19/E4B_SPY/e4b_run.py
X=/c/TETHER_RUNS/S6_2026-10-19/split/six_umwelt
O=C:/TETHER_RUNS/S6_2026-10-19/ACT
NEW=6d0ed2b84ceae5df2797cc0b0a70c96d0450125a
OLD=0b027bad
U=$(date -u +%Y%m%dT%H%M%SZ)
export PYTHONDONTWRITEBYTECODE=1
for v in $(env | grep -o '^TETHER_[A-Z_0-9]*'); do unset $v; done
mkdir -p "$O"
one() {  # label sha max_s margin seed slice_min slice_max
  local lab=$1
  local sha=$2
  git -C $X fetch -q /c/TETHER_RUNS/S6_2026-10-19/split/general-agent "$sha" 2>/dev/null
  git -C $X checkout -q --detach "$sha" || { echo "$lab STOP checkout $sha"; return; }
  local dry=C:/TETHER_RUNS/S6_2026-10-19/E4B/dry_act_${lab}_$U
  local out=$O/${lab}_$U
  mkdir "$dry" || { echo "$lab STOP dry exists"; return; }
  local s=$(date +%s)
  timeout $(( $3 + 120 )) $PY -B $RUN "$X" "$dry" "$out" $3 $4 $5 $6 $7 1 > "$out.launch.txt" 2>&1; local rc=$?
  local row=$(awk -F'\t' '$1 ~ /^[0-9]+$/' "$out/switch.tsv" 2>/dev/null)
  local st=$out/stream.jsonl
  n() { grep -c "$1" "$st" 2>/dev/null; }
  local peak=$(grep -o '"peak_job_commit_gib": [0-9.]*' "$out"/sup/*.json 2>/dev/null | head -1 | awk '{print $2}')
  echo "$lab tree=$(git -C $X rev-parse --short HEAD) rc=$rc wall=$(( $(date +%s) - s ))s game=$(echo "$row" | cut -f2) steps=$(echo "$row" | cut -f6) first_act_s=$(echo "$row" | cut -f15) levels=$(echo "$row" | cut -f7) ending=$(echo "$row" | cut -f8) lookup_deferred=$(n '"event": "lookup_deferred"') walk_cut=$(n '"event": "walk_cut"') step_act=$(n '"event": "step_act"') MINT=$(n '"step": "MINT"') ROUTE=$(n '"step": "ROUTE"') faults=$(grep -cE '"event": ?"agent_fault"' "$st" 2>/dev/null) peak_gib=$peak out=$out"
}
case "$1" in
  smoke) one smoke $NEW 300 60 9a2ede8f 120 180 ;;
  speed) one cn04_old $OLD 120 60 00000006 60 60; one cn04_new $NEW 120 60 00000006 60 60 ;;
esac
git -C $X checkout -q --detach $NEW
echo "six_umwelt at $(git -C $X rev-parse --short HEAD); status $(git -C $X status --porcelain --untracked-files=no | wc -l)"
