# Item 11 — the branch and repo audit

Reviewer seat, 2026-10-08. Read from git, not from memory: all 59 branches fetched and each measured
against `seat-act` (is it an ancestor; how many commits ahead; does its change already reverse-apply
to the tip); every tracked file on `seat-act` e50406d classified by its import graph, its
`__main__`, its docstring and the docs inventory. The seat's branch map (Drive, 09:00) agrees with
these measurements on every point checked.

---

## Part 1 — Branches (59)

### The line of record — straighten this first
- **The main line is `seat-act` (tip e50406d).** It holds every committed and gated change through
  F511 (`c8bbb31`), plus the complete rulings file and the run harness.
- **`arc-agent` is one commit (4b476e6, Isaiah's staged commit) on 9df70c9**, the point where
  seat-act forked on 2026-10-06. Despite its name, it is not the latest code.
- **GitHub's default branch is `core`, two months old**, so anyone opening the repo lands on stale
  code.

**Recommendation (Isaiah's call, on his account):**
1. Bring Isaiah's commit 4b476e6 into the line (done by the seat as a MERGE, nothing rewritten). Correction (seat, 12:02): the seat-map line in seat-act is Isaiah's own 2026-10-06 amendment (F461), not a seat edit; his staged copy has the pre-amendment sentence. Which stands is his call.
2. Fast-forward `arc-agent` to the result, so the original name is the main line again.
3. Set GitHub's default branch to `arc-agent`.
4. From then on, the seat commits to `arc-agent`, and `seat-act` is retired.

### Every other branch, by status

| status | branches | verdict |
|---|---|---|
| **bookmark**: already an ancestor of the main line, nothing extra | seat-abort, seat-base, seat-cost, seat-cuts, seat-f506, seat-f507, seat-f508, seat-f509, seat-f510, seat-objdomain (10) | **DELETE**: their commits are in the main line |
| **contained**: one commit whose change already reverse-applies to the tip | wip/wt15-1007, wip/wt37-1007, wip/wt38-1007, wip/wt41-1007 (4) | **DELETE** |
| **superseded**: its one entry is already in the main line's complete rulings file | seat-entry | **DELETE** |
| **queued builds**: one change each, not merged, each ruled | seat-bondread, seat-novelbin, seat-filled, seat-commens, seat-prev, seat-armstate, seat-observer, seat-types (built on 7f6501e; must be replayed onto the tip); seat-budget, seat-costcount (built on c8bbb31; apply cleanly) | **KEEP** until each lands, then delete. **Re-order the queue under the library plan:** several now fold into it (seat-filled, seat-observer and seat-types touch the readings and types that readings.json supersedes) |
| **parked or withdrawn experiments** | seat-lever-a (Lever A, parked F482; seat-budget is its successor); contest-withdrawn-F417 (the contest arm, withdrawn under F417); agency-belief-ruling5 (2026-10-03, one change to instruments.py) | **ARCHIVE** as tags `archive/<name>`, then delete the branch |
| **leftover worktree states**: one commit each, "NOT reviewed", no longer apply | seat-wip, seat-wip2, wip/wt5, wip/wt9, wip/wt16–36, wip/wt39–40 (27) | **ARCHIVE** as tags, then delete. Each is most likely a draft of the main-line commit after its base, which git cannot prove. Tags keep them recoverable without 27 branches |
| **old scratch tree** | wip/prefix (2026-09-21, +200 commits of an earlier session, 119 files) | **ARCHIVE** as a tag, then delete |
| **original** | core | **KEEP** as the historical root, but not as the default branch |

**Result:** 59 branches become **2 plus the queue**: `arc-agent` (the line), `core` (history), and the
queued builds until they land. 31 tags keep everything recoverable.

---

## Part 2 — Files on the main line (about 175 tracked)

**Shape:** 75 root files (71 modules), 64 docs, 20 conform, 8 harness, 6 library, 1 test fixture
folder, `.claude/settings.json`.

### Agent and habitat — KEEP
tether, gamma, arc_atoms, arc_percept, arc_world, arc_predict, arc_holdout, arc_lens, arc_run,
interface, routine, sensors, instruments, condition, composer, retrieval, relations, observer,
priors, visible, speak, grammar, habitat, world, gridworld, snaps, self_family, arc_self, summary,
gate, census, ledger, behaviour, probe, experiment, closure_map, kaggle_agent, kaggle_bundle,
tether_agent, tether_runner, demo.

### Library-adjacent — CONSOLIDATE (CODEBASE_CHECK.md)

| file | verdict | why |
|---|---|---|
| inherited.py | **MERGE** into the library runtime | a second lighting path; its only consumer is the curiosity aim |
| detectors.py | **RETIRE** after the template generator lands | conditions written by hand per atom: the 2,700-functions path in small (Figure 13) |
| mapping.py | **MOVE** to `tools/` (seat-side) | lint-fenced as a cue module; an answer-key mapper, not the agent's path |
| sensors_heavy.py | **DELETE** | its own docstring (reviewer 2026-09-23): "SUPERSEDED, AND PENDING DELETION … Do not build on this module". Two importers (detectors, observer) must drop it first |
| self_graded.py | **KEEP, UPDATE** | read the library's `working_set` flags |
| observer.py | **KEEP, UPDATE** | widen from "the frozen 8" (the freeze was withdrawn 2026-09-22) to readings.json |

### Seat-side tools (not imported by the agent; scripts with `__main__`) — MOVE to `tools/`
arc_check, arc_online (keep; needed for the live gateway), arc_screen, demand, feeder,
reverse_engineer, rlvr, framepair, synth, tieracc, transcript, check_paths (imported by nothing).
Moving them stops the root mixing the agent with the instruments that measure it (Figure 10: the
seat may author what has no truth value; keeping the two apart keeps that visible).

### DELETE
- **scratch_bins, scratch_detector2, scratch_determinism, scratch_equiv, scratch_panel, scratch_smoke,
  scratch_why.** These are one-off probes; their findings are in INDEX; git keeps them.
- **contest_table.py, contest_read.py.** The contest arm was withdrawn (F417). Archive with the
  `contest-withdrawn-F417` tag.

### harness/
- **rb_all25.py, rb_one.py**: **DELETE**, superseded by their pinned versions `rb_all25p.py` and
  `rb_onep.py` (the 2026-10-08 one-commit rule).
- **rb_links.py / rb_links2.py**: **KEEP both, renamed** `rb_links_first_reader.py` /
  `rb_links_second_reader.py`. Both readers are pre-registered instruments, and the first all-25 was
  read under the first.
- **rb_heads.py and its test**: **KEEP**.

### conform/ (20)
**KEEP all.** Add `fast_check.py` (item 10) and the library check (LIBRARY_SPEC §5 #8).
`conform/ITEM` is the aim seat's input. Keep it; `fast_check` now fingerprints it.

### docs/ (64)
See **DOCS_CONSOLIDATION.md**: 27 deletions now, 5 after named changes, moves to `library/sources/`
and `docs/corpus/`.

### library/ (6 → the new set)
Replace with `library_v2/`:
- **data:** atoms, molecules, agent_atoms, relations, readings, grammar, clusters, domains,
  grid_groundings, reads_explicit, orientation_draft;
- **derived:** index;
- **logs:** DEDUP_LOG, ROLES_LOG;
- **docs:** LIBRARY_SPEC, LIBRARY_DESIGN, BUILD_REPORT;
- **code:** build_library.py, library_runtime.py.

`tag_index.json` is superseded by `index.json`; delete it after `inherited.py` moves.

---

## Part 3 — Checked against the Tether

| finding | figure | where |
|---|---|---|
| **Two stores of one library, three copies of the perception vocabulary, four lighting paths** | Figure 6: *"What is recorded only grows. What is reachable is derived"*; one record, derived reach | CODEBASE_CHECK |
| **A built cue with no consumer on the reach path** (`self.cue`) | Figure 11: *"An improvement that does not change contact changes nothing, however much it improves."* | tether.py `_narrate_cues` says so itself |
| **Conditions written by hand per atom** | Figure 13: *"That record is not documentation of the term. It is the term"*: entries are data run by one path | detectors.py |
| **A registry fixed at construction: the agent cannot add an atom** | Figure 12: *"A settled molecule becomes an atom for whatever composes over it"* | gamma.py |
| **Built capabilities left switched off by default with no ruling** (11 found; all ruled 2026-10-08) | Figure 10: *"a convention nothing can check is a constant the seat authored"* | conform/arms registry |
| **A superseded module still in the tree, still imported** | Figure 10, the same line | sensors_heavy.py |
| **The default branch and the line of record disagree; a seat edit in a corpus file** | the authority order (figures, then corpus, then rulings) | Part 1 |
| **59 branches, from a hook so slow it was routed around** | Figure 12: *"where the arrangement is recorded, re-deriving it is a lookup"* (the fast gate) | item 10 |

## Figure census
Figures 6, 10, 11, 12 and 13, quoted above and grepped against the figure text. Strained: none.
