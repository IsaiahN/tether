WATSON 79 — the relations/attributes library is the substrate the extraction must feed (2026-11-24)

ISAIAH'S CORRECTION (verbatim): "dont forget relations.md and attributes, thats literally what it was
for......... and that powers search or should....." This corrects my D3 framing: I used source_of for
the causal unit but did not connect extracted human effects to the relations/attributes vocabulary
that the search operates on.

## SEARCHED — the substrate is live, read this turn
- library/given.json 12 MB, relations.json 20 MB, index.json 3.6 MB, ATTRIBUTE_INDEX.json 0.8 MB,
  vocabulary.json 5.9 MB. All present.
- docs/03-DESIGN/02-LIBRARY_RETRIEVAL.md:437-443: "a solution may test our instruments and measure
  how far the agent got; it may never decide what the agent is given. Instruments are built from
  RELATIONS.md / ATTRIBUTES.md for every board -- never from one game's answer." And
  "RELATIONS.md's own line -- computed from the board is perception; composed from other sensors is
  the agent's job."
- composer.lookup(described) (composer.py:504) searches the library by a DESCRIBED residual;
  lookup_query/lookup_iter/lookup_junctions are its variants.
- ATTRIBUTE_INDEX.by_cluster (tether.py:3346, rdl_parse.py:35) maps readings to clusters; _topk
  (tether.py:8949) ranks candidates by those tiers; _cat_load (tether.py:8892) loads them.
- relations.json is the ConceptNet vocabulary (CapableOf/ReceivesAction); TETHER_RELATIONS_READ
  merges it into affordance priors (affordance.py:26-32).

## FIGURES (verbatim, verified earlier)
- Fig 4: "Only head starts come down" / "a head start, never a recording."
- Fig 9: "describe it before you go looking, or any frame you pick will seem to fit."
- Fig 5: "mint φ if the description length pays"; "the candidates are ENUMERABLE rather than intuited."
- Fig 10: "What a seat may author is a question whose answer is unmeasurable before the run."

## VERDICT / CORRECTION TO THE BUILD
An extracted human effect that stays as a ledger row is inert. To become something the agent can
find, it must be DESCRIBED in the same vocabulary lookup searches over: the relation/attribute kinds
from RELATIONS.md/ATTRIBUTES.md's successors (given.json kinds, ATTRIBUTE_INDEX clusters,
relations.json relations). Then a dependency learned from the trace is a described query that
composer.lookup can return, priced by the ordinary bargain — never a handed composition.

The extraction pipeline therefore has FOUR stages, not three:
1. causal unit: source_of groups changed slots into incidents (WATSON 78 D3);
2. invariant core: conditions present in every trace where the incident occurs (WATSON 76 D1);
3. DESCRIPTION: name the incident and its core in the library's relation/attribute vocabulary, so
   it is a findable described residual (this WATSON, Isaiah's correction);
4. credit: pass/fail for enumerated candidates, closeness for novel compositions (WATSON 76 D2).

Stage 3 is the piece I had omitted. It is also the correctness check: if a learned dependency cannot
be described in the shared vocabulary, it cannot be found by search and is a recording, not a
head start — which is exactly what the membrane (Fig 4) forbids crossing down.

FIGURE CENSUS: Fig 1 · Fig 4 · Fig 5 · Fig 9 · Fig 10 (verbatim). Strained: none.
Anchor: library/*.json sizes; composer.py:504 lookup; tether.py:3346/8949 ATTRIBUTE_INDEX/_topk;
02-LIBRARY_RETRIEVAL.md:437-443; Isaiah's correction this turn.
