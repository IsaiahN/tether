# Item 10 — fast commits, full green kept

**The problem (the seat's own account, relayed by Isaiah):** `.git/hooks/pre-commit` runs
`conform/check.py`, which runs all 23 seats one after another, several of them running the agent.
That's about 4 minutes on a quiet machine and about 20 under load. The seat routed around it
(worktrees, branches, an unreviewed backlog); Isaiah has switched the hook off for now.

**The fix: `conform/fast_check.py`**, which reuses `check.py`'s own STAGES table and
`run_stage`, so nothing is copied.

1. **A seat's pass is reused only when its inputs are byte-identical.** Each seat declares the
   files it reads, kept as data and conservative. Its fingerprint is the git blob ids of those
   files *in the index*, which is the exact tree being committed. An identical fingerprint plus an
   earlier `ok` means the pass is reused, and it's printed with the commit it was earned on.
   FAIL, INCOMPLETE and DID-NOT-RUN are never reused. `aim`, which reads `git status`, always
   runs. Changing `fast_check.py` or `check.py` invalidates everything, and `--all` ignores the
   cache.
2. **Whatever runs, runs in parallel,** one worker per core.

**Measured on `seat-act` e50406d with `--explain`:**

| a commit that changes | seats that re-run |
|---|---|
| a docs file that no code reads (LEDGER.md, rulings, plans) | **0**: all 23 reused (aim still runs) |
| docs/INDEX.md | **1** (`figures`) |
| any `.py`, `library/*`, `docs/library-closure/*` | all 23, in parallel |

Most of the seat's commits are record commits, and those become seconds. Code commits keep full
re-checking, but in parallel rather than in a row.

**To install:** `.git/hooks/pre-commit` runs `python conform/fast_check.py` instead of
`conform/check.py`. The commit-msg hook (`focus.py`) is unchanged.

**Follow-ups for the seat (not done here):**
- The M2, entry and perception suites each warm their own agent. Warming one agent per run and
  sharing it is the next saving, and it's a change inside those suites.
- Any new code that opens a doc must add that path to `DOCS_READ_BY_CODE`. Otherwise the cache
  would wrongly reuse a pass. The seat should add a check for this to the record-format seat:
  every `read_text` or `open` of a non-code path appears in the table.

**Isaiah's ruling needed:** does a pass reused on byte-identical inputs count as "full green"
under the 2026-09-30 rule? The case for yes is that a seat's result depends only on its inputs,
and every reuse is printed with its fingerprint, so it can be checked commit by commit.

**Figure census:** Figure 12, *"where the arrangement is recorded, re-deriving it is a lookup and the actions were spent once"* (the reuse); Figure 10, *"a
convention nothing can check is a constant the seat authored"* (every reuse is printed and
checkable); Figure 11, the run names exactly which tree it measured. Strained: none.
