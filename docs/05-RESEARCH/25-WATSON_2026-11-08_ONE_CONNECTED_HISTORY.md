# WATSON 2026-11-08 -- One connected history: this game, my earlier games, and the library are not separate pools

Isaiah, 21:04 CST, replying to "the comparison should be 'this game vs my earlier games', not 'me vs an ancestor'":

"It's this game versus my previous games (+ my recallable life experience in library (which includes priors and outcomes and past predictions, etc., etc.)). Beings take all of their experiences into a situation or challenge. While they can't cherry-pick per se, in terms of word clusters and thesauruses in our terminology, you can't rip out some without losing the connectivity or connective thread to others. There's never a clean break or delineation that separates them (they are all connected). That's what also makes transfer possible too, or why a dog seeing a 'tennis ball' gets excited and anticipates playing fetch, or maybe more"

Builds on WATSON_2026-11-08_catalogs_and_word_clusters (thesaurus / sense cluster) and r1516 (the earlier save is the agent's past self).

## Unpacked (the five-step rule)

1. **He said:** the agent brings ALL its experience into a game: earlier games, plus what the library holds (priors, outcomes, past predictions). None of it is cleanly separable, because it is connected. The connections are what make transfer possible.
2. **He did not say:** that earlier experience should be trusted blindly in a new game, or that nothing is ever released.
3. **The model he is correcting:** experience as SEPARATE POOLS ("this game" against "earlier games") with one trust weight between them. That is what B2 does today. tether.py `_b2_cues`, at 5d881de :9440-9470, mixes "own" against "inh" per kind by one `w`.
4. **What replaces it:** one connected history. What comes forward into this moment is chosen by CONNECTION to what is in contact now. The tennis ball (a cue) lights the fetch sense cluster, with its expected outcome. Trust is earned or lost by that cluster's own predictions in this game, not by a blanket discount on "the past".
5. **Where it lands:** the B2 validity record, and D1/S2/S3 of the search package.

## TETHER (primary, verbatim)

- Symbols table :20-21: belief is "Formed from its own history and from what it inherited, mixed by w."
- Symbols table :24-26: "How far the belief leans on private history versus inherited prior. w_A + w_B = 1, and w is learnable from the outcomes of past weightings. Two frames with identical architecture diverge because their histories and their w diverge."
  - The w axis is PRIVATE HISTORY against INHERITED PRIOR. Earlier games are private history, so they sit on the same side as this game. In this build, the inherited prior is the corpus (inherited.py) and the architecture. So w belongs between the agent's whole history and the corpus, not between this game and its earlier games.
- Fig 12 :107-110: "where the arrangement is recorded, re-deriving it is a lookup and the actions were spent once ... Inside a run the arrangement persists and nothing is re-earned".
  - Within the one run, nothing earned in an earlier game should be re-earned from zero.
- Fig 12 :104: "A settled molecule becomes an atom for whatever composes over it."
  - Learning is built on learning. Removing a part breaks what was composed over it. That is Isaiah's "you can't rip out some without losing the connectivity".
- Fig 13 :75-76: "which structure it is bonded to is part of what it is."
  - A sense lives in its connections. Cut out as a separate pool, it is no longer the same sense.
- Fig 11 :67: "Move the residual and you must reproduce everything its goal required, and you inherit the new habitat's actors".
  - A new game IS a new habitat, so what held elsewhere is untested here. That is handled where it applies, by the sense cluster's own prediction, not by a blanket discount.

Triangulated: the Symbols table (where the w axis lies), Fig 12 (persistence and composition), Fig 13 (meaning is connection), Fig 11 (new habitat), with low overlap.

## WORLD (secondary, each source read)

- **Transfer rides on shared elements.** Thorndike & Woodworth, 1901, via Wikipedia "Transfer of learning": transfer "was restricted or assisted by the elements in common" between "the original context and the next context"; it "depends on how similar the learning task and transfer tasks are".
  - Predicts: what comes forward from earlier experience is decided by what it shares with now, not by when it was learned. Corroborates.
- **The cue now retrieves what was encoded with it.** Tulving & Thomson, encoding specificity, via Wikipedia: "contextual information is encoded with memories which affect the retrieval process", and "accessibility is governed by retrieval cues".
  - Predicts: the tennis ball retrieves fetch because they were stored together. The cue in contact selects the cluster. That is D1's filter. Corroborates.

No conflict found.

## VERDICT

1. **One history.** This game and the earlier games are one private history, with no partition between them. The w mix belongs where the Symbols table puts it: between the agent's whole history and the inherited prior, which in this build is the corpus, not between this game and its earlier games.
2. **What comes forward is chosen by connection.**
   - The cues in contact select the sense clusters they were stored with.
   - Those clusters bring their outcomes and past predictions (encoding specificity; shared elements).
   - Nothing is ripped out. Unconnected experience is simply not lit right now, not deleted.
3. **Trust is per sense cluster, and it moves on its own predictions in this game.**
   - A new game is a new habitat (Fig 11 :67), so a cluster's prediction is checked here. A miss lowers it, a hit raises it, and a sense is released only when its own prediction misses (already ruled for D1/D2).
   - There is no blanket discount on "my earlier games".
4. **Applied to B2 (design, not code):**
   - B2's per-kind validity becomes one record across all games.
   - It is read through the sense cluster the current cues select, once D1 exists.
   - The "own vs inh by w" mix comes out of the game-vs-earlier-games axis.
   - Until D1 exists, the honest interim is to fold "own" and "inh" into one count per kind. The w-by-holding is kept only if a measured case shows the blind fold choosing worse in a new game.

- **Cost if wrong:** the agent over-trusts an earlier game's habit in a game where it fails, for a few cycles until the cluster's predictions miss and release it. Bounded by the prediction gap.
- **Undoable:** yes, by a switch, and the design comes first.
- **Reversed by:** the retest showing more first-cycles-wasted on habits carried from unlike games with the fold than with today's w mix.

## Sources

- [Transfer of learning (Thorndike & Woodworth 1901) (Wikipedia)](https://en.wikipedia.org/wiki/Transfer_of_learning)
- [Encoding specificity principle (Tulving & Thomson) (Wikipedia)](https://en.wikipedia.org/wiki/Encoding_specificity_principle)
