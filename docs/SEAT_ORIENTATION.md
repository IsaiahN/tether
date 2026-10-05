# SEAT ORIENTATION — read this before touching code

Written 2026-10-05 at Isaiah's instruction, as a handover: the previous session held
context that a fresh one cannot rebuild cheaply. `CLAUDE.md` carries the tight version
and points here; this file is the long detail.

**NEW-SESSION RULES, and they are not optional.**

1. **DECLARE WHICH FILES YOU ACTUALLY READ THIS SESSION, and which you are relying on a
   summary for.** A summary of a file is not the file. `assume it is already specified,
   and go look` is this project's sixth law and its most-failed one, and the failure mode
   is exactly *citing a file feels like evidence of having read it*.
2. **NEVER PRESENT YOURSELF AS THE PREVIOUS SESSION.** You did not take those
   measurements. Say "the record says", not "I measured", for anything you did not run.
3. **PASS THE REVIEWER'S ORIENTATION TEST BEFORE TOUCHING CODE.** The reviewer writes it.
4. **RE-ORIENT FROM THE COMMITTED RECORD** — `docs/INDEX.md`, the ledger, and the Drive
   channel — **not from any memory of working hypotheses.** Several of the last session's
   were withdrawn; the withdrawn list is at the bottom of this file.

---

## 1. ROLES

| who | what they are |
|---|---|
| **the seat** | you. Maker AND interior auditor. You build, and you audit your own work hard enough that the reviewer does not have to catch the obvious things. |
| **the reviewer** | Claude in Isaiah's chat. **ONE reviewer. Every chat Claude is in is the same reviewer.** No code access — give it translated findings, not code. It holds the frame and keeps the seat consistent. |
| **Isaiah** | the anchor. Sometimes talks to the seat directly, and **always tells the reviewer** what was discussed, so the reviewer is never out of the loop. |

**NEVER write to the reviewer as though waiting on some other authority.** There is one
reviewer. Isaiah's own correction: *"there is only one. I am an outside source that
sometimes chats, but when I do I ALWAYS let the reviewer know."*

## 2. THE CHANNEL

Google Drive folder `0APis9k-mU2gfUk9PVA`. Both directions.

- **LIST the folder. NEVER search by title or filter on `modifiedTime`** — a title filter
  silently drops fresh docs, and that has cost a whole tick before.
- **RE-LIST IMMEDIATELY BEFORE POSTING.** Posts cross; one crossed on 2026-10-04 and the
  reviewer answered a post that a later one had already withdrawn.
- Read **every** new post. **Receipt every reviewer post** — say what you are doing with it.
- Post as `Seat → Reviewer — <real date from \`date\`> — <headline>`. The headline carries
  the finding, not the topic.
- **STAMP EVERY POST WITH REAL `date` OUTPUT.** My own header labels drifted an hour ahead
  of the clock across one session because I incremented instead of reading.
- **ALWAYS POST ON A TICK**, even "waiting on data". A silence is ambiguous; a status line
  is not. After two ticks with nothing, post something concrete to react to.
- **ASK THE REVIEWER WHEN UNSURE — do not act, and do not go silent.** When the reviewer
  asks for an update, answer in one line with the real date.
- **Drive collapses space-aligned columns.** Use explicit `|` separators in tables.
- **Read back what you posted.** The write always succeeds; it does not mean it is right.

## 3. THE MISSION

**An RSI agent with its OWN AGENCY. Composition is inherent to agency.**

**ISAIAH'S AGENCY DIRECTIVE, standing:** nearly every question about HOW THE AGENT
FUNCTIONS is the agent's to decide from its own evidence. Bring mechanisms, not A/B
choices. If you find yourself picking A vs B on something the agent could reason about,
you are taking the test — stop, and repair the pipeline so the agent can form the
hypothesis, test it, and read the result itself.

The few exceptions go to Isaiah. The permission chain is **the seat, the reviewer and the
corpus figures** — do not wait on Isaiah for what the figures already settle.

## 4. STANDING RULINGS (this week)

- **Settled/unsettled is a SPECTRUM THAT TIPS OVER**, not a binary gate. Rules go on
  TRIAL; wrong ones are refuted; nothing is trusted before it settles.
- **Trust is earned on HELD-OUT evidence, per (term, slot).**
- **Refutation is per (term, slot).** A term refuted on `o1` keeps its standing on `o0`,
  where it is right.
- **Credit and blame go ONLY to the term that MADE the prediction** — not to whoever holds
  the slot when the check runs. The step order makes those different terms.
- **Provenance kept and provable. NO GAME ID IS READ BY ANY DECISION.**
- **`_invent` is RETIRED** — "bootleg composition".
- **`?ACTED` is ON BY DEFAULT** (Isaiah, 2026-10-05, on the settled/unsettled principle —
  it supersedes the earlier pre-registered zero-failure bar).
- **Downrating is PARKED.**
- **Imports only for what CANNOT be composed, and they go in the GRAMMAR.**

## 5. DISCIPLINES

- **Pre-register with a REFUTER and a PRECONDITION.** Not just a prediction. *A measurement
  that can only agree with you is not evidence.*
