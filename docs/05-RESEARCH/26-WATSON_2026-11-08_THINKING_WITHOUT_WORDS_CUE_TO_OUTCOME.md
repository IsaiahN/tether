# WATSON 2026-11-08 -- Thinking without words: the cue, the outcome, and what gets stored

Asked by Isaiah, 18:19 CST: "Humans with no inner monologue exist and can still reason ... Even animals like dogs see the cue of a tennis ball or hear sounds or utterances that match the outcomes expected, like 'park', 'go for a walk', 'eat' ... The complexity of the vocabulary or sound doesn't matter; the outcome is what is saved and compressed. I will need you to WATSON this as well."

This refines WATSON_2026-11-08_from_babbling_to_inner_speech (written 30 minutes earlier). Its T6/D3 is corrected here.

## QUESTION

Is language, or an inner stream of words, the medium the agent's thinking must run in? Or is the unit of thought a cue paired with the outcome it predicts, with words as only one possible label for it? Each answer leads somewhere different:
- If thinking is in words, the agent should think in NSM.
- If thinking is cue to outcome, NSM is a readout, and what gets stored and compressed is the predicted outcome.

## DOMAIN CENSUS

- **R:**
  - Arity: a cue, an expected outcome, and the verdict.
  - Symmetry: two cues that predict the same outcome are ONE entry. "walk", "park" and a jingling lead are one expectation.
  - Scale: the step (prediction), the game (standing), and the lineage.
- **The cue channel:**
  - actors: changes, contact, sounds or tokens;
  - currency: residual;
  - anchor: the frames.
- **The expectation (what is stored):**
  - actors: cue kind to outcome kind;
  - currency: prediction error, paid or not;
  - anchor: the ledger.
- **Notation (words, templates, NSM):**
  - actors: labels;
  - currency: bits;
  - anchor: none of its own. It is a convention (Fig 2 :41).
- **Partition:** notation is a separate domain from the expectation. It labels the expectation and does not hold it.
- **Order (Fig 3):** perceive, then predict, then the verdict, then name what worked.

## TETHER (primary, verbatim)

1. **Prediction is the loop; words are not.**
   - Fig 1 :9: "perceive · plan · act · predict".
   - Fig 5 :4-5: "the prediction gap / fires on every action".
   - So the unit that fires on every action is a prediction against an outcome, not a sentence.
2. **Meaning is grounded by the outcome, not by the label.**
   - Fig 10 :49: "Declaring a meaning does not ground it."
   - Fig 2 :41: "agreement about a shared meaning is the product, not a corruption of it" (a convention).
   - So a word is a convention. What grounds it is the outcome it predicted and whether the ground paid.
3. **Describe the effect.**
   - Fig 9 :30-31: "your words are borrowed too, so describe the effect rather than the cause".
   - So what should be keyed and stored is the effect (outcome), not the surface form of the cue.
4. **Store only what is new.**
   - Fig 5 :24-25: "is it actually new? / it is not already in the library".
   - Fig 5 :26: "does the new term cost less to state than the confusion it removes?".
   - So a cue that predicts nothing beyond what is already predicted earns no entry. This is compression by the bargain.
5. **Name what worked.**
   - Fig 3 :15: "name what worked, verify it, and carry it to the next problem".
   - So the naming comes AFTER the outcome, and is a label for what paid.
6. **Composition carries meaning through structure.**
   - Fig 12 :2: "The Bond: How Composition Carries Meaning".
   - So meaning sits in how parts relate, not in the token used.

Triangulated: Fig 1 with Fig 5 (prediction); Fig 10 with Fig 2 (meaning as a convention until grounded); Fig 5 :24-26 (compression). These have low overlap.

## WORLD (secondary, each source read)

- **People without inner speech reason fine; words help specific verbal tasks.**
  - Nedergaard & Lupyan, *Psychological Science*, 2024, via BPS Research Digest: 46 people with near-absent inner speech ("anendophasia") against 47 with near-constant inner speech.
  - Worse on rhyme judgement and on recall of briefly shown words.
  - NO difference on task switching (adding vs subtracting) or on visual categorisation.
  - Speaking the words aloud removed the recall gap; the differences "may often be masked because people with anendophasia use alternative strategies".
  - Predicts: language is a tool for word-shaped tasks, not the medium of reasoning. Corroborates.
- **Inner speech varies widely.** Hurlburt and Heavey, descriptive experience sampling, via Hurlburt's *Psychology Today* column (2011): inner speech in "26 percent of all samples". "Some people talk to themselves a lot, some never, some occasionally."
  - Predicts: thinking does not require a verbal stream. Corroborates.
