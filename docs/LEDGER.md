# The open-items ledger — who holds what, and when it last moved

**Isaiah, 2026-09-20: *"follow up with the reviewer on stuff it seems to not follow up with you on,
ask for status — keep a ledger, keep it current, and discuss if things need to update on it."***

**WHY THIS FILE EXISTS, STATED AS THE FAILURE IT IS FOR.** On 2026-09-20 a reviewer ruling landed at
**01:48** saying *"the honest L1 is the wire. It is now unblocked"* — and the seat did not see it for
**nine and a half hours**, posting four times in that window that it was *"still waiting only on the
CUE_BOUNDARY adjudication."* Two independent causes, and both are the kind a ledger catches:

- **The heartbeat prompt froze the world as it was when written.** It named CUE_BOUNDARY as the
  blocking item. That was true at 00:30 and false from 01:48, and every tick re-injected it as
  present tense. **A recurring instruction carries its stale parts forward most reliably when it is
  followed most faithfully.**
- **The channel query matched the seat's own posts.** `title contains 'Reviewer'` also matches
  `Seat → Reviewer`, so at pageSize 1–5 eight seat posts buried every ruling. **Query
  `title contains 'Reviewer → Seat'` for rulings.**

> **THE RULE THIS FILE INSTALLS: an item's status is what the LEDGER says, never what the brief says.
> Check the brief against this file, not the other way round.**

---

## FORMAT

Each row carries **who holds it · opened · last moved · what would move it**. A row whose *last
moved* is older than a day gets an explicit status chase, not a silent carry-forward.

---

## HELD BY ISAIAH

| item | opened | last moved | state |
|---|---|---|---|
| **The objective/predictor price tie** | long-standing | 2026-09-20 (F152) | **WITHHELD RULING. Report, do not price.** The precondition *build the subject before pricing it* is now met — arm D gave it a subject (`F135`/`F136`), and `F152` gave it a measured consequence: the OBJ-bound population is what feeds gate 1, and it reads 1 · 1 · 3 across four boards with only the 3 ever qualifying. **Nothing is being asked for; this is a note that the question now has a denominator behind it.** |

## HELD BY THE REVIEWER

| item | opened | last moved | state |
|---|---|---|---|
| **`_library_fit`: absolute vs comparative** | 2026-09-20 early | not since | Neither test admits a partial improvement without discarding lateral rebinds. Escalated, unmoved, **not urgent** — arm D is off and nothing waits on it. |
| **The 2700 bridge** | **2026-09-20, NEW (`F157`)** | today | **This replaces the CUE_BOUNDARY question as the live blocker.** `closure_map`'s recipe primitives are **0 of 15** present in Γ; its target atoms **2 of 10**. Three candidate bridges — admit the fifteen as atoms · map each recipe down to existing Γ atoms · something else — **and choosing among them is a vocabulary-admission decision, not the seat's.** |
| **Are the 249 Phase-2 games REPRESENTATIVE?** | 2026-09-20 (their own caveat) | today | Their ruling settles *unexposed*; it explicitly does not settle *representative*. They name Isaiah's cluster analysis as the instrument and call the check cheap. **Open, and it decides what a Phase 2 pass is worth.** |

## RULED — CLOSED, AND RECORDED SO THEY ARE NOT RE-LITIGATED

| item | ruled | outcome |
|---|---|---|
| **The four transformation atoms / CUE_BOUNDARY** | 01:48 and again 10:57 | **PROCEED — source not type; Figure 4's membrane is the authority.** Option (c) (strip the op labels) refused as *the withholding reflex renamed.* **Spent rather than blocking: `F157` shows the wire it permits is empty.** |
| **§14.8 Q3 design-loop seal** | 11:17 | **Phase 2 is the held-out set; seed 1618 withdrawn.** No subset of the 25 is unexposed. |
| **Convergence grading level** | 2026-09-18 | **ATOM + POLICY.** Compositions not graded cross-game. |
| **Waypoint spacing** | 2026-09-18 | **Sweep it, do not pick it.** Report per rung; the curve is the finding. |

## HELD BY THE SEAT

| item | state |
|---|---|
| **Phase 2 re-prioritisation** | The reviewer's ruling promotes `PHASE2_GUIDE_CURRICULUM` from *extra curriculum, later* to **the internal private-set proxy**, which must run **before** the architecture freezes. The plan still files it as later. **Owed: update `TRAINING_PLAN` §14.7's ordering.** |
| **`F130`'s supply-side table is stale** | It reports Γ holding `recolour` and `translate` among 48 atoms. Measured today: **45 atoms, neither present.** Do not quote it again without re-measuring. |
| **Forward-binding seal** | Ready to install; largely moot under the Phase 2 ruling. Revisit only if the reviewer wants the 25 split as well. |