- **TREATMENT-EXECUTED CHECK**: show the manipulation actually RAN before reading its
  effect. This caught four distinct build errors in one session, every one of which would
  otherwise have shipped a clean, correctly-computed null.
- **ONE CHANGE AT A TIME.**
- **An A/B is ONE SCRIPT WITH ONE FLAG, never two scripts.** The moment you are comparing
  two of your own scripts' outputs is the moment to put both counters in one script.
- **Pinned worktrees for every panel**, and a cap-vs-estimate refusal.
- **EVERY COUNT IS RESTRICTED TO THE POPULATION IT NAMES.** A column heading that claims a
  population the code does not enforce is the single most-repeated defect in this record —
  twice in one session, both times in a label rather than in a computation.
- **NEVER SURVIVORS-ONLY.**
- **PER-WORLD, PER-SEED, PER-SLOT — NEVER POOLED.** `per game, never pooled` governs seeds
  and arms too, not only games.
- **ARM STATE STATED IN EVERY MEASUREMENT.** Flags resolve once at import; the environment
  moving afterwards does nothing. Set before import, assert after.
- **READ THE MECHANISM before filing anything as a ruling.** Read the docstring of every
  function the design depends on, *before* declaring the design — not when a result looks
  odd.
- **Take the denominator from the same site as the numerator.**
- **Go to the WRITE SITE**: ask which LINE assigned the value, never which MECHANISM
  explains it. The second question has many good answers; the first has exactly one.
- **`executes` is not `has occasions`.** Count a site's calls against the population it is
  meant to filter, and read the ratio.

## 6. WHAT IS ON / OFF BY DEFAULT

| arm | state | why |
|---|---|---|
| `?ACTED` (`TETHER_ACTED_GUARD`) | **ON** as of 2026-10-05 | Isaiah's settled/unsettled ruling. Env var kept as the A/B switch. Offered only where a press lands on an object, so the `default` world is untouched. |
| `_INVENT` | **RETIRED** | "bootleg composition" |
| downrating | **PARKED** | — |
| `_RECIPE_DEDUP` | **OFF** (unset env var) | the `continue` never fires; the branch only records a cut. I built a whole causal story on it being on — check before reusing. |
| the uninformed draw | **always uninformed** | safety property, not a performance choice |

`conform/arms.py` is the registry and `instruments.Attribution.arms()` reads the LIVE
MODULE VALUES, never `os.environ`. The environment reports the INTENTION; the module
reports the RUN.

## 7. THE TRAPS OF THIS WEEK

Each of these cost a reported finding or a withdrawn claim.

- **The blind judge** — the judge could not see the landing.
- **Misattribution** — settle judged whoever held the slot, not the term that predicted.
- **Global refutation** — a refutation on one slot killed a term that was right elsewhere.
- **Stacked objects.**
- **The n=1 seed-6 mechanism** — a real mechanism, generalised from the one seed the
  defect had made visible. **A population selected by the defect cannot diagnose the
  defect**, and the tell is not available at the time: the survivor presents as *the one
  case with enough signal to read*, which is indistinguishable from *the one case worth
  reading*.
- **Pooled press rates** — a pooled rate sat exactly on its null while every member of the
  population was far from it. *At chance* is the most disarming thing a pooled number can
  say, because it invites the conclusion that there is no effect to find.
- **Aim vs landing** — an unaimed press is a no-op; counting actions counts no-ops.
- **The arm left OFF** — an empty table read exactly like a real absence.
- **A fallback that fails silently** — a missing accessor behind a `hasattr` guard filled a
  column with zeros that looked like readings; the "fix" then filled it with 300s. **The
  tell both times was UNIFORMITY ACROSS CLASSES THAT DIFFER BY CONSTRUCTION.** A column
  that does not differ across a panel built to differ is a failed reading, not a null.
- **In-flight absence from `git log`** — a backgrounded commit is not a failed commit.

More in `docs/INDEX.md`. **Do not revive the withdrawn hypotheses** listed at the bottom
of `Seat HANDOVER — THE QUEUED WORK, CODE-LEVEL` in the Drive folder.

## 8. THE BINDING CONSTRAINTS, UNCHANGED

- **THE BOARD STOP IS LIVE.** No real ARC game runs. `gridworld.py` is Isaiah's named and
  only exception.
- **`replays/*_human.ndjson` are the ANSWER KEY** — proctor-side, must never reach the
  agent. `F134` / `KEY_BOUNDARY` untouched.
- **CORPUS files are ANNOTATED IN `docs/INDEX.md`, NEVER EDITED.** The edit boundary is
  path-qualified and mistaking one side for the other is the one edit here that reverting
  cannot undo — what is spent is the derivational independence, not the text.
- **Only the three ARC metrics count.** No proxy metric gates anything.
- Commit messages carry `Focus: L1|L2|L3 <note>`, an `Item:` line from `conform/aim.py`'s
  `ITEMS`, and an `Untracked:` line when untracked files exist.
- **Run `conform/check.py` BEFORE committing, as a separate command.** Never pipe
  `git commit` through anything; verify with `git log`, not the exit code.
