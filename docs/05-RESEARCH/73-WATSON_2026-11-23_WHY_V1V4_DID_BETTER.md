WATSON 73 — why the older agents did better: blindness, raw pixels, or population? (2026-11-23)

ISAIAH'S OBSERVATION: the ARC board is an image; the older Ouroboros v1-v4 agents, "not any more
special than this," could figure out the games "with enough generations," while this agent clears 0.
He suspected the agent is bad because it converts the board to typed slots and never sees the pixels,
and offered: "blind animals just have lower evolutionary cognition... there's just less data to
process." He asked that the WATSON bear this out, and said no arm test is needed.

## QUESTION
1. Do the figures support "less data to process -> less capable"? (yes, derived below)
2. Is the historical difference v1-v4 vs Tether actually about raw pixels / blindness?
3. What SHOULD we conclude about why the old agents did better?

## TETHER (primary, verbatim, 13 quotes verified)
- Fig 3: "perceive · plan · act · predict"; "it has terms for what things afford: what can be moved,
  opened, joined, blocked" -> "what the search can reach" -> "reached, so its state can be read" /
  "not reached, so not assessable." -> PERCEPTION IS UPSTREAM; fewer readings = less reachable. Your
  "less data to process" is figure-faithful.
- Fig 3: "Optimising a link that already works cannot rescue one that does not." / "A link with no
  instrument is not a link that works. It is a link nobody has looked at." -> polishing the loop
  cannot recover a perception it never had.
- Fig 11: "A system cannot be made more capable by improving the agent in isolation. An improvement
  that does not change contact changes nothing, however much it improves." / "You do not invent the
  list. You read it off the world, and what you cannot perceive or measure yet is the residual."
- Fig 6: "MINT composes inside the closure and can never add an atom." / "No frame escapes its own
  closure. The bound moves only on contact with a frame whose closure differs." / "instruments extend
  what can be represented at all." -> a frame's reach is bounded by its instruments; this is the
  mechanism behind your intuition.
- Fig 1: "perceive · plan · act · predict"; guards "support · reach · novel."

## WORLD / HISTORY (secondary; v1-v4 read from the actual repos by a fresh investigation)
- **The hypothesis is PARTLY refuted.** v1-v4 did NOT search raw board states. Raw 64x64 frames were
  the INPUT (Ouroboros-v4 `game_player.py:278-282` -> ndarray(64,64)), but the search was over a
  POPULATION OF AGENTS across generations: `evolution_runner.py:228-231` "population_size=100,
  agents_per_generation=30, games_per_generation=3, max_generations=10"; `_calculate_arc_fitness`
  and "zero_fitness_detected: evolution is RANDOM DRIFT" (`:160,225`). Knowledge crossed agents via
  a shared SQLite "network brain" and "viral packages" (README.md:301,114,126-129).
- v3 ALREADY had typed perception (VisualCortex, PerceptualField with objects/delta/goal_state) but
  it was disconnected: "1 out of 80 rungs reads it" (PERCEIVE_THINK_MAP_ACT_v3.md:27). So typed
  perception is not new to Tether and is not the thing that changed.
- **The record states the tradeoff explicitly**: tether/CLAUDE.md:1270-1276 — "cold start is valid
  and Isaiah has already demonstrated it in general (Ouroboros v1-v4)... Three ways to pay the bill
  — evolution's bodies and time, a PARALLEL POPULATION splitting it by numbers, or inheriting from
  something that already paid. WE HAVE ONE AGENT, so two of the three are unavailable. Frontloading
  is the substitute for population size." So Tether deliberately gave up population/generations.
- **Evidence of old success is conflicted and I report both sides verbatim**:
  - Isaiah's corpus claim: THE_ALIGNMENT.md:11-14 "v1-v4 beat ls20, vc33, ft09 — dumb
    agents, smart network, could not explain themselves." (read by the investigating subagent from
    Ouroboros-Redux; I did NOT independently re-verify this exact line in the local checkout — the
    v4-side numbers below I did verify directly via `git show Ouroboros-v4:loop_state.md`).
  - v4's own metrics snapshot: loop_state.md:12-27 "VC33 has 0 level completions across ~18,853 games";
    "FT09 has only 2 level completions across ~335 games"; "alignment_velocity: 0.00 (no full game
    wins)"; generation 5112. No independent scorecard was found. The claim is not resolved here.
  - The "clears 0 games" number belongs to REDUX, not v1-v4: WHAT_REDUX_MEASURED.md:14-16 "Redux
    ended at 3 of 183 levels, 0 of 25 games. A uniform-random policy scores 7 of 183." (verified
    directly in tether's own docs/carryover/WHAT_REDUX_MEASURED.md).
- What persisted v1->v4 was NOT a subsystem (all 37 dropped by v3) but "the generative question"
  (THE_DESCENT.md:220-222) and the allocentric network thesis: "dumb agents en masse become
  intelligent in a marketplace" (:234-239).

## VERDICT (from the figures, honestly reconciled with history)
Your "less data to process" is RIGHT as a figure-derived mechanism: perception bounds reach (Fig 3/6/11),
and the current agent sees typed slots only, so it has fewer instruments than a frame that also reads
the raw image. Fig 4's round trip throws away detail going up, and that loss is real.

But the history does NOT support "the old agents won because they saw raw pixels." They saw raw frames
AND ran a population+generations search with network-level method transfer — that is the difference
the record names, and it is exactly what Tether traded away (one agent, frontload instead of population).
Blindness to images is a real additional loss (WATSON 72: zero recognised rows; board passes is_picture),
but it is not the whole explanation, and the "blind animals" analogy overstates it — the figures' claim
is about instruments bounding reach, not about a hierarchy of intelligence.

So the honest answer to "why did the old agents do better": the record says bodies + generations + a
network that transferred methods — not raw-pixel search. Tether's fork chose legibility and a single
whitebox loop at the cost of that population, and frontloading was the declared substitute. The
chunking feeder (WATSON 69) is the current attempt to recover generational contact within one agent;
it has not yet been settled to ground (run died to the disk outage). The image-route connection
(WATSON 72) is a real, separate loss worth an experiment, but it should not be mistaken for the main cause.

**Reversed by:** a settled chunking sweep showing whether generational contact moves the ground;
and the pre-registered image-route A/B (WATSON 72) showing whether a shape reading moves reach. Both
are measurements, not claims.

**Cost if wrong:** attributing the failure to blindness would send us to wire images while leaving the
population/generational gap untouched. **Undoable:** yes.

FIGURE CENSUS: Fig 1 · Fig 3 · Fig 4 · Fig 6 · Fig 11 (verbatim, 13 quotes verified). Strained: none.
Anchor: Ouroboros-v4 evolution_runner.py:228-231, game_player.py:278-282, README.md:114/126-129/301;
PERCEIVE_THINK_MAP_ACT_v3.md:27; tether/CLAUDE.md:1270-1276; THE_ALIGNMENT.md:11-14; loop_state.md:12-27;
WHAT_REDUX_MEASURED.md:14-16; THE_DESCENT.md:220-239.
