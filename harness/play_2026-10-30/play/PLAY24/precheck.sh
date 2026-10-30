#!/bin/bash
# PLAY20's pre-launch checks (arc-solver-agent 7b9a90f on fresh_r26; the reviewer r376, r377): the chain's own gate lines
# read against the clone, then the per-commit checks inside the clone (ruff, test_gate, test_entry, test_gate_ledger,
# test_arm_modules, conform/arms.py, log_index verify), and tether.__file__ printed first. Read-only on the lineage (it
# never opens it). Output: PLAY20/precheck.log. argv: none.
sleep 3   # Start-Process sets BelowNormal on this bash before any child starts; children inherit it
export PATH="/usr/bin:/mingw64/bin:$PATH" PYTHONDONTWRITEBYTECODE=1
P="C:/TETHER_RUNS/S6_2026-10-19/PLAY24"
E="C:/TETHER_RUNS/S6_2026-10-19/E4B_SPY"
T="C:/TETHER_RUNS/S6_2026-10-19/split/fresh_r30/arc-solver-agent"
G=eadee1aa0c5c6f7e24381099d8573f28be254e04
H=26a68e0e23bef27a622ccfa5f86bb01d83f04126
HW=2bf2d6b61afebe42   # PLAY19 round 8's head_out, filled in after its WRITE VERIFIED
CHK="C:/TETHER_RUNS/S6_2026-10-19/PF/pf_check.py"
L="$P/precheck.log"; : > "$L"
say() { echo "$(date +%H:%M:%S) $*" >> "$L"; }
WANT="$(cat "$P/play_chain.want")"
got="$(sha256sum "$E/e4b_box.py" "$E/e4b_run.py" "$E/e4b_read.py" "$E/break_audit.py" "$CHK" "$T/harness/mem_store/e4_stream.py" "$T/tether.py" "$T/harness/log_index.py" "$P/play_across.py" "$T/arc_percept.py" "$T/arc_world.py" "$T/conform/arms.py" "$T/gamma.py" "$T/lineage.py" "$T/arc_atoms.py" | cut -c1-16 | tr '\n' ' ' | sed 's/ $//')"
[ "$got" = "$WANT" ] && say "GATE files = want" || say "GATE FAIL files $got"
[ "$(sha256sum "$E/kind_spy.py" | cut -c1-16)" = "0df3871e1b49935b" ] && say "GATE kind_spy.py 0df3871e1b49935b" || say "GATE FAIL kind_spy.py"
[ "$(git -C "$T" rev-parse --abbrev-ref HEAD)" = "arc-solver-agent" ] && say "GATE branch arc-solver-agent" || say "GATE FAIL branch"
[ "$(git -C "$T" rev-parse HEAD)" = "$H" ] && say "GATE head $H" || say "GATE FAIL head"
[ "$(git -C "$T" diff --name-only "$G" HEAD)" = "README.md" ] && say "GATE diff vs general-agent README.md only" || say "GATE FAIL diff"
[ -z "$(git -C "$T" --no-optional-locks status --porcelain --untracked-files=no)" ] && say "GATE tree clean" || say "GATE FAIL tree not clean"
[ -e "$T/.venv/Scripts/python.exe" ] && [ "$(ls "$T/environment_files" | wc -l)" = "25" ] && say "GATE junctions ok (25 environment files)" || say "GATE FAIL junctions"
[ ! -e "$T/lineage" ] && say "GATE no lineage folder in the clone" || say "GATE FAIL lineage folder"
[ ! -e "$P/chain.log" ] && say "GATE no chain.log yet (a fresh log per launch)" || say "GATE FAIL chain.log exists"
[ "$HW" != "__ROUND8_HEAD__" ] && [ "$(cat "$P/head.txt")" = "$HW" ] && say "GATE head.txt $HW (PLAY19 round 8's head_out, WRITE VERIFIED)" || say "GATE FAIL head.txt"
LIN="C:/TETHER_RUNS/E4_2026-10-18/lineage"
[ "$(ls "$LIN" | grep -c -E 'memory\.db-(shm|wal|journal)')" = "0" ] && say "GATE 0 -shm / -wal / journal files in the lineage ($(ls "$LIN" | wc -l) names) (r342 1(e))" || say "GATE FAIL SQLite side files in the lineage"
[ ! -e "$P/round_01" ] && [ "$(grep -c '^FIRST_ROUND=1$' "$P/play_chain.sh")" = "1" ] && say "GATE no round_01 yet, the chain starts at FIRST_ROUND=1" || say "GATE FAIL round dirs or FIRST_ROUND"
[ "$(grep -c "uniq -d" "$P/play_chain.sh")" = "1" ] && [ "$(grep -c "| tail -1)" "$P/play_chain.sh")" = "1" ] && say "GATE the chain asserts one SEED line per round and takes the last match" || say "GATE FAIL the SEED checks"
[ ! -e "$P/STOP" ] && say "GATE no STOP file" || say "GATE FAIL a STOP file is present"
# r376 5: the box carries NO arm pin -- the credit_on copy restored (de890479); only TETHER_AGENT_SEED is set
[ "$(sha256sum "$E/e4b_box.py" | cut -c1-16)" = "de890479b92db1ea" ] && [ "$(grep -c 'os.environ\["TETHER_' "$E/e4b_box.py")" = "1" ] && [ "$(grep -c '^os.environ\["TETHER_AGENT_SEED"\] = "0"' "$E/e4b_box.py")" = "1" ] && say "GATE the box de890479: no arm pin, only TETHER_AGENT_SEED" || say "GATE FAIL the box carries an arm pin or is not de890479"
cd "$T" || exit 3
PY="$T/.venv/Scripts/python.exe"
say "tether.__file__: $("$PY" -B -c 'import tether; print(tether.__file__)' 2>&1 | tail -1)"
run() { n=$1; shift; s=$(date +%s); "$@" > "$P/precheck_$n.out" 2>&1; rc=$?; say "$n rc $rc $(( $(date +%s)-s )) s | $(grep -v '^\s*TETHER_' "$P/precheck_$n.out" | tail -1 | cut -c1-160)"; }
run ruff "$PY" -m ruff check .
run test_gate "$PY" -B tests/test_gate.py
run test_entry "$PY" -B tests/test_entry.py
run test_gate_ledger "$PY" -B tests/test_gate_ledger.py
run test_arm_modules "$PY" -B tests/test_arm_modules.py
run arms "$PY" -B conform/arms.py
# r329: LOG_INDEX verify in the precheck -- the last indexed ledger (PLAY19 round 8) recomputed against the index
run log_index_verify "$PY" -B harness/log_index.py verify "C:/TETHER_RUNS/S6_2026-10-19/PLAY23/round_01/stream.jsonl"
run spy_sweep "$PY" -B "$P/spy_sweep.py" "$T" "$E/kind_spy.py"
say "arms summary: $(head -1 "$P/precheck_arms.out" | cut -c1-120)"
say "status after: [$(git status --porcelain | tr '\n' ' ')]"
say END
