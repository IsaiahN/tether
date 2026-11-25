WATSON 77 — the HUD/playfield filter is not a row band (2026-11-24)

Assumption tested: WATSON 75/76 said playfield filtering was owed before dependency inference,
because cd82's first extracted effect was a one-cell change at grid [63,63], read as the HUD score
counter. I measured where changes actually occur across the human replays before cropping anything.

## MEASUREMENT (probe_hud.py, read-only)
For each game, every consecutive frame transition, count changed cells by row.
- cd82 (136 steps, 16,473 changed cells): most-changed rows 25-37 (row 31: 778). Bottom 4 rows
  (60-63): 153 changes = 0.9%. Row 63 alone: 0.9%.
- ar25 (577 steps, 138,811 changes): most-changed rows 18-32. Bottom 4 rows: 1.5%. Row 63: 0.0%.
- r11l (167 steps, 16,264 changes): most-changed rows 28-45. Bottom 4 rows: 3.2%. Row 63: 0.9%.

## VERDICT
There is no persistent HUD band. A fixed crop of rows 60-63 would discard real mechanic changes and
would not even capture cd82's first effect reliably. The [63,63] change was a one-off early event,
not a score-counter region. So the filter cannot be a row band.

This leaves one design choice unresolved: what counts as ONE effect. The extractor currently records
a bounding box of changed cells per transition, which can mix an avatar move, a score tick and a
world change. The invariant-core rule (WATSON 76 D1) needs a stable effect identity across traces,
and that depends on this choice. I will not silently embed a partition of the frame into
"mechanic vs display" — Fig 10's rule: "a candidate set chosen by a participant is an authored room
however well the selection is reasoned."

## WHAT IS NEEDED (one decision, D3)
D3: what counts as one effect in a frame transition? Options a user could elaborate on:
- one effect per connected component of changed cells (spatially contiguous moves);
- one effect per colour change, regardless of position;
- one effect per distinct (colour, region) pair the human's action produced;
- coarse: the whole frame's change as one signature (what the probe already does).
This decides the unit that the invariant-core count operates on, so it must be fixed before the
inference, like D1/D2 were. It is not a number to tune after seeing results.

FIGURE CENSUS: Fig 10 (verbatim, verified in WATSON 76). Strained: none.
Anchor: probe_hud.py measured on cd82/ar25/r11l replays; trace_extract.py effect rows.
