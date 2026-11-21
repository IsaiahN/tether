WATSON — are the Tether cards reasoned with, and can the agent speak? (2026-11-21)

PROMPT: Isaiah — "what's the status of the agent being able to think and reason via the tether
in its library?" and "what about the agent's ability to fluently speak?"

Read-only audit at the write sites; every claim quoted and re-verified here. The figures decide;
this is a finding, not a build. No code changed.

===============================================================================
1. THE CARDS: 13 cards, recorded but NOT causally read
===============================================================================
Corrections to my own prior framing: the JSON holds **13** cards (not 12); the symbol census in
the card metadata is stale (says "13 of 22 bound, 9 UNBOUND"; actual `symbols.BOUND` = **18**,
4 UNBOUND with reasons). Verified at `symbols.py:230-241` and `library/tether_rules.json:L18`.

What the cards hold: 13 named shapes of residual, each with `when`/`asks`/`do`/`do_sym` — full
figure rules (Which link first, Read the predecessor, Instrument the middle, Describe before you
look, Filters-not-verdicts, Three texts before acting, Could it have come out the other way…).
The content is genuinely faithful to Figs 3/9/13.

Selection and read sites (`agenda.py`):
- load `:45-47`; loop `:118-120` by `order` + two predicates; question read `:129,133`;
  `do_sym` evaluated `:169-174`; row written `:178-180` (`event=agenda, slot=@agenda, step=PLAN`).
- **Only TWO shape predicates exist** (`:92-95`): `Which link first` and `Instrument the middle`.
  A third path writes `Describe before you look` unconditionally (`:110-114`); a fourth writes
  `Three texts before acting` on goal refusal (`:144-154`). So **4 of 13 cards ever fire**;
  the other 9 have no predicate and no write site.

DOES CARD CONTENT ENTER A DECISION? **NO.** Verified at the write sites:
- `tether.py:11089` — `self._agenda.step(self)` — **the return value is discarded**;
  `_hyp_check()` follows unconditionally at `:11091`.
- `agenda.py:45-47` — `_ANSWER` is a hand-written pointer table
  (`'SEE': 'read the board again'`, `'GOAL': 'the goal path proposes one'`, …), not derived from
  card text. The card's `do` rule is never executed; only its `asks` string is copied into a row.
- The subgoal push at `:11566` happens BEFORE `self._agenda.refused(...)` at `:11578-11579` —
  the card records the push; it cannot cause it.
- Only other consumer: `rdl_parse.py:29-31` makes 13 tier-4 preloads that "set search priority
  only … never makes anything reachable, never adds to the library, never writes standing"
  (`tether.py:2008-2010`).
- The actual card rules are implemented as SEPARATE arms citing cards in comments
  (`TETHER_REPAIR_AT_REFUSAL`, `TETHER_GOAL_VARIES` at `tether.py:4033-4049`) — the card text
  is not the source of the behaviour.

Built-and-reached measurement (real ledgers, cards event, per game never pooled):
ar25 60 rows (51 Describe / 5 Which-link / 4 Instrument; all 5 carry `R⁺_s: unbound`);
cd82 40; t0_ka59 20; t0_lp85 19. Only the 4 cards with write paths appear. `tests/test_symbols.py`
enforces "only the agenda reader imports symbols" (S5) — so the isolation is deliberate.

