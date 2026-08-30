# NSM × operators × atoms — one grammar in three layers

**The answer is that they are not three things. NSM already contains the operators, and its
substantives are the placeholder variables.**

---

# The claim

**NSM's ~65 primes split into three families, and each family is one of the layers.**

| family | primes | role | what fills it |
|---|---|---|---|
| **Substantives & determiners** | SOMETHING · SOMEONE · THIS · THE SAME · OTHER · PART · KIND | **the placeholder variables** | atoms |
| **Frames** | DO · HAPPEN · MOVE · BE · WHERE · WHEN · TOUCH · INSIDE | **the slots with arity** | substantives, filled by atoms |
| **Connectives** | AND · NOT · IF · BECAUSE · THE SAME · MORE · LIKE · MAYBE · CAN | **the operators** | frames |

**So `OPERATORS.md`'s seven symbols are not a separate invention.** They are the connective
family, and six of the seven have an exact prime:

| operator | prime | note |
|---|---|---|
| `+` | **AND** | conjunction |
| `→` | **BEFORE / AFTER** | sequence — and it is a *time* prime, not a logic one |
| `⇒` | **BECAUSE** | production — A causes B to be |
| `−` | **NOT** | subtraction is negation of an operand |
| `≡` | **THE SAME** | identity |
| `⋛` | **MORE** | comparison |
| `∥` | *(none)* | **disjunction is not an NSM prime** |

**`∥` having no prime is worth stating rather than papering over.** NSM's designers found *or*
not to be universal — it is expressible as *maybe this, maybe that* using MAYBE, **which is a
different claim than disjunction.** Either `∥` is a convenience that decomposes, or it is a
genuine addition to the prime set, **and that is a ruling rather than a fact.**

---

# The placeholder mechanism, and NSM already has both kinds

**The grammar's typed hole is existential** — *a bare type as a leaf: a template without
content. This is how a question is asked.* Two holes are indistinguishable, and a probe answers
one and it is gone.

**A key's `?c` is universal** — *I do not care which, and it is the same one twice.* It must
stay open and must bind consistently.

**NSM distinguishes them with determiners, which is exactly what determiners are for:**

| written | prime | means |
|---|---|---|
| `SOMETHING` | SOMETHING | **existential** — there is one, I do not know which. The grammar's current hole |
| `SOMETHING · THIS` | THIS | **bound** — the one already introduced |
| `THE SAME` | THE SAME | **binding constraint** — this occurrence is the same one as that occurrence |
| `OTHER` | OTHER | **anti-binding** — this occurrence is not that one |

**So `?a blocks ?b` is written `SOMETHING (THIS) blocks SOMETHING OTHER`**, and the
same-versus-different question is carried by a prime rather than by a subscript.

**And that is the affordance-key problem solved in the grammar's own vocabulary.** *A 3×3 of
`?c`* is `PART: KIND — THE SAME colour`, and the colour identity is a binding rather than a
value.

---

# Why this solves the arity block

**The current block:** an atom is `fn(value, action, operands) → value`. **One slot in, one slot
out. A relation has no slot, so `contains`, `touches` and `blocks` cannot be bet on.**

**The prime carries the arity, and the atom does not have to.**

```
TOUCH(X, Y)                     a two-place frame
  X ← SOMETHING (THIS)
  Y ← SOMETHING OTHER
```

**`touching` stops being an atom that needs two operands** and becomes **a frame whose slots are
filled by substantives.** The atom fills one slot; the frame holds the arity.

**Which is why the arity park kept not firing.** Three checks, three different reasons, and none
was cost — **the blocker was that a relation had nowhere to live, and a frame is where it
lives.**

**Stated as a claim to check, not a fact:** this needs the composition layer to admit a frame
type, which is §2622's contract question. **It does not need `Term.operand` to become N-ary**,
and the 13×-for-zero-capability measurement is untouched by it.

---

# A worked composition

**Take the thing the loop currently cannot say:** *the wall blocked me when I moved left.*

## In atoms alone — inexpressible

`blocks` is two-place. `Ctx` has `action` and `operands`. **The best available is a per-slot
value prediction that fails, with no way to say what it failed against.**

## In NSM with atoms filling the slots

```
BEFORE:  I DO MOVE(left)
AFTER:   SOMETHING (THIS) BE WHERE it was BEFORE
BECAUSE: SOMETHING OTHER BE WHERE I WANTED TO BE
```

**Read as a term:**

```
DO(self, Translate) → NOT(HAPPEN(Position-change, self))
                    ⇒ TOUCH(self, SOMETHING OTHER)
```

**Every capitalised word is a prime. Every italic word is an atom.** `Translate`,
`Position-change` and the substantive fillers come from the list; **the frame, the negation, the
sequence and the causation come from NSM.**

## And it is checkable in three ways the current form is not

**The frame has fixed arity, so a two-place claim is well-formed or it is not.**

**The operators are explicit, so `→` and `⇒` are distinguishable** — *the move did not produce
the position change* is a different claim from *the move produced a contact.*

**And `SOMETHING OTHER` is a hole with a binding constraint**, so *the thing that blocked me* is
a variable the next observation can fill, **rather than a gap with nothing to attach to.**

---

# What this makes of each layer

## NSM is the syntax and the variables

**It supplies arity, binding, negation, causation, sequence and comparison** — and **it supplies
nothing about the domain.** A frame is empty until an atom fills it.

**Which is the property that makes it safe to load.** *All possible priors exist and the frame is
a slice* — **and a prime is the shape of a slice rather than its content.**

## The operators are NSM's connective family, written as symbols

**Not a separate notation.** So `OPERATORS.md`'s seven tests remain the operational form — *swap
the operands, remove one, is the absence the point* — **and each test names a prime rather than a
convention.**

**Which upgrades the operator work from a notation proposal to a lookup**, with one open item:
`∥`.

## The atoms are the content, and they are almost entirely nouns

**Measured against the prime families:**

| prime | atoms that could fill it |
|---|---|
| DO | 16 |
| MOVE | 10 |
| KNOW | 9 |
| LIVE/DIE · GOOD/BAD | 7 each |
| SOMEONE · WANT · WHERE | 6 each |
| **KIND** | **0** |
| **CAN** | **0** |
| **TRUE** | **0** |
| SEE · PART · BECAUSE | 1 each |

**Three primes have no atom at all, and they are the three that matter most for this project.**

**`TRUE` with zero is the sharpest.** The whole loop turns on *the ground settled it* — **and
there is no atom for truth, verification, or a claim being confirmed.** The mechanism exists
throughout the code and the vocabulary has no word for it.

**`CAN` with zero is the affordance question.** §16.4's profile is *behaviour under contact* and
there is no atom for possibility itself.

**And `KIND` with zero is why the affordance key had to be invented.** *This is a kind of thing*
has no prime-filling atom, **so `kind_of` was built from colour and shape because nothing named
the concept.**

---

# What I want checked before any of this is built

**Whether the corpus already specifies the frame layer.** §15.5 gives the six primes as a lookup
and calls them *one grammar, not a bolted-on combinator language* — **which is this claim, and it
may say more than I have here.**

**Whether `∥` decomposes into MAYBE.** If it does, the operator set is seven symbols over six
primes plus a convenience. **If it does not, adding a prime to NSM is a much larger claim than
adding an operator**, and it needs to be made deliberately.

**And whether the frame layer is `Gamma`'s or `grammar.py`'s.** This is the routine-pricing
question from `4a` arriving in a different form — **a frame is composed and a term is priced, and
Q10's *keep the bridge, do not unify* constrains it without deciding it.**

**Report the shape. Do not build.**
