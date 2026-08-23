# THE FORMULA

The per-step cycle in compact form, with every symbol defined. This is the whole of the mechanism; the figures are its parts drawn out.

**Why the ordering matters more than any single step.** Each step consumes what the one before produces. A diagnosis that cannot be traced to a step is probably vocabulary rather than a derivation, and a reading taken below a step whose input never arrived describes nothing.

*Revision note: this supersedes the Aug-2026 draft. Every change is itemised in **CHANGES** at the end.*

---

## SYMBOLS

Read this first if you have not seen the notation. Every symbol below appears in the loop.

| symbol | name | what it is |
|---|---|---|
| **Γ** | the library | Everything the system can currently express: its primitives, and everything it can build by combining them. Read *gamma*. |
| **atoms(Γ)** | the primitives | The terms in the library that were not built from anything else. The floor of what it can say. |
| **closure(Γ)** | the reach | Everything expressible by combining the primitives, at any depth. What the system could say if it searched forever. |
| **b** | the belief | What the system takes to be the case before it acts. Formed from its own history and from what it inherited, mixed by `w`. Not the observation. |
| **w** | the weighting | How far the belief leans on private encounter history versus inherited prior. `w_A + w_B = 1`, and `w` is learnable from the outcomes of past weightings. **Two frames with identical architecture diverge because their histories and their `w` diverge — that is the pose, and it is what makes them non-identical for a stateable reason.** |
| **a** | the action | What it does. |
| **o′** | the observation | What actually happened. Read *o-prime*. |
| **Γ(b,a)** | the prediction | What the library says should happen, given belief `b` and action `a`. |
| **R** | the residual | The gap between prediction and observation. The central quantity: everything the system does is driven by it. **It is the aim, not only the error signal** — it selects the question, the frame, and what the verifier may see. **And it is always a slice**: what cannot be perceived or measured yet *is* residual, it simply cannot be read. There is no state in which `R` is fully known. |
| **s** | the slot | One object, region or entity being tracked. `R` is measured per slot, never as a single global number. |
| **R⁺_s** | the live mass | The part of the residual on slot `s` that is positive: something happened there the prediction missed. |
| **φ** | a candidate term | A new predicate the system is considering adding to the library. Read *phi*. |
| **\|φ\|** | its cost | How much it costs to state `φ`, under a **declared code**. Also written `cost(φ)`. |
| **\|R\|φ\|** | the leftover | How much residual remains once `φ` explains what it can. Also written `left(R,φ)`. **May be greater than zero.** |
| **T_A** | going up | Abstraction. Detail is thrown away, which is what makes the result reusable. *(≡ `α` in abstract interpretation.)* |
| **T_E** | coming back | Concretisation. Putting an abstract result back into a specific situation. *(≡ `γ`.)* |
| **R_T** | the round trip | The gap between what was sent up and what came back down. Measures what the coarser description cannot hold. |
| **F** | the frame transform | The map between allocentric and egocentric **at one scale**. Distinct from `T_A`/`T_E`, which run between scales. Cannot be run without a pose. |
| **the ground** | the anchor | Whatever settles the question and does not change its answer because of what any frame thinks. **It is not a frame. It has no vantage to update from.** Not in the library; the loop cannot modify it. |
| **the habitat** | the field of contact | Everything in contact with the residual: actors, conditions, relations. Enumerated, never composed. |

**Two words used throughout.** A **frame** is any bounded system with a library — an agent, a person, a discipline, a model. *A frame is a theory with a signature, not a coordinate system: frames differ in what they can express, not in how they label it, and there is no known transform between two of them.* A **seat** is a position in a checking arrangement, defined by what it can and cannot see rather than by who occupies it.

---

## THE LOOP

