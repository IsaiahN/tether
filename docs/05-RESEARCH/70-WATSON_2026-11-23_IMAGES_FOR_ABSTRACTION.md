WATSON 70 — images + WordNet/ConceptNet/VerbNet as a substitute for embodiment in abstraction (2026-11-23)

ISAIAH'S IDEA (verbatim intent): humans abstract — they turn stick figures into meaning, see Pac-Man
and Galaxian as the same kind of thing. Part of that ability comes from existing in the real world
and building causal models of objects, their attributes, their functionality, and the interactions
between self and others. The agent is not embodied yet, so the hope was: real-world images + WordNet
+ ConceptNet + VerbNet could give it abstraction anyway.

## QUESTION (effect terms)
Can images plus lexicons give a non-embodied agent abstraction, and is that what the ImageNet cache
was for? What would actually have to be true for it to pay?

## DOMAIN CENSUS
- R: arity = (frame, object, attribute, bond, ground); symmetry = recognition maps many images to one
  class (lossy, one-way); scale = one frame vs a lifetime of causal models.
- **embodiment (human)**: actors = body + world; currency = sensorimotor prediction error; anchor =
  survival. Builds causal models by acting and being wrong. (upstream — the source of the ability)
- **the agent's umwelt**: actors = objects + typed slots; currency = residual; anchor = RLVR. Sees
  "not a picture, a tree" (WHAT_THE_AGENT_SEES:11) — segmented objects with placement/name/shape,
  never pixels. (mid)
- **image + lexicon route**: actors = a screenshot + WordNet/ConceptNet/VerbNet; currency = class
  name / synset; anchor = the external corpus. (downstream head start)
- order (Fig 3): perception → vocabulary → objective → planning. The image route is DOWNSTREAM of
  perception: it can only feed a perception path that can already turn a frame into objects.

## TETHER (primary, verbatim, verified)
- Fig 4: "Going up throws away detail; that is what makes the result reapplicable." "A recording
  carried upward looks like knowledge and is a description of one occasion." "So take the round trip
  and measure the gap." -> abstraction IS the membrane round trip: throw away detail, carry the
  method, bring it back and measure. The agent ALREADY does this on grids (colours -> names ->
  placements -> shape atoms; "the strategies are reachable because the structure matched, not because
  the colours did", WHAT_THE_AGENT_SEES:231). That is the stick-figures-to-Pac-Man move, done on slots.
- Fig 4: "The level a method lands on remakes it. A seed carries no small tree: it carries what will
  grow one, and the conditions it lands in decide what it becomes." -> a class name is a seed, not the
  causal model. It becomes abstraction only in a habitat whose ground pays it.
- Fig 6: "An instrument is not built from a description. It is improved from a worse instrument already
  returning something." / "instruments extend what can be represented at all." -> images are an
  INSTRUMENT for the perception layer, and the layer must already return something to extend.
- Fig 11: "capability is a property of agent-and-habitat." -> the ability is not in the images; it is
  in agent+habitat. No picture-bearing habitat = no capability, however good the recognition.
- Fig 1: "The ground enters as the only metric." -> a class name that never changes a decision is not
  knowledge; it is a row.

## WORLD (secondary corroboration)
- The analogy is right about HUMANS: abstraction from sensorimotor causal models is the embodiment
  literature's grounding claim (Barsalou, grounded cognition; Glenberg, embodied cognition) — concepts
  are built from perception and action. Corroborates Fig 4's round trip and Fig 11's habitat claim:
  you cannot get the model from the label; you get it from acting and measuring the gap.
- The project's OWN prior verdict (WATSON 44, 2026-11-20) already demonstrated ImageNet->AKAZE->synset
  end to end (6 classes, 2.18 MB, zero abstentions), then stated: "real boards still carry no picture
  field so the route remains inert in the live task." The mechanism works; the habitat is absent.

## VERDICT (from the figures)
Your theory is CORRECT about what abstraction is and why humans have it, and the images+lexicons idea
is the right KIND of head start — Fig 4 licenses it: a class name + synset + WordNet/ConceptNet/VerbNet
priors are a head start (a seed), never a recording of an answer. But the route is inert for a precise,
figure-derived reason: the agent's umwelt is typed object slots ("not a picture, a tree"), and no live
board carries a picture field. The ImageNet cache gave the agent a recognition instrument and a
vocabulary — a seed — but no habitat in which that seed is pressed by the ground. That is WATSON 44's
"inert" and Fig 11's "capability is agent-and-habitat," not a Missing feature to add.

For the idea to pay, THREE things must all be true (conjunction, Fig 8 union):
1. a picture-bearing habitat (real problems: a screenshot whose objects the agent must act on);
2. a perception bridge from image -> the agent's typed slots (the Phase 2 design names this exactly:
   sprite-grouping, HUD-crop, scroll handling — an instrument improved from arc_percept, Fig 6);
3. ground that pays the class reading: the recognised class must change a bet or a bond that the
   board then settles. Without (3) it is a row, not knowledge (Fig 1).

So the cache was not wasted in INTENT — it was the right head start — but it was bought before the
habitat existed, so it has paid ZERO capability so far and its 153 GB is re-downloadable while the
derived part (0.9 MB WordNet lexicon, the builder, the recognition path) is already committed. The
right moment to spend that 153 GB is when (1) and (2) exist; until then it is a seed with no ground.

**Carry the method:** a head start (vocabulary/instrument) is only worth its download when a habitat
exists to press it — Fig 4's seed needs conditions to land in. Buy the instrument with the habitat,
not before. This corrects the timing of the ImageNet purchase, not its logic.

**Cost if wrong:** deleting the cache now costs nothing live but loses a re-download if a picture
habitat appears; keeping it costs 153 GB of disk that has already caused a real outage indirectly (the
disk filled to 0.2% and killed the training sweep). **Reversed by:** a picture-bearing habitat reaching
the agent with the perception bridge built — then the ImageNet class memory would be activated and
measured against the ground, which is the first honest test of whether it buys abstraction.

FIGURE CENSUS: Fig 1 · Fig 3 · Fig 4 · Fig 6 · Fig 8 · Fig 11 (verbatim). Strained: none.
Anchor: WATSON 44:103-133 (ImageNet demo + "inert"); WHAT_THE_AGENT_SEES:11,231 ("not a picture, a
tree"; "structure matched, not colours"); Phase 2 design (sprite-grouping/HUD-crop/scroll, first
buildable piece); affordance.py:39-41 (class memory OPTIONAL, env-gated).