- **Dogs link arbitrary sounds to meanings, and meaning is separate from tone.** Andics et al., *Science*, 2016, via ScienceDaily: dogs process word meaning in the left hemisphere "regardless of intonation" and intonation in the right. Vocabulary learning is "a more ancient function that can be exploited to link arbitrary sound sequences to meanings."
  - Predicts: the sound is arbitrary; what is learned is what it predicts. Corroborates Isaiah's "the complexity of the vocabulary or sound doesn't matter".
- **Fast mapping by exclusion.** Kaminski, Call & Fischer, *Science*, 2004, via ScienceDaily: Rico knew about 200 words (37 of 40 toys retrieved). Asked for a new name among seven familiar toys, he fetched the new toy in 7 of 10 sessions, because "new words tend to refer to objects that do not already have names". He kept some of these a month later (3 of 6 sessions).
  - Predicts: a new cue binds to the unexplained thing in contact (Fig 5's guard "is it actually new"). Corroborates.
- **Only surprise is learned.** Kamin's blocking and the Rescorla-Wagner model, via Wikipedia "Blocking effect": when one cue already predicts the outcome, "nothing will be learned about a second CS". Learning is based on "the difference between what is predicted and what actually happens."
  - Predicts:
    - the store holds cue-to-outcome pairs that carried a prediction error;
    - a redundant cue is not stored;
    - that is the compression.
  - Corroborates Fig 5 :24-26 almost word for word. Fig 5's third guard IS blocking.

No conflict found.

## VERDICT (from the figures)

1. **The unit of the agent's thought is a cue-to-expected-outcome pair (a prediction), keyed by the KIND of cue in contact and the KIND of outcome.** It is grounded when the board pays, and refused when it doesn't (Fig 1, Fig 5, Fig 10).
2. **Words, templates and NSM are NOTATION** (Fig 2 :41, Fig 10 :49). They are the format a prediction is stated in, so it can be tested, logged and read by us. They are not the medium of thinking.
   - This matches Isaiah's 11-03 ruling: the agent "need not think in NSM" but must translate its reasoning into NSM.
3. **What is stored and carried is the outcome expectation, compressed by blocking.** A new cue earns an entry only if it predicts something the held cues don't (Fig 5 :24-26). The surface complexity of the cue is irrelevant: two cues with the same outcome are one entry, with aliases.

**CORRECTIONS to the 18:16 WATSON (babbling to inner speech):**
- **T6/D3 is withdrawn as a requirement.** Inner speech is not needed for thinking. NSM narration stays as the readout, and as a tool on word-shaped tasks (stating a plan so it can be refused, Fig 5 :65-66), never as the substrate.
- **D1 is restated.** A "verb island" is an island of cue kind to outcome kind that has paid ("walk" means the park), not a grammar verb. A template is just how that island's prediction gets written down.
- **D2 gains blocking.** A template or cue gains reach only if it predicts an outcome the held ones don't. An existing predictor blocks a redundant one.

**WHERE THE AGENT ALREADY DOES THIS:**
- B2 (committed today) learns per contact kind how often a goal paid. That is cue kind to outcome, own history mixed with inherited.
- The goal's ending (paid, parked, refuted) is the outcome record.
- **What is missing:** generation is not yet driven by these expectations (it fills templates widely), and nothing yet blocks a redundant cue from earning standing.

**THE DESIGN ITEMS, revised, for Isaiah's approval:**
- **D1 (cue to outcome islands).** Generate goals from the cue kinds in contact that have a paid outcome expectation, stated in whatever template fits. Fill slots from contact order.
- **D2 (critical mass plus blocking).** Reach widens only after several paid endings. A cue that adds no prediction beyond held ones earns no standing.
- **D3 (narration as readout).** NSM states the prediction BEFORE the test, so the ground can refuse it. That is the only thinking duty it has.

- **Cost if wrong:** moderate; reversible under arms.
- **Reversed by:** the online retest showing that paying goals come from cue kinds with no prior expectation and that blocking suppressed them. That would mean the critical mass is too high, or blocking is too strict.

## Sources

- [Nedergaard & Lupyan 2024, anendophasia (BPS Research Digest)](https://bps.org.uk/research-digest/silent-inner-world-anendophasia)
- [Hurlburt, Not everyone conducts inner speech (Psychology Today)](https://www.psychologytoday.com/gb/blog/pristine-inner-experience/201110/not-everyone-conducts-inner-speech)
- [Andics et al. 2016, dogs process words and intonation (ScienceDaily)](https://sciencedaily.com/releases/2016/08/160829192701.htm)
- [Kaminski, Call & Fischer 2004, Rico and fast mapping (ScienceDaily)](https://www.sciencedaily.com/releases/2004/06/040611072744.htm)
- [Blocking effect and the Rescorla-Wagner model (Wikipedia)](https://en.wikipedia.org/wiki/Blocking_effect)