```
1. PERCEIVE
   Bet, act, observe.
   R = |Γ(b,a) − o′|, measured per object slot s.

   The residual is indexed by slot, never aggregated. A global R near zero
   with one live slot is a legal state and not an inert one, and averaging
   across slots is how a live signal disappears.

   The bet is placed on b, the belief — not on the observation. Under partial
   observability those differ, and a system that predicts from what it just
   saw has no model to be wrong.

   R IS ALWAYS A SLICE. What the instruments do not reach is not absent
   residual; it is residual that cannot be read. The habitat is enumerated
   outward until the cascade stops mattering, and that bound is pragmatic,
   never a completeness claim. So a low reading has three causes and only two
   of them are about R stopping:

     the prediction is good              genuine
     the channel closed                  step 8's undetectable case; a seat's office
     the instrument never reached it     the slice is too small; step 7 INWARD

   The third is not a stopping condition. It is the permanent condition, and
   the only remedy is to extend the instrument from one already returning
   something that fails to resolve.

2. ROUTE
   The boundary diff sorts R into four bins. Each has a different remedy
   and using the wrong one wastes the residual:

     TRANSFERRED         the invariant held. Nothing is owed.
     NOVEL               something unmodelled. Extend perception, aim the probe here.
     BROKEN · rebinding  the model is right and attached to the wrong thing.
                         Re-fit the binding. Do not mint.
     BROKEN · mechanism  the model itself is wrong. A mint is owed.

   Record why not the neighbouring bin. A bin without its discriminator is
   a label, not a diagnosis.

   AND THE SORTER MUST NOT BE THE COMPOSER. A frame that authors the vocabulary,
   the emission and the interpretation reads zero — three of three, and it
   arrives dressed as a paragraph. You cannot correct integration drift from
   inside the integration; only an external landmark can.

3. MINT
   Offer a candidate φ against the bin that owes one.

   THE BARGAIN — a bargain, not a threshold:
     |φ| + |R|φ| < |R|
   Both halves are lengths under a code. DECLARE THE CODE. Without one the
   inequality is not evaluable, and two implementations are not running the
   same test. A margin, if used, carries its provenance.

   THE GUARDS — a product, not a checklist. Any factor at zero forces inertness:

     SUPPORT       |R⁺_s| > 0 for some slot s      before the search
     REACHABILITY  φ ∈ closure(Γ)                   during
     NOVELTY       φ ∉ atoms(Γ)                     after a candidate exists

   Ordered by when each becomes checkable, not by importance. In scalar form
   the same product is density(R) × orthogonality(R,Γ) × reachability(φ,Γ),
   where orthogonality is H(R|Γ) — what Γ cannot already explain. The
   syntactic guards are proxies for it and are zero in the same cases.

   REACHABILITY HAS NO NEGATIVE. A witness proves reachable. An exhausted
   budget proves UNREACHED, which is not unreachable: no frame certifies its
   own limit, so a search that finds nothing is never a proof of absence.

   SUPPORT AT ZERO IS AN INSTRUCTION, NOT A STOP. If |R| ≈ 0 the bargain is
   unsatisfiable whatever atoms exist — you cannot compress what you never
   observed. Perturb: an uninformed probe, triggered by the system's own
   prediction error falling to nothing, whose outcome re-enters as an ordinary
   observation. A probe aimed at reward is Goodhart in a probe's coat. A probe
   that is read is an experiment.

   PAYS IS NOT CLOSES. |R|φ| may exceed zero. A term that pays is worth
   accepting and the slot still owes. Step 7 fires on failure to CLOSE R,
   never on failure to PAY.

4. ACCEPT
   Γ ← Γ ∪ {φ}, stamped with where it came from and when.

   The stamp is not bookkeeping. A term derived independently and a term
   adopted from elsewhere are identical in content and differ only in origin,
   and only the record separates them. The stamped record is a REIFICATION —
   the loop's own state made available as data — which is what allows a
   checker to read it without reading the machine.

   AND THE LIBRARY IS RESTRUCTURED, NOT ONLY EXTENDED. Accepting only ever
   adds. A library that only grows accrues the debt it was minted to avoid.
   Refactoring is the one payment that is voluntary, and the one nobody
   schedules.

5. SETTLE
   The ground settles it. Verified only by what pays.

   A gate passing is not the ground. A build whose only evidence is its own
   test is a candidate, because the test is the maker's instrument.

   Until the ground settles it, a term is CANDIDATE: it may be held and it
   may not be cited. An unsettled term used as evidence in a later bet is how
   a wrong term compounds.

6. PROMOTE
   Generators cross upward; playback never does.
   Priors descend; replays never do.

   A recording carried up looks like knowledge and is a description of one
   occasion. Replayed downward it produces a system that repeats a past
   success and cannot produce a new one.

   Unbracketed, the transform is dead reckoning:

     R_T  =  gap( x , (T_E ∘ T_A)(x) )        x concrete

   Send it up, bring it back down, compare against what was sent. T_A and T_E
   form a Galois connection, so x ⊑ T_E(T_A(x)) always: the round trip can
   only lose precision, never gain it, and R_T is therefore non-negative by
   construction. That gap is not an error to eliminate. It is the measurement
   of what the coarser level cannot hold.

   SHADOW DECIDES WHETHER TO MINT; ECHO DECIDES WHETHER IT WAS A PRIMITIVE.
     shadow   local, in-episode: does this close a residual already recorded,
              recorded BEFORE the candidate was chosen?
     echo     cross-domain, between episodes: does it appear where you did
              not build it?
     echo without shadow is apophenia — a structure found elsewhere and given
     somewhere to live. shadow without echo is a working local hack, which is
     legitimate and does not cross. shadow then echo is a primitive.

   AND THIS IS NOT THE ONLY TRANSFORM. T_A/T_E runs between SCALES. F runs
   between allocentric and egocentric at ONE scale, and cannot run without a
   pose. Ego→allo is learning: the allocentric map is the integral of
   egocentric deltas. Allo→ego is acting: the map cannot move your body.
   Neither alone is navigation, and a stationary observer never builds a map.

7. WHEN NOTHING IN closure(Γ) CLOSES R

   FIRST: IS THERE A FACT HERE? Disagreements that do not shrink with effort,
   where each rule keeps working well on a different subset, are not one hard
   question but several well-formed ones. Split rather than search. And when
   the split lands on a union rather than a partition, unbundle before
   searching again.

   THEN it is two questions, not one, and their instruments are opposed.
   Never read one against the other.

   INWARD   Is our representation adequate to hold it?
            Extend the instrument. An instrument is improved from a worse one
            already returning something, never built from a description. So
            the question is not whether a sensor could exist, but whether
            anything, at any resolution, already returns something that fails
            to resolve.
            Sharpen the description in the machinery's own terms.

   OUTWARD  Does another frame already hold it?  IMPORT.
            Characterise R first, in effect terms, then find the frame whose
            closure already predicts its shape.
            Gated on: where it came from, and whether it explains a gap this
            frame could not. Debited against that frame's independence.

   IMPORT ADDS NO ATOM TO THE WORLD. The world gains no primitives; a frame
   gains access. Composition explores what the operators reach; instruments
   extend what can be represented at all — which is why some unreachability
   is depth and some is genuine absence, and from inside the frame the two
   look the same.

8. REPEAT
   The residual drives the next cycle.
   ┌──────────────────────────────────────────────────────────────────┐
   │  Γ is now larger by whatever was accepted, so the prediction at   │
   │  step 1 is different, so R is different. Return to 1.             │
   └──────────────────────────────────────────────────────────────────┘

   Nothing here maintains the ground. The ground does not decay; the channel
   to it does, and keeping that channel open is a seat's office, not the
   loop's.

   AND THE SEAT ABOVE IS INSTANTIATED ON DEMAND. A seat at the next level
   exists when a residual crosses the seam that this level cannot settle, and
   not otherwise. The stack is a meta-continuation: its depth is set by how
   often something actually fails to settle, never by a standing hierarchy.
   Which is why there is no top rung — the tower is infinite in the
   specification and finite in the run, and that is a result with an
   implementation rather than an argument.
```

