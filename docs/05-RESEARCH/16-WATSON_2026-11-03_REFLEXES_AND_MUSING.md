# WATSON 2026-11-03: reflexes, habits and musing

Reviewer, 2026-11-03 ~14:55 CST. A helper ran this under the tether-watson procedure. The reviewer spot-checked the figure quotes against docs/FIGURES_TEXT.md. This is a read-only review; no code was changed.

## QUESTION

Isaiah, 14:29: "habit is the wrong word, its closer to reflexes. the the reflex to dodge ... you can compose them via the grammar and the atoms so that the agent has them loaded in cache by default ... (not really deletable or always settled as part of umwelt)?"

On musing: "an ability of the agent, but it chooses when to do that, and what to muse on ... if thought to be important should be acted on or remembered in cache ... and if proven effective stored longterm right?"

## DOMAIN CENSUS

R has three parts: the trigger reading, the response intent, and the deliberation that may inhibit it.
- It is asymmetric. The reflex fires first, and only deliberation can inhibit it, never the other way round.
- It runs on several scales:
  - frame: the reflex;
  - step: deliberation;
  - level or game: adaptation;
  - lineage: the innate core;
  - quiet steps: musing.

| Domain | Actors | Currency | Anchor |
|---|---|---|---|
| D1 Reflex tier (umwelt) | settled atoms composed as When(reading, Act(intent)) | presses made without deliberation | the next frame |
| D2 Adaptation (habituation, sensitization) | per-kind counts | share of firings that paid | board outcomes; it changes reach, never the record |
| D3 Deliberation and inhibition | route, mint, plan | evaluations | the step |
| D4 Musing (a chosen offline ability) | _muse, parked residuals, settled methods | evaluations on quiet steps | the board, only through a later test press |

Two overlaps matter:
- D1∩D3 is inhibition. There is one press per step, which is Sherrington's "final common path".
- D4∩D1 is how a habit forms: a settled muse finding can join the fast tier.

Order (Fig 3): perception, then reflex, then deliberation, then muse and carry.

## TETHER (primary, verbatim)

**D1. What a reflex is and how it is built**
- Fig 12 :104 "A settled molecule becomes an atom for whatever composes over it." A reflex is a settled composition used as one unit.
- Fig 12 :107-110 "where the arrangement is recorded, re-deriving it is a lookup and the actions were spent once ... Inside a run the arrangement persists and nothing is re-earned." This is the "loaded in cache by default".
- Fig 12 :112 "A plan is a sequence. A goal is a comparison. Progress is a subtraction." A reflex is a comparison guarding an act.
- Fig 4 :11 "a head start, never a recording". Innate reflexes may be loaded as head starts. They must be methods keyed by kind and relation, never press logs.
- Fig 9 :29 "matching is a one-pass check, not a search". The reflex check before deliberation is a one-pass match.
- Fig 11 :40 "An improvement that does not change contact changes nothing." This is what justifies reflexes: presses made without deliberation raise contact.

**D2. Fixed or adaptive**
- Fig 6 :42 "What is recorded only grows. What is reachable is derived, and it can fall." "Not deletable" is right for the record. The standing to fire, which is reach, can fall.
- Fig 5 :55 "Nothing leaves the library. What falls is the reach."
- Fig 11 :49-51 "An actor's valence is relative to the residual, not a property it carries ... No standing list of good actors survives a change of residual." A reflex may NOT hard-wire "kind X is dangerous". The trigger must be relational, such as "approaching me" or "a life lost".
- Fig 9 :41 "keep every cut ranked and reversible." A habituated reflex is gated, never removed.

**D3. Override**
- Fig 9 :60 "Use filters for the budget and witnesses for the verdict. Never let a filter hand you a verdict." Deliberation may override a reflex only with a witness, meaning a reading.
- Fig 2 :42 "Buy independence in proportion to the cost of being wrong." A false dodge costs one press; a missed dodge costs a life. So hazard reflexes fire on thin evidence.

**D4. Musing**
- When:
  - Fig 5 :15-16 "the curiosity drive / fires when nothing is scoring".
  - Fig 9 :53 "Nobody chooses. The gap does". "The agent chooses" means its own reading chooses, with no governor above it.
