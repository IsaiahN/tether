# WATSON 2026-10-26 15:20 CDT: are we missing what babies do? Contact before concept

## Isaiah, verbatim (15:07 CDT)

> "Are we missing something? Like how babies learn or something ? Do a watson check against umwelt repo and the reasoning. Also has reasoning or actions per sec increased?"

## 1. Actions per second (measured, from the round lines)

All three rounds below played 25 games.

| Round | Build | Actions | Wall (s) | Actions/min | Seconds per action |
|---|---|---|---|---|---|
| PLAY11 r9 | 68db0d7, before the Umwelt build | 176 | 4,294 | 2.46 | 24 |
| PLAY13 r1 | 8dae023, Umwelt + limbs | 75 | 5,477 | 0.82 | 73 |
| PLAY14 r1 | 9f77f70, + think-or-act at the step | 96 | 5,114 | 1.13 | 53 |

- **Since this morning:** actions per minute rose about 37% (0.82 to 1.13).
- **Against the pre-Umwelt round:** still about 2.2x slower per action. The stores and seeds differ, so this is a direction, not a pairing.
- The empty-store cn04 test this morning (5 steps on 68db0d7, 3 on 2e77f16, in the same minute) says part of that is the build.
- **"Reasoning per second"** has no direct instrument; the stream carries no time. What is measured is thinking time per action, 73 s down to 53 s.

## 2. QUESTION

Is the agent missing a basic way infants learn, such that more thinking per action cannot make up for it?

## 3. DOMAIN CENSUS

**R:** arity 3 (the gap, the action that could test it, the term that could explain it); scale step, game, round.

| Domain | Actors | Currency | Anchor |
|---|---|---|---|
| CONTACT | presses | actions per slice | the ground's answer to each press |
| DESCRIPTION | mints, lookups | candidates walked | a term that pays (cost + left < base) |
| DEVELOPMENT | the order in which the two are used | (none) | the round's learning (mints accepted, settles) |

**Order (Fig 3):** contact first, then description.

## 4. TETHER (primary, verbatim)

- **Fig 5 :4-5** "the prediction gap / fires on every action".
- **Fig 5 :10-14** "sort the gap into four kinds / held: the model was right, nothing owed / new: extend perception, aim the probe here / mis-attached: refit what you have, do not invent / mechanism broken: a new term is owed".
- **Fig 5 :15-17** "the curiosity drive / fires when nothing is scoring / aimed at the new bin".
- **Fig 5 :24** "is it actually new?"
- **Fig 5 :49** "Machinery firing is not the milestone. A running system can mint and still return nothing new".
- **Fig 11 :40** "A system cannot be made more capable by improving the agent in isolation. An improvement that does not change contact changes nothing, however much it improves."
- **Fig 12 :128** "A long chain of cheap parts is expensive to describe and may cost one action to refute."

**What these decide.** The Tether sorts each gap BEFORE paying for it. A "new" gap is a perception question: aim a probe, act. Only a "mechanism broken" gap owes a new term.

## 5. THE CODE (read at ae028d6)

- `route()` bins a slot NOVEL only while `len(self.trace) < 2` (tether.py :10747-10748). From the second frame on, every unexplained slot is MECHANISM, which goes to a full mint.
- So the agent treats almost every gap as "mechanism broken" and theorises on two or three frames.

**Measured in round 1 (PLAY13 and PLAY14):**
- tr87's single step ran 5 full mints, each to its budget.
- PLAY14 r1 made 218 searching parks, every one budget_exhausted.
- 0 mints were accepted in PLAY14 r1 (1 in PLAY13 r1).

That is Fig 5 :49's "can mint and still return nothing new", and Fig 11 :40's no gain without contact: 1 to 3 actions per game.

**Triangulated:** Fig 5, Fig 11, Fig 12.

## 6. WORLD (secondary; each source read)

- **Developmental robotics / cognitive science.** Smith & Gasser, "The Development of Embodied Cognition: Six Lessons from Babies" (Artificial Life, 2005):
  - "In babies, spontaneous movement creates both tasks and opportunities for learning."
  - "Without spontaneous movement, without exploration, there is nothing to learn from the mobile."
  - Corroborates: contact first.
- **Infant learning experiments.** Rovee-Collier's mobile conjugate reinforcement (Lancaster glossary): infants of 2 to 6 months "learn to kick a foot ... in order to produce movement in an overhead mobile"; "The infant discovers the contingency between the kicking movements and the reinforcement."
  - Corroborates: the first thing learned is an action-effect contingency, from many cheap repetitions.
- **Developmental psychology.** Piaget's secondary circular reactions (University of Nottingham HELM): "Secondary circular reactions involve repeating action ... The infant begins to discover that means (actions) can lead to ends (interesting events)."
  - Corroborates: repeat what produced an effect before explaining it.

## 7. VERDICT (from the figures)

**Yes, something basic is missing: the "new" bin.**

- **The gap.** The agent mints for gaps it has not yet earned the right to explain. A baby kicks a hundred times, and finds which kick moves the mobile, before it has any concept. Our agent tries to build a term from two or three frames, on every unexplained slot, each step. It then gets about 3 actions per game, which is too little contact for any term to pay.
- **The fix, in the Tether's own words (Fig 5 :12):** a young gap is NEW. Answer it with a probe (an action), not a mint. Repeat or vary the press that produced the change (the circular reaction). Mint only when the gap is "mechanism broken": the slot's own record shows a residual that persists, or a held term was refuted.
- **What it should change:** more actions per slice (contact) and fewer, better-supported mints. Contact is what Fig 11 :40 says capability comes from.

**Not settled here: the evidence bar for "mechanism broken".** It must be derived, not picked: no magic number. The existing pieces it can use:
- the window's recurrence evidence (_lag_evidence);
- the support check that already parks a mint as no_support;
- R-B's run counter.

**A second gap, already known (M1, open decision 1):** the action-effect table, the agent's contingency learner, lives within one game and is not carried between games. A baby keeps "kicking moves things". Carrying it by kind is the developmental analogue.

**Cost if wrong:** some real mechanisms are explained a few steps later. **Undoable:** yes, an arm. **Reversed by:** more actions per game with no rise in accepted mints and settles over several rounds.

## Sources

- [Smith & Gasser, The Development of Embodied Cognition: Six Lessons from Babies](https://legacy.cs.indiana.edu/ftp/gasser/alife.pdf)
- [Mobile conjugate reinforcement (Lancaster University psychology glossary)](https://www.lancaster.ac.uk/fas/psych/glossary/mobile_conjugate_reinforcement/)
- [Why do babies do the same thing over and over again? (University of Nottingham HELM)](https://nottingham.ac.uk/helm/dev-test/ncc/0_2_years/intellectual-0-2_first_1001_days/page_six.html)
