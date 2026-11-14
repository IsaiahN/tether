# WATSON 2026-11-13: strata, islands and gap widths (for Recursive Diffusion Learning)

Status: FUTURE STATE, a companion to [40](40-WATSON_2026-11-13_RECURSIVE_DIFFUSION_LEARNING.md). Nothing is built.

## Isaiah's words (verbatim, spelling corrected)

> In my head I just see a spectrum or continuum of lossy transforms as gaps, with fading back into colour or signal, similar to those single-slit, double-slit experiments from science. These gaps represent the "lossy transformation" separating one stratum or level from another. On top of that seemingly uniform gap band there is also a gradient that is recursively reinforcing the strengths, but at an offset, so that as you move through the spectrum or continuum the signal gets stronger and stronger, with more overlapping offsets and overlays. In effect this simulates the left side temporally getting more faint.

> What we do know is that concepts build on top of each other, so their strength depends on knowing the previous terms. In that way we can sort them and determine "initial strength or placement". Contact can rearrange this somehow, or dim areas, but could that work? I'm not sure what would make one gap wider than another, possibly how big an "environment" was? For instance, these word "islands" (or whatever we call them): there's probably a mathematical strength of connection between them, node to node and cluster to cluster. If we combine that with the lineage speciation point, like oranges to orange drink after X number of deviations, there should be a mathematical way of clustering whole neighbourhoods based on signal strength. As terms and links get settled or removed, the strength of the neighbourhoods might falter and recalculate, causing gaps to widen or shrink. I think I'm making it complicated, so do another WATSON to see if there are graph theories or other concepts that could provide a clearer system for handling this that are still Tether compliant.

## Question, in effect terms

What decides three things, and how is each recomputed when the board settles or refutes something?
- a term's starting place and strength;
- which neighbourhood ("island") a term belongs to;
- how wide the gap is between two strata, or between two islands.

## Domain census

**R, the relation being decided.**
- Arity: two terms (a bond), two clusters (a gap), or a term and its parts (its placement).
- Symmetry: a bond between two parts is directional in the parts graph, because the whole is composed over its parts. Within a neighbourhood it is undirected.
- Scale: a term, an island, a stratum.

**Two kinds of gap are bundled in the picture.** Fig 9 :54-58 says to unbundle first:
- **Vertical gaps** separate strata: what a term is composed from, and how much detail was lost going up.
- **Horizontal gaps** separate islands at the same level: how little two neighbourhoods share.

They are different quantities with different anchors, so each gets its own derivation.

**Domains (actors / currency / anchor):**
- **Composition (vertical):** terms and their parts / depth / Fig 12 :104.
- **Neighbourhoods (horizontal):** terms and bonds / ground-paid bond strength / Fig 8 :46-49 and Fig 2 :31.
- **Speciation:** a term against its kind / core change (its parts and their arrangement) / Fig 12 :117.
- **Recomputation:** the store / derivation / Fig 6 :44, Fig 3 :18.

**Order (Fig 3):** placement first, because islands only exist among placed terms. Then islands, then gaps, then recomputation.

## Tether (primary, verbatim)

**1. Placement is depth, and depth is a level, not a fact about the world.**
- Fig 12 :104 "A settled molecule becomes an atom for whatever composes over it. So irreducible is a fact about a level and never about the world, and there is no bottom".
- Fig 3 :20 "The chain is ordered by dependency, not by importance. Each link consumes what the one above produces".

Your "concepts build on top of each other" is exactly this. A term's stratum is one more than the deepest of its parts. Triangulated.

**2. A term is only as reachable as its parts.**
- Fig 6 :44 "A term is reachable if it is derivable under everything currently held, so what happens to terms built on a refuted one follows from derivation rather than being stipulated."

Starting strength is therefore capped by the weakest part it stands on. When a part is refuted, everything above it dims by derivation, with no clean-up.

**3. The width of a horizontal gap is independence.**
- Fig 2 :31 "Independence, between two frames, is how little they draw on the same evidence."
- Fig 8 :47-49 "Independence is one quantity read twice. How much two frames draw on the same evidence decides both whether their agreement means anything and whether their union has any surplus. Two frames that overlap almost completely are one frame wearing two names."
- Fig 8 :46 "Composition crosses the boundary between them, and that surplus is where imports live."

So a gap is not empty space. It is where composing across two islands can produce something neither holds. Wide gaps are rare to cross and valuable when crossed. Triangulated.

**4. Where a gap falls is a reading, so it is derived, never stored and patched.**
- Fig 3 :18 "Where a given chain stops is a reading, never a property of the chain."
- Fig 6 :44, as above.

Gap widths and island boundaries are recomputed from the current graph after each settle or refusal. Triangulated.

**5. Speciation is a structural test, not a count of deviations.**
- Fig 12 :117 "isomer. Same atoms, different bond, different substance."
- Fig 2 :43 "a convention that decides an outcome has stopped being one."

"After X deviations" would make X a convention that decides the outcome. The 11-10 fold design already has the structural test: remove a defining part, or change the arrangement, and it is a new kind (orange to orange drink).

