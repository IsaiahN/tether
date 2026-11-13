# WATSON 2026-11-08 -- Categorise, relate, anticipate: search the way search engines do, without a neural net

Asked by Isaiah, 18:23 CST: "this is what llms have right, these are the vectors of data or 'neural net' but we cannot rely on that, but we can simulate the categorization process (which search engines also do ...) it seems this is more important semantic search and searches that casually relate to future searches (similar to how llms are primed to anticipate the users next prompt or query to help them with speed) ... you can borrow from the pagerank search but we still will need specific details"

This builds on:
- WATSON_2026-11-02_how_search_engines_keep_many_tags_fast (r810: top-K with fall-back, tiers, AND by smallest list first);
- WATSON_2026-11-08_thinking_without_words_cue_to_outcome (the unit of thought is cue kind to outcome kind).

## QUESTION

LLMs get item-based categorisation for free from learned vectors, and we will not use vectors. How does the agent get the same three powers with transparent counts?
1. Categorising: what kind of situation this is, and which "islands" apply.
2. Relating: what is semantically near, without embeddings.
3. Anticipating: what the next search will probably need, so it is ready before it is asked for.

Where does PageRank fit, and where must it not?

## DOMAIN CENSUS

- **R:**
  - Arity: the current cues, the library, and the next step.
  - Symmetry: entries that lead to the same outcomes are one concept.
  - Scale: the step (lookup), the game (sequence), and the lineage (what crosses).
- **The index (categorise):**
  - actors: entries filed under facets;
  - currency: postings length, i.e. work;
  - anchor: the library.
- **The relation graph (relate):**
  - actors: entries linked by shared use and shared outcomes;
  - currency: activation;
  - anchor: the ledger's endings.
- **The sequence model (anticipate):**
  - actors: outcome kinds in order within a game;
  - currency: probability of the next concept;
  - anchor: the sequences actually played.
- **The ground (standing):**
  - actors: endings;
  - currency: paid or not;
  - anchor: the board.
- **Partition, and it is the crux.** The first three ORDER search (filters). Only the ground SETTLES (witness).
- **Order (Fig 3):** categorise, then relate, then anticipate, then the ground decides.

## TETHER (primary, verbatim)

1. **A lookup is keyed by the described effect and returns a kind.** Fig 9 :25-32: "one lookup / R's own predicates name the habitat that holds φ* / describe it before you go looking ... matching is a one-pass check, not a search / ... describe the effect rather than the cause / → you get a kind of thing, never the answer itself".
   - So categorising is filing by described effect (facets), and the lookup returns a short kind-list.
2. **Filters order search; only witnesses decide.** Fig 9 :60: "Use filters for the budget and witnesses for the verdict. Never let a filter hand you a verdict."
   - Fig 9 :40-41: "a wrong cut removes the answer and speeds up / so keep every cut ranked and reversible".
   - So every ranking below (facets, nearness, anticipation, PageRank) may decide what is looked at FIRST. None may decide what is TRUE.
3. **Endorsement among frames is not evidence.** Fig 2 :40: agreement "is worthless when the agreeing frames share an evidence pool". Fig 7 :35: "Selection between rooms is where the ground votes."
   - So PageRank, which is endorsement by links, is a filter, never standing. Standing comes from endings alone.
4. **What comes down is what makes the next search cheaper.** Fig 4 :24: "downward: something that makes the next search cheaper. Never a replay of what worked once."
   - So anticipation and caching are the lawful head start: prepare the likely next lookup, never replay the last answer.
5. **Prefetching spends budget.** Fig 12 :126-127: one accounting "cannot compare them and will not notice the shortfall. It proposes arrangements it cannot afford to test, and the budget is what decides how much of the space is reached at all."
   - So anticipation must be priced in work and kept within budget.
6. **Spread the search.** Fig 6 :50: search "Fails by spending budget on a region already swept. Distribute the search."
   - So nearness spreads outward, and areas already swept are marked.

