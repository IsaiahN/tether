# An ARC game, from the agent's side — as the build produces it

**A rewrite of `library-closure/ARC GAMEPLAY - WHAT THE AGENT SEES.md`, telling what this build
actually produces after ten seams and three items of deliberation. The original is corpus and is left
untouched; this is the working version, and `STORY_PROOF.md` is the line-by-line reconciliation.**

---

## Before the first move

**A frame arrives. Not a picture, a tree.** The agent sees a structure of objects, each one a node with
its own attributes, and it holds them the way a browser holds a DOM. Every same-symbol region is a
node, including the one that looks like background — *nothing is assumed to be scenery*. That costs it
slots and it refuses an assumption, and the agent may learn later that some colour behaves like a
floor, which is a thing it earned rather than a thing it was handed.

**It watches for change, and it names the two kinds apart.** Between one settled board and the next
there is a **transition** — a node moved, an attribute changed, a node appeared, a node vanished. Inside
a single action there may also be a **cascade**: the chain of frames one press set off, where A moved
and *then* B reacted. **The transition is what it bets against. The cascade is what it learns the
mechanism from.** Reading only the settled board would throw away the ordering, and the ordering is the
only place *what caused what* is legible. On some boards there is no cascade at all — one frame per
action, always — and there the agent learns the *what* and never the *why*, and can say so.

**And it reads the tree in an order, not evenly.** Everything gets read; the order is what the reading
pattern decides, and it is recomputed every frame because the board can shift mid-episode. The agent
narrates the order it used and why, and **it never saves that order as a term** — a read-order for a
frame it has not seen would be a guess, and on a procedurally generated board a wrong one. It is a
description that leaves no atom behind.

**When no pattern fires, it falls back to something it earned.** Its own record of unexplained mass, per
slot: *look first where the model has been most wrong.* That is not carried in from anywhere. It is
the residue of every bet it has lost, used as an ordering.

## Naming what it sees

**The first distinct colour it meets is not written down as a colour.** The agent knows the palette is
disposable — this object is one hue now and another next play, and the game means the same. What it
records is a **placement**: a slot in a shared, monotonic sequence, the *n*th distinct colour it has met.
The next distinct one is *n+1*. **The number is the order of the read, and nothing else.**

**And the placement is not the object's name.** That is the thing this build is strictest about. The
placement is a **value** — a position another object can hold at another time, on another play. The
object's name is a **pointer**, assigned once and never reused, and it is not a colour at all. An
object that changes colour keeps its name; an object that arrives later can take a placement an earlier
one has left.

**The raw value stays in cache, and it works for its keep all play.** It is not held merely to tell two
similar hues apart at first sight — it is the key the grouping runs on. Every time an object changes
colour or a new one appears, the agent compares the actual value against everything it has recorded to
decide where the new one sits and whether it joins a group that already exists. **The value is the
grouping key during play; the name is the identity key across play.** At the boundary the values go and
the names stay, and that is not housekeeping — **the losing is the mechanism.** What survives the loss
is what transfers.

## Grouping, and who moves with whom

**Colour makes the first cut; structure makes the rest.** Everything sharing a placement is one class,
and within the class the objects still differ — by shape, by orientation, by how they sit relative to
each other — and those differences subdivide the class into subgroups.

**Then it watches who moves with whom, and it does not settle for *together*.** Three readings, and
they are different claims:

- two objects move on the same action, by **different** displacements — that is **coincidence**, and the
  agent files it as independent.
- two objects move on the same action, by the **same** displacement — that is **one body**, and it can
  say so from a single step.
- two objects move together **consistently but not identically** — that is **correlated, not rigid**, and
  it cannot be said from one step. The agent holds it as *believed* while the ranking keeps settling,
  and it becomes a conclusion when the ordering stops changing — not when a counter reaches a number
  someone chose.

**Everything carries the full attribute set, null where it could not be read.** Null, not absent. *The
instrument could not see it here* is a different claim from *the thing is not there*, and the
difference travels: a term built on a null returns a null rather than inventing a value.

## Who am I here?

**The agent does not know, at the start, what kind of thing it is on this board.** It finds out per
locus, and it re-reads every step.

- If one object's motion lines up with what it commanded, that object is **embodied** — an avatar. And
  once that holds first-hand, the agent stops tracking that motion as a surprise: *it knows it moved
  left because it chose left.* What it tracks instead is the prediction, and whether the thing **stops**
  answering.
- If nothing it tracks correlates **and the board moved anyway**, that is **disembodied** — it is acting
  at a distance, through a control surface with no self on the board. **It is careful here: the absence
  of a correlating object proves nothing on its own.** The board having moved is what makes the reading
  causal instead of a shrug.
