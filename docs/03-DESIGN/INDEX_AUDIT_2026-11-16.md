# INDEX AUDIT, 2026-11-16 (build sequence step 5, second half)

The step: *"audit the index, every entry against its source, and fix filings that point at the
wrong described effect"* (docs/04-PLANS_AHEAD/02-BUILD_SEQUENCE_FUTURE_STATE.md, step 5).

**Instrument:** `conform/index_audit.py`, read-only, about 1 s. **World:** the library files in
`library/` (given.json, index.json) at `development` 40c5eb2. **Population:** every filing in
index.json: one (map, value, key) posting, 96,826 of them over 13 posting maps. **Arm state:** none.
This is a file audit; no agent ran.

## What a filing is, and the classes

A filing is one posting: `index.by_reading_affects["gone"]` lists `ADHERENCE|Unbreakable`, so the
entry is filed as PRODUCING `gone`. That map is the **described effect**: `Library.produces` (the
abductive lookup) reads it, and `default_role` makes an entry PROCESS rather than STATE because it
has `affects`. The build derives `affects` by running `AFFECT_VERBS` (verb stems) over the entry's
grid meaning (`@grounding`, a SOURCE field), or for a molecule over its definition plus its
operands' affects.

| class | meaning |
|---|---|
| OK | the source entry declares it |
| ORPHAN | the key names no entry in given.json |
| STALE | index and entry disagree: the entry's field, or the build's rule re-run on the SOURCE text, no longer gives the filing, or the entry declares a value the index lacks |
| MISFILED | every phrase in the source that produced the filing is NEGATED in its own clause, or is a word that is not the effect (the noun "appearance"/"passage"; "turns" as the time step under the greedy `turn .* colour`). A molecule's filing is MISFILED when every route (its definition, each operand's filing) is MISFILED |
| QUESTIONED | the only producing phrase is a TRIGGER ("deforms *when pushed*") or a HYPOTHETICAL ("an object *would* fall"). A judgement call: not changed, listed for Isaiah |

The structural maps (by_reading_reads with weights, by_tag, by_grid_term, by_substrate, by_kind,
by_domain, by_attribute plus name_match, ingredient_of, by_default_role, and the tag section's
by_tag / by_pair / by_attribute) are checked both ways for ORPHAN and STALE against the entry's
declared field. The semantic test (MISFILED / QUESTIONED) runs on by_reading_affects and is
carried to by_default_role: a PROCESS default with no role_of, no MEASURE meaning and only
MISFILED affects is MISFILED (it should be STATE).

## Result

- **ORPHAN 0, STALE 0** across all 13 maps. Every posting points at an entry that exists, and every
  entry's declared fields match its postings in both directions. That agrees with
  `build_library.py --check`: the index is reproduced from its sources byte for byte.
- **MISFILED 142** before the fix: 104 by_reading_affects filings and 38 PROCESS role defaults.
  They come from **32 source phrases** (atom groundings and molecule definitions). The other
  filings are molecules that inherited the effect from an operand.
- **QUESTIONED 253** (196 affects plus 57 role defaults). Not changed; listed below for Isaiah.

## The fix (through the builder, not by hand)

`library/build_library.py` `_affects` now skips a verb match its own description denies:
`_declares()` plus the data tables `AFFECT_NEGATOR`, `AFFECT_CLAUSE_END`, `AFFECT_NEG_REACH = 6`,
`AFFECT_NOT_A_NEGATOR` and `AFFECT_NOT_THE_EFFECT`. It skips a verb negated in its own clause
within 6 words, and it skips a stem that caught a noun. Triggers and hypotheticals are NOT skipped.
Then the library was rebuilt with `python -B library/build_library.py`.

| | before | after |
|---|---|---|
| by_reading_affects filings removed | | **104** (no filing added) |
| by_default_role PROCESS -> STATE | | **38** |
| by_substrate filings removed (substrate is derived from reads + affects) | | 6 |
| entries changed (only the DERIVED fields `affects` 67, `roles` 57, `substrate` 6) | | 67 |
| audit: MISFILED / QUESTIONED / ORPHAN / STALE | 142 / 253 / 0 / 0 | **0 / 253 / 0 / 0** |
| `build_library.py --check` | OK | **OK** (derived files reproduced, A3 no SOURCE field touched, S1 DB rows, tether_rules sha) |

New sha256 values (old values in brackets):
- given.json `5eac44b774cb3c103799beb6daf1fc811d55821de6aa7f5d5ce7655ca5913098` (`d5d4e063d3c7575f593f78d5db49cb6cbc6f6073b78097ab93fba4b24531c034`)
- index.json `33ff6214835149cb9c875e45537a467f9dcc03423c8a8e9915942bdc379a1a5a` (`154a9fdcfad966376da37f275ee717c694c61f7ad63b57e788489ccea30342bf`)
- frame.json, BUILD_REPORT.md and MANIFEST.md are unchanged. tether_rules.json still matches its
  approved sha.

Other tests run after the fix: `pytest tests/test_compile.py tests/test_cue_key_path.py
tests/test_cards_v4.py tests/test_attribute_index_path.py` passed 7 of 7, and the
`library/library_runtime.py` self-test reported 0 failures. `conform/libagree.py` reports 13
findings, the same 13 at the base commit 40c5eb2. They are about agent-atom arms, and libagree does
not read affects or roles. `ruff check .` passes.

