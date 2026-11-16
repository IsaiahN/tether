# REVIEW 2026-11-16: the index judgement calls, and the word-map category disagreements

Documentation only. No data file is changed by this review. Every ruling below is a
RECOMMENDATION; where a ruling belongs to Isaiah it says so.

Sources read for this review: `docs/03-DESIGN/INDEX_AUDIT_2026-11-16.md` ("For Isaiah" parts 1
and 2, and the QUESTIONED table, 253 rows), and `library/word_map.json` (header and all 4,048
entries). Counts come from a throwaway script that parsed those two files (not committed). The
figure text was not reopened in this window; no figure census is claimed here, and any ruling
taken from this review carries its own.

---

## Part A. The 253 QUESTIONED filings, and the six named OK filings that look wrong

### A.0 What the 253 are, by pattern

The audit's QUESTIONED rows split into four patterns. Only the first two are judgements; the
other two follow from them mechanically.

| # | pattern | filings | entries | whose ruling |
|---|---|---:|---:|---|
| P1 | TRIGGER: the producing phrase is what happens TO the entry ("when pushed", "after a push", "if ...", "despite moving") | 25 | 16 | **Isaiah's** (what `by_reading_affects` means) |
| P2 | CAPACITY / HYPOTHETICAL: "can pass", "can absorb", "would fall", "able to move" | 24 | 12 | **Isaiah's** (same question) |
| P3 | INHERITED: a molecule's filing rests on an operand atom that is itself QUESTIONED | 147 | ~78 | none: follows P1/P2 through the builder |
| P4 | ROLE: `by_default_role` PROCESS rests only on QUESTIONED affects; with none it is STATE | 57 | 57 | none: follows P1-P3 through the builder |
| | total | **253** | | 196 affects + 57 role defaults, matching the audit |

Trigger words within P1: `when` 11, `after` 6, `if`/`If` 6, `despite` 2. Within P2: `can`/`Can` 20,
`would` 2, `able to` 2.

### A.1 P1, TRIGGER (25 filings) -- recommended ruling: split the trigger from the effect

Examples:

1. `MATERIAL|Ductile` -> `dcol`: "an object that stretches **when pushed** instead of breaking".
2. `LINEAGE|Legacy` -> `gone`: "... stays on the board **after** an object is removed".
3. `ACOUSTIC|Snell's law` -> `colour_changed`/`dcells`: "Sound bends **when passing** between mediums".

