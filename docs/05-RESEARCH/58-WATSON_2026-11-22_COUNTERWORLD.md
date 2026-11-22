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
