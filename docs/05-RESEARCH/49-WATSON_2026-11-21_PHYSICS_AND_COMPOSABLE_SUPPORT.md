WATSON — does the agent understand physics, and can/should it compose it? (2026-11-21)

PROMPT: Isaiah — "Since we have our shapes loaded by default with akaze, do we have the core
concepts of balls roll vs blocks stack? ... by blocks stack, it should really be more general
like anything 3d with a flat surface or anything 2d with a straight edge can stack or be at
rest on that face ... unless acted upon or it has its own autonomy/clockwork. ... does the
agent understand physics of motion, force, etc and can it be taught to understand these things
in a way that it composes? Should it?"

Three questions, unbundled (Fig 9 :5 split, do not search): (A) does it have the concepts today;
(B) can it be taught to compose them; (C) should it. Read-only audit at the write sites; every
claim quoted. The figures decide, the agent's own evidence is the means.

===============================================================================
A. DOES IT HAVE THE CONCEPTS TODAY? — NO (measured, all arms ON)
===============================================================================
Shape→concept bridge (word_map.json, 6 declared rows; header :468244 "a DECLARED CONVENTION
... not derived"):
- `disc/disk` → `sphere` → **ball**, verbs hit/throw/kick/play/bounce/push/roll. The gloss even
  contains "the ball rolled into the corner pocket" (:550430) — but that string is NOT an action.
  "roll" reaches ball only through ConceptNet `CapableOf roll` → collapsed to the single
  reading **"moves"** (relations.json:10018; affordance.py:104-113). It is a narration label
  after the fact (`"rolls" if ... else "glides"`, affordance.py:138-144), not a physical model.
- `square` does NOT reach block: runtime `resolve('square') → AGENT|is_square` via SHAPE_ATOMS
  (no form). Recognised 3D `cube` likewise falls through to `AGENT|is_square`.
- **`block` resolves to nothing** — its `actions: []` (word_map.json:550557); `stack` sits under
  a different bridge (`box→stack UsedFor`) and UsedFor is excluded by policy (affordance.py:103).

Physics readings present and composable: contact / contact_faces (arc_atoms.py:133), speed
(Chebyshev magnitude, arc_percept.py:1183), `stability` (CONSECUTIVE FRAMES UNCHANGED,
:1195-1208 — a frame counter, not mechanical support), solid, orientation, girth, perimeter,
density, holes (sensors_heavy.py:107-164), touch/dcontact pair transitions (observer.py:82-107).

Physics readings ABSENT: support / rest / stack / flat / face / force / accel / inertia /
momentum / gravity / tilt. `relations.py:257` — `"HUMAN|Support": ("unbound","no support
reading")`. `contact_kind` (face/edge/point with "point→pivoting, edge sliding, face pushing")
is explicitly **"SEAT-SIDE AND NOT AN ATOM"** (arc_percept.py:721); it shares 4-adjacency for
the reason `touching` gives. It is System-0's enumeration, not a term the composer can bind.

So: the agent can say *"this was named ball, it moved when pressed, it kept moving / did not."*
It cannot say *"this has a flat face, therefore it can rest or be stacked on."* **Verdict: a
flat per-object hint table (3,577 WordNet priors + ConceptNet verbs, every readable one
predicting "moves"), never a derived generic rule.** `block` — the obvious stacking concept —
resolves to nothing at all. The "balls roll / blocks stack" pair is NOT present even as priors.

Staleness found (question 0-3): `word_map.json:468238` `"readers": [] ... "NOTHING in the
agent reads this file"` and `relations.json` header `"readers": []` are BOTH FALSE — tether.py
imports affordance (:33) and calls load_sources/resolve (:27072,:27092). Another stale record.

===============================================================================
B. CAN IT BE TAUGHT TO COMPOSE IT? — YES, and the means are already in the library
===============================================================================
Fig 13 :8-12 names space and time as two of the six kinds; :73 "Everything else is a
composition across the two kinds"; :109 "each composition becomes an atom for whatever
composes over it"; :114 "The set is closed. The arrangements are not." So **no new kind and no
new sense are needed** — the ingredients (contact, time/stability, speed, solid, geometry) are
already published atoms. This is a missing published reading and bond, not a closure wall.

Fig 9 :29-31: describe the residual in effect terms before looking — *"an object whose lower
face has contact with another object and whose cell set is unchanged across frames."* Do NOT
promote a WordNet row ("box UsedFor stack") to the verdict: that is a recording, and Fig 4
refuses recordings crossing the membrane ("Only the actors, the currency and the anchor
change"). Only METHODS cross. The method here is the composition itself.

Fig 11 :38-39,47,60-61: capability is agent-and-habitat; contact decides; "you do not invent
the list, you read it off the world"; introduction (never subtraction) is the available move.

The smallest composable path:
1. publish `contact_kind` WITH a beneath/above direction as a RELATION atom — it is currently
   seat-side and undirected (the one genuine instrument gap; Fig 6's entry rule licenses
   improving an instrument already returning something that fails to resolve).
2. compose with the existing `stability` (unchanged cells) and `speed` (arc_percept.py:1183).
3. one priced bond: `face-contact_below ∧ stability>0 → supported/resting`, settled by the
   board; the agent's existing "keeps moving" test (tether.py:27142-27162) is its natural
   refuter. Flatness comes free from solid/girth/perimeter/orientation (sensors_heavy.py).

"Anything 3D with a flat surface or 2D with a straight edge can rest" is then a GENERIC
composition over geometry, not eleven per-object priors — exactly Isaiah's point.

===============================================================================
C. SHOULD IT? — YES to the means, NO to the answers. My judgment, figure-derived.
===============================================================================
- NO: do not hand "balls roll / blocks stack" as priors. Those are recordings (WordNet/ConceptNet
  rows) and would encode the answer — Fig 4 refuses them, and the ablation (terminal condition
  clause 4) would be blind to the cheat. "block" as a preloaded concept with `stack` attached is
  precisely the answer-shaped gift that transfers to nothing.
- YES: publish the directional face-contact reading. That is a MEANS (Fig 6), frontloadable
  under the inheritance rule — it lowers the agent's distinction horizon and changes contact
  (Fig 11). The agent must then COMPOSE "supported" itself from the board's evidence; we supply
  the vocabulary and the instrument, never the sentence.
- The general principle ("object at rest stays at rest unless acted upon or self-driven") is
  NOT to be installed as a rule. It is the SHAPE of the bond the agent should derive: the
  "keeps moving" test is its refuter — a press, then a step with no new press; if motion stops,
  rest was the default; if it continues, something (autonomy/clockwork) sustains it. That is a
  testable composition, not a handed axiom. This also answers "unless acted upon or it has its
  own clockwork": those are the two ways the test's condition fails, both observable.

ACTION TAKEN: research only. No code, no prior, no new sense installed. The bond above is a
proposal to be derived at the write site with its own WATSON and must-fail test before any build;
the ground (an OOD board where face-contact + unchanged actually predicts a settle) decides.
The 1800s proving run is the wrong surface to tune it on — no pooling, no game identity.

FIGURE CENSUS: Fig 1 claim/mode · Fig 2 cost-of-being-wrong · Fig 4 methods-only membrane ·
Fig 6 instrument entry rule (improve from a worse reading that fails to resolve) · Fig 9
describe-effect / one-pass / recordings-not-verdicts · Fig 11 contact / introduce-never-subtract /
read-the-list-off-the-world · Fig 13 closed kinds / open arrangements / composition becomes atom.
Strained: none.

Sources: read-only code audit at tether.py, affordance.py, arc_percept.py, arc_atoms.py,
sensors_heavy.py, observer.py, relations.py, library/word_map.json, library/frame.json —
verified at the write sites on 2026-11-21.
