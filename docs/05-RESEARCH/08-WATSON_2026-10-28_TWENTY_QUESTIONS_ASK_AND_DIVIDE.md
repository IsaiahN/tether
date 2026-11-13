# WATSON 2026-10-28 15:20 CDT — Twenty questions: does the agent ask good questions, and does it divide the space with the answers?

## Isaiah, verbatim (15:15 CDT)
> "In a nutshell, if I had to summarize what the metalaws of the Tether are, it's the proof behind why the 20 questions game works. And it's also loosely the procedure needed. In that vein, we need to think about the quality of the questions the agent is asking, and is the agent dividing the search space properly when it gets answers or feedback from the board."

His framing, from the two attached conversations: the formula travels by narrowing, not by being stated. The generator expands from the base, and transmission contracts back toward it: the same procedure run in the opposite direction.

## QUESTION
For each open gap, two things:
1. Does the agent choose presses (its questions to the board) that split its live explanations?
2. Does each answer remove the explanations it refutes, so that the next question starts from what survived?

## DOMAIN CENSUS
- **R:** arity 3 (the open gap, its candidate explanations, the press that could tell them apart); scale step → game → life.
- **ASK.** Actors: presses. Currency: actions. Anchor: the board's answer.
- **DIVIDE.** Actors: candidate terms for one gap. Currency: candidates priced. Anchor: elimination by a frame's row.
- **ORDER (Fig 3):** DIVIDE is upstream of ASK. A question is only good relative to the candidates still alive, so without division there is nothing to aim a question at.

## TETHER (primary, verbatim)
- **Fig 9 :6-8.** "1 · the verdict: is φ* in here at all? / 2 · the lookup: which frame holds it? / 3 · the narrowing: which one is it?"
- **Fig 9 :38-42.** "elimination compounds here, and only here / cheap because the new atom shrank the space / a wrong cut removes the answer and speeds up / so keep every cut ranked and reversible / → narrowing gets you close, the ground decides"
- **Fig 9 :4-5.** "Disagreements that do not shrink with effort … are not one hard question but several well-formed ones. Split it rather than search."
- **Fig 9 :60.** "Use filters for the budget and witnesses for the verdict. Never let a filter hand you a verdict."
- **Fig 5 :12, :18.** "new: extend perception, aim the probe here"; the curiosity drive "seeks the gap that is large and compressible".
- **Fig 13 :136-139** (corrected 10-29 from "Fig 12"; r325). "What it can do is narrow. It can say the question is not one question and must be split before it is searched again … narrowing gets you close while the ground decides."

These are triangulated: Fig 9, Fig 5 and Fig 12 have low overlap. Read together, they say the twenty-questions procedure is the Tether's narrowing step. A question is worth asking when its answer cuts the live candidates. The cut compounds from one answer to the next, and it is kept ranked and reversible.

## THE CODE (read at d12c74e / c179020)

### ASK: what chooses the press
- **The exits in `choose()`:** routine, discriminate:goal, probe (a starved contact, or boredom → ELICIT), system0 (unexplored contacts), distinguish, draw.
- **DISTINGUISH** (interface.py :964-972, `separability` :1432) ranks actions by how DISTINCTIVE each action's past effect is in the action-effect contingency record. It separates *buttons from each other*. It does not separate the *agent's competing explanations of an open gap*.
- **The ruling was never built.** The interface's own comment (:65-69) records it: "discrimination returns at the INTENT level — *the agent picks the intent whose predicted outcomes differ most across its hypotheses*". No exit computes that.
- **The one branch that came close was deleted on 2026-09-28.** The old `discriminate` spread branch scored each action by how many distinct values Gamma's candidates predicted under it. It collapsed onto one button (93 of 131 presses on g50t; ACTION2 105 of 150 on ls20). It was also the agent ranking buttons with its own model.
- **Reading: why it collapsed.** A question is only best relative to the candidates still alive. Nothing removed candidates after each answer, so the "best question" never changed, and the same button stayed best forever. The collapse is a symptom of the missing DIVIDE half, not proof that asking splitting questions is wrong.

### DIVIDE: what an answer does to the candidates
- **Inside one mint, candidates are priced against the slot's record.** That is elimination, but it lasts only for that mint.
- **Across mints the narrowing is thrown away.** The frontier's resume key (tether.py :15697-15702) includes the held term's base bits, the trace epoch, the gap description, the library and the guard scope. Any new frame changes it, so 0 of 75 re-mints hit (found 10-26). Every mint restarts from the cheapest end of the full candidate space, and the budget cuts it at the same place. The agent re-asks the questions it has already had answered.
- **B1/B2's owed mints restart the same way.** PLAY16 r4: owed minted 62, dropped 210, unpaid 177.
- **PLAN re-enumerates 1,675,070 candidate goals every step on bp35.** Its "tried this level" refusal is keyed per instance (template, slot, operand). Late in a life the open set returns to 73k-218k (PLAY16 r3/r4).
- **The cost, measured.** PLAY16's clock: step-1 MINT time against first action is +0.87 (r1) and +0.76 (r4). One exhausting mint is about 67% of bp35's wait before its first press. Mints accepted: 0 in PLAY16 r1-r4.

