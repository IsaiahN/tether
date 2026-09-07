# THE FREEZE READ — `arc-freeze-01`, the unattended multi-game window

**What this is.** A read of the frozen build against real ARC boards. Nothing was built, nothing was
fixed, no build file was touched. **30 commits, every one documentation.** `git diff arc-freeze-01 --
'*.py'` is empty; 9/9 conformance seats green on every commit.

**Scope.** Public games only, offline and cold, 17 board ids reached. The private/OOD set was never
opened. `arc_holdout.play` crashes at line 221 *after* the loop, so its setup was replicated and the
ledger read directly — `play` was not repaired to make it report.

**How to read this.** Two things are held apart throughout and never collapsed:

- **MECHANISM FIRES** — a thing in the build ran and its record is readable.
- **CAPABILITY PURSUES** — the agent reached a goal on its own.

A synthetic solve proves the first and never the second. Where a slot was handed to the machinery to
see what it did, that is said in the line that reports it.

---

## 1 · THE THREE CONDITIONS

### COND 1 — scope wider than 2

    max scope observed   20        synthetic fixtures capped at 2

**Supplied.** Real boards give the objective a population to be a fraction of; the fixtures could not.

### COND 2 — residual rich enough to buy a term

    means    3.42 .. 15.53     eight of twenty games fall BELOW the ~8.9 cheapest term
    maxima  20.44 .. 36.00     on every one of the eighteen games that mints at all

**Supplied, and the statistic matters.** The condition is *rich enough to pay for a term AT ALL*,
which is a per-ROW question. Sweep 1 read five means and said it held everywhere; that was the wrong
statistic, and the correction is in `INDEX`. **Every game that attempts a mint has rows at 20–36
bits.**

**`8.9189` is not an approximation — it is `term_bits` for a length-1 term at this alphabet**, and it
recurs as the exact cost on every `_install_reuse` row in §5.

### COND 3 — does an objective ever WIN a contest

    contests across the public set    predictor 36 · tie 2 · objective 3   (41 total)
    games where an objective WON      ls20 · sb26 · tu93                   (3 of 19)

**Yes, and on three independent boards** sharing no slot count, scope or action set. **The value arm
takes 88%.** Both halves are the reading: the capability is real and it is rare, and neither number
is the finding without the other.

**Depth does not move it in a direction.** `sb26` improves 6→44 cycles, `lf52` is unchanged, `ls20`
worsens. The contest outcome is a property of the board, not of depth and not of the mechanism.

### `R_goal` range, per board

    board   values observed              shape                      trigger fires?
    ------------------------------------------------------------------------------
    tr87    0.0 · 0.016 · 0.031 · 0.062  near zero, small drift      YES, 2 of 9
    sb26    0.0 <-> 0.923                oscillating, full width     no
    ar25    0.462 -> 0.615               increasing                  no
    tu93    0.044 · 0.971                flat, two levels            no
    ka59    0.857 · [1.0, 0.0]           flat, plus one large drop   no
    ls20    0.85 · 1.0                   flat                        no
    lf52    1.0                          flat at maximum             no
    bp35    1.0                          flat at maximum             no
    re86    1.0                          flat                        no
    dc22    --                           `_res` empty                no

**Amplitude is not the property; monotonicity over the last three readings is.** `sb26` swings the
full width of the range and qualifies never, because an alternating series always answers its own
decrease. `tr87` drifts by 0.03 and qualifies.

---

## 2 · MECHANISM FIRES — what is built and was measured running

**The trigger fires unaided.** `tr87`, override disabled at source, ten cycles of the agent's own
trajectory: the real `_goal_choice` opened on **2 of 9 gate evaluations**, and `CAN` returned `yes`
both times. Sixteen boards silent and one firing is the correct shape — a gate keyed on a
confidently shrinking residual should stay shut where nothing shrinks.

