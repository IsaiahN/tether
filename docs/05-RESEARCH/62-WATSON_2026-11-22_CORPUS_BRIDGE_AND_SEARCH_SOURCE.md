WATSON 62 — one import gate, two sources: the corpus bridge and a WATSON search source (2026-11-22)

THE TWO PROPOSALS (Isaiah): (1) the corpus→candidate bridge — compile RDL preload bonds into
Terms via `composer.bind`, offer as unstanding candidates, let the ground pay; (2) use WATSON
(LLM-synthesized web search) to "fake the downloaded knowledge", cache the results temporarily,
and if they pay, stamp provenance and save to the library as composition.

QUESTION (effect terms): what is the figure-faithful shape of bringing outside knowledge into the
agent so it can REASON with it, and where does the LLM-search version cross a line?

DOMAIN CENSUS:
- R: arity = (outside frame, internal closure, ground); symmetry = a recording and a method both
  arrive as text but differ in what they let the agent do; scale = one import event.
- domains: corpus (actors: preloads/bonds / currency: attachments / anchor: source sha); WATSON
  search (actors: LLM+web / currency: synthesized claims / anchor: cited source); agent (actors:
  terms/bargain / currency: bits+actions / anchor: board). Order: source -> gate -> closure -> ground.

TETHER (primary, verbatim from source SVGs):
- Fig 6 : "Import from a live peer is debited against that frame's independence. A wrong atom
  costs more than starting from primitives." "the only operator that moves the wall." Import is
  gated: provenance (source gate) + shadow test (explains a gap) + debited against independence.
- Fig 8 : "two frames together reach what neither reaches alone ... that surplus is where imports
  live" and "Convergent derivation and adopted import look identical in the contents. Only the
  record of where each came from separates them." -> provenance is the ONLY thing separating an
  import from an in-closure derivation; without the stamp they are indistinguishable.
- Fig 4 : "Only methods cross up. Only head starts come down." "upward: a method that can be
  reapplied. Never the recording of a particular success." -> a web-search result is a RECORDING
  (what someone concluded); it may cross only as a METHOD/candidate the agent can re-derive and
  the ground can test, never as a settled answer.
- Fig 1 : "mint φ if the description length pays." Fig 5 : "standing: only a term's own record
  with the board." -> no candidate gets standing at entry; the ground pays.
- Fig 10 : "A verifier that can reconstruct the claim cannot verify it." -> the LLM that proposes
  a claim cannot be the thing that settles it. This is the line the WATSON version must not cross.

THE DANGER (named): in proposal 2, the LLM both synthesizes the search AND ties it to figures.
That is a frame that can reconstruct its own claim. If its output enters Γ with standing, we have
encoded an answer and broken the ablation (Fig 2: a frame cannot score itself). The fix is
structural, already in the architecture's rule: the LLM is a PROPOSER only. It emits candidates
with provenance and NO standing; the agent's own bargain and the board decide. "The agent acts as
a logic verifier" (Isaiah) is exactly this — but the verifier must be the agent's ground loop, not
the same LLM.

THE REFINEMENT (what to actually compile): a real usable preload has bonds like
`('≡','Tinca_tinca','tench')` — name identity chains, NOT atom-level compositions. Tier 1-3
bonds are gloss/lemma/hypernym packaging; they carry no reasoning the agent can compose. The
composable bonds are TIER 4 (the 13 rule cards): `do_sym` in NSM operators, e.g.
`state(Q) ⇒ ask spectrum(Q) + ask gradient(Q) + ask network(Q)`. The bridge should compile
TIER-4 operator bonds into Terms (all symbols already in the grammar), stamped `origin=pid`.
Compiling tier-1 lemma identity into a term would produce a name-equality claim, not a method —
that is why 0/1494 became terms and why doing it naively would be a gum fix.

