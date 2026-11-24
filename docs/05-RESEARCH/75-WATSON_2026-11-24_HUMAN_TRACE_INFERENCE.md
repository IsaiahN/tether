WATSON 75 — how the agent learns from human traces: extract structure, never copy (2026-11-24)

ISAIAH'S AIM (verbatim): "the human trace supplies the head start, the agent extracts the structure
itself, and the ground is the only judge. It never supplies the composition. This is what I care
about." He confirmed the public replays are free to use for training (competition closed, open source)
and asked to proceed.

## QUESTION
How should the agent turn a human replay into reasoning it can compose with, without copying the
human's composition? What is settled by the figures, and what must be decided before building?

## SEARCHED — sources read this turn
- The 25 human replays are ALREADY in the repo: replays/<game>_human.ndjson, all 25 readable by
  reverse_engineer.load_replay; r11l 168 steps, ar25 578, wa30 1565. No download needed.
- A step carries keys: action_id, avail, frames, grid, level, state, xy. `grid` is the 64x64 board.
  `action_id` is the human's action. The feeder already reads these.
- trace_extract.py (new, seat-side, read-only) records each frame-to-frame effect (cells changed,
  bounding box) and whether an effect followed one. Measured on cd82: 136 steps, 126 with an effect.

## DERIVATION (figures, verbatim)
- Fig 4: "Only methods cross up. Only head starts come down" / "a head start, never a recording".
  The human trace may cross down only as a head start; the agent extracts the method itself.
- Fig 12: "where the arrangement is recorded, re-deriving it is a lookup and the actions were spent
  once." Structure the agent derives is kept; a copy of the human's route is not.
- Fig 2: "Each frame is corrected by it separately" — the ground alone settles a prediction.
- Fig 8: "searchers drawing on the same evidence are one searcher wearing many names" — independent
  sources decide whether agreement means anything.
- Fig 10: "The residual selects the members, but only from what is available. A candidate set chosen
  by a participant is an authored room however well the selection is reasoned." So the proctor must
  not choose which candidates the agent weighs.

## WORLD (secondary, primary sources read this turn)
- Apprenticeship via inverse reinforcement learning (Abbeel & Ng, 2004): the learner infers the
  reward/goal structure behind an expert's behaviour rather than copying the expert's actions.
  Directly supports "extract structure, not composition".
- Animal culture (Wikipedia, citing Whiten's chimpanzees and field studies): transmission is
  selective; chimpanzees copy successful and higher-status models; "the 'zone of latent solutions'
  hypothesis" says many behaviours are individually reinvented and social learning shapes their
  frequency rather than transmitting the behavioural form. Supports selective weighting over
  wholesale imitation, with the ground's outcome as the "status".
- Teaching in animals (ant tandem running, orca beaching): highest-fidelity transfer, and the
  teacher changes behaviour to suit the naive learner. The agent analogue is a head start whose
  structure the learner still rebuilds.

## VERDICT
The method that satisfies Isaiah's aim and the figures is:
1. the human trace is an observation, not an answer: the agent infers the dependency structure
   behind the human's effect, as IRL infers a reward, and does not copy the action string;
2. dependencies that recur across independent sources are kept; a route seen once is provisional;
3. the agent's own mints are checked by the ground on held-out effects, so no composition is supplied;
4. the proctor supplies means and the ground, never the candidates or a per-chunk hint.

Status: step 0 (extraction) is built and measured on cd82. The inference of dependency structure and
the cross-trace weighting are NOT built. Two decisions are required before they can be, because they
change what a dependency and a held prediction mean, and choosing them after seeing results would be
tuning rather than learning:
- D1: what counts as an independent trace, and the cross-game threshold for agreement;
- D2: what counts as a held prediction on the ground (does a partial match, right object wrong order,
  move the weight?).

A measured caution on the extraction: cd82's first effect is a change at grid cell [63,63], the HUD
score counter, not the mechanic. The Phase 2 design already names HUD-vs-playfield separation as the
first buildable piece. The extractor's raw effects must be filtered to the playfield before any
dependency is inferred, or the agent will learn the score counter.

FIGURE CENSUS: Fig 2 · Fig 4 · Fig 8 · Fig 10 · Fig 12 (verbatim). Strained: none.
Anchor: replays/*_human.ndjson (25 files); reverse_engineer.load_replay; trace_extract.py measured
cd82 136 steps/126 effects; Abbeel & Ng 2004; animal-culture primary source.
