# STATUS REPORT — the unattended run window

**Build frozen at `arc-freeze-02`.** Tag object `46349f36`, **commit `67ceacd`** — two different
hashes for one word, noted because it is exactly the collision this window kept finding.

> **THIS REPORT IS A SNAPSHOT AT `72b8a3c` (2026-09-09 05:41) AND THE PARAGRAPH BELOW WENT STALE
> FIVE HOURS LATER.** It is repaired rather than rewritten, because the original sentence and what
> replaced it are the finding. **A status report is a claim with a timestamp, and this one carried
> its strongest claim without one.**

**AS WRITTEN, AND TRUE AT `72b8a3c`:** *“`git diff arc-freeze-02 -- '*.py'` is empty. No build file
was touched after the freeze, and that was checked at every commit rather than asserted once.”*

**AS OF `fcb87bd`, THAT SENTENCE IS FALSE, AND THE REASON IS SANCTIONED RATHER THAN A BREACH.**
The diff is **139 insertions across two files**, from **three commits, each applied under a ruling
and each recorded against its finding before it was made:**

    c009007  09-09 10:51  System 2 beside System 1 -- the F14 fix, Isaiah's ruling, named
                          in the code comment at its own site
    1c6fb2e  09-09 10:53  transcript.py, a new READ-ONLY renderer; it wraps the ledger and
                          adds no emitter
    92bd9c5  09-09 12:18  the F23 fix -- `action=action` on the REPEAT row, purely additive,
                          483 rows before and after

**AND THE STALE CLAUSE IS THE ONE WORTH KEEPING VISIBLE: *checked at every commit rather than
asserted once*.** The checking stopped when this document stopped being updated — so **a check
recorded as continuous, in a document no longer maintained, silently becomes an assertion again.**
That is the exact failure the sentence was written to avoid, performed by the sentence.

**9/9 conformance seats clean at every commit**, enforced by the pre-commit hook rather than by me
— and that half is still true and still checked, because the hook runs whether or not anyone
writes it down. **The durable check is the one nothing has to remember.**

---

## 1 · WHERE THE PHASES STAND

| phase | state |
|---|---|
| **1 · finish the buildable queue** | **complete.** Items 1–2 done before the window opened; item 3 filed unbuilt |
| **2 · freeze** | **complete.** Tagged, hash recorded in `INDEX.md` before any run |
| **3 · the 5-game read** | **complete.** 5 games × depths 6/12/24, plus 48 on the two affordable boards |
| **4 · notes, then refined notes** | **complete.** Both passes written; second pass is the deliverable |

**Phase 1 item 2 returned the OPPOSITE of the brief's premise, and that is the first thing to
read.** The brief asked me to record that the reach circle was broken because `accepting()` is
non-empty on six of eight types. **`accepting()` is `Registry.accepting()` over the NINE SENSORS;
`resolve()` closes over `env.sensors()` and never over Γ.** The 19/16/15 figures were **atoms** — a
different registry. Measured against the one the mechanism reads:

    SENSORS accepting an attribute type : NONE -- empty on every one
    closure((OBJECT,), depth 2|3|4|5)   : 4 chains, composable=0 -> UNREACHED

**The circle is intact.** `CLAUDE.md` now records the *prohibition* as spent (parity/holes admitted
under your 2026-09-05 entry clause, with `ADMITTED` stamps naming which clause admitted each) and
the *verdict* as unchanged. **Both suspended citations stay withdrawn, now with measurement behind
them rather than inheritance.**

