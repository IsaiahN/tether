WATSON — the intent/interface seam, and why colour is the wrong key (2026-11-21)

PROMPT: Isaiah — "the problem with this is that games change their colour. is a cheap key but
merely temporary and wont hold. its like trying to stick something to the wall with gum.
Furthermore the agent is merely supposed to come up with its INTENT, and the interface
interprets what that means in terms of actions. that way, this agent could drive a car
autonomously if it needed, or steer a ship or play a different game etc."

This is a CORRECTION to my WATSON 51/52 framing. I had written the gap as "compose a cause
keyed on the latch/colour slot" and proposed a kernel fix. Isaiah is right that this is the
gum fix: colour is a temporary property of one habitat's actors, and Fig 4 forbids baking it
into the reasoning. The figures decide; I re-derived and re-audited the code. Verdict below.

===============================================================================
1. THE FIGURES DECIDE — the seam is Fig 4, not a patch
===============================================================================
- Fig 4 :19-20 "The kernel is the part that does not change with size: the same loop and the
  same rule for naming what worked ... **Only the actors, the currency and the anchor change.**"
  → the invariant part of the agent is the reasoning; the habitat-specific part (button names,
  colours, action vocabularies) is what varies. Colour belongs BELOW the seam.
- Fig 4 :7 "it has terms for what things afford: what can be moved, opened, joined, blocked."
  Fig 12 :115 "having terms for what a situation affords was taken for a dictionary and it is
  a grammar." → the agent reasons about AFFORDANCES in NSM primes, never about buttons.
- Fig 11 :39-43 capability is agent-and-habitat; "The habitat is enumerated, never composed";
  "you do not invent the list, you read it off the world" (:48). → the interface reads the
  world's action vocabulary off the world; the agent never authors it.
- Fig 6 :26 "The world does not gain primitives; a frame gains access." A new habitat changes
  what is reachable, not what is said. The car/ship generality is exactly this: swap the
  actors (interface), keep the kernel (intent reasoning).

SO the architecture Isaiah states is not a new idea — it is Fig 4 applied to the action
boundary, and it is ALREADY A BINDING RULING in this repo (2026-09-14, reaffirmed 2026-09-28).

===============================================================================
2. WHAT THE REPO ALREADY HAS — the seam is BUILT and REACHED (audit, re-verified)
===============================================================================
`docs/03-DESIGN/03-ACTION_INTERFACE.md` (762 lines, title "a plan, not a build") opens with
Isaiah's 2026-09-28 instruction verbatim and the 2026-09-14 ruling: *"ACTIONS MUST NOT BE BAKED
IN — action-mapping happens AFTER, is trivial, and must stay agnostic."* The seam:
  ABOVE: systems 0/1/2 emit INTENT in NSM primes; never name, price, or wager on an action.
  INTERFACE: `Interface` (`interface.py:536`) "Translates intent down, reports capability up.
  Knows nothing about goals"; holds a table of what each action was OBSERVED to do, empty at
  birth, built only by acting.
  BELOW: the world's advertised action names.

Implementations (all default ON, all reached):
- Intent (`interface.py:350-366`): "What the agent wants to be true. It names no action and
  carries no button. Multi-step is a TUPLE of these." Fields: kind, subject, object, repeat,
  value. The verbs are NSM prime compositions: ELICIT="BECOME OTHER", TOUCH, BE_AT, BECOME,
  DISTINGUISH="NOT SAME" (`interface.py:55-72`).