Also in the pattern: `MATERIAL|Plasticity` ("stays deformed after a push"), `HEAT|combustible`
("changes when a spreading change reaches it"), `THOUGHT|Simulate` ("What if I move this
piece here?"), `CHARACTER|Identity` ("tracked across turns despite moving").

**Recommendation.** *The trigger is the condition, not the effect: unfile the trigger's effect.
A conditional effect is an effect under its condition: keep it, marked conditional.* So
Ductile keeps the stretch (a shape effect, conditional on contact) and loses `dcol` as filed
from *pushed*; Legacy loses `gone` (the removal is the trigger; what it describes is a
persistence); Snell's law keeps nothing it does not itself describe. The `if` rows that are a
quoted hypothetical question (`THOUGHT|Simulate`) or a counterfactual (`EMBODIMENT|Efference
sense`) describe no effect at all and would be unfiled. **Isaiah's ruling**: whether the index
files the effect an entry SHOWS or also the event that SETS IT OFF is a definition of the field,
which the audit already declined to decide.

### A.2 P2, CAPACITY (24 filings) -- recommended ruling: a capacity is not a described effect

Examples:

1. `ACOUSTIC|Aperture` -> `colour_changed`/`dcells`: "... through which something **can pass**".
2. `ONTOLOGICAL|No Base` -> `dcol` (+1): "nothing underneath (an object **would fall**)".
3. `THOUGHT|Control` -> `dcol` (+1): "being **able to move** a value by acting".

Also: `ATMOSPHERIC|Nutrients` ("cells an object can absorb to grow"), `AESTHETIC|Clarity`
("the board can be split cleanly"), and `LINGUISTIC|Pragmatic inference`, which is not even a
capacity: "Can you pass the salt?" is a quoted example sentence.

**Recommendation.** *A capacity is not a described effect: unfile it from `by_reading_affects`.*
If the capacity is worth keeping for search, it belongs in a separate, declared field
(an affordance: "what this lets happen"), never mixed with what the entry is seen to do, so a
prediction drawn from the index can be blamed on the right kind of claim. The pragmatic-inference
row is a plain word-sense error and would be unfiled under any ruling. **Isaiah's ruling**, for
the same reason as P1; the two should be ruled together, since "would fall" is a conditional
effect with an unstated trigger and the line between P1 and P2 is the line the ruling draws.

### A.3 P3, INHERITED through an operand (147 filings) -- no separate ruling

Examples (operand in brackets):

1. `CHARACTER|Identity formation` -> `dcol` [`CHARACTER|Identity`]; 64 filings rest on Identity alone.
2. `AESTHETIC|Elegance` -> `dholes` [`AESTHETIC|Clarity`]; 18 filings.
3. `AUTOMATON|The rule master` -> `dcol` [`THOUGHT|Control`]; 18 filings.

Other operands: `MATERIAL|Plasticity` 10, `PATHOLOGICAL|Mortality` 5, `MATERIAL|Elasticity` 4,
`KINETIC|Articulation` 4, `LINEAGE|Legacy` 4, `ATMOSPHERIC|Nutrients` 3, and 2 or 1 for nine more.
One row (`LINEAGE|The legacy drive`) also rests on a MISFILED operand (`LINEAGE|Immortality`).

**Recommendation.** Whatever P1/P2 rule, rebuild through the builder and let these follow; do
not rule them one by one. Note the concentration: three operand atoms (Identity, Clarity,
Control) carry 100 of the 147, so the P1/P2 ruling on those three atoms decides most of the
table.

### A.4 P4, ROLE PROCESS on QUESTIONED affects only (57) -- no separate ruling

Examples: `ACOUSTIC|Aperture`, `AESTHETIC|Clarity`, `ATMOSPHERIC|Nutrients` (each: "PROCESS
rests only on affects filings that are QUESTIONED; with none it is STATE").

**Recommendation.** Mechanical: if P1-P3 unfile, these become STATE on rebuild. This matters for
Part B, since STATE maps to `property` in `word_map.json`.

### A.5 The six named OK filings that look wrong (audit Part 2)

| entry | filing and phrase | pattern | recommended ruling | whose |
|---|---|---|---|---|
| `ACOUSTIC\|Absorption` | `shape/dholes/dperimeter` via stem `reflect` ("Reduces reflections") | word sense (sound reflection, not a mirrored outline) | unfile; needs a word-sense rule or a grounding edit | seat may propose; the grounding edit is a SOURCE edit, so it is reviewed |
| `CURIOSITY\|Urge` | `drow/dcol` ("the pull toward an untested action") | metaphor | unfile: a metaphorical verb is not a described effect | seat, under the audit's existing test |
| `CURIOSITY\|Systematic` | `completed` ("in a complete order") | word sense (adjective) | unfile | seat |
| `LINEAGE\|Fruit` | `came` via `produc` ("the product at the end of a chain") | word sense (noun "product") | unfile | seat |
| `ACOUSTIC\|Medium` and others | `drow/dcol` ("a change travels") | wrong effect, right idea | refile to `spread` (`colour_changed/dcells`): a change that propagates is spread, not object motion | seat proposes, reviewer checks |
| `ACTION\|Exertion` | motion ("actions spent, or cells moved") | a MEASURE filed as an effect | unfile from affects: a measure of an effect is not the effect | **Isaiah's**, ruled with P2 (same family: something about an effect, not the effect) |

Four of the six are word-sense errors that the stem matcher cannot see; they are one rule ("the
affirmed verb must be the sense the phrase uses"), and that rule is not Isaiah's to make, but any
SOURCE edit to grounding text that implements it is.

---

## Part B. The 2,148 category disagreements in `library/word_map.json`

### B.0 What a disagreement is

The builder's rule (header `category_rule`): `category` = the chosen WordNet senses' lexname
category when they agree (several disagreeing -> `other`); else the library's category; both
written, a difference flagged `disagreement`, never overridden. The library category comes from
`category_library_map`: `STATE -> property`, `PROCESS -> action`, `RESULT -> property`,
`CAUSE -> action`, `AGENT/INSTRUMENT -> object`, `MEASURE -> measure`, `RELATION -> relation`,
`RULE/TEST -> rule`.

Population: 4,048 entries; `category_source` wordnet 3,025, library 957, none 66. Flagged
`disagreement`: **2,148**, all with source `wordnet`. (A raw `category != category_library`
count gives 2,214; the extra 66 are the source-`none` rows, which have no WordNet category and
are not flagged.) Of the 2,148, sense status is `context` 988, `tie` 753, `sole_sense` 407.

### B.1 The pairs (WordNet `category` vs library `category_library`)

| WordNet | library | count | library role behind it | top WordNet lexnames | examples |
|---|---|---:|---|---|---|
| action | property | 478 | STATE 477, RESULT 1 | noun.act 135, verb.change 55, noun.event 43 | `ACOUSTIC\|Binaural beat`, `ACOUSTIC\|Interference`, `ACOUSTIC\|Standing Wave` |
| other | property | 393 | STATE | noun.communication 103, noun.cognition 45, noun.group 38 | `ACOUSTIC\|Beat`, `ACOUSTIC\|Cochlear implant`, `ACOUSTIC\|Motion` |
| other | action | 295 | PROCESS 293, CAUSE 2 | noun.communication 52, noun.group 35, noun.cognition 33 | `ACOUSTIC\|Acoustic lens`, `ACOUSTIC\|Acoustic mirror`, `ACOUSTIC\|Medium` |
| object | action | 185 | PROCESS | noun.artifact 79, noun.person 37, noun.object 23 | `ACOUSTIC\|Accelerometer`, `ACOUSTIC\|Aperture`, `ACOUSTIC\|Helmholtz resonator` |
| property | action | 156 | PROCESS | noun.attribute 64, noun.state 51, adj.all 29 | `ACOUSTIC\|Acoustic ecology`, `ACOUSTIC\|Acoustic radiation pressure`, `ACOUSTIC\|Reverberation` |
| rule | property | 152 | STATE | noun.cognition 152 | `ACOUSTIC\|Acoustic holography`, `ACTION\|False Intent`, `ADHERENCE\|Discipline` |
| object | property | 151 | STATE | noun.artifact 50, noun.person 29, noun.substance 24 | `ACOUSTIC\|Electrode`, `ACOUSTIC\|Headphones`, `ACOUSTIC\|Listener` |
| rule | action | 86 | PROCESS | noun.cognition 86 | `ADHERENCE\|Covenant memory`, `ADHERENCE\|Love`, `ADHERENCE\|The bound universe` |
| relation | property | 43 | STATE | noun.location 22, noun.relation 16 | `AGENT\|centroid`, `ALEATORY\|Gaussian`, `ATMOSPHERIC\|Cold Air` |
| measure | action | 33 | PROCESS | noun.time 24, noun.quantity 9 | `ACOUSTIC\|Beat frequency`, `ADVERSARIAL\|False history`, `ATMOSPHERIC\|Drought` |
| relation | action | 33 | PROCESS | noun.location 15, noun.relation 14 | `ACOUSTIC\|Multiple Surfaces`, `AESTHETIC\|direction`, `ALEATORY\|Monte Carlo` |
| measure | property | 31 | STATE | noun.time 22, noun.quantity 9 | `ACOUSTIC\|20kHz`, `ACOUSTIC\|<20Hz`, `AESTHETIC\|Rhythm` |
| property | measure | 28 | MEASURE | noun.attribute 20 | `ACTION\|Duration`, `ACTION\|Scope`, `ADHERENCE\|Reliability` |
| shape | action | 17 | PROCESS | noun.shape 17 | `AESTHETIC\|Logarithmic spiral`, `CONNECTION\|Membrane boundary`, `DYNAMIC\|Chaotic edge` |
| shape | property | 15 | STATE | noun.shape 15 | `AESTHETIC\|Triangle`, `OPTICAL\|Light Ray`, `PSYCHOLOGICAL\|Bias` |
| action | measure | 15 | MEASURE | noun.act 5 | `AGENT\|count`, `CHARACTER\|Depletion`, `CHEMICAL\|spatial spread` |
| other | measure | 13 | MEASURE | noun.attribute 4 | `ACOUSTIC\|Amplitude`, `ACOUSTIC\|Speed of Sound`, `AESTHETIC\|Scale` |
| object | measure | 5 | MEASURE | noun.possession 3 | `AGENT\|dholes`, `ECONOMIC\|price`, `EXCHANGE\|Currency` |
| action | relation | 4 | RELATION | verb.contact 2, verb.perception 2 | `ADHERENCE\|Covenant bind`, `AGENT\|touches`, `AGENT\|touching` |
| action | rule | 4 | TEST | | `AGENT\|holds`, `CHARACTER\|Integrity check`, `LOGISTICAL\|Bottleneck analysis` |
| property | rule | 2 | TEST | | `AGENT\|both`, `AGENT\|either` |
| property | relation | 2 | RELATION | | `AGENT\|owner`, `AGENT\|same` |
| shape | measure | 1 | MEASURE | | `AGENT\|corners` |
| other | relation | 1 | RELATION | | `AUTOMATON\|Automaton network` |
| other | rule | 1 | TEST | | `CURIOSITY\|Surprise inquiry` |
| (smaller pairs) | | 4 | | | |
| **total** | | **2,148** | | | |

### B.2 The systematic causes

1. **The library's two DEFAULT roles carry almost all of it.** `library_default_role` is STATE on
   2,049 of 4,048 entries and PROCESS on 1,781. STATE maps to `property` and PROCESS to `action`,
   so a default that only means "no affects filing" (STATE) or "some affects filing" (PROCESS) is
   read as a word category. **STATE stands behind 1,262 disagreements and PROCESS behind 803:
   2,065 of 2,148 (96%).** The explicit roles (MEASURE 62, RELATION 7, TEST 7, CAUSE 2, RESULT 1)
   account for 79.
2. **PROCESS is itself downstream of the index audit.** It is set when an entry has any
   `by_reading_affects` filing, so the 57 QUESTIONED role defaults of Part A (P4), and every
   MISFILED affects filing, feed the `object vs action` and `property vs action` rows directly
   (e.g. `ACOUSTIC|Aperture` is in both). A P1/P2 ruling will move some rows from `* vs action` to
   `* vs property` on rebuild.
3. **`other` is not a category, it is an absence.** `category_map` sends noun.communication,
   noun.group, noun.motive and noun.Tops to `other`, and the builder writes `other` when chosen
   senses disagree (753 of the 2,148 are `tie` rows). `other` stands in 702 disagreements
   (393 + 295 + 13 + 1).
4. **`noun.cognition -> rule` is too coarse.** All 238 `rule vs property/action` rows are
   noun.cognition: `Discipline`, `Love`, `Acoustic holography` are not rules. The map line, not
   the library, is the cause there.
5. **Head-word sense on a compound name.** The WordNet category is the head word's sense
   (`Binaural beat` -> beat, noun.act/event; `Acoustic lens` -> lens). That is right for what the
   name NAMES (object vs action: an accelerometer is an object), and says nothing about what the
   entry DOES, which is what the library role encodes. Most `object vs action` rows are both true
   at once: the thing is an object, and it acts.

### B.3 Which source should win, per pair, for search ordering (RECOMMENDATIONS)

These are recommendations for the ORDER in which search tries categories, not for overwriting
either field (the builder writes both and must keep doing so; nothing in the agent reads this
file today, header `readers_note`). None of these is Isaiah's ruling unless it changes what the
agent may reach; they are the seat's and the reviewer's to settle, and the board judges them.

| rule | pairs | rows | recommended winner | why |
|---|---|---:|---|---|
| R1 an explicit library role beats WordNet | `* vs measure` (MEASURE), `* vs relation` (RELATION), `* vs rule` (TEST) | 76 (+3 CAUSE/RESULT rows that sit inside R2/R3 pairs) | **library** | an authored role is a reading of the entry; WordNet's is a reading of its head word (`ACTION\|Duration` is a measure; `AGENT\|touches` is a relation) |
| R2 a specific WordNet lexname beats a library DEFAULT | `action vs property` 478, `object vs property` 151, `object vs action` 185, `measure vs *` 64, `relation vs *` 76, `shape vs *` 32, `property vs action` 156 | 1,142 | **WordNet**, tried first; library second | STATE/PROCESS are defaults about filings, not about the word (`Interference` is an event; `Headphones` an object; `20kHz` a measure) |
| R3 WordNet `other` never wins | `other vs property` 393, `other vs action` 295 | 688 | **library** | `other` carries no search key; the default is weak but is something |
| R4 noun.cognition `rule` does not win | `rule vs property` 152, `rule vs action` 86 | 238 | **library**, with the map line flagged for review | the coarse map, not the word, made them rules |
| R5 tie rows are low confidence either way | any pair with status `tie` | 753 (overlaps the above) | order as above, flagged | several senses chosen; neither side is a reading |

(R1-R4 rows: 76 + 1,142 + 688 + 238 = 2,144; the remaining 4 rows are in pairs smaller than the 25 listed.)

Refuter for these recommendations: if, once something reads `word_map.json`, ordering by R2 puts
the right entry first LESS often on the board than ordering by the library field, R2 is wrong.
Until then they are recommendations with no standing, like every row in the file (header
`standing: none`).

---

## What is Isaiah's, in one list

1. P1 + P2 together (49 direct filings, carrying 147 inherited and 57 role defaults): does
   `by_reading_affects` hold only what the entry is described as doing, or also what sets it off
   and what it could do? The recommendation is: trigger -> unfile; conditional effect -> keep,
   mark conditional; capacity -> unfile (a separate affordance field if wanted).
2. `ACTION|Exertion` (a measure of an effect), ruled with P2.
3. Any SOURCE edit to grounding text made to fix the word-sense rows.

Everything else here (P3, P4, the four word-sense OK rows, the Part B ordering) follows
mechanically or is the seat's and the reviewer's to settle, measured on the board.
