# Derivation log

Derive-first step 7 (Fig 4: *"carry up a method that can be reapplied, never the recording of a
particular success"*). Each entry is a **method**, indexed by the shape of the residual it
settles, so the next case is a lookup by shape rather than a re-derivation. The full reasoning
for each lives in the WATSON it names; this log is the index of *how*, not the record of *what*.

Figures are primary; world research corroborates. Every entry below was used on a real case in
2026-11-21/22 and re-verified at the write site before being carried.

---

## M1 — "A mechanism that does not exist" claim: check the repair, then the write site
**Residual shape:** a doc/record says a mechanism is "never reached / zero producers / not built."
**Method:** (1) find the named repair commit in git history, not just the current tree; (2) open the
write site and count calls, not existence; (3) take the denominator from the SAME site as the
numerator (a gate after `pays()` has a different population than one before it). A stale row of
this class closes a question falsely. Quoted: CLAUDE.md *"a map entry saying a thing does not
exist is worse than one saying it is unfinished — the first closes the question."*
**Cases:** WATSON 54 (`_trees` "never reached" was F348's stale measurement; `cf27e315` fixed it),
WATSON 56 ("routines adopted 0" was short-run-only; cd82 buys 6), the `tether.py:5289` stale seam
comment.
**Falsifier:** a call count of zero at the write site with the arm on, after the repair commit.

## M2 — "Repair the code" vs "amend the kernel": the species test
**Residual shape:** numbers are bad and a threshold change would make them green.
**Method:** ask whether the code CONTRADICTS a figure (conformance) or whether the figure's rule
itself is being amended. Fig 4 :19-20 *"the kernel is the part that does not change with size …
the same rule for naming what worked … Only the actors, the currency and the anchor change."*
The bargain `pays` is that rule. Editing it to accept what it refused = a new species. Repairing
a place where the code fails to obey the rule = conformance, allowed.
**Cases:** gamma.py:2478 promotion dropped the settled method, contradicting Fig 12 :103 →
conformance fix (built, WATSON 54). The routine price edit → retracted (WATSON 53 correction).
**Falsifier:** any fix that changes a decision with the arm OFF, or moves a threshold.

## M3 — Build nothing that has no occasion
**Residual shape:** an intent/atom/sensor is declared but never produced or consumed.
**Method:** before adding the consumer/realisation, grep the ledgers for the producer. Zero
formation sites and zero ledger mentions = a solution looking for a problem; record it as a
finding, do not build it.
**Cases:** `BE_AT` has a declaration and no realisation branch, but 0 formation sites and 0 ledger
mentions → not built (this session). Contrast: method-bearing trees settle on 4 of 6 boards →
Fix 1 has occasions (WATSON 55).
**Falsifier:** a ledger mention appearing after you claimed none.

## M4 — Instrument before conclusion: validate the detector
**Residual shape:** a census/count comes back zero or uniform and looks like a finding.
**Method:** prove the detector CAN see the alternative before trusting the null. Check the shape
it counts against a known positive. A bound operand `<o0.col>` is not a method `<translate(o5.add_n)>`
— the first detector conflated them and nearly reported a schema where there was a binding.
**Cases:** nested-method census (WATSON 57): validated by confirming double-`<` is near-absent and
the one hit is a provenance stamp, not a method. Perf A/B (WATSON 55) was discarded as invalid for
the same reason (cost + detector bug), not read as evidence.
**Falsifier:** a known positive the detector cannot see.

## M5 — Capability claim needs contact, not representation alone
**Residual shape:** "we made X representable" is about to be read as "the agent can now do X."
**Method:** separate three levels — representable (in the library/closure), reachable (a candidate
the search offers), paid (the ground settles it). Fig 5 :69 *"settling is necessary for a term to
be composed over, and it is not sufficient."* Show a per-game run where the new form becomes an
operand of a later PAYING term; a structural test that only proves the unit exists is not a
capability result.
**Cases:** Fix 1 — representation confirmed (distinct schema unit keeps `operand_term`), but
`enumerate_closure` walks `unit.atoms` (gamma.py:2545) so no composed term uses the method;
payoff NOT claimed (WATSONs 55/57).
**Falsifier:** a schema-named unit becoming an operand of a paid term on a per-seed run.

## M6 — Correct abstention is a result, not a gap
**Residual shape:** a gate refuses candidates and the count is nonzero.
**Method:** read the refused population and ask whether refusal is what the figure requires. If
every refused plan has reach 1, the bargain is right (a plan saving one action cannot pay
`term_bits > log2(n)`), and the fix is to change the habitat, not the threshold. Fig 9 :60 filters
are not verdicts; Fig 11 :39-40 capability is agent-and-habitat.
**Cases:** routine `does-not-pay` — reach 1 on all boards, cd82 (large gap) buys 6 → correct
abstention, no kernel change (WATSON 56).
**Falsifier:** a refused plan whose reach exceeds the number of actions it would save.

## M7 — Stale record classes to check first (cheap, before any build)
**Residual shape:** "X was never done / still off / zero" in CLAUDE.md, INDEX, a card JSON, or a
code comment.
**Method:** these sources go stale independently; check in this order — the repair commit in git,
the live module values (not `os.environ`), the reader at the write site, then the ledger. Known
stale instances this session: `_trees` "never reached" (CLAUDE.md:774), "routines adopted 0"
(CLAUDE.md:1154), the `tether.py:5289` seam comment, the `tether_rules.json` symbol census
(13 bound vs 18), `word_map.json`/`relations.json` `"readers": []`.
**Falsifier:** the live value differs from what the record asserts.

---

Entries are numbered for reference; add a method only when it survives use on a real case. A
one-off finding with no reusable shape belongs in its WATSON, not here.

## M8 -- Never ask the anchor for a ruling the figures decide

**Residual shape:** I am about to ask Isaiah to choose A vs B on a design question.
**Method (Fig 10: the seat reads the ground; it does not ask the maintainer to decide design):**
(1) Check the record first -- code and docs -- because he has likely already thought of it (the
real-world-habitat idea was Phase 2; nested methods were in 08-METAPROGRAMMING_DESIGN). (2) If not
in the record, derive it with WATSON from the figures as metalaws (they govern every level). Only
if both fail is it a genuine gap for the anchor. "Needing a human RLHF ruling" is the signal I
stopped deriving too early -- the seat's own failure mode.
**Cases:** WATSON 60 retracted three rulings I had deferred (nested methods, habitat, composer
change); all were decidable from Fig 12 / Fig 11 / the record.
**Falsifier:** a question that survives the record check AND the figure derivation with no verdict.