## FLAGGED BY THE REVIEWER ABOUT THEMSELVES

| item | state |
|---|---|
| **Their figure reads are provisional** | Their extraction strips `<metadata>` but **does not join `tspan`s**, so words split across element boundaries were invisible. **Four rulings this week cited figures read with that instrument**, and they have adopted the corrected recipe (join tspans → strip `[A-Za-z0-9+/=]{24,}` → word-bound). Nothing to do; recorded so a future citation of those four is checked. |

---

## CHECKED

    2026-09-20 11:2x    channel read with the CORRECTED query. Found two rulings the old query
                        had hidden (01:48, 10:57) plus the 11:17 seal ruling.

---

## THE REVIEWER'S NINE-ITEM STATUS REQUEST (2026-09-20 11:43) — answered

**They opened by naming their own failure: reactive, no ledger, items going quiet with neither side
noticing. Answers below are from evidence, and where I do not know I say so rather than guessing.**

| # | item | verdict |
|---|---|---|
| **1** | **Spacing sweep** (ladder 1/2/4/8/16, pre-registered 09-18) | **NEVER BUILT, NEVER RAN.** No spacing/rung parameter exists anywhere in the code — the only `ladder` hits are an unrelated lint fixture and an `arc_screen` comment. No run artifacts. **The pre-registration is live and the build is not started.** |
| **2** | **§13 step 4** | **UNKNOWN TO ME — not touched this session and I have no evidence either way.** Flagging rather than asserting; it needs a look before anyone calls it parked. |
| **3** | **Pretraining run** | **HALF.** `work_budget` IS in (`tether.py:343`, default 15000, consumed at :2748), so F180's fix landed. **No pretraining run has been executed or reported** — every commit since 09-18 is this session's findings. Built, never run. |
| **4** | **`chunk_reuse` vs `reuse_install`** | **CONFIRMED AND HARDENED, measured tonight on four boards at 60 cycles.** `reuse_install` 12 · 9 · 4 · 4 — term-level reuse works everywhere. **`routine_cut` 0 · 0 · 0 · 0 — procedure-level reuse has never once fired.** Not 2; zero. And the refusal side is stark: ls20 installs 12 against **792** `reuse_refused`. **Your molecule question is not just unanswered, it is measured at zero with a denominator.** |
| **5** | **The `_explains` cause (F130)** | **READ, and superseded TWICE.** `F133` corrected F130's attribution the same night (*the arity split is real, the supply story is not*), and `F157` today found F130's supply table stale — it reports Γ holding `recolour`/`translate` among 48 atoms; the measured set is **45 and holds neither**. **Do not cite F130's supply side again.** |
| **6** | **Arm B** | **LIVE AND UNRESOLVED. Still default OFF.** `F137` decomposed it into two distinct effects (ls20 gains from the binding itself, tn36 from arity-2 reuse and it costs a goal slot), and every depth run in `F153`'s panel was taken under it. **It is the one arm never settled, and I did not resolve it.** |
| **7** | **Composition-overlap base rate — how was the null built?** | **I DO NOT KNOW.** It predates this seat and I have not reconstructed it. **You are right that it is the one number in that finding nobody outside can check, and I am not going to assert a construction I did not verify.** Needs the original run or a rebuild. |
| **8** | **`_library_fit` absolute vs comparative** | **OPEN, genuinely, not urgent.** Arm D is off and nothing waits on it. |
| **9** | **Phase 2 re-prioritisation** | **I OWN IT.** Your 11:17 ruling makes Phase 2 the held-out set, which moves it from *later* to *before the architecture freezes*. `TRAINING_PLAN` §14.7 still orders it as later. **Mine to update.** |

**AND THE ITEM THAT SUPERSEDES THE ONE YOU THINK IS CLOSED: `F157`.** You ruled the wire in bounds
twice. **Measured before importing: `closure_map`'s recipe primitives are 0 of 15 present in Γ and
its target atoms 2 of 10.** The wire is permitted and empty — importing it would hand the agent
*`Translate = Ct + Co`* in a vocabulary it does not hold. **The 2700 blocker was never
`CUE_BOUNDARY`; it is a vocabulary disjunction, and that is now the live question in your column.**

---

# THE REFUSED / PARKED REGISTER

**Isaiah, 2026-09-20: *"create a list of stuff you guys refused due to reasons like proxy numbers
etc. I'd want to know in case it was a genuinely good idea and it needed to be reviewed and
resurfaced to me."***

**SURFACING RULE, HIS: NOT in heartbeat updates. Only when he is corresponding directly, every few
hours or so.** It is not a limiting list and nothing here is being re-argued — it exists so a good
idea killed for a procedural reason can be found again.

