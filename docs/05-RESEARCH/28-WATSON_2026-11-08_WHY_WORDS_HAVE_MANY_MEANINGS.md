# WATSON 2026-11-08 -- Why words have many meanings, why placement changes them, and why it is recursive

Asked by Isaiah, 18:56 CST: "Why does every word have nearly multiple connotations or meanings? and also how you can take a word and based on the placement in the sentence change the meaning. like: 'this is how i live peacefully' vs 'coming to you live from the capital' ... the word itself while holding meaning is still being filtered or contextualized by the sentence it is in. this is so recursive ... humans say looks for visual cues ... versus 'that signal is your cue (to take an action)' we understand both simultaneously at least if they have been experienced or heard in that manner."

Builds on WATSON_2026-11-08_catalogs_and_word_clusters.

## TETHER (primary, verbatim)

1. **Many meanings is compression by reuse.**
   - Fig 5 :26: a term is admitted only if it "cost[s] less to state than the confusion it removes".
   - Fig 5 :43-44: "A term that explains everything by saying nothing fails this, and so does a term that explains one occasion perfectly."
   - Re-using a held term in a new cluster costs less than minting a new term per occasion. So a catalog of senses under one word is the cheapest code, as long as context can pick the sense.
2. **Placement is part of the meaning.**
   - Fig 12 :46: "A bond is the typed relation between two operands ... which one holds is not recoverable from the operands."
   - The asymmetric-bond test, Fig 12 :74: "swap them. Does it become a different thing? Yes."
   - Fig 12 :94: "The arrangement is the substance."
   - Fig 13 :75-76: "which structure it is bonded to is part of what it is."
   - So the same token in a different slot or role is a different term. That is "live" the verb against "live" the adjective.
3. **The recursion is the alternation.**
   - Fig 13 :28: "They alternate, and the alternation is where both the recursion and the randomness come from."
   - Fig 13 :29-30: "A state with no structure has no magnitude ... A structure with no state is empty: an ordering over nothing".
   - So a word (state) means nothing without a sentence (structure), and a sentence is empty without its words. Each re-reads the other, and that back-and-forth IS the recursion Isaiah sees.
4. **Look up the kind, then narrow.** Fig 9 :25-32: the lookup returns "a kind of thing, never the answer itself", and narrowing comes after.
   - So all of a word's clusters can be reached cheaply, and context narrows to one.

Triangulated: Fig 5 (reuse is cheap), Fig 12 and Fig 13 :75-76 (arrangement is meaning), Fig 13 :28-30 (alternation is the recursion). These have low overlap.

## WORLD (secondary, each source read)

- **Ambiguity is efficient.** Piantadosi, Tily & Gibson, *Cognition*, 2012, via ScienceDaily/MIT News. Ambiguity lets speakers "reuse easy [words] in different contexts over and over again", and it is "cognitively cheaper" for listeners to infer from context than for speakers to say longer things. Across English, Dutch and German, shorter, more frequent words were the most ambiguous.
  - Predicts: the most-used kinds carry the most clusters. Corroborates Fig 5.
- **Meaning only in context.** Frege, *The Foundations of Arithmetic*, 1884 (Wikipedia "Context principle"): "never to ask for the meaning of a word in isolation, but only in the context of a proposition".
  - **Compositionality**, Partee via Wikipedia: "The meaning of a compound expression is a function of the meanings of its parts ... and of the way they are syntactically combined."
  - The two principles pull against each other: the whole is built from its parts, and the parts' senses come from the whole.
  - Predicts: the recursion Isaiah sees is a recognised, unresolved tension between two principles. Fig 13's alternation is how it runs.
- **Both meanings at once.** Swinney, 1979 (Wikipedia "David Swinney"): listeners "accessed multiple meanings for ambiguous words, even when faced with strong biasing contexts". Both the "insects" and "surveillance" meanings of "bugs" were primed.
  - Predicts: Isaiah's "we understand both simultaneously" is measured. All senses are reached first, cheaply.
  - (The later selection step is the standard reading of this work, but the page read does not state it, so it is not cited here.)

No conflict found.

## VERDICT

1. **Why many meanings:** compression by reuse (Fig 5). One headword serves many clusters, and context picks the sense more cheaply than separate words would cost. The dictionary is a catalog. In the agent, expect the most-used kinds (contact, move, same, −) to grow the most clusters. That is healthy compression, not a defect to fix.
2. **Why placement changes meaning:** the ROLE is part of the term (Fig 12 :74, :94; Fig 13 :75-76).
   - Add to the catalog design: a cluster's key includes the kind's ROLE, meaning its slot position in the template and which operand it is in an asymmetric bond.
   - The same atom as subject and as object, or before and after "→", are different clusters, the way "live" (verb) and "live" (adjective) are.
3. **Why it is recursive:** Fig 13's alternation.
   - The agent resolves a template by alternating: fill the most constrained slot first (Take The Best), let that narrow the others' clusters, then re-check the template against its filled parts.
   - It stops when nothing changes, or when the budget is spent (Fig 12). This is the same alternation the figures name, run a few rounds, never a full search.
4. **Both senses at once:**
   - When a kind comes up, reach all its clusters cheaply, headwords only (Swinney; Fig 9's kind list).
   - Then let the collocates in contact and the slot role select one (Yarowsky, catalogs WATSON).
   - Only clusters earned by experience are in the catalog. That is Isaiah's "at least if they have been experienced or heard in that manner": a sense never paid for is not there to be reached.

These go into the catalogs design (D1/D2, S1) as three additions:
- (a) role in the cluster key;
- (b) reach all clusters, then select by context;
- (c) resolve by bounded alternation.

- **Cost if wrong:** finer clusters by role could split senses that should be one. Merge on shared outcomes (S2) re-joins them.
- **Undoable:** yes.
- **Reversed by:** the retest showing role-keyed clusters picking wrong senses more often than role-blind ones.

## Sources

- [Piantadosi, Tily & Gibson 2012, ambiguity makes language efficient (ScienceDaily)](https://www.sciencedaily.com/releases/2012/01/120119133755.htm)
- [Context principle (Frege 1884) (Wikipedia)](https://en.wikipedia.org/wiki/Context_principle)
- [Principle of compositionality (Wikipedia)](https://en.wikipedia.org/wiki/Principle_of_compositionality)
- [David Swinney, cross-modal priming (Wikipedia)](https://en.wikipedia.org/wiki/David_Swinney)