**6. Brightness counts only what the ground paid for.**
- Fig 2 :29-30 "If it moves when you push on it, it is not an anchor."

A bond counts toward island strength only where the board settled both ends together, scored by contrast (the tier-2 contrast fix from the 2026-11-13 planner retest). Bonds that only reflect co-use are excluded. Triangulated with Fig 9 :60.

## World (secondary; each source was read)

- **Learning theory: knowledge space theory (Doignon and Falmagne, 1985).** Items are ordered by prerequisites: "if a(⪯)b in this partial order, then a must be learned before b". The outer fringe of a learner's state is "what the student was ready to learn". (Knowledge space entry in [Wikipedia](https://en.wikipedia.org/wiki/Knowledge_space); [kst package documentation, Stahl and Hockemeyer 2022](https://anorien.csc.warwick.ac.uk/CRAN/web/packages/kst/vignettes/kst.pdf).)
  - **Predicts:** placement comes from the prerequisite order, and what to release next is the outer fringe.
  - **Corroborates** Tether lines 1 and 2. It also replaces the "release rate" in the earlier write-up with something cleaner.

- **Network science: Newman 2006, "Modularity and community structure in networks", PNAS ([arXiv physics/0602124](https://arxiv.org/abs/physics/0602124)).**
  - Communities are found by maximising "the quality function known as 'modularity'". It "can be reformulated in terms of the eigenvectors of a new characteristic matrix", which gives "a spectral algorithm for community detection".
  - **Predicts:** islands can be computed from bond weights alone, with no hand-drawn boundaries.
  - **Corroborates** the islands.

- **Spectral clustering: von Luxburg 2007, "A Tutorial on Spectral Clustering", Statistics and Computing 17(4) ([arXiv 0711.0189](https://ar5iv.arxiv.org/html/0711.0189)).**
  - Choose k "such that all eigenvalues λ1,…,λk are very small, but λk+1 is relatively large". "The larger this eigengap is, the closer the eigenvectors of the ideal case and the perturbed case are, and hence the better spectral clustering works". The heuristic weakens "the more noisy or overlapping the clusters are".
  - **Predicts:** a measurable gap width (the eigengap) that says how cleanly the islands separate, and how stable they stay as bonds change.
  - **Corroborates** Tether line 3. Mathematics even uses the name "spectral gap".

- **Sociology: Granovetter 1973, "The Strength of Weak Ties", American Journal of Sociology 78(6) ([text](https://smg.media.mit.edu/classes/library/granovetter.weak.ties/granovetter.html)).**
  - A bridge is "a line in a network which provides the only path between two points", and "all bridges are weak ties". "Weak ties are more likely to link members of different small groups", and they give "access to information different from that which we receive."
  - **Predicts:** the terms that cross a gap are few and weakly bonded, and they carry what neither island has.
  - **Corroborates** Fig 8 :46 (the surplus lives at the boundary).

## Verdict (from the figures): a clearer system, all of it derived

| Quantity | What decides it | How it is computed | When it changes |
| --- | --- | --- | --- |
| Stratum (vertical placement) | What the term is composed of | 1 + the deepest stratum among its parts (longest path in the parts graph) | Only when a new composition settles |
| Reachable (yes or no) | Derivation | Derivable under everything currently held (Fig 6 :44) | A part refuted makes it unreachable, by derivation |
| Search priority (where to look first; NEVER standing) | Depth and its weakest part | Order candidates by stratum and by their weakest part's own board record | A part refuted drops it down the order |
| Standing | Only the term's own record with the board | Paid bargains, and refusals, on its own row | Each contact |
| What is released next | The outer fringe (it sets priority, not standing) | Terms whose parts are all settled. The inherited priors count as the base layer (see the review's amendment) | Each settle moves the fringe |
| Island (horizontal neighbourhood) | Ground-paid bonds | EARLY: the existing kind and sense clusters and the ego networks (write-up [24](24-WATSON_2026-11-08_NAMING_THE_ORBIT_EGO_NETWORKS.md)). LATER, once the paid-bond graph can support it: communities by modularity over contrast-scored bond weights | Recomputed locally after a settle or refusal |
| How many islands are real | Cluster separation | The eigengap (von Luxburg's heuristic), as the test of whether computed islands are real at all | Rechecked as bonds settle |
| Gap width between two islands | Independence | Size-normalised separation of that pair: conductance, or the normalised cut (bonds crossing divided by the smaller island's bonds) | Widens when a bridge is refuted; narrows when a new bridge settles |
| Gap width between strata | Detail lost per crossing | Read off the board: the share of each stratum that settled | Each lineage, from the ledgers |
| New kind (speciation) | Core change | The 11-10 structural test: a part removed, or the arrangement changed | At the sighting that crosses it |

**Your question about "how big an environment is".** Size alone should not widen a gap. A big island has many internal bonds, so a raw count of crossing bonds would always make it look isolated. The measure has to be normalised by size, which is what conductance and the eigengap do. What widens a gap is how little two islands share, relative to how much each holds.

**The simplification.** Your picture has two axes, and each has one rule.
- **Vertically:** composition decides the stratum, and the fringe decides what comes next.
- **Horizontally:** paid bonds decide the islands, and independence decides the gaps.

Contact moves both only through derivation: settling adds, refuting adds a refusal, and every number is recomputed from what is held. Nothing is set by hand, so nothing goes stale.

**Pushback:** drop "after X deviations" for speciation. The structural test already exists, and a fixed X would be a convention deciding outcomes (Fig 2 :43).

## Amendments from the outside review (2026-11-13 17:55, adopted by Isaiah 17:57)

An outside review of this write-up and the README. All four fixes are adopted, plus its practical risk:

1. **Priority is never standing.** "Starting strength" read like a confidence value. It is now three quantities: reachable (yes or no, by derivation), search priority (where to look first: depth and weakest part set only this), and standing (only the term's own record with the board). If priority blurs into standing, the preload starts acting like knowledge.
2. **The parser's compressions are candidates, stamped with provenance.** This is recorded in the RDL write-up as C6. It follows Isaiah's line in write-up [33](33-WATSON_2026-11-09_TRANSCRIBE_BEFORE_COMPRESSING.md): the right to compress "only works when the agent fully understands the system".
3. **Islands start as the kinds already held.** Paid bonds will be sparse on ARC boards for a long time. Modularity on a sparse graph gives noisy boundaries, and it has a known resolution limit that merges small real communities. So the early islands are the existing kind and sense clusters and the ego networks from write-up [24](24-WATSON_2026-11-08_NAMING_THE_ORBIT_EGO_NETWORKS.md). Computed communities take over only when the bond graph supports them. The switch is gated by the eigengap test above, and its exact threshold is set in the design.
4. **The eigengap and the pairwise gap width are different measures.** The eigengap says how many islands are real. Conductance or the normalised cut gives the width between two particular islands. The table offered them as alternatives in one cell; it now gives each its own row.

**The practical risk: what counts as settled at the start.** Fringe release needs a base layer. If the inherited priors do not count, the fringe starts nearly empty: the same starvation write-up [10](10-WATSON_2026-10-31_DOES_IT_REMEMBER_WHAT_WORKED.md) records, where the mint parked with its budget exhausted in 58 of 66 parks. Decision: the inherited priors count as the base layer for release. Because release sets only search priority (amendment 1), seeding the fringe from the priors gives no term standing. This is decided explicitly here, and carried into RDL's T0 design.

**The review's order of work, adopted inside this future design:** RDL T0 with provenance stamps, then fringe release against release-all (cheap, decided in hours), then islands starting from the existing kinds. All of it still comes after the gates set after the 2026-11-13 hand test: perception first, then the agenda reader.

## Header

- **DECIDES (when built):**
  - Fringe release versus release-all, measured on wasted work and levels. If the fringe cuts waste with no lost levels, keep it; otherwise release everything.
  - Gap-crossing compositions should settle less often, but give more new reach when they do (Fig 8 :46). If they do, rank crossings first when search is stuck. If they don't, the gap is not where the surplus is for this board, so re-read the census.
- **HOURS:**
  - the parts graph and depth: hours;
  - islands by modularity: a day;
  - none of this before RDL's T0.
- **PRIOR CASE:**
  - the 11-10 fold design (the structural speciation line);
  - the 2026-11-13 planner retest (tier-2 counts that agree with everything, fixed by contrast);
  - Ouroboros v4's kind table.
- **ANALOGUE:** a school curriculum. The prerequisite order is the strata, subjects are the islands, and interdisciplinary courses are the bridges.
- **LIMIT:** at 10^6 terms a full eigendecomposition is too costly. Recompute locally: a correction reaches only what was built on that corner (general-agent README, "It learns by appending"). Modularity on a neighbourhood scales with that neighbourhood, not with the store.

**Cost if wrong:** low. Every number is derived and reversible.

**Reversed by:** fringe release or gap-ranked crossing showing no gain over flat release and flat ranking.

## Sources

- [Knowledge space (Doignon and Falmagne 1985), Wikipedia](https://en.wikipedia.org/wiki/Knowledge_space)
- [Stahl and Hockemeyer 2022, Knowledge Space Theory (kst documentation)](https://anorien.csc.warwick.ac.uk/CRAN/web/packages/kst/vignettes/kst.pdf)
- [Newman 2006, Modularity and community structure in networks](https://arxiv.org/abs/physics/0602124)
- [von Luxburg 2007, A Tutorial on Spectral Clustering](https://ar5iv.arxiv.org/html/0711.0189)
- [Granovetter 1973, The Strength of Weak Ties](https://smg.media.mit.edu/classes/library/granovetter.weak.ties/granovetter.html)
- Tether figures: docs/01-FOUNDATIONS/03-FIGURES_TEXT.md (Figs 2, 3, 6, 8, 9, 12)