---

## WHY THIS IS A LOOP AND NOT A PROCEDURE

**It closes.** Step 8 returns to step 1 with a changed `Γ`, so the prediction changes, so `R` changes. Nothing here runs once and finishes: the output of the last step is an input to the first.

**It is a feedback loop in the control sense**, with the usual parts in the usual places:

| control term | here |
|---|---|
| **reference** | the ground: what the system is being held to |
| **plant** | the world the action lands in |
| **error signal** | `R`, the residual, measured per slot |
| **controller** | `Γ`, which produces the prediction and therefore the next action |

**And one part is not usual.** In standard adaptive control the controller tunes its *parameters* against the error. Here steps 3 and 4 change the controller's **vocabulary** — the set of things it can represent at all — which is why an unmodelled effect is a different failure from a mis-tuned one, and why step 2 sorts them before anything is done about either.

**Two loops, nested.** Steps 1 to 5 close within one agent at one scale. Step 6 closes across scales: send a method up, bring a prior down, and compare what returns against what was sent. The second loop's error signal is `R_T`, and a system that runs the inner loop without the outer one is stable and unmoored — confident about a position nobody checked.

**It has no convergence criterion, by construction.** There is no state in which the loop is finished. It stops only in two ways, and they look alike from inside:

- **`R` stops arriving because the prediction is perfect.** No system in contact with a changing world reaches this.
- **`R` stops arriving because the channel closed.** Stale readings, a saturated metric, a substituted habitat, a pooled population. The loop keeps turning and is now measuring itself.

