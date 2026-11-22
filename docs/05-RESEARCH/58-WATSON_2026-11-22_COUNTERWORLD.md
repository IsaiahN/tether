WATSON 58 -- counterworld: same-type contact for the count-cause mechanism (2026-11-22)

RESIDUAL (effect terms): `TETHER_INFERRED_CAUSE` (interface cause inference: a COUNT of
presses since a slot changed == n, or a LATCH) is built, default ON, and has never formed a
cause. On latchworld it had occasion (latch.armed: 1,112 rows, `invent` fired at cycles 12/21)
but was type-refused (`above does not accept POSITION`) and `priced_out_at_depth`, `none paid`.

DOMAIN CENSUS:
- R: arity = one cause (slot, action, n); symmetry = a BOOL latch and a COLOUR goal are the
  same "something changed" effect but different types; scale = one board.
- domains: agent-kernel (actors: causes / currency: bits / anchor: the bargain); interface
  (actors: observed effects / currency: counts / anchor: the trace); habitat (actors: presses /
  currency: slot changes / anchor: the ground). Union: "a press changed a slot" spans interface
  and habitat — the cause needs the count from one and the numeric slot from the other.
- order (Fig 3): habitat -> interface trace -> cause formation.

DERIVATION (figures decide, from source SVGs):
- Fig 11 :39-40 "capability is a property of agent-and-habitat ... an improvement that does not
  change contact changes nothing." The cause mechanism is built; what is missing is a habitat
  where the changing slot and the count share a type. Change the contact, not the kernel.
- Fig 11 :48 "what you cannot perceive or measure yet is the residual." The count is in the
  agent's own trace (its presses); the slot change is on the board. Both are perceivable here.
- Fig 12 :5 "the bond is the rest of the information, and it is the half nothing was recording."
  The count->change bond is what the cause names; the world provides it without publishing it.
- Fig 9 :60 filters are not verdicts: the world never tells the agent which action counts.

DESIGN (standalone CounterWorld, world2d contract, one vocabulary):
- Three objects, three `press_i`. One hidden action is the COUNTER, one hidden period N in 2..4.
- Each press of the counter increments a per-action count; on the Nth press since the goal last
  changed, `oG.size` (EXTENT/val) advances by one and the count resets. Other presses advance
  distractor colours. Goal `BECOME(oG.size, target)`, reachable by N-press groups.
- The goal slot is NUMERIC -- the same type the cause mechanism's atoms work on. This is the
  specific difference from latchworld that gives a same-type occasion.
- Seed-drawn wiring before any agent; world reads nothing from the agent; `wired=False` control
  makes the goal directly reachable.

MUST-FAIL CHECKS (tests/test_counterworld.py, 8/8 pass):
contract binds; reachability by construction; REFUTER (no single press moves the goal -- else it
is click_only and the test fails); period exact (no early advance, resets after firing);
non-counter presses never move the goal; goal slot derived + numeric type; control arm direct;
determinism + one vocabulary. gridworld's four families stay byte-identical (verified hashes).

WHAT THIS DOES NOT CLAIM: that the agent now forms the cause. It is a MEANS -- a habitat that
can exhibit a count-conditioned numeric cause. Whether the mechanism fires, and pays, is a
ground run, per game, never pooled. No kernel change, no prior given standing, no ARC game.

FIGURE CENSUS: Fig 1 mint-if-pays · Fig 3 dependency order · Fig 4 kernel/actors-currency-anchor ·
Fig 9 filters-not-verdicts · Fig 11 capability=agent-and-habitat / enumerate / contact · Fig 12
bond-is-the-rest · Fig 13 closed-set-open-arrangements. Strained: none.



## GROUND READ, 2026-11-22 (appended) — counterworld gave an occasion, but the goal cause was not bought

Bounded run: 3 seeds × 40 cycles, direct agent driver, every arm default, supervised (24 GB
ceiling, 1800 s cap; actual wall 51 s, peak 0.37 GB). Per game, never pooled.

| seed | cycles | invent events | settled causes | completed | goal rows |
|---|---|---|---|---|---|
| 0 | 40 | 5 | 1 (`inc?INVENTED` on o0.colour) | 0 | 40 |
| 1 | 40 | 5 | 2 (`inc?INVENTED` on o0/o2.colour) | 0 | 40 |
| 2 | 40 | 4 | 2 (`inc?INVENTED` on o0/o2.colour) | 0 | 40 |

`invent_picks` breakdown: 2 caused causes paid per seed (always `inc?INVENTED` over a distractor
COLOUR slot), and 2–3 `none paid` refusals. The write-site narration shows the cause candidates
were formed (cycles 12–16), so — unlike latchworld, where the BOOL latch was type-refused
("above does not accept POSITION") — the same-type numeric occasion here let cause CANDIDATES
form. That is the specific thing the habitat was built to exhibit, and it exhibited it.

WHAT THIS IS: evidence the mechanism has an occasion on a numeric slot (candidates formed,
no type-refusal). A MEANS working as designed.

WHAT THIS IS NOT: not a capability result. The two PAID causes are the easy `inc` over a
distractor colour, not the count cause over the goal's numeric size slot; the goal's cause was
refused (`none paid`). The goal was not completed in 40 cycles (it needs several N-press
groups). So the agent bought the cheap cause available to it and not the one that closes the
objective. This is consistent with the bargain being strict (Fig 5 "mint if it pays") — a
cheap cause that explains a colour change can pay while the harder goal cause cannot yet.

REFUTERS / next: a longer, properly-budgeted run (more cycles, per seed) would be needed to see
whether the goal's count cause ever pays when the cheap colour causes are exhausted. A null in a
40-cycle run is NOT a finding about the mechanism — "executes is not has occasions" in reverse:
here it HAS occasions and the short run is simply too short for the target. Do not read a
capability verdict either way from this bounded read.

Lineage: full ledger at C:\TETHER_RUNS\CLEANUP_2026-11-21\counter_ground\s{0,1,2}.jsonl;
supervisor sup.json rc=0, peak 0.37 GB. No code or kernel change; habitat and tests unchanged.
