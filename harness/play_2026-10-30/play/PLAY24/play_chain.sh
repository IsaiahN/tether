#!/bin/bash
# PLAY24 = PLAY23 on the tree arc-solver-agent 26a68e0 (arms 9 + 10 (same trees as PLAY23); the spy fixed 0df3871e; spy_sweep in the precheck (the reviewer r440, r441)). PLAY23 = PLAY22 on the tree arc-solver-agent 26a68e0 (arms 9 CONTINGENT_ONE_PASS and 10 ARRIVAL_ALIAS (wip/finish3, wip/arrival-alias); the reviewer r429-r438). PLAY22 = PLAY21 on the tree arc-solver-agent a3ad3ef (wip/finish2's arms 7 VIEW_HOLD_SAME and 8 VIEW_HOLD_SAME_ROLE; the reviewer r414-r423). PLAY21 = PLAY20 on the NEW tree arc-solver-agent 9d23841 (wip/finish's five arms; the reviewer r392-r399). PLAY20 = PLAY19 on the NEW tree: arc-solver-agent 7b9a90f (general-agent 9133034, decisions 1b-1e and 4:
# TETHER_ASK, TETHER_OWED_REJUDGE, TETHER_S1_REPRICE, TETHER_STOP_RULES, TETHER_NAMED_REMAINDER, TETHER_PLAN_NARROW;
# TETHER_DIVIDE_CREDIT default OFF; + README), a fresh clone split/fresh_r26 with M3 (the reviewer r376, r377), the
# E4B_SPY box with NO arm pins (the CREDIT pin dropped: the credit_on copy restored); from PLAY19 round 8's verified write.
# Open-ended; the STOP file is the exit.
# PLAY19 = PLAY18 on the NEW tree: arc-solver-agent 8412f6f (general-agent dad9d2b, decision
# 1a: TETHER_DIVIDE, TETHER_DIVIDE_CREDIT, + README), a fresh clone split/fresh_r25 with M3
# (the reviewer r319), the same E4B_SPY box; from 2ce4b329 (PLAY18 r3's kept generation).
# Open-ended; the STOP file is the exit.
# PLAY18 = PLAY17 on the NEW tree: arc-solver-agent 45234ba (general-agent 549f403, decisions
# 2+3: TETHER_INSTANCE_RETIRE, TETHER_KIND_SAVE, TETHER_SETTLE_PRED, + README), a fresh clone
# split/fresh_r24 with M3 (the reviewer r305), the same E4B_SPY box; from f6e42d42 (PLAY17 r3's kept generation).
# Open-ended; the STOP file is the exit.
# PLAY17 = PLAY16 on the NEW tree: arc-solver-agent 5153347 (general-agent 6c04c56, decision 5
# TETHER_ARRIVAL_GAP + the step_derived TIMINGS fix, + README), a fresh clone split/fresh_r23 with M3 (the reviewer
# r286, r287), with the same E4B_SPY box; from fa086387 (PLAY16 r44's kept generation). Open-ended; the STOP file is the exit.
# PLAY16 = PLAY15 on the NEW tree: arc-solver-agent f5453c3 (general-agent d12c74e, the step clock
# TETHER_STEP_CLOCK + B2 TETHER_STEP_DERIVED, + README), a fresh clone split/fresh_r22 with M3 (the reviewer r265, r273),
# with the same E4B_SPY box; from 5526aed5 (PLAY15 r3's kept generation). Open-ended; the STOP file is the exit.
# PLAY15 = PLAY14 on the NEW tree: arc-solver-agent ba01d98 (general-agent d7fd81d, B1 whole mints per step:
# TETHER_STEP_MINT, + README), a fresh clone split/fresh_r20 with M3 (the reviewer 2026-10-26 r252), with the same
# E4B_SPY box; from 2c535e6f (PLAY14 r1's kept generation). Open-ended; the STOP file is the exit.
# PLAY14 = PLAY13 on the NEW tree: arc-solver-agent 9f77f70 (general-agent ae028d6, think-or-act at the step: A1
# TETHER_STEP_ACT, A2 TETHER_WALK_BUDGET, + README), a fresh clone split/fresh_r19 (the reviewer 2026-10-26 13:01 CDT), with
# the same E4B_SPY box; from ce482278 (PLAY13 r1's kept generation). Open-ended; the STOP file is the exit.
# PLAY13 = PLAY12 on the NEW tree: arc-solver-agent 8dae023 (general-agent 0b027ba, the limbs, + README), a fresh clone
# split/fresh_r18 (the reviewer 2026-10-26 10:33 CDT), with the same E4B_SPY box; from 467ff7e8 (PLAY12 r1 restored). THE
# chain.log FIX, BOTH (the reviewer 10:20): a fresh chain.log per launch (refused if one exists), the seed lookup takes
# the last match, and exactly one SEED line per round is asserted before round 1.
# PLAY12 = PLAY11 on the NEW tree: arc-solver-agent 2e77f16 (general-agent 8314ed6, the Umwelt build, + README), a fresh clone
# split/fresh_r17 (the reviewer 2026-10-26 07:51 CDT), with the same E4B_SPY box; from PLAY11 round 9's head_out 467ff7e8. The fault
# count reads agent_fault EVENT rows (the reviewer 05:50).
# PLAY11 = PLAY10 on the NEW tree: arc-solver-agent ebcb1b1 (general-agent 30be254 + README), a fresh clone split/fresh_r16 -- (ii), the carried kind entry as a
# TEST (TETHER_KIND_TEST; the reviewer 2026-10-25 19:02 item 8 approved, 19:17 named) -- with the same E4B_SPY box. From round 10's head_out.
# PLAY10 = PLAY9 on the NEW tree: arc-solver-agent 64e8e6b (general-agent 0330b7d + README), a fresh clone split/fresh_r15 -- D2's newborn fix
# (the reviewer 2026-10-25 16:48, 16:52) -- with the same E4B_SPY box (the reviewer 17:26 (2): the spy stays in). From round 9's head_out.
# PLAY8 = PLAY7 on the tree arc-solver-agent de78104 (general-agent 19c861a + README): D2 THE OWN CLOCK (TETHER_OWN_CLOCK_SUBJECT) and P3 THE MEMO
# CLEAR AT THE AGENT'S OWN BREAK (TETHER_MEMO_AT_BREAK) for the first time (the reviewer 2026-10-25 12:48, 13:11, 13:22, 13:28, 13:36, 13:53).
# PLAY5 = PLAY4 on the tree arc-solver-agent 2337226 (general-agent b17cb2d + README): the kind-carry K1-K3 (TETHER_KIND_CARRY, TETHER_KIND_EFFECTS) and ROUTE FIRST (TETHER_HYP_ROUTE_FIRST, P1) for the first time
# (the reviewer 2026-10-25 10:17 P0, final plan 10:29; Isaiah 10:16 "proceed with building"). Everything else as PLAY4, whose header follows.
# PLAY4 = PLAY3 on the tree arc-solver-agent eaaf712 (general-agent a0a4b5a + README): the cap (i), (ii), the relational-slots cache, the game-name constant and the slot set
# for the first time (the reviewer 05:42, 05:54). PLAY2 (Isaiah 2026-10-25 05:26 / 05:31 via the reviewer 05:28 / 05:31): the same chain, OPEN-ENDED -- no end date
# (deadline 2026-12-31, rounds up to 999), the 2 h per-round cap kept, a clean stop by a STOP file in PLAY2 checked
# between rounds. Tree, lineage, box and readers unchanged from the overnight run.
# THE OVERNIGHT PLAY RUN (Isaiah 2026-10-23 20:54 "learning by the morning"; the reviewer 20:55, 21:42 draft accepted in
# principle 21:43 with 5 additions). ROUNDS, each ONE E4b stream (all 25 public games, one life, never told the game
# changed), on the REAL lineage in place, from the committed arc-solver-agent a04eb7b5 (fresh_r4 clone). The E4b box and
# readers are reused unchanged. Every round's seed is fixed and logged BEFORE round 1 (sha256 of round|chain-start UTC);
# the chain then waits 180 s so the seeds can be posted. A round starts only if it can finish before the deadline:
# time left >= ROUND_NEED (1.25 x the longest round so far, at least 1.25 x E4b's 4593 s) + RESERVE; else the chain ends
# cleanly ("no partial round"). Each round: pf_check before (names), e4b_run (max_s = time left - RESERVE), pf_check after
# from the previous verified head (rc 3 STOPS), e4b_read, break_audit, log_index add + verify of the round's ledgers,
# then play_across.py over every round so far (per game per round with its position; load wall and dedup per round).
# Stop triggers: a non-zero run rc, a failed write check, an agent_fault row, free disk < 10 GB. Nothing is restored,
# nothing deleted, nothing killed. argv: none. Only through a launch copy.
P="C:/TETHER_RUNS/S6_2026-10-19/PLAY24"
E="C:/TETHER_RUNS/S6_2026-10-19/E4B_SPY"
T="C:/TETHER_RUNS/S6_2026-10-19/split/fresh_r30/arc-solver-agent"
G=eadee1aa0c5c6f7e24381099d8573f28be254e04
H=26a68e0e23bef27a622ccfa5f86bb01d83f04126
LIN="C:/TETHER_RUNS/E4_2026-10-18/lineage"
PY="C:/Users/Admin/Documents/GitHub/tether/.venv/Scripts/python.exe"
CHK="C:/TETHER_RUNS/S6_2026-10-19/PF/pf_check.py"
DEADLINE_LOCAL="2026-12-31 00:00:00"
RESERVE=600
E4B_WALL=4593
MAX_ROUNDS=999
FIRST_ROUND=1
L="$P/chain.log"
export PYTHONDONTWRITEBYTECODE=1
case "$0" in *.launched.*) ;; *) echo "STOP run this chain only through a launch copy"; exit 2;; esac
[ ! -s "$L" ] || { echo "STOP $L exists: a fresh chain.log per launch (the reviewer 2026-10-26 10:20)"; exit 2; }
WANT="$(cat "$P/play_chain.want")"
got="$(sha256sum "$E/e4b_box.py" "$E/e4b_run.py" "$E/e4b_read.py" "$E/break_audit.py" "$CHK" "$T/harness/mem_store/e4_stream.py" "$T/tether.py" "$T/harness/log_index.py" "$P/play_across.py" "$T/arc_percept.py" "$T/arc_world.py" "$T/conform/arms.py" "$T/gamma.py" "$T/lineage.py" "$T/arc_atoms.py" | cut -c1-16 | tr '\n' ' ' | sed 's/ $//')"
[ "$got" = "$WANT" ] || { echo "STOP a chain file changed: $got" >> "$L"; exit 2; }
SPY=0df3871e1b49935b   # kind_spy.py, which the box imports and the want does not list
[ "$(sha256sum "$E/kind_spy.py" | cut -c1-16)" = "$SPY" ] || { echo "STOP kind_spy.py changed" >> "$L"; exit 2; }
[ "$(git -C "$T" rev-parse --abbrev-ref HEAD)" = "arc-solver-agent" ] || { echo "STOP branch" >> "$L"; exit 2; }
[ "$(git -C "$T" rev-parse HEAD)" = "$H" ] || { echo "STOP head" >> "$L"; exit 2; }
[ "$(git -C "$T" diff --name-only "$G" HEAD)" = "README.md" ] || { echo "STOP diff vs general-agent" >> "$L"; exit 2; }
[ -z "$(git -C "$T" --no-optional-locks status --porcelain --untracked-files=no)" ] || { echo "STOP tree not clean" >> "$L"; exit 2; }
[ -e "$T/.venv/Scripts/python.exe" ] && [ "$(ls "$T/environment_files" | wc -l)" = "25" ] || { echo "STOP junctions" >> "$L"; exit 2; }
[ ! -e "$T/lineage" ] || { echo "STOP the clone holds a lineage folder" >> "$L"; exit 2; }
[ -s "$P/head.txt" ] || { echo "STOP no PLAY/head.txt (the replay's verified head)" >> "$L"; exit 2; }
DL=$(date -d "$DEADLINE_LOCAL" +%s)
U0=$(date -u +%Y%m%dT%H%M%SZ)
echo "$(date '+%Y-%m-%d %H:%M:%S %Z') PLAY_START files $got; arc_world.py $(sha256sum "$T/arc_world.py" | cut -c1-16) interface.py $(sha256sum "$T/interface.py" | cut -c1-16) (pinned by the head check, printed for the reader: the reviewer 2026-10-25 12:02); kind_spy.py $(sha256sum "$E/kind_spy.py" | cut -c1-16) (pin $SPY); tree $T at $H; head $(cat "$P/head.txt"); deadline $DEADLINE_LOCAL" >> "$L"
for r in $(seq 1 $MAX_ROUNDS); do
  echo "SEED round $r $(printf '%s|%s' "$r" "$U0" | sha256sum | cut -c1-8)" >> "$L"
