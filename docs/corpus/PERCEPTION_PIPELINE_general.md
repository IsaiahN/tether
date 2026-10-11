# The Perception-to-Persistence Pipeline

**A specification, codebase-agnostic. What a bounded agent must build to read a 2D grid the way a
person reads a page, act on it under a budget, and carry what it learns across plays and across
games without contaminating the transfer claim.**

Seven layers, each consuming what the one above produces. The order is a dependency order: nothing
in a lower layer can run until the layer above it exists, and the whole is a chain in the sense of
Figure 3, so it breaks at whichever layer is thinnest.

---

## Layer 1 — The frame as a change-tracked tree

**A frame is not an image. It is a tree of objects, one node each, held the way a document tree is
held.**

The agent does not re-read the whole frame each tick. A change detector watches the tree the way a
`MutationObserver` watches a document: it reports *what changed* between frames — a node moved, a
node's shape or orientation changed, a node's tracked attribute changed, a node appeared, a node
vanished. Every attribute the system tracks is a watched property, not only position.

**Animation is first-class, not discarded.** A single action may return several frames — the
animation between the before-state and the settled after-state. The detector runs across the whole
sequence, because a relation that forms and breaks mid-animation is invisible if only the settled
frame is read.

**This layer is the substrate for everything below it.** Color, objects, attributes, relations and
causality are all reads off this tree. Build it first or nothing else can run.

---

## Layer 2 — The reading pattern: a per-frame attentional prior

**Everything in the tree gets read. What this layer decides is the *order*.**

Humans do not read a page evenly. They read in a pattern, and the pattern is a codified prior:
absent in pre-literate children, emerging through adolescence, culturally reinforced. It is not
learned per game and it is not composed — it is carried in.

**The default is the F-shape:** a horizontal sweep across the top, a shorter horizontal sweep
lower, then a vertical scan down the left. It is the *default* precisely because it is what the eye
does when no strong cue pulls it elsewhere. The research is explicit: the F-pattern appears when
three conditions hold together — the content is a wall with little formatting, the reader is trying
to be efficient, and the reader is not committed enough to read everything.

**When cues are present, the eye follows them instead**, and other patterns take over:

| pattern | when it fires | what it reads |
|---|---|---|
| **F-shape** | default: no strong cues, efficient reader | top bar, shorter second bar, left stem |
| **layer-cake** | distinct headings/boundaries present | the boundaries, skipping the interior |
| **spotted** | looking for a specific feature | jumps to candidates, skips the rest |
| **marking** | tracking one locus while the field moves | holds a fixation as the scene scrolls |
| **bypassing** | repeated left-aligned starts | deliberately skips the shared prefix |
| **commitment** | high motivation | fixates almost everything |

**On a grid, these abstract to layout conditions** — a uniform field falls to the F-shape; strong
row or region boundaries invite the layer-cake; a salient target invites the spotted scan. The
abstraction rule is a design obligation: *the same layout under the same conditions must yield the
same ordering every time*, ablation or not. Distinct and consistent is the specification. An
80/20 split is acceptable — F by default, the others as conditioned fallbacks — provided the
fallback conditions are themselves consistent.

**Three properties are non-negotiable:**

- **Per-frame.** The layout can shift mid-episode; when it does, the eye re-prioritizes, so the
  pattern is recomputed every frame rather than fixed at level start.
- **Described, never composed.** A read-order for a frame not yet seen would be a guess, and on a
  procedurally-generated board a wrong one. The agent narrates which pattern it used and why, but
  never settles the ordering into a reusable term. It is a prior that runs fresh each frame and
  leaves no atom behind.
- **Load-bearing on action.** Ordering is not perception polish. Under a budget the first bet is
  the one that gets made, so the read-order can decide whether an action pays. It is part of what
  makes later budgeting correct.

---

## Layer 3 — Color as order-of-encounter, never as stored value

**Color separates objects into classes. The color value itself is disposable and must never be
stored as a transferable fact.**

The reason is that the palette is not stable across plays: a class green on one play may be orange
the next, and the game means the same thing. Color is being used to make objects *distinct*, and
distinctness is all that carries. So the raw value is cache-only, held for the length of one play so
the agent can tell two similar hues apart, and it never enters durable storage.

**Naming.** The visible spectrum, `R O Y G B I V`, is the one ordering humans share for color — the
one nobody states aloud (no one thinks *blue is color five*) but everyone accepts, and the only one
grounded in a physical continuum. Each new color the reading pattern encounters is placed on that
spectrum between the two anchors it falls between, and given an ID by band plus order-of-encounter:
the first color found between green and blue is `GB1`, the second `GB2`, and so on. Hues the
spectrum names poorly — cyan, magenta — are placed by their RGB coordinates against the values
already recorded, then given the same band-plus-increment ID.

**The ID is a filing position, not a rank.** `GB1` does not mean *greater* or *first in magnitude*.
It is the anchor a strategy is filed under, and its whole purpose is substitution: when the palette
changes next play, a brand-new hue that lands in the same band and role can be aliased onto `GB1`
and inherit everything already learned under it. This sits *beside* the fact that color is a label
— comparable, not ordered in any more-and-less sense — rather than replacing it. The label says
*these are distinct*; the position says *this is where the strategy lives*. They answer different
questions and do not conflict.

**The split at this layer:**

| cache only, this play | durable, if the play settles |
|---|---|
| raw RGB values | color IDs and their band structure |
| per-object live position | the groupings and relations keyed to those IDs |

---

## Layer 4 — Objects, groups, and subgroups

**Color makes the first cut. Structure makes the rest.**

Everything sharing a color ID is one group. Within a group the objects still differ — by shape, by
orientation, by their relations to each other — and those differences subdivide the group into
subgroups. Groups and subgroups are tracked both as individuals and as classes.

