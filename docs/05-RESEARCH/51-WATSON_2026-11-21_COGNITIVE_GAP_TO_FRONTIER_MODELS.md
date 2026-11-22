WATSON — the cognitive gap between this agent and frontier models, derived from the figures (2026-11-21)

PROMPT: Isaiah — "all the ingredients here already exist to make an excellent general agent, but
we need to see the cognitive gap between this and topline models like claude opus, or openai sol
or your model. Intelligence is an arrangement and llms show us that, i need to create an
arrangement or rather leverage the agents current umwelt to maximize its capabilities to reason
and speak and interact." Plus: "keep our agent mostly preserved ... leveraging its composition
abilities and its abilities to make programs. whatever we need to put in place needs to be
accessible by the agent via the library as one of those composition metaprograms."
Plus: "retain the architecture, keep it transparent, whitebox, 100% interpretable."

METHOD: unbundle (Fig 9 :5 split), describe effects before looking (Fig 9 :27-31), figures decide
and the world only corroborates, both currencies (Fig 12 :125-130), judge by contact (Fig 11
:39-40). Two read-only code audits and web research on frontier reasoning were done BEFORE this
synthesis; every code claim below was re-verified at the write site.

===============================================================================
0. THE GOVERNING FIGURES — they decide what the gap even is
===============================================================================
- Fig 11 :39 "capability is a property of agent-and-habitat, never of the agent alone"; :40 "an
  improvement that does not change contact changes nothing, however much it improves"; :43 "The
  habitat is enumerated, never composed."
- Fig 12 :5 "A set of ingredients is not one. The bond is the rest of the information"; :14 "the
  ingredients are recorded and the arrangement is not"; :94 "The arrangement is the substance";
  :103-105 "a settled molecule becomes an atom for whatever composes over it ... a system that
  cannot settle has one level however large its library" (verbatim :106).
- Fig 13 :114 "The set is closed. The arrangements are not. That gap is why import exists."
- Fig 9 :60 "filters for the budget and witnesses for the verdict. Never let a filter hand you a
  verdict."
- Fig 6 :26 "The world does not gain primitives; a frame gains access. Composition explores what
  the operators reach; instruments extend what can be represented at all."

SO: the gap is NOT a missing dictionary and NOT a missing prior. The ingredients are present.
The gap is in the ARRANGEMENT — what can be bonded, what can compose over what, and what the
ground is allowed to settle. That is the same thing the LLM literature calls reasoning.

===============================================================================
1. WHAT FRONTIER MODELS ACTUALLY HAVE (world witness, corroboration only)
===============================================================================
Survey evidence (test-time compute surveys 2025-26; long-CoT survey, Sci China Inf Sci 2026;
Patterns 2025 LRM survey; SKiC EMNLP 2024; Structured Task Hypothesis ACL 2024; ICLR 2025 FTCT):
- **Deliberation = scaling reasoning STEPS at test time**: search, self-correction, tree search,
  verification. Long CoT is the defining feature of o1/R1-class models. A 1B model can beat a
  405B on reasoning with compute-optimal test-time scaling (Liu 2025). CAPABILITY IS AN
  ARRANGEMENT OF STEPS, NOT PARAMETER COUNT — this is Isaiah's claim, independently corroborated.
- **In-context learning is composition of pre-existing skills**, not task-selection or
  meta-learning (Structured Task Hypothesis, Li et al. ACL 2024). SKiC: showing foundational
  skills AND compositional examples grounded in them unlocks near-perfect systematic
  generalization, activating latent pretrained skills (Chen et al. EMNLP 2024).
- **Fragmented-knowledge chaining** (ICLR 2025 FTCT): if B=f(A) and C=g(B) are learned
  separately, a transformer can deduce C=g(f(A)) at test time. The fragments need not be
  co-present in training — the arrangement supplies the bridge.
- **Knowledge graphs help only when used as a SEARCH PRIORITY / validator, not as a verdict**
  (KG+LLM surveys 2024-25; ConceptNet commonsense eval 2025 shows leading models still fail
  abstract single-relation selection). This MATCHES the figures' priority-only rule exactly.