**WHY THIS REGISTER IS NOT REDUNDANT WITH THE RECORD.** A refusal is written at the moment it is
made, filed under the thing it refused, and then it is structurally invisible: nobody greps for what
is absent. **`CLAUDE.md`'s own warning is that a map entry saying a thing does not exist closes the
question** — and a refusal is exactly that entry.

### ranked by how likely I think the refusal was WRONG

| what was refused | why it was refused | why it might deserve another look |
|---|---|---|
| **ARM D — the bargain at retrieval** (`_library_fit` accepting on `pays()` instead of exact `_explains`) | Net harm: arity-1 reuse 7/7 → 0/7, mints 5 → 1, goal rows 10 → 5. **And a second reason: shipping it would settle the objective/predictor tie BY DEFAULT in favour of predictors, with nobody ruling on it.** | **IT IS THE ONLY THING THAT HAS EVER MOVED ARITY-2 OFF ZERO — 0/127 → 8/70 on ls20, 0/51 → 5/41 on vc33. The first arity-2 reuses ever recorded.** Arity-2 is the largest measured gap in the build (0.0–5.5%, four boards). The refusal was right on the evidence and it killed the only demonstrated lever. **If the tie were ruled, arm D becomes a live proposal again rather than a default.** |
| **The `is_atom` novelty relaxation** (narrow or wide) | Pre-registered refutation: partner fired but the wall did not move. ls20 reach-failure flat at 802; sk48 3857 vs a 3839 floor. Recommendation to Isaiah was **do not**. | **The reviewer later reframed its own evidence: partner settled 70 on sk48 and was DEMOTED 53 times — the ground refusing terms that had paid the bargain. They called that "the loop working," the first validation of demotion at volume.** So the probe produced a real positive about the architecture while failing its stated target, and the do-not rests only on the target. |
| **The five `partner_<T>` atoms + the typed predictor stream** (relation→value dereference) | Built twice, inert twice, reverted both times: zero partner events on vc33, byte-identical aggregates on ls20, +15–31% wall cost for no capability. Pure denominator growth. | **`F157` changes the frame under this.** The 2700 are now known to be blocked by a **vocabulary disjunction** — Γ holds none of the 15 closure recipe primitives. The partner work was an attempt at exactly this class of bridge and was judged only on whether the wall moved. **One of the three candidate bridges is "admit the primitives as atoms," which is what partner was.** |
| **The 13 heavy scalars typed `EXTENT`** | **This is the PROXY-NUMBER refusal, and the clearest one.** `EXTENT` is accepted by ZERO atoms, so typing 13 attributes into it would multiply a dead population: "chains 4 → 18" with reach unmoved. THE FORMULA step 8 — *a system measuring progress by terms minted is counting the denominator.* | **The refusal was of the WIRING, not of the attributes.** `EXTENT` having no consumer was itself flagged as possibly an oversight rather than a decision (`is_max`/`is_min`/`rank_in` accept POSITION and are exactly the shape that would apply to a magnitude). **If EXTENT gains a consumer, the scalars stop being a dead population.** That question was put to the reviewer and never answered. |
| **Option (c) — emit deltas without the op label** | Refused BY THE REVIEWER as *"the withholding reflex Isaiah diagnosed, wearing a new costume"* — the 19 names are already frontloaded, so making the agent re-derive them proves nothing and costs the diagnostic. | **I still think (c) was the interesting build and I said so before it was refused.** The refusal is doctrinally correct on frontloading. Recording it because *it was the option the seat would have chosen*, and that disagreement should be visible rather than settled silently. |

### refused and I believe correctly — recorded so nobody re-derives them

| what | why, and why it stays refused |
|---|---|
| **Tuning `MIN_REPEAT`** so gate 1 opens | *Tuning a constant until a board passes is the encoded answer in a fix's clothes.* Now has two boards behind it from opposite directions (vc33 too-short, tn36 flat). **Stays refused.** |
| **More goal slots** to break gate 3's tie | A REVERTED option — §13.4 records that it measurably chose to stand still. |
| **Arm E — the finer vote** | Not merely inert: the votes are SATURATED at 1.0, so there is no difference for a finer measure to resolve. Genuinely dead. |
| **Arm C — the relation channel** | Correct-by-parity with two sibling sites and changes no reading, alone or combined. Retired rather than held. |
| **A transitive `ISOLATED` reachability rule** | No outcome-blind root set exists: hand-listed roots give 44 false positives, `__main__` guards launder the one real case. **And Figure 9 says why it was malformed — a lint rule is a filter and cannot hand a verdict.** |
| **Sealing a subset of the 25** | Measured: every one of the 25 is exposed, and the least-exposed are the degenerate one-action boards. Superseded by the Phase 2 ruling. |
