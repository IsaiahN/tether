# docs

Four documents. They have different jobs and should not be merged.

| file | job | read it when |
|---|---|---|
| **[THE_FORMULA.md](THE_FORMULA.md)** | **the mechanism.** Eight steps, every symbol defined, the notes that the ordering carries | you need to know what the loop *does*. Start here |
| **[DISCOVERY.md](DISCOVERY.md)** | **the build.** 29 numbered questions with status, what the reference branches taught, the proposed layout | you are about to write code, or deciding what to build |
| **[BUILD_PLAN.md](BUILD_PLAN.md)** | **the order.** Seven stages, each with a done-when and a falsifier; what is not being built; how it fails | you are ready to start, or deciding what to rule on first |
| **[PHILOSOPHY.md](PHILOSOPHY.md)** | **the why.** Where the figures came from, which analogies are load-bearing, the grounded imports, the formalisations | you need to defend a claim, or you are writing the paper |
| **[../CLAUDE.md](../CLAUDE.md)** | **the proctor rules.** How the work is done, and the terminal condition | every session. It is loaded automatically |

**Reading order for someone new:** `THE_FORMULA` → `PHILOSOPHY` §0 (the Turing inversion,
the three questions, why the laws apply to themselves) → `DISCOVERY` §5's index.

---

## How they relate

`THE_FORMULA` is normative. The other two serve it.

- **PHILOSOPHY §8** audited the previous draft and found ten gaps. **Nine are now in the
  formula**; that section is kept as the record of the audit, not as a live list.
- **PHILOSOPHY §16** formalised nine claims that had been prose. **All nine are now in the
  formula**; the section is kept for the derivations and the scope notes.
- **DISCOVERY §5** carries the questions. **Q-numbers are permanent IDs** — they never
  change, so a reference from code or from a commit message stays valid.

**Where they disagree, the formula wins**, and the disagreement is a bug in one of the other
two. Say so rather than reconciling silently.

---

## Status, plainly

- **Built, 2026-08-22.** All seven stages of `BUILD_PLAN`. `python demo.py` runs it end to
  end; `python gate.py runs/demo.jsonl` checks the record. 1,481 lines of core.
- The earlier ~700-line spike under `tether/` is gone, superseded by the flat modules.
- `PHILOSOPHY` §8 found ten gaps in the previous formula draft: **nine fixed, one
  withdrawn as miscast.** No live gaps remain in that list.
- Five rulings unblock a build (`DISCOVERY` §5), and **`BUILD_PLAN` §5 says which stage
  each one actually blocks** — stages 0 and 1 need only Q10.

## Provenance

The figures, `THE_FORMULA`, and the corpus these were synthesised from are Isaiah's, from
`Ouroboros-Redux` — branches `v4-cold`, `new-horse`, and `Nexus`, each read for shape only
and each labelled where cited. The proctor doctrine in `CLAUDE.md` is distilled from
`THE_MISSION_north_star.md`, `THE_ALIGNMENT.md`, and `THE_TERMINAL_CONDITION.md`.