Which is why the last line of step 8 is a boundary rather than a flourish: **detecting the second case is not something the loop can do**, because a loop with no error signal has nothing to detect it with. That job belongs to a position outside the loop, and Figure 10 is about who can hold it.

**One structural defence against that blindness is available and belongs in any implementation.** The time-integral of prediction error is **monotone**: a drive may read it and may never reduce it. What a term explains reduces the *outstanding* residual and never the integral, because understanding a surprise afterwards does not unmake having been surprised. A system that could zero its own surprise record could look calm by having forgotten it was ever wrong — and then the two stopping cases become indistinguishable from outside as well as from inside.

---

## WHAT THE ORDERING CARRIES

**The guards are a product.** `novelty capacity = density(R) × orthogonality(R,Γ) × reachability(φ,Γ)`. A system minting nothing may have nothing wrong with its minting: any one factor at zero stops it. And the three are not interchangeable remedies — a zero in the first says *probe*, a zero in the third says *import*.

**The bill runs underneath step 3.** Cost is never escaped, only relocated: you choose the currency, the schedule, and the exponent. Selection over `N` variants supplies at most `log₂ N` bits about the target, and the variants are what you pay for. Aiming the variation lowers the exponent; reading the failure instead of counting it raises the bits per trial — and that second one only works with an interpreter independent of the thing being explained.

**closure(Γ) has a lower bound the environment sets, not the designer.** Only variety absorbs variety: `H(outcome) ≥ H(disturbance) − H(regulator)`, where `Γ` is the regulator. Minting is variety acquisition. Which is the diagnostic in step 3 restated: if `R` is not falling, either `Γ`'s variety is below the environment's, or the disturbance variety was never observed.

**And closure(Γ) is only searchable because it is typed.** An untyped bag of `V` primitives grows as `Vⁿ`. A typed grammar grows as `λⁿ`, where `λ` is the spectral radius of the type transfer matrix — and `λ < V` whenever the type graph is sparse. Typing does not shrink the library; it shrinks the branching at the point of choice, which is what makes REACHABILITY a search rather than a wish.

**Step 6 is a membrane in both directions.** What crosses is a method, never a recording. A seed carries no small tree — it carries what will grow one, and the level it lands on decides what it becomes.

**Step 7 has two routes and they must not be confused.** Import is the only operator that adds a primitive. Instrumentation is the only thing that extends what can be represented at all. Neither can be deposited in mid-air: composition extends from the atoms you hold, instrumentation extends from a reading that already exists and fails to resolve.

**And step 8 marks the boundary of the loop.** The loop composes and mints. Keeping the anchor reachable is somebody's job and it is not the loop's.

---

## WHY THERE IS NO REGRESS

Three answers, and they are not the same answer.

**The seed is the seedline.** There is no first seed to find: the question is malformed. A copy regresses — two identical mirrors add zero at every reflection, which is an infinite *and uninformative* loop. A transform imports variation at every step, and a finite system terminates by exhaustion.

