WATSON — two figure-faithful fixes from the composition/routine audits (2026-11-21)

This records BOTH fixes the audits found, one BUILT and one HELD PENDING a ground run. It
corrects my WATSON 51/52 framing: the "max_depth=3 / _trees never reached" story was STALE
(cf27e315 fixed the placement; _trees is reached 3/7/13 on default seeds), and "routines
adopted 0" was STALE (bought on cd82 cy14 reach-31, cy56 until(o10.col/38)).

===============================================================================
FIX 1 -- BUILT: a settled term keeps its METHOD when promoted to a unit
===============================================================================
DEFECT (write site gamma.py:2478): promotion emitted `Term(t.atoms, origin=t.origin)`,
dropping operand_term and guard -- so a term settled as f<g(s)> re-entered the search as bare
f. F325 named this ("settles under one identity, promoted under another ... the reusable
chunk is a different computation from the one the ground paid for") and said it had "never
bitten" because operand_term was dead. That premise expired: trees are live (F470/F348).

FIGURES: Fig 12 :103-106 "a settled molecule becomes an atom for whatever composes over it";
:5-14 "the ingredients are recorded and the arrangement is not ... the parts are not the
thing"; Fig 5 amendment "settling is necessary ... and it is not sufficient"; Fig 4 "only
methods cross up ... a binding is a recording"; Fig 13 "the lineage is the term".

CHANGE: `TETHER_UNITS_KEEP_METHOD` (default ON) -- `Term(t.atoms, origin=t.origin,
operand_term=t.operand_term, guard=t.guard)`. The METHOD crosses; the per-board BINDINGS
(operand, guard_ref) stay unset, re-decided per slot at mint. `Term.name` already namespaces
the schema (f<g(:ANY)> vs f . g), so two trees with the same outer atoms stay distinct.
No threshold, bargain, atom, or denominator touched -- the term is made REPRESENTABLE; the
existing _cannot_pay/pays still decide whether it is PAID (Fig 9 :60 filters not verdicts).

LINEAGE / WHITEBOX (the binding constraint): the change adds no hidden state -- units are
plain Terms in the same ledger-visible library; arm declared in conform/arms.py; OFF is
byte-identical (verified: promoted unit is bare `f` with operand_term None). Four must-fail
tests in tests/test_units_keep_method.py, incl. the F325 mutation control (two branches must
stay two units) and a binding-not-carried refuter. ruff clean; test_world2d, test_latchworld,
test_symbols, arms registry all pass.

WHAT WOULD FALSIFY: (i) zero settled terms with operand_term on the panel -> no occasions
(INDEX:48673 "executes is not has occasions") -> the wall is price, not representation;
(ii) after the change every representable depth-2 candidate still fails pays -> correct
abstention, not a representation defect; (iii) any decision/binding/bargain change with the
arm off -> reject. NOT YET RUN on a real ledger in this session -- representation is proved,
contact is not. A per-game run must show a promoted schema being COMPOSED and paid before any
capability claim.

===============================================================================
FIX 2 -- HELD PENDING GROUND RUN: routine price currency mismatch
===============================================================================
The routine bargain is NOT blanket-broken: the gate reaches 6-200 candidates per game and
buys composed plans on cd82 (large integer gap). But there is a UNIT MISMATCH at the write
site: `base` (tether.py:25864) and `left` (25993-94) are computed from `unsat`, which
`goal_residual` returns as a FRACTION, while `loop_budget` (25910), `_claim` (25913-15) and
`Rt.reach` use the INTEGER subject gap. On small-gap boards base≈0.01 bits vs cost≥5.6, so
`cost + left < base` is false by construction for every plan; `loop_budget = max(int(round
(unsat)),1)` = 1, so no multi-step candidate is even enumerated. This is the CLAUDE.md
prohibition "a metric whose denominator the mechanism changes cannot falsify that mechanism"
-- the price is read from the trend fraction while the plan acts on the integer gap.

FIGURE-FAITHFUL FIX (per the audit, NOT applied): use the SAME population on both sides --
the integer step count N = max(_claim,1) (the agent's own expected iterations, Isaiah
2026-09-30) for base and left, with base moved below the _claim block so both see it. The
comparison stays strict: `term_bits(L,n) < reach·log2(n)` -- "a program of L constructors
beats naming reach actions" (Fig 5 :16 mint if it pays; Fig 12 :126 bits price description,
actions price finding out). It does NOT buy on g50t/lf52 (N=1 -> base=2.585 < cost 5.61),
so those refusals stand. Must-fail refuter: large-gap latch run, ON vs OFF, per seed; a
bought plan whose reach>N, or one that fails plan_clears, or small-gap boards starting to
buy, each falsifies it.

WHY HELD: Fig 11 :40 -- change contact first. The audit's own verdict: the kernel change is
warranted ONLY if the latch habitat is run and the routine is still refused with `claim`
large and `unsat` fractional. My latch world has target 1-3 colour steps (small N), so it
does not yet exercise the large-gap case. I did not build a large-gap variant or run it in
this session; doing the kernel change on inference from small-gap boards is the "measurement
taken below the break" error the record warns about. NO kernel price change was made.

===============================================================================
STATUS
===============================================================================
Built and committed: Fix 1 (arm, gamma.py:2478 behind the arm, arms registry, 4 must-fail
tests, OFF identity verified). Held: Fix 2 (derived, refuter specified, no code). Full lineage
preserved throughout: every new decision stays a plain ledger row; no output routes around
the loop; README.md and watson-gpt-banner.svg (another author's work in the tree) untouched.

FIGURE CENSUS: Fig 1 mint if it pays · Fig 4 methods up/bindings down · Fig 5 necessary not
sufficient · Fig 6 more search at same reach · Fig 9 filters not verdicts · Fig 11 contact /
capability=agent-and-habitat · Fig 12 arrangement-is-substance / two currencies · Fig 13
closed set open arrangements / lineage. Strained: none.
