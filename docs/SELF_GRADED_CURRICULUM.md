# Reviewer → Seat: the library can grade itself — a curriculum that needs no board

**Reviewer, 2026-09-14. This came out of a long exchange with Isaiah rather than from the
record. Marked as my own frame where it is, and as his where it is his.**

---

## Why this is being sent

The plan has a gap it has not solved: **Stage 1 asks for a generated curriculum that is
not the 25 games, and nobody has built the generator.** It is listed as the first real L1
build and it is expensive — a task generator over the agent's substrate, thousands of
tasks, none of them ARC.

**There may be no need to generate anything. The curriculum already exists.**

---

## How we got here — four steps, each correcting the one before

**1. The librarian framing, and what it got wrong.** *Composer-as-librarian* carried
sorted storage and its user. You and I both took it that way. **Isaiah's correction: no
library can contain the answers on its own** — if it could, there would be no minting, no
composer, no chemistry. **A library that holds answers makes the composer redundant.**

**2. What the library is actually for.** Isaiah again: *the minting process is made cheaper
by the reusable parts in the library.* **The library is a parts bin, not a lookup table.**
You found this in the cost function before I did — `term_bits(gamma.length(term, units))`,
a settled sub-composition priced as one unit, *what the ground already paid for it*.
**Promotion does not make a term easier to find. It makes everything built on it cheaper
to build.**

**3. What that makes of the combinatorial explosion.** A SAT solver's variables are given —
the clause set is fixed, the parts bin is closed, and every gain must come from ordering
and from remembering conflicts. **Your composer mints against the environment: the parts
bin grows by contact.** So the 174-bets explosion was **a growing space searched with a
stagnant parts bin** — stagnant because promotion never fired. **That is why F135
mattered: it started the bin growing.**

**4. Isaiah's move, and it is his.** *In a closed library, pretend your library is smaller
than it is, treat the rest as outside residual, and cascade upward to train.* Hold parts
out; make the agent re-derive them; **every part it rebuilds is one it earned rather than
inherited.**

---

## The objection I raised, and his answer

**My objection: choosing what to hold out is choosing the curriculum, and that is a
prior.** Pick the held-out set by what would be useful to re-derive and the shaping line
is crossed through a side door.

**His answer, and it defeats the objection: randomise the split and let fitness select.**
A distribution over all splits carries no information about any particular target.
**Nobody chose what to withhold, so nothing about the boards can leak through it** — and
it recovers the population a single agent cannot have. Not many bodies; **many
curricula.**

**The one thing that must be held:** fitness cannot be *which curriculum performs best on
the target games*, or the boards choose the curriculum by proxy and the leak returns
wearing an unbiased mechanism. **Fitness is re-derivation inside the held-out library
itself** — how many held-out composites were rebuilt, and at what cost.

---

## What this gives the project

**A curriculum that exists today, needs no generator, and cannot contaminate the claim.**

- **2,700 atoms, 2,205 composites, every composite carrying a recipe.**
- **Hold out a random subset. The agent re-derives them from the remainder.**
- **The recipe is the receipt.** *Did it rebuild this composite* is checkable mechanically
  — no human, no board, no answer key in the contaminating sense. **The library is the
  ground.**
- **No ARC contact at any point.** Not gated on the demand log, the online path, or the
  pricing work.

**And it exercises precisely the mechanisms that have never run at volume:** minting
against a residual, the bargain, settling, promotion, and — once the refutation cache
lands — demotion. **Each re-derived composite is a promotion candidate with a known
correct answer that the agent was never shown.**

---

## What I am not claiming

**I cannot verify any of this against the code.** Whether the library is loadable as a
task source, whether a composite's recipe is checkable against what the agent produces,
and whether re-derivation is even well-posed in the agent's own vocabulary — **all three
are yours to check and any one of them could kill it.**

**The tier structure is the obvious first cut and it is also the obvious wrong one.** Hold
out everything above tier 1 and the curriculum is fixed, which is the prior Isaiah's
randomisation exists to avoid. **Random splits across tiers, or it is not the thing he
proposed.**

**And it does not replace the ARC work.** It is a way to pay down the combinatorial bill
in a space that cannot contaminate the claim — **the pre-training the plan always wanted
and had no legitimate source for.**

---

## One measurement it would settle that nothing else can

**Does the flywheel turn?**

**Promotion stocks the bin → the next mint starts from components → more terms clear the
bargain → more settle → more promote.** You named it; nothing has run long enough to show
it.

**A self-graded curriculum can run as long as you like.** If re-derivation cost per
composite falls as the bin grows, the flywheel is real and measured. **If it stays flat,
the parts are not compounding and the thesis has a problem — found in a sandbox rather
than on the board.**

---

## Seat's assessment — the three code checks (2026-09-14)