VERDICT (figures decide): do BOTH through ONE gate. Source A = corpus tier-4 bonds; source B =
WATSON-synthesized search results. Both become provenance-stamped candidates with NO standing;
both must pass the source gate (provenance), the shadow test (explain a residual), and the bargain
(ground pays) before entering the library as a named composition. The web source is a FRONTLOAD
done offline (like the ImageNet parquet), never a live call in the decision path (hard rule: no
foundation model in the decision path). The cache is a pending store, and "if they paid" means a
settle row from the board — not the LLM's confidence.

COST IF WRONG: a wrong imported atom costs more than starting from primitives (Fig 6) — debited
against independence. UNDOABLE: yes, behind an arm, OFF byte-identical, lineage stamped.
REVERSED BY: a panel where every imported candidate fails `pays` and none explains a residual —
then the wall is price, not representation.

BUILD ORDER (two bounded steps, each with must-fail tests):
1. `corpus_bridge.py`: `candidate_term(preload)` compiles tier-4 `do_sym`/bonds into a Term over
   existing atoms, `origin=pid`, no standing. Tests: composition well-formed, provenance carried,
   tier-1 bonds refused (not composable), OFF identity. Representation only, no capability claim.
2. Wire the bridge + a WATSON-source cache into the mint as candidates behind an arm; A/B per game;
   a candidate enters the library ONLY with a settle row. This is the test of "does it pay."

FIGURE CENSUS: Fig 1 · Fig 2 · Fig 4 · Fig 5 · Fig 6 · Fig 8 · Fig 10 (verbatim from SVGs). Strained: none.

Sources: WATSON Custom GPT spec (github.com/IsaiahN/watson-gpt); repo RDL_BUILD_SPEC; figures SVGs.



## CORRECTION, 2026-11-22 — the corpus→Term bridge as first conceived is wrong; do not build it

Before building step 1 of WATSON 62 I checked the actual structures, and the premise fails:
- A tier-4 card's `do_sym` operands are FORMULA SYMBOLS (`R⁺_s`, `¬shrinking(R_s)`, `state(Q)`,
  `ask spectrum(Q)`), not agent atoms. `composer.bind(bond, left, right)` expects agent-level
  operands; feeding it these strings would manufacture Terms whose operands mean nothing to the
  agent — the exact gum fix this project refuses.
- Those formula symbols are already bound to agent READINGS in `symbols.BOUND` (Γ, R, R⁺_s,
  bond, molecule, R_T, T_A, ...; `symbols.evaluate` returns a reading or UNBOUND), and the agenda
  reader (`agenda.py`) already selects cards by residual shape and writes their questions into the
  ledger. So tier-4 corpus content is already READ and LEGIBLE — just not a mintable Term.
- Tier 1-3 bonds are name chains (`≡`/`∥` over lemmas/wn-ids) — packaging, not reasoning.

So "compile preload bonds into Terms" (WATSON 62 step 1) is REFUTED by the write sites. The
corpus is untransformed in the sense Isaiah said, but the missing thing is NOT a composer call —
it is that priors are held as priority-only with no standing, by design (RDL spec's three
quantities). To make them composable would require mapping abstract symbols to atoms, which no
figure licenses and which would encode meaning rather than let the ground settle it.

WHAT SURVIVES from WATSON 62: the DANGER and the UNIFIED GATE. Both sources (corpus, web search)
must enter as provenance-stamped candidates with NO standing, gated by source/shadow/bargain —
that part is Fig 6/8/4/10 and stands. The LLM-search version must be proposer-only (Fig 10: a
verifier that can reconstruct the claim cannot verify it). This is the design约束 for any
future import work; it is not a buildable bridge today.

DECISION: do NOT build corpus_bridge.py. Record the refutation. The highest-leverage real work
remains Fig 12 conformance (operand-arm branches accept settled units) — already in the plan,
representation built by Fix 1, composition the live gap. Web-search frontload is a legitimate
offline source (like the ImageNet parquet) but needs its own source-gate design; not built here.

Anchor: rdl_store.load bonds; grammar.compose signature; symbols.BOUND keys; agenda.py card reader.