VERDICT (Fig 9 :60 "filters for the budget, witnesses for the verdict" / Fig 11 "an improvement
that does not change contact changes nothing"): the cards are a **legible record of the agent's
own procedure**, running as a `PLAN`-step narration, but they do not steer. The behaviour they
describe is implemented elsewhere, behind arms. This is honest instrument work, not a failure of
correctness — but it is NOT "the agent thinks using the Tether in its library" in the causal
sense. That claim would be false if I made it. Two options exist and I have not chosen between
them: (a) accept the cards as an audit instrument (what they are), or (b) make card selection
causally read by the decision path — which risks handing the agent a hand-written `_ANSWER` and
is closer to encoding a procedure than to reasoning. This is Isaiah's call; no code changed.

===============================================================================
2. SPEECH: a bounded typed term grammar; template narration, not generative speech
===============================================================================
No `translate.py` — translation lives in `nsm.py:102-111,149-167,186-234` and `arc_predict.py:88`.
- `nsm.py` — trace narrator, 16 `say_row` templates over ~15 event kinds; reads rows, writes
  nothing back (`:1-5`).
- `speak.py` — account narrator, 36 event branches / 40 sentence forms; `:3-8` says
  "Compositional fluency in the library is the target here; sounding human is not."
- The compositional part is REAL: term encoding/decoding `DO a1 AFTER a2 [OTHER x] [IF guard]
  [WHERE ref]`, recursive on `operand_term`; inverse `read_term` with regex + typed refusal
  (`gamma.accepts_type`), `read_node` refuses non-`→` bonds with listed reasons. "Every sentence
  compiles back to the same Term, or is refused with a listed typing reason" (`nsm.py:13-16`).
- Self-narration is fixed if/elif template filling with hardcoded English and backticked names
  (`nsm.py:249-311`, `speak.py:29-355`). Motion words are two template branches in
  `affordance.py:138-144` ("rolls" if a roll verb else "glides") + direction `:123-135`, rendered
  `nsm.py:331-335`; arm `TETHER_MOTION_WORDS` ON, but record-only. Searched every `*.jsonl` and
  `*.log` under `C:\TETHER_RUNS`: **zero** real-run hits for `manner`/`rolls`/`glides` — only the
  fixture `tests/test_affordance.py:151-158`. Built-and-test-fired, never fired in a real run.

Real `nsm.log` from the proving run (verbatim):
  `c0 #24 WANT @goal.completed: I WANT ALL(BECOME(level, completed))`
  `c0 #30 BET o0.age: I THINK: IF I DO THIS NOW, AFTER THIS I SEE 1 (BECOME OTHER)`
  `c11 #5964 MINT o12.drow: SOMETHING HAPPENED HERE; I THINK translate . recolour<o10.col> CAN SAY THIS`
First 5,000 lines: BET 3841, WEIGHT 848, LOOKUP 82, SETTLE 24. No COMPOSE/GENERALISED.

VERDICT: legible whitebox report, not fluent generative speech — by design (`speak.py:3-8`).
The grammar composes TERMS and round-trips them typed; it does not generate free narrative.
Nothing in either narrator reaches the decision path (`nsm.py:4-5`, `speak.py:3-4`). "Fluent
speech" as an LLM has it is not a present capability and is not a declared target.

===============================================================================
STALE RECORDS FOUND (question 0-3)
===============================================================================
- `word_map.json:468238` `"readers": [] ... "NOTHING in the agent reads this file"` — FALSE:
  `tether.py:33` imports affordance and calls load_sources/resolve at `:27072,:27092`.
- `relations.json` header `"readers": []` — FALSE for the same path.
- `tether_rules.json:L18` symbol census 13/9 — FALSE: 18 bound / 4 unbound.
All three are pre-fix snapshots that a reader would treat as current. Recorded, not edited
(corpus boundary); the code is the record.

FIGURE CENSUS: Fig 1 claim/instrument/mode · Fig 4 methods-only membrane · Fig 9 describe-effect /
one-pass / filters-not-verdicts · Fig 11 contact, improvement-not-changing-contact · Fig 13 closed
set/open arrangements (the term grammar). Strained: none; the cards-as-decision question is a
design fork, not a figure contradiction.

Sources: read-only audits of agenda.py, symbols.py, nsm.py, speak.py, affordance.py,
arc_predict.py, tether.py, library/tether_rules.json, library/word_map.json, library/relations.json,
conform/arms.py; real ledgers under C:\TETHER_RUNS. All key claims re-verified at the write sites
on 2026-11-21.