**Non-identity has a mechanism, and it is not entropy.** Two frames of identical architecture diverge because their encounter histories differ and `w` differs. An object has no vantage; a process has one; here the process has a parameter. *("Each copy is imperfect" grounds non-identity in noise, which is the weaker answer and is retired.)*

**And the tower is finitely implementable.** A level above is instantiated only when something below reflects. Levels nothing has reached are identical and cost nothing; every actual crossing pays, and the crossing is where the transform sits.

**Why a transform must exist at all:** an invertible map, iterated, is a permutation — every state has one predecessor and one successor, so a lineage cycles and never branches. Divergence requires the map to be **one-to-many forward**; irreversibility requires it to be **many-to-one backward**. Speciation is the observable signature of both. *A tower of levels that has produced no branching has no transform, and that is checkable from outside without access to the transform itself.*

---

## DECLARING THE MODE

The notation creates a demand for quantities. Where they are not measured, a reader supplies them, and `|φ| + |R|φ| < |R|` followed by *accepted* reads as a check that was run.

**Three legitimate modes, and the mode must be stated.**

| mode | what it means |
|---|---|
| **general** | the procedure, no quantities. What the framework licenses on its own. |
| **specified** | quantities named as targets for measurement, labelled as such. An unmeasured number is a specification of what to measure and can be worth a great deal: it names a comparison nobody had framed. |
| **grounded** | quantities from data, with the source. |

**What is not a mode is the label.** *Accepted* means the ground settled it. A candidate labelled accepted claims a settlement that did not occur, and the formalism makes it look rigorous. Same numbers, same reasoning, labelled **candidate** — nothing else changes.

**And a room does not upgrade the label.** A group reaching a conclusion without the ground is agreement, and agreement among frames is a weighted average of influence. Adding people raises the vocabulary and does not add an anchor. Two estimators correlated at `ρ` average to variance `σ²(1+ρ)/2`: at `ρ = 1` the second frame buys nothing, and twenty frames at `ρ = 0.9` are worth about 2.2.

> The machine specifies. An instrument measures. The ground settles.
> A room locates and argues, which is upstream of all three.

---

## THE LOOP APPLIES TO ITSELF

Every law here binds this document. A theory about frames that exempts itself is special pleading, and the frameworks that stalled on self-application are cited in the figures for exactly that reason.

**But applying is not certifying**, and the distinction is load-bearing:

> **The framework applies every law TO itself. It does not CERTIFY itself.**

Self-application is a consistency requirement and it is met. Self-validation is forbidden — by rule 2 of the framework's own citations, a consistent system cannot prove its own consistency — and it is not claimed. What settles the artefacts is the ground, as it is for anything else.

**Which is also why the prohibitions are scoped rather than absolute.** *A rule no real occupant could meet describes an idealisation, not a position* — and an idealisation licenses inferences no real position would support, drawn by whoever finds them useful. Before enforcing an absolute, ask what would have to be true for a real occupant to meet it.

---

## WORKED READING

To demonstrate the loop on a case, state each step explicitly and stop where the input stops arriving.

**1 · What was predicted, what happened, and where.** Name the slot. If the gap is stated as one global number, the reading is already lost.

**2 · Which bin, and why not the neighbour.** Most misapplied effort is a rebinding problem treated as a mechanism problem, which produces a new term where a repair was owed.

**3 · What term is offered, and does the bargain pay.** State all three guards and the code. If any guard is zero, say which and stop: the mint is not going to fire and nothing below step 3 is diagnosable. If the offer pays but does not close, say so — that is step 7's trigger, not a success.

**4–5 · Where it came from, and what settled it.** If nothing settled it, the result is a candidate. Say so, and do not cite it.

**6 · What crosses.** A method, or a recording? If a recording, the promotion is invalid regardless of how well it worked. And which test is being reported — shadow, or echo?

**7 · If nothing closes the gap.** Is there even one fact here, or several? Then: inadequate representation, or a frame elsewhere that already holds it? Answer one. Answering both at once produces a description sharpened into terms only you can read.