**Handed a slot, the whole chain runs on real perception.** Five boards of thirteen non-excluded run
end to end: `sb26`, `ka59`, `tr87`, `re86`, `ar25`. Composer returns 4–8 candidates; guards are
`CAN`-checked; the budget is derived from the gap.

**The bargain discriminates, with no threshold anywhere in it.**

    board  routine                        cost    left    base    verdict
    ---------------------------------------------------------------------
    sb26   ACTION5                       3.1699   1.0      2.00   cut
    ka59   ACTION1                       4.6439   0.0      2.00   cut
    sb26   until(o20.w/3)   {ACTION5}    4.7549   0.0      3.00   cut
    tr87   until(o54.dcol/3){ACTION2}    6.9658   0.0      6.00   cut
    sb26   until(o20.w/23)  {ACTION5}    4.7549   0.0     23.00   PAYS
    ar25   until(o13.drow/13){ACTION1}   8.4221   0.0     33.60   PAYS
    re86   until(o24.dcol/24){ACTION3}   7.7549   0.0     55.73   PAYS

`cost + left < base` on every row. Description cost is flat across every `until` shape — `term_bits`
reads length and alphabet only, by design — so what moves is `base`, and the crossover falls out of
the arithmetic. **The bare-action row is the two-part bargain earning its pre-freeze repair:** `cost
3.17` with `left 1.0` is *cheap to say and does not finish the job*, and folded into one number no
reader could see which half killed it.

**The execution half runs.** `sb26`, 45 cycles: `advance` called 75 times, the budget decrementing
one per cycle and the rest returned being itself a routine — cross-step state on real perception
rather than a fixture. **Both non-completing terminations occur and are recorded apart:** `blocked`
at c15 with 15 of 23 budget unspent, `exhausted` at c41 carrying its whole §18.2 payload — `status:
refuted`, `rejections`, and `reopens_above` pinned to the goal residual at the moment of failure.

---

## 3 · CAPABILITY PURSUES — three blockers, located

**`levels_completed` is 0. `done` is 0. No routine has been minted from a slot the agent chose
itself.** The window's contribution is that the reason is now named per board rather than pooled.

    no objective binds        sk48 · sp80 · wa30      the missing WIRE, already named unbuilt
    _goal_split finds no      tr87 unaided, and       the trace carries no action-to-slot
      learned route           5 boards under override   evidence under phase: probe 1.0
    the trigger declines      the other 9 boards      correct on a non-shrinking residual

**One uniform loop, no type branching between them** — the loop reporting a difference in the
habitat rather than in itself.

### And the deepest of the three is binding

15,304 `goal_residual` calls across five boards, no override, classifier agreeing with the build on
every call:

    board   calls   nothing bound   bound, not OBJ   READABLE   OBJ share
    ---------------------------------------------------------------------
    sb26     3394        3339             25            30        55%
    lf52     7552        7486             52            14        21%
    ka59     1642        1560             72            10        12%
    wa30     1590        1563             27             0         0%
    sp80     1126        1053             73             0         0%
    ---------------------------------------------------------------------
    TOTAL   15304       15001            249            54        17.8% of bound

**An objective is bound and readable on 0.35% of slot-cycles.** `lf52` has 480 slots and **one**
carries an objective — `o59.w`, the same slot sweep 3 read as flat at 1.0 for 31 cycles.

**The zero is exact; the ordering is not.** Both 0% boards are precisely the gate-0 boards, on 5 of
5. But the share does not order the rest — `ka59` at 12% reaches the bargain while `lf52` at 21%
does not clear `_goal_split`. **A monotone reading was available and is false.**

**Three of `goal_residual`'s five `None`-exits have never fired.** The slot never vanishes from the
state, the peer group is never empty, `objective_degree` never fails to resolve. Recorded with its
denominator: *never fired* and *cannot fire* are different sentences and only the first is measured.

---

## 4 · LOG 1 — SYSTEM ERRORS, with candidate fixes