done
[ -z "$(grep '^SEED round ' "$L" | awk '{print $3}' | sort | uniq -d)" ] || { echo "STOP a round holds more than one SEED line" >> "$L"; exit 2; }
echo "$(date +%H:%M:%S) seeds fixed; one SEED line per round; waiting 180 s before round $FIRST_ROUND" >> "$L"
sleep 180
longest=$E4B_WALL
for r in $(seq $FIRST_ROUND $MAX_ROUNDS); do
  R=$(printf '%02d' "$r"); O="$P/round_$R"
  [ ! -e "$P/STOP" ] || { echo "$(date +%H:%M:%S) CLEAN STOP before round $r (STOP file)" >> "$L"; break; }
  seed=$(grep "^SEED round $r " "$L" | awk '{print $4}' | tail -1)
  now=$(date +%s); left=$(( DL - now )); need=$(( longest * 5 / 4 + RESERVE ))
  free=$(df -B1 C:/ | tail -1 | awk '{print $4}')
  if [ "$left" -lt "$need" ]; then echo "$(date +%H:%M:%S) END: round $r cannot fit (left $left s < need $need s); no partial round" >> "$L"; break; fi
  if [ "$free" -lt 10737418240 ]; then echo "$(date +%H:%M:%S) STOP free disk $free under 10 GB before round $r" >> "$L"; break; fi
  [ ! -e "$O" ] || { echo "STOP $O exists" >> "$L"; break; }
  head_in=$(cat "$P/head.txt")
  mkdir -p "$O"
  echo "$(date +%H:%M:%S) ROUND $r START seed $seed head_in $head_in left $left need $need free $free names $(ls "$LIN" | wc -l) lineage_bytes $(du -sb "$LIN" | cut -f1) store_bytes $(stat -c %s "$LIN/memory.db")" >> "$L"
  "$PY" -B "$CHK" before "$LIN" "$O" >> "$L" 2>&1 || { echo "STOP names snapshot round $r" >> "$L"; break; }
  maxs=$(( left - RESERVE )); [ "$maxs" -gt 7200 ] && maxs=7200
  t0=$(date +%s)
  "$PY" -B "$E/e4b_run.py" "$T" "$LIN" "$O" "$maxs" 300 "$seed" 120 300 25; rc=$?
  wall=$(( $(date +%s) - t0 )); [ "$wall" -gt "$longest" ] && longest=$wall
  echo "$(date +%H:%M:%S) ROUND $r RUN rc $rc wall $wall s max_s $maxs" >> "$L"
  "$PY" -B "$CHK" after "$LIN" "$O" stream "$head_in" >> "$L" 2>&1; wrc=$?
  echo "$(date +%H:%M:%S) ROUND $r WRITE_CHECK rc $wrc head_out $(cat "$P/head.txt") names $(ls "$LIN" | wc -l) lineage_bytes $(du -sb "$LIN" | cut -f1) store_bytes $(stat -c %s "$LIN/memory.db") free $(df -B1 C:/ | tail -1 | awk '{print $4}')" >> "$L"
  "$PY" -B "$E/e4b_read.py" "$O" > "$O/read.out" 2>&1; rrc=$?; echo "$(date +%H:%M:%S) ROUND $r READ rc $rrc" >> "$L"
  "$PY" -B "$E/break_audit.py" "$O" > "$O/break_audit.out" 2>&1; brc=$?; echo "$(date +%H:%M:%S) ROUND $r BREAK_AUDIT rc $brc" >> "$L"
  "$PY" -B "$T/harness/log_index.py" add "$O" > "$O/log_index_add.out" 2>&1; ia=$?
  "$PY" -B "$T/harness/log_index.py" verify "$O/stream.jsonl" > "$O/log_index_verify.out" 2>&1; iv=$?
  echo "$(date +%H:%M:%S) ROUND $r LOG_INDEX add rc $ia verify rc $iv (index only; no retire)" >> "$L"
  # EVENT rows only (the event field), never rows that name the ending (the reviewer 2026-10-26 05:50)
  faults=$(grep -cE '"event": ?"agent_fault"' "$O/stream.jsonl" 2>/dev/null)
  "$PY" -B "$P/play_across.py" "$P" > "$P/across.out" 2>&1; xrc=$?; echo "$(date +%H:%M:%S) ROUND $r ACROSS rc $xrc (PLAY/across.out, all rounds so far)" >> "$L"
  echo "$(date +%H:%M:%S) ROUND $r END agent_fault events ${faults:-0}" >> "$L"
  [ "$rc" = "0" ] || { echo "STOP round $r run rc $rc" >> "$L"; break; }
  [ "$wrc" = "0" ] || { echo "STOP round $r write check rc $wrc" >> "$L"; break; }
  [ "${faults:-0}" = "0" ] || { echo "STOP round $r agent_fault events $faults" >> "$L"; break; }
done
echo "$(date '+%Y-%m-%d %H:%M:%S %Z') PLAY_END" >> "$L"
