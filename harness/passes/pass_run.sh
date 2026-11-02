#!/bin/bash
# ONE PASS (r731, r769, r771): one serial e4_stream life over all 25 games, SLICE s per game, on the CENTRAL library (it
# loads the last pass's head and writes the next), from a tree pinned at the cut commit. Then pf_check's write check,
# the read, the faults. Machine paths come from the caller, never from this file:
#   PASS_DIR      the passes folder (head.txt, passes.log, pass_NN/)
#   PASS_LINEAGE  the central library folder (e4b_run.py refuses any other)
#   PASS_PY       the python that runs the harness
# argv: pass_no tree slice_s seed
export PYTHONDONTWRITEBYTECODE=1
for v in $(env | grep -o '^TETHER_[A-Z0-9_]*'); do unset $v; done
unset OPERATION_MODE ARC_BASE_URL ARC_API_KEY
: "${PASS_DIR:?}" "${PASS_LINEAGE:?}" "${PASS_PY:?}"
N=$1; T=$2; SLICE=$3; SEED=$4
H=$(cd "$(dirname "$0")" && pwd)
PS=$PASS_DIR; O=$PS/pass_$(printf %02d "$N"); L=$PS/passes.log; LIN=$PASS_LINEAGE; PY=$PASS_PY
MAXS=1800; MARGIN=300   # r731: 30 min for the whole run; the margin pass 3 used (its end path 168.7 s)
[ ! -e "$O" ] || { echo "$(date +%T) STOP pass $N: $O exists" >> "$L"; exit 2; }
side=$(ls "$LIN" | grep -E 'memory\.db-(shm|wal|journal)' | tr '\n' ' ')
[ -z "$side" ] || { echo "$(date +%T) STOP pass $N: side files $side" >> "$L"; exit 2; }
head_in=$(cat "$PS/head.txt")
mkdir -p "$O"
echo "$(date +%T) PASS $N START tree $(git -C "$T" rev-parse --short HEAD) head_in $head_in slice $SLICE seed $SEED max_s $MAXS margin $MARGIN names $(ls "$LIN" | wc -l)" >> "$L"
"$PY" -B "$H/pf_check.py" before "$LIN" "$O" >> "$L" 2>&1 || { echo "$(date +%T) STOP pass $N names snapshot" >> "$L"; exit 2; }
t0=$(date +%s)
"$PY" -B "$H/e4b_run.py" "$T" "$LIN" "$O" "$MAXS" "$MARGIN" "$SEED" "$SLICE" "$SLICE" 25; rc=$?
echo "$(date +%T) PASS $N RUN rc $rc wall $(( $(date +%s) - t0 )) s" >> "$L"
"$PY" -B "$H/pf_check.py" after "$LIN" "$O" stream "$head_in" >> "$L" 2>&1; wrc=$?
echo "$(date +%T) PASS $N WRITE_CHECK rc $wrc head_out $(cat "$PS/head.txt") names $(ls "$LIN" | wc -l)" >> "$L"
"$PY" -B "$H/e4b_read.py" "$O" > "$O/read.out" 2>&1; echo "$(date +%T) PASS $N READ rc $?" >> "$L"
faults=$(grep -cE '"event": ?"agent_fault"' "$O/stream.jsonl" 2>/dev/null)
side=$(ls "$LIN" | grep -E 'memory\.db-(shm|wal|journal)' | tr '\n' ' ')
echo "$(date +%T) PASS $N END faults ${faults:-0} side_files [${side}]" >> "$L"