- If the detectors simply found nothing and the board sat still, that is **unknown**, and unknown is a
  value, not a failure. It is the same discipline as a null attribute, one level up.

**The board as a whole is whatever its parts compose to.** An avatar it drives *and* buttons that change
the world independently is **hybrid** — not an ambiguous middle, but what the loci add up to. And that
composed reading is a **finding**: something the agent reports, never something it branches on. What
drives its behaviour is the per-locus conclusion; what the board is called is a thing it says
afterwards.

**And the mode has a history.** *Embodied at the start; a second controllable thing found at step k;
hybrid from there.* Those transitions are events, filed like an object appearing or vanishing — and on
a later play the agent expects the same transition around the same trigger. **It expects it. It does not
assume it**, and a first-hand reading overrules a remembered one every time.

## What it holds, split two ways

**In cache, this play only:** the raw palette values, the live tree, the per-object position tracking,
the bindings this episode happened to produce.

**Durable, if the play settles:** the object's structural name, its change-list, the groupings and
relations keyed to those names, the attribute deltas, and every term it minted with a record of where
that term came from. **Everything except the raw values** — because the raw values are the arrangement
that will not survive, and the structure is the part that will.

**And a third split runs across both, which is the one that decides what it can actually do.** A term
it has paid for is not the same as a term it can build on. **The library only ever grows and nothing is
ever deleted from it** — a term that stops paying loses its standing and keeps its place, so the agent
can always tell *never had it* from *had it and gave it up*. What moves in both directions is the
**reach**: what it can currently compose over. So the library growing is not the agent getting further,
and it is the reach that decides what the next bet can even consider.

## The first bet

**All of that happens before a single move.** Then the agent looks up: given the shape of what it could
not explain, which terms in its library fit? **One pass over the library, ordered by fit** — not a
search, no composition, no walking the closure. The library is an asset when you look things up by the
shape of your gap and a liability when you walk it in registry order.

**A settled change is what fires the lookup; the size of the surprise is what decides whether it is
worth the pass.** One event, two thresholds. The agent does not retrieve for everything that moves; it
retrieves for what moved and mattered.

**It sizes the bet against a budget it is spending and cannot see the end of.** It knows what things
have cost — *this strategy took forty steps in that game, and half that here* — and it has no number
for how many actions a level allows. **That absence is on purpose.** It can compare effort across games
and it cannot look up the answer, so if it ever works out the ceiling, working it out is the
demonstration. Being told would have proved nothing.

## Moving, and being surprised

**It presses once, and the object slides further than it meant.** The gap between what it predicted and
what happened is the signal. It goes back to the cascade — the frames between the press and the settled
board — and asks what property it missed: did the thing *slide*, or did it *jump*? The cascade says
which, because it holds the order. **On this surface, one press means slide-until-stop.** That is a term
now, minted from a residual, priced against what it costs to say — and every later bet is sized against
it.

**Another move fails the other way: it heads up and something stops it.** Back to the cascade. Was there
a node it did not account for? Did something appear, vanish, or turn from pass-through to solid partway
through? **It names the blocker and the condition** before it adjusts — because *the move failed* is not
a thing it can reuse, and *this kind of object stops that kind of motion* is.

## The board changes what it is, mid-level

**Halfway through, the avatar stops answering.** Presses that moved it now move nothing. The agent does
not raise an alarm, because it does not need one: the conclusion *this locus is embodied* was proven
first-hand, and it demotes the moment it stops paying. **The demotion is the detection.**

**And a button on the edge, inert until now, starts changing the board.** That locus reads disembodied
— the board moved and nothing tracked did it — and the composition flips: *embodied at the start,
hybrid from step k.* The agent writes the transition down, keeps playing, and the next time it meets
this level it will expect the handover without relying on it.

## A colour changes, and is logged in place

**An object it has been tracking changes colour mid-game.** Nothing about its name changes — the name
was never a colour. What changes is its **placement**: it takes the next slot in that band's running
sequence, and that slot is now taken for everyone, so the next new colour after it goes one further.
The old placement is not overwritten. It is **appended to a list** that records what the object has
been, when it changed, and what else changed with it.

**Nothing leaves that list, ever.** You can dilute what is in the glass and you cannot take it out
without emptying the glass, and the agent does not get to empty the glass. Its record of what it has
been wrong about, and its record of what an object has been, are both things that only ever grow.

## What it cannot say