**S1 · `probe.choose` divides by zero when no action is surfaced.** Six of 25 public games advertise
exactly one action and surface none; the adapter dropping a positioned click it cannot supply is
correct, and `probe.choose` crashing on the resulting empty tuple is not. `tether.py`'s own first
line says *or there is no action*, and the loop never reaches that outcome. **Candidate fix:** take
the existing no-action outcome where `self.actions` is empty.

**S2 · `arc_holdout.play` crashes assembling its report.** `dict(Counter(r["detail"]["by"]))` —
`by` is a string on action rows and a dict on the `mode` row. `A6i` in the ledger's detail schema.
**Candidate fix:** key the counter on one type, or stop reusing the field name.

**S3 · Four of the eight gates in `_mint_routine` return with no ledger row.**

    1. slot is None / not in before   SILENT      5. CAN != yes          row
    2. gap is not an int              SILENT      7. no candidate        row
    3. R_goal is None or <= 0         SILENT      8. guards unreachable  row
    6. _goal_split returns None       SILENT      9. does not pay        row

Not game-gated. **The proof of harm is a measurement it already cost:** sweep 7 read `rows written 0`
across 37 entries and could not tell gate 1 from gate 6, which is why sweeps 8 and 8c had to build
wrappers. **Candidate fix:** a `routine_refused` row at each of the four carrying that gate's reason.

**S4 · `_install_reuse` admits into Γ what the bargain would refuse — 19 of 21.** See §5.

---

## 5 · S4 IN FULL — the question the build asked itself

`_install_reuse`'s docstring, unedited:

> *"`_install_reuse` was never called across the demo panel ... So the row states what the bargain
> WOULD have said ... **the first run that exercises this path answers the question instead of a
> decision made without one.**"*

**The path is exercised on 13 of 17 public boards. The run has happened.**

    board   installs   would_pay=False        cost          base
    -------------------------------------------------------------------
    lf52       3          2 of 3            8.9189      3.32 – 12.00
    wa30       5          5 of 5            8.92–13.38  3.91 –  7.00
    sp80       5          5 of 5            8.9189      3.32 –  7.00
    ar25       4          3 of 4            8.9189      7.00 – 12.00
    dc22       4          4 of 4            8.9189      7.00
    -------------------------------------------------------------------
    TOTAL     21         19 of 21  (90.5%)

**The split is arithmetic, not noise.** Both `would_pay=True` rows carry `base = 12.00` against
`cost = 8.9189`; every one of the nineteen refusals carries `base <= 7.00`. `left` is `0.0` on all
twenty-one, which is the condition this path enters on.

**And it lands exactly on COND 2's scale.** The condition asks whether the residual can buy the
cheapest thing sayable. **On nineteen of these it cannot — and the term enters anyway**, because
this path tests `left == 0` and never asks the question COND 2 exists to ask.

**Candidate fix is the one the docstring names:** consult `pays` here as `mint` does. Its stated
blocker — *no board on which to read the change* — is removed twenty-one times over, and `would_pay`
means the before is already recorded.

**It reaches the ablation clause.** A third entry path consulting no bargain is a category the wipe
partition does not name. **The mitigation is already in the code:** `gamma.accept(cand, ...,
residual=f"reuse:{slot}@{self.cycle}")` stamps these distinctly, so the ablation can separate them.
**The provenance survived even though the pricing did not.**

**And it may be the same fact as the cost wall.** Library baseline is 21, measured. Across those five
boards, growth was 46 and **21 of it — 46% — entered through this path.** LOG 3 locates the wall in
`mint` pricing a candidate space that grows with the library. Each link is measured; **the
composition of them is a hypothesis, and the counterfactual is a build change the freeze forbids.**

> **HELD APART, AND IT IS THE HALF THAT COULD MAKE THIS A NON-ERROR:** whether a REUSED term should
> be priced at full `term_bits` at all is a design question, not a measurement. If reuse is properly
> cheaper than derivation, nineteen refusals are nineteen correct admissions at a wrong price. **The
> measurement is unambiguous and its interpretation is Isaiah's** — which is the shape the docstring
> set up.

