# The operator grammar

**`+` is doing seven jobs and the recipes are unreadable as procedures because of it.**

**Measured across 2,651 recipes:** `+` appears in **2,111**. Every other operator combined
appears in **48**. `>` five times, `or` four, `=` once, `-` once.

**So the notation has one symbol and seven meanings**, and which one applies is recoverable only
by reading the definition beside it.

---

# The seven operators

| symbol | name | means | test that distinguishes it |
|---|---|---|---|
| **`+`** | **conjunction** | both present, order irrelevant | **swap the operands — does the meaning change?** No → conjunction |
| **`→`** | **sequence** | A then B; B needs A to have happened | swap them — **does it become nonsense or a different thing?** |
| **`⇒`** | **production** | A produces B; B did not exist before | is there a B **before** A fires? No → production |
| **`∥`** | **disjunction** | either suffices; not both required | **remove one — does it still work?** Yes → disjunction |
| **`−`** | **subtraction** | A with B removed or absent | is the ingredient's **absence** the point? |
| **`≡`** | **identity** | two names, one referent | **substitute one for the other — is anything lost?** No → identity |
| **`⋛`** | **comparison** | a threshold relation between two quantities | is the recipe about **which is larger**, not about both being present? |

## And two qualifiers that are not operators

| notation | means |
|---|---|
| **`A(x)`** | A, qualified — *Freq (high)*, *Stim (low)*, *Var (extreme)* |
| **`A?`** | A, optional — present in some instances of the element and not others |

**These are already in the recipes as parentheses** and are being read as operators. They are
not — **a qualifier narrows one operand; an operator relates two.**

---

# Why it matters — the worked example

**One element, written seven ways. Same three ingredients. Seven different things.**

**Take `Balance`, `Propulsion` and `Contact` — the three ingredients of `Walk`.**

| written as | reads as | is it walking? |
|---|---|---|
| `Bal + Prop + Cnt` | **all three, simultaneously** | **yes — this is `Walk`** |
| `Bal → Prop → Cnt` | balance, *then* push, *then* touch down | **no — that is falling forward and catching yourself** |
| `Prop ⇒ Cnt` | pushing **produces** contact | **no — that is a collision** |
| `Bal ∥ Cnt` | balance **or** contact, either will do | **no — that is `Hover` or `Crawl`, not both** |
| `Prop − Cnt` | propulsion **with contact removed** | **no — that is `Fly`** |
| `Bal ≡ Stance` | balance **is** stance, two names | **not a recipe at all — a synonym** |
| `Prop ⋛ Trac` | propulsion **exceeds** traction | **no — that is `Slip`** |

**Seven readings of three ingredients, and six of them are different elements that are already
in the list.**

**`Fly`, `Crawl`, `Hover`, `Slip` and `Collide` all exist as separate entries** — and every one
is reachable from `Walk`'s ingredients by changing nothing but the operator.

## Which is the point

**The operator carries as much information as the ingredients.** `Prop + Cnt` and `Prop − Cnt`
share every operand and name opposite things.

**And a composer that reads `+` as *combine somehow* will generate all seven and cannot tell
which one it made.** Which is worse than not composing — **it produces a term that names one
thing and does another**, and nothing downstream can catch it, because the recipe is
well-formed either way.

---

# The pairing example, in full

**`Erase` and `Construct` were added as a pair, and they demonstrate every operator at once.**

| element | recipe | operator doing the work |
|---|---|---|
| **Erase** | `Contact ⇒ (Object − Object)` | **production of an absence** — contact *produces* the state where the object is gone |
| **Construct** | `Rep ⇒ (Bind + Ge)` | **production of a presence** — replication *produces* a bound shape that was not there |
| **Camouflage** | `Recolour ≡ Surround` | **identity** — the object's colour *becomes* the surround's; not added to it |
| **Uncamouflage** | `Recolour ⋛ Surround` | **comparison** — the colour now *differs enough* from the surround to be found |
| **Merge** | `A + B ⇒ C` where `C − A` and `C − B` are both empty | **conjunction producing a third, with both originals subtracted** |
| **Abut** | `A + B` where `A` and `B` both persist | **plain conjunction — nothing produced, nothing removed** |
| **Layer** | `A ⇒ over(B)` where `B` persists and `read(B) ⋛ read(A)` | **production plus comparison** — B is still there and *less readable than* A |

**Read those seven with `+` everywhere and they are indistinguishable.** `Erase = Contact +
Object`. `Construct = Rep + Bind + Ge`. `Merge = A + B`. `Abut = A + B`. **`Merge` and `Abut`
become the same recipe**, which is exactly the distinction that took a ruling to establish.

---

# How to use it

## When writing a recipe

**Ask the operator's test before writing `+`.**

**Swap the operands.** Same meaning → `+`. Different meaning → `→`.
**Remove one.** Still works → `∥`. Breaks → `+`.
**Is one absent?** → `−`.
**Does the result exist beforehand?** No → `⇒`.
**Is it about which is bigger?** → `⋛`.
**Can one substitute for the other with nothing lost?** → `≡`.

**Six yes/no questions, and they are exhaustive over the seven.**

## When reading one

**A recipe with only `+` is under-specified until checked**, not wrong. **2,111 of them are in
that state** — the ingredients are right and the relation is unstated.

**And the default assumption should be conjunction**, because that is what most of them are —
**but *most* is not *all*, and the exceptions are the interesting entries.**

## When traversing

**The three edge types map onto the operators directly.**

| edge | operator |
|---|---|
| ingredient | `+` `→` `∥` `−` `⋛` — anything that names an operand |
| identity | `≡` — **a hop that costs zero** |
| default | the absence branch of `−` and the unfilled branch of `∥` — **fires when nothing else does** |

**So encoding the operators is what makes the identity and default edges findable.** Right now
they exist and nothing marks them, **which is why `Setpoint ≡ Goal` was found by accident and
`Latency` was found by a prose translation rather than by a graph walk.**

---

# What this is derivable from, and what it is not

**Some of it falls out of the definitions.** A recipe whose definition contains *then*, *after*,
*triggers* or *leads to* is sequential. One containing *without*, *absent*, *removed* or *zero*
has a subtraction. One containing *either*, *or*, *whichever* has a disjunction.

**Measured: 18 recipes carry an explicit negation word, 14 a slash, 4 an *or*.** So the
mechanically findable cases are **fewer than fifty out of 2,651.**

**The rest need the definition read.** Which is 2,600 judgements — **and that is the same wall
the axes hit**, with the same answer: **do not tag by hand in one sitting.**

**The usable move is narrower.** Tag the operators **only for entries that are used as
ingredients** — 1,266 by the middle count, and they are the only ones a composer reads. **The
other 1,400 are leaves and their internal structure is never traversed.**

**That is roughly half the work for all of the benefit**, and it is checkable: an entry becomes
worth tagging the moment something composes from it.
