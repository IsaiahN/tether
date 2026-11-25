WATSON 78 — D3 decided: one effect = one causal source, not one region (2026-11-24)

ISAIAH'S ANSWER (verbatim substance): asked whether a frame's simultaneous changes are one event or
several, he refused the spatial framing: "its a matter of perspective... in a house fire, do all of
the reactions that occur due the fire count as separate events or as one?... it looks like only one
event caused all the trouble and in truth it was the inciting event, even if there were chain
reactions that made it worse that they were unaware of... the real question is if they have any
relationship with each other casually or if it was coincidental and or nonconsequential. sometimes
aspects or features are being shown for you to draw a relationship, othertimes its window dressing or
to help you establish placement and establish setting... 'is that one event' = is there one agent
present? or are their several independent beings, mechanisms etc, that not only can work
independently but where working independently and happened to coincide? this is lowkey a
triangulation/alignment/drift problem or anchor type problem that figure 2 answers." Then: "in terms
of causality if the main focus is one agent or object, all that will matter is did they incite the
incident were they involved directly or indirectly or did they have anything to do with it."

## FIGURES (verbatim, verified in earlier WATSONs)
- Fig 2: "An anchor is whatever settles the question and does not change its answer because of what
  any frame thinks" and "agreement about the world is worthless when the agreeing frames share an
  evidence pool"; "Frames range against the ground. They do not negotiate with it."
  -> from inside the frame, a coincidence and a causal chain are indistinguishable; only an outside
  anchor separates them. Isaiah is right that this is Fig 2.
- Fig 1: "The gap is measured per object, not per step. A system that averages across objects has
  thrown away the only signal that says where to look."
- Fig 10: "a candidate set chosen by a participant is an authored room however well the selection
  is reasoned."

## SEARCHED — the mechanism already exists
`tether.py:3497 source_of(ag, slot) -> (src, first_bind, gain, n)`: "WHO the slot's change depends
on." Candidate order (line 3501-3502): "my action, then each slot of each object in contact with the
owner, then the next ring out." Verdicts (3503-3504): SELF (my action closes every row), COUPLED (my
action partly), BY:<kind> (another object, direct/indirect contact ring), OWN (the slot's own past),
HIDDEN (nothing gains). Decided by leave-one-out information gain (3517-3545), i.e. by an anchor,
not by spatial proximity.

## VERDICT — D3 as a rule, fixed before the inference run
The unit of an effect is a CAUSAL SOURCE, from `source_of`, not a region, colour or whole frame.
- Changed slots with the same inciting actor/source are ONE incident (the fire and its chain
  reactions are one event: the inciting event plus everything that depended on it).
- A changed slot whose source is HIDDEN or OWN is not part of that incident: it is coincidental,
  window-dressing, or its own clock. It is discarded from the dependency core.
- "Incited / involved directly / involved indirectly / unrelated" maps exactly onto
  SELF/COUPLED / BY:<contact ring 1> / BY:<ring 2> / HIDDEN.
This also dissolves WATSON 77's HUD problem: the score tick is a slot whose source is OWN or HIDDEN,
so it is excluded by causality, not by a guessed row band.

## CONSEQUENCE FOR THE BUILD
The extractor should NOT partition by connected components, colour, or bounding box. For each
changed slot it should record `source_of`; group slots by (source, inciting actor) into one incident;
and exclude HIDDEN/OWN slots. The invariant-core count (WATSON 76 D1) then runs over incidents, not
frame boxes. Nothing new is invented: source_of is a built, reached mechanism and this is a reuse.

FIGURE CENSUS: Fig 1 · Fig 2 · Fig 10 (verbatim). Strained: none.
Anchor: tether.py:3497-3554 source_of; probe_hud.py measurement; Isaiah's D3 answer this turn.