- What to muse on:
  - Fig 7 :40 "The room is summoned by the residual rather than composed".
  - Fig 5 :18: it "seeks the gap that is large and compressible".
- The ladder:
  - Fig 1 :27 "A frame cannot score itself with a quantity it also produces." So a muse finding is only a candidate.
  - Fig 12 :126 "Actions price finding out whether it holds." The candidate becomes a test press.
  - Fig 5 :70 "A term is settled when the ground pays for it."
  - Fig 4 :8-9 "a method that can be reapplied / verified, and compressed to its essentials". This is long-term storage.
  - Fig 5 :53: a refuted term is owed a refusal, so failures are stored long-term too.

**Strength:** triangulated across Figs 4, 5, 6, 9, 11 and 12.

**Gaps for Isaiah:**
- No figure names "reflex" or "freezing". The reflex tier is derived from Fig 12 :104 and :107-110 and from Fig 4 :11.
- Whether ARC-AGI-3 games offer a no-op, which freezing would need, is a fact about the habitat.

## WORLD (secondary; each source read)

- **Sherrington 1906, *The Integrative Action of the Nervous System*.**
  - "The main secret of nervous co-ordination lies evidently in the compounding of reflexes."
  - "Antagonistic reflexes interfere, one reflex deferring, interrupting, or cutting short another."
  - Excitability "varies much under various circumstances."
  - Reflexes are compositions that compete for one output; the arc persists while its strength varies. Corroborates D1–D3.
- **Sokolov's orienting reflex** (via Rust 1976, a secondary witness).
  - A comparator checks incoming input "against a library of images of past stimulation"; novelty triggers orienting.
  - Habituation is a change in that comparator.
  - The trigger is a prediction mismatch, which is the agent's surprise. Corroborates.
- **Habituation and sensitization** (Rankin et al. 2009; Schmid, Wilson & Rankin 2015).
  - Habituation is stimulus-specific and recovers with time.
  - Sensitization is a separate, incremental process.
  - Two independent counts; the reflex is gated, never lost. Corroborates D2.
