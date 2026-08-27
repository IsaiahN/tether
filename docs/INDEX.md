# Mechanism → source

**What decides each thing in the code, and where that decision is written.** Built while
reading rather than reconstructed after, because reconstructing it is what produced eight
batches of *this was decided and nobody carried it forward*.

Read this before changing a mechanism. **Four documents read for conflicts so far and every
one contradicted something already built**, so the prior is that a mechanism has a source
and the source says more than the code does.

`ok` the code matches the source · `gap` the source specifies more · `wrong` the code
contradicts it · `open` specified, not built

## The two fields — `kind` and `provenance`, INSTALLED 2026-08-27 as a rule, not a stamp

**The obvious build was 202 hand classifications. `git blame` makes that unnecessary and
worse.** Per-row commit and date are already recorded, so **the provenance of every existing
row is a FACT recoverable from history rather than a judgement made in one sitting.** The
fields say where to look and mark the boundary.

**`kind`** — `mechanism` · `measurement` · `citation`. **Only `mechanism` rows are in the
count.** A measurement sourced to *measured, 12 worlds* has no corpus citation and is not a
leak; it is not a mechanism at all, and counting it as one is what made the first attempt
read 74% and mean nothing.

**`provenance`** — four values, because *invented with no source* is not automatically bad:

| value | what it means | how it is decided |
|---|---|---|
| `derived` | the corpus specified it, then it was built | the citation predates the code in history |
| `found` | it was built, then traced to the corpus | **the citation POSTDATES the code** — `lint.py` records this as the sixth law's own shape: *every one of these was built first and found afterwards* |
| `chosen` | it fills a design space the corpus MARKED and did not settle | the corpus rules out wrong answers and leaves choices; a decision is not a leak |
| `unattributed` | no source and no marked space | **the population to examine.** Not automatically wrong either — but it is where a game leak would live |

### The watermark, and why it is a commit rather than a stamp

**Every row in this file today was written before any game was played.** That is not an
opinion — no adapter exists, `2a` has not started, and `git blame` dates every line. So:

> **WATERMARK: unset. It becomes the FIRST `2a` COMMIT, recorded here at the moment `2a`
> begins.** Every row at or before it is `pre-game` by construction. Every row after it
> carries `provenance` explicitly, and `unattributed` after the watermark is the one
> combination that must be justified rather than noted.

**A watermark is checkable and a stamp is not.** `git blame docs/INDEX.md` against one commit
hash answers *was this row written before any game* exactly, for every row, forever — and it
keeps answering after the memory that would have supplied a hand stamp is gone. **Which is
the point: the fact decays, and git is where it does not.**

> **SO THE DEADLINE DISSOLVES RATHER THAN BEING MET, and the board item changes shape.**
> The clock was on the MEMORY, and a watermark does not need it. **These two fields no
> longer stand BEFORE `2a` — `2a` RECORDS the watermark as part of itself.** Nothing is
> gated on them, and treating them as a blocker would be holding up a phase for a fact
> that git already keeps.

---

**AND THE COUNT THIS FILE IS SUPPOSED TO BE THE INSTRUMENT FOR, WHICH IT CANNOT YET RUN.**
`[I]`: ablation shows the loop can REDISCOVER, not that it GENERALISES, because *every design
decision that survived is one that helped on these 25* — **so the count worth running is how
many mechanisms would have been built the same way with no games at all.** Attempted
2026-08-27: **202 rows, 150 citing a corpus source (74%), 52 citing none.** **That number
does not answer the question, for two reasons, and both are fixable with one field each.**

- **The rows are three kinds and the count is about one.** Mechanisms, measurements and
  citations share this file. A measurement sourced to *measured, 12 worlds* has no corpus
  citation and is not a leak — it is not a mechanism at all. **Needs a KIND field.**
- **A citation does not prove derivation.** `conform/lint.py`'s own record of the sixth law's
  nine instances is *every one of these was built first and found afterwards*, so a corpus
  source is equally consistent with **derived** and with **built, then traced.** Only 7 rows
  say which, by prose a grep can find, and that is a floor rather than a reading. **Needs a
  PROVENANCE field, and FOUR values rather than three** — because *invented with no source*
  is not automatically bad. **The corpus rules out wrong answers and leaves choices**, so a
  mechanism filling a marked design space is a DECISION, not a leak: `derived` (corpus
  first) · `found` (built first, traced after) · **`chosen` (fills a design space the corpus
  marked and did not settle)** · **`unattributed` (no source and no marked space — the
  population to examine).** Collapsing the last two would file every legitimate decision as
  a leak, which is the mistake that invites answering the question on the agent's behalf.

**The 52 is the firmer half and it is the population to examine**, because *a game showing you
something is broken* is the residual working and *a game telling you what to build* is the
leak — and the test between them is whether the fix generalises. **No games have been played,
so none of the 52 can be a game leak yet. Which makes now the right time to install the
field, while every row's provenance is still knowable.**

**THE DEADLINE IS PINNED AT `2a`, AND THE PIN IS DELIBERATELY EARLY.** The TRUE boundary is
**the first observed frame** — writing `arc_world.py` is safe, because the adapter is built
from an API contract now checked out in source and nothing about it can be game-shaped.
That line sits INSIDE `2a`, between writing it and running it. **A boundary inside an item
is one you cross without noticing**, which is the failure being guarded against — so it is
pinned at the item edge instead: **both fields land before `2a` begins.** Slightly early,
and impossible to cross unaware. **Everything up to that point — blocker 1's three parts,
blockers 2 and 3, `0a`'s binding side — is toy-world work with every row's provenance still
knowable by whoever wrote it.** **So the clock is REAL AND NOT URGENT, and the distinction is worth keeping: *deadline* invites doing it now, and what is actually true is that NOTHING BEFORE `2a` CAN DECAY.** That says WHEN rather than HOW SOON, and it is the same reasoning as the atom-order pin — a boundary you can cross without noticing is not a boundary, and one you cannot reach early is not a rush.

**What this column establishes, and what it does not.** It is a claim about INTERNAL
FIDELITY -- whether the build matches what was decided -- and nothing else. **The corpus
being right about the code is not the corpus being right about the world.** The transfer
reading is flat, STAGE 1's trade is unresolved, and neither of those is affected by any row
here.

**And some early `gap` rows were the reader's, not the code's.** Three moved to `ok` on
reading rather than on repair: the one-alphabet number, `Config.max_depth = 3`, and
`starving()` -- which the audit filed as an unwired trigger when **branching on it is what
would be the defect**. That was a rule (*a producer needs a consumer*) applied where the
consumer is a reader rather than a branch: **the rule's subject narrower than it looked,
which is the same shape as the six checker sites.**

---

## The loop

| mechanism | source | |
|---|---|---|
| `units()` — settled terms re-enter the search | `ARC_AGENT` §14.1, §14.2 | **ok** — *unsettled is a binding, settled is a building block* |
| `pays` — the MDL bargain | `PHILOSOPHY` §16.8 · `DISCOVERY` Q8 | **gap** — code declared; margin absent. Measured: a margin would remove 3 correct mints and 0 wrong |
| `CODE` declared beside the inequality | `PHILOSOPHY` §16.8 | **ok** |
| SUPPORT × REACHABILITY × NOVELTY | `DISCOVERY` Q11 · `PHILOSOPHY` §16.3 | **gap** — NOVELTY is `φ ∉ atoms(Γ)`, a **stated proxy** for `H(R|Γ)` |
| `_accumulated` — cost(R) per slot | `DISCOVERY` Q8 | **ok** — *accumulated, and that makes an evidence-count gate unnecessary* |
| unreachability is not provable inside | **Figure 9 · Figure 8** | **ok** — *the witness is always imported; the edge can only be named from beyond it.* **Figure 8 gives the reason with citations: closure is idempotent (definitional), Gödel/Tarski for the metaframe, and Chaitin — a frame cannot certify its own limit.** So `depth_exhausted`'s refusal to claim absence is a theorem, not a wording choice |
| the five collapse modes | **Figures 2, 7, 8** | **reference** — mutual update · common cause · the mirror chain · the blend · **the undirected union**, which is importing without describing R first. §15.3's retrieval is the guard against the fifth and is unbuilt |
| split before search | **Figure 9** · `THE_FORMULA` step 7 | **open** — *not one hard question but several well-formed ones. Split it rather than search.* Nothing splits; the mint searches harder |
| the curiosity drive aims at NOVEL | **Figure 5** · `probe.py` | **open** — *aimed at the new bin, seeks the gap that is large and compressible.* The docstring says it; the draw is uninformed. Distinct from the transition probe, where uninformed IS the safety property |
| mint verdicts | `ARC_AGENT` §19.1 | **gap** — four of five. `UNREACHED` is reserved for after escalation |
| the escalation ladder | `ARC_AGENT` §19.2 | **open** — five priced rungs, each a ledger entry |
| `coverage` on a mint row | **Figure 1** · `ARC_AGENT` §19.1 | **ROUTE** — Figure 1 lists coverage among things that *do not count; a frame cannot score itself with a quantity it also produces*. §19.1 makes it the number that turns `unreached` into a measurement. **Both hold if it is a qualifier on a verdict and never a score of the agent** — which is how it is used |
| the dependency chain, and where it stops | **Figure 3** | **ok** — `demo.py` reports *stopped at link 2 — vocabulary (measured)*, and the figure says the middle link is where chains usually break and **has the fewest instruments**. *A reading taken below the break is a reading of nothing* — every minting and transfer number this session was taken at link 2 |
| `space_estimate` — the coverage denominator | `ARC_AGENT` §19.1 | **gap** — `V^d`; the signature takes a count so it cannot take `λ` |
| `type_report` — `λ` | `ARC_AGENT` §11.3 | **ok** — `λ = V` is the toy world, not the instrument |
| `_bindings` — which slots fill operands | `ARC_AGENT` §17.1, §16.5 | **wrong** — returns every slot. *You do not invent the list. You read it off the world* |
| operand arity | `ARC_AGENT` §17.1 · `BUILD_PLAN` 0a | **gap** — arity 1; cap 4 measured, quartic cost |
| atom registry order | `ARC_AGENT` §13.6 | **ok** — pinned this session; append-only |
| `Config.max_depth = 3` | `world._ladder` | **ok** — the falsifier sits one step past |
| `Config.budget = 4000` | measured this session | **gap** — bounds closure yields; work is yields × bindings, and exceeded it |

## Standing and settlement

| mechanism | source | |
|---|---|---|
| candidate held, not cited | `DISCOVERY` Q7 · `ARC_AGENT` §14.2 | **ok** — cite/hold rows |
| held-out payment settles | `DISCOVERY` Q7 | **ok** |
| a term partial from birth cannot settle | `BUILD_PLAN` §8 | **ok** |
| `Standing` — weighted, decaying | `ARC_AGENT` §18.2 | **gap** — 2 of 4. Missing: *decisive new surprise REOPENS a refuted hypothesis* |
| refutation keyed on `term.name` | `ARC_AGENT` §18.2 | **wrong** — **pathogen mimicry**: a name carries its binding, collapse is 6.3×, so ~6 twins escape |
| `sweep` — retroactive re-attribution | `ARC_AGENT` §19.5 | **ok** |
| `promote` — shadow then echo | `PHILOSOPHY` §5, §16.9 | **ok** — seq ordering proves pre-registration. `ARC_BUILD_PLAN` §4 still says *not built* |
| the boundary revert — *shadow without echo does not cross* | `PHILOSOPHY` §5 · **`SNAPS_PLAN` §3** | **CLOSED — stays out, and by ruling rather than by measurement.** §3's persistence table is explicit: **`Γ library + standing ✅ — this IS the transfer claim`**. Standing persists across a level boundary; the revert un-settles at exactly that boundary. §5's *does not cross* is about crossing a SCALE or a domain, and a level boundary in this ladder is not one |
| ablation wipes Γ | `ARC_AGENT` §23.4, §15.2 · `CLAUDE.md` | **gap** — must be **stratified** once priors load. And §15.2 names what survives it: *what gets wiped is the library, what remains is the ability to describe* |

## Perception and the interface

| mechanism | source | |
|---|---|---|
| the `Env` contract | `DISCOVERY` Q26 · `PHILOSOPHY` §14 · `ARC_AGENT` §4 | **ok** — the eight-vs-ten conflict dissolves. §4's adapter table gives `actors = available_actions` and `substrate = cell values 0–15`; `actions()` and `alphabet()` are those two made **machine-readable**. Ten members over eight slots, not a widening |
| `alphabet()` per slot | this session | **ok** |
| `transform()` / `R_T` | **Figure 4** · `DISCOVERY` Q19 · `PHILOSOPHY` §16.1 · `ARC_AGENT` §4 | **ROUTE — figure and document disagree.** Figure 4: the gap *is the measurement ... the only honest report*. Q19: it is *the admission criterion*, and says it is extending the figure. **What is built matches the figure.** The remaining `wrong` is the view SUBSTITUTING where Q19 says *added, never substituted*. Formerly: **wrong** — the measure is right; it **reports** where the ruling says it **gates**, and the view **substitutes** where the ruling says *added, never substituted* |
| habitat enumeration | `ARC_AGENT` §16.5 · **Figure 11** | **open** — B12's subject. *What you cannot perceive or measure yet is the residual* — and the figure adds a clause no document carries: **enumerate the habitat, RANK BY CASCADE**. That ordering is what `_bindings` would need |
| the substituted habitat's second failure mode | **Figure 11** | **open** — *two silent failure modes: what you failed to reproduce, **and what you brought with you***. `demo.py` prints the first. The second is unprinted, and its clearest instance is `snaps.key()`: **exhaustive extensional grading the real domain cannot supply** |
| affordance profile | `ARC_AGENT` §16.4 | **open** — seven booleans per kind, learned by contact |
| the slot set is fixed per level | this session | **gap** — a new object mid-episode is invisible, not an error |
| retrieval by characterised residual | `ARC_AGENT` §15.3 · Figure 9 | **open — HIGHEST PRIORITY.** It is the guard against **collapse 5, the undirected union**: *a surplus exists, but no residual is described; nothing was aimed; the union is mute.* **The only open row where a specified guard is missing for a mechanism the project intends to build.** — keys are **type signature · arity · what varies vs is invariant · effect shape**, and *matching is a one-pass check, not a search*. The extension-class index scoped this session is a different and heavier mechanism |
| no gating on the library | `ARC_AGENT` §15.2 | **open** — *can it characterise the gap? then it can have the tool.* An import ceremony nobody can perform at test time is shadow mode in a third costume |
| IMPORT / step 7 OUTWARD | `ARC_AGENT` §15.1 · Figure 6 | **open** — the channel was never closed. *external source: nature · corpus · peer frame*, **and the game is nature** |

## Drives and instruments

| mechanism | source | |
|---|---|---|
| probe on SUPPORT at zero | `DISCOVERY` Q20 | **ok** — uninformed; boredom refuses the model the wheel |
| `never_live` | `DISCOVERY` Q18 · `ARC_AGENT` §18.2 | **wrong** — `tried` is labels, not trials from distinct states. *Inert is a verdict earned by trials* |
| coverage-first as a phase | `DISCOVERY` Q18 | **open** — goal pursuit gated on a complete action map |
| the stage code | `ARC_AGENT` §18.1 | **ok** |
| phase histogram | `ARC_AGENT` §22.3 | **ok** — read off `by` |
| two clocks | `ARC_AGENT` §22.5 | **ok** — and the EMA in `ARC_BUILD_PLAN` 1c is superseded |
| chunk reuse count | `ARC_AGENT` §14.7 | **READ** — 13.9% provable, deepest term 6 against max_depth 3. **Not zero**, so the failure signature does not fire |
| reuse rate vs DS — the transfer curve | `SNAPS_PLAN` §1, §6, §7 | **READ** — 0.72 / 0.35 / 0.21 / 0.20 / 0.04. **And reuse HALVES on a constant change alone**: DS 0.2 moves only `k` and `a`, same families, same structure. **The library is tied to specific constants, not to the mechanisms they parameterise** — which composes with the false-mint read from the other direction |
| CUSUM regime detector | `ARC_AGENT` §18.2, §21.5 | **open** — reset vs advance without a level flag |
| reset vs advance | `ARC_AGENT` §21.5 | **open** — and it predicted the step-6 failure in words |
| `starving()` — nothing is scoring | `ARC_AGENT` §20.3, §8 risk 2 | **ok** — and the audit's *unwired trigger* reading was WRONG. §8: the reward channel is near-always zero, so *the curiosity drive's trigger has to be the transition channel or it is useless*. Computed and reported is §20.3's real result; **branching on it is what would be the defect** |
| three level terminations | `SNAPS_PLAN` §4 | **ok** — `advance` / `death` / `run_end`, and AVOID's inversion is implemented: *surviving the budget is the win* |
| the curriculum sweep | `SNAPS_PLAN` §5, §8 | **open, S5** — a monotone sweep over **fraction of slots outside closure** and **mean minimal term length**, both computed from the key and unmovable by the agent. **DCS rejected as a metric the frame produces and then grades itself with.** Its own plan rates it *least certain to matter* |
| three termination classes | `ARC_AGENT` §20 | **open** — bounded / mortal / open. In the third the cap is the measurement interval, not noise |
| phase mix across levels | `ARC_AGENT` §22.2 | **ok** — built, and **READ**: phase 1 flat at ~90% across four levels, and not a confound of this session's probe fix. The transfer reading is negative |
| ratio + stage code | `ARC_AGENT` §22.6 | **gap** — stage code built; the ratio needs a human reference. *Same alarm, different repair, and without the stage code they are indistinguishable* |

## The checkers

| mechanism | source | |
|---|---|---|
| **THE GRAMMAR HAS NO VERBS, and that is why STRATEGY is zero** | `ARC_AGENT` §15.5 | **the deepest structural gap the reading found.** All thirteen primes describe **a STATE** — `BE_AT TOUCH BECOME BECAUSE · SAME OTHER NOT · EXIST CAN · ALL SOME ONE NONE`. **Not one action or time prime.** §15.5: *the grammar has no verbs, **which is precisely why routines would not fit in it** and why I reached for a separate algebra.* The missing six are **`DO` · `MOVE` · `HAPPEN` · `IF` · `BEFORE`/`AFTER` · `FOR SOME TIME`** — and `BECAUSE` does not cover `IF`, being causal rather than conditional. **The ruling: the routine algebra is NOT a new language, it is THE MISSING THIRD of the one already chosen**, dropped by a Kant-category read of NSM. One grammar, three spaces, rather than a grammar plus a bolted-on combinator language — routines would then compose through the same `compose()`, be priced by the same bargain, and chunk by the same rule. **AND IT RELOCATES A ZERO ALREADY ON THIS BOARD**: `STRATEGY` is filed as an honest structural zero *until routines exist*. **Routines do not exist because the grammar cannot express them.** The zero is one level deeper than recorded. **The salvage symptom confirms it**: `relation.py` had to hand-write five relations *because the basis could express what a state looks like and not what a sequence of doings looks like* — **a workaround whose existence is the diagnosis.**

**BUT IT DOES NOT REACH ARRIVAL, and I said it did.** Q10's ruling is why: **two vocabularies with a citation bridge, and they are disjoint objects** — `gamma.Term is not grammar.Term`, gamma holds `idn inc dec dbl neg act wrap take` for DOING, grammar holds the thirteen state primes for STATING, and **the utterance CITES a gamma term as a RECORD (`G.ref(bound, "term")`) rather than decomposing it into primes.** So **a promoted atom needs no verb to be spoken about. Arrival lands in gamma; the verb gap is in grammar.** **Two zeros, two causes:** `STRATEGY` is zero because the grammar cannot express a routine; **arrival is zero because `promote`'s echo condition needs a term minted for one slot to close a residual on another, and four independent slots make that nearly accidental.** Panel property, not grammar gap. **They do not order each other**