**8 · What the next cycle is driven by.** If the answer is the same residual as last cycle, nothing moved, and the report should say that rather than describing the activity that occurred meanwhile.

---

## CHANGES FROM THE PREVIOUS DRAFT

**Corrections**

1. **`R_T` composition order.** Was `R_T = |T_A ∘ T_E(x) − x|`, which reads as concretise-then-abstract and requires `x` abstract — the *reductive* law. The prose beside it describes the *extensive* one. Now `R_T = gap(x, (T_E ∘ T_A)(x))` with `x` concrete, which is what "send it up, bring it back down" means.
2. **`R_T` is directional, not a metric difference.** `T_A`/`T_E` form a Galois connection, so `x ⊑ T_E(T_A(x))` always. The gap is non-negative by construction rather than by hope.
3. **Step 5 renamed ECHO → SETTLE.** "Echo" was carrying two meanings in one body of work: the ground settling a term, and the cross-domain promotion test. SETTLE is what step 5 does; ECHO is reserved for the promotion grade in step 6.
4. **`α` → `w`** for the private-versus-inherited weighting. `α` is standard for the abstraction map, which this framework also uses. `w_A`/`w_B` already existed elsewhere for the same quantity, so this is a consolidation.
5. **Prohibitions scoped rather than absolute**, per the idealisation rule.

**Additions to the loop**

6. **Step 1 — the belief is the bet.** `b` is formed with `w` and is not the observation. Under partial observability a system that predicts from what it just saw has no model to be wrong.
7. **Step 2 — the sorter must not be the composer.** The independence clause was in Figure 10 and not in the loop, and the loop is where it binds.
8. **Step 2 — record why not the neighbouring bin.**
9. **Step 3 — declare the code.** The bargain is not evaluable without one, and two implementations with different codes are not running the same test.
10. **Step 3 — REACHABILITY has no negative.** UNREACHED at a budget is not unreachable.
11. **Step 3 — SUPPORT at zero is an instruction.** Probe, uninformed, outcome back through the same residual. Previously the loop said a zero guard forces inertness and said nothing about the remedy.
12. **Step 3 — pays is not closes**, and step 7 fires on the second.
13. **Step 3 — the scalar guards defined.** `orthogonality(R,Γ) = H(R|Γ)`; the syntactic guards are proxies, zero in the same cases.
14. **Step 4 — the stamp is a reification**, which is why a checker can read it without reading the machine.
15. **Step 4 — the library is restructured, not only extended.** Nothing in the previous draft ever refactored `Γ`.
16. **Step 5 — candidate may be held, not cited.**
17. **Step 6 — shadow and echo separated**, with apophenia named.
18. **Step 6 — `F`, the frame transform**, distinct from `T_A`/`T_E` and requiring a pose.
19. **Step 7 — the malformed precondition.** Is there one fact here, or several? Split before searching; unbundle a union before searching again.
20. **Step 7 — import adds no atom to the world.**
21. **Step 8 — the seat above is instantiated on demand.** The stack is a meta-continuation; the tower is infinite in specification and finite in the run.

31. **Step 1 and the symbol for `R` — `R` is always a slice.** What cannot be perceived is residual that cannot be read, not residual that is absent. A low reading has three causes, and only two of them are about `R` stopping: the third is the permanent condition and its remedy is step 7 INWARD.

**Additions to the notes**

22. **The monotone surprise integral** as a structural defence against the undetectable stopping case.
23. **The bill**, with `log₂ N` as the bit-rate of selection over `N` variants.
24. **Requisite variety** — `closure(Γ)` has a lower bound the environment sets.
25. **Typing beats size, quantified** — `λ`, the spectral radius of the type transfer matrix, against `V`.
26. **"Why there is no regress"** as its own section, with three distinct answers and the branching argument that says why a transform must exist.
27. **The correlated-agreement arithmetic** — `σ²(1+ρ)/2`, and twenty frames at `ρ = 0.9` worth 2.2.
28. **"The loop applies to itself"** — self-application is required, self-validation is forbidden.
29. **Frame defined against the coordinate-system reading**, in the two-words note.
30. **`R` named as the aim**, not only the error signal.