- `Interface.realise(intent, offered, ...)` (`interface.py:657`) → one `Realisation` (action,
  coord, why, term, evidence). 25 `.realise()` call sites in tether.py; `_explore` forms
  `Intent(ELICIT, subject)` at :22351; goal path forms `Intent(BECOME, slot, value=tgt)` at
  :11683-11701. The interface picks the action from `offered` — availability, not semantics,
  reaches the agent (F28's hard line).
- `_took` (`tether.py:26268`) keeps the intent beside the realisation; the action is sent at
  :17913-17917; `audit()` reports capability back up. A routine step is an INTENT
  (`_realise_step`, :26511), re-realised every step, so a mid-plan remap is survived.
- `Action.action` in `routine.py:62-75`: "NOT a button — what the agent WANTS that step to
  achieve."

So "the agent emits intent and the interface interprets it into actions" is NOT something to
build — it is the operating architecture today. The car/ship generality comes for free: swap
the interface's action vocabulary, keep the intent grammar. No colour, no button name above
the seam.

A STALE RECORD to correct: `tether.py:5289-5294` still says "The strip that moves CHOOSING
through it is step 2 and is not done" — contradicted by 25 realisation sites. I am annotating
it, not acting on it. (Same stale-record class as the 53-min step.)

===============================================================================
3. WHAT IS ACTUALLY NOT BUILT — narrow, and domain-general
===============================================================================
- `tether.py:18277-18296` `_route_reward`: the reward channel's remedy "composing actions that
  advance the objective — is not built"; `remedy="deferred: composition of actions is not
  built at agent scale"`. This is what my latch run exhibited (48 goal candidates, 0 checked).
- `interface.py:1405-1410` `leads_to_gap`: "ONE STEP ... looking further would be planning over
  the map, and is not built." `reach()` is a one-step count over the observed table.
- `realise()` returns ONE `Realisation`, never a tuple. `Intent`'s "Multi-step is a TUPLE" has
  no consumer; routines compose repeated intent STEPS, not interface-side path search.
- `BE_AT` is declared (`interface.py:57`) with no realisation branch. `BECOME(slot,value=v)`
  single-step outcome IS served (the `lands` table, `interface.py:818-906`, keyed by
  `(ctx, slot, before) -> after`, "IT SAYS THIS HAS HAPPENED, NEVER THIS WILL").

SMALLEST ADDITION (domain-agnostic, no colour key): one interface-side `realise_outcome` that
takes an existing `Intent(BECOME, subject, value=)` and searches the interface's OWN
`(context, slot, before) -> after` table for a bounded multi-step path, returning a TUPLE of
Realisations; extend `_took`/`_realise_step` to accept the tuple and re-resolve each step. It
keys on slot readings and observed effects only, with relationality asked of the world via
`env.relational_slots()` — never colour or action names. Open sites: `interface.py:1410` and
`tether.py:18296`. Reuse `frontier_pick` for tie-breaks; keep intent and realisation both in
the record. No atom, no new sense, no text channel, no ARC game.

===============================================================================
4. CORRECTION TO MY LATCH HABITAT
===============================================================================
WATSON 52 framed the latch as giving a "BOOL→COLOUR cause" a contact surface. That framing was
wrong: the agent should never key a cause on colour. The habitat is still useful AS A SURFACE —
it made the agent say `composition of actions is not built` at the write site — but the thing
to build is the interface-side outcome→path planner above, NOT a colour/BOOL cause in Γ. I am
annotating WATSON 52 with this and leaving the kernel untouched.

===============================================================================
5. WHAT IS BEING DONE / STATUS
===============================================================================
Recorded: this WATSON + an annotation on WATSON 52 + the stale comment at tether.py:5289. NOT
done (deliberately, pending Isaiah): the interface-side `realise_outcome`. That is the real
GAP 2 fix, it is domain-general, and it is the one change that would let the agent pursue a
multi-step intent — the prerequisite for "drive a car / steer a ship" being a matter of
swapping the interface, not the agent. No code changed in this WATSON beyond the doc.

FIGURE CENSUS: Fig 1 claim/mode · Fig 3 dependency order · Fig 4 kernel/actors-currency-anchor /
affordances-as-grammar · Fig 6 primitives vs access · Fig 9 describe-effect · Fig 11
capability=agent-and-habitat / enumerate / read-off-world · Fig 12 two currencies / affordance
grammar · Fig 13 closed set open arrangements. Strained: none.

Sources: read-only audit of interface.py, docs/03-DESIGN/03-ACTION_INTERFACE.md, tether.py,
routine.py, speak.py, gridworld.py, arc_world.py; key claims re-verified at write sites.
