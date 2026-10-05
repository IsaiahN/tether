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

## 0. THE BIG PICTURE — READ THIS BEFORE SECTION 1

**Added 2026-10-05, second pass, at Isaiah's instruction relayed by the reviewer.** The
first draft of this file covered the week's click-learning chain in depth and said almost
nothing about **why any of it matters** — so a fresh session could do the week's work well
and still drift on direction. The reviewer supplied a six-point draft and asked that it be
**checked against the record rather than transcribed**. It was. **Appendix A** lists what changed and
why; **two of the six points were wrong in a way that mattered**, and one of those two would
have put a prohibited thing at the top of the first file a new session reads.

### 0.00 AGENCY IS PARAMOUNT — THE FIRST THING, AND THE TEST FOR EVERY DECISION BELOW

**Isaiah, 2026-09-23 (agent-first, not a mech suit), 2026-10-01 (the standing agency
directive) and 2026-10-05.**

**THE AGENT IS THE DRIVING FORCE BEHIND EVERY DECISION, NEVER A PILOT INSIDE MACHINERY THAT
DECIDES FOR IT.** This is a **recursively self-improving** agent. It must be allowed to
**GROW** and to **DECIDE THINGS ON ITS OWN**: composing its own programs in its grammar,
minting and importing what it lacks, and deciding from its own evidence — **recording why**.

> **OUR JOB IS TO SUPPLY THE MEANS AND NEVER THE MEANING.** The means are offers, evidence,
> instruments, vocabulary, and the ground that judges. The meaning — which composition, which
> goal, which cause, what to invent when nothing fits — is the agent's work and is refused to
> us. That is this file's §0.5 test (*ANSWER or MEANS?*) applied to decisions rather than to
> the library.

**WHEN A QUESTION IS ABOUT HOW THE AGENT FUNCTIONS, THE DEFAULT ANSWER IS: LET THE AGENT
DECIDE, AND RECORD ITS REASON.** Not *decide it carefully on the agent's behalf*.

**EVERY STOP-GAP THAT DECIDES FOR IT IS TEMPORARY AND IS TO BE CONVERTED** — a numeric
threshold, a hand-picked tie-break, a gate that refuses before the agent is consulted. They
are allowed to exist; they are not allowed to be the destination. **The audit of 2026-10-05
found the shape of the work: at all four of Isaiah's sites the machinery already WRITES the
offer and nothing READS it, so the conversion is a READER, not a rebuild** (§7e).

**THE EXCEPTIONS THAT STILL GO TO ISAIAH** are listed in `docs/ISAIAH_RULINGS.md`
(2026-10-01): anything that would encode an answer; ARC boards and the board stop; provenance
(learned vs carried); the corpus and its rulings; data sources and what is published.

### 0.0 THE DEADLINE, AND THE RECORD THIS FILE IS CHECKED AGAINST

**THE AGENT COMPLETE AND KAGGLE-READY BY 2026-10-12** (Isaiah, 2026-10-05) — **a FEATURE
sprint, not readiness-only**: the queued features are in scope, ordered by dependency, with
Kaggle readiness running alongside rather than after. **Then 1–2 weeks** of private-test
results coming back from Kaggle and human-replay prior training (the Phase 2 walkthrough
work). **THEN THE FINAL SUBMISSION, 2026-11-02.**

**AND HIS WORKING RULE, WHICH IS PART OF THE SAME RULING.** **NO STOPPING FOR TIME-OF-DAY
REASONS, EVER** — neither the seat nor the reviewer judges elapsed time well, and the work
runs faster than either estimates. **The only legitimate stops are a genuine blocker that
needs a ruling — post it and keep working on anything independent — or a context clear
Isaiah has scheduled.** Real `date` is for timestamps, never for a reason. **And size work
by WHAT IT INVOLVES — files, sites, checks — never in days or sessions.**

**THE ARC PRIZE 2026 FINAL SUBMISSION DEADLINE IS 2026-11-02.** It belongs at the top of the
big picture because **it is the clock every priority below is set against.**

**AND THE RECORD IS THREE PLACES, NOT ONE: `docs/INDEX.md` + THE DRIVE CHANNEL +
`docs/ISAIAH_RULINGS.md`.** **Appendix A** records two rulings I reported as unverified after
searching `INDEX` and not the channel. **Both were Isaiah's, both were ruled and posted, and
a grep could never have reached either**, because the channel is not in the repository.
`docs/ISAIAH_RULINGS.md` exists to close that hole and **is kept current in the session a
ruling arrives.**

### 0.1 THE GOAL

Build the agent's reasoning and composition until it generalises across the public games
and then, **ALONE, into the PRIVATE out-of-distribution set it has never seen** — with only
its library and its own reasoning — **and can say HOW and WHY it acted.**

Wins on the public 25 are not the deliverable. `CLAUDE.md`'s first rule: **the agent is the
prize, winning is not** — *a black box that wins teaches nothing.* **A win produced by us is
worth less than a loss the agent can explain.**

### 0.2 THE ENGINE

**One uniform per-step loop for every problem. No type branching.** perceive · bet · be
wrong · mint · settle · promote · import. **Γ predicts explicitly**, so its model is
readable; **the residual is the cause-and-effect signal**, and it is an explicit object;
**a term mints only when it pays the bargain**, and minting is an inspectable event.

**That legibility is the instrument, not a nicety.** It is the only reason triangulation is
possible at all — Isaiah and the reviewer read the agent *through* predict → residual →
mint. **A change that makes the agent better and its reasoning unreadable is a LOSS.**

### 0.3 WHERE WE ARE IN THE SEQUENCE

**ARC boards are STOPPED.** Not paused for convenience — stopped because the work was
drifting toward building for those specific games, which is the one unforgivable failure in
`CLAUDE.md` wearing a reasonable costume. **`gridworld.py` is Isaiah's named and only
exception**, and the current job is to finish the agent there.

