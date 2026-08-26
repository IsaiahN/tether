# SNAPS — the generated habitat, with levels

Plan only. Nothing here is built.

`snaps.py` today generates one flat world: 5 slots, 6 rule families, 1 objective, no
progression. It already produced the number that matters — **42.3% false mints against
1.5% false abstentions** — so the instrument works. What it cannot yet measure is the
thing the whole architecture claims: **that Γ transfers.**

Transfer needs levels. Levels need a controlled relationship between them. That control
is the one genuinely load-bearing thing the retro corpus supplies.

---

## 0. What the corpus contributes, and what it does not

The five documents are a design for a 30-expert mixture-of-experts router. **None of
that comes in.** The catalog's own numbers say why: 3% of 57,170 games expert-tagged,
66% novel-archetype-tagged, 31% MISSING. 353 new archetypes from 500 screenshots — about
0.7 new archetypes per screenshot examined. Building experts reveals archetypes faster
than it closes them. The catalog is a measurement *of* the archetype trap.

Three things do come in, all of them descriptions of *worlds*, never of *solvers*:

| from | what | used as |
|---|---|---|
| `EXPERT_ALGORITHM_GROUPS` F1–F15 | a taxonomy of mechanic families | **rule families to generate** |
| `EXPERT_AUDIT_DEEP` §4A | private-set composition estimate | **sampling weights** |
| `GAME_FAMILY_GRAPH` DS | deviation strength between parent and variant | **the level ladder** |

And one for later, not this plan: `EXPERT_AUDIT_DEEP` §7C, mechanic-signature probes.
Those are the only lines in the corpus written as *what to look at*, and they are the
Phase 3 sensor spec.

---

## 1. The level ladder is DS-controlled. This is the whole idea.

A level sequence only measures transfer if the relationship between consecutive levels is
known. Two failure modes:

- level *n+1* unrelated to level *n* → nothing can transfer, the metric reads zero and
  means nothing
- level *n+1* identical to level *n* → everything transfers, the metric reads one and
  means nothing

`GAME_FAMILY_GRAPH` already solved this for real games. **Deviation Strength**: 0.0 same
mechanic, 0.3–0.5 meaningful mechanic addition, 0.6–0.8 new mechanic layer, 0.9–1.0 genre
pivot. Generate level *n+1* at a *specified* DS from level *n* and the question stops
being "does it transfer" and becomes **a curve**:

```
        reuse rate
            │
        1.0 ┤●──●──●
            │        ●╲
            │           ●╲
        0.0 ┤              ●───●───●
            └──┬───┬───┬───┬───┬───┬──▶  DS
              0.0 0.2 0.4 0.6 0.8 1.0
```

**Where that curve falls off is a measurement of how general the library is**, and it
needs no win to read. A library of over-fitted terms dies at DS 0.2. A library of real
mechanisms survives to 0.6.

DS is implemented as concrete edits to the parent world's spec, not as a fudge factor:

| DS | edit |
|---|---|
| 0.0 | same families, same arity, new constants and new start state |
| 0.2 | one slot's rule swapped within its own family |
| 0.4 | one new family introduced; the rest held |
| 0.6 | objective family changes; rules held |
| 0.8 | rules and objective both change; slot count changes |
| 1.0 | fresh seed, nothing shared |

The DS is recorded in the key. The agent never sees it.

---

## 2. Eleven families, weighted by the §4A estimate

Current six: `identity · affine · quadratic · action · interact · delayed`.

Five to add, taken from F1–F15 as *world shapes*:

| add | F | shape | in closure? |
|---|---|---|---|
| `chain` | F5 | A reads B, B reads C — multi-hop causality | only with arity **and** depth |
| `lagged` | F9 | effect at fixed lag k>1 (generalises `delayed`) | **no** |
| `constraint` | F1 | value must satisfy a relation to another slot | partially |
| `hidden` | F11 | the driver is not in the observable state | **no** |
| `regime` | F15 | the rule changes after N steps — a rule about rules | **no**, until split |

Three of the five are outside closure, which roughly doubles the honest-abstention test
surface. Sampling weights come from §4A's private-set estimate (F1 25–35%, F15 20–30%,
F5 15–20%, F10 10–15%). Whether that estimate is *right* is unknowable; as a coverage
prior over generated worlds it costs nothing and beats uniform.

**`chain`, `lagged` and `hidden` are the direct attack on the 42% false-mint rate.** They
are exactly the shapes that punish a term fitted to a narrow observed slice, because the
slice cannot contain the evidence that would refute it.

