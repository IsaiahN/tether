# ISAIAH'S STANDING RULINGS

**Source: the reviewer's record of Isaiah's rulings, posted to the channel 2026-10-05.**

**WHY THIS FILE EXISTS, AND IT IS A CORRECTION TO A MISTAKE I MADE THE SAME DAY.** Many of
these rulings exist **only in the Drive channel and the reviewer's notes, not in `INDEX`**.
On 2026-10-05 I searched `INDEX` for *jigsaw* and for the ARC-reopening conditions, found
nothing, and reported both as unverified — **and both are Isaiah's, ruled and posted.**

> **THE RECORD IS `docs/INDEX.md` + THE DRIVE CHANNEL + THIS FILE. NOT `INDEX` ALONE.**
> That is `I26`'s scope error one widening further: `*.py` → `docs/` → the seats and the
> import graph → **and now the channel**, which is the only one of the four that is not in
> the repository at all and therefore the only one a grep can never reach.

**Keep this file current.** A ruling that reaches the seat through the channel is written
here in the same session it arrives, or the next search for it fails the same way.

---

## 2026-09-28

- **Reasoning is divorced from actions:** Systems 0/1/2 reason in **intents** (expressed in
  the existing NSM-style grammar), and an action interface translates intents to actions.
  The interface also reports **in reasoning terms** what actions do and when that changes
  ("you can now click freely"), never in action terms.
- **System 0 is always on, never holds the wheel;** it finds contacts/relations and
  characterises what actions do (repeatable, cyclic, count-limited, one-time switch, wall).
  **An avatar is not required** — `RELATIONS.md` is about interactions.
- Store **intents and plans with their meaning**, not raw actions.
- Grammatical classes may carry different weights; ALL vs SOME by implicit counting; **bond
  sufficiency is decided by the board**; compositions are the agent's discretion.
- **ARC games are STOPPED** because the work drifted toward those games; **the real test uses
  none of them.** After the agent is built and tested, Phase 2 widens gridworld/priors to
  other game families.

## 2026-09-29

- A goal **met then unmet** is data about the actions that undid it. Whether exploration may
  disturb a met goal is **the agent's decision**, recorded so it can backtrack.
- RESET/undo are ungated in the interface, but it must **NEVER issue RESET,RESET
  consecutively** (that restarts the whole game).
- **Guards name intents, not buttons.** Intent-level prediction (before, intent, after): yes.
  **Pricing counts intents by KIND.**
- **Nomenclature:** proximity = closeness; distance = length of the unobstructed path;
  position = where something is relative to you.
- **ARC BOARD STOP — LIFTING CONDITIONS. Isaiah says when**; prerequisites are **(a) the agent
  complete** and **(b) a measured way to automate/randomise which boards are shown so the
  proctor cannot build toward specific boards**, likely with a freeze. **Notes and ideas about
  ARC go through the reviewer and Isaiah first.** Before ARC reopens he wants more priors
  trained outside the game distribution (walkthroughs + images of retro games).
- Checks that **could not run count as passing for now** but are regression-tested once ARC
  boards return.
- Store **what the agent did AND why**, with the board state that prompted it.
- **Routines decay only on tried-and-failed, never from disuse.** Intent-keyed guarded terms
  carry across games as **soft schemas**, losing standing only on use failure; how hard a
  failure counts and when it is forgiven is **the agent's call**, so it must be able to bring
  demoted ones back. Same for subroutines.
- Rules awaiting confirmation **survive level changes only under similar conditions**
  (dormant, re-eligible when the conditions recur).
- **Carried rules are surfaced by likelihood of working** (pattern similarity + track record),
  **not by a price discount**; never thrown away because one board lacked the mechanic.
- **Mispredictions on trial and failures after settling are two separate records**; one
  failure is not a verdict, across levels as across games.
- **Phase 2 game list:** the NES Walkthrough Index (50 games, three tiers). Guide sources:
  StrategyWiki first, then GameFAQs, then alternatives, case by case.

## 2026-09-30

- **Commits require full green;** a persistently failing check goes to the reviewer, **never
  bypassed**.
- `WHAT_THE_AGENT_SEES` was the original concept; **its language must never be used to limit,
  block or revert the agent.**
- The agent **may downrate a goal-scope member** from its own evidence that nothing moves it;
  when every member looks inert, **downrating steps aside** and the goal counts normally.

## 2026-10-01

- **Downrating's default stays OFF until ARC-style boards (PARKED).**
- **Click-only worlds have cause and effect** (one object acting as a button for another);
  seeking object-to-object relations is a missing feature for avatar and click-only games
  alike — **extend the existing machinery, do not duplicate it.**
- **Nothing in the agent or library may depend on game IDs;** the one decision that read them
  moved to session provenance, **on condition that it stays provable where everything in the
  library came from.**
- The agent may **SET ASIDE** a goal it has never been able to affect — **not drop it** — and
  when to revisit is its own decision.
- **Rule adoption:** value understanding for its own sake and make cause-and-effect rules
  cheaper to adopt. *A living being prices decisions only when dealing with actual currency;
  most decisions are weighed as value of understanding and predicted outcome.* (Measured
  afterwards: **the bargain already prices the slot's own unexplained residual, so no separate
  term was built.**)
- **The protection against wrong rules is settled vs unsettled, revisable by experience — not
  price.** Settled/unsettled is a **graduated spectrum that tips over**.