**Then Phase 2:** human-gameplay priors harvested from retro-game walkthroughs, for the
kinds of game the public set leaves out. **Stage 1 passed and is paused.** The data
directory lives outside the repository, the games are aliased (`G01`, `A01`), and **no
repository file carries licence commentary.**

**If Phase 2 proves unviable:** ARC, then a Phase 3 that reverse-engineers the priors games
require and simulates them on boards.

**ARC REOPENS ONLY WHEN ISAIAH SAYS SO, AND THE CONDITIONS ARE HIS — RULED 2026-09-29.**
**(a) the agent complete**, and **(b) a measured way to automate or randomise which boards are
shown, so the proctor cannot build toward specific boards**, likely with a freeze. **Notes and
ideas about ARC go through the reviewer and Isaiah first.** And before ARC reopens he wants
**more priors trained outside the game distribution** — walkthroughs and images of retro
games. (`docs/ISAIAH_RULINGS.md`, 2026-09-29.) **I filed this as the reviewer's unverified
label on 2026-10-05 and was wrong; see **Appendix A (d)**.** What binds regardless: **building toward a
board is forbidden whether the freeze is on or off, and that prohibition never depended on the
freeze.**

### 0.4 WHY THE TEST WORLDS MATTER

Each `gridworld` family stands in for a capability the agent **does not yet have** — not for
itself, and not for its own number.

**AND THE PARADIGM IS ISAIAH'S, RULED 2026-10-03 AND RESTORED HERE AFTER I WRONGLY CUT IT:
THE PLAYER IS OUTSIDE THE BOARD, AND IT IS A JIGSAW PUZZLE, NOT A MAP.** Bird's-eye, working
buttons and levers, never a piece in it; the purpose on every board is to **win the level**.
*Hold a fuzzy picture of where things go, made concrete by filling gaps, pattern-matching and
verifying in a loop — faster as pieces settle.* **Goal formation is designed on that
paradigm**: root goal = win; candidate end-states held as unsettled hypotheses; the gap points
to the levers; track record crosses games. (`docs/ISAIAH_RULINGS.md`, 2026-10-03.)

| family | the capability it stands in for |
|---|---|
| `click_only`, `buttons` | **acting with NO AVATAR** — the player is outside the board and presses things; pressing one object changes another. The agent must learn *what my action causes* with nothing it can identify as itself |
| `remap_after` | the controls changing underneath a belief the agent has already formed |
| `default` | the baseline, and **it cannot test `?ACTED` at all** — no press lands on an object there, so the guard is never offered |
| **the mode-switch fixture** (the BODY SWAP) | **games that change how you control them** — the controls are swapped underneath the agent mid-run. **It is a TEST, not a `gridworld` family**: `test_gate.py:296`, and `gridworld.FAMILIES` is exactly four. **Agency's reset on belief withdrawal is OPEN** (paper; no `reset`/`withdraw` symbol in `instruments.py`) |

**The point is never the family's number.** A capability that lifts one test world and
transfers nowhere has done nothing; see §0.6.

### 0.5 THE CONSTRAINTS THAT SHAPE EVERY CHOICE

- **THE BUDGET.** The private test runs on a fixed time budget, so the library is
  **FRONTLOADED** — roughly 2,700 atoms reachable — rather than searched from cold.
  Measured: **gridworld today runs on 14 of them**, and the vocabulary bridge is open work.
- **FRONTLOAD IS NOT ENCODING, and this is the mistake every seat here has made.** A
  vocabulary is **what the agent can SAY**; the answer is the **composition** over it.
  Handing the alphabet does not hand the sentence. **The test is one question: does this
  hand the agent an ANSWER, or a MEANS?** A fold construct is a means; a solved board is an
  answer.
- **COMPOSITION IS INHERENT TO AGENCY.** Imports are rare, are for what cannot be composed,
  and go **in the grammar**.
- **THE LIBRARY IS MADE EXECUTABLE BY A FEW GENERATORS, NEVER BY 2,700 HAND-WRITTEN
  FUNCTIONS** (Isaiah, 2026-10-05). A **condition compiler**, **bond combinators** and a
  **recipe compiler**, built LAZILY on demand, turn a library entry into something that runs
  from its own description.
- **AND THE AGENT WRITES ITS OWN PROGRAMS IN ITS GRAMMAR, which is the requirement behind
  that.** A minted term, an imported atom, a routine — **each must be EXECUTABLE because it
  is built from executable parts by executable bonds.** Otherwise nothing the agent mints or
  imports can actually work: **the grammar is the agent's programming language and the
  combinators are its interpreter.** This is the same ruling as *belief is a wager* from the
  other side — recipes carry conditional logic, so the agent programs its own subroutines
  without writing code. **That is the RSI.**
  **MEASURED STATE, so nobody reads the above as done:** **`BONDS = 1`** (`tether.py`, ~line 311 -- grep the symbol)
  — one of the seven bonds has a form in PREDICT, so **terms are chains**. **`or` exists in
  GUARDS** (`condition.py:158` parses it into `Bool("or", …)`; `_compound_guards` builds
  them) and in routines via guards. The generators are **not built**.
- **NO DECISION MAY DEPEND ON A GAME'S IDENTITY.** The moment one does, transfer is
  impossible and the whole claim is unfalsifiable.

### 0.6 THE PRIORITY RULE

**When choosing what to work on, prefer what moves the agent's GENERAL capability — one
loop, legible, transferable — over what improves a number on one test world.**

This week's chain matters because **"learn what my action causes, with no avatar" is a
prerequisite for a whole class of games**, not because of the `buttons` world.

