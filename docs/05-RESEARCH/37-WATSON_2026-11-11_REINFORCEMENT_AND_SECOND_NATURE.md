# WATSON — reinforcement of mundane things, and second nature (2026-11-11 03:00 CST)

Isaiah, 02:55, verbatim: "No, safe as built, but also check: should strength be slightly bumped, and also by, like, occurrence, like strong, then weaker, weaker bump over time? WATSON check how reinforcement of mundane things that become second nature works"

QUESTION: Should a term's strength rise a little with each repetition, by less each time (strong, then weaker, then weaker)? And how do routine things become second nature?

DOMAIN CENSUS:
- R: arity 2 (a term; its occurrences) · symmetry: repeated confirmations are interchangeable reports of one regularity · scale: step -> game -> lifetime.
- Domains (actors / currency / anchor):
  - The record: confirmations and refusals / counts / the ground paying.
  - The reading: confidence and youth / a number in (0, 1) / derived from the counts.
  - Cost: search / heads / what the next search no longer has to do.
- Order: the record, then the reading, then cost.

TETHER (primary, verbatim):
- Fig 5 :11 "held: the model was right, nothing owed". A repetition that holds owes no new term. It adds evidence, not a new idea.
- Fig 4 :24 "downward: something that makes the next search cheaper." Second nature is this: a settled thing becomes cheap to reach, so the next search starts further on.
- Fig 6 :42 "What is recorded only grows. What is reachable is derived, and it can fall." Each repetition is recorded. The strength is the derived reading.
- Single-pool caution, Fig 2 :31: repeated confirmations of one regularity draw on one evidence pool. That is a reason for each extra one to count for less.
- Triangulated: Fig 5, Fig 4, Fig 6, Fig 2.

WHAT THE AGENT ALREADY DOES (gamma.py, read now):
- Each settle adds +1 confirmation (gamma.py:1543).
- confidence = (confirmations + 1) / (confirmations + failures + 2), the Laplace posterior mean (gamma.py:1696).
- So the bump per occurrence already shrinks: 0.50 -> 0.667 (+0.167), -> 0.75 (+0.083), -> 0.80 (+0.05), ... the 10th adds under +0.01. Strong, then weaker, then weaker, to a plateau.
- youth = 1 / (1 + trials) shrinks the same way.
- Second nature in the build: a settled term becomes a part the next search builds on, and tonight's walk memo by pattern and compile memo make a repeated walk cost almost nothing.

WORLD (secondary, each read):
- Animal learning, Rescorla-Wagner (1972; worked example, Navarro, "The Rescorla-Wagner Model"): v <- v + alpha·beta·(lambda - v). The step is proportional to the distance left, so the increments shrink with each trial (in the worked output, 0.090, 0.082, 0.075, 0.068). Corroborates.
- Human habits, Keller, Kwasnicka, Klaiber, Sichert, Lally & Fleig, Br. J. Health Psychol. 2021: automaticity follows a curve "in which the increase with each day reduces over time until a plateau is reached"; "a median of 59 days was needed to reach 95% of the asymptote"; and "multiple omissions are impeding the habit formation process." Corroborates the curve, and adds that missed repetitions slow it.

VERDICT (from the figures):
- Yes: strength should rise with each occurrence by a shrinking amount. The agent's confidence already has exactly that shape (Laplace), and so does youth. No new constant is needed.
- What is open is WHAT COUNTS AS AN OCCURRENCE. Today a confirmation comes from a settle (the ground paying for a term), not from every routine step where a prediction held. Counting every held step as a small confirmation, on the same shrinking curve, would let mundane repetition build strength the way habits do.
  - Caution, Fig 5 :11: a held step owes nothing new.
  - Caution, Fig 2 :31: many held steps of one regularity are one pool. If held steps count, they should count on the shrinking curve, and only once per regularity per step.
  - It would not have rescued the newborn's term (that was a refusal not fading, which Isaiah ruled stays as built). It strengthens what already works; it does not forgive what failed.
- Recommendation: no code change tonight. On the e2e, measure how many held steps each settled term saw per game. If routine terms reach the plateau only through settles while holding hundreds of times, propose counting held steps (once per regularity per step, on the same curve), behind its own switch, for Isaiah's word.
- Cost if wrong: small (a switch). Reversed by: the e2e count showing routine terms already plateau through settles alone.

Sources:
- [Rescorla-Wagner model, worked example (Navarro)](https://minds-machines-4103.djnavarro.net/rescorla_wagner.html)
- [Keller et al. 2021, habit formation (Br. J. Health Psychol.)](https://discovery-pp.ucl.ac.uk/10118622/1/Jan%20paper.pdf)
