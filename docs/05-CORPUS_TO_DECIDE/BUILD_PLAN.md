# Build plan

**Status: BUILT, 2026-08-22.** All seven stages. See §8 for what actually happened.

Companion to `DISCOVERY.md` (the questions), `THE_FORMULA.md` (the mechanism), and
`PHILOSOPHY.md` (the why). This says what gets built, in what order, and what would
count as done.

---

## 1. What is being built first, and what it is not

**The deliverable of the whole plan is one behaviour:**

> An agent that derives an answer, records the derivation, is blocked by a checker if the
> derivation is malformed, renders what it did in language you can read — **and says
> plainly when the answer is not reachable from what it holds, with the budget it spent.**

That last clause is the product. Everything before it is scaffolding for it.

**And what a first result will honestly be worth.** Figure 11: *isolation is substitution,
not removal — a synthetic solve proves wiring and never capability.* Stage 6 will prove
**wiring**. That is the correct first claim and it should be stated in those words in the
run report, not discovered later by a reviewer.

---

## 2. The one structural decision: the Gate exists before the thing it gates

Every previous attempt built an agent that worked and then added the framework beside it —
`v4-cold` in shadow, `new-horse` unimported, `Nexus` double-loaded. **In all three, the
framework was optional because something else could already decide.**

**So the order is inverted here.** The ledger and the Gate are built in Stage 0, before any
loop exists. There is nothing to gate yet, and the Gate correctly refuses everything,
because nothing has been derived. Then the loop is built *into* a system that already
refuses undocumented action.

**This is the single decision that makes this v7 rather than v8.** If at any point there is
a path from perception to action that does not pass through a composed, checked utterance,
the build has reproduced the failure and should stop.

**Two consequences, accepted up front:**

- The agent will be **worse** than a heuristic for a long time. The rung ladder existed
  because it worked. Deleting it means the framework has to carry the performance itself,
  and early on it will not.
- Progress will look flat before it looks like anything. Per Figure 2 and the doctrine, a
  flat metric is not a dead direction — but it must not be rescued by inventing an internal
  one.

---

## 3. The stages

Built in dependency order, which is the framework's own rule: each stage consumes what the
one before produces, and a stage whose input never arrived cannot be diagnosed.

Each stage states **done-when** (a fact, not a feeling), a **falsifier**, and **what contact
it changes** — Figure 11's criterion, because an improvement that does not change contact
changes nothing.

---

### Stage 0 · The record and the checker

`grammar.py` · `ledger.py` · `gate.py`

The typed utterance grammar — types, primes, heads, terminals, `compose()` that raises with
its reason and never silently. The append-only ledger, one entry per loop step, **every
entry naming its step**. The Gate: reads the ledger file, imports nothing else.

**Gate checks at this stage** — form only, and each is structural:

1. every entry names a loop step, and steps appear in dependency order
2. no step consumed an input that never arrived
3. every slot with live mass was routed into exactly one bin, with its why-not-neighbour
4. all three guards were evaluated and recorded, **including the ones that passed**
5. nothing labelled ACCEPTED without a settle event
6. a mode is declared — general, specified, or grounded
7. **no filter has issued a verdict** *(Figure 9, C1)*
8. every cut is ranked and reversible *(Figure 9, C2)*

**Done when:** a hand-written valid ledger passes; a hand-written ledger with each of the
eight defects fails, naming the failing head and a fixed token.

**Falsifier:** if the Gate passes a ledger with a step missing, it is not checking order,
and the rest of the plan rests on nothing.

**Contact changed:** none yet — this stage is the instrument, and per the observer's defect
its first output is a claim about the instrument rather than about the system.

---

### Stage 1 · The library, and a number on day one

`gamma.py`

Atoms, **molecules as priors** (named type-valid composites with holes, stamped `prior`),
type-directed closure enumeration, provenance stamps.

**And it reports `λ` immediately** — the spectral radius of the type transfer matrix,
against `V = |atoms|`. That is *typing beats size* as a measured quantity rather than a
claim, computable before anything runs, and it gives REACHABILITY a cost model: depth `d`
costs `λᵈ`.

**Done when:** the enumerator emits well-typed terms only; `λ` and `V` are reported; every
term carries an origin stamp.

**Falsifier:** if `λ ≈ V` the type system is not sparse and is buying nothing — which is a
real finding about the grammar, not a bug.

**Contact changed:** none. Still instrument.

---

### Stage 2 · The world, and the eight-slot contract

`world.py`

The `Env` protocol as **eight required members** — substrate, environment, actors,
currency, ground, slot, atom, transform. An adapter that cannot supply one fails at
construction, not at run time. *(Q26 as an import error rather than a paragraph.)*

**The first env, and it is deliberately not a gridworld:** a symbolic transition world.
Named slots holding typed values; each slot has a hidden update rule drawn from a known
DSL; the ground is exact match on the next state — mechanical, instant, constitutive.

