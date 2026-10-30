#!/bin/bash
# PLAY23's want: the same 15 files the chain hashes, from E4B_SPY, PF, fresh_r29 and PLAY23
E=/c/TETHER_RUNS/S6_2026-10-19/E4B_SPY; T=/c/TETHER_RUNS/S6_2026-10-19/split/fresh_r29/arc-solver-agent
P=/c/TETHER_RUNS/S6_2026-10-19/PLAY23; CHK=/c/TETHER_RUNS/S6_2026-10-19/PF/pf_check.py
sha256sum "$E/e4b_box.py" "$E/e4b_run.py" "$E/e4b_read.py" "$E/break_audit.py" "$CHK" "$T/harness/mem_store/e4_stream.py" "$T/tether.py" "$T/harness/log_index.py" "$P/play_across.py" "$T/arc_percept.py" "$T/arc_world.py" "$T/conform/arms.py" "$T/gamma.py" "$T/lineage.py" "$T/arc_atoms.py" | cut -c1-16 | tr '\n' ' ' | sed 's/ $//' > "$P/play_chain.want"
