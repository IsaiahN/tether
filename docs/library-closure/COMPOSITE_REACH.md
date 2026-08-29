# The irreducible set — measured, and the answer is that there isn't one

**585 tier-1 atoms. 2,205 composites. And coverage grows almost linearly in atoms added.**

**Greedy set cover, each pick chosen for marginal coverage:**

| atoms | composites reachable | share |
|---|---|---|
| 10 | 72 | 3% |
| 20 | 125 | 6% |
| 30 | 180 | 8% |
| 60 | 330 | 15% |
| 100 | ~460 | 21% |
| 200 | 948 | 43% |
| 300 | 1,420 | 64% |
| 477 | 2,022 | 92% |

**About five composites unlocked per atom added, from the first pick to the sixtieth.** No knee,
no plateau, no core.

**That is a real structural finding and it is not the one anyone wanted.**

---

# Why there is no core

**Composition is local. 74% of ingredient references stay inside their own domain.**

**So this is not one tree with a small trunk.** It is **sixty-one nearly independent little
trees**, each with about ten atoms and forty composites, and each domain's composites are built
from that domain's atoms.

**Which explains three earlier results at once:**

**The domain graph was only 8% dense** — because most recipes never leave home.

**The super-categories barely predicted edges** — because there is not much cross-domain
structure to predict.

**And the entry graph was a thin spine with a large fringe** — because the spine is *within*
domains, not across them.

## Self-sufficiency varies sharply

| most self-sufficient | | least |  |
|---|---|---|---|
| Tabula Rasa | **100%** | Mechanical | **45%** |
| Adversarial | **100%** | Cellular | 50% |
| Atmospheric | 93% | Aquatic | 50% |
| Kinetic | 89% | Exchange | 56% |
| Mnemonic | 89% | Thaumaturgical | 59% |
| Optical | 88% | Ludic / Absurdist | 60% |
| Cybernetic | 87% | Pathological | 60% |

**Tabula Rasa and Adversarial compose entirely from themselves.** Raw values and the opponent's
model need nothing borrowed.

**Mechanical is the most dependent at 45%** — levers and gears reach constantly into Human for
solidity and support, **which is what you would expect of a domain that is applied physics.**

**And `Pathological` and `Ludic` being near the bottom is the finding to keep.** Suffering and
humour are the two domains that borrow most heavily — **they are made of other domains' parts,
which is what it means to say they are responses rather than substrates.**

---

# What the top of the list looks like anyway

**Most-used atoms, merged by symbol. `⚠` marks a symbol collision across domains.**

| uses | symbol | atom |
|---|---|---|
| 45 | `ident` | Identity |
| 44 | `flow` | Flow ⚠ *four different Flows* |
| 43 | `net` | Network |
| 42 | `meaning` | Lived Meaning |
| 41 | `node` | Node |
| 38 | `trace` | Memory Trace |
| 32 | `state` | State ⚠ |
| 31 | `edge` | Edge |
| 30 | `auto` | Autocatalysis / Automaticity / Automaton ⚠ |
| 30 | `alt` | Alternative |
| 28 | `rand` | Randomness |
| 25 | `prop` | Proposition / Proprioception / Propulsion ⚠ |
| 24 | `group` · `fdbk` | Group · Feedback |
| 23 | `bound` · `rule` · `res` | Boundary · Rule · Resource |
| 22 | `mem` · `self` | Memory · Self |
| 20 | `set` | **Setpoint** |

**Six of the top twelve are symbol collisions.** `flow` names four different things, `prop`
three, `auto` three. **The concentration at the top is partly an artifact of ambiguous
abbreviations**, and the true counts are lower.

**And `Identity`, `Meaning`, `Self` and `Trace` in the top eight is the same finding as
Phenomenological being the second hub** — arriving a third time, from a third direction.

---

# The level-2 combo set — and it matters more, not less

**Given there is no irreducible core, the second layer is where the leverage is.**

**Only 390 of 2,205 composites are ever used as an ingredient. 198 of those are tier 2.** So the
**working set is about two hundred entries**, not two thousand.

## The most-used composites

| uses | tier | entry | domain | recipe |
|---|---|---|---|---|
| 44 | 2 | **Flow** | Dynamic | `Stim optimal + Resp matched + Coup unity` |
| 38 | 2 | **Trace** | Lineage | `Anc + Desc + Connection` |
| 16 | 2 | **Retrieve** | Psychological | `Mem + cue` |
| 12 | 2 | **Practice** | Learning | `Apply + Repetition + Refinement` |
| 12 | 3 | **Insight** | Psychological | `constraint relaxed + recombination` |
| 10 | 2 | **Move** | Action | `Init + Exertion + Dur + Trajectory` |
| 9 | 2 | **Cycle** | Automaton | `Loop + Clock + Iteration` |
| 9 | 2 | **Grab** | Action | `Init + Perc + Contact` |
| 9 | 3 | **Strategy** | Ludological | `Action + State + Obj + Prediction` |
| 8 | 2 | **Break** | Habit | `Habit + Disruption + Novelty` |
| 8 | 2 | **Stress** | Dynamic | `Stim high + Res depleting + Damp overloaded` |
| 8 | 2 | **Market** | Economic | `Trd + common price + Asy` |
| 7 | 2 | **Observe** | Learning | `Sens + Attn + Intake` |
| 7 | 2 | **Loop** | Habit | `Cue + Routine + Reward` |
| 7 | 2 | **Recovery** | Temporal | `Cooldown + Action repeated` |
| 7 | 2 | **Release** | Action | `Init + Agency cease + Contact break` |
| 7 | 2 | **Wound** | Pathological | `Trauma + Event + Breach` |
| 6 | 2 | **Chaos** | Dynamic | `Sens high + Coup high + Var extreme` |
| 6 | 2 | **Run** | Kinetic | `Walk + Inertia` |
| 6 | 2 | **Shift** | Transformation | `Form + Phase + Transition` |

## What is in this list that is not in the atom list

**`Move`, `Grab`, `Release`, `Observe`, `Practice`, `Break`, `Loop`, `Recovery`.**

**These are verbs, and the atom list is almost entirely nouns.** Every one of them is a thing a
body does, **and every one is a tier-2 composite rather than a tier-1 atom** — which is the verb
gap showing up in the statistics rather than in the grammar.

**`Move + Grab + Release + Observe` is close to a minimal action vocabulary**, and it was not
designed as one. It fell out of counting what other entries reach for.

---

# The practical recommendation

**Do not look for an irreducible set. There is not one, and the search for it would cost
weeks.**

**Instead: two working sets, both measured rather than chosen.**

## Set A — the atoms that actually get used

**About 200 symbols carry 70% of all atom references.** Not a core, but a **working vocabulary**,
and it is 200 rather than 585.

**With the collisions resolved first**, because six of the top twelve are ambiguous and their
counts are inflated.

## Set B — the level-2 combos

**About 200 composites, of which 198 are tier 2.** These are what other entries reach for, **and
they are the layer a composer would actually traverse.**

**`Move`, `Grab`, `Release`, `Observe`, `Loop`, `Break`, `Cycle`, `Practice`, `Recovery`** —
**nine verbs that between them cover most of what an agent does**, none of which is an atom.

## And the thing this measurement establishes

**The list is broad, not deep.** Sixty-one shallow trees rather than one tall one.

**Which is fine for a visible set** — the agent sees what exists and aims at it. **And it is bad
for a composer**, because there is no short path from a small vocabulary to most of the list.

**The composer's leverage is the level-2 set**, and that is the answer to the question: **not
which atoms are irreducible, but which two hundred entries everything else is written in terms
of.**