**No perception layer.** A gridworld tests perception *and* the loop at once, which is two
experiments in a trench coat. Slots are given by name here so that a failure is
unambiguously a loop failure.

**And unreachability is constructible.** Because we control the atom set, a slot can be
given a rule provably outside `closure(Γ)` at any budget. That makes the abstention claim
in Stage 6 exact rather than anecdotal — *and the agent is told nothing.*

**Done when:** the env runs, exposes eight members, and a partial adapter raises at
construction.

**Falsifier:** if a slot's rule is expressible in the atom set when it was meant not to be,
Stage 6 measures nothing.

**Contact changed:** first contact. The agent can now be wrong about something.

---

### Stage 3 · The loop

`tether.py` — steps 1 to 5.

Belief (not observation) as the bet. Residual **per slot, on three channels** —
`transition · reward · bracket` *(Figure 1; audit A1)*. The four-bin router with
why-not-neighbour recorded. Mint: the bargain with a **declared code**, the three guards as
a product, `UNREACHED` rather than unreachable, accumulated `|R|` per slot with **no
`min_support` constant**. Accept with provenance. Settle against the ground; candidate until
then, and **held but not cited**.

**Done when:** the loop runs and every step emits a ledger entry the Gate passes. A term is
minted, settles against the ground, and the ledger shows the whole path.

**Falsifier:** if any action executes without a passing utterance, one-track has failed and
the build stops.

**Contact changed:** the agent now acts, and the ground now refuses it.

---

### Stage 4 · Speech

`speak.py` — the builder. Reads **agent state only**; the Gate reads the world and the
ledger; neither reaches the other's sources.

Fixed tokens are the record; prose is a rendering **of** the record. Every sentence traces
to an entry. Compositional fluency in Γ is the target; human-likeness is the failure
signature.

**Done when:** the agent's account of a run can be checked line by line against the ledger,
and a deliberately false sentence is caught.

**Falsifier:** a sentence that traces to nothing and is emitted anyway.

**Contact changed:** none for the agent — but this is where the work becomes legible to us,
and legibility is the instrument.

---

### Stage 5 · The two zero-density branches

`probe.py`

Both triggers, on both channels *(audit A4)*:

- **nothing is scoring** → the curiosity drive, aimed at the NOVEL bin *(Figure 5)*
- **nothing is surprising** → the probe, uninformed by construction *(probe.py's shape)*

The probe sees the advertised action set and the state's shape. Not the score, not the
goal, not the effect model. Its outcome re-enters as an ordinary observation and is scored
under the unchanged bargain.

**Done when:** a run that has gone quiet perturbs, and the perturbation's outcome appears in
the residual as an ordinary observation.

**Falsifier:** if the probe reads anything it should not, it can only confirm the current
model.

**Contact changed:** the agent can now widen its own slice.

---

### Stage 6 · The abstention demo — the actual deliverable

`demo.py`

Four things, in one run, on the planted-unreachable slot:

1. a human reads the library and **locates one wrong term** — by id, step, and the residual
   it answered
2. an injected bad atom is caught by the ground, or traced by provenance to its entry point
3. the agent **abstains correctly** on the unreachable slot, stating the budget spent
4. **the false-abstention rate is reported** on the slots that *were* reachable

**Done when:** all four, with the run report stating its mode, which of Figure 3's five
links it stopped at *(C10)*, and that a synthetic solve proves wiring and never capability.

**Falsifier — and this is the one that matters:** if false-abstention is high, the agent is
not abstaining, it is failing. Both numbers are required; either alone is marketing.

**Contact changed:** this is the first stage whose result is about the agent rather than
about the instrument.

---

## 4. What is explicitly not being built

| | why |
|---|---|
| step 6 PROMOTE, population scale | the adult on Mars is complete without it |
| step 7 OUTWARD / IMPORT | needs a second frame; until then the loop records the debt |
| the tiny proposer | a training artefact plus a loader, not a module of the loop. **If removing it breaks the loop, it stopped being a proposer** |
| perception / segmentation | Stage 2 gives slots by name on purpose |
| the seat stack | lazy instantiation is designed (Q22) and unneeded until there is a second level |
| any competition adapter | own branch |
| a test suite | a few tests that pin what would silently break, and nothing else |

---

## 5. What blocks what

| stage | needs a ruling on |
|---|---|
| **0** | **Q10** — one vocabulary or two. Decides whether `grammar.py` and `gamma.py` are separate files or one |
| **0** | **Q15** — the Gate blocks from the start. *The plan assumes yes; the whole structure depends on it* |
| **all** | **Q12** — one track. *The plan assumes one; stated so it can be refused* |
| **2** | **Q27** — the symbolic transition world, as reframed by the audit. Changes what gets written |
| **3** | **Q11** — SUPPORT × REACHABILITY × NOVELTY, MDL after |
| **5** | **Q17** — the brake invariant: monotone integral, no `suppress()` |
| **later** | Q13, Q18, Q22, Q26's finer points |

**Stages 0 and 1 need only Q10.** Everything else can be ruled on while they are being
written.

---

## 6. How this fails, stated in advance

- **The Gate becomes advisory.** The first time it blocks something that looks right, the
  temptation is to add an override. That override is shadow mode with extra steps.
- **A metric gets invented.** Terms minted, coverage, compression achieved — all
  frame-internal, all forbidden, all tempting when the real number is flat.
- **A filter starts issuing verdicts.** A search cutoff that returns "no" reads exactly like
  a finding.
- **The env grows.** A richer world looks like progress and moves the experiment away from
  the loop.
- **`min_support` comes back**, or another bare constant, because the arithmetic is slow to
  earn its evidence.

Each of these is checkable, and the last four are Gate checks or constants-block entries
rather than good intentions.

---

## 7. Rough shape of the work

Ordering matters; the sizes are a guess and carry no provenance.

| stage | files | rough |
|---|---|---|
| 0 | grammar, ledger, gate | the largest, and correctly so |
| 1 | gamma | small |
| 2 | world | small |
| 3 | tether | medium — this is the loop |
| 4 | speak | small |
| 5 | probe | small |
| 6 | demo | small |

**Target: under 1,500 lines total.** v1–v6 died of weight. If a stage is pushing that,
the design is wrong rather than the estimate.

**READ 2026-08-26, AND IT FIRED. 2,374 lines** across the nine — 1,785 discounting blanks
and comments. **`tether.py` is 936 of them, 39% of the package, against an estimate of
*medium*.** The stage pushing it is stage 3, which is the loop.

**Most of the overshoot is one week's work: net +388 across the nine, +278 in `tether.py`.**
The residual bound, cite/hold, the A4 cause codes, `R_T` as pre-image bits, per-slot
alphabets. Every one derived from the corpus, every one justified on its own, **and this
line says that is exactly the condition under which to distrust them.** It is failure
mode #1 in `CLAUDE.md`, and the audit that produced the additions did not measure weight
because the number lives here and nothing reads it.

**Recorded rather than acted on.** Subtracting to a target is how a number gets gamed; the
finding is that the design is carrying more than it was meant to, and the next build should
close a mechanism rather than open one. **The falsifier was pinned before the work and read
after — which is the only order in which it could have said anything.**

---

## 8. What actually happened

Built in one pass on 2026-08-22. **1,481 lines of core plus 105 of tests**, against a
target of 1,500. Lint clean; the gate passes on a 289-entry run; the eleven gate-defect
tests pass; `demo.py` exits 0.

### Results

| | |
|---|---|
| slots the agent modelled | `climb -> inc`, `driven -> act`, `swing -> dec . neg` — all correct against the hidden rules |
| settled by the ground | `dec . neg`, on a transition it was never fitted to |
| **abstention** | **1/1 correct** on `opaque`, the planted-unreachable slot |
| **false abstention** | **0/4** |
| what it said | *"I searched 399 compositions to depth 3 and none of them pays. That is unreached at this budget, which is not a proof that it is unreachable."* |
| stopped at link | 2 — vocabulary (measured: 1 slot unreached at budget) |

### Falsifiers that fired, and were reported rather than tuned away

- **Stage 1's falsifier fired.** `λ = V = 7`, advantage 1.0. Every atom in this world has
  one type, so the type graph is a single node and **typing buys nothing here**. That is a
  real finding about this grammar. The temptation was to add types until the number looked
  good, which would have been inventing a metric.

### Defects the build found in itself

- **The gate refused the loop three times before the loop was right**, which is the whole
  point of building it first. Two were real loop defects (utterance steps out of order; the
  probe recorded after SETTLE). One was a defect in the *gate*: the step-order check was
  global per cycle when the dependency chain is per **slot**, since slots are independent
  within a cycle. The gate was wrong and the loop was right, and that is worth recording.
- **The reward channel was live and unrouted.** The boundary diff sorts `R`, and reward is
  a channel of `R` — so it is routed and diagnosed now, with its remedy stated as unbuilt
  rather than going silent.
- **`Ledger.__len__` returning 0 made an empty ledger falsy**, so `led or Ledger(...)`
  silently discarded the ledger that was passed in and the whole run wrote to a ghost.
  Caught because the demo reported 0 entries beside a populated library.
- **A partial term settled on a lucky hit.** `inc . inc` pays on `opaque` and never closes,
  and it was settling on one later correct prediction. A term known-partial from birth is
  not eligible to settle: it stays a candidate until something closes.

### Honest scope

Stage 6 proves **wiring**. The harness is a substituted habitat and a synthetic solve
proves nothing about capability; the run report says so in those words. The reward channel
is recorded and routed but its remedy — composing actions that advance the objective — is
not built. The bracket channel is inert because this world defines no coarse view, and the
entry says that rather than omitting the channel.

### Not built, as planned

Step 6 PROMOTE, step 7 OUTWARD/IMPORT, the tiny proposer, perception, the seat stack, any
competition adapter.
