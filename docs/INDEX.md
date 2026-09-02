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

> **WATERMARK: SET 2026-08-27, at the commit bearing this line.** Every row at or before it
> is `pre-game` **by construction** — no game existed, no adapter had run, and `git blame`
> against this commit hash answers *was this written before any game* for every row, forever.
> **Every row after it carries `provenance` explicitly, and `unattributed` after the watermark
> is the one combination that must be justified rather than noted.**
>
> **DELIBERATE, NOT CROSSED.** The line is set in its own commit, before `environment_files/`
> exists and before any download — because a watermark that arrives as a side effect of
> fetching a game records the moment badly. The gitignore went first for the same reason: each
> is free only before, and neither is folded into the run.

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
version.** **And the single type is the one that keeps being paid for**: it is not a question
awaiting an answer but a property every type-keyed measurement on this panel is missing, so it
is stated as a defect below rather than as an open question. Each for a stated structural reason rather than a hunch.

| question | what the panel would need | why `snaps` cannot |
|---|---|---|
| ~~should shadow-only terms cross?~~ | **ANSWERED — `SNAPS_PLAN` §3 rules standing persists.** Not a panel question after all | — |
| ~~does the library transfer?~~ | **ANSWERED — not waiting.** Reuse across DS is 0.72, 0.35, 0.21, 0.20, 0.04, monotone. `SNAPS_PLAN` §7 falsifier 1 does not fire. The level-wise flatness was one point at DS 0.4 | — |
| **REUSE NEVER CLOSES — the second panel defect, found by `3d`.** The funnel reports `{'no-eligible-target': 4}` and the ladder stage is **`REUSE_UNWIRED`**, *implementation, loop not connected*. **Every unit reads `used == 1`, flat at 16, 40 and 80 cycles.** So anything ranked by, gated on, or measured over REUSE is undefined here — `3d`'s rank function has two of three terms inert on it. **Stated as a defect, not an open question, for the same reason as the type node: the third mechanism to hit it should not pay the discovery cost again** | a run in which a settled term is bound a second time, or bound for a second slot | the funnel attempts and finds no eligible target, every time |
| **does coarsening make rules expressible?** | a value space with non-trivial quotients, or structure that regroups rather than coarsens | `M = 7` is **prime**, so no non-trivial coarsening of Z₇ preserves the arithmetic the atoms are made of |
| **what does a coarse view lose?** — **NOT *NEVER MEASURED*; *FIRST MEASURED IN THE NEXT BUILD*.** The reason it is unmeasured here — a domain sweep needing 16,807 against a 4,000 budget — **does not apply to a fidelity number over a detected grid.** Different disposition: not a dead mechanism, an unexercised one whose first real reading is scheduled. **AND IT IS LOAD-BEARING THERE.** `ARC_AGENT` §5: `logical_grid` commits to a detected board **only if the round trip is near-lossless**, returning `None` otherwise, and **`1 − fidelity` IS `R_T`**. So the mechanism with zero readings here **is the lens's admission criterion there.** Its calibration is the anti-citation in this file: a true 5-px grid scored **0.818** while a spurious 2-px tiling scored **0.946** — **the wrong answer scored higher**, which is why the gate sits at 0.98 and the stride is taken from motion instead of from fidelity | a domain small enough to sweep within the declared budget | **`R_T` HAS NEVER PRODUCED A READING.** `world` returns `None` from `transform()`, so `_round_trip` is not called -- recorded honestly as `channel_closed` with `inert` naming the reason. `snaps` DOES offer views, so it is called, and returns `(0.0, False)` every time: the sweep needs `7^5 = 16,807` and `budget` is `4,000`. The toy world would need `823,543`. **Every reading in existence is the capped case**, which is why the docstring's *not a small R_T, it is NO R_T* is carrying the entire mechanism |
| **ONE TYPE NODE — and it is a PANEL DEFECT, not one mechanism's question.** Originally filed as *does typing beat size?*, which is λ's version of it. **It has now cost two mechanisms and will cost the third**: `λ` reads `V` by construction, and `3c`'s retrieval read **3% work avoided** on the demo before the corollary caught it — *retrieval discriminates on type signature, and there is one signature.* On `3b`'s three spaces the same code reads **11 evals → 4**. **Anything keyed on, ranked by, or measured over TYPE is undefined on this panel** — which is `3d`'s rank function next, since *type-match to the residual* is one of its four terms. **Do not rediscover it a third time: state the panel first, then read the number.** `3b`'s own closing line is the general form, written before either measurement — *the instrument was working; it just had nothing to measure* | atoms spanning more than one type | **every atom is the same type**, so the transfer matrix is 1×1 and `λ = V = 8.0` BY CONSTRUCTION, `types: 1`. `demo.py` reports it and reads it correctly — *typing buys nothing in this world, and that is the instrument working*. But a panel that can only ever return `λ = V` **cannot distinguish a sparse grammar from a dense one**, so the falsifier fires without carrying information about the code. **`ARC_BUILD_PLAN` Phase 3b's done-when is `λ < V` with a real ratio — it cannot be graded here at all**, which is a sequencing fact rather than a defect |

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

# WHAT THE FRAMEWORK IS FOR, and the question to ask a reading FIRST

`[I]` *"The metatheory does not solve anything. It says what a solution has to look like. And
the residual tells you which part of that shape is missing."*

**NEITHER HALF WORKS ALONE: the shape without a reading is a claim; a reading without the shape
is a null.** And today is the clean example — **the shape said *the outcome should be the
world's response, per slot*; the reading said `0.0`; the gap between them was a wrong
variable.** Neither the shape nor the number would have found it.

### WHY SO MUCH OF THIS IS INSTRUMENTS

**The shape constrains the instruments too**, and that is what most of this file records.
*Three states, not two.* *A refusal names its condition.* *Report, do not adjudicate.* **None
is about the agent** — each is **the form a checkable claim has to have**, applied to the thing
doing the checking.

> **Which is why the corpus keeps being right about tooling and silent about design choices.
> It constrains FORM. It does not pick CONTENTS** — and that is exactly why *a choice nobody
> has made* is a **residual and not a gap.**

### AND AN INSTRUMENT IS MADE BY BEING WRONG, NOT BY BEING BUILT

**Not built, then used. Built, used, found wrong in a specific way — and the finding is what
made it an instrument.** The nulls sweep's first output was its own false positive.
`disproof`'s first version was a tautology, width 7 over the whole of Z₇. The controlled
experiment measured the MODEL where §21.1 asks about the WORLD. **Each is the loop applied to a
tool, and this register is not a list of failures — it is how each became one.**

### WHAT CHANGES IN PRACTICE

**The first question about a reading is not *what did it measure*. It is *does this reading
have the form the shape says it should*.** *The outcome is the world's response* would have
flagged the residual variable **before the number was taken**.

**Twice in one stretch a null was read as a result** — `pairs 0` and the reuse funnel — **and
both were the instrument rather than the quantity.** The shape is what asks that first.

### AND THE GUARD IT MUST ARRIVE WITH

**A proctor who knows the shape can fit findings to it.** That is the failure this discipline
exists against, and it is why **pre-registration, the panel-cannot-exercise corollary, and
*report, do not adjudicate* are all defences against the person holding the shape.**

> **The shape says what a solution looks like, and a reading that conforms to the shape is not
> thereby correct. BOTH HALVES, ALWAYS TOGETHER.**

### TWO CONSEQUENCES RECORDED WITH IT

**`B17` is at two instances and the discipline caught neither.** *Nine-versus-thirty-seven* and
*residual-versus-world* were both large enough to notice on their own; pre-registration held in
both cases and did not help. **The discipline names the branches; it does not check the
variable.** Two instances, zero caught by the thing meant to catch them.

**And a decision's value cannot be assessed when it is made.** `signature()` was chosen against
Figure 2's collapse and paid for §21.1's determinism precondition, which nobody was measuring.
**Which is the argument for recording the REASONING rather than the conclusion — the reason is
what lets someone later see what else it bought.**

---

# THE LOOP APPLIED TO DESIGN DECISIONS — §0.2 rules it IN, and it breaks in two places

`[I]` *"If the framework is recursive over bounded frames, a design decision is a bounded
frame ... a choice nobody has made is a residual, and it has been treated as the place the
theory stops."*

**Filed as two break points and NOT as an endorsement** — a general endorsement would be
exactly the coherence §0.2 says the recursion buys, sold as the correctness it says the
recursion does not.

### 0 · IT IS NOT A PROPOSAL. §0.2 ALREADY RULED, AND IT RULED IT IN

> *A theory about frames that exempts itself is either **special pleading** (the law binds
> every frame but this one) or **incomplete** (it does not cover the case of itself, so it is
> not general). **There is no third option.***

**So exempting design decisions is the special-pleading branch, already named.** The gap is
that the recursion has not been RUN at this scale, not that it was undecided.

**And §0.2 pre-answers the thin part, differently from how it was framed.** The distinction it
holds is **apply vs certify**: self-application is a consistency requirement and is met;
self-validation is forbidden by Figure 8's rule 2. Then the closing line — ***the recursion
buys coherence, not correctness, and the framework already says which one settles it. The
ground does.*** **The slow clock rate is therefore not thinness in the recursion**: the
recursion settles nothing at ANY scale, agent included. The ground being expensive here is a
fact about the ground.

**The decision type also already exists, and it is the four-value `provenance` field above.**
`chosen` — *fills a design space the corpus MARKED and did not settle* — IS this category,
already carved, and already given the reason it cannot collapse into `unattributed`: *the
corpus rules out wrong answers and leaves choices, so a mechanism filling a marked design
space is a DECISION, not a leak.* **It is scoped to mechanisms. That is a SCOPE gap, not a
missing primitive.**

**And the ground is cheaper than a phase.** `ARC_BUILD_PLAN` §191 supplies it: *the test is
whether the fix generalises — **bindings come from contact** is general; **this game needs a
wall detector** is not*, over the two-row typing (*a game showing you something is broken* is
legitimate; *a game telling you what to build* is the leak), and it calls the count
**COUNTABLE rather than a matter of confidence.** Step 5 does not have to cost a phase.

### 1 · BREAK ONE — THE INDEPENDENT SCORER AND THE GENUINE RESIDUAL ARE DISJOINT

**The section-check is not a settle. It is step 2, reachability, and it is `_library_fit` at
the seat's scale.** It asks *does the corpus already determine this* — *can it be composed
from commitments already made.* A settle is a verdict on whether a choice was **right**; this
returns whether it was **already made.**

**Six for six today the answer was REBIND — and by the loop's own accounting a rebind is not a
discovery.** It means there was no residual there. The check has been paying by finding that
the gaps were not gaps. **Real value, and not evidence the recursion produces mints.**

Then the disjointness. §8.4 carries the clause: ***death → explanation requires an interpreter
derivationally independent of the thing being explained. Otherwise it is two mirrors.*** The
corpus qualifies — written earlier, in a different context — which is Figure 6's *contact with
a frame whose closure differs*, and is **why the check works at all.**

> **But the corpus is silent BY CONSTRUCTION on exactly the decisions that need settling.** A
> genuine unmade choice is one it did not rule on — that is what makes it unmade.
>
> **Where the corpus speaks, the decision was not a residual. Where it is silent, there is a
> real residual and no independent frame except the slow ground.**
>
> **The section-check can never settle the decisions that need settling.**

**And §8.4's complaint at agent scale is this same gap one level up** — *nothing says the
sorter must be independent of the composer.* **The theory failing in the same place at both
scales is a stronger result than it succeeding at both**, and it is the sharpest evidence in
this section that the recursion holds.

### 2 · BREAK TWO — NO DECLARED CODE, SO THE BARGAIN IS UNPRICEABLE

`|φ| + |R|φ| < |R|` requires a **declared CODE**, and the loop declares one on every mint row.
**At seat scale nothing declares one.**

So *a decision taken because it is convenient is a threshold wearing a bargain's clothes* is
true and understated: **without a code the two cannot be told apart even in principle.**
**Not a discipline failure — a missing declaration.** Decisions can be COMPARED; they cannot
be PRICED.

**And the split is clean: the guard triple lifts, the bargain does not.** SUPPORT (is there
evidence in the frame), REACHABILITY (composable from decisions already taken), NOVELTY (a new
commitment or a restatement) are **three predicates and all three survive the lift.** The
bargain is **one inequality and it does not.**

### 2b · BREAK THREE — a second independent frame exists, and it qualifies only intermittently

**The analysis above concludes the corpus is the one derivationally independent frame.** That
missed one that was operating the whole time: **the ARRANGEMENT — two parties, one proposing
and one checking.** It met Figure 2's condition **twice in a day, in opposite directions**: a
class I proposed over four different failures, dissolved by a check; a connection Isaiah
proposed, held at a link. **Neither was caught by whoever proposed it.**

> **But the property is not *two frames*. It is *two frames DISAGREEING*, and agreement
> between them is worth exactly what Figure 2 says agreement is worth** — *two frames agreeing
> tells you about their shared evidence pool, not about the world.*

**AND THE RECORD SAYS SO PLAINLY.** The identity violation, the three-of-five split, the
reproduce-versus-collide — **all agreements, all wrong.** The two that held were the two where
one party pushed back. **So the arrangement produced results twice and cannot be relied on,
because nothing makes either party disagree. It happened; it is not a mechanism.**

**WHICH LEAVES THE SECTION'S HONEST STATE AS TWO FRAMES AND NEITHER SUFFICIENT:** one that is
independent and **constitutively silent** exactly where a decision needs settling, and one that
is independent **only when it disagrees**, with nothing to make it. **That is a third break
point rather than an improvement to the first two** — and it is why the recursion buying
coherence rather than correctness is the operative clause, not a caveat on it.

### 3 · THE ENUMERATION IS PARTIALLY AVAILABLE, AND THE REST IS REFUSED

| | |
|---|---|
| **available** | decisions typed **by source** — the four-value `provenance` · typed **by cause** — §191's two rows · the **generality test** |
| **NOT available** | a typed space of what decisions are **about** |

**Refused rather than supplied, and the reason is this session's own catch:** inventing it
would be **`type-match` at seat scale** — a term that reads well, is not in the corpus, and
silently double-weights the same evidence. `3d` caught that one because §17.7 had a tuple to
check against. **Here there is nothing to check against, which is precisely why it must not be
invented.**

**One observation, with its n stated: all three instances are the same shape — *which of two
already-built objects owns this responsibility*.** Slots vs objects · extension classes vs
retrieval keys · grammar vs gamma pricing. **An ALLOCATION decision between existing things.
n = 3, one candidate shape, not an enumeration** — and it should arrive a fourth time
unprompted before being treated as one.

### 4 · TWO CORRECTIONS TO THE CLAIM AS STATED

**It is residual vs ABSENCE, not residual vs gap.** `R_T` *is* a gap; the two are not opposed.
The live distinction is that a residual is **charged** and an absence is **uncharged** — and
**absence is charged unless something proves otherwise** was adopted from three sites earlier
today. **So the claim is a consequence of a standing rule rather than a new one**, and filing
an unmade choice as *where the theory stops* is the uncharged reading that default already
rules out.

**And the `3b` analogy is stronger than stated.** `3b`'s finding was that `enumerate_closure`
was ALREADY type-directed and `Atom` ALREADY carried types — ***the machinery needed nothing
new***; what was missing was an atom set with varied types. **Applied here: the loop is already
domain-agnostic, `provenance` already types decisions, and what is missing is again INSTANCES
WITH VARIED TYPES.** **Which is the panel defect for the third time, now at the seat's scale**
— beside the single type node and the unwired reuse funnel.

### 5 · HELD, NOT FILED — two observations with their bars, and the second is why this exists

**THE THIRD PANEL DEFECT MAY NOT BE ONE, AND IT PRESENTS IDENTICALLY TO THE TWO THAT ARE.**

| | the type node · the reuse funnel | the seat-scale one |
|---|---|---|
| what supplies the missing property | **a different panel** | **nothing can** |
| how the next mechanism meets it | it **re-announces itself** the moment something keys on it | **silently, from zero** |

**Decisions arrive one at a time, from Isaiah, unrepeatably — the instances ARE the project's
history.** So there is no panel that could supply varied ones, which makes it **categorically
different while looking the same from inside a null reading.** It may be a fourth thing the
GROUND is expensive about rather than a fourth defect — **which is §0.2's own recursion-thin
vs ground-costly distinction, arriving one level further in.**

> **HELD AT n = 1. BAR: a second arrival before it is filed as anything.**

**And it is recorded for an asymmetry that applies to it and not to its neighbours.** The other
two re-announce themselves; **this one, if lost, is met from zero and mistaken for them** —
which is the confusion it exists to prevent. **It was called the sharpest thing in a writeup it
was not in**, so the compaction failure `CLAUDE.md` names landed on the one observation least
able to survive it, and that is the argument for the row rather than a reason to note it.

**The two held observations, in one place so neither is a memory:**

| held | n | bar |
|---|---|---|
| the **allocation shape** — *which of two already-built objects owns this responsibility* | 3 | a **fourth, unprompted** |
| **the seat-scale defect may be the ground being expensive, not a defect** | 1 | a **second arrival** |
| **a guard whose SUBJECT excludes the thing it guards against** | **1 observed** (+1 predicted) | a **second OBSERVED instance**, not a second instance |
| **the producer states a distinction AT THE SITE and the consumer discards it** | **2** | a **sixth instance** |

**THE FOURTH ONE, AND ITS COUNT WAS CORRECTED BEFORE IT WAS WRITTEN DOWN.** I claimed *three
of five* in conversation. **Checked: one of five.** Only `Affordances.profile` states the
distinction in its own docstring — *`None` means UNREAD ... a different claim from False, kept
distinct **for the same reason `unreached` is kept distinct from `unreachable`*** — and
`_rtype` collapsed it into *affords nothing* one layer up. **`Objects` states *an object not
found is NOT dead* and that rule was FOLLOWED. `components` states no totality distinction at
all; §12.2 does, in the corpus.**

**AND CHECKING THE COUNT SHOWED THE FIVE ARE NOT ONE CLASS.** `never_live` is the fourth
failure class above; `_bindings` is the ninth, a citation making wrong code look derived;
`_cannot_pay` was a filter-versus-order error; `components` was a missing totality specified in
the corpus rather than at the site. **Four classes, and the pattern I proposed was a fifth
laid over them.** A count taken as a figure would have made a class out of a resemblance.

**WHAT IT IS, NARROWLY: the sixth law one layer in.** *Assume it is already specified and go
look* has been applied to the corpus all week; **this is the same move at a CALL SITE.** The
producer wrote down what its output distinguishes, and the consumer did not read it — **not a
subtlety missed, the thing it consumes unread.**

**And the check it implies is a READ rather than an analysis**: *what states does this output
distinguish*, answerable from the producer's own docstring, **local to one call site.** That
locality is what separates it from the general form — and **at n=2 it is an observation, not a
rule.**

**A LINK, NOT A NARROWING.** The `REUSE_UNWIRED` collision has the same shape one level out —
**a rule whose SUBJECT excludes what it guards against, arriving as a RECORD whose FIELDS
exclude what a reading needs.** *Guard's subject* and *schema's expressiveness* are different
layers, and **the connection being exact is not evidence: two things having the same shape is
what a resemblance looks like from inside.** **Third instance before either is narrowed
against the other** — the same restraint the four-classes correction required this morning,
and the second time today it has been applied to a pattern proposed from a resemblance.

**A NINTH INSTANCE, AND IT IS A DIFFERENT AND MORE EXPENSIVE CLASS: A CORRECT CITATION
ATTACHED TO CODE THAT DOES THE OPPOSITE.** A6i is two meanings under one word. **This is one
meaning, cited accurately, implemented backwards** — `_bindings` quotes §16.5 and Figure 11
correctly and then **invents the list §16.5 forbids inventing**, ranking by variance while the
contact sensor sits unused.

> **The citation is what makes it expensive.** A wrong implementation with no citation reads
> as unfinished. **A wrong implementation with a right citation reads as DERIVED — and
> therefore as already checked.** It survived a session, a status of *built*, a filed report
> calling it *specified and needing no ruling*, and an owed-demonstration row that presupposed
> the mechanism existed.

**The tell is available and cheap: the cited clause is a claim about the CODE, so read the
clause and the code together, not the clause and the docstring.** *You do not invent the list*
is checkable in one line — `others = [s for s in self.slots if s != slot]` — and nobody looked,
**because the citation had already answered the question the reading would have asked.**

**AND TWO RULES ABOUT RULINGS, both of which earned their keep the day they were written:**

**A PARK MUST STATE A CHECKABLE TRIGGER, because a park exists to be correctly NOT lifted.**
`0a`'s said *an atom that consumes past index 0* — **which is a grep.** *Revisit later* is a
memory. **Today that specificity stopped an unpark Isaiah proposed and I would have agreed
with**: a real board arrived, the typing case fired, and *the domain has supplied it* was half
right. **A vague park would have been lifted on the strength of the half**, reviving a
mechanism whose measured 13×-for-zero-capability is still exactly true. **The rule is worth
having because the instance shows what a vague one costs.**

**A RULING WITH THREE SUPPORTS, ONE FALSE, LOAD CARRIED BY THE OTHER TWO, IS NOT A WRONG
RULING.** `0a`'s premise *Phase 3d replaces the atom set anyway* was false — `3d` was the rank
function. **Saying *the ruling was wrong* discards the 13× and the atom-count argument, both
still true and neither dependent on it.** And the qualifier that makes it fair: **nobody could
have known without running**, which is the **only kind of false premise that is not a failure
of checking** — and what distinguishes it from the seven wrong-pointer instances, all of which
were checkable in advance and were not checked.

**THE THIRD ONE, because its n is the whole question.** Two instances: `never_live` requires
`misses == 0` and therefore **cannot fire on the case it was named for** — *observed*; and
§11's entry discipline governs what enters **the library** while four of the five surviving
prior shapes never touch it — ***predicted***, read out of the text, not yet gone quiet
because `3a` has not run. **CLAUDE.md's seven laws were each found by a checker going quiet
ONCE, and none by reasoning about what a good checker should do** — so against that standard
this is **n = 1**, and the bar is a second *observed* instance.

**And it is a FOURTH failure in a family of three, which is why it is worth holding at all:**

| named already | what it is |
|---|---|
| **VACUOUS** | nothing to examine |
| **harness cannot go red** (`lint.py`) | *found nothing because the subject is clean* and *found nothing because the harness cannot reach it* produce identical output |
| **the seventh law** | a denominator **the mechanism moves** |
| **THIS** | **the rule is well-formed, the harness CAN reach it, the evaluation is correct — and the failure case is outside the rule's SUBJECT by construction** |

**It is the worst of the family because all three existing detectors report health.** There is
plenty to examine and none of it is the thing.

**Held is a status, not a weaker row.** Filing either early is the `type-match` move — a shape
that reads well, with nothing to check it against.

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

# PHASE 3's ORDER IS `3b` → `3c` + `3d` → `3a`, and §23.6 says so outright

**Sixth time the check has been applied, sixth thing it found — and this one the corpus states
in a numbered list rather than leaving to be derived.**

> §23.5: *Loading is not free. More atoms means a larger `λ`, so `λ^d` grows and a fixed budget
> covers a **smaller fraction** of the space — which shows up as coverage falling and, if
> nothing is done, **as more false `UNREACHED`**.*
>
> ***Loading generously therefore REQUIRES retrieval-by-characterised-residual, not
> enumeration.** A big library is an asset when you look things up by the shape of your gap
> and a liability when you walk it in registry order.*
>
> **Plan consequence: Phase 3c stops being optional.** *If the library is loaded heavily,
> retrieval AND THE RANK FUNCTION are prerequisites rather than improvements — **otherwise
> loading makes the agent WORSE by drowning every search**.*

**And §23.6 item 6 makes it explicit: *Phase 3c (retrieval + rank) is promoted to a
prerequisite of loading, not a follow-on.*** Note *and the rank function* — **`3d` moves
too.** The table's `3a → 3b → 3c → 3d` is wrong in three places at once.

**So `3a` is not blocked on one thing but on three**: the unrun priors path, the unwritten Cyc
pre-emption, and now **`3c` + `3d` as stated prerequisites.** *(`3c` and `3d` have since been
built, and the `3a` section check added a FOURTH that is not a code path at all — the ablation
scoping. See that section's closing.)* Which is consistent — *load
generously* is the item that makes every other cost worse, and it is listed first.

### And §23.6 item 4 is already built

*Report minted-fraction per solution — **the composer-vs-lookup number, free from the
stamps***. `minted_fraction` is already in the ladder's row keys, computed from the origin
stamps at `grade`. **Fifth instance today of work that exists and is filed elsewhere**, and
this one is a whole reporting item.

---

# `3b` — BUILT 2026-08-27. `λ < V` for the first time, and the falsifier stops firing

**`arc_atoms.py`: EXTRACT + RELATE + QUANTIFY, joined to whatever PREDICT the domain
supplies.** Measured side by side in one run:

    one space    lambda 3.0 = V 3.0,  1 type    <- the Stage 1 falsifier, firing
    three spaces lambda 3.0 < V 14.0, 4 types   advantage/depth 4.67

> **The falsifier that has fired for this project's entire life stops firing**, and §11.3
> called it exactly: *`λ = V = 7`, because every atom was `val → val` and the type graph was a
> single node ... **the instrument was working; it just had nothing to measure.***

### The machinery needed nothing new

**`enumerate_closure(in_type, out_type, ...)` was already type-directed and `Atom` already
carried `in_type`/`out_type`.** What was missing was an atom set whose types are not all
`val → val`. **A whole phase item turning out to be an atom set rather than a mechanism** —
fourth instance today of work that exists and is filed elsewhere.

> **AND THAT SAYS SOMETHING ABOUT THE PLAN'S UNIT.** `[I]`: **the tables list CAPABILITIES, and capabilities and mechanisms are not the same unit.** Three of the four times, **the mechanism was present and the capability was not** — the type-directed closure without varied types, the seven sensors without the item that lists them, the retro sweep without a level trigger. **So *is it built* is the wrong question to ask a row; *what does it still owe* is the right one**, and the two differ most where the mechanism is finished.

### And the graph connects, sparsely, in the right place

    OBJ  -> ATTR   colour, row, col                 the extractors
    OBJ  -> PRED   colour . same, colour . other    extract then relate
    OBJ  -> OBJ    colour . same . all              THE FULL CHAIN
    val  -> val    idn, inc, dbl                    PREDICT, separate
    ATTR -> val    0 found                          <- the sparsity is REAL

**`ATTR` does not reach `val`**, so a search in one space does not drown in the other — which
is *most primitives do not compose with most others*, measured rather than asserted. **And
`colour . same . all` is an `OBJ → OBJ` term: an objective that can be POSED**, which §11.2
says is impossible without extractors. Figure 3's link 2, unbroken.

### Two things it does not do, said rather than discovered later

**The extractors are `2b`'s sensors WRAPPED, not rewritten** — `colour`, `row`, `col`, `h`,
`w` come off the component dict `arc_percept.components` already builds, because a second
`position` would be the reinvention no grep can see.

**And operand TYPING is `0a`'s and stays parked.** `gamma` types an atom's input and output
and not its operand, so §11.2's `ATTR × ATTR → PRED` is expressed as `ATTR → PRED` with an
operand-reading atom. **The type GRAPH is what `λ` is computed over and it is sparse either
way — but the second argument's type is unchecked**, and saying so now is cheaper than
discovering it at `3c`.

---

# THE AGENT DIAGNOSES LINK 2, AND §11.2 PREDICTS LINK 2 — independently

**`demo.py`, measured:**

    stopped at link : 2 - vocabulary (measured: 1 slot(s) unreached at budget)

**§11.2, written before it:** *without extractors there are no attributes; without attributes
no predicates can be stated; without predicates no objective can be posed* — **Figure 3's
chain breaking at LINK 2, exactly where the figure says chains usually break, *because it
attracts the least attention and the fewest instruments*.**

> **These agree and neither is derived from the other.** The demo's link code is computed from
> the loop's own state — no slot owes, is anything bound, did anything settle — and reports
> the first link that fails. §11.2's claim comes from the composition spaces and the absence
> of `grid × object → ATTR`. **Two routes, one link.**

**Which is a stronger argument for taking `3b` first than the ordering was.** The ordering
says `3a` is unreadable without `λ`; this says **`3b` is work on the link the agent's own
instrument reports itself stopping at.** A self-report that agrees with an independent
prediction is the one case where the self-report carries weight — *a frame cannot score itself
with a quantity it produces*, and here the corroboration comes from outside the frame.

---

# `3b` CHECKED — two of §11.2's three statuses have moved since it was written

**§11.2 is `3b`'s real spec, and it is sharper than the Phase 3 table:**

| space | signature | §11.2 said | actually |
|---|---|---|---|
| **PREDICT** | `slot × action → slot` | built | **built** — `gamma.py`'s atoms |
| **RELATE / QUANTIFY** | `ATTR × ATTR → PRED → OBJ` | *`grammar.py` exists, **unwired*** | **WIRED FOR SPEAKING, NOT FOR SEARCHING** |
| **EXTRACT** | `grid × object → ATTR` | **missing** | **the extractors exist; the TYPING does not** |

**RELATE is not unwired.** `tether` imports `grammar` and `G.compose` has eleven call sites —
every action passes through a composed utterance or does not happen. **But the MINT enumerates
`gamma`'s closure only.** Grammar composes utterances; nothing composes over it as a SEARCH
SPACE. **A narrower gap than *unwired*, and a different fix.**

**And EXTRACT's extractors exist — they are `2b`'s sensors.** `colour`, `position`, `extent`,
`shape` are literally `OBJ → ATTR`; `components` is `FRAME → [OBJ]`. **What is missing is not
the computations but the TYPING** — they are Python functions, not typed atoms in a registry
the closure can compose over.

> **So `3b` is not three families built from scratch. It is one space to type, one space to
> join to the search, and one already there.** Which is the same shape as seven-of-nine: **the
> work exists and is filed where it was needed rather than where it is listed.** Third
> instance today.

**And §11.2 names the stake**: *without extractors there are no attributes; without attributes
no predicates can be stated; without predicates no objective can be posed* — **Figure 3's
chain, breaking at link 2, exactly where the figure says chains usually break, *because it
attracts the least attention and the fewest instruments*.**

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

# `3c` — BUILT 2026-08-27. `retrieval.py`, and the null it first read was the panel again

**§15.3 is `3c`'s spec and it is one sentence:** *the whole library is present and reachable;
**what you cannot do is ask for a primitive by name** — you get it by describing the gap it
fits.* Figure 9 supplies the procedure — ***matching is a one-pass check, not a search*** —
and §23.5 supplies the stake: a big library is *an asset when you look things up by the shape
of your gap and a liability when you walk it in registry order.*

**`_library_fit` was the registry walk, in those words.** It scored **every** library term
against the **whole** history and took the shortest that explained. Now the residual is
characterised, the library is ordered by how well each term's key fits that description, and
the first explainer wins.

### 1 · WHAT IS KEYED, AND THE HALF THAT DELIBERATELY IS NOT

§15.3 lists four keys. **Two are properties of a TERM and two are properties of its
BEHAVIOUR**, and only the first two are free:

| key | keyed here? | why |
|---|---|---|
| type signature | **yes** | read straight off `Atom.in_type / out_type` |
| arity | **yes** | `reads_operand`, against the gap's own counted arity |
| what varies / invariant | **no** | needs the term applied to the residual's frames |
| effect shape | **no** | same — *describe in effect terms* requires running it |

**Keying what is free and evaluating what is not IS the one-pass check.** Keying all four
would need every term evaluated to compute its key, which is the search §15.3 replaces —
**the mechanism would consume exactly the work it exists to save.**

### 2 · TWO THINGS IT DOES NOT DO, BOTH BECAUSE A CHECK ALREADY SAYS SO

**It materialises nothing.** `closure(Γ)` is generated and never stored (A1), and the REACH
rule exists to keep **one producer of reach**. So this indexes the **library**, which is
stored anyway, by a function computed on demand. **A stored index over the closure would be a
second producer of reach** — and the index already recorded that the A1 REACH check was built
first *to protect against a design the corpus never asked for*. It holds: `3c` did not want
one.

**It does not gate.** Retrieval **orders** and returns every name; a term scoring zero is
tried last, never dropped. This is `_cannot_pay`'s lesson reused verbatim — *filtering by what
a term ought to need lost a closing term* — and contact ranking's: **order, never exclude.**

**Length is the tie-break inside the habitat**, so MDL's preference is not overturned, only
**restricted to the habitat first**. Ordering by length alone is the registry walk; ordering
by fit alone would discard the one preference the bargain is built on.

### 3 · IT READ 3% AND THE 3% WAS THE PANEL

Measured against the implementation it replaced, on the demo, both running on every call:

    library-fit calls  27          SAME PICK  27 / 27          differing  none
    _explains evals -- registry walk 253  ·  retrieval 245  ·  work avoided 3%

**27/27 identical picks is the result that matters** — behaviour preserved exactly, nothing
excluded, which is the claim the no-gating design has to make good on.

**And 3% is not a null about retrieval.** The corollary fired before it could be read as one:
*before a null is read as a finding about a mechanism, state what property of the panel the
mechanism would need in order to show, and confirm the panel has it.* Retrieval discriminates
on **type signature**. The demo's library is **entirely `val → val` — one distinct signature,
one node in the type graph.** There is nothing to discriminate on, so it structurally cannot
show. On `3b`'s three spaces, which is the panel that has the property:

| library | terms | signatures | registry walk | retrieval |
|---|---|---|---|---|
| demo | 8 | **1** | 1 eval | 1 eval — *nothing to show* |
| three spaces | 19 | **4** | **11 evals** | **4** — one per habitat |

**One evaluation to reach the right habitat, for every signature.** That is §15.3's *one
lookup*, and the registry walk needs up to **five** for the same term — a gap that widens with
the library, which is exactly §23.5's asset-or-liability.

**This is the fourth time a null has been a fact about the world it was measured in**, and the
second time the world was *this repo's own demo*. **`3b`'s closing line predicted it in
advance** — *the instrument was working; it just had nothing to measure* — written about `λ`,
and now true word for word of retrieval. **Two mechanisms, one panel defect, one sentence
covering both.**

### 4 · IT IS NOT AN `arc_` MODULE, AND THAT WAS A CORRECTION

Built as `arc_index.py` and renamed to **`retrieval.py`** before wiring. Nothing in it is
ARC-specific — it keys on `Atom`'s own types — and `tether.py` is the **domain-agnostic**
loop. An `arc_` import there would have inverted the dependency and put a domain name in the
one file that must not have one. **The rename cost nothing at 3c and would have been
structural by Phase 5.**

---

# `3d` — BUILT 2026-08-27. The rank function, and TWO OF ITS THREE TERMS ARE INERT HERE

### 1 · THE SECTION CHECK MOVED THE BUILD BEFORE IT STARTED

**The row says four terms — *cost, reuse count, type-match to the residual, recency*. The spec
says three.** §17.7's interim fix is `(cost, reuse count, recency of the residual it last
closed)`, and **`type-match` appears nowhere in the corpus — only in the build-plan row.**

**And it is not a harmless extra.** `3c` shipped last turn ordering the library by type fit.
Adding type-match to the rank would **apply the same signal twice at two stages**: retrieval
selects the habitat, the rank orders *within* it. The row's fourth term is a reinvention of the
module built the turn before — **and on this panel it would have been silently constant**,
since there is one type node. The panel row written this session called this exact item.

**Two more things the section says and the row cannot:**

- **§18.7: a rank function is one of only TWO genuinely new builds in the document.** *Six of
  eight gaps had answers already written ... the two that are genuinely new build are the two
  the hunt came back empty on: **delayed effects, and a rank function.*** So the sixth law's
  *go look* returns nothing here — **which makes this the item where invention is most likely
  and least checkable**, and the reason the stated tuple is taken verbatim rather than improved.
- **§17.7: the trained proposer (§15.6) replaces this and *should not be waited for*.** Interim
  by instruction. Four fields, not a model. And §15.6 conditions that proposer on **the
  characterised residual from §15.3** — which is `3c`. The two builds are already joined.

### 2 · THE GATE ALREADY PASSES, SO THE GATE IS NOT THE DEMONSTRATION

§17.7: *the gate already requires every cut ranked and reversible, **so a rank function is
mandatory, not optional — and there isn't one.*** **It has been passing all along.** 300 cuts
across 25 rows, every one carrying `rank` and `reversible`. But `rank` is `rank += 1` — **the
enumeration position** — and the gate's test is `"rank" not in cut`, a **field-presence check**.
**Registry order satisfies the requirement that was meant to force a rank function into
existence.** A check that cannot distinguish a principled ordering from a counter.

*(Recorded because I first reported this check as vacuous. It is not — I queried the key `cut`
and the field is `cuts`. The corrected finding is sharper than the withdrawn one.)*

**So the falsifier is `candidates_tried`, which the ledger already records** — and the reading
is `3c`'s shape: **same terms minted, fewer candidates tried.** `enumerate_closure` breaks on
the first zero-residual term, so order decides how many are tried before it is found.

### 3 · IT RANKS UNITS, NOT CANDIDATES

**A minted candidate is by construction not in the library** — the novelty guard cuts the ones
that are — so its own reuse count is zero always and a rank over candidates is dead on arrival.
The objects with reuse histories are **the units the search composes from** (§14.2: *a settled
term re-enters the search as one unit*), so `units()` is ordered and every composition
downstream inherits it, at no per-candidate cost. `gamma.unit_rank` defaults to `None`, which
keeps the exact registry order — **installing a rank is an observable change and not installing
one changes nothing.**

### 4 · THE READING, AND WHY IT IS NOT A READING ABOUT THE RANK

    candidates_tried   registry 77,006   ranked 77,183   (+0.2%)
    terms minted       4                 4               SAME TERMS: True

**Same four terms — behaviour preserved.** And +0.2% is inert. **Two of the three terms cannot
act on this panel, each for a named reason:**

| term | live? | why |
|---|---|---|
| **cost** | yes | but BFS already approximates it, so it is nearly the order that was there |
| **reuse count** | **NO** | **the funnel never closes.** `reuse funnel: {'no-eligible-target': 4}`, ladder stage **`REUSE_UNWIRED`** — *implementation, loop not connected.* Every tracked unit reads `used == 1`, so `-used` is **constant** and orders nothing. Flat at 16, 40 and 80 cycles |
| **recency** | no | third key; only reached when cost AND reuse tie, and reuse never varies |

**Only cost is live, and cost was already approximated. That is the whole +0.2%.**

**AND THE DEMO HAS BEEN PRINTING THE REASON ON STDOUT THE WHOLE TIME.** `stage: REUSE_UNWIRED`
is in every run's output. The corollary's *read the things that produce conditions* has a
weaker sibling here: **this condition was not hidden in a generator or a config — it was in the
report**, and it still took a null reading to look at it.

### 5 · ONE WIRING DEFECT, FOUND BY THE PANEL CHECK RATHER THAN BY A TEST

First wiring noted reuse at the three `self.bound[slot] = …` sites. **A bind is once-per-term
by construction** — a rebind picks a *different* term, since `_library_fit` excludes the
incumbent — so `used` would have read `1` forever **and the flat 16/40/80 result would have
looked like a fact about the panel.** Worse, the funnel's `cross` branch (a term reused for a
*different* slot, which is the reuse §17.7 means) **never touches `bound` at all.** Now noted
where `note_reused()` fires, which is the funnel's own definition. **The reinvention rule: the
detector existed and I built a second one beside it.**

### 6 · WHAT IT OWES

**A panel where reuse fires** — same disposition as contact ranking and `never_live`, and now
the third item waiting on the same kind of thing. **Not a dead mechanism; an unexercised one**,
and the distinction is the one `R_T` needed too.

---

# `3a` CHECKED BEFORE ITS BLOCKERS CLEAR — and it is NOT one load into Γ

**Read before building, on the argument that if the section says something the row does not —
which it has every time — better to know before the blockers clear than after.** It does, five
times, and one of them is a defect in the corpus rather than in the row.

### 1 · THERE ARE EIGHT SHAPES, NOT SEVEN, AND EACH SECTION SHOWS A DIFFERENT SEVEN

**§23.2 opens *"the seven shapes from §12.1 sort cleanly"*. They are not the same seven.**

| | §12.1's seventh | §23.2's seventh |
|---|---|---|
| name | **ALREADY THE LOOP** | **ROUTINE** |
| what it says | *several catalogued priors ARE the architecture — adding them as library entries would **duplicate the loop inside the loop*** | *a routine is a solution, and **solutions are the thing that must not transfer in*** |
| appears in the other section? | **no** — `ROUTINE` occurs exactly once in the document, inside §23.2 | **no** — §12.1 never names it |

**Both tables have seven rows. Both look complete. Neither is.** And the two missing entries
are **both prohibitions, and each section carries only one of them** — so a builder working
from §23.2 alone never meets the duplication trap, and one working from §12.1 alone never
meets *never load a routine*, **which is the single most important rule in `3a`.**

**This is A6i at the level of a SET.** Not one word with two meanings — two sets under one
count, each internally coherent, each citing the other. **The check that finds it is reading
both, and nothing short of that would.**

### 2 · "ALL STAMPED `prior`" IS TRUE OF ONE SHAPE IN SIX

**§12.1 has a `lives in` column, and the row and §23.6 both read as though it says Γ:**

| shape | lives in | in Γ? |
|---|---|---|
| **TERM** | **Γ, stamped `prior`** | **yes — this one** |
| SENSOR | a typed registry | no |
| CONSTRAINT | a filter **before** the bargain | no |
| TRACKER | perception's identity rule | no |
| BIAS | search order, reversible | no |
| BUDGET | the constants block | no |

**So *Γ ships loaded* (§23.6 item 1) and *load generously across the six loadable shapes, all
stamped `prior`* (the row) both describe a single-destination operation, and the operation is
SIX LOADS INTO SIX HOMES, five of them outside Γ.** A stamp is a Γ concept; five of the six
cannot carry one. **`3a` is not a loading task with a provenance stamp on it — it is five
integrations plus one stamped load**, and the ablation clause reaches only the sixth.

### 3 · BIAS'S CONSUMER IS `3d`, BUILT TWO COMMITS AGO

§12.1: *a prior that reorders search is a cut ... **biases enter as ranked, reversible cuts or
they do not enter.*** **`3d` is that machinery**, and until two commits ago the BIAS shape had
nowhere to land. **The reordering got this right by accident** — `3a` moved last for §23.5's
reason (retrieval before loading), and the BIAS dependency is a second, independent reason for
the same order that neither the table nor §23.5 states.

### 4 · "LOAD GENEROUSLY" HAS A BOUNDARY THE ROW DOES NOT CARRY

§12.3, on the Tier 2 compositions — symmetry, containment, holes, counting-by-colour,
alignment: ***they are Tier 2 and the agent should have to reach for them, because reaching is
the only evidence the composition system works.***

> **Generous ACROSS the six shapes. Never across what composes from the nine.** Loading
> `symmetry` or `count` is not over-generosity — **it removes the evidence that the
> composition system works at all**, which is the thing `3a` exists to be graded on.

### 5 · `BUDGET` IS TWO QUANTITIES UNDER ONE WORD — CHECKED, AND CLEAR

**§12.1's BUDGET is *a number with provenance* in the constants block, and its examples are
`subitizing ≤ 4`, `relational complexity ~ 4`, `working-memory span`** — bounds on COGNITION.
**§22.1's is `MAX_ACTIONS`, the harness cap**, anchored to human play. **Same shape name,
different objects, and one of them is behind the second firewall.**

**No conflict: a subitizing bound is a fact about the world and is loadable; the harness cap is
the seat's and is not.** Recorded because `3a` is the only item that loads one of them, the
word does not distinguish them, and **A6i's two known instances both surfaced exactly where a
headline was about to be made.**

### 6 · THE NINE, CONFIRMED

`delta` (7) and `changed` (9) still owed; seven built under `2b`/`2c`. **§12.3's own list
matches what was filed under the other items** — no change.

### 7 · THE ABLATION CLAUSE REACHES ONE SHAPE IN SIX — a finding about a test that SHOULD NOT RUN YET

**RE-FILED 2026-08-27 as post-mastery, and the corpus already sequenced it that way.** The
clause reads *if **the win** survives* — **it takes the win as its subject**, so below mastery
it has no referent. Wipe the library at 3/25 and the result is 3/25 or lower, **uninterpretable
in both directions because there was nothing worth wiping.** *It wins* is clause 1; this is
clause 3. **No disagreement to surface: the corpus sequences it this way implicitly but
unambiguously**, and §11 says it from the other side — *you cannot tell a composer from a
lookup table*, which needs something composed.

**So everything below is TRUE AND NOT LIVE.** It is a defect in an instrument that should not
be run before 25/25, and **it needs to be right before 25/25 rather than before `3a`.** What
IS live from the same ruling is the **load side** — Tier 2 forbidden — which binds `3a` today
and is already implemented in `sensors.minimum_set()`.

**AND ONE PART OF THE DEFERRED HALF DOES NOT DEFER.** The partition is by *which clause
admitted a thing*, and §7 above shows the admitting clause is recorded nowhere. **It cannot be
reconstructed at 25/25 from a `prior` stamp**, so the field has to exist while entries are
happening. **The decision defers; the recording cannot** — the watermark's shape exactly.

**Terminal condition clause 3 is the sharpest one and the only runnable falsifier:** *back up
Γ, verify the backup, wipe Γ, re-run. If the win survives, the agent composed it; if it
disappears, the library was carrying the answer.*

**It wipes Γ. Only TERM lives in Γ.** So `SENSOR`, `CONSTRAINT`, `TRACKER`, `BIAS` and
`BUDGET` — **five of the six shapes `3a` loads generously — survive the wipe untouched**, and
the clause is silent about all five.

**The corpus already knows something can survive a wipe, and made that case honest.** §11's
**bench** is *primitives NOT in Γ that the agent cannot reach, entering only by an IMPORT
ceremony citing the residual it closes* — with a shadow-test gate, a Figure 6 debit, and
*every pull counted*. Its stated payoff is precisely this: ***wipe Γ and the bench remains, so
composed-it and was-handed-it stay distinguishable.***

> **The five shapes are a THIRD category the corpus does not have a name for: they survive,
> and unlike the bench they are uncounted, unceremonied, and loaded generously.**

**And §11's entry discipline misses them by its own scope.** *A prior enters **the library**
only if the loop cannot run without it, or the agent minted a crude version first ... because
the moment a prior enters for the second reason, we have encoded an answer, and **the ablation
clause will not be able to tell us we did**.* **Four of the five never touch the library**, so
the rule written to protect the ablation does not reach the shapes the ablation cannot see.

**THE COUNTERWEIGHT, WHICH IS REAL AND SHOULD BE VOLUNTEERED.** Some of what survives *should*
survive. **The nine minimum sensors are `loop cannot run without it` by construction** —
wiping them makes the agent blind rather than untaught, and a blind agent failing demonstrates
nothing. So the fix is **not** a wider wipe. The distinction that matters is inside the five:

| within the surviving five | should the ablation see it? |
|---|---|
| the **nine minimum sensors** — the loop cannot run without them | **no.** Wiping them tests blindness, not composition |
| **everything loaded beyond the nine** — Tier 2 reaches, CONSTRAINT, TRACKER, BIAS, BUDGET priors | **yes**, and it currently does not |

**So clause 3 measures *did the agent compose the TERMs*, not *did the agent compose*.** That
is narrower than the clause reads, and **`3a` is the item that widens the gap**, because
loading generously across five invisible shapes is exactly the operation the test cannot see.

**§12.3's Tier 2 rule is this same point from the other side** — *reaching is the only evidence
the composition system works* — so loading the composables and running the ablation would leave
**nothing demonstrating composition in either instrument.**

**AND THE CLAUSE NOW HAS THREE STATED DEPENDENCIES, TWO OF THEM THE CORPUS'S OWN.** §17.8:
*library persistence across levels and games is undecided, and **it is exactly what the
ablation clause tests** — that test only means something once persistence is a stated policy
rather than an accident of process lifetime.* §11: the entry discipline above. **This is the
third, and unlike the other two it is structural rather than undecided** — no policy fixes it,
because the shapes are in different homes by design.

### 8 · THE ABLATION SCOPING — RULED 2026-08-27, and it is a corpus scope error

**The ruling is a RE-SCOPING, not a new line.** §11 already states the entry rule; it is
scoped to *the library*; priors load into six homes and only TERM lives in Γ. **So four of
five shapes escape a rule whose stated purpose is the thing they escape** — a scope error in
the corpus, not a decision anyone had to make. **The rule binds all six homes.** What entered
under *cannot run without it* is what the ablation stays blind to; what entered under
*promoted from crude* is what it wipes.

| shape | entered under | ablation | note |
|---|---|---|---|
| **SENSOR** — the nine | cannot run without | **blind** | wiping tests blindness, not composition |
| **SENSOR** — beyond the nine | **neither** | **FORBIDDEN, not wiped** | **the ruling's real bite** — §12.3 requires these be REACHED, so the re-scoping does not decide their fate, it **forbids them**, and that directly constrains `3a`'s *load generously* |
| **TERM** | promoted, or prior | **wiped** | unchanged |
| **BIAS** | never necessary | **wiped** | safe: a reversible cut removes speed, not answers |
| **CONSTRAINT** | plausibility, not necessity | **wiped** | |
| **TRACKER** | cannot run without | **blind** | identity across frames is **perception, not knowledge** — and `2b` demonstrated it load-bearing by producing three defects in its absence |
| **BUDGET** | see below | **cognitive bounds wiped** | |

**AND `BUDGET` SPLIT CLEANLY, so one of the two open calls dissolved rather than being
decided.** §12.1's examples are `subitizing ≤ 4`, `relational complexity ~ 4`,
`working-memory span` — **all three are bounds on cognition.** The termination-bearing numbers
are `max_depth` and `budget` in `Config`: **seat-side, already anchored, already behind the
second firewall, and never one of the six shapes.** So *termination blind* is **vacuously
true** and needs no carve-out. **The `BUDGET` collision flagged in §5 as a hazard arrived as a
live consequence one ruling later** — the argument for having recorded it while it was clear.

**Written into `CLAUDE.md` under terminal-condition clause 3**, which is where §11 said to put
it — *a discipline to write into `CLAUDE.md` before any of it* — **and where it had never
been.** Second unwritten pre-emption in the Cyc class, and unlike Cyc it was load-bearing on a
ruling rather than on a reader.

**SEPARABLE AND RECORDED AS FOLLOWING: justified is not enumerable.** Re-scoping the entry rule
makes what survives **justified**; it does not make it **countable**. §11's bench ceremony —
recorded import, cited residual, every pull counted — is the answer to the second, and **the
ablation's own claim eventually needs it**: *composed-it and was-handed-it stay
distinguishable* requires knowing what was handed, and **a justified-but-uncounted survivor
cannot be reported.** Not now.

### WHAT THE CHECK CHANGES

**Not the two known blockers.** The unrun priors path and the unwritten Cyc pre-emption are
unmoved. **But §7 adds a third, and it is a different kind of thing** — not a code path and not
a missing sentence, but **a decision about what `3a`'s own falsifier can see.**

> **SETTLE THE ABLATION SCOPING BEFORE `3a` LOADS, NOT AFTER — and the argument is decisive on
> its own.** Afterwards the untested load is already in and the wipe still cannot see it.
> **There is no recovery position: you cannot retrospectively distinguish what was loaded from
> what was composed if the instrument never saw either.**

**And the line inside the five is what drawing it requires** — the nine the ablation should
stay blind to, versus everything loaded beyond them, which it should see. **Neither the
`derived`/`chosen` split nor §11's bench ceremony draws it, and nobody has.**

**So these are ONE item, not two: the scoping decision requires the line, and the line IS the
scoping decision.**
**What changes is what clearing them means**: `3a` was filed as *load Γ generously and stamp
it*, and it is **five integrations into five subsystems, one stamped Γ load, and a prohibition
that exists in only one of the two sections that define the taxonomy.**

---

# THE HOLDOUT AND THE HARDER WORLDS — CHECKED 2026-08-27, before either was ordered

### 1 · THE BLOCKER, NAMED — and it is the one item where doing the work destroys it

**It is not *an environment file*, and the engine is not the gap.** `arcengine` **is
installed** and exports `ARCBaseGame`, `Level`, `Sprite`, `Camera`, `FrameData`,
`GameAction`, `GameState`. **`arc_world.py` already imports the types.** The package ships
**no data directory and no game.** `ARCBaseGame` is an **ABC**; a game is a concrete subclass
supplying levels, sprites and win conditions.

> **THE BLOCKER IS AN AUTHORED GAME, AND IT MUST BE AUTHORED BY SOMEONE ELSE.**
>
> **The only item on the board that is not work — and the only one where doing the work
> destroys the thing it delivers.** *A fixture with a payable rule I designed tests my rule,
> not the ranking.* **All three owed validations fail identically if the board is ours**, so
> effort here is not merely useless but disqualifying.

**AND THE SPLIT IS CLEAN: THE BLOCKER IS DATA, NOT CODE.** Everything the holdout needs can be
**built**; none of it can be **run**. **Which unblocks Phase 5's bridge today** — `5b`'s
`MyAgent(Agent)` / `choose_action` is buildable and checkable against the engine's types with
no game present. **Not visible before the check, and it is a real unblocking rather than a
reordering.**

### 2 · PHASE 4 IS PARTLY UNGRADEABLE BEFORE THE HOLDOUT, NOT MERELY WORSE

**Two of five items are gated on measurements only a real board produces:**

| item | the gate | why the toy world cannot supply it |
|---|---|---|
| **4c** — Γ as simulator | depth gated by **measured** `sim_fidelity` | a measurement, not a setting |
| **4e** — level-reset as controlled experiment | **determinism** | *a property of the DOMAIN, not of the design* |

**That is a stronger claim than *cheaper to fail early*.** Phase 4 is not better after the
holdout; **it is partly ungradeable before it.**

### 3 · WHAT THE HOLDOUT DISCHARGES, AND THE HALF THAT STILL NEEDS A NUMBER

**Three owed validations — and one of them has since been WITHDRAWN rather than discharged:
contact ranking is not built, so it was never owed a demonstration.** As read at the time —
contact ranking,
`never_live`, and **`3d`'s reuse term**, inert on `snaps` because the funnel never closes.
Plus **the watermark**, which §*provenance* makes a line crossed by a commit rather than by a
decision, and which should be deliberate.

**And §22.6 splits into two halves of different readiness.** *Ratio is the alarm, stage is the
diagnosis, and without the stage code they are indistinguishable — which is how a wiring gap
gets written up as a theory failure.* **The diagnosis half is already live**: today's `3d`
read `REUSE_UNWIRED` off that ladder. **The alarm half needs `human_reference`** — a human
step count per level **that nobody has supplied.** So a holdout yields a diagnosis either way;
the ratio needs one more number, and it is not the game.

### 4 · HARDER WORLDS — CONFIRMED VERBATIM, AND THE RISK IS NOT AESTHETIC

**`SNAPS_PLAN` §2 confirms exactly**: five families, **three outside closure** (`lagged`,
`hidden`, `regime`), *the direct attack on the 42% false-mint rate* — they punish a term
fitted to a slice **that cannot contain the evidence that would refute it.**

**And the timing argument is corpus-backed.** `ARC_AGENT` §9: the agent must abstain when the
atom it needs is not in the closure, *which on ARC is **not planted but real, and therefore no
longer measurable against a known answer**. **That is a loss of measurement we should feel.***
**So the toy world is the only place false-abstention is measurable at all**, and
*don't become a small ARC* **protects the one measurement that does not survive the move** —
not a preference about panel quality.

**RE-PINNED: that clause is `ARC_AGENT` §9, NOT `SNAPS_PLAN` §9**, which is the exclusion
list. **Both documents have a §9, and the two citations sat one sentence apart.** **A bare
section number across two files is the A6i hazard class** — same shape, same day — and it is
worth fixing wherever a bare `§n` appears, not only here.

### 5 · ONE FREE FINDING FOR PHASE 5

**`5c` specifies the digest as ≤ 16 KB. `arcengine` exports `MAX_REASONING_BYTES = 16 * 1024`
and RAISES past it.** The numbers agree and nothing is broken — but **the constant has an
authoritative source, and `5c` should import it rather than restate it.** *One producer, at a
boundary the seat does not own.* The plan's own note is right — *test the boundary rather than
discover it in a scored run* — and **the failure mode is a crash, not a truncation.**

---

# `3a` — PART ONE BUILT 2026-08-27. Part two is blocked by yesterday's own ruling

### 1 · THE SEVEN "BUILT" SENSORS WERE BUILT AS FUNCTIONS

**`NOT_RESOLVED` did not occur anywhere in the repository.** §12.2 defines a sensor as a
dataclass with six fields and four properties — **typed output, total with an explicit
non-reading, composable, priced** — and the seven filed as BUILT under `2b`/`2c` had none of
the four. Plain functions returning `list`, `frozenset`, `float`, `bool`. **The fourth step
verbatim: the MECHANISM was present, the CAPABILITY was not, and *is it built* returned yes.**

### 2 · TOTALITY WAS A LIVE CONFABULATION PATH, ONE LEVEL BELOW WHERE ABSTENTION IS BUILT

§12.2: *never a guess, never a default ... it is what lets "this instrument cannot see it"
propagate up instead of becoming a wrong attribute.* **The chain that existed:**

    components(unreadable) -> []        asserts "there are no objects"
    Objects(...)           -> {}        no slots
    ArcWorld._decomposed   -> {}        `{} if b is None else ...`
    the loop               -> no slots, no residual, CLEAN BILL OF HEALTH

**A blind instrument reporting a healthy world** — which is the exact failure the whole
architecture exists to prevent, running one level below where it is implemented. **`blind` is
now a reading and an empty dict is a guess**, and the two are separated at the world boundary.

### 3 · THE NINE EXIST, AND TWO OF THEM WERE OWED

`sensors.py`: `Sensor`, `NOT_RESOLVED` as a falsey singleton, a typed `Registry`, and
§12.3's nine wrapped around `arc_percept` — **never reimplemented.** **`delta` (7) and
`changed` (9) were the two owed since `2b`** and are built. **Tier 2 is deliberately absent**,
which the 2026-08-27 ruling makes *forbidden* rather than merely ungenerous.

**THE PRICE IS DECLARED WITHOUT A UNIT, AND THAT IS SAID RATHER THAN PAPERED OVER.** §12.2
gives `cost: int` and the bargain *a sensor that costs more than the residual it resolves is
not worth having* — but **a residual is in BITS and a sensor's cost is READS, and the corpus
never gives the conversion.** So `cost` is reads-per-call, countable from the signature, and
**the sensor bargain must not be run until the unit is settled.** Inventing a bits-like number
would be the magic number; comparing the two would be the seventh law's error one level down.

### 4 · THREE THINGS THE BUILD ITSELF FOUND

**The registry's type-directed lookup has NO CONSUMER, and lint said so on the first pass.**
`producing()` / `accepting()` are what make a registry more than a dict — **and nothing
composes sensors yet**, because the decomposition arrives as one injected callable. They
belong with §12.4. **Not shipped**, on *never ship half a mechanism*; the ISOLATED rule caught
it before the commit.

**The obvious wiring was a circular import.** `sensors` wraps `arc_percept`, so `arc_percept`
cannot read back through it. **The consumer had to be `arc_world`**, which sits above both —
and that is the correct layer anyway, since the world owns the frame.

**AND THE FIRST GUARD MANUFACTURED A FALSE ABSTENTION.** It tested `isinstance(frame, list)`;
**boards arrive as `ndarray`**, so a perfectly readable board reported BLIND and the fixture
died with an empty slot set. **A totality guard that is too strict is the same defect as one
too loose, in the opposite direction** — and `ARC_BUILD_PLAN` already names it for filters:
*manufactures false abstentions.* Now duck-typed: **the question is whether the instrument can
see, not what the frame is made of.** Caught by the fixture on the first run.

### 5 · THE CYC PRE-EMPTION — WRITTEN, and there was no README at all

`README.md` did not exist. Q3's line is now in it, with the distinction made checkable rather
than asserted: **Cyc's predicates were correct when their authors agreed; there was no arbiter
that could return a verdict they had not anticipated.** Here the arbiter is fixed before the
agent starts and returns the same verdict regardless of what the library says.

### 6b · PART TWO — RULED AND BUILT. *Visible, not held*, and it dissolves the conflict

**The ruling: a TERM may be VISIBLE without being HELD.** All possible priors exist already;
an organism does not compose its priors, it inherits them and expresses what the environment
triggers. **The seed needs ACCESS to everything, because the terrain and the pressure are
unknown and reactivity is the point — but access is not possession**, and that is the
distinction §11 and §23.2 were both reaching for with one word.

**§11 IS UNTOUCHED. §23.2's *load generously* becomes *populate the visible set generously*.**
Visibility is not entry, so there is no third clause and no weakening.

**AND IT CORRECTS YESTERDAY'S RE-SCOPING.** I called §11's library scope *a scope error rather
than a decision* and bound it to all six homes. **That was the error.** Entering means
entering Γ; the five non-Γ homes are **populated**, not entered. **Two tests, two questions:**
§23.2's *what to look at vs what to do* governs loading the five; §11's two clauses govern
entry into Γ. **And yesterday's *TERM wiped* becomes vacuous** — nothing unearned is in Γ to
wipe, which is the ruling's *the ablation problem shrinks rather than being managed.*

**NOT CALLED A CATALOGUE, AND THAT WAS A FIFTH A6i CATCH.** §14.7 uses `catalogue` for the
FAILURE: *a library that grows and is never reused is a catalogue, and a catalogue is what
"the agent is composing" looks like when it is not* — the metric it puts on the wall, with
zero reuse as *the failure signature that would otherwise look like progress*. **The two are
structural opposites**: §14.7's is HELD BUT NEVER USED inside Γ; this is VISIBLE BUT NEVER
HELD outside it. **The ruling prevents the failure its original name described**, and *load
TERM into the catalogue* would have read as the failure mode endorsed. **`the visible set`**
— `seed` was rejected on the ruling's own logic: a seed becomes the thing, and this is what
the agent can see and has not grown.

| an entry carries | and deliberately omits |
|---|---|
| `kind` · `affordance` (what it WOULD do) · `provenance` · `holders` | **the composition, the atom chain, the parameters, the implementation** |

**AIM** adopts the affordance predicates as a goal hypothesis — *the agent sees a capability
exists and what it would do, and cannot execute it.* **EARN** is regenerating the pattern
under ablation, and it then enters **under §11 clause two, `promoted`** — which the
admitting-clause field records, built one commit earlier for a different reason.

### 6b-ii · THE CORRECTION, APPLIED AT THE SITE — and it closed a trapdoor

**`CLAUDE.md`'s entry was written as a re-scoping and is not one any more**, so it is
corrected in place rather than annotated — the working-document treatment, so the next reader
meets the correction instead of the error. **Most of yesterday's ruling survives**: the load
side still binds, SENSORs beyond the nine are still forbidden, the shape-by-shape dispositions
still hold. **What goes is the re-scoping itself, and with it *TERM wiped*.**

**AND THE CORRECTION HAD A CONSEQUENCE IN CODE.** `Gamma.__init__` took a `molecules`
parameter that installed TERM priors at construction with `origin=PRIOR` — **the one route by
which a term could enter Γ without being earned.** It had **zero call sites**, which had been
filed as *the unrun priors path* and `3a`'s first blocker.

> **It was not dormant. It was a trapdoor to a state the ruling forbids** — and leaving it
> would have made `admissions` report a bucket that must never be populated. **Removed.**

**`unstated` therefore changes meaning: it is now a FALSIFIER, not a population.** Before the
ruling it meant *no clause recorded*; now the only ways into Γ are `necessary` (the atoms) and
`promoted` (earned), so **a non-zero `unstated` means something entered by a route that should
not exist.** Kept so it can be checked rather than assumed. Reads `{'necessary': 8}`.

**And it retires half of `molecule`'s A6i collision** — the first of the two named instances,
*a prior term in `gamma` and a quantified objective in `DISCOVERY` Q21.* **The `gamma` sense
no longer exists.**

### 6c · THE LOAD — 17 ROWS, ALL CITED, AND NONE CHOSEN FOR USEFULNESS

`priors.py`, from `ARC_HUMAN_PRIORS.md`: **CONSTRAINT 5 · TRACKER 4 · BIAS 4 · BUDGET 4.**
`visible.py` makes all 17 visible and holds none. **Every row cites a catalogue line**, and
the only question asked of each was *which shape is this, and does §23.2 admit it* — **never
*is this useful*, which is the move that encodes an answer and is indistinguishable from a
real prior afterwards.**

**DELIBERATELY ABSENT**: the catalogue's problem-solving and analogical rows are mostly
**ROUTINE** — means-ends analysis, goal decomposition, backward chaining are *what to do* —
and the meta-learning rows are **ALREADY THE LOOP**, which §12.1 says would *duplicate the
loop inside the loop*. **BUDGET is cognitive bounds only** (subitizing 4, relational
complexity 4, focus 4, span 7); the termination caps stay seat-side, per the third A6i
instance.

**UNVERIFIED AGAINST ITS SOURCE, AND SAID IN THE MODULE.** The four entry fields are the
ruling's. **The earlier architecture material specifying this structure is not in `docs/` and
was not read**, so anything it adds beyond the four is unchecked here rather than
contradicted.

**One defect the build produced:** `Γ` in a **runtime** string killed the fixture on the
Windows console's cp1252. Docstrings are never printed and are fine; **strings that reach
stdout are not.** Fixed, and worth knowing before Phase 5 emits a digest.

### 6 · WHAT PART TWO WAS BLOCKED ON, BEFORE THE RULING

**Two findings, and the second is the blocker.**

**Q3 flags the payload as unspecified**, in the corpus's own words: ***"Still needs answering:
what molecules does the rover start with, concretely?"*** So the priors path is not merely
unrun — **nobody has said what it loads.**

**And the entry rule appears to forbid the load.** Yesterday's ruling binds §11 to all six
homes, and was explicitly used to **forbid** SENSORs beyond the nine — so it constrains ENTRY,
not only ablation scope. Applied to TERM:

| clause | does a TERM prior at start qualify? |
|---|---|
| *the loop cannot run without it* | **no** — the loop mints its own terms |
| *the agent minted a crude version first and we are promoting it* | **no** — nothing is minted at start |

> **So no TERM prior can be loaded at start under the rule as written — and that is `3a`'s
> headline operation and §23.6 item 1's *Γ ships loaded*.**

**§23.2 permits exactly what §11 forbids.** They are two different entry tests: §23.2 asks
*does it name what to look at, or what to do*; §11 asks *cannot-run-without / promoted-from-
crude / never because it would help.* **§11 is strictly stronger, and yesterday's ruling
adopted it.** **This is a doctrine conflict revealed by the ruling rather than created by it**
— and it is Isaiah's to resolve, because deciding it here would be picking which of two corpus
rules governs.

### 7 · THE `PRIOR` COLLISION — and it makes yesterday's ruling UNIMPLEMENTABLE as written

**Three usages, at three scales.** `gamma.PRIOR` is an **origin stamp**, and **every atom
receives it at construction** — so it means *no mint record*, a provenance default. §11's
`prior` is **a category admitted under an entry rule**. And §12.1's title is the corpus saying
so outright: ***a prior is not one kind of thing, so it cannot have one code shape.***

> **The stamp is not evidence the rule was applied.** `3a`'s *all stamped `prior`* invites
> exactly that reading, and `gamma` stamps things that never faced an entry test.

**AND HERE IS THE CONSEQUENCE.** Yesterday's ruling partitions by **which clause admitted a
thing** — *what entered under `cannot run without it` is what the ablation stays blind to;
what entered under `promoted from crude` is what it wipes.* **Nothing records the clause.**
`stamps[name]` carries `origin`, `seq` and `residual`; **the admitting clause is nowhere**, so
the partition cannot be computed and **the ruling is unimplementable as written.**

**This is not a defect in the ruling — it is a missing field**, and the same shape as the
four-value `provenance` that was added for mechanisms when a citation turned out not to prove
derivation. **The fix is one field recording which clause admitted an entry.** Stated, not
taken: adding it decides how the ablation partitions, which is Isaiah's.

### 7b · THE ADMITTING CLAUSE IS NOW RECORDED — the input, not the decision

**The split is one level finer than *record vs decide*, and that is what made it takeable.**
*Which clause admitted this* is **a fact about the entry**; *what each clause implies for the
wipe* is the deferred decision. **The field records the first and presupposes nothing about
the second.**

**§11's enumeration is clean, which is the condition that had to hold.** Exactly two admitting
clauses; the bench's IMPORT ceremony is a separate route **already carried by
`origin=IMPORTED`**; so the missing distinction lives only *within* `origin=PRIOR`. **And
there is no judgement in the classification** — `promoted` is checkable, because a mint record
for the crude version exists, and `necessary` is **inherited from §12.3's stated criterion**
rather than decided per entry.

`gamma`: `NECESSARY` / `PROMOTED`, on `stamps`, reported through the ledger as `admissions`.
**Atoms are `necessary`** — the loop cannot run without a vocabulary. **Molecules load with
`None`, and that is deliberate**: no clause is stated for them, `unstated` is the honest
reading and **the population to examine**, which is `unattributed`'s disposition exactly.
Demo reads `{'necessary': 8}`.

**Taken now because it is unrecoverable later** — a `prior` stamp at 25/25 cannot be
back-classified, so the deferred half would have become unrunnable against its own subject.

### 8 · `3a` AND THE HOLDOUT ARE COUPLED, AND THE PLAN SHOWS THEM APART

**`3a` is where the false-abstention population arrives.** Loading raises `λ`, `λ^d` grows,
coverage falls, and **false `UNREACHED` multiplies** — §23.5's whole argument for `3c` being a
prerequisite rather than a follow-on.

**And `never_live` is the detector whose subject is empty here.** Its two premises were
corrected; its subject is not, because the panel has no walls.

> **So `3a` widens a failure mode whose detector only fires on a board nobody has, and the
> first place the population and the detector exist together is THE HOLDOUT.**

**The plan lists them in different phases with no dependency drawn.** Recorded because it is
the kind of coupling that is invisible in a table and obvious in a run.

---

# STEP 7 OUTWARD AND THE PEER CHANNEL — mostly already recorded. NOT BUILDING TOWARD IT

**Checked, and the corpus carries more of this than the note assumed.** `ARC_AGENT` §13:

- **Figure 6 names three external sources** — *nature · corpus · peer frame* — and the
  corrected reading is recorded: *"I have been writing that a lone agent has no IMPORT channel
  — Mars, no peer frame, step 7 OUTWARD closed. **Figure 6 does not say that.**"*
- **Three channels the environment actually imports through**: action-set growth (**yes** —
  atoms, the closure expands), value-domain growth (**yes**), instrument extension
  (**inward**, not import).
- **And the game-is-nature-not-a-peer clause is there verbatim**: *the game is not a peer
  frame in Figure 8's sense: **you cannot read its closure, only its outputs**, so there is no
  union surplus to search and no triangulation. **That channel is what a swarm would open**,
  and it is the honest reason swarms are on the roadmap rather than a nicety.*
- **`low ρ` is present too**, in the breeder's-equation form — *low ρ between rooms; the next
  room is picked against the residual the last one surfaced* — **about room-to-room handoffs,
  not about two frames meeting.**

**WHAT IS NOT RECORDED, and is filed here as NOT A RULING AND NOT TO BE BUILT TOWARD:**
frames meeting frames as an **interface-construction** problem; **low ρ paired against high
ρ** rather than as a handoff property; and **systemic forensics** — *how did this terrain
form, what are the rules of engagement, what are the conditions of agreement.*

**Filed, not scheduled.** The corpus already routes the peer channel to the swarm, and the
game supplies nature instead — so nothing here changes what is built next.

---

# THE FIRST HOLDOUT — `ls20`, 2026-08-27, and the chain stops where the toy world stops

**THE BLOCKER WAS NEVER *NOBODY HAS A GAME*.** `arcengine` ships no games — that finding held.
**But `arc_agi`, the CLIENT, was installed the whole time**, and `make()` dispatches
`NORMAL → "download game and run locally" → LocalEnvironmentWrapper`. **Get-it-from-the-API
and play-locally-fast are ONE path.** I checked the engine and stopped; the client was one
directory over. **The session's own genus, once more.**

### 1 · THE RUN

Anonymous key (`/api/games/anonkey`, no registration), **25 environments visible**, `ls20`
downloaded at version `9607627b`, played through `LocalEnvironmentWrapper`. **Pre-watermark
atoms only** — the three-atom plumbing set authored before any game existed, so **provably not
fitted to `ls20`.** ARC's real PREDICT atoms **do not exist**: `arc_check` says they *arrive at
3d*, and `3d` delivered the rank function.

    board 64x64, palette 13 READ FROM THE FRAME     100 object slots, blind=False
    40 cycles, 8,940 ledger rows, GATE: PASS        1 mint, verdict `pays`, 1 accept, 1 rebind
    229 parks, 6 slots owed, 0 advances, 0 capped   admissions {necessary: 3}

**Perception worked on a real board.** 100 slots from a 64×64 grid, `blind` false, the palette
read rather than assumed. **The gate passes on a real run.**

### 2 · WHERE THE CHAIN STOPS — `REUSE_UNWIRED`, and it is a WIRING verdict

    stalls (closed segments)  {REUSE_UNWIRED: 1}        last_stage  REUSE_UNWIRED
    reuse funnel              {no-eligible-target: 1}

**§22.6 is the whole reason this is readable**: *ratio is the alarm, stage is the diagnosis,
and without the stage code they are indistinguishable — which is how a **wiring gap gets
written up as a theory failure.*** `REUSE_UNWIRED` is *implementation, loop not connected*.
**The same rung as the toy world, reached on a real board** — which makes it a fact about the
loop rather than about `snaps`.

**AND I NEARLY PUBLISHED THE WRONG ONE.** `chain.seg.stage()` read **`DIED_PRE_DIFF`** — a
dramatic headline and false. `seg` is the **currently open** segment; a fresh one has
`diff_ran=False` by construction. **The instrument is `stalls`, *which link breaks as a
measured distribution*, over CLOSED segments.** A live snapshot and a measured distribution are
different objects, and `note_diff` fires every step, which is what made the reading impossible
rather than merely surprising.

### 3 · THE THREE OWED VALIDATIONS — none demonstrated, and their statuses now DIFFER

| owed | status after `ls20` |
|---|---|
| **`never_live`** | **its SUBJECT now exists.** All four actions tried at **10 distinct states each** — the toy world could not supply that. **No action is never-live, because all four stayed available for 40 cycles.** A real null with a real subject, which is a different object from the empty-subject null |
| **contact ranking** | **WITHDRAWN AS AN OWED GREEN — it is NOT BUILT.** The run was to be its demonstration; reading the code for §16.5 showed there is nothing to demonstrate. `_bindings` takes **every other slot** and ranks by **variance**, with `touching()` built and unused. **A demonstration was never what it was owed** — it was owed the mechanism it is named after |
| **the rank function's reuse term** | **unchanged.** Funnel attempted once, `no-eligible-target`. **The second panel defect is not a `snaps` defect** — it reproduces on `ls20` |

**Two of the three moved from *unexercisable* to *exercised and null*, which is progress of a
kind the plan did not distinguish.** The third did not move at all, and **that is now a finding
about the mechanism rather than about the panel.**

### 3b · THE FIREWALL BREACHED IN THE TOOLING, FIRST THING, AND GITIGNORE WAS NOT ENOUGH

**The download put `ls20.py` under `environment_files/`, and `conform/lint.py` walks the
FILESYSTEM rather than git.** So the first thing that happened after the run was **the linter
reading the game's source and printing its constants and function names into the seat's
view.**

> **Two exclusion mechanisms, and only one had been done.** Gitignoring keeps content out of
> **commits**; it does nothing about tools that `rglob` the tree. **`ruff` happens to be
> gitignore-aware and excluded it unasked, which is why exactly one checker surfaced it** —
> the other would have gone on reading it silently.

**Game source is CONTENT, not harness.** *The seat may read the harness* does not reach it.
Fixed at source; `environment_files` and `recordings` now skip alongside `.venv` and `runs`.
**And the shape is the day's shape again: I did the half I was thinking about and not the half
I was not.**

**WHAT IS CONTAMINATED AND WHAT IS NOT, stated rather than left at *breached*:**

| | |
|---|---|
| **seen** | two constants (a background and a padding colour) and three function names, in lint output |
| **NOT seen** | any rule, level, objective, transition or solution. The linter reports shapes, not behaviour |
| **the agent** | **read none of it.** The breach is in a checker that runs beside the loop, not in the loop |
| **entered a brief, the library, the priors, the grammar or a decision** | **nothing** |

**AND THE CONTAINMENT IS CHECKABLE RATHER THAN PROMISED.** The one leaked constant that could
conceivably matter is a background colour — **and `arc_percept` refuses the concept outright,
in text written before any game existed**: *NO BACKGROUND COLOUR. Every same-symbol region is
a component, INCLUDING colour 0. **Treating 0 as background is domain knowledge about what a
board means, and this file is not entitled to it.*** `components(board)` takes **one
argument**. **There is no parameter for it to have entered**, and that refusal is
pre-watermark, so `git blame` settles it rather than my memory.

### 4 · WHAT THE RUN SAYS IS MISSING

**One mint in 40 cycles over 100 slots, and 229 parks.** The atoms are arithmetic on slot
values; the domain's operators are grid transforms. **The plumbing set is the honest thing to
have run** — authoring grid atoms with a game present is the encoded-answer path — **and the
stopping point is the argument for building them deliberately, pre-registered, rather than the
excuse for skipping the step.**

---

# ARC'S PREDICT ATOMS DO NOT EXIST — and the plan points at the wrong item for the SIXTH time

**`arc_check` says it plainly and nobody read it as a debt:** *"ARC's real atom set is grid
transforms and arrives at 3d; these three are a plumbing set and nothing is read off them."*
**`3d` delivered the rank function.** `arc_atoms.three_spaces(predict)` takes PREDICT as an
argument *because inventing one there would be that file choosing what the agent may bet on* —
and **no caller has ever supplied one.** The holdout ran on `idn · inc · act`: arithmetic on
slot values, against a domain whose operators are grid transforms.

**SIXTH INSTANCE OF THE PLAN NAMING THE WRONG ITEM**, and the list is checkable:

| # | the plan said | it was |
|---|---|---|
| 1 | `2b`'s detector is `never_live` | `R_T` |
| 2 | build tables order phases | they group by **cost**; dependency falls out of neither |
| 3 | `3a → 3b → 3c → 3d` | **reversed** — §23.5 makes `3c` a prerequisite |
| 4 | `3d` ranks on four terms incl. `type-match` | §17.7's tuple has **three**, and the fourth double-applies `3c` |
| 5 | "the seven shapes from §12.1" | **eight**, as two tables of seven |
| 6 | **PREDICT atoms arrive at `3d`** | **`3d` was the rank function. They do not exist** |

**AND THE STOPPING POINT IS THE ARGUMENT FOR BUILDING THEM DELIBERATELY, NOT THE EXCUSE FOR
SKIPPING THE STEP.** Authoring grid atoms *now*, with `ls20` downloaded and a stall to explain,
is **the encoded-answer path wearing a diagnosis's clothes** — the fix that helps one case. They
should be pre-registered against the corpus and authored from it, the way the nine sensors were,
**and the run that motivated them is exactly why that has to be deliberate.**

---

# ARC'S PREDICT ATOMS — DERIVED AND PRE-REGISTERED 2026-08-27. Two of six, and both bind

**A LOOKUP, NOT A DESIGN.** `ARC_AGENT`'s eight-member table names them: *grid transforms:
**translate, recolour, reflect, rotate, appear, vanish***. The sixth law again — the set was
specified and the plan pointed at `3d`.

### 1 · FOUR OF THE SIX CANNOT BE EXPRESSED, AND THE GAP IS IN `Ctx`

An atom is `val × action × operands → val` **for one slot**, and a slot is one int.

| | | |
|---|---|---|
| **translate** | ✓ | `v + operand` |
| **recolour** | ✓ | `v → operand` |
| **appear · vanish** | ✗ | **existence is not a slot VALUE.** The slot SET changes, and `_present` already sees it — an event, not a transform |
| **reflect** | ✗ | needs the **board extent**; `Ctx` carries only `action` and other slots' values, and **the board is not a slot** |
| **rotate** | ✗ | **couples row and col**, and an atom returns one slot's value |

**Reported, never substituted.** *A `reflect` that quietly reflected about the object's own box
would be a different operator wearing the corpus's word, and it would have passed every check.*
**And neither delta is chosen**: both read an OPERAND, following `take`'s pattern, so the step
size and the target colour are **discovered by binding** — a `translate` hardcoded to `+1`
would be this file choosing the world's step size.

**A THIRD ATOM WAS FORCED BY THE LOOP, NOT CHOSEN: `idn`.** `_predict` falls back to
`self.bound.get(slot, IDN)`, so **a Γ without an identity raises `KeyError` on the first
unbound slot** — which is exactly what the first run did. *The loop cannot run without it* in
the most literal available sense, so it enters under §11 clause one. **Every working atom set
in the repo already had one and none said why**, which is how the omission survived into a
named six-atom list.

### 2 · PRE-REGISTERED BEFORE THE RUN, AND BOTH HELD

| # | registered | read |
|---|---|---|
| 1 | **`λ < V`** — Stage D: *here the type graph is genuinely sparse, so the number should mean something* | **HELD** — recorded as *λ 3.0 vs V 14*, ⚠ **and 3.0 was wrong**: `type_report` used unshifted power iteration, which does not converge on the cyclic type graph. **True λ = 3.5569**, corrected 2026-08-28. **`λ < V` holds either way** and the conclusion is unchanged |
| 2 | **both atoms must BIND**, or they are not part of the world's vocabulary | **translate 3 · recolour 4**, across 7 bound slots. **HELD** |
| 3 | **no claim about mint count** — the stall was `REUSE_UNWIRED` and these atoms do not touch reuse | mints **1 → 7**, all `pays`; library 4 → 21; parks 229 → 192 |

**ROW 3 IS AN OBSERVATION AND NOT A VINDICATION, and the distinction is the point of having
written it down first.** No prediction was made, so none was confirmed. **And the stall did
NOT move — still `REUSE_UNWIRED`, funnel `no-eligible-target` seven times instead of one.**
More mints, same wall: *a game showing you something is broken is legitimate; a game telling
you what to build is not*, and the build was derived from the corpus before the run rather
than from the run.

### 3 · `0a` ARRIVES AS A LIVE CONSEQUENCE

The minted terms are readable: `idn . translate<o12.col>` · `idn . recolour<o17.colour>` ·
**`idn . recolour<o11.h>`**. **Every atom is `val → val`, so nothing stops a colour operator
binding a height as its operand.** `arc_atoms` flagged this when it was written — *operand
TYPING is `0a`'s and is parked; `gamma` types an atom's input and output and not its operand*
— **and it is now visible in real bindings rather than as a caveat.** The type graph has four
nodes and the ATTRIBUTE type has none.

### 3b · THE RUNNER MOVED INTO THE REPO, BECAUSE LINT REFUSED THE ALTERNATIVE

**`arc_predict` was isolated and the commit was blocked.** The runner lived in a scratch file,
so nothing in the package imported the atoms. **`arc_holdout.py` is the consumer**, seat-side,
and the refusal was right for a second reason the rule does not state: **a run reported from a
scratch file is not reproducible, and this is the project's first real reading.**

**Not run by `conform/check.py`** — it needs the network and downloads content, and the
checkers stay offline and deterministic. **A game IDENTIFIER is a public name and is in the
file; no mechanics are**, and `environment_files/` is gitignored **and** linter-excluded.

### 3c · `0a`'s UNPARK CONDITION FIRED FOR ONE HALF AND NOT THE OTHER

**The park ruling names its own trigger:** *neither half until **Phase 2 says what an
interaction looks like on a real board**.* A real board now exists and has produced real
bindings — **so the trigger is checkable rather than a matter of judgement, and it splits.**

| half | fired? | evidence |
|---|---|---|
| **operand TYPING** | **YES** | `idn . recolour<o11.h>` — a **height** bound as a colour operator's operand. `gamma` types an atom's input and output **and not its operand**, so nothing refused it. **The parked decision produced exactly the defect it predicted, on a real board** |
| **operand ARITY** (N-ary) | **NO** | the ruling's condition was *an atom that consumes past index 0*. **`translate` and `recolour` both read `operands[0]`.** Grepped: **nothing in the repo reads index 1.** So the measured **13× for zero capability** still stands, unchanged |

**The domain supplied the typing case and not the arity case**, and conflating them would
unpark a mechanism whose own cost argument is still exactly true.

**AND THE PARK RULING LEANED ON THE WRONG-POINTER BUG ITSELF.** One of its reasons was
*Phase 3d replaces the atom set with grid transforms anyway, so a toy-world operand-1 atom is
scaffolding for a panel that gets replaced.* **`3d` was the rank function; the atoms arrived
at `3a` and had to be derived from the corpus by hand.** **The seventh instance of the plan
naming the wrong item, and this one is inside a ruling that used it as a premise** — the
conclusion survives on its other reasons, and the premise did not.

### 4 · THE COUNT IS NOT A MEASUREMENT

**Six was a list; two is what the signature admits; neither is derived from the environment.**
`ARC_BUILD_PLAN`: Ashby's inequality gives `closure(Γ)` *a lower bound the environment imposes
rather than one the designer picks* — **and nothing computes it.** Stated so the number is not
mistaken for a reading.

---

# THE GAP UNDER THE GAP — reported, not built. **ONE absence, and the corpus already filed it**

### 1 · WHAT PATH EXISTS TODAY: exactly one, and it structurally cannot carry structure

    perceive() -> predict per BOUND SLOT -> compare -> SlotResidual

**That is the only route.** And **a slot is one int** — `{obj}.row | .col | .h | .w |
.colour`. **So structure enters only by BECOMING a slot**, and a relation between two objects
is never a slot. **Contains, touches, blocks, supports, occludes cannot be bet on, so they
cannot be wrong, so they cannot produce a residual.** Not a missing feature — a closed door.

**And the structural sensors mostly feed nothing:**

| sensor | where it goes |
|---|---|
| `components` · `shape` · `overlap` | the decomposition → slots → bets. **The only structure that reaches the loop, and only by becoming a value** |
| **`touching` (sensor 8)** | **NOWHERE.** Built at `2b`, computed, **never consulted by any decision** |
| `Affordances` (sensor 4) | **the fixture's display only** |
| `Preconditions` · `Agency` | in the loop — but they feed the control-mode and gating reads, **not the residual** |

### 2 · THE CORPUS ALREADY FILED IT AS ONE ABSENCE — and as THREE findings, not two

**`ARC_AGENT` §16.5, *Habitat enumeration as an operation the agent runs*, citing Figure 11:**

> *List everything in contact with the residual, then what is in contact with those, and
> outward until the cascade stops mattering. **You do not invent the list. You read it off the
> world**, and **what you cannot perceive or measure yet is the residual.***

**`ARC_BUILD_PLAN` already wrote the unification, and it names THREE:** *§16.5 is one mechanism
answering three separate findings* — **the operand binding** (§17.1's *the slot that owes plus
whatever is in contact with it*), **B12 `NO-BEHAVIOUR`** (*the habitat is enumerated* — the
checker property exists and **nothing implements it**), and **the interface question** (*not a
coarser alphabet, a different slot set* — Figure 11 says which slots: the ones in the cascade).

**And it already identified the direction clause**: *what you cannot perceive or measure yet IS
the residual* — filed there as ***the clause that settles the direction question outright.***

### 3 · FIGURE 9 IS NOT THE SECOND MECHANISM. IT IS THE ARGUMENT FOR THE FIRST

**Figure 9 in these documents is not *split before search*** — that phrasing does not appear in
any file I have, and I cannot confirm it. **What Figure 9 says is:**

> *φ* out of reach: **nothing inside can prove that** · **the witness is always imported** ·
> **the edge can only be named from beyond it***

**Which is the standing-gap problem stated as a limit.** Everything outside the slice is not
provable from inside — so **the edge has to be read off the world rather than derived**, and
that is precisely what §16.5 does. **Figure 9 explains why §16.5 must exist; it is not a second
route to the same place.**

### 4 · A DEFECT IN THE ONE PLACE THAT CITES §16.5 — and it is mine, from this session

`_bindings`' docstring: *"ORDERED by contact ... §16.5 enumerates contact; Figure 11 ranks by
cascade."* **The code does neither.**

    others = [s for s in self.slots if s != slot]              <- EVERY other slot
    seen   = {s: len({st[s] for st, _, _ in robs ...})}        <- ranked by VARIANCE
    return [None] + sorted(others, key=lambda s: (-seen[s], s))

**Two departures.** It **invents the list** — which is `ARC_BUILD_PLAN`'s own complaint about
`_bindings`, verbatim, still true after the change. And it **ranks by variance, not contact**,
while **`touching()` is built and unused.** **Contact ranking ranks by variance and is called
contact ranking** — the eighth A6i-shaped instance, in a mechanism I built this session and
filed as *owed only its demonstration*. **It was owed more than that.**

### 5 · THE LIFETIME IS ALREADY ENFORCED BY A MECHANISM

A map of one board is **playback**, and *generators cross up, playback never does*. **The
boundary already exists**: `retarget` clears `bound`, `trace`, `abstained`, `owed_import`,
`candidates`, `_disproof`, `drive`, `_view` — **and keeps `gamma`.** So a map goes where the
per-episode state goes, **and the firewall is enforced by an existing method rather than by
discipline.** *Vocabulary permanent, instances transient* — the visible set's shape one level
down. **A map that persists "just as a cache" is the failure with a reasonable-sounding
reason**, and it is worth stating on the row before anyone builds one.

**NOT BUILT. Reported.**

---

# §16.5 CHECKED BEFORE BUILDING — three questions, and the corpus answers all three

### Q1 · BUILDABLE — and it does NOT need `0a`'s arity. The park stays parked

**The relations in §16.5 are consumed in TRAVERSAL, not bet on.** *List everything in contact
with the residual, then what is in contact with those, and outward* — the contact edge is
**walked**, and the output is an ordered list of ACTORS. **Binding one operand from that list
is still arity 1.**

> **So `0a`'s trigger — *an atom that consumes past index 0* — stays unfired.** §16.5 is
> **parallel to the arity park, not downstream of it**, and the 13×-for-zero-capability
> argument is untouched. **The closed door is not the same door as `0a`.**

**What it DOES require is one channel opened**: contact must become visible to the loop, which
today sees `slots()` → names and `observe()` → name→int and nothing else. **That is an
interface decision about the eight-member contract**, and it is the only structural cost.

### Q2 · MOSTLY SPECIFIED. The STOPPING RULE is the design space, and it comes to Isaiah

| habitat column | specified? |
|---|---|
| **actors** | **yes** — objects **with affordance profiles**, and §16.4 fixes the vocabulary: *blocks · passes · moves-when-touched · changes-on-touch · triggers-remote*, **read by behaviour under contact, never by substance** |
| **conditions** | **yes** — the action set plus the precondition lattice (§16.1, *at most seven booleans, no pixels involved*) |
| **relations** | **yes** — contact, containment, precondition, correlate-with-my-action |
| **rank by cascade** | **orders on distance outward from the residual** |
| **when to stop** | **DECLARED PRAGMATIC, not unspecified** — see below. The figure says so in its own words, and the loop has no convergence criterion by construction |

**And the bad regions are already marked, which is what makes it a decision rather than a
guess:** a **fixed depth** is an invented number; **everything** is inventing the list again,
which is the defect §16.5 exists to name. **Neither is available, and nothing in between is
specified.**

### Q3 · IT PRODUCES A RESIDUAL. That is the door opening

**The corpus already flagged the clause as settling this** — *the clause that settles the
direction question outright*:

> ***What you cannot perceive or measure yet IS the residual.***

**And the mechanism is immediate rather than subtle: the habitat's third column is RELATIONS,
and no relation has a slot.** So enumerating the habitat **produces, on the first pass, a set
of things the agent can see and cannot represent** — and each is a residual by that clause.
**That is exactly the route from structural observation to recorded residual**, and it does not
wait for a bet to be wrong.

**If it only ordered a search it would be Figure 11's ranking half alone** — which is what
`_bindings` does today, badly, and calls contact ranking.

### A FOURTH CONSTRAINT THE QUESTIONS DID NOT ASK FOR, AND IT BOUNDS THE BUILD

**§16.7's trap.** *"Building a case for what it believes to be true about its purpose"* is
objective abduction, and **the measured history is `abduced=[]` on most games.** The corpus's
fix: *discovering the objective = **minting the φ that explains the residual***, on Figure 3's
ordering — **perception, then vocabulary, then objective** — and ***a module that jumps to the
third is a reading taken below the break.***

> **So §16.5 is a PERCEPTION-LAYER enumeration that emits RESIDUALS. The moment it emits
> GOALS it is the trap, and the trap is where every prior attempt died.**

### WHICH OUTSTANDING ITEMS THE CHECK TOUCHES

| item | touched? |
|---|---|
| **contact ranking** (withdrawn) | **yes — §16.5 IS what it was owed** |
| **B12 `NO-BEHAVIOUR`** | **yes** — *enumerated, never composed* is B12's own wording; the check becomes runnable |
| **the interface question** | **yes** — same mechanism, per the plan's own unification |
| **`touching` built and unused** · **`Affordances` fixture-only** | **yes** — both get their first consumer |
| **the closed door** | **this is what opens it** |
| **`0a` arity** | **NO. Parallel, and the park's trigger stays unfired** |
| **`REUSE_UNWIRED`** | **NO.** §16.5 does not touch reuse. The standing diagnosis is unaffected |
| `never_live` · the reuse term · the visible set's unverified structure · step 7 · justified≠enumerable | **no** |

### THE STOPPING RULE — the corpus DECLARES it rather than leaving it open

**Filed above as *NOT SPECIFIED*. That was wrong, and the sixth law found it:**

> `PHILOSOPHY` §16: *the enumeration runs "outward until the cascade stops mattering", **which
> is a pragmatic bound and says so**.* · `THE_FORMULA`: *that bound is pragmatic, **never a
> completeness claim**.* · **Step 8: *the loop has no convergence criterion by construction*.**

**So the requirement is not to FIND a principled rule — it is to DECLARE whatever rule as
pragmatic and never let it read as completeness.** The bad regions stay marked (a fixed depth
is an invented number; *everything* is inventing the list), **and the honest part was already
fixed: the reporting, not the rule.**

**Two candidate forms, both derived and neither recommended — the choice is Isaiah's:**

| candidate | form | precedent |
|---|---|---|
| **no new relation TYPE in the next ring** | a property of the world, read rather than set | **the IoU threshold dissolving into *match by maximum overlap*** — the same move, and the threshold had *no recorded basis*, which was the ANCHOR problem |
| **the ring stops paying** — no new residual recorded | a reading rather than a setting, in the loop's own currency | **§20.4's surviving proposal**: *end the epoch when the agent stops learning, not at a fixed count* — **a game still surprising you gets more actions because it is still paying** |

**They differ in what they read.** The first stops on **type novelty** and is closer to *read
it off the world*; the second stops on **residual yield** and is closer to the loop's existing
accounting. **Both are pragmatic and must say so on the row that reports them.**

**NOT BUILT. The stopping rule is the one decision owed, and its FORM is freer than the check
first suggested while its REPORTING is fixed by the corpus.**

---

# §16.5 — BUILT 2026-08-27. **The first residual produced without a bet being wrong**

`habitat.py`, seeded from the residual as Figure 11 specifies, run on `ls20`:

    seed o10 (the slot carrying the most unexplained mass)
    2 rings · 3 actors · 8 relations · types ['contact']
    stopped_at_ring 2 -- "no new relation type in ring 3"
    residuals_emitted 8        goals_emitted 0

**EIGHT RESIDUALS FROM STRUCTURE, WITH NO BET HAVING BEEN WRONG.** That is the closed door
opening, and it opens **from the side the check predicted**: not by making relations bettable,
but by making the **inability to represent them** the thing recorded. *What you cannot perceive
or measure yet is the residual*, mechanised.

### THE FALSIFIER HELD, AND IT WAS STATED FIRST

**§16.7's trap: *a module that jumps to the third is a reading taken below the break.*** The
report carries **`goals_emitted: 0`** as a standing field — not because zero is expected, but
because **the moment it is non-zero this is objective abduction wearing a perception layer's
name**, and `abduced=[]` on most games is the measured record of where that ends. **Stated
before the first run rather than discovered after.**

### ONE RELATION OF FOUR, AND THE OTHER THREE ARE REPORTED

| §16.5's relation | disposition |
|---|---|
| **contact** | **built** — sensor 8, Tier 1, and it finally has a consumer |
| **containment** | **NOT hardcoded.** §12.3 lists it with *symmetry, holes, counting-by-colour* as **Tier 2**, composing from the nine, and *the agent should have to reach for them*. **Hardcoding it deletes the evidence the composition system works** — the same rule that forbids loading it |
| **precondition** · **correlate-with-my-action** | **loop-side.** §16.1's lattice and the action history are not perception's to compute |

**Same shape as the atoms this afternoon: the corpus names four, one is available, the rest are
reported rather than substituted.**

### THE STOP IS PRAGMATIC, SAYS SO, AND LEAVES A TRACE

Ruled: **no new relation type in the next ring** — a property of the world, read rather than
set, the same move as the IoU threshold dissolving into match-by-maximum-overlap. **And the
report carries the types seen and the ring at which the set stopped growing**, so the stop is
auditable from the record rather than only correct in the moment — the one thing the
type-novelty rule lacked on its own.

**Declared pragmatic in the output itself**, per `PHILOSOPHY` §16's *a pragmatic bound and says
so* and `THE_FORMULA`'s *never a completeness claim.* **No maximum-rings parameter**: the
object set is finite, so the cascade terminates without an invented number.

### `Affordances` WIRED — the stopping rule now DISCRIMINATES, and the caution caught a defect

    before   2 rings ·  3 actors ·  8 relations · types ['contact']
    after    3 rings ·  9 actors · 13 relations · types ['contact:moves_when_touched',
                                                         'contact:changes_on_touch',
                                                         'contact:unobserved']
    stopped_at_ring 3 -- "no new relation type in ring 4"    residuals 13, goals 0
    97 affordance kinds learned over 40 steps

**It stopped at ring 2 BY CONSTRUCTION and now stops at ring 3 ON A READING.** The rule was
never inert; the panel was one-dimensional, and the thing it discriminates by had been built
at `2c` and wired to nothing since. **A consumer arriving for a mechanism that was waiting —
the connection-table shape rather than new work.**

**DRIVEN STEP-WISE, because §16.4 is a LEARNED reading.** *Behaviour under contact* needs a
before/after pair per step, `run()` offers no hook, and putting a domain reader inside the loop
would be the wrong side of the wall. So the holdout drives `step()` and notes the pair.

### AND THE CAUTION CAUGHT A LIVE DEFECT IN CODE TWENTY MINUTES OLD

**`_rtype` returned `unread` for an all-`False` profile as well as an all-`None` one** —
collapsing *read, and it affords nothing* into *never observed*. **`Affordances` keeps `None`
distinct from `False` in its own docstring, *for the same reason `unreached` is kept distinct
from `unreachable`*, and my type function threw that away one layer up.** Three states now:

| type | means |
|---|---|
| `contact` | **no reader wired** — a fact about the build |
| `contact:unobserved` | reader present, **this kind never seen in contact yet** |
| `contact:inert` | **read**, and it affords nothing |
| `contact:blocks,…` | read, and these are what it affords |

**`contact:unobserved` appears in the live run as its own type**, alongside two read
affordances — so a sparse type set is now readable as *early* rather than as *unwired*, and
**only the first row is a defect.** The second resolves with play and the report says which.

### THE ONE-TYPE READING, SUPERSEDED

`types: ['contact']`. **The relation type is contact QUALIFIED BY THE CONTACTED OBJECT'S
AFFORDANCE PROFILE** — §16.5's actors column is *objects, **with affordance profiles***, so the
profile is part of the habitat rather than an addition. **With no affordance reader wired the
type is bare `contact`, one type, and any ring after the first adds none.**

**`Affordances` is built and fixture-only**, so wiring it is what gives the stopping rule
something to discriminate. **Recorded rather than worked around**: the rule is not inert, the
panel is one-dimensional, and that is the fourth time this session — after the type node, the
reuse funnel, and the seat-scale case.

---

# `REUSE_UNWIRED` CHECKED — **it is a MISREADING, and the funnel is correctly refusing**

### 1 · WHICH CONDITION NEVER PASSES — measured, not reasoned

`eligible = [t for t in targets if stale(t[3]) and t[2]]`, over 7 sweeps on `ls20`:

    owed_targets    33 total, present in ALL 7 calls    targets EXIST
    owed_with_hist  33                                  condition 2 passes for every one
    owed_stale       0, in 0 of 7 calls                 CONDITION 1 NEVER PASSES
    parked_targets   0 always                           0 advances, so that source is empty

**`stale()` is the single gate.** It is false only when `verdict == depth_exhausted` **and**
the unit count has not grown. **All five owed slots read `depth_exhausted`**, and `units` grew
**exactly once** — 14 → 15.

**AND TWO TERMS SETTLED, NOT ZERO.** `idn . translate<o1.h>` and `idn . translate<o12.row>` —
**but they share the atom sequence `(idn, translate)`, and `units()` dedups on the EMITTED
sequence, which carries no operand.** So two settlements produced **one** unit. The gate needs
the unit set to grow *after* an abstention; it grew once, before them.

### 2 · NEVER-SATISFIED, NOT NEVER-SUPPLIED — and the funnel is RIGHT

**Supplied**: targets exist, every one has history. **Not satisfied**: the precondition is unit
growth after an abstention, and it does not recur. **The sweep is not broken and is not
disconnected — it is refusing correctly, for a reason it can state.**

### 3 · ⚠ THE IDENTITY FINDING WAS WRONG AND IS WITHDRAWN. The defect is the GLOSS

**WITHDRAWN 2026-08-28, same session, before it was acted on.** I reported
`sum(reuse_branch) = 7` against `reuse_attempts = 0` as a **violated identity**. It is not.

    Chain.report()["branch_identity_holds"] : True
    NOT_ATTEMPTS = ("no-eligible-target", "rescan")

**`Chain.report` already computes the identity over ATTEMPTS ONLY, and says why beside it:**
*two keys are bookkeeping, not attempts — **"no-eligible-target" (there was no second task to
fail on)** and "rescan" (the unit set grew, so the search was re-run). **Both are counted so
their zeros are measured, and both are excluded from the identity.*** **I summed the counter
naively and read a violation into a distinction the code had already drawn.**

> **This is the session's own recurring shape, and this time I am the consumer.** `Objects`
> stated non-observation ≠ death and was followed. `Affordances` stated `None` ≠ `False` and
> `_rtype` collapsed it. **`Chain` states attempts ≠ bookkeeping and I collapsed it — then
> recorded the collapse as a finding and committed it.** The producer wrote the distinction
> down; the consumer did not read it. **A second instance of the fourth held observation, and
> it moves that bar from n=1 to n=2.**

**SO `reuse_attempted == False` IS CORRECT BY THE CODE'S OWN DEFINITION** — nothing was
attempted, because there was no eligible target to attempt against. **The early return is not
a bypass; it is the documented path for a non-attempt.**

### 3b · WHAT SURVIVES: the LADDER'S GLOSS, and it is still the real defect

**The flag is right and the label's gloss is wrong.** `REUSE_UNWIRED` is glossed ***minted,
reuse never ATTEMPTED → implementation — LOOP NOT CONNECTED.*** **The loop is connected. It
ran seven times and refused seven times at a gate, correctly, for a stated reason.**

> **`not attempted` is true. `not connected` is false.** The rung conflates them, and the next
> rung up is `MINTED_UNUSED` — ***ARCHITECTURE, the only code that indicts*** — so the state
> sits between a wiring gloss it does not deserve and an architecture verdict it has not
> earned. **That is still the §22.6 boundary, and the seventh rung is still the fix.**

**THE CONSEQUENCE IS THE STANDING DIAGNOSIS ITSELF.** `seg.reuse_attempted` stays `False`, so
the ladder can never pass `REUSE_UNWIRED` — which the corpus glosses ***minted, reuse never
ATTEMPTED → implementation, loop not connected.*** **The sweep attempted seven times and
refused seven times for a stated reason, and the ladder reports that no attempt happened.**

> **And the next rung is `MINTED_UNUSED` — *ARCHITECTURE, the only code that indicts*.** So
> the misreading sits exactly on the boundary between a **wiring** verdict and an
> **architecture** verdict, which is the one distinction §22.6 exists to protect.

**WHICH RUNG IT SHOULD READ IS A RULING, NOT A REPAIR.** The observed state — *attempted,
refused before trying, correctly* — is neither *never attempted* nor *tried and not explained*.
**It may be a seventh rung the ladder does not have.**

### 4 · PHASE 4 — ONE HALF CLEARED, THE OTHER NEVER WAS A BOARD PROBLEM

**I said Phase 4 was *partly ungradeable until a real board exists*. Half of that was right,
and for the wrong reason.**

| | |
|---|---|
| **`4e`** — level-reset as controlled experiment | **CLEARED.** Determinism is a property of the domain, and a playable board now exists, so it is measurable: same start, vary one action |
| **`4c`** — Γ as simulator, gated on `sim_fidelity` | **NOT cleared, and a board was never the blocker.** §0.2: *that is a threshold on an average across slots, which is the construction deleted from `probe.py`* — **and the EMA weight and the depth schedule are both magic numbers. *Needs restating as a predicate before it is built.*** **It also violates a hard rule directly: *no aggregation across slots; averaging is how a live signal disappears.*** |

**NOT BUILT. Two rulings owed: which rung the refusal reads as, and whether the identity is
repaired by counting the attempt or by not counting the branch.**

---

# THE RUNG, AND THE ASSERTION REGISTER — both checked, and the corpus has both

### 1 · THE RULING IS ALREADY IN THE CORPUS, so it governs rather than being designed

`THE_FORMULA`, on a low residual reading:

> *a low reading has three causes and only two of them are about R stopping:*
> *the prediction is good — **genuine** · the channel closed — step 8's undetectable case,
> **a seat's office** · the instrument never reached it — **step 7 INWARD***

**One reading, three causes, and one of them explicitly adjudicated by a layer above because
it is undetectable from inside.** That is the ruling — *the rung reports, the layer above
judges* — **already written, applied to the residual rather than the ladder.** And the office
concept recurs: *the loop does not maintain the ground, that is a seat's office*; *the ground
did not decay, the channel did — that is a seat's office, and the cat has no seat.*

**So no seventh rung.** The vocabulary stays fixed, no reading already taken is against a
different instrument, and what changes is that **a rung's gloss stops being a verdict.**

### 2 · IT IS *NOT* DISTINGUISHABLE FROM WHAT IS RECORDED — and that is the finding

**The funnel records the OUTCOME, not the CONDITION.** One bucket, `no-eligible-target`, for
both causes:

    refused, condition legitimately holds    not a fault
    refused, nothing supplied the condition  a fault

**I had to INSTRUMENT the run to tell them apart** — 33 targets present, all with history,
zero passing `stale()`. **None of that is in the record.** The input exists in the code and is
not written down, so **the adjudicating layer would have nothing to adjudicate on.**

**And the corpus's own discipline points at the fix without extending it:** *the reuse funnel
charges every attempt to **a string literal written at the branch that resolved it***. **A
finer literal is inside that discipline**, not a change to it — the branch names which
condition refused rather than that some condition did.

### 3 · THE GLOSS IS CORRECTED AT SOURCE, per the ruling and the document split

**`instruments.py` is a working file, so repaired.** *Loop not connected* is false on the
`ls20` run regardless of who adjudicates. **`ARC_AGENT`'s copy of the gloss is CORPUS and is
annotated, not edited** — the independence is worth more than the tidiness, and this is the
third live instance of that split costing something.

### 4 · THE ASSERTION REGISTER ALREADY EXISTS, AND IT IS THE READ-STATE BLOCK

**One thing, not two — and the read-state block is already the general form, scoped small.**
It states the principle in its own words:

> **The index is a CLAIM ABOUT THAT RECORD, and *a claim about a record has to be checked
> against it.* It never was.**

**And its header is a sharper *how established* than read/inferred/recalled:** ***READ AGAINST
WHAT, not merely read*** — *a section read before a finding and the same section read after
are different reads, and the read-state's `read` is weaker than it looks.* **Recording the
date is the same instinct**, and the block already carries it implicitly by living in a
git-blamed file behind a watermark.

**So: GENERALISE THE BLOCK, do not build a parallel register.** A second one is precisely the
collision this project has caught three times — and the near-miss is real, because
`provenance`'s four values (`derived · found · chosen · unattributed`) are **the same shape for
a different subject**: how a MECHANISM came to be, not how a CLAIM was established. **Two
registers with four-value provenance fields would read as one.**

**AND THE CAUTION THE BLOCK ITSELF SUPPLIES: a register of assertions is a set of
assertions.** The read-state **was** a register and it **was wrong** — it said `DISCOVERY` Q1
and Q8 were unread when the batch log recorded both. **A register does not check itself**, so
the value is entirely in `recalled` entries actually being checked against a source — which is
why the stated bar (*it gates a decision expensive to unwind*) is load-bearing rather than
tidy: **it keeps the register small enough to check.**

### 5b · ⚠ RETROACTIVE: THE DIAGNOSIS DID NOT REPRODUCE. IT COLLIDED

**I argued this morning that `REUSE_UNWIRED` on `snaps` and on `ls20` was *the same rung on
both, so a fact about the loop rather than about a panel*. That was the argument that made it
the next item.** The finer literal shows it false:

> **⚠ REFINED 2026-08-29, AND THE CAUSE IS ONE LAYER BELOW THE COLLISION.** *Did not reproduce*
> is right and *collided* is not the whole of it: **`REUSE_UNWIRED` is a CHAIN STAGE and
> `none-stale` is a FUNNEL REASON — two instruments, not two readings of one.** And the chain's
> stage is **never computed on ARC at all**: `Chain.close()` has two callers, `snaps.py` and
> `tether.run()`, and `arc_holdout.play()` drives `ag.step()` directly because *`run()` gives
> no hook*. **So `ls20` never had a stage to compare.** The comparison was between a reading
> and an absence, and the absence had a name that looked like a reading.

    ls20    none-stale ONLY          every refusal is the loop correctly declining
    snaps   none-stale AND no-targets   correct declining MIXED with supply failures

**Two different states under one label, and I read their agreement as corroboration.**

**IT IS FIGURE 2's COLLAPSE 2, AT THE READING LEVEL, and the corpus is explicit:** ***two
frames agreeing tells you about their shared evidence pool, not about the world. Agreement is
disqualifying for a verdict.*** `ARC_AGENT` applies it to detectors — *four correlated
detectors are one detector wearing four names* — and **mine is the inverse: two states wearing
one name, with the agreement MANUFACTURED BY THE LABEL rather than observed.** The shared pool
was the string.

**DISPOSITION: the item was worth doing and the reason was wrong.** Both true, and separating
them is what stops a good outcome from validating a bad argument — **the same treatment as the
ruling with three supports where one was false.** The conclusion survives on the gloss defect
and the panel split; the premise does not.

**AND WHAT WOULD HAVE CAUGHT IT EARLIER: NOTHING.** The panels reported *identical strings*,
and no instrument could separate them until the literal was split. **This is not a check that
was skipped — it is a distinction that did not exist to be read**, which is a different
category from every other failure recorded today and the only honest thing to file it as.
**The fix and the diagnosis of the misreading arrived together, because the fix is what made
the misreading visible.**

> **THE BOUNDARY, STATED GENERALLY: a record that cannot express a distinction will read as
> agreement no matter how carefully it is read.** So the section check's coverage is bounded
> by **the record's expressiveness**, not by the reader's care — and that is the first limit
> anyone has put on a check that has otherwise paid on every item.

**AND THE INSTRUMENT THAT ADDRESSES IT IS A DIFFERENT ONE, not a refinement.** The section
check reads **what a record says**; this asks **what the record's fields are incapable of
saying** — ***what could this record not distinguish***. Different subject, different
question, **and answerable without a run**, which makes it a standing sweep rather than an
investigation. **It is the nulls sweep pointed at the SCHEMA rather than at the values.**

**ITS OWN LIMIT, STATED WITH IT:** it can only ask about **fields that exist.** A distinction
nobody thought to have a field for is invisible to it too — **the same regress the checker
laws hit, and it stops in the same place: a person asking *what am I not able to tell
apart*.** Recorded as bounded rather than as a solution.

### 5 · BUILT — the refusal now names its condition, and the two panels differ

    ls20    {'no-eligible-target:none-stale': 7}
    snaps   {'no-eligible-target:none-stale': 3, 'no-eligible-target:no-targets': 1}

**Four literals, exhaustive over the gate**: `no-targets` (nothing owed and nothing parked),
`none-stale` (**the condition legitimately holds — the loop working**), `no-history` (targets
with no evidence), `none-eligible` (each target fails one or the other).

**AND THE TWO PANELS ALREADY READ DIFFERENTLY, which is the whole point.** `ls20` is
**entirely `none-stale`** — every refusal is the loop correctly declining, none is a supply
failure. **`snaps` carries both**, so the same bucket was covering opposite diagnoses on the
panel it was read from all week. **The adjudicating layer now has something to read; it had
nothing before.**

**ONE COUPLING THAT WOULD HAVE FAILED SILENTLY.** `NOT_ATTEMPTS` is an exact-string tuple, so
a new literal that is not listed **starts counting as an ATTEMPT** and breaks
`branch_identity_holds` — the identity would have gone false without anything naming why.
**Listed rather than prefix-matched**, per the checker law: *exemptions as data, not logic — a
table can be pinned; logic widens quietly.* A `startswith` test would exempt any literal
anyone later coined, including one that genuinely is an attempt.

---

# `4c` AND `4e` CHECKED — one has a template and a marked space, one is ready

### `4c` · THE PREDICATE FORM HAS THREE WORKED PRECEDENTS, and the specific one is UNSPECIFIED

**The direction is not a hand-wave — REPAIRS 1 did this conversion three times, and each is a
different shape:**

| threshold deleted | what replaced it |
|---|---|
| `EPS = 0.02` | ***the guard is `any(mass > 0)`, not `mean < eps`*** — an **existential over slots** replacing an aggregate |
| `WARM = 12` | **deleted outright** — *a predicate warms itself; a fresh model has live mass on its first miss* |
| the IoU cutoff | `overlap` returns a **RATIO**, and tracking takes **maximum overlap**, so ***nothing needs a cutoff*** — **relative, not absolute** |

**And Q20 is the closest analogue**: it specified *an error EMA fallen to ~0 with enough
observations*, and the build uses **a single-step predicate**, because *REPAIRS 1 removed the
EMA for aggregating across slots.* **`sim_fidelity` is that same construction, unconverted.**

**WHAT THE CORPUS DOES NOT SAY IS WHICH.** The three precedents give three forms — existential
over slots, delete-because-it-self-corrects, or relative-so-no-cutoff — and *depth grows as
fidelity rises* would become a **reading** under any of them (§20.4's surviving proposal:
*end the epoch when the agent stops learning, not at a fixed count*). **The form is specified,
the choice is not. A marked design space, and it goes to Isaiah rather than getting invented.**

**AND THE REASON NOT TO LEAVE THE ROW AS IT STANDS** is the `_bindings` shape exactly: **a line
that reads as buildable and is not, which nobody re-reads.** The row currently specifies a
construction that violates a hard rule — *no aggregation across slots; averaging is how a live
signal disappears* — and reads as a spec.

### `4e` · READY, and the deferred gate check's subject arrives with it

**Determinism is a domain property and `ls20` is playable locally**, so the controlled
experiment is available: same board, vary one action, read the difference. **§21.1 calls it
the only place in the loop a controlled experiment exists.**

**And §21.2's discriminator is BUILT, not owed.** `disproof` records `{live, splits,
refuted_at_least, by}` and **varies 40–71 across 74 rows** — so it distinguishes a well-chosen
discriminating action from a poor one. §21.2's two discriminators both hold: **the mechanism**
(`ResetGate` bans the *agent* calling RESET; a game-inflicted restart is the world's own rule)
and **the intent** (hypothesis and disproof stated *before* the action).

> **THE CHECK THAT WAS DEFERRED SHIPS WITH THIS ITEM.** The index already records it: *a gate
> check over `disproof` — the field exists; no check reads it*, deferred *when deliberate
> death does, which is where its subject comes from.* **`4e` IS that arrival**, so the check
> ships with `4e` rather than staying deferred — and a control that examines nothing cannot
> demonstrate a clean state.

**Plus the number §21.2 names to publish beside it: *what fraction of the action budget went
to deliberate deaths. If that is 40%, someone should see it rather than infer it.***

### WHAT THE TWO CHECKS TOUCH

| | |
|---|---|
| **held observations** | **none of the four.** Neither item bears on them |
| **panel defects** | **the single type node — `4c` only, and indirectly**: a predicate over slots needs slots that differ, and `ls20` supplies 105. **Not the toy world** |
| **outstanding rows** | **`4e` closes one**: the deferred `disproof` gate check. **`4c` closes none and opens a ruling** |
| **`REUSE_UNWIRED`** | untouched by both |

**NOT BUILT. One ruling owed on `4c`: which predicate form. `4e` needs no ruling.**

---

# `4e` — BUILT 2026-08-28. Three mechanisms, and all three read NULL at 40 cycles

### 1 · WHAT WAS BUILT

**`experiment.py`** — §21.1's controlled comparison. *Same starting board, vary exactly one
action, observe the difference*, keyed on **the full slot reading, never a digest**: two boards
agreeing on a hash is Figure 2's collapse at the level of the key, and the mechanism's whole
claim is *the same moment, re-run*. **Determinism is MEASURED as repeats rather than assumed**,
and an unstable repeat invalidates the pairs drawn from that state.

**Gate check 10** — §21.2's discriminator. A **chosen** death with no `disproof` stated before
it is refused. **World-inflicted deaths are not its subject** — declaring one would be theatre
— and that exemption is **data on the row** (`deliberate`) rather than logic in the check.
**Three tests: the defect, the declared case that passes, and the out-of-scope case.** 13 gate
checks → 16.

**`terminal()` got its consumer.** It was written *read by the harness, never by the loop* and
read by nothing since `2a`. A `GAME_OVER` nobody reads is a level-resetting loss the agent
cannot exploit — **and the loss is the only controlled experiment available.**

**And §21.2's number is published rather than inferred**: `budget_to_deaths`.

### 2 · ALL THREE READ NULL, AND THE NULLS CHAIN

    endings {}          no terminal reached in 40 cycles
    states_seen 40      controlled_pairs 0      states_revisited 0
    budget_to_deaths 0.0

**Forty steps, forty distinct states.** On a 64×64 board with 105 slots the full reading
essentially never repeats — **so the only thing that returns you to a seen state is a RESET,
and a reset needs a death.** The chain is: **no death → no reset → no repeated state → no
control.**

**AND THE PANEL DOES SUPPLY DEATHS.** Blind cycling of all four actions reads `GAME_OVER` on
**172 of 300 steps** — confirmed *before* the build, not after, per the panel-property rule.
**So the null is not the panel lacking the property.**

**AND THE BLIND NUMBERS SAY MORE THAN THEY FIRST READ AS.** 300 steps split **128
`NOT_FINISHED` then 172 `GAME_OVER`** — which is not *dies often*, it is **died once around
step 128 and stayed dead.** So `ls20` does not auto-reset on death; the state persists.

| run | endings | states | revisited | pairs |
|---|---|---|---|---|
| 40 cycles | none | 40 | 0 | 0 |
| **100 cycles** | **none** | 100 | 0 | 0 |

**A 100-cycle agent run sits BELOW blind play's death point**, so the null is consistent with
scarcity and says nothing yet about policy. **220 cycles is running.** *(And the earlier
reading of 172-of-300 as "the panel supplies deaths abundantly" was a misread of a persisting
state as a recurring event — the property holds, the abundance does not.)*

**AND IF THE GAME DOES NOT AUTO-RESET, §21.1's EXPERIMENT NEEDS SOMETHING TO RESTART IT** —
which `ResetGate` bans the agent from doing. **That would make the controlled experiment
depend on a seat-side restart, and whether that is legitimate is §21.2's question, not a
wiring detail.** Flagged rather than assumed.

### 2b · THE CRASH, DIAGNOSED — the death arrives at cycle 130 and the loop does not survive it

    CRASH at cycle 130    env.terminal() 'death'    env.blind True
    slots 0               frame GameState.GAME_OVER    board None

**It was scarcity, and the death lands where the panel said it would** — blind play's
transition is ~128, the agent's is 130. **So the nulls at 40 and 100 were runs that stopped
before the transition**, and everything past it was **unmeasured rather than empty.** Every
reading taken at those lengths had an unstated ceiling and nobody knew there was one.

**AND THE CAUSE IS NOT AN UNREADABLE BOARD — THERE IS NO BOARD.** `board()` returns `None` on
a terminal frame, so `_decomposed` sets `blind`, `slots()` is empty, and
`focal = max(sorted(self.slots), …)` raises on an empty sequence. ***No slots to act on* is a
legitimate state and `max()` is a crash.**

**`terminal()` IS CORRECT AND UNREACHED.** It returns `'death'` at exactly that moment — the
mechanism works. **`4e`'s wiring reads it AFTER `ag.step()`, and the step raises first**, so
the ending is never recorded and `retarget` never fires. **The only controlled experiment
available is behind a crash rather than behind a design gap.**

### 2c · WHOSE SHAPE IS IT — and the answer argues for keeping two things apart

`ArcWorld.blind` **is set correctly** and the loop **never reads it**; the loop reads
`slots()`, which is `list[str]` and cannot express *blind* at all.

> **That is NOT cleanly the fourth held observation.** There, `Affordances` stated `None` ≠
> `False` **in a value the consumer read**, and `_rtype` collapsed it. **Here the consumer
> reads a DIFFERENT accessor that never carried the distinction** — a record whose fields
> exclude what a reading needs, which is **the LINKED instrument, not the observation.**

**So this instance sits on the junction and does not settle it — it shows the two are
genuinely distinguishable.** Which is an argument for the separation that was recorded as a
link rather than a narrowing, and **the held observation stays at n = 2.**

### 3 · A CORRECTION TO MY OWN SECTION CHECK

**I wrote that `4e` IS the arrival of the deferred `disproof` check's subject.** It is not.
The subject is a **DELIBERATE** death — the agent *choosing* to die to buy an experiment — and
that is an **agent-policy** change, not wiring. **§21.1's controlled experiment needs only a
level-resetting LOSS**, which is a different clause from §21.2's licence to seek one.

> **The check ships and its subject is still empty.** Which is the thing I said a check must
> not do, arriving in the item I said would fix it. **Recorded rather than smoothed**: the
> check is correct and cheap, and it examines nothing until deliberate death exists.

---

# `ResetGate` AS A STATE CONDITION — CHECKED, and the corpus rules against it AT THAT STATE

**The proposal: RESET from `GAME_OVER` is continuing rather than farming — nothing to escape,
no attempt to farm — so the gate becomes a readable condition and the restart stops being
borrowed.** Checked against §21.2 as asked. **It draws the line elsewhere, and the recorded
incident is the exact case.**

### 1 · THE INCIDENT IS RESET-ON-`GAME_OVER`, BY NAME

> ***`bounds.py` exists because the Redux harness once violated this by force-RESETting **on
> GAME_OVER** to farm ~18 unearned attempts.***

**The state the proposal licenses is the state the incident occurred in.** And the mechanism is
visible in the wording — ***unearned ATTEMPTS***. **On a scored run the scarce resource is
attempts, not board position.** After `GAME_OVER` there is nothing to escape *within the
episode*, which is what the proposal reads; **what a restart buys is another attempt at the
level**, which is what the scorecard counts and what "farming" names.

### 2 · AND THE CORPUS DRAWS THE LINE BY *WHO*, NOT BY *WHICH STATE*

`arc_world`, at the site: ***a GAME-INFLICTED restart is the world's own rule and reaches the
loop as an observation; an AGENT-CALLABLE one is a bypass of it.*** §21.2 the same: *`ResetGate`
bans the **agent calling** RESET.* **The distinction is agency, and the proposal re-draws it by
state.** Where the corpus already draws a line elsewhere, that governs.

### 3 · AND THERE IS NO DECISION POINT TO GATE — RESET IS NOT IN THE ACTION SET

`actions()` filters it: `… and GameAction.from_id(i) is not GameAction.RESET`. **The agent
never sees RESET, so a gate that reads a condition and refuses has no subject.** Making it
state-conditioned means **putting RESET back into the agent's action set**, which is not a gate
reading a condition — **it is re-opening the path `bounds.py` closed**, with a condition
attached.

**On the second question asked — can the gate read the state where it decides — the state IS
readable (`terminal()` returns `'death'` at the moment of the crash). That is not the
obstacle. The obstacle is that there is no decision to condition.**

### 4 · SO THE BORROWING STANDS, AND THE PROPOSAL ADDS NOTHING EITHER WAY

**Scored run: the restart is farming, by the recorded incident.** **Unscored run: the seat can
already restart, which was ruled legitimate an hour ago.** **So there is no case where the
agent-callable version buys something the seat-side version does not** — and the cost recorded
on that row stands unchanged: *an experiment the agent cannot run alone is not a capability the
agent has; on the private set nobody restarts anything.*

**NOT BUILT, and not a close call: the corpus rules on the exact state, with a measured
incident and a number attached.**

---

# THE CRASH REPAIRED, AND `4c` BLOCKED — both after their section checks

### 1 · THE REPAIR GOES IN `step()`, AND THE CHECK CHANGED ITS SHAPE

**Ruled: the loop tolerates a boardless frame, because *no slots to act on* is a state of the
world and not a condition the seat sets.** Verified: **no crash in 220 cycles**, and
`terminal()` reads `'death'` where the loop used to die.

**THE VOCABULARY NAMED IN THE RULING EXISTS FOR A DIFFERENT SUBJECT.** `CHANNEL_CLOSED` in
the loop is **per-slot** — *the slot owes and this step read zero* — and `probe`'s is *nothing
the frame can see has ever moved*. **Neither is *there are no slots at all*.**

**AND THE CORPUS CONSTRAINS *the loop must be able to hear it*.** `THE_FORMULA`: *R stops
arriving because the prediction is perfect* and *because the channel closed* look alike from
inside — ***detecting the second is not something the loop can do; that job belongs to a
position outside the loop.***

> **So the repair REPORTS AND ADJUDICATES NOTHING.** It records that the slot set is empty and
> explicitly does not say whether that is a terminal frame, a closed channel or a perception
> failure. **The rung reports; the layer above judges — the same ruling, arriving in the
> repair that prompted it.** `PHILOSOPHY` Q3 gives the positive form: *what the agent can do
> instead is **report its own epistemic state soundly***, which is achievable where knowing
> the truth is not.

**TWO DETAILS THE CHECK SUPPLIED.** `False` was already the right return — the contract is
*returns False if no action was proposed, which is a legal outcome* — so **a step that cannot
happen returns what a step proposing nothing returns.** And **the monotone surprise integral
is untouched**, which `THE_FORMULA` names as the one structural defence against this exact
blindness: *a system that could zero its own surprise record could look calm by having
forgotten it was ever wrong.* **A turn with no reading must not look like a turn that went
well.**

### 1b · THE REPAIR OPENED THE ENDING, AND EACH FIX EXPOSED THE NEXT DEFECT — ALL MINE

    before the repair    CRASH at 130
    after the repair     endings {'death': 32}   states 130   deaths 0.200
    edge-triggered       endings {'death': 1}    states 131   revisited 1   deaths 0.006
    absence excluded     endings {'death': 1}    states 130   revisited 0   deaths 0.006
    seat restarts        endings {'death': 1}    states 159   revisited 0   PAIRS 1

**§21.1's CONTROLLED EXPERIMENT HAS FIRED — one pair.** Same state, exactly one action varied,
both outcomes read. **The only controlled experiment available anywhere in the loop, run for
the first time.**

**And the restart recovered the dead time**: 159 live states against 160 cycles, where without
it ~30 steps produced nothing. **`revisited 0` with `pairs 1` is the mechanism's own
separation** — no state recurred under the SAME action (which would be a determinism reading),
one recurred under a DIFFERENT one (which is the experiment).

> **BORROWED, AND THE LABEL SITS WHERE THE NUMBER IS PUBLISHED, not only on the row:** *the
> controlled pairs exist only because the SEAT restarts the bench; on a scored run nobody
> restarts anything, so the pair count is not a capability the agent has.* **Strictly more
> borrowed than determinism** — determinism survives the port and this does not.

**All four readings are now correct, and every null is explained rather than open.** The
phantom revisit is gone, the ending count is one, and **§21.2's number reads 0.006** — one
death in 160 cycles, which is what happened.

**`terminal()` IS NOW READ AND `retarget` FIRES.** `4e`'s wiring is out from behind the crash.

**DEFECT ONE, MINE: A PERSISTING STATE READ AS A RECURRING EVENT — THE THIRD TIME TODAY.**
`terminal()` reports the CURRENT frame, so once `ls20` is `GAME_OVER` it answers `death` on
every later step. The wiring retargeted on each, recording **32 endings for one death** and
publishing **`budget_to_deaths` as 0.200 when the honest figure is 0.006** — **§21.2's number,
the one written down precisely so nobody has to infer it, wrong by a factor of 32.** *(First
appearance: my reading of 172-of-300 `GAME_OVER` frames as abundant deaths. Second and third:
this wiring and this number, an hour later, in code.)* **Edge-triggered now: an ending fires
where the state CHANGES.**

**DEFECT TWO, ALSO MINE, EXPOSED BY THE FIRST FIX.** `revisited 1` appeared. After death
`observe()` returns `{}`, so **every boardless frame shares the signature `()`** and two
absences read as *the same state revisited* — a determinism reading over nothing. **An absence
is not a state of the world**, which is the rule that made `components` return `NOT_RESOLVED`
rather than `[]` this morning, **arriving one layer out and unenforced there.**

### 1c · AND THE REMAINING NULLS ARE NOW EXPLAINED RATHER THAN OPEN

**131 states from 160 cycles: about 30 steps produce no state at all.** After death the board
stays `None`, the agent survives and idles. **`revisited 0` and `pairs 0` follow directly —
nothing restarts the board, so no state recurs, so the controlled experiment has no subject.**

**Which lands exactly where the borrowing ruling put it**, with the cost now measured rather
than argued: **without a seat-side restart, ~30 of 160 cycles are dead time and the pair count
is structurally zero.** §21.1 needs *the same starting board*; `ls20` does not auto-reset; and
`ResetGate` correctly bans the agent from restarting.

### 2 · `4c` CANNOT BE BUILT — its subject does not exist

**`4c` is *roll forward a candidate ROUTINE before committing*, and routines are `4a`/`4b`.**
Neither is built; **no NSM primes occur anywhere in the tree.** And `disproof`'s form needs
**more than one candidate to group by prediction** — with none, it is zero by construction.

**THE RULING ON THE FORM STANDS AND IS UNAFFECTED.** Two mechanisms, on the lens's precedent;
`disproof` as the second signal, because it is **a barrier rather than a score and cannot be
satisfied by doing nothing** — a no-change rollout matches perfectly and refutes nothing.
**With the clause at the site: the second signal must not be derivable from the first, since a
second signal computed from the same trace is one mechanism with two names.**

**Blocked on `4a`/`4b`, which is sequencing rather than a defect in the ruling.**

---

# A PERSISTING STATE READ AS A RECURRING EVENT — three instances in one session, all mine

**Same misread three times, in three different materials, and the third only became visible
once the second was fixed:**

| # | where | what it did |
|---|---|---|
| 1 | **a reading** | 300 steps splitting 128 `NOT_FINISHED` / 172 `GAME_OVER` read as *the panel supplies deaths abundantly*. It is **one death at ~128 and a state that persists** |
| 2 | **wiring** | `terminal()` reports the CURRENT frame, so the seat retargeted on every post-death step — **32 endings for one death** |
| 3 | **a signature** | after death `observe()` is `{}`, so **every boardless frame shares the key `()`** and two absences read as *the same state revisited* |

### AND THE THIRD IS THE WORST BECAUSE OF WHERE IT LANDED

**Instance 2 published `budget_to_deaths` as `0.200`. The honest figure is `0.006`.**

**That is §21.2's number** — the one specified as ***if that is 40%, someone should see it
rather than infer it*** — **wrong by a factor of 32, in the field built precisely so a reader
would not have to infer.** A number whose entire purpose is to stop an inference, misreporting
by 32×. **The failure is in the instrument, not in the thing measured**, which is the class the
whole session has been chasing and this is its sharpest instance.

> **THE INSTRUMENTS BUILT TO PREVENT INFERENCE ARE NOT EXEMPT FROM THE ERRORS THEY EXIST TO
> PREVENT** — and the exposure is structural: **a number that exists to be trusted is a number
> nobody re-derives.** `coverage`, `disproof`, `admissions`, `branch_identity_holds` and
> `goals_emitted` are all of that kind, and **each is read rather than recomputed**, which is
> the property that let this one stand at 32× until a recount was forced by something else.

### WHAT DISTINGUISHES THE THREE, SINCE RESEMBLANCE IS NOT A CLASS

**They are one shape and not one mechanism.** Instance 1 was an inference from a summary;
2 was a level-versus-edge trigger; 3 was a key that could not tell absence from a value.
**Related by the same confusion — *is this thing happening, or is it still true?* — and by
nothing else.** Recorded as a shape with three instances rather than filed as a class, per the
four-classes correction.

**The one transferable clause: *an absence is not a state of the world*** — which is the rule
that made `components` return `NOT_RESOLVED` rather than `[]` this morning, **arriving one
layer out and unenforced there.** The rule existed; the layer above did not carry it.

---

# MECHANISMS WAITING FOR CONSUMERS — four, and the fourth was DECLARED rather than found

| mechanism | built | consumer arrived |
|---|---|---|
| `touching` (sensor 8) | `2b` | **2026-08-27, §16.5's habitat** — computed and consulted by nothing until then |
| `Affordances` | `2c` | **2026-08-27** — fixture display only, until it qualified the habitat's relation types |
| `terminal()` | `2a` | **2026-08-28, `4e`** — written *read by the harness, never by the loop* and read by nothing |
| **`experiment.pairs`** | **2026-08-28** | **NONE — and said on the day it was built** |

**THREE WERE FOUND BY A CHECK. ONE WAS DECLARED AT BIRTH.** That is the register working
prospectively for the first time in this class — the same distinction the A6i entry draws
between its retrospective and prospective instances, arriving in a different class on the same
day.

**And the declaration is the whole difference.** An object produced with no reader is a shape
this project has catalogued repeatedly; **naming it while building it costs nothing and finding
it later costs a check.** `pairs` has no consumer, building one is a separate item with its own
section check, and **one pair is a mechanism working rather than a result.**

---

# THE CONTROLLED EXPERIMENT, REBUILT AS APPARATUS — and it discriminates 3 for 3

    states_seen 1        all four trials from the same board -- the reset is exact
    controlled_pairs 3   four actions from one state
    DISCRIMINATING 3     every pair shows a per-slot difference in the WORLD's response
    unstable 0

### 1 · WHAT I BUILT AN HOUR AGO WAS A CONTINUATION, AND THE RULING EXCLUDES IT

**Ruled: the seat may restart for its OWN reasons and may not restart to help the agent
learn** — and the check is **carriage, not intent**: *does the agent carry anything across the
restart?* **`retarget` keeps `gamma`.** So the first version handed the level back **with what
had been learned**, which is an attempt however it is labelled, and *who pressed the button
does not change what it bought.*

**`ArcWorld.restart()` DELETED rather than rewired.** Its only caller was that continuation,
and a method whose purpose is restarting into a live agent is **a trapdoor to the version the
ruling forbids** — second trapdoor removed today, after `molecules`.

**`controlled()` is the replacement and it has no agent in it at all.** Fresh wrapper reset per
trial, fresh tracker, no Γ. **The carriage question does not arise rather than being answered
well.**

### 2 · AND THE OUTCOME VARIABLE WAS WRONG, WHICH IS WHY THE FIRST PAIR READ 0.0

**The first version compared `sum(_last_mass.values())` — the MODEL's residual, aggregated
across slots.** Two defects in one expression:

- **It measures the model, and §21.1 asks about the world.** *Disambiguating intervention*
  (Schulz & Bonawitz) and *causal structure learning from intervention* (Gopnik) are about
  **causal structure, not about calibrating a predictor.** Both quantities are per-slot and
  available at the same instant, **so the substitution is invisible** — `_rtype`'s shape
  exactly: the right quantity one layer down, a plausible neighbour used instead.
- **It is an aggregate across slots**, the construction the hard rules refuse and the one
  `sim_fidelity` was refused for **the same afternoon**.

**THE 0.0 WAS THE VARIABLE, NOT THE QUANTITY.** With the world's per-slot response and an
existential reading — ***any slot differing***, never a sum — the same experiment reads
**3 of 3 discriminating.** *(And the model-state confound dissolves rather than being managed:
with the world as the outcome, two visits whose slots were all `IDN`-bound are simply
irrelevant, because the model is not a term in the measurement.)*

### 3 · BOTH BRANCHES WERE NAMED IN ADVANCE AND NEITHER WAS THE ANSWER

*The object carries a signal* or *a controlled experiment measuring a quantity that does not
discriminate.* **It was a third thing: a defective outcome variable**, which reads exactly like
the second and is a different repair. **Named in advance, and still not the shape it turned out
to be** — which is the argument for inspecting rather than characterising, one more time.

**BORROWED, AT THE POINT OF PUBLICATION:** *the pairs exist only because the SEAT restarts the
bench, for its own measurement, with no agent in the run. On a scored run nobody restarts
anything.* **Strictly more borrowed than determinism, which survives the port.**

### 3b · `signature()` PAID FOR SOMETHING NOBODY WAS MEASURING

**The key is the full slot reading, never a digest**, and the reason recorded this morning was
Figure 2: **two boards agreeing on a hash is the collapse at the level of the key**, and the
mechanism's whole claim is *the same moment, re-run* — which a collision silently falsifies.

**It bought a second thing that was not the reason.** `states_seen 1` across four trials means
**all four resets returned the SAME board, exactly** — and that is §21.1's determinism
precondition, ***the property the only controlled experiment in the loop rests on***,
**measured rather than assumed.**

> **A digest would have hidden precisely that.** Two *similar* boards collide into one key and
> read as *exact*, so the precondition would have looked confirmed whether or not it held —
> **the reading would have been identical and the fact underneath it unknown.**

**A decision taken to avoid one failure, paying for something nobody was measuring yet.** Worth
recording as a shape: the reason a choice was made and the thing it turned out to secure are
**different**, and the second is invisible at the time the first is being argued.

### 4 · IT IS `B17`, SECOND INSTANCE — the same law, not one layer out

***Pre-registration does not protect a reading if the instrument measures something else.***
**That is literally this**: two outcomes pinned in advance, and the instrument measured the
MODEL where the reading was about the WORLD. **B17's mechanism was a label with two meanings;
this one was a quantity substitution. Same law, different mechanism.**

**And B17's cost clause applies exactly.** *It cost nothing only because 9-versus-37 is
impossible to miss; 15-versus-18 passes straight through.* **`0.0` against 3-of-3 is impossible
to miss too** — **had the residual read a small nonzero difference I would have taken it as a
weak signal and never checked the variable.** Both instances survived on the size of the gap
rather than on the discipline.

**AND THE LIMIT THIS PUTS ON PRE-REGISTRATION IS THE FINDING.** Both branches I named were
about the measurement's RESULT; the defect was in the MEASUREMENT. **A defective outcome
variable reads exactly like a quantity that does not discriminate — same zero, different
repair — and no amount of naming the outcomes separates them.**

### 5 · AND THE COUNT WAS THREE, AND IT IS TWO

**Claimed: `_rtype`, the residual-versus-world outcome, and the aggregate `sim_fidelity` was
refused for.** **Instances 2 and 3 are ONE EXPRESSION.** `sum(_last_mass.values())` was *both*
the wrong quantity (model, not world) *and* the wrong construction (a sum, not per-slot) —
**two defects in one line, which is how it was reported when found and then became two
entries.**

**n = 2**, and the over-count is this morning's three-of-five in the same shape, on the same
day. **Corrected before it was carried.

---

# THE STALE LIBRARY AND THE ROUTINE'S PRICE — three checks, three different answers

### 1 · THE DISPOSITION IS §21.4, AND ITS DECAY HALF WAS BUILT AND WITHDRAWN

**§21.4 rules it already:** *a completion is simultaneously a settle and a regime-change
warning* — **credit** the hypotheses live at completion, **and** *ARC-AGI-3 changes mechanics
between levels, so **do not trust them in the next level until RE-TESTED***. *Crediting without
the decay is the incumbency pathology; decaying without the credit throws away the only
positive evidence there is.*

**And *re-tested* is the staleness test, by name.**

**BUT THE DECAY HALF WAS BUILT, MEASURED ON TWO PANELS, AND WITHDRAWN** — `tether.py` carries
the record: *reverting unpromoted terms to candidate at a boundary cost opportunity, uptake and
carried in both, with nothing measurable bought; the rate difference was 1.3 SE.*

> **AND THE WITHDRAWAL'S DIAGNOSIS IS THE ARGUMENT FOR THE NEW PROPOSAL.** *Settled-ness was
> never the property that separates a mechanism from a term that closed a slice — all ten wrong
> terms in the false-mint read fired the held-out test and survived it — so **gating a boundary
> on it removed good terms along with bad.*** The revert was a **blanket** disposition on the
> **wrong gate.**

**The staleness test is a different gate: a per-term OBSERVED failure, not a boundary sweep.**
*The terms that fail name themselves*, so upsert/caveat/re-derive apply to a named set rather
than to the library. **That is what the withdrawal asked for in its own words** — *`promote`
remains and still records ... worth keeping observable **for whatever gates on it next***.

### 2 · AND NO, A FAILURE CANNOT BE ATTRIBUTED TODAY. The field is small and absent

**`Standing.refute()` sets `settled_at = None`.** So after a refutation:

    a term that settled at tick 40 and failed at 90   ->  settled_at None, rejections 1
    a term that never settled and failed              ->  settled_at None, rejections 1

**Identical records.** *Held before, fails now* and *never held here* are the same row — **which
is the two-state collapse again, in the field the mechanism would read.**

**The nearest thing that exists is `_settled_at_level`**, the segment's starting line, used once
to compute `settled_here` in the retarget row. **It is overwritten at every boundary and queried
by nothing**, so the history exists for exactly one level and is then gone.

### 3 · THE CORPUS PRICES ROUTINES IN BITS, AND MARKS IT SETTLED — so that governs

> `DISCOVERY` **Q21 — *is `R_goal` measurable* — SETTLED: yes, `1 − degree(molecule)`, **priced
> by the same MDL one level up***. · `ARC_AGENT`: *ACT | routine | Seq/When/Until | a goal
> residual no routine closes* — **demonstrated by pricing a quantified objective with the same
> two-part MDL one level up.**

**AND THE OBJECTION ADDRESSES ONLY THE FIRST TERM.** *Move left then press* and *move left three
times then press* are not separated by description length — **true, and the bargain is
TWO-part.** What separates them is `|R|φ|`: **the wrong routine leaves the goal residual
unexplained and fails the second term.** Description length alone was never the test.

**BUT THE ACTION COST IS GENUINELY UNCOUNTED, AND THAT PART IS NOT A CORRECTION — IT IS A
GAP.** *Every step is one of 500, non-refundable, accruing*; a three-step routine costs three
actions **to find out about**, whether or not it pays. **Nothing prices that.** The bits budget
measures what a routine EXPLAINS; the action budget measures what trying it COSTS, and the
corpus prices the first and nothing prices the second.

> **So the two do not dissolve into one question — they are two budgets.** Routines compete
> with terms for BITS (Q21, settled) and with probes for ACTIONS (unpriced). *What does this
> buy given what I am currently trying to do* is `disproof`'s form pointed at the second
> budget, **and the second budget has no accounting at all.**

**NOT BUILT. Three checks, and the third is the one that opens something.**

---

# THE FOUR QUESTIONS ARE ALREADY RECORDED — at the ruled unit, and nothing needs adding

**Ruled: the unit is the (term, slot) pair, because the loop's event is the slot-step and a
term-level total is an aggregation across slots.** Checked, and **the ledger already records
every event at exactly that unit.**

| every `bet` row carries | every `settle` / `demote` row carries |
|---|---|
| `bound=<term>` · `mass=r.bits` · `cause` · slot · cycle | `asked=[name, slot]` · `ground_said` · `term` · cycle |

    called   a bet row exists with that term bound to that slot
    held     mass == 0 and cause == GENUINE
    failed   mass > 0
    arc      first `settle` row to first `demote` row, by cycle

**AND `cause` ALREADY CARRIES THE FOURTH DISTINCTION.** *Applied and wrong is a different state
from did not apply* — and `mass == 0 with CHANNEL_CLOSED` is *the slot owes and this step read
zero*, **which is did-not-deliver rather than predicted-right.** The third state is on the row.

### ⚠ A CORRECTION: I SAID THE RECORD COULD NOT DISTINGUISH THEM. IT CAN

**This morning I reported *held-before-fails-now and never-held-here are the same row*. That is
true of `Standing` and false of the record** — **I checked the in-memory object and called it
the record.** `Standing.refute()` erases `settled_at`; **the ledger keeps the `settle` row AND
the `demote` row, both with cycles.** A term with a settle followed by a demote is visibly
different from one with only a demote.

> **So the third-state repair is not a precondition of the arc.** It is a defect in `Standing`
> — real, and worth fixing on its own terms — **but the arc is computable without it**, and
> building the repair *in order to* enable the arc would be repairing the wrong layer.

### SO THE ANSWER TO *WHAT SHOULD AN ACCUMULATED SETTLE RECORD CARRY* IS: NOTHING NEW

**Not four counters. Not a list of settle events. A QUERY.** The events are already recorded,
already per-pair, already with the outcome and the cycle — **and step 5's outcome IS written
where it can be read; what is missing is only that nothing reads it.**

**Which is the sixth law at a call site again:** *assume it is already recorded, and go look.*
**And it matters more than usual here, because four fields on `Term` would have been a second
producer of a fact the ledger already holds** — the A1 shape, at the level of a record.

**WHAT IS GENUINELY ABSENT** is the reader, and its disposition is the staleness test: *held
consistently and then stopped* is the room's signal and **nothing computes it.** The other two
readings — *held whenever it applied* and *held rarely* — bear on the 42%: **a term that closed
once and never held again is visibly different from one that keeps holding**, and ten wrong
terms fired the held-out test and survived it.

**NOT BUILT.**

---

# THE THIRD-STATE RULE — eight sites, enumerated, and ONE place it is violated

**The count was being carried in conversation and not in the record** — *seventh site*, *eighth
site*, quoted three times and enumerated nowhere. **Which is the assertion class exactly: a
claim about state, load-bearing, recorded nowhere as a claim.** Checked, and it holds:

| site | the two states that are not one |
|---|---|
| `sensors.NOT_RESOLVED` | a value · **never read** |
| `Affordances.profile` | `None` ≠ `False` — *for the same reason `unreached` is kept distinct from `unreachable`* |
| `habitat._rtype` | `contact:unobserved` (reader present, never seen) ≠ `contact:inert` (**read**, affords nothing) |
| `tether.sweep` | `no-targets` (nothing supplied) ≠ `none-stale` (**the condition legitimately holds**) |
| `arc_world.blind` | cannot see ≠ nothing there |
| `tether._cause` | `CHANNEL_CLOSED` — owes and read zero ≠ **predicted right** |
| `behaviour.no_delivery` | did not deliver ≠ **held** |
| `gate` | `unreached` ≠ `unreachable` — stopped looking ≠ proved absent |

**EIGHT WHERE THE RULE IS APPLIED. ONE WHERE IT IS NOT:** `Standing.refute()` sets
`settled_at = None`, collapsing *held-then-failed* into *never-held*. **The defect stands alone
against eight instances of the same rule**, which is a stronger case for repairing it than any
argument about the rule.

**AND THE `no_delivery` ONE WOULD HAVE BEEN THE MOST EXPENSIVE.** Counting a `channel_closed`
zero as a hold **inflates the exact number the staleness disposition reads** — *a term that
stopped being tried would have read as a term that keeps working.* **Least visible, in the
field that measures holding.**

**The sites were always in the code. The COUNT was in the conversation** — and that is the
distinction the assertion register exists to make.

---

# SPLITTING — CHECKED. The clause IS in the corpus, and the trigger's input is DISCARDED

### ⚠ CORRECTION FIRST: I SAID IT WAS NOT THERE

When *split before search* was raised earlier I reported ***that phrasing does not appear in
any document I have***. **It does — `THE_FORMULA` step 7.** I searched `ARC_AGENT` and
`PHILOSOPHY` for *Figure 9* and never searched `THE_FORMULA` for the words. **A search for the
citation, not for the content**, which is the familiarity inversion the sixth law names.

### 1 · AND IT IS RICHER THAN THE SUMMARY IN THREE WAYS

> *IS THERE A FACT HERE? Disagreements that do not shrink with effort, **where each rule keeps
> working well on a different subset**, are not one hard question but several well-formed ones.
> Split rather than search. **And when the split lands on a union rather than a partition,
> unbundle before searching again.*** · *THEN it is two questions, not one, and **their
> instruments are opposed. Never read one against the other.***

| the summary | what step 7 adds |
|---|---|
| *does not shrink with effort* | **and each rule works well on a DIFFERENT SUBSET** — the trigger is competitive, not just flat |
| — | **unbundle when the split lands on a union rather than a partition** — a second operation |
| — | **the output is INWARD / OUTWARD, and their instruments are OPPOSED** |

### 2 · THE OUTPUT IS NEITHER RESIDUALS NOR GOALS — it is a fork between two REMEDIES

    INWARD   is our representation adequate to hold it?  Extend the instrument.
    OUTWARD  does another frame already hold it?  IMPORT.

**So §16.7's trap is not the falsifier here** — step 7 emits a **routing decision**, and
emitting a goal would be the trap, but the nearer failure is Figure 9's: *some unreachability
is depth and some is genuine absence, and **from inside the frame the two look the same***. **A
split that concludes OUTWARD has made a claim about absence the frame cannot make.**

### 3 · NEAR-DECOMPOSABILITY ALREADY LICENSED A SPLIT, AND IT IS SPENT

§12.1 files it under **ALREADY THE LOOP**: *near-decomposability — **the licence for per-slot at
all.** Simon 1962, and it is already the ground under `perception.py`.* **The world factoring
into sparsely interacting parts is why `R` is indexed per slot.** So it does not license
splitting a search; **it licensed the split the architecture already has**, and adding it again
would duplicate the loop inside the loop.

### 4 · THE TRIGGER'S QUANTITY EXISTS AND IS DESTROYED BY A SUM

**`_left(term, slot, hist)` returns a FLOAT** — it loops the history accumulating bits and
returns the total. **The trigger needs *which observations each candidate got right*, and the
sum is exactly what destroys that.**

> **Two candidates each explaining a different subset is INVISIBLE to a scalar.** `_left` is
> computed per candidate on every mint and thrown away, so the split's input is produced and
> discarded on every cycle.

**Which is the day's shape once more: an aggregate hiding the structure the mechanism needs.**
The repair is small — `_left` returning the mask alongside the total — **and it is a
precondition rather than the mechanism.**

**And the loop's existing responses are all *one hard question*:** abstain, park, search
deeper. ***None of them is "this is not one question."***

**NOT BUILT.**

---

# THE READER'S FIRST READING WAS 95% DEFAULT BINDING — and the cause is a NINTH site

    idn      held-then-stopped        104   |   minted   held-then-stopped     6
    idn      never-held                 9   |   minted   never-held           12
    idn      closed-once-then-failed    2   |   minted   never-called          1

**`held-then-stopped: 110` would have been quoted as *the room invalidated 110 things*.**
**104 of them are `idn`** — and `idn`'s whole track record is *the slot was static, then it
moved*, which is a fact about slots rather than about terms.

### THE REAL READING IS 19 PAIRS, AND IT BEARS ON THE 42%

**6 held-then-stopped** — genuine staleness, on terms that could carry it. **12 never held at
all**, of 19 minted pairs. *A term that closed once and never held again is visibly different
from one that keeps holding*, and **most minted pairs are in the first group.**

### AND THE CAUSE IS A NINTH TWO-STATE SITE, IN THE ROW ITSELF

    bound=self.bound.get(s, IDN)

**The bet row writes `IDN` both when `idn` IS the bound term and when NOTHING is bound.** So
the record cannot separate ***a hypothesis that this slot does not change*** from ***no
hypothesis at all*** — and 104 pairs are the second wearing the first's name.

> **`_predict` falling back to `IDN` is correct** — the loop must predict something. **Writing
> that fallback to the ledger as if it were a binding is not.** The prediction needs a default;
> **the record needs the difference.**

**Ninth site, and the first one found IN A LEDGER ROW rather than in code that reads one** —
which is why it contaminated a reading built to be careful about exactly this. **The reader
counts three states correctly and the row it reads only has two.**

**AND IT IS NOT THE READER'S TO FIX.** Excluding `idn` in `behaviour.py` would paper over a
record that cannot express the distinction — **the repair belongs at the write, and changing
what a bet row carries is a record-format decision rather than a patch.**

---

# THREE CHECKS ON WHAT A BET ROW CARRIES — and the second one's premise is wrong

### 1 · `no_change` IS NOT A WORD THE CORPUS HAS. And the confidence asymmetry IS

**Nothing names a no-term stance.** `no_change` would be new vocabulary — small, and the
ruling's reasoning is its own justification: **`idn` is a term with a cost and a provenance;
having no term is not.**

**BUT THE CONFIDENCE QUESTION HAS A HALF-ANSWER AND THE ASYMMETRY IS THE FINDING.** The corpus
names **strength of REFUTATION** and not strength of confirmation: `falsified_ledger` is
*weighted, never binary — strength-of-rejection, so the consumer de-prioritises*, decayed over
a **logical clock**; `Standing.rejections` is that, built.

| side | exists |
|---|---|
| **how much a term has been REFUTED** | `Standing.rejections` — weighted, decaying, built |
| **how much a term has HELD** | **`behaviour`'s `held`/`called`, per pair, built today** |
| **the two combined into a confidence** | **nothing, and combining them would be an invented number** |

**So the two sources you named are both real and both present — a term's history of holding
(now computable) and the present residual (`_last_mass`).** **The corpus supports neither being
turned into a scalar**, and *nothing scores itself with a quantity it produces* is the reason
to leave them as two readings rather than one number.

### 2 · A MULTI-STEP BET IS ALREADY EXPRESSIBLE — the premise is wrong, with one condition

**`ARC_AGENT` §2 answers it directly and says the opposite of the assumption:**

> ***It needs no new row type and no contract member.*** *`perceive(action)` calls
> `env.step(action)` once and compares the reading before against the reading after. **It never
> assumes the env took one step.** If an action is a sequence and `env.step` executes it, the
> bet is already over the whole attempt and the residual is already about the whole attempt —
> because **the loop only ever sees before and after.*** · *The intention half is free. **The
> composition half is not** — building `northwest` out of what actions turn out to do is
> composing over a second type, and `Gamma` is typed `val → val`. **A contract question rather
> than a field.***

**SO THERE IS NO MID-PLAN STEP TO MARK — PROVIDED THE ROUTINE EXECUTES AS ONE `env.step`.**

**AND THE ARC ADAPTER DOES NOT MEET THAT CONDITION.** `ArcWorld.step(action: str)` takes one
`GameAction` and calls `w.step` once. **A three-action routine is three bets today**, so the
mid-plan problem is real *here* — **and its repair is an adapter decision (does `step` accept a
sequence?), not a field on the bet row.**

**AND `STRATEGY` ALREADY EXISTS AS AN HONEST ZERO:** *STRATEGY arrives with routines and is 0
until then — an honest zero, not a gap.* **Sixth time the thing being designed already had a
name and a socket waiting.**

> **THE LIMIT STATED PLAINLY, AS ASKED: every reading over bet rows is SINGLE-STEP-ONLY until
> routines execute atomically.** `behaviour`'s counters would score a correct multi-step term
> as `never-held`, and **that limit is now written down.**

### 3 · THE CATEGORIES EXIST AND THE MASK SHOULD REUSE THEM

| the mask's category | the existing vocabulary |
|---|---|
| **objects** | the slot's own attribute — a slot IS `{obj}.{row\|col\|h\|w\|colour}` |
| **movements** | `DELTA` — §12.3 sensor 7, in `sensors.py`'s attribute set |
| **relations** | `contact`, from `habitat` — the only one built; containment is Tier 2 |
| **channel** | `transition` · `reward` · `bracket`, already on every row |
| **why unexplained** | `genuine` · `channel_closed` · `slice_too_small`, already on every row |

**No new taxonomy is needed and inventing one would be the third classification beside `_rtype`
and the affordance profile.** **The attribute is already in the slot NAME**, so the object
categorisation costs a split on `.` and nothing else.

**NOT BUILT.**

---

# BOTH HAVE NAMES, AND THE FIRST CARRIES A CASCADE NOBODY CONNECTED

### 1 · `no_change` IS A PERSISTENCE PRIOR, and `DOCTRINE_AUDIT` §8 already named the defect

**Titled *The identity default is an unstamped prior*, quoting the exact line:**

> `term = self.gamma.library[self.bound.get(slot, IDN)]`
>
> *An unbound slot is predicted to **not change**. That is a **persistence prior** — a real and
> defensible one, and **one of the six loadable shapes.** But it is applied invisibly: **not
> stamped `prior`, not recorded as a choice, not falsifiable.***

**So the ruling is stronger than *record that nothing was bound*.** The fallback is not the
absence of a claim — **it is a prior being applied without entering under the entry rule,
without a stamp, and without being falsifiable.** Recording `no_change` makes an invisible
prior visible, which is a different and better act than noting an absence.

**AND THE CASCADE IS THE PART NOBODY CONNECTED:**

> *For an unbound slot, "residual" means **it moved**, not "my model was wrong" — **there is no
> model.** So **`density(R)` is inflated at the start by every slot that simply changes**, and
> **`bored()` reads that inflated value.***

**One root, two consequences, found six months apart:** the audit found `density(R)` and
`bored()` inflated; **today's reader hit the same root and read 95% noise.** Neither was
connected to the other until now, and **the drive layer's trigger is downstream of it.**

### 2 · THE BOOLEAN-PLUS-EVIDENCE FORM IS `PRICE`, AND IT IS A STUB

`grammar.py`: `PRICE = "PRICE"  # **a cost claim with its evidence count**, or an explicit
null.` **That is the ruled form — a claim, its evidence, and an explicit null — already a type
in the speech grammar.**

**And `DOCTRINE_AUDIT` §9 records it as stubbed:** *`PAY` carries a step count, not a price
... **value and evidence-count are the same number.*** **So the form exists, is typed, is
checked for SHAPE by the gate, and carries nothing.**

**The built instance of the same discipline is `disproof`:** ***presence with a number is an
experiment, absence is a stall*** — **a boolean whose evidence rides with it, never a score.**

### 3 · THE ABORT CASE IS EXPRESSIBLE TODAY, AND THE RECORD FOR IT DOES NOT EXIST

**Every frame carries what the distinction needs:**

    state              NOT_FINISHED · GAME_OVER · WIN    -> the world ended it
    available_actions  the next action gone mid-sequence -> a condition closed
    levels_completed   changed                           -> a level boundary
    full_reset                                           -> the board was replaced

**So *the sequence stopped at step 2 because the world ended it* IS distinguishable from *it
completed and did not work*** — the signals are per-frame and already read by `terminal()`.

> **What does not exist is the record it would go on.** `ArcWorld.step(action: str)` takes ONE
> `GameAction`, so **no sequence executes and there is no outcome row for one.** The third
> state is not missing from the data — **it is missing from a record that has no subject yet.**

**Which makes it `4a`'s to supply rather than a field to add now**, and the constraint is worth
stating with it: **three outcomes, not two — completed-and-failed, completed-and-worked, and
stopped-by-the-world — and the third collapses into the first if nobody asks.**

**NOT BUILT.**

---

# `no_change` BUILT — and the staleness signal is six named terms, not 110

    TERM dispositions  never-held 10 · held-then-stopped 6 · never-called 1 · mixed 2   19 pairs
    persistence prior  held-then-stopped 104 · never-held 9 · closed-once 2            115 pairs
    room-invalidated   idn . translate<o1.h>   @o20.w  @o21.w  @o22.w
                       idn . translate<o12.col>@o21.col @o22.col · <o12.row>@o20.col

**THE SIX ARE NOT SCATTERED — they are TWO TERMS ACROSS SIBLING SLOTS.** `translate<o1.h>`
invalidated on the `.w` of o20, o21 and o22; `translate<o12.col>` on the `.col` of o21 and o22.
**A term failing across a family of slots at once is what a room change looks like**, and under
110 it was invisible.

**AND THE PRIOR'S OWN READING IS KEPT, NOT DROPPED.** `held-then-stopped: 104` on the
persistence prior is a real reading — *the world was still, then it moved*, 104 times — and
`DOCTRINE_AUDIT` §8 is right that it is *a real and defensible prior*. **What was wrong was
reading it as a term's track record**, not recording it.

**AND THE CASCADE IS NOW EXPOSED RATHER THAN REPAIRED.** The audit's *`density(R)` is inflated
by every slot that simply changes, and `bored()` reads that inflated value* is **the same 104**,
seen from the drive layer. **The row now names the prior; nothing yet stops it inflating
`density(R)`** — the record is fixed and the cascade is not.

---

# `PRICE` CHECKED — the refusal it promises does not exist, and cannot at the current write

### 1 · THE TYPE IS RIGHT AND ONE CALL SITE IS ALREADY CORRECT

`grammar.py`: `PRICE = "PRICE"  # a cost claim with its evidence count, or an explicit null`,
and `price(value, n, reason)`. **The two callers differ:**

    G.price(float(len(self.trace)), len(self.trace))    <- the stub: value == n
    G.price(None, None, "explicit-null: nothing bound") <- CORRECT, and already there

**So the explicit-null path is built and used.** The defect is one call site, exactly as
`DOCTRINE_AUDIT` §9 says: *value and evidence-count are the same number.*

### 2 · BUT THE GATE REFUSAL IT PROMISES DOES NOT EXIST

**`price`'s own docstring:** *"A number without evidence is representable here and **refused at
the gate**."* · **`DOCTRINE_AUDIT` §9:** *"a stub in a slot **the gate checks the shape of** but
not the meaning of, so it passes."*

> **`gate.py` contains no reference to `PRICE` and none to utterances. `grammar.py` has no
> type-check or validator.** The gate checks **neither** shape nor meaning. **The stub passes
> because nothing looks at it.**

### 3 · AND IT COULD NOT, BECAUSE THE UTTERANCE IS FLATTENED AT THE WRITE

    self.led.record(..., "utterance", kind=kind, id=uid, text=repr(term), heads=[...])

**`text=repr(term)`.** A `PRICE` leaf with a value and no evidence arrives at the ledger as
**characters inside a string** — `"PAY(PRICE(4.0, 4, None))"` — and nothing can inspect it.
**The structure is destroyed before the record exists**, so filling the stub changes what is
computed and nothing that is checked.

**Which is the day's shape at the level of a whole subsystem: the record cannot express what a
check would need**, and here the promise of the check is written into the producer's docstring.
***A guarantee that reads as enforced and is not*** — `_bindings`' shape, in the grammar.

### 4 · ⚠ CORRECTION TO MY OWN REPORT: the utterance layer IS checked, at the right site

**I said *the whole utterance layer is unchecked*. That is wrong.** `DISCOVERY` Q4 puts the
refusal at construction, not at the ledger:

> ***PARSE, which precedes all three: an ill-typed utterance is refused at the head before any
> currency is charged.*** · *`compose()` **raises with its reason, never silently.** An
> ill-typed utterance is a refusal with a named head, not a shrug.*

**And `compose()` does exactly that** — `raise Ill(f"ill-typed: {head} expects {want} but got
{got}")`, plus `_check_terminal`. **The type layer is checked where the corpus says, and it
works.**

**SO THE GAP IS NARROWER AND SHARPER: `compose` checks TYPE, and *a number without evidence* is
a CONTENT claim.** `price(4.0, 4, None)` and `price(4.0, None, None)` are **both well-typed
`PRICE` leaves** — the type system cannot separate them, by construction. **A type-checked
grammar was never going to catch this**, and the docstring names the wrong site *and* the wrong
kind of check.

| the docstring claims | the truth |
|---|---|
| refused **at the gate** | the gate never sees it; `compose` does |
| refused for **having no evidence** | `compose` refuses ill-TYPING; this is well-typed and empty |

### ⚠ AND I REPEATED THE AUDIT'S CLAIM WITHOUT CHECKING IT

**I reported *the gate checks its shape* an hour ago, taken from §9.** **Third time today I
have repeated an unverified claim out of a document** — after *split before search is not in
the corpus* and *the record cannot distinguish held-then-failed*. **All three were checkable in
one grep**, and the pattern is the same each time: **a document's statement about the code,
carried forward as if it were a reading of the code.**

### 5 · BUILT — the content rule, at the site the content is assembled

    value + evidence     accepted
    explicit null        accepted
    value, NO evidence   REFUSED: PRICE carries a value with no evidence count
    null, NO reason      REFUSED: a null PRICE must be EXPLICIT -- state the reason

**Not in `compose`, and not in the gate.** `PAY` is a Speech-act prime rather than a terminal,
and more to the point **the check is not a type check** — so it goes where the content is
assembled, and a malformed `PRICE` leaf becomes **unconstructible** rather than refused later.

**BOTH HALVES COME FROM THE TYPE'S OWN DEFINITION.** *A number **with its evidence count*** →
a value requires `n`. *Or an **explicit** null **with a reason*** → a null requires the reason
that makes it explicit. **An unexplained null is the same defect in the other direction**, and
it was representable before.

**And the docstring's false guarantee is replaced by the true one**, with both errors named:
it claimed *refused at the gate* where the gate never sees an utterance, and it claimed a
refusal for missing evidence where `compose` refuses only ill-TYPING.

### 6 · AND IT DOES NOT FIX §9's ACTUAL COMPLAINT — said plainly

**`G.price(4.0, 4)` is still accepted, and the live caller is
`G.price(float(len(self.trace)), len(self.trace))`.** §9's defect is ***value and
evidence-count are the same number*** — **a step count wearing a price** — and that is
**well-formed under this rule and always will be**, because a price may legitimately equal its
evidence count and a rule forbidding it would be arbitrary.

> **The rule catches an unevidenced number. It does not catch a number that is the wrong
> quantity.** §9 needs `PAY` to have a price to carry, and **nothing computes one** —
> *Figure 8's surplus accounting has no real input.* **That is a different item and it is not
> closed by this.**

---

# `4a` CHECKED — and the check found a defect in the type system `4a` would extend

### 1 · §15.5's CLAIM IS ABOUT THE PRIMES, AND THE TYPE SET DOES NOT SUPPORT THEM

**§15.5 is exact and its mapping is a lookup:** `Act(a)` → **DO, MOVE, HAPPEN** · `Seq` →
**BEFORE, AFTER** · `When` → **IF** *(`BECAUSE` is causal, not conditional — a different
prime)* · `Until` → **FOR SOME TIME + NOT** · the guard → **CAN, which is already there.**
*The routine algebra is not a new language. It is the missing third of the one already chosen.*

**But every one of the thirteen primes produces `PRED` or `OBJ`, and the type set is
`OBJECT · ATTR · REGION · PRED · OBJ · RECORD · PRICE`. There is no ACTION and no ROUTINE.**
So `DO` has nothing to take and `Seq` has nothing to take or return.

**§2622 named the same gap from the other side**: *composing over a second type — actions
rather than values — and `Gamma` is typed `val → val`. **A real extension, and a contract
question rather than a field.*** **Two sections, one conclusion: `4a` needs a type before it
needs a prime.**

### 2 · AND `OBJ` ALREADY MEANS TWO THINGS, IN ONE FILE

`arc_atoms.py`:

    _extract()   Atom(k, pick(k), OBJ, ATTR)    OBJ -> ATTR    OBJ is AN OBJECT
    _quantify()  Atom("all", ..., PRED, OBJ)    PRED -> OBJ    OBJ is AN OBJECTIVE

**`grammar.py` keeps them apart** — `OBJECT = "a slot's identity"` and `OBJ = "a complete
objective"` — **and `arc_atoms` uses one constant for both.** So the type graph has a node that
is two things, and **`λ = 3.0` over 4 nodes was measured on it.**

**MEASURED, NOT ARGUED:**

    depth 3   0 pipelines cross the conflated node
    depth 4   225, the first being  `colour . same . all . colour`

***Read a colour, compare it, quantify to an OBJECTIVE, then read a COLOUR OFF THE
OBJECTIVE.*** Well-typed, meaningless, and the type system exists to refuse exactly this.

**IT IS LATENT AT `max_depth = 3` AND NOT ABSENT** — and the depth that hides it was anchored
to *the toy world's chunking falsifier*, **for an unrelated reason.** *(Chunking composes over
UNITS, so a settled 2-atom chunk reaches 4 atoms at depth 3 — whether a chunk path crosses this
node is **not verified here**, and the structural possibility is stated rather than claimed.)*

> **A6i, in the type system `4a` would extend, found by checking `4a` before building it.**
> Adding verbs to a graph with a conflated node compounds it — and **the node is the one
> `QUANTIFY` produces, which is exactly where routines attach.**

### 3 · λ SURVIVES THE SPLIT — and checking that found λ ITSELF IS WRONG

**Measured in memory, without building the split:**

    conflated (as built)   V=14  lambda=3.5569  types=4   depth-4 crossings=225
    OBJ split              V=14  lambda=3.0     types=5   depth-4 crossings=0

*(Both λ figures re-measured after the shift fix below. The first reading of this table said
**3.0 for both**, which is what a broken instrument looks like when it is asked to compare.)*

**So the Stage 1 answer stands** — and the reason it stands is not the reassuring one.

    TRUE spectral radius : 3.5569        the 3-cycle (5*3*3)^(1/3) = 3.5569
    type_report reports  : 3.0000

**`type_report` NORMALISES BY MAX-NORM, AND POWER ITERATION DOES NOT CONVERGE ON A PERIODIC
MATRIX.** The conflated graph is a **3-cycle** `OBJ→ATTR→PRED→OBJ` (period 3) **plus an
aperiodic `val` self-loop** — so the iterate oscillates on the cyclic block and the reported
value settles on the self-loop's 3.0. **The missing 0.557 is exactly the cycle.**

**AND THIS IS THE QUANTITY THE STAGE 1 FALSIFIER WAS ANSWERED WITH.** `CLAUDE.md`'s citation
table names it exactly: *typing beats size, as a number — **spectral radius** of the type
transfer matrix, standard analytic combinatorics.* **The specified instrument is the spectral
radius; the implementation computes something else whenever the graph has a cycle.**

> **THE CONCLUSION SURVIVES AND THE NUMBER DOES NOT.** `λ < V` reads 3.0 < 14 and 3.56 < 14 —
> **`3b`'s finding holds.** But *the falsifier stopped firing for the first time in the
> project's life* was reported with a number that is wrong on the graph it was measured over.

**AND THE SPLIT REPAIRS IT AS A SIDE EFFECT — AND BUYS A THIRD THING NOBODY COULD SEE.** With
the cycle broken the matrix is acyclic plus one self-loop and 3.0 is correct. But re-measured
with the fix, **the split LOWERS λ: 3.5569 → 3.0.** So it buys **225 meaningless pipelines
removed, λ made computable, and a real reduction in the search's growth rate** — and **the
third was invisible under the broken instrument, which reported 3.0 for both and made the split
look free.**

> **A broken instrument does not only misreport a value. Asked to COMPARE, it reported no
> difference where there is one** — which is the failure mode that would have retired the
> split as *no measurable benefit*.

**AND IT IS NOT THE TWO-STATE COLLAPSE, THOUGH THE SYMPTOM IS IDENTICAL.** Two distinct states
reading as one is the same *appearance* — but **every one of the nine sites is a REPRESENTATION
that cannot hold the difference**: a guard's subject, a key, a signature, a field, a stamp.
**Here the representation is a float and holds `3.5569` perfectly well. The collapse is in the
COMPUTATION.**

**Grouping them would be the four-classes error again** — a resemblance made into a class on the
same day the correction was recorded. **Filed as distinct, at n = 1**, with the sharper
statement of what makes it worse than a wrong number:

> **A wrong value is a wrong value. A COMPARISON returning *no difference* reads as a
> FINDING** — so the instrument was about to make a decision, not merely report badly, and the
> decision would have been **to skip a repair that buys three things.**

**Bar: a second instance where a broken computation, not a broken representation, returns a
false null on a comparison.**

**AND THE λ DEFECT IS SEPARABLE AND SHOULD BE FIXED ANYWAY.** The split removes *this* cycle;
**`4a`'s own primes could reintroduce one** — `When(PRED, ROUTINE) → ROUTINE` with any routine
producing a `PRED` closes a loop. **A λ that is silently wrong on cyclic graphs is a defect in
the instrument, not in this graph.**

### 4 · BUILT — the `OBJ` split, across all three files that meant it

    before   V=14  lambda=3.5569  types=4   depth-4 crossings=225
    after    V=14  lambda=3.0     types=5   depth-4 crossings=0

**`arc_atoms` now takes `OBJECT` into EXTRACT and yields `OBJ` from QUANTIFY** — the line
`grammar.py` had drawn all along, where `OBJECT` is *a slot's identity* and `OBJ` is *a
complete objective*.

**AND `sensors.py` WAS RENAMED WITH IT, because it had the same constant meaning the same
thing.** Leaving it would have kept `OBJ` meaning *object* in one file and *objective* in
another — **the collision half-repaired, which is how it comes back.** All three files now mean
one thing by each word.

**The fixture reads `lambda, three spaces: 3.0 < V 14.0, **5 types**`** and the nine sensors
still resolve. **Stage 1's two readings both stand**: `λ = V = 3.0, 1 type` for the single
space (the falsifier firing), `3.0 < 14.0, 5 types` for the three (it not firing).

**Two of `4a`'s four parts are done — λ's computation and the split — and both were repairs to
things already built, checkable against readings that already existed.** What remains is
**ACTION and ROUTINE**, which is the contract question §2622 named, and then **the six primes,
which are a lookup and already exact.**

---

# THE CONTRACT QUESTION IS BIGGER THAN A TYPE — ARC HAS NO ACTION-READING ATOM AT ALL

    action chosen BY   : {'draw': 82, 'probe': 38}      no 'discriminate', ever
    rows with disproof : 0
    phases             : probe 1.0   directed 0.0   strategy 0.0

**§2622 measured what this costs, in the toy world, before it was built here:**

    spread distinguishes the actions, with `act`    33/96   (34%)
    spread distinguishes the actions, without `act`  0/96   ( 0%)

> ***`choose`'s discriminate branch is a property of the atom set, not a model the agent
> built. Remove that one atom and the agent cannot tell its actions apart at all. It has never
> had to learn what pressing something does, because the primitive it was given already knew.***
> **That is the thing the action world has to take away.**

> **⚠ AND THE PANEL THIS WAS MEASURED ON IS THE WEAK END, established afterwards by the
> screen: `ls20` has EVERY action distinct and NOTHING inert — the corpus's *still encoded*
> case. So `0 discriminating draws` was taken on the board least able to reward action
> learning.** It does not invalidate the gap — **the agent still could not tell four distinct
> actions apart** — but the number is weaker than it looked and the caveat belongs here rather
> than in the screen's section.

**ARC IS ALREADY THAT WORLD, BY ACCIDENT.** `arc_predict`'s three atoms — `idn`, `translate`,
`recolour` — **all read operands and none reads `c.action`**, because they were derived from
the corpus's six grid transforms and the corpus's list has no action-reader in it. **The thing
§2622 says has to be taken away was taken away this afternoon and nobody noticed.**

### AND THE PHASE READING WOULD HAVE BEEN THE WRONG DIAGNOSIS

**§22.2's phase curve was recorded as *available and never plotted*. It is now plotted, on a
real board: probe 1.0.** And §22.2's own reading of that is ***random still dominant late → it
never left phase 1, nothing is being modelled.***

**THAT WOULD BE FALSE.** Seven terms minted on this run. **The agent models slots and never
ACTS to discriminate**, because `DIRECTED` is a property of how the ACTION was chosen, not of
whether anything was modelled. **A phase histogram at 100% probe with a live mint rate is a
different state from phase 1**, and the curve alone cannot say so.

### ⚠ ONE CAUSE, NOT TWO — I RECORDED A SECOND AND IT IS WRONG TWICE OVER

**Recorded minutes earlier as *two causes point the same way*. Corrected on reading the CODE
rather than the audit.**

**THE ONE REAL CAUSE.** `choose`'s discriminate branch computes spread over candidate
predictions; **with no atom reading the action, every action predicts identically** and the
branch cannot fire. **`0/96` is the corpus's own measurement of exactly this.**

**THE SECOND WAS NOT A CAUSE OF THIS READING, AND ITS DIRECTION WAS BACKWARDS:**

    note_step(any_live):  self.live = any_live
    bored():              return self.n > 0 and not self.live

- **It does not touch the phase histogram.** `phase = DIRECTED if by == "discriminate" else
  PROBE`, so `by='draw'` — **82 of 120** — counts as PROBE too. **The 1.0 is entirely about
  discrimination never firing**; `bored()` is not in it.
- **And the direction is inverted.** `bored()` is true when **NOTHING** carried live mass, so
  inflating `density(R)` with slots that simply change makes `any_live` true MORE often →
  `bored()` fires **LESS** → **fewer probes, not more.**

> **`DOCTRINE_AUDIT` §8 says *`bored()` reads that inflated value* and does not say which way
> it moves. I supplied the direction and got it backwards** — the fourth time today a
> document's statement was carried forward **with something added that the document did not
> say.**

**The persistence-prior cascade is still real and still open. It is NOT a cause of the phase
reading**, and pairing them would have aimed a repair at a symptom it does not produce.

**SO THE CONTRACT QUESTION HAS A MEASURED MOTIVATION RATHER THAN A CITED ONE.** Not *the corpus
says add verbs* — **the agent cannot tell its four actions apart, measured, and `DO` is the
prime that would let it.**

---

# THE ACTION WORK SPLITS IN TWO, AND THE CORPUS PRE-REGISTERED ITS VACUITY CHECK

### 1 · READING AN ACTION NEEDS NO TYPE. COMPOSING OVER ONE DOES

**`Ctx.action` already exists** — *what an atom may read: `action`, `operands`* — and the toy
world's `act` reads it today. **So an action-reading ARC atom is `Atom(name, fn, "val",
"val")` and needs nothing new.**

> **The contract question §2622 names is only about COMPOSING over actions** — `Seq` producing
> a compound action — **which is routines.** *The intention half is free; the composition half
> is not.*

**Which separates the item: the measured gap — 0 discriminating draws in 120 cycles — is fixed
by an atom, not by the contract decision.** They were one thing an hour ago.

### 2 · BUT §5 PRE-REGISTERS THE VACUITY CHECK, AND IT BINDS BEFORE ANY OF IT

> *If motor learning does not fire, that has two readings and **they must be separable BEFORE
> the run**: **the mechanism does not work** ← a result · **this world could not have shown
> it** ← vacuous.*
>
> **This world can show it only if all three are present and reachable:**
> *an actuator whose effect is discoverable from the record alone* · *an actuator that **does
> nothing**, so `useless` is a finding the agent can reach* · *two actuators that are
> **indistinguishable**, so `I cannot tell these apart` is reachable.*

**And the encoding clause with it:** ***an unlabelled action set where every action does
something distinct and useful is still encoded. Most should do nothing or nothing detectable.
Finding that out is the work.***

### 3 · `controlled()` IS THE INSTRUMENT FOR THIS — AND IT CANNOT ANSWER TWO OF THE THREE

**It pairs every action against the FIRST one**, not against each other:

    other = sorted(prior)[0]        # 1v2, 1v3, 1v4 -- never 2v3, 2v4, 3v4

**So `ls20`'s reading of *3 pairs, 3 discriminating* says ACTION1 differs from each of the
others. It says NOTHING about whether 2, 3 and 4 differ from each other** — which is exactly
*two actuators are indistinguishable*, the third required property.

> **A gap in my own instrument, at precisely the property the corpus demands be checked before
> the run.** `n−1` pairs where the check needs `n(n−1)/2`.

**AND `an actuator that does nothing` IS UNTESTED TOO** — a pair records that two actions
*differ*, never that one action *changes nothing*, which needs the before/after of a single
action rather than a comparison of two.

**So the vacuity check cannot be run today**, and running motor learning without it would
produce a null with two readings and no way to separate them — **which §5 says must be
separable BEFORE the run.**

### 4 · BUILT, AND THE VACUITY CHECK RETURNS **FALSE**

    pairs 6  discriminating 6            n(n-1)/2 = 6, where the old instrument formed 3
    discoverable effect : ACTION1 ACTION2 ACTION3 ACTION4
    does nothing        : NONE
    indistinguishable   : NONE
    ALL THREE PRESENT   : False

**`ls20` CANNOT SHOW MOTOR LEARNING IN §5's SENSE.** Two of three required properties are
absent: **no action does nothing**, so `useless` is not a finding the agent can reach; **no two
are indistinguishable**, so `I cannot tell these apart` is not reachable.

**AND THE CORPUS'S OWN CLAUSE IS THE DIAGNOSIS:** ***an unlabelled action set where every
action does something distinct and useful is STILL ENCODED. Most should do nothing or nothing
detectable. Finding that out is the work.*** **All four of `ls20`'s actions do something
distinct** — so by the corpus's standard there is nothing about *which ones don't matter* to
discover.

> **So a motor-learning null on `ls20` would be VACUOUS, and §5's whole purpose is that this be
> known BEFORE the run.** It is now known before the atom exists.

**AND THE OLD READING WAS NARROWER THAN IT SOUNDED.** *3 of 3 discriminating* this afternoon
was **1-versus-each**, and it read as completeness. **6 of 6 is the same board saying something
strictly stronger**, and only the completed instrument could ask the question §5 requires.

**THE LIMIT ON THIS READING, STATED:** four trials from the **initial board only.** A later
board may gate actions differently — §16.1's *`available_actions` changes per frame* is exactly
that — so **`does_nothing` and `indistinguishable` are unreachable HERE and not proven
unreachable in `ls20`.** The check is over one state.

**NOT BUILT beyond the instrument. The atom's validation cannot be `ls20`'s action set as it
stands**, and that is a panel finding rather than a reason not to build the atom.

---

# THE PANEL SCREEN — two of 25 boards can show motor learning, and the decision dissolves

    game   pairs  disc  inert  same
    g50t   10     7     3      3     <-- ALL THREE
    sk48   10     9     2      1     <-- ALL THREE
    ls20    6     6     0      0     the board everything has been measured on
    lf52   10     0     0     10     all four actions IDENTICAL at the start
    sc25    6     0     4      6     four inert, every pair indistinguishable

**§2622 §5's three properties, screened across every game the anonymous key exposes.**
`g50t` is the strongest — **3 inert, 3 indistinguishable, 7 discriminating** — so each
property is well-represented rather than marginal.

> **So the choice between *find a board* and *build the action world* had a third answer, and
> it was one measurement away.** §2622 §4's action world is still specified and still
> unscheduled; **it is no longer the only route.**

### WHY SELECTING ON THIS IS NOT ENCODING, STATED BECAUSE PANEL CHOICE IS WHERE IT HIDES

**The screen reads STRUCTURE ONLY** — does an action change anything, do two actions differ.
**No rule, objective, or mechanic is read**, and the instrument is the one already behind
`controlled()`.

**And the property selected on is the SHAPE OF THE QUESTION, not its answer.** *Some actions
are inert* does not predict whether the agent will do well; **it makes `useless` a reachable
FINDING.** That is §5's own criterion — *this world can show it only if all three are present*
— so selecting for it **is the check, not a thumb on it.** A board chosen because the agent
scores well there would be the other thing.

### AND THE SCREEN SAYS MORE THAN ITS HEADLINE

**`lf52`: 10 pairs, ZERO discriminating, 10 indistinguishable** — at the initial board **all
four actions do exactly the same thing.** **`sc25`: four inert, every pair indistinguishable.**
**And `ls20` — the board every reading today was taken on — is the opposite extreme**: every
action distinct, nothing inert, which is the corpus's *still encoded* case.

**THE LIMIT, UNCHANGED: initial board only, six trials.** `available_actions` changes per
frame (§16.1), so **a board reading zero here is not proven to lack the properties later.** A
positive is strong; a negative is *unreachable at the start*.

---

# ⚠ THE ATOM IS NOT SEPARABLE FROM THE PRIMES — my ordering an hour ago was wrong

**I split the action work into *an atom, which needs no contract decision* and *the contract
question*. Checking what such an atom could COMPUTE reverses it.**

### THE SPECIFIED FORM IS A PARAMETERISED FAMILY, AND THE CORPUS SAYS SO TWICE

§13's channel table: ***action-set growth → new operators → **yes — atoms, straightforwardly.
The closure expands.**** · §1093: a **parameterised atom family**, `HAS_COLOUR(c)`, extended
when the domain grows. **So: one atom per advertised action, growing with the action set.**

### BUT AN ATOM CANNOT LEARN, AND THAT IS THE WHOLE PROBLEM

The toy world's `act` is `v + DELTA.get(c.action, 0)` — **the effects are a table closed over
at construction**, which §2622 names as the handout to remove. **Without the table, an atom
reading `c.action` has nothing to return**: an atom is a fixed function, so any per-action
output it produces IS a mapping, handed.

**To predict differently per action without being told the difference, exactly one of three
must be true:**

| | |
|---|---|
| **an atom hands the mapping** | the toy world. **The thing to remove** |
| **binding becomes per (slot, ACTION)** | `self.bound: dict[str, str]` is **keyed by slot alone** — a contract change |
| **conditional composition exists** | *IF action was A, then transform* — **and `IF` is one of §15.5's six primes** |

> **The corpus names the third.** `When(P, R)` → **IF**, in the constructor table. **So the
> action atom is useful only once conditional composition exists, and that is the primes.**

**AND A GATE ATOM DOES NOT SUBSTITUTE.** `under_A(v, c) = v if c.action == "A" else 0` returns
**0** on a non-match — a specific wrong prediction, not *no claim*. Atoms compose sequentially,
so there is no additive branch to hide it in. **The gate needs `IF`'s semantics and cannot
approximate them.**

**SO THE ORDER INSIDE `4a` IS: the primes (with `IF`), THEN the per-action atom family** — and
the measured gap does **not** get fixed by a smaller piece first. **The two items I separated
an hour ago are one item, and separating them was the error.**

---

# THE CONTRACT QUESTION RESOLVES FROM THE CORPUS — and there are FOUR spaces, not three

### 1 · ROUTINES DO NOT EXTEND `Gamma`. §985's TABLE SAYS SO OUTRIGHT

> *The whole composition story, stated once:*
>
>     space     object    composes by                   priced against
>     SENSE     sensor    prime(extractor, extractor)   discriminability
>     PREDICT   term      chaining + chunking            transition residual
>     ACT       routine   Seq / When / Until             goal residual
>
> *One bargain across all three — `|φ| + |R|φ| < |R|`.*

**Three spaces, three COMPOSERS, three PRICES, one bargain.** **PREDICT composes by chaining —
that is `enumerate_closure`, `val → val`. ACT composes by `Seq / When / Until`, which is not
chaining and not `Gamma`.**

> **So §2622's *composing over a second type* is not an extension of `Gamma`'s closure.** It is
> **a different space with a different composer**, priced against the goal residual — which is
> Q21, already SETTLED. **The contract question resolves by reading rather than by ruling.**

### 2 · AND "THREE COMPOSITION SPACES" NAMES TWO DIFFERENT TRIPLES

    §11.2   PREDICT · RELATE/QUANTIFY · EXTRACT      "we have one and a half"
    §985    SENSE   · PREDICT         · ACT          "the whole composition story"

**They overlap on PREDICT, and on EXTRACT/SENSE** — §11.2 names the extractors
(`grid × object → ATTR`), §985 composes sensors **from** extractors, **the same space at two
levels.** *(Identification stated so it can be disputed: if they are distinct, the union is
five rather than four.)*

**§11.2 has no ACT. §985 has no RELATE/QUANTIFY. So the union is FOUR and each table shows
THREE.**

> **SECOND INSTANCE OF THE TWO-TABLES SHAPE, in the same document as the first** — after
> *the seven shapes from §12.1* which were eight. **Both tables read as complete; neither is;
> and each omits what the other's third member is.**

### 3 · WHICH MEANS `3b` BUILT §11.2's TRIPLE AND `4a` NEEDS §985's THIRD

`arc_atoms.three_spaces()` is **EXTRACT + RELATE + QUANTIFY joined to PREDICT** — §11.2's,
correctly, and that is what `3b` was. **ACT is a space nobody has built, with its own composer
and its own price**, and it is where routines live.

**So `4a` is not an extension of `3b`'s work. It is the fourth space.** And the ordering
inside it stands: **the primes (with `IF`) are the composer for that space, and the per-action
atom family needs `IF` to be useful.**

---

# WHERE *FOUR ACTIONS* COMES FROM — and a quarter of the panel is invisible to the agent

**Asked because the number had been repeated all day without being checked. Two answers, and
both matter.**

### 1 · ON `ls20` THE FOUR ARE THE GAME'S — and the advertised set never changes

`ls20` advertises **`[1, 2, 3, 4]`**, all simple, no RESET. **The adapter drops nothing there**
and both its filters are no-ops. And over 120 steps: **one distinct advertised set, zero
changes.** So on this board *four* is `ls20`'s figure, not the agent's.

> **AND THAT IS ITSELF A PANEL PROPERTY NOBODY HAD.** §16.1 calls the action-set delta *a
> causal readout with no perception at all* — *the previous action changed the world's
> gating.* **On `ls20` that channel is empty for 120 steps**, so the precondition lattice has
> had nothing to read, on the board every measurement was taken on.

### 2 · ACROSS THE PANEL THE ADAPTER DROPS `ACTION6`, AND IT BITES 19 OF 25

    19 of 25   advertise ACTION6, and it is dropped in every one
     6 of 25   advertise ONLY ACTION6 -> the adapter surfaces NOTHING
     6 of 25   no drop:  g50t · ls20 · re86 · tr87 · tu93 · wa30

**The drop is a stated decision, not a default:** *`ACTION6` is complex and carries `x, y` — a
POSITIONED action, §17.1's arity question and `2c`'s to answer. **Advertising it here without
the position would be advertising an action the loop cannot actually take.*** **The reason is
sound and the consequence was never stated.**

> **AT THE INITIAL FRAME, SIX GAMES ADVERTISED ONLY `ACTION6`, so the adapter surfaced
> nothing.** `ft09` · `lp85` · `r11l` · `s5i5` · `tn36` · `vc33`.

**⚠ AND *A QUARTER OF THE PANEL IS UNPLAYABLE* IS ONE SCOPE TOO WIDE — corrected.** What was
measured is **one state, at step zero, before anything happened.** And `available_actions`
**changes per frame** — the check established that this afternoon — so *these games offer only
that action* is **a claim about a whole game from a single observation.** **The collapse
catalogued ten times today, made in the summary of the finding that catalogued it.**

**WHAT SURVIVES, WHICH IS STILL THE POINT:** the adapter **drops `ACTION6` on every frame**,
because a positioned action has no position to supply — **so the agent cannot take a positioned
action on any board at any frame.** That is frame-independent and it is the fact. **What is not
established is that the six stay empty**; an action could become available later, and
**assuming either way is the error.**

### 3 · ⚠ AND THE SCREEN'S ZEROS WERE NOT READINGS

**Those six read `0 pairs, 0 disc, 0 inert, 0 same` in the panel screen and I tabulated them
beside real measurements.** They are not *this board has no discriminating actions* — they are
**this board has no actions**. **A row of zeros meaning ABSENCE OF INSTRUMENT, printed in a
column meaning ABSENCE OF EFFECT.**

**The selection survives**: `g50t` has **no drop**, so its all-three reading is over its full
advertised set. **`sk48` drops `ACTION6`**, so its reading is over a subset and it is the
weaker of the two.

### 4 · WHICH REPRICES `2c`

**Positioned actions are outside every measurement taken today**, and §17.1's arity question
is not a refinement — **it is the difference between six of twenty-five games being playable
and unplayable**, and between the agent ever being able to express *reach the anchor, then
act*.

---

# `Agency`'s CONSUMER — the corpus answers, and it first refuses the sensor

### 1 · `Agency` IS §16.2's SINGLE DETECTOR, AND §16.2 IS AMENDED IN ITS OWN HEADING

`### 16.2 Avatar or actuator is a per-step read, never a label · **⚠ AMENDED BY §18.3**`

**`Agency`'s docstring cites §16.2 and not the amendment.** And §18.3's correction is explicit:

> ***Correction to §16.2: control-mode detection is a FAMILY with an independence requirement,
> not a single correlation test.*** *A family of four **translation-flavoured** detectors would
> not have helped: **their failure modes are correlated, so they fail together on the same
> games.*** · *Four correlated detectors are **one detector wearing four names**, which is
> collapse 2 inside the perception layer.*

    TranslationSelf   a rigid object that moves
    GrowthEdgeSelf    a growing / advancing trail
    ValueLatentSelf   non-spatial -- a scalar, a colour's total count
    RegionToggleSelf  a bounded region that genuinely alternates

**`Agency` is one test** — *a slot is action-contingent when some action has always moved it
and some other never has.* **Correct as a predicate, and the amended-away design.**

> **AND IT WAS REFUTED ON `ls20` SPECIFICALLY.** *The first live `ls20` test refuted the
> keystone's single instantiation: **`has_self: false` for 904 steps**, because the forward
> model looked for ONE thing — a rigid object that translates — and **`ls20`'s self does not
> translate. It is a growing/advancing trail.*** **The board every measurement today was taken
> on is the board that refuted the single detector.**

### 2 · AND §18.4 ANSWERS THE CONSUMER QUESTION, AS A MEASURED FAILURE

> *The live `ls20` test proved the sensorium had become **DIAGNOSTIC-ONLY**: it found the
> right self and **changed nothing**, because **the only consumer of perception was the
> post-hoc veto**, which has no legal move at an all-directions-fatal board. **Perception has
> to enter the PROPOSER, not just what it forbids.***

**So: the PROPOSER — what the agent TRIES — and explicitly not a veto or a filter.** Of the
three candidates, **the probe's choice of action is proposer-side and admissible**; the contact
cascade's ranking is proposer-side too; **§16.5's habitat enumeration is perception-side and
would make it diagnostic again** — *found the right self and changed nothing* is that failure,
measured.

**And *the drive* was right to hold back**: the drive is where a veto-shaped consumer would sit,
and §18.4 names exactly that as the thing that changed nothing.

### 3 · A PER-STEP READ CAN BE CONSUMED — AS A DECAYING ESTIMATE, NEVER A CLASSIFICATION

§16.2 forbids a **label**; §18.3's family is *each priced by its own ground-facing residual and
**selected by EWMA***. **An EWMA is re-selectable every step and decays** — so it is a
preference that can be overturned, not a classification that persists. **That is the corpus's
own form, and it is the constraint stated before anything reads it:** a consumer may hold a
decaying estimate; **holding a decision is the label §16.2 forbids.**

**SO THE ORDER IS: the family before the consumer.** Consuming `Agency` as built would wire a
decision to a detector the corpus corrected, **on the board that produced the correction.**

### 4 · AND IT IS NOT *BUILT, NO CONSUMER*. IT IS *SUPERSEDED, NO CONSUMER*

**A different item, and the difference decides what happens to it.** `touching`, `Affordances`
and `terminal()` were **correct mechanisms waiting** — each was wired the day a consumer
arrived, unchanged. **`Agency` is fed every step** (`self.agency.note(...)` in `perceive`) and
**its reading is never taken** — and if it were taken, the reading is the one §18.3 corrected.

> **So it does not join the four on the consumers-waiting list.** Wiring it is not the fix;
> **replacing it with the non-simulable family is**, and the family's members are named
> already. **`Agency`'s accumulation may survive as one member — `TranslationSelf`'s
> neighbour — and it cannot be the whole detector.**

**And the refutation was in the record the whole time.** *904 steps of `has_self: false`* is a
measured result about `ls20`, sitting in §18.3, **while every reading today was taken on
`ls20`.**

---

# THE DETECTOR FAMILY — checked. One question is a lookup, one is marked, one is unsettled

### 1 · THE MEMBERS ARE NAMED. THEIR DETECTION RULES ARE NOT

    TranslationSelf   a rigid object that moves
    GrowthEdgeSelf    a growing / advancing trail
    ValueLatentSelf   non-spatial -- a scalar, a colour's total count
    RegionToggleSelf  a bounded region that genuinely alternates

**Four, by name, each with a one-line gloss — so the SET is a lookup and needs no ruling.**
**And the glosses say what *self* MEANS, not how to detect it.** §18.3 gives no signature, no
input, no rule. **The membership is specified; the detection is a marked design space**, and
saying which is which is the answer to the first question.

**And the set already satisfies the requirement it was built for**: `GrowthEdgeSelf` does not
assume rigidity, `ValueLatentSelf` does not assume spatiality at all. **The corpus's own set
covers both of the exclusions asked for.**

### 2 · INDEPENDENCE IS REQUIRED AND ITS TEST IS NOT GIVEN — and the panel has a trap

> ***"Non-simulable" means the members do not share a failure mode.*** *Four correlated
> detectors are one detector wearing four names.*

**A requirement, with no measurement attached.** The panel screen is the instrument — run each
member across the twenty-five and check they fail on **different** games.

> **⚠ AND THE SIX GAMES WITH NO SURFACED ACTION WOULD FALSIFY THE TEST.** On `ft09`, `lp85`,
> `r11l`, `s5i5`, `tn36`, `vc33` **the adapter surfaces no action** — they advertise a
> positioned click and the adapter drops it, because the loop cannot supply a position. So
> **every detector fails there BECAUSE NOTHING ACTS**, which is a shared failure mode from the
> **HARNESS** rather than from the family. Included, four independent detectors read as
> correlated. **Excluded, and the exclusion is data rather than judgement**: no surfaced
> action, checkable per game.
>
> **AND THE LABEL MUST NOT BE *NO-ACTION GAMES*, WHICH IMPORTS A CLAIM ABOUT THE GAMES FROM A
> FACT ABOUT THE ADAPTER.** What is true is that the agent has no surfaced action there. **What
> is NOT established is that those games have no actions** — a click at a coordinate could be a
> button, a pad, a placement, or a proxy for a movement nobody named, **and nothing has ever
> been able to find out.** The claim would be **false the moment positioned actions are
> supplied**, which is what the arity work is for. **Same collapse as the zeros: absence of
> instrument printed in a column meaning absence of effect** — corrected in the results table,
> and it survived here, which is where whoever runs the test would have met it.

### 3 · WHETHER `Agency` IS A MEMBER IS NOT SETTLED BY §18.3, AND I WILL NOT ASSERT IT

**`Agency` is not among the four by name.** And the two readings differ in kind:

| | |
|---|---|
| **`Agency`** | *which slots respond to my actions* — contingency, per (slot, action) |
| **the four** | *what KIND of thing the self is* — form |

**§18.3 frames the family as *control-mode detection*, which is `Agency`'s question** — so they
are the same subject. **But `Agency` MEASURES contingency and the four INTERPRET its shape**,
which makes *substrate all four read* as available a reading as *a fifth member*.

**The corpus does not say.** Ruling it a member is defensible and **it is a ruling, not a
finding** — recorded as unsettled rather than resolved by the nearest fit, because *four
detectors wearing one name* is precisely what the wrong answer here looks like.

**Its docstring needs the amendment regardless** — it cites §16.2 and §16.2's heading carries
`⚠ AMENDED BY §18.3`.

---

# READ: REDUX's `self_family.py` — the rules are general, and it answers the `Agency` question

**Read for the RULE, never the classification, and capability-at-write-time.**

### 1 · IT IS A FAMILY OF FOUR, WHICH IS EVIDENCE **FOR** §18.3's AMENDMENT

`TranslationSelf · GrowthEdgeSelf · ValueLatentSelf · RegionToggleSelf`, plus a
`SelfHypothesis` base and a `SelfModelFamily`. **Redux did not use one test that worked — it
used four**, so the amendment is not contradicted by the thing it was drawn from.

### 2 · THE RULES ARE GENERAL, AND THE INDEPENDENCE DISCIPLINE IS IN THE BASE CLASS

> *`observe(before, action, after) → residual in [0,1]` (0 = perfectly predicted this step,
> 1 = explained nothing). **Members are compared ONLY by this ground-facing residual, never by
> judging each other.***

**Each reads a signal, not a game.** Translation: `1 − (vacated+arrived)/changed`. Growth: the
colour whose count grew most, `1 − new_cells/changed`. Toggle: ***a cell toggles iff its value
returns to what it was two steps ago — this rejects random repaint, where cells change every
step but never come back.*** **That last is a rule with its own falsifier attached.**

**And the selector is the corpus's own form**: EWMA per member, `selected()` = the
lowest-residual member that `has_self()`, plus **a completeness critic** — `self_unmodeled()`
fires when *no member has a self, OR the best residual is still high — **the whole family
failed together, which flags a shared smuggled presupposition to surface.***

### 3 · IT ANSWERS THE `Agency` QUESTION — AND WITH A THIRD OPTION

`ValueLatentSelf` carries `act_delta = {}  # action → EWMA change in the tracked resource`, and
*attribute the resource change under THIS action, so "preserve the resource" is actionable*.

> **So Redux does NOT separate *what responds to me* from *what kind of thing I am*. Each
> MEMBER carries its own action attribution.** Neither *fifth member* nor *substrate* —
> **per-member contingency**, which is the option neither of us had. **Still Isaiah's ruling,
> now with a worked precedent.**

### 4 · WHAT DOES NOT TRAVEL, AND ONE THING I READ THAT SHOULD NOT HAVE

**Seven unanchored constants**: `window=2`, `res < 0.5`, `streak >= 2`, `K=8`, `bucket=8`,
`alpha=0.3`, `unmodeled_threshold=0.6`. **None carries a basis in the file.** Under this repo's
anchor rule each needs one, and `0.5` and `0.6` are thresholds on residuals — **the exact
construction `EPS` was deleted for.**

**And `GrowthEdgeSelf` and `ValueLatentSelf` both call `background_colour()`** — *the
background is the frame, not the self.* **This repo's `arc_percept` refuses the concept
outright**: *treating 0 as background is domain knowledge about what a board means, and this
file is not entitled to it.* **So two of the four rules rest on a primitive this project ruled
out**, and salvaging them as-is would import it.

> **⚠ AND THE FILE NAMES A GAME MECHANIC IN A DOCSTRING, WHICH I READ BEFORE I COULD AVOID
> IT.** `ValueLatentSelf`'s docstring identifies a specific colour and what it does in `ls20`.
> **Recorded as read, and it does not enter**: the member's RULE is *find the colour whose count
> moves monotonically* — general, and it never needed the instance. **The rule salvages; the
> docstring is the thing to leave**, which is exactly the line drawn before reading.

---

# §18.3's INDEPENDENCE REQUIREMENT IS ASSERTED, AND ONLY ITS FAILURE HALF IS MEASURABLE

**Found by reading the critic against the clause it implements.** §18.3 names collapse 2 from
the AGREEMENT side:

> *"Non-simulable" means the members do not share a failure mode. Four correlated detectors
> are **one detector wearing four names**, which is collapse 2 inside the perception layer.*

**Redux's critic fires from the FAILURE side, and only there**: *no member has a self, OR the
best residual is still high — **the whole family failed together***.

> **THE TWO ARE NOT THE SAME EVENT, AND THE ASYMMETRY IS THE POINT.** Four members **failing**
> together is visible in the residuals alone. Four members **agreeing and all being right by
> common cause** is invisible without the ground. **So the critic instruments the detectable
> half and §18.3's actual requirement — that they not share a failure mode — is instrumented by
> nothing.** Redux measured what it could see.

**AND THAT IS THE PANEL LAW ONE LEVEL DOWN.** *A panel property must be MEASURED before it is
used as a premise, never asserted from the shape of the generator.* **Non-simulability is
currently asserted from the shape of the four descriptions** — translation, growth, scalar,
toggle *look* independent. **The DS ladder looked like easing on ten seeds.** The four are
plausibly independent and that is not a measurement; **the six games with no surfaced action
are the worked case of why — every detector fails there because nothing acts, and four
independent ones read as correlated.**

**So the exclusion recorded under *exemptions as data* is not a detail of one test. It is the
only reason the independence measurement can be run at all**, and the measurement is owed
before the premise is used.

---

# THE QUARANTINE SHAPE, NAMED BY ISAIAH, AND THIS IS ITS SECOND INSTANCE

> **The mechanics quarantined, the second-order content salvaged.**

A source that carries both a specific task's mechanics and a general structural rule is read
**for the rule**, with the mechanics recorded-as-read and refused entry. `self_family.py` is an
instance: the rule *find the colour whose count moves monotonically* travelled; the docstring
naming a colour and its behaviour in one game did not, **and the rule never needed it.**

**THE TEST IS WHETHER THE RULE STILL STANDS WITH THE INSTANCE DELETED.** If it does, the
instance was illustration. **If it does not, the instance WAS the rule** and nothing salvages —
which is the case the shape exists to catch, and neither instance so far has hit it.

---

# TWO OF REDUX's FOUR RULES REST ON A PRIMITIVE THIS REPO REFUSED, AND THE GAP IS NAMED

`GrowthEdgeSelf` and `ValueLatentSelf` both call `background_colour()` — *the background is the
frame, not the self.* `arc_percept` refuses it: *treating 0 as background is domain knowledge
about what a board means, and this file is not entitled to it.*

**WHAT THE CALL IS ACTUALLY DOING is excluding the LARGEST region from being read as the self**,
and *largest* is a reading the repo already has. **Whether that substitution is legitimate is
not settled here** — it is a different rule with the same effect on the cases Redux ran, which
is exactly the shape `reflect` was refused for: *a different operator wearing the corpus's word,
and it would have passed every check.* **Recorded as the gap, not closed.**

---

# THE COLOUR FINDING IS A LIFETIME PROBLEM — AND THE REPO ALREADY HAS THE LEAK

**Isaiah's correction, checked at the sites.** `arc_percept`'s refusal was of background as a
DOMAIN PRIMITIVE and was right about that; it was never a refusal of reading a colour's ROLE
within an episode. **Colours permute when a game refreshes, so a colour identity is valid for
the episode it was read in** — vocabulary permanent, instances transient.

### 1 · IS THE LIFETIME ENFORCEABLE AT THE SITE? **FOR A NEW READING YES, FOR THE EXISTING ONE NO**

`retarget`'s clear list is nine assignments, and **every one of them is on the AGENT**:
`bound`, `trace`, `owed_import`, `abstained`, `candidates`, `drive`, `_view`, `_prev_bet`,
`_prev_pred`, plus `slots`/`actions`/`alphabet` re-read from env. **A per-episode colour
reading placed on the agent is enforced by one line there.**

> **BUT THE TWO COLOUR-HOLDING OBJECTS ARE BOTH ON THE FAR SIDE OF THAT BOUNDARY.**
> `Affordances` is a local in `play()`; `Objects` is `ArcWorld._decompose`. **`retarget` cannot
> reach either, and does not try.** So the lifetime is enforceable for something built agent-side
> and **is not enforced for what exists** — which is the leak, stated as asked.

### 2 · DOES THE PROBLEM EXIST ELSEWHERE? **ONE REAL INSTANCE, ONE SMALL ONE, ONE CLEAN**

| site | keyed on | crosses a boundary? |
|---|---|---|
| **`Affordances.seen`** | **`kind_of(obj)` = `(colour, shape)`** | **YES — constructed once per RUN, never reset** |
| `ArcWorld._palette` | `max(board)+1` at the first frame | yes, held for the run |
| `Objects.tracked` | overlap, then shape at normalized offsets | **clean — its docstring says *survives recolour*** |

**`Affordances` IS THE INSTANCE, AND ITS OWN DOCSTRING NAMES THE CONTRADICTION:** *the PROFILE
is what transfers, because a private-set game with a wall it has never seen still has a thing
that blocks.* **The value is claimed to transfer and the KEY it is stored under cannot** —
vocabulary and instance in the same dict, and *colour 4 blocks* is arithmetic wearing a
profile's name.

**AND `kind_of`'s JUSTIFICATION IS EPISODE-SCOPED WITHOUT SAYING SO.** *Splitting is
recoverable, conflation is the silent failure, so the finer key wins* — **sound within an
episode.** Across a refresh colour is a random relabel rather than a discriminator, so the
finer key buys **both** directions: the same thing splits, and two different things can merge
into one row. **The premise that colour carries information is what dies at the boundary, not
the key.**

> **AND THIS IS THE MEASURED FINDING WITH ITS MECHANISM NAMED.** *Reuse halved when only the
> constants changed — same mechanisms, different numbers: the library is fitted to the
> arithmetic it saw.* **A colour-keyed affordance row is exactly that arithmetic**, and it is
> the first site where the fitting is visible in a key rather than inferred from a rate.

### 3 · SO TWO OF REDUX's FOUR MEMBERS COME BACK

`GrowthEdgeSelf` never needed background as a concept — **it needs the most common colour, this
episode**, discarded at retarget alongside `bound` and `trace`. **Re-scope, not repair.** The
earlier *does not travel* verdict on these two is **withdrawn**; what stands against them is the
constants, which is a separate objection.

**AWAITING THE RULING BEFORE RE-SCOPING**, and the family's shape changes if they return.

### 4 · RECLASSIFIED: PLACEMENT, NOT A MECHANISM GAP

**Ruled by Isaiah on the reading**: *it isn't that the lifetime is unenforceable — it's that
these two aren't where the enforcement lives.* `retarget` is a working boundary with nine
things already clearing through it. **Nothing is missing; two objects sit outside it.** The
earlier framing invited a mechanism to be built, and **the mechanism exists.**

### 5 · A DECISION CORRECT FOR A SCOPE NOBODY STATED — AND IT IS NOT `A6i`

`kind_of`'s asymmetry argument *inverts* at the boundary: within an episode the finer key only
risks splitting; across one it buys splitting AND merging. **The reasoning was sound and the
scope it was sound for was never written down.**

> **DISTINGUISHED FROM `A6i` DELIBERATELY, because the smell is the same and the defect is
> not.** `A6i` is **two legitimate quantities under one word** — `molecule`, `DIRECTED`,
> `BUDGET`, `PRIOR`. **This is ONE quantity under an unstated LIFETIME.** A6i's check is *look
> the word up in both places*; that check passes here, because `kind_of` means one thing
> everywhere. **What is missing is not a second sense — it is the scope over which the
> justification holds.**

**Recorded as a finding, not proposed as a law.** Whether this earns a step is Isaiah's; what
is checkable now is that it exists and that the existing check would not have caught it.

### 6 · MARKED: THE FITTING IS VISIBLE IN A KEY, NOT INFERRED FROM A RATE

Every prior instance of *the library is fitted to the arithmetic it saw* was **a number** —
reuse halving, the false-mint rate. **A colour-keyed affordance row is the mechanism itself, in
a dict key.** *Checkable rather than inferred*, which is the difference between a reading and
a measurement of the thing that produced it.

---

# THE GRAMMAR's HOLE AND A VARIABLE KEY ARE **NOT** THE SAME MECHANISM — AND MERGING THEM IS `A6i`

**Checked before building, which is the whole value of asking.** `is_hole(x)` is
`isinstance(x, T)` — **the hole IS the type enum member** — and it appears in exactly two
places, both gates inside `_check_terminal`. **Three differences, and the third is the one that
matters.**

| | grammar's hole | a variable key's `?c` |
|---|---|---|
| **identity** | `T.ATTR is T.ATTR` — **two holes are indistinguishable** | `?c` in two positions must be **the same** `?c` |
| **binding** | **never bound by anything.** Two uses, both gates | **must** bind per episode, and drop at a boundary |
| **quantifier** | *I don't know, and I'm asking* | *I don't care which, and it's the same one* |

**THE HOLE IS CLOSED BY MEASUREMENT; `?c` IS DESTROYED BY IT.** The grammar's docstring says so
outright — ***"a bare type as a leaf: a template without content. This is how a question is
asked."*** A probe answers it and it is gone. **A key's `?c` is meant to stay open forever**;
resolving it re-creates the exact defect the re-scoping removes.

> **SO NAMING THEM ONE THING PUTS AN EXISTENTIAL AND A UNIVERSAL UNDER ONE WORD, WHICH IS
> `A6i` — the real one, and the check FAILS here where it PASSED on `kind_of`.** Look *hole* up
> in both places and you get two quantities. **Two things, and the collision is FOUND rather
> than made, because it was checked before either was built.**

**AND THE HOLE IS THE DEGENERATE CASE ONLY IF YOU IGNORE THE QUANTIFIER** — one occurrence, no
binding, which is what makes the resemblance strong enough to be dangerous. **The resemblance
is the hazard, not the evidence.**

---

# DOES THE VARIABLE KEY REACH PREDICATES? **NO — AND `Term`'s SHAPE IS WHY**

**I was about to say yes.** The predicate constructors do carry concrete values —
`G.Leaf(G.T.ATTR, before[s])` in the GROUND, and for a `.colour` slot **that int is a colour.**
Four such sites in `tether.py`.

**BUT Γ's LIBRARY CANNOT HOLD ONE.** `library[term.name] = term`, and a `Term` is
`atoms: tuple[Atom, ...]` plus **`operand: str | None` — a SLOT NAME, never a value.** No
concrete number can enter, which is the same property `arc_predict` established deliberately:
***neither delta is chosen; both atoms read an OPERAND, so the step size and the target colour
are discovered by binding.***

**The valued leaves live in the UTTERANCE layer and land in the LEDGER** — a record of what was
said at a cycle, stamped with it. **A record holding an episode's colour is correct; that is
what a record is.**

> **SO THE SCOPE IS NARROW AND CHECKABLE: the variable key is needed exactly where a KEY is
> built over a concrete value, and there is ONE such site — `kind_of`.** `ArcWorld._palette` is
> a held scalar, not a key. **Predicates are closed by construction.**

**AND THIS WOULD HAVE BEEN THE FIFTH UNVERIFIED CARRY-FORWARD.** The exposure was visible, the
inference from it was natural, and `Term`'s two fields refute it. **The four prior instances
were all documents; this one would have been a data-flow I could see half of.**

**AND THAT IS A DIFFERENT KIND, WHICH IS THE PART WORTH KEEPING.** A document claim has a
citable source and can be grepped — *assume it is already specified, and go look* is a step
that fires on it. ***I traced it and it looked like it reached predicates* has no source to
check against.** Both existing mitigations are document-oriented and **neither reaches this.**

**WHAT REFUTED IT WAS READING THE DESTINATION'S SHAPE, NOT TRACING THE PATH.** The path was
traced correctly: valued leaf → GROUND → bet → recorded. **Every step true, terminating in
something that cannot hold what was traced.** `Term` is two fields and only reading them says
so.

> **So the transferable half is: READ WHAT RECEIVES, before concluding what reaches it.** The
> mirror of *read the things that produce conditions before the things that produce results* —
> same asymmetry, opposite end. **Recorded as a finding; whether it earns a step is Isaiah's.**

---

# BUILT: §18.3's DETECTOR FAMILY — `self_family.py` + `arc_self.py`

**Three rulings landed together.** Section check first: §18.3 read in full, §16.2 read as the
clause it amends, §16.4 and §18.4 read as the ones it sits between.

### THE SPLIT, AND IT IS THE REPO's OWN PATTERN

`self_family.py` holds **the seam and the selection** and is domain-agnostic; `arc_self.py`
holds **the four members**, which read boards. The members are INJECTED, on
`arc_atoms.three_spaces(predict)`'s pattern — **the agnostic file must not know what a self can
look like**, or membership becomes a decision taken there.

**THE DISCIPLINE IS IN THE BASE CLASS**: members are compared only by a ground-facing residual
and never by judging each other; the family holds no cross-member state. **And the completeness
critic came with it** — `unmodeled()` fires when no member has a self **or** the best one leaves
more unexplained than it explains.

### THIRTEEN CONSTANTS, NOT SEVEN — AND MY OWN COUNT WAS THE ERROR

**I counted constructor defaults and the bodies carried six more.** All are accounted for at the
site: `window` (x2) and `bucket` **dropped by scope** — used only by `self_frame`, Redux's
state key for a policy, which has no consumer here; `K` **dropped by scoping** — the history IS
the episode; `alpha` → **running mean**; `res < 0.5` (x2) and `0.6` → **`explained >
unexplained`**, two halves of one quantity meeting where nobody chose; `mono < 0.8` →
**every nonzero step shares a sign**, existential; `-10**9` **removed**; `net >= len(nz)`
**transcribed unchanged**, already parameterless.

> **ONE NUMBER SURVIVES: `MIN_REPEAT = 2`, and the ANCHOR rule caught it before I wrote the
> basis.** *One observation is a coincidence — over a single step every direction is monotone,
> every change is a first change, and no repeat has happened.* **The checker fired on exactly
> the thing it exists for**, which is the second time a rule in `conform/` has found something
> in a build rather than confirming one.

### WHERE THE PER-EPISODE BINDING LIVES, AND WHAT CLEARS IT — ASKED FOR, ANSWERED

**The rule is permanent and lives in the member; the binding is `Episode.common` and lives with
it.** *The most common colour, this episode* — bound on first sight, **not** `background_colour()`,
which names a stable fact that is not one.

**The family lives on `ArcWorld` because the members read BOARDS and the loop may not.** So the
drop is triggered from `retarget`, **the tenth thing clearing where nine already do** — and a
world with no episode bindings **records that it had no hook** rather than being skipped
silently.

### AND IT IS DIAGNOSTIC-ONLY TODAY, WHICH §18.4 NAMES AS A MEASURED FAILURE

> *The sensorium found the right self and changed nothing, because the only consumer of
> perception was the post-hoc veto. **Perception has to enter the PROPOSER.***

**Nothing reads `selected()`.** Stated in the code and here rather than left for a reader to
discover — the consumer is its own item, and shipping one inside this build would be half a
mechanism.

### THE BOUNDARY FIRES, MEASURED — AND ONE HALF OF IT IS STILL UNOBSERVED

**150 cycles, one ending: `boundary rows: 1`, `env_dropped = True`, and the episode binding
reads `None` afterwards.** The hook is reached from `retarget`, the world's `boundary()` runs,
and the binding is gone. **Not a wiring that type-checks — a wiring that ran.**

> **WHAT IS NOT SHOWN IS THE RE-BIND.** The ending landed with no further steps, so *drops at a
> boundary* is measured and *binds again on the next episode* is only readable from the code
> (`see()` sets `common` only while it is `None`). **Stated because a clean reading of half a
> cycle looks exactly like a clean reading of the whole one** — which is the shape three
> recorded nulls already had.

**And the residuals stay spread at 150 cycles** — `translation 0.199 · growth 0.394 ·
value 0.008 · toggle 0.462`, consistent with the 40-cycle run. **Four readings, not four names
for one**, though that remains an observation about agreement rather than the independence
MEASUREMENT, which is still owed.

---

# VARIABLES IN THE KEY — THE CORPUS SPECIFIES IT, AND `retrieval.py` HAS HALF OF IT ALREADY

**Reported, not built.** Three lookups, three answers, and the expectation that at least one
was already the same idea was **correct on the first one.**

### 1 · IT IS §15.3's THIRD KEY, AND THE BUILT HALF IS THE ONE NOT NAMED IN THE ASK

§15.3's keys are **`type signature · arity · what varies vs is invariant · effect shape`**, and
`ARC_BUILD_PLAN` 3c records what was built: *keys the two free properties (signature, arity)
and leaves the two behavioural ones to the bargain.* `INDEX` line 1184 gives the reason —
**`what varies / invariant | no | needs the term applied to the residual's frames`.**

> **BUT `characterise()` ALREADY COMPUTES BOTH.** `retrieval.py` returns
> `{"arity", "varies", "invariant", "n"}` — **on the GAP side.** And `key_of(term)` returns
> `(t_in, t_out, arity)`, with `fits()` scoring signature and arity only.
>
> **SO THE GAP ALREADY SAYS WHAT VARIES AND THE TERM SAYS NOTHING.** *A shape with holes is
> exactly what varies* is not an analogy — **it is the same object, and the missing half is the
> TERM side.** The built half is the half the ask did not mention.

**Same idea, not new, half-present, and the absent half is named with its blocker already
written down.** The design step is a search of the corpus, and this is the tenth time.

### 2 · THE ARITY PARK's TRIGGER HAS **NOT** FIRED — AND THE REPAINT FIX CANNOT FIRE IT

**Grepped today: nothing reads `operands[1]`.** The only operand readers are `same`, `other`,
`greater` and `translate`, `recolour` — **all index 0**, unchanged by this session's build.

**A variable-keyed affordance table is a LOOKUP, not an atom**, so it creates no operand
consumer and the trigger does not notice it. **The COMPOSITION half would fire it** — a relation
term binding two objects reads index 1 — **but it is blocked one level earlier by something
that is not arity**, and `habitat.py` already states it:

> ***A relation is not a slot**, so `contains`, `touches`, `blocks` cannot be bet on, cannot be
> wrong, and cannot produce a residual.*

**R is indexed per slot and a relation has none.** So **the park sits downstream of a blocker
that is not cost**, and unparking on the composition claim would unpark a mechanism whose
consumer still cannot exist. **The trigger's condition is exact and it is still unmet — third
check, third time unfired.**

### 3 · THE 13× WAS NEVER RECOMPUTED — IT WAS CARRIED, AND ITS PANEL IS GONE

`INDEX` 2094 reads *the measured 13× for zero capability still stands, unchanged* — and the
evidence offered is **the grep**. **A grep establishes ZERO CAPABILITY; it does not re-measure
a COST.** The number itself — 32% of closure yields reading an operand, 185 of 584 at depth 3,
bindings per candidate 5 → 65, per-mint work 925 → 12,025 — **was measured on the TOY panel
under the old atom set.**

> **AND THE RULING THAT PRODUCED IT PREDICTED ITS OWN EXPIRY:** *Phase 3d replaces the atom set
> with grid transforms anyway, so a toy-world operand-1 atom is scaffolding for a panel that
> gets replaced.* **3d is built. `arc_predict` is three atoms.** The ratio is a function of atom
> count and closure depth and **both changed**, so the number is stale **by the ruling's own
> reasoning** rather than by a new argument.

**It is not a verdict and it is not yet a trade either** — a trade needs a capability on the
other side, and §2's blocker says there is not one. **Re-measuring is cheap and is what makes
13× either a real price or a stale one; it is not the thing standing in the way.**

### THE PARK's THREE CHECKS EACH FAILED DIFFERENTLY, AND THE LIST IS THE CHEAP PART

**Recorded so a fourth check does not re-run a settled one.** The trigger is *an atom that
consumes past index 0*, and it has been tested three times:

    1  the new atom set        `translate` and `recolour` both read index 0 -- NO CONSUMER
                               among the atoms that replaced the toy set
    2  16.5's habitat (Q1)     the candidate consumer turned out to be ARITY 1 itself
    3  variables in the key    a variable-keyed TABLE is a lookup, not an atom; and the
                               composition half is blocked UPSTREAM by a non-cost blocker

**Three different reasons, none of them cost.** A fourth candidate should be checked against
this list first: **the question is not *is it N-ary* but *is it an ATOM, and can it exist at
all*.**

### AND A RULING THAT NAMES ITS OWN EXPIRY IS DISCHARGED, NOT FALSIFIED

The 13× is the fifth or sixth stale premise found inside a ruling **and it is not the same kind
as the others.** It stated the condition under which it would go stale — *Phase 3d replaces the
atom set* — **and the condition happened.**

> **THE OTHERS WERE PREMISES THAT TURNED OUT FALSE. THIS ONE WAS A PREMISE THAT EXPIRED ON
> SCHEDULE.** The park working as designed, and the difference is checkable rather than a
> matter of tone: **look for a named condition in the ruling itself.** One that has none and
> goes stale is a defect; one that named the condition and it fired **did its job.**

### AND `composed_from` DOES NOT EXIST — THE MECHANISM DOES, AND IT IS STRONGER

**No such tag anywhere: not in the code, not in any document.** What exists is `Term.atoms`
with `name` = `" . ".join(a.name ...)` — **a composite does not carry a tag naming its parts,
it IS its parts**, and §14.7's chunk reuse counts a term appearing as a CONSTITUENT of a later
mint. **A label can drift from what it labels; a constituent tuple cannot.**

> **AND THIS ONE IS A DIFFERENT KIND OF CARRY-FORWARD: A MECHANISM THAT HAS NEVER EXISTED
> ANYWHERE.** The prior instances each had a real source that said something, or that was
> misread. **This had no source at all**, so there was nothing to check against and the only
> refutation is exhaustive absence.
>
> **WHICH IS AVAILABLE HERE AND IS NOT AVAILABLE MID-EPISODE, AND THE DOCTRINE DRAWS EXACTLY
> THAT LINE.** *Absence of evidence resting on completeness never holds mid-episode* — because
> the world is open and unvisited states outnumber visited ones. **A repo is a CLOSED world**:
> a grep over the code and every document is genuinely exhaustive, so *it does not exist* is
> positive evidence here and a guess there. **The rule is unchanged; what changes is whether
> completeness is reachable, and that is a property of the search space rather than of the
> claim.**
>
> **AND THE REGISTER IS NOT ONE PERSON's.** This entry was Isaiah's assertion, the prior five
> were mine, and a register that only holds one side would have missed it.

---

# RULED: DO NOT RE-MEASURE THE 13×, AND THE REASON IS A NEW COROLLARY

> `[I]` ***Don't re-measure. It isn't in the way, three checks say the blocker is elsewhere,
> and a cheap measurement that changes nothing is a number someone will later cite.***

**THIS IS NOT THE INVENTED-METRIC RULE AND IT IS SHARPER.** The documented failure is
*inventing metrics and magic numbers* — a quantity that was never legitimate. **Here the
measurement would be REAL, correctly taken, and cheap.** The objection is what happens
afterwards: **a number acquires authority by existing**, and one with no decision attached gets
cited by whoever finds it, against a question it was never measured for.

    the existing rule    do not invent a quantity
    this corollary       do not TAKE a legitimate one that cannot change a decision

**Checkable before the measurement rather than after**: *name the decision this would change.*
If none, the number is a citation waiting to happen. **And it is the cheapness that makes it
dangerous** — an expensive measurement has to argue for itself.

### AND IT PAIRS WITH THE NAMED-CONDITION TEST AS WRITE-SIDE AND READ-SIDE

`0a`'s trigger is *an atom that consumes past index 0* — **a grep, not *revisit later***. The
named-condition test is the same discipline from the other end:

    WRITING a ruling    state the condition under which it expires, in checkable form
    READING one         look for that condition; if it named one and it fired, the ruling was
                        DISCHARGED. If it named none and went stale, that is the defect

**One habit, two moments, and each is worthless without the other** — an expiry nobody reads is
a comment, and a reader looking for an expiry that was never written finds nothing and calls it
sound.

### THE ORDERING, RULED

    1  THE TERM SIDE OF §15.3's THIRD KEY   largest, and it has a BUILT HALF -- the gap says
                                            what varies and the term says nothing. The transfer
                                            question with a named missing piece
    2  `Affordances`'s KEY                  the live site, and small
    3  THE 13×                              NOT TAKEN. Ruled above

---

# BUILT: §15.3's THIRD KEY, TERM SIDE — AND THE BLOCKER WAS A GROUPING, NOT A COST

**Checked before assuming, as ruled.** The recorded blocker was *needs the term applied to the
residual's frames*, filed in a table beside `effect shape` under ***properties of its
BEHAVIOUR***, with the argument that keying all four *would consume exactly the work it exists
to save.*

> **THE ARGUMENT IS RIGHT AND THE GROUPING IS WRONG.** `effect shape` genuinely requires running
> the term. **This does not.** `Ctx` has TWO FIELDS — `action` and `operands` — and an atom is
> `fn(v, c)`, so **a term's dependency set is bounded at CONSTRUCTION**: its own slot, its
> operand slot, the action. **It cannot vary with a slot it has no accessor for**, and
> `reads_operand` is *declared at construction, never inferred*. **O(1) off the term.**

**AND THAT IS THE BUILD-TABLE STEP AT THE LEVEL OF A KEY TABLE.** *Build tables group by cost;
the dependency order falls out of neither the table nor the cost.* **Here a KEY table grouped
two keys by cost and the grouping was false for one of them** — five for five, and the first
instance outside a build plan.

**SOUND ONE WAY ONLY, WHICH IS WHY IT IS A KEY AND NOT A GATE.** Invariance is exact — no
accessor, no dependence. *Varies* is an upper bound: a term reading its operand may still
ignore it. **`fits` orders and excludes nothing, so an over-approximation is the right shape.**

### MEASURED, AND THE NULL IS NOT YET INTERPRETABLE — THE PANEL PROPERTY IS NAMED

**Toy panel: byte-identical output.** Not evidence of neutrality on its own — *a control that
examines nothing cannot demonstrate a clean state* — so the key was instrumented on a real run.

    2,792 (term, gap) pairs      one game, 30 cycles, library 21, world slots 105
    28 points awarded            ALL to unary terms in gaps where nothing else varied
    692 operand-term pairs       ZERO points
    6 distinct operand slots     across the whole library, against 105 slots

**Namespaces CHECKED, not assumed** — `term.operand` reads `o12.col`, `gap["varies"]` holds
`o11.col`. **Same format, so 692-and-zero is not a mismatch.**

> **WHAT THE MECHANISM WOULD NEED IN ORDER TO SHOW, STATED BEFORE THE NULL IS READ:** *a gap
> whose `varies` contains a slot some library term is bound to.* **The library binds six slots
> of 105 and none coincided.** So this is a reading about a thin panel, **not a verdict on the
> key** — and it is the fourth time a null has been recorded against a world structurally
> unable to reward the thing tested, this time with the property named in advance instead of
> found afterwards.

---

# BUILT: `Affordances`'s KEY HOLDS A VARIABLE — AND ITS DEFENCE ANSWERED THE WRONG OBJECTION

**Section check first: §16.4 in full.** It names no key at all — *seven booleans per object
kind, learned by interaction* — so `kind_of` was the repo's invention and had to be checked
against §16.4's actual test rather than its own note.

### THE OLD DEFENCE CHECKED PROVENANCE WHERE §16.4 TESTS SURVIVAL

> *It is not a taxonomy: §16.4 says do not classify the substance. **Colour and shape are what
> the sensors already report, not a category anyone named.***

**§16.4 does not ask who named it.** It says *a taxonomy learned from the public set **will not
survive contact with a private one***. **Colour fails that twice**: it permutes on a refresh,
and §16.4's own example is ***a wall it has never seen***, whose colour is one it has never seen
either. **A defence that answers a different objection reads as a defence**, which is why it
survived being quoted.

**AND SHAPE ALREADY CARRIED THE INVARIANCE, ONE FUNCTION UP.** `shape_of` is §12.3 sensor 5 at
normalized offsets — ***identity under translation as well as under recolour***. **The property
the new key needs was stated in the file, in the function the old key was calling.**

### THE COARSENING IS REAL, MEASURED, AND MADE LOUD RATHER THAN CLAIMED HARMLESS

The old note's own objection to a coarse key was ***and nothing says so***. So `Affordances` now
records which colours bind to each key this episode and reports any key carrying more than one:

    56 keys under the variable key        against 77 the old key would have made
    20 keys carrying >1 colour            largest carries 3
    bindings after `boundary()`: 0        table kept: 56

> **THE CONFLATION THE OLD NOTE SAID NOTHING ABOUT IS NOW THE THING THAT SAYS SO** — and 20 of
> 56 is not a rounding error. **Reported as a live reading rather than settled**: whether those
> rows contradict themselves is a question the profile can answer and nobody has asked it.

### AND THE PLACEMENT IS THE RULED ONE, MEASURED

**`Affordances` moved from a local in `play()` onto `ArcWorld`**, where `boundary()` reaches it
— *a local sat outside the boundary `retarget` triggers, which is the placement the ruling was
about.* **Table permanent, bindings transient, and both halves measured in the same run.**

**The contact reading moved into `step()` with it**, which also fixed a smaller thing: the
before-snapshot in `play()` was the PREVIOUS iteration's tracker state, and the world has a
true before/after pair. **Found by moving the reading, not by looking for it.**

> **AND THE RE-BIND IS STILL NOT SHOWN — THIS RUN MEASURED A DIFFERENT PAIR.** *Bindings 0,
> table 56* is **DROP plus RETENTION**, which the family's run could not show because it has
> nothing to retain. **Re-bind is *does a new episode repopulate it*, and neither run reached
> a second episode.** Three measurements, easily read as one: **drop · retention · re-bind**,
> and only the first two exist. Recorded because *bindings 0, table kept* looks like the whole
> cycle and is two thirds of it.

### THE ELEVENTH LOOKUP, AND THE SHORTEST DISTANCE YET

The invariance the new key needed was in `shape_of` — ***identity under translation as well as
under recolour*** — **the function `kind_of` was already calling.**

> **NOT A DOCUMENT, NOT ANOTHER MODULE, THE CALLEE.** The step's own clause is that *familiarity
> actively suppresses it: citing a file feels like evidence of having read it.* **This is the
> strongest form — not citing, CALLING.** A function you invoke every time reads as known, and
> there is no state recording that its docstring was never opened. **Proximity did not help and
> may be what hid it.**

### AND THE 20 OF 56 ARE A CHECKABLE CONFLATION, WHICH IS A DIFFERENT OBJECT

`[I]` ***A conflation that can be checked is a different object from one that can't.*** The
rows carrying two colours either contradict themselves in their seven booleans or they do not,
and **the profile can answer it.** Left as a live reading with the question named: **nobody has
asked it, and the asking is what separates a coarsening from a defect.**

---

# MEASURED: §18.3's INDEPENDENCE — AND MY PRE-REGISTERED CHECK WAS ITSELF INSUFFICIENT

19 games, 25 cycles, apparatus with no agent and no Gamma. **The exclusion held: all 19 played,
none skipped inside the panel.**

    member        found a self    failed    on
    translation      4 / 19         15      ar25, ls20, re86, tr87
    growth           3 / 19         16      ls20, sk48, tu93
    value           16 / 19          3      sixteen
    toggle           0 / 19         19      NONE

### THE CHECK REPORTED `all_pairs_separable: True` AND THAT READING IS WRONG

**`separable_here` asked *did one member find a self where the other did not*. A member that
never fires satisfies that against everyone.** All three `toggle` pairs came back separable
**because toggle is dead, not because their failure modes differ** — and the pre-registration I
committed before the reading did not catch it.

> **THIS IS `B17` ON MY OWN INSTRUMENT.** *Pre-registration does not protect a reading if the
> instrument measures something else.* The condition was pinned in advance, in a file committed
> before the run, **and it measured *do they differ* where the question is *do they FAIL
> differently*.** Discipline correctly applied, producing a reading that would have been
> published as *independence confirmed on all six pairs*.

**THE CORRECTED CONDITION, AND IT IS ONE LINE**: *a member carries failure-mode information only
if it has BOTH a success and a failure on the panel.* **A constant member is neither independent
nor correlated — it is uninformative**, and every pair containing it is unreadable rather than
passing.

### WHAT THE PANEL ACTUALLY SUPPORTS

**Three of four members are informative.** `toggle` is constant-False across 19 games and **the
measurement cannot say whether it shares a failure mode with anything** — it has no successes to
compare. Whether that is the rule being right and the panel having no toggling region, the
driver's cycling actions interacting with a two-step rule, or a transcription defect, **is not
decided by this run and is not guessed here.**

**And the one real signal is small and stated as such**: `translation`'s successes are a strict
SUBSET of `value`'s, `growth`'s are not. **At a 16-of-19 base rate subset-hood is nearly
automatic, so it carries little** — recorded so it is not mistaken for a correlation finding.
`translation` and `growth` overlap on **one** game of seven successes between them, which is the
closest thing here to the property §18.3 asks for.

> **SO THE REQUIREMENT IS STILL NOT DISCHARGED, AND NOW IT IS UNDISCHARGED FOR A NAMED
> REASON** rather than for want of a measurement. **That is the improvement**; the number is
> not.

---

# `toggle` AT 0/19 WAS THREE DEFECTS DEEP, AND THE FAMILY IS FOUR

**Three candidate causes were named and none guessed. Two were falsified with positive evidence
and the third turned out to be the wrong question.**

    transcription defect     FALSIFIED. Fed a synthetic period-2 alternation, the rule fires at
                             exactly the right step -- streak 1 at step 2, `has_self` at step 3
    the driver's actions     FALSIFIED. Re-ran the panel with a single REPEATED action against
                             the cycling one. Both zero, so the action policy is not it
    no toggling regions      OVERTURNED, NOT CONFIRMED. **15 of 19 games have cells returning to
                             their two-steps-ago value**, seven reach residual 0.0, and `sk48`
                             reaches streak 3 -- above `MIN_REPEAT`

**ELIMINATION WOULD HAVE LANDED ON THE THIRD AND IT WAS FALSE.** *Prefer positive causal
evidence over absential* is the rule, and this is the case it is for: two exclusions and a
subtraction would have published *the panel has no toggling regions*, **which the direct
measurement refutes in its first column.**

### THE ACTUAL CAUSE: `has_self` IS ONE WORD OVER TWO QUANTITIES, INSIDE THE FAMILY

    translation · growth · toggle    `self._streak >= MIN_REPEAT`   -- MOMENTARY, right now
    value                            the whole episode's series     -- CUMULATIVE

**The screen read `has_self()` ONCE, at the final step.** So it asked the momentary three *are
you mid-streak* and the cumulative one *did it ever hold*, **and compared the answers as though
they were the same reading.** `sk48` reached streak 3 and had reset before step 25.

> **THIS IS `A6i`, INSIDE A FAMILY BUILT THIS SESSION, AND IT WAS INHERITED RATHER THAN
> INTRODUCED** — Redux's members carry the same split. **The check is *look the word up in both
> places*, and both places are in one file.** Four members, one method name, two quantities.

**THE FIX IS TO THE INSTRUMENT, NOT THE MEMBERS.** *Transcribe, do not improve* holds: the
members are unchanged and the screen now POLLS every step and records whether a member EVER
reported a self. **That is §18.3's own phrasing** — *`has_self: false` for **904 steps*** means
never, not *not right now*.

### AND THE READING CHANGES COMPLETELY

    member        ever    at final step        fails on
    translation   12/19       4/19             7 games
    growth         4/19       3/19            15 games
    value         18/19      16/19             1 game
    toggle         2/19       0/19            17 games

**`uninformative: []` — all four have both a success and a failure. `all_pairs_readable: True`,
and this time not as an artefact.** Every pair disagrees somewhere: 10, 6, 12, 2, 14, 16.

> **THE FAMILY IS FOUR.** `toggle` fires on two games and the question of whether to drop it
> does not arise.

**AND ONE WEAKNESS IS STATED RATHER THAN LEFT IN THE TABLE.** `value` fails on **one** game, so
every pair containing it rests on that single game plus the other member's failures — **thin,
and `informative` is true by the narrowest margin the predicate allows.** `growth|toggle` at 2
disagreements is the other thin one. **Four of six pairs are comfortable; two are not, and the
requirement is discharged only as far as the thin ones allow.**

---

# SECTION CHECK: THE PROPOSER — §18.4 AND `probe.py` CONFLICT AT ONE OF THE THREE EXITS

**Reported, not built.** §18.4 is a rule drawn from a measured failure:

> *The sensorium had become **diagnostic-only**: it found the right self and changed nothing,
> because the only consumer of perception was the post-hoc veto. **Perception has to enter the
> PROPOSER**, not just what it forbids.* **Sensors must feed proposal, not only filtering.**

**`choose()` HAS THREE EXITS AND THEY ARE NOT INTERCHANGEABLE:**

    bored -> "probe"     support at zero, so the model is refused the wheel
    "discriminate"       a slot owes and reachable terms disagree; picks the action that
                         separates their predictions most. ALREADY MODEL-DRIVEN
    "draw"               nothing owes, or no action separates anything

**AND `probe.py` STATES THE DRAW's PROPERTY IN TERMS THAT NAME WHAT WOULD ENTER:**

> *UNINFORMED BY CONSTRUCTION, and that is the safety property. The draw sees the advertised
> action set and nothing else — **not the score, not the goal, not the effect model, not a
> slot's value.** A probe chosen by the current model can only confirm the current model.*

> **A SELF-FRAME IS SLOT VALUES.** So perception entering the draw breaks that clause **word for
> word**, not by interpretation. **§18.4 and `probe.py` are in real conflict at two of the three
> exits** — and the two they conflict at are exactly the ones where perception is most obviously
> absent.

### WHERE IT CAN LAND WITHOUT BREAKING A STATED PROPERTY

**`discriminate` only.** It already reads `Gamma`, the owed slots and the alphabet, so it holds
no uninformedness to lose.

**AND WHAT WOULD ENTER IS `contingency()`, NOT `selected()`.** `contingency` is a **measured
per-action fact** — this member's own signal under each action. **`selected()` as a target would
be a GOAL**, and §16.7's trap is exactly that: *a module that jumps to the objective is a
reading taken below the break.* **The member says what responded; it must not say what to want.**

> **SO THE FORK IS ISAIAH's, AND IT IS A REAL ONE RATHER THAN A GAP:** either §18.4 lands on
> `discriminate` alone and the draw keeps its property, or the draw's *not a slot's value*
> clause is amended — **and the second is the one that costs the safety argument.** Not built
> either way.

---

# `discriminate` IS FLAT BECAUSE NO ARC ATOM READS THE ACTION — AND THAT DECIDES THE RULING's FATE

**Measured before building into it, and the site turned out dead.** 120 steps on one game:

    draw 82 · probe 38 · discriminate 0

**Then the three guards, separated:**

    bored -> probe                  38
    not bored, but NOTHING OWED      2      <- the branch IS reachable
    owed, but SPREAD FLAT           80      <- and this is where it dies

**SO IT IS NOT UNREACHABLE. SLOTS OWE ON 82 OF 120 STEPS, CANDIDATES ENUMERATE (12 and 20),
AND EVERY ACTION SCORES IDENTICALLY.**

### THE CAUSE IS THE ATOM SET, AND IT IS EXACT

`spread[act]` applies each candidate under `Ctx(action=act, operands=())`. **The three ARC atoms
are `idn`, `translate`, `recolour`** and, with `operands=()`:

    _idn(v, _c)        -> v                                    signature takes `_c`, unused
    _translate(v, c)   -> v + c.operands[0] IF c.operands ELSE v   -> v
    _recolour(v, c)    -> c.operands[0] IF c.operands ELSE v       -> v

**All three return `v` for every action.** Grepped: **`c.action` is read in exactly three places
in the repo — `world.py`, `snaps.py`, and a fixture — and NONE of them is an ARC atom.**

> **SO `spread` IS CONSTANT BY CONSTRUCTION AND `max > min` CAN NEVER HOLD ON ARC.** The branch
> that chooses between actions is scored by a vocabulary in which **no action is expressible.**
> `discriminate` did not fail; it was asked to distinguish actions using terms that cannot
> mention one.

**AND `arc_predict`'s PRE-REGISTRATION DID NOT REACH IT.** It pinned three claims — `λ < V`,
*both atoms must BIND*, and *no claim about mint count* — **all about the atoms as PREDICTORS,
none about what the atom set makes unavailable elsewhere.** The corpus's six are all grid
transforms and **not one is action-indexed**, so the gap is in the specified list rather than in
the transcription. **A sixth structural consequence of an atom set nobody costed for the branch
that consumes it.**

### WHAT THIS DOES TO THE RULING — IT STRENGTHENS IT

`[I]` ***§18.4 lands on `discriminate` alone*** — correct, and **now with the reason the branch
needs it.** `contingency()` is a **measured per-action fact**, and the branch is flat **precisely
because it holds no per-action content at all.** So perception entering there is not a tie-break
on a working mechanism: **it is the only action-sensitive signal available to a branch whose
whole job is choosing between actions.**

> **BUT IT IS A DIFFERENT INSERTION POINT THAN THE ONE I PROPOSED, AND THAT IS ISAIAH's TO
> RULE.** A tie-break inside `max(spread)` is dead — there are no ties, there is no winner. The
> live point is **the case the branch currently DECLINES**: owed slots, flat spread, and a
> measured per-action difference. **Not built.** And the two must not be blended: `spread` is
> Gamma's prediction and `contingency` is a measurement, **and a frame cannot score itself with
> a quantity it produces** — so they are separate readings, never summed.

---

# THE BLIND WRITE IS FIXED, AND THE FIX IS MEASURED ON THE SAME TRAJECTORY

    before      +1..+6   blind=True  tracked=20  aff_bindings=15   <- all 15 in ONE step
    after       +1..+6   blind=True  tracked=20  aff_bindings=0    <- guarded

**Both readers now abstain when `blind`, and the abstention is COUNTED** (`unobserved`) rather
than silent — *the flag says why, the counter says how much.*

**AND THE FLAG HAD NO CONSUMER.** `blind` is set and used inside `_decomposed` to produce `{}`,
and its only other reader in the repo is a report field. **The loop was safe by a different
route** — `{}` slots trip `no_slots` — **so the flag protected nothing a new caller could
inherit, which is how a sibling reader walked past it.** *A correctly-computed flag with no
consumer is a report, not a safeguard.*

> **AND THE RE-BIND IS STILL NOT DEMONSTRATED FOR EITHER HALF.** The `0 -> 15` was the blind
> write, not a re-bind. **Drop and retention are measured; re-bind needs a run that crosses a
> boundary and then SEES a readable board**, which this trajectory does not provide within six
> steps.

---

# `appear` / `vanish` ARE `recolour`, AND `consumed` CARRIES THE SAME DEFECT — DEMONSTRATED

**Section check first, as ruled. Nothing changed.**

### 1 · THE CORPUS DOES NOT RULE ON CAMOUFLAGE — IT NAMES THE PRIOR THAT DECIDES IT

**`camouflage` appears nowhere in the corpus.** But its licence does, as a named TRACKER prior:

> `ARC_AGENT` §12.1, TRACKER row: *persistence, occlusion, **numerical-vs-featural identity***

and `priors.py` already loaded it with the catalogue's operational statement:

> ***'same individual' is tracked separately from 'same appearance'*** — Xu & Carey 1996

**That sentence IS the derivation.** A thing persisting while its look changes is the case the
prior exists to name. **Loaded, cited, and never applied to the atom table.**

**AND THE NEAREST THING TO A RULING IS AN OPEN QUESTION, NOT A RULING.** §13.2: *`GONE` is a
**fourth** outcome the four bins do not name. A slot that vanishes is neither held, novel,
rebinding, nor mechanism. **Worth deciding where it routes.*** — and it is about a SLOT
vanishing, **the level `arc_predict` already refused appear/vanish at.** So nothing governs, the
question is open in the corpus's own words, and the prior that answers it was already in the
building.

### 2 · `consumed` IS EXPOSED, AND IT IS MEASURED RATHER THAN ARGUED

§16.4 defines it as ***it disappears on contact*** — and *disappears* is the ambiguous word.
`Affordances.note` writes it on `survivor is None`, and `survivor` comes from the tracker, whose
rule is **death only on evidence**: *dies only when its cells are taken over by other live
objects.*

**CAMOUFLAGE PRODUCES EXACTLY THAT APPEARANCE.** A block recoloured to match its surround stops
being a separate component, the surround absorbs its cells, the surround is live — so the object
is dropped. **Run:**

    before tracked: ['o0', 'o1']        a 2-cell block inside a surround
    after  tracked: ['o0']              the block recolours to the surround's value
    dropped: ['o1']
    affordance row written: consumed: True

> **THE TRACKER's RULE IS NOT WRONG IN FORM — ITS EVIDENCE PREDICATE CANNOT SEPARATE ABSORPTION
> FROM TAKEOVER.** *Death only on evidence* is right; *cells held by other live objects* is
> satisfied identically by a thing being overwritten and a thing changing colour to match. **The
> distinction the prior draws is exactly the one the predicate cannot make.**

### 3 · THE TWO ARE ONE FINDING AT TWO LAYERS, AND `arc_predict` HAD THE OBSERVATION WITH THE WRONG CAUSE

    atom table    calls it a WORLD OPERATION      appear / vanish
    tracker       calls it a DEATH                consumed
    both          are reading a VALUE CHANGE through a segmenter that groups by COLOUR

`arc_predict` refused them because *existence is not a slot VALUE — the slot SET changes and
`_present` sees it: an event, not a transform.* **The observation is exactly right and the cause
is one layer off.** The slot set changes **because the segmenter merged two components**, not
because anything ceased to exist. **Refused for the right reason at the wrong level**, which is
why the refusal read as settled.

### 4 · WHAT THE CORRECTION WOULD COST, AND WHY THE ATOM HALF IS THE BLOCKED ONE

Six become four — `translate · recolour · reflect · rotate` — with **`recolour` doing the work of
three**, and `arc_predict` expressing **two of four** rather than two of six. `reflect` and
`rotate` are unchanged in their reasons: board extent, and coupling two slots.

> **BUT THE ATOM HALF CANNOT LAND FIRST.** Expressing camouflage as `recolour` requires a slot to
> still be there to recolour, **and the tracker deletes it before the atom could bet on it.**
> The tracker defect is load-bearing and the atom-table correction is downstream of it. **A
> six-to-four edit alone would name an operation the perception layer destroys.**

**Reported, not changed.**

---

# `discriminate: 0` IS THE DESIGNED STATE — AND THE PROPOSED FIX WAS THE ENCODED ANSWER

**Read this before proposing an atom against a flat spread.** `ARC_AGENT` measured both arms
and recorded the number:

    spread distinguishes the actions, WITH `act`     33/96   (34%)
    spread distinguishes the actions, WITHOUT `act`   0/96   ( 0%)

> *`act` is the only atom that reads `c.action`, and its effect table is **closed over at
> construction**. **`choose`'s discriminate branch is a property of the atom set, not a model
> the agent built.** It has never had to learn what pressing something does, because the
> primitive it was given already knew. **That is the thing the action world has to take
> away**, and taking it away is what makes motor learning a question rather than a lookup.*

**THE ARC SET HAS NO `act` DELIBERATELY.** The only `c.action` readers in the repo are the two
toy worlds and a fixture. **So 80-of-82 flat on `ls20` is `0/96` reproduced on a real board** —
**a known result, reported as a discovery across four exchanges.**

### THREE READINGS AS A DEFECT, TWO OF THEM MINE, AND THE FIX WAS THE UNFORGIVABLE ONE

**`discriminate: 0` was filed as a defect three times**, and each time the proposed repair was
*an atom that reads `c.action`* — **which is the encoded answer, with a name, a section and a
measurement already standing against it.** It was ruled on as *expensive and honest against
cheap and meaning-changing*, **and the third option was that the expensive one hands the agent
the discrimination.**

**NOTHING CAUGHT IT UNTIL THE CORPUS DID, FOUR SECTIONS FROM WHERE THE READING WAS TAKEN.** The
framing was supplied by the same party proposing the build, so the check had nothing
independent to run against — **which is §8.4's own condition, failing in the small.**

### THE REAL ITEM, AND IT IS ALREADY MEASURED

**A LEARNED contingency becoming bindable, not an atom that arrives knowing.**
`SelfHypothesis.contingency()` reads `toggle: {ACTION1: 0.962, ACTION2: 0.481, ...}` on `ls20`
— **that separates the actions, it was learned rather than handed, and nothing consumes it.**

**Which is §18.4's proposer half, ruled and never built** — *the member says what responded; it
must not say what to want.* **The item is not new; it is the answer to the question atoms were
being proposed against.**

---

# THE GUARD: A REAL `When(P, R)` WITH A FALSE WARRANT, AND THE PRE-REGISTRATION CAUGHT IT

**Built, works, mints — 4 of 7 terms on a 30-cycle run carry one.** Bounded on the residual
rather than the action set, `None` first, no atom added.

**AND ITS JUSTIFICATION WAS FALSE.** Predicted: `SPREAD FLAT` falls, `REUSE_UNWIRED` stays,
`none-stale` moves. **Measured: 21 of 21 flat, `room_invalidated` 0, and no segment closed so
`REUSE_UNWIRED` was UNOBSERVABLE rather than confirmed.**

> **THE CAUSE WAS NOT THE LINK NAMED, AND THE AUTHORISED REPAIR WAS INERT.** `spread`'s
> `Ctx(operands=())` was diagnosed and a one-line change ruled — **and confirmed inert before
> it was made**: `units()` strips the operand and the guard before emitting, *the chunk IS the
> atom sequence and the operand has no business in the key*, **so `enumerate_closure` yields
> bare chains and `spread` never sees a guard at all.** Deliberate, documented one method
> away, and the justification was written without reading it.

**A SECOND INERT MECHANISM WOULD HAVE SHIPPED IN THE SAME SESSION AS THE FIRST.** `operand_type`
read `None` on 911,035 calls because it lived on the atoms and the check read a `Term`;
**this one was caught before the edit rather than after.**

---

# FOUR INDEPENDENT DETECTORS CONVERGED ON ONE FACT — §18.3's AMENDMENT PAYING OFF

**Recorded independently of the proposer build, which failed its own falsifier. This is a
family result and it stands whatever happens to that.**

150 cycles, `ls20`, per-member per-action attribution:

    value    ACTION3  -2.692     against  +0.98, +0.50, +0.41
    toggle   ACTION3   0.878     against   0.43,  0.29,  0.28
    growth   ACTION3   0.523     against   0.75,  0.71,  0.54
    translation ACTION3 0.941    against   0.50,  0.66,  0.91

**OPPOSITE SIGNS, INCOMMENSURABLE UNITS, SAME ACTION.** Three members report an explained
fraction in [0,1]; `value` reports a **signed count difference**. **A shared reading across
those has to survive a change of units, not only a change of member** — which is what makes
this evidence rather than a leak.

> **AND THE INVERSION IS THE PART TO KEEP.** *If every member produces the same split, that is
> about the world* was the natural framing and **it is backwards.** Same split across
> commensurable signals is a common cause; **same split across INCOMMENSURABLE ones is either
> the world or a leak, and the units decide which.** Here they differ, so it is the world.

### AND IT RETIRES THE TWO-PAIR SHAPE AS A LENGTH ARTEFACT

At 40 cycles the reading was `toggle: {A1 0.962, A2 0.481, A3 0.962, A4 0.481}` — **two pairs,
alternating.** At 150 it is **ACTION3 against the rest**, in every member independently. **The
pairing was the run length, not the world** — the fourth time this session a reading at one
length did not survive a longer one, and the first where the shorter reading looked more
structured than the truth.

### 4a: MOVES, THEN STABILISES — WHICH IS LEARNING RATHER THAN TRACKING

    toggle      / ACTION3   0.0 -> 0.746 -> 0.838 -> 0.853 -> 0.878
    translation / ACTION3   0.962 -> 0.89 -> 0.921 -> 0.935 -> 0.941

**Monotone toward a limit in both, from opposite directions.** *Non-constant* was necessary and
not sufficient; **converging is the sufficient half**, and both converge.

---

# `REUSE_UNWIRED` IS UNOBSERVABLE ON ARC, AND TWO RUNS MEASURED NOTHING

**`segments closed: 0` at 30 cycles and at 150.** Read as *needs a longer run* the first time.

**`Chain.close()` has exactly two callers: `snaps.py` and `tether.run()` on `run_end`.**
`arc_holdout.play()` drives `ag.step()` directly and **never calls `run()`** — it says so in its
own comment, *`run()` gives no hook*. **So no segment can close on the ARC path at any length.**

> **A precondition that fails twice for the same structural reason is a fact about the
> instrument's reachability**, and setting a third cycle count would have measured nothing a
> third time. **Third instance of the session's pattern** — a mechanism reachable in principle
> and called from nowhere on the live path, after `touching()` and `contingency()` itself.

---

# THE PROPOSER's FIRST BUILD FAILED ITS OWN FALSIFIER, AND THE GUARD WAS IN THE CLAIM

    every action observed at step  22
    first `discriminate:learned`    2
    fired before all seen        TRUE

**Pre-registered before the number existed, in the form stated as un-cheatable by its author,
and it withdrew the author's own build.**

**THE CLAIM WAS *structural* AND THE PROPERTY WAS *of degree*.** *`contingency()` is keyed on
observed actions, so it cannot separate until every action has been tried* — **true premise,
false implication.** `act` separates on ZERO evidence; that build separated on PARTIAL evidence.
**Both separate before the agent has learned what its actions do**, and the difference claimed
to be in kind was in degree.

**AND *there is no parameter for me to tune* WAS ALSO TRUE AND ALSO DID NOT IMPLY IT.** A
falsifier can be un-tunable and still be guarded by an assertion rather than by the code. **The
gate is now a `continue` in the loop: a member contributes only when every advertised action
appears in ITS OWN dict.**

---

# FOUR FLAVOURS OF ONE DEFECT, AND ALL FOUR PASS EVERY CHECK

**Found separately over one session and they are one class.** A mechanism that is present,
correct, and never reaches the thing it was built for.

    computed with no consumer     `blind` is set correctly inside `_decomposed`, and its only
                                  other reader in the repo is a report field
    producing with no consumer    `contingency()` had exactly one caller -- `report()`
    reachable with no caller      `Chain.close()` has two callers, neither on the ARC path;
                                  `touching()` likewise; the frame layer likewise
    ABSENT RENDERED AS PRESENT    `last_stage: None` reads as *no stall*, not as *never ran*

> **THE FOURTH IS THE WORST AND IT IS THE ONE THAT SPEAKS.** The first three are silent — an
> unread flag, an unconsumed producer, an uncalled method — and silence eventually prompts the
> question *is anything using this*. **`None` renders as a clean outcome.** It was compared
> against a `snaps` reading for a whole exchange as though it were a measurement, and the
> comparison was between a reading and an absence **whose name looked like a reading**.

### AND THE RULE THAT SHOULD CATCH THEM CHECKS A NARROWER THING

`conform/lint.py`'s ISOLATED: ***"Defined and referenced nowhere in the package."*** **Its
subject is REFERENCED; the property is REACHED ON THE LIVE PATH.** A reference from a report
field, a test, or a branch that never executes satisfies it.

**All four above are referenced. None is reached when the agent plays.** **Seventh site for *the
rule's subject was narrower than the property it was written for*,** and the first where four
independent instances were found before anyone looked for the class.

---

# THE PROPOSER: THREE POST-HOC CLAUSES REFUSED, AND THE PATTERN IS THE FINDING

**Each clause was individually defensible. The count is what makes them tuning.**

    1  population gate      after the build fired at step 2 with one action observed
    2  `sep` differs-from-all   after the gated build never fired in 150 cycles
    3  stability clause     after the gated build fired on single samples -- REFUSED

> `[I]` ***A build converging on a target by being told where it missed, which is what the
> pre-registration exists to prevent.*** **No single step looks like tuning and the sequence
> is nothing else.**

**WHAT THE FAILED RUNS ESTABLISHED, AND IT IS REAL:**

- **the gate needs population AND stability** — *every action seen* is satisfied by one
  observation each, and four single values are trivially all-different, so `sep` credits noise
- **the driver must be measured at a NAMED MOMENT** — reading 5 predicted from end-of-run data
  and measured at first fire. **Two moments, and the registration named neither, so it did not
  fail — it was unaskable as written**
- **`sep` means *differs from all others*** — *at least one* is satisfied by nearly every action

**A PRE-REGISTRATION THAT DOES NOT NAME *WHEN* IS UNDER-SPECIFIED EVEN WHEN IT NAMES *WHAT*.**
Every reading in this session's tables named a quantity and a direction; **none named a moment**,
and the one that needed to was the one that could not be read.

---

# AN ACTION LABEL IS AN INSTANCE, NOT VOCABULARY — THE COLOUR RULING'S THIRD ARRIVAL

**Found while justifying the binding-drop, and it is better than the justification it replaced.**

    ls20 advertises   ACTION1 ACTION2 ACTION3 ACTION4
    sk48 advertises   ACTION1 ACTION2 ACTION3 ACTION4 ACTION7

**BOTH WERE WRONG ABOUT WHY THE GUARD MUST DROP.** The stated reasons were *the slot does not
exist elsewhere* and *the action may not be advertised* — **and `ACTION1` IS advertised on both.**

> **THE DROP IS NOT PREVENTING A BROKEN REFERENCE. IT IS REFUSING A CLAIM THAT WAS NEVER TESTED
> THERE.** A guard learned on `ls20` says *this term applies when ACTION1 is taken* **on ls20**,
> and `ACTION1` on `sk48` is a different action wearing the same label.
>
> **A dangling reference fails loudly. A label that resolves to something different fails
> silently** — and it would have read as a guard that transferred.

**SO IT IS THE COLOUR RULING ON THE ACTION DIMENSION.** `ACTION1` names a POSITION IN AN
ADVERTISED LIST, and two games' lists are not the same list. **Vocabulary permanent, instances
transient** — third arrival, **and the first where the instance is a NAME rather than a NUMBER,
which is the harder case: a number reads as arbitrary and a name reads as meaning something.**

**AND `ACTION7` IS WHAT MAKES IT CHECKABLE RATHER THAN ARGUED.** The action sets differ, so a
term guarded on a label that means different things in the two games would be
**indistinguishable** from one guarded on a label that means the same — **unless the binding is
dropped.** `sk48` was picked as a second board for an unrelated reason (the panel screen found it
clean apart from dropping `ACTION6`) and turns out to be the pair that can test this.

---

# THE `getattr` BUG, AND THE DIRECTION IT FAILED IN

`stamps` are **dicts**. `getattr(st, "origin", None)` returned `None` on every pull, so the
transfer column would have reported **no imported term was ever pulled, whatever the truth.**

> **NOT A CRASH AND NOT A WRONG NUMBER — THE ANSWER THE ARCHITECTURE IS BUILT TO BE ABLE TO
> TRUST**, produced by a lookup that could not work, **on the project's own central claim.**
> **Sixth instance of an absence rendered as a value, written in the session that recorded the
> flavour, and the third of them caught by RUNNING rather than by reading.**

**AND THE THIRD BUCKET EARNS ITSELF HERE.** *Across games there is no first* was raised AGAINST
the import; it is what makes the import measurable. **A term entering as `promoted` would be
indistinguishable from one minted locally and the transfer claim would have no subject.**
`IMPORTED` wipes like `promoted` — **the distinction it buys is countability, not survival**, and
countability is exactly what makes the number exist.

---

# THE FALSIFIER FIRED ON ITS FIRST REAL READING, AND IT WAS OVER-BROAD

**`unstated` read 19 of 21** on the first run that put real mints through it -- and it could
not have read anything before, because it also filtered `origin != PRIOR` and so counted the
atoms alone. **Fixed, and then it fired.**

    necessary   14      the atoms
    imported     2      minted on ls20, loaded into sk48
    unstated    19      every term `accept()` put in the library

**RULED: `unstated` WAS OVER-BROAD, AND A FOURTH CLAUSE IS THE ANSWER.** *`accept()` writing to
the library IS the mint working* -- a term that closed a residual and paid the bargain is
**earned; it simply has not crossed a boundary yet, and `promoted` is a claim about surviving
one.** Moving it to `candidates` would stop the closure composing over it, **which breaks
chunking, and chunking is measured working.**

> **AND THE DOCSTRING WAS CORRECT ABOUT THE ROUTES IT KNEW AND SILENT ABOUT THE ONE THAT
> CARRIES EVERYTHING.** *The only ways in are `necessary` and `promoted`* was written before
> minting produced entries at scale. **`unstated` is kept as a fifth bucket and verified able
> to fire** -- a clauseless install reads `{necessary: 14, accepted: 1, unstated: 1}` --
> because **a falsifier that cannot be non-zero is exactly what this one had just stopped
> being.**

### AND THE DIVERSITY FINDING IS THE SHARPER OF THE TWO

`ls20` minted **seven** terms. Loading them into `sk48` read **`loaded: 2, already_held: 5`** --
not a dedup against `sk48`, but **the binding-strip collapsing seven entries into two chains**:
`idn . translate` and `translate . translate`.

> **ALL THE DIVERSITY WAS IN THE BINDINGS AND NONE IN THE COMPOSITION.** So
> `chunk_reuse_count: 0` has a narrower cause than *everything is depth 2*: **there were only
> ever two shapes.** **A library growing in bindings is not a library growing** -- which is
> §14.7's catalogue failure with a mechanism nobody had named.

### AND THE FIRST TRANSFER READING IS ZERO, AS A BASELINE RATHER THAN A VERDICT

**Two compositions offered, 25 cycles, one pair of games: `imported_pulled: 0`.** The load, the
origin, the handle and the refusal column all worked -- **so this is the number, not a
mechanism failure and not an excuse for one.** Too thin to conclude against transfer, and it
stands as the baseline the next reading is compared to.

> **RETIRED 2026-08-31, AND NOT AS *TOO THIN*. THE NUMBER WAS NEVER A MEASUREMENT.** Three
> independent reasons, each sufficient on its own. **(1)** Every composition of length >= 2
> reads an operand -- 12 of 12 at depth 3, and `idn` becoming non-composable closed the only
> escape -- so binding correctly not crossing makes an imported term **extensionally `idn` on
> arrival**, and `_explains` tests exact explanation of a slot's whole history. It can only
> explain a slot that never moves. **(2)** The only path that re-binds is the sweep, and it
> emits no `pull` row, which is the only event `reused()` counts. **(3)** A re-bound term's
> name carries its binding, so `_install_reuse` enters it as a NEW name stamped `accepted` --
> `transfer`'s `held` set is keyed on imported names and cannot match it. **The paragraph
> above says the load, the origin, the handle and the refusal column all worked. They did.
> The column measuring the outcome did not exist.**
>
> **AND THE TWO RULINGS COLLIDE WITHOUT EITHER BEING WRONG.** *The composition crosses; the
> binding does not* is correct. *`_explains` tests behaviour exactly* is correct. **Together
> they produce a quantity that cannot be non-zero**, and nothing in either ruling says so.

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

---

# THE ORDERING A/B WAS READING `idn`'s SYMMETRY — `differ: True` BEFORE AND AFTER, AND ONLY ONE OF THEM IS ABOUT ORDERING

**Re-read after the narrow cut, as ruled — *it may become measurable for free*. It did, and the
free part is not the one that was expected.**

    BEFORE                                    AFTER
    ordered   admits  9                       ordered   admits 13
    unordered admits  9                       unordered admits 13
    identical set: False                      identical set: False
    differ:        True                       differ:        True

    only-in-ordered                           only-in-ordered
      translate . idn<o1.w>                     recolour . recolour<o1.colour>
      translate . idn<o12.col>                  recolour . recolour<o8.colour>
      translate . idn<o15.row>?ACTION1          recolour . translate<o1.colour>?ACTION2
      translate . idn<o2.row>?ACTION1           recolour . translate<o16.colour>?ACTION2
    only-in-unordered                         only-in-unordered
      idn . translate<o1.w>                     translate . recolour<o11.w>
      idn . translate<o12.col>                  translate . recolour<o6.row>
      idn . translate<o15.row>?ACTION1          translate . translate<o16.row>?ACTION2
      idn . translate<o2.row>?ACTION1           translate . translate<o17.row>?ACTION2

> **THE BEFORE COLUMN IS THE SAME FOUR FUNCTIONS TWICE.** `translate . idn<o1.w>` and
> `idn . translate<o1.w>` share their operand, their guard and their behaviour — `idn` is the
> neutral element, so the two chains are one function written two ways. **The A/B reported that
> ordering changes what is admitted, and what it had actually detected was which side of the
> composition the identity landed on.**

**AND `differ: True` IS THE SAME VALUE IN BOTH COLUMNS.** The boolean cannot separate them; only
the differing elements can, and the boolean is what a reading records. **A true result, on a
real difference, that was not about its subject** — B17's shape without B17's protection,
because there was no label to check. **The instrument was the enumeration, not a name.**

### WHAT THE AFTER COLUMN ESTABLISHES, AND WHAT IT DOES NOT

Different first atoms, different operands, different bound attributes. **`recolour`-first on one
side and `translate`-first on the other, systematically** — not scattered, which is what a
budget boundary with a real preference looks like. **So clause 1 is now demonstrable on content:
ordering changes which terms survive a fixed budget.**

**It does not establish that the ordering is BETTER.** Both arms admit 13. Nothing here ranks the
ordered four above the unordered four, and **the quantity that would — whether the admitted set
pays more against the ground — is not measured.** *Coverage rose* would be the invented metric;
*a different set at the same count* is what was measured.

### 9 → 13 IS THE CUT, NOT THE ORDERING

**Both arms move together**, so the extra four are the budget no longer being spent on
`idn`-padded duplicates. **A direct consequence of the cut and not an ordering effect** — it
would be read as one from either column alone.


---

# B17's THIRD VARIANT: NO LABEL AT ALL, BECAUSE THE READING WAS THE MEASUREMENT

**Named from the ordering re-read.** The prior instances of *pre-registration does not protect a
reading if the instrument measures something else* all had **a name to look up in two places** —
`molecule`, `DIRECTED`, `BUDGET`, `PRIOR`. The check is *read the word in both places before
pinning a shape to it*, and it presumes there is a word.

> **`differ: True` HAS NO WORD.** It is a boolean over two sets produced by the enumeration
> itself. It read `True` before the `idn` cut and `True` after, **same value, opposite meaning**,
> and there was nothing to disagree with it because **the reading and the measurement were the
> same object.**

**SO THE TRIGGER IS DIFFERENT AND HAS TO BE.** `A6i` asks *what does this name mean in the other
place*. This asks: **can this reading be wrong while still being true?** A boolean over
constructed sets can, because the sets carry structure the boolean discards — **and the discarded
structure is exactly where a symmetry of the mechanism hides.** The check is to look at the
differing ELEMENTS at least once before trusting a difference, **and it costs one print.**

**IT IS A STEP, NOT A LAW, FOR THE SAME REASON THE OTHER FOUR ARE.** After the fact `differ:
True` is a clean reading with a clean provenance trail, and there is nothing to catch.

---

# THE CONTROL CAUGHT AN ATTRIBUTION — FIRST TIME THIS SESSION, AND THAT IS WHAT CONTROLS ARE FOR

**9 → 13 admitted terms, and both arms moved together.** From the ordered column alone the four
extra terms read as the ordering finding a better set. **What separates them is that the
unordered arm gained the same four**, so the cause is the cut, not the ranking.

> **Every other control this session CONFIRMED a clean state** — the toy panel's byte-identical
> output, the bit-identical enumeration runs, `_cannot_pay`'s zero terms lost. **This one
> reassigned a cause.** *A control that examines nothing cannot demonstrate a clean state* is the
> corollary already filed; this is its other half — **a control that examines something can take
> a result away from the mechanism that was about to be credited with it.**

### REGISTERED: WHAT WOULD SETTLE THE ORDERING, SO IT IS A GAP AND NOT A SILENCE

**Clause 1 is demonstrable on content; *better* is unmeasured.** The quantity is **whether the
admitted set pays more against the ground** — same budget, same count, and the ordered arm's
terms surviving more settles than the unordered arm's. **`settled_terms` after N cycles, both
arms, one panel.** Not run. It is cheap and it is not blocked on anything; it is registered here
so *13 either way* is never read as neutral evidence for the ranking.

---

# THE COVERAGE DENOMINATOR — FIXED, AND THE WARRANT WAS 298 ROWS CONTRADICTING THEMSELVES

**`ARC_BUILD_PLAN` §19.1 recorded this and left it**: *`Gamma.space_estimate` computes
`sum(units^d)` — `V^d`, not `λ^d`.* It was left because in the snaps world `λ = V = 8` made them
numerically identical. **In the three-space world they are not, and the consequence was printed
on every mint row.**

    BEFORE                                        AFTER
    verdict           n     coverage              verdict           n     coverage
    depth_exhausted  298    0.005078 .. 0.011065  depth_exhausted  298    1.000000 .. 1.000000
    pays              13    0.002031 .. 0.011065  pays              13    0.400000 .. 1.000000

> **`depth_exhausted` MEANS *I SAW THE WHOLE SPACE AT THIS DEPTH*. It printed `coverage 0.005`
> BESIDE ITSELF, 298 TIMES OUT OF 298.** §19.1's own rule is *coverage near 1.0 licenses "not at
> this depth"; coverage near zero licenses nothing at all.* **Every row made the strong claim in
> its verdict and withdrew it in its number**, and the two had been sitting adjacent in the
> ledger the whole time.

### THE FIX IS THE SPECIFIED QUANTITY COUNTED INSTEAD OF APPROXIMATED

§19.1 offers `≈ λ^d` **and says why: because `λ` was already computed.** That is a cost argument,
not a definition — `λ^d` is the ASYMPTOTIC FORM of the number of type-valid chains at depth `d`,
and **three things it cannot see are decided per call**: the closure starts only at `in_type`,
yields only at `out_type`, and now refuses `idn` inside a chain. `space_exact` counts them.

**AND UNLIKE AN ESTIMATE IT HAS A FALSIFIER, WHICH IS THE POINT.** Enumerate with an unbounded
budget; the count must agree exactly. **100 (in, out, depth) triples across four depths, 0
mismatches.** `val→val` at depth 3: emitted 15, counted 15 — **the same 15 the `idn` cut left.**

### `λ` IS COMPUTED OVER ATOMS, SO §23.5's MECHANISM COULD NOT HAVE APPEARED

> *More atoms means a larger `λ`, so `λ^d` grows and a fixed budget covers a smaller fraction —
> which shows up as coverage falling and, if nothing is done, as more false `UNREACHED`.*

**`type_report` builds its matrix from `self.atoms`, which MINT cannot add to.** So `λ` is
constant for the life of a run whatever the library does, and **a loaded library would have shown
no fall in coverage no matter what happened** — the mechanism §23.5 makes Phase 3c non-optional
for was structurally unable to appear. `space_exact` counts over `units()`, which grows as the
ground pays for chunks. **Fourth null-with-a-named-cause, and this one was found before the null
rather than after.**

### AND IT WAS POINTING THE ESCALATION LADDER AT THE WRONG RUNG

**The space at depth 3 is 15 candidates, not 2,954.** `budget_spent` never occurs in the run —
the budget was never the binding constraint. **Under `V^d` the agent read as having seen 0.5% of
a large space, which is a picture that argues for rung 2, *more budget*.** The true picture is
that rungs 1 and 2 are useless here and only **depth** or **arity** can help. §19.2 is not built,
so nothing acted on it; **the denominator would have chosen the rung when it is.**


---

# `type_report`'s DOCSTRING WAS MEASURING A GRAPH `4222e32` HAD ALREADY DELETED

**Found while checking `λ` before using it as a denominator.** The docstring reads the
three-space type graph as a **3-cycle `OBJ → ATTR → PRED → OBJ`**, gives the true spectral radius
as **`3.5569 = (5*3*3)^(1/3)`**, and calls the iteration's **`3.0000`** the bug — *the missing
0.557 was exactly the cycle*.

    the graph as it actually is
      OBJECT -> ATTR   5        a thing on the board, then one of its attributes
      ATTR   -> PRED   3
      PRED   -> OBJ    3        ... a COMPLETE OBJECTIVE. the path ends here
      val    -> val    3        the only cycle

> **`(5*3*3)^(1/3)` CLOSES THE CYCLE BY TREATING `OBJECT` AND `OBJ` AS ONE NODE** — which is the
> exact conflation commit `4222e32` was written to split, `arc_atoms.py`'s own comment saying so:
> *under one name the type graph had a node that was two things, and the closure composed across
> it — 225 pipelines at depth 4.* **So 3.0 is the true spectral radius, and the docstring names
> the correct value as the defect.**

**A REPAIR ONE LAYER UP FALSIFYING THE READING BELOW, AND THE READING KEPT ASSERTING THE OLD
WORLD.** The law is already filed — *a repair can break the layer above, and that is where causes
get asserted* — **and this is the first instance where the broken layer is a DOCSTRING rather
than a check.** Nothing could go silent, because nothing was running: a stale measurement claim
in prose is inert until someone believes it, and **the someone was going to be whoever wired
`λ^d` in as the denominator.** Repaired at source.


---

# WHAT THE WRONG DENOMINATOR WOULD HAVE COST, HAD ITS CONSUMER EXISTED

**It cost nothing, and the reason is build order rather than the size of the defect.** §19.2's
escalation ladder is not built, so no code read `coverage` and chose a rung. **That is the only
thing standing between this and a permanent misdirection**, and it is worth writing down because
a defect measured by its damage would score zero here.

    the ladder, and what the two denominators argue for
    rung 1  re-rank      free       V^d: "seen 15 of 2954" -- 0.5%, barely looked
    rung 2  more budget  linear     V^d: the obvious read. MORE OF THE SAME SPACE
    rung 3  more lag     xk
    rung 4  more depth   xlambda    exact: "seen 15 of 15" -- the space is EXHAUSTED
    rung 5  more arity   quartic    exact: the only two rungs that can change anything

> **`budget_spent` NEVER OCCURS IN THE RUN.** The budget was never the binding constraint and
> could not become one, because the whole depth-3 space is 15 candidates. **Rungs 1 and 2 are
> provably incapable of finding anything**, and `V^d` is precisely the picture that argues for
> them: *0.5% seen* is what "try harder in the same direction" looks like.

**AND IT WOULD HAVE BEEN SELF-CONFIRMING, WHICH IS THE WORST PROPERTY.** Escalate to rung 2,
spend more budget, find nothing — because there is nothing left to find — and the result reads as
*still under-explored*, arguing for rung 2 again. **The ladder climbs its two cheapest rungs
forever and never reaches depth or arity**, and every step of it is a ledger entry saying the
agent looked harder. **A false `UNREACHED` with five rungs of provenance behind it** is exactly
what §19.2 exists to prevent.

### THE RECORDING, WHICH IS THE GENERAL PART

**A defect whose cost is zero because its consumer is unbuilt is not a small defect. It is an
unexercised one**, and the two are indistinguishable by any measurement taken now. **Build order
decided which of those it was, not judgement** — the same accident that made `A6i`'s `BUDGET`
worth recording while nothing was wrong.


---

# ELEVEN OF FOURTEEN ATOMS ARE NEVER ENUMERATED — EXTRACT, RELATE AND QUANTIFY ARE INERT

**Found while measuring the warrant for the `ATTR` split, and it is larger than the warrant.**
Every `enumerate_closure` call in the live loop asks `("val", "val")` — three sites in `tether.py`,
one in `world.py`, one in `snaps.py`.

    reachable from (val, val)   idn  translate  recolour
    never enumerated            colour row col h w · same other above · all any none

> **§11.2 CALLS EXTRACT THE DECISIVE SPACE** — *without extractors there are no attributes;
> without attributes no predicates can be stated; without predicates no objective can be posed*,
> and it puts the break at link 2 of Figure 3's chain. **It is built, typed, and the mint never
> asks for it.** The three-space work exists as a vocabulary the loop has no way to reach.

**Fifth flavour of *mechanism present, never reached*, and the largest.** It is also the reason
two of today's numbers read as they do: `λ = 3.0` is the `val` self-loop **because the val
self-loop is the only part of the graph anything walks**, and the depth-3 space is 15 candidates
for the same reason. **Both were read as facts about the closure and they are facts about one
corner of it.**

---

# `ATTR` WAS A SPACE'S NAME USED AS A TYPE — SPLIT 2026-08-30

**§11.2's table names three composition SPACES**, one row of which is `ATTR × ATTR → PRED`.
**§12.3's table names the TYPES**: `OBJ → COLOUR`, `OBJ → POSITION`, `OBJ → EXTENT`, `OBJ → SHAPE`.
`_relate` cited §11.2 and typed on the space's name.

> **CORRECT ABOUT THE SPACE, WRONG ABOUT THE TYPE** — and the citation is why it survived, which
> is `_bindings`' finding arriving a second time: **a wrong implementation with a right source
> reads as derived, and so as already checked.**

**The consequence was `above` — an ORDER — applying to a colour**, which the colour ruling says is
a label that permutes on refresh, so `>` compares two arbitrary indices.

    closure OBJECT -> {PRED, OBJ}, depth 3      before   after
      terms                                        60      56
      `above` on POSITION or EXTENT                16      16
      `above` on a COLOUR                           4       0
      `colour . same`, `colour . other`            yes     yes

**The falsifier was *fewer meaningless terms, the same legitimate ones*, and it passes.** Equality
holds on every attribute and is untouched; order is refused by TYPE rather than by a rule naming
`colour`. **`space_exact` tracked the split with no change** — 196 (in, out, depth) triples, 0
mismatches — because the denominator is counted over the same `accepts` the closure walks.

### AND IT DOES NOT MOVE `λ`, WHICH IS A DIFFERENT ITEM

`λ` is 3.0 before and after; types 5 → 7. §12.5's *what changes is that the type graph becomes
sparse — which is the thing that was making `λ` uninformative* **is about the PREDICT atoms
getting real types instead of `val → val`.** The `ATTR` split sparsifies a region nothing walks.

### NOTHING ENTERED Γ, SO NO ADMITTING CLAUSE IS OWED YET

**This is a retyping of atoms already present, not an entry.** The `necessary` stamp for `shape`,
`overlap`, `delta` and `touching` is owed **at the moment they enter**, on §12.3's *the loop
cannot run without it* — and the three-of-nine split is an encoding accident rather than a second
admission decision, so the ablation partition is unaffected.

---

# §12.4 DOES NOT SPECIFY THE INTERSECTION QUERY — THE INDEX IS A PARALLEL MECHANISM

**Section check, asked before integrating the attribute work.** §12.4's trigger is an EQUALITY
test — *two slots with the same attribute vector and different residuals* — and its three guards
are support (*two slots differ and we cannot tell them apart*), reachability (**a composition of
sensors splits them**), novelty.

> **THAT IS A DISCRIMINATION QUERY: IN, TWO ATTRIBUTE VECTORS; OUT, A SENSOR THAT SEPARATES
> THEM.** An attribute index answers the inverse — in, attribute names; out, atoms carrying them.
> **§12.5 names the candidate generator outright**: *the sensor closure is the same enumerator.*

So the index is not §12.4's input, and cannot borrow its warrant. **It is a retrieval structure
over a large candidate set, which is §15.3 and §23.5's question**, and it has to be argued there —
where the standing finding is that `_explains` is `retrieve()`'s only consumer and the ranking
feeds a decision it cannot change.


---

# ONE ATTRIBUTE-TYPE TABLE — AND THE PRE-REGISTERED TRIGGER FIRED

**`slot_types()` returned the slot's KEY and called it the type.** §12.2: *`ATTR` alone is not
enough — `SAME(ATTR, ATTR)` would happily compare a colour to a cell count. **The attribute types
are what make the join sound.*** Its set is `COLOUR COUNT POSITION EXTENT SHAPE BOOL DELTA AXIS
RATIO`, in which `row` and `col` are one POSITION and `h` and `w` are one EXTENT.

### THE DUPLICATE WAS ONE COMMIT OLD AND IT WAS MINE

**`sensors.py:44-45` already declared all nine.** The `ATTR` split declared four of them again in
`arc_atoms.py` a commit later — **two producers of one fact, with identical strings**, which is
harmless exactly until one side changes. Imported now, and `ATTRIBUTE_TYPE` is the single key→type
table both `_extract` and `slot_types` read, **because a slot IS an object's attribute.**

### THE MEASUREMENT, PRE-REGISTERED, AND WHAT IT COULD NOT SETTLE

    ls20, 30 cycles          BEFORE     AFTER
    operand checks          666,311   532,289
    refused                 530,356   354,384
    refusal rate             0.7960    0.6658
    library (minted)             13         9   <- the pre-registered trigger
    mint events                  13         9
    defects                       0         0   8 seats, 16 gate checks

> **THE BEFORE/AFTER PAIR IS CONFOUNDED AND THE TRIGGER FIRED ON THE CONFOUND.** A different
> admitted binding means a different term, a different action, **a different board** — so the two
> runs are not one trajectory measured twice. **`13 → 9` cannot be attributed to the widening from
> these numbers**, and a pre-registration that names a quantity does not make the quantity
> comparable.

**THE TRAJECTORY-FREE MEASUREMENT IS THE ONE THAT ATTRIBUTES.** Enumerate every (target, bind)
pair under both type schemes — no run, no divergence:

    translate  (SAME_AS_TARGET)   admits 5 -> 9   NEW: (row,col) (col,row) (h,w) (w,h)
    recolour   (COLOUR)           admits 5 -> 5   unchanged

**Four pairs, every one within a type, and exactly §12.2's grain.** Cross-type is still refused.

### SO WHAT THE WIDENING BOUGHT IS THE BARGAIN CHOOSING DIFFERENTLY

**`recolour`'s admission set is bit-identical and its candidates are still reached 184,275 times**
— not starved by the ordering, reaching the bargain and not paying. So the terms that left did not
leave through the filter; **four extra `translate` bindings close residuals that `recolour` chains
previously closed.**

> **AND THAT IS A CAPABILITY CHANGE, WHICH `_operand_fits`' WARRANT DOES NOT COVER.** Its
> docstring's licence is *the narrowing costs no capability, which is the only kind of narrowing
> that is free* — measured as 80% refused with the library unchanged. **A widening is not that
> claim in reverse and does not inherit it.** Recorded as its own event, with its own number.

**WHAT THESE FOUR QUANTITIES CANNOT SAY IS WHETHER IT IS AN IMPROVEMENT.** Library size is
frame-internal — the count fell and the *kind* changed, and neither is evidence. **The
ground-facing quantity is residual closure, and it was not in the pre-registered set**, which is
the honest limit of this reading rather than a result to interpret around.


---

# B17's FOURTH VARIANT: THE FLAW WAS IN THE MEASUREMENT'S DESIGN, AND IT WAS APPROVED

**Pre-registration protected nothing here, and for a new reason.** The first three variants had a
NAME whose two meanings could be looked up — `molecule`, `DIRECTED`, `BUDGET`, `PRIOR`. The third
had no name at all, the reading being the measurement. **This one has a well-defined quantity,
correctly named, measured before and after, and the pair is not comparable.**

    library (minted)   13 -> 9      registered in advance as the trigger
                                    and a different admitted binding means a different
                                    action, so the two runs are not one trajectory twice

> **NAMING A QUANTITY IN ADVANCE DOES NOT MAKE THE QUANTITY COMPARABLE.** Pre-registration fixes
> WHAT is measured and says nothing about whether the two measurements share a subject. **A
> before/after on a system whose behaviour the change alters is two subjects**, and the discipline
> that is supposed to catch fitting is silent about it.

**AND THE PART WORTH RECORDING IS WHO WROTE IT.** The pre-registration was Isaiah's, approved and
carried out as specified, **and the flaw was in it at the moment of approval.** Both of us read it
as sound. **A registered quantity reads as a decision already made**, which is exactly the
property that makes registration valuable and exactly what stops it being re-examined.

**THE CHECK IS ONE QUESTION AND IT IS CHEAP:** *does the change alter the trajectory the
measurement is taken over?* If yes, the before/after is confounded and something trajectory-free
is needed — **which existed here, cost one enumeration, and settled it exactly.**

---

# THE DUPLICATE WAS FOUND BY BUILDING THE CONSUMER, NOT BY READING EITHER FILE

**`sensors.py` declared §12.2's nine types; the `ATTR` split declared four of them again one
commit later.** Identical strings, so **no check could fire and no diff would look wrong** — and
`grep COLOUR` returns both without either looking like a mistake.

> **IT SURFACED WHEN ONE THING NEEDED TO READ BOTH.** `slot_types` had to name the same types
> `_extract` names, and at that moment the question *where does this constant live* has exactly
> one right answer and the repo had two. **Neither file is wrong when read alone. The pair is
> wrong, and only a consumer of both is positioned to see it.**

**WHICH IS A DIFFERENT DETECTION MODE FROM EVERY LAW IN `CLAUDE.md`** — those install something
that fires, or are steps taken before the work. **This one is a shape that becomes visible only
when a third thing depends on both halves**, and until then it is two correct files.


---

# THE FIXED-SEQUENCE MEASUREMENT — 45% WAS THE CONFOUND, 1.6% IS THE EFFECT

**`step(action=...)` already accepted a forced action, so the replay needed no new mechanism.**
Both arms run the same 30 actions, see the same boards, and differ only in whether `slot_types`
declares §12.2 types or slot keys. **Taken in both directions** — once on each arm's own free
trajectory — so neither arm is measured only on ground it chose.

    FREE (each its own trajectory)          FIXED, TYPED's seq      FIXED, KEYED's seq
      typed  integral 233.128  lib  9         typed  233.128  9       typed  421.850  13
      keyed  integral 425.551  lib 13         keyed  236.828  9       keyed  425.551  13

**THE LIBRARY DIFFERENCE IS ENTIRELY TRAJECTORY.** On a fixed sequence both arms mint the same
count — **9 and 9, 13 and 13.** The pre-registered `13 -> 9` was confound with nothing under it,
**and that is now measured rather than argued.**

**THE REAL EFFECT IS -3.70 BITS, THE SAME IN BOTH DIRECTIONS** — `236.828 -> 233.128` and
`425.551 -> 421.850`, identical to three decimals, **which reads as one recurring correction
rather than a diffuse gain.** Sign consistent under the symmetric check. **1.6% of the integral.**

> **THE FREE COMPARISON WOULD HAVE READ AS A 45% REDUCTION IN SURPRISE.** `425.551 -> 233.128`.
> **The effect is 1.6%, so the confound overstated it by 29x, and in the direction that flatters
> the change.** Not a distortion at the margin — it would have been the headline, it was
> pre-registered, and every number in it is correctly computed.

**THE INSTRUMENT WAS ALREADY THERE AND IT IS THE WRONG ONE OF TWO — CORRECTED.** `DISCOVERY`
names them in consecutive bullets: **`pe_integral()`** is *every surprise ever, monotone
non-decreasing* and is built as `_integral`; **`outstanding()`** is *surprise not yet explained*
and is annotated ***this is the aim and the currency*** — **and it does not exist in the code**,
nor does `explain(bits)`. **So this reading is PREDICTION ERROR on a fixed sequence, not residual
closure**, and the two differ exactly where it matters: the integral rises whether or not the
library explains anything. Direction and magnitude are unaffected; the name was.

**AND THE LAW FIRED ON THE READING RATHER THAN ON THE BUILD.** *Assume it is already specified,
and go look* — the lookup happened AFTER the measurement, and what it found was that the corpus
distinguishes two quantities where the reading assumed one. **The instrument being present is what
stopped the search**, which is the familiarity failure in its exact form: finding something is
evidence in the wrong direction.

### WHAT IT LICENSES, WHICH IS LESS THAN IT LOOKS

**The widening is not a regression**, and on the ground-facing number it is slightly positive both
ways. **It does not license *the typed grain is better***: 1.6% on one game over 30 cycles, with a
single-correction signature, is a reading consistent with the two schemes being near-equivalent
**and with the four newly-admitted pairs mattering once.** The reason to keep it is §12.2's, not
this number's.


---

# `outstanding()` AND `explain(bits)` — BUILT 2026-08-30. THE AIM EXISTED AS A SPEC AND NOT AS A NUMBER

**`DISCOVERY` names two quantities in consecutive bullets and the code had one.**

    pe_integral()   every surprise ever, monotone non-decreasing        built as `_integral`
    outstanding()   surprise not yet explained -- THE AIM AND THE       ABSENT
                    CURRENCY
    explain(bits)   reduces outstanding only; the integral is           ABSENT
                    untouched

> **THE FIRST COUNTER-INSTANCE TO THE NINE.** Every prior case of *assume it is already
> specified, and go look* found the specified instrument PRESENT and better. **Here the corpus
> named the aim, annotated it as the currency, and it was not there at all** — so the tally is
> nine specified-and-present and one specified-and-absent, **and the absent one is the aim.**
> *Most of this system is specified-and-unconsumed* was the wrong reading of the nine.

### PER SLOT, WHICH IS A DEVIATION FROM THE SPEC'S OWN SIGNATURE AND THE RULE OUTRANKS IT

`DISCOVERY` writes `outstanding()` and `explain(bits)` — nullary, scalar. **`CLAUDE.md`: *No
aggregation across slots. R is indexed per object slot. Averaging is how a live signal
disappears.*** Stored per slot; `outstanding()` sums on read, **so the total is a reading and
never the storage.** `explain` takes the slot.

**AND IT PAID ON THE FIRST RUN.** `o10.row` and `o11.row` hold 33.3 bits each of the 99.9
outstanding — **the surprise is concentrated, and the scalar the spec asked for could not have
said where.**

### THE IDENTITY IS THE FALSIFIER, AND THE CLAMP IS REPORTED

    pe_integral  233.128   =   outstanding  99.912   +   explained  133.218
    monotone: True             overclaimed 0.000 on 9 of 9 mint rows

**`base - left` and the accumulated per-step mass are two accountings of one slot's residual**,
and whether they were commensurable was an assumption. **Zero overclaim on every row measures
it.** The clamp returns what it swallowed rather than swallowing it — *a clamp that reports
nothing is an absence rendered as a value*, and that flavour has now been caught three times.

**43% of the run's surprise is explained and 57% is outstanding** — the first ground-facing
closure figure this loop has been able to produce, and the denominator every closure claim from
here reads against.


### AND THE LINT REFUSED THE FIRST VERSION OF THIS COMMIT

    ISOLATED  FAIL - tether.py: `pe_integral`: defined and referenced nowhere in the package

**`pe_integral()` was called only by the probe that measured it.** Reading `self._integral`
directly at the one site that reports it left the specified accessor as a synonym sitting beside
the raw attribute — **a mechanism present and never reached, added while writing the record of
five other instances of exactly that.** The report now reads through it.

> **THE CHECKER'S SCOPE IS THE PACKAGE AND THAT IS WHY IT FIRED.** A probe outside the package
> exercised the method perfectly, and *tests reach, not existence* is the law that makes an
> external caller not count. **Being able to demonstrate it from a script is precisely the state
> ISOLATED exists to refuse**, and it is the seventh site.


---

# ELEVEN OF FOURTEEN WAS TRUE AS A FACT AND WRONG AS A DIAGNOSIS — RETRACTED

**The item was *the mint asks for the slot's declared type*, and it is measurably wrong.**

    RELATE/QUANTIFY candidates against real slot histories, ls20/20
      (candidate, binding) pairs tried    476
      pairs that BEAT the held term         0
      closest any came                     25.9 bits WORSE
      all(v) -> 0 or 1                     vs a slot value in [0, 13)

**§11.2's TABLE ASSIGNS THE CONSUMER AND I READ PAST IT.**

    PREDICT             slot x action -> slot         what can be BET ON
    RELATE / QUANTIFY   ATTR x ATTR -> PRED -> OBJ    what can be STATED AND WANTED
    EXTRACT             grid x object -> ATTR         what can be REPRESENTED AT ALL

**The mint bets. These atoms state.** Everything downstream of an extract atom is a truth
value, so **no chain from a slot type can produce a slot value** — not marginally, structurally.

> **SO *ELEVEN OF FOURTEEN ARE NEVER ENUMERATED* IS THE CORRECT BEHAVIOUR OF A MINT THAT BETS.**
> Five EXTRACT atoms duplicate what perception already publishes as slots; six RELATE/QUANTIFY
> atoms cannot pay a betting bargain. **The fact was right, the reading was that a space was
> being starved, and the space was never the mint's.** Same shape as `differ: True` — a true
> observation whose subject was wrong.

### AND BUILDING IT WOULD HAVE CORRUPTED THE DENOMINATOR COMMITTED AN HOUR AGO

**476 unpayable candidates per slot per cycle enter `space_exact`'s count and `candidates_seen`
alike.** Coverage rises, `outstanding` does not move, and every `UNREACHED` verdict is taken over
a space most of whose members are structurally incapable of explaining anything. **A metric whose
denominator the mechanism changes cannot falsify that mechanism** — the law, arriving at the
build that would have triggered it.

### THE SIX HAVE TWO SPECIFIED CONSUMERS AND NEITHER IS THE MINT

- **§12.4's discrimination.** *A composition of sensors splits them* — `same(v, operand)`
  separates two slots with the same attribute vector. **It does not bet, so a truth value is
  exactly the right output.**
- **The objective side.** §11.2's *stated and wanted*, and `DISCOVERY` Q21's `score_molecule` —
  *one bargain, two levels*. A `PRED -> OBJ` chain IS a candidate objective, and `grammar.T.OBJ`
  glosses `OBJ` as *a complete objective*. `env.objective()` is currently only read.

**WHICH COLLAPSES THE CHAIN'S ITEMS 2 AND 4 INTO ONE.** The six become useful when a
discrimination consumer exists, and not before — and `shape` is the same case, since `OBJECT ->
SHAPE` cannot be bet on either. **The whole EXTRACT/RELATE/QUANTIFY half of Γ has one consumer.**


---

# THE AUDIT: WHAT THE CORPUS NAMES THAT HAS NO REFERENT — RUN 2026-08-31

**A different search from *what is built and unreached*, which is the one that has been running
all week.** Every `name(...)` written inside backticks across the seven corpus documents, checked
against every name the package defines. **39 distinct, and they sort into five classes — only one
of which is dangerous.**

    A  LOAD-BEARING INSIDE BUILT MACHINERY, no referent      outstanding · explain · density
    B  ABSENT AND DECLARED ABSENT BY THE CORPUS ITSELF       suppress · Act · Seq · Until
                                                             holes · parity · ratio
    C  INSIDE A SECTION THAT IS WHOLLY UNBUILT               orthogonality · prime
    D  PRESENT UNDER ANOTHER NAME                            position · extent · delta
                                                             reachability · is_refuted · HAS_COLOUR
    E  NOT OURS                                              MyAgent · Arcade · choose_action
                                                             logical_read · float · H · T_A · T_E

**CLASS B IS THE ONE THAT MAKES THE AUDIT WORTH RUNNING, BY BEING SAFE.** `There is no
`suppress()`` and §15.5's *in the basis today: **no*** are the corpus tracking its own gaps.
**A gap the corpus declares is not a defect; a gap it does not is.** Without the split, 39 names
read as 39 problems and the audit would be noise.

### THE NEW HIT IS `density(R)`, AND IT IS `outstanding()`'s SHAPE EXACTLY

**§11.6 settles where the curiosity drive lives, and rests it on the quantity:**

> *the curiosity trigger **must be on the transition channel**, because `density(R) ≈ 0` on the
> reward channel is the normal state and would fire the drive permanently.*

**The three channels are built. The drive is built. `density` has never been computed** — so a
placement decision in running code rests on *a panel property asserted from the shape of the
generator*, which is the corollary's exact subject.

    ls20 / 30 cycles       per bet     per step (what `drive.note_step` consumes)
      reward                0.0000     0.0000
      bracket               0.0000     0.0000
      transition            0.0200     0.8000

**MEASURED, AND THE PREMISE HOLDS** — 0.0000 against 0.8000 is the distinction the argument
needs. **But the word carries two denominators 40x apart, and under the other one the argument
fails**: 0.00 against 0.02 is two channels that are both nearly always zero. **`A6i` in a
quantity rather than a label** — and the corpus's gloss (*`levels_completed` moves rarely*) and
the code (`note_step`, per step) resolve it the same way without either saying so.

### TWO SIDE FINDINGS

**§15.5's table is stale on one row.** It lists `When(P, R)` under *in the basis today: **no***,
and `Term.guard` is a real `When(P, R)`, built and committed. `Act`, `Seq` and `Until` are still
correctly **no**. **Corpus, so recorded and not fixed.**

**`quantifier(ALL/SOME/ONE/NONE)` names four and `_quantify` builds three.** `all`, `any`, `none`
map to ALL, SOME, NONE. **`ONE` — exactly one — has no atom.**

### THE RATE, AND WHY IT ARGUES FOR RUNNING IT AGAIN

**Two Class-A hits from two items, both found by accident before the search existed.** The search
is one regex over seven documents and it took minutes. **`what is built and unreached` and `what
is named with no referent` are different searches over the same corpus**, and only the first had
ever been run.


---

# THE SEMANTIC PASS — ROLES AND CONSUMERS, NOT STRINGS. ONE HIT, AND A CORRECTION TO THE RATE

**The mechanical pass finds names wearing parentheses. This one runs over TABLE SHAPES** — every
corpus table with a *lives in* / *consumer* / *status* column, nine of them.

    §12.1  seven prior shapes, `lives in`      ALL SEVEN HOMES EXIST -- clean
    §11.2  three spaces, `status`              STATUSES DECLARED -- Class B
    §15.3  four retrieval keys                 effect shape unbuilt, ALREADY RECORDED
    Q26    the eight-slot Env protocol         ALL EIGHT built on `ArcWorld` -- clean
    Q24    requisite variety, `H(...)`         DECLARED AT THE SITE -- Class B
    Q25    the branching test                  **CLASS A**

### AND IT CORRECTS THE RATE I USED TO ARGUE FOR RUNNING IT

**§11.2's status column reads *`grammar.py` exists, unwired* and *EXTRACT: missing*.** I called
RELATE/QUANTIFY's absent consumer the audit's second hit. **The corpus declares both, so it was
Class B all along** — the same distinction that makes the audit an instrument, applied to my own
count and taking one off it. **Two Class-A hits from the mechanical pass, one from this one.**

### Q25 IS A CHECK, WHICH IS A THIRD SHAPE

> *An invertible transform, iterated, is a permutation — orbits, not a tree... **a tower of
> seats, agents, or generations that has produced no divergence has no transform and is a copy
> loop however deep it goes** — and that is visible without access to the transform itself.*
> **Recommendation. Ship it as a check on any multi-level structure the build grows. Cheap,
> external, and it fails loudly.**

**The library chain IS that structure** — `ls20 → sk48` through `save`/`load`, with `IMPORTED` as
its own admitting clause — **and it is built.** Nothing implements the test and no site declares
the gap. **`outstanding` and `density` were quantities; this is a diagnostic**, which is why no
regex over callables would have surfaced it.

**AND THE DATA TO RUN IT ON ALREADY EXISTS.** The holdout runs read `imported held/pulled: 3/0`
and `11/0` — **inherited terms were never pulled.** That is not the same claim as *no divergence*
and it points the same way: **the second generation produced nothing from its inheritance.** The
check is not built and I have not run it; **what is recorded here is that the subject exists, the
structure is built, and the diagnostic the corpus recommends for exactly this has no referent.**

### WHY IT MATTERS MORE THAN ITS SIZE

**It is the cheap external half of the terminal condition's clause 3.** The ablation wipes Γ and
re-runs, and `CLAUDE.md` defers it to 25/25 because below mastery *neither number is
interpretable*. **Q25 needs no mastery**: a tower either branched or it did not, and that is
readable now, on runs already taken.


---

# Q25's BRANCHING TEST — BUILT 2026-08-31, AND GENERATION 2 READS `False`

**The audit's Class-A hit from the semantic pass, built as `summary.branching`, called by
`arc_holdout.play`.**

    gen 0  ls20   inherited  0   final 15   added --   diverged None   cold: cannot branch
    gen 1  sk48   inherited 15   final 20   added  5   diverged True
    gen 2  g50t   inherited 20   final 20   added  0   diverged False  <- fires

**`g50t` INHERITED 20 COMPOSITIONS AND RETURNED 20.** The older holdout row for the same game
reads *minted 12* — **twelve terms minted, zero new shapes.** The library grew in bindings and
not in compositions, which is *fifty saved entries were eleven shapes* with a verdict attached.

### THE DESIGN DECISION IS THE WHOLE CHECK: COMPOSITION, NEVER BINDING

**Bindings are re-decided per slot in every game**, so a binding-keyed difference is non-empty by
construction and `diverged` could never read `False`. **A check that cannot fail is not a check**
— *a metric whose denominator the mechanism changes cannot falsify that mechanism*, arriving as a
design constraint rather than as a post-hoc catch. The atom sequence is what `save` carries and
what `units` composes over, so it is what a generation can be said to have added.

**AND ALL THREE VERDICTS WERE SHOWN REACHABLE BEFORE THE RUN** — `None` on a cold parent, `False`
on an identical inheritance, `True` on one composition more. **A diagnostic whose failure state
has never been produced is an assertion.**

### THE COLD-RUN FIELD WAS AN ABSENCE RENDERED AS A MAXIMAL DIFFERENCE

With no parent, `added = final - {}` listed **the entire library, atoms included**, as new
compositions. The verdict was already `None`; the list was not. **Null now, like the verdict it
belongs to** — fourth instance of that flavour, and the first caught by reading the code between
writing it and reading its output.

### THE VERDICT DOES NOT TRAVEL ALONE, AND SHIPPING IT ALONE WAS HALF A MECHANISM

> **No divergence is a copy loop only if there was something left to explain.** If `g50t`'s
> residuals were already covered by the inherited shapes, retrieving was correct and there was
> nothing to compose.

**Which is the terminal condition's clause 3 asked cheaply** — *if the win survives the agent
composed it; if it disappears the library was carrying the answer and the agent was retrieving.*
**`outstanding()` is the disambiguator and it was built two commits earlier**, so the holdout
report now carries `pe_integral` and `outstanding` beside `branching`. **Neither reading is a
claim without the other.**

### DETERMINISM, ARGUED AND BEING CONFIRMED

`ls20`, `sk48` and `g50t` contain no randomness, and the loop's only random call is the handle
suffix, which touches no decision. **So one run is the verdict rather than a draw.**

**CONFIRMED: the repeat run is identical on every field** — inherited, final, added and verdict
across all three generations, and the same five compositions at gen 1. **The argument from the
absence of a source and the measurement agree**, which is the order to do them in: the argument
said what to expect and the run could have refuted it.

**AND THE FIVE ARE ALL PREDICT-SPACE** — `recolour . recolour`, `recolour . translate`,
`translate . recolour`, `translate . translate . translate`, `recolour . recolour . recolour`.
**Every composition this tower has ever added is drawn from the three `val → val` atoms**, which
is the one corner anything enumerates. The branching that exists is happening in 3 atoms of 14.


---

# §12.4's SECTION CHECK — TWO `A6i` INSTANCES, RECORDED BEFORE THE BUILD

**Both are PROSPECTIVE, and the item that would collide with them is nameable: §12.4's trigger,
which is the next build.** That is the condition `BUDGET` established for recording a cleared
hazard, and it is what stops a register filling with near-misses.

### `slot` — AND IT DECIDES WHAT IS PERMITTED, NOT ONLY WHAT IS MEASURED

    corpus   a slot is an OBJECT             §12.3: "no slots, so `R` cannot be indexed per slot"
                                             §12.3 s3: "a slot is not the SAME slot next frame"
    code     a slot is an OBJECT.ATTRIBUTE   `env.slots()` -> 100 names over 20 objects

**Five code-slots per corpus-slot — and that gap is exactly §12.4's *attribute vector*.** The
trigger reads, translated: **two OBJECTS whose attribute values all match and whose residuals
differ**, and the code's `slot` cannot express it.

> **AND THE HARD RULE READS OPPOSITE WAYS UNDER THE TWO MEANINGS.** *No aggregation across slots*
> — forming an object's residual from its five channels is aggregation ACROSS slots in the code's
> vocabulary and WITHIN one slot in the corpus's. **A step that is required under one reading is
> forbidden under the other**, which is the first `A6i` to change a permission rather than a
> number.

### `residual` — THREE QUANTITIES, AND ONE OF THEM I BUILT THIS WEEK

    outstanding      surprise not yet explained          `DISCOVERY`, built 2026-08-30
    per-step mass    this step's correction bits         `SlotResidual.mass`
    |R| held         over the slot's history vs the      `_accumulated` -- what the MINT
                     term currently bound                calls `base`

**Adding `outstanding` two commits ago made this word carry three quantities**, which is worth
noting on its own: **a new instrument can create an `A6i` rather than only inherit one.** The
mint's `base` is the codebase's own meaning and is the one to read §12.4 against.

### THE VECTOR IS FEATURAL, AND THE CORPUS DOES NOT SAY SO

    pairs sharing (colour, row, col, h, w)   0     across 25 steps, 21 objects
    pairs sharing (colour, h, w)            75

**Zero is structural, not rare: two distinct objects cannot share a position**, and `priors.py`
carries solidity as a CONSTRAINT saying so. **So the trigger with position in its vector can
never fire** — and the null would have read as *no two slots are ever indistinguishable* when the
cause is that the test included the one attribute that cannot collide.

**AND §12.4's OWN REMEDY SETTLES THE FIX RATHER THAN MY PREFERENCE.** Its example is
`parity(position)` — **position is what the new sensor reads to SPLIT them, so it cannot also be
what made them look alike.** Derived from the corpus's example, not chosen.


### THE PANEL PROPERTY — AND `ls20` ALONE WOULD HAVE KILLED THE BUILD

    25 steps each        objects   featural-dup pairs   same |R|   TRIGGER   steps fired
      ls20                    21                  100        100         0        0 / 25
      sk48                    70                 5161        663      4498       25 / 25
      g50t                    15                    8          0         8        7 / 25

**`sk48` fires on every step. `g50t` fires on 7 of 25 and every pair it finds triggers. `ls20`
never fires.** One panel was measured first and it is the outlier.

> **THE PRECEDENT IS THE DS LADDER, RUNNING IN THE OPPOSITE DIRECTION.** *Called easing on ten
> seeds, flat on forty* is cited against over-claiming a POSITIVE. **This is the same error with
> the sign reversed — over-claiming a NULL — and it is the more dangerous one, because a null
> presents as caution.** *§12.4's trigger cannot fire* was drafted, with a mechanism-shaped
> explanation attached (*objects that look alike behave alike*), and it was a fact about 21
> objects on one board.

**AND THE EXPLANATION WAS THE TELL.** A null with a satisfying causal story is harder to doubt
than a bare one. **The story was true of `ls20` and general in its wording**, which is exactly how
a panel fact becomes a mechanism claim.

### WHAT IT MEANS FOR THE BUILD

**§12.4 is demonstrable, and the trigger is if anything too permissive.** 4,498 triggering pairs
over 25 steps on `sk48` is ~180 per step; if each launches a sensor search the mechanism spends
its whole budget on the trigger. **§12.4 prices the REMEDY by the bargain and says nothing about
ordering the triggers** — so the ordering question is real, unspecified, and the next thing to
check rather than to invent.


---

# §12.4's TRIGGER — BUILT 2026-08-31, RANKED BY VECTOR MULTIPLICITY

    25 steps each   steps fired   groups/step   max multiplicity   top group's |R| gap
      ls20             0 / 25          0.0            --                  --
      sk48            25 / 25          8.0            24               66.42
      g50t             7 / 25          0.3             2               36.54

    sk48's top group   vector [COLOUR 2, EXTENT 1, EXTENT 1] x 24 objects

**Twenty-four objects, all colour 2 and all 1x1, whose residuals span 66 bits.** The vocabulary
says they are one thing; the world says they are not. **That is §12.4's condition, on a board.**

### THREE DERIVATIONS, NONE OF THEM CHOSEN

**The subject is an OBJECT**, because a corpus slot is one and a code slot is one of its
attributes. **The grouping is declared by the domain** — `ArcWorld.slot_owner`, the same shape and
the same reason as `slot_types`: *a loop that split on `.` would be reading domain structure.*
**The vector is featural**, because solidity makes a position-bearing vector unmatchable and
§12.4's own remedy `parity(position)` puts position on the remedy's side.

**AND *FEATURAL* IS EXPRESSIBLE ONLY BECAUSE THE TYPES EXIST.** It is `!= POSITION`, not a list of
attribute names — **the `ATTR` split from four days ago is what makes this line writable.**

### THE RANKING IS MULTIPLICITY, AND THE ALTERNATIVE WAS THE TRAP

**Ranking by the residual gap ranks on a quantity the mechanism moves.** *How many objects shared
the vector* is fixed before any sensor is composed: **the remedy changes what splits them, never
how many looked alike.** A ranking and never a cut — the bargain still decides which remedy pays.

### THE DEFECT I INTRODUCED, AND WHAT CAUGHT IT

    before   sk48 multiplicity 21, vector [['COLOUR', 2]]        <- ONE element
    after    sk48 multiplicity 24, vector [COLOUR 2, EXT 1, EXT 1]

**`slots`, `alphabet` and `slot_types` are refreshed at THREE sites** — init, retarget, and a
per-step one that fires when *an object arrived or left*. **I held owners as a field and
maintained the invariant at two of the three; the one I missed is the object-arrival site, which
is the exact case this trigger exists for.** `get(s, s)` then made every unmapped slot its own
single-attribute object, **ten of which matched each other on a bare colour and read as a
21-object discrimination failure.** Reading fresh removes the invariant rather than maintaining
it.

> **WHAT CAUGHT IT WAS THE VECTOR BEING IN THE LEDGER ROW.** `pairs` and `multiplicity` alone read
> as a strong result; `vector [['COLOUR', 2]]` is visibly wrong to anyone who knows it should have
> three elements. **Legibility as the instrument, doing the job the doctrine claims for it** — the
> record named the shape and the shape was the defect.

**FIFTH INSTANCE OF AN ABSENCE RENDERED AS A VALUE, AND THE FIRST I INTRODUCED** — written while
composing the record of the other four. **The fallback is where it entered**: `get(s, s)` turns
*no declared owner* into *is its own owner*, the same move as a clamp that swallows what it
clamped.

**AND MY FIRST EXPLANATION WAS WRONG AND IS CORRECTED AT THE SITE.** I wrote *held on the agent it
went stale*, which would make `slot_types` stale too — **measured at 0 untyped slots over 15 steps
on both panels, so the sibling is clean and the cause was a missed refresh site, not staleness.**
A wrong cause recorded in code is worse than none.

### `CLAUDE.md` REPAIRED: THE SAMPLE-SIZE COROLLARY NOW STATES BOTH SIGNS

*Ten seeds versus forty* was filed against over-claiming a positive. **Over-claiming a null is the
worse case, because a null presents as caution and needs no defence** — and the tell is the
explanation, since a null carrying a satisfying causal story is harder to doubt than a bare one.


---

# §12.4's REMEDY — BUILT, AND ITS VERDICT IS `UNREACHED` WITH A DENOMINATOR

**`sensors.py:95`'s booked debt is paid.** `Registry.accepting` and `Registry.closure` exist;
`env.sensors()` hands the loop the registry the way `env.atoms()` hands it Γ's vocabulary.

    g50t   fired 5/20   top multiplicity 2, gap 16.61
                        remedy {closure 4, composable 0, verdict UNREACHED}
    ls20   fired 0/20   no trigger, so no remedy

**NOVELTY EXCLUDES THE BARE SENSORS**, because *the current sensor set says those slots are
identical* is the trigger's own premise — so a remedy has to be a COMPOSITION, and §12.5 names
the guard as *novelty (not already a sensor)*. **There are none, so the agent abstains, and the
abstention carries the number that makes it checkable.** §12.4: *we can know the closure of our
own sensor set, and therefore we can still score whether abstention was correct.*

### THE VERDICT IS STRUCTURAL, WHICH DEFERS THE BLOCKER INSTEAD OF HITTING IT

**Evaluating a candidate against two objects needs the objects, which the loop does not have.**
There are no candidates, so **the answer does not depend on which objects triggered** — and the
objects-into-the-loop question defers to the moment a composable candidate exists.

### THE REASON I FIRST RECORDED WAS WRONG, AND THE OTHER ENTRY POINTS CAUGHT IT

    from (OBJECT,)          4 chains, longest 1
    from (FRAME,)           5 chains, longest 2   <- components . colour, . position, . extent, . shape
    from (OBJECT, OBJECT)   3 chains, longest 1
    accepting(COLOUR | POSITION | EXTENT | SHAPE | RATIO | DELTA | BOOL | REGION)   all EMPTY

**I wrote *no sensor accepts another's output* and it is false** — `components . colour` composes.
**The true statement is narrower: nothing accepts an ATTRIBUTE type**, so a chain that reaches one
terminates, and from an OBJECT that is one step. **Second wrong cause recorded in this build**,
and both were caught by measuring an adjacent case rather than by re-reading the claim.

### AND THE CIRCLE IS THE FINDING

**What would accept an attribute type is `parity(POSITION)` or `holes(SHAPE)` — §12.4's own
examples of what the agent should compose.** §12.3 forbids installing them, *because reaching is
the only evidence the composition system works.*

> **So the reach mechanism cannot reach.** The nine terminate at attributes; Tier 2 is exactly the
> class that would extend past one; and Tier 2 may only enter by being reached. **`UNREACHED` is
> therefore the correct and permanent verdict under the current entry rule** — not a gap in the
> build, and not something more search would fix.

**WHICH IS WHY THE ABSTENTION IS THE RESULT RATHER THAN A DISAPPOINTMENT.** The agent says *I
cannot tell these apart, and I cannot build an instrument that would, from what I hold* — and
names the closure it searched. **That is the alignment claim at the perception level, measured.**


---

# AN ADJACENT CASE IS A BETTER INSTRUMENT THAN RE-READING THE CLAIM

**Both wrong causes in the §12.4 build were caught the same way, and it was not by checking the
reasoning.**

    claim   "held on the agent it went stale"        the SIBLING was the control:
                                                     `slot_types` measured 0 untyped slots
                                                     over 15 steps on both panels, so it was
                                                     unaffected and the hypothesis died
    claim   "no sensor accepts another's output"     the OTHER ENTRY POINT was the control:
                                                     `closure(("FRAME",))` returns
                                                     `components . colour`, so composition
                                                     exists and the wide claim was false

> **A CAUSE STATED ABOUT A MECHANISM PREDICTS SOMETHING ABOUT ITS NEIGHBOURS.** *Fields on the
> agent go stale* predicts `slot_types` is stale too. *Sensors cannot compose* predicts every
> entry type is flat. **Both predictions are cheap, and both were false** — where re-reading the
> claim would have found it plausible each time, because it was written to be.

**AND THE CORRECT NARROWER CLAIM SURVIVED IN BOTH CASES.** The cause was a missed refresh SITE,
not staleness; nothing accepts an ATTRIBUTE type, not nothing composes. **The wide version is
what a plausible explanation reaches for**, and the adjacent case is what distinguishes them.

**`producing` IS THE THIRD, AND ISOLATED FOUND IT.** Booked beside `accepting` in a comment
promising both to §12.4, and §12.4 needed one. **The check fired on a debt rather than on a
build** — a booked debt is a guess about what a mechanism will need, and it is worth checking
against the mechanism when the mechanism arrives.


---

# PRE-REGISTERED, BEFORE THE REBUILT TRANSFER COLUMN RUNS

**A number that has never been non-zero has no baseline**, so anything above zero would read as
success. The meaning is fixed here, in advance.

    what is being changed
      1  `characterise` reports WHICH TYPES varied, not which slots
      2  `key_of` reads `Term.operand_type` -- declared at construction, so it CROSSES --
         instead of `term.operand`, which is a slot name and does not
      3  the pull site RE-BINDS a candidate that reads an operand and holds no binding,
         which is what "binding does not cross" requires and the import path never did
      4  `transfer` keys on the COMPOSITION, and the sweep's reuse emits a `pull` row

    what would falsify the rebuild
      *  a term that paid before and does not now -- the third key must ORDER, never admit
      *  `space_exact` disagreeing with the enumeration -- the type change touches `accepts`
      *  8 seats, 16 gate checks

    what a non-zero reading DOES NOT license
      *  `imported_pulled > 0` is NOT evidence of transfer on its own. A re-bound imported
         composition explaining a slot is **one composition, one slot, one board.**
      *  The claim needs the pull to be on a board the term was NOT minted on, which the
         handle's prefix already records -- **so the reading is `pulled AND handle-prefix !=
         this game`, and anything else is a local reuse wearing an import's name.**
      *  A rise from 0 is not an improvement over a measured 0. **The old number measured
         nothing**, so the first honest reading has no predecessor and must not be reported
         as one.


---

# PRE-REGISTERED: THE COMMENSURABILITY WIDENING

**Does this change alter the trajectory the measurement is taken over? YES** — new bindings admit,
so different terms are minted, so different actions are taken. **Fixed sequence is therefore the
only comparable form, and that is settled BEFORE approval rather than discovered after.** B17's
fourth variant, applied in advance for the first time.

    three arms, one fixed action sequence
      A  no delta slots                    the state before the sensor was called
      B  delta slots, SAME_AS_TARGET       the sensor published and unusable
      C  delta slots, COMMENSURABLE        the ruling

    the four quantities
      out_base        outstanding over the ORIGINAL slots only -- the like-for-like column
      library         terms admitted
      refusal rate    `_operand_fits`, which the widening moves by construction
      defects         8 seats, 16 gate checks

**WHAT WOULD FALSIFY THE RULING.** `out_base` for C equal to A and B. **B already measured
bit-identical to A in both directions — 70.31 and 199.82 — so an unchanged `out_base` means the
widening bought nothing and the sensor is inert for a second reason.**

**WHAT A FALL DOES NOT LICENCE.** `out_base` falling is one game, one sequence. **It says the
affine term was reachable and paid, not that motion is now modelled** — and per-game, never
pooled, so it is a reading about `ls20` until another panel says otherwise.


---

# `delta` CALLED, AND THE ONE TERM THAT USES IT IS RIGHT ON A SEGMENT

**Sensor 7 was never called by anything.** Four of the six perception sensors wrap a function in
`arc_percept` and all four run every step; `_delta` and `_changed` were written as **leaves** with
the arithmetic inline, **so the perception layer had nothing to reach for.** `delta_of` now exists,
`_delta` wraps it like the other four, and the tracker publishes `drow`/`dcol` at the one moment
both frames are in hand.

**A BIRTH GETS NO DELTA AND NOT A ZERO.** §12.2 requires a value or an explicit non-reading, and
`0` says *it did not move* where the truth is *there was nothing to move from*. **Absent, which
the loop already handles** — *a new slot has no history and owes nothing yet*.

### THE PAIRING, SETTLED BY A WITNESS RATHER THAN THE GLOSS

`OBJ x OBJ` covers *two objects now* and *one object twice*, and §12.3 separates them only in
prose. **Of its three, `overlap` and `delta` are DIACHRONIC and `touching` is SYNCHRONIC** — and
`arc_percept:250` already reads one across time: `overlap(obj["cells"], old["cells"])`.

### THE COMMENSURABILITY WIDENING, AND WHAT IT DID AND DID NOT BUY

    fixed sequence, 20 steps        out_base   library   refusal rate
      A  no delta slots               70.31        7        0.6671
      B  delta, SAME_AS_TARGET        70.31       11        0.7619
      C  delta, COMMENSURABLE         70.31       11        0.4956

**`out_base` identical in all three.** `row + drow` — a position plus its own displacement — was
refused by `SAME_AS_TARGET`, and the rule's own warrant is *commensurability*, which a row and a
row-delta satisfy. **`SAME_AS_TARGET` was an implementation of commensurability under a type
system where same-type was the only commensurable pair.** The widening admits **216,202 bindings
that were refused before**, and no delta-bound term was minted.

**`(EXTENT, DELTA)` WAS IN THE TABLE AND IS OUT.** Height plus a row-displacement has nothing
behind it but both being cell counts. **Removed before it was ever read, which is what a pinned
table buys** — a second pair would have ridden in on the first's warrant.

### B17'S FIFTH VARIANT: AN OUTCOME REGISTERED AS THE FALSIFIER FOR A WARRANT-BASED RULING

**I registered *`out_base` unchanged falsifies the ruling*.** It is unchanged, and the ruling is
right anyway.

> **TWO CLAIMS, AND ONLY ONE IS WHAT THE WIDENING RESTS ON.** The CAPABILITY claim — *the rule now
> expresses commensurability* — is testable and passed, at 216,202 bindings. The PERFORMANCE claim
> — *it explains more* — was never the justification. **Registering the second as the test of the
> first means a correct rule is falsified by a board that does not exercise it**, which is
> *per-game, never pooled* arriving inside a pre-registration.

**THE GENERAL FORM:** when a change is justified by *the rule already said this*, **the test is
whether the rule now expresses it, not whether anything improves.**

### AND THE FINDING UNDERNEATH IS A SCOPING PROBLEM, NOT A BARGAIN ONE

    o10 (row, drow)   (40,-5) (40,0) (40,0) (45,5) (40,-5) (40,0) (40,0) (45,5) (40,-5)
                      (35,-5) (30,-5) (25,-5) (20,-5) (15,-5)
    `row + drow` predicts the next row: 7 of 13

**Seven steps of oscillation, then six of uniform -5.** The constant-velocity model is **exactly
right on the run and wrong at every turn**, and `_left` scores the slot's WHOLE history, so a term
correct on a segment cannot pay. **The first case this session where a CORRECT term is refused by
where the accounting is scoped** — and possibly the level boundary's shape: `retarget` clears
per-episode state, and the residual accounting does not know boundaries exist. **Owed as a check,
not a fix.**


---

# THE SEGMENT CHECK — THE DISTINCTION IS CARRIED, AND ITS BREAK EVENTS ARE THE WRONG GRAIN

**`instruments.Segment` already states the principle, almost word for word:**

> *One span of play between two break events. **Signals are scoped HERE, never cumulated over
> the run**: a mint in segment 3 must not credit the stall in segment 7, or a wiring gap
> silently reads as progress.*

**Substitute one word and it is the finding** — *a term correct in segment 3 must not be charged
for segment 7's regime.* **`Segment` scopes the CHAIN DIAGNOSTICS; `_left` cumulates the RESIDUAL
over a slot's whole history.** One of the two things the principle should govern.

### BUT SCOPING TO IT WOULD CHANGE NOTHING, AND THAT IS THE ANSWER

    step  0..13   level 0 throughout · seg.steps 1..14 unbroken · boundary/ending rows: 0
    o10.drow      -5 0 0 5 -5 0 0 5 | -5 -5 -5 -5 -5 -5

**The regime changes at step 8 and there is no break event anywhere near it.** `Segment`'s spans
are LEVEL boundaries; `o10` goes from oscillating to running while nothing at the episode scale
moves. **A segment-scoped `_left` would score the same whole history, because there is one
segment.**

### WHICH NAMES THE REAL FINDING, AND IT IS A THIRD CIRCLE

**The regime change is a property of the SLOT's behaviour, not of the episode.** So a
segment-scoped residual needs per-slot break detection — **and the signal that a regime changed IS
a term that stops explaining, which is the residual.**

> **THE THING THAT WOULD DETECT THE BOUNDARY IS THE QUANTITY BEING SCORED OVER THE SPAN THE
> BOUNDARY WOULD DEFINE.** Same shape as §12.4's — *reaching needs Tier 2, Tier 2 enters only by
> being reached* — and as the transfer column's, where the binding that must not cross is what the
> gate tests. **Third this session, and all three are correct designs rather than defects.**

**Recorded as a check, not a fix.** What it establishes: the principle exists and is right, the
machinery exists at the episode grain, and the case needs a grain nothing currently produces.


---

# A MECHANISM WHOSE INPUT IS ITS OWN OUTPUT — THREE THIS SESSION, AND IT IS A CLASS

**Each was found separately and each is the design being honest rather than a defect.**

    §12.4       reaching needs a Tier-2 sensor; Tier 2 may enter only by being reached
    transfer    the binding that must not cross is what the gate tests behaviour with
    segment     a segment-scoped residual needs break detection, and the break signal is
                a term that stops explaining -- which is the residual

> **THE TELL IS THAT THE FIX NAMES ITSELF AND IS FORBIDDEN BY THE THING IT WOULD FIX.** Install
> the sensor and the reaching is no longer evidence. Keep the binding and the composition no
> longer crosses. Scope the residual and you need the boundary the residual defines.

**AND ALL THREE SURFACED FROM A NEGATIVE.** `UNREACHED` with closure 4; `imported_pulled: 0`; *no
change from scoping to `Segment`*. **A circle presents as a null**, which is why the null had to be
read carefully rather than reported — and twice this session a null was nearly published as a
mechanism finding.

**NOT A LAW AND NOT A DEFECT REGISTER.** It is a shape to recognise: **when a mechanism's
precondition is its own product, the honest move is to state the circle and measure inside it**,
which is what the closure denominator, the three reasons, and the segment grain each are.


---

# THE REGISTRATION RE-READ — AND THE POPULATION CHANGED UNDER IT

**Written before `drow`/`dcol` existed, and the key it registers is measured against residuals.**
Re-read rather than re-run, and it does not survive unamended.

    ls20 / 18 steps, 154 gaps characterised
      gaps whose `varies_types` contains DELTA        154 of 154
      THIRD KEY's own spread per gap                  1, on every gap
      THIRD KEY vs ARITY KEY, identical score         3227 of 3696 pairs -- 87.3%
      gaps where the two differ at all                154 of 154

**DELTA SLOTS VARY EVERY STEP, SO *SOMETHING VARIED* BECAME UNIVERSALLY TRUE.** The
`SAME_AS_TARGET` branch — *aimed wherever anything moved* — is now a **constant 1**. It was
written when a non-empty `varies` was a real discriminator, and 42 new slots ended that.

**AND THE KEY HAS LARGELY COLLAPSED ONTO ARITY.** 87.3% identical. **A key that duplicates another
orders nothing new, and a spread measurement cannot see it** — the spread reads 1 on every gap and
looks healthy. The surviving 12.7% is entirely `recolour`'s typed `COLOUR` operand, where the type
is genuinely sometimes absent from `varies_types`.

> **THE REGISTERED FALSIFIER COULD NOT CATCH EITHER.** *A term that paid before and does not now*
> tests ADMISSION. Both findings are about ORDERING. **The registration had no falsifier for the
> thing that changed**, which is what re-reading catches and re-running does not.

### THE AMENDMENT, DERIVED

`SAME_AS_TARGET` means *the operand has the target's type*, so the aimed test is **is the TARGET's
type among the types that varied** — discriminating, and instance-free. **`fits` cannot ask it
today**: it receives `in_type`/`out_type` as `val`/`val`, the PREDICT space, and never sees the
target slot's §12.2 type. `characterise` knows the slot and can carry it.

**ADDED TO THE FALSIFIER SET:** *key 3's agreement with key 2*. A key whose scores duplicate
another's is inert however wide its spread, **and nothing in the original registration would have
reported it.**


---

# THE TRANSFER COLUMN HAS A SUBJECT — AND THE KEY THAT MOTIVATED IT DID NOT CAUSE THE RESULT

    F1  retrieve returns every library name   29 of 29 -- ORDERS ONLY          PASSES
    F2  key 3 vs key 2 identical              88.6%, was 87.3%                 FAILS

    TRANSFER  ls20 -> sk48, 18 steps each
      imported_held     2
      imported_pulled   2   translate . translate x7 · recolour . translate x1
      pulled_elsewhere  both -- handle prefix is `ls20`, pulled on `sk48`
      never_pulled      none

**THE THREE REASONS ARE CLOSED AND THE NUMBER IS A MEASUREMENT.** An unbound import computed the
identity — `translate . translate` on 7 returned **7**, re-bound it returns **13**. The sweep
re-bound and emitted no `pull` row. A re-bound import installs under a new name stamped
`accepted`, so a name-keyed column could never match it. **Re-bind at the pull site, a pull row
from the sweep, and a column keyed on the composition.**

### AND THE AMENDMENT I DERIVED MADE THE KEY WORSE

**F2 was registered from the re-read: *a key that duplicates another is inert however wide its
spread*.** The fix — `SAME_AS_TARGET` means *the operand has the target's type*, so ask whether
the TARGET's type varied — is correct about what `SAME_AS_TARGET` means **and moved the agreement
from 87.3% to 88.6%.** It reduced the independent signal it was derived to restore.

> **SO §15.3's THIRD KEY IS SUBSTANTIALLY THE ARITY KEY WEARING A SECOND NAME**, and a derivation
> from what a constant *means* did not fix it. **The remaining independent signal is `recolour`'s
> typed `COLOUR` operand and nothing else.**

### WHICH MAKES THE HONEST ATTRIBUTION UNCOMFORTABLE AND WORTH STATING

**F1 guarantees `retrieve` returns EVERY name, so ordering cannot determine whether a term is
found — only when.** The transfer result therefore comes from **re-binding, the sweep's row, and
the composition key**. The two key changes that motivated the whole build — types instead of slot
names, `operand_type` instead of `operand` — **are correct, are what made *pattern crosses,
instance does not* apply to retrieval, and did not cause this number.**

**Following the key through the pull site is what exposed the other three defects.** The
motivation was sound and the mechanism it motivated was not the one that worked.

### WHAT IT DOES NOT LICENCE, PRE-REGISTERED BEFORE THE RUN

**One pair of games, 18 steps, two compositions.** And **a rise from 0 is not an improvement over
a measured 0** — the old number measured nothing, so this reading has no predecessor. **Per game,
never pooled.**


---

# THE FIGURES ON THE ITEM IN FLIGHT — FIVE READINGS, AND FOUR OF THEM REFRAME RATHER THAN CONFIRM

**FIGURE 9 · THE INSTANCE-FREE KEY IS NOT A REFINEMENT.** *Evidence bearing on the residual is
admissible; evidence bearing only on its MAKER is a stake-inducing channel, and the verifier is
denied it.* **A slot name is evidence about whose residual it was.** So slot-keyed retrieval was
admitting a channel the figure disqualifies — **the change removed an inadmissible key rather than
improving a key.**

**FIGURE 6 · THE CIRCLE'S EXIT IS NAMED.** *The question is not whether a sensor could exist. It
is whether anything, at any resolution, is already returning something that FAILS TO RESOLVE.*
**`_delta`'s body was `rb - ra`, already returning something, sealed in a two-place sensor.** So
§12.4's `UNREACHED` stands and the exit is **not install the missing sensor** but **find the
proto-instrument already returning something unresolved** — *an instrument is improved from a
worse instrument already returning something, never built from a description.*

**FIGURE 10 · THE CONVENTION/VERDICT LINE.** *It carries only what it did not author... It does
author CONVENTIONS, because nothing else can see across a seam. A convention makes no claim about
the world; a verdict and an atom both do.* **The handle scheme is a convention. A skill map is a
verdict.** The ruling made twice this week, arriving with its reason.

**FIGURE 3 · WHERE EVERY READING THIS WEEK SITS.** Link 2 is *terms for what things afford* —
measured and failing. Link 3, the objective — **never reached, so never assessed.** **Everything
measured this week is at link 2**, and *a reading taken below the break is a reading of nothing.*

**FIGURE 8 + 9 · WHY FULL REACH IS A REQUIREMENT.** *Only a sealed room can be searched to the
end, and no frame is a sealed room* — so an abstention is worth something **only when it names the
closure it searched.** §12.4's does. **A reach that cannot touch 2,689 of 2,700 entries makes every
abstention a reading over a corner, and the agent cannot say which corner, because it does not
know the entries are there.**

---

# F2, FILED AS A FINDING WITH ITS SHAPE STATED

**§15.3's third key is substantially the arity key wearing a second name.** 87.3% identical, and
the derived amendment moved it to **88.6%** — correct about what `SAME_AS_TARGET` means and
reducing the signal it was meant to restore.

> **THE SIGNAL IS MISSING, NOT THE BRANCH.** A better branch over the same inputs cannot separate
> the keys, because both are computed from *does this term read an operand* and *did anything
> move*. **The surviving independent signal is `recolour`'s typed `COLOUR` operand and nothing
> else.**

**NOT A TASK, AND NOT TO BE GUESSED AT.** §15.3's four keys are named and this is the third; a
fifth signal invented here is the improvised-metric failure at the level of a key. **The corpus
names the remaining one — `effect shape`, *what changed, not what caused it* — and it is the one
key never built.**


---

# `_changed` CLOSES, AND THE SHARPER TEST FINDS `shape` — 43 OF 43

**FIGURE 6 SET THE TEST: *is anything, at any resolution, already returning something that fails
to resolve?*** Applied to `_changed` in its weak form and its strong one.

    WEAK    changed cells lying outside every tracked object
              ls20  728 changed, 0 outside        g50t  246 changed, 0 outside
    STRONG  objects whose CELLS changed while no published attribute moved
              ls20   72 changed, 13 silent (18.1%)  -- SHAPE moved in 13
              g50t   34 changed,  6 silent (17.6%)  -- SHAPE moved in  6
              sk48  259 changed, 24 silent  (9.3%)  -- SHAPE moved in 24

**`_changed` CLOSES ON THE WEAK TEST.** Every changed cell belongs to a tracked object, so it sees
no region the decomposition misses — **measured, where my earlier answer was the arity argument.**
And §12.3 glosses it *where to look*: an attention reading, so `_extract` was never its consumer.

**THE STRONG TEST FINDS `shape`, ON EVERY PANEL, AT 43 OF 43.** An object's cells change, the
agent's entire slot vocabulary holds still, and **`shape` moved every time.** Per game, never
pooled: 18.1%, 17.6%, 9.3% — three boards, three rates, not one board's quirk.

> **THE `delta` FINDING AGAIN AND STRONGER.** `delta` was never computed by anything; **`shape` is
> computed every step by the tracker, for identity, and discarded.** Sensor 5, one of the nine, so
> no entry question arises — and *the composable set was decided by which sensors happened to
> return integers* now has its cost measured: **43 invisible changes, 100% of them shape.**

### THE BLOCKER IS NOT WHAT I WAS ABOUT TO SAY

**`correction_bits` is already the comparable-only form:** `0.0 if a % alphabet == b % alphabet
else log2(alphabet)`. **An equality test that never uses order** — the `%` is normalisation, not a
metric. So §12.2 typing SHAPE as *comparable, not orderable* costs the residual accounting
nothing, and the machinery is there.

**WHAT IS ACTUALLY IN THE WAY IS THE ALPHABET.** `log2(alphabet)` is what being wrong costs, and a
shape slot has no bounded alphabet declared. **A derivable form exists** — a shape is a subset of
its own bounding box, so the uniform code over that space is `h*w` bits, from two attributes
already published — **but that is per object per step, where `_alphabets` is per slot and declared
once by the domain.** That is a contract question and a ruling, not a line.


---

# `shape` PUBLISHES — THE GAP CLOSES 18 OF 18, AND IT IS NOW 98% OF THE RESIDUAL

    ls20   cell-changes 68 | five-attrs-silent 12 | SHAPE CAUGHT 12 of 12
    g50t   cell-changes 32 | five-attrs-silent  6 | SHAPE CAUGHT  6 of  6

    ls20   integral 233 -> 18,883 (81x) | outstanding 15,164, of which SHAPE 14,843 (98%)
    g50t                                | outstanding  6,722, of which SHAPE  6,328 (94%)

**PUBLISHED AS A PER-EPISODE ID, WHICH IS THE COLOUR TREATMENT.** A shape is a frozenset and a
slot is an int — *the composable set was decided by which sensors happened to return integers* —
so the id is a LABEL: arbitrary, comparable, never orderable, valid only for the episode it was
assigned in. **`correction_bits` was already an equality test**, so nothing in the accounting had
to change.

**THE ALPHABET IS PER SLOT AND PER STEP**, as ruled. `_alphabets` always accepted a dict; every
slot that existed when it was written had a constant range. **A shape slot's is `2**(h*w)` over
its own bounding box — derived from two published attributes, nothing tuned — and it moves when
the object resizes.** The declaration is still the domain's; only *when* it is read has moved.

**AND THE DELTAS WERE PUBLISHED AGAINST THE PALETTE**, so `drow = -5` and `drow = 8` both read as
8 under the modulo on a 13-colour board. **A collision introduced with the sensor and found while
implementing this.** Fixed to the board's range.

### TWO THINGS CAUGHT IN MY OWN WORK

**8 SEATS READ CLEAN WHILE THE REAL PATH WAS BROKEN.** `if b` on a numpy board raises, and no
conform world hands one back — **so the checks were green and the first real run died.** `b is
None` now, with the reason at the site.

**AND MY FIRST VERIFICATION WAS VACUOUS.** It tested whether the shape SLOT EXISTS, which is now
always true, rather than whether its VALUE changed — *a control that examines nothing cannot
demonstrate a clean state*, and mine examined nothing. The corrected check is 12 of 12 and 6 of 6.

### THE ALPHABET IS A FORK AND IT IS NOT MINE TO TAKE

**`2**(h*w)` is a sound UPPER BOUND and a vast overestimate.** A component is CONNECTED and must
touch all four sides of its own bounding box, so the reachable space is far smaller — and the
uniform code charges **4,096 bits** for being wrong about a full-board object.

> **NO TERM CAN EXPLAIN A CHANGING SHAPE ID.** The atoms are `idn`, `translate`, `recolour`;
> `idn` explains a static shape and arithmetic on a label means nothing. **So the mint will be
> drawn to the slots carrying the most bits, and they are the ones it structurally cannot
> explain.** That is honest — the surprise IS unexplained — and it will dominate every aggregate.

**THE ALTERNATIVE IS THE LABEL READING:** a shape alphabet is the count of distinct shapes, as
`colour`'s is the palette. **That is a GROWING denominator**, which is the defect class recorded
against `lib ok here / lib`. **Two defensible derivations with opposite failure modes**, and
picking between them on the number they produce is fitting.


---

# THE LABEL READING, AND THE PRICE DRIFTS WITHIN A RUN

**A shape slot holds an ID and an id is a label** — arbitrary, comparable, never orderable — so
its alphabet is the count of labels, exactly as `colour`'s is the palette. **`2**(h*w)` priced the
space of shapes that COULD exist, which is not what the slot holds.**

                  integral   outstanding   SHAPE share      under 2**(h*w)
      ls20           608.2         455.2      133.8  29%    18,883 / 15,164 / 98%
      g50t           575.6         477.6       75.8  16%    14,778 /  6,722 / 94%
      detection   12 of 12 and 6 of 6 -- UNCHANGED. only the pricing moved

### THE GROWING DENOMINATOR IS REAL, AND IT IS PER GAME

    distinct shapes at steps 1,5,10,15,20,25,30
      ls20   18 25 36 52 52 52 52     settled at step 15
      g50t   12 16 22 26 33 38 44     +18 in the last 15 -- STILL GROWING

**`ls20` settles and `g50t` does not**, which is *per game, never pooled* arriving in the failure
mode rather than in the result. **The growth is logarithmic in cost** — a doubling of the shape
count adds one bit — so unbounded growth gives unbounded-but-slow cost rather than a blow-up.

> **AND IT DRIFTS THE PRICE WITHIN A RUN, WHICH COLOUR DOES NOT.** A shape miss at step 5 on
> `g50t` costs `log2(16)` and the same miss at step 30 costs `log2(44)`. **`pe_integral` is
> monotone by construction and now sums a quantity charged at different rates over its own
> span** — two identical events, two prices. **Colour has no such drift: its palette is declared
> at construction and discovered by nobody.**

**DIFFERENT FROM `lib ok here / lib`, WHICH WAS A RATIO WHOSE DENOMINATOR THE MECHANISM MOVED.**
This is a per-slot cost whose denominator grows with **observation** — a fact about the world, not
a metric drifting under its own mechanism. **Recorded as a watch, not a defect**, and the thing to
check is whether a board exists where the count never settles at all.

### AND THE FORK'S OTHER HALF SURVIVED THE RULING

**No term can explain a changing shape id under either reading.** The atoms are `idn`, `translate`,
`recolour`; `idn` explains a static shape and arithmetic on a label means nothing. **The label
reading reduced the cost and did not make the slot explicable.**

> **THE AGENT IS NOW MAXIMALLY SURPRISED BY EXACTLY THE THING IT HAS NO VOCABULARY FOR** — and
> `recolour`'s form over a label already works, so *shape becomes that shape* is expressible while
> *bigger* is not. **The id has no structure; the shape it stands for does.** That is the label
> ruling's honest cost, and it is filed as the finding rather than solved with a smaller number.


---

# THE GROUND HAS NEVER MOVED — AND MY READING OF WHY WAS A PROXY I BUILT FROM OUR OWN CONFIG

**RETRACTED IN PART, SAME DAY. The measurement stands; the interpretation was invented.**

    MEASURED    objective degree FLAT at 0.0 on `ls20` and `g50t` over 30 actions
                level 0 -> 0, terminal "" -- no level has ever completed
                `win_levels = 7`, `levels_completed = 0`

    ASSERTED AND NOT MEASURED
                "500 actions per level, so our runs are ~1% of an episode"
                `PER_LEVEL = 500` is `arc_run.py:24` -- OURS. A seat-side cap.
                `CLAUDE.md`'s second firewall says so: the cap is the seat's choice.
                **NOTHING IN THIS REPO ASKS THE GAME WHAT A LEVEL AFFORDS.**
                A game that ends at 40 actions is consistent with every number above.

> **I ARGUED AGAINST PROXY METRICS AND THEN BUILT ONE, WITH A DENOMINATOR TAKEN FROM OUR OWN
> CONFIG AND PRESENTED AS A FACT ABOUT THE WORLD.** The `1%` was arithmetic over a constant we
> set. **Same shape as `space_estimate`, in the week `space_estimate` was fixed** — and the
> failure mode is the one `CLAUDE.md` lists against me by name.

> **WHAT SURVIVES: the runs are short and the ground has never moved, and I cannot say short
> RELATIVE TO WHAT.** Zero levels over 30 actions is the absence of a measurement, not a result
> about the agent — **and that much needed no assumed denominator to say.** Every reading in this
> document does carry an unquantified scope condition — `outstanding`, coverage, the branching test, `bench pulls`, the transfer column,
> §12.4's firing rates, the `delta` and `shape` findings. **All of them are characterisations of
> the first moments of a game.**

**WHICH IS FIGURE 3's LINK-3 POINT WITH A NUMBER ON IT.** *Everything measured is at link 2, and a
reading taken below the break is a reading of nothing* — and the break is not only that link 3 was
never built. **It is that the runs stop before the ground could have said anything.**

**AND IT IS THE PANEL-PROPERTY LAW APPLIED TO RUN LENGTH RATHER THAN TO WORLD CONTENT.** *Before a
null is read as a finding, state what property the panel would need in order to show it.* **A
40-action run on a 3,500-action episode cannot reward anything that takes a level to appear**, and
that was true of every measurement taken this week.

**AND THE PROPOSAL I DREW FROM IT CONTRADICTED THE ARGUMENT THAT PRODUCED IT.** *Twenty
findings, three contact changes* — then I proposed a RUN, which is **zero contact changes and the
purest instrument of all.** Figure 11: *an improvement that does not change contact changes
nothing.* **The answer to too many instruments is not one more instrument.**

**AND `levels_completed` IS LINK 4, READ BELOW A BREAK AT LINK 2.** Zero levels on a five-slot
vocabulary cannot separate *the machinery is broken* from *the agent cannot express the
objective*. **It would be an uninterpretable null with a satisfying story available** — the failure
named twice this week, walked into a third time by the person naming it.


---

# `varies`' SUBJECT — CLOSED, AND THE DESCRIPTION KEY IS CORRECT AND PREMATURE

**The test was the corpus's own wording: *from the residual's own structure*. A slot that moved
and was correctly predicted has no residual, so scoping `varies` to residual-carrying slots is a
reading of the spec rather than a design choice.**

    same window, both games          as built    scoped to residual-carrying
      ls20, 168 gaps                    23.6            23.6      reduction 1.00x
      g50t, 120 gaps                    23.9            23.9      reduction 1.00x

**NO REDUCTION. Every slot that varied in the window also carried residual mass in it.** So both
diagnoses die together — **mine (*the key measures the board's activity*) and the *different
languages* reading.** The key is measuring the residual's structure already.

### AND THE MECHANISM IS ONE LINE

    ls20   176 slots | bound to something other than `idn`: 13   (163 -> idn)
    g50t   120 slots | bound to something other than `idn`:  5   (115 -> idn)

**93% and 96% of slots predict *nothing changes*.** So **moved and mispredicted are the same
event**, and `varies` equals the residual-carrying set **by construction, not by coincidence.**

> **THE DESCRIPTION IS SATURATED BECAUSE THE RESIDUAL IS SATURATED, AND THE RESIDUAL IS SATURATED
> BECAUSE THE AGENT PREDICTS ALMOST NOTHING.** The key is not broken, the vocabulary is not the
> wrong language, and a finer one would not help. **The key is CORRECT AND PREMATURE.**

**IT BECOMES INFORMATIVE AS THE AGENT IMPROVES.** When most slots are correctly predicted,
`varies` shrinks to the few that are not — **and a handful of slots is a residual's own structure
in the sense §15.3 means.** The saturation is a symptom of the agent, measured through the key.

### WHICH CONVERGES THE ITEMS INSTEAD OF MULTIPLYING THEM

**The cluster rewrite stays refused** — for a better reason than *the gap side says everything
moved*: **the gap side is right that everything is wrong.**

**F2's diagnosis closes.** Not a missing signal, not different languages, not a saturated
description — **a library that explains 13 slots of 176.**

**And the description vocabulary is not the next build.** It is correct, it is waiting, and what
it waits on is the agent explaining more.

**WHICH LANDS ON THE OPERATOR FINDING.** The agent explains 13 of 176 with a vocabulary of
`translate`/`recolour` chains at arity 1, under one relation. **2,111 of 2,651 recipes are written
in `+`, and `Term` is left-to-right, which is `→`.** The reason it cannot predict and the reason
`+` has no form are the same reason.


---

# THE COMPOSITE SYSTEM HAS ONE LEVEL, AND THE GATE IS THE CLOSURE TEST'S SCOPE

**Measured 2026-09-01, after three threads — `varies`, `≡`, multi-operand — that were all
downstream of this and none of which moved it.**

    ls20 / g50t, 20 steps each
      SETTLED terms                              0        0
      len(units()) at step 1 and step 20      17->17   17->17     never grows
      terms longer than max_depth                0        0       nothing reused a unit
      mint rows                                 13        7       ALL verdict "pays"
      candidates (closed: left == 0)             0        0
      demotions                                  0        0

**NOTHING HAS EVER SETTLED, SO `units()` HAS NEVER HELD ANYTHING BUT ATOMS.** The second level has
not failed — **it has never existed.** And *chunk reuse reads zero* is therefore a **tautology**,
not a finding: no chain can contain a settled term when there are none.

### THE CHAIN, EACH LINK MEASURED

    every mint PAYS and none CLOSES        13 of 13, 7 of 7, `left > 0` every time
      -> `closes = left == 0.0` is never true, so `candidates` stays empty
      -> `settle()` requires `name in self.candidates`, so nothing settles
      -> `units()` = atoms + settled, so it never grows past 17
      -> no settled term is ever a building block
      -> ONE LEVEL, structurally

### AND THE TERMS THAT WOULD SETTLE ALREADY EXIST

    close over the WHOLE history   0 of 13    0 of 5
    close over a SUFFIX of >= 3    7 of 13    3 of 5
    longest exact suffix seen      12 of 19 observations

**`left` is exactness over the slot's ENTIRE history.** More than half the bound terms are exact
over a recent stretch and are charged for a stretch they were never fitted to. **The promotion
path is not failing to find terms — it is refusing the ones it has, on scope.**

> **AND §21.5 IS THE CORPUS SAYING SO.** *Level RESET after a loss — the board is KNOWN — a
> residual means the model is wrong. Level ADVANCE — the board is UNKNOWN — **a residual means
> nothing yet.*** `_left` charges it either way.

### THE SUFFIX SIDESTEPS THE THIRD CIRCLE

**The segment check closed because `Segment`'s break events are LEVEL boundaries and there were
zero of them in 14 steps — and because a segment-scoped residual needs break detection, whose
signal is the residual.** **A SUFFIX needs no break detection at all**: *how far back does
exactness extend* is computable without knowing where the regime changed. **The circle has an exit
and it is the direction of the scan.**

**WHAT IS NOT ESTABLISHED, AND IT IS THE ruling:** whether promoting on a suffix is correct at
all, what length would qualify, and what it does to false mints. **A term exact on a suffix was
wrong earlier**, and the defeasible demotion machinery — `refute`, decaying rejection — is what
would have to carry that. **Nothing is built.**


---

# PRE-REGISTERED: CANDIDACY

**The change is one arrow: every accepted mint becomes a candidate.** Q7 — *a candidate becomes
accepted once it predicts transitions it was never fitted to.* Candidacy is currently gated on
`left == 0`, and nothing has ever closed.

    THE FALSIFIER -- `outstanding`, on a FIXED SEQUENCE, before and after
      Its denominator is the run's total surprise, which candidacy does not move, so numerator
      and denominator are independent -- the property `false_mint_rate` lacks, and the reason
      that one withdrew a correct mechanism once already.

      IF `units()` GROWS AND `outstanding` DOES NOT FALL, the settled terms are not explaining
      anything and the gate was doing real work.

    THE WIRING CHECK -- `len(units())` at step 1 versus step 20. Currently 17 and 17.
      Flat after the change means the arrow did not land: wiring, not design.

    HELD SEPARATE -- promoting on a SUFFIX is a different proposal and is not in this change.
      It rides in only if candidacy fails to move `units()` without it. Kept apart so the
      reading attributes.

**Does this change alter the trajectory the measurement is taken over? YES** — settled terms enter
`units()`, so the search space changes, so different terms are found. **Fixed sequence is the only
comparable form, settled before approval rather than discovered after.**


---

# CANDIDACY — BUILT 2026-09-01. THE COMPOSITE SYSTEM HAS A SECOND LEVEL

**One arrow: every accepted mint becomes a candidate.** Q7's ordering — *the mint makes a
candidate; the ground settles it by held-out payment* — where the code had closure make one.

    fixed sequence, 20 steps        BEFORE            AFTER
      ls20  units                   17 -> 17          17 -> 19
            settled                        0                14
            candidates                     0                23
            outstanding               637.86            455.91     -28.6%
            library                       20                30
      g50t  units                   17 -> 17          17 -> 19
            settled                        0                10
            outstanding               582.88            526.88      -9.6%

**THE WIRING CHECK PASSES**: `units()` grows, so the arrow landed. **THE FALSIFIER PASSES**:
`outstanding` falls on both, on the same actions, replay faithful. The registered failure — *units
grows and outstanding does not fall* — did not occur, **and `outstanding`'s denominator is the
run's total surprise, which candidacy does not move.**

### AND THE SECOND LEVEL IS USED, WHICH IS A DIFFERENT CLAIM

    settled 14 -> 2 DISTINCT new units    `translate . translate`, `recolour . recolour`
    terms longer than `max_depth` (3)     ls20: 2 · g50t: 0

**A four-atom term is not constructible from atoms alone at depth 3.** `translate . translate .
translate . translate` exists only by composing over a settled unit. **Twice on `ls20`, never on
`g50t`** — per game, never pooled: on one board the second level is in use, on the other it is
available and unused.

**AND 14 SETTLED BECAME 2 UNITS**, because `units()` dedups on the emitted name with the binding
stripped. *Fifty saved entries were eleven shapes*, measured again from the other side.

### WHAT IT DOES NOT LICENSE

**20 steps, two games.** And **`outstanding` falling is not solely the second level** — the
library also went 20 to 30, and more terms explain more whether or not any composed over a unit.
**The `> max_depth` count separates EXISTENCE from USE and does not apportion the fall.**

**The ground has not moved.** Levels 0, degree flat. This is a reading about the machinery.

### AND THE SUFFIX PROPOSAL DID NOT RIDE IN

**Held separate as ruled, and it was not needed** — candidacy moved `units()` on its own. Whether
promoting on a suffix is correct remains unruled and unbuilt.


---

# THE CHEMISTRY MAPPING — FOUR ROWS, TESTED AGAINST *DOES IT PREDICT A RESIDUAL*

**Table 1 is definitional and already load-bearing**: element/atom, valence bond/operator,
molecule/molecule, straight-chain alkane/linear recipe, branched molecule/complex recipe,
structural formula/recipe. **It settled *chains are molecules* — a chain is the degenerate case,
one bond type and a spine — and it retired the multi-operand line by making branching visible.**

**The four extended rows, each against the stated test:** *does it predict a residual the current
frame cannot explain?* **Two are already out for failing it — bond strength and the loop as a
macro-molecule — and an analogy is load-bearing only when the target casts a shadow.**

### ISOMERS — PASSES, AT 100%

    multisets with more than one arrangement          3
    of those, EXTENSIONALLY DISTINCT                  3   (100%)
      [recolour, translate] -> `translate . recolour` and `recolour . translate`

**Order alone — the one structural variation this system has — produces a distinct substance in
every case measured**, with one bond type. **And it separates two things one word was covering:**
`idn`'s *39 names, 7 functions* was redundant **spelling**, not isomerism. **Isomers are where the
arrangements genuinely differ; `idn` was where they did not**, and *extensional collapse* was
naming both.

### CATALYST — PASSES, AND ITS SUBJECT ARRIVED WITH CANDIDACY

    ls20   settled 14 | spent (demoted) 7 | survived use unchanged 7
    g50t   settled 10 | spent           7 | survived use unchanged 3
    `rejection_of` on survivors: 0.386, 0.0, 2.747 -- GRADED, not binary

**The instruments existed all along** — `refute`, `rejection_of`, `is_settled`. **What did not
exist was a population**: settled was 0, so nothing could be spent. **The row was unaskable
yesterday and is askable today**, which is a correction to *nothing currently distinguishes a term
that regenerates from one that is spent* — both instruments distinguish it and neither had a
subject.

### CYCLIC — SPLITS, AND THE HALF THAT WAS CITED IS THE HALF THAT FAILS

**The three circles are a fact about OUR CODEBASE, checkable by inspection.** They are not a
residual the agent's frame cannot explain, and the test is about the agent's frame. **On that
reading the row fails.**

**The AGENT-SIDE reading passes**: a slot whose delta increases with its own delta is positive
feedback, decreasing is negative, and *the sign of the loop decides the outcome* is a **gap shape**
— matchable against a residual, and `drow`/`dcol` are exactly the slots that would show it.

**So the row survives on a reading that was not the one given for it**, and the seat-side version
is a useful description rather than a prediction.

### FUNCTIONAL GROUP — FALSIFIABLE, AND NOW THIN RATHER THAN EMPTY

*`Ascent` and `Descent` share `Momentum` and differ only in the feedback sign* needs molecules to
check against. **There were none; there are now two distinct units per game.** **n = 2 is thin and
it is not zero**, which is a change of state rather than of verdict.


---

# THE BOND TERM — TAKEN AS `log2(|bonds|)`, WHICH IS ZERO TODAY

    CODE   uniform(M) per correction; (k+1)*log2(|atoms|+1) + (k-1)*log2(|bonds|) per term
    BONDS  1   -- a `Term` is applied left to right, which is ONE bond: sequence

**`log2(7)` would charge for a choice among one.** `CODE` charges `log2(alphabet)` per position and
**the alphabet is what is available** — a symbol from a one-symbol alphabet costs nothing because
it tells you nothing. **The zero is a consequence, not a concession**, and it prices every future
operator automatically.

**NO STOP, AND THE ASYMMETRY IS DERIVED.** The atom term carries `+1` because a sequence's LENGTH
is unknown. **There are exactly `k-1` bonds and `k` is already read**, so nothing terminates them.

    measured against the libraries as they stood, under a FLAT log2(7)
      terms paying    ls20  7 -> 4       g50t  3 -> 2
      the marginal payers pay by 1.49 bits; the cheapest bond is 2.8

**SO IT WILL RISE SILENTLY AND WILL LOOK LIKE A REGRESSION.** Those four stop paying the moment
branching is a choice — **which is correct: a branched molecule says more than a spine, and today
it says more for free.** The reason is at the site so the next reader does not read it as a defect.

### AND THE ISOMER FINDING IS WHY THIS IS NOT A CONTRADICTION

**3 of 3 arrangements are extensionally distinct under ONE bond type** — because the distinction
there is **order**, not bond choice. **Order is already priced**: two arrangements are two
sequences at the same cost. **The operator carries information in proportion to how many
alternatives exist, which is none today.**

### THE REGISTRATION'S TWO OUTCOMES DID NOT EXHAUST THE SPACE

*Most still pay* and *the code needs a different form* were the branches. **Neither fired: the code
needed the GENERAL form it already implied.** Fourth or fifth time a registration's outcomes have
turned out not to exhaust the space, **and each time the registration was written before the
mechanism was read.**


---

# `CHEMISTRY.md` READ — THE CATALYST TEST BUILT, AND MY OWN MORNING NUMBER CORRECTED

**`summary.catalysts` implements *does this term survive its own use unchanged*, which the
document names as checkable and unrecorded.** Right about the derived property; the material was
always there — `Standing.settled_at` and a decaying `rejections`, with `refute` clearing one and
raising the other. **What did not exist was a population: nothing settled until candidacy landed.**

    ls20   survived use unchanged 1 | spent 25 | recovering 6
    g50t   survived use unchanged 0 | spent 10 | recovering 3
    recovering, graded: 1.0 · 4.236 · 2.758 · 1.917 -- still settled, having been turned on

**AND IT CORRECTS THIS MORNING'S READING.** I reported *7 survived* from `settled` minus the demote
list, **which counts terms that settled late and were never tested.** The strict property —
`settled_at is not None and rejections == 0` — **is 1 and 0.** Almost every term that settles is
eventually turned on.

> **WHICH MAKES THE COMPOSED CATALYST CASE NEARLY UNAVAILABLE HERE.** `Break habit = Dither +
> Witness stance + Damp` *works because both survive the breaking; a consumed component could not
> be used again on the next groove.* **One term in about thirty survives.**

**AND `rejections` IS GRADED WHERE CHEMISTRY IS BINARY.** A catalyst is consumed or not; here a
term carries how often the ground turned on it, halved over `REJECTION_HALFLIFE`, **so spent has a
degree and a term can recover** — six did on `ls20`. **More than the analogy asked for**, which is
the mapping paying rather than fitting.


---

# `contact_first` — THE ONLY BIAS DECLARED WITHOUT A FUNCTION, NOW IMPLEMENTED

**`priors.py` carried it with a citation and no `fn`** — Michotte 1946, Leslie & Keeble 1987 —
while `simplicity` and `take_the_best` both had one. **`_delta`'s shape a third time: admitted,
cited, and never given an implementation.**

**AND `_bindings` RECORDED THE CONSEQUENCE AT ITS OWN SITE**: *the list is EVERY other slot, which
is exactly what §16.5 forbids — you do not invent the list, you read it off the world — and
`touching()` is built and unused.*

### THE PUBLICATION QUESTION ANSWERED BY THE CORPUS, NOT BY ARITY

**`touching` does not become a slot.** Dense pairs are `O(n^2)` — 2,415 on `sk48`, and the
measurement **timed out computing them**. Sparse pairs churn the slot set. **§16.5 names the real
consumer: the binding candidate list**, which is `O(n)` for the one slot being minted.

    contact density   ls20  21 objects, 210 pairs, 24-26 touching per step (12%)
                      g50t  16 objects, 120 pairs, 13-16 touching per step (13%)
    mean contacts per object ~2.4

> **WHICH RETIRES A FINDING I CARRIED FOR DAYS.** I recorded *a relation is not a slot, so it never
> crosses* as the right diagnosis with the wrong remedy, and said the remedy was publishing the
> scalar. **The corpus's remedy is that the relation never crosses at all** — it orders candidates
> on the perception side and the loop receives a list.

### AND IT ORDERS, WHICH MEANS ITS EFFECT IS CONFINED TO TIES

    fixed sequence, 20 steps       outstanding    library    settled
      ls20   before / after        455.91 / 455.91   30 / 31   14 / 14
      g50t   before / after        526.88 / 526.88   11 / 11   10 / 10
      bound terms with an operand on a CONTACTING body:  ls20 5 of 13 · g50t 0 of 3

**`outstanding` is unchanged to the decimal, and that is correct rather than disappointing.** The
mint iterates EVERY binding and keeps the best, breaking only on a closer — **and nothing closes**
— so an ordering decides which of several equal-`left` bindings wins and nothing else. **One extra
term on `ls20`.**

**AN ORDERING MATTERS WHEN THE SEARCH IS TRUNCATED, AND THIS SEARCH IS NOT.** `contact_first` will
move a number when the budget binds or when something closes. **Neither happens today**, and that
is the same shape as `enumerate_closure`'s `order=` — built, correct, and waiting on a search that
stops early.


---

# THE ACCOUNT — SCOPED TO THE LEVEL BOUNDARY, AND ITS FIRST READING IS `UNREACHED`

**The per-term reader was the wrong shape.** *This term reduced 14 bits and held 38 steps* is true
and says nothing about what contributed to anything. **`levels_completed` is the only ground
signal, so a level advance is the one moment `contributed` has a referent** — and the per-term
account is the INPUT rather than the deliverable.

    summary.levels(rows) -- four columns per level
      held      what was in the library entering it
      used      what was pulled during it
      minted    what was composed during it
      residual  what `outstanding` did across it

    g50t, 12 steps    verdict UNREACHED · advanced False
                      level 0 | held 0 · used 2 · minted 7 · residual moved +383.136

**ONE LEVEL MEANS NO DIFFERENCES, AND THE VERDICT IS `UNREACHED` RATHER THAN NULL** — *no level
advanced, so no contribution reading exists*, which is a statement about the run and not about the
library. **The class the register is full of, declared instead of discovered.**

### THE LEDGER WAS MISSING THE FIELD THE SERIES NEEDS

**Nothing recorded which level a cycle was in.** The `ending` row carries `to_level` and marks the
boundary; the `repeat` row carried the integral, the outstanding and the stage and not the level.
**One field, and the four columns had no way to be segmented without it.**

### AND IT PRODUCES A SERIES, WHICH IS §14.7's OWN FORM

*Unreached rate over time, and it should fall as chunks accumulate.* **A per-level series is that
shape**, and the prediction is registerable before the first advance:

> **Each level ADDS problems to a cup that still holds everything the last one did not explain.**
> So **a library that is not composing should show RISING unexplained mass per level, and one that
> is composing should show the opposite.** The one level we have reads `+383.136` with nothing to
> compare it to.

### AND `retarget` DOES NOT EMPTY THE CUP — CORRECTED IN `CLAUDE.md`

I wrote it as *the cup being emptied because the room changed.* **It is not.** The bindings clear
because the SLOTS do not survive; **the residual does not clear**, and `outstanding` is
monotone-by-addition for exactly that reason. **A level boundary is the world expanding, not being
replaced** — and the mechanism was already correct for it.

### THE HOIST — COST ONLY, VERIFIED

`_bindings` depends on the slot and the residual and **was being rebuilt for every candidate**: an
owner map, a contact set and a variance count each time. **True before `contact_first` and made
expensive enough to notice by it.**

    outstanding  455.91 / 526.88 -> 455.91 / 526.88   IDENTICAL
    library, settled                                   identical
    wall clock   the pair timed out at 120s -> 53s + 26s


---

# NO SEAT MEASURES COST — A MISSING CHECK CATEGORY, NOT A MISSING RULE

**`_bindings` was rebuilt for every candidate in the mint's hottest loop** — an owner map, a
contact set and a variance count each time, when it depends only on the slot and the residual.
**Eight seats read clean throughout.**

    ruff · lint · kernel · stateful · shipped · demo · gate · tests
    all green, and none of them measures how long anything takes

**THE TELL IS THAT THE DEFECT PREDATED THE CHANGE THAT EXPOSED IT.** `contact_first` did not cause
it; **it made it expensive enough to notice.** So the trigger was a THRESHOLD BEING CROSSED, not a
change introducing anything — **and the only signal was a measurement of mine failing to finish.**

> **ELEVENTH INSTANCE OF *NOTHING WOULD HAVE SAID SO*, AND THE FIRST WHERE THE MISSING CHECK IS A
> CATEGORY.** Every earlier one was a rule with a narrow subject that went quiet — a denominator,
> an exemption, a witness. **This is a whole class of property with no seat at all**, which means
> the same defect can sit anywhere in the loop and nothing will report it.

**FILED AS A GAP, NOT A BUILD.** What a cost seat would need is not obvious — a wall-clock
assertion is a magic number and a machine-dependent one, and *`CLAUDE.md` records invented metrics
and magic numbers as a known weakness*. **The honest form is probably a COUNT rather than a time**
— calls to `_left`, or candidates evaluated per mint — **which is machine-independent and has a
denominator.** Not designed, and not to be guessed at from the shape of a good checker.

**AND THE ADJACENT FINDING STAYS RECORDED**: `_bindings`' rebuild was invisible to every check for
the life of the project, and the hoist changed **no number** — `455.91` and `526.88` identical.
**A pure-cost defect leaves no trace in any reading the register keeps.**


---

# OPEN QUESTION: DOES THE BOND VOCABULARY THIN WITH LEVEL?

**Recorded as a question, not a claim.** Figure 4: *the transform between scales loses
information, and that is the point — going up throws away detail, and that is what makes the
result reapplicable.* **If loss is what carries a composition up, the lowest level is where least
has been thrown away** — so more bond types would be available there, and higher levels would
carry coarser relations because that is what survived. **Seven at the term level, fewer at
whatever composes over terms.**

**AND IT WOULD PARTLY EXPLAIN THE RECIPES.** 2,111 of 2,651 written with `+`. **Read so far as a
notation failure; it may also be a LEVEL fact** — those recipes describe a coarser level than the
terms they would compile to, and `+` is what survived the climb. **Both can be true: the notation
is flat AND the level may genuinely carry less structure.**

> **IT FITS WHAT WE ALREADY SEE, WHICH IS WHY IT IS A QUESTION.** *Fitting what we see* is what
> the two cut rows of the chemistry mapping were cut for — bond strength and the loop as a
> macro-molecule — and an analogy is load-bearing only when the target casts a shadow.

**WHEN IT BECOMES MEASURABLE, AND IT IS FURTHER OFF THAN IT LOOKS.** It needs the second level to
hold more than one SHAPE. Today `ls20` has two terms longer than `max_depth` — **and both begin
`translate . translate . translate`, so they may be one shape under two bindings.** *Fifty saved
entries were eleven shapes* is the same collapse, and **a count of terms is not a count of shapes**,
which is the distinction the question turns on.


---

# §14.7's FOUR NUMBERS — BUILT, AND THE MVS WAS NEVER A SEPARATE ITEM

**§14.8: *report the four numbers every run, next to the abstention rate.* None was built.** And
the MVS is one of them: ***bench pulls, PER PRIMITIVE — which imports the agent actually needed.***
`summary.reused` counts pulls by TERM NAME; per primitive decomposes those into atoms, **which is
*which atoms compose most of the rest*, read off what the agent reached for.** Not a fifth number.

> **SO *WHAT IS IT WAITING ON* HAS THE ANSWER: NOTHING.** Deferred three times because I treated
> it as a study to design rather than a number the corpus had specified — **the third time this
> week. `score_molecule` had a specified price I went looking for; `contact_first` had a specified
> consumer I proposed a third thing for; the MVS had a specified form I kept scheduling.**

    ls20   effective atom depth 6 (flat = 3)   unreached over time [0.943, 0.867, 0.919, 0.954]
           bench pulls  recolour 5 · translate 4 · none 2 · all 2   never pulled 13 of 17
    g50t   effective atom depth 6              unreached over time [1.0, 0.938, 0.978, 0.992]
           bench pulls  recolour 17 · translate 3                   never pulled 15 of 17

**EFFECTIVE ATOM DEPTH READS 6 AND NOT 3** — units of length two exist, so a depth-3 search reaches
six atoms. **It was flat until candidacy landed this morning**, and §14.7's own number reads the
second level.

**AND THE UNREACHED RATE IS NOT FALLING.** §14.7: *should fall as chunks accumulate — and if it
does not, reach is not growing whatever the library size says.* **The number reads the failure it
was built to detect, on its first run.**

### THE NEVER-PULLED COLUMN HAS THREE POPULATIONS, AND I HAD IT AS ONE

    applied to a slot value (an int), the 17 atoms are:
      9 EXTENSIONALLY `idn`   idn · colour · row · col · h · w · drow · dcol · shape
      6 truth-producers       same 0 · other 1 · above 1 · all 1 · any 1 · none 0
      2 predictors            translate · recolour

**`pick`'s non-dict branch returns its argument, so every EXTRACT atom is the identity on an
integer.** They are never pulled because **`idn` is shorter and wins the bargain outright** — not
because they are unreachable. **`_library_fit` does not filter by type**: `retrieve` returns every
name and `_explains` decides, which is why `all` and `none` were pulled on `ls20` — they explain a
slot sitting at 0 or 1.

> **NINE ATOMS ARE ONE FUNCTION.** I reported the `all`/`any` pair as the extensional collapse in
> the priors; **the real number is nine**, and the 39-names-7-functions measurement was taken over
> an alphabet already 9-to-1 redundant **on the input the loop actually supplies.**

**AND *A NEVER-PULLED BENCH ITEM WAS A GUESS* IS RIGHT, WITH THE GUESS NAMED**: that eight
`OBJECT → ATTR` atoms would do something when handed an integer.

### TWO IMPLEMENTATION CHOICES §14.7 DOES NOT SETTLE, MADE AND RECORDED

**Chunk reuse read 0 because `Term.name` carries the binding and the atom tuple does not** — a
bound settled name never matched an unbound chain. **§14.7's stated failure signature, produced by
a comparison rather than by the library.**

**And it now counts OCCURRENCES over a CONTIGUOUS SUBSEQUENCE of the atom tuple.** *How OFTEN a
settled term appears inside a later mint* reads as occurrences; the alternative — how many later
terms contain it — is the smaller number and is not what the sentence says. **The substring test
over the joined name was the wrong shape and would match a name that embeds another.**


### AND CHUNK REUSE MOVED THREE TIMES WITHOUT THE LIBRARY CHANGING

    0  / 0    a bound `Term.name` compared against an unbound chain -- never matched
    8  / 1    compositions, substring over the joined name, terms-containing
    18 / 2    contiguous subsequence over the atom tuple, OCCURRENCES

**Three readings of one library, and the first is §14.7's stated failure signature.** *Zero is the
failure signature, and it is the one that would otherwise look like progress* — **and it can be
produced by the measurement before the library gets a say.** Which is the corollary already filed,
arriving on the number the corpus singles out: *a metric can report the failure it was built to
detect, for a reason that is not the failure.*


---

# THE PER-TERM ACCOUNT — `minted` EXTENDED, AND IT SAYS THE CLAUSE IT COULD NOT

**Not a new reader.** `summary.minted` already carried nine of the columns — handle, composition,
origin, admitting clause, the residual it was aimed at, cost and left. **A parallel `account()`
would have been two producers of one fact**, which is the duplication I created between
`sensors.py` and `arc_atoms.py` a week ago and then had to undo.

    ls20_TT_chain_9448fc3f
      translate . translate   aimed at o16.w@4
      reduced 14.802 bits | cost 12.51 | left 3.7 | operand in contact: False
      settled at None | rejections 1.42 | admitted accepted

**`operand in contact` reads True on one of three and False on two** — a real discrimination, from
a sensor computed every step and discarded until today.

### THE CONTACT CLAUSE HAD TO BE RECORDED, NOT DERIVED

**Contact is a fact about THIS frame and `summary` reads after the run**, so *bound to a slot that
was in contact* cannot be recovered later. **One field on the mint row, written where the binding
is chosen** — and that is **twice in two builds that a reader forced a field the ledger did not
carry**, after `level` on the repeat row. **The readers are finding gaps in the record rather than
only reading it.**

### AND THE SPLIT FOUND A DEFECT IN THE READER ITSELF

    31 accounts: 24 from a MINT · 7 installed by the SWEEP

**`_install_reuse` accepts against a parked residual and writes no mint row**, so every
mint-sourced column read `None` for those seven. **`reduced_bits: None` reads as *reduced
nothing*** where the truth is *this did not come from a mint*. **Sixth flavour of an absence
rendered as a value, and the first found inside a reader written to state accounts** — `installed_by`
now names the reason the columns are empty.


### AND I SWEPT A CORPUS FILE IN WITH `git add -A` — SECOND INSTANCE, TEN DAYS AFTER RECORDING THE FIRST

`docs/THE_FORMULA.md` had been edited externally — **Figure 12 integrated into the corpus**, with
the bond paragraph, the recursion paragraph, the two-currencies paragraph and notes 32–33 — **and
`git add -A` put it in a commit whose message named none of it.**

**The first instance swept 23,000 lines of `docs/library-closure/` deliverables and was recorded
at the time.** This one is worse in kind: **a CORPUS file, which I may annotate and never edit**,
in a commit that reads as mine.

> **THE RECORD DID NOT PREVENT THE REPEAT, AND THAT IS THE FINDING.** A note saying *I used
> `git add -A` and it swept files* is a description of an event; **it installs nothing.** The
> laws that hold are the ones that fire — and there is no seat that inspects a commit's file list
> against its message. **Same category as the cost seat: a property with no check, not a rule
> that went quiet.**

**Both were caught by reading the commit output, and both were unpushed.** The working-tree
discipline caught it twice and the register caught it neither time.


---

# THREE QUANTITIES THAT ARE ZERO TODAY AND FIRE TOGETHER

**All three are correct now, all three go live the instant a second bond exists, and none was
written down as a set.** A reader finding one has no reason to look for the others.

    1  THE BOND TERM        `(k-1)·log2(|bonds|)` in `term_bits`, with `BONDS = 1`
                            zero because `log2(1) = 0`. Rises to 2.8 bits per bond at seven.
                            MEASURED under a flat `log2(7)`: terms paying fall 7->4 on `ls20`
                            and 3->2 on `g50t`, the marginal payers paying by 1.49 bits.

    2  THE `k!` OVERCHARGE  `THE_FORMULA` note 33 -- a sequence-charging code overcharges by
                            `log2(k!)` under a SYMMETRIC bond. `->` is ordered, so today the
                            overcharge is EXACTLY ZERO. 1 bit at k=2, 2.58 at k=3, 4.58 at k=4.

    3  `space_exact`        counts type-valid CHAINS, which is arrangements under one bond.
                            *`closure(Γ)` is a space of arrangements rather than of sets*, so
                            the denominator UNDERCOUNTS the moment a second bond exists -- and
                            every coverage figure computed against it moves with it.

## THEY ARE NOT ONE SET. TWO ARE PRICES AND ONE IS A DENOMINATOR

**A MISPRICED TERM FAILS TO PAY, AND THE FAILURE IS RECOVERABLE.** Items 1 and 2 move `cost` in a
comparison against `base`. A term that should have paid and did not is **still in the residual** —
`outstanding` is monotone against the actual, nothing was spent, and re-pricing later re-offers
every term that was refused. **The loss is throughput.**

**A WRONG DENOMINATOR CORRUPTS A VERDICT, AND THE VERDICT IS ALREADY PUBLISHED.** Item 3 sits under
coverage, and coverage is what an `UNREACHED` is a claim about. **A closure searched to the end
against the wrong `λ^d` is an abstention that names a room it did not search** — which is the one
thing reach-must-be-total exists to prevent, and the reading is already in the ledger. *A metric
whose denominator the mechanism changes cannot falsify that mechanism*, and adding a bond changes
it.

> **SO THE ORDER IS FIXED WHEN THEY GO LIVE: the denominator first, prices after.** Re-pricing over
> a corrected space is arithmetic. **Re-reading every published `UNREACHED` is not, and the
> abstentions are the deliverable.**

---

# RULED: `molecule` HAS FOUR HOMES AND Q21's SENSE YIELDS

**`conform/lint.py` registers it as `A6i`** — *a prior term in `gamma` and a quantified objective in
`DISCOVERY` Q21, 9% and 37% on the same runs.* **`THE_FORMULA`'s symbol table now adds a third
gloss** — *any composition of atoms and the bonds between them* — **so two corpus documents
disagree, which is worse than a register entry: the register is where an `A6i` lives UNTIL it is
ruled.**

**Q21's own sentence contains the resolution**: *a molecule is a quantified typed **objective***.
**The thing already has a word.** Figure 12's sense has no alternative — a bonded arrangement is
what *molecule* imports from chemistry, and the whole mapping rests on it.

> **SO `molecule` MEANS A BONDED ARRANGEMENT, AND Q21's SENSE IS AN OBJECTIVE.** `score_molecule`
> becomes `score_objective` when it is built. **It costs nothing in code today** — it is unbuilt —
> **which is the cheapest moment a naming collision is ever resolvable.**

**AND THE PRECEDENT IS `OBJECT`/`OBJ`.** One constant was two things, the type graph composed
across it, and `grammar.py` had kept them apart all along. **The same shape: one word, two
quantities, and one of them already had another name.**


---

# I EDITED THE CORPUS, AT INSTRUCTION, AND THIS IS WHAT IT COST

**`THE_FORMULA.md` now carries two clauses in my hand** — a paragraph after *only one is usually
noticed*, and a sentence appended to note 33. Both say the same thing: **the `k!` overcharge and
the bond term are LATENT, not present**, because `→` is the only bond with a form in the signature.

**The instruction was explicit and the reason was sound** — *a reader taking note 33 as a live
defect would go looking for an overcharge that is exactly zero*, which is the same disclosure error
as writing *the overcharge is measured and it's small* in the wrong tense.

**THE COST IS THE ONE THE RULE NAMES.** *A defect annotated externally is still checkable. A corpus
I have edited is not.* The corpus is the one derivationally independent frame available — written
earlier, by Isaiah, in a different context — **and that independence is what every section check
has been spending.** Two clauses is a small withdrawal from it. It is still a withdrawal.

**THE MITIGATION IS THAT THE PROVENANCE IS IN `git`, NOT IN MY MEMORY OF IT.** The commit isolates
the two hunks and names them as mine, so a future reader diffing the corpus can separate Isaiah's
Figure-12 integration (`c28a0fc`) from my latency clause. **That is checkable; *I only added a
disclosure* is not.** If a later section check leans on either clause, it is leaning on itself, and
the diff is where that gets caught.


---

# SECTION CHECK ON THE TRUTH SPACE: THE PRICE IS SPECIFIED, THE STREAM IS FLAT

**The question was** *what does §11.2's "stated and wanted" consume, and does the corpus name a
price for it that isn't the transition bargain.* **It names one, and it is not a second bargain.**

**Q21, in its own words:** *"And it is priced by the same bargain, one level up. `score_molecule`
asks whether the molecule's per-step degree partitions the progress stream, thresholded at **its own
median** so the split is data-driven — 'no free parameter' — and charges two bits for the
description. Same two-part MDL, applied to objectives instead of transitions."* And the
recommendation: **one bargain, two levels — atoms priced against transitions, objectives priced
against progress.** Which is also how Q1 closes: the two residuals share machinery, so they are two
readings of one mechanism rather than two mechanisms.

**THE TENTH TIME THE CORPUS HAD ALREADY NAMED THE INSTRUMENT.** I was carrying *invent a price for
the objective level* as an open design question with a magic-number hazard attached. There was no
design question. **The threshold rule is specified AND is specified to have no free parameter.**

## And the charge has the defect note 32 just repaired, one level up

**Two bits is `log₂(4)` and four is the QUANTIFIER alphabet** — `ALL SOME ONE NONE`. But an
objective is `quantifier × relation × scope × pairing`, and **pairing alone is a choice among three**
(`consecutive` `all_pairs` `unary`). **So the objective's code charges one of its four dimensions:
it records its ingredients and not its arrangement, which is note 32's sentence verbatim.**

**Recorded, not fixed** — and the source is out of bounds. `redux_arch/molecule.py` is in the parent
folder, so this is a defect in **what the corpus states**, which is the layer the build reads.

## THE BLOCKER, AND IT IS A PANEL PROPERTY, CHECKED BEFORE THE BUILD RATHER THAN AFTER

**`score_molecule` partitions THE PROGRESS STREAM. We do not have one.** `arc_world.ground()`:
*"levels_completed, read off the frame. **There is no score field**, and `levels_completed ==
win_levels` is the win."* **Measured: `level start 0 end 0` on both games.**

> **A median-thresholded partition of a CONSTANT stream separates nothing.** Every objective scores
> identically, the scorer returns the same verdict for all of them, **and it looks like it works.**

**This is the panel-property law run FORWARD for the first time.** *Before a null is read as a
finding about a mechanism, state what property of the panel the mechanism would need in order to
show, and confirm the panel has it.* Three nulls were read before that check; **this one is being
read before the mechanism exists**, which is the only position from which it costs nothing.

**AND IT MAKES A SECOND ITEM'S DEPENDENCY VISIBLE.** The level-series prediction — *rising
unexplained mass per level if the agent is not composing* — **is waiting on the same event, and
neither item was filed as depending on it.** *Is it built* was the wrong question; **what does it
still owe** returns: **a stream with variance, which is not a component of either item.**

**THE FALSIFIER, PRE-REGISTERED:** the moment any game advances one level, the stream has variance
and both items unblock together. **Until then, manufacturing a stream to price against is the
invented-metric failure mode with a specification quoted over it** — and `outstanding()` is the
nearest candidate and is disqualified for exactly the stated reason: **it is frame-internal, so
pricing an objective against it is a frame scoring itself with a quantity it produces.**


---

# `[I]` THE CONSERVED AND THE EXPENDABLE — AND THE CORPUS ALREADY HAD FOUR FIFTHS OF IT

**Isaiah's connection from the free-energy article, recorded with his cut intact.** The check ran
first this time, and it found a boundary rather than a duplicate.

## The table, as given

| | atoms | bonds | residual | ground |
|---|---|---|---|---|
| **evolution** | genes | linkage, epistasis, recombination | fitness gap | survival and reproduction outcome |
| **agents** | primitives | the seven operators | prediction error | whatever the board returns |
| **chemistry** | elements | covalent, ionic, hydrogen | **ΔG** — what could still happen, zero at equilibrium | the second law |

**Three corrections it carries.** *The niche is the habitat, not the ground* — Figure 11's own
distinction, and the most common way this table gets written wrong. **Conservation laws are
constraint priors, not the ground**: they say what is admissible before you look, and the second law
says which admissible direction happens. **And ΔG rather than G**, because free energy is not
absolute and only changes are physically meaningful.

> **AND THE ROW THAT FITS BEST IS THE ONE TO DISTRUST.** *Agents* is the case the framework was
> built from, **so its fitting perfectly is not evidence.** Recorded in his words because it is the
> discipline applied to his own table, which is the half that usually goes unwritten.

## Why chemistry has a residual and no frame

**It is Figure 11's unmaintained mode** — *no seat, no live frame; nothing selects, and what survives
is what the ground kept.* **Evolution is the same regime.**

**So the generalised residual is the gap between the current state and what the ground will settle
for.** Prediction error where a frame exists; **fitness gap or ΔG where none does.** The frame is
what makes the gap *predictive* rather than merely *actual* — it is not what makes there be a gap.

## The claim, and the version that is NOT claimed

**NOT CLAIMED: that the second law explains why the transform is lossy.** Figure 4's loss has its own
reason — *going up throws away detail, and that is what makes the result reapplicable.* **A lossless
transform is possible and useless, so the necessity comes from the PURPOSE, not from
thermodynamics.**

**CLAIMED, in the article's own words:** *"Free energy is subject to irreversible loss in the course
of such work. Since first-law energy is always conserved, it is evident that free energy is an
expendable, second-law kind of energy."* **Two kinds of quantity in one system: one conserved, one
expendable, and only one survives a process.**

## Which is the membrane rule with a reason under it, AND THE FOOTING CHANGES

*Only methods cross up, only head starts come down.* **The method is the conserved kind; the
occasion is the expendable kind.**

> **It was stated as a prohibition WE IMPOSED. This says a recording is the expendable kind and was
> ALREADY SPENT — so carrying it up is not forbidden; there is nothing left in it to carry.**

**A prohibition invites the question *what if we allowed it*. An emptiness does not.**

## THE CHECK: four fifths present, and the fifth is exactly the load-bearing half

**Ordered as Isaiah predicted — Figure 4's notes and the Weismann citation first, and both paid.**

| | where | verdict |
|---|---|---|
| the membrane rule, verbatim | `ARC_BUILD_PLAN` 2032, quoting Figure 4 | **present** — *"a recording carried upward looks like knowledge and is a description of one occasion"* |
| Weismann | `PHILOSOPHY` 241 and 754 | **present, twice** — and 754 already carries the independence: *"arrived at a century earlier for its own reasons"* |
| **the cut** | `PHILOSOPHY` 395, quoting Figure 4 | **PRESENT, AND IT IS THE CORPUS'S OWN SENTENCE** — *"going up throws away detail; that is what makes the result reapplicable, but it means the trip is not reversible"* |
| the round trip's meaning | `PHILOSOPHY` ~445 | **present, near-verbatim** — `R_T` is *"the honest report of what the coarser description cannot hold"* |
| irreversibility as a REQUIREMENT | `ARC_BUILD_PLAN` 830 · `PHILOSOPHY` 398 | **present** — *a bijection has neither branching nor irreversibility*; an invertible transform is **fatal**, because a bijection iterated gives orbits and not a tree |
| **the conserved/expendable split** | — | **ABSENT.** No `conserved`, `expendable`, `free energy`, `second law` or `thermodynam` anywhere in the corpus |
| **the changed footing** | — | **ABSENT.** The corpus states the rule and its CONSEQUENCE — *"produces a system that repeats a past success and cannot produce a new one"* — never a reason the recording is empty |

**SO THE CUT WAS UNNECESSARY AND IS THE MOST VALUABLE PART OF THE ITEM.** Isaiah cut the
thermodynamic explanation of lossiness before offering it; **the corpus had already refused the same
claim, for the same reason, in Figure 4's own words.** Two frames arriving at one boundary
independently is what the whole method is for — **and it means the surviving claim is the one that
was never in contention.**

## ANNOTATION TO `PHILOSOPHY` 754 — Weismann is now corroboration at maximum independence

**Corpus, so annotated and not edited.** The citation reads *"generators cross up, playback never
does, arrived at a century earlier for its own reasons."* **It should now say THIRD FRAME.**

    1  the membrane rule   ours, derived from Figure 4's round trip
    2  Weismann 1892       germline barrier, biology, a century earlier
    3  free energy         conserved vs expendable, thermodynamics

**Three frames, three centuries, three fields, one distinction** — and none of the three derived from
another. **§8.4's requirement is an interpreter DERIVATIONALLY INDEPENDENT of the thing explained;
this is that condition met twice over on a single rule**, which is the strongest corroboration
available and is stronger than anything the corpus currently claims for it.

---

# THE DELIBERATE PASS: FIVE THINGS WAIT ON A LEVEL ADVANCE, AND TWO HAVE NEVER EXECUTED

**Two were found by accident, which is why the pass was worth running.** *Is it built* returns yes
for all five; ***what does it still owe*** returns the same event five times.

    1  score_objective         the progress stream has no variance -- a median-thresholded
       (the truth space)       partition of a constant separates nothing
    2  the level series        rising unexplained mass per level, if the agent is not
                               composing. One level = one point = no series
    3  Budget's ACCRUAL        `left += per_level`. NEVER RUN LIVE -- `level_starts()` is
       ** never executed **    called ONCE at `arc_holdout.py:78` and never again. Exercised
                               only by `arc_check.py`'s two-level fixture
    4  `boundary()` at a       `arc_world.py:65` -- bindings drop at a LEVEL change. Fires
       level change            live only via `retarget` on GAME_OVER, which is a different
       ** never on a level **  event reaching the same code by a different route
    5  terminal 1 and 3        "it wins" is clause 1; the ablation is a POST-MASTERY test

**ITEMS 3 AND 4 ARE THE FINDING.** The first two are measurements that would read null, which is
recoverable. **These are MECHANISMS that have never run in the situation they were written for** --
and item 3's own docstring says *"THE ACCRUAL IS THE PART THAT GETS LOST. `500 per level` reads as a
flat cap"*, so it is a mechanism that documents its own failure mode and has never once been in
position to exhibit it.

**A fixture is not an execution.** `arc_check.py` proves the accrual CAN run; **nothing shows it
DOES**, because the live path calls the trigger once. *Tests reach, not existence* -- and here the
test reaches something the loop never does.

> **AND THE DEPENDENCY WAS IN NO GRAPH.** Five items, five different files, one event, **and not one
> of them names it as a precondition.** The single common cause was invisible because each item
> looked complete on its own.

## Which makes `levels_completed` a PRECONDITION, not a metric

**And it has been neither all week.** As a metric it was correctly refused -- *a ground reading taken
below the break is a reading of nothing*. **As a precondition it was never considered at all**, and
that is a different role for the same quantity: **not what we read off the run, but what five
mechanisms are waiting for permission from.**

---

# AND THE TRUTH-SPACE FINDING IS SHARPER THAN RECORDED: THE OBJECTIVE EXISTS AND IS CONSTANT

**`arc_world.objective()` returns `("ALL(BECOME(level, completed))", levels_completed / win_levels)`.**
Measured: **`start 0.0 max 0.0 end 0.0` on both games.** So Q21's shape -- a quantifier over an inner
relation, returning a degree -- **is already instantiated**, and I filed the consumer as needing a
thing that is built.

**THERE ARE TWO GATES AND THEY ARE AT DIFFERENT LEVELS.**

**GATE 1 -- there is ONE objective and the agent did not pose it.** The bargain prices a CHOICE;
**a bargain with a single candidate is not a bargain.** `ALL(BECOME(level, completed))` is the
terminal condition read off the frame, which is legitimate -- **the ground is allowed to be known.**
What is missing is the **sub-objectives**, the intermediate wants that would partition progress
toward it, **and those are what Q21 prices.**

**And there are none because there is no vocabulary to state one in.** No EXTRACT -> no attributes ->
no predicates -> no sub-objective. **§11.2's chain, breaking at link 2, exactly where Figure 3 says
chains break** -- *"because it attracts the least attention and the fewest instruments."*

**GATE 2 -- the stream is flat**, which blocks the pricing even if candidates existed.

> **GATE 1 IS ABOVE GATE 2, AND ONLY GATE 1 IS OURS TO MOVE.** A level advance is a capability
> outcome. **EXTRACT is a build.** So the item's true dependency is not the event after all -- it is
> the missing space in §11.2's own table, and the flat stream is what would block it AFTERWARDS.

**I had the order backwards when I reported the section check**, and the correction changes what is
actionable: **the truth-space consumer is not gated on a level advance. Its INPUT is.**

---

# THE GENERAL RULE FROM THE `molecule` CASE

> **RESOLVE A NAMING COLLISION WHILE THE LOSING SENSE IS UNBUILT. It is the cheapest a collision is
> ever resolvable, and the cost rises with every call site.**

**`score_molecule` -> `score_objective` cost nothing because nothing calls it.** `OBJECT`/`OBJ` cost
a type-graph audit because the type graph already composed across it. **Same collision class, two
prices, and the difference was entirely WHEN.**

**AND IT GIVES `A6i` A TRIGGER IT LACKED.** The register says *check what a name means in both places
before pinning a shape to it*, and its trigger is *where a headline or a ruling is about to be made*.
**This adds a second and cheaper one: at the moment a second sense is FIRST WRITTEN DOWN, before
anything consumes it.** `molecule` was catchable when Figure 12's gloss entered the symbol table --
one edit ago, with zero call sites -- **and A6i's existing trigger would not have fired there,
because no ruling was being made.**


---

# `[I]` THE FOUR LAWS: ONE FINDING, THREE PARALLELS, AND ALL FOUR ARE IMPORTS

**Marked by kind in the figures' own convention, and entered as IMPORTS WITH A SOURCE rather than
as ground.** Thermodynamics is a frame's laws and the frame is ours, **so Figure 8's rule applies:
an import is debited against the source frame's independence, and the source is named.**

## THE SECTION CHECK, WHICH WAS THE SPECIFIC QUESTION

**Asked: does Figure 11's isolation law or Figure 10's channel decay already carry the direction?**

**FIGURE 11 DOES NOT.** *Isolation is substitution, not removal*, with **two silent failure modes:
what you failed to reproduce, and what you brought with you.** Both are properties **of the moment
of substitution** -- a static comparison of two habitats. **Nothing about what happens next.**

**FIGURE 10 DOES, FOR THE CHANNEL.** *"The ground does not decay, the channel does -- stale
percepts, dropped transients, saturated metrics, pooled readings. The output is not a verdict, it is
`you have lost touch`* -> **keep the anchor reachable.**" **That is a direction and a contact remedy,
already stated**, and closer to the claim than I expected to find.

> **SO THE FINDING NARROWS AND SURVIVES, AND THE RESIDUE IS THE PART THAT MATTERS.** Figure 10 gives
> **FOUR MECHANISMS** by which a channel decays. **The second law gives a direction that does not
> depend on which mechanism** -- and an enumeration of failure modes is always potentially
> incomplete, so *a channel exhibiting none of the four* is arguable under Figure 10 and refused
> under the second law. **A list of ways is not a direction.**

**And the scope differs: Figure 10's subject is the CHANNEL -- the instrument going stale. The
claim's subject is the FRAME -- what it holds.** Neither figure orients that one.

**Eleventh instance, and the third distinct form this week.** Not *the corpus named the instrument*,
not *the corpus refused the claim*, but **the corpus carried it at one scope and not the other.**

## THE FINDING, SCOPED AS IT MUST BE

> **`[F]` IN THIS FRAME, ISOLATION HAS A DIRECTION.** A frame that stops touching the ground can
> only lose structure. **Not *might drift* -- the direction is fixed, and it does not reverse
> without contact.**

**NOT CLAIMED: that isolated frames degrade necessarily and everywhere.** The import is from this
universe's physics; **a frame with different laws would need a different filler for the same
structural slot.**

**THE SLOT IS WHAT THE FRAMEWORK CLAIMS. THE FILLER IS WHAT WE IMPORTED** -- vocabulary versus
instance, arriving at the level of the whole framework, **and that split has now been the answer six
times.**

**What it adds:** it makes **Figure 10's *permanent work rather than a solved state* a NECESSITY
rather than an observation.** And the weaker form the corpus already holds without it is Figure 11's
*what you failed to reproduce is invisible until the goal fails* -- **the direction is the import's
contribution, held at the import's confidence.**

## THE THREE PARALLELS

**`[P]` ZEROTH -- transitivity licenses the thermometer.** Without it temperature is not a
well-defined quantity. **Restates Figure 2:** frames are comparable without talking because each
ranges against the anchor separately and **the comparison runs through the thing neither can move.**
**And collapse 1 is the zeroth law broken** -- an anchor that updates means the third system moved
and transitivity fails. *It says why the design works; the design already says it.*

**`[P]` FIRST -- energy is neither created nor destroyed, only transformed.** **Restates Figure 6:**
*MINT composes inside the closure and can never add an atom.* Minting is **re-reading, not
creation.** **And IMPORT is the open-system exception**, the first law holding only for a closed one:
*the wall moves only on contact with a frame whose closure differs.*

**`[P]` THIRD -- absolute zero is approachable and unattainable in finitely many operations.**
**Restates Figure 7:** *every room closes some of the gap; no finite number of them ever arrives.*
**And zero residual is the framework's absolute zero** -- perfectly ordered, nothing left to explain,
completely inert. **Which is the loop's stopping condition and why it is ambiguous:** *a perfect
prediction or a closed channel, and from inside those look the same.*

## AND THE REASON THE FRAMEWORK DOES NOT REST ON ANY OF THEM

**Figure 6: an import adds no atom to the world.** The world does not gain primitives; **a frame
gains ACCESS.** So *other universes have different atoms* is already stated, and what is ours is
access rather than the inventory.

**Which is why the framework cannot be grounded in physics: physics is a frame with a closure, and
grounding a metatheory in one frame's closure is what Figure 2 calls collapse 1.**

**The corpus's load-bearing results are the ones that hold in ANY frame** -- *composing inside a
closed set never leaves it* is definitional, and **Godel, Tarski and Chaitin are theorems.** Those do
not depend on our physics. **The thermodynamic parallels are corroboration from a frame that reached
the same structures separately, which is worth more as corroboration than it would be as
foundation.**

## THE ENTROPY IDENTITY -- FILED AS A NOTE, AT THE CODE'S SITE

**Placed at `tether.BONDS`, not in the figure**, because its value is that a reader can check the
formula against Shannon rather than take it on trust. **Shannon and thermodynamic entropy are the
same mathematics, MDL is built on Shannon, and both are already cited on Figure 5** -- so
`log2(|bonds|)` **is** the entropy of the arrangement space in bits. **Two laws in one line: the
first says you cannot create atoms, the second says rearranging them is not free.**


---

# SECTION CHECK ON `EXTRACT`: IT IS BUILT, AND THE DEFECT IS THAT IT CANNOT ABSTAIN

**The question was what §12.2's `OBJECT -> ATTR` sensors need in order to publish. THEY ALREADY
PUBLISH.** `arc_atoms.ATTRIBUTE_TYPE` carries **eight** keys and `_extract` makes an `Atom` of each:

    colour -> COLOUR     row, col -> POSITION     h, w -> EXTENT
    drow, dcol -> DELTA  shape -> SHAPE

**All four of §12.3's unary sensors are represented**, two of them on both axes. **So §11.2's table
saying EXTRACT is *missing* is stale against the code** -- corpus, annotated here, not edited.

**Twelfth instance, and a fourth form: the corpus was BEHIND the code.** Every previous one had the
corpus ahead. **The check is not only a lookup for things I am about to design -- it is a diff, and
it runs in both directions.**

## THE DEFECT, AND IT IS §12.2's SECOND PROPERTY EXACTLY

**§12.2:** *"Total, with an explicit non-reading. A sensor returns a value or `NOT_RESOLVED`. **Never
a guess, never a default.** That is abstention at the sensor level, and it is what lets 'this
instrument cannot see it' propagate up instead of becoming a wrong attribute."*

**`arc_atoms._extract`'s `pick`:**

    return o.get(key, 0) if isinstance(o, dict) else o

> **`o.get(key, 0)` IS A DEFAULT, AND IT IS THE ONE THE RULE NAMES.**

**`sensors.py` honours the rule at every branch** -- eleven `NOT_RESOLVED` returns, and its own
header says the pre-existing code had *"no `NOT_RESOLVED`"* and that this was the defect being
repaired. **The extractor wrapping reintroduced it one layer up**, in the file whose docstring says
the sensors were *wrapped rather than rewritten*.

## AND THE CASE IS ALREADY WRITTEN DOWN AT THE OTHER SITE, IN ITS OWN WORDS

**`arc_percept.py` 288, at the tracker**, on why `drow`/`dcol` are ABSENT on a birth:

> *"...it did not move* where the truth is *there was nothing to move from*. An absent slot is what
> the loop already handles -- *a new slot has no history and owes nothing yet* -- so **absence is the
> reading**."

**The absence was built deliberately, with the hazard named at the site. `pick` restores the exact
`0` the absence exists to prevent.** On every birth, `drow` extracts `0` and the agent cannot
separate **did not move** from **was not there last frame.**

**TWO FILES, ONE RULE, OPPOSITE BEHAVIOURS -- and neither is wrong on its own reading.** The tracker
is right that absence is the reading; the extractor is right that an atom must return something.
**The rule that resolves them is §12.2's, and only one file is applying it.**

**This is the alignment claim failing at the lowest level it can fail at.** Not a wrong answer -- **a
confabulated one, at the sensor, where the whole architecture says abstention must start.**

## WHAT THE CHECK ALSO CAUGHT: THE DOCSTRING SAYS FIVE AND THE TABLE HAS EIGHT

**`_extract`'s docstring:** *"WHICH FIVE THESE ARE WAS NEVER DECIDED... `cells` and `shape` hold
frozensets and were skipped by the wrapping, not by a rule. **The ceiling on what can be represented
is an encoding accident, and the next reader will assume five was chosen.**"*

**`shape` and the two DELTA keys were published since**, so the table is eight and the warning is
stale -- **and the warning was RIGHT: the ceiling moved by an encoding change, exactly as it said,
and the docstring recording that fact is now the thing that is out of date.** Repairable at source;
it is code.

## SO THE BUILD IS NOT "ADD EXTRACT". IT IS THREE THINGS, AND THE CORPUS SPECIFIES ALL THREE

    1  `pick` returns NOT_RESOLVED on a missing key      §12.2, verbatim
    2  NOT_RESOLVED PROPAGATES through composition       §12.2: "lets 'this instrument cannot
       to the term, which then cannot bet on that slot   see it' PROPAGATE UP instead of
                                                         becoming a wrong attribute"
    3  the docstring's count and warning repaired        it is code, and it is now false

**No design question in any of the three.** Propagation was the one place a choice looked available
and §12.2 answers it in the same sentence that states the rule.

**AND THE THING THAT WOULD MAKE IT VISIBLE IS ALREADY MEASURED.** The extractors are **8 of the 13
never-pulled atoms**. If abstention changes nothing, the pull counts do not move and the mechanism
is inert; **if it changes something, it changes what a term is allowed to bet on, and that is
contact.**


---

# BUILT: §12.2 ENFORCED AT THE EXTRACTOR. THE FALSIFIER READ NULL, AND THE NULL IS THE FINDING

## TWO CORRECTIONS FIRST, BOTH MINE, BOTH FROM ASSERTING A CONSEQUENCE WITHOUT CHECKING IT

**ONE -- THE BIRTH CLAIM WAS WRONG.** I wrote that on every birth `drow` extracts `0` and the agent
cannot separate *did not move* from *was not there last frame*. **`arc_percept` 317 is `if attr in
obj`**, so on a birth the slot `name.drow` is **absent from the state dict**, and `perceive` bets only
over `[s for s in self.slots if s in before]`. **The perception layer was already abstaining
correctly, exactly as its own comment at 288 says it should.** `pick`'s `o.get(key, 0)` needs a dict
and never receives one.

**TWO -- AND I DID IT AGAIN IN THE SAME BREATH.** I then wrote that eight atoms *could previously earn
credit for predicting "no change" while reading nothing*. **The A/B refutes it: every published
number is identical.** They earned nothing, because **nothing ever evaluated them.**

> **BOTH ERRORS HAVE ONE SHAPE: READING A BRANCH WITHOUT CHECKING ITS REACHABILITY.** The law is
> already written -- *read the things that produce conditions before the things that produce
> results* -- and `_decomposed` is the producer I read last, after `pick`, after `sensors.py`, after
> §12.2. **Twice in one item, and the second time was after naming the first.**

## THE A/B, RUN AS A WORKTREE AT `HEAD` AGAINST THE WORKING TREE -- ONE VARIABLE

    BEFORE  ls20  outstanding 741.131 | pe 1367.156 | library 67 | minted 39 | advanced False
    AFTER   ls20  outstanding 741.131 | pe 1367.156 | library 67 | minted 39 | advanced False
    BEFORE  g50t  outstanding 971.088 | pe 1397.375 | library 45 | minted 23 | advanced False
    AFTER   g50t  outstanding 971.088 | pe 1397.375 | library 45 | minted 23 | advanced False

**IDENTICAL TO THREE DECIMALS ON EVERY PUBLISHED QUANTITY.** The pre-registration said *inert if the
pull counts do not move, contact if it changes what a term may bet on.* **It is inert, and the reason
is structural rather than accidental.**

## THE MECHANISM WORKS -- VERIFIED DIRECTLY, NOT INFERRED FROM THE NULL

    extractor on an int (the live stream)  -> NOT_RESOLVED
    extractor on a dict WITH the key       -> 5
    extractor on a dict WITHOUT the key    -> NOT_RESOLVED
    two-atom chain, first atom abstains    -> NOT_RESOLVED   (propagates, never becomes a value)

**So this is not *the change did nothing*. It is *the change is correct and nothing reaches it*** --
and those are different findings that a null alone cannot separate. **Checking the mechanism
separately from its effect is what made the difference readable.**

## AND THE REASON IS THE TYPE GRAPH, WHICH IS DOING ITS JOB

    OBJECT -> COLOUR        colour
    OBJECT -> POSITION      row col
    OBJECT -> EXTENT        h w
    OBJECT -> DELTA         drow dcol
    OBJECT -> SHAPE         shape
    COLOUR -> PRED          same other
    POSITION -> PRED        above
    PRED -> OBJ             all any none

**Every extractor's `in_type` is `OBJECT`. The transition bargain enumerates `slot -> slot`.** A
different node, so **an extractor can never be a candidate for a transition** -- not by accident, by
typing. The atoms were never identity-on-an-int in the loop **because the loop never applied them.**

> **THE CHAIN IS COMPLETE AND TYPED END TO END -- `OBJECT -> ATTR -> PRED -> OBJ` -- AND NOTHING
> CONSUMES `OBJ`.** It terminates in an objective, and an objective has no reader.

## WHICH IS THE GAP `CLAUDE.md` ALREADY NAMES, NOW MEASURED INSTEAD OF ASSERTED

The instantiation map lists as NOT INSTANTIATED: *the objective layer* and **the second consumer for
EXTRACT/RELATE/QUANTIFY.** **This run is that entry, arrived at from the other end.** Not *we have not
built the consumer yet* but **a complete, correctly typed, three-space chain that produces objectives
nobody reads**, and a measurement that is byte-identical because of it.

**AND IT REPLACES THE DIAGNOSIS I GAVE AN HOUR AGO.** I said EXTRACT runs before the loop at a
vocabulary the seat fixed, and that the agent cannot reach for an attribute because attributes are
computed on the way in. **The first half is true and the second half is not the binding constraint.**
`_decomposed` does flatten, **but the extractor atoms exist, are correctly typed, and compose into
`PRED` and `OBJ`.** What stops them is not the flattening -- **it is that the far end of the chain
has no consumer, so the chain is never enumerated for anything.**

## THE THREE, BUILT AND KEPT

    1  `pick`         BOTH branches were guesses. `o.get(key, 0)` asserted the attribute is zero;
                      returning a non-dict unchanged asserted THE SCALAR IS THE ATTRIBUTE
    2  `Term.apply`   short-circuits on NOT_RESOLVED, plus six consumers: `_predict` returns None
                      and the slot is not bet on with a row saying so; three bargain sites charge
                      unread AS UNEXPLAINED, the rule they already applied to `inapplicable`; two
                      branching sites drop a candidate that cannot read, because it splits nothing
    3  docstring      the old warning CAME TRUE -- *the ceiling is an encoding accident* predicted
                      five going to eight by exactly the route it named -- so it is restated

**KEPT ON THE RULE, NOT ON THE RESULT.** §12.2 is a constraint the architecture rests on, and the
measurement says nothing currently exercises it. **Before this, `NOT_RESOLVED` had ONE consumer in the
repo** -- `arc_world` 108, testing board readability. `sensors.py` returned it from eleven branches
and **nothing downstream could receive one: a declared abstention with no path.** There is now a
path, and it is empty.


---

# THREE CHECKS: `∥` RULED, THE CYCLE BOUND LOCATED, AND THE CONSUMER FOUND ALREADY BUILT

## 1 · `∥` -- THE OUTSIDE DOCUMENT IS WRONG, AND `∥` HAS ONE SENSE

**`OPERATORS.md` does not merely gloss the operators; it supplies a DISCRIMINATING TEST for each,
and the test decides this.**

    +   conjunction   both present, order irrelevant   swap the operands -- does meaning change?
    ∥   disjunction   either suffices, not both        REMOVE ONE -- does it still work?

**"Run independently or in parallel" IS *both present, order irrelevant*. That is `+`.** The document
assigned `+`'s meaning to `∥`'s glyph.

**And the test settles it rather than the gloss.** Two genuinely concurrent contributors: **remove one
and it breaks -> `+`.** It survives removal only where one was redundant -- **and then it is
disjunction, correctly classified.** *Concurrency is not a second sense of `∥`; it is `+` under
another name.*

**THE CAUSE IS NAMEABLE: it read the GLYPH's convention -- process-algebra `P ∥ Q` -- rather than the
table's definition.** Which is `A6i` from the outside: **one symbol, two conventions**, and here the
corpus's definition is authoritative **because it carries an operational test and the convention does
not.**

> **AND IT DOES NOT TOUCH `≡`, WHICH IS A DIFFERENT FINDING IN KIND.** `≡`'s two senses are INTERNAL
> -- `OPERATORS.md` defines it as *two names, one referent* and its own worked example says a
> definitional identity **is not a recipe at all**. The outside document split the same seam
> independently. **`∥`'s claimed second sense exists only in the outside document and fails the
> corpus's own test.** One is corroboration at independence; the other is a misreading.

## 2 · THE CYCLE BOUND IS NOT IN THE CORPUS -- BUT THE RULING ON WHERE IT GOES IS

**Composition cannot cycle today, and the reason is structural: `Term.atoms` is a TUPLE applied left
to right.** No branch, no back-reference, termination guaranteed by length. **Figure 12's *a chain
cannot close by construction* is the code's actual shape**, not an aspiration.

**What IS bounded is the SEARCH** -- `Config.max_depth` and `Config.budget`, `while frontier and depth
<= max_depth`. **That bounds ENUMERATION, not EVALUATION**, and a cyclic term would loop at evaluation
regardless of how it was found.

**So the bound is not in the corpus, exactly as read -- and it becomes necessary the moment trees
arrive.** Same latency class as the other three, **and the first that is not a number.**

**AND `snaps._acyclic` CARRIES THE RULING, one level over, in its own docstring:**

> *"A `chain` slot reads its target's NEW value, so chain-to-chain would be a cycle inside one tick.
> **Repair at the SPEC, not with a guard at evaluation -- a world that cannot be evaluated is a
> malformed world, not a runtime case to handle.**"*

**Transferred: refuse a cyclic composition AT CONSTRUCTION, never with a runtime guard.** The corpus
does not have the bound and **does have the ruling on where it belongs**, which is the more expensive
half.

## 3 · THE CONSUMER FOR `OBJ` IS BUILT, TYPED, AND IN EVERY BET

**`grammar.py` 81:** `_p(WANT, "Speech-act", (T.OBJ,), T.PRED, ...)`

> **`WANT : OBJ -> PRED`.** It is one of the four nodes of `_BET_ORDER`, so **every bet the agent
> makes already consumes an objective.**

**I SAID LAST TURN THAT NOTHING CONSUMES `OBJ`. THAT WAS WRONG, and `CLAUDE.md`'s instantiation map
says it too** -- *the second consumer for EXTRACT/RELATE/QUANTIFY* listed as NOT INSTANTIATED.
**Fourth form again: the corpus behind the code, and me repeating the corpus without checking.**

**WHAT IS ACTUALLY MISSING IS THE WIRE.** `tether` 1537:

    name, deg = self.env.objective()
    want = G.compose(G.WANT, G.compose("ALL", G.compose(
        "BECOME", G.Leaf(G.T.OBJECT, name), G.Leaf(G.T.ATTR, "satisfied"))))

**The `WANT` is hand-built from the world's ONE hardcoded objective string.** The composed chain
`OBJECT -> ATTR -> PRED -> OBJ` produces objectives; `WANT` consumes objectives; **the two are never
connected.** Producer built, consumer built, no wire.

**AND `arc_atoms` ALREADY NAMES THE CORRESPONDENCE**: *"`_quantify` yields OBJ -- a complete objective,
which is `grammar.T.OBJ`'s own gloss."* **So the two `OBJ`s are declared to be the same thing in two
representations, and nothing acts on the declaration.**

## AND THE WIRE NEEDS A SELECTOR, WHICH IS WHERE IT STOPS

**One objective needs no choosing. A COMPOSED chain yields many** -- every `PRED` through
`all`/`any`/`none`. **So wiring the producer to the consumer requires something that picks, the
moment it is wired.**

**Q21 is the picker and it is the only one named:** *the same bargain one level up, thresholded at its
own median against the progress stream.* **And the progress stream is `levels_completed / win_levels`,
measured `0.0` start to end on both games.**

> **SO THE CIRCLE IS: the wire needs a selector, the selector is Q21, Q21 needs progress variance, and
> the stream is flat.** Recorded two days ago as the truth-space blocker, **now reached from the
> opposite end and arriving at the same edge** -- which is what makes it structural rather than a gap
> in what has been built.

**AND THE PRECEDENT IS `0a`, WHICH IS THIS EXACT SHAPE ONE NODE OVER.** *Structurally complete and
observably inert*, parked on a measured 13x-for-zero-capability, with the trigger *an atom that
consumes past index 0* -- **a grep, not *revisit later*.** The trigger here is the same kind of thing:
**a progress stream with more than one value.**


---

# THE MAP CARRIED A FALSE BLOCKER, AND THREE THINGS RECORDED BEHIND IT

## THE CORRECTION TO `CLAUDE.md`, WHICH IS THE ITEM THAT MATTERS

**The instantiation map listed *the second consumer for EXTRACT/RELATE/QUANTIFY* as NOT
INSTANTIATED. IT EXISTS.** `WANT : OBJ → PRED`, one of `_BET_ORDER`'s four nodes, in every bet.

**Repaired at source, because `CLAUDE.md` is a working document.** What replaces it is smaller and
true: **the WIRE and the SELECTOR are missing, not the consumer.**

> **A MAP ENTRY SAYING A THING DOES NOT EXIST IS WORSE THAN ONE SAYING IT IS UNFINISHED.** *Does not
> exist* closes the question; *unfinished* invites a look. **This one closed it for a week and was
> quoted back several times, by me, as a blocker.**

**AND THE FAILURE IS THE FOURTH FORM'S WORST CASE.** The other three had the corpus ahead of the code
or behind it. **This one had me READING the corpus, QUOTING it, and never checking it** — and
familiarity is the mechanism: *citing a file feels like evidence of having read it.*

## THE GLYPH RULE, FROM `∥`

> **A GLYPH'S CONVENTION AND A TABLE'S DEFINITION CAN DIVERGE, AND ONLY ONE OF THEM HAS A TEST.**

**`∥` reads as process-algebra parallel composition to anyone arriving from outside**, and
`OPERATORS.md` defines it as disjunction **with a discriminating test attached** — *remove one, does
it still work?* **The definition wins because it is falsifiable and the convention is not.**

**And the rule names when it applies: wherever a corpus borrows a symbol that already means something
elsewhere.** Which is most of them — `≡`, `⇒`, `∥`, `⋛` all carry prior conventions. **The table is
authoritative for the same reason the ground is: it is the thing that can be checked against.**

## THE CYCLE BOUND IS THE FOURTH LATENCY, AND THE FIRST THAT IS NOT A NUMBER

    4  A CYCLIC COMPOSITION   impossible today: `Term.atoms` is a TUPLE applied left to right,
       ** not a number **     so there is no branch and no back-reference, and termination is
                              guaranteed by length. `max_depth` bounds ENUMERATION, never
                              EVALUATION. Becomes reachable the moment TREES arrive.

**The other three are quantities that read zero. This one is a STRUCTURE that cannot be expressed**,
which is why it needs a different repair: **not a value to recompute, but a refusal to install.**

**AND THE RULING IS ALREADY WRITTEN, one level over, in `snaps._acyclic`:** *repair at the SPEC, not
with a guard at evaluation — a world that cannot be evaluated is a malformed world, not a runtime
case to handle.* **So the bound goes at construction and is not a runtime check to design** — the
expensive half was already decided.

## THE TRIGGER, AS A GREP RATHER THAN A NOTE TO SELF

**`0a`'s trigger is *an atom that consumes past index 0* — checkable, and checked three times.** The
objective wire gets the same treatment.

> **TRIGGER: `summary.levels(rows)["advanced"] is True` on any game.** One level advancing gives the
> progress stream a second value, **which is precisely what Q21's median threshold needs in order to
> partition anything.**

**Until it fires, wiring the producer to the consumer installs a selector that cannot discriminate**
— and that is the failure shape the last two items established, **with the check available before the
build for once.**

**AND IT IS THE SAME TRIGGER AS FOUR OTHER PARKED ITEMS** — `score_objective`, the level series,
`Budget`'s accrual, and `boundary()` at a level change. **Five items, one grep.**

## AND THE BOARD HAS NO BUILDABLE ITEM

**Stated plainly rather than replaced with something adjacent.** Everything remaining is behind one
of two events: **a level advancing**, or **a decision about trees** that has not been asked for.

**That is a real state and it is not a stall** — *an improvement that does not change contact changes
nothing*, and the honest reading of today is that **the contact-changing work is gated on the
ground, not on the code.**


---

# `[I]` THE IMPROV FRAME, AND THE CUE CENSUS: HALF A LOOKUP, AND A TYPE NODE WITH NO PRODUCER

**Isaiah's frame — Improv plus 20 Questions.** A Conductor knows a secret ending, may not speak or
write, **judges and does not explain**, and every turn must end with an action. **That is RLVR, and
the starved cue vocabulary is the firewall stated as a rule of play.**

**Three corrections to my reading, all taken.** The Conductor need not want them to win — *the board
is no more adversarial than a maze* — and **the adversarial stance is the MAKERS', which is Figure
10's office: a ground with a reputation to protect is disqualified.** Cues are rationed **by type,
not by count** — a limited alphabet with unlimited repetitions, **which explains a flat counter
without appealing to the ground.** And **the shared-language objection was mine and was wrong**:
*both speak in motions, actions and causality*, which is Figure 1's own line. **Charades settles it —
no shared vocabulary, full communication, because the channel is action and the reading is causal.**
So not thin-channel-versus-rich: **same channel, same language, more raw frame and fewer words.**

## THE BLOCKER, RESTATED BETTER THAN WE HAD IT

> **The Conductor is giving no *warmer*, and the game is unplayable without one.** Thumbs-down and
> nothing else — counter flat, state *not finished* forever, **and a frame diff says something
> changed without saying whether it was toward anything.**

**And the corpus answers it.** Figure 5: *when nothing is scoring, the drive manufactures a gradient*
— seek the gap that is large and compressible, **and it is built.** **A posed sub-objective is a
self-made wrist tilt**, which reframes the objective layer entirely: **not to score better, but to
have a warmer signal at all.** With Figure 5's own warning kept — *its own output is never a measure
of success.*

## SECTION CHECK 1 · IS THE CENSUS A LOOKUP? HALF OF IT IS, AND NOT THE HALF NAMED

**`alphabet()` IS NOT IT.** It is the **coding range** — what a slot COULD take, declared by the
domain for `correction_bits`: `2**(h*w)` for a shape, board dimensions for a delta. **Declared from
the generator's shape, which is the kind of quantity the corpus says must never be used as a measured
premise.** The census asks what the world ACTUALLY produced. **Different subjects.**

**BUT §16.4's SEVEN ARE, AND THEY ARE BUILT.** `arc_percept.Affordances`:

    blocks · passes · moves_when_touched · changes_on_touch · triggers_remote
    terminates · consumed

**That IS a cue alphabet, per object kind, learned by interaction** — and it is *cues rationed by
type* as a data structure. **It even keeps unread apart from absent**: *on a board with no avatar
those stay unread rather than false, and the profile records which it is.* **Fourteen for fourteen,
and `triggers_remote` is the unlocking cue while `terminates` is the ending cue.**

> **WHAT IS NOT BUILT IS THE TOPOLOGY.** `Affordances` records **which cues a kind has**. The five
> shapes are about **how cues depend on each other** — independent, sequential, unlocking,
> conditional, k-of-n. **Nothing reads relations BETWEEN cues.** The alphabet is a lookup; the
> grammar over it is not.

## SECTION CHECK 2 · k-OF-n IS NOT `ONE`'s GAP, AND THE TWO SHOULD NOT BE MERGED

**Built: `all`, `any`, `none`. Q21 names four — ALL, SOME, ONE, NONE. So `ONE` is absent, as read.**

    none  k = 0        any  k >= 1        all  k = n        ONE  k = 1 exactly

**`ONE` IS NOT GENERAL k-OF-n.** `ONE` is a fixed threshold at one; k-of-n needs an **arbitrary**
one. **Installing `ONE` would not deliver k-of-n**, so they are different gaps and merging them would
hide that.

**AND THEY DIFFER IN STANDING, WHICH IS THE PART THAT MATTERS:**

- **`ONE` is a COMPLETENESS gap against a spec** — the corpus names four and the code has three.
  **But it still fails the entry rule**: the loop runs without it and the agent has not minted a
  crude version. **So it is not installable either, and *the corpus names it* is not an entry
  clause.**
- **k-of-n is OUTSIDE the spec.** Nothing names a counting quantifier, and **what it needs is
  `COUNT`.**

**AND `COUNT` IS A TYPE NODE WITH NO PRODUCER.** `sensors.py` 44 declares it beside COLOUR, POSITION
and EXTENT; **`ATTRIBUTE_TYPE` has no key that yields it and no atom returns it.** A declared node in
the type graph **with zero in-edges** — which is why no chain can ever reach a counting quantifier.

> **AND §12.3 ALREADY RULED IT.** *`count` composes from components plus a colour filter* is listed
> among the Tier 2 examples, with **the agent should have to reach for them, because reaching is the
> only evidence the composition system works.** **So k-of-n is not a missing feature. It is the
> §12.4 circle again, at a third site** — and the ruling that forbids installing `parity(POSITION)`
> forbids installing `count` for exactly the same reason.

**Second time this week the counting gap has surfaced from a different direction, and it is the same
node both times.**

## WHAT THE CENSUS WOULD COST, STATED AND NOT BUILT

**All five topology readings are over frame-diff history, which every run already has** — no level
advance required, which is what makes it the one item not behind that grep. **What it is not is
free**: the k-of-n reading needs *which combinations were tried and what followed*, and **that is a
record over ACTION SUBSETS, not over steps.** The two hidden variables are asymmetric — **how many
cues exist is a count; how many of which are needed is invisible to any count**, and only shows in
combinations attempted.


---

# THE CUE TOPOLOGY IS §16.1, IT IS BUILT, AND IT IS NEVER READ ON A LIVE RUN

**The ruling was *build the four*. THREE OF THEM EXIST, ONE IS RULED OUT IN ADVANCE, AND THE ACTUAL
GAP IS SOMEWHERE ELSE.** Sixteenth check this week and the largest.

## §16.1 SPECIFIES THE INSTRUMENT, AND SPECIFIES IT OVER A DIFFERENT SOURCE THAN WE ASSUMED

> *"`available_actions` is three sensors in one, and it is the cheapest data in the game... **the
> pattern over time** — which conditions gate which, a **precondition structure**... A precondition
> lattice over ≤7 operators is the cheapest structural model in the whole problem, and it answers
> exactly the question — **what conditions are gated, and do they build on each other?**"*

**WE WERE GOING TO READ IT OFF FRAME-DIFF HISTORY. §16.1 READS IT OFF THE ADVERTISED ACTION SET** —
*at most seven booleans, no pixels involved.* **The cue topology is in the availability channel, not
in the board**, and that is a materially cheaper instrument for the same question.

## AND `instruments.Preconditions` IS IT, BUILT TO THE SPEC

    after: Counter          (b, a) -> n     `a became available after b`
    gone_after: Counter     (b, a) -> n     the inverse

**Fed every step from `_advertised`**, which re-reads the set and attributes the change to
`self._last_action` — *the action just taken is the only candidate for having met the condition.*
**And the docstring already carries the discipline: *a count is not a claim... reading it is the
agent's job rather than this table's.***

## THE FIVE SHAPES AGAINST WHAT EXISTS

| shape | status |
|---|---|
| **sequential** | **BUILT** — `Preconditions.after` is *b then a*, with counts, exactly §16.1's pairwise edges |
| **unlocking** | **BUILT, same table** — an action APPEARING is a condition met; `gone_after` is the inverse |
| **independent** | **A READING OVER THE BUILT TABLE** — an action whose predecessors are evenly spread has no precondition. **No new instrument** |
| **conditional** | **NOT BUILT.** `Affordances.bindings` is the nearest thing and its subject is COLOUR CONFLATION — *a key with two colours in it is a row carrying two things* — not *the same action gives a different cue depending on state* |
| **k-of-n** | **RULED OUT IN ADVANCE BY §16.1 ITSELF** |

**§16.1 ON k-OF-n, WRITTEN BEFORE THE QUESTION WAS ASKED:** *"The lattice is over subsets, so it is
**exponential in principle**; the useful version is **pairwise edges** — *a became available after b*
— with counts, not the full subset order. **Pairwise is 49 cells and it is enough to see a chain.**"*

> **SO THE SUBSET RECORD IS NOT A MISSING FEATURE TO FILE. IT IS A THING THE CORPUS DECLINED, WITH
> ITS REASON AND ITS SUBSTITUTE NAMED IN THE SAME SENTENCE.** *File it separately with what it needs*
> would have recorded as an open item something already closed against.

## THE ACTUAL GAP, AND IT IS NOT ANY OF THE FIVE

**`Preconditions.report()` HAS EXACTLY ONE READER IN THE REPO: `arc_check.py` 211, a conform seat
print.** It is **not in the holdout report.** So on every real run the table is fed at every step,
counts every edge, **and its output reaches nothing.**

**Same shape as `NOT_RESOLVED` before yesterday: a declared reading with no path.** Third instance of
that pattern this week — **and the pattern is now nameable: an instrument fed by the loop and read
only by a test is indistinguishable, from the outside, from one that does not exist.**

**THE CHEAPEST CONTACT-ADJACENT ITEM ON THE BOARD IS ONE LINE** — publish `pre.report()` beside
`affordance_kinds` — **and it is what makes the independence reading possible at all**, since a
reading over a table nobody prints is a reading nobody can take.

## AND `ONE` STAYS OUT, AS A GENERAL STATEMENT

> **THE CORPUS NAMING A THING IS NOT AN ENTRY CLAUSE.** The two clauses are *the loop cannot run
> without it* and *the agent minted a crude version and we are promoting it*. **`ONE` satisfies
> neither**, and Q21 listing four quantifiers is a description of a scheme rather than a licence to
> install its members.

**This matters beyond `ONE` because the corpus names a great deal** — nine sensors, seven
affordances, four quantifiers, seven operators. **Every one of those lists would otherwise read as a
build order**, and §12.3 says the opposite in its own words: *they are Tier 2 and the agent should
have to reach for them.*


---

# `[I]` THE VALIDATING CUE — AND THE STREAK BREAKS ON IT

**A cue that fires and, in firing, says the earlier steps counted.** Not *this happened* but ***that
stretch was a piece of the solution.*** **Retroactive validation: the confirmation arrives after the
work and is about the work, not about the moment.**

**Structurally unlike the other four.** Independent, sequential, unlocking and conditional are all
statements about **WHEN a cue fires.** This one is a statement about **WHAT AN EARLIER STRETCH WAS
WORTH** — same event, different subject. **And it is the only one that turns an ambiguous history
into a graded one**: before it every step reads *nothing happened*; after it, a specific run of steps
reads *those counted*.

**It is the wrist tilt in the only form an indifferent board can give.** The board cannot say
*warmer* about a plan it does not know — **but it can fire a cue whose precondition was a set of
prior actions.** *A warmer signal delivered late rather than continuously: no gradient, and a
checkpoint.*

**AND THE CORPUS HAS THE MECHANISM ONE LEVEL DOWN.** Q7: *a candidate becomes accepted once it
predicts transitions it was never fitted to.* **A term settles because something later confirms it.
Same structure at the cue layer — a stretch of actions settles because a later cue confirms it — and
the mechanism exists for TERMS with nothing applying it to ACTIONS.**

**And it makes the fifth reading cheap.** A validating cue **supplies the subset for free**: the
actions since the last one ARE the candidate set. **No combinatorics** — the same trick as
`settled_at`, where the boundary is recorded when it happens rather than reconstructed afterwards.

## THE CHECK: NEITHER CANDIDATE IS IT, AND SIXTEEN-FOR-SIXTEEN ENDS HERE

**`Chain.close(how)` is NOT it.** Its vocabulary is `win · death · reset · advance · cap · run_end` —
**episode endings, not cue firings** — and the two that DO validate a stretch, `win` and `advance`,
**are the gated ground signal we already have.** No new information.

**`Affordances.triggers_remote` is NOT it, and the reason is a finding.** It is declared in `SEVEN`
and **never written.** `note` is **contact-local by construction** — it `continue`s when an object
has no touching partner — **and a remote trigger has no touching partner at the remote end.**
`terminates` likewise. **Five of seven are set: `consumed`, `moves_when_touched`,
`changes_on_touch`, `blocks`, `passes`.**

> **SO `profile()` RETURNS `None` = UNREAD FOR TWO OF SEVEN, FOREVER, AND NOTHING SAYS SO.** The
> docstring defends `None` as *a different claim from False* — correctly — **but it cannot separate
> *not yet observed* from *no input path exists*.** `blocks`/`passes` abstain CONTINGENTLY, awaiting
> an avatar. `triggers_remote`/`terminates` abstain **STRUCTURALLY.** **That is `unreached` versus
> `unreachable`, the corpus's own pair, unapplied one layer down from where it was invented.**

**THIRD DECLARED-NODE-WITH-NO-PRODUCER TODAY** — `COUNT`, `ONE`, and now two of the seven. **And this
one has a cause the others lacked: the instrument's SCOPE is narrower than its VOCABULARY.**

**AND I CLAIMED THE CUE ALPHABET WAS BUILT. IT IS FIVE-SEVENTHS BUILT**, and the missing two are
exactly the ones this question needed. **Corrected here rather than carried.**

## BUILT: THE DENOMINATOR, WHICH IS WHAT MAKES `conditional` A READING

**`Preconditions` counted successes and nothing else.** `b -> a` seen four times is **four out of
four or four out of ninety**, and only the second is a condition. **A count with no denominator
cannot distinguish a rule from a coincidence, so every edge read as a rule and none could read as
gated.**

    taken: Counter          how often each action was taken -- EVERY step, not only changes
    sometimes: {edge: [n, taken[b]]}    0 < n < taken[b] -- fired some times and not others

**`conditional` is therefore not an instrument. It is the fifth topology as two counts**, and it
needed the denominator rather than a new sensor. **Published as counts, never a verdict** — the
table's own rule: *a count is not a claim.*

**AND FEEDING IT UNCONDITIONALLY EXPOSED A LATENT BUG.** `_advertised` read `self._last_action` at
the top of every step, and **the attribute was initialised only in `retarget`** — reachable before
its own initialisation, and masked because the early return meant the read was only ever hit after
the set had already changed. **Repaired at the constructor.** *A repair can break the layer above*,
and here the break was the useful part.

## AND THE ONE LINE

**`pre.report()` now rides in the holdout report beside `affordance_kinds`.** It had **one reader in
the repo — a conform print.** **An instrument fed by the loop and read only by a test is
indistinguishable, from outside, from one that does not exist.**

**MEASURED ON PUBLICATION:** **THE TABLE IS EMPTY ON BOTH GAMES, AND THAT IS THE POINT OF HAVING PUBLISHED IT.**

    ls20   taken {ACTION1: 31, ACTION2: 3, ACTION3: 3, ACTION4: 2}   -- 39 steps
    g50t   taken {ACTION1: 9, ACTION2: 17, ACTION3: 4, ACTION4: 3, ACTION5: 6}   -- 39 steps
    BOTH   came_after {}   gone_after {}   sometimes {}

**THE ADVERTISED ACTION SET NEVER CHANGED ONCE, IN 39 STEPS, ON EITHER GAME.** So §16.1's
precondition lattice -- *the cheapest structural model in the whole problem* -- **has no data at all
on the games we run**, and `_advertised`'s ledger row never fires either. **Sensor 1 and sensor 2 are
both silent on this panel.**

> **AND THE PANEL LAW APPLIES BEFORE THE NULL IS READ.** §16.1's premise is that availability *changes
> per frame because a condition is met or unmet*, and `arc_world.actors()` repeats it. **Measured:
> constant on both.** The premise is a property of the panel and **was never checked before an
> instrument was built on it.** Two games is a small panel and `sk48` is untested here -- §12.4's
> trigger fired 0/25 on `ls20` and 25/25 on `sk48`, **so per-game variation is exactly what to
> expect, and *the trigger cannot fire* is the over-claim to avoid.**

**WHAT THE ONE LINE BOUGHT IS THIS PARAGRAPH.** An instrument read only by a conform print would have
stayed empty indefinitely and looked built. **The `taken` column is the only thing with content, and
it is a reading about the DRIVE rather than the world** -- `ACTION1` 31 of 39 on `ls20` -- which is
not what the table was for and is worth knowing anyway.

## THE THIRD AUDIT QUESTION, AND IT WAS OVERDUE

**Not *what has no referent*. Not *what has no seat*. But *what is fed by the loop and read only by a
test*.** Three instances now — `NOT_RESOLVED`, `Preconditions.report()`, and the two unwritten
affordances are its inverse (**declared and never fed**). **Both halves are the same grep from
opposite ends: a producer with no consumer, and a consumer with no producer.**


## AND IT WAS RUN. SEVEN INSTRUMENTS, TWO HITS

| instrument | fed by the loop | read on a LIVE run | |
|---|---|---|---|
| `chain` | yes | `stalls`, `reuse_funnel` | ok -- and its own report says `close()` never fires |
| `rank` | yes | consumed as `gamma.unit_rank` | ok -- a POLICY, not a reading, correctly unreported |
| `phases` | yes | via `rep.phases` | ok |
| `clocks` | yes | via `rep.clocks` | ok |
| `pre` | yes | **now** in the holdout | fixed this turn |
| **`agency`** | **yes, every perceive** | **`arc_check` only** | **HIT** -- the shape exactly |
| **`term`** | **NEVER** | **`arc_check`, which feeds it itself** | **HIT, and worse** |

**`self.term` appears ONCE in `tether.py` -- the construction at line 229.** Never noted, never read.
**And `arc_check` 194 does `term = agent.term` then `term.offer(...)`: the seat reaches into the
agent, supplies the input the loop never supplies, and checks the output.** *A control that examines
nothing cannot demonstrate a clean state* -- **and a test that provides its own subject's input is
testing itself.**

> **THE DISTINCTION THE PASS TURNED ON IS *REPORTED* VERSUS *CONSUMED*.** `rank` is read by nothing
> and is not dead: `gamma.unit_rank = self.rank.key` makes it **a policy the loop runs on.** Four of
> seven would have read as dead on the grep alone. **The audit question needs its second half --
> *and is its output used for anything at all* -- or it manufactures five findings where there are
> two.**


---

# `[I]` FOUR CHECKS ON THE RELATION VOCABULARY, AND ONE OF THEM RETRACTS THIS WEEK'S NULLS

## 1 · RUN LENGTH IS RULED, AND WE HAVE BEEN RUNNING AT 4% OF IT

**`arc_holdout.play(game, cycles: int = 40)`.** Measured: `taken` sums to **39 steps** on `ls20` and
**39** on `g50t`.

**`ARC_AGENT` §22.1 RULES 1000 PER LEVEL, WITH PROVENANCE:** *humans complete a level in under 500
actions, typically ~100; this is the 2× honest ceiling* — filed as **anchored to a measurement of
the world the agent cannot move**, *specified mode, with provenance*. And `[I]` separately: *"under
500 moves per level to understand."*

> **`arc_run.PER_LEVEL = 500` is the accruing budget. `cycles=40` is the UNDECLARED cap that
> actually binds, and it is 25× tighter than the ruled one.**

**SO EVERY NULL READ THIS WEEK WAS TAKEN AT 4% OF THE RULED BUDGET** — the precondition table empty,
the objective degree `0.0` throughout, no level advanced, the extractor A/B byte-identical. **All at
39 steps.** *What if a game takes 300 moves* has never been tested because **nothing ran past 40.**

**WHAT THIS DOES AND DOES NOT RETRACT.** It does **not** touch the structural findings: typing
excludes extractors from the transition bargain at any run length, and `triggers_remote` is
unwritten at any budget. **It does retract the PANEL readings** — *a flat progress stream at 39
steps is not evidence that the stream is flat*, and I published it as one. **The single condition
under every measurement, never declared as a condition.** *Read the things that produce conditions
before the things that produce results*, and `play`'s own signature is the producer.

## 2 · `_overlap` IS NEITHER CELLS NOR BOXES — IT IS NORMALISED SHAPES

    def _overlap(a, b):  return P.overlap(P.shape_of(a), P.shape_of(b))

**`shape_of` normalises to the bounding-box origin, so this is intersection-over-union of two
FORMS.** It measures **congruence — are these the same shape — and carries no spatial information
whatever.**

**AND THE WORRY WAS RIGHT ABOUT THE VERSION IT IS NOT.** Over raw board cells, **solidity means two
distinct objects never share a cell, so cell-IoU between them is identically `0` on any frame.**
**Containment, intersection and coincidence therefore CANNOT reduce to cell-overlap on a solid
grid.** They need **bounding boxes**, which nothing computes.

> **SO IT IS A DIFFERENT SENSOR, NOT ONE LINE** — and publishing `_overlap` as built would deliver
> shape congruence under the name of spatial overlap.

**AND IT IS AN `A6i`.** `arc_percept.overlap` is IoU over **board cells across frames**, used by the
tracker for identity — correct. `sensors._overlap` is IoU over **normalised shapes in one frame** —
also correct, different subject. **One name, two quantities, and the relation vocabulary reduces a
dozen entries to the wrong one of them.**

**AND `_overlap` IS NEVER CALLED.** `SENSORS.read` appears once in the repo, for `components`.
**Fourth declared-with-no-consumer today.**

## 3 · FIGURE 11 DOES NOT SAY THE HABITAT BOUNDS THE VOCABULARY

**`DISCOVERY` C7 quotes Figure 11 as *an improvement that does not change contact changes nothing* —
an acceptance criterion about CAPABILITY.** §16 treats the habitat as a thing to **ENUMERATE** —
*what is this world made of, what are the levers.* **Neither says the medium bounds the atom set.**

**So it is a genuine extension, and the second check this week the corpus did not already answer.**
**Recorded as `[I]`, not derived here.**

## 4 · THE SPLIT HAS THREE CATEGORIES, NOT TWO — AND THE MIDDLE ONE IS OURS

**Filing the absent terms as *dropped by the medium* versus *a library gap* loses the category that
matters.**

    DROPPED BY THE MEDIUM     `occlude` -- no viewpoint, no depth. RELATIONS.md's own words:
    (correct, not ours)       *the one static relation a grid genuinely cannot express*

    FLATTENED BY OUR RULING   `spin` `interlock` symmetry similarity rotation rolling --
    (ours, and revisitable)   they need ORIENTATION, and 90° rotation SURVIVES the
                              compression fine. What flattened it is `shape` being a label:
                              *arbitrary, comparable, never orderable* -- the accounting's
                              ruling, not the grid's

    ABSENT FROM THE LIBRARY   `disjoint` `intersect` `adjacent` `align` `nest` `concentric`
    (the real gap)            `collinear` `perpendicular` `congruent` `offset` `tangent`

**The middle category is the finding.** *The compression is the filter* is right, **and it does not
cover these: we flattened them, the medium did not.** Which makes the shape ruling's cost countable
in a second place, and **the only one of the three that is a decision to revisit rather than a fact
to accept.**

**`perpendicular` sits across the line and shows why the split needs care** — dropped in its 3D
sense, **composable on a grid** (*one extends in row, the other in column*). **One word, two
relations**, and only one of them is gone.


---

# PRE-REGISTERED: THE RULED-BUDGET RE-RUN, WRITTEN BEFORE THE NUMBERS

**Launched `g50t` and `ls20` at `cycles=1000`, §22.1's ruled budget, against the `cycles=40` every
reading this week was taken at. THIS SECTION IS COMMITTED BEFORE EITHER RETURNS.**

## IT IS AN EXPERIMENT, NOT A REPEAT, AND THE REASON IS `[I]`'s

> *"You just happened to be testing on games with a board constraint on actions, like `ls20`. `g50t`
> doesn't have that, so it's a good test."*

**I have been treating two games as two samples of one thing, and they differ in the exact variable
the budget question is about.** On a board that caps actions **board-side**, 40 steps may be a real
fraction of what is available. **On an unconstrained one, 40 is nothing** — and its nulls are
**uninformative rather than merely under-powered.**

**Same 39 steps, two different meanings — and the empty precondition table is the clearest case.**
If `ls20` constrains actions board-side, **its action set not changing may be a fact about the
board.** On `g50t` the same emptiness is **an unfinished search.**

> **SO `g50t` IS THE TEST AND `ls20` IS THE CONTROL.** If `ls20` barely moves at 25× the steps while
> `g50t` moves, **that separates *the board is constrained* from *we did not look long enough* in one
> comparison, which neither run alone can do.**

**AND IT IS THE SHARPEST CASE YET FOR *PER GAME, NEVER POOLED*.** *Pooling a constrained board with
an unconstrained one averages two different worlds* — **and every reading this week did exactly
that**, including the ones I wrote the pooling rule beside.

## THE PINNED EXPECTATIONS, AND BOTH BRANCHES ARE INFORMATIVE

| expected | if it goes the other way |
|---|---|
| **`g50t`'s nulls move** — precondition edges appear, degree leaves `0.0`, or a level advances | **they do not: 1000 is still too few, and the finding is about the SEARCH rather than the budget** |
| **`ls20`'s mostly hold** | **they move too: the constraint is not what it is thought to be, and the asymmetry was mine** |

**NEITHER OUTCOME IS THE HEADLINE.** *A null carrying a satisfying causal story is harder to doubt
than a bare one* — and **"the board constrains actions" is exactly such a story**, so it is the one
to distrust rather than the number.

## WHAT IS BEING READ, DECLARED IN ADVANCE

    preconditions   taken / came_after / gone_after / sometimes
    levels          the `advanced` flag -- the trigger five parked items wait on
    residual        outstanding, pe_integral
    library         size, mints
    endings         death / cap / reset counts, and `blind`

**AND WHAT THE RE-RUN CANNOT SETTLE, STATED NOW SO IT IS NOT CLAIMED LATER.** It cannot move the
structural findings: **typing excludes extractors from the transition bargain at any run length, and
`triggers_remote` is unwritten at any budget.** *That split is what makes the retraction survivable
rather than total*, and it is also the limit on what a longer run can buy.


---

# `[I]` RANDOM WALK IS AN ATOM — AND THE CORPUS HAS THE ARGUMENT WITH A MEASUREMENT

**Committed while both ruled-budget runs are still going, so the sharpened prediction below is
pinned rather than fitted.**

**The claim: for large or infinite action games, random walk is a real atom and a real strategy when
paired with cue detection.** *Actors must be created with random walk natively. **Entropy always
was.*** **Alone it is motion; paired with a detector every step is a sample of the relation space**
— and it is **optimal under a stated condition: when the target configuration is invisible to you.**
You cannot aim at what you cannot perceive. **It stops being best the moment the relation becomes
readable.**

> **WHICH REFRAMES THE WANDERING AS CORRECT RATHER THAN BROKEN.** What is missing is not direction.
> **It is the detector that would make the walk pay**, and `touching` alone catches almost nothing.

## CHECK 1 · Q20 HAS THE ARGUMENT, AND WITH BETTER EVIDENCE THAN THE CLAIM CARRIED

> *"Uniform noise visits **884 distinct frames** on one game while the agent orbits **51 distinct
> frames in 2,050 steps** on another. **You cannot compress what you never observed.**"*

**That is random walk as a SUPERIOR SAMPLER, measured, 17× on distinct frames.** And beside it the
self-criticism: *eight builds attacked the third factor for eight +0s while the FIRST factor was
never touched — if `|R| ≈ 0` then no φ can mint, whatever atoms exist.*

**BUT Q20 RULES THE *TRIGGERED* PROBE** — *the trigger is the agent's own prediction error and may
be nothing else, never a score, never a step count.* **That is a conditional intervention, not a
standing policy.**

**AND THE STANDING POLICY ALREADY EXISTS, SEPARATELY, AS `draw`.** `tether` 959 and 997 call **the
identical `self.drive.choose(self.actions, self.cycle, _where(before))`** and differ only in the
label returned — `"probe"` against `"draw"`.

> **ONE MECHANISM, TWO LABELS — AND THE LABEL IS WHY I READ IT AS A FAILURE STATE.** `draw` reads as
> *nothing decided*; the truth is *the policy ran*. **So the STATUS is already the code's behaviour
> and is unnamed**, which is the fourth form once more: not the corpus ahead or behind, but **a
> correct mechanism carrying a name that misreports it.**

**Same shape as `DIRECTED`'s `A6i` (`by == "discriminate"` against *bets with bound terms*), and it
is the same field.** `by` now carries three values whose names imply a quality ordering the
mechanism does not have.

## CHECK 2 · ADMISSION BY DERIVATION IS ALREADY THE RULE — SEVENTEEN FOR SEVENTEEN

**`bench pulls per primitive` is the MVS's specified instrument and it is a MEASUREMENT of what the
agent needed.** But it is not the admission test.

**§11's entry clause 1 is *the loop cannot run without it*** — **a derivation from the loop's
structure, not a pull count** — and **§12.3's nine sensors were admitted by exactly that**:
*Criterion unchanged: the loop cannot run without it.*

> **SO RANDOM WALK NEEDS NO NEW RULE AND PASSES THE EXISTING ONE OUTRIGHT: without an action
> selector the loop cannot take a step.** `Drive.choose` on the `draw` branch **is** that selector.
> **`bench pulls` measures need after the fact; the entry rule admits before.** Two instruments,
> two moments, and I had been treating the measurement as the gate.

## AND THE PRE-REGISTRATION SHARPENS AND SPLITS — PINNED BEFORE THE RUNS RETURN

**At 1000 steps on `g50t`, the walk will have had 25× the samples it had at 40.**

    SOMETHING FIRES   random walk plus one published relation was enough, and the budget
                      was the binding constraint
    NOTHING FIRES     evidence about the DETECTOR rather than the budget -- because the
                      sampling cannot be what was short

**Two things tested at once and separable**, which the original two-row registration did not
distinguish. **And it answers the standing worry about registrations whose branches do not exhaust
the space: this one adds a row rather than reinterpreting the existing two.**


---

# CORRECTION: RANDOM WALK IS ONE THING, NOT A PAIRING — AND TWO CHECKS, ONE OF WHICH NARROWS YESTERDAY

**`[I]`: *the cues, rigid-body and geometry sensors are why random walk isn't random.***

**I wrote *random walk paired with cue detection* — two things, one of which could be built first.
IT IS ONE THING.** The walk is **random in the ACTION channel and structured in the READING.** Every
step is a sample, **and the detector is what makes it a sample rather than a step.**

> **A walk with no reading accumulates nothing.** Motion without observation. **A walk with relation
> detectors is systematic sampling of the configuration space** — undirected in *where it goes*,
> exhaustive in *what it notices when it arrives.*

**AND THE FRAMING MATTERS FOR WHAT GETS BUILT.** *Pair X with Y* **invites building one and
deferring the other, and the deferred half is the one that does the work.** The walk exists. **The
reading is what is missing** — and the detectors are **not an optimisation on a baseline strategy,
they are half of the strategy.**

**WHICH MAKES THE MISSING HALF COUNTABLE, AND THE OLD FRAMING COULD NOT.** *Thirty composable
relations, one published* — **the reading is roughly a thirtieth built.** First time the walk's
weakness has been a number rather than a description.

## TWO SUPPORTS HELD LOOSER THAN OFFERED, AND ONE IS DROPPED

***Entropy always was*** — there is no state of a system in which undirected movement is unavailable
— **is exactly the property an irreducible needs, and it carries the claim alone.**

***Computational randomness is a very lossy compression* PREDICTS NOTHING I CAN CHECK.** A PRNG is
deterministic and looks random. **Keep the claim, drop that support** — *that is what two rows were
cut from Figure 12 for*, and the same test applies to a support as to a bond.

## CHECK 1 · `probe.py`'s DOCSTRING CARRIES BOTH ENDS ALREADY

    UNINFORMED BY CONSTRUCTION ... The draw sees the advertised action set and nothing else
    Its outcome re-enters as an ordinary observation and is judged under the unchanged bargain

**The first sentence is how the draw is MADE. The second is what the draw YIELDS.** So it is *the
same sentence read at the other end*, and **the docstring frames the structure as a SAFETY property
where the new reading frames it as a STRATEGY.** Same mechanism, and *you cannot compress what you
never observed* is already in the file.

**Eighteen.**

## CHECK 2 · THE CORPUS DOES PRICE A SEARCH BY ITS READING — AND IT NARROWS YESTERDAY'S RECORD

**Q24, via `ARC_BUILD_PLAN`:** *"If `R` is not falling: either Γ's variety is below the
environment's — **mint** — or the disturbance variety was **never observed** — **probe**. It
reframes MINT as **variety acquisition**, which gives `closure(Γ)` **a lower bound the environment
imposes rather than one the designer picks.**"*

**That is a policy priced by what it OBSERVED, and it is Ashby's requisite variety.** Built
instrument on the same side: **`Drive.tried` is `action -> distinct states it was drawn from`** —
*how many distinct states each action was drawn from*, a reading-side count, **not an action-side
one.**

> **AND IT NARROWS WHAT I RECORDED YESTERDAY.** I wrote that *the habitat bounds the vocabulary* is a
> genuine extension because Figure 11 speaks only of capability. **Against Figure 11 that stands.
> Against Q24 it does not: *a bound the environment imposes rather than one the designer picks* is
> the same principle, already written.** What is new is the **DIRECTION** — **Q24 bounds `closure(Γ)`
> from BELOW by disturbance variety; the habitat claim bounds it from ABOVE by what the medium
> admits.** **Two bounds, one source, and only the floor was written down.**

**Nineteen, and the correction is the more useful half:** *checked against Figure 11* is not
*checked against the corpus*, **and naming the figure I checked is what let the miss be found the
same day.**

**AND THE CORPUS FLAGS ITS OWN AS UNBUILT:** *Ashby's inequality is the principled version and
nothing computes it* — `Config.max_depth = 3` is anchored to the toy world's chunking falsifier,
**a different quantity.** So the floor is specified and uncomputed, **and the ceiling is now
specified and uncomputed beside it.**

## AND THE RE-RUN'S THIRD ROW GAINS ITS REASON

**Registered before the runs: *if nothing fires at 1000, that is evidence about the detector rather
than the budget.*** **It now has a reason rather than a hunch: ONE published relation is the reading
almost entirely absent**, so the expected outcome is that the budget moves **the counts** and not
**the kind of thing the agent notices** — *which the precondition table and the affordance profile
would show separately.*


---

# THE RULED-BUDGET RE-RUN: BOTH GAMES LOCK ONTO ONE ACTION, AND THE AGENT IS NOT WANDERING

**1000 cycles each, §22.1's ruled budget. `g50t` 34 minutes, `ls20` 86.** Read against the three
rows pinned before either returned.

    game   taken                                          came_after  advanced  outstanding   library
    g50t   A1 881  A2 94  A3 4  A4 8  A5 11   (88.3%)     {}          false     971 -> 2834   45 -> 127
    ls20   A2 954  A1 34  A3 6  A4 4          (95.6%)     {}          false     741 -> 2680   67 -> 105

**Both: one death, `blind` true at the last frame, one unobserved step, `sometimes` empty.**

## ROW 2 FIRES, AND IT WAS `[I]`'s: THE ASYMMETRY WAS MINE

**Registered:** *`ls20`'s readings mostly hold* — **or** *they move too: the constraint is not what
it is thought to be, and the asymmetry was mine.*

> **THEY MOVED, AND THEY MOVED THE SAME WAY.** The two games are structurally identical in every
> reading taken: **lock onto one action, empty precondition table, no level advance, outstanding
> near 2700–2800, one death.** ***`ls20` has a board constraint on actions and `g50t` does not*** **is
> not distinguishable in any of this** — and the hypothesis was mine to test, not to confirm.

**The between-game difference the experiment was built to find is invisible, because a THIRD factor
dominates both boards.**

## THE THIRD FACTOR, AND IT INVERTS A WEEK OF READING

**`Drive.choose` is a uniform round-robin**: `sorted(actions)[(cycle * 7 + seed) % len(actions)]`.
**Stride 7 against 4 or 5 actions is coprime to both, so it cycles every action evenly.** It cannot
produce 954 of 998, or 881.

> **SO THE AGENT IS NOT RANDOM-WALKING. IT LOCKS ON — 96% ONE ACTION ON `ls20`, 88% ON `g50t`.** I
> have spent the week calling it a wanderer and reasoning from that. **It is the opposite failure.**

**AND THE MECHANISM IS A GREEDY ARGMAX WITH NO TIE-BREAK AND NO EXPLORATION TERM.** Two branches
select without the draw — `max(self.actions, key=lambda a: spread[a])` returning `discriminate`, and
`_learned_split()` returning `discriminate:learned`. **`max` over a fixed-order tuple resolves every
tie to the same element**, so a stable spread returns the same action indefinitely.

**WHICH OF THE TWO, I CANNOT SAY.** The `by` field distinguishes them, the ledger wrote it on every
row, **and my script did not print it.** *That is a gap in the measurement, not a finding* — and the
confirmation is one counter over rows already on disk.

## WHAT THIS DOES TO THE EMPTY PRECONDITION TABLE: CONFOUNDED, NOT EXPLAINED

**`came_after` empty over 998 transitions is a real null and it is not the null I registered.** With
one action taken 90%+ of the time, *the advertised set never changed* **is a statement about a very
narrow slice of the state space** — `ACTION3` was taken **four times in a thousand steps** on
`g50t` and **six** on `ls20`.

**So *the board's action set is constant* is NOT established.** What is established: **it is constant
over the states this policy reaches, and this policy reaches almost none of them.**

## AND MY THIRD ROW'S PREMISE WAS WRONG TWICE OVER

**Registered:** *if nothing fires, that is evidence about the DETECTOR rather than the budget,
because the sampling cannot be what was short.*

**The sampling WAS what was short.** Not in step count — **in variety.** The walk was not running,
so 25× the steps bought 25× more of the same action. **Q20's 884-versus-51 reproduced in our own
numbers from the other side: uniform noise would have spread over four or five actions; the agent
spread over one.**

> **AND THIS IS WHY THE RANDOM-WALK CORRECTION MATTERED AND WAS STILL NOT ENOUGH.** *It is one thing,
> not a pairing* fixed the framing. **It did not check whether the walk was the policy in force —
> and it was not, on either board.** *Read the mechanism before pinning the registration* was applied
> to `play`'s signature and not to the branch that chooses the action.

## WHAT DID MOVE, AND IT IS NOT NOTHING

**`outstanding` 2.9× and 3.6×, `pe` 3.4× and 2.9×, `library` 2.8× and 1.6×, 104 and 74 mints.**
**The loop does far more work at budget and still advances no level and still reads degree `0.0`.**
So the budget was binding on the WORK and not on the OUTCOME — **which is a third thing neither row
predicted, and the honest form of *what the re-run bought*.**


---

# `RECURSIVE_TRANSFORMATION` READ — AND IT NAMES OUR STATE AS ONE OF ITS OWN FALSIFIERS

**Corpus, read and not edited.** Offered as *a proposed organizing principle, not a law*, and its own
Part 6 calls the exercise **a coherence result, not a discovery.** Recorded at that standing.

    relations → fields → gradients → flows → networks → new relations and fields

## THE FALSIFIER IT LISTS IS OUR MEASURED CONDITION

**Part 6, on what would break the cycle:** ***a flow that reshapes nothing, so the last step never
feeds the first — which would make the sequence a chain rather than a cycle.***

> **THAT IS THE AGENT AT THE RULED BUDGET.** It acts, and **what it can perceive afterwards is
> identical to what it could perceive before** — one relation of roughly seventy. **The last step
> does not feed the first, so there is no second turn.**

## WHICH RESTATES THE COMPOSITION PROBLEM AND SAYS WHAT TO BUILD

**The agent is stuck at the FIRST term.** One relation published means **almost no field**; no field
means **no variation to take a gradient over**; and *a gradient is a difference capable of driving
directed change — it makes energy available for work rather than merely present.*

**AND THE DOC NAMES THE MEASUREMENT EXACTLY:** *a system at equilibrium may contain abundant energy
while exhibiting no net macroscopic change.* **At 1000 cycles: `outstanding` 2834, library 127, 104
mints — abundant activity — with `advanced: false` and degree `0.0`.** **Energy without a gradient.**

> **SO *THE BOARD GIVES NO WARMER SIGNAL* WAS THE WRONG DIAGNOSIS.** *There is no gradient because
> there is no field because there is one relation* is the right one. **Same fact, and only the second
> form says what to build.**

## AND IT RULES ON THE SHAPE QUESTION INDEPENDENTLY

> ***Discrete symmetry — reflection, rotation by a right angle, permutation — requires no smoothness
> at all. It holds on a grid, on a graph, on any set with structure. Available at every level.***

**So 90° symmetry is exactly the kind a grid admits**, and the six relations blocked by *`shape` is a
label* are **flattened by our accounting rather than by the medium.** **Third independent
confirmation of the three-category split**, and it arrives from physics rather than from the
relation vocabulary.

## THREE PLACES IT AGREES WITH WHAT WE ALREADY HOLD, ARRIVED AT SEPARATELY

| the doc | ours |
|---|---|
| *a structure that persists becomes an entity, and an entity has states* | `THE_FORMULA`: **a settled molecule becomes an atom for whatever composes over it** |
| *the swap upward requires the arrangement to STABILISE — a structure that does not persist never becomes an entity, and the ladder stops there* | **a frame that cannot settle has one level, however large its library** — and this is the **third** independent statement of it |
| *going up, the arrangement's internal detail is discarded and only what became a state survives* | Figure 4's membrane, and `R_T` as *the honest report of what the coarser description cannot hold* |

**A LEVEL IS WHERE STRUCTURE STABILISED**, and *the number of levels is a fact about the world rather
than a choice of description.* **Which is why our composite system having one level is a reading
about the world-and-agent and not a parameter.**

## AND THE NOISE ROW BEARS ON THE RANDOM-WALK RULING

**The three-way split on apparent randomness** puts **statistical noise** as *the detail a
coarse-graining discarded, reappearing as variance above* — **derived, and the companion of
smoothness.** So an undirected draw is **not the absence of information: it is the level below
showing through.** *Which is a better support for the random-walk claim than the one dropped* — and
unlike *computational randomness is a very lossy compression*, **it names what the variance is a
compression OF.**

---

# CORRECTION: THE ROWS ARE NOT ON DISK

**I said twice that the `by` counter was *one counter over rows already on disk*. `arc_holdout` uses
`ledger.Ledger()` with no path, so rows live in memory and the run discarded them.** **`by` IS
written — `tether` 1699, on every ACT row — and nothing read it**, which is the third audit's shape
again.

**Published as a report field and re-measured at 150 cycles**, since the lock-on is visible by step
40. **The claim was wrong in the cheap direction — it made the check sound free when it costs a
short run — and it is the same error as *one line* for `overlap`.**


---

# `[I]` STATES AND STRUCTURES ARE A PAIR — AND THE PAIRING CLAIM FINDS A DEFECT IN THE SUMMARY TABLE

**The claim, sharper than the document's:** they are pairwise the way a function and its domain are.
**A state with no structure has no magnitude** — three of what, ordered how, varying across what?
**A structure with no state is empty** — a network with nothing at the nodes, a gradient in no
quantity. ***Neither exists without the other***, which is definitional rather than behavioural, and
**stronger than *lockstep*.**

**AND IT CORRECTS THE DOCUMENT'S STATEMENT OF THE SWAP.** *Structure becomes state at the next level*
is close and slightly wrong. **A state-structure PAIR, once it stabilises, becomes the STATE HALF of
a new pair**, and something else supplies the structure at that level. Molecules with their collision
network become a fluid; **the fluid is a state and the flow field is its new structural partner.**
**Which is why levels come in units: a level is a complete PAIR, not a lone quantity.**

## CHECK 1 · THE ASYMMETRY HAS A REASON, AND THE CODE CARRIES IT

**The worry: *mutually necessary, asymmetrically recursive* reads as a contradiction until said in
one breath.**

**AND THE DOCUMENT ALLOWS BOTH DIRECTIONS, WHICH DISSOLVES HALF OF IT:** *the same holds downward —
every entity, examined finely enough, is an arrangement of smaller ones.* **So the DIRECTION is not
asymmetric.** What is asymmetric is **the MECHANISM: the swap upward is driven by PERSISTENCE, and
the swap downward by DECOMPOSITION.** Two different operations, and the document names both
conditions.

> **AND PERSISTENCE IS ONLY INFORMATIVE ABOUT AN ARRANGEMENT.** A structure that persists gains an
> identity — there is something being held together. **A state that persists is the same state.**
> Nothing is added, because there are no parts whose continued relation could be the news.

**THE CODE IS THE SAME ASYMMETRY WITH THE SAME REASON.** `gamma.units()` is *the atoms, plus every
SETTLED term as one unit* — **an atom is a unit by construction; a term becomes one by settling.**
**Nothing promotes an atom, because an atom has nothing to settle.** So *structure becomes state by
persisting, and a state does not* is **already instantiated**, and the reason is that settling is a
predicate over compositions.

## CHECK 2 · THE PAIRING HOLDS IN ALL FOUR DERIVATIONS — AND TWO ROWS OF THE TABLE ARE INCOMPLETE

**The worry was the zeroth law: `SPECTRUM` and `NETWORK`, both STRUCTURAL, which under the pairing
should be impossible.**

**IT HOLDS, AND THE PROSE SUPPLIES WHAT THE TABLE OMITS.** *A spectrum makes **thermal state** a
single ordered range... a network makes *in thermal contact with* a relation between **systems**.*
**Thermal state is the state; systems are what the network relates.** The structures are what does
the work; **the states are the operands, present and unlisted.**

> **AND THE SAME DEFECT RUNS THE OTHER WAY, WHICH IS THE FINDING.** The **first law's** row is
> `space, time` — **both STATES** — and its structural half is in the *additionally needs* column as
> **homogeneity, a symmetry.** **So two of four rows draw from one column only, in opposite
> directions, and in both cases the missing half is in the prose.**

    zeroth   spectrum, network          BOTH STRUCTURES   -- state (thermal state) in the prose
    first    space, time                BOTH STATES       -- structure (homogeneity) in the next column
    second   network, gradient, space, energy             -- both columns, complete
    third    time, gradient                               -- both columns, complete

**THE PAIRING CLAIM IS CONFIRMED AND THE TABLE IS WHAT IS WRONG.** *Derives from* lists the operative
members rather than the complete ingredients, **and a reader taking the table as the derivation gets
a law that stands on one column.** **Corpus — recorded here, not fixed.**

**AND IT IS THE CLAIM EARNING ITS KEEP ON FIRST USE:** it was offered as a sharpening and it
**found something**, which is more than a restatement does.

## AND THE FRAMEWORK'S OWN VERSION IS ALREADY LOAD-BEARING

**A slot with no type has no alphabet, so no residual can be priced. A type with no slot holds
nothing.** *The loop treats them as one thing* — and `slot_types` being **the domain's declaration
rather than the loop's derivation** is that pairing enforced at the boundary.

**And `space_exact` counts ARRANGEMENTS rather than sets** because a term is atoms **and** their
arrangement. **Figure 12's *the arrangement is the substance* is this claim at the composition
layer** — and *a vocabulary holding only ingredients can name a state and not a route to one* is the
pairing stated as a failure mode.


---

# A VALUE THAT EXISTS IS NOT A VALUE THAT CROSSES — TWO INCIDENTS, ONE TENDENCY

**Twice this week I called a build a publish, and the error is one thing.**

**`_overlap`** — proposed as *one line* to unlock containment, intersection and coincidence. It is
IoU over **normalised shapes**: congruence, no position. **The value existed and was not the value
wanted.**

**`by`** — said twice to be *one counter over rows already on disk*. `arc_holdout` uses
`ledger.Ledger()` with **no path**, so the rows were in memory and the run discarded them. **The
value existed and could not cross.**

> **THE CHECK IS TWO QUESTIONS AND I SKIPPED A DIFFERENT ONE EACH TIME:** *is this the value I want*,
> and *can anything read it*.

**AND IT IS THE THIRD AUDIT QUESTION FROM THE OTHER SIDE.** *An instrument fed by the loop and read
only by a test is indistinguishable, from outside, from one that does not exist.* **The tendency and
the audit are the same fact — one is the error, the other is its detection** — which is why one entry
beats two incidents: **the audit already existed and I was not running it on my own proposals.**

**THE DIRECTION IS THE TELL.** Both mistakes made the work sound **smaller** than it was, **which is
the direction that gets an item scheduled rather than examined.** A publish and a build differ by an
order of magnitude, so mis-sorting one **mis-orders the whole board** — and both times the mis-sorted
item went to the top of it.


---

# PRE-REGISTERED: HOW THE `by` SPLIT READS, PINNED BEFORE IT RETURNS

**Four outcomes, and the fourth is the one that says my inference was wrong.**

    discriminate dominates          the greedy argmax over `spread` is the lock. `max` over a
                                    fixed-order tuple resolves every tie to the same element,
                                    and there is no exploration term. FIX IS IN THAT BRANCH

    discriminate:learned dominates  `_learned_split()` returns a stable action and the loop
                                    takes it. Different branch, same shape, and the fix is
                                    there instead

    draw / probe dominate           MY INFERENCE WAS WRONG. `Drive.choose` is provably uniform,
                                    so a skew of 954-in-998 through it would mean the skew is
                                    not where I placed it -- `self.actions` order, or
                                    `_last_action` not being the action I think it records

    no branch dominates             the lock-on is EMERGENT rather than from one site, which
                                    is the worst case: no single fix, and the four-way split
                                    would be the finding rather than a pointer

**THE FOURTH ROW EXISTS BECAUSE FIVE REGISTRATIONS THIS SESSION FAILED TO EXHAUST THE SPACE**, and
every one of those failed by having only the outcomes I expected. **A row for *the mechanism is not
where I said* is the one that has been missing.**

**AND WHAT THE SPLIT CANNOT SHOW:** *why* the argmax stays put. **A dominant branch names the site;
it does not say whether `spread` is genuinely flat-topped, whether ties are being broken by tuple
order, or whether one action really does dominate the divergence.** Those are three different repairs
and the counter separates none of them.


---

# TWO GENERAL FORMS, FROM THE `by` WAIT

**`[I]`: A REGISTRATION WITH ONLY EXPECTED OUTCOMES IS A PREDICTION WEARING A TEST'S CLOTHES.**
Five this session failed that way, **and the repair is a ROW rather than better foresight** — *the
space I did not enumerate* is exactly what enumeration cannot reach. **The standing row is *the
mechanism is not where I said*.** It costs one line and catches the class.

**And pin what the reading CANNOT show in the same breath.** A dominant branch **names the site and
not the cause**; stating the ceiling before the result arrives is what stops a reading overrunning
its instrument.

**`[I]`: THE AUDIT NEEDS A SECOND SUBJECT RATHER THAN A SECOND QUESTION.** *Fed by the loop and read
only by a test* was framed outward, at the codebase, **and never framed as a question about a
PROPOSAL.** **Read-past is a memory failure; authored-and-not-turned-around is a SCOPE failure** —
and the worse kind, because **the author has no reason to doubt a check they just wrote.** *Run it on
the codebase, and run it on anything about to be added to it.*

**AND THE BIAS IS NOT IN THE ESTIMATE, IT IS IN WHAT THE ESTIMATE EXEMPTS YOU FROM.** *Harder than it
looked* draws scrutiny; *one line* gets queued. **So a cheap-sounding estimate is self-protecting: it
produces the conditions that hide it** — which is why both mis-sorted items went to the top of the
board rather than into a queue where they would have been examined.


---

# PINNED: THE THREE REPAIRS `by` CANNOT SEPARATE, AND THE MEASUREMENT THAT CAN

**Registered before the split returns, because a dominant branch names the site and not the cause.**

| cause | symptom | repair |
|---|---|---|
| **flat-topped `spread`** | the values are genuinely tied and `max` picks first | **a tie-break — and the question becomes WHAT breaks it** |
| **tuple order resolving ties** | same symptom, different cause: **equal-scoring actions always resolve the same way** because the ordering is stable and arbitrary | **shuffle the candidate order, or make the tie-break explicit** |
| **one action genuinely dominating** | the spread is real and one action IS the best discriminator every step | **none on the selector. The finding would be about the BOARD** |

> **THE FIRST TWO PRODUCE THE SAME `by` COUNTS AND THE SAME `taken` COUNTS.** They differ only in
> whether `spread`'s values are equal *at the top* or equal *everywhere*, **which neither counter
> records.** And the third needs no repair at all — **so one third of the outcome space is *do
> nothing*, and the counter cannot reach it.**

## THE DISCRIMINATOR IS `spread` ITSELF, AND IT IS A BUILD

**`[I]`: print the values rather than the argmax.** *Flat* means all equal. *Tied-at-top* means
several equal and one chosen. *Dominant* means one clearly higher. **One reading separates all three.**

**AND THE AUDIT, TURNED ON THIS PROPOSAL RATHER THAN ON THE CODEBASE — WHICH IS THE SECOND SUBJECT,
APPLIED:**

- **Is it the value I want?** **Yes.** `spread` is the argmax's own input, so it is the quantity the
  three causes disagree about.
- **Can anything read it?** **NO.** `spread` is a local in the discriminate branch, written and
  discarded every step. **No ledger field, no report entry.**

> **SO IT IS A SMALL BUILD AND A SECOND RUN, NOT A FREE READ OFF THE ONE IN FLIGHT.** Said now
> rather than after — *a cheap-sounding estimate is self-protecting*, and this is the third time this
> week the same proposal shape has come up. **The run currently going cannot answer it.**


---

# BUILT: THE TIED-AT-TOP READING — AND TWO OF THE THREE CAUSES COLLAPSE INTO ONE

**Reading the branch before building the measurement changed what the measurement is.**

    if spread and max(spread.values()) > min(spread.values()):
        pick = max(self.actions, key=lambda a: spread[a])

**THE GUARD IS `max > min`, SO AN ALL-FLAT SPREAD NEVER REACHES THE ARGMAX.** It fails the guard and
**falls through to the uniform draw.** *Flat-topped spread* as a cause of the lock-on **cannot
happen** — the branch does not fire at all in that case.

> **SO THE FIRST TWO CAUSES ARE NOT TWO.** *Values tied and `max` picks first* and *tuple order
> resolving ties* are **one mechanism with two necessary conditions**: a tie AT THE TOP, and a stable
> arbitrary ordering. **Neither alone produces it, and describing them as alternatives implies a
> choice of repair that does not exist.**

**WHICH LEAVES TWO OUTCOMES, NOT THREE:**

    tied_at_max >= 2   several actions scored equal-highest and `self.actions` order chose.
                       ARBITRARY AND STABLE -> a tie-break is the repair
    tied_at_max == 1   one action scored highest alone, every time. The selector is doing
                       what it says -> NO REPAIR, and the finding is about the board

**And the *do nothing* outcome survives the collapse**, which is the row worth keeping explicit.

## THE READING

**`Agent.ties()`** — `{tied_at_max: n}` per discriminate call, published in the holdout report beside
`preconditions`. **`1` is genuine dominance; any mass at `>= 2` is tuple order deciding.**

**It is the argmax's own input, one aggregate over it, and it separates the two remaining causes in a
single number.** The `by` counter names the branch; **this says whether that branch had a choice.**

**NOT RUN IN PARALLEL.** The `by` measurement is compute-bound at 35 minutes and a second heavy run
would halve both. **And the `ties` run supersedes it** — the report carries `by` too — so the next
run answers both questions and this one is the last that will not.


---

# THE COST IS FRONT-LOADED, AND EVERY RUN-LENGTH ESTIMATE THIS WEEK ASSUMED IT WAS NOT

**`ls20` at 150 cycles ran 47 minutes and did not finish. `ls20` at 1000 cycles took 86.** So
**15% of the cycles cost more than half the time**, and short runs are not cheap fractions of long
ones.

**THE MECHANISM IS IN THE BRANCH.** `owed` is largest **before any term binds**, and the discriminate
branch loops **`actions × owed × cands`** every step. **The early cycles do the most work**, and they
are exactly the ones a short run consists of.

> **FOURTH INSTANCE OF THE CHEAP-DIRECTION BIAS, AND THE FIRST ABOUT MEASUREMENT RATHER THAN BUILD
> COST.** `_overlap` and `by` were builds mis-sorted as publishes. **This is an INSTRUMENT mis-sized**
> — and the same direction, which is what makes it the same tendency rather than a new one.

**AND IT RETROSPECTIVELY EXPLAINS A SCHEDULING CHOICE.** *Run at 40 cycles* looked like prudence and
was **near the expensive end of the curve** — so the cheap-looking runs this week were not
proportionally cheap, and the 25× budget increase cost far less than 25×.

## THE RUNS ARE LOCAL, WITH ONE OUTBOUND REQUEST AT SETUP

**`arc_holdout`'s own docstring:** *One game, played **LOCALLY**. `arc_agi`'s `NORMAL` mode
**downloads once** and hands back a `LocalEnvironmentWrapper` ... an anonymous key is fetched
automatically.* **And `NOT RUN BY conform/check.py` — it needs the network, and the checkers must
stay offline and deterministic.**

**Checked: no `requests`/`httpx`/`urllib`/`http` anywhere in the repo's own files or in
`arcengine`.** So **play is compute, not network** — consistent with 34.3 CPU minutes against 34.9
wall — **and the front-loaded cost is a property of the loop rather than of a connection.**

**The caveat worth stating: it is not air-gapped.** `arc.make` makes one outbound request, so **a run
without egress fails at SETUP rather than degrading** — the right failure mode, and the reason the
eight seats are deliberately excluded from that path.


---

# THE FRONT-LOADING CHECK IS PER GAME, NOT A RATIO — PINNED BEFORE THE RUNS LAND

**Proposed: *if the cost is front-loaded, `g50t`'s 2.5× advantage at 1000 should shrink at 150 — and
if the gap holds, the cost is not front-loaded.*** **THAT IS NOT WHAT THE RATIO TESTS.**

**Front-loading is a WITHIN-GAME claim** — early cycles cost more than late ones. **If both boards
are front-loaded to the same degree, the ratio between them is unchanged**, because it divides out.
**So a gap holding at 2.5× falsifies nothing.**

**AND THE BETWEEN-GAME GAP HAS A DIFFERENT DRIVER, WHICH THE 1000-CYCLE NUMBERS ALREADY SHOW:**

    g50t   5 actions   library 127   104 mints   12 slots used   2024s
    ls20   4 actions   library 105    74 mints   22 slots used   5147s

**`g50t` has MORE actions, MORE library and MORE mints, and runs 2.5× FASTER.** So the driver is
**neither cycles nor library size** — and the one column that moves the right way is **slots**, which
sets `owed`, which the discriminate branch loops over. *Roughly 2× the slots, roughly 2.5× the time.*

## THE CORRECT TEST, AND ONE HALF IS ALREADY IN

> **PER GAME: compare `time(150)` against `0.15 × time(1000)`.** Much greater means front-loaded.

    ls20   0.15 x 5147s = 772s ~ 13 min predicted.  MEASURED: >47 min and did not finish.
           ** FRONT-LOADED, and by more than 3.6x on a lower bound **
    g50t   0.15 x 2024s = 304s ~ 5 min predicted.   pending

**So the claim already has one confirmation and the pending run is the second**, and neither depends
on the ratio.

**AND THE RATIO IS STILL WORTH READING — for the OTHER question.** If `slots` drives cost, the gap
should hold near 2.5× at any length. **A gap that MOVES would say the driver is not slots**, which is
a finding about the cost model rather than about front-loading. **Two readings, two claims, and
they were about to be run together.**


---

# `|owed|` IS ONE VARIABLE WITH TWO WAYS OF BEING LARGE — AND ONLY ONE FIX HELPS BOTH

**`[I]`: front-loading and the between-board gap have the same cause.** `owed` is large **early**
because nothing has bound yet, and large on a **slot-heavy** board because there is more to bind.
**One variable, two symptoms, and the discriminate branch loops over it.**

**THE QUALIFICATION, BECAUSE *THE FIX FOR ONE HELPS THE OTHER* IS TRUE OF ONLY ONE KIND OF FIX:**

    early-largeness    A TRANSIENT. Shrinks as slots bind. A fix that speeds BINDING
                       removes it and does nothing for a slot-heavy board
    slot-heaviness     A CONSTANT of the board. 22 against 12. No amount of binding
                       makes ls20 into g50t

> **SO A FIX THAT SPEEDS CONVERGENCE HELPS THE TRANSIENT ONLY. A FIX THAT BOUNDS THE LOOP HELPS
> BOTH** — and the two are not interchangeable, which is what *the same cause* would otherwise
> suggest.

## AND THE CONFOUND IS ONE LEVEL UP FROM THE USUAL ONE

**`[I]`: *the comparison that separates two boards is blind to what they share.*** A ratio cancels
every factor common to both, **which is exactly what makes it a good between-board instrument and
exactly what makes it useless for a within-board claim.**

**The `false_mint_rate` shape at a new site** — and the difference is worth marking: that one was
**numerator and denominator moving together.** This one is **a single reading asked to carry two
claims**, where the instrument is fine and the question was doubled. **Seventh instance, first of
this kind.**


---

# `g50t` ANSWERS: ROW 2 FIRED — `discriminate:learned`, AND MY INSTRUMENT WAS ON THE WRONG DICT

    by     draw 15   probe 23   discriminate:learned 93        (131 acts over 150 cycles)
    ties   {}  -- EMPTY
    taken  ACTION2 94                                          advanced false
    secs   1940

**`discriminate` — the `spread` argmax I named all week — FIRED ZERO TIMES.** `ties` is empty because
**that branch never runs on this board.** The lock is `_learned_split`, and **`discriminate:learned`
93 against `ACTION2` 94 is the same event counted twice.**

## THE MECHANISM IS THE ONE I DESCRIBED, AT A SITE I DID NOT INSTRUMENT

    _learned_split, last line:   return max(self.actions, key=lambda a: sep[a])

**Same greedy argmax, same `max` over a fixed-order tuple, no tie-break, no exploration** — **over
`sep`, not `spread`.** So the shape of the diagnosis held and **the site was wrong.**

> **THE PINNED ROW 2 CAUGHT IT AND THE INSTRUMENT DID NOT.** I registered *`_learned_split` returns a
> stable action, different branch, same shape, fix is there instead* — **and then built the tie
> counter on the branch I had been talking about.** *Read the mechanism before building the
> instrument* was applied to `spread`'s guard **and not to the other branch I had myself named as a
> candidate.**

**THE ERROR IS INSTRUMENTING THE FAVOURED HYPOTHESIS.** Both branches were pinned as possible; only
one was measured. **A registration that enumerates two causes and an instrument that covers one is
worse than either alone** — it returns a confident empty reading. **`ties: {}` looked like a finding
and was a blind spot.**

**REPAIRED: both argmaxes counted, keyed by which dict they came from** — `spread:n` and `sep:n`.
**The tie question is still unanswered** and needs one more run.

## AND THE FRONT-LOADING IS CONFIRMED ON THE SECOND GAME, HARDER THAN THE FIRST

    predicted   0.15 x 2024s = 304s
    measured    1940s        = 6.4x the linear prediction

**150 cycles cost 96% of what 1000 cycles cost.** Under comparable contention both times — the 1000s
ran as a pair, the 150s ran as a pair. **Almost the entire cost of a 1000-cycle run is in its first
150 cycles.**

> **WHICH SETTLES THE RUN-LENGTH QUESTION FOR GOOD: THERE IS NO CHEAP SHORT RUN.** A 150-cycle probe
> costs what a 1000-cycle answer costs, **so the only rational run length is the long one** — and
> every short run this week paid nearly full price for a fraction of the evidence.


---

# THE INSTRUMENT MUST SPAN EVERY ROW OF ITS OWN REGISTRATION

**`[I]`: *vacuity with a hypothesis attached.*** A registration naming two causes with an instrument
covering one **returns a null that looks like an answer** — which is strictly worse than no
instrument, because no instrument prompts a question and an empty reading closes one.

**THE CHECK IS ONE LINE, BEFORE THE RUN:** *for each row of the registration, name the field that
would show it.* **A row with no field is a row that cannot fire** — and the registration then reads as
covering a space it does not reach.

**AND IT IS DISTINCT FROM THE UNEXPECTED-ROW LAW, THOUGH THEY LOOK ALIKE.** That one is about the
SPACE being too small. **This one is about the INSTRUMENT being narrower than a space that was
correctly drawn** — and here the space was right, the row was there, **and the row that fired was the
one nothing measured.** *The pinned row caught what the instrument missed*, which is the fourth row's
second save and only worked because it existed.


---

# RETRACTED: "EVERY NULL WAS READ AT 4% OF THE BUDGET" — THE BUDGET WAS NEVER BINDING

**`[I]` confirms, from knowledge held at the seat and deliberately not shared, that the action budget
was ample at BOTH run lengths.** The specifics are a property of a particular game, **are
seat-readable and must not enter this record**, and are not needed for the finding.

## THE REASON IS RETRACTED. THE WITHDRAWAL STANDS.

**I withdrew a week of panel readings on the grounds that *a flat progress stream at 39 steps is not
evidence the stream is flat*.** **That premise is false: the budget was not the limiter at 39 steps
and was not the limiter at 998 either.**

> **BUT THE READINGS DO NOT COME BACK, AND SAYING SO EXPLICITLY IS THE POINT.** They were never
> readings of the panel. **They are readings of a LOCKED SELECTOR on a panel** — the policy visited
> one configuration repeatedly at every length — **which is a different fault from under-sampling and
> equally disqualifying.**

**So: withdrawn, and the reason changes.** *The retraction was on a false premise* reads as *the
readings are back* **and they are not.** `[I]`, and the correction is the half that would otherwise
have been inherited.

> **AND IT IS EXACTLY THE FAILURE MODE I HAD WRITTEN DOWN.** *A null carrying a satisfying causal
> story is harder to doubt than a bare one, so the story is the thing to distrust.* **"We did not look
> long enough" is that story**, applied to my own null, **three days after recording the rule.**

## WHICH MAKES `advanced: false` A STRAIGHT NEGATIVE

**I have been reporting *the loop does far more work at budget and still advances no level* as a
curiosity — a third outcome neither row predicted.** **It is not a curiosity. It is a plain negative
on the objective, at a budget that was never the constraint.**

## AND THE REAL CONFOUND IS THE ONE THE RE-RUN FOUND

**The selector.** `discriminate:learned` locking the great majority of acts onto one action — **that
is why the precondition table is empty and why nothing advances, and it holds at every run length.**
**The confound was never budget. It was always the policy.**

**The re-run still earned its keep** — it produced the branch split and the front-loading number —
**but not for the reason it was run.** *It was run to lift a ceiling that was not there.*

## THE DISCIPLINE NOTE, WHICH IS THE PART THAT GENERALISES

**A per-game quantity is seat-readable and must not be recorded, and must never calibrate a
parameter.** Sizing a run against a game's own action counts is **tuning the harness to the task**,
which is *never encode the answer* wearing an operational disguise. **`environment_files/` is
gitignored, so the artefact cannot be committed** — but the constraint is on REASONING FROM IT, not
only on storing it, and the gitignore does not enforce that half.


---

# `[I]` THE HUMAN ANCHOR IS A READING ON ONE OF §22.5's TWO CLOCKS, AND §22.1 DOES NOT SAY SO

> *"The reason 500 is a decent number is that humans have already composed these atoms and priors
> thousands of times, and the agent is coming in relatively cold."*

**§22.1's anchor is sound and its provenance is right** — *a human's move count is not a quantity the
agent produces, so using it as a reference is not self-scoring.* **The anchor is legitimate. What it
MEASURES is narrower than it reads.**

**AND §22.5 ALREADY SUPPLIES THE VOCABULARY, ONE SECTION LATER:**

    steps-to-model   the transition-residual EMA falling and staying low   links 1-2
    steps-to-win     `levels_completed` rising                             links 3-5
    "the gap between them is the cost of EXECUTION as distinct from the cost of LEARNING"

> **A HUMAN'S MOVE COUNT IS A `steps-to-win` READING WITH `steps-to-model` AT APPROXIMATELY ZERO** —
> not because a human paid nothing to learn object permanence and contact and support, **but because
> that cost was paid before the run started, thousands of times over.** *The corpus names the two
> clocks and then anchors a budget to one of them without saying which.*

## SO THE 2× IS DOING UNPRICED WORK

**The multiplier reads as a safety margin on search. It is not.** **It is the whole allowance for
`steps-to-model` in an agent that has none of it done** — and **nothing checks whether 2× is the
right multiple**, because the quantity it stands in for was never measured on either side.

**A COLD AGENT'S TOTAL IS `steps-to-model + steps-to-win`. THE ANCHOR IS THE SECOND TERM ALONE.**
Comparing them is a category error the corpus is already equipped to refuse, **and §22.5 says they
FAIL differently, which is the same claim from the diagnostic side.**

## AND IT IS THE `post-mastery` CATEGORY, WHICH THE TERMINAL CONDITION ALREADY USES

**Clause 3 says the ablation is a POST-MASTERY test — *wipe the library of an agent at 3/25 and
neither number is interpretable, because there was nothing worth wiping.*** **A human is a
post-mastery agent by construction.** So the human anchor is **the right comparison for a mastered
agent and the wrong one for a cold one**, which is the distinction clause 3 already draws for the
ablation and nobody drew for the budget.

## WHAT IT DOES NOT DO

**It does not rescue the current agent.** Budget is not the binding constraint at any length — **the
selector is** — so this changes how the anchor should be READ and changes nothing about the
diagnosis. **Recorded because the next person to size a run will read §22.1 and not §22.5.**


---

# THREE DISCIPLINES WITH NO MECHANISM — CHECKABLE BY A PERSON AND BY NOTHING ELSE

**`[I]`. They share a property and have been recorded separately, which hid it.**

    1  THE COST SEAT              nothing measures what a change costs in actions.
                                  `THE_FORMULA`'s second currency has no reader
    2  COMMIT MESSAGE vs FILES    no seat compares what a message claims against what
                                  was staged. `git add -A` swept a corpus file twice
    3  PER-GAME QUANTITY          seat-readable, must not be recorded, must never
                                  calibrate a parameter. `environment_files/` is
                                  gitignored, so STORAGE is covered and REASONING is not
    4  A WRITTEN CAUTION          added 2026-09-02. Nothing consumes a warning, so
       ** the clearest case **    nothing can fail on it. The other three at least
                                  have a moment they would matter; this one has none

**THE THIRD IS THE ONE THAT CANNOT BE MECHANISED EVEN IN PRINCIPLE.** *A seat that may read the
harness can always reason from what it read.* **The gitignore enforces the half that was never the
risk** — and the thing that stopped the reasoning was a person, in the same minute, **not a check.**

**AND LISTING THEM TOGETHER IS THE POINT:** a discipline with no mechanism looks like an oversight
when it stands alone and like a CATEGORY when it stands with two others. **Three is enough to say the
category is real rather than that three checks are missing.**

---

# `RUN IT ON YOURSELF` IS NOW SHORTER THAN THE RULES IT KEEPS QUALIFYING

**Fourth instance of authored-and-not-turned-around, and this one on a rule three days old:** *a null
carrying a satisfying causal story is harder to doubt than a bare one, so the story is the thing to
distrust.* **I applied it to the agent's nulls and not to my own retraction**, whose story —
*we did not look long enough* — was exactly the satisfying kind.

    the audit question   framed at the codebase, never at a proposal
    the panel law        applied to the games, never to my own measurement population
    the story rule       applied to the agent's nulls, never to my own retraction
    read the mechanism   applied to `spread`'s guard, never to the branch I had also pinned

> **FOUR RULES, ONE OMISSION, AND IT IS NOT A MEMORY FAILURE.** Every one was in hand and in use.
> **What was missing each time is that the rule's SUBJECT was assumed to be the code.** So the
> general form is not another rule — **it is a second subject for the ones that exist**, and *run it
> on yourself* is shorter than any of them.


---

# `ls20` CONFIRMS `g50t` ON ALL FOUR READINGS — AND THE SPREAD BRANCH IS DEAD ON BOTH BOARDS

    ls20   by: discriminate:learned 128 · draw 20 · probe 2      ACTION2 105    4978s
    g50t   by: discriminate:learned  93 · probe 23 · draw 15     ACTION2  94    1940s
    BOTH   discriminate (the `spread` argmax): ZERO.   ties: {} on both.   advanced: false

**`discriminate` FIRED NOT ONCE ON EITHER BOARD.** The branch I named all week, and built the first
tie counter on, **does not run.** The lock is `_learned_split` on both games — **128 of 150 and 93 of
131** — and `discriminate:learned` against `ACTION2` is the same event counted twice on each.

**FRONT-LOADING, CONFIRMED TWICE AND AT THE SAME MULTIPLE:**

    ls20   150 cycles 4978s vs 1000 cycles 5147s   = 97%   (6.4x the linear prediction)
    g50t   150 cycles 1940s vs 1000 cycles 2024s   = 96%   (6.4x the linear prediction)

**Two boards, two run lengths, and the same 6.4×.** *There is no cheap short run* is now measured
rather than inferred.

**AND THE RATIO HELD — 2.54 AT 1000, 2.57 AT 150** — which was the pinned reading for the OTHER
question: **a gap that does not move with length means the driver is a CONSTANT of the board.** Slots,
22 against 12, feeding `owed`. **Confirmed, and kept separate from the front-loading claim as
registered.**

---

# SECTION CHECK ON THE THREE READINGS: TWO ARE IN THE CORPUS, AND THE INCREMENTS ARE DIFFERENT

## READING TWO IS FIGURE 12's, VERBATIM

> *"A vocabulary holding only ingredients can name a state and not a route to one: a plan is a
> sequence, **a goal is a comparison**, progress is a subtraction, and each of those is a bond."*

**A sub-goal IS a relation, and it is a BOND.** So *you cannot want a configuration you cannot name*
is **already stated**, and `RELATIONS.md` does not supply the claim — **it supplies the CUSTOMER
LIST.** *About twenty relations, each `same`/`other`/`above` over two objects' attributes.*

> **WHICH IS THE MORE USEFUL CONTRIBUTION AND SHOULD BE FILED AS THAT.** The claim was unfalsifiable
> while nothing named what a goal would be a comparison OF. **Twenty named relations is the first
> evidence the sentence has ever had.**

## READING ONE IS PARTLY FIGURE 3, AND THE NEW PART IS THE PART THAT SAYS WHAT TO BUILD

**§11.2 already has a chain breaking:** *without extractors no attributes; without attributes no
predicates; without predicates no objective — Figure 3's chain, and the break is at link 2.*

**BUT THAT DIAGNOSIS WAS SUPERSEDED THIS WEEK.** EXTRACT is built; attributes exist. **Figure 3's
*vocabulary* is one link and does not split UNARY attributes from BINARY relations** — and that split
is the whole finding: **the unary half is built, the binary half is one of seventy.**

**And the gradient vocabulary is genuinely new.** *No field without relations, no gradient without a
field, and a gradient is what makes energy available for work rather than merely present* — **Figure
3 has no such term**, and it is what makes the measurement legible: *2,834 outstanding and 104 mints
is abundant energy at equilibrium.*

**SO: the chain is Figure 3's, the TERM it names is finer than Figure 3's, and the gradient framing
is `RECURSIVE_TRANSFORMATION`'s.** Three parts, one already held.

## READING THREE STANDS AS RECORDED — third confirmation, first from outside the vocabulary.

---

# THE PAIRING IS AN EXTENSION OF FIGURE 12, AND THE INCREMENT HAS AN EDGE CASE

**Figure 12: a notation recording only ingredients *has recorded half of itself*.** That is a claim
about **information content** — the arrangement must be PRICED.

**The pairing: neither is DEFINED without the other.** That is **definitional**, and strictly
stronger. **Half is not nothing, so Figure 12 does not say the ingredients fail to denote.**

> **AND THE EDGE CASE IS `k = 1`.** A one-atom term has **no bond** and denotes perfectly well —
> which looks like a state with no structure. **The resolution is that at `k = 1` the structure is
> the TYPE, not a bond** — and the loop already enforces exactly that: an `Atom` carries
> `in_type`/`out_type`, **and a slot with no type has no alphabet and cannot be priced.**

**So the pairing holds across the composition layer with *structure* read as TYPE at `k = 1` and
BONDS at `k > 1`** — and that reading is not in Figure 12, which speaks only of bonds. **Extension,
with the increment stated.**

---

# RULED: THE TIER-2 CIRCLE AT THIS SITE, AND IT DISSOLVES RATHER THAN NEEDING AN EXEMPTION

**§12.3 states the test as a table row:** *whether it composes from the nine — **if yes it is Tier 2
and should be MINTED, NOT INSTALLED.*** **`contains` composes from overlap and extent. `aligned`
composes from position equality.** **Both are Tier 2. Publishing them as sensors is forbidden**, and
*publishing a relation is not installing a composite* does not survive the row's own wording.

> **BUT `overlap` IS SENSOR 6 OF THE NINE — TIER 1 — AND IT COMPUTES THE WRONG QUANTITY.** IoU over
> **normalised shapes**: congruence, no position. **Repairing a Tier 1 sensor to compute what §12.3
> says it computes is not an exemption. It is the repair the entry rule was written to permit.**

**AND IT DISSOLVES THE CIRCLE INSTEAD OF WIDENING IT.** `CLAUDE.md`: *what breaks the circle
legitimately is a RICHER TIER 1 — a perception question with its own entry rule — never a Tier 2
exemption.* **Fixing `overlap` is precisely a richer Tier 1**, and containment, intersection,
coincidence and nesting become **reachable by composition**, which is what §12.3 says must happen.
**The agent still has to reach.**

**THIRD SITE, AND THE FIRST WHERE THE CIRCLE HAD A LEGITIMATE EXIT.** §12.4's `parity(POSITION)` had
none; `count` had none. **This one does, because the blocked composite reduces to a Tier 1 sensor
that is BUILT AND WRONG rather than absent.**

---

# THE ORDERING, WITH THE RUN'S ANSWER IN HAND FOR TWO OF THREE

    NOT BLOCKED    repair `overlap` to bounding-box or cell-set position. TIER 1, ruled above,
                   independent of the tie question and of the selector entirely
    BLOCKED ON A   the selector fix. `tied_at_max` is still unmeasured -- the instrument was
    RE-RUN         on `spread`, which fires zero times. If `sep:1` dominates, NOTHING IS
                   BROKEN and the fix would be wrong
    REFUSED        installing `contains` / `aligned` / the four relation atoms as sensors

**AND ON THE ORDERING CLAIM:** *if reading one holds, the relation vocabulary is not third behind the
selector fix — it is what the selector fix exists to serve.* **True, and it does not reorder the
work**, because the two failures compose: **a locked selector visits one configuration repeatedly, and
a thin vocabulary notices nothing about wherever it arrives.** *Widening the reading buys nothing
while the search repeats itself; fixing the search buys nothing while there is nothing to notice.*

> **WHICH IS WHY `overlap` GOES FIRST AND IS NOT A COMPROMISE: it is the only one of the three that
> is unblocked, ruled, and Tier 1.** The selector's turn comes when the re-run says whether it is
> broken.


---

# RULED: `OBJ × OBJ` IS A SPACE, NOT A TYPE — THE `ATTR` ERROR, AT THE SENSOR REGISTRY

**§12.2 declares the whole in-type vocabulary as `("FRAME","OBJ") | ("OBJ","OBJ") | ("ATTR","ATTR")`.
Nothing in it marks time.** §12.3's table carries the distinction **in the prose column only**:

    6  overlap(a,b)   OBJ x OBJ -> RATIO   "tracking -- the slot is the SAME slot NEXT FRAME"
    7  delta(a,b)     OBJ x OBJ -> DELTA   "motion, and the contingency test for self"
    8  touching(a,b)  OBJ x OBJ -> BOOL    "contact, the default causal hypothesis"

**Six and seven are BEFORE/AFTER pairs of ONE slot. Eight is TWO slots in ONE frame.** *Same type,
opposite operands.*

## AND `arc_atoms` ALREADY CARRIES THE PRECEDENT, IN ITS OWN WORDS

> *"`ATTR` IS A SPACE, NOT A TYPE, AND THE CODE MADE IT A TYPE ... `_relate` cited §11.2 and typed on
> the space's NAME, which is correct about the space and wrong about the type: it made `above` — an
> ORDER — apply to a colour."*

**`OBJ × OBJ` is correct about the space — pairs of objects — and wrong about the type.** Identical
shape, identical symptom: **a well-typed, meaningless composition that nothing refuses.** Feed two
same-frame objects to `delta` and you get a position difference where motion was asked for.

> **RULED: the type must carry the temporal relation, following the `ATTR` fix and the `OBJECT`/`OBJ`
> split.** *Same-frame pair* and *before/after pair of one slot* are **two nodes**, not one.

## WHAT THE RULING SETTLES, AND IT IS THE THING THAT WAS BLOCKING

**`_overlap`'s target is now determined rather than chosen.** Under the ruling, sensor 6 is
**cross-frame cell IoU** — *exactly what the tracker already computes and what §12.3 names.* **And
shape congruence, which is what `_overlap` returns today, has no sensor slot at all**: it is neither
6 nor 8, so it would be a **Tier 1 addition** and fails *the loop cannot run without it.*

**The drift is explained rather than merely corrected.** *Same-frame is the only reading `OBJ × OBJ`
can express, and congruence is the only non-vacuous thing available there* — **the type pushed the
function.**

**AND CONTAINMENT STAYS BLOCKED.** Bounding-box overlap is neither node. **The exit that led nowhere
still leads nowhere, and now for a stated reason rather than an unexamined one.**

## STANDING: A REFUSAL, NOT AN ADDITION — AND THE FIFTH LATENCY

**It adds no atom and no sensor. It REFUSES compositions currently admitted**, which is the
`OBJECT`/`OBJ` split's standing exactly — that one removed 225 well-typed meaningless pipelines.

**And it is inert today.** `SENSORS.read` is called once in the repo, for `components`; **`_delta`,
`_overlap` and `_touching` are never invoked**, because §12.4's reach mechanism is `UNREACHED`.
**Fifth latency — and the first that REMOVES possibilities rather than adding cost.**


---

# BUILT: THE TEMPORAL TYPE SPLIT — AND THE REFUSAL IS DEMONSTRATED

**`OBJECT_BEFORE` added to `sensors.py`.** Sensors 6 and 7 are typed `OBJECT_BEFORE × OBJECT`;
sensor 8 keeps `OBJECT × OBJECT`.

    accepting(OBJECT, OBJECT)          before: overlap, delta, touching    after: touching
    accepting(OBJECT_BEFORE, OBJECT)   before: --                          after: overlap, delta

**Two sensors removed from the same-frame composition space, and nothing added.** `delta(x, y)` over
two objects in one frame is now **ill-typed** rather than well-typed and meaningless.

**THE WARRANT IS AT THE SITE, IN THE FORM THAT SEPARATES A REFUSAL FROM AN EXEMPTION:** §12.3 puts
the distinction in its **prose column** and §12.2's whole in-type vocabulary is
`("FRAME","OBJ") | ("OBJ","OBJ") | ("ATTR","ATTR")`, **which has no marker for time.** *This
implements a distinction the corpus draws and cannot say.*

**AND `overlap`'s BODY IS DECLARED WRONG RATHER THAN LEFT WRONG.** It returns congruence and is now
typed cross-frame; **the mismatch is stated in the comment beside it**, with the reason the repair is
deferred — *cross-frame cell IoU is what the tracker already computes, so it agrees with an existing
quantity and unlocks nothing.*

---

# STATE AND STRUCTURE: THE BUILD HAS THE DISTINCTION, AND DOES NOT ENFORCE THE PAIRING

## 1 · IT EXISTS, UNDER TWO NAMES, AND IT IS NOT A CONVENTION

    slot_types()   "What KIND of quantity each slot holds"        -> THE STATE HALF
    slot_owner()   "Which SUBJECT each slot is an attribute of"   -> THE STRUCTURAL HALF
    contacts()     which objects touch, this frame                -> a second structural reading

**All three carry the same sentence: *THE LOOP MAY NOT DERIVE THIS.*** And `slot_owner`'s docstring
answers the *is it just a naming convention* question directly:

> *"A slot name is `{object}.{attribute}` here, **and a loop that split on `.` would be reading domain
> structure.** Grouping is that same split, so **the domain declares it and the loop only
> compares.**"*

**The `.` split happens inside the DOMAIN's method. That is the whole point of it being there.** So
the structural half is **declared, not inferred** — and the build had the state–structure pair before
either of us looked for it.

## 2 · THE PAIRING IS NOT ENFORCED, AND THAT CLAIM ABOUT THE CODE IS FALSE

**Checked, and it fails in both directions:**

    _slot_types   "A world that declares no types gets {} and every operand check is
                   SKIPPED -- which is REPORTED, not assumed"
    _slot_owners  "A world that declares no owners gets {} and §12.4's trigger reports
                   that it has NO VECTOR TO FORM"

> **A SLOT CAN EXIST WITH NO DECLARED TYPE. The loop DEGRADES AND REPORTS; it does not REFUSE.**

**And the *no type, no alphabet* half is wrong too, for a separate reason:** the coding alphabet
comes from `_alphabets(env)` and the decomposition — **not from `slot_types`.** A slot has an
alphabet whether or not a type was declared. **The two are independent and independently optional.**

**So *the loop already enforces it at the boundary* is not true of this code.** It **records** the
absence, which is the abstention discipline working correctly — **and is a different thing from
enforcement.** *Recorded as a correction to the claim, not as a defect to repair: reporting an
absence is the right behaviour and the pairing was never installed as a requirement.*

## 3 · THE OPERATIONAL DEFINITION IS IN THE BUILD AND NOT IN THE DOCUMENT

**`RECURSIVE_TRANSFORMATION`'s test is *can you have three of it*** — three joules yes, three
networks no. **That is a linguistic test and nothing can apply it.**

> **THE BUILD HAS ONE THE DOCUMENT LACKS:** **a STATE is what a slot's value is drawn from; a
> STRUCTURE is which slots belong to one subject.** Both are **domain-declared strings**, both
> comparable, both with an explicit absent-reading. **That is operational and it is running.**

**WHICH INVERTS THE USUAL DIRECTION.** Twelve section checks this week found the corpus ahead; **this
one finds the code holding the operational form of a distinction the corpus states philosophically.**
**Third instance today of the corpus being behind the build** — and the first where what the code has
and the document lacks is *the test itself*.

**AND IT ANSWERS THE QUESTION THAT PROMPTED THE CHECK.** *A distinction the corpus draws and the
build cannot express* was the timing ruling. **This is the opposite: a distinction the build
expresses and the corpus states without a test.** **Found twice in one day, in both directions**, and
that pair is worth more than either alone: **the corpus and the code drift apart in both directions,
and only a diff run in both catches it.**


---

# `[I]` THE SIX TERMS AGAINST THE CODE — THREE HOLD, THREE NEED CORRECTING

**Checked each, none taken. And it goes in `INDEX` as a section, not a new document** — *a new
document that nothing reads is the failure this session has found eleven times*, and this is a
build-versus-corpus correspondence, which is what `INDEX` is for.

| term | mapping | verdict |
|---|---|---|
| **SPACE** | the grid; `row`/`col` off `components` | **holds** |
| **TIME** | `tether.history(slot)` — `[(state, action, value)]` per slot | **holds** |
| **SPECTRUM** | `_alphabets` | **splits in two, and the build's split is the better one** |
| **GRADIENT** | the residual | **holds for `R`, not for `outstanding`** |
| **NETWORK** | `contacts` built, `Preconditions` empty | **holds, partial as posed** |
| **ENERGY** | the action budget | **finiteness holds, conservation does not** |

## SPECTRUM SPLITS, AND THE BUILD IS MORE CAREFUL THAN THE DOCUMENT

**`_alphabets` returns `dict[str, int]` — a SIZE per slot.** Its docstring: *"the SIZE is the
domain's."* **That is cardinality, not ordering.**

**And the document is consistent with that**, in its own words: *"`SPECTRUM` supplies
DISTINGUISHABILITY, and distinguishability is all counting requires."* **So the mapping holds for the
counting half.**

> **BUT THE ORDERING HALF LIVES SOMEWHERE ELSE AND IS NARROWER:** `arc_atoms` declares
> **`COMPARABLE = (COLOUR, POSITION, EXTENT, DELTA, SHAPE)`** against **`ORDERED = (POSITION, EXTENT,
> DELTA)`** — *order is meaningful only on these.* **A colour is countable and has no more-and-less.**

**The document's *ordered range* would give colours a magnitude they do not have.** The build
separates *how many* from *is it orderable*, **and the corpus does not.** *Fourth instance today of
the build holding a distinction the corpus states more loosely.*

## GRADIENT IS `R`, NOT `outstanding` — AND THE DIFFERENCE IS THE WHOLE POINT

**`outstanding` is MONOTONE BY ADDITION** — it is the record of unexplained mass and *cannot unspend
itself*. **An integral is not a gradient.**

**The driving quantity is `SlotResidual.bits` per step**, which the bargain runs on: *a difference
capable of driving directed change.* **`outstanding` is what the difference has left behind.**

> **AND THAT PAIR IS THE DOCUMENT'S OWN STRUCTURE:** gradient drives, and what accumulates is the
> remainder. **`pe_integral` and `outstanding` are the accumulation; `R` is the gradient.** Mapping
> the term to the integral would make the loop appear to run on a quantity that only grows.

## ENERGY: THE FINITENESS SURVIVES AND THE CONSERVATION DOES NOT

    Budget.level_starts   left += per_level      GRANTED, by the seat
    Budget.spend          left -= 1              CONSUMED

**It is granted and consumed. Nothing transfers it and nothing conserves it.** *Transferred rather
than created* fails outright — **the seat creates it at every level boundary.**

> **BUT THE PROPERTY THE SECOND LAW'S DERIVATION USES IS FINITENESS, NOT CONSERVATION.** *"Finite
> energy in a finite region means finitely many configurations, which is what makes the counting
> terminate."* **Finite actions on a finite board is exactly that**, and it survives. **The half that
> was doing the work is the half that holds** — which was the stated risk, and it lands on the right
> side of it.

**AND THE TWO-CURRENCY CLAIM NEEDS ITS REASON RESTATED.** *One is a length under a code and the other
is a conserved quantity being spent* — **the second clause is wrong.** They do not add because
**bits are a property of a DESCRIPTION and actions are a resource the SEAT grants**; one is measured
off the term, the other is issued from outside the frame. **Different provenance, not different
conservation.**

## WHAT THE MAPPING BUYS, AND IT IS THE PART TO KEEP

**`Preconditions` empty stops being a null and becomes a NAMED MISSING TERM.** *The `NETWORK` term at
the action layer reads empty* is a statement about which step of the cycle is absent — **and the
cycle says a network is what a flow propagates through, so an empty one means nothing is
propagating.** *Which is the same reading as the chain-not-a-cycle falsifier, arriving from the term
list instead of from Part 6.*

**And the budget gains a role.** *A number in a config, mis-sized four times* becomes **the finite
resource that makes the configuration count terminate** — with a stated reason it cannot be summed
with bits, **and now the correct reason.**


---

# `[I]` THE BOND AS A SIGNATURE FIELD — CHECKED, NOT BUILT. IT SUBSUMES, AND BOTH MISS THE SAME HALF

## 1 · IT CAN BE A FIELD, AND IT DOES SUBSUME THE SPLIT

**`Sensor` is a plain dataclass — `name · fn · in_types · out_type · origin · cost`.** Adding
`bond` is one field, and `Registry.accepting` matches `s.in_types == tuple(in_types)`, so it would
match on **(in_types, bond)** with no structural change.

    OBJECT_BEFORE says   operand 1 comes from an earlier frame
    `->`          says   operand 1 precedes operand 2

**At the sensor layer those are the same claim about frames**, so **yes: subsumed** — and the bond is
the better encoding, **one field over seven values against a type name per temporal role.**

> **BUT NEITHER EXPRESSES WHAT `delta` ACTUALLY REQUIRES, AND THAT IS THE FINDING.** *Motion* needs
> **the same slot** at two moments. **`delta(objA@t1, objB@t2)` is ordered, is typed
> `OBJECT_BEFORE × OBJECT`, and is a position difference rather than motion.** **Both mechanisms
> encode TEMPORAL ORDER and neither encodes IDENTITY ACROSS TIME.**

**So the split I built yesterday and the bond proposal miss the same half.** The bond generalises the
half that was covered; **it does not reach the half that was not.** *Identity across frames is the
tracker's job and the type system cannot state it.*

**RECOMMENDATION: keep the split until the bond field exists, then replace it.** A working refusal is
not withdrawn for a proposal — **and the replacement is a strict generalisation, so nothing is lost
in the swap.**

## 2 · ITS OWN COLUMN, AND §12.2 IS THE RIGHT HOME FOR THE COLUMN

**A bond is not a type — it is the relation BETWEEN typed operands** — so **a value inside `in_types`
would be the `ATTR` mistake exactly: one column carrying two quantities.** **A separate field on the
same dataclass is the right shape**, and §12.2 is the right home because it IS the signature.

> **AND THE FIELD'S ARITY IS ALREADY DETERMINED BY THE PRICING.** `term_bits` charges
> **`(k-1)·log₂(|bonds|)`** — *`k-1` bonds for `k` operands.* So the field is **`bonds: tuple[str,
> ...]` of length `k-1`**, one per adjacent pair, **not a single scalar.** The formula fixed the
> shape before the field was proposed, which is the corpus specifying an instrument again.

## 3 · THE RECURSION IS NOT STATED, AND THE MEMBRANE TELLS AGAINST THE STRONG FORM

**`THE_FORMULA`:** *"a settled molecule becomes an atom for whatever composes over it."* **It says
nothing about the bond travelling** — and the sentence immediately after **makes crossing
substrate-dependent**:

> *"Whether a settled arrangement must be re-earned depends on the substrate — where the record
> crosses, re-deriving is a lookup and the cost was spent once; across a boundary that drops it,
> every lineage pays again."*

**And Figure 4's membrane tells against it directly:** *going up throws away detail.* **A
molecule-as-atom presents as an atom, and its internal bond is precisely the internal detail the
membrane drops.**

    STRONG FORM   the bond travels with the operand        NOT STATED, and the membrane refuses it
    WEAK FORM     bonds exist at every level, and a NEW    HOLDS, and it is the state-structure
                  bond applies above                        swap in the bond's own terms

**The weak form is what the recursion claim needs and all it gets** — *the arrangement becomes
substance, and a new arrangement applies above*, which is the pairing section's own sentence. **One
vocabulary at every level, and not one bond carried up through them.**


---

# THE IDENTITY GAP CONSTRAINS §12.4's REACH MECHANISM, NOT JUST THE TYPES

**The gap, with its owner:** *`shape_of` answers **is this the same object**, and that answer never
reaches the type checker.* **Identity across frames is the tracker's, and no signature can state it.**

**AND THE CONSEQUENCE IS ABOUT WHO SUPPLIES THE OPERANDS.**

    the loop calling `delta`      SAFE. The tracker matched the slots, so the two operands are
                                  the same object by construction
    a COMPOSED chain calling it   UNSAFE. Nothing matched anything. The chain satisfies the
                                  types, satisfies the bond, and may pair two different objects

> **SO SENSORS 6 AND 7 ARE SAFE IN THE LOOP'S HANDS AND UNSAFE IN THE COMPOSER'S** — and §12.4's
> whole purpose is to hand them to the composer. **The reach mechanism cannot admit the two
> cross-frame sensors as they stand, and neither the split nor the bond field changes that.**

**Which makes it a SIXTH LATENCY, and unlike the other five it is a constraint on a mechanism rather
than a quantity or a type.** It bites the moment `accepting`/`closure` yields a chain through `delta`
or `overlap` — **which is `UNREACHED` today for unrelated reasons, so nothing is wrong yet and
something will be.**

**AND IT NARROWS WHAT A BOND FIELD WOULD BUY.** *Subsumes the split, generalises the encoding, houses
the remaining five* — all true — **and it does not make the two sensors composable.** Worth carrying
beside the specification so the field is not built expecting it.


---

# `[I]` `frame` IS A LIST AND WE TAKE THE LAST — MEASURED, AND THE TWO BOARDS DIFFER COMPLETELY

## THE READ: FOUR SITES, ALL `frame[-1]`

    arc_holdout 65, 233, 242      arc_world 264 (`board()`)

**And `board()`'s docstring KNOWS it is a sequence:** *"`frame` is a stack played oldest to newest,
so acting on `frame[0]` means betting on a board the world has already left."* **It defends `[-1]`
against `[0]` and is silent on everything between them.** *The discard is deliberate about the wrong
end.*

## THE MEASUREMENT, AND IT IS A PER-GAME FACT

    ls20   41 responses   frames-per-response {1: 41}                NOTHING IS DISCARDED
    g50t   41 responses   frames-per-response {1: 25, 7: 4, 9: 12}   39% CARRY 7 OR 9

> **SO BOTH BRANCHES OF THE CHECK ARE TRUE, ONE PER BOARD.** On `ls20` the identity gap stands as
> filed and frames are not the answer. **On `g50t`, 16 of 41 actions return a 7-or-9-frame animation
> and we keep one of each — six or eight intermediate frames thrown away per motion event.**

**AND *PER GAME, NEVER POOLED* IS VINDICATED AGAIN**: averaging a board that animates with one that
does not would have produced *some frames are sometimes discarded*, **which is true of neither
board.**

**THE DISCARD IS NOT UNIFORM — IT CONCENTRATES ON THE MOTION EVENTS.** A single-frame response is a
step where little moved; **the 7- and 9-frame responses are where something travelled.** *So the
frames are being dropped exactly where identity across time is hardest to establish*, which is the
supporting fact rather than the proof.

## WHAT IT DOES AND DOES NOT CLOSE

**IT MAKES THE TRACKER'S JOB EASIER AND DOES NOT CLOSE THE GAP I FILED.** `Objects` matches by
**maximum overlap**, and overlap between consecutive animation frames is far larger than between two
settled boards — **so matching becomes near-trivial where today it is ambiguous, on the board that
has them.**

**BUT THE TYPE SYSTEM STILL CANNOT STATE IDENTITY**, and **the composer is still unsafe**: a chain
that pairs two objects satisfies the types and the bond whatever the tracker knows. **The sixth
latency is unchanged.** *The frames remove the NEED on one board; they do not give the signature a
way to say it.*

**AND `delta` WOULD CHANGE KIND, WHICH IS THE PART WORTH KEEPING.** *Motion as continuity across a
sequence* rather than *a difference between two snapshots* — **and the `→` bond would then already
exist in the data rather than being encoded**, which is the strongest form of the claim.

## WHAT THE PERCEPTION LAYER WOULD HAVE TO CHANGE — STATED, NOT BUILT

    board()        returns one grid; would return the stack, or the loop would iterate it
    _decomposed()  runs once per response; would run per frame, in order
    Objects        threads identity by max overlap between CONSECUTIVE frames rather than
                   between settled boards -- the same mechanism, smaller steps
    delta          a sum over the sequence rather than one difference

**Not a new sensor and not a new type. The same tracker over a finer sampling** — which is why it is
worth checking before anything is built on the gap.

**NOTE ON THE MEASUREMENT ITSELF: it created a scorecard on the API** — the environment does that on
`Arcade(...)`, and it is an outbound artefact of running the read at all.


---

# `[I]` `OFFLINE` IS THE RIGHT MODE — AND MY SCORECARD CLAIM WAS WRONG

## THE CORRECTION FIRST

**I wrote that running the frame read *created a scorecard on the API* and that *a read is never free
on the API*. BOTH ARE FALSE.** `base.py`, at the site:

    # Local scorecard (NORMAL or OFFLINE)
    card_id = self.scorecard_manager.new_scorecard(...)

**The `session.post` branch is `ONLINE`/`COMPETITION` only.** **Nothing was posted, in either mode**
— and I reasoned from a log line to a network call **without reading the branch that emits it**,
which is the reachability error at a fourth site.

## WHAT `NORMAL` ACTUALLY COSTS, AND IT IS REAL BUT SMALLER

**`base.py` 173–177:** `NORMAL` fetches **an anonymous API key** and calls **`_fetch_from_api()`**;
`OFFLINE` skips both. **Measured: construction 1.31s against 0.02s**, and `NORMAL` logs *fetched 25
environments*.

## AND THE MODE DOES NOT TOUCH THE TIMING — WHICH ISOLATES THE FRONT-LOADING FINDING

    NORMAL   ctor 1.31s | 300 steps in 0.12s = 2428 steps/s
    OFFLINE  ctor 0.02s | 300 steps in 0.12s = 2422 steps/s

**Identical within noise, and it matches the documented ~2,000 FPS local.**

> **SO THE ENVIRONMENT IS NOT THE COST. 300 steps take 0.12 SECONDS; a 1000-cycle run took 2,024.**
> **The environment accounts for about 0.4s of it — 99.98% is the agent's own loop.**

**THE FRONT-LOADING FINDING STANDS AND IS NOW ISOLATED RATHER THAN INFERRED.** *96–97% of a long
run's cost in the first 150 cycles* was attributed to `owed × cands × actions` **by reading the
branch**; this measures the alternative to zero. **The run-length ruling was not measured through a
network-attached session in any way that mattered.**

## SWITCHED, WITH THE DEFAULT INVERTED RATHER THAN PINNED

**`arc_holdout` now takes `_mode()`: `OFFLINE` unless `OPERATION_MODE` says otherwise.** The package
reads that variable itself and **defaults to `NORMAL`**; an explicit argument overrides it, so the
default is inverted in one place **and the variable still works.**

**AND THE ONE-TIME COST IS STATED AT THE SITE:** *a game not yet in `environment_files/` needs one
`NORMAL` run to fetch it* — **one run per game, ever.** The header previously defended `NORMAL` on
the grounds that *get it from the API and play locally are one path* — **true, and it took the
expensive path to the same place**, which is `board()`'s shape again: **a defence of the right answer
against the wrong alternative.**


---

# TWO SHAPES NAMED, EACH WITH TWO INSTANCES — AND NEITHER IS IN THE CORPUS

## `[I]` A JUSTIFICATION THAT ESTABLISHES THE CONCLUSION AND FORECLOSES THE BETTER QUESTION

    board()          defends `frame[-1]` against `frame[0]`     silent on the MIDDLE
    arc_holdout hdr  defends NORMAL as "one path, not two"      silent on the CHEAPER path

**Both defences are CORRECT. Both are aimed at the wrong alternative.** `frame[0]` really would be
betting on a board the world has left; *get it from the API and play locally* really is one path.
**And each answer, being right, stopped the question that would have found the better route.**

> **THE TELL IS A DEFENCE AGAINST A NAMED WORSE OPTION.** *Not `[0]`.* *Not two paths.* **A
> justification that names its alternative has drawn a boundary, and everything outside the pair is
> now invisible** — which is why a reader inherits the foreclosure rather than the question.

**AND IT IS DISTINGUISHABLE FROM A PLAIN GAP.** A gap has nothing written; **this has a good
argument written, which is what makes it survive review.** The check is *what else was available*,
and it is only askable by someone who has not read the justification.

## `[I]` A WARNING IS THE SHAPE THAT GETS REPEATED WITHOUT CHECKING

**Fourth site for the reachability error — and the first in a CAUTION rather than a proposal.**

    "running the read created a scorecard on the API"     read a log line, not the branch
    "a read is never free on the API"                     generalised from it, unverified

> **NOBODY RE-VERIFIES A CAVEAT.** A proposal invites *is this worth it*; **a warning invites
> agreement.** *It costs nothing to accept and looks like diligence*, so it propagates on the
> strength of sounding careful — **the cheap-direction bias, inverted: a warning is
> self-protecting because doubting it looks reckless.**

**THE OTHER THREE INSTANCES WERE PROPOSALS AND WERE CAUGHT BY THE WORK.** `_overlap`'s *one line*,
`by`'s *rows on disk*, `ties` on `spread` — **each failed when someone tried to use it.** **A warning
is never used, so nothing tests it**, and this one survived from the moment it was written until it
was falsified by an unrelated question.

**Which makes the repair the same one as the audit's second subject:** *run it on yourself* — **and
the new half is that a caution needs the same check as a claim, because it IS one.**


---

# THE FOURTH UNMECHANISABLE CHECK, AND IT IS THE CLEAREST CASE OF THE PROPERTY

**`[I]`: the other three proposals had a DOWNSTREAM that failed. A caution has no downstream at
all.** `_overlap`'s *one line*, `by`'s *rows on disk*, `ties` on `spread` — **each died the moment
someone reached for it.** **A warning is never reached for.**

> **SO THE FAILURE NEVER ARRIVES, AND NOTHING CAN BE WATCHING FOR IT.** That is the property the
> other three unmechanisable checks share, **and this is its cleanest instance** — the cost seat, the
> commit-message check and the per-game rule all have a MOMENT they would matter. **A written caution
> has none.**

**WHICH MOVES THE DISCIPLINE FROM *CHECK IT BEFORE ACTING* TO *CHECK IT BEFORE WRITING*.** There is
no acting. **And a discipline with no natural trigger has to have one installed, because nothing
downstream will supply it.**

## AND THE FORECLOSURE CHECK HAS THE SAME TRIGGER PROBLEM

**Review is the wrong instrument for it.** *A gap invites the question; a correct argument answers it
and closes it* — **and the one question that catches it, *what else was on the list*, is only askable
by someone who has not read the justification.**

**So it too must be asked at WRITING time.** **Same trigger problem, same repair** — and the pair is
worth keeping together: **an underestimate exempts an ITEM from scrutiny; a caution and a good
justification each exempt THEMSELVES.**

