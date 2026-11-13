# WATSON — second nature per task, and what carries over to all (2026-11-11 07:26 CST)

Isaiah, 07:24, verbatim: "One nuance is if the agent is able to distinguish per task or per problem; for instance, my second nature moves in basketball differ from tennis or driving. How do we handle this? Some carry over to all. You might need to WATSON that too - and always do the full Tether with WATSONs, please"

Method: the full procedure. The census was written at 07:25, before any figure line was chosen. Every figure line below was checked in the original SVG (metadata stripped, tspans joined). The world sources were each read.

QUESTION: Should second nature (reuse counts, residency tiers, settledness) be kept per task? How does the agent tell what carries over to every task?

DOMAIN CENSUS (written first):
- RESIDUAL (effect terms): a skill automatic in one task is not automatic in another, and a few skills are automatic everywhere. One global reuse count would either push one task's habits into another or miss what is general.
- R: arity 3 (the skill; the task or context; the self) · symmetry: is the same skill in two tasks one term or two? (the open question) · scale: step -> game -> family of games -> lifetime.
- Domains (actors / currency / anchor):
  - ground: games / settlement / what paid where;
  - composition: terms and the structures they bond into / the arrangement / which structure a term is bonded to;
  - record: evidence rows with where they paid / per-context counts / settled_on;
  - search: cues in contact / the filter / which context is selected;
  - scale (the membrane): task-level vs general / methods vs recordings / what crosses between scales;
  - habitat: agent-and-task / contact / where capability lives.
- Union: context x residency = a per-context tier. The general tier is the overlap across contexts: its own compound, with its own loop.
- Order: ground -> record -> composition -> search. The membrane decides what crosses between contexts.

TETHER (primary, verbatim, SVG-checked), per domain:
- Habitat. Fig 11 :39 "capability is a property of agent-and-habitat, never of the agent alone."
  - Second nature is a property of the skill in a task, not of the skill alone. Basketball moves are capable in basketball.
- Record. Fig 1 :19-22 "The residual is indexed by object slot, not aggregated. ... Aggregating across slots is how a live signal disappears into an average."
  - Counts are kept per context and never pooled. The agent already keeps settlement per slot: gamma.is_settled(name, slot) ("a term settled on A must read NOT settled on B", gamma.py:1682-1698), and refutations carry `where` and `slot`.
- Composition. Fig 13 :75-76 "a gradient over a network is a different term from a gradient over space, because which structure it is bonded to is part of what it is."
  - The same motion bonded into basketball and into tennis is two terms, even when the atoms are the same.
- Composition. Fig 12 :123 "functional group. A substructure whose presence fixes the outcome. The group says what kind; the qualifier says which member."
  - What carries over is the GROUP (the kind of move). The QUALIFIER (the per-task setting) is chosen in each task.
  - The agent already splits the two: gamma.units() keys a settled unit on its atoms alone, and "The binding is re-decided per slot at mint" (gamma.py:2397-2402). The unit is the group; the binding is the qualifier.
- Scale. Fig 4 :22-26 "Only methods cross up. ... upward: a method that can be reapplied. Never the recording of a particular success. ... A recording carried upward looks like knowledge and is a description of one occasion."
- Scale. Fig 4 :34-35 "The level a method lands on remakes it. A seed carries no small tree: it carries what will grow one, and the conditions it lands in decide what it becomes."
  - What carries to every task is a method, and each task remakes it. Balance carried from basketball to surfing is the same method, set differently.
- Scale. Fig 4 :28-30 "take the round trip and measure the gap."
  - Transfer is tested, not assumed: carry it to the new task and measure how far it falls short.