---

## 3. What persists across a level boundary, and what does not

This is the load-bearing table. Get it wrong and the transfer claim is unmeasurable.

| | persists | why |
|---|---|---|
| **Γ library + standing** | ✅ | this *is* the transfer claim |
| **parked residuals** | ✅ | **the sweep's only real target.** A residual parked on level 2 is not re-searched by the mint while playing level 5 — which is precisely the condition the toy world could not create |
| **the trace** | ❌ | different slots, different world |
| **bound slot→term map** | ❌ | slot names do not carry meaning across levels |
| **instruments** | ✅ accumulate, ❌ per-segment | Chain segments close per level; Phases records per level |

The second row is the answer to Phase 1's open falsifier. The sweep fired 5 times in 40
flat worlds, which was enough to prove it runs. Cross-level parking is what makes it
*matter*.

---

## 4. Three ways a level ends

Currently there is only `run_end`. Levels need all three, because each closes a Chain
segment differently and the stage-code discipline depends on the distinction.

| event | trigger | segment closes as |
|---|---|---|
| **advance** | objective degree reaches 1.0 | `advance` — **not** scored as a loop firing |
| **death** | an `AVOID` objective is violated | `death` — the reset signal, which is juicy data |
| **exhausted** | action cap reached | `run_end` |

`AVOID` already exists as an objective family and currently only reads as a degree. Wiring
it to terminate the level is what turns it into a loss condition — and a loss that resets
the level is a strong, cheap signal the agent can learn from.

---

## 5. Curriculum order — anchored, not invented

The corpus proposes ordering by **DCS**, a Developmental Ceiling Score. **Rejected.** DCS
is a quantity the frame produces and then uses to grade the frame, including grading
itself. That is the invented-metric failure mode by name.

Two orderings are available that are properties of the *world*, computed from the key,
and that the agent cannot move:

1. **fraction of slots outside closure** — how much of this level is honestly unknowable
2. **mean minimal term length** — how deep the reachable answers are

Both are external, both are checkable, neither is anything the agent produces. A
curriculum is a monotone sweep over those two, and it is reported with its basis rather
than a bare number.

---

## 6. What the grader gains

`grade()` currently returns per-world false-mint rate, abstention accuracy, minimality
gap, mixture. Levels add four:

| | reads |
|---|---|
| **reuse rate vs DS** | the transfer curve of §1 — the headline |
| **minted fraction per level** | of the terms a level's solution used, how many were minted here vs carried in. Free from the origin stamps. Distinguishes composing from retrieving with no ablation run |
| **probe-share trend** | already in `Phases`; needs levels to have anything to plot. Phase-1 share shrinking across levels **is** the transfer claim in the human-reference frame |
| **cross-level retro** | parked on level *i*, closed on level *j*. The only reading where the sweep is doing work the mint could not |

---

## 7. Falsifiers

Per phase, in the build-plan convention. Each is a way this is wrong.

| | falsifier |
|---|---|
| **1. ladder** | if reuse rate is flat across DS 0.0→1.0, DS is not controlling anything and the ladder is decoration |
| **2. families** | if `chain`/`lagged`/`hidden` do **not** move the false-mint rate, then the 42% is not about narrow slices and my diagnosis is wrong |
| **3. persistence** | if cross-level retro stays at zero with parked residuals persisting, the sweep is genuinely redundant and should be deleted rather than defended |
| **4. termination** | if death-resets produce no measurable change in behaviour, the loss signal is not reaching the loop |
| **5. curriculum** | if ordered and shuffled curricula give the same end-state Γ, ordering does not matter and the section is waste |

Falsifier 3 is the one I most expect to have to act on, and deleting the sweep is an
acceptable outcome.

---

## 8. Build order

| | | why first |
|---|---|---|
| S1 | five families + weights | cheapest, and it directly attacks the known 42% |
| S2 | level loop, three terminations, persistence table | the ladder needs somewhere to run |
| S3 | DS-controlled generation | needs S2 |
| S4 | grader extensions | needs S3 to have anything to read |
| S5 | curriculum sweep | last; it is the least certain to matter |

Estimate: ~180 lines on top of the current 243. No new files beyond `snaps.py` and a
`levels` section in the grader.

---

## 9. Explicitly not coming in

- the 30-expert taxonomy (E01–E30)
- the MoE router and `MISSING:EXPERT:*` dispatch
- DCS and the developmental-ceiling framing
- the 52–82% coverage projection
- any per-game mechanic ("bp35 is Sokoban") — absence lists only, never content
