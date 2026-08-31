# The attribute vocabulary, clustered — for ruling

**You were right and I was arguing against work I had not tried.** It clusters, mechanically, in
three passes, and the result is a decision list of about eighty rather than 5,076 judgements.

---

# Pass 1 — form variants, no judgement at all

**Case, camelCase, punctuation, plurals.** Purely mechanical.

**5,055 → 4,924.** 262 written forms collapse to 131.

```
trajectory     <- trajectory, trajectories
contactPoint   <- contactPoints, contactPoint
position       <- position, positions
pixelValue     <- pixelValue, pixelValues
```

**Small, free, and nothing to decide.**

---

# Pass 2 — head words, also mechanical

**Most attributes are `<qualifier> <concept>`, and the last word is the concept.**

**2,202 head words. 775 of them have more than one member**, and those carry **5,904 of 7,932
mentions — 74%.**

```
[action]   69 forms   action · agent action · observed action · deceptive action · future action …
[time]     43 forms   time · action time · response time · decision time · cycle time …
[state]    50 forms   state · current state · game state · knowledge state · steady state …
[change]   41 forms   change · behavioural change · temperature change · belief change …
[force]    35 forms   force · load force · normal force · contact force · upward force …
```

**No judgement here either** — the head word is a parse, not a decision.

**And it is where the fanout is.** 3,497 distinct written forms sit inside those 775 groups.

---

# Pass 3 — semantic clusters over head words

**This is the only part that needs a ruling, and it is a list you can read.**

**Seventeen clusters, ruled, covering 1,736 mentions:**

| cluster | mentions | forms | head words gathered |
|---|---|---|---|
| **ACTION** | 184 | 94 | action · input · trigger · command · move · intervention |
| **SPEED** | 182 | 96 | rate · speed · flow · velocity · acceleration · throughput · pace · tempo |
| **SIGNAL** | 176 | 63 | report · response · signal · output · observation · measurement |
| **TIME** | 172 | 77 | time · duration · phase · period · interval · latency · delay · lag |
| **FORCE** | 155 | 89 | force · pressure · energy · tension · mass · stress · weight · load · momentum |
| **CHANGE** | 123 | 79 | change · shift · transition · difference · variation · update · delta |
| **EXTENT** | 113 | 75 | size · length · area · depth · scale · volume · height · dimension · width |
| **STRUCTURE** | 108 | 74 | pattern · structure · order · arrangement |
| **STATE** | 105 | 62 | state · condition · mode |
| **CONTACT** | 93 | 42 | distance · boundary · edge · contact · gap · adjacency · overlap |
| **DIRECTION** | 73 | 50 | path · direction · vector · trajectory · orientation · axis · heading · bearing |
| **COUNT** | 67 | 41 | frequency · count · number · quantity · population |
| **POSITION** | 52 | 32 | cell · position · location · coordinate · placement |
| **SHAPE** | 50 | 23 | shape · form · angle · curvature · symmetry · topology |
| **MOTION** | 41 | 29 | motion · movement · displacement · mobility · locomotion |
| **IDENTITY** | 36 | 23 | identity · type · label · name · kind · category |
| **COLOUR** | 6 | 4 | color |

## The three rulings, applied

**`RATE` renamed `SPEED`, and `velocity` moved into it.** *Motion means can it move; speed means
at what rate* — so `velocity`, `acceleration`, `flow` and `throughput` are all SPEED, and MOTION
keeps only the fact of moving.

**`DIRECTION` split out as its own cluster.** *These do not collapse.* It takes `path`,
`trajectory`, `orientation`, `vector`, `axis`, `heading` — **73 mentions across 50 forms**, and
they were previously scattered across MOTION and SHAPE.

**`delta` ruled into CHANGE, not MOTION.** A position delta is motion and a temperature delta is
not; **the head word cannot tell them apart and CHANGE is the honest home** — the qualifier
carries which kind.

## Two things the rulings exposed

**`phase` is in two clusters and should be in one.** Thirteen of its sixteen mentions are the bare
word `phase`, with `expansion phase`, `collapse phase` and `beat phase` the rest — **all
temporal.** So **`phase` is TIME**, and STATE loses it.

**And `COLOUR` at 6 is real, not a parse failure.** Audited the whole file for the colour family:
**22 mentions across 16 forms**, and most are `colorIntensity`, `incidentIntensity`,
`backgroundColor` — **optical-domain attributes about light rather than about an object's
colour.**

**Which is a finding rather than a gap.** The list was written for a general object model and
**colour is barely load-bearing in it** — while it is one of five attributes the ARC loop actually
has. **The source list and the domain disagree about what matters, and the domain is right.**

---

# What is left, and it is the honest remainder

**688 multi-member head words are unassigned, carrying 4,184 mentions.**

**The top of that list is not noise — it is concepts I did not draft a cluster for:**

| mentions | forms | head |
|---|---|---|
| 42 | 25 | `object` |
| 42 | 18 | `rule` |
| 41 | 30 | `event` |
| 36 | 20 | `meaning` |
| 34 | 11 | `outcome` |
| 31 | 25 | `level` |
| 30 | 15 | `sequence` |
| 30 | 3 | `persistence` |
| 29 | 14 | `cycle` |
| 28 | 19 | `behaviour` |
| 28 | 16 | `choice` |
| 28 | 13 | `node` |
| 27 | 9 | `belief` |
| 27 | 13 | `memory` |

**Adding sixty more clusters at this rate reaches roughly 78% of all mentions**, which is the
ceiling of what head-word grouping can do.

**And `a` and `b` at 29 mentions each are `entityA` / `entityB`** — the two-place attributes, and
they should be their own cluster because **they are the relational bucket that needs the predicate
residual.**

---

# What I would ask you to rule

**The sixteen names, or your own.** They are labels and changing one costs nothing.

**The three overlaps** — `flow`, `speed`, `delta`. Each is one attribute in two clusters and it
should be in one.

**And whether to draft the next sixty from the unassigned list.** That would take the coverage from
22% to roughly 78%, **and it is the same kind of decision sixty more times rather than a different
kind.**

## The rule that comes out of it either way

***One attribute name per concept, and unique per atom.***

**Dedup within an atom's own list is free and mechanical** — an atom naming `position` and
`positions` names one thing twice, **and after pass 1 that collapses without anyone deciding
anything.**