Triangulated: Fig 9 with Fig 4 (lookup and head start), Fig 9 :60 with Fig 2 / Fig 7 (filter vs witness), Fig 12 with Fig 6 (budget). These have low overlap.

## WORLD (secondary, each source read)

- **PageRank (link authority).** Brin & Page 1998, via a summary of the paper (mwhittaker.github.io): PageRank(A) = (1 - d) + d Σ PageRank(Ti)/OutDegree(Ti), "where d is a damping factor". Pages rank high when "frequently linked to or linked to by other sites with high PageRank". Ranking also used "proximity", and anchor text is credited to the page it points to.
  - Predicts: authority from being used by authorities. Corroborates the shape; Fig 2 limits its role to ordering.
- **Concepts from shared outcomes, and next-query prediction.** Cao, Pei et al. (KDD 2008; the TIST paper "Mining concept sequences", read):
  - queries are clustered into concepts "in a click-through bipartite", because "if two queries share many clicked URLs, they are similar to each other";
  - "A concept sequence suffix tree is then constructed from session data";
  - online, the user's queries are mapped "to a sequence of concepts" to "find out the concepts to which the user's next query most likely belongs."
  - Predicts:
    - (a) two cue kinds that led to the same paid outcomes are ONE concept, the categorisation step, with no vectors;
    - (b) the next lookup is predicted from the sequence of concepts so far. Corroborates.
- **Spreading activation (semantic priming).** Wikipedia "Spreading activation", citing Collins & Loftus 1975: activation flows from source nodes along weighted links. The update is A[j] += A[i] × W[i,j] × D, with a decay factor D and a firing threshold F. Related primes speed recognition ("doctor" after "nurse"). It has been applied to retrieval over networks of documents and terms.
  - Predicts: nearness without embeddings, from a graph of use, decaying with distance. Corroborates.
- **Predictive prefetching.** Padmanabhan & Mogul, *ACM CCR* 1996 (abstract): "predicting and prefetching files that are likely to be requested soon" gives "a significant reduction in the average access time" at "the cost of an increase in network traffic by a similar fraction."
  - Predicts: anticipation buys speed with budget, so it must be priced (Fig 12). Corroborates.
- **Isaiah's own rulings:**
  - 11-02: attributes as tags, like blog categories;
  - 11-03: "PageRank-style ranking: if thats useful lets do it";
  - 11-06: search "dynamically reweighted, with results cached so the same or a like-kind query isn't searched again unless the library changed", and the agent can "prime" itself, "preloading skills it expects to need when efficient, like web-page preloading".
  - Consistent with all of the above.

No conflict found.

## VERDICT (from the figures): four mechanisms, each a FILTER, with standing from endings only

**S1. CATEGORISE: a faceted index (no vectors).**
- Every entry (term, recipe, held expectation) is filed under the facets the agent perceives:
  - cue kind: contact level, change type, attribute class;
  - subject class (S0, S1, S2);
  - outcome kind: what ending it produced.
