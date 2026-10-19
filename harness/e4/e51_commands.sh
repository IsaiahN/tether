# E5.1 (Isaiah 2026-10-18 14:20 "e5.1 should upload"; the reviewer 14:24, 17:05 2b; REWRITTEN for 7c77689 at the
# reviewer's 2026-10-19 02:18 item 1): commit the E4 harness (NOT agent code) on a NEW branch from 7c77689, in its
# own worktree, tag it, push to origin. The local package (C:\TETHER_RUNS\E4_2026-10-18\E51_package) goes alongside.
# WRITTEN OUT, NOT RUN. It runs only after Isaiah answers A/B/C and the reviewer rules. Post HEAD after.
set -e
export PYTHONDONTWRITEBYTECODE=1
S=C:/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad
REPO=C:/Users/Admin/Documents/GitHub/tether
W=$S/wt_e51                                   # a fresh worktree: wt_fix (E4's tree) is never moved or switched
test "$(git -C $S/wt_fix rev-parse --short=12 HEAD)" = "7c776898de2e"    # E4 games 19-25 and the probe ran on this
test ! -e $W                                                             # the worktree must not exist yet
git -C $REPO worktree add -b e51-harness $W 7c776898de2e
cd $W
test "$(git rev-parse --short=12 HEAD)" = "7c776898de2e"

# 1. the E4 harness into harness/e4/ (the runs' drivers and launchers, and the read-only readers behind every posted
#    reading), so each E4 reading is reproducible from the pushed tree. One-off edit scripts are left out (listed in
#    the post).
mkdir -p harness/e4
for f in e4_driver.py e4_practice.py e4_stream.py e4_stream_check.py manifest.py run_mf.py run_e4b.py run_probe.py \
         copy_lineage.py practice_table.py shapes.py pyspy_proof.py \
         run_e4a.sh run_e4a2.sh run_e4a3.sh run_e4a4.sh run_practice.sh run_mftest.sh deploy_7c77689.sh watch_hung.sh \
         e51_commands.sh mf_rows.py e4_stream.probe_cf5a455.py census_heap.py run_census.py census_watch.sh; do
    cp $S/e4/$f harness/e4/
done
for f in collect.py e6a.py e4b_estimate.py baseline.py transient.py edges.py extra.py package_e51.py stepstarts.py \
         loadfit.py vals.py dkshapes.py plant.py figtext.py census.py peek.py \
         census_read.py compare_rows.py census_selftest.py; do
    cp $S/e52/$f harness/e4/
done
cp $S/e4/E51_README.md harness/e4/README.md
test "$(ls harness/e4 | wc -l)" = "46"            # the reviewer 02:28: uncertain provenance counts as in
$REPO/.venv/Scripts/python.exe -B -m ruff check --line-length 120 harness/e4 || true   # reported, not a gate
git add harness/e4
git commit -F $S/e4/e51_msg.txt                              # Focus: L3 harness ... / Item: / Co-Authored-By

# 2. tags (annotated; the run each names)
git tag -a e4-tree-38b2daa 38b2daa -m "E4a games 00-17 ran on this tree. One agent. Games 00-17 ran on 38b2daa, games 18-24 and the probe on 7c77689. The only agent change between them is a crash guard (ALPHA-LAST), which alters nothing except where the older tree crashed. The harness cap counted load time on 38b2daa and play time only on 7c77689, so games 00-17 had up to ~85 s less play."
git tag -a e4-tree-7c77689 7c776898de2e -m "E4a games 18-24, the E4b 5-game probe and census run 1 (PYTHONHASHSEED 0, seed 49b07888) ran on this tree. One agent. Games 00-17 ran on 38b2daa, games 18-24 and the probe on 7c77689. The only agent change between them is a crash guard (ALPHA-LAST), which alters nothing except where the older tree crashed. The harness cap counted load time on 38b2daa and play time only on 7c77689, so games 00-17 had up to ~85 s less play."
git tag -a e5.1-2026-10-19 HEAD -m "E5.1: the E4 harness committed on e51-harness, from 7c77689; E4b one-life ruled out on this tree (the reviewer 2026-10-19 01:55). One agent. Games 00-17 ran on 38b2daa, games 18-24 and the probe on 7c77689. The only agent change between them is a crash guard (ALPHA-LAST), which alters nothing except where the older tree crashed. The harness cap counted load time on 38b2daa and play time only on 7c77689, so games 00-17 had up to ~85 s less play."

# 3. push the new branch, the E4 code line it was built from, and the tags
git push origin e51-harness e1-reach-exact e4-sortkey e4-alphalast e4-deadline e0-want t3-row b-triage
git push origin e4-tree-38b2daa e4-tree-7c77689 e5.1-2026-10-19
git log -1 --format="HEAD %H"                                # post this, read from git