---

## 6 · LOG 2 — GAME QUIRKS, and not one carries a candidate fix

| | | |
|---|---|---|
| **Q1** | six games supply only a positioned click | correct given input |
| **Q2** | `ka59`/`sp80` mint no objective in six cycles | **resolved and split** — `ka59` binds at 14 cycles, `sp80` never at 16 |
| **Q3** | action counts vary 1–7 across the set | habitat property |
| **Q4** | `su15` mints nothing in six cycles | no live mass, so it probed — `choose`'s stated safety property |
| **Q5** | `wa30` attempts 57 mints and buys none | the bargain refusing a thin residual |
| **Q6** | `sk48`/`sp80`/`wa30` bind no readable objective | the missing WIRE, absent by design |
| **Q7** | `dc22` reads an objective on 1 cycle of 13 | third shape, **no account offered** |
| **Q8** | `CAN` yes with `_goal_split` None, same slot | three disjuncts; the one that fires carries no action evidence |
| **Q9** | `tu93` stops calling `_goal_choice` after cycle 5 | **cause unestablished and not guessed** |
| **Q10** | `tr87` refuses its own routine by 0.97 bits | a bargain that paid would be the defect |
| **Q11** | seven of nine residual series never reach length 3 | `note_goals` popping an unreadable objective is right |
| **Q12** | an objective is readable on 0.35% of slot-cycles | cross-board, and the WIRE measured |

**Q8 deserves its line.** `can` reaches `yes` by three disjuncts — *holds now* · *has held before* ·
*an action has been observed to move it that way* — and only the third is the evidence `_goal_split`
needs. The disjunct that fires on `tr87` is the second. **The route requirement is strictly stronger
than the guard requirement and should be**, since `Until` commits to repeating an action.

---

## 7 · LOG 3 — THE COST WALL

**The `calls × slots` model is refuted across boards.**

    board   slots   bet rows   bet*slots/cycle    ACTUAL s/cycle
    lf52     480      7584        227,520             0.90
    tr87     520      4066        264,290            88.92

**16% apart in the predictor, 99× apart in the cost.** `bp35` carries the largest product in the set
and costs a third of `ar25`, whose product is 184× smaller.

> The original `ls20` profile is not wrong; **its scope was one board.** *916,212 calls × 168 slots =
> 153.9M against 153.3M measured, ratio 0.996* is sound accounting of what `_record` does on `ls20`,
> and it was read as a model of the wall. **A ratio of 0.996 on a single board fits itself.**

**Profiled at both ends.** `mint → _cannot_pay` is the wall on both; what differs is where
`_cannot_pay` spends — almost all `_record` on `lf52`, spread across `_record`, `objective_step`,
`_sat` and `gamma.apply` on `ar25`. **It runs 40,835 times per cycle on `ar25` against 5,297 on
`lf52` — 7.7× more work with 4× fewer slots.**

**Which function grows with history: the candidate space, because the library does.** `ar25` enters
`mint` 73 times in 4 cycles against `lf52`'s 9 in 10. The per-cycle curves show it directly —
`lf52` 2.37s → 4.24s, `ar25` 1.23s → 11.08s.

**`_left` stays refuted, now on two independent grounds.** The trace is 8 long after 8 cycles (an
argument about the input), and `tottime 0.177s` against `cumtime 9.600s` says it walks nothing itself
(an argument about the work).

**NO CANDIDATE FIX, deliberately.** The cost is `mint` pricing a space that grows as the agent
learns — the mechanism working, not a defect in it. A performance change to the one loop the whole
instrument reads is the trade `CLAUDE.md` names as a loss.

---

## 8 · THE PANEL, CHECKED RATHER THAN USED