- An "island" is the postings list for a facet combination.
- A lookup builds its facets from the cues in contact now. It intersects the shortest list first (r810, AND by increasing frequency), ranks by how many facets match, evaluates the top K, and falls back to the next tier only when fewer than K fit (r810's TK).
- A cut is "not yet", never "nothing here" (Fig 9 :44, :60).
- This is D1's index (cue-to-outcome islands).

**S2. RELATE: concepts from shared outcomes, and nearness by spreading activation.**
- (a) Two cue kinds or entries that led to the same paid outcomes (overlap above a threshold, counted from endings) become ONE concept, held as aliases (Cao's click-graph clustering, with endings in place of clicks). This is also D2's blocking: a cue whose outcomes are already covered adds no new concept.
- (b) A use graph: an edge between two entries for each time they were used in the same PAID chain or the same game, weighted by count. From the current concept, activation spreads with decay D and threshold F, giving the "near" set that is looked at after the direct island (Collins & Loftus).
- D, F and the count threshold are starting values the agent re-weights from its own history (Isaiah 11-06: dynamically reweighted). They are plain numbers, logged when they change (11-06).

**S3. ANTICIPATE: a concept-sequence model, with priced priming.**
- Within a game, the agent keeps the sequence of concepts it acted on and the outcomes that followed (own history mixed with inherited by w), as counts of "after concept X came concept Y".
- After an outcome of kind X, the likely next concepts are prefetched into the cache: their islands looked up and their near sets activated. This happens only if P(Y | X) is above a threshold AND the prefetch fits within the step's budget (Fig 12; Padmanabhan's traffic cost).
- Cached lookups are reused for the same or a like-kind query until the library changes (a new mint, a settle or a refute invalidates the entries it touches). That is Isaiah's 11-06 cache rule.
- This is the head start that "makes the next search cheaper" (Fig 4 :24). It is never a replay: what is prefetched is a kind-list to search, not an answer to act on.

**S4. PAGERANK: authority as search ORDER, never as standing.**
- A term's authority = (1 - d) + d × Σ over PAID recipes that compose it of (that recipe's standing / its part count).
- So a part used by many well-paid recipes rises in search order, like a page linked from good pages.
- It is recomputed on library change (incrementally), damped by d.
- It is used ONLY inside S1's ranking (which of the top K first). It never adds to a term's standing, which only the board's endings give (Fig 2 :40, Fig 9 :60).

**THE ONE RULE ACROSS ALL FOUR:** they change what the agent looks at first, and they cost budget. They never decide what is true. A term pruned by them is reachable later. A concept merged by S2 keeps its member aliases, so a split can be recovered if the outcomes later diverge.

**WHAT EXISTS TODAY:**
- r810's top-K with fall-back and tiers;
- a lookup cache;
- kinds (K1);
- contact levels and their learned validity (B2, committed today);
- steer standings per template form.

**WHAT IS MISSING:**
- facets keyed by OUTCOME kind;
- concepts merged by shared outcomes;
- the use graph with spreading activation;
- the concept-sequence model with priced prefetch;
- the authority score.

**PROPOSED ORDER** (with D1-D3 from the 18:40 WATSON, as one "thinking by search" package, after the history test and the write-at-endings design):
1. S1 together with D1 (the index the islands live in).
2. S2 together with D2 (concepts, blocking and nearness).
3. S3 (anticipation and the cache rule).
4. S4 (authority inside the ranking).
5. D3 (narration states the prediction before the test).
Each goes behind its own switch, built to fixtures and invariants (r1482), with its payoff read in the online retest.

- **Cost if wrong:** search order is worse than today for some situations. Nothing is lost, because every cut is ranked and reversible.
- **Undoable:** yes, by switch.
- **Reversed by:** the online retest showing more lookups per pick (the "checked N of M" diagnostic) or fewer paid goals with S1-S4 on than off. That would mean the facets or the nearness are mis-keyed.

## Sources

- [Brin & Page 1998, The Anatomy of a Large-Scale Hypertextual Web Search Engine (summary)](https://mwhittaker.github.io/papers/html/brin1998anatomy.html)
- [Cao, Pei et al., Mining concept sequences from large-scale search logs (TIST, PDF)](https://www2.cs.sfu.ca/~jpei/publications/Concept%20Sequence%20TIST.pdf)
- [Spreading activation (Collins & Loftus 1975)](https://en.wikipedia.org/wiki/Spreading_activation)
- [Padmanabhan & Mogul 1996, Using Predictive Prefetching to Improve WWW Latency](https://www.microsoft.com/en-us/research/publication/using-predictive-prefetching-to-improve-world-wide-web-latency/)
- Prior: claude/WATSON_2026-11-02_how_search_engines_keep_many_tags_fast.md (Manning, Raghavan & Schütze 2008; Lucene block-max WAND)