**Is the post-fix zero independent evidence? No.** The builder's guard and the audit's MISFILED
test use the same phrase rules, written twice and kept apart (the audit does not import the
build's guard). So after the fix, MISFILED 0 only shows that the guard ran. The independent
evidence is the list below, where every source phrase was read by hand before the fix. Two
false positives found that way were removed from the rule before anything was fixed:
`HUMAN|Support` ("an object with nothing below it falls": it does fall) and
`ONTOLOGICAL|Void contemplate` ("the nothing from which being emerges": "nothing" is a noun
there). **What the audit cannot see:** an effect a stem misses, and a wrong filing whose phrase is
affirmed (see "for Isaiah", part 2).

**Behaviour:** the agent reads `affects` through `Library.produces` (under the abduce arm) and
through the role views (the default role, and PROCESS candidates drawn from `affects`). The 38
entries above now default to STATE, and 104 abductive postings are gone. That is a change to what
the agent can look up, and it is confined to entries whose own description says the effect does
not happen.

---

# For Isaiah

## Part 1. QUESTIONED filings (judgement calls, left as filed)

Each one rests only on a trigger or a hypothetical. Example: "an object that deforms when pushed"
is filed as producing `drow/dcol` because of *pushed*, which is what happens TO it. "An object would
fall" and "how many ways an object can move" describe a capacity, not an effect. Whether a
capacity or the effect that triggers an entry should be filed as its described effect is a ruling
about what `by_reading_affects` means, so it is not decided here. The full list is in the
QUESTIONED table below.

## Part 2. Affirmed phrases that look wrong (not counted by the audit, not changed)

The audit counted these OK, because the verb is affirmed. A reader may still judge the filing
wrong. Seen while reading the stem census, not an exhaustive list:

- `ACOUSTIC|Absorption` (molecule): "Reduces reflections" files `shape/dholes/dperimeter` through
  the stem `reflect`, which is sound reflection, not a mirrored outline.
- `CURIOSITY|Urge`: "the pull toward an untested action" files `drow/dcol`; the pull is a
  metaphor.
- `CURIOSITY|Systematic`: "trying actions or cells in a complete order" files `completed`;
  "complete" is an adjective there.
- `LINEAGE|Fruit`: "the product at the end of a chain of changes" files `came` through `produc`.
- `ACOUSTIC|Medium` and others: "a change travels" files `drow/dcol`
  (object motion) for a change that propagates; `spread` (`colour_changed/dcells`) may be the
  described effect instead.
- `ACTION|Exertion`: "the cost of an action: actions spent, or cells moved" is a measure, filed as
  producing motion.
- `ATMOSPHERIC|Nutrients`, `PATHOLOGICAL|Mortality` and the other `can ...` entries are in Part 1.

Each one would need a word-sense rule, or a SOURCE edit to the grounding. Either is a ruling, not a
plain fix.

---

# The tables (generated by `python conform/index_audit.py --md`, BEFORE the fix)

Molecules whose evidence reads `operand X: MISFILED` inherited the filing. Their own definition
did not say it.

### Counts, per map (every filing, one class each)

| map | OK | MISFILED | QUESTIONED | ORPHAN | STALE |
|---|---|---|---|---|---|
| by_attribute | 8285 | 0 | 0 | 0 | 0 |
| by_default_role | 3953 | 38 | 57 | 0 | 0 |
| by_domain | 4048 | 0 | 0 | 0 | 0 |
| by_grid_term | 2371 | 0 | 0 | 0 | 0 |
| by_kind | 4048 | 0 | 0 | 0 | 0 |
| by_reading_affects | 4508 | 104 | 196 | 0 | 0 |
| by_reading_reads | 10368 | 0 | 0 | 0 | 0 |
| by_substrate | 15099 | 0 | 0 | 0 | 0 |
| by_tag | 8002 | 0 | 0 | 0 | 0 |
| ingredient_of | 6452 | 0 | 0 | 0 | 0 |
| tag.by_attribute | 8285 | 0 | 0 | 0 | 0 |
| tag.by_pair | 5772 | 0 | 0 | 0 | 0 |
| tag.by_tag | 15240 | 0 | 0 | 0 | 0 |
| **all** | **96431** | **142** | **253** | **0** | **0** |

### ORPHAN (0)

None.

### STALE (0)

None.

### MISFILED (142)

| map | filed under | entry | evidence |
|---|---|---|---|
| by_default_role | PROCESS | ACOUSTIC\|Acoustic holography | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | ACOUSTIC\|Phased array | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | ADHERENCE\|Loyal stay | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | ADHERENCE\|Resist | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | ADHERENCE\|Unbreakable | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | ATMOSPHERIC\|No Precipitation | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | ATMOSPHERIC\|Stationary | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | CHARACTER\|Authenticity | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | CHEMICAL\|barrier | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | CURIOSITY\|Suspense | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | DESIRE\|Loss Control | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | DESIRE\|The desire fire | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | ECONOMIC\|Adverse selection | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | ECONOMIC\|hidden type | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | EMOTION\|Conservation | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | EXCHANGE\|Unfulfilled | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | LINEAGE\|Immortality | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | LINGUISTIC\|Homonymy | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | LINGUISTIC\|Unrelated Meanings | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | LUDOLOGICAL\|Implicit Rule | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | MECHANICAL\|one-way | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | MEDICAL\|Immunity | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | MEDICAL\|The immune system | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | NOETIC\|Mindful decision | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | NOETIC\|Stillness | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | NOETIC\|Sustained single focus | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | NUTRITIONAL\|Starvation response | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | ONTOLOGICAL\|Illusion | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | ONTOLOGICAL\|Illusion pierce | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | ONTOLOGICAL\|The illusion network | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | OPTICAL\|Opacity | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | OPTICAL\|Shadow | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | PHENOMENOLOGICAL\|Phenomenal reduction | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | PHENOMENOLOGICAL\|The meaning given | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | REBELLION\|Non-Violence | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | REBELLION\|Passive resistance | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | REBELLION\|non-violence | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_default_role | PROCESS | ZOOLOGICAL\|Immobile | PROCESS rests only on affects filings that are ['MISFILED']; with none it is STATE |
| by_reading_affects | dcol | ACOUSTIC\|Phased array | definition NEGATED 'without ... moving' in one clause -- "...d phase delays. Steers the beam without moving parts." |
| by_reading_affects | drow | ACOUSTIC\|Phased array | definition NEGATED 'without ... moving' in one clause -- "...d phase delays. Steers the beam without moving parts." |
| by_reading_affects | dcol | ADHERENCE\|Resist | grounding NEGATED 'not ... move' in one clause -- "an object that does not move or change when pushed or clic"; grounding NEGATED 'not ... pushed' in one clause -- "...bject that does not move or change when pushed or clicked" |
| by_reading_affects | drow | ADHERENCE\|Resist | grounding NEGATED 'not ... move' in one clause -- "an object that does not move or change when pushed or clic"; grounding NEGATED 'not ... pushed' in one clause -- "...bject that does not move or change when pushed or clicked" |
| by_reading_affects | gone | ADHERENCE\|Unbreakable | grounding NEGATED 'no ... remove' in one clause -- "an object no action can change or remove" |
| by_reading_affects | came | AESTHETIC\|Visible affordance | definition NOT_THE_EFFECT 'appearance' is a noun, not the effect -- "a thing's appearance says what can be done wit" |
| by_reading_affects | came | ATMOSPHERIC\|No Precipitation | grounding NEGATED 'nothing ... appears' in one clause -- "nothing falls or appears from above" |
| by_reading_affects | dcol | ATMOSPHERIC\|No Precipitation | grounding NEGATED 'nothing ... falls' in one clause -- "nothing falls or appears from above" |
| by_reading_affects | drow | ATMOSPHERIC\|No Precipitation | grounding NEGATED 'nothing ... falls' in one clause -- "nothing falls or appears from above" |
| by_reading_affects | dcol | ATMOSPHERIC\|Stationary | grounding NEGATED 'not ... moving' in one clause -- "not moving between turns" |
| by_reading_affects | drow | ATMOSPHERIC\|Stationary | grounding NEGATED 'not ... moving' in one clause -- "not moving between turns" |
| by_reading_affects | came | CHARACTER\|Authenticity | grounding NOT_THE_EFFECT 'appearance' is a noun, not the effect -- "an object whose appearance matches its behaviour" |
| by_reading_affects | colour_changed | CHEMICAL\|barrier | grounding NOT_THE_EFFECT 'passage' is a noun, not the effect -- "a wall that blocks passage" |
| by_reading_affects | dcells | CHEMICAL\|barrier | grounding NOT_THE_EFFECT 'passage' is a noun, not the effect -- "a wall that blocks passage" |
| by_reading_affects | came | CURIOSITY\|Suspense | grounding NEGATED 'not ... appeared' in one clause -- "a predicted change that has not yet appeared: the prediction differs fro" |
| by_reading_affects | dcol | DESIRE\|Loss Control | grounding NEGATED 'no ... moving' in one clause -- "the agent's actions no longer moving what it intends" |
| by_reading_affects | drow | DESIRE\|Loss Control | grounding NEGATED 'no ... moving' in one clause -- "the agent's actions no longer moving what it intends" |
| by_reading_affects | dcol | DESIRE\|The desire fire | definition NEGATED 'no ... movement' in one clause -- "...e fire of life. Without it, there is no movement." |
| by_reading_affects | drow | DESIRE\|The desire fire | definition NEGATED 'no ... movement' in one clause -- "...e fire of life. Without it, there is no movement." |
| by_reading_affects | came | ECONOMIC\|hidden type | grounding NOT_THE_EFFECT 'appearance' is a noun, not the effect -- "...ject whose kind is not visible from its appearance" |
| by_reading_affects | colour | EMOTION\|Conservation | grounding NOT_THE_EFFECT 'turn' is the time step, not a recolour (greedy `turn .* colour`) -- "a total that stays the same across turns (cells of a colour, object count)" |
| by_reading_affects | colour_changed | EMOTION\|Conservation | grounding NOT_THE_EFFECT 'turn' is the time step, not a recolour (greedy `turn .* colour`) -- "a total that stays the same across turns (cells of a colour, object count)" |
| by_reading_affects | completed | EXCHANGE\|Unfulfilled | grounding NEGATED 'not ... completed' in one clause -- "an exchange started and not completed" |
| by_reading_affects | came | HUMAN\|Recolour | definition NOT_THE_EFFECT 'appearance' is a noun, not the effect -- "appearance changes, identity does no" |
| by_reading_affects | gone | LINEAGE\|Immortality | grounding NEGATED 'never ... removed' in one clause -- "an object never removed" |
| by_reading_affects | came | LINGUISTIC\|Unrelated Meanings | grounding NOT_THE_EFFECT 'appearance' is a noun, not the effect -- "the same appearance for unrelated roles" |
| by_reading_affects | dcol | LUDOLOGICAL\|Implicit Rule | grounding NEGATED 'never ... falls' in one clause -- "...ys holding: a rule whose standing never falls" |
| by_reading_affects | drow | LUDOLOGICAL\|Implicit Rule | grounding NEGATED 'never ... falls' in one clause -- "...ys holding: a rule whose standing never falls" |
| by_reading_affects | dholes | MATERIAL\|Brittle failure | definition NEGATED 'no ... deformation' in one clause -- "...ness shatters instantly with no plastic deformation (glass, ceramic)." |
| by_reading_affects | dperimeter | MATERIAL\|Brittle failure | definition NEGATED 'no ... deformation' in one clause -- "...ness shatters instantly with no plastic deformation (glass, ceramic)." |
| by_reading_affects | shape | MATERIAL\|Brittle failure | definition NEGATED 'no ... deformation' in one clause -- "...ness shatters instantly with no plastic deformation (glass, ceramic)." |
| by_reading_affects | colour_changed | MECHANICAL\|one-way | grounding NOT_THE_EFFECT 'passage' is a noun, not the effect -- "passage allowed in one direction o" |
| by_reading_affects | dcells | MECHANICAL\|one-way | grounding NOT_THE_EFFECT 'passage' is a noun, not the effect -- "passage allowed in one direction o" |
| by_reading_affects | colour_changed | MEDICAL\|Immunity | grounding NEGATED 'not ... spreading' in one clause -- "an object not affected by a spreading change" |
| by_reading_affects | dcells | MEDICAL\|Immunity | grounding NEGATED 'not ... spreading' in one clause -- "an object not affected by a spreading change" |
| by_reading_affects | gone | NOETIC\|Mindful decision | definition NEGATED 'without ... attachment' in one clause -- "... a decision with full presence, without attachment to the outcome." |
| by_reading_affects | touching | NOETIC\|Mindful decision | definition NEGATED 'without ... attachment' in one clause -- "... a decision with full presence, without attachment to the outcome." |
| by_reading_affects | dcol | NOETIC\|Stillness | grounding NEGATED 'nothing ... moving' in one clause -- "nothing moving" |
| by_reading_affects | drow | NOETIC\|Stillness | grounding NEGATED 'nothing ... moving' in one clause -- "nothing moving" |
| by_reading_affects | came | ONTOLOGICAL\|Illusion | grounding NOT_THE_EFFECT 'appearance' is a noun, not the effect -- "an appearance that does not match behav" |
| by_reading_affects | came | ONTOLOGICAL\|The Plato cave | operand ONTOLOGICAL\|Illusion: MISFILED; definition NOT_THE_EFFECT 'appearances' is a noun, not the effect -- "A false reality where agents mistake appearances for truth. The myth of t" |
| by_reading_affects | colour_changed | OPTICAL\|Opacity | grounding NEGATED 'cannot ... pass' in one clause -- "an object a beam cannot pass through" |
| by_reading_affects | dcells | OPTICAL\|Opacity | grounding NEGATED 'cannot ... pass' in one clause -- "an object a beam cannot pass through" |
| by_reading_affects | came | PHENOMENOLOGICAL\|Phenomenal reduction | definition NOT_THE_EFFECT 'appearance' is a noun, not the effect -- "...ature of an object to focus on its pure appearance (the epoché)." |
| by_reading_affects | colour_changed | PHENOMENOLOGICAL\|The meaning given | definition NEGATED 'not ... passively' in one clause -- "The world is not passively perceived; it is activel" |
| by_reading_affects | dcells | PHENOMENOLOGICAL\|The meaning given | definition NEGATED 'not ... passively' in one clause -- "The world is not passively perceived; it is activel" |
| by_reading_affects | gone | REBELLION\|Non-Violence | grounding NEGATED 'without ... removing' in one clause -- "reaching the goal without removing objects" |
| by_reading_affects | gone | REBELLION\|non-violence | grounding NEGATED 'without ... removal' in one clause -- "progress without removal" |
| by_reading_affects | dcol | ZOOLOGICAL\|Immobile | grounding NEGATED 'never ... moves' in one clause -- "never moves" |
| by_reading_affects | drow | ZOOLOGICAL\|Immobile | grounding NEGATED 'never ... moves' in one clause -- "never moves" |
| by_reading_affects | dholes | ZOOLOGICAL\|The wild self | definition NEGATED 'not ... reflective' in one clause -- "...ned by ecological relationships, not by reflective thought." |
| by_reading_affects | dperimeter | ZOOLOGICAL\|The wild self | definition NEGATED 'not ... reflective' in one clause -- "...ned by ecological relationships, not by reflective thought." |
| by_reading_affects | shape | ZOOLOGICAL\|The wild self | definition NEGATED 'not ... reflective' in one clause -- "...ned by ecological relationships, not by reflective thought." |
| by_reading_affects | dcol | ACOUSTIC\|Acoustic holography | operand ACOUSTIC\|Phased array: MISFILED |
| by_reading_affects | drow | ACOUSTIC\|Acoustic holography | operand ACOUSTIC\|Phased array: MISFILED |
| by_reading_affects | dcol | ADHERENCE\|Loyal stay | operand ADHERENCE\|Resist: MISFILED |
| by_reading_affects | drow | ADHERENCE\|Loyal stay | operand ADHERENCE\|Resist: MISFILED |
| by_reading_affects | gone | ADHERENCE\|The iron vow | operand ADHERENCE\|Unbreakable: MISFILED |
| by_reading_affects | came | ATMOSPHERIC\|Drought | operand ATMOSPHERIC\|No Precipitation: MISFILED |
| by_reading_affects | came | CHARACTER\|Authentic act | operand CHARACTER\|Authenticity: MISFILED |
| by_reading_affects | came | CHARACTER\|Authenticity break | operand CHARACTER\|Authenticity: MISFILED |
| by_reading_affects | came | CHARACTER\|Authenticity struggle | operand CHARACTER\|Authenticity: MISFILED |
| by_reading_affects | came | CHARACTER\|The authentic self | operand CHARACTER\|Authenticity: MISFILED |
| by_reading_affects | colour_changed | CHEMICAL\|Selective transport | operand CHEMICAL\|barrier: MISFILED |
| by_reading_affects | dcells | CHEMICAL\|Selective transport | operand CHEMICAL\|barrier: MISFILED |
| by_reading_affects | came | CURIOSITY\|Mystery maintenance | operand CURIOSITY\|Suspense: MISFILED |
| by_reading_affects | came | ECONOMIC\|Adverse selection | operand ECONOMIC\|hidden type: MISFILED |
| by_reading_affects | colour | EMOTION\|Sad withdrawal | operand EMOTION\|Conservation: MISFILED |
| by_reading_affects | colour_changed | EMOTION\|Sad withdrawal | operand EMOTION\|Conservation: MISFILED |
| by_reading_affects | completed | EXCHANGE\|The unpaid debt | operand EXCHANGE\|Unfulfilled: MISFILED |
| by_reading_affects | came | HUMAN\|Camouflage | operand HUMAN\|Recolour: MISFILED |
| by_reading_affects | came | HUMAN\|Transfigure | operand HUMAN\|Camouflage: MISFILED |
| by_reading_affects | came | HUMAN\|Uncamouflage | operand HUMAN\|Recolour: MISFILED |
| by_reading_affects | came | KINETIC\|Stalk | operand HUMAN\|Camouflage: MISFILED |
| by_reading_affects | came | LINGUISTIC\|Homonymy | operand LINGUISTIC\|Unrelated Meanings: MISFILED |
| by_reading_affects | dcol | LUDOLOGICAL\|Ruleset | operand LUDOLOGICAL\|Implicit Rule: MISFILED |
| by_reading_affects | drow | LUDOLOGICAL\|Ruleset | operand LUDOLOGICAL\|Implicit Rule: MISFILED |
| by_reading_affects | dcol | LUDOLOGICAL\|The game itself | operand LUDOLOGICAL\|Ruleset: MISFILED |
| by_reading_affects | drow | LUDOLOGICAL\|The game itself | operand LUDOLOGICAL\|Ruleset: MISFILED |
| by_reading_affects | colour_changed | MECHANICAL\|Accumulator | operand MECHANICAL\|Ratchet: MISFILED |
| by_reading_affects | dcells | MECHANICAL\|Accumulator | operand MECHANICAL\|Ratchet: MISFILED |
| by_reading_affects | colour_changed | MECHANICAL\|Escapement | operand MECHANICAL\|Ratchet: MISFILED |
| by_reading_affects | dcells | MECHANICAL\|Escapement | operand MECHANICAL\|Ratchet: MISFILED |
| by_reading_affects | colour_changed | MECHANICAL\|Governor | operand MECHANICAL\|Escapement: MISFILED |
| by_reading_affects | dcells | MECHANICAL\|Governor | operand MECHANICAL\|Escapement: MISFILED |
| by_reading_affects | colour_changed | MECHANICAL\|Programmable device | operand MECHANICAL\|Escapement: MISFILED |
| by_reading_affects | dcells | MECHANICAL\|Programmable device | operand MECHANICAL\|Escapement: MISFILED |
| by_reading_affects | colour_changed | MECHANICAL\|Ratchet | operand MECHANICAL\|one-way: MISFILED |
| by_reading_affects | dcells | MECHANICAL\|Ratchet | operand MECHANICAL\|one-way: MISFILED |
| by_reading_affects | colour_changed | MEDICAL\|Autoimmune | operand MEDICAL\|Immunity: MISFILED |
| by_reading_affects | dcells | MEDICAL\|Autoimmune | operand MEDICAL\|Immunity: MISFILED |
| by_reading_affects | colour_changed | MEDICAL\|Immunotherapy | operand MEDICAL\|Immunity: MISFILED |
| by_reading_affects | colour_changed | MEDICAL\|The immune system | operand MEDICAL\|Immunity: MISFILED |
| by_reading_affects | dcells | MEDICAL\|The immune system | operand MEDICAL\|Immunity: MISFILED |
| by_reading_affects | dcol | NOETIC\|Sustained single focus | operand NOETIC\|Stillness: MISFILED |
| by_reading_affects | drow | NOETIC\|Sustained single focus | operand NOETIC\|Stillness: MISFILED |
| by_reading_affects | colour | NUTRITIONAL\|Starvation response | operand EMOTION\|Conservation: MISFILED |
| by_reading_affects | colour_changed | NUTRITIONAL\|Starvation response | operand EMOTION\|Conservation: MISFILED |
| by_reading_affects | came | ONTOLOGICAL\|Ego illusion | operand ONTOLOGICAL\|Illusion: MISFILED |
| by_reading_affects | came | ONTOLOGICAL\|Illusion pierce | operand ONTOLOGICAL\|Illusion: MISFILED |
| by_reading_affects | came | ONTOLOGICAL\|The illusion network | operand ONTOLOGICAL\|Illusion: MISFILED |
| by_reading_affects | colour_changed | OPTICAL\|Shadow | operand OPTICAL\|Opacity: MISFILED |
| by_reading_affects | dcells | OPTICAL\|Shadow | operand OPTICAL\|Opacity: MISFILED |
| by_reading_affects | gone | REBELLION\|Passive resistance | operand REBELLION\|Non-Violence: MISFILED |

### QUESTIONED (253)

| map | filed under | entry | evidence |
|---|---|---|---|
| by_default_role | PROCESS | ACOUSTIC\|Aperture | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | ADHERENCE\|The stubborn soul | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | AESTHETIC\|Clarity | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | AESTHETIC\|Elegance | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | AESTHETIC\|Iconicity | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | AESTHETIC\|Visible affordance | PROCESS rests only on affects filings that are ['MISFILED', 'QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | ATMOSPHERIC\|Nutrients | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | AUTOMATON\|The programmer god | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | AUTOMATON\|The rule master | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | CELLULAR\|Plasmid | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | CELLULAR\|The gene trader | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | CHARACTER\|Identity | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | CHARACTER\|Narrative coherence | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | CHARACTER\|Self narrate | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | CHARACTER\|The authentic self | PROCESS rests only on affects filings that are ['MISFILED', 'QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | CHARACTER\|The integrated self | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | CHARACTER\|The narrative self | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | CHARACTER\|The shadow | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | CHEMICAL\|monomers | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | CONNECTION\|Hierarchy link | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | CURIOSITY\|The eternal asker | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | CURIOSITY\|The wondering soul | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | EMBODIMENT\|Efference sense | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | LARGE-SCALE\|Speed limit | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | LEARNING\|Metacognitive | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | LINEAGE\|Legacy | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | LINEAGE\|Legacy revision | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | LUDIC / ABSURDIST\|Gallows humor | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | LUDIC / ABSURDIST\|The ironist | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | MORPHOGENETIC\|French flag | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | MORPHOGENETIC\|Phenotypic plasticity | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | NETWORK\|The cluster | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | NOETIC\|Surrender control | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | NOETIC\|Surrender win | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | NUTRITIONAL\|Chemical Energy | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | ONTOLOGICAL\|No Base | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | ONTOLOGICAL\|The game is real | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | ONTOLOGICAL\|The real is sim | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | PATHOLOGICAL\|Cathartic expression | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | PATHOLOGICAL\|Dark night | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | PATHOLOGICAL\|Face death | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | PATHOLOGICAL\|Mortal awareness | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | PATHOLOGICAL\|Mortality | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | PATHOLOGICAL\|The cathartic purge | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | PATHOLOGICAL\|The eternal return | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | PATHOLOGICAL\|The suffering soul | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | REBELLION\|Counter culture | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | REBELLION\|Defiant selfhood | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | SKILL\|The skilled self | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | SOCIAL\|Subculture | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | SOMNIAL\|Catch-Up | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | SOMNIAL\|Lucid dream | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | THOUGHT\|Control | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | THOUGHT\|Metacognition | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | THOUGHT\|Simulate | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | TOPOLOGICAL\|Orientability | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_default_role | PROCESS | TRANSFORMATION\|Rebirth | PROCESS rests only on affects filings that are ['QUESTIONED']; with none it is STATE |
| by_reading_affects | colour_changed | ACOUSTIC\|Aperture | grounding HYPOTHETICAL 'can ... pass' -- "...dary object through which something can pass (a hole on the boundary)" |
| by_reading_affects | dcells | ACOUSTIC\|Aperture | grounding HYPOTHETICAL 'can ... pass' -- "...dary object through which something can pass (a hole on the boundary)" |
| by_reading_affects | colour_changed | ACOUSTIC\|Snell's law | definition TRIGGER 'when ... passing': what happens to it -- "Sound bends when passing between mediums of differe" |
| by_reading_affects | dcells | ACOUSTIC\|Snell's law | definition TRIGGER 'when ... passing': what happens to it -- "Sound bends when passing between mediums of differe" |
| by_reading_affects | dholes | AESTHETIC\|Clarity | grounding HYPOTHETICAL 'can ... split' -- "the board can be split cleanly into objects with no " |
| by_reading_affects | dperimeter | AESTHETIC\|Clarity | grounding HYPOTHETICAL 'can ... split' -- "the board can be split cleanly into objects with no " |
| by_reading_affects | shape | AESTHETIC\|Clarity | grounding HYPOTHETICAL 'can ... split' -- "the board can be split cleanly into objects with no " |
| by_reading_affects | dcells | ATMOSPHERIC\|Nutrients | grounding HYPOTHETICAL 'can ... grow' -- "cells an object can absorb to grow" |
| by_reading_affects | h | ATMOSPHERIC\|Nutrients | grounding HYPOTHETICAL 'can ... grow' -- "cells an object can absorb to grow" |
| by_reading_affects | w | ATMOSPHERIC\|Nutrients | grounding HYPOTHETICAL 'can ... grow' -- "cells an object can absorb to grow" |
| by_reading_affects | colour_changed | CELLULAR\|Plasmid | definition HYPOTHETICAL 'can ... transferred' -- "...mall, circular piece of DNA that can be transferred between bacteria." |
| by_reading_affects | dcells | CELLULAR\|Plasmid | definition HYPOTHETICAL 'can ... transferred' -- "...mall, circular piece of DNA that can be transferred between bacteria." |
| by_reading_affects | dcol | CHARACTER\|Identity | grounding TRIGGER 'despite ... moving': what happens to it -- "...ame object tracked across turns despite moving" |
| by_reading_affects | drow | CHARACTER\|Identity | grounding TRIGGER 'despite ... moving': what happens to it -- "...ame object tracked across turns despite moving" |
| by_reading_affects | gone | CHEMICAL\|monomers | grounding HYPOTHETICAL 'can ... joined' -- "identical small units that can be joined into a chain" |
| by_reading_affects | touching | CHEMICAL\|monomers | grounding HYPOTHETICAL 'can ... joined' -- "identical small units that can be joined into a chain" |
| by_reading_affects | dcol | EMBODIMENT\|Efference sense | definition TRIGGER 'if ... move': what happens to it -- "...sensory frame *should* feel like if you move your arm. If the world moves "; definition TRIGGER 'If ... moves': what happens to it -- "...like if you move your arm. If the world moves differently, you know an ext" |
| by_reading_affects | drow | EMBODIMENT\|Efference sense | definition TRIGGER 'if ... move': what happens to it -- "...sensory frame *should* feel like if you move your arm. If the world moves "; definition TRIGGER 'If ... moves': what happens to it -- "...like if you move your arm. If the world moves differently, you know an ext" |
| by_reading_affects | came | EMBODIMENT\|Self agency | definition TRIGGER 'If ... produces': what happens to it -- "...se that "I caused this." If your action produces the predicted outcome, agen" |
| by_reading_affects | colour_changed | HEAT\|combustible | grounding TRIGGER 'when ... spreading': what happens to it -- "...bject that is removed or changes when a spreading change reaches it" |
| by_reading_affects | dcells | HEAT\|combustible | grounding TRIGGER 'when ... spreading': what happens to it -- "...bject that is removed or changes when a spreading change reaches it" |
| by_reading_affects | dcol | KINETIC\|Articulation | grounding HYPOTHETICAL 'can ... move' -- "how many independent ways an object can move" |
| by_reading_affects | drow | KINETIC\|Articulation | grounding HYPOTHETICAL 'can ... move' -- "how many independent ways an object can move" |
| by_reading_affects | dcol | LARGE-SCALE\|Speed limit | grounding HYPOTHETICAL 'can ... travel' -- "a maximum number of cells a change can travel per turn" |
| by_reading_affects | drow | LARGE-SCALE\|Speed limit | grounding HYPOTHETICAL 'can ... travel' -- "a maximum number of cells a change can travel per turn" |
| by_reading_affects | gone | LINEAGE\|Legacy | grounding TRIGGER 'after ... removed': what happens to it -- "...t stays on the board after an object is removed" |
| by_reading_affects | colour_changed | LINGUISTIC\|Pragmatic inference | definition HYPOTHETICAL 'Can ... pass' -- "...rs meaning beyond the literal. "Can you pass the salt?" is a request, not " |
| by_reading_affects | dcells | LINGUISTIC\|Pragmatic inference | definition HYPOTHETICAL 'Can ... pass' -- "...rs meaning beyond the literal. "Can you pass the salt?" is a request, not " |
| by_reading_affects | dcol | MATERIAL\|Ductile | grounding TRIGGER 'when ... pushed': what happens to it -- "an object that stretches when pushed instead of breaking: its he" |
| by_reading_affects | drow | MATERIAL\|Ductile | grounding TRIGGER 'when ... pushed': what happens to it -- "an object that stretches when pushed instead of breaking: its he" |
| by_reading_affects | dcol | MATERIAL\|Elasticity | grounding TRIGGER 'when ... pushed': what happens to it -- "an object that deforms when pushed and returns to its shape" |
| by_reading_affects | drow | MATERIAL\|Elasticity | grounding TRIGGER 'when ... pushed': what happens to it -- "an object that deforms when pushed and returns to its shape" |
| by_reading_affects | dcol | MATERIAL\|Plasticity | grounding TRIGGER 'after ... push': what happens to it -- "an object that stays deformed after a push" |
| by_reading_affects | drow | MATERIAL\|Plasticity | grounding TRIGGER 'after ... push': what happens to it -- "an object that stays deformed after a push" |
| by_reading_affects | gone | MORPHOGENETIC\|Cell fate map | definition TRIGGER 'if ... disappears': what happens to it -- "...ntiation is stable even if the gradient disappears)." |
| by_reading_affects | came | MORPHOGENETIC\|Phenotypic plasticity | definition HYPOTHETICAL 'can ... produce' -- "The same genotype can produce different forms depending on" |
| by_reading_affects | gone | NUTRITIONAL\|Chemical Energy | grounding TRIGGER 'when ... consumed': what happens to it -- "...ed in an object and released when it is consumed" |
| by_reading_affects | dcol | ONTOLOGICAL\|No Base | grounding HYPOTHETICAL 'would ... fall' -- "nothing underneath (an object would fall)" |
| by_reading_affects | drow | ONTOLOGICAL\|No Base | grounding HYPOTHETICAL 'would ... fall' -- "nothing underneath (an object would fall)" |
| by_reading_affects | gone | PATHOLOGICAL\|Mortality | grounding HYPOTHETICAL 'can ... removed' -- "that the controlled object can be removed" |
| by_reading_affects | dcol | SOMNIAL\|Catch-Up | grounding TRIGGER 'after ... falling': what happens to it -- "closing a gap after falling behind" |
| by_reading_affects | drow | SOMNIAL\|Catch-Up | grounding TRIGGER 'after ... falling': what happens to it -- "closing a gap after falling behind" |
| by_reading_affects | dcol | THOUGHT\|Control | grounding HYPOTHETICAL 'able to ... move' -- "being able to move a value by acting" |
| by_reading_affects | drow | THOUGHT\|Control | grounding HYPOTHETICAL 'able to ... move' -- "being able to move a value by acting" |
| by_reading_affects | dcol | THOUGHT\|Simulate | definition TRIGGER 'if ... move': what happens to it -- "...ion of a possible situation. "What if I move this piece here?"" |
| by_reading_affects | drow | THOUGHT\|Simulate | definition TRIGGER 'if ... move': what happens to it -- "...ion of a possible situation. "What if I move this piece here?"" |
| by_reading_affects | dcol | TOPOLOGICAL\|Orientability | grounding TRIGGER 'when ... moved': what happens to it -- "...her an object keeps its handedness when moved around a loop" |
| by_reading_affects | drow | TOPOLOGICAL\|Orientability | grounding TRIGGER 'when ... moved': what happens to it -- "...her an object keeps its handedness when moved around a loop" |
| by_reading_affects | gone | TRANSFORMATION\|Rebirth | grounding TRIGGER 'after ... removal': what happens to it -- "an object reappearing after removal" |
| by_reading_affects | colour_changed | ACOUSTIC\|Helmholtz resonator | operand ACOUSTIC\|Aperture: QUESTIONED |
| by_reading_affects | dcol | ADHERENCE\|The stubborn soul | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | ADHERENCE\|The stubborn soul | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dholes | AESTHETIC\|Ambiguous figure | operand AESTHETIC\|Clarity: QUESTIONED |
| by_reading_affects | dperimeter | AESTHETIC\|Ambiguous figure | operand AESTHETIC\|Clarity: QUESTIONED |
| by_reading_affects | shape | AESTHETIC\|Ambiguous figure | operand AESTHETIC\|Clarity: QUESTIONED |
| by_reading_affects | dholes | AESTHETIC\|Clear edge | operand AESTHETIC\|Clarity: QUESTIONED |
| by_reading_affects | dperimeter | AESTHETIC\|Clear edge | operand AESTHETIC\|Clarity: QUESTIONED |
| by_reading_affects | shape | AESTHETIC\|Clear edge | operand AESTHETIC\|Clarity: QUESTIONED |
| by_reading_affects | dholes | AESTHETIC\|Elegance | operand AESTHETIC\|Clarity: QUESTIONED |
| by_reading_affects | dperimeter | AESTHETIC\|Elegance | operand AESTHETIC\|Clarity: QUESTIONED |
| by_reading_affects | shape | AESTHETIC\|Elegance | operand AESTHETIC\|Clarity: QUESTIONED |
| by_reading_affects | dholes | AESTHETIC\|Iconicity | operand AESTHETIC\|Clarity: QUESTIONED |
| by_reading_affects | dperimeter | AESTHETIC\|Iconicity | operand AESTHETIC\|Clarity: QUESTIONED |
| by_reading_affects | shape | AESTHETIC\|Iconicity | operand AESTHETIC\|Clarity: QUESTIONED |
| by_reading_affects | dholes | AESTHETIC\|Visible affordance | operand AESTHETIC\|Clarity: QUESTIONED |
| by_reading_affects | dperimeter | AESTHETIC\|Visible affordance | operand AESTHETIC\|Clarity: QUESTIONED |
| by_reading_affects | shape | AESTHETIC\|Visible affordance | operand AESTHETIC\|Clarity: QUESTIONED |
| by_reading_affects | dholes | AESTHETIC\|Visual hierarchy | operand AESTHETIC\|Clarity: QUESTIONED |
| by_reading_affects | dperimeter | AESTHETIC\|Visual hierarchy | operand AESTHETIC\|Clarity: QUESTIONED |
| by_reading_affects | shape | AESTHETIC\|Visual hierarchy | operand AESTHETIC\|Clarity: QUESTIONED |
| by_reading_affects | dcells | ATMOSPHERIC\|Sahara dust | operand ATMOSPHERIC\|Nutrients: QUESTIONED |
| by_reading_affects | h | ATMOSPHERIC\|Sahara dust | operand ATMOSPHERIC\|Nutrients: QUESTIONED |
| by_reading_affects | w | ATMOSPHERIC\|Sahara dust | operand ATMOSPHERIC\|Nutrients: QUESTIONED |
| by_reading_affects | dcol | AUTOMATON\|The programmer god | operand THOUGHT\|Control: QUESTIONED |
| by_reading_affects | drow | AUTOMATON\|The programmer god | operand THOUGHT\|Control: QUESTIONED |
| by_reading_affects | dcol | AUTOMATON\|The rule master | operand THOUGHT\|Control: QUESTIONED |
| by_reading_affects | drow | AUTOMATON\|The rule master | operand THOUGHT\|Control: QUESTIONED |
| by_reading_affects | colour_changed | CELLULAR\|The gene trader | operand CELLULAR\|Plasmid: QUESTIONED |
| by_reading_affects | dcells | CELLULAR\|The gene trader | operand CELLULAR\|Plasmid: QUESTIONED |
| by_reading_affects | dcol | CHARACTER\|Identity formation | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | CHARACTER\|Identity formation | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | CHARACTER\|Narrative coherence | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | CHARACTER\|Narrative coherence | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | CHARACTER\|Self narrate | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | CHARACTER\|Self narrate | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | CHARACTER\|The authentic self | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | CHARACTER\|The authentic self | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | CHARACTER\|The integrated self | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | CHARACTER\|The integrated self | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | CHARACTER\|The lifeworld self | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | CHARACTER\|The lifeworld self | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | CHARACTER\|The narrative self | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | CHARACTER\|The narrative self | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | CHARACTER\|The shadow | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | CHARACTER\|The shadow | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | CHARACTER\|The soul's archive | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | CHARACTER\|The soul's archive | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | CONNECTION\|Hierarchy link | operand THOUGHT\|Control: QUESTIONED |
| by_reading_affects | drow | CONNECTION\|Hierarchy link | operand THOUGHT\|Control: QUESTIONED |
| by_reading_affects | dcol | CONNECTION\|The thread | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | CONNECTION\|The thread | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | CURIOSITY\|The eternal asker | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | CURIOSITY\|The eternal asker | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | CURIOSITY\|The wondering soul | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | CURIOSITY\|The wondering soul | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | DESIRE\|Aspiration hold | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | DESIRE\|Aspiration hold | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | DESIRE\|The passionate soul | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | DESIRE\|The passionate soul | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | LEARNING\|Metacognitive | operand THOUGHT\|Control: QUESTIONED |
| by_reading_affects | drow | LEARNING\|Metacognitive | operand THOUGHT\|Control: QUESTIONED |
| by_reading_affects | gone | LINEAGE\|Leave mark | operand LINEAGE\|Legacy: QUESTIONED |
| by_reading_affects | gone | LINEAGE\|Legacy build | operand LINEAGE\|Legacy: QUESTIONED |
| by_reading_affects | gone | LINEAGE\|Legacy revision | operand LINEAGE\|Legacy: QUESTIONED |
| by_reading_affects | dcol | LINEAGE\|Lineage memory | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | LINEAGE\|Lineage memory | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | LINEAGE\|The dynastic soul | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | LINEAGE\|The dynastic soul | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | LINEAGE\|The heritage self | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | LINEAGE\|The heritage self | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | gone | LINEAGE\|The legacy drive | operand LINEAGE\|Legacy: QUESTIONED; operand LINEAGE\|Immortality: MISFILED |
| by_reading_affects | dcol | LINEAGE\|The seed self | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | LINEAGE\|The seed self | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | gone | LUDIC / ABSURDIST\|Gallows humor | operand PATHOLOGICAL\|Mortality: QUESTIONED |
| by_reading_affects | dcol | LUDIC / ABSURDIST\|The ironist | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | LUDIC / ABSURDIST\|The ironist | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | MATERIAL\|Anneal | operand MATERIAL\|Plasticity: QUESTIONED |
| by_reading_affects | drow | MATERIAL\|Anneal | operand MATERIAL\|Plasticity: QUESTIONED |
| by_reading_affects | dcol | MATERIAL\|Composite | operand MATERIAL\|Ductile: QUESTIONED |
| by_reading_affects | drow | MATERIAL\|Composite | operand MATERIAL\|Ductile: QUESTIONED |
| by_reading_affects | dcol | MATERIAL\|Ductile failure | operand MATERIAL\|Plasticity: QUESTIONED |
| by_reading_affects | drow | MATERIAL\|Ductile failure | operand MATERIAL\|Plasticity: QUESTIONED |
| by_reading_affects | dcol | MATERIAL\|Metallurgical memory | operand MATERIAL\|Plasticity: QUESTIONED |
| by_reading_affects | drow | MATERIAL\|Metallurgical memory | operand MATERIAL\|Plasticity: QUESTIONED |
| by_reading_affects | dcol | MATERIAL\|Perfect elasticity | operand MATERIAL\|Elasticity: QUESTIONED |
| by_reading_affects | drow | MATERIAL\|Perfect elasticity | operand MATERIAL\|Elasticity: QUESTIONED |
| by_reading_affects | dcol | MATERIAL\|Perfect plasticity | operand MATERIAL\|Plasticity: QUESTIONED |
| by_reading_affects | drow | MATERIAL\|Perfect plasticity | operand MATERIAL\|Plasticity: QUESTIONED |
| by_reading_affects | dcol | MATERIAL\|Viscoelasticity | operand MATERIAL\|Elasticity: QUESTIONED |
| by_reading_affects | drow | MATERIAL\|Viscoelasticity | operand MATERIAL\|Elasticity: QUESTIONED |
| by_reading_affects | dcol | MATERIAL\|Weld zone | operand MATERIAL\|Composite: QUESTIONED |
| by_reading_affects | drow | MATERIAL\|Weld zone | operand MATERIAL\|Composite: QUESTIONED |
| by_reading_affects | dcol | MATERIAL\|Work harden | operand MATERIAL\|Plasticity: QUESTIONED |
| by_reading_affects | drow | MATERIAL\|Work harden | operand MATERIAL\|Plasticity: QUESTIONED |
| by_reading_affects | dcol | MORPHOGENETIC\|French flag | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | MORPHOGENETIC\|French flag | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | NETWORK\|The cluster | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | NETWORK\|The cluster | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | NETWORK\|The hub | operand THOUGHT\|Control: QUESTIONED |
| by_reading_affects | drow | NETWORK\|The hub | operand THOUGHT\|Control: QUESTIONED |
| by_reading_affects | dcol | NOETIC\|Surrender control | operand THOUGHT\|Control: QUESTIONED |
| by_reading_affects | drow | NOETIC\|Surrender control | operand THOUGHT\|Control: QUESTIONED |
| by_reading_affects | dcol | NOETIC\|Surrender win | operand NOETIC\|Surrender control: QUESTIONED |
| by_reading_affects | drow | NOETIC\|Surrender win | operand NOETIC\|Surrender control: QUESTIONED |
| by_reading_affects | dcol | ONTOLOGICAL\|The game is real | operand ONTOLOGICAL\|No Base: QUESTIONED |
| by_reading_affects | drow | ONTOLOGICAL\|The game is real | operand ONTOLOGICAL\|No Base: QUESTIONED |
| by_reading_affects | dcol | ONTOLOGICAL\|The real is sim | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | ONTOLOGICAL\|The real is sim | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | PATHOLOGICAL\|Cathartic expression | operand KINETIC\|Articulation: QUESTIONED |
| by_reading_affects | drow | PATHOLOGICAL\|Cathartic expression | operand KINETIC\|Articulation: QUESTIONED |
| by_reading_affects | dcol | PATHOLOGICAL\|Dark night | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | PATHOLOGICAL\|Dark night | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | gone | PATHOLOGICAL\|Face death | operand PATHOLOGICAL\|Mortality: QUESTIONED |
| by_reading_affects | gone | PATHOLOGICAL\|Mortal awareness | operand PATHOLOGICAL\|Mortality: QUESTIONED |
| by_reading_affects | dcol | PATHOLOGICAL\|The cathartic purge | operand KINETIC\|Articulation: QUESTIONED |
| by_reading_affects | drow | PATHOLOGICAL\|The cathartic purge | operand KINETIC\|Articulation: QUESTIONED |
| by_reading_affects | gone | PATHOLOGICAL\|The eternal return | operand PATHOLOGICAL\|Mortality: QUESTIONED |
| by_reading_affects | gone | PATHOLOGICAL\|The mortal hero | operand PATHOLOGICAL\|Mortality: QUESTIONED; operand LINEAGE\|Legacy: QUESTIONED |
| by_reading_affects | dcol | PATHOLOGICAL\|The suffering soul | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | PATHOLOGICAL\|The suffering soul | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | PATHOLOGICAL\|The wounded self | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | PATHOLOGICAL\|The wounded self | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | REBELLION\|Counter culture | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | REBELLION\|Counter culture | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | REBELLION\|Defiant selfhood | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | REBELLION\|Defiant selfhood | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | REBELLION\|The revolutionary self | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | REBELLION\|The revolutionary self | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | SKILL\|The skilled self | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | SKILL\|The skilled self | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | SOCIAL\|Subculture | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | SOCIAL\|Subculture | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | SOMNIAL\|Dream laboratory | operand THOUGHT\|Control: QUESTIONED |
| by_reading_affects | drow | SOMNIAL\|Dream laboratory | operand THOUGHT\|Control: QUESTIONED |
| by_reading_affects | dcol | SOMNIAL\|Lucid dream | operand THOUGHT\|Control: QUESTIONED |
| by_reading_affects | drow | SOMNIAL\|Lucid dream | operand THOUGHT\|Control: QUESTIONED |
| by_reading_affects | dcol | SOMNIAL\|The nocturnal self | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | drow | SOMNIAL\|The nocturnal self | operand CHARACTER\|Identity: QUESTIONED |
| by_reading_affects | dcol | THOUGHT\|Metacognition | operand THOUGHT\|Control: QUESTIONED |
| by_reading_affects | drow | THOUGHT\|Metacognition | operand THOUGHT\|Control: QUESTIONED |
| by_reading_affects | dcol | TOPOLOGICAL\|Klein bottle | operand TOPOLOGICAL\|Möbius twist: QUESTIONED |
| by_reading_affects | drow | TOPOLOGICAL\|Klein bottle | operand TOPOLOGICAL\|Möbius twist: QUESTIONED |
| by_reading_affects | dcol | TOPOLOGICAL\|Möbius twist | operand TOPOLOGICAL\|Orientability: QUESTIONED |
| by_reading_affects | drow | TOPOLOGICAL\|Möbius twist | operand TOPOLOGICAL\|Orientability: QUESTIONED |
| by_reading_affects | gone | TRANSFORMATION\|Morph | operand TRANSFORMATION\|Rebirth: QUESTIONED |
| by_reading_affects | gone | TRANSFORMATION\|The chrysalis | operand TRANSFORMATION\|Rebirth: QUESTIONED |

### AFTER the fix: counts, per map (every filing, one class each)

| map | OK | MISFILED | QUESTIONED | ORPHAN | STALE |
|---|---|---|---|---|---|
| by_attribute | 8285 | 0 | 0 | 0 | 0 |
| by_default_role | 3991 | 0 | 57 | 0 | 0 |
| by_domain | 4048 | 0 | 0 | 0 | 0 |
| by_grid_term | 2371 | 0 | 0 | 0 | 0 |
| by_kind | 4048 | 0 | 0 | 0 | 0 |
| by_reading_affects | 4508 | 0 | 196 | 0 | 0 |
| by_reading_reads | 10368 | 0 | 0 | 0 | 0 |
| by_substrate | 15093 | 0 | 0 | 0 | 0 |
| by_tag | 8002 | 0 | 0 | 0 | 0 |
| ingredient_of | 6452 | 0 | 0 | 0 | 0 |
| tag.by_attribute | 8285 | 0 | 0 | 0 | 0 |
| tag.by_pair | 5772 | 0 | 0 | 0 | 0 |
| tag.by_tag | 15240 | 0 | 0 | 0 | 0 |
| **all** | **96463** | **0** | **253** | **0** | **0** |