**Sometimes the honest answer is that it cannot get there.** Not *I do not know* — **I have searched
what I hold, and the thing that would answer this is not composable from it.**

That is a verdict with a shape: the agent can say *this question is not one question and must be split
before it is asked again*, and it can describe what is missing in terms of what it would *do* rather
than what it would be called. What it cannot do is name the missing piece, because naming it would mean
already having it. **And the verdict only counts because it names the closure it searched.** An
abstention over a room it never sealed is a shrug, and this one is not.

**It can say that something is false, and it does.** The draft of this section said it could not —
*there is no way to compose a refusal, because the operators it holds all join two things and none of
them negates one* — and that is wrong twice over. `¬` is the eighth operator and is not a bond;
`grammar.py` declares `NOT : PRED → PRED`, and `negate` is an atom the agent holds. **Measured on
`ls20`: it mints 3, settles 3 with the ground agreeing, is cited 6 times and drives 9 bets.** Zero on
the other boards, which is the per-game reading rather than an absence.

**What it cannot do is be ASKED for one.** The residual is sorted into four bins — held, novel,
rebinding, mechanism — and all four sort the gap by what is MISSING. None sorts it by what is WRONG.
So a refusal can be composed and is never DEMANDED: the agent arrives at one the way it arrives at any
term, and nothing in the loop says *a term you hold is false, and a refusal is owed.*

**Which is a narrower gap than the draft claimed and a stranger one.** The vocabulary is present and
the demand is absent, so the capability exists without an occasion. Refutation still mostly happens as
a term quietly losing standing — the machinery doing something *to* a term rather than the agent
stating it — and that half of the draft stands: **a correction that leaves no term behind is one the
next play inherits the consequence of and not the reason for.**

**And some of what it paid for it can never build on.** Terms that settle but whose shape already exists
in the library are real, and they predict when bound, and they add nothing to what can be composed. The
agent has no way to notice this from the inside: **from where it sits, a term that bought reach and a
term that bought nothing look identical**, because both are settled and both are in the library. Only a
reading that counts the reach rather than the library tells them apart.

## The game is lost

**Game over. The names and the terms stay; the palette goes.**

**The game resets, and the colours have swapped.** Same board, same structure, new hues. The agent does
not start over and it does not go looking for the old colours. It recognises the objects by **their own
shape** — the pattern of cells relative to their own corner, which does not change when they move and
does not change when they are recoloured — and it hangs the new placements on the names that were
already there.

**The strategies are reachable because the structure matched, not because the colours did.** That is the
whole of why this is recall and not lookup: an agent that found its way back by hue would be doing the
thing that scores zero the moment the palette is unfamiliar.

## Where this play goes when it ends

**It asks: have I seen this game before?** It computes a hash from the game's own structure — the
distinctive groupings and attributes, the shape of the thing and not its colours — and checks the prefix
against what it holds, confirming there is no collision before it uses it. **This is the opposite of
reading an identity the environment handed it.** An agent keyed on a given ID looks like it is learning
and is only doing lookup, and it scores zero the moment identities are hidden or new. A hash derived
from structure survives exactly that case, **which is why it is recall and not contamination** — and it
is the same construction, one scale down, that gives each object its name.

**Plays of one level stack under that hash, by episode, then by level.** Each carries what it decided,
what worked, what did not, and the deltas per object and per action. A later level uses the earlier ones
lossily: the earlier plays are residual the new level composes against, available at reduced strength
rather than overwritten. **Each entry carries the stamp of the play that made it**, because the
placements inside it were numbered by a counter that has since reset, and without the stamp they would
be unreadable — or worse, readable and wrong.

## Coming back, and looking across games

**Leave, play other games, return, and it recognises this one** — the hash matches, and it starts from
the shape of what it learned instead of from cold.

**Stuck, it looks wider.** *This obstacle is familiar — where have I seen this shape?* Not this game, this
**shape of situation**. It searches what it holds from every game it has played, its own game weighted
highest, and it only looks outward once its own strategies are spent and its confidence is low.

**When a match comes back from another game, it arrives as the weakest kind of claim.** Not proven —
that is what holds first-hand right now. Not believed — that is what it carried from a prior play of
this game. **Open**: a thing another world suggested, taken at low priority, stamped with the game and
the hash it came from, and traceable ever after. It gets tested like anything else, and it earns its
way up or decays back down.

**And that stamp is the whole difference between a library and a claim about one.** Two agents holding
identical terms — one that derived them and one that borrowed them — are indistinguishable in the
contents. **Only the record of where each came from tells them apart**, which is why the record is not
documentation of the term. It is the term.