- Ground (how to know it's general). Fig 2 :31 "Independence, between two frames, is how little they draw on the same evidence. ... Independence is what makes agreement mean something."
  - A skill is shown to be general when it pays in INDEPENDENT tasks. A thousand uses in one task is one evidence pool and proves nothing about other tasks.
- Search. Fig 9 :4-5 "Disagreements that do not shrink with effort, where each rule keeps working well on a different subset, are not one hard question but several well-formed ones. Split it rather than search."
  - A habit that keeps paying in one task and failing in another is two terms: split it by context.
- Search. Fig 9 :55-58 "A bundled problem is usually a union of overlapping conditions ... a case in two conditions is not a harder case of either. It stops being a mixture and becomes a specific compound."
  - What holds across tasks is its own compound (the general tier), not an average of the task tiers.
- Search. Fig 9 :60 "Use filters for the budget and witnesses for the verdict."
  - A context filter decides what is kept ready, never the verdict.
- Triangulated across Fig 11, Fig 1, Fig 13, Fig 12, Fig 4, Fig 2 and Fig 9, with low overlap. No strain: each line governs the quantity it is used for.

WORLD (secondary, each source read):
- Motor learning. Schmidt 1975, schema theory (via Wikipedia "Motor program"): a generalized motor program holds "an abstract representation for a class of movements with invariant features", while "parameters such as overall movement duration, overall force of contractions" are set per situation.
  - Predicts: what carries over is the class of movement; each task sets the parameters. Corroborates Fig 12 :123 (group and qualifier) and the agent's unit/binding split.
- Memory by context. Godden & Baddeley 1975 (via Wikipedia "Context-dependent memory"): "words learned underwater were best recalled underwater, and words learned on land were best recalled on land"; and "the effects of context change on memory retrieval are much greater in recall tasks than in recognition tasks."
  - Predicts: what is learned in a context is reached most easily in that context, so residency should follow context. The second finding fits Fig 9: reaching unaided (recall) depends on context more than checking a given candidate (recognition) does.
  - (The PMC replication page could not be read past a browser check, so it is not cited.)
- Animals. Nieto & Bernal-Gamboa, "The Role of Attention in the Renewal Effect", Rev. Mex. Análisis de la Conducta 41(2), 2015: "In the renewal effect, an extinguished response returns whenever the subject is tested outside the extinction context"; "the retrieval of extinction learning is highly context specific".
  - Predicts: a habit suppressed in one context returns in another. Refusals must be kept per context, so a failure in tennis must not erase a basketball habit.
  - Corroborates Fig 1 :19-22 and the agent's per-slot refutation and per-context reassessment (r1713).
- How far skills travel. Sala & Gobet, "Does Far Transfer Exist?", Current Directions in Psychological Science 26(6), 2017: "near transfer takes place often"; "far transfer of learning rarely occurs"; with active controls "the overall effect sizes were minimal or null".
  - Predicts: the default is task-specific. General standing has to be earned on independent evidence and not assumed. Corroborates Fig 2 :31 and Fig 4 :28-30.
- Machine learning. Yosinski, Clune, Bengio & Lipson, "How transferable are features in deep neural networks?", arXiv 1411.1792, 2014: first-layer features "appear not to be specific to a particular dataset or task, but general"; "Features must eventually transition from general to specific by the last layer"; "the transferability of features decreases as the distance between the base task and target task increases."
  - Predicts: what carries over to all is the low-level, perceptual layer. In the agent that is the kernel, the innate atoms and the perception kinds, and most learned terms will be specific. Corroborates.
- Economics. Becker 1964 (via Groen, "Occupation-Specific Human Capital and Local Labor Markets", BLS Working Paper 376, 2005): "skills that are specific to a given firm and skills that are completely general".
  - Predicts: both kinds exist and are worth keeping, and only the general kind is portable. Corroborates the two tiers.
- No conflict found.

VERDICT (from the figures):
1. PER CONTEXT BY DEFAULT.
   - Reuse counts, the chances window, residency tiers and refusals are all kept per context, never pooled (Fig 1 :19-22; Fig 11 :39; Fig 13 :75-76).
   - Failing in tennis does not touch basketball (renewal).
2. CONTEXT IS A KIND, NEVER A NAME.
   - The agent can't use a game id as "the sport". That would be a convention deciding an outcome (Fig 2 :43, Fig 10), and it would repeat the failure Isaiah caught at 20:49 on 11-10.
   - The context is the sense cluster the cues in contact select (step 8b). So 8d is built on 8b, after it.
3. WHAT CARRIES OVER IS THE GROUP, NOT THE SETTING.
   - A settled unit (atoms only) is the transferable group. Its binding, re-chosen per slot at mint, is the per-task qualifier (Fig 12 :123; Schmidt).
   - This split already exists in gamma.units().
4. GENERAL STANDING IS EARNED ON INDEPENDENT EVIDENCE.
   - A unit joins the GENERAL tier only when it has paid in at least two independent contexts (Fig 2 :31). Two is HOT/COLD's precedent; E2E2 will show whether it holds up.
   - Many uses in one context never make a unit general.
   - Transfer is measured by the round trip (Fig 4 :28-30): a general unit used in a new context records its gap there.
5. THE TIERS AT GAME START:
   - the kernel and innate atoms (general by construction; Yosinski's first layer);
   - the general tier, always loaded;
   - each context's tier, loaded when the cues select that context (the thesaurus filter);
   - everything else cold on disk, read on a miss. Nothing is deleted.
   - The reuse count still decides residency only, never which action wins (Fig 9 :60).
6. A FAILURE IN A NEW CONTEXT SPLITS; IT DOESN'T DEMOTE.
   - If a general unit fails in a new context while still paying in the others, that is Fig 9 :4-5: split it. It stays general where it pays and gets a refusal in that context only.
   - It leaves the general tier only if it stops paying in independent contexts.

What E2E2 can read now (before 8b exists, game is the only stand-in for context, and it is used only as a READING, never as a decision):
- (f) per settled unit: the number of distinct games it was used in and the number it paid in.
  - Units that paid in two or more games are the candidates for the general tier.
  - Units used in many games but paying in one are the "near-transfer only" cases.
  - Expectation (Sala & Gobet; Yosinski): few general units, mostly perceptual or kernel-near.

Cost if wrong: small, behind 8d's arm. Undoable: yes.
Reversed by: 8c's retest showing per-context keying loses levels, or fails to reach a unit that would have paid in a new context, against a pooled count.

Sources:
- [Motor program (Wikipedia), Schmidt's schema theory](https://en.wikipedia.org/wiki/Motor_program)
- [Context-dependent memory (Wikipedia), Godden & Baddeley 1975](https://en.wikipedia.org/wiki/Context-dependent_memory)
- [Nieto & Bernal-Gamboa 2015, The Role of Attention in the Renewal Effect](https://www.redalyc.org/pdf/593/59341195012.pdf)
- [Sala & Gobet 2017, Does Far Transfer Exist?](https://pmc.ncbi.nlm.nih.gov/articles/PMC5724589)
- [Yosinski et al. 2014, How transferable are features in deep neural networks?](https://www.emergentmind.com/papers/1411.1792)
- [Groen 2005, Occupation-Specific Human Capital (BLS), on Becker 1964](https://www.bls.gov/osmr/research-papers/2005/pdf/ec050020.pdf)
