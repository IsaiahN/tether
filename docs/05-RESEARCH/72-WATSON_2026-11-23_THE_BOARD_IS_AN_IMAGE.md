WATSON 72 — "the board is already an image": frames, motion, and the unused image route (2026-11-23)

ISAIAH'S POINT (this turn, correcting WATSON 71): humans think not only in words but in images and
video, and can generatively imagine and synthesize visual strategies, drawing on a compiled,
compressed library of objects, relationships, attributes and abilities. Then: "the game itself —
while the ARC is given as pixels and code, they are 'images' still. Perhaps the agent just needs to
see them as such. That's what 'frames' are anyway. Frames over time depict motion."

## QUESTION
Is there an image route in the agent that is simply not connected to the frames it already gets?
Is Isaiah's "see the board as an image" the missing bridge, rather than buying more images?

## SEARCHED (write sites + measurements, all read this turn)
- `affordance.is_picture` (affordance.py:456-465): uint8 array, 2D/3D, >= PICTURE_MIN_SIDE=16.
  Measured this turn: a 20x20 or 30x30 board PASSES; 5/10/15 do not. ARC boards are valid images.
- `affordance.pictures` (affordance.py:468-481): reads ONLY a field named `picture`/`image` in obs,
  or `<object>.<picture>`. No such field on ARC/gridworld boards.
- `recognize.recognise_shape` exists; shipped shape memory `library/shapes/memory.npz` 72,854 B.
  This is the DEFAULT route ("recognise_shape over the repo-relative shape memory" — affordance.py:36-38),
  NOT the ImageNet class memory. It maps a picture region to a shape_name.
- Measured: **zero `recognised` rows** in the proving_1800 ledgers — the image route never fires on boards.
- gridworld.observe() returns a flat typed dict: o0.row/col/colour/shape, o1..., and NO pixel board key.
  The native habitat does not expose an image at all; the ARC path exposes pixels but the perception
  layer (arc_percept) converts them to objects/slots ("not a picture, a tree", WHAT_THE_AGENT_SEES:11)
  before any decision.
- `lookahead(state, actions, predict, gap, more)` (tether.py:4239) + `_lookahead_act` (17263): the agent
  ALREADY has a generative simulator — breadth-first over SEQUENCES of intent units, predicting the
  next typed state and ranking by gap, returning the first unit of the best sequence. This is the
  "imagine a strategy" loop, run over typed states, never rendered as pixels.
- `arc_percept` frame-to-frame observer: dh/dw/dcells/colour_changed, add_n/rem_n, break detector —
  "two frames, one field, no shared reading." That IS motion read from frames over time.

## DERIVATION (figures, verbatim, verified)
- Fig 1: "perceive · plan · act · predict" / "The ground enters as the only metric." -> prediction
  is a first-class step; a generated image would need ground to pay it (Fig 1).
- Fig 5: "the prediction gap"; "it composes from what we already have"; "A frame searching for an
  answer of a particular shape holds that shape as a PREFERENCE rather than as a term" -> the agent's
  generative medium is the typed gap and the held shape preference — lookahead simulates typed
  states, not pixels. That is "imagination" in the figures' own terms.
- Fig 4: "Going up throws away detail; that is what makes the result reapplicable." / "the round trip"
  -> converting pixels to slots IS the upward abstraction; frames-over-time-motion is read in the
  typed space (deltas), not by re-rendering images.
- Fig 6: "An instrument is not built from a description. It is improved from a worse instrument already
  returning something." / "instruments extend what can be represented at all." -> the image route is
  a built instrument that ALREADY returns something (recognise_shape on the shipped memory) but is
  never CONNECTED to the board frames. That is exactly a Fig 6 "extend from an existing reading" case,
  not a new capability.

## VERDICT
Isaiah is RIGHT, and WATSON 71 under-credited him. The gap is not "reasoning in images" (which would be
a category error) and not "buy more images." It is a CONNECTION: the agent has a working image
instrument (recognise_shape + 72 KB shipped shape memory) and the frames are already flowing through
it, but the observation exposes typed slots, not a `picture` field, so the route reads zero rows.
Seeing the board as an image would mean exposing the current board as a `picture` observation so the
existing recogniser can name its shape — a Fig 6 extension of a reading that already returns something.

What this would change (and what it would NOT):
- It would give the agent a SECOND description of the same board: typed slots (what it has) PLUS a
  shape class from the AKAZE memory (what the image route returns). Fig 2: two frames of the same
  object with low overlap — corroboration only if independent; here they share the same pixels, so
  agreement is one evidence pool. The surplus (Fig 8) would be whatever the shape reading says that
  the slots do not — e.g. recognising a configuration as "the same shape" across recolouring/scale,
  which is precisely the abstraction Isaiah describes.
- It would NOT make the agent reason in pixels or render imagined images. Lookahead already simulates
  strategies in typed states; the image route adds a reading, not a new medium.

The honest caution (why this is an experiment, not a decree): every vocabulary widening measured in
this record has been inert ("adding readings without moving reach", INDEX:36134). A shape class is a
reading; it pays only if a bond or bet that uses it settles differently on the ground (Fig 1). So the
right next step is a PRE-REGISTERED A/B: arm that exposes the board as a `picture` field, OFF
byte-identical, then measure whether `recognised` rows appear AND whether any decision/ground result
moves. If the shape reading is inert, that is a clean null and the instrument stays a record. If it
moves reach, it is the bridge Isaiah intuited, bought with data already in hand.

**Cost if wrong:** a shape reading that adds a row but no reach -- measured, withdrawn, no capability
claim. **Undoable:** yes, an arm. **Reversed by:** a per-game ground result showing the `recognised`
shape reading changes a bet/bond and moves clear/reach, OFF byte-identical.

**Carry the method:** before buying a new instrument, check whether a built instrument is disconnected
from a signal already flowing through the agent. Here the images were always there; only the field name
separated them.

FIGURE CENSUS: Fig 1 · Fig 2 · Fig 4 · Fig 5 · Fig 6 · Fig 8 (verbatim). Strained: none.
Anchor: affordance.py:456-481 (is_picture/pictures gates, measured); recognize.py (recognise_shape);
library/shapes/memory.npz 72,854B; proving_1800 zero recognised rows; tether.py:4239/17263 (lookahead);
gridworld.observe() typed dict, no pixel key; INDEX:36134 (inert widenings).
