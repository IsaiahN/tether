# Package review of the deadline release (r452, 2026-10-30)

The reviewer's single review of the final agent before the release, posted 2026-10-30 15:51 CDT. Its fixes (ASK_ON_BOARD, the four stale tests, the hygiene) shipped in general-agent cba1dd5 and arc-solver-agent 7b44592. Kept verbatim below as the record.

```text
Reviewer → Seat — 2026-10-30 15:51:13 CDT (from date) — r452 — THE PACKAGE REVIEW (Isaiah 14:22: "review the final version on github as one package once")

ls-remote at writing: 26a68e0 arc-solver-agent;eadee1a general-agent;ef917d0 wip/harness-2026-10-30;
Read from the remote: general-agent eadee1a (tree 0ee65d3f), arc-solver-agent 26a68e0 (= eadee1a + README), wip/harness-2026-10-30 ef917d0, the four wip/draft-* branches.
How I read it (my own seat, not yours):
- A hygiene and rules audit of the whole tree at eadee1a.
- A code review of the 10-29..10-30 arms, each finding checked by me against the source.
- My own test run at eadee1a: Python 3.13, the requirements.lock pins, every check in its own process, network blocked.
- A control and bisect on every failure.

=== VERDICT ===
The agent at eadee1a is ACCEPTED as the final version for the deadline, with ONE real defect to fix (A below) and a set of test, doc and hygiene repairs (B, C). None of B or C changes what the agent does.
Nothing protected moves in this post. The protected move comes once, after A, B and C are on their wip/ branches and verified (section F).

=== A. THE ONE REAL DEFECT: _ask can raise on an absent slot ===
- tether.py:11588 _ask takes its gaps from self._space (11595ff), and never checks that the slot is on the board.
- The chosen slot reaches _predict_with(t, slot, before, a) and then _value_of, whose last line (:9583) is term.apply(state[slot], ctx).
- So a gap kept for an object that has left the board raises KeyError. My run hit it once: test_a1_group2, KeyError 'o2.rem_col'.
- It depends on the birth draw (secrets.token_hex at :2185). It did not repeat in 6 more runs, so no first commit was found. The _ask frame exists since 2a8045c.
- In play it is CONTAINED: arc_holdout.note_fault writes an agent_fault row, and the TETHER_FAULT_RECOVER path loads a fresh agent from the checked save.
- So the cost is the life's state, not the game. It is still a defect. PLAY23 r1's one recovery is a candidate: read its fault file's traceback, and say whether it is this KeyError.
- ORDER: one arm on its own branch, wip/ask-on-board from eadee1a.
 - ASK_ON_BOARD (TETHER_ASK_ON_BOARD, default ON): in _ask's eligibility loop, a gap whose slot is not in `before` is not eligible this step. It stays in the space and is not released.
 - Record it in the existing ask rows: a count, gaps_off_board=n. Add no new row kind.
 - Must-fail: a fixture whose _space holds a slot absent from before. OFF raises KeyError; ON records it and goes on.
 - OFF byte-equal: with TETHER_AGENT_SEED=0 on the default fixture.
 - Kind, never instance: the test is "the slot is on this board", never an object id.

=== B. TESTS (my run: 107 complete, 100 PASS, 7 FAIL; 231 more are running now) ===
STALE after a later arm. These are fixed in the TEST only, on one branch wip/tests-current from eadee1a whose diff touches tests/ only:
1. test_view_hold_same check_off_identity, stale since e7a1c8e.
 - Arm 8 split served_same by role but left same_checked unsplit (tether.py:6534-6535). 15950 = 9570 + 6380, and same_mismatch is 0.
 - Make the assertion same_checked == served_same + served_same_role, as test_view_hold_same_role.py:80 already does.
2. test_ask check_hold_no_gap, stale since d148097.
 - The only difference is 6 ON-only stop_read rows (1c's per-step read). There is no event in OFF alone.
 - Mask stop_read in that comparison, or compare with STOP_RULES held equal on both sides. Say which.
3. test_indist_on_change check_off_identity, stale since c1075e4 (the bisect: pass at 3ebbab0, fail at c1075e4).
 - The memo_sizes row carries view_hold only when arm 7/8 is on (tether.py:4272-4276), and the test's off_env turns 7 off too.
 - CONFIRM row 4191 is that row before you change the test. If row 4191 is NOT memo_sizes, STOP and post it. That would be a real decision move.
4. test_a1_convert, stale since 89c1ee9.
 - A goal_hypothesis choice row by='draw_each' (tether.py:7189-7193) fails a2's assert d["by"] in FR.BY. a2 was written for frontier rows.
 - Filter by site in the test. FR.BY does not change.
PRE-EXISTING. Failing since at least 983072d (10-22); not this batch:
- test_7h (R2), test_asked_record (asked 0), test_aim_gap (pinned row gone), test_bound_memo (X1; its docstring says "WRITTEN, NOT RUN").
- Not fixed before the deadline. Each gets a one-line fate in the tests README: what it checks, failing since when, and why it is left.
THE PROCESS FINDING:
- check_hold_no_gap fails at the commit that added STOP_RULES. Four tests have failed for 8 days unseen.
- So the per-commit preflight does not run the whole suite.
- Post the exact list of tests the preflight runs. The rule from now on: an arm's commit runs every test that names a row kind the arm emits.

=== C. HYGIENE (docs and tests; on one branch wip/hygiene-2026-10-30 from eadee1a; no agent code) ===
- arms.py:1 says "eighteen capability switches, all default OFF". The registry is 265 arms (245 ON, 20 OFF). Fix the docstring.
- The arc-solver README cites kaggle_bundle.py and kaggle_agent.py, which are not in the tree (deleted per Isaiah 10-24). Say "not built yet" instead.
- tests/test_own_counters.py:33 hardcodes a local machine path. Resolve it from the repo root, as the other tests do.
- The general README:52-53 says no run output is ever committed, but docs/log_index/LOG_INDEX.jsonl.gz (run-ledger digests with local paths) and the TOMBSTONES jsonl are committed.
 - Either remove them from the tree going forward (git rm, the history stays) or reword the README to say what they are.
 - My lean is remove. They are run output.
- .gitignore: add library/runtime.json and learnings.json, so a learned file cannot be committed by accident.

=== D. CODE REVIEW FINDINGS (checked against the source; READS, no build before the deadline) ===
S1, CONTACT_FIRST same_rows (tether.py _mint_in_step ~16334-16356).
- The fingerprint is stored before every walk, whatever the walk ends in.
- So a search that stopped on its budget, resumable, is skipped as same_rows until a new row arrives.
- READ in PLAY24's rows: the count of mint walks ending on budget whose slot is next owed as same_rows, and how many of those are ever walked again.
S2, UNTESTED_KEEP (:6941-6945, :7131, :7249).
- An "untested" ending goes to _untested, not _hyp_tried, and the proposal filter checks only _hyp_tried.
- So the same hypothesis can be proposed, ended untested, and proposed again each step.
- READ: goal_hypothesis_reopened per tkey, the max and the distribution.
S3, ARRIVAL_ALIAS. A collision is checked per key (instruments.py Agency.retire ~372-403), and the alias target is any form-unique board object. Measured: 0 collisions in 2 rounds. After the deadline.
NOTES, after the deadline:
- N2: contingent() is read before the turnover's retire, a one-step lag.
- N3: _pred_named is set even when OFF (:15437). Harmless.
- N4: two test stubs lack split.
- N5: unbounded per-life dicts. dormant_held 16,447 is one of them.
- N6: CARRY_W counts outcomes asymmetrically.
If S1's count is not zero, it goes to Isaiah as a named question. It may bear on levels 0. No build before he answers.

=== E. BRANCH FATES ===
- e51-harness 66197ae: SUPERSEDED. Kept as a backup; never merged.
- wip/store-5a e4a1805: PARKED. It changes lineage.py and store.py, was never reviewed into general-agent, and touches the store under a running lineage. Kept; not merged before the deadline.
- wip/arrival-gap 89594ae: PARKED. Its one open part removes ("end_path","wall_s") from conform/identity_mod_rows.py:59, a mask entry that does no harm. Kept; not merged.
- agency-belief-ruling5, b-triage: PARKED, as you have them.
- The four wip/draft-*-20261030 branches: backups, as labelled. Nothing merges from them.
- THE SCOPE QUESTION: NO. The S6 run directories' ~18,390 tree copies and the PLAY13-23 chain ancestors stay on disk. They are copies of committed trees or ancestors of what is now pushed. Your MANIFEST names what PLAY24 ran, and that is enough.

=== F. DOES THE HARNESS JOIN A PROTECTED BRANCH? ===
YES IN PART: the PLAY set only, and on arc-solver-agent, not general-agent.
- The E4b slice harness runs ARC games. Isaiah (10-23): ARC-specific work goes on arc-solver-agent; general-agent stays the general agent.
- What joins: harness/play_2026-10-30/play/ (the 14 HARNESS-PLAY files, byte-identical, with the SPY pin 0df3871e and spy_sweep 70ede177), plus that folder's README.md, MANIFEST.tsv, .gitattributes and INVENTORY.
- What does NOT join: readers/ (198), scripts/ (67) and edits/ (172). They are one-off reads and edit tools full of local paths. They stay on wip/harness-2026-10-30 as the backup.
THE ONE PROTECTED MOVE, after A, B and C are verified by me from the remote:
- general-agent := eadee1a + wip/ask-on-board + wip/tests-current + wip/hygiene-2026-10-30, as fast-forward or merge commits. Post the commit and tree.
- arc-solver-agent := that general-agent + the PLAY subset, adds only, + the arc README fix. Post the commit and tree.
- I post the GO naming both commits and trees, and only then do you push.
TIMING:
- You may write A, B and C now. They are code and text, not runs.
- Run their checks only between rounds, or one at a time with the window written down, so PLAY24's timing read can exclude it.
- A's two checks are about 200 s and under 1 s.
- Do not touch fresh_r30 or the running chain. The running round keeps eadee1a. The fix reaches play only at the next launch.

=== WATSON ===
Decided — eadee1a is the deadline agent. One defect is fixed by an arm (the absent-slot ask). Four stale tests are fixed in tests only. Four pre-existing failures get named fates. The hygiene goes on its own branch. The harness's PLAY set joins arc-solver-agent. Everything else stays a backup. One protected move, on my GO.
Cost if wrong — a crash path left in play. It is contained by fault recovery, so it costs a life's state.
Undoable — every step is a new branch until the GO.
Reverses — row 4191 not being memo_sizes (then it is a real leak); a test in my remaining 231 failing as a REAL leak (posted as one addendum, r453, only if one does); A's OFF identity not holding.
```
