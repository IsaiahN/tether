# The frozen vocabulary — 2026-09-14

**Reviewer-mandated precondition (REVIEWER-STANDING, 2026-09-14):** *freeze the vocabulary before
the first mapping, dated. Once a human-panel solution is mapped onto the atom set, every later
addition is suspect, because the natural next sentence is "this game needs an attribute we do not
have" — which is the forbidden move arriving as completeness. With a frozen vocabulary an
expressibility failure is a finding; without one it is a shopping list.*

**This freezes the agent's atom set and perceptual reach AS OF 2026-09-14.** Any atom or attribute
added after this date is dated and audited against this baseline. The per-game reverse-engineering
answer key (docs/TRAINING_PLAN.md §13) is written ONLY in what appears below; a chunk that cannot
be expressed in it is recorded as an inexpressibility finding in the demand-ranked gap log — never
a reason to add to this set. Perception grows only by accumulated cross-game demand, re-derived at
threshold, never to close one game's key gap.

---

## Source of truth

- `arc_atoms.py` — sha256 prefix **`3f85bced6ea04a5f`** (freeze fingerprint; a change here means the
  vocabulary changed).

## The atom set — 45 discoverable atoms

**Perceptual extractors (8) — what the agent reads off each object (`ATTRIBUTE_TYPE`):**
`colour` · `row` · `col` · `h` · `w` · `drow` · `dcol` · `shape`

(Code-evidence note: the plan text said "5 attributes"; the code exposes **8** granular keys —
`row`/`col` are position, `h`/`w` are extent, `drow`/`dcol` are the per-frame delta, plus `colour`
and `shape`. Frozen as 8.)

**Relation (1):** `touching`

**Composed / derived atoms (36):**
`above` · `abs_delta` · `aligned` · `all` · `all_same` · `any` · `any_same` · `area` · `bbox_area`
· `both` · `canonical` · `centroid` · `corners` · `count` · `distinct` · `either` · `holes` ·
`is_max` · `is_min` · `is_mode` · `is_square` · `negate` · `none` · `none_same` · `orbit_size` ·
`other` · `parity` · `perimeter` · `rank_in` · `reflect` · `rotate` · `same` · `sign` · `sum_group`
· `symmetric` · `touching_n`

## The admission partition (from `arc_atoms.ADMITTED`) — the ablation must keep these apart

- **Named by the machinery** (`arc_predict.unexpressible()` or §12.4's worked examples), the
  legitimate reaches: `rotate` · `reflect` · `count` · `holes` · `parity` · `centroid` ·
  `touching_n` · `area`.
- **Named `ON DEPTH` by a measurement the proctor ran** (a sweep priced them), a weaker
  provenance the ablation must be able to isolate: `bbox_area` · `perimeter` · `corners` ·
  `orbit_size` · `canonical` · `symmetric` · `is_square` · `rank_in` · `is_max` · `is_min` ·
  `sum_group` · `distinct` · `is_mode` · `aligned` · `abs_delta` · `sign`.
- **Named by a structural absence** (the set had ∀/∃/¬∃ and no connectives): `negate` · `both` ·
  `either`.

## What is NOT here (the perceptual ceiling, per `ATTRIBUTE_REACH`)

Only these 8 attributes + `touching` are grounded. `ATTRIBUTE_REACH` records ~1,749 further atoms
gated behind a single scalar-emitting sensor, and most of the ~70 relations in `RELATIONS.md` are
uncomposable today. **A chunk needing any of those is an inexpressibility finding, logged with the
gap (evidence) and a candidate fix (hypothesis) in separate fields — not built here.**