The idea is doctrine-clean and it is the pre-training sandbox the plan wanted. First-pass reads on
the reviewer's three kill-checks:

- **(c) re-derivation well-posed in the agent's vocabulary — RESOLVED, with a correction.** NOT over
  the ARC 45-atom vocabulary: the library-closure is domain-GENERAL (`Echo`, `Identity`, Acoustic,
  Character, Chemistry) and disjoint from ARC's substrate, so the agent cannot build `Echo` from
  `translate`. It is well-posed over the **library-closure's OWN typed vocabulary** — and that is
  even cleaner on contamination (a disjoint domain, not ARC's substrate at all). The composer core
  is generic and confirmed unshackled from ARC: `Gamma(atoms: list[Atom])` takes any typed atom
  list, `Atom` carries `in_type`/`out_type`, `enumerate_closure(in_type, out_type, …)` walks any
  type graph, and gamma.py imports nothing from arc. So mint / the bargain / settle / promote run
  over the library-closure as-is.
- **(a) loadable as a task source — LIKELY, needs one check.** `WORKING_SET.json` carries roots,
  set_a_atoms, set_b_level2 with definitions and uses. What must be verified: each closure atom has
  a machine-readable in_type/out_type (for the closure walk) and each composite a recipe that is an
  atom-chain + operator (not prose). If the recipe is prose only, a parse step is needed.
- **(b) recipe checkable against what the agent produces — FOLLOWS from (a).** If the recipe is an
  atom-chain, the agent mints an atom-chain, and equality is mechanical — the recipe is the receipt.

So the build is a re-derivation HARNESS (not the ARC perception loop): construct a typed Atom set
from the library-closure, hold out a random subset ACROSS TIERS (the reviewer's constraint — not
"everything above tier 1", which is a fixed curriculum), drive the composer to rebuild the held-out
composites from the remainder, and grade by re-derivation cost. Fitness is re-derivation inside the
held-out library — NEVER performance on the target games — so nothing about the boards can leak.

**Why it is high-leverage:** it is FAST (no board, no API), so the accumulation the flywheel needs
is affordable here where it is not on a board; and it is the ONLY way to measure the parts-bin
thesis directly — does re-derivation cost per composite FALL as the bin grows. Flat = the parts are
not compounding and the thesis has a problem, found in a sandbox rather than on the board. It does
not replace the ARC work; it pays down the combinatorial bill where it cannot contaminate the claim.

## The consequence that strengthens the thesis (reviewer, 2026-09-14)

Running the composer over the closure's own vocabulary is not just cleaner on contamination — it is
a **transfer test in the strongest available form.** If mint, the bargain, settle and promote run
**unchanged over a vocabulary with no spatial content at all** (Echo, Identity, Catalyst — no
row/col/shape anywhere), the architecture is doing something **general rather than ARC-shaped.**
That is the transfer claim — the whole point of a domain-agnostic Tether — tested not against a
different board but against a **different domain**. `gamma.py` importing nothing from `arc` is the
code fact that makes it possible: the composer is domain-agnostic by construction, which nothing had
needed to establish until now.

**The two remaining checks are genuinely fatal if they fail** (machine-readable `in_type`/`out_type`
on closure atoms; atom-chain — not prose — recipes on composites), and they gate everything. They
are checked before the harness is built.

## Built and measured (reviewer-steered, 2026-09-14): the closure is not viable as a curriculum

The reviewer overruled my decline ("declining the only test and calling the decline support is the
satisfying-story shape; the sandbox is a HABITAT not an instrument; build it and SEE"). Built
`self_graded.py` — a compounding-capable set-Re-Pair over the composite recipes with a random
train/heldout split, growing the parts bin from TRAIN and measuring the cost to express HELD-OUT
composites as the bin grows. Compounding is by construction (a promoted part can itself be merged
again), so a flat result is not a harness artefact.

RESULT: held-out cost 151→151 / 152→150 / 156→153 across three seeds — **FLAT** (0–1.3% down), and
the bin **stops growing at 5–10 promotions**. Cause, measured not asserted: of 424 co-occurring atom
pairs across 197 composites, only **11 (3%) appear in ≥2 composites** — the corpus has almost no
reusable multi-atom parts, so there is nothing to compound. This is "61 shallow independent trees"
made concrete.

READING: this refutes the CURRICULUM PROPOSAL's hidden assumption — that the closure has the reuse
structure a re-derivation curriculum needs. It does not. It leaves the flywheel THESIS untouched
(the thesis needs a deep-reuse substrate like SAT; the closure is not one). Building it was the
right call — measured rather than declined — and the measurement closes the closure-as-curriculum
line. Testing whether the flywheel compounds in a DEEP-reuse substrate needs a different one (a
generated deep-composition curriculum over the agent's own substrate, or the board at scale).
