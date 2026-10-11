# An ARC game, from the agent's side

## Before the first move

**A frame arrives. Not a picture, a tree.** The agent sees a structure of objects, each a node, and holds it the way a browser holds a DOM. Something watches the tree the way a `MutationObserver` watches a page: not re-reading the whole thing each frame, but noticing what changed, a node moved, a shape changed, a node vanished.

**And it reads the tree in an order, not evenly.** It reads the way a person reads a page, in a pattern. This is a prior it carries, not something it worked out: the research says the pattern is absent in babies and emerges through the teenage years, which is what a codified, culturally-reinforced prior looks like. Most of the time the pattern is F-shaped, across the top, across again lower, down the left. On odder layouts other patterns take over when their conditions are met.

**It recomputes the pattern every frame**, because the board can shift mid-episode and the eye re-prioritizes when it does. The pattern doesn't tell it *what* to read, everything still gets read. It tells it the *order*, and the agent narrates that ordering as it goes. But it never saves the ordering as a reusable term, because a read-order for a frame it hasn't seen yet would be a guess, and on a procedurally-generated board it would be a wrong one. **The pattern is described, never composed.**

**The order matters more than it looks.** Whatever the eye lands on first is first, and under a budget the first bet is the one that gets made, so the ordering can be the difference between an action that pays and one that doesn't. It is not perception polish. It is part of what makes the later budgeting correct.

## Naming the colors

**The first distinctly-colored object it meets is cyan.** The agent does not write down "cyan," and it does not write down `RGB(0,255,255)`. It knows what you told it: the color itself is disposable, this object might be cyan now and orange next play and the game would mean the same. What matters is that cyan is different from the others, and where it sits.

**It places cyan on the one arrangement humans actually accept for color** — `ROYGBIV`, the visible spectrum, the ordering nobody says out loud but everybody shares. Cyan lands between green and blue, and it's the first thing there. **Its name is `GB1`.**

**And `GB1` is not a rank.** The agent is not saying cyan is *color number one*, the way it would never think of blue as *color five*. It's saying: *this is the anchor I file this object's strategy under.* The position exists for one reason, so that when the colors all change next play, a brand-new hue landing in the same spot can alias into `GB1` and inherit everything already learned. The raw RGB it keeps, but only in cache, only to tell two blues apart this play.

**The next new color is cerulean.** It checks the RGB against everything named, finds it distinct, and it too falls between green and blue. **It becomes `GB2`** — the second thing encountered in that band, not the darker or lighter one. The number is the order of the read, and nothing else.

## Grouping what it named

**Color has done the first cut.** Everything `GB1` is one group. But within the group the objects differ, some square, some L-shaped, some turned different ways, and shape and orientation and the relations between them subdivide the group into subgroups.

**And it watches how the group behaves.** Do the `GB1` squares all move together, or does each respond on its own? A group that moves as one is a different kind of thing from individuals that share a color, and that answer is relational data recorded per object, per group, and per subgroup.

**Everything carries the full attribute set, null where it can't be read** — null, not absent, so the agent knows it's a thing it couldn't see rather than a thing that isn't there.

## What it holds, split two ways

**In cache, this play only:** the raw RGB, the per-object position tracking, the live tree.

**Bound for the library if this play settles:** the color IDs and their structure, the groupings, the attribute deltas, the relations. **Everything except the raw color** — because the raw color is a temporary arrangement that won't survive into another game, and the ID is the part that will.

## The first decision

**All of that happened before a single move.** Now it looks up: given these attributes and changes, which atoms are candidates, which recipes apply. It forms a hypothesis to test.

**It sizes the bet against a budget it doesn't fully know.** A placeholder ceiling for now; the real one it learns from cache once it's moved a little. Cheap hypotheses it tries; expensive ones it weighs.

## Moving, and being surprised

**It predicts five presses left to reach `x1,y1`.** It presses once and the object slides all the way. One action, not five. That gap is a signal: it inspects the animation between the before-frame and the after and asks what property it missed. The board is ice. **It updates, on this surface one press means slide-until-stop**, and re-sizes every future bet.

**Another move fails the other way.** It heads up and something blocks the path. Ten presses and it can't finish. Back to the animation: was there a node it didn't account for, did something appear, vanish, or turn from pass-through to solid mid-move? **It names the blocker and the condition** before it adjusts, all of it in real time, off the tree it's been watching.

## The game is lost

**Game over. Everything stays in cache.**

**The game resets, and the colors have swapped.** Same board, same patterns, new hues. The agent doesn't start over. It reassesses the new colors against the shapes and groupings that didn't change, and **aliases them onto the old IDs in place**, so the strategies and data filed under `GB1` are still reachable. The type of read is the same because the board type is the same. This is the lossy recall, a color-swap survived by filing under structure rather than under hue.

## Where this play goes when it ends

**It asks: have I seen this game before?** It computes a hash from the game's own structure, the distinctive groupings and attributes, the shape of the game and not its colors. This is the opposite of reading an ID the environment handed it, which is the thing that must never happen, because an agent keying on a given ID looks like it's learning and is only doing lookup, and scores zero the moment the IDs are hidden or new. **A hash it derives from structure survives exactly that case**, which is why it's recall and not contamination.

**It checks the hash prefix against the library, then the cache.** `eec40c6`, never seen. First episode of level one, stored `eec40c6_1_1`.

**Play after play the same level stacks:** `eec40c6_2_1`, `eec40c6_3_1`, each carrying its decisions, what worked, what didn't, the transformations and deltas per object and per action. Eighty plays of level one might sit there before a win. Then level two starts: `eec40c6_<n>_2`.

**Level two doesn't confuse itself with level one.** Grouped by hash, then level, then ordered by episode. Level two uses level one, but lossily, the new level carrying similar patterns and adding new ones, the way juice already in the glass isn't removed when you add water, only diluted. The old plays are residual the new level composes against.

## Coming back, and looking across games

**Leave, play other games, return, and it recognizes this one** — pulls up `eec40c6` and the shape of what it learned, instead of starting cold.

**Stuck, it looks wider.** *This obstacle is familiar, where have I seen this shape?* It searches every game's stored scenarios, its current game weighing highest. If it's exhausted its own game's strategies and low on confidence, and a strong match turns up from another game, **it imports that as a low-priority test, marked with the game and hash it came from**, so the borrowing is always traceable.

---


**The reading pattern** is now stated as a per-frame prior that's described and never composed, with the reason it can't be an atom, and with the note that ordering is load-bearing on action rather than a nicety.

**The color ID** is now explicitly *not a rank* — a filing position that exists to let a new hue alias onto an old strategy, sitting beside the label rather than replacing it.

**The hash** is now framed as the opposite of the banned thing — structure the agent computes versus an ID the environment hands it, with the OOD-zero failure named as what the firewall exists to prevent.