**How a class behaves is itself data.** Whether the members of a group move together or respond
individually to a board event distinguishes a coordinated class from a set of individuals that
merely share a color. That answer is recorded per object, per group, and per subgroup, and it is
relational information the next layers consume.

---

## Layer 5 — Attributes, relations, causality: tracked in real time

**Every object carries the full attribute set. Where an attribute cannot be read, it is null — not
absent.** Null records *the instrument could not see it here*, which is a different claim from *the
thing is not there*, and the difference matters downstream.

The change detector polls every watched attribute each frame — not only position, but shape,
orientation, and the rest. Appearance, disappearance and transformation are routed to a causality
tracker that runs in real time alongside the attribute tracker.

**Settled change triggers the lookup.** When an object's attribute changes settle for a frame, that
settling is the event that fires retrieval: the changed attributes become the key, and the key
returns candidate atoms and candidate recipes. This is the seam where perception hands off to
reasoning, and it can only name what the perception layers publish — so a thin relation vocabulary
here caps everything the agent can look up, however large its library.

---

## Layer 6 — The action loop: budget-sized bets and corrected predictions

**All of the above happens before the first move.** The agent looks up candidates, forms a
hypothesis, and sizes the bet against a budget.

**The budget is a spendable quantity with a ceiling the agent does not yet know.** It runs on a
placeholder ceiling until experience lowers it, and it sizes bets accordingly — a cheap hypothesis
is tried, an expensive one is weighed. The budget is a *gradient*, a difference that can be spent,
not a conserved quantity; it depletes in one direction and never refills within a play.

**Every action carries a prediction, and the prediction is checked against the outcome.**

- *Predicted five actions to reach a cell; one sufficed.* The gap is a signal. The agent inspects
  the animation between before and after and asks what property it missed — the surface slides. It
  updates its model of the surface and re-sizes every future bet.
- *Predicted a clear path; the move stalled.* The agent returns to the animation and asks what
  intervened — a node it did not account for, a new object, a vanished one, an object that turned
  from pass-through to solid mid-move. It must name the blocker and the condition before it can
  adjust.

**All of this is real-time, off the tree from Layer 1.** The prediction-outcome delta is the loop's
learning signal at the action scale, distinct from the residual at the perception scale.

---

## Layer 7 — Persistence, recall, and cross-game import

**A play that ends is filed under a structure it computes, never under an identity it is handed.**

**Identity by computed hash.** The agent derives a hash from the game's own structure — the
distinctive groupings, the attributes, the shape of the game and not its colors. It checks the hash
against durable storage and cache for a collision, then keys the play under it. A prefix of the
hash is sufficient for a compact key provided the prefix is collision-checked before use.

This is the opposite of reading an identity the environment supplies. An agent that keys on a
given ID appears to learn and is only doing lookup, and scores zero the moment identities are hidden
or new — which is the private, out-of-distribution case that matters. **A hash derived from
structure survives exactly that case, which is why it is recall and not contamination.** The line
is precise: *a persistent key the agent reads from the environment is contamination; a persistent
key the agent computes from structure is recall.*

**Storage shape.** Keys are `HASH _ episode _ level`. Plays of one level stack by episode:
`h_1_1`, `h_2_1`, `h_3_1`, and so on. A new level starts its own stack under the same hash:
`h_1_2`, `h_2_2`. Grouping is by hash first, then level, then episode order, so one level's data is
never confused with another's.

**Reset with palette swap.** On reset the agent keeps its cache. If the structure is unchanged but
the palette has rotated, it reassesses the new colors against the groupings that did not change and
aliases them onto the existing IDs in place. The *type* of read is stable because the board type is
stable. This is the color-swap survived by filing under structure rather than under hue.

**Lossy stacking across levels.** A later level uses an earlier one, but lossily — it carries
similar patterns and adds new ones. The earlier plays are residual the new level composes against,
the way solute already in a container is not removed when more solvent is added, only diluted. The
prior levels' strategies remain available at reduced strength.

**Cross-game lookup.** When stuck, the agent searches every stored game's scenarios for a matching
shape. The current game's own data weighs highest. If the agent has exhausted its own game's
strategies and is low on confidence, and a strong match surfaces from another game, it may import
that as a low-priority test — carried with provenance, tagged by the source game and hash, so the
borrowing is always traceable and always subordinate to native strategy.

**What never enters durable storage:** the raw color values (Layer 3), and any identity the
environment handed the agent (Layer 7). Everything else — structure, strategy, deltas, provenance —
is what makes the transfer claim demonstrable rather than a replay.

---

## The chain, and where it breaks

```
1  tree                         the substrate; everything reads off it
2  reading pattern (prior)      picks the encounter order, per frame, described not composed
3  color IDs                    numbered by that order; value cached, ID durable
4  objects / groups             color splits, structure subdivides
5  attributes / relations       tracked per frame; settled change triggers the lookup
6  action loop                  budget-sized bets, predictions corrected against outcome
7  persistence                  hash by structure, stack, recall, import with provenance
```

Each layer consumes what the one above produces, so the whole is a dependency chain. It is only as
strong as its thinnest layer, and a reading taken below a thin layer is a reading of nothing: if the
relation vocabulary at Layer 5 is one relation of many, no richness at Layers 6 or 7 rescues it,
because the lookup they depend on can never name what Layer 5 never published.

**Three claims in this specification rest on rulings rather than on the specification itself:** that
the reading pattern is a prior rather than something reached (Layer 2), that color's ordering is a
filing position beside its label rather than a magnitude (Layer 3), and that a computed structure
hash is recall rather than the contamination the firewall forbids (Layer 7). Each is stated here as
resolved; each is a place a reader may reopen.
