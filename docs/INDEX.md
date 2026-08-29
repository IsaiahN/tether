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