- **Aplysia (Kandel's work, via Hedges, U Iowa).**
  - A fast, modifiable trace forms first.
  - Long-term change needs new gene expression after repetition.
  - Corroborates the candidate → settled ladder.
- **Yilmaz & Meister 2013, *Current Biology*.**
  - Looming "reliably triggered one of two behaviors: escape or freezing", some in under 250 ms, on "the animal's very first exposure".
  - The response is innate and relational: it is triggered by looming, not by a kind of object. Corroborates Fig 11 :49-51.
- **Primitive reflexes (Modrell, *StatPearls*).**
  - They are "eventually inhibited" in infancy and "may return" with disease.
  - Inhibited, not deleted. Corroborates Fig 6 :42.
- **Brooks 1986, subsumption architecture.**
  - "Higher-level layers can subsume the roles of lower levels by suppressing their outputs."
  - Level 0 is "Avoid contact with objects".
  - Corroborates override by suppression.
  - PARTIAL CONFLICT: Brooks's layers don't adapt. The figures stand: the form is fixed and the reach adapts.
- **Evans & Stanovich 2013 (dual process).**
  - Type 1 is defined by autonomy and covers both innate modules and practised automaticity.
  - Deliberation intervenes on "intuitive default responses".
  - Reflexes and habits share one fast tier. Corroborates.
- **Mason et al. 2007, *Science*.**
  - Mind-wandering rises during practised, quiet blocks: "a psychological baseline that emerges when the brain is otherwise unoccupied".
  - Muse when quiet. Corroborates.
- **Mattar & Daw 2018, *Nature Neuroscience*.**
  - Which memory to replay is set by gain (the expected improvement) × need (how often that state will recur).
  - Muse on the parked gap with the largest gain × need. Corroborates Fig 7 :40 and Fig 5 :18.
- **Wilhelm et al. 2011, *J Neurosci*.**
  - Sleep preferentially consolidates memories relevant to future behaviour.
  - Keep what will be needed. Corroborates.

## VERDICT (from the figures)

1. **Definitions**
   - A **reflex** is a settled composition of innate atoms, shaped When(relational reading, Act(intent)). It is held as a recorded arrangement, so firing it is a lookup.
   - A **habit** has the same shape but became settled through play (a LEARNED term). It sits in the same tier with a different provenance. gamma.py already separates INNATE from LEARNED (:377-385).
   - **Musing** is a chosen computation, run when the agent's own reading says nothing is owed.
   - Isaiah's "reflex, not habit" stands. The figures add learned habits to the same fast tier.

2. **Fixed or adaptive: both, on two different quantities**
   - Never deleted: the record, the atoms and the reflex form. Innate terms are never demoted (gamma.py :1371-1378).
   - Adapts: whom the reflex fires for, and how strongly.
     - Habituation is a recorded, stimulus-specific gate.
     - Sensitization raises priority after harm.
     - Both are ranked and reversible.
   - Hard-wiring a valence ("kind X is a threat") is ruled out by Fig 11 :51.

3. **Override:** allowed only on a witness (Fig 9 :60). Hazard reflexes fire on thin evidence (Fig 2 :42).

4. **Isaiah's musing ladder is CONFIRMED, with three corrections**
   - (a) "If thought to be important": importance is never the muse's own score (Fig 1 :27). What it finds is a candidate.
   - (b) "Acted on or remembered in cache": it must be ACTED on. When its slot kind is on the board, the candidate becomes a test press (Fig 12 :126). Remembering it alone buys nothing.
   - (c) "Proven effective → stored long-term": yes, when the BOARD pays (Fig 5 :70). Proven failures are stored too, as refusals (Fig 5 :53). Nothing is deleted.

**Cost if wrong:**
- A wrong reflex press costs one action.
- A badly gated reflex could pre-empt goal presses, which would show up as dithering.
- Musing costs quiet-step evaluations, which MUSE_BOUND already caps.

**Undoable:** yes. One switch per reflex, plus one for the muse-to-test link; with them OFF, behaviour is byte-equal to today.

**Reversed by:**
- the dodge reflex is ON and deaths per press do not fall on games with chasers;
- reflex presses raise contact but reached goals and levels do not change;
- tests derived from muse findings settle no more often than ordinary candidates;
- a figure line that makes valence a property of a kind.

## Candidate reflexes, and what exists today (development 053ace1)

| Reflex | Trigger (agent's own readings) | Response (intent) | Fixed / adaptive | Exists today? |
|---|---|---|---|---|
| Orienting | outstanding surprise on an object's slot; an object appears or vanishes | focus on or probe that object | habituates per kind; recovers on change | partial: SURPRISE_NOMINATES biases goal choice *after* deliberation and does not pre-empt it |
| Avoid / dodge (looming) | a world-caused object (via reafference) whose distance to the avatar is shrinking | increase the distance or leave its path | the form is fixed; priority sensitizes on deaths and habituates when approaches are harmless | the atoms exist (Approach, Avoid, toward/away); there is no reflex. DEATH_VOTE is avoidance learned after a death, by press kind |
| Startle / interrupt | a large out-of-range miss, a lost life, a level reset | drop the held routine or plan and re-perceive | habituates | no; the pre-emption slot `_urgent` returns False |
| Freeze | a hazard approaching and no "away" route known | press something that leaves the avatar unchanged, if the limb knows one | adaptive | no |
| Track / pursue | an object moving on its own; the goal kind moving | keep its identity; move toward it if it is the goal | tracking is fixed; pursuit adapts | tracking yes; pursuit only through goal choice |
| Contact (circular reaction) | an untried action or an untouched kind | press it | a fixed drive, ending when the board is covered | yes, as System 0's drive, but it still runs *after* the step's full lookup and mint |
| Habituation (modifier) | a change that comes with every press, the same way each time | stop steering by it | adaptive, recorded | yes (DISCRIMINATE_STEER; CONTACT_FIRST (b); the muse's "unchanged since" check) |
| Sensitization (modifier) | a death in this kind of situation | raise avoidance priority for that kind | adaptive; read as a share, so it decays | yes, in DEATH_VOTE's weighting |

**Overall:** the agent has the atoms for every one of these reflexes and some of the adaptation logic. It has no tier that fires before deliberation. `_urgent` was declared for exactly this and was never fed.

## DESIGN

### The reflex tier

1. **Composition.** Each reflex is a routine When(guard, Act(intent)), using routine.py's existing When.
   - The guard uses only settled relational atoms: approach, avoid, surprise, life count.
   - The intent is a limb intent; the limb picks the press.
2. **Caching.** A small list of these recorded arrangements.
   - Innate ones are loaded at birth as head starts.
   - Habits are added when LEARNED terms settle in play.
   - It is checked as a one-pass match right after perceiving, before route and mint.
3. **Settled-ness.** Innate reflex forms are never demoted or deleted.
   - Each reflex keeps two per-kind, per-game counts: habituation (it fired and nothing followed) and sensitization (harm followed, or firing kept a life).
   - Together these set whether it fires for a kind. They are stimulus-specific, recover on change, and nothing is erased.
4. **Override (inhibition).** When a reflex matches, its press is the default.
   - Deliberation may replace it only with a witness: a settled prediction that the press hurts the goal.
   - Every override is recorded.
   - A hazard reflex is never inhibited by a budget filter.
   - The danger reflex's state feeds `_urgent`.

### Musing as a chosen ability

- **When:** chosen by the agent's own reading, never by a timer:
  - a quiet step (nothing owed, bets paying);
  - after a level clear;
  - when a line of work has stopped gaining (the marginal-value rule of 10-31).
- **What to muse on:** parked residuals ordered by gain × need.
  - Gain is the gap's size and how compressible it is.
  - Need is whether its slot kind is on this board or recurs.
  - It is never other games' leftovers by default (ties to the per-game park question).
- **The ladder:**
  1. **Candidate.** A method that pays on a parked residual is held in working memory. Today the "paying" list is written and read by nothing; this is the missing rung.
  2. **Tested.** When its slot kind appears on the board, it becomes a test intent, a probe press.
  3. **Settled.** If the board pays, it is admitted and carried as a method by kind. It becomes an atom and, if it fires often and cheaply, a habit in the reflex tier.
  4. **Refuted.** If the board refuses it, the refusal is recorded long-term. A candidate that is never tested may lapse from the cache, but its ledger row stays.

## Sources

- [Sherrington 1906, The Integrative Action of the Nervous System](https://archive.org/stream/integrativeacti00shergoog/integrativeacti00shergoog_djvu.txt)
- [Rust 1976 (Sokolov's model)](https://www.psychometrics.cam.ac.uk/system/files/documents/GenOrientingResponse.pdf)
- [Schmid, Wilson & Rankin 2015, Front Integr Neurosci](https://www.frontiersin.org/journals/integrative-neuroscience/articles/10.3389/fnint.2014.00097/full)
- [Habituation (Wikipedia)](https://en.wikipedia.org/wiki/Habituation)
- [Hedges, Molecular Mechanisms of Memory: Aplysia](https://pressbooks.uiowa.edu/inb/chapter/molecular-mechanisms-of-memory-aplysia)
- [Yilmaz & Meister 2013, Current Biology](https://meisterlab.caltech.edu/documents/8117/yilmaz_2013_looming_response.pdf)
- [Modrell, Primitive Reflexes, StatPearls](https://www.statpearls.com/articlelibrary/viewarticle/27744/)
- [Brooks 1986, A Robust Layered Control System](https://mae.engr.ucdavis.edu/dsouza/brooks.pdf)
- [Evans & Stanovich 2013, Perspectives on Psychological Science](https://library.scottbarrykaufman.com/uploads/2014/04/dual-process-theory-Evans_Stanovich_PoPS13.pdf)
- [Mason et al. 2007, Science](https://labs.psych.ucsb.edu/grafton/scott/Papers/Mason2007Science.pdf)
- [Mattar & Daw 2018, Nature Neuroscience](https://www.princeton.edu/~ndaw/md18.pdf)
- [Wilhelm et al. 2011, J Neurosci](https://research.uni-luebeck.de/en/publications/sleep-selectively-enhances-memory-expected-to-be-of-future-releva/)
