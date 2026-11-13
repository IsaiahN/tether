# WATSON 2026-10-25 — what the limbs (the interface) should tell the agent: report like skin

Asked by Isaiah 19:39 CDT: "You guys need to figure out how to make these "limbs" provide useful info. Maybe something isn't possible they need to communicate to the agent, but just not the details on the action level, but inform just like how the skin informs the brain of temperature, texture, pressure, etc., without the brain having to know everything about how the intricacies work. This needs a WATSON skill check"

## QUESTION
The agent sends an intent down (make this object's row go down; reach that thing). The interface (the limbs) picks the press. What should come back UP to the agent, and in what form? The agent must not see actions, but it must learn whatever lets it choose better.

## EVIDENCE (measurements, r4-r9)
- Delivery of non-clock intents was 1/37, 3/49, 0/50, 5/36, 11/56 and 14/58 (deliv_resplit.py 1434249f0d5efbb5).
- Carried-kind routes (toward/graded) were 0/36, 0/29, 1/40 and 1/42 in r6-r9. By subtraction, the non-carried routes were 5/7, 10/16 and 13/16 in r7-r9. That is two scripts, so not yet one pool; a one-pass split has been ordered.
- TOUCH outcomes are never graded, and 13 of 15 right intents were never graded.
- In r9, 32 intents were both wrong and not delivered.
- What the code returns up today (30be254; read by me):
  - interface.py :839-848: when there is no route, `return None` ("the agent learns the intent was unrealisable").
  - tether.py :10743-10747: UNREALISABLE is a non-trial.
  - Otherwise the agent's grader reads the board after the press (toward / unchanged / gone; kind test borne out / not).
  - F1 credits every change to the press.

## DOMAIN CENSUS
- R:
  - arity 2: the intent sent down, and the outcome read back;
  - symmetry: one press, read twice (by the interface's own credit, F1, and by the agent's grade). That is a seam (Fig 10);
  - scale: the step (press), the cycle (intent held), the life.
- Domains:
  - The membrane between the agent and its limbs. Actors: the reasoning loop and the realiser. Currency: intents go down, reports come up. Anchor: the board's next frame on the target slot.
  - The limb's own learning (the action-effect table). Actors: the interface. Currency: press -> change by kind. Anchor: the board.
  - The agent's record (the grades). Actors: the grader. Currency: outcome words. Anchor: the board.
  - Union / seam: the same change credited by F1 below and graded above.
- Order (Fig 3): the board -> the limb's table -> the report up -> the grade -> the choice of subject.

## TETHER (primary, verbatim)
- Fig 4 :20 "Only the actors, the currency and the anchor change." The membrane rule is scale-free, so it holds between the agent and its limbs as it does between the agent and the population.
- Fig 4 :22-24 "Only methods cross up. Only head starts come down. / upward: a method that can be reapplied. Never the recording of a particular success. / downward: something that makes the next search cheaper. Never a replay of what worked once."
  -> Down goes the intent only, never a press sequence. Up goes a compressed, reusable reading, never the press log.
- Fig 4 :28 "Going up throws away detail; that is what makes the result reapplicable."
  -> This is Isaiah's skin: temperature, not receptor firing.
- Fig 4 :30-31 "So take the round trip and measure the gap. ... The gap is not an error to eliminate. It is the measurement of what the coarser description cannot hold"
  -> The report up IS the gap: intended change vs felt change, on the target.
- Fig 9 :30-31 "your words are borrowed too, so describe the effect / rather than the cause"
  -> Report effects on the object (moved / did not move / moved the other way / something else moved), never which action.
- Fig 1 :19, :22 "The residual is indexed by object slot, not aggregated." / "Aggregating across slots is how a live signal disappears into an average."
  -> Per object, the way skin reports where.
- Fig 8 :39-42 "So a search that finds nothing is never a proof of absence. ... Underivable-in-principle and unreachable-at-this-budget are different facts, and they issue different instructions."
- Fig 9 :20 "\"it is not in here\" cannot be proved from inside" / :60 "Use filters for the budget and witnesses for the verdict. Never let a filter hand you a verdict."
  -> The limb may NEVER report "impossible" as a verdict. It reports which of the different facts it holds:
    - no route known (its table is empty for this change);
    - tried N here, it never moved;
    - blocked, witnessed (the move produced an empty frame while touching: interface :1363, :1723).
  -> The agent decides what to do: search more, change subject, or test.
- Fig 11 :40 "An improvement that does not change contact changes nothing, however much it improves." / :48 "what you cannot perceive or measure yet is the residual."
  -> The limbs ARE the agent's contact. An ungraded TOUCH is a sense the agent does not have.

Triangulated: Figs 4, 9, 8, 1 and 11, with low overlap.

## WORLD (secondary; each source read)
- Human sensorimotor neuroscience: Johansson & Flanagan, Nature Reviews Neuroscience 10:345-359 (2009).
  - Action phases are "delineated by distinct mechanical contact events".
  - "Mismatches between predicted and actual sensory outcomes can be used to quickly and flexibly launch corrective actions".
  - Predicts: the report up is discrete contact events plus the mismatch with the prediction. CORROBORATES (Fig 4 :30-31; TOUCH as a graded event).
- Animal neuroscience: Poulet & Hedwig, Science 311:518-522 (2006), "The cellular basis of a corollary discharge".
  - "How do animals discriminate self-generated from external stimuli during behavior"
  - "corollary discharges or efference copies, are forwarded from motor to sensory areas"
  - Background: von Holst & Mittelstaedt 1950, reafference vs exafference (Wikipedia, read; the 1950 paper itself was not read).
  - Predicts: the sense must say whether a change was self-caused or the world moving. CORROBORATES, and names fault (C): F1 credits every change to the press.
- Robotics engineering: ROS actionlib GoalStatus.msg (read from github.com/ros/common_msgs).
  - "ABORTED ... aborted during execution by the action server due to some failure"
  - "REJECTED ... rejected by the action server without being processed, because the goal was unattainable or invalid"
  - Predicts: the lower layer returns a small, fixed set of outcome words, not its internals. CORROBORATES the form.
  - PARTIAL CONFLICT: REJECTED lets the server say "unattainable". The figures stand (Fig 8 :39, Fig 9 :60): the limb may say "no route known" (a filter) or "blocked, witnessed", never "impossible".

## VERDICT (from the figures)
The limbs report UP, per intent and per target object, in effect words, never actions. A small fixed vocabulary, like skin:
1. The gap: as wanted / partly / no change / the other way / the target is gone.
2. Self or world: was the change the limb's doing, or would it have happened without the press (reafference)? This fixes F1.
3. Contact: reached it / blocked against it (witnessed) / not reached. This grades TOUCH.
4. Reach honesty: no route known / tried N here, never moved / blocked, witnessed. Never "impossible"; the agent decides.
5. Sense quality: felt here (this life's experience) / a guess from a carried kind (a test). This is the reliability of the sense, not its mechanics.
Down goes the intent only.

Fit to the evidence: points 2 and 3 address 13 of 15 right intents never graded, and F1. Point 4 lets the agent drop a subject that nothing moves, which feeds the choice-of-subject fault (e). Point 5 already exists as mode kind_test (30be254) and must be reported, not hidden.

- Cost if wrong: a derivation page and a ledger census, no code.
- Undoable: yes.
- Reversed by: the census showing that the agent already receives these distinctions and ignores them (then the fault is the agent's reading, not the report), or a figure line that puts any of these below the seam.

Sources:
- [Johansson & Flanagan 2009, Nat Rev Neurosci](https://link.springer.com/article/10.1038/nrn2621)
- [Poulet & Hedwig 2006, Science](https://edoc.mdc-berlin.de/id/eprint/11036/)
- [Efference copy (Wikipedia)](https://en.wikipedia.org/wiki/Efference_copy)
- [ROS actionlib GoalStatus.msg](https://raw.githubusercontent.com/ros/common_msgs/noetic-devel/actionlib_msgs/msg/GoalStatus.msg)