**And the sharper form of the same rule, from `CLAUDE.md`:** *capability is a property of
agent-and-habitat. An improvement that does not change CONTACT changes nothing, however much
it improves.* **Ask of a change whether the agent can now reach something it could not** —
not whether a number moved. Most work does not touch contact, and that is not a failure;
only contact moves capability.

### 0.7 CORRECTIONS TO THIS SECTION

**Recorded in Appendix A at the end of this file.** Five corrections were made to the
reviewer's draft of section 0, two of which were later overturned. **The evidence is kept in
full — an error entry whose evidence is edited away stops being evidence — but it is at the
back, because a fresh session should meet the RULINGS before it meets the withdrawn versions
of them.**

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

- **FIND NEW POSTS BY `createdTime > last_seen`. NOT by listing and reading the top.**
  **This replaces *list the folder and read the newest*, which was wrong in a way that cost
  most of 2026-10-05.** That rule carried an unstated assumption — **that a listing comes
  back newest-first — and it does not.** A check returned a 12:08 post as the first row
  while four later ones existed, and two reviewer rulings sat unread behind it. *Every
  "waiting on the reviewer" that day was this.*
  - **Keep `last_seen` = the `createdTime` of the newest post you have read, and state it
    in each post you write**, so the next check has an anchor and so the reviewer can see
    what you had when you wrote.
  - **Query `createdTime > last_seen`, read EVERY result, and sort them yourself.**
  - **An empty result means nothing new.** A listing whose first row is old means nothing
    at all.
  - **`createdTime` IS A LEGITIMATE FILTER AND `modifiedTime` IS NOT, and the difference is
    the whole point:** `createdTime` never changes, so nothing can slip behind a watermark;
    `modifiedTime` moves and its index lags, which is how a `modifiedTime >` filter drops
    documents that already exist. **Never filter by title either** — that drops fresh docs
    for a different reason and has cost a whole tick before.
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
- **CARRY A STEP THROUGH ONCE IT IS ORDERED. Do not wait for a reviewer doc to start or
  finish something that needs no ruling.** Wait only where a GENUINE RULING is needed —
  and then post the question and keep working on anything independent. **Today's stalls
  were the listing defect above rather than this**, but the rule belongs beside the
  protocol, because a broken channel and an unnecessary wait are indistinguishable from
  the outside and the fix for one is not the fix for the other.

## 3. THE MISSION

**An RSI agent with its OWN AGENCY. Composition is inherent to agency.**

**ISAIAH'S AGENCY DIRECTIVE, standing:** nearly every question about HOW THE AGENT
FUNCTIONS is the agent's to decide from its own evidence. Bring mechanisms, not A/B
choices. If you find yourself picking A vs B on something the agent could reason about,
you are taking the test — stop, and repair the pipeline so the agent can form the
hypothesis, test it, and read the result itself.

The permission chain is **the seat, the reviewer and the corpus figures** — do not wait on
Isaiah for what the figures already settle.

**THE EXCEPTIONS THAT DO GO TO ISAIAH, and they are the whole list:**

- **Anything that would ENCODE AN ANSWER.** The one unforgivable failure; never the seat's
  call, never the reviewer's.
- **ARC BOARDS AND THE BOARD STOP.** The stop is live. `gridworld.py` is his named and only
  exception.
- **PROVENANCE — learned vs carried.** What counts as which, and what may cross.
- **THE CORPUS AND ITS RULINGS.** Annotate in `docs/INDEX.md`; never edit; never reinterpret
  a ruling of his into a different scope.
- **DATA SOURCES AND WHAT IS PUBLISHED.** What the agent may read, and what leaves here.

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

**THE PRICING RULINGS, which are easy to get wrong because two of them are partial:**

- **THE BARGAIN'S VALUE IS THE SLOT'S OWN UNEXPLAINED RESIDUAL.** Understanding is already
  priced — Oct 1. **The ADOPTION half of that ruling was WITHDRAWN**; do not cite the whole
  thing as standing.
- **GUARD KIND costs `log2(k+1)`; THE REFERENT costs `log2(|refs|+1)`.** Both in
  `_guard_bits` (`tether.py:616`). `ACTED_SELF` is collapsed into `ACTED_ON<own owner>` and
  pays the same — no cheaper special case.
- **INTENT GUARDS ARE STILL UNPRICED.** `F408`, OPEN. A guarded term is strictly more
  specific than its unguarded form whatever the guard, so the free ride is wrong in
  principle — but repricing every guard broke 6 of 29 M2 checks, so it needs its own
  pre-registration and has not had one.

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
| `?ACTED` (`TETHER_ACTED_GUARD`) | **ON. FLIPPED 2026-10-05 — the default is now `"1"` and `tether._ACTED_GUARD` reads `True`** | Isaiah's settled/unsettled ruling, superseding the zero-failure bar. **The warrant is HIS RULING, not the per-seed test**: at the flip, all six world-seeds read INSUFFICIENT and only the pooled fallback passed (guarded 3/7 vs unguarded 0/2) — see the comment at the flag. **Do not cite "the condition was met" as though it was met per seed.** The env var stays as the A/B switch. Offered only where a press lands on an object, so the `default` world is untouched. |
| `_INVENT` | **REMOVED FROM THE TREE 2026-10-05** — flag, call site, `_invent` and the `conform/invent.py` seat | "bootleg composition"; RETIRED means gone. `conform/arms.py` `RETIRED` now refuses the flag if it is read anywhere. `gamma.invent` stays: a carried library re-invents on load |
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

More in `docs/INDEX.md`.

### WITHDRAWN — DO NOT REVIVE