The standing brief names a five-game sample and expects `routine-fires` unreadable everywhere, *the
wall confirmed per-build*. The prior question is whether the panel could show it:

    ls20    4 actions,  objective on  9 of 11 cycles    reaches gate 6
    ar25    6 actions,  objective on  6 of  8           reaches the bargain
    ka59    4 actions,  objective on  5 of 14           reaches the bargain
    vc33    0 actions   --                              NO. nothing acts
    sp80    5 actions,  objective on  0 of 16           NO. no objective exists

**Two of the five cannot produce a routine for reasons that have nothing to do with routines.** The
sample's null is a null on three boards, and *the wall confirmed per-build* is the right account on
three and the wrong one on two. **The expectation is not wrong about the wall — it is wrong about
what this panel can isolate.**

**What a panel would need, stated so it is checkable:** an action surfaced, a readable objective, a
residual the trigger accepts, **and** one large enough for the bargain to pay. The first three are
satisfied somewhere in the seventeen. **The fourth has not been observed together with the third.**

---

## 9 · MY OWN INSTRUMENT ERRORS

**Eight this window. Six caught before the finding was written; one caught only because it
contradicted an established result.**

| | what it was | how it was caught |
|---|---|---|
| 1 | key filter dropped `outcome`; `routine_end` looked inconsistent | read the write site before writing the finding |
| 2 | two `_goal_choice` call sites conflated by the `in_mint` flag | checked call sites for three functions, then the fourth |
| 3 | the override perturbed the trajectory it measured | the record had already adjudicated the same board |
| 4 | `maxdisc` from a loose `awk` field filter | **it contradicted a result two sweeps old** |
| 5 | heredoc patch failed silently; a run launched unpatched | `grep`ed the probe for the patch before reading output |
| 6 | classifying whole series where the mechanism reads a tail | earlier in the window |
| 7 | post-hoc probing at instants the loop never samples | earlier in the window |
| 8 | claimed the cost wall truncated `ka59`'s falsifier series | ran it twelve cycles further and it produced nothing |

**#4 is the one worth keeping.** Had it read plausibly it would have shipped. That is the argument
for selecting on a named key rather than on a shape whenever both are available.

**#8 is a substantive self-correction.** I wrote that `Q11` was wrong and the wall had truncated the
series. `ka59` got twelve more cycles and fired zero times; `o14.dcol` was gone from `_res` entirely.
**`Q11` was right and my correction to it was withdrawn.** The tell: it made the wall the villain of
a question the wall was not in — a story that indicts an instrument rather than the world, supported
by a real timeline, and available before the run that could refute it.

---

## 10 · WHAT THE WINDOW DID NOT ESTABLISH

- **Whether `tr87`'s gate-6 pass and `routine_cut` came from a real slot or an overridden one.** The
  probe tags neither. The unaided run settled the trigger; it did not settle this.
- **Whether reuse should be priced at full `term_bits`.** §5's held-apart half.
- **Why `tu93` stops calling `_goal_choice` after cycle 5.** Q9, cause unestablished on purpose.
- **Why `dc22` reads an objective on exactly one cycle of thirteen.** Q7, no account offered.
- **Whether the other 54% of library growth is bargained.** `mint` consults `pays`, so it is
  presumed — presumed, not read.
- **Whether the three never-fired `None`-exits can fire.** Five boards is the denominator.

---

## 11 · WHAT IS OWED TO ISAIAH

1. **S4's interpretation.** The measurement is unambiguous; whether it is a defect turns on the
   pricing question the docstring set up.
2. **The action policy.** `_goal_split` needs a trace where some action is observed to move a slot
   consistently. `phase: probe 1.0` accumulates that only by coincidence. This is the one change that
   would plausibly move contact rather than instrumentation — and it is a ruling, not a repair.
3. **The four candidate fixes in LOG 1**, none applied, all with the reintroduce-the-defect test
   available.

**Nothing in this document was acted on. The tag is intact.**
