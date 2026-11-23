WATSON 69 — the chunking method and the human replay: reconciling Isaiah's solution with WATSON 68 (2026-11-22)

ISAIAH'S WORDS: "I had a solution for this but I fretted teaching the agent this way. Look up the chunking method and the human replay. It was meant to teach the agent how to compose like a human."

## QUESTION
1. What exactly is the chunking/human-replay method, and is it BUILT?
2. Was Isaiah's fret (teaching the agent from human replays) justified — does it encode answers / breach the walls?
3. Does this change WATSON 68's verdict that "contact" is missing?

## SEARCHED (the record — M8: check first)
All of this was already specified and mostly built. Verbatim, file:line:

- **The purpose, in Isaiah's own words** (INDEX:36989-36993): *"the shuffle is so the agent would not transform and learn and unlearn stuff, or associate a recipe with one game."* §14.5: *"sequential training would DEFORM the shapes: defeasible demotion means a later game can actively un-settle an earlier game's composition."* The mechanism is so *"only the shapes that recur EVERYWHERE pay off; the shared compositions settle hard as invariants before any game applies pressure."*
- **The fret is already answered in the design** (`feeder.py:40-42`, KEY_BOUNDARY): *"the tape carries FRAMES, which are what the world showed. It never reads the answer key's compositions or effects — `rlvr` does that, afterwards, to score. Watching a human play is not being told the answer; being handed the derivation would be."* This is Fig 4's membrane made mechanical: the agent EARNS the composition by predicting and being wrong against a trajectory it did not choose (`feeder.py:18-21`), nothing is installed.
- **BUILT**: `feeder.py` (492 lines) — `ReplayTape`, `chunk_order(offset/spacing/skip/take)`, `watch`, `watch_many`, `probe`, `sweep` with the reviewer's pre-registered ladder 1/2/4/8/16. Commits `18f83f2`, `3f938cb`; refined `1c341dae`, `56369ab5`. Seat-side: the agent does not import it (`feeder.py:4-5`), exactly like `arc_holdout`.
- **The design is a tape behind the EXISTING world** (`feeder.py:13-16`): same segmentation, slots, atoms and perception path — no second world. The library switch was already built (`play(library=...)`, §17.8). One dial, spacing, IS §14.5's annealing (`feeder.py:23-28`).
- **The reviewer retired my binary design before commit** (INDEX:37125-37129): coherent/shuffled were the two ends of one dial; the spacing ladder is §14.5 in one parameter. The witness is the TRANSFER CLIFF, never the rise (pre-registered 09-18): *"a real capability degrades GRADUALLY as spacing widens; a marker-follower holds flat then drops off a CLIFF"* (verbatim: "holds flat then drops off a CLIFF").
- **The measure is game-locality** (INDEX:36997-37004): 1,468 distinct effect signatures across 25 boards, 94% on one board only, the whole cross-board set ~94 (6%). The agent's one learned shape is `{moved 2, resized 2}` — the dominant family at the 2-board tier, not the 7-board one. *"THAT IS THE SYMPTOM OF THE MISSING SHUFFLE, STATED AS A MEASUREMENT."*
- **CAPABILITY UNCLAIMED, deliberately** (INDEX:37151-37152): *"A sweep is in flight; no rung has landed. Mint count is frame-internal and is not evidence — the ground reading is the probe."* The first coherent-vs-shuffled effect (3 vs 28 mints) was WITHDRAWN as a population error (different content, not ordering). No sweep artifact exists on disk.

## DERIVATION (figures, verbatim)
- Fig 4: "Only methods cross up. Only head starts come down." / "a head start, never a recording" -> the tape carries FRAMES (observations), the agent MINTS the method; the answer derivation never crosses into the agent. This is exactly why the fret is unfounded: it is not a recording being handed over.
- Fig 6: "No frame escapes its own closure. The bound moves only on contact with a frame whose closure differs." -> watching human trajectories is contact with a frame whose order/closure differs from the agent's own play; that is the licensed way the wall moves, not an answer key.
- Fig 11: "capability is a property of agent-and-habitat." -> the tape is a substituted habitat (frames in the existing world), so it is a contact change, which is what moves capability.
- Fig 1: "The ground enters as the only metric." / "A frame cannot score itself with a quantity it also produces." -> hence the capability stays UNCLAIMED on mint counts; only the ground probe can settle it. The record's restraint is figure-correct.
- Fig 2: frames range against the ground, they do not negotiate -> `rlvr` scores afterwards; the tape never grades itself.

## VERDICT
1. **"What are we missing" (WATSON 68) must be corrected: contact has a designed, built mechanism already.** The chunking feeder IS the contact device — the agent watches human frames in an order the seat controls, predicts, is wrong, and earns compositions without being handed any derivation. It was never run to a ground verdict, which is why the loop products looked starved. Missing is not the mechanism; missing is the SWEEP's ground reading (the transfer cliff), i.e. the experiment has not been settled, not that the capability is absent.
2. **The fret was justified to raise and is already structurally answered.** The danger Isaiah felt is real (being handed the derivation = answer-encoding, the unforgivable failure), but the KEY_BOUNDARY refuses it: frames only, never compositions/effects; the agent mints them itself; rlvr scores after. Under Fig 4 this is a method earned by contact, not a recording installed. It does not hit the copyright catch-22 either: these are the 25 public human replays, held seat-side outside the repo, already authorized as a READING (Isaiah 14:03).
3. **Human replays are the data-light, copyright-clean version of the Phase 2 walkthrough idea** — same shape (state + human trace), but the frames are the world's own and no guide text or answer derivation enters the agent. This is the bridge from WATSON 65/67 that needs no external content and no unshippable data.
4. **What remains is a measurement, not a build.** The pre-registered witness exists (transfer cliff), the dial exists (spacing 1/2/4/8/16, library carries, ramp upward, identical frame set per rung), the probe exists. The honest next step is to RUN the sweep to a ground verdict — not to build another mechanism. Until then capability stays UNCLAIMED, as the record already says.

**Cost if wrong:** running the sweep and finding no cliff means the ordering curriculum does not produce transferable composition — a null with a clean denominator, which is a finding, not a failure. **Undoable:** yes — seat-side, arms exist, no kernel change. **Reversed by:** a ground probe showing coherent-ordered training transfers to a held-out game and shuffled does not (the cliff); or its absence.

**To Isaiah, plain:** you were right and the fix was already yours. The chunking feeder is built — it shows the agent human frames in a controlled order, lets it predict and be wrong, and makes it mint the composition itself. The worry you had is exactly the one the design refuses: the tape carries only what the world showed (frames), never the answer's derivation; the grader scores afterwards. Nothing is handed to the agent. It is built but never settled — no rung landed, so the capability was deliberately left unclaimed. So contact is not missing in mechanism, only in measurement. The next move is to run the pre-registered spacing sweep and read the transfer cliff against the ground, not to build anything new.

FIGURE CENSUS: Fig 1 · Fig 2 · Fig 4 · Fig 6 · Fig 11 (verbatim). Strained: none.

Anchor: feeder.py:1-43,123,214,300,359,436; INDEX:36989-37004,37107-37152; git 18f83f2/3f938cb/1c341dae.