**Phase 1 item 3 (§4's producer) is filed, not built**, per its own condition. The semantics are
clean; the specified design contradicts its purpose. There are exactly two `gamma.accept` sites,
both restricted to `val`/`OBJ`, so **a settled term can never carry `out_type` PRED** — measured,
`['val']`. `both`/`either` need PRED. A producer *"bounded by the settled library"* cannot supply
their operand, ever. Built as described, `and_op`/`or_op` stay identity.

---

## 2 · THE HEADLINE FINDING

### `F14` — the asking window closes before the supply opens

    ka59, depth 24
    _mint_routine called at : [0, 1, 2, 3, 4, 5, 11]      last ask = cycle 11
    _goal_choice returned   : None, 14 of 14 times
    a series QUALIFIED at   : cycle 14 (o14.dcol), cycle 24 (o13.w)

**Every refusal was correct.** No goal-residual series qualified at any moment the gate was
consulted. **But one does qualify — at cycle 14, three cycles after the last thing that could
consult it.**

> *"Gate 1 refuses because supply is empty"* is **true at every asking moment and false as an
> account of why M2 does not fire.** Supply arrives. Nothing asks.

`_goal_choice` is called only from `_mint_routine`; `choose()` reaches it only on cycles falling
through to a draw; and **`draw` freezes at 7 on this board at every depth from 6 to 48**, against
41 learned actions at depth 48. Seven calls, seven draws.

**It arrived through a check written to refute me.** `rescensus2.py` prints *"F5 IS WRONG and the
refusal is a DEFECT"* if it finds a qualifying series. It found one.

**Denominator: one board.** `ls20` at depth 24 is running. `sp80` cannot test it — no objective at
any depth, so no series can ever qualify there.

---

## 3 · ERRORS — one, and the seats cannot see it

**`E1` · the gate refuses every real board's ledger.** `refuse / steps / step-order`, note
`"*: PLAN after PERCEIVE"`. `step()` opens with four narrators at `tether.py:2849-2852` — before
`_present()` and before `env.observe()` — stamping `PERCEIVE`, which is `STEPS[1]`. The `PLAN` row
from `_mint_routine` arrives later. **4 of 4 boards that ran, every depth.** Wrong regardless of
board; **wrong-given-the-input**, because the ledger violates the build's own declared step order.

    candidate (a)  stamp the four narrators PLAN rather than PERCEIVE -- they run BEFORE
                   perception, so the stamp may always have been wrong. No call moves
    candidate (b)  move the four calls after the PLAN phase. RISK: narration describes the
                   pre-action frame, so this may change WHAT IT NARRATES

**Neither applied, and the choice is not the seat's** — (b) is only an ordering fix if narration's
content does not depend on when it runs, and that is unmeasured.

**`E1b` · the seat's coverage is bounded by the toy world's vocabulary, and this outlives the
fix.** `demo.jsonl` contains **zero** narration rows, so the `gate` seat validates a ledger
**structurally incapable of containing the rows that break it.** Nine seats green and every real
board refusing, simultaneously. **Repairing `E1` leaves this exactly where it is**, and it is the
more general of the two.

---

## 4 · QUIRKS — two, both the build being right, neither gets a fix

**`Q1` · `vc33` runs nothing and says so.** `{"verdict": "no_cycles", "reads": "nothing ran"}`,
`gate: pass`, 0.1s at every depth. Reports an absence as an absence rather than manufacturing a
null.

**`Q2` · `sp80` never wins an objective contest, at any depth.** 0 of 1, 0 of 6, 0 of 9, 0 of 10.
A board with no objective cannot lose an objective contest.

> **`Q2` is doing work.** Without a board that offers nothing, *"the objective arm wins on some
> boards"* cannot be separated from *"it wins where the thing exists."* The zero is what makes the
> `ka59` climb readable.

---

## 5 · FINDINGS WITH DENOMINATORS

**`F1` · six cycles is not a reading.** 100% probe on every board at depth 6; directed on 14–17 of
24 at depth 24. Nothing in the six-cycle output distinguishes *the agent only probes* from *it has
not learned a split yet*.

**`F2` · a null with a denominator of 23 was still wrong.** `ar25` read *the objective arm never
wins* at depth 12 across 23 contests. It wins 7 times at depth 24.

**`F3` · S5 is why any of this is visible.** `discriminate:learned` is excluded by exact match
under the pre-S5 counter, so the identical runs would read `directed: 0` everywhere. **An
instrument repair changed a conclusion about the agent.**

**`F11` · the price tie is observed, for the first time.** `ka59` at depth 48:
`{predictor 10, objective 35, tie 2}`. `mint`'s comment promised *"the tie is published as a
tie"* and it had never been seen in a run. **Your held pricing ruling is now about something
observed rather than derived.**

**`F12` · the objective arm's share rises monotonically across four depths.** `ka59`: 0/0 → 4/9 →
13/20 → **35/47**. `sp80` at zero throughout as the control.

**`F10` · the growing-candidate-space account is SUPPORTED, and my earlier "four refutations" was
wrong.** Three readings measured three different quantities under one phrase: `lf52` refutes
cost ∝ **calls**; the `negate` matched pair refutes cost ∝ **atom count**; the depth series
supports cost ∝ **units**. `enumerate_closure` runs over `units()` = atoms + settled terms.

    board   doubling    d(library)   wall ratio
    sp80    24 -> 48        +1         1.64x     cycles doubled, library did NOT grow
    ka59    24 -> 48       +27         4.52x     cycles doubled, library grew hard

**`sp80` 24→48 is nearly a natural experiment.** Correlational and within-board — `sp80` stopped
minting and stopped growing at the same moment, so those are not separated. **Better supported
than before; still not established.**

**`F15` · exit census of `choose()`** — 17 runs, 5 boards, 4 depths, 247 actions:

| exit | actions |
|---|---|
| `discriminate:learned` | 140 |
| `draw` | 104 |
| `probe` | 3 |
| `routine` · `discriminate` · `discriminate:goal` | **0** |

`routine`'s zero is `F14`. The other two are **not filed on the count** — *never fired* is
absential, and the positive-cause measurement is written and queued. And **`draw` is not the probe
path**, which I had been reading it as all window: `draw` is the last-resort exit, `probe` is the
deliberate boredom perturbation.

---

## 6 · INSTRUMENT ERRORS — three, all mine

**`I1`** · a scratchpad `queue.py` shadowed the stdlib and **executed during `urllib3`'s import**,
its output landing inside an unrelated log. Fires only on the game-loading path — every Phase 3
run — so it would have contaminated the whole window.

**`I2`** · I read a gate refusal off rows I built myself and got `no-mode`, **a property of my
dicts, not the build.** The real token is `step-order`. Fix generalises: **wrap the call the build
makes; never reconstruct its inputs.**

**`I3`** · I confounded my own cost series after writing the rule against it. Cycles 6/11/16
predate the overlap and stand; **16–25 are contended and are not read.**

> Two of the three would have produced a confident wrong statement — `no-mode` names an innocent
> subsystem, and a contaminated cost series is exactly §8's open question.

---

## 7 · HELD FOR YOU — nothing here was decided

1. **Should a learned single-step split preempt FORMING a plan?** (`F14`.) `choose` already answers
   the harder version deliberately for execution — a held routine runs before anything else — and
   **formation appears to have inherited that ordering rather than been given it.** The
   cheapest-looking repair, calling `_mint_routine` every cycle, would make routines reachable
   **and multiply the mint's cost by the cycle count on the exact mechanism §8 is characterising.**
2. **The objective/predictor price tie** — now observed, `F11`. Still unbroken, still published as
   a tie.
3. **§4's producer** — needs a PRED stream admitted to `mint` to serve its purpose. The
   alternative, drawing operands from the library rather than the settled library, conflicts with
   `gamma.units()`.
4. **`E1`'s two candidate fixes** — (a) or (b).
5. **S4's pricing question** — whether a reused term should be priced at full `term_bits`.
6. **§6 doctrine** — with 6a's premise corrected: `slot_types` and `slot_owner` are both declared
   across the membrane, so **composing** a grouping is legal; only **deriving** one by
   name-splitting is forbidden.

---

## 8 · THE TWO COLUMNS, NOT SUMMED

    MECHANISM FIRES     minting scales 1 -> 49 · both contest arms win across the panel · the
                        objective arm takes 74% on ka59 at depth 48 · the price tie observed ·
                        directed action 0 -> 41 of 48 · every refusal names its gate ·
                        vc33 reports an absence as an absence
    CAPABILITY OWED     ZERO routines formed · ZERO levels advanced · ZERO chunk reuse ·
                        levels_completed 0 -- in ALL FOURTEEN board-depth readings, out to
                        48 cycles

**Depth bought mechanism and bought no capability.** Fourteen readings, and the capability column
is unchanged in every one.

---

## 9 · ONE DESIGN DECISION I TOOK, RECORDED SO IT CAN BE OVERRULED

**The brief said run repeatedly so run-to-run variance is visible. There is no variance.**
`Drive()` takes no seed at either construction site and `choose` is deterministic in the cycle, so
**nothing reachable without editing a build file makes two runs differ** — and the freeze forbids
editing. Measured: two `ka59` runs differ on one key, and inside it only random handle suffixes;
`handle()`'s own docstring calls the suffix *a mnemonic, never a key.*

**So repetition was spent on DEPTH**, the only axis reachable from outside the build. **That
substitution is what produced `F1`, `F2`, `F12` and `F14`.** Executing the brief literally would
have produced N identical reports and a *variance is low* line measuring nothing.

---

## 10 · STILL RUNNING

`ls20` at depth 24 under the `F14` timing harness — the second board for the headline finding.
~3700s of ~3950s at last check. **Until it reports, `F14` is a mechanism observed once.**