- **STANDING AGENCY DIRECTIVE: nearly every question about how the agent functions is the
  agent's own decision from its evidence.** Exceptions that go to Isaiah: **anything that would
  encode an answer; ARC boards and the board stop; provenance (learned vs carried); the corpus
  and its rulings; data sources and what is published.**
- **Phase 2:** archived copies (Wayback / search indexes) allowed; **human replays are the real
  need** (walkthroughs + images + maps are the data-lite version); **test viability on ONE game
  first** — if not viable, ARC then a Phase 3 that reverse-engineers the priors games require
  and simulates them on boards. **The answer key comes only from fetched, cited guide text,
  never from model knowledge.** Game names are aliased in repo data; the walkthrough data lives
  outside the project; **no licence commentary in any repo file.**

## 2026-10-03

- **Click-only / non-avatar games: the player is OUTSIDE the board** (bird's-eye, working
  buttons and levers), **not a piece in it**; the purpose on every board is to win the level.
  **Treat it as a JIGSAW PUZZLE, not a map:** hold a fuzzy picture of where things go, made
  concrete by filling gaps, pattern-matching and verifying in a loop, **faster as pieces
  settle.** Goal formation is designed on that paradigm (root goal = win; candidate end-states
  held as unsettled hypotheses; the gap points to levers; track record crosses games).
- **Build the metaprogramming** (lazy generators making library entries executable), with the
  jigsaw paradigm designed in parallel.

## 2026-10-04

- **"Composition is inherent to agency" — composition is always on.** `_INVENT` is "bootleg
  composition": **RETIRED, not repaired.**
- **Imports only after a real search failed, the change has recurred, and no existing atom
  already expresses it** — and new knowledge is stored **IN THE GRAMMAR**, never a side system
  such as lookup tables.
- **There is ONE reviewer.** Isaiah sometimes talks to the seat directly and **always tells the
  reviewer.**

## 2026-10-05

- **AGENCY IS PARAMOUNT — restated and made the first entry of the record, 2026-10-05.**
  **The agent is the driving force behind every decision, never a pilot inside machinery that
  decides for it.** It is a recursively self-improving agent and must be allowed to **GROW**
  and **DECIDE ON ITS OWN**: composing its own programs in its grammar, minting and importing
  what it lacks, deciding from its own evidence and **recording why**. **We supply the MEANS —
  offers, evidence, instruments, the ground that judges — and never the MEANING.** Default
  answer on any question about how the agent functions: *let the agent decide, and record its
  reason*. **Every stop-gap that decides for it is temporary and is to be converted.**
  Continuous with 2026-09-23 (agent-first, not a mech suit) and 2026-10-01 (the standing
  agency directive); the exceptions are that directive's list, above.
- **`?ACTED` ON by default**, on the settled/unsettled principle (**supersedes the earlier
  zero-failure bar**). **FLIPPED 2026-10-05**, `tether.py` default now `"1"`. **The warrant is
  the ruling, not the per-seed test:** at the flip all six world-seeds read INSUFFICIENT and
  only the pooled fallback passed (guarded 3/7 vs unguarded 0/2).
- Before any context clear: **a code-level handover, updated instructions and memory, full
  copies for the reviewer, a big-picture section first, and an orientation test.**
- **THE DEADLINE: the ARC Prize 2026 FINAL SUBMISSION DEADLINE is NOVEMBER 2, 2026.** It is in
  the big picture because **it is the clock every priority is set against.**
- **THE TIMELINE: the agent COMPLETE and KAGGLE-READY by 2026-10-12**, then ~1–2 weeks to get
  PRIVATE (OOD) results back from Kaggle and to strengthen the agent with more human-replay
  prior training (the Phase 2 walkthrough work). **It is a FEATURE sprint, not readiness-only**
  — the queued features are in scope, ordered by dependency, with Kaggle readiness alongside
  rather than after.
- **NO STOPPING FOR TIME-OF-DAY REASONS, EVER.** Neither the seat nor the reviewer stops "for
  the night" or because a session feels long. **The only legitimate stops are a genuine blocker
  needing a ruling — post it and keep working on anything independent — or a context clear
  Isaiah has scheduled.** Real `date` is for timestamps only, never a reason.
- **AND DROP DURATION ESTIMATES.** Report size as what is involved — files, sites, checks —
  never in days or sessions. Our sense of elapsed time is unreliable and the work runs faster
  than either of us estimates.
- **"THE INTERCEPT" IS ISAIAH'S NAME FOR `interface.py`**, recorded here 2026-10-05 so the next
  search does not cost what this one did. The repository has **never** used that word: a
  case-insensitive grep of project code, `INDEX` and the whole commit log returns nothing.
  What he is remembering is real and was **built at `04ab502` on 2026-09-28, the day of his own
  ruling** — commit subject *"the action interface's UPWARD half"*. Its parts are
  `Intent` · `Realisation` · `Capability` · `Interface.realise()` (intent → action, the
  downward half) · `Interface.capability()` (the report upward).
- **`THE_MISSION_north_star.md`, `THE_ALIGNMENT.md` and `THE_TERMINAL_CONDITION.md` go INTO
  this repository**, copied byte-for-byte from `Ouroboros-Redux` and **never reconstructed from
  memory or from citations.** They enter as **CORPUS** — read-only under the edit-boundary
  rule, annotated in `INDEX.md`, never edited. Done 2026-10-05; see `docs/` and the
  edit-boundary table in `CLAUDE.md`.