Copied verbatim from the bottom of the Drive doc `Seat HANDOVER — THE QUEUED WORK, CODE-LEVEL`
on 2026-10-05, at the reviewer's instruction, because that doc is now banner-marked SUPERSEDED
and this list had no home in the repository.

      * "condition.py has no Or"            FALSE. `Bool(op="and"|"or")` exists,
                                            parser accepts `or` (condition.py:156),
                                            `evaluate` is Kleene-correct.
      * the n=1 seed-6 closed-gate mechanism as the PANEL's blocker
                                            REAL for seed 6, wrong by 10x in scope.
      * "the blocker is residual size"      base reaches 18.0; withdrawn.
      * "9 of 10 adopt"                     0 of 10; the counter had no slot filter.
      * "aiming is causally blind"          it is a BIAS, at half chance; the pooled
                                            figure hid it.
      * "`inc` explains most rows"          nine of ten slots are UNBOUND.
      * the lock-in hypothesis              R is clean on 100% of late cycles on all
                                            nine, and they still adopt nothing.

## 7b. THE OLDER BACKLOG — status as of a59c77b, so it is not lost

**Status verified from the code where the column says VERIFIED; otherwise it is the
reviewer's label and says so.** Do not read "paper" as "abandoned" — it means nothing is
built yet.