### Verdict on the code
The agent fails both halves:
- It asks NOVELTY questions (what has not been pressed, which button acts distinctively), not CONSTRAINT-SEEKING questions (which press splits its live explanations).
- Its answers do not COMPOUND (Fig 9 :38). Each mint searches the whole space again.

## WORLD (secondary, each source read)
- **Machine learning.** Tom M. Mitchell, "Generalization as search", *Artificial Intelligence* 18(2):203-226, 1982. In the candidate-elimination algorithm, "for each example x, the hypotheses that are inconsistent with x are removed from the space" (Wikipedia, *Version space learning*). It predicts here that the candidate set for a gap should be a carried version space that each frame shrinks. Corroborates Fig 9 :38.
- **Developmental psychology.** Ruggeri, Lombrozo, Griffiths & Xu, "Sources of Developmental Change in the Efficiency of Information Search", *Developmental Psychology* 52(12):2159-2173, 2016. "Children's information search strategies are typically less efficient than those of adults"; "older children and adults more readily ask 'constraint-seeking' questions"; and "one crucial source of developmental change in information search efficiency lies in children's 'stopping rules.'" It predicts that a maturing learner moves from hypothesis-scanning to constraint-seeking questions, and learns when to stop asking and act. Corroborates the ASK verdict, and links to think-or-act. It also continues the 10-26 "how babies learn" WATSON: contact first, then constraint-seeking questions.

## VERDICT (from the figures)
The twenty-questions procedure is Fig 9's narrowing. The agent runs neither half, and the two are one fix, in dependency order.

1. **DIVIDE first: a carried version space per open gap.**
   - For each open gap, keep the candidates priced so far: survivors, and the eliminated (with the frame that refuted each), ranked and reversible (Fig 9 :41).
   - A new frame re-prices only the SURVIVORS against the new row, using the two-part cost added frame by frame, and eliminates the ones it refutes.
   - The next mint for that gap continues from the survivors, not from scratch.
   - Key it by the KIND of gap, not the instance (kind-not-instance, 10-17).
   - This replaces the resume key that never hits.
2. **ASK second: the question that splits the survivors.**
   - For a young gap with two or more survivors that predict differently, the probe is DISTINGUISH aimed at THAT gap. The interface realises the press whose predicted outcomes split the survivors most evenly: the twenty-questions halving, Shannon's expected information.
   - Ties go to A1's choice. The seam is kept, because the intent is "tell these explanations apart" and the interface picks the press.
   - With DIVIDE in place the 09-28 collapse cannot recur: each answer changes the survivors, so the best split changes.
3. **Stopping rules** (Ruggeri et al.; the think-or-act rule):
   - one survivor that pays → bind it and let the ground settle it;
   - none survives → "mechanism broken", a new term is owed (Fig 5 :14; Fig 8's new atom);
   - no press separates the survivors → "split_refused" is a reading, and perception must extend (Fig 5 :12).

This IS decision 1 (C1, new before mechanism), approved 10-26, given its procedure:
- a young gap is a version space to be narrowed by questions;
- "mechanism broken" is the version space emptying, which is a derived bar, not a picked number.

## Cost, undo, reversal
- **Cost if wrong:** survivors carried on a mis-keyed kind could leak across unrelated gaps. That is guarded by keying on the gap's kind and by re-pricing every survivor against each new row.
- **Undoable:** yes, one arm per half (DIVIDE, ASK), default ON, with arms rows, tests (must-fail, must-hold) and OFF byte-equal.
- **Reversed by:**
  - PLAY rounds where carried survivors do not cut candidates re-priced per mint, with no fall in step-1 MINT time;
  - or the ASK probe collapsing onto one press across a game while survivors still change. That would mean the split is computed over the wrong set.

## Measure before building (read-only, on PLAY16's files, today)
- **m1, re-asked questions.** For consecutive mints of the same slot, the share of candidates priced in mint k that were already priced in mint k-1. The rows may carry only counts; if names are missing, say so, and m1 goes into the DIVIDE build as its own row.
- **m2, what each answer bought.** Per press, the change in the survivors of the gaps it touched. Not measurable today; it is the DIVIDE row's first reading.

## Sources
- [Ruggeri, Lombrozo, Griffiths & Xu 2016, Developmental Psychology (PDF)](https://cocosci.princeton.edu/papers/Ruggeri_DevPsych.pdf)
- [Version space learning (Wikipedia; cites Mitchell 1982, Artificial Intelligence 18(2))](https://en.wikipedia.org/wiki/Version_space_learning)