**AND §15.5 CONTAINS THE OPEN INTERFACE QUESTION, unresolved.** It says routines *compose in the same type system, **type-check through the same `compose()`**, get **priced by the same bargain**, and **chunk by the same rule***. The first two are GRAMMAR-side; the second two are GAMMA-side. **Q10 ruled *keep the bridge, do not unify*.** So **where a routine lives — a gamma term wearing grammar names, or a grammar term borrowing gamma's pricing — is undecided**, and it is exactly the decomposition question already scoped as *the interface is the decomposition, and it is a choice nobody has made.* **The six primes are a completion; their economy is not** |
| **the typed grammar, inherited exactly** | `DISCOVERY` Q4 | **ok, and it is the thing Q4 rates highest.** **13 primes, 9 heads, 3 terminals, 7 types**, every name matching the specification. The idea Q4 calls *the single best in the reference tree* is live: **terminals PRODUCE records, so a later step can only consume what an earlier one produced** -- `BET` must be `_BET_ORDER` exactly, `ACT` must be `(NEED,)`, and **`DERIVE cites no record and is not a probe` raises**. Precedence as a TYPE SYSTEM rather than a convention. **And the typed hole is built AND enforced**: *DERIVE against a holed WANT composes with a probe only*. Q4's *grammatical form of "I do not know", and it typechecks* is literal |
| **nine heads, and the count has not moved for a reason** | `DISCOVERY` Q4 | **ok, and it closes Q4's open sub-question.** The basis rule is that **heads grow or merge ONLY on a composition failure surfaced as a named refusal**. `refused` is **0 across 360 cycles**. So nine is correct BY THE RULE rather than by inertia -- **the trigger for changing it has never fired**, which is the one reading that makes an unchanged count evidence instead of an absence |
| **MAP-as-market's two properties, by another mechanism** | `DISCOVERY` Q5 | **ok.** Q5 asks for a currency **measured externally** -- *a hypothesis cannot self-report its own salience*, which is Figure 1 arrived at independently -- and **Goodhart-guarded by construction**: *a hypothesis that predicts "nothing changes" scores zero on a frame that changed, so it can never win by saying nothing, and over-claiming is penalised too.* Here the ground settles rather than the term, and the bargain is symmetric: **`wrong += got != actual` increments both for predicting stillness where something moved and for predicting motion where nothing did.** Figure 5's *a term that explains everything by saying nothing* closed off in arithmetic rather than warned about in prose |
| the gate blocks from step one | `DISCOVERY` Q15 | **ok** — no shadow mode |
| one track — the derivation IS the decision | `DISCOVERY` Q12 | **ok** — verified: `except G.Ill: return False`. An utterance that does not typecheck is not an action, and **no fast path exists** |
| the probe's three properties | `DISCOVERY` Q20 | **ok, with the deviation documented.** All three carried: the trigger is the agent's own prediction error and may be nothing else; **it is a closed loop** -- `note_step`'s docstring is Q20's self-regulation verbatim; and it is **uninformed by construction, which is the safety property**. Q20 specifies an *error EMA fallen to ~0 with enough observations*; the build uses a single-step PREDICATE, because REPAIRS 1 removed the EMA for aggregating across slots and **a predicate warms itself -- a fresh model has live mass on its first miss**. Measured probe rate ~14%, not runaway. **The separator Q20 draws mechanically is intact**: random selection TO SCORE is Goodhart; random perturbation as an experiment whose outcome is consumed by the residual is not |
| the monotone integral | `DISCOVERY` Q17 | **ok** — `_integral` is `+=` only. No reset, no decay, no suppress, and `retarget` correctly leaves it alone |
| `R_goal` per objective | `DISCOVERY` Q1, Q21 | **ok** — recorded as `shortfall`; per objective, never per slot, which is why A7 was right to refuse `mass`. Its remedy — *composition of actions* — is routines, unbuilt |
| closure(Γ) sized by requisite variety | `DISCOVERY` Q24 | **open** — Ashby gives `closure(Γ)` **a lower bound the environment imposes rather than one the designer picks**. `max_depth` is anchored on the chunking falsifier instead — a good anchor for a different quantity |
| the branching test | `DISCOVERY` Q25 | **ok, unrecognised** — *no divergence means no transform, and it is visible from outside*. The carried-vs-cold run is this test: 24 of 30 comparisons diverge. **Ship it as a standing check** |
| `outstanding` — surprise not yet explained | `DISCOVERY` Q17 | **open** — *two quantities, not one*, and the missing one is the one the corpus calls **the aim and the currency**. `explain(bits)` reduces outstanding; the integral is untouched |
| **`Agent.settled` is historical, and named as if current** | measured | **gap, cosmetic, and the consequential path is clean.** `self.settled` is `add`-only with no discard, while `Standing.refute` sets `settled_at = None` -- so a demoted term stays in the agent's set and `run.settled` lists it. **The ledger is COMPLETE**: mint 4, accept 4, hold 5 and 6, settle 7, **demote 8**, cite 8 -- the reversal is a row. And `_standing` reads `gamma.is_settled`, the retracting source, so **citability is intact and a refuted term is held rather than cited**. The `cite` after the `demote` in one cycle is the documented read-at-the-bet behaviour, symmetric to the case its docstring already gives |
| **the shadow test is a gate check nobody wrote** | `PHILOSOPHY` §16.9 | **open, and correctly NOT YET.** Shadow-before-echo's rigorous content is **out-of-sample evaluation**: did the structure close a residual *recorded before the import was chosen*? §16.9 -- *checkable in the ledger, compare the sequence number of the residual against the sequence number of the import; **echo without shadow is post-hoc fitting and the timestamps prove which one happened; no new mechanism required***. **The data IS stamped** -- `_promotions` carries `recorded_before` from `gamma.stamps[name]["seq"]`, and terms are stamped `seq=len(self.led)` at accept. **Nothing compares them.** The gate's `_steps` checks a slot's chain does not run backwards within a cycle, which is a different property. **And `promote` fires zero times, so the check would examine nothing -- it ships WITH arrival, not before it**, or it is a control that demonstrates a clean state by looking at an empty set |
| **§20.4 cites two constants that no longer exist** | `ARC_AGENT` §20.4 | **stale twice over, and the file marks only one.** §20.4 carries `⚠ CORRECTED BY §22.1` for its anchoring claim — **the corpus correcting itself in place, which is the disposition to keep.** It is ALSO stale in a way nothing marks: it points at **`probe.py`'s `EPS` and `WARM`** as constants that *already have their reasoning stated*, and **REPAIRS 1 deleted both** — a predicate warms itself, and a threshold on a predicate was never derived. **Its core proposal survives both**: *end the epoch when the agent stops learning, not at a fixed count*, which makes the epoch **a reading rather than a setting** — a game still surprising you gets more actions **because it is still paying** |
| **a negative result that never travelled** | `PHILOSOPHY` §15 | **gap, and the design already complies.** §15 records a gate that came back NEGATIVE: *ARC game-shapes do not predict solving primitives, measured three ways*, with the instruction that **it should travel with the hypothesis, not behind it**. Neither `ARC_BUILD_PLAN` nor `ARC_AGENT` carries it. They do not contradict it -- §15.3 rejects keying by game and keys by residual shape, which is exactly what the negative result implies -- **but a design choice separated from the evidence that forced it reads as a preference**, and that is the `0.98` standard applied to a decision instead of a constant |
| **the tautology guard, satisfied by interface rather than by guard** | `DISCOVERY` §6 carry-list | **ok, and STRONGER than both references.** The law: *a φ that reads the after-state compresses perfectly and predicts nothing.* `new-horse` raises on `reads_after=True`; `v4-cold` uses an import-time AST wall -- **two branches, two mechanisms, one law, which is how the corpus knows it is load-bearing.** Here there is no guard and none is needed: `term.apply(state[slot], Ctx(action, operands=_ops(term, state)))` gives a term **only the before-value, the action, and before-state operands**. `actual` is compared against and never passed in. **The capability does not exist rather than being blocked.** And nothing says so -- **a refactor adding the after-state to `Ctx` for a plausible reason would silently delete it**, which is the atom-order pin's argument again |
| **build order is set by the ground's quality** | `DISCOVERY` Q27 | **ok, ruling taken -- and it sets the ARC sequence.** Three tiers: an interpreter or proof checker is **near-perfect** (mechanical, instant, unarguable); a rover, game or puzzle is **good** (sparse, slow, does not negotiate); human judgement is **poor**, because it updates, which is Figure 2 collapse 1. Q27's *open for you* proposed replacing the gridworld; **Stage 2 built the symbolic transition world and landed in the TOP tier** -- *exact match on the next state, mechanical, instant, constitutive*. **And the sequencing clause is the one to carry forward**: *a crisp-ground domain tests the MACHINERY; a poor-ground domain tests the ALIGNMENT CLAIM; doing both at once teaches nothing about either.* **ARC is the middle tier**, so it is a step down in ground quality and tests machinery more than alignment -- which is correct order, and means **the alignment claim still needs a domain neither `snaps` nor ARC provides** |
| **the objective is read, never priced** | `DISCOVERY` Q21 | **open, and it is the untested half of a load-bearing argument.** Q21's first half is built -- `R_goal = 1 - degree`, recorded as `shortfall`. **The second half is the bargain applied one level up**: `score_molecule` asks whether an objective's per-step degree PARTITIONS the progress stream, thresholded at **its own median so the split is data-driven, no free parameter**, charging two bits for the objective's description. Same two-part MDL, objectives instead of transitions. **`env.objective()` is only read.** And Q21's conclusion is what rests on it: *one bargain, two levels... **the strongest argument yet that the two residuals are two readings of one mechanism rather than two mechanisms.*** **With one level priced, that argument is unmade rather than wrong** |
| **`molecule` names two different things** | `DISCOVERY` Q21 · `BUILD_PLAN` Stage 1 | **a collision inside the corpus, inherited by the code.** In Stage 1 and `gamma.py` a **molecule is a named type-valid composite PRIOR** -- a term with holes, stamped `prior`. In Q21 and `redux_arch/molecule.py` a **molecule is a quantified typed OBJECTIVE** -- `ALL/SOME/ONE/NONE` over a relation, returning a verdict and a degree. **Both usages are the corpus's own**, the code follows the first, and **anyone reading Q21 then `gamma.py` will conflate a prior term with an objective.** Not a defect in either; a hazard in the join |
| **`verdict` is a mixed field, and the gate matches on it** | `DISCOVERY` Q16 | **gap, latent rather than live.** Q16's rule: **fixed tokens are the record, prose is a rendering OF the record** -- *a fixed token is a value and a sentence is not*, and `v4-cold`'s output was worse to read and **the only one of the two a gate could check**. Measured: `verdict` is `pays` on mint and `depth_exhausted` on park -- tokens -- and on settle it is **`held on a transition it was not fitted to`, a sentence**. `gate._unreached` does `d.get("verdict") in (...)`. No collision today, and **the settle verdict is a claim the Gate structurally cannot check**. The checkable content is already in adjacent TOKEN fields on the same row -- `asked`, `ground_said`, `held_out_cycle`, `fitted_through` -- so the sentence is redundant narration sitting in a field the Gate reads |
| **the inliner is an AUDIT of the seam, not a packaging chore** | `ARC_AGENT` §6 | **open, and it is the sharper reading.** *The builder/gate split has to survive the flattening or it was never structural.* **A separation that exists only because of file boundaries is a convention; one that survives being flattened into a single file is a property.** So **Kaggle's one-file requirement is an accidental audit of the architecture's central claim** — the first time a deployment constraint tests something rather than merely constraining it. The constraint half: Kaggle wants one file; the core is eight modules. §6's three rules: **`gate.py` imports nothing and must still import nothing after inlining** -- inline it as its own section with no cross-references and run it after the play loop over the local ledger -- because **its non-access is the whole reason it is sound, and an inliner that quietly wires it to the loop destroys that.** **The builder/gate split has to survive the flattening or it was never structural.** And the output must be **generated, never hand-edited** -- *a notebook edited in place is a notebook whose source of truth has moved* |
| **what `2a` needs, and what is Phase 5's** | scoped 2026-08-27 | **two of the three open checklist items are Phase 5's, and the third resolves as a side effect of `2a`'s own prerequisite.** The **gateway readiness loop** is the ONLINE/COMPETITION path through `gateway:8001`; `2a` is *the eight members over `arc_agi` **OFFLINE*** — no credentials, no gateway — **so Phase 5.** The **submission schema** governs the submission artifact — **Phase 5**, and §6 already flags one sample as stale. The **16 KB validator** binds when reasoning is first attached, which is stage **E**, not `2a` — **and it lives inside `arc_agi`, so it stops being unverifiable the moment that package exists locally.** **AND THE PREREQUISITE NOBODY NAMED: `arc_agi` IS NOT INSTALLED.** The harness pins **`arc-agi>=0.9.1`**; this venv has no such module, so **`2a` cannot start.** Installing it also makes item 1 checkable, **so the open list shrinks by one at the moment `2a` becomes possible.** **And it would be this repo's FIRST third-party dependency** — `arc-agi` pulls `pydantic`, `numpy`, `requests`. That does not touch the Gate's soundness argument, which is about `gate.py`'s IMPORTS and not the venv's contents, and TID251 already governs what the loop may import with `arc_world.py` on the domain side. **But a stdlib-only repo acquiring dependencies should be a decision rather than a `pip install` nobody recorded** |
| **PRE-SUBMISSION CHECKLIST — RECONCILED AGAINST SOURCE 2026-08-26** | `ARC-AGI-3-Agents` @ `agents/agent.py`, cloned | **the checkout was worth it: TWO OF FIVE WERE WRONG, and two new facts came out that no notebook shows.** **(1) `step(reasoning=…)` — CORRECTED.** §1 says building against the toolkit signature *would not run on Kaggle*. **The harness calls that signature itself**: `do_action_request` does `reasoning = getattr(action, "reasoning", None)` then **`self.arc_env.step(action, data=data, reasoning=reasoning)`**. The harness WRAPS the toolkit; they are not alternatives. §1's instruction (attach to the action object) is right and **its reason is wrong** — and a non-dict reasoning is auto-wrapped as `{"text": str(...)}`. **(2) `agents/__init__.py` — CONFIRMED, with a better reason.** It eagerly imports langgraph (lines 8–10) and smolagents (line 16), **and `AVAILABLE_AGENTS` is built from `Agent.__subclasses__()`, so a subclass must be IMPORTED to register at all.** That is why the rewrite is necessary, not merely that it is. **(3) the 16 KB validator** lives in the `arc_agi` package, not this repo — **still unverified.** **(4) the gateway readiness loop** and **(5) the submission schema** are notebook- and competition-page-side — **still open.** Original body: **NO LOCAL SYMPTOM ON ANY OF THEM. Everything passes, nothing runs**, and they will all be discovered in the same fifteen minutes unless they are checked as a set. **(1)** only the **harness** API runs on Kaggle — the toolkit's `step(reasoning=…)` signature works locally and does not run there. **(2)** the `reasoning` blob **raises above 16 KB** rather than truncating, and no platform doc states the limit. **(3)** `agents/__init__.py` **must be rewritten** — the shipped one eagerly imports packages that are not installed. **(4)** the **gateway readiness loop** must run before anything else. **(5)** the **submission schema differs between samples and one looks stale** — confirm against the competition page. **THE CHECKLIST IS A SYMPTOM AND THE FIX IS ONE ACTION.** §10 flags the root cause
honestly: the `ARC-AGI-3-Agents` repo *is not checked out anywhere locally*, so the `Agent` base class's exact contract — constructor args, `MAX_ACTIONS`, what it does with the returned action — **is being read second-hand from notebooks rather than from source.** **Every one of the five is downstream of that**, so the repair is not five checks but **check out the repo and read the contract from source** — which is the session's own shape one more time: **five items reconstructed from fragments, with the primary source available and unopened.** The docs interleave two APIs and **only the harness runs on Kaggle** -- building against the toolkit's `step(reasoning=…)` signature works locally and does not run there. Same class as the **16 KB `reasoning` cap that raises rather than truncating**, which no platform doc states. **Everything works, nothing runs**, and the cost is a submission window rather than a debugging session. §6 adds two more of the same kind: **`agents/__init__.py` must be rewritten** because the shipped one eagerly imports packages that are not installed, and **the gateway readiness loop must run before anything else.** §6 also flags its own uncertainty — the submission schema differs between samples and **one looks stale; confirm against the competition page** |
| **reset vs advance INVERTS the verdict — and the chain is now complete** | `ARC_AGENT` §21.5 ⭐ · §1 · §2 | **the specification the withdrawn boundary build did not have.** Both events change the board, so **both produce a large residual, and the meaning inverts.** A level **RESET** after a loss returns a **KNOWN** board — *on a board you have already modelled, a residual has no excuse* — so a spike means **your model is wrong: real evidence, demote.** A level **ADVANCE** gives an **UNKNOWN** board with new mechanics by design, so the same spike means **normal: evidence about nothing yet.** ***Same number, opposite verdict, disambiguated for free by which event fired.*** **And the failure without it is precisely targeted:** *the demotion logic poisons itself at exactly the wrong moment — every level advance would demote the good terms that carried the last level. **The agent would punish its best work for the crime of a scene change.*** **The chain closes across three sections**: §21.5 gives the rule, **§1 says COMPETITION collapses the two events in the API's semantics**, and **§2 says the frame still carries `full_reset: bool` and `levels_completed: int`** — so the discriminator is recoverable from the data even where the platform stops exposing it as a distinction. **The boundary revert was withdrawn because the build did not turn on this. This is what it was supposed to turn on** |
| **a completion is a settle AND a regime warning, and both are needed** | `ARC_AGENT` §21.4 | **open, and it is a both-and rather than a choice.** The two readings pull opposite ways and **both are correct**: the hypotheses live at a level completion **got the crux, so credit them** — and ARC changes mechanics between levels, so **do not trust them in the next level until re-tested.** ***Crediting without the decay is the incumbency pathology; decaying without the credit throws away the only positive evidence there is.*** `Standing.decay` exists for rejections with a half-life; **there is no boundary decay** — `demote_unpromoted` was built and reverted, correctly, because it did not turn on §21.5's discriminator |
| **`disproof` — BUILT 2026-08-26, and the first version was vacuous** | `ARC_AGENT` §21.2 | **CLOSED.** Written at the one site where it is not vacuous: **the discriminating draw**, where `choose` already computes how many distinct values the live candidates predict per owed slot. **74 of 2,520 bet rows carry it (2.9%)** — exactly the discriminating draws — and it is **absent rather than null** elsewhere, following `of`'s stated intent. **THE FIRST IMPLEMENTATION WAS WRONG AND I CAUGHT IT ON THE MEASUREMENT, NOT ON REVIEW.** It recorded the *set of values the candidates predict*, and every one of the 74 rows read **width 7 — the whole of Z₇.** True, and **UNFALSIFIABLE: it lists every possible outcome, so nothing can contradict it.** That is the tautology guard's own subject — a statement admitting everything predicts nothing — arriving in the field built to prevent exactly that. **The falsifiable form is what the action BUYS**: group the candidates by prediction, and `live − largest bucket` die **whatever happens**. Now `{live, splits, refuted_at_least, by}`, and it **VARIES** — 40, 54, 55, 56, 70, 71 across the 74 rows — so it distinguishes a well-chosen discriminating action from a poor one. **§21.2's discriminator holds: presence with a number is an experiment, absence is a stall.** Prior state: A level-resetting loss returns the agent to a known board, so **choosing to die is a way of buying an experiment — *aiming the variation*, which §2's bill ledger names as THE FRONTIER MOVE.** It is also one step from farming, and this project has been burned there: `bounds.py` exists because ***the Redux harness once violated this by force-RESETting on GAME_OVER to farm ~18 unearned attempts.*** **Two discriminators, both checkable.** The mechanism: `ResetGate` bans **the AGENT calling RESET**, while a game-inflicted restart is the world's own rule and not a bypass of it. The intent: **an experiment states its hypothesis AND ITS DISPROOF BEFORE THE ACTION; farming states nothing and just wants the board back.** §21.2: *the discriminator is a gate check and the fields already exist.* **Here `expect` exists — it IS the bet, recorded before the action — and `disproof` is recorded nowhere.** Without it a deliberate death and a stall are the same row. **And §21.2 names the number to publish beside it: what fraction of the action budget went to deliberate deaths. *If that is 40%, someone should see it rather than infer it.*** |
| **the retro sweep + level-completion credit** | `ARC_AGENT` §21.3 | **built, and its ARC consumer is specified.** Seven levels means **seven separate positive settlements, not one**, so the reward channel is sparse but is not the single bit a game win would be. But **a level completes at step 500 and the last action did not cause it — the trajectory did**, so crediting the final action is the delayed-effects bug at the scale of a whole segment. **The sweep is the mechanism**: on completion, re-examine the segment for which hypotheses were live, which terms had settled, which residuals closed along the way — **retrospective credit over a RECORDED history, costing no actions.** `tether` already emits `retro` rows for exactly this operation on residuals. **The mechanism exists; the level-completion trigger does not** |
| **COMPETITION collapses reset and advance — and names where the discriminator lives** | `ARC_AGENT` §1 | **the fact the withdrawn boundary build needed.** Kaggle **forces COMPETITION and it cannot be opted out of**: `make` may be called **exactly once per environment**, the scorecard cannot be read mid-run, and **game resets SILENTLY BECOME LEVEL RESETS.** So the platform hands the agent one signal for two events. The loop's level-change handler fires either way — it clears `bound`, `trace`, `owed_import`, `abstained`, `candidates` and keeps Γ, on the stated ground that *a new level is a new instrument: the verdict was about the OLD slot set* — **and cannot tell an advance from a reset-after-loss.** **Reset-versus-advance was the stated discriminator the boundary revert turned on**, and §1 says where it must come from: **`levels_completed` is in the frame**, which is also why the mid-run reward signal cannot come from the scorecard. **Nothing in the loop depends on re-making an env, so that half is satisfied by construction** |
| **RULED 2026-08-27 — availability is state-conditioned, and `never_live` claims too much** | Isaiah | **the ruling that unblocks Phase 2, and it changes the shape of the fix rather than only the denominator.** `[I]` *if an action suddenly becomes available or unavailable, **it is because a condition of some sort has been met or unmet**.* **So availability is BOTH** — an observation about the world, because a change in it carries information about a condition; **and** level-scoped, because conditions are level-specific. Not either/or. **AND THE SECOND HALF IS THE SHARPER ONE.** `[I]` *if an agent tries all the available moves and nothing changed, **it is possibly stuck somewhere (like trapped by walls) or it does not understand what state or mode itself or the game board is in that requires a particular move OR SEQUENCE that it has not done**.* **So `never_live` firing has THREE causes and the row collapses them into one**: the instrument is dead; the agent is positioned where actions look inert (Q18's wall); or **the required thing is a SEQUENCE and the denominator is over ACTIONS.** **Trying every action individually and seeing nothing does not exclude a two-action sequence doing something** — so *I drew every action on offer and nothing changed* is a positive bound over SINGLE ACTIONS being read as a bound over WHAT THE AGENT CAN DO. **Those differ by exactly composition, which is §15.5's verb gap**, and the cheap correct move is to narrow the claim to what it supports rather than wait for routines |
| **`0a` operand arity — PARKED 2026-08-27, ruled** | `ARC_BUILD_PLAN` Phase 0 · Isaiah | **not built, and the reason is measured.** `0a` wants arity N with cap 4. **`Ctx.operands` is already N-ary; only `Term.operand` is unary — so the work is binding-side only.** But **only `take` reads an operand and it reads `operands[0]`. NOTHING READS INDEX 1.** So the loop half alone is **structurally complete and observably inert**: 32% of closure yields read an operand (185 of 584 at depth 3), bindings per candidate would go **5 → 65**, and per-mint binding work **925 → 12,025 — 13× for zero capability** until an atom consumes past index 0. **And the atom that would is the DOMAIN's, not the loop's.** Appending one honours the atom-order pin, but the atom COUNT moves `space_estimate`, `coverage`, `λ`, `V` — **and every number on this panel was measured under the current set**: the false-mint rate, the exponent, chunk reuse, the transfer curve. **Phase 3d replaces the atom set with grid transforms anyway, so a toy-world operand-1 atom is scaffolding for a panel that gets replaced.** **Ruled: neither half until Phase 2 says what an interaction looks like on a real board** — the same argument that made the availability row a plain event |
| **`actions()` is a fixed tuple; ARC's action set varies per frame** | `ARC_AGENT` §2 · **and §15.7 says what the growth IS** | **BLOCKING FOR ARC, and it is `never_live`'s SECOND unsound premise.** `FrameData.available_actions` is **raw ints that change per frame**. The `Env` contract is `actions() -> tuple[str, ...]`, read once, and **`never_live(len(self.actions))` gates on that fixed count** — so *I drew every action on offer* is computed against a total that no longer means what it meant. **This is independent of the `tried`-has-no-state defect and stacks with it**: one makes *every action tried* insensitive to WHERE, the other makes it insensitive to WHEN. **And TID251's own message anticipates only GROWTH** — *add `actions()` to the Env contract and grow it through step 7* — which is monotone. **ARC's set also SHRINKS**, and an action becoming unavailable is not the same event as one never having existed. **AND §15.7 RULES ON THE GROWTH DIRECTION**: *IMPORT was closed for a lone agent, and is now **open via nature — action-set growth and value-domain growth ARE IMPORT EVENTS, and should be recorded as such.*** So a widening action set is not a contract violation, it is **step 7 firing**, which is exactly where TID251's message already points it. **Shrinkage still has no home** |
| **the ground is `levels_completed`, and there is no score** | `ARC_AGENT` §2 | **the eight-slot contract's `ground`, named from the package rather than from prose.** `FrameData` has **no `score` field** — a sample notebook records having to replace `latest_frame.score` with `levels_completed`. **`levels_completed == win_levels` is a game win, which is the terminal condition's first clause already in `CLAUDE.md`.** And the frame carries **`full_reset: bool`** alongside `levels_completed`, **which refines the row above**: COMPETITION collapses the two events in the API's SEMANTICS, and the frame still carries both fields to tell them apart |
| **`frame` is a stack, and the settled board is `frame[-1]`** | `ARC_AGENT` §2 | **a trap with a receipt.** `frame: list[list[list[int]]]` is **3-D — a STACK of 2-D grids, not one grid** — and the animation plays oldest to newest. `new-horse`'s `unwrap_frame` worked it out the hard way and wrote down why: **acting on `frame[0]` means betting on a board the world has already left.** Which is the bet-side error the whole loop is built to make impossible, available for free through a shape assumption |
| **two APIs, and one of them does not run on Kaggle** | `ARC_AGENT` §1 | **a build-target fact, recorded because the platform docs interleave the two.** The `arc_agi` **toolkit** has you drive the loop — `env.reset()`, `env.step(action, reasoning=...)`. The **`ARC-AGI-3-Agents` harness** drives you: subclass `Agent`, implement `choose_action()`, attach `action.reasoning`. **All three sample notebooks use the harness, Kaggle uses the harness, and building against the toolkit's `step(reasoning=…)` signature would not run there.** OFFLINE is the development mode — ~2,000 FPS, no rate limit, no credentials, no scorecards |
| **ARC reintroduces the confound Stage 2 removed** | `ARC_AGENT` §5 | **a property of the target domain, and it changes how a failure reads.** Stage 2 gave slots BY NAME on purpose -- *a gridworld tests perception and the loop at once, which is two experiments in a trench coat* -- **so that a failure was unambiguously a LOOP failure.** §5: **ARC removes that choice; slots have to be found.** So an ARC failure is not unambiguously a loop failure, and **this compounds Q27's tiering rather than duplicating it**: ARC is a step down in ground quality AND a reintroduction of the confound. **Both belong in the run report before the run** |
| **`MAX_REASONING_BYTES` raises, and no doc states it** | `ARC_AGENT` §3 | **a hard external constraint, recorded because it is invisible.** The platform's `reasoning` field is an opaque JSON blob echoed back verbatim, capped at **16 KB by a validator that RAISES rather than truncating**, and **§3 notes the platform docs state the limit nowhere -- it is in the package.** So an oversized derivation record **fails the action** rather than being clipped. **A full cycle's ledger will exceed it**, which is why §3 splits full-ledger-local from digest-on-the-wire |
| **the echo does not reach the live agent at all** | `ARC-AGI-3-Agents` source | **§3 is true of the API and FALSE OF THE HARNESS.** §3 builds on *`frames[i].action_input.reasoning` returns what was attached to the action that produced frame `i` — **the agent can read why it did each past thing from the environment's own record of it**.* **`_convert_raw_frame_data` constructs `FrameData` from eight fields and `action_input` is not one of them.** In the live loop `self.frames` are those converted objects, so **the echo is dropped by the harness's own conversion.** `action_input` is read in exactly one place: the **`Playback`** class, from a recording file. **So the reasoning survives into the RECORDING and not back to the playing agent** — §3's *what appears in replays* holds, and *the agent can read its own past reasoning* does not |
| **`MAX_ACTIONS` is 80 in source, and the corpus anchored 1000** | `ARC-AGI-3-Agents` @ `agents/agent.py:22` | **the anchoring discussion was about a different number.** `Agent.MAX_ACTIONS: int = 80`, commented *to avoid looping forever if agent doesnt exit*, and `main()` enforces it as a hard loop bound. §22.1 defended **1000** with *humans complete a level in under 500 actions, so this is the 2× ceiling* — **a legitimate anchor for a value 12.5× the base-class default.** A subclass override is the mechanism (one in-repo agent sets `MAX_ACTIONS = 1000000`), so **the anchor still applies — to a number the project must set deliberately rather than inherit** |
| **the echo is not corroboration** | `ARC_AGENT` §3 | **pre-empted before anything was built on it.** The platform returns the agent's own `reasoning` blob attached to each past frame, so **the agent can read why it did each past thing from the environment's own record**. §3 refuses the tempting reading: *it is the agent's own words handed back by a server that stored them. **No independence is gained.*** Figure 7's mirror chain, applied to an API. **What IS gained is a tamper-evident timestamped copy outside the agent's process** -- it survives a crash and it is what appears in replays |
| **`tried` has no state context** | `DISCOVERY` Q18 · **and `ARC_BUILD_PLAN`'s second pass found it first** | **BLOCKING FOR ARC, not open. NOT A NEW FINDING** -- the second pass already states the diagnosis (`set[str]`, action labels with no record of the state they were drawn from), the fix (`tried` keys on `(action, state)`), and the unbuilt larger half (coverage-first as a phase). **What this reading adds is the CONSEQUENCE, which that entry does not state:** A correctness defect the moment the agent meets a world with obstacles, **which is the target domain**. And it produces **a false abstention that is indistinguishable from an honest one** -- same `park` row, same `coverage`, same *unreached at this budget, NOT unreachable* caveat, same denominator. **The one failure mode the abstention claim cannot afford**, arriving wearing the record that was built to make abstention trustworthy. Q18: coverage-first, then **re-probe any unmapped action FROM A DIFFERENT CELL each time**, because *an action can look inert merely from having been tried twice against a wall.* **Inert is a verdict earned by trials, never assumed early.** `Drive.tried` is `set[str]` -- action NAMES, no state. `never_live` is sound here anyway because it also requires zero misses across the WHOLE RUN and `snaps` slots update every step, so state varies and no action can hide behind one position. **`snaps` has no walls. ARC does**, and there a cornered agent draws every action, sees nothing move, and `never_live` writes `unreached` about the world when the true reading is about its position. **The positive-bound reasoning in the docstring is right and its premise is a panel property nobody stated** |
| **Q18's phase, not flag** | `DISCOVERY` Q18 | **open.** *An agent that pursues a goal before knowing what its own actions do is betting with an unmodelled slot, and the slot is itself.* Q18 asks for coverage-first as a **phase rather than a toggle** -- goal pursuit gated on having mapped its own effects. `Phases` has PROBE / DIRECTED / STRATEGY and `by` names the site that chose, **but nothing gates pursuit on coverage** |
| **what may cross between agents** | `ARC_AGENT` §7 | **deferred, and NOTED so the deferral is not silent.** `Swarm` is population scale — one agent per game, threaded, scorecard lifecycle, replay links — which is step 6 and out of scope. **The membrane rule is the design constraint when it arrives**: what crosses between agents is **a METHOD, never a recording of one game's success.** Generators cross up, playback never does. **§7's own warning is the memorable form: *a shared library that accumulates replays is the failure mode with a nice name.*** |
| **the `[REPLAY]` membrane rule, kept without its name** | `DISCOVERY` Q13 · **Figure 4** | **ok, unnamed and unchecked.** Q13 asks for range tags -- `[EP]`, `[OWN]`, `[COL]`, `[REPLAY]` -- and singles out `[REPLAY]` as **Figure 4's membrane rule enforced in the record: playback is never narrated as a fresh decision**, costing nothing and preventing a real error. **No tag exists anywhere.** But the one place playback could occur is the `retro` sweep closing a residual parked in an earlier cycle, and there the rule is kept by construction with its reasoning stated inline: *the sweep is not the target slot's per-step loop running a second time... **the target is named, not impersonated***. **Honoured where it applies, named nowhere, enforced by nothing** -- and the argument for tagging it is the ATOM-ORDER PIN's argument, not a risk assessment: **the next person to touch the retro sweep has no way to know the rule exists. Correct by habit, and habit is not a mechanism** |
| **a constant with two consumers** | `BUILD_PLAN` §7 · measured | **gap, and nothing asks.** ANCHOR checks that a number HAS a basis. `cfg.budget` has one, and it is true of one consumer and silent about the other: never binds on closure yields (1,884 of 4,000), always binds on the `_round_trip` domain sweep (16,807 needed). **A basis that is true and partial reads as complete**, and no rule asks how many consumers a constant has. Same shape as the six narrow subjects, on the constant instead of the rule |
| one constants block | `DISCOVERY` Q14 | **gap** — per-site anchors enforced by a rule instead; deviation, now recorded |
| a basis attached to the wrong question | `DISCOVERY` Q24 | **declared limit** — `max_depth = 3` HAS provenance (the chunking falsifier) and the principled bound is a different quantity (Ashby's requisite variety). **ANCHOR checks that a number has a basis. It checks NEITHER of the two properties that make a basis an anchor.** (1) that the basis answers the question the number is used for — this row's original finding. (2) **that the basis is EXTERNAL TO THE FRAME**, named by `ARC_AGENT` §22.1: *"increased for better pattern exploration"* is **tuned toward a desired behaviour by the frame that benefits from it** and is the failure mode; *"humans complete a level in under 500 actions, so 1000 is the 2× ceiling"* is **anchored to a measurement the agent cannot move**. **A human's move count is not a quantity the agent produces, so using it as a reference is not self-scoring** — Figure 1's rule deciding which of two justified numbers is legitimate. **Both are bases. Only one is an anchor, and the checker cannot tell them apart.** §22.1's diagnosis of the original defect is the one to keep: ***what was missing was never the basis — it was that the basis was in your head and not in the constants block.*** Not closable statically — declared, like default arguments |
| provenance standard | `DISCOVERY` Q19 | **gap** — `0.98`'s docstring names the measurement that forced it *and the value that would have been wrong*. No constant here meets that bar |
| **the eight-member contract assumes PURITY and never says so** | `world.Env` · measured at `2b` | **a property of the CONTRACT, not of the code that tripped on it.** `slots()` and `observe()` are separate members and nothing says they may not both be called per step — **so a domain whose decomposition is STATEFUL advances its state twice and the two members disagree.** Perception cannot be pure: tracking is what makes a slot the SAME slot next frame. It surfaced as a `KeyError` on a slot present in one call and not the other, and the fix is that **the decomposition is a function OF THE FRAME** — computed once, cache cleared on `step`. **The next domain with stateful perception hits this identically**, which is why it is filed against the contract |
| the checker imports nothing | `DISCOVERY` Q23 | **ok, UNCHECKED** — *the Gate receives a reification, not the running machine, and a checker over data is domain-blind by construction.* `gate.py` imports `json` and `sys`; `conform/kernel.py` only stdlib. **Holds, and no rule enforces it** — and `BUILD_PLAN` §5's falsifier says *if the inliner wires it to the loop, the soundness argument is gone* |
| A1 — closure generated, not stored | `PHILOSOPHY` §14 · `CONFLATIONS` A1 | **ok** — REACH, written to the property |
| **the proctor rules themselves** | `PHILOSOPHY` §0.2 | **ok, and they are not what they look like.** *Never encode the answer · the proposer proposes, never scores · a hardcoded procedure that pre-answers is a fault even when correct · generators cross up, playback never does · residue is the agent's to close.* These read as a working style. **They are the clauses of a substitution constraint**: natural selection is the only known process that produced open-ended structure with no designer, so it is both the existence proof and the specification, and *unnatural selection* is legitimate only where it preserves all six of its ordering properties. **Relaxing one does not make the build faster -- it makes the result authorship rather than selection, and an authored result does not transfer because nothing external tested it** |
| **the builder/gate split: three sources, three assignments** | `DISCOVERY` Q2 · `BUILD_PLAN` Stage 4 · `speak.py` | **wrong in ONE CLAUSE, and I over-charged this row first time.** Q2 and Stage 4 say **the builder reads AGENT STATE and the Gate reads the world and the ledger**. `speak.py` line 3 says **the builder reads the LEDGER only and *the gate reads the world*.** **`ARC_AGENT` §6 sides with `speak.py` on the first half** -- *`speak.py` reads the ledger only* -- so **builder-reads-ledger is two sources plus the code, and is not the error.** The error is the second clause alone: **the Gate does not read the world.** The code does neither: **`speak.sentences/account/verify` and every `gate` check all take `rows: list[dict]` -- both read the ledger**, and `gate.py` imports `json` and `sys`, so **it never reads the world at all.** That last point matters beyond tidiness: **Q23's entire soundness argument is that the Gate receives a reification and is therefore domain-blind**, so a docstring asserting the Gate reads the world contradicts the reason the Gate is sound. **The arrangement that exists is coherent** -- one record, `speak` renders it, `verify(rows, said)` checks every sentence traces to a row, `gate` checks form -- **it is just not the specified one, and nothing says so** |
| **the two dropped check currencies** | `DISCOVERY` Q2 | **deviated, with the reason recorded under a different question.** Q2 names three currencies plus PARSE: **LEDGER** (looked up in earned records), **EXECUTABLE** (run through the world's own mechanics), **COMPLETENESS** (a set checked AS A SET against what actually differed). **This gate has LEDGER only.** The reason is good and is Q23's: a checker that ran things through the world's mechanics would not be domain-blind. **But the deviation is recorded nowhere** -- Q23 is filed as satisfied, Q2 as unread. And Q2's own open question goes with it: *the completeness check measures map fidelity, differing versus reported, and nothing reads it as one* |
| **the gate declares no mode, and requires one** | `DISCOVERY` Q21b | **gap, and it is SELF-APPLICATION, not tidiness.** Q21b turns §0.2 into build properties, one of which is *a mode is declared on the run's output, **including on the run's own diagnostics***, under the heading **the Gate is subject to the seat's own prohibitions**. **`lint` meets it in full** -- *a static pass is single-frame: no promotion, no import, no second scale*, plus 25 properties it cannot see in four categories. **`gate` emits `{verdict, check, token, rows}` and declares nothing** -- while its check 1, `_mode`, REQUIRES the ledger to declare one. **A law enforced outward and not inward is the special pleading §0.2 says is unavailable**, and Q23 already supplies the content it would declare: the Gate reads a reification, so it cannot see the running machine |
| **the observer's defect, met by accident** | `DISCOVERY` Q21b | **ok, and it happened live.** *A new instrument's first output is a claim about the instrument, not about the system.* The nulls sweep built this session reported `allowed: true` on 32 rows as a guard that never denies. **It was a false positive** -- the refusal is a different event, `hold` -- so **the sweep's first finding was about the sweep.** Predicted by the corpus, and not recognised as the prediction until afterwards |
| **THE SECOND FIREWALL — harness config is the seat's, the frame is the agent's** | `pyproject.toml` · measured | **stated, entries pending the bridge.** The first firewall bans GAME FACTS — `RULES`, `TRUTH`, `DELTA`, `ACTIONS`, `M` — with `demo.py` and `test_gate.py` exempt by office. **The checkout made a second class of thing readable, and it is the more dangerous one BECAUSE IT SOUNDS ADMINISTRATIVE**: a config value is easier to justify reading than a rule of the game, which is exactly what makes it easier to leak. **THE SEAT MAY READ THE HARNESS. THE AGENT MAY READ ONLY THE FRAME.** `MAX_ACTIONS`, the import graph, signatures, how `FrameData` is constructed, what the platform will and will not deliver — **all the seat's business, and reading it is how we know whether a submission runs at all. None of it enters the library, the priors, the grammar, or any decision.** **The agent discovers its budget by running out, or is told by the frame — never by a number someone read from a config.** **THE RISK IS IN ENCODING, NEVER IN READING, and it is checkable rather than trusted**: *if the agent's behaviour changes when the number changes, the number is in the agent.* **MEASURED 2026-08-26** on this loop's own budget, `run(cycles)`: **a 40-cycle run is a BIT-IDENTICAL PREFIX of a 90-cycle run on all six panel worlds.** The budget is not in the agent. **And `MAX_ACTIONS` sits in a specific place: a RUN PARAMETER the seat sets, not a fact the agent holds** — the 2× human ceiling is a legitimate external basis for choosing it, and the choice belongs to whoever configures the run. **The ban cannot name `agents.agent.Agent`, because the bridge must subclass it; it is the CONFIG the loop may not read, bridge exempt by office** |
| **gate the wiring, never gate the design** | `PHILOSOPHY` §1 step 6 | **ok, verified across all fourteen checks.** Nine gate checks and five lint rules, and **every one grades FORM**: mode declared, step order, inputs arrived, routing bins, guards recorded including those that passed, settlement provenance, no filter verdict, cuts ranked and reversible, abstention denominator; anchor, singleton, nofail, reach, isolated. **None grades outcome, accuracy or quality.** The rule's reason is that *the wiring has a fact of the matter and a behavioural self-test does not*, and that **a bad gate applied often is worse than no gate, because narrowing amplifies whatever the gate rewards** |
| **describes rather than decides** | `PHILOSOPHY` §13 | **the same failure at four scales, and the fourth is a discipline.** `v4-cold` spoke without deciding; `new-horse` was typed without running; `Nexus` was imported twice; **and cybernetics itself fragmented into a vocabulary that survived without its content** -- Pickering's charge that the second-order revival was a linguistic turn abandoning the technical practice it inherited. **The defence is identical at both scales: the framework has to be the thing that DECIDES, or it becomes the thing that describes.** Verified here -- no path from perception to action avoids the composed utterance -- with the measured caveat that **it has never once refused** |
| **the internal-gate temptation** | `PHILOSOPHY` §1 step 6 | **predicted, and the seventh law is an instance of it.** §1 states its own failure mode in advance: *if the only trustworthy gate is external and rare, the build will be slow and the landscape flat -- **and the temptation will be to manufacture an internal gate.*** `false_mint_rate` is that: computed over CLAIMS, by a frame whose mechanism changes what counts as a claim. **A correct mechanism was withdrawn on it.** The law was derived from the wreckage; §1 had named the category |
| the seven laws | `conform/lint.py` · **Figure 10** | **ok** — and the figure is their source: *a declared meaning is not a grounded one → **install what can be violated***; *the convention does not fix the bug, it makes the bug statable*. The laws were written from defects; the figure had the general form |
| **the refactor has TWO referents, and both are the same move** | `PHILOSOPHY` §2 · `ARC_AGENT` §15.4 | **the board item is bigger than it was filed as.** §15.4 on DreamCoder: **the abstraction sleep phase refactors the library**, finding subexpressions common across many solutions and naming them as new primitives, scored by compression over the whole corpus — ***that is "nothing refactors Γ", answered.*** And it is **the same bargain at a different scope**: per-mint chunking is local and greedy, **global refactor is periodic and finds chunks no single mint could see because the evidence is spread across episodes.** §15.4's own closing line makes the join: *local chunking on accept, global refactor on a schedule — **and the second one is the voluntary payment the ledger says nobody schedules.*** **So the refactor item covers the code's weight AND Γ's structure, and §2's ledger row is the same move for both** |
| **the refactor is a payment, not a cut** | `PHILOSOPHY` §2 | **corrects my own framing of the weight finding.** I called subtracting to 1,500 *gaming the metric*, and that is true of cutting to hit a number. It is NOT true of the thing §2 names: *refactor -- restructure commitments mid-stream -- **pays a bill already owed, before it compounds** -- **the one voluntary payment, and nobody schedules it***. **Every other move on the bill ledger relocates the cost or lowers a coefficient; the refactor is the only one that discharges a debt early.** So the weight row's remedy is not *cut to the target* and not *ignore it* -- it is the one payment the corpus says nobody ever schedules |
| **under 1,500 lines total** | `BUILD_PLAN` §7 · **dated by `ARC_AGENT` §6** | **wrong, and it is OURS -- AND THE TARGET WAS ONCE MET.** §6 records the core as **eight modules and about 1,481 lines**, which is INSIDE the 1,500 target. **The same eight modules are 2,211 today: +730, +49%.** So this is not a target that was never achievable; it is one that was achieved and then left behind, and the growth is datable to after §6 was written. — the nine files are **2,374 lines**, 1,785 discounting blanks and comments. `tether.py` alone is 936, **39% of the package**, against an estimate of *medium*. This session is most of it: **net +388 across the nine, +278 in `tether.py`**. The plan attaches the rule rather than leaving it to judgement — *v1–v6 died of weight; if a stage is pushing that, **the design is wrong rather than the estimate***. Every addition was justified singly, which is the condition the rule names, and **nothing measures it** |
| paired arms cannot corroborate | **Figure 2** | **ok, learned the hard way** — *one evidence pool: they never talk and still agree, so **the agreement is the pool talking***. carried-vs-cold shares its worlds, so **only disagreement between the arms carries information**. Read as confirmation once, and retracted |

---

## Sections read for conflicts

**READ AGAINST WHAT, not merely read.** A section read before a finding and the same section
read after are different reads, and the read-state's `read` is weaker than it looks. **§5 is
the demonstration**: first pass it is a rule about analogies; against §4's arrival finding it
is **the verdict table for the library that actually exists**, and the verdict was already
written. Where it mattered, the entries below say what a section was read against.

    ARC_BUILD_PLAN   all
    DISCOVERY        **COMPLETE — every question, plus the §6 carry-list.** Q4's typed
                     grammar is inherited exactly and is the strongest confirmation in the
                     file; **Q2 found the `speak.py` docstring contradicting Q23's own
                     soundness argument**; Q26 turns the shadow test on this project's
                     choice of domain and it is unanswered; Q27's tiering decides what an
                     ARC result may be read as. **Q6 is unbuilt BY DESIGN** — perception is
                     deferred, Stage 2 gives slots by name so a failure is unambiguously a
                     loop failure — and the
                     last four read produced CONFIRMATIONS rather than rows: the guards
                     are built as ruled (SUPPORT x REACHABILITY x NOVELTY, MDL after);
                     citability is built (`cite`/`hold`); the seat stack is a data
                     structure, not an argument; and Q10's bridge was VERIFIED AT SOURCE
                     rather than assumed -- one importer of `grammar`, eleven `compose`
                     sites, one `env.step`, and `G.Ill` returns False before `perceive`
                     runs, so an ill-typed utterance costs the step. The type system is
                     load-bearing here, which is the condition Q10 set for it not being
                     decoration
    PHILOSOPHY       **COMPLETE — every section.** **§0.2 is the strongest**: the proctor
                     rules are a SUBSTITUTION CONSTRAINT rather than a style, and its
                     *supply a prior* clause found a built-and-never-run code path on the
                     next build's critical route. **§4 with §9 is the largest fact** —
                     arrival has never occurred, and **§9 stated it first, about itself**,
                     so the reading added the number and the cause rather than the finding.
                     **§5 re-read against §4** carried the verdict name the numbers had
                     lacked for eleven batches. **§2, §10 and §15 each independently name
                     the search-reduction factor as the frontier quantity, and nothing
                     computes it.** §6 corrected a citation of mine; §13 caught two more
                     lineages that would have been counted twice. **There is no §17** — the
                     document ends at §16.9
    ARC_AGENT        **COMPLETE — every section.** §15.5 is the deepest finding in the
                     file: **the grammar has no verbs**, thirteen state primes and not one
                     action or time prime, which is why routines do not fit and why
                     `STRATEGY` is zero. §21.5 ⭐ supplies **the specification the withdrawn
                     boundary build should have turned on**. §9 knew the abstention
                     measurement would be lost on ARC **before anyone framed the move as a
                     loss**. §22.4 aims *never encode the answer* at a metric
    BUILD_PLAN       ALL — and it was the right document to resume on, being a PLAN and so
                     the class the seventh corollary reads first. Stages 0/1/2/5/6 confirm
                     at source (`_filters` and `_cuts` are gate checks 7 and 8; molecules
                     are stamped `prior`; `opaque` is QUADRATIC against affine atoms, so it
                     is outside the closure at ANY budget rather than merely past a depth
                     bound; false-abstention is reported beside abstention). **Its §7
                     falsifier fired against this session's own output**
    SNAPS_PLAN       ALL — and four of ten sections overturned a published conclusion
    FIGURES          ALL 11. They are readable as SVG text and were opened last. They
                     produced a scoping correction, a routing precedent used three times,
                     a named collapse I had diagnosed the hard way, the source of the
                     checker laws, a theorem behind the UNREACHED ceiling, and three
                     mechanisms no document carries: cascade ranking, split-before-search,
                     and R = h² × S. PHILOSOPHY §3 says at least one still carries a
                     retired answer, so they are primary and not automatically current

## Not yet read

    (nothing)

**THE RANGE NOTATION WAS HIDING ENTRIES.** `Q20–23` does not name **Q21b** or **Q21c**, and
`§0–7` reads as one section where there are four: §0, §0.1, §0.2, §0.3. A list written as
ranges cannot be checked against the file it describes -- so it is enumerated now. **§0.2 is
*why every law applies to itself*, which is the corollaries' own subject, and that makes it
the highest-priority remaining section by content rather than by position.**

**Expect the remainder to be reasoning behind decisions rather than specifications of
mechanisms** — fewer *this was built wrong*, more *this was decided for a reason nobody
carried forward*. **That expectation was met and then confirmed by the stopping rule.**

**THE READING IS STOPPED, on its own rule and not on exhaustion.** Three consecutive
batches produced no actionable row: `PHILOSOPHY` §7/§11, then `DISCOVERY` Q7/Q11, then
`DISCOVERY` Q10/Q22. The rule was set at two or three before the batches were read, which
is what makes stopping here a result rather than a decision to stop.

**What remains unread is recorded, not closed.** The yield curve fell off in the order
predicted — figures and `SNAPS_PLAN` overturned published conclusions, the mechanism
sections corrected specific builds, and the reasoning sections confirm what is already
built. **A section listed above is a place to look when a row goes `open`, and the four
confirmations are the evidence that looking there works.**

---

## A standing control for this panel

**The cold arm is required on every level-over-level number**, and it is what caught the
error below.

**RETRACTED: `the DS 0.4 ladder drifts toward easier worlds`.** Claimed on 10 seeds from a
cold-arm rise of 2.30 → 3.30. **At 40 seeds it is 2.92, 2.67, 2.95, 2.88 — a difference of
−0.05 at 0.2 SE. The ladder is FLAT, not easing.** `in_closure` likewise: 24%, 22%, 22%,
29%, non-monotone, +5% at 1.0 SE.

**What survives, and it is the part that matters.** The cold control's own finding stands,
because it is paired within seed: a carried agent binds *exactly* what a fresh one does at
every level, 0.00 difference throughout. **The 2.30 → 3.30 appeared in both arms identically
because it was the same noise in the same worlds — which is the control working, not a
drift it detected.**

**And the transfer negative is cleaner for it:** flat behaviour on a flat ladder is honestly
flat, rather than stagnation masked by easing.

---

# Already in the code, and not connected

**The index's other use.** Not *what does the corpus say* but *what is already built that
belongs together* — because the same instrument has now been built twice in one session,
days apart, by the same reader.

| these are one mechanism | and they were built separately |
|---|---|
| `never_live` + the monotone `_integral` | Q17 names them as one: *integral flat because nothing surprising happened* versus *integral flat because nothing is arriving*, **read against the record rather than against the moment**. `never_live` is that predicate; the integral is what makes it readable. Neither build knew about the other |
| `_bindings` + habitat enumeration + the interface question | §16.5 is one procedure — *list everything in contact with the residual*. Three separate problems this session, one absence: nothing enumerates contact |
| `space_estimate` + `type_report` | the denominator is `V^d`; the corpus says `λ^d`; `λ` is computed and used in one `demo.py` print. **The number and its consumer are both present and unwired** |
| `Standing` keyed on `term.name` + `units()` dedup key | the same key defect with two consumers — a name carries its operand binding while the thing being reasoned about does not. Fixed in `units()`, live in `Standing` as pathogen mimicry |
| `starving()` + §20.3's third stopping case | the computation and its meaning. It is reported and branches on nothing, and §8 says branching is what would be wrong |
| **a human's numbers are a pressure to encode priors** | §22.4 is *never encode the answer* aimed at a METRIC. **The 30/10/5 phase counts are a human's, with a human's priors** — the agent starts with nine sensors and no affordance profiles, **so expecting 40 moves is not a fair target and *would be a selection pressure toward encoding priors to hit it*.** The discipline: **compare the SHAPE, not the counts.** *The ratio between phases, and its movement, is comparable. The absolute count is not — yet.* **And the closing clause is the good part: when it becomes comparable, THAT IS ITSELF THE RESULT** | `ARC_AGENT` §22.4 |
| **two clocks — BOTH BUILT, and `execution_gap` with them** | **`Clocks.report()` returns `steps_to_model`, `steps_to_win`, `execution_gap`, and a `reads` string naming §22.5's four cases with their link attribution.** This sat on the board as a MEASUREMENT TO TAKE; it is built. **It moves to the defect list rather than off the board** — see the denominator mismatch below. Measured: `execution_gap` 2 and −2 across the two worlds that reached both clocks. Original: | §22.5: **understanding and winning are different events and they fail differently.** `steps-to-model` — the transition residual falling and staying low — **a long value means perception or minting, links 1–2**; `steps-to-win` — `levels_completed` rising — **a long value means you modelled it and could not act on it, links 3–5.** `steps_to_model` exists in the loop and reads NO SLOT OWES rather than an averaged error. **The gap between the two is the cost of EXECUTION as distinct from the cost of LEARNING**, and nothing computes it | `ARC_AGENT` §22.5 |
| **THE PHASE CURVE, SWEPT 2026-08-26 — and it does not measure what §22.2 names** | **6 DS x 12 seeds x 5 levels** | **THE READING IS UNAVAILABLE AS INSTRUMENTED, and that is the finding.** The sweep ran: PROBE share is **0.84–0.99 at every level and every DS**, and the L0→L4 change is **POSITIVE** at every DS but 0.0 (+0.06 to +0.09, SE 0.03–0.06). **§22.2's first signal — *random still dominant late, it never left phase 1* — would fire, and taking it would be sound arithmetic on the wrong axis.** The code labels `DIRECTED` **iff `by == "discriminate"`** — a fact about **how the action was selected**. §22.2's *directed* is ***MINT, bets with bound terms*** — a fact about **whether a model is driving**. **Measured on the same runs: the label says 9% directed (22 of 240 steps) while a non-`idn` bound term drives 446 of ~1,200 bet rows, 37%.** Four-fold divergence. **AND `tether.py` REJECTED §22.2's VERSION DELIBERATELY**: *it used to be `DIRECTED if a term is bound`, attached to an action drawn by the identical mechanism either way — **a label the mechanism could not make.*** That reasoning is right for a label about the ACTION and does not carry to a label about the PHASE OF LEARNING. **Two legitimate quantities, one name.** **And the naive reading may be BACKWARDS, as an argument from the mechanism rather than a measurement**: `DIRECTED` requires a slot to OWE, so a library that explains more produces fewer owing slots, fewer discriminating opportunities, and **a RISING probe-label share.** Untested, and it is why the rise is not evidence either way. **MY PRE-REGISTERED PREDICTION WAS ALSO ABOUT THE WRONG QUANTITY.** I pinned the expected shape before the numbers — a shrink at low DS decaying at high DS, derived from the reuse curve — which was the right discipline **applied to a label whose meaning I had not checked.** **Pre-registration does not protect a reading if the instrument measures something else**, and that is the corollary this sweep adds to the one that prompted it |
| **the phase curve + the composition claim** | §22.2 makes *the agent is composing* falsifiable **without a win**, which is the hardest thing on the board to evidence. Not a count — **a phase structure**: random acquires density (the probe, `density(R)` at zero), directed tests hypotheses (MINT with bound terms), strategy executes multi-step plans (routines, unbuilt). **Three readings, all curves:** random still dominant late → *it never left phase 1, nothing is being modelled*; directed growing as random shrinks → *the mint is firing on real structure*; **phase 1 shrinking on level 2 → the library transferred, which is the whole thesis.** §22.3: **the histogram is free — the loop already knows which branch produced each action, and labelling costs one field.** **`phase` and `by` are both recorded already**, with STRATEGY at an honest structural zero until routines exist. **The curve is available and has never been plotted** |
| chunk reuse + `probe_share_trend` | two halves of one transfer reading, and they disagree: the library compounds, the behaviour does not move |
| `_cannot_pay` + §15.3's retrieval keys | the same job by two mechanisms — filter after construction, or retrieve by residual shape. The first is built and is a constant; the second is specified and is a decomposition |
| `ladder(ds=…)` + every transfer reading | **the most expensive instance.** The machinery takes DS as a parameter, `SNAPS_PLAN` §1 says the reading IS a curve across it, and it was never swept. Eleven batches of correct reading produced a wrong conclusion because a dial that already existed was left at 0.4 |
| **THE EXPONENT, TAKEN 2026-08-26 — and it is lowered by the other mechanism** | **measured, 12 worlds** | **THE PANEL PRECONDITION, STATED FIRST**: this reads above 1 only if the panel contains targets whose ATOM-depth exceeds the search depth. It does — **4 of 41 minted terms are deeper than `max_depth = 3`** (atom-depths 4, 4, 5, 6), so they were provably reached by chunking. A panel without such targets would leave the number undefined rather than equal to 1, **and that would be a fact about the panel.** **THE READING: chunk-enabled mints 4 of 41 (9.8%); search-reduction factor median 33.7x, max 365.8x.** `neg . act . neg . neg . act . neg` needs depth 6 in atoms — a space of **299,592** — and was found in an **819**-term unit space. **BUT THE REDUCTION IS FROM CHUNKING, NOT FROM AIMING.** §2's ledger row is *aim the variation with a spec — **the frontier, falsifiable, unrun***; §15's falsifier needs an `F*` spec narrowing to a neighbourhood. **Neither exists.** Chunking reaches the same EFFECT by a different route — **fewer levels, not fewer branches** — so the frontier move remains unrun and the exponent has still been lowered. **n = 4. Small.** **AND THE METRIC DIRECTION IS A TRAP THE COROLLARY CAUGHT**: ratioing compositions searched carried-versus-cold **reads backwards**, because more units means a larger space (`units^d`), so raw search count GROWS with the library. **The reduction shows only as depth saved.** Original row: **THREE sections name this as THE quantity and nothing computes it.** §10 restates the project's own definition into it -- *what is the achievable search-reduction factor, and where is the crossover past which directed search beats the problem's growth* -- and calls it measurable **without a benchmark, without a win, and without anyone's permission, which is the only kind of claim that counts**. §15 independently names it as FMap's falsifier: *if it is large, generation got dramatically cheaper; if it is 1, the map is doing within-span retrieval*. **And the paired design already ran**: carried-vs-cold was executed this session and read for CLAIMS -- identical bound counts, 24 of 30 terms differing, +6 claims of which 5 wrong. **The experiment exists, the quantity is named twice, and the two were never introduced.** `demo` already prints `searched 1463 compositions`, which is the numerator. **And §2's bill ledger names it a third time and had already labelled it**: *aim the variation with a spec -- **lowers the exponent** -- **THE FRONTIER. Falsifiable, unrun.*** Every other move on that ledger pays, relocates, or lowers a coefficient; this is the only one that touches the exponent |
| **`cfg.budget`'s two jobs** | ONE constant bounds two unrelated quantities with opposite behaviour. On CLOSURE YIELDS it never binds -- max 1,884 against 4,000, `budget_exhausted` reported zero times. On the `_round_trip` DOMAIN SWEEP it binds always -- 16,807 needed on a 5-slot `snaps` world, 4,000 available. **The anchor comment written this session describes only the first**: *it bounds the wrong quantity... the declared bound never binds*. True of closure, false of the sweep, and the sweep is where it decides everything. **A basis that covers one of a constant's two consumers reads as a basis** |
| **the `accept` rows + the proposer's training corpus** | §15.6: the proposer displaces exactly three alternatives — **not guessing** (blind), **not lookup** (retrieval reaches only what is indexed), **not gradient descent** (needs a differentiable objective this has not got) — and what it does is *aim the variation with a spec*, **which is §2's exponent move.** For ARC it conditions **not on a verified term but on the CHARACTERISED RESIDUAL**: seed with the gap's signature, sample, type-check free, price with the unchanged bargain. Conditioning is already measured and does not wash out — `ALL`→99.8%, `SOME`→100%, `BECAUSE`→99.8%, even `NOT NOT`→99.8%, **because a generation is one short term against a 32-token window so the seed never scrolls off.** **And the training pairs are already being written: every `accept` entry is a `(residual → term that closed it)` pair**, and `gamma.accept(term, seq=…, residual=…)` records both. **DreamCoder's dream phase with a corpus generated by play rather than by fantasy — sitting in the ledger, unused** |
| **`speak.sentences` + the per-action digest** | §3 specifies a **per-action reasoning digest**: a rendering of the record, **≤16 KB**, that **must cite the ledger sequence numbers so a reader can join the two** -- and says outright that this is `speak.py`'s job. **`speak.py` already does both halves**: `sentences()` returns **`(source sequence numbers, sentence)`**, `account()` renders them as `[seq,seq] sentence`, and **`verify()` already counts orphans -- *a sentence citing nothing is a defect***. **The mechanism and its specified consumer are both present. Only the byte budget and the wire are missing** |
| **the Cyc objection + the prior loader** | Q3 pre-empts a reviewer in one line and **the line was never written**: *a hand-authored library of composable knowledge predicates is **Cyc**. The answer is that Cyc's ontology was graded by its authors and these are graded by **a ground that does not update** -- but say it in the README before a reader thinks it.* **No README says it.** Not yet live, because priors have zero call sites -- **and Phase 3a loads generously, which is exactly when a reader thinks it.** Same pre-emption class as Q27's tiering: cheaper before the run than after |
| **molecules-as-priors + the isolation discipline** | `gamma.py` takes `molecules`, stamps them `PRIOR`, installs them with `residual=molecule:<label>` -- and there are **ZERO call sites**. All six `Gamma(...)` constructions pass atoms only, so the path has never run. `BUILD_PLAN` Stage 1 specifies it in the done-when and **`ARC_BUILD_PLAN` Phase 3a *loads generously* through it**. `PHILOSOPHY` §0.2 names that path as where the unforgivable failure enters -- *supply a prior, you may not thereby pre-answer the question the agent should ask* -- and the guard is not a content check but the SOURCE ISOLATION already practised between `speak.py` and the Gate. **Both halves exist; nothing connects them, and the next build's first phase runs through the join** |
| **`_cannot_pay`'s bit-identical run + clause 1 of the substitution constraint** | §0.2: *variation is produced before selection acts*. `_cannot_pay` is the MDL bargain -- the SELECTOR -- reaching into enumeration, which is the shape of a violation. What clears it is that it is a sound necessary condition: **zero terms lost, bit-identical runs, measured**. That measurement was taken as an efficiency claim and **it is the doctrinal licence**, unconnected to it |
| the A1 REACH check + the effect-index | the check was built first, correctly, **to protect against a design the corpus never asked for** — §15.3's index materialises nothing |

**AND THE INDEX ITSELF WAS THE ELEVENTH INSTANCE, in the way that was least visible.**
`ARC_BUILD_PLAN` from line 397 **is the running batch log of this entire reading** -- every
batch, the figures, `SNAPS_PLAN`, the retraction, the transfer correction. The index is a
CLAIM ABOUT THAT RECORD, and **a claim about a record has to be checked against it.** It
never was. The read-state said `DISCOVERY` Q1 and Q8 were unread when the log records both,
and **Q25 was re-read and deposited as a confirmation into the same document that already
carried it from batch 13.**

> **An index is a frame reporting on a ground. Triangulate it or it drifts** -- Figure 2's
> own condition, missed in the one place it would be least visible, because the index is
> what everything else gets checked against. **The instrument built to prevent re-derivation
> was re-deriving.**

**What this does not undermine:** the findings stand, and several re-reads landed
differently against later findings -- §5 against §4 is the clearest. **What it does mean is
that the reading was shorter than it looked**, and *what this reading added* is a smaller
set than the batch count suggests. **Reconcile index against log before committing.**

**AND A CLASS OF `open` ROW THAT IS NOT A GAP.** Three times the reading found a question the
corpus constrains and does not settle: **slots versus objects**, **extension classes versus
retrieval keys**, and **grammar-versus-gamma pricing for routines** (§15.5 against Q10). Each
was filed as something missing. **They are the same thing, and it is not an absence: the corpus
rules out the wrong answers and leaves the choice, which is what a metatheory does.** A design
space with its bad regions marked is a deliverable, not a hole — **and mistaking one for the
other invites exactly the move the doctrine forbids, which is answering it on the agent's
behalf.**

**How to use this.** Before building a mechanism, search this table as well as the source
column. **Ten instances of *the parts existed for an architecture that could not use them*,
and the last one had both parts made in the same week.**

---

# Waiting on a panel

**TWO open questions cannot be answered on `snaps` as it stands.** It was three; the
transfer question turned out to be answerable with a parameter the machinery already took;
and the second below arrived from `BUILD_PLAN` Stage 1 rather than from the panel's own
list. **`the panel is the binding constraint` was a general claim, and what remains is two
specific structural facts — a prime modulus and a single type — rather than the systemic
version.** Each for a stated structural reason rather than a hunch.

| question | what the panel would need | why `snaps` cannot |
|---|---|---|
| ~~should shadow-only terms cross?~~ | **ANSWERED — `SNAPS_PLAN` §3 rules standing persists.** Not a panel question after all | — |
| ~~does the library transfer?~~ | **ANSWERED — not waiting.** Reuse across DS is 0.72, 0.35, 0.21, 0.20, 0.04, monotone. `SNAPS_PLAN` §7 falsifier 1 does not fire. The level-wise flatness was one point at DS 0.4 | — |
| **does coarsening make rules expressible?** | a value space with non-trivial quotients, or structure that regroups rather than coarsens | `M = 7` is **prime**, so no non-trivial coarsening of Z₇ preserves the arithmetic the atoms are made of |
| **what does a coarse view lose?** — **NOT *NEVER MEASURED*; *FIRST MEASURED IN THE NEXT BUILD*.** The reason it is unmeasured here — a domain sweep needing 16,807 against a 4,000 budget — **does not apply to a fidelity number over a detected grid.** Different disposition: not a dead mechanism, an unexercised one whose first real reading is scheduled. **AND IT IS LOAD-BEARING THERE.** `ARC_AGENT` §5: `logical_grid` commits to a detected board **only if the round trip is near-lossless**, returning `None` otherwise, and **`1 − fidelity` IS `R_T`**. So the mechanism with zero readings here **is the lens's admission criterion there.** Its calibration is the anti-citation in this file: a true 5-px grid scored **0.818** while a spurious 2-px tiling scored **0.946** — **the wrong answer scored higher**, which is why the gate sits at 0.98 and the stride is taken from motion instead of from fidelity | a domain small enough to sweep within the declared budget | **`R_T` HAS NEVER PRODUCED A READING.** `world` returns `None` from `transform()`, so `_round_trip` is not called -- recorded honestly as `channel_closed` with `inert` naming the reason. `snaps` DOES offer views, so it is called, and returns `(0.0, False)` every time: the sweep needs `7^5 = 16,807` and `budget` is `4,000`. The toy world would need `823,543`. **Every reading in existence is the capped case**, which is why the docstring's *not a small R_T, it is NO R_T* is carrying the entire mechanism |
| **does typing beat size?** | atoms spanning more than one type | **every atom is the same type**, so the transfer matrix is 1×1 and `λ = V = 8.0` BY CONSTRUCTION, `types: 1`. `demo.py` reports it and reads it correctly — *typing buys nothing in this world, and that is the instrument working*. But a panel that can only ever return `λ = V` **cannot distinguish a sparse grammar from a dense one**, so the falsifier fires without carrying information about the code. **`ARC_BUILD_PLAN` Phase 3b's done-when is `λ < V` with a real ratio — it cannot be graded here at all**, which is a sequencing fact rather than a defect |

**And the structural guarantee is the same in all three:** whatever sets the panel's
property must not be shown what the agent carries — the way `_views(names)` is never shown
`spec.rules`. **A panel tuned until the mechanism shows has encoded the result.**

**Plus the measured precondition:** state what makes the panel harder / recurring /
quotient-bearing, and **confirm it before using the panel as a premise.** The ladder was
called easing on ten seeds and is flat on forty.

---

# Alignment is a property of the arrangement, not of the system

`[I]` **Alignment is triangulation, and it is what makes disagreement LOCATABLE.** The
system shows its reasoning. The human shows theirs. **Neither is the anchor.** The reasoning
is on the table and the ground settles it -- **Figure 2 stated as a procedure rather than as
a warning.**

**A disagreement has exactly two causes, and they take different repairs:**

| cause | what it is | the repair |
|---|---|---|
| **the human or frame has more context** | information the system's library does not contain | **an import.** Name what is missing and supply it |
| **something else is weighting the decision** | risk, reward, the cost of being wrong. **Not a disagreement about the world at all** -- a difference in what is at stake, and **the system was never going to derive it** | state the weighting at the point it matters |

**And both are visible only if the reasoning is legible.** A black box that disagrees with
you gives you neither: **you cannot tell whether it lacks context or is weighting
differently**, so the only available responses are to override it or to defer to it.
**Neither is alignment.**

### Which makes §0.1's Q3 the mechanism rather than a proxy for it

*The agent's report of its own epistemic state is sound, and checkable from outside* is not
a nearby virtue that stands in for alignment. **It is what makes the triangulation possible
at all** -- and a system that cannot state why it concluded something **cannot be aligned
with in this sense, because there is nothing to disagree with.** The six-row checklist above
is therefore the deliverable in the strict sense, not an instrument pointed at it.

### And it dissolves the value-encoding problem rather than solving it

**Values do not have to be encoded.** They enter as **the weighting a human brings to a
specific disagreement, stated at the point it matters.**

**Which is better than encoding them, on two counts.** It does not require anyone to have
settled what the values ARE -- an open problem that encoding presupposes is closed. And it
**works for a person whose weighting differs from the majority's**, where an encoded value
set silently substitutes the majority's. The corpus already supplies the ruling that makes
this more than a preference: **agreement is efficient for a convention and disqualifying for
a verdict**, so a majority preference is a convention and never a ground.

### Two consequences, and the first corrects a row above

**1 · Q27's tiering does NOT say what I wrote into the ARC plan.** I recorded *the alignment
claim needs a poorer-ground domain, and nothing on the board supplies one.* **On this reading
alignment does not need a poor ground. It needs a ground THE AGENT CANNOT SEE** -- a
different requirement, and a weaker one.

**And `demo.py` already implements it.** `unreachable in fact: ['opaque'] -- the harness
knows; the agent is not told`, then **1/1 correct abstentions and 0/6 false**, scored over
**the agent's REPORT rather than over its answers**. Top-tier ground, withheld, report-scored.

**So the missing domain is a top-tier ground withheld and scored on the report** -- buildable,
and **much smaller than a test of values.**

**AND §9 SAID IT FIRST, from the other direction.** `ARC_AGENT` §9, on what *done* means
for stages A–F: **the agent abstains correctly when the atom it needs is not in the closure
-- *which on ARC is not planted but real, and therefore no longer measurable against a known
answer*. THAT IS A LOSS OF MEASUREMENT WE SHOULD FEEL.** The toy world could score
abstention **because the harness knew the truth**; ARC cannot. **So the abstention number
lives on the withheld-ground panel and ARC does not carry it** -- and §9's instruction
follows directly: **keeping a planted-unreachable toy slot in the local suite is how the
false-abstention number stays alive.** Do not retire `snaps` when ARC starts. **Eighth
instance of the corpus being ahead, AND IT IS A DIFFERENT KIND.** The other seven are *the
corpus said where the build would stop* — a destination predicted. **This one is *the corpus
said what would be LOST by changing domains, and what to do about it*, before anyone had
framed the move as a loss at all.** And the instruction is the actionable half: **the
natural move once ARC runs is to stop maintaining the toy panel, and §9 says the opposite
for a stated reason** — the false-abstention number is the deliverable's own evidence and
`snaps` is the only place it exists.

**2 · The ARC caution is unchanged.** ARC is middle-tier and tests machinery. **A strong
score is not evidence for this claim**, and that belongs in the ARC documents before the run
rather than in a write-up after it.

---

# Arrival has never occurred, and that is the scope statement

**The largest single fact the reading produced, and it is not a defect.**

`PHILOSOPHY` §0.1 Q1 splits the loop: **steps 2-4 are ARRIVAL** -- route the failure, offer
a term, accept it -- **step 5 is SELECTION**, the ground settling it. Selection has
centuries of company; *arrival is the part that was empty*. §4 then says what fills it:

> **Minting is not creation. It is re-reading. A new primitive is existing material you
> start reading as a primitive.** Pressure is a residual the current partition cannot
> explain; the operation draws a boundary in existing material; **the product is an atom
> that was always there, unread.**

**Measured: 20 composites minted across six worlds and 360 cycles, 6 settled, and
`gamma.primitives` is EMPTY after every run. Zero atoms, ever.**

**AND THE CORPUS SAID IT FIRST, which corrects my own framing of this as the reading's
largest discovery.** `PHILOSOPHY` §9, on its own weaknesses: *a theory whose strongest
results all land in the region every field has conquered is a theory of the easy half.
Region ① is crowded;* **region ③ still holds zero minted primitives from this project.**
Already written, about itself. **What the reading added is the number, the panel-wide
scope, and the located cause** -- `promote` is the only path to an atom, echo needs a term
minted for one slot to close a residual on another, and four independent slots make that
nearly accidental. **The fact was the corpus's. The mechanism is the contribution.**

| | |
|---|---|
| what runs | **composition within the closure** -- and Figure 8 says composing inside a closed set never adds an atom, *definitionally* |
| what has never run | `promote`, the ONLY path by which a composite becomes an atom. **0 across 360 cycles** |
| so what has never happened | **arrival, as §4 defines it** |

**This reframes the `promote: 0` row rather than repeating it.** That row read as a panel
property -- *four independent slots make echo nearly accidental*, already written down. True,
and it is the CAUSE. **The consequence is that the mechanism §0.1 calls the empty part has
never demonstrated**, and the panel is why.

**AND §5 ALREADY HAD A NAME FOR IT.** Shadow decides whether to mint; **echo decides
whether it was a primitive or a patch**. The verdict table:

| verdict | |
|---|---|
| echo without shadow | apophenia -- a structure found elsewhere and given somewhere to live |
| **shadow without echo** | **a working local hack. Legitimate, earns its keep, DOES NOT CROSS** |
| shadow, then echo | a primitive |

**20 mints is shadow firing 20 times. 0 promotions is echo never firing.** So every term in
the library is the middle row, by the corpus's own naming -- and the middle row is
legitimate. **It is not a failure verdict. It is the one that does not transfer.**

**Which is what the DS curve measured without knowing the name for it.** Reuse across
deviation is 0.72 / 0.35 / 0.21 / 0.20 / 0.04, collapsing as DS rises. **`does not cross` is
what that curve looks like from the outside.** Two readings of the same library, one a
counter inside the loop and one a cross-world measurement -- **not independent frames, so
not triangulation, but the number now has a verdict attached and the verdict was already
written.**

**And the corpus diagnoses this exact state, in §4's own closing paragraph:** the one built
instance of re-partitioning *knows what a rotation is*, so it detects instances of a known
form, **which is schema completion, which is closed**. *The chisel exists and is pointed at
the board. This needs it pointed at the grammar -- re-partitioning the form-space rather
than within it.* **The code is re-partitioning WITHIN the form-space.** That is where it is,
it is said here rather than discovered by a reviewer, and it is Figure 11 again: a synthetic
solve proves wiring and never capability.

---

# The deliverable — and it is the precondition, not a proxy for it

**FILED TOO LOW ONCE ALREADY.** This was recorded as *the corpus's definition of the
deliverable*, six-for-six, and read as a strong confirmation OF AN INSTRUMENT. It is not an
instrument. **A sound, checkable report of the agent's own epistemic state is what makes
triangulation possible at all** -- see the alignment section above -- so **a system that
cannot state why it concluded something cannot be aligned with, because there is nothing to
disagree with.** Six-for-six against a live ledger is therefore a confirmation of **the
precondition for the deliverable existing**, which is a larger result than a checklist
passing. **A row is read at the weight it is filed at.**

**`PHILOSOPHY` §0.1 Q3 is not framing, it is a checklist** -- six things *the agent can
always say*, each named with its mechanism, and the stated deliverable is **not that the
agent knows the truth but that its report of its own epistemic state is sound and checkable
from outside.** Checked item by item against a live ledger rather than recalled. **Six for
six.**

| the agent can always say | mechanism | measured |
|---|---|---|
| which slot owes, and how much | `R` per slot, never pooled | 128 rows carry per-slot `mass`; **no pooled field exists** |
| why that failure is that kind | ROUTE's four bins, why-not-the-neighbour | 128 rows, **7 distinct** why-not reasons |
| settled versus merely held | candidate vs accepted, citability | cite 32 / hold 13, **both branches live** |
| where every term came from | origin stamps, provenance | present -- **and only ever `minted`**, because priors never load and imports are unbuilt |
| that it searched and did not find | unreached at budget, WITH the budget | `park` + verdict; **21 rows carry `coverage`, `units`, `depth`**, and `gate._unreached` examines all 21. **Not vacuous** |
| that it has been wrong, always | monotone integral, no `suppress()` | `+=` only; **no `suppress` token in the source** |

**And §0's thesis behaves as written.** The abstention states `searched 1463 compositions to
depth 3` -- **the work actually done, not the 4,000 cap** -- plus bits unexplained, plus the
caveat in the corpus's own words: *unreached at this budget. NOT unreachable.* 1/1 correct,
0/6 false, **both numbers**, because either alone is marketing.

**One reader's error worth keeping**, since it is the fourth this session: I searched the
ledger for an `abstain` event, found none, and had written down that the product clause was
the one item of six with no record. **The event is `park`, carrying a verdict.** A search
for the wrong name returns the same empty set as an absent mechanism, and only the second is
a finding.

---

# PHASE 3 CHECKED BEFORE ORDERING — and it is NOT the same shape as the owed greens

**Fifth item the check has been applied to, and it found two things.**

### 1 · `λ < V` IS gradeable by Phase 3 itself — my row read as though it were blocked

The index said Phase 3b's done-when *cannot be graded here at all*, which is true of `snaps`
and reads as though Phase 3 were stalled like the two owed greens. **It is not, and §11.3 says
why:**

> *The Stage 1 falsifier fired in the toy world: **`λ = V = 7`, because every atom was
> `val → val` and the type graph was a single node.** With three spaces the graph is genuinely
> sparse — `grid → ATTR`, `ATTR × ATTR → PRED`, `PRED → OBJ`, `slot × action → slot` — and
> most primitives do not compose with most others. **`λ < V` for real, and the number starts
> reporting something. The instrument was working in the toy world; it just had nothing to
> measure.***

**The types come from `3b`'s OWN DESIGN, not from the domain.** So Phase 3's done-when is
supplied by Phase 3 — **a real difference from contact ranking and `never_live`, which need a
board nobody can author.** One waits on a file; the other waits on itself.

**And the closing line is the corpus ahead again**: *the instrument was working; it just had
nothing to measure* is the panel-cannot-exercise pattern, **written about `λ` before `λ` was
measured.**

### 2 · SEVEN OF THE NINE MINIMUM SENSORS ARE ALREADY BUILT

`3a`'s first clause is *the nine minimum sensors, typed, total with `NOT_RESOLVED`, priced*.
**Seven landed under Phase 2's item numbers**, at `2b` and `2c`:

    1 components  BUILT     2 colour   BUILT     3 position  BUILT
    4 extent      BUILT     5 shape    BUILT     6 overlap   BUILT
    8 touching    BUILT     7 delta    NOT       9 changed   NOT

**Nobody would have known**, because the work is filed under the items that needed it rather
than under the item that lists it — **the same shape as §19's two halves, fixed months apart
under different numbers and connected only by §19's own title.**

**What `3a` still owes** is `delta` and `changed`, the typing and totality with
`NOT_RESOLVED`, the pricing — **and its real blocker is unchanged**: *load generously across
the six loadable shapes, all stamped `prior`*, which runs through the **molecules path that
has zero call sites**, with **the Cyc pre-emption still unwritten.**

---

# PHASE 3's PRECONDITION — two blocker validations wait on a file nobody has

**Not two open rows. One dependency, and it is the one thing on the board nobody can build.**

| owed | what it needs |
|---|---|
| **contact ranking** | a board where **the mint actually fires** AND slots **differ in variance**. The fixture has the second and not the first |
| **`never_live`** | a board with **walls** — somewhere the agent can be genuinely stuck |

**AND NEITHER CAN BE SUPPLIED BY A FIXTURE I AUTHOR.** *A fixture with a payable rule I
designed would be testing my rule, not the ranking* — which is the structural guarantee
applied one level out: **whatever supplies the rule must not be shown what the mechanism
needs**, the way `snaps._views` is never handed `spec.rules` and states that as its whole
guarantee. **And the discriminator is not *do not author both sides*** — `Grows` and the lens fixture
each had one author and both were fine.

> **A FIXTURE IS SAFE EXACTLY WHEN THERE IS NOTHING IN IT THE RESULT COULD BE SMUGGLED
> FROM.** Plumbing has no answer to leak: whether the eight members fill, whether a row
> reaches the gate, whether a slot survives a frame — **the author cannot tilt those by
> knowing them.** A payable rule is different in kind, because the ranking's result is a
> fact ABOUT that rule, and whoever wrote the rule has already chosen the answer.
> **Same author, opposite verdicts, and the test is what the fixture CONTAINS rather
> than who wrote it.**

> **Real environment files supply both without anyone choosing them**, which is the point:
> the rule is payable or it is not, and the walls are there or they are not, and **nobody
> decided either.** So both owed validations sit on the same dependency as `2a`'s watermark —
> **the first real environment file** — and that is a thing to obtain rather than to build.

**Two of three blocker validations therefore wait on a file nobody has**, and that is worth
knowing as a precondition rather than discovered as two stalled rows in Phase 3.

---

# CORRECTION — TWO of the three greens still owe their demonstration, not one

**I said contact ranking would get its first real test at sensor 4, and then restated that as
though it had.** It did not, and the claim was wrong twice over:

- **sensor 4 does not touch `_bindings`.** The affordance profile reads objects under contact;
  contact RANKING orders operand bindings inside the mint. Different mechanisms, and the
  connection was an argument about variance rather than a code path.
- **and the ARC fixture never reaches the mint at all.** Measured: 12 cycles, 333 rows —
  `utterance 36 · bet 134 · route 122 · park 18 · rebind 3 · probe 4` and **zero `mint`
  events.** The search runs and parks; nothing pays, because a trivial rule over three atoms
  offers nothing to buy. **No mint means no `_bindings` means no ranking.**

| green | state |
|---|---|
| **blocker 2 · slot re-read** | **DEMONSTRATED.** Perception produced a genuinely changing slot set and `_present` caught it three times, on real behaviour rather than a wrapper built to fire it |
| **blocker 3 · contact ranking** | **STILL OWED.** Needs a board where the mint actually fires AND slots differ in variance. The fixture supplies the second and not the first |
| **blocker 1 · `never_live`** | **STILL OWED.** Needs a board where the agent is genuinely stuck; nothing has produced one |

> **A prediction restated as an outcome, and it survived two exchanges before being
> checked.** The tell was available the whole time — the fixture's event counts were printed
> on every run and `mint` was never among them. **Nothing failed; a green was simply
> credited to the wrong cause.**

---

# PHASE 2 CLOSES — the sweep trigger, a third site for §19, and one check deferred

### The cap is a PSEUDO-DEATH, and that found §19's bug a third time

`[I]` **the max-actions cap is a pseudo-death, and it is imposed from outside the game.**
`2d` already handled it for the termination class. **`Chain.close` did not**: anything not
`advance` counted as a **STALL AT THE CURRENT STAGE**, so a capped run was attributed to a
reasoning stage as though the loop had failed to progress there.

> **It had not. It ran out of room the seat granted.** A cap is neither an advance nor a
> stall, and it now counts apart. **Third site for §19** — the mint's `UNREACHED`, the
> episode's ending, and now the CHAIN: *never let a filter hand you a verdict*, and a budget
> is a filter. **The first two report an exhaustion as a verdict about the WORLD; this one
> reported it as a verdict about the AGENT'S REASONING.** Verified: 2 advances, 2 capped, 1
> stall — a cap in neither bucket.

### The sweep trigger — credit only, and the row says where the other half is

§21.3: ***a level completes at step 500 and the last action did not cause it — the trajectory
did***, so crediting the final action is the delayed-effects bug at the scale of a whole
segment. **A completion now emits a `credit` row over the SEGMENT** — what settled during it,
what was bound while it ran, over how many steps, on a recorded history costing no actions.
Verified: three completions, the first crediting three terms settled in-segment.

**CREDIT ONLY.** §21.4: *crediting without the decay is the incumbency pathology; decaying
without the credit throws away the only positive evidence there is.* **The decay is boundary
demotion, which is its own item and turns on §21.5's event type** — so the row carries
`decay_half` naming where the missing half lives, **rather than leaving a both-and looking
finished.**

### And the `disproof` gate check is DEFERRED — I argued the instruction down

**§21.2's discriminator separates a CHOSEN death from an inflicted one. The agent cannot
choose to die**: there is no mechanism, and `arc_world` withholds RESET so it cannot
self-restart. **Every death is world-inflicted, so the check would examine ZERO rows, pass,
and read identically to a check that examined many.** Same as `reset_kind`, removed for being
ahead of its consumer, and the shadow-test check, deferred to ship with arrival. **It ships
when deliberate death does, which is where its subject comes from.** The FIELD stays and is
right to — it fires 74 times recording what a discriminating draw buys, which is a different
thing and waits on nothing.

**AND THE GATE CANNOT REPORT VACUITY, WHERE `lint` CAN.** *"The gate passed"* is currently
indistinguishable from *"the gate looked at nothing"* without measuring from outside — which
is what answering this question required. **Measured 2026-08-27: all nine examine something.**
Smallest subjects are `_guards` and `_settlement` at **4 rows** each; `_unreached` 21,
`_cuts` 25, `_filters` 28, `_routing` 128, and three over all 421. **A fact that can quietly
stop being true, and the next check added to the gate is exactly when it would.**

**No regression:** 1/1 correct, 0/6 false, 1,463 compositions, mint 20 / settle 6.

---

# `2e`'s event types — BUILT 2026-08-27, recorded and deliberately not consumed

**Five endings in `ledger.py`, each with its reading**, and `retarget` carries the kind rather
than defaulting it:

    win      the objective was met
    death    the world ended the episode -- evidence about the world
    reset    the next board is KNOWN, so a spike means THE MODEL IS WRONG
    advance  the next board is UNKNOWN by design, so a spike means NOTHING YET
    cap      the seat's budget ran out. NOT a verdict about the world

**§21.5's pair is the point: `reset` and `advance` produce the SAME residual spike and mean
OPPOSITE things**, and the reading is on the row so a later reader does not have to infer it.
Verified firing on a real ladder — three `ending` rows, each carrying `how`, `to_level` and
its reading.

**AND THE LADDER NOW CARRIES THE PREVIOUS LEVEL'S ENDING** rather than defaulting to
`advance`. **A kind that is always `advance` is a field that says nothing** — the same defect
as `allowed: true` on 32 rows, which the nulls sweep flagged and which turned out to be its
own false positive. Here it would have been real.

### RECORDED, NOT CONSUMED — and that is the decision

**What reads this is boundary demotion, which is its own board item.** The revert was
withdrawn because **settled-ness was the wrong gate**, and §21.5 proposes a different one —
the event type. **Building the consumer inside `2e` would be the same mistake in the other
direction**: a mechanism arriving with its trigger, before the item that owns the decision.
The row says so in `consumed_by`.

### Still open in `2e`, both already-known rows

| | |
|---|---|
| **a gate check over `disproof`** | §21.6: *deliberate death is legitimate when `expect` and `disproof` are stated first — **a gate check, not a judgement call***. The field exists; no check reads it |
| **the level-completion sweep trigger** | §21.6: *a completion is a per-level settle, **credited by the sweep over the segment***. `retro` rows exist; nothing fires them on a completion |

**No regression:** 1/1 correct, 0/6 false, 1,463 compositions.

---

# `2e` checked — it is the EPISODE HALF of a bug fixed halfway at Phase 0d

**Fifth item the check has been applied to, fifth thing it found — and this one reframes the
item rather than adding to it.**

**§19: *"I ran out" is not "I was wrong" — THE SAME BUG IN TWO PLACES.***

| where | the conflation | state |
|---|---|---|
| **the mint** | `UNREACHED` means both *the search budget ran out* and *no such term exists at this depth* | **FIXED at Phase 0d** — `no_support` / `not_novel` / `budget_spent` / `depth_exhausted`, each with coverage |
| **the episode** | a run ending means both ***I hit the action cap*** and ***the world killed me*** | **`2e`'s CAP event. Unfixed** |

> ***In both cases a resource exhaustion is being reported as a verdict about the world*** —
> Figure 9's rule violated in the loop's own reporting: **never let a filter hand you a
> verdict.**

**So `2e` is not five event types plus two open rows. It is the second half of one bug**, and
the first half was fixed months earlier under a different item number. **Nobody connected
them**, and §19 connects them in its own title.

**And it is the same distinction `2d` was built on an hour ago** — a cap firing is not a
verdict about the game, which is why a capped ending leaves the termination class `open`.
**The mint half, the termination half, and the event-type half are one rule at three sites.**

### `2e`'s full scope, now known

| | |
|---|---|
| **the five event types** | WIN / DEATH / LEVEL-RESET / LEVEL-ADVANCE / CAP, distinguished — **§21.5's rule inverts the meaning of a residual spike between the middle two** |
| **a gate check over `disproof`** | §21.6: *deliberate death is legitimate when `expect` and `disproof` are stated first — **a gate check, not a judgement call*** |
| **the level-completion sweep trigger** | §21.6: *a completion is a per-level settle, **credited by the sweep over the segment**, not by the last action* |

**Two of those three are already open rows that close as a side effect**, and the third is
§19's episode half. **Nothing here is new work discovered late — it is three known things
that turn out to be one item.**

---

# `2d` — BUILT 2026-08-27. The class latches, and the accrual is provably not flat

**`Termination` in `instruments.py`, `Budget` in `arc_run.py`.** Four states, verified to
discriminate:

    no endings yet  -> open, "never proven, only defaulted to"
    after a CAP     -> STILL open, capped_seen=True
    after a death   -> death_possible, PROVEN
    +3 clean ends   -> STILL death_possible  (it LATCHES)

**A CAP FIRING DOES NOT PROVE `bounded`**, and that is the slip worth naming: the run ended
because WE stopped it, not because the game did. §20.1 is exact — *without a death **and
without your cap firing*** — so a capped ending leaves the class `open` and records
`capped_seen` separately. **Treating a cap as an ending is the two-state version arriving by
the side door** — **and it is the first of today's five where the collapse would have been HIDDEN rather than obvious.** The other four are visibly two-state when they go wrong: a field reads `False` instead of `None`, a claim says `unreachable` instead of `unreached`. **Here all three states exist in the code and one is simply never entered** — `open` becomes unreachable the moment a cap counts as an ending, because every run ends one way or the other. **A three-state discipline with an unreachable third state reads as compliant**, which is the vacuity problem arriving in a state machine.

**AND `OPEN` IS REPORTED AS AN ASSUMPTION**, never as a finding. `report()` splits `proven`
from `assumed`, so *this game has no death* is not sayable — **fourth site today for the same
three-state rule**, after `None`-means-unread, `unreached` against `unreachable`, and
`channel_closed` against a zero.

### The accrual, proven distinguishable rather than assumed built

**The flat version passes a short fixture perfectly**, so the fixture runs TWO levels and
leaves budget on the first:

    2 levels x 6 accrued, 8 spent  ->  4 LEFT
    the flat cap would leave       ->  2

**Different numbers, so the fixture says which implementation ran.** The accrual is one line
that can be pointed at — **`left += per_level`, never `left = per_level`** — and it is written
that way because it is the part that gets lost.

### And the second firewall decided the shape

**The agent does not read the cap.** `arc_run.py` is seat-side and the loop never imports it;
**`capped` reaches the sensor as an EVENT.** A cap value inside the agent's reasoning is the
second firewall's whole subject — *the agent discovers its budget by running out, or is told
by the frame, never by a number someone read from a config.* **One module rather than a copy
per runner**, because the fixture uses it now and the bridge will at Phase 5, and two
accruing budgets would drift on exactly the clause that is easiest to lose.

**`bounded` IS ABOUT THE PAIR**, and the row says so: under accrual the cap firing is partly a
fact about the agent's efficiency, so the same board is `bounded` for a careful agent and
`capped` for a wasteful one.

---

# THE CAP — RULED 2026-08-27. Four parts, and one of them is the one that gets lost

> ### 500 actions PER LEVEL, ACCRUING. Unspent budget carries forward.

**FOUR PARTS, RECORDED TOGETHER BECAUSE THREE SURVIVE A CARELESS READ AND ONE DOES NOT:**

| | |
|---|---|
| **the number** | 500 |
| **the unit** | per LEVEL, not per run |
| **the accrual** | **unspent budget CARRIES FORWARD, so an efficient agent has more room later** |
| **the basis** | `[I]` *measured from agents I have trained. **Just enough room to make mistakes*** — an observation about how learners actually behave, not a guess and not a preference |

**`500 per level` without the accrual reads as a flat cap, and someone will implement the flat
version.** The accrual is the part that gets lost first, which is why it is a named part
rather than a clause.

**AND THE BASIS IS EXTERNAL IN §22.1's SENSE**, which is what makes it an anchor rather than a
number tuned toward a behaviour by the frame that benefits from it: **it is not a quantity
this agent produces and it cannot be moved by performing differently within a run.** The
harness's **80** is a comment about infinite loops; §22.1's **1000** is 2× a human's move
count; **this is measured on LEARNERS, which is closer to the thing being bounded.**

### What it does to `2d`, and it must be said on the row

§20.1 defines `bounded` as *the run ends without a death and without your cap firing.* **Under
an accruing budget, the cap firing is partly a fact about the AGENT's efficiency rather than
only about the game** — so **the same board is `bounded` for a careful agent and `capped` for
a wasteful one.**

> **That is correct, and it means the classification is about THE PAIR and not about the game
> alone.** It goes on the row rather than being left for a later reader to infer, because
> *termination class* reads as a property of the world and under accrual it is not.

### And the fixture — stated rather than assumed

**The fixture does NOT share this number.** A fixture running a handful of steps does not need
500, and a convenient value there is **how the accrual quietly does not get built: the FLAT
version passes a short fixture perfectly.** So the fixture gets its own value with its own
recorded reason, under the same label `SIDE` and `PALETTE` already carry — *a fixture
dimension, nothing read off it.*

> **AND THE ACCRUAL HAS TO BE EXERCISED SOMEWHERE OR IT IS UNTESTED.** A single-level fixture
> cannot show carry-forward, so `2d`'s fixture must run **more than one level** with budget
> left over on the first. **Otherwise the flat implementation and the accruing one are
> indistinguishable**, which is the vacuity problem arriving in a cap.

---

# `2d` and `2e` checked against their own sections — and both need a number nobody set

**The check is now a step rather than a caution, and it found the same dependency in both.**

**§20.1 makes the cap DEFINITIONAL for `2d`.** Its four reads are asymmetric on purpose:

| read | from | direction |
|---|---|---|
| a win is possible | `win_levels > 0` | given up front |
| **death is possible** | `state == GAME_OVER`, once | **proven on the first death, NEVER disproven** |
| **bounded** | the run ends without a death **and without your cap firing** | proven by observation |
| **open** | none of the above, so far | **never proven — only defaulted to** |

> ***Not having died is not evidence that you cannot die.*** So `DEATH_POSSIBLE` **latches**
> true and never latches back, and **`OPEN` is a standing ASSUMPTION rather than a finding,
> and must be reported as one.** The easy two-state version reports *this game has no death*,
> which is the absential reading the corpus rules out: *absence of evidence resting on
> completeness never holds mid-episode.* Same discipline as the affordance profile's `None`
> and as `unreached` against `unreachable` — **three states, and the third is a claim about
> what has not been observed.**

**And `2e`'s five event types are WIN / DEATH / LEVEL-RESET / LEVEL-ADVANCE / CAP** — the cap
again, this time as an event that must be told from the other four.

> ### BOTH DEPEND ON `MAX_ACTIONS`, WHICH IS A SEAT PARAMETER AND IS STILL UNSET.
> The harness base class defaults to **80**; §22.1 defends **1000** on the 2× human ceiling,
> **a legitimate external basis for a number 12.5× the default.** `2d` cannot read `bounded`
> without it and `2e` cannot name `CAP` without it. **Inheriting 80 silently is the failure;
> overriding without recording why is the same failure wearing a decision's clothes** — and
> it is now blocking rather than tidy.

**`2e`'s hard part remains answered**: §21.5 gives reset-versus-advance, and the frame carries
`full_reset` and `levels_completed`, so the discriminator is recoverable even where
COMPETITION collapses the two.

---

# THE BUILD TABLES GROUP BY COST, NOT BY DEPENDENCY — twice now

**§16.8 lists four sensors with a `cost` column: trivial, 49 cells, one correlation, one row
per kind.** Nothing in it says **4 depends on 3 and on 8**, and 8 is not even in the table —
it is one of §12.3's nine. **Building in listed order would have produced sensor 4 against an
avatar that had not been read yet**, and the `blocks`/`passes` readings would have been
guessed rather than left unread.

**Same shape as the `2c` split**, which grouped a lens and four sensors under one item and hid
that half of them needed `2b`. **A table that orders by cost tells you what is cheap; the
dependency order falls out of neither the table nor the cost.**

> **So read the SPEC of each item before ordering a phase, not the row that summarises it.**
> Both misorderings were caught by reading §16.8 and §16.4 rather than by anything failing —
> **nothing would have failed. The work would just have been done against something that was
> not there yet.**

**`2d` and `2e` are the remaining rows in the same table.** Their dependencies have not been
checked against their own sections.

---

# Sensors 3 and 4 — BUILT 2026-08-27, and 4 needed a sensor from the other list

**§16.8's four are now four**, and building 4 surfaced a dependency the build table does not
show: **§16.4 defines an affordance as behaviour UNDER CONTACT, so sensor 4 needs
`touching(a, b)` — which is §12.3 sensor 8, not one of the four.** And *blocks: movement into
it fails* presupposes an avatar, which is sensor 3's read. **So the four cheap sensors are not
independent: 4 depends on 3 and on 8.**

### Sensor 3 · control mode, a per-step read and never a label

§16.2 is strict: *it BLENDS mid-game, so it must be detected contingently per step, never used
to label the game.* Built as `Agency`, re-read every step:

    one contingent slot   -> avatar        several -> coupled
    none, but change      -> actuator      none, no change -> unread

**A PREDICATE, NOT A THRESHOLD.** A slot is action-contingent when SOME action has always
moved it and SOME OTHER has never — an existence claim over what was observed, **no rate, no
cutoff, no window to tune.** Verified to discriminate all three: `avatar ['a']`,
`coupled ['a','b']`, `actuator []`. On the fixture it reads **actuator**, correctly — the
board changes on a clock rather than by action, so nothing is action-contingent.

### Sensor 4 · affordances, not substances

§16.4: **do not classify the substance** — a blob-kind taxonomy learned on the public set is
*the archetype trap wearing a perception costume*. ***"Wall" is not a category, it is a
profile — and the profile is what transfers.*** Seven booleans per kind, and **`None` means
UNREAD rather than false**, kept distinct for the same reason `unreached` is kept from
`unreachable`. The fixture reads **7/7 unread**: its objects touch and nothing happens.

**KIND IS COLOUR AND SHAPE**, on the asymmetry that decided 4-connectivity: **too coarse
conflates two behaviours into one contradictory row and nothing says so; too fine splits a
kind that would have transferred, which is recoverable.**

### Two defects, both found by running it

**1 · A false `consumed`.** The background region scored *consumed* because something moved
THROUGH it: matching survivors BY KIND fails when a kind carries shape, so any RESHAPE looks
like death. **`Objects` already owns identity by overlap and then by shape** — the fix is to
READ it rather than re-derive it, and re-deriving was a second and worse answer to a question
already answered.

**2 · A false `moves_when_touched`.** Cell-set inequality conflates §16.4's *displaces* with
its *transforms*. **Shape and position already separate them** — same shape and different
place is a displacement; different shape is a transformation. No new sensor needed, and the
background now reads `changes_on_touch`, which is what happened to it.

---

# `2b` — BUILT 2026-08-27, and blocker 2's detector fired for real

`arc_percept.py`. **Segmented objects as slots, tracked by overlap, dying only on evidence.**
An object contributes five int slots — `row`, `col`, `h`, `w`, `colour` — because `POSITION`
and `EXTENT` are two-dimensional and the loop takes one int per slot, **and separate axes are
the only encoding in which a `translate` atom acts on a slot sensibly.**

    perception        10 object slots, 2 tracked objects
    slot-set changes  3 `present` rows -- came=['o1.col', 'o1.colour', 'o1.h']
    gate              pass, 333 rows

> **BLOCKER 2'S DETECTOR FIRED FOR REAL.** Not on a wrapper built to make it fire —
> **perception genuinely produced a changing slot set** and `_present()` caught it three
> times. **One of the three undemonstrable greens is now a measurement.**

### Two choices the corpus does not settle, made and stated

**4-CONNECTIVITY, not 8.** *Connected same-symbol components* does not say which. Four splits
diagonal touches into separate objects, so the agent sees MORE slots — and **over-segmentation
is recoverable** (the agent can learn two slots move together) while **under-segmentation is
the loud/silent failure**, one slot hiding a rule operating below it.

**NO BACKGROUND COLOUR.** Every same-symbol region is a component, including colour 0.
**Treating 0 as background is domain knowledge about what a board means**, and perception is
not entitled to it. It costs slots and refuses an assumption.

### Three defects, found by running it

**1 · Overlap alone cannot track a move, and the ATOM SET proves it is a defect rather than a
limit.** A 1×2 object moving one row has ZERO cell overlap with itself, so a translation read
as a death and a birth. **`translate` is in the specified atom set, and a translate atom is
unobservable if translation destroys identity.** §12.3 sensor 5 is the answer and I had
skipped it as not-needed-for-slots-to-exist: **`shape(obj)` at NORMALIZED OFFSETS is
position-independent**, so it carries identity across a move. After: `{'o1.row': (1, 2)}` — a
translation as a single-slot delta, which is what an atom can act on.

**2 · The eight-member contract assumes PURITY and perception cannot be pure.** `slots()` and
`observe()` each called the decomposition, and tracking is stateful — **so two calls per step
advanced the tracker twice and the two disagreed**, surfacing as a `KeyError` on a slot that
existed in one call and not the other. **The decomposition is a function OF THE FRAME**, so it
is computed once per frame and cached, and the cache clears on `step`.

**3 · The slot set can move WITHIN a step, and `_present` only catches boundaries.** An object
can die between the bet and the reading, so `self.slots` is stale by the time `after` is read.
**A slot that vanished under the bet is UNEXPLAINED, not absent** — it is charged a full code
and the row carries `vanished`. Same rule as `_applies` and the round-trip fallback: **missing
is charged, never skipped.** Third instance today of that exact direction.

**No regression:** 1/1 correct, 0/6 false, 1,463 compositions, mint 20 / settle 6.

---

# `2b`'s three decisions — ALL SETTLED BY THE CORPUS, checked before writing

**Three choices live inside *connected components as slots, tracking by overlap, death only on
evidence*, and the third is the one that gets made by whoever writes it.** Asked before, not
after — and **all three turn out already answered.**

| decision | answer | where |
|---|---|---|
| **what counts as a component** | **connected SAME-SYMBOL components** — near-decomposable clusters after Simon, *the boundary is where cohesion drops*. Adjacency AND colour identity, not either | `DISCOVERY` Q6 · `ARC_AGENT` §5 |
| **same object across frames** | **permanence by IoU overlap**, so identity survives recolour and reshape | `ARC_AGENT` §5 · Q6 |
| **when the object is not found** | **it persists.** *Segmentation is a revisable belief*; an object **persists through non-observation (occlusion) and DIES ONLY ON EVIDENCE — when its cells are taken over by other live objects.*** Not-found is NOT dead | `DISCOVERY` Q6, SETTLED |

**AND THE THIRD IS THE EROSION, ANSWERED AGAINST THE EASY OPTION.** The cheap move is to drop
a slot when its object is not found — **which is a silent slot-set change, blocker 2's defect
arriving from the other direction.** The corpus refuses it, and blocker 2 now makes it loud
anyway: dropping a slot trips `_present()` and emits a row. **The rule and the detector agree,
and neither knew about the other.**

**AND THE ONE THAT LOOKED OPEN DISSOLVES.** The IoU THRESHOLD has no recorded basis, which is
the ANCHOR problem — **and there is no threshold.** The sensor table types it
**`overlap(a, b) : OBJ × OBJ → RATIO`**, a measured ratio rather than a boolean, so tracking
matches each object to the previous one with **maximum overlap** and nothing needs a cutoff.
**The predicate-not-threshold discipline that REPAIRS 1 enforced when it deleted `EPS` and
`WARM`, holding one layer out — and I was one step from inventing a number the type signature
already rules out.**

---

# `2c`'s sensors — TWO BUILT, TWO BLOCKED ON `2b`, and that splits the item

**§16.8's four, read rather than taken from the build table's one-line summary:**

| | sensor | state |
|---|---|---|
| **1** | **action-set delta** — *the previous action changed the gating* | **BUILT, and it was half-built already.** `_advertised` detected the delta at blocker 1, but §16.8 says THE PREVIOUS ACTION, and nothing attributed it. That attribution is also sensor 2's whole input, so they were one change |
| **2** | **precondition edges** — pairwise *a became available after b*, with counts | **BUILT.** `Preconditions` in `instruments.py`, at most `|actions|²` cells — 49 for ARC's seven |
| **3** | **control mode** — avatar / actuator / coupled | **BLOCKED ON `2b`.** It asks which OBJECT the actions move, and that is not expressible while slots are cells |
| **4** | **affordance profile** — seven booleans per object KIND, by contact | **BLOCKED ON `2b`.** Per KIND, and there are no kinds until perception makes them |

> **So `2c` splits, and it is not a clean reorder.** The lens and sensors 1–2 land BEFORE
> `2b`, because the lens is `2b`'s instrument. **Sensors 3 and 4 land AFTER it**, because they
> need what `2b` produces. **The item is not one block that moved — it is two halves either
> side of `2b`**, and treating it as a single reorder would have left 3 and 4 unbuildable at
> the front of the queue with nobody noticing why.

**AND THE NEAR-MISS IS A KNOWN CLASS ARRIVING IN A SEQUENCING DECISION.** The reorder's
reason was correct and applied to HALF the item: *the lens is `2b`'s instrument, so `2c` moves
first.* **Moving the whole item carried two sensors that need what `2b` produces.** A correct
reason generalised one step too far — the same shape as a rule whose subject is narrower than
its property, which this file already tracks six times in the checkers. **This one was in a
plan rather than in code, and it was caught by reading §16.8 properly rather than by anything
downstream.** Nothing would have failed; sensors 3 and 4 would simply have sat at the front of
the queue, unbuildable, with no signal saying why.

**MEASURED, on a fixture that gates an action after five steps** — `snaps` and the toy world
have constant action sets, so neither sensor could fire there:

    action-set delta    came=['ACTION4']  after=ACTION2
    precondition edges  {'ACTION2->ACTION4': 1}

**A COUNT IS NOT A CLAIM.** `Preconditions` counts pairs and does nothing else — no ranking,
no cause named, no gate. **`b` preceding `a` many times is evidence the agent reads; reading
it is the agent's job rather than the table's**, which is the same line the probe holds when
it draws uninformed.

> **AND IT IS THE ONE MOST LIKELY TO ERODE.** A table that RANKS is one line from a table that
> DECIDES, and nobody would call the line a violation — sorting by count reads as a
> convenience. **The proposer/scorer separation is the same distinction and it is enforced by
> nothing here**: `Preconditions` has no consumer yet, so the first consumer is where it gets
> decided. **Recorded now, while the table is inert and the decision is free.**

**No regression:** 1/1 correct, 0/6 false, 1,463 compositions.

---

# `2c`'s lens — BUILT 2026-08-27, and the bracket channel is open

`arc_lens.py`. **Offer coarse views of a board, and offer NONE unless one is near-lossless** —
§5's rule, with `1 − fidelity` as `R_T`. **Both outcomes are exercised**: a uniform board
commits `['full', 'stride:2']`; a speckled one returns **`None`**, which is the honest state
for a board that is not a rendering of anything coarser. **`None` is a READING, not an
absence** — the loop already records it as `channel_closed` with the reason on the row, and a
lens that offered views nothing could commit to would report a channel open and carrying
noise.

**THE VIEWS ARE BUILT FROM SHAPE ALONE.** A stride divides the side or it does not; nothing
in the file is shown a rule, a colour's meaning, or an outcome — the same guarantee
`snaps._views` states for itself, and what keeps offering a view from being answering the
question. **And the block takes its first member's value rather than a mean**, because
averaging would invent a value no cell held.

**The gate is inherited with its provenance rather than chosen:** `0.98`, because a true 5-px
grid scored **0.818** while a spurious 2-px tiling scored **0.946** — the wrong answer scored
higher — so fidelity alone cannot discriminate and the stride comes from motion.

**AND THE CHANNEL IS OPEN FOR THE FIRST TIME ON AN ARC-SHAPED WORLD:** 12 bracket rows,
`cause=genuine`, `R_T=0.0`, `view=full`. **Zero because the agent uses the identity view** —
`stride:2` is offered and nothing selects it, which is INWARD and unbuilt. **Measured zero,
not assumed zero**, which is the whole distinction the nulls sweep exists to make.

**One producer of the quantity.** `round_trip_gap` moved to module level in `tether.py` so
the loop and anything scoring a view share one implementation — the alternative was a second
copy of the gap in the lens, which is the reinvention no grep can see. **And the lens takes
`fidelity` as a callable rather than importing the loop**: the lens knows about shape, the
loop knows about bits, and the domain does not depend on the loop.

**Two things ISOLATED caught, both on first run**, continuing the day's pattern: `lens`
defined and referenced nowhere until the fixture consumed it, and — earlier — `reset_kind`
built ahead of its consumer and removed. **The checker on the author, twice.**

**AND THE STRONGEST FORM OF THE VACUITY DISCIPLINE, arriving as a CONSTRUCTION
REQUIREMENT rather than as a check.** *A control that examines nothing cannot demonstrate a
clean state* is normally asked AFTER the fact — did this see anything? **Here it could not be
deferred: the `None` path needs a board with a cell that differs INSIDE a block, and that
cell is exactly what a coarse view loses.** So **the fixture cannot be completed without
constructing the failure it is meant to detect.** A checker asks whether something examined
anything; this made finishing impossible without it. **Better position than a checker can
occupy, and it was not designed — it fell out of the thing being measured.**

> **AND IT DOES NOT GENERALISE.** The fixture and the failure COINCIDED here: a lens
> whose failure is losing a cell inside a block cannot have its refusal tested without
> such a board. **Most instruments have no such property**, and elsewhere the case has
> to be constructed deliberately — as `Grows` was for blocker 2. **The discipline came
> free once. It is not free.**

**And one error of mine the fixture caught.** I claimed to exercise both lens outcomes and
tested the same case twice: `reset()` sets `n = 0`, so the probe board is **uniformly zero**
and coarse-representable. The `None` path needed a board with a cell that differs inside a
block — which is exactly the cell a coarse view loses, and the reason the path matters.

---

# `R_T` WORKS — 2026-08-27, and it was the invented quantity all along

**`2c`'s first move was a fix, not a build.** `PHILOSOPHY` §0.3 and §16.1 say it twice, in
the same words: ***`R_T` is the gap between `x` and `T_E(T_A(x))`*** — guaranteed
non-negative by the extensive law, *the measurement of what the coarser description cannot
hold*. **That is LOCAL**: the loss on the state actually sent, O(slots), no budget.

**What was built counted the PRE-IMAGE** — how many concrete states share a coarse one —
which is a GLOBAL property of the view and needs a domain sweep. **Different quantity, and
the sweep is why R_T never produced a reading anywhere**: 8.24e+05 on the toy world against a
4,000 budget, 1.68e+04 on `snaps`, 3.32e+13 on a 4x4 board, past float range on 64x64.
**Ninth-plus instance of the sixth law, and the most expensive: the corpus specified the
instrument, the build did something else, and the something-else made it unmeasurable
everywhere.**

**FIRST WORKING READINGS IN THE PROJECT**, and they order the views by what each loses:

    full          0.000    lossless
    drop:sN       2.807  = log2(7), exactly one slot's whole code
    merge:sX+sY   5.615  = two slots
    parity, half 14.037  = all five, since correction_bits is binary

**And the `measured` flag is gone with the sweep** — it guarded a cap, there is nothing to
cap, and leaving it would have been a branch that cannot fire. On the panel: **360 bracket
rows, all reading 0.000, because the view in use is `full`.** That is the same number it
always showed and it now means something different — **before, zero meant UNMEASURABLE;
now it means the view lost nothing**, which is what the code comment always claimed: *`full`
until INWARD exists, where it is measured to be zero rather than assumed to be.*

**THE FIX CAUGHT A BUG IN ITSELF, and it is the same direction error twice in one day.**
First implementation read **`drop:s0` as 0.000 bits** — a view that DROPS a slot, scoring
lossless. The cause was a tolerant fallback: reconstructing a missing key from the true value
lets `T_E` recover exactly what the view discarded. **A dropped slot costs its whole code.**
Identical in shape to `_applies` this morning, where dropping unevaluable frames would have
made a term evaluable on half a history read as a perfect explainer. **Both were caught by
looking at whether the numbers moved, not by review.**

**No regression:** 1/1 correct and 0/6 false abstentions, 1,463 compositions, mint 20 /
settle 6.

---

# `2b`'s detector does not exist, and two documents disagree about which one it is

**Asked before `2b` rather than discovered as a green.** The loud/silent split is `2b`'s
characteristic failure — *an object-level view of a sub-object rule read **zero residual for
twenty steps**, the agent believing it had explained a world still moving underneath it.*
**Three things are true and they do not fit together.**

**1 · `ARC_BUILD_PLAN` names `never_live`, and `never_live` structurally cannot fire on it.**
Phase 2's note reads *`never_live` is now built as the detector, and the utterance can say
it.* But `never_live` requires **`misses == 0`**, and `misses` is WHOLE-INSTRUMENT —
`note_step` increments it when SOME slot carried mass. **The loud/silent case is one slot
reading zero WHILE THE WORLD MOVES**, so other slots are live, `misses > 0`, and the detector
never fires. **A trigger and a signature that do not meet.**

**2 · `DECOMPOSITION.md` specifies a different detector, and names it exactly.** *A
decomposition failure is a PERSISTENT zero, and the predicate that would catch it is **a
fraction over the run rather than a boolean over the step**.* Then, on the round trip: ***that
is exactly the instrument that would have made the silent loss loud. The objects view of a
sub-object rule read zero residual for twenty steps; its round-trip gap on the fleck cell
would have been positive on every one of them.*** **The detector is `R_T`, not `never_live`.**

**3 · And the built `R_T` cannot compute it anywhere.** `_round_trip` finds the pre-image by
**sweeping the domain**, capped by `cfg.budget`:

    toy world        span 8.24e+05    budget 4000   UNMEASURABLE
    snaps            span 1.68e+04    budget 4000   UNMEASURABLE
    arc, 4x4 cells   span 3.32e+13    budget 4000   UNMEASURABLE
    arc, 64x64 cells span OVERFLOWS A FLOAT

**Not merely over budget on a real board — past the range of the number type.** The sweep
implementation is toy-shaped and does not transfer at all. **`logical_grid`'s `R_T` is
`1 − fidelity`, a DIFFERENT computation that does not sweep — and it arrives at `2c`.**

> ### So `2b` ships blind to its own worst failure unless `2c` lands with it or before it
>
> **`2b` is where a decomposition can be wrong, and the instrument that would say so is
> `2c`'s.** `arc_world.transform()` returns `None` today, so the bracket channel is inert
> exactly where the failure lives. **This is a sequencing fact and it was findable before
> `2b` started, which is the only time it is cheap.**

**And the earlier note stands corrected**: `DECOMPOSITION` records *the socket existed and
was not being read* — `transform()` was the tenth contract member and **nothing ever called
it**, its only occurrence being inside a STRING asserting it returns None. **That half is
fixed** — `_round_trip` calls it now and the bracket row names `env.transform() returned
None` as the cause. **The socket is read. What flows through it is still nothing.**

---

# `2a` — BUILT 2026-08-27. The watermark is NOT set

**`arc_world.py`: the eight members over `arc_agi`, and deliberately nothing more.**
`arc-agi 0.9.9` and `arcengine 0.9.3` are installed — **this repo's first third-party
dependencies, 27 transitive** including flask, matplotlib, numpy and pydantic.

**THE DECOMPOSITION AND THE ATOM SET ARE INJECTED, NOT CHOSEN.** ARC has no named slots;
finding them is perception, which is `2b`. The atom set is grid transforms, which is `3d`.
**Both are constructor arguments, because a default for either would be the adapter
answering a question it exists to defer** — and the fixture's `cells` is the IDENTITY
decomposition, which assumes no structure, because assuming none is the only honest
placeholder before perception.

### Three corrections from source, none of them in any document

| | |
|---|---|
| **AND THE §2 RELIABILITY CLAIM NARROWS** | I filed §2 as *the one transcription of three with no error* — nine fields, same names, same types, verified. **That is true OF `FrameData` AND NOT OF THE RAW TYPE.** `FrameDataRaw` is what the wrapper actually returns, and §2 does not describe it. **A section verified on one type is not a section verified**, and carrying it as a general reliability reading would be the same over-generalisation the transcription errors themselves were |
| **`FrameDataRaw` has no `frame` FIELD** | it is a **property over a `PrivateAttr` holding `List[ndarray]`** — *runtime-only, not validated, not serialized*. **The board is a numpy array, not `list[list[int]]`** |
| **the two API paths differ in the board's TYPE** | the harness converts with `arr.tolist()`; the toolkit path does not. **A decomposition written against the harness's lists would silently receive arrays** |
| **`RESET.is_simple()` is `True`** | so `actions()` would have advertised it. **§21.2 bans THE AGENT CALLING RESET** — `bounds.py` exists because a harness once force-RESET on GAME_OVER to farm ~18 unearned attempts. **Withheld explicitly, and the fixture asserts it** |

### The checkers caught two things on the first run

**ISOLATED** flagged `arc_world.py` immediately: `ArcWorld` referenced nowhere, and
**`reset_kind` defined and referenced nowhere in the package.** The second is the pattern
from earlier today — **a mechanism ahead of its consumer.** `reset_kind` is §21.5's
discriminator and `2e` is what consumes it, so **it was removed rather than kept**, with a
comment saying the frame carries `full_reset` and `levels_completed` so it stays recoverable.
**TID251** then caught the fixture reaching `world._atoms` — *a private name across a module
boundary* — so **the fixture declares its own atoms**, which is what a domain does.

### `arc_check.py` is the consumer, and it says what it cannot say

Real `FrameDataRaw` objects from a fake wrapper: **the type contract is genuinely exercised
while the game is not a game.** The eight members fill, `bind` accepts, the loop turns 12
cycles over 478 rows, the gate passes. **And it prints its own limit: A SYNTHETIC SOLVE
PROVES WIRING AND NEVER CAPABILITY.** Figure 11's second failure mode bites hardest here
because the same hand authored both sides.

> ### THE WATERMARK IS NOT SET, AND THAT IS THE RULING
>
> **A synthetic fixture is not a game.** No environment files exist — not in this repo, not
> in the harness repo, not bundled; `arcengine` ships the framework for WRITING games, not
> games. **So the boundary waits for the first REAL environment file**, and every row in this
> index is still `pre-game` by construction. **This is exactly the line that gets crossed by
> a commit message rather than by a decision, which is why it is written down before `2a`
> lands rather than after.**

---

# Why three blockers pass and none can be demonstrated here

**Stated as the reason rather than as an apology.** The three fixes are correct, the panel
shows nothing, and **that is a property of what they fix rather than a gap in the testing.**

> **THE DETECTOR AND THE THING IT DETECTS ARRIVE TOGETHER.** Each blocker repairs a
> mechanism whose subject does not exist on `snaps`, so its correctness is untestable until
> the subject does — **and the subject is Phase 2.**

| blocker | first real test | why not before |
|---|---|---|
| **1 · `never_live`** | **`2b`**, perception | `never_live` is now correct and still fires 0 of 6. **`2b` is the first place that correctness is exercised** — connected components as slots inherits the loud/silent split, and `never_live` is the plan's own detector for it. Blocker 1 went first for exactly this reason |
| **2 · slot re-read** | **`2b`** | `snaps` slots never change. The falsifier had to be CONSTRUCTED to fire — and firing it found three defects, so the construction was not ceremony |
| **3 · contact ranking** | **`2c`**, the affordance profile | every `snaps` slot varies across the residual, so contact scores are near-uniform and ranking has nothing to rank. **§16.4's seven booleans learned by contact are exactly where slots DIFFER in variance** — a wall that never moves, a background that never changes, an object that responds. **`2c` is the first place the ranking has anything to order** |

**So two of three get their first real test INSIDE Phase 2 rather than before it**, and the
third was tested by building its subject. **A green panel here is not coverage and was never
going to be** — which is why it is written down beside the builds instead of inferred from
them later.

---

# Blocker 3 — BUILT 2026-08-27, and the corpus had already refuted the obvious version

**`_bindings` returned `[None] + every other slot`, unordered.** §16.5 says *enumerate
contact*; Figure 11 adds *rank by cascade*. **The obvious build is a contact FILTER, and it
was already tried and already measured.** `_cannot_pay`'s docstring, three lines above code
edited twice today: *the version that skipped operand-reading terms when R showed no
dependence on another slot ... **drops terms that read an operand without varying with it on
the observed slice. Measured, IT LOST A CLOSING TERM.*** **Sixth law, on a docstring already
read twice in the same session.**

> **So contact may ORDER the bindings and may never EXCLUDE any.** Ranking cannot lose a
> term — every binding is still reached — and it is consequential anyway, because **the mint
> breaks on the first closer**, so order decides WHICH closer is found and never WHETHER one
> exists. Filtering is what lost the term; ordering is what §16.5 and Figure 11 actually ask
> for.

**Built:** `None` first, still Occam-priced; then the others by **how much each varies across
the residual's own frames** — a slot constant wherever the bound term was wrong carries
nothing that could discriminate those frames, so it is tried last rather than dropped.

**MEASURED, AND IT CHANGED NOTHING HERE.** Toy world identical — 1/1, 0/6, 1463 compositions,
the same three settled terms. Panel identical — **mint 20, settle 6, the same six terms.**
**The reason is structural: on `snaps` every slot varies across the residual** (five slots over
Z₇, all updating every step), so contact scores are near-uniform and the order barely moves.
**Ranking matters where slots DIFFER in variance — a static slot, a wall, a background.
`snaps` has none; ARC does.** Third mechanism this batch whose exercise waits for ARC, after
`advertised` and `present`'s gone/orphaned branch. **Said here so a green panel is not read as
coverage.**

---

# Blocker 2 — BUILT 2026-08-27, and firing the falsifier found three more defects

**`self.slots = env.slots()` was read at construction and at retarget and nowhere else**, so
an object arriving mid-episode produced **no bet, no residual and no row** — invisible rather
than an error, which is why Phase 2's falsifier could not fire. **`_present()` now re-reads
every step, before the frame is taken, and emits a plain `present` row** naming what came,
what went, and which bound terms were orphaned by a departed operand.

**MADE TO FIRE**, with a throwaway env that grows a slot at step 20 — because `snaps` never
does and a mechanism nothing exercises is the class this file already tracks:

    present rows: 1  ->  cycle 20, came=['newborn']
    bets on the new slot after arrival: 25   (previously 0 -- invisible)
    ran to cycle 45, no fault · gate: PASS over 1,167 rows

**THREE DEFECTS, FOUND BY FIRING IT, none of them predicted:**

- **`history` faulted** on frames where the slot was absent — a slot has no history from
  before it existed
- **and faulted again on the ARRIVAL FRAME specifically**, which holds the slot in `after`
  and not in `before`. **Both endpoints are required**: a transition observation needs a
  before-value, and the arrival frame has none
- **`_ops` faulted** when a candidate term bound the new slot as an OPERAND and was evaluated
  against frames predating it — `_residual_obs` had filtered for the BOUND term, and
  `_cannot_pay` evaluates CANDIDATES

**AND ONE DIRECTION ERROR IN MY OWN FIX, caught before it landed anywhere else.** The first
pass DROPPED unevaluable frames. That is backwards: `_explains` requires `_left == 0.0`, so a
term evaluable on half a history would have looked like **a perfect explainer**. **Inapplicable
is UNEXPLAINED**, and all three sites now charge it — `_left` adds a full unit, `_residual_obs`
includes the frame in R, `_cannot_pay` counts it wrong. **Evaluating it as if unary would have
been worse: a silent change to what the term says.**

**No regression**: `1463` compositions, `16.844` bits, 1/1 correct and 0/6 false abstentions —
identical. `_applies` is always true where slots are stable, argued and then measured.

---

# Blocker 1 — BUILT 2026-08-27

**All three parts in, verified rather than assumed, 8/8 and ruff clean.**

| part | built | measured |
|---|---|---|
| **WHERE** | `Drive.tried` is `dict[str, set]` — action to the **distinct states it was drawn from** — and `choose` takes `where`. `never_live` counts an action only once it has **two** distinct states behind it | `trials()` reads `{A: 8, B: 7, C: 7}` on the panel, so the new denominator is reachable rather than unmeetable |
| **WHEN** | `env.actions()` is **re-read every step** and in `retarget`, which never re-read it. A change emits an **`advertised`** row naming what came, what went, and that **the denominator moved** | **0 events on `snaps`, honestly** — its action set is constant. **And the gate was run over a synthetic ledger containing the new row: `pass`**, so Phase 2 will not discover a rejection |
| **WHAT** | the row carries `trials` and a `scope` field; the verdict says *no SINGLE action, each drawn from at least two distinct states, changed any slot*; **`speak.py` renders the narrow claim** | the account now names its own limit: *that is a claim about single actions and not about everything I could do — **a SEQUENCE I have not tried may still move something, and I have no way to tell from here*** |

**The anchor on the two:** an action earns `inert` at **two** distinct states, never one — one
state cannot separate a dead action from a positional artefact, two is the smallest number
that can. **Not tuned; the smallest with the property.**

**`never_live` still fires 0 of 6, unchanged** — nothing about this made the panel produce it,
and it was never supposed to. **The row and the sentence are exercised by construction rather
than by the panel**, which is stated here so it is not mistaken for coverage.

---

## The brief it was built from

**It goes first because 2b's detector IS `never_live`.** The plan's own remedy for the
loud/silent split is *`never_live` is now built as the detector, and the utterance can say
it*, so **Phase 2's perception layer has no way to see the silent failure it is most exposed
to until this lands.** The other blockers are not blocked by it — they are useless before it.

| part | what | source |
|---|---|---|
| **WHERE** | `tried` keys on **`(action, state)`**. Action labels alone make *every action tried* insensitive to WHERE it was tried, so an action inert against a wall counts as inert | `DISCOVERY` Q18, and `ARC_BUILD_PLAN`'s second pass already states the fix |
| **WHEN** | the denominator is **LEVEL-SCOPED**, and an availability CHANGE is recorded. `actions()` is a fixed tuple read once; ARC's set varies per frame, which makes the same claim insensitive to WHEN | `ARC_AGENT` §2 · the 2026-08-27 ruling |
| **WHAT** | the claim **NARROWS** to *no single action, from the states I have occupied, changed anything* | the ruling's second half |

### Two things answered before parts two and three land — decisions, not rulings

**1 · The availability change is a PLAIN EVENT, not a fourth channel. Decided, and the
reason is the decision.** A condition being met or unmet is residual-shaped — predicted
availability against actual — so the easy path is a channel beside transition, reward and
bracket. **It is not taken, because the loop does not yet know what a condition LOOKS LIKE on
a real board; Phase 2's perception layer is what would say.** Building a channel for a shape
nobody has seen is the decomposition-from-a-description catch, one domain over.

> **And the asymmetry is the reason rather than simplicity: a plain event can become a
> channel later; a channel is harder to unbuild.** Recorded so the next reader knows it was
> DECIDED and not DEFAULTED — picking the easy option silently is how a channel gets born
> without anyone choosing to build one.

**2 · The utterance says the NARROW claim.** Part three changes what the row asserts, and
`speak.py` renders rows into the agent's account of itself. ***No single action, from the
states I have occupied*** is a different sentence from ***nothing I can do changes anything***
— and the second is what the current wording implies.

> **This is the deliverable, not a detail.** *The agent's report of its own epistemic state
> is sound and checkable from outside* is the precondition for triangulation. **A record and
> an account that disagree at the point the claim is strongest is the fifth instance of that
> class this session, and the first that would land in the sentence a reviewer reads.**
> **And the narrow version is the better sentence anyway** — it says what the evidence
> supports and names its own scope, where the broad one overclaims **in the direction the
> whole abstention discipline exists to prevent.**

---

# ABSENCE IS CHARGED UNLESS SOMETHING PROVES OTHERWISE — a standing default

**Three unrelated sites in one day, one direction, and the direction is what matters.** Each
was a place where something was MISSING rather than wrong, and each had a locally reasonable
lenient reading:

| site | what was missing | the lenient reading | what it would have claimed |
|---|---|---|---|
| **`_applies`** | a frame the term cannot be evaluated on | skip it | **a term evaluable on half a history is a PERFECT EXPLAINER** — `_explains` needs `_left == 0.0` |
| **`round_trip_gap`** | a slot the view dropped | reconstruct it from the truth | **a slot-DROPPING view is LOSSLESS** — `drop:s0` read 0.000 bits |
| **`perceive`** | a slot that vanished under the bet | omit it from the residual | **an object that died was correctly predicted** |

> **ALL THREE FAIL TOWARD *NOTHING WAS LOST*, which is the direction that goes quiet.** So it
> is a DEFAULT and not three decisions that happened to agree: **absence is charged unless
> something proves otherwise.** The exception has to be argued at the site; the charge does
> not.

**And none was visible to review** — skipping an inapplicable frame, filling a missing key,
omitting a dead slot all read as reasonable. **All three were caught by a number that did not
move**, and each time only because the right value was derivable from outside the code.

---

# A fallback in a reconstruction is a CLAIM THAT NOTHING WAS LOST

**Twice in one day, in unrelated code, and identical in shape.** Both were leniency in a
reconstruction, both made a loss invisible, and **both failed toward *nothing was lost*,
which is the direction that goes quiet.**

| | the tolerant line | what it claimed | what it was |
|---|---|---|---|
| **`_applies`** | drop frames a term cannot be evaluated on | *this term explains the history* | `_explains` requires `_left == 0.0`, so **a term evaluable on half a history reads as a PERFECT EXPLAINER** |
| **`_round_trip`** | `back.get(s, before[s])` — fall back to the true value for a slot the view dropped | *this view is lossless* | **`drop:s0` read 0.000 bits.** Dropping a slot is maximal loss; the fallback let `T_E` reconstruct exactly what `T_A` discarded |

> **A reconstruction that fills a gap from the source is not a reconstruction. It is the
> source wearing the reconstruction's name**, and every measurement taken across it reads
> zero loss.

**AND NEITHER WAS VISIBLE TO REVIEW.** Both lines are locally reasonable — a missing key
plausibly means *unchanged*, an inapplicable frame plausibly means *skip*. **Both were caught
by watching whether a number moved**, and only because the right value was known
independently: a view that drops a slot must cost that slot's code, and `2.807 = log2(7)` is
checkable without trusting the implementation.

**So it is witnessed the way an exemption is**, per the checker law — *witness the boundary,
not the decision*. **A fallback is a boundary: it is where the measurement stops measuring
and starts assuming**, and it belongs in a table that can be pinned rather than in a line
that reads fine.

---

# Which nulls can the panel only produce?

**A standing sweep, not a row.** Three mechanisms were found reporting a null the panel
cannot make read otherwise, each REPORTING IT HONESTLY -- which is what made them invisible.
The honest-null habit that makes everything else readable is what hides these.

**The instrument:** a recorded field that never varies across a whole run is either a
constant or a mechanism that never fires. Fourteen such fields in the demo ledger; the
event counts are the sharper cut.

| measured zero | across | which kind |
|---|---|---|
| **`Clocks.reads` says *suspect luck* on half the panel** | 10 worlds | **the panel, and it is STRUCTURAL rather than empirical — a verdict built from two quantities with DIFFERENT DENOMINATORS.** `modelled` is *no slot owes*, over **all five** slots. `won` is *objective degree >= 1.0*, over the **two** the objective scopes (`spec_for` sets `n = max(1, slots // 2)`). **So winning before modelling is guaranteed by construction on every generated world**, and `won without modelling -- suspect luck` fired on **5 of 10**. **The numbers are sound — `execution_gap` read 2 and -2 — and the STRING is a null the panel can only produce.** Fourth instance of the class, and the first where it is a VERDICT rather than a field: **a field that never varies is visible; a verdict that is always available is not.** The fix is a denominator, not a measurement |
| **`R_T`, zero readings** | every run ever | the panel cannot: no `transform()` in `world`, and `snaps`'s sweep needs 16,807 against a 4,000 budget |
| **priors, zero loads** | every run ever | nothing passes `molecules`; the parameter has no call site |
| **`promote`, zero** | 360 cycles, 6 worlds | **the panel, AND IT WAS ALREADY WRITTEN DOWN** -- *four independent slots make echo nearly accidental*. Echo needs a term minted for one slot to close a residual on another. This is that claim with a number attached for the first time |
| **`refused`, zero** | 360 cycles, 6 worlds | not the panel -- nothing has ever been ill-typed. **Corrects a claim made three batches ago**: the type system is load-bearing STRUCTURALLY (no path to `env.step` avoids `_utter`, verified) and has NEVER ONCE BLOCKED ANYTHING. Both true, and only the first was said |
| **`unreached`, zero** | 360 cycles, 6 worlds | open -- `never_live` needs every action tried with no miss anywhere |

**THE EIGHTH LAW'S SHAPE, recorded here and NOT installed** -- putting it in `CLAUDE.md`
and `conform/lint.py` is a build and has not been asked for. **A search for the wrong name
returns the same empty set as an absent mechanism, and only the second is a finding.** It
is the law most likely to recur precisely because the sweep above is an instrument that
produces empty sets BY DESIGN: every null it reports has to survive that question first.
Three instances in one batch -- `abstain` for `park`, the fatal-invertible case that cannot
arise, and the field below.

**AND ITS COMPANION, which cost more:** *an explanation that satisfies closes the question
just as firmly as an absent one.* `promote: 0` had a correct, already-written explanation --
**four independent slots make echo nearly accidental** -- and being correct is what stopped
anyone asking what the zero MEANT. It meant arrival had never occurred. **A satisfying
answer and an absent answer both end the inquiry, and only one of them looks like a
finding.** §5 states the discipline as a rule already: *residual first, frame second --
describe the gap before you go looking, or any frame you pick will seem to fit.*

**And the instrument's own limit, found by it firing wrong.** `allowed: true` on 32 rows
looked like a guard that never denies. It is not: the refusal is a DIFFERENT EVENT --
`hold`, with `status="candidate"` -- and `cite` carries `allowed` only on the branch where
it is true. **A field emitted on one branch can never vary.** cite 32 / hold 13, both live.
So the sweep must be run over EVENTS as well as fields, and a constant field is a question
rather than a finding.

---

# Claims with citations

**Not rows. What a stranger asks for when they press**, and what makes an exception
auditable. Collected while reading, with the source that carries each.

| claim | the citation | where |
|---|---|---|
| **a frame cannot certify its own limit** — so `depth_exhausted` refusing to claim absence is a theorem | **Chaitin**: beyond a fixed constant, no system proves any object exceeds its own complexity | Figure 8 |
| a frame cannot reach its own metaframe | **Gödel** second theorem · **Tarski**: truth for a language is not definable within it. **ONE DIAGONALISATION FAMILY, NOT SIX PILLARS** — Turing, Gödel I & II, Tarski, Rice and Chaitin are faces of one result, and Figure 8's rules 1–3 are that family. **Counting them as independent supports is the inflation the corpus warns against**, and the same arithmetic as the design effect one row down | Figure 8 · `PHILOSOPHY` §6 |
| **`R_T` is a definition, not an invented measurement** | **Cousot & Cousot 1977**, the Galois connection -- and the corpus's ruling is that this is *strictly better than relativity for every purpose you had for it*: lossy by construction, non-invertible by construction, levels genuinely differing in expressive power. **An INVERTIBLE transform would be fatal** -- a bijection iterated gives orbits, not a tree, so one lineage cycles and nothing speciates | `PHILOSOPHY` §0.3 |
| **the anchor is not a privileged frame, it is the invariant** | **special relativity** as the existence proof that *no privileged frame* does not imply *no objective truth* -- observers disagree on duration and length and agree exactly on the interval. Tagged **translation, weight zero**, and the corpus then breaks the analogy in three places itself. Says WHY the anchor must not update: not governance but a type distinction, since the anchor is not a frame and has no vantage to update from | `PHILOSOPHY` §0.3 |
| **the framework applies every law to itself and does not certify itself** | the same **Gödel** rule, turned on the corpus. Self-application is a consistency requirement and is met; self-validation is forbidden BY THE FRAMEWORK'S OWN RULE 2 and is not claimed. **Both halves in one sentence or it is a free kill** -- and the volunteered counterweight is that coherence is not correctness, since astrology is internally coherent too | `PHILOSOPHY` §0.2 |
| composing inside a closed set never adds an atom | **definitional** — it is what closure means | Figure 8 |
| **generation is nearly empty, and checkably so** | **Frank on the Price equation**: *a mathematical identity ... dynamically insufficient* · **Kerr & Godfrey-Smith**: *no natural way for novel entities to appear* — origination must be added by hand as an extra term | `PHILOSOPHY` §7 |
| `R_T` is non-negative by construction | **Galois connection**, abstract interpretation — `T_A ≡ α`, `T_E ≡ γ`; the extensive law gives the sign | `PHILOSOPHY` §16.1 |
| agreement among correlated frames is worth less than it looks | **the design effect**: `n` correlated observations carry the information of `n / (1 + (n−1)ρ)` independent ones — twenty frames at ρ = 0.9 are worth about 2.2 | `PHILOSOPHY` §16.4 |
| selection transmits at most `log₂ N` bits per round | **Levin's conservation of information, 1974** — `I(A(x):y) ≤ I(x:y) + c_A`. **Cite this one and not the weaker `K(f(x)) ≤ K(x) + K(f) + O(1)`**, which §6 records the corpus citing by mistake, with the wrong year, and with a half that had no published proof until **Vereshchagin 2019**. **Disambiguate from Michael Levin**, a different person in a different region | `PHILOSOPHY` §16.5 · §6 |
| **a verifier's non-access is what makes verification sound** | **Goldwasser–Micali–Rackoff** — not a limitation the verifier tolerates but the source of soundness. **This is the guard the prior loader needs**, in its strongest available form: `speak.py` reads agent state, the Gate reads world and ledger, and whatever loads priors must not see what the agent has to learn | `PHILOSOPHY` §6 |
| the shadow test has a formal parent | **Gentner's structure-mapping, 1983**, and its **systematicity principle** — prefer mappings preserving higher-order relational structure over surface attributes. Named forty years before Figure 9's lookup | `PHILOSOPHY` §6 |
| **entropy falls in the survivors, not over the survivors plus the discarded** | **Landauer** (`kT ln 2` to erase a bit) · **Bennett's** resolution of Maxwell's demon (the sorter must reset its memory, and the reset is where the debt is paid). Selection IS a sorting operation, so it cannot come out ahead for free. **§15 notes the corpus had these filed apart from the entropy claim** -- region ⓪ carries them under *the bill has a physical floor*, and they are the same result | `PHILOSOPHY` §15 |
| **falling entropy proves nothing unless the anchor is still** | a population converging against an anchor that UPDATES shows the same falling entropy as one genuinely learning -- **same measurement, opposite meaning**, and collapse 1 is indistinguishable from selection by the entropy reduction alone. So *the anchor must not update* is **the condition under which the reduction means anything**, not a governance preference. **The falsifier it hands Figure 2: measure population entropy AND anchor movement.** Population-scale, so not available at n = 1 | `PHILOSOPHY` §15 |
| **randomness supplies the variation; the ground supplies the information** | **Levin's conservation clause** again -- a random source raises algorithmic information only weakly, with bounded expected gain, so a kernel cannot be conjured from randomness. Keeps the entropy claim consistent with `NOVEL = 0` and with A2, *the seed is interchangeable, the kernel is decisive* | `PHILOSOPHY` §15 |
| **the shadow test, turned on this project's own domain choice** | Q26 closes the eight-slot contract with the framework applied to its own porting: *was there a residual in this domain already unexplained that the framework predicts, or did we go looking for somewhere to put it?* **Echo without shadow is apophenia, INCLUDING when the thing being ported is this framework.** The question is answerable and has not been answered in writing | `DISCOVERY` Q26 |
| **what is deliberately NOT formalised** | §16.9's closing list, and it is a discipline rather than a gap: *the answers already exist* is metaphysics and §9 rules it inert; **the marble is an intuition pump and formalising it would produce a worse version of NFL, which is already cited**; **echo's cross-domain half is a question about the world's supply of analogies, not a quantity -- keep it a judgement and say so**; and *the same booth at every scale* is a research programme, not a theorem, carrying FMap's own label: empirical hypothesis | `PHILOSOPHY` §16.9 |
| **the framework's actual position in the control literature** | it **is** a first-order cybernetic system and says so -- ground = reference, world = plant, `R` = error signal, Γ = controller. **What it adds: steps 3 and 4 change the controller's VOCABULARY rather than its parameters**, which is a real distinction from classical adaptive control. **The precise claim to make, instead of the large one** | `PHILOSOPHY` §13 |
| **the information theory arrived by MDL, not by Wiener** | the acceptance bargain is **Rissanen 1978**, itself a composition of **Kolmogorov and Shannon**. So citing cybernetics for the information-theoretic half would count one lineage twice -- **Shannon was inside the loop by a shorter route before anyone went looking**. Third anti-inflation catch after the diagonalisation family and the Ashby/Conant-Ashby pair | `PHILOSOPHY` §13 |
| **the regress has ONE formal answer, not two** | the reflective tower (Smith, Wand & Friedman) and eigenforms (von Foerster 1976, Kauffman 2003) are **both fixed points of an infinite recursion, finitely representable, terminating a regress by fixed point rather than fiat**. Y-combinator / Scott-domain theory is the shared floor. **Two citations, one answer** | `PHILOSOPHY` §12 |
| **cite Wolpert for the proof, cybernetics for the vocabulary** | *the observer is inside the system* is **a framing in second-order cybernetics and a theorem in Wolpert 2008**. Tag the tradition **translation, weight zero**. And **Spencer-Brown's *Laws of Form* is explicitly NOT to be made load-bearing** -- historically important, mathematically contested | `PHILOSOPHY` §13 |
| **the dot map, not the belief** | *"The answer already exists" and "I have the answer" are separated by exactly one thing: **an instrument a sceptic cannot wave away.**" Snow's contribution was not believing cholera was waterborne -- others suspected it -- but the map, and a pump handle you could remove and watch the deaths stop. **The rule §10 invokes when it calls the search-reduction factor the only kind of claim that counts** | `PHILOSOPHY` §1 step 5 |
| **you cannot escape the bill, only choose the currency, schedule and exponent** | **somatic hypermutation** is the one natural instance of steered variation -- AID targets antigen-binding regions and spares the constant ones, paid in lymphocytes rather than organisms. **But unsteered evolution paid in organisms over a billion years to build the targeting machinery.** You can have steering; somebody buys the aim first | `PHILOSOPHY` §2 |
| **the only controlled experiment in the whole loop** | **Schulz & Bonawitz** on *disambiguating intervention* — after confounded evidence, act to separate hypotheses — and **Gopnik** on causal structure learning from intervention. §21.1: everywhere else the agent gets **observational** data, and *correlation is cheap; causation is not, because **you can never re-run the same moment.*** A level-resetting loss breaks that **because the games are deterministic**: same starting board, vary exactly one action, observe the difference. **That is the machinery separating `A→B` from `A and B co-occur`, and it is the only place in the loop where a controlled experiment is available.** Its precondition is determinism, which is a property of the domain and not of the design | `ARC_AGENT` §21.1 |
| **arrival is a separate problem from survival** | **de Vries, 1905** — *the arrival of the fittest*, as distinct from the survival of the fittest. Selection explains survival; nothing explains arrival. §6: *the whole project's title and its whole problem* | `PHILOSOPHY` §6 · §0.1 |
| no inference device can infallibly predict or control itself | **Wolpert, physical limits of inference, 2008** — independent of the physical laws. The most direct formalisation of *the interpreter cannot be the composer* | `PHILOSOPHY` §6 |
| typing beats size, as a number | **spectral radius** of the type transfer matrix, standard analytic combinatorics for context-free specifications | `PHILOSOPHY` §16.6 |
| a strict MDL inequality needs a margin | **normalised maximum likelihood**, or a **Bayesian mixture code** — both build the penalty in rather than bolting a factor on | `PHILOSOPHY` §16.8 |
| the ledger makes a domain-blind checker sound | **reification vs reflection**, Friedman & Wand, LFP 1984 | `DISCOVERY` Q23 |
| a termination regress is killed for free; productivity is what costs | **Smith's** reflective tower — lazy instantiation over dormant levels | `PHILOSOPHY` §11 |
| the mint-vs-probe fork has a number | **Ashby 1956**: `H(outcome) ≥ H(disturbance) − H(regulator)`; **Conant–Ashby** with its scope attached | `DISCOVERY` Q24 · `PHILOSOPHY` §13 |
| no rank-order vote among candidate grids picks the true one | **Arrow's impossibility** — so the arbiter is a measurement, not a vote | `DISCOVERY` Q19 |
| a settled term re-entering the search as one unit | **Chase & Simon 1973** chunking · **Soar** · **DreamCoder** library learning | `ARC_AGENT` §14.2 |

**And one anti-citation, kept because it is the standard being aimed at:** `logical_grid`'s
`0.98` docstring records the measurement that forced it **and the value that would have
been wrong**. No constant in this repo meets that bar.