| item | status | where |
|---|---|---|
| **session provenance** — the `carried` field | **BUILT (verified)** | `gamma.py:755`, `self.carried: dict[str, dict]`, *"SET AT LOAD, never at mint: a term that originated elsewhere says so without the reader having to parse a game name out of a handle."* A merge that forgets its members fails the provenance claim (reviewer, 2026-10-03) — surviving name → the birth handle of every instance absorbed into it. |
| **session provenance** — the post-play transfer report | **PARTLY BUILT** (reviewer's label; I did not verify the report end) | pairs with the `carried` field above |
| **operand transfer** | **OPEN** | no `operand_transfer` symbol anywhere in the tree (verified absent) |
| **the mode-switch fixture** | **PARTLY BUILT (verified)** — a TEST exists, not a world | `test_gate.py:296`, `test_agency_cannot_see_a_mode_switch_and_inverts_the_reading`. **It is NOT a `gridworld` family** — `FAMILIES` has four and this is not one of them. |
| **the Agency reset on belief withdrawal** | **PAPER** (reviewer's label; no `reset`/`withdraw` symbol found in `instruments.py`) | pairs with the mode-switch fixture |
| **the pairwise-distance atom (Change B)** | **PAPER** (verified absent from `arc_atoms.py`) | — |
| **set-aside goals** | **PAPER** (verified: no symbol in the tree) | — |
| **the Phase 2 walkthrough viability test** | **STAGE 1 PASSED AND PAUSED** | and its conditions are constraints, not notes: **the data dir lives OUTSIDE the repo**; **aliases `G01`/`A01`**; **no licence commentary in any repo file.** |

## 7c. THE TEST WORLDS — what each one can and cannot test

`gridworld.FAMILIES = ("default", "click_only", "remap_after", "buttons")` (verified,
`gridworld.py:759`). **`gridworld.py` is Isaiah's named and only exception to the board
stop.**

| world | what it is | what it CAN test | what it CANNOT |
|---|---|---|---|
| `default` | movement, no positioned click | the loop end to end | **anything about `?ACTED`** — no press lands on an object, so the guard is never offered. This is why the flip must be byte-identical here. |
| `click_only` | clicking recolours the object clicked | SELF-caused rules; the true rule binds as `inc ?ACTED_ON<the slot's own owner>`, `left 0.0` -- **NOT `ACTED_SELF`, which was collapsed into it** (section 4) | remote causes — there are none |
| `buttons` | **Fixture C** — a button advances its PARTNER and leaves itself alone, so the effect is unambiguously remote | remote causes, the four-way cause split, everything in handover items 2–4 | — |
| `remap_after` | the action mapping swaps mid-run | re-learning after a rule change | needs `cycles` — it raises without one |
| the mode-switch fixture | a test, not a world (`test_gate.py:296`) | that Agency cannot see a mode switch and inverts the reading | it is not a habitat; you cannot run a panel on it |

**THE DRIVE HANDOVER'S ITEM-1 PRE-REGISTRATION IS SUPERSEDED HERE (reviewer, 2026-10-05).** It
predicts the `click_only` true rule binds `inc ?ACTED_SELF<o0>`. **It binds `inc ?ACTED_ON<the
slot's own owner>`** — `ACTED_SELF` was collapsed into it (section 4). The handover's banner
vouches for it on *code sites, traps and pre-registrations*; **read that as code sites and traps
only.** Its pre-registrations are superseded wherever this file states one.

**SEEDS 0–2 ARE THE STANDARD PANEL.** **AND 30 CYCLES IS TOO SHORT FOR A REMOTE CAUSE
(`F436`)** — at 30 cycles 1 of 10 ONE-remote slots clears the mint's floor; at 60, 10 of 10.
Every ONE-remote null taken at 30 cycles is a reading of a slot with nothing to spend, not a
reading of any mechanism.

## 7d. THE LIVE OPEN ITEM — `CUE_BOUNDARY` IS THE 2,700-ATOM WIRE'S BLOCKER

**Reviewer, 2026-10-05: keep this LIVE in the queue, not as history.** It is not a finished
finding; it is the reason the vocabulary bridge in §0.5 keeps stalling across seats, and
nothing has been done about it.

`conform/lint.py`'s **`CUE_BOUNDARY`** rule blocks the betting path from importing
`_CUE_MODULES = {relations, observer, mapping, detectors, composer}`. **It is wrong on two
independent axes, both verified 2026-09-22** (memory: `cue-boundary-scoped-by-module-not-input`):

1. **ITS ONLY STATED PREMISE WAS WITHDRAWN.** The rule cites `ARC_AGENT` §12.3 verbatim —
   *"reaching is the only evidence the composition system works"* — and **Isaiah superseded
   exactly that clause on 2026-09-19**: the evidence moved to OOD composition, and
   reaching-for-a-thing is a frame-internal proxy. `CLAUDE.md` carries the withdrawal.
   **`VOCABULARY_FROZEN.md` rested on the same clause and was retired; its twin was left
   standing.**
2. **IT BLOCKS BY MODULE NAME WHERE THE REAL LINE IS INPUT PROVENANCE.** Measured at module
   scope: `composer` reads only `docs/library-closure/ATOMS.md` (domain-agnostic, no board);
   `relations` reads no files; `detectors` and `observer` read a human replay **only under
   `if __name__ == "__main__"`**, so as libraries they touch nothing. **Only `mapping` imports
   `reverse_engineer` at module scope.**

> **WHAT MUST NOT MOVE: `KEY_BOUNDARY`.** `F134` — `reverse_engineer`, `*_human.ndjson`,
> `closure_keys`. **That is the real *never encode the answer* check and nothing here weakens
> it.** The proposal is to re-scope `CUE_BOUNDARY` by input provenance and **keep `mapping`
> blocked**; it is not to relax the firewall.

**Do not re-derive this.** Check the rule's premise against `CLAUDE.md`'s 2026-09-19
withdrawal first, then measure the module-scope reads again before changing a line.

## 7e. WHAT CHANGED AFTER THE HANDOVER WAS FIRST COMMITTED — 2026-10-05, AND THE QUEUE

**Everything below happened after `0246431`, so the earlier sections do not carry it.**

### DONE AND COMMITTED

    47e62b9  L1  THE FLOOR DRAW MOVED BELOW THE SEAM. `tether` no longer ranks action
                 names: it asks `Interface.undirected` and gets a `Realisation` back.
                 **Byte-identical BY CONSTRUCTION** -- 1,600 comparisons, 0 mismatches --
                 because the EXISTING coprime sweep moved rather than being rewritten.
    2f98779  L1  `Interface.moved_slots()` replaces the reach into `iface.table`. The
                 action key is now UNREACHABLE rather than merely unread. No-op today:
                 its one caller is behind `_DOWNRATE`, parked.
    e80e780  L3  THE LAYER SEAT, `conform/layers.py`, the 20th. See below.
    c01a5d1  L1  **`?ACTED` FLIPPED ON** -- the default is `"1"`.

### THE SEAM, AND WHAT "THE INTERCEPT" IS

**Isaiah's "the intercept" is `interface.py`** -- `Intent` / `Realisation` / `Capability` /
`Interface.realise`. The word appears nowhere in the repository; the thing was built at
`04ab502` on 2026-09-28, **the day of his ruling**. Not eroded since: three commits touch
both sides and all three cross in reasoning terms.

**THE LAYER RULE IS PER LAYER, NOT PER NAME, AND THAT WAS ISAIAH'S CORRECTION OF MY FIX.**
The old guard was a ruff ban naming `world.ACTIONS` -- the TOY world -- while `gridworld`
was uncovered. **I proposed extending the list; he refused it:** *"my leg isn't in one room
and I in another."* A rule that enumerates worlds protects only the worlds someone
remembered. **So the REASONING side is enumerated and everything else is environment-side by
default** -- a world nobody has written yet is already covered. Proof includes a world named
nowhere in the rule; the real tree is green at 0 crossings.

> **AND THE TRAP IN BUILDING IT: check TOP-LEVEL imports only.** Walking the whole AST flags
> `detectors`/`observer` importing `reverse_engineer` -- **the ANSWER KEY** -- which reads as
> a `KEY_BOUNDARY` breach and is not one: both are `__main__`-only. **An alarm nobody can
> reproduce teaches people to ignore the alarm.**

### AGENT-FIRST IS A WIRING JOB — THE AUDIT'S BEST FINDING

**At all four of Isaiah's sites the offer is ALREADY WRITTEN** -- decomposed into causes,
zero-initialised so a zero is legible -- **and nothing READS it.** `tether.py:5472` writes
`chose` / `instead_of` / `because` / `status` and then says of itself:
***"recorded as a CONFLICT I was in, not a decision I made: nothing read this before the
choice."*** **The remedy is a READER, not a rebuild.**

    (a) ATTEND   MEASURED AND BIMODAL. Agent-set focus (`focus_by_want`) is 30-43% of
                 cycles on `default` (seeds 0,1,2) and **ZERO on all six `click_only` /
                 `buttons` runs**. Pooled = 12.2% and describes NEITHER. So agency in
                 attention exists where there is an avatar and is absent in exactly the
                 worlds this week's chain is about.
    (b) BELIEVE  FOUR binding sites -- `tether.py` 6581 (mint) 6785 (reuse) 7346 (rebind)
                 7357 (refit). **Ties go to the FIRST candidate encountered**: every
                 comparison is STRICT (`btotal < best[0]`), so an equal later candidate
                 can never displace an earlier one.
    (c)/(d)      one gate, `_goal_choice` gate 1. Its refusal is decomposed four ways
                 (`too_short / flat / rose / qualified / arrived`) and nothing consumes it.

**THE READER, AS THE REVIEWER DESIGNED IT ON PAPER:** one reader for all four sites, not
four mechanisms. The agent ACCEPTS the computation's proposal or OVERRIDES it and records
which and why. **Start byte-identical** -- accept unless the agent has a reason in its own
evidence. **First override: when gate 1 refuses for a SUPPLY reason (`too_short`, `flat` --
*there was nothing to refuse*), the agent may plan anyway as a WAGER**, a routine adopted on
trial and judged by the ground. Bar reasons (`qualified`, `arrived`) stay.

### THE OPEN TENSION — SETTLE THIS BEFORE DESIGNING THE READER

**Two claims cannot both be true in the simple form.** The reviewer accepted that
`enumerate_routines` is reached zero times *because gate 1 exits every cycle*. **But
`focus_by_want` is 13 of 30 on `default`** -- if gate 1 exited every cycle everywhere, that
would be zero. Either

    (i)   gate 1 does NOT exit every cycle on `default`, and the zero-reach reading was
          generalised from a click world (the reviewer's own guess, which he told me to
          MEASURE rather than take), or
    (ii)  `focus_by_want` is set by a route that does not pass through gate 1 -- in which
          case two claims share one counter, which is `A6i`, and the counter gets split.

**It gates the reader because the first override is aimed at gate 1.** If (ii), the override
points at a site attention does not flow through -- `guard-the-site-that-carries-traffic`,
one design step earlier.

### KAGGLE — AND THE HEADLINE IS THAT THERE IS NO ENTRY POINT

**`kernel.py` exists only as `conform/kernel.py`, a conformance linter.** No `agent_main`, no
notebook, no harness-facing API. Against *complete and Kaggle-ready by 2026-10-12* the
submission form is **NOT**, not PARTLY.

    THE FORM, from ARC's own samples in `docs/example/`: subclass `agents.agent.Agent`;
    exactly TWO abstract methods, `is_done(frames, latest)` and
    `choose_action(frames, latest) -> GameAction`; `Agent.main()` OWNS the loop, capped by
    `MAX_ACTIONS` (base 80, sample overrides to 1,000,000). Packaging: ONE file into
    `agents/templates/`, wheels `--no-index`, gateway `http://gateway:8001/api/games`,
    submission a parquet (`row_id, game_id, end_of_game, score`).

**THE INVERSION IS CHEAPER THAN IT LOOKS:** `tether.py:7065` already exposes
`step(action=None)` and `arc_holdout.py:181` drives it one step at a time, so
`choose_action` has something to call. **Offline is the strongest column** -- every agent-path
import is standard library, no network anywhere on it. **The real constraint is one-file
packaging against ~70 modules.**

**THE PRIOR WORKING NOTEBOOKS ARE NOT ON THIS MACHINE.** Seven sibling repos searched
(Ouroboros, -Nexus, -Redux, tabula-rasa, ARC-AGI-3-Agents, Serendipity-Engine,
Ariadnes-Mirror-MCP): **zero notebooks, zero builders.** The scored submissions (0.08-0.22)
are real; they live on Kaggle under Isaiah's account. **The five known interface bugs remain
a checklist:** `is_done` must signal WIN; `choose_action` must RETURN `RESET` on `NOT_PLAYED`
and `GAME_OVER`, never twice consecutively; a click is `ACTION6` with `set_data(x, y)`;
`arcengine` must not be bundled with the framework import; the notebook needs the `arc-agi`
install cell.

### TWO FACTS THE ORIENTATION TEST ASKED FOR AND THIS FILE DID NOT CARRY

**Found by checking the test against the record rather than by being asked.** Both were
established on 2026-10-05 and both lived only in the channel or in code — which is the exact
hole `docs/ISAIAH_RULINGS.md` exists to close, reappearing in the handover itself.

**THE ACTION COUNT IS THE AGENT'S; THE ACTION NAMES ARE NOT.** The reviewer's ruling,
2026-10-05: **the reasoning side MAY hold the COUNT and pass the SET down; it may NOT CHOOSE
AMONG or COMPARE action NAMES.** Knowing *how many things I can do* is a fact about the
world's affordances and is reasoning-side by right; knowing *which button is called what* is
the interface's. **And the count is load-bearing, not a convenience:** `tether.py:5180` and
`5378` derive the bargain's priced alphabet from `len(self.actions)`, so removing it would
move the price of every term. That is why `self.actions` STAYS after the seam fixes, and why
the four name-level readers are classified separately (5694, 3945, 4305 convert; 5508 is the
routine item).

**`OR` — WHERE DISJUNCTION LIVES TODAY.** `OPERATORS.md` defines `∥` as **disjunction**:
*either suffices; not both required*, with the test *remove one — does it still work?*

    in TERMS      NO. `BONDS = 1` (`tether.py`, ~311): one of the seven bonds has a form in
                  PREDICT, so **terms are chains**. The price is general (`log2(|bonds|)`),
                  the implementation is one.
    in GUARDS     YES, and it is built. `condition.py:158` parses `or` into
                  `Bool("or", ...)`; `Not`, three-valued evaluation and `Call` are there too.
                  `tether.py:4638` `_compound_guards` builds them and `routine._guard_excess`
                  prices a compound to sort AFTER the plain guard it extends.
    in ROUTINES   via guards, through `When` / `Until`, which take a guard.

> **SO `acted_on(o0) or acted_on(o1)` IS ALREADY EXPRESSIBLE** — and I claimed the opposite
> earlier in the week, having grepped class names, found none called `Or`, and read the
> capability off the NAME. The reviewer had approved a build on that false premise. **It is
> recorded here because the next session will meet the same question**, and because *a map
> entry saying a thing does not exist is worse than one saying it is unfinished.*

### THE QUEUE FOR THE NEXT SESSION, ORDERED

    1  settle the (i)/(ii) tension -- per world per seed: gate 1 exits vs passes, and
       whether every `focus_by_want` increment passes through gate 1
    2  the three approved seam CONVERSIONS: `tether.py` 5694 (level-change diff -> an
       upward Capability report), 3945 (coverage -> `Interface.capability()`), 4305
       (**key on the `_intent` ALREADY in every trace row -- no new plumbing, F438**)
    3  Kaggle a-e verdicts and the smallest step to an entry point
    4  the seven-bond table: per bond, executable? in terms / guards / routines.
       Measured so far: **`BONDS = 1`** (`tether.py`, ~311) -- terms are chains
    5  THE READER, aimed at whichever site the settlement shows attention and planning
       actually flow through
    6  **THE ROUTINE ITEM -- ALREADY RULED, NOT AWAITING ISAIAH.** `routine.py:533` builds
       `[Act(a) for a in actions]`, so ROUTINE STEPS HOLD BARE ACTION NAMES -- *store
       intents and plans with their meaning, not raw actions* (Isaiah, 2026-09-28), which
       **decides the direction**. **I filed this as "Isaiah's call" and was corrected: the
       ruling exists, so what is open is the ORDER, not the question.** Depends on item 1,
       because (a) cannot be read until the gate-1 tension is settled:
         (a) read WHY adoption is 0 of 145 -- gate refuses vs never reached
         (b) routines as INTENTS, on paper first: the existing verbs plus referents and the
             undirected want, realised by the interface AT EXECUTION, priced BY KIND
         (c) keep the bare-string branch for FIXTURES ONLY, with a production assertion
         then build.
       **Occasions today: ZERO**, since adoption is 0 of 145 -- so nothing is acting on the
       breach, and it goes live the moment adoption is fixed.

### THE FEATURE WORK — ITEMS 7 ONWARD, WHICH THE OCTOBER 12 SPRINT DEPENDS ON

**Appended 2026-10-05 at the reviewer's instruction, and the defect is worth naming: the
six items above all came out of ONE DAY'S AUDIT, so the queue had quietly become that
day's list.** Everything the handover-plan doc carried and section 7e did not is here.
**Dependencies are stated per item; where there is none, it says so.**

    7   THE PER-REFERENT OFFER FIX, then its two consequences, in this order:
        (a) the fix itself -- no dependency
        (b) the read of WHY PRESSES STEER AWAY FROM THE CAUSE -- needs (a)
        (c) the exploration build against the 7-press line: failure records and the
            per-slot rung -- needs (b), because what to explore FOR is what (b) finds
        **AND THE CAUTION IS THIS FILE'S OWN SECTION 7: the offer fix was filed from
        SEED 6, which is the n=1 trap named there.** A population selected by the defect
        cannot diagnose the defect. **Re-measure on seeds 0, 1, 2 before building on it**
        -- not a reason to drop the item, a reason not to inherit its scope.
    8   `or` WIRED INTO THE MINT for TWO-CAUSE slots. No dependency on 7.
        **The guard machinery EXISTS** -- `condition.py:158` parses it,
        `_compound_guards` builds it, `routine._guard_excess` prices it -- so this is a
        MINT-side wire and not a build. See the `or` entry above.
    9   GOAL FORMATION IN CLICK WORLDS on the jigsaw paradigm, and SET-ASIDE GOALS
        (section 7b: PAPER, no symbol in the tree). **Depends on items 1 and 5** -- click
        worlds are exactly where `focus_by_want` reads ZERO, so this is the capability
        the reader is being built to reach.
    10  THE AGENCY RESET ON BELIEF WITHDRAWAL (the mode switch). Section 7b has it as
        PAPER -- no `reset`/`withdraw` symbol in `instruments.py` -- and **its fixture
        already exists**, `test_gate.py:296`. No dependency.
    11  THE `CUE_BOUNDARY` RE-SCOPE (section 7d), then THE VOCABULARY BRIDGE to the
        ~2,700 atoms. **The bridge needs the re-scope; the re-scope needs nothing.**
        `KEY_BOUNDARY` does not move, and `mapping` stays blocked.
    12  METAPROGRAMMING -- THE GENERATORS (section 0.5): the condition compiler, the bond
        combinators, the recipe compiler, built LAZILY on demand. Two parts:
        (a) the 2,638 PROSE CONDITIONS turned into precise groundings. **I draft them and
            Isaiah rules ONLY THE UNCERTAIN ONES** -- his 2026-09-23 ruling, and the
            division is the point: drafting is the seat's, adjudicating the doubtful ones
            is his
        (b) sorting library entries into PARTS vs AGENT FUNCTIONALITY (meaning, belief)
        **Depends on 11**: generators over a vocabulary the agent cannot reach have
        nothing to generate.
    13  RANK-BASED REFERENT NAMING · IMPORTS IN THE GRAMMAR · OPERAND TRANSFER (section
        7b: no `operand_transfer` symbol anywhere in the tree) · **`F408`, INTENT-GUARD
        PRICING, which is OPEN**: a guarded term is strictly more specific than its
        unguarded form whatever the guard, so the free ride is wrong in principle --
        and repricing every guard broke 6 of 29 M2 checks. **It needs its own
        pre-registration and has never had one.**
    14  KAGGLE, in two parts, and only the second is gated:
        (a) THE ENTRY-POINT BUILD -- an `Agent` subclass calling `tether.step`, one-file
            packaging against ~70 modules, and the five known interface bugs.
            **OFFLINE, needs no real board, so it may proceed EARLY** (Isaiah,
            2026-10-05). Item 3 is its only predecessor.
        (b) ONE INTEGRATION RUN against the real ARC harness. **RULED BY ISAIAH
            2026-10-05 AND NO LONGER AWAITING HIM.** *"That can be allowed only after we
            fix the issues with the agent and before it's Kaggle-ready."* So: **ALLOWED,
            but ONLY AFTER the agent's issues in this queue are fixed, and as the LAST
            STEP before declaring Kaggle-ready.** It goes at the END, after the feature
            work, never earlier. **Its conditions bind: a RANDOM choice of board;
            results used ONLY to confirm the agent runs end to end -- load, step, RESET
            handling, WIN signalling, clicks, time budget; and NOTHING tuned toward any
            board. The board stop otherwise stays live.**
    15  HOUSEKEEPING: `3dembedding` and `temperature` commented out;
        `probabilityDistribution` and `aboutness` removed. **CONFIRM each against the
        tree before acting** -- this line is inherited and nobody has re-read it, which
        is the standing question *is it actually reached* pointed at a to-do list.

**NOTHING IN 7-15 IS STARTED THIS SESSION. Isaiah, 2026-10-05: all of it -- the feature
items, the Kaggle entry-point build and the integration run -- happens AFTER the context
clear, in the next session.** This session does the documentation fixes, the commit, the
copies, the index and READY, and nothing else is built or measured.

**AND THE LESSON THE WHOLE DAY PAID FOR, WHICH IS THE ONE TO CARRY:** **five instructions
were refuted by READING THE SITE BEFORE CHANGING IT** -- extend the ban list · route through
`ELICIT` · "a uniform draw" · swap the pick at the call site · walk the whole AST. **Not one
would have failed a test. Two would have passed a measurement written specifically to catch
a regression. One would have accused the answer-key firewall of a breach it did not commit.**

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

---

## APPENDIX A — CORRECTIONS TO SECTION 0, WITH THE OVERTURNED ENTRIES KEPT

**Moved here 2026-10-05 at the reviewer's instruction.** It was in the middle of section 0,
which put withdrawn claims in front of a fresh session before the rulings they were
withdrawn in favour of.

### WHAT I CHANGED IN THE REVIEWER'S DRAFT, AND WHY

The instruction was to check each point against `THE_MISSION`, `CLAUDE.md` and the corpus,
correct what was wrong, and say what changed. Five changes:

**(a) `THE_MISSION_north_star.md` WAS NOT IN THIS REPOSITORY, so point 1 could not be checked
against it — AND ISAIAH RULED ALL THREE IN THE SAME DAY. They are now at
`docs/THE_MISSION_north_star.md`, `docs/THE_ALIGNMENT.md` and
`docs/THE_TERMINAL_CONDITION.md`, copied BYTE-FOR-BYTE from `Ouroboros-Redux` and entered as
CORPUS** — read-only, annotated in `INDEX.md`, never edited. **Reconstruction from the
citations was explicitly forbidden and would have been the worst available option**: a corpus
rebuilt from the documents that quote it is two mirrors, which is exactly the property the
edit boundary exists to preserve. The finding as originally written: `CLAUDE.md`'s PROCTOR RULES open by naming three files *carried from
`Ouroboros-Redux`* — `THE_MISSION_north_star.md`, `THE_ALIGNMENT.md`,
`THE_TERMINAL_CONDITION.md` — and **none of the three is present.** Seven documents cite
`THE_MISSION` by name. **A fresh session told to check something against it will hunt for a
file that does not exist here.** The authority for §0.1 in THIS repository is `CLAUDE.md`'s
own *THE JOB* and *THE TERMINAL CONDITION* sections, and that is what §0.1 is derived from.

**(b) THE DRAFT'S CHARACTERISATION OF THE TWO GAME SETS IS REMOVED, AND THIS IS THE ONE THAT
MATTERED.** The draft read: *the public set is a biased slice (mostly navigate and collect;
the private set leans formal and rule-based).* **It is not in the record** — I searched for
it and found no such characterisation — **and more importantly it is a SKILL MAP, which
`CLAUDE.md` hard-rules:**

> *The skill map is a reading, never an input. Which games need which skill is taken from
> the ledger AFTERWARDS. **The moment it is available beforehand the mechanism has been
> handed its answer** — `act` arrived knowing what each action does; a skill map would
> arrive knowing what each game requires. Same failure, one level up.*

**Putting a per-skill characterisation of the two sets at the top of the first file a new
session reads is putting the skill map one step from being an input** — and it would arrive
wearing the authority of an orientation. **The direction it was trying to express survives
without it** (§0.1: generalise to a set we never see), and the fact that *does* bind is a
fact about the harness rather than about skills: **Kaggle never shows us the games, one
submission a day, a scalar back.**

**(c) — OVERTURNED BY THE REVIEWER, 2026-10-05, AND THE JIGSAW IS RESTORED IN §0.4.
*jigsaw* IS ISAIAH'S OWN RULING OF 2026-10-03, POSTED IN THE DRIVE CHANNEL.** My search
covered `INDEX` and not the channel, so the null was a reading of the wrong closure — **an
abstention counts only when it names the closure it searched, and I named one I had not
searched.** The original entry, left standing as the evidence:

**(c) THE "JIGSAW" FRAMING IS REMOVED; "NO AVATAR" IS KEPT.** *The player is outside the
board, working it like a jigsaw* returns **nothing** in the record. **"No avatar" is in the
record repeatedly and is load-bearing** — including as the night's one recorded contact
change — so §0.4 states the capability and drops the simile. A vivid image that is not in
the record will be quoted back as if it were.

**(d) — OVERTURNED THE SAME WAY, 2026-10-05: THE CONDITIONS ARE ISAIAH'S RULING OF
2026-09-29** and §0.3 now states them as his. **Same cause as (c), and that is what makes it
a class rather than a slip** — two nulls in one document, both from searching `INDEX` for
something that only ever lived in the channel. The original entry:

**(d) THE ARC-REOPENING CONDITIONS ARE MARKED AS THE REVIEWER'S, NOT VERIFIED.** I could not
find the *randomised way to choose boards* clause in `INDEX`. It is attributed in §0.3
rather than asserted — the same convention used for corrections (d) and (e) in the first
pass, where the column says which claims I verified from code and which are the reviewer's
label.

**(e) "PHASE 2" IS TWO DIFFERENT THINGS IN THE RECORD, AND THAT IS AN `A6i` COLLISION.**
`INDEX` carries both *Phase 2 (held-out): arc-interactive's 249 games* and *Phase 2 (guide
harvest): GameFAQs retro walkthroughs*. §0.3 means **the second**. `A6i` is this project's
named unlintable failure — *two legitimate quantities under one word is well-formed code,
well-formed docs and a well-formed measurement* — and the moment to record it is while
nothing is wrong, which is now.

**WHAT I DID NOT CHANGE:** points 2 and 6 are correct as drafted and are reproduced in
substance above. The 2,700 figure and the measured 14 are both in the record and were
checked.