So the LLM "umwelt" that matters is not more facts — it is (a) a workspace where a chain of
intermediate results can be held and verified, and (b) skills available as composable pieces.
Both have direct counterparts in this agent. That is the whole point.

===============================================================================
2. WHAT THE AGENT ALREADY HAS — the ingredient census (audit, re-verified)
===============================================================================
ALL PRESENT, default-ON, reached:
- **A typed composition grammar** (grammar.py): 7 types, 13 NSM primes, 9 heads, 3 terminals;
  the loop's dependency chain is ENFORCED BY TYPE (PERCEIVE→BET→ACT). A composer
  (composer.py) with 7 bonds and priced arrangements (Fig 12's bond cost).
- **A metaprogram algebra** (routine.py): Act, Seq, When, Choose, Try, Until, Call, Let, Expect;
  `advance` carries multi-cycle behaviour in one field; `Call` reaches a NAMED shelf so programs
  are reusable by name (`tether.py:24859, 25881`). This is the "make programs" capability Isaiah
  names — it is built.
- **RDL + three lexicons** (rdl_parse/store/release, word_map, relations): 1,494 preloads,
  3,577 WordNet priors, ConceptNet relations, VerbNet widening; AKAZE picture recognition.
- **Per-slot residual, bargain, minting, promotion, self-steer, correction-as-subtext** — the loop.

So the ingredient census agrees with Isaiah: the parts are all here.

===============================================================================
3. THE ACTUAL GAP — three structural facts, each with its write site
===============================================================================
Not one is a missing dictionary. All three are about the ARRANGEMENT.

GAP 1 — COMPOSITION CANNOT STACK (Fig 12 :105 "a system that cannot settle has one level").
  `Config.max_depth = 3` (tether.py:4979); library chains longer are cut (:10694-10696).
  `_ops` (tether.py:14306-14308): "Binary tree, depth one, by construction" — the operand is a
  VALUE, never a term, so there is no second branch to descend into. MEASURED across all six
  1800-cycle proving ledgers: distinct terms 13-187, max chain atoms 2-7, but **nested
  operand_term = 0 on every board**. The longest real term is `subtract . recolour . subtract .
  translate<o0.dist_o1>` — a flat chain whose `⟨...⟩` holds ONE slot. There is no mechanism that
  feeds a term's output into another term's operand tree. This is the exact counterpart of the
  LLM's inability-to-chain that long CoT fixes — except here it is structural, not statistical.

GAP 2 — THE METAPROGRAMS ARE BUILT BUT STARVED AT THE BARGAIN (Fig 5 :16 "mint if it pays").
  The routine algebra is complete, `htn_tier1` decomposition fires (21/21/103 across three
  boards), but a COMPOSED multi-step plan is refused every time: `routine_cut reason="does-not-
  pay"` (tether.py:26032-26044). Record: "routines adopted 0 and chunk_reuse 0 in ALL FOURTEEN
  board-depth readings" (INDEX:27007); "routine_cut 0·0·0·0 — procedure-level reuse has never
  once fired" (07-LEDGER:844). The only surviving routine is `verdict=actuator`: a single TOUCH
  wrapped in Until — not a composed plan. `_goal_choice` returns ONE slot (tether.py:23664), so
  no parallel multi-goal pursuit. So the agent can write a program but has never bought one.

GAP 3 — EVERY PRIOR IS PRIORITY-ONLY BY DOCTRINE (Fig 9 :60 filters≠verdicts).
  RDL/WordNet/ConceptNet/VerbNet/affordance are explicitly "SEARCH PRIORITY ONLY — never makes
  anything reachable, never adds to the library, never writes standing" (tether.py:2007-2013);
  affordance "never moves an action choice" (affordance.py:22-23). Of 1,494 preloads, **0 become
  a term Γ composes over**; 191 usable ones only reorder a lookup; 1,303 are not even offered
  (tier1 gloss text is raw WordNet text, `wn:` id chains for tiers 2-3). The one genuine
  transformation is AKAZE pixels→class→concept→verb→predicted reading, and even it writes a
  stamped ROW, not a composed atom. Isaiah's "for the most part untransformed" is correct.

===============================================================================
4. WHY THE LLM GAP IS REALLY THESE THREE (the triangulation)
===============================================================================
Long CoT / test-time search = GAP 2 (a chain of steps the ground verifies) + GAP 1 (steps that
can be chained at all). SKiC / skill composition = GAP 3 (skills present but only as priority,
never as composable, settled pieces). There is no fourth gap: the umwelt (integer slots + derived
relations + optional pictures) is enough to *exhibit* the three — Fig 11 :40 says adding facts
or senses that don't change contact changes nothing, and there is no text channel precisely
because the project refused to make language a shortcut (speak.py:3-8).

The gap is therefore NOT "become an LLM." It is: make a SECOND composition step representable
and payable, and let a multi-step metaprogram be BOUGHT when the ground pays for it. That is a
Fig 12 arrangement change, not a Fig 6 primitive change — so it keeps the architecture and the
closed atom set intact. Every addition stays a library object (a recipe on the routine shelf /
a molecule), rendered in the ledger, so it remains whitebox and human-readable.

===============================================================================
5. WHAT TO BUILD — habitat first (Fig 11), not kernel, not priors
===============================================================================
The figures forbid the two tempting shortcuts: do not raise max_depth by decree (Fig 9 :60 a
filter is not a verdict — a chain that is *allowed* is not a chain that is *paid*), and do not
hand the lexicon as answers (Fig 4 methods-only membrane). The only Fig 11-legitimate move is to
CHANGE CONTACT: give the agent habitats where a multi-step composition and a bought metaprogram
PAY. That is what "more gridworlds" is for.

Concrete plan, each a means with a must-fail test, no game identity, no encoded answer:
  A. A new gridworld family that presents a TWO-STEP causal consequence (press A changes B;
     B's change is the only thing that moves the goal) — so a single-action policy cannot clear
     and a composed two-step routine, if paid, can. Reachable by construction; the world never
     reads the agent. This is the habitat that can make GAP 2 fire.
  B. A world variant where the same press has DIFFERENT effects under a derived RELATION
     (above/below/contact) — requiring the operand to be a relation, not a value — to give GAP 1
     a contact surface where depth-2 pays.
  C. Tests that assert the PRECONDITION (the world can show the capability at all) and the
     REFUTER (a depth-1 / single-action policy fails), per the panel-precondition and
     treatment-executed disciplines — so a null is a statement about the run, not the library.

FIG 11 :40 is the test: these worlds change what the agent can REACH, not a number. If a
composed routine is bought on world A and no single-action policy clears A, contact changed.

WHAT I WILL NOT DO: change tether.py's kernel rules, raise max_depth, hand priorities standing,
add a text input channel, or tune to any ARC game. Architecture preserved; every addition a
library/habitat object the agent can reach; every decision legible in the ledger.

FIGURE CENSUS: Fig 1 claim/mode · Fig 3 dependency order · Fig 4 methods-only membrane · Fig 5
when a composition pays · Fig 6 primitives vs arrangements · Fig 8 closure/surplus · Fig 9 split /
describe-effect / filters-not-verdicts · Fig 11 capability=agent-and-habitat / enumerate /
contact / introduce-never-subtract · Fig 12 bond-is-the-rest / arrangement-is-the-substance /
one-level-without-settling / two currencies · Fig 13 closed set open arrangements. Strained: none.

Sources (world — witnesses only): survey of test-time compute (arXiv 2501.02497), long-CoT
survey (Sci China Inf Sci 2026), LRM survey (Patterns 2025), SKiC (EMNLP 2024), Structured Task
Hypothesis (ACL 2024), FTCT (ICLR 2025), KG+LLM survey (2024-25), ConceptNet commonsense eval
(2025). Code claims: two read-only audits re-verified at write sites 2026-11-21.
