---
name: tether-derive-first
description: Derive every ruling, design, diagnosis or proposal on The Tether / Ouroboros agent FROM the Tether figures before concluding — residual, figure lines, outward frame, witness, round trip, anchor, carry. Use for any decision on the agent, the seats' process, or pricing/design questions.
---

# Derive from the Tether first

Isaiah, 2026-10-09: *"the tether is so good that it should be able to explain all of these things … im just stating the instantiation but its purely in the tether recursively applied to this domain."* Made a priority for every agent working on the project (reviewer, proctor/seat, any Claude) and, at its own level, for the agent being built.

**Why this exists.** On 2026-10-09 the reviewer reasoned forward from a problem, posted a ruling ("consequences and bits enter ONE bargain"), and attached the figure census afterwards as a postscript. Only when asked to *derive* the ruling from the figures did Fig 12 refuse it: *"A composition costs in two currencies, and they do not add … Summing them into one figure is the error this names."* A census written after the conclusion decorates the conclusion. A derivation written before it can refuse it. This skill makes the derivation the premise.

## The procedure — in this order, every time

1. **Name the residual, as an effect.** What does the current frame fail to explain, or what failed? State it in effect terms, not cause terms. Fig 9: *"your words are borrowed too, so describe the effect rather than the cause."* If it is several questions, unbundle first (Fig 9: *"Split it rather than search."*).

2. **Derive: open the source and find the lines that bear — BEFORE concluding.** Open the SVGs (all 13 figures, plus the Operators and Symbols tables) and the formula, joining tspans and stripping the base64 metadata (recipe below). For each candidate conclusion, find the figure, formula or substrate line it follows from, and quote it verbatim. Never reason from a summary, including memory's. Write these lines down first, as a DERIVATION block, then the conclusion.

3. **Search in order: searched, inward, outward** (the formula, step 7).
   - **Searched:** do the corpus, project docs or the code already answer it? This is the cheapest, so ask it first.
   - **Inward:** extend an instrument already returning something (Fig 6).
   - **Outward, on purpose:** what living system, game, trade or other domain already faces this exact *shape*? Find the frame whose closure predicts it (Fig 8: *"Residual first, frame second."*). This is the step Isaiah does from his own lived world. An LLM holds an enormous import pool, so use it deliberately when stuck rather than waiting for someone to supply the analogy.

4. **Witness.** Corroborate any outward claim with real sources (web, papers) and cite them. Fig 9: *"the witness is always imported."* A witness is not the ground.

5. **Round trip: translate back and measure the gap.** Map the outward frame back onto the figures line by line (Fig 4: *"So take the round trip and measure the gap."*). Anything the derivation contradicts in your draft (or in an earlier ruling) is corrected explicitly and named as a correction, not silently rewritten.

6. **Anchor.** Check the conclusion against what cannot be argued with: measurements (code read at file:line, commits, ledgers, test output) and the figures' text. Agreement between seats is weak, because it is one evidence pool (Fig 2: collapse 1, mutual update). If no figure line supports a proposal, say so plainly: it is either a gap in the figures (for Isaiah) or a proposal that should not be made.

7. **Carry the method.** Record the derivation as a reusable method (residual shape → lines that bear → conclusion → corrections found) in the project's derivation log, so the next case is a lookup by shape. Fig 4: carry up *"a method that can be reapplied. Never the recording of a particular success."*

Then write the post or ruling. The FIGURE CENSUS still closes it, as a check on the derivation, not a substitute for it.

## Output shape for any ruling or proposal

```
RESIDUAL (effect terms): …
DERIVATION (before the conclusion):
  - Fig N: "<verbatim>" → what follows
  - formula step k: "<verbatim>" → what follows
  - outward frame: <domain> — <shape match>; witness: <source>
  - round-trip gap: <what the derivation corrected, or "none">
CONCLUSION / RULING: …
ANCHOR: <measurement or text it was checked against>
FIGURE CENSUS: … / Strained: …
```

## Extraction recipe (tspans joined, base64 stripped)

```python
import re, html, glob
for fn in sorted(glob.glob('<figures dir>/*.svg')):
    s = re.sub(r'<metadata.*?</metadata>', '', open(fn, encoding='utf-8', errors='replace').read(), flags=re.S)
    s = re.sub(r'</?tspan[^>]*>', '', s)
    t = [html.unescape(x).strip() for x in re.findall(r'<text[^>]*>([^<]*)</text>', s) if x.strip()]
    t = [x for x in t if not re.fullmatch(r'[A-Za-z0-9+/=]{24,}', x)]
    print('=' * 20, fn); print(' | '.join(t))
```

A zero from a dirty extraction is the most convincing kind of wrong. Re-run with the recipe before trusting an absence.

## For the agent being built (the same loop, one level up)

The agent already runs this loop on boards: residual → lookup (forward and abductive) → mint priced by the one body → ground. Isaiah's ruling makes the same loop apply to the agent's *own process*:

- **D1:** its own process is a world it perceives. A search stopped below the cheapest term, a sealed slot, a stalled level: each is a residual with slots.
- **D2:** those process residuals are described as effects, so the lookup can find a method that predicts them.
- **D3:** the meta level's ground is level and game outcomes only. It never grades its own self-diagnosis. Fig 10: *"A verifier that can reconstruct the claim cannot verify it."*
- **D4:** methods carry across levels and games, and are replayed as methods, never recordings (MC6).

Design first, measured behind an arm, under the registered rule.
