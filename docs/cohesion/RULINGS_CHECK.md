# Item 9 — ISAIAH_RULINGS.md checked against the figures and today's plan

> **RESOLVED 2026-10-08 ~12:10 CDT.** Isaiah: *"all the rulings are stale - lets use your suggestions"*. Every A and B item is adopted as written; see RULINGS_UPDATE_2026-10-08.md for the text to append to ISAIAH_RULINGS.md.

Reviewer seat, 2026-10-08. Read: the complete file on `seat-act` (effa298, 32,873 bytes, entries
2026-09-24 → 2026-10-08 morning). Three parts: **A** rulings missing from the file; **B**
contradictions and stale lines, with the figure or ruling that decides each; **C** what checks out.
Corpus and rulings are Isaiah's: B proposes, Isaiah decides.

---

## A. Missing — Isaiah's rulings from 2026-10-07 and 2026-10-08 that are not in the file

Proposed entries, verbatim where he wrote them:

**2026-10-07**
1. **MINT and IMPORT, defined.** *"on minting (thats remixing existing atoms, or adding new recipes
   using the operator) the IMPORTS are meant to be like across games in this context so we dont have
   to worry about that. every atom has to have that metaprogrammng setup wheter we preload it from
   the 2700 or the agent creates it."*

**2026-10-08**

2. **NO GAME TESTING until the library is in and working.** *"until we get those atoms (which are
   the human priors/primitives) in the library and working in a metaprogramming way so that there
   are not 2700 functions, but still actionable, and that the agent can compose and create new
   functions on its own using the existing grammar it has, no testing should be done. Testing
   against games would be logically pointless ... so there is no debate on this. Check the tether
   figures to see why."* (Figures 6, 8, 13.) This pauses every "its own all-25" in the reviewer
   rulings of 2026-10-08.
3. **One library.** *"everything agent is preloaded that are atoms or recipes -> library"*. The
   "index" is not a second store; every index is derived.
4. **Grid-world meanings.** *"both of you are llms, can you not come up with decent explanations of
   what these atoms would represent in a 2d grid world?"* Written for every atom, as candidates.
5. **All 2,700 representable.** Every entry is representable, or its meaning is, by other atoms plus
   the operators and symbols from the figures. *"I need the codebase to be robust."*
6. **Duplicates removed.** *"the 256 duplicates can be removed"*: 139 true duplicates removed, logged
   and reversible; the rest were different concepts or role pairs.
7. **Roles, prepositions, orientation.** Atoms act as subject or verb by position (*"effect vs
   affect"*). Prepositions are role markers. Look-alikes carry orientation (*"temp(properties, cold,
   warm, hot - or increasing in heat, decreasing in heat ...)"*). *"make sure that all the other
   atoms get those distinctions"*, and generically for future atoms.
8. **The search index plan:** *"construct the search index plan i had initiated that used
   attributes and relations.md to act with the mutation observer to narrow the search space
   candidates because all atoms that are made or created would be tagged with attribute qualities
   that they can affect or that affect them."*
9. **Agent-made atoms and recipes.** *"the agent gets to name the atoms, but the composition is
   created in the metaprogramming via the agents grammar and the atoms + operators"*, and they fire
   like the preloaded ones.
10. **Commits.** The pre-commit hook was switched off by Isaiah (*"i believe this is why it resorted
    to doing this with worktrees, and having a large backlog"*). Fast commits are to keep the checks
    and drop the wait.
11. **Branches.** `core` and `arc-agent` are the originals; the rest are the seat's, to be
    straightened with the reviewer.
13. **Generalisation (2026-10-08):** the colour ruling above (B4), recorded as Isaiah's: colours change on every
    load; private boards may be rearranged, rotated or shrunk; nothing that stores a raw value carries.
12. **Both seats use the Tether as a self-consistent, cohesive ruleset** (paraphrase of his
    heartbeat instruction): a recursive barrier metatheorem, domain-agnostic, applying at every layer
    of a problem, used by every agent (the one being built and both seats) to avoid combinatorial
    explosion, i.e. brute force.

## B. Contradictions and stale lines — for Isaiah

| # | the line | the conflict | proposed |
|---|---|---|---|
| B1 | **2026-10-06 (6): "invented atoms skipped on load, counted"** | Narrower than first read: the code's old invented atoms were REPLAYED EFFECT TABLES, i.e. recordings (Figure 4). Today's inventions are conditions over readings | **Decision 6 STANDS for recordings.** An invention that passes `carry_check` (relations only) is a method and carries; one naming a raw value stays in its episode (METAPROGRAMMING_DESIGN §6). Isaiah to confirm |
| B2 | **2026-10-04: "Imports only after a real search failed, the change has recurred, and no existing atom already expresses it"** | Written when "import" meant bringing in a new atom. On 2026-10-07 Isaiah redefined IMPORT as across games | **Re-label** the 10-04 conditions as the trigger for **INVENTED** atoms (an abstention receipt: searched, recurred, nothing expresses it), which is how `invent_atom` is specified. The meaning is unchanged; only the word moves |
| B3 | **2026-10-04: "new knowledge is stored IN THE GRAMMAR, never a side system such as lookup tables"** | `library/index.json` is a set of lookup tables | **Consistent if read as Figure 6 reads it**: knowledge lives in library entries (atoms + operators: the grammar); the index is DERIVED, holds nothing of its own, and is regenerated from the entries. Asking Isaiah to confirm that reading |
| B4 — **RESOLVED by Isaiah, 2026-10-08:** *"the colors are changing everytime the game loads so anyting that stores that would be problematic. you might even assume objects are randomly arranged on the private OOD board or the entire rotated or shrank for instance all in service of showing that your generalizing"*. Colour joins the nominal set (identity/difference only, no arithmetic, never stored across episodes); no raw colour, position or size crosses an episode; axis-bound relations cross with the axis as a variable. | **The reviewer's 2026-10-08 nominal-set ruling: "COLOUR ... arithmetic stays, with its cyclic alphabet"** | The **corpus** (PERCEPTION_PIPELINE Layer 3; "ARC GAMEPLAY") models colour as **order of encounter within a spectrum band** (GB1, GB2), "never as stored value". The corpus outranks a reviewer ruling | **Retract my ruling's colour clause**: colour is a disposable label with a spectrum ordering. Arithmetic on the palette index is withdrawn pending Isaiah. `readings.json` should follow the corpus once he confirms. **This was my error** |
| B5 | **2026-10-05 authority order: rulings first, corpus second, reviewer third** | 2026-10-06 ("control relinquished to the figures") and 2026-10-07 ("the figures dictate logic and decisions") put the **figures above everything**; the seat-map field guide orders figures → derived docs → rulings → reviewer → seats | **Update the list**: (0) Figures 1–13 and the Operators and Symbols tables; (1) Isaiah's rulings; (2) the corpus; (3) the reviewer; (4) prior seats |
| B6 | **2026-09-28 "ARC games are STOPPED"**, 2026-09-29 lifting conditions, 2026-10-07 "real boards offline only" | Three states of one stop with no single current line | **State the current position once**: lifted 2026-10-07 for offline confirm-only runs over all 25, evenly; paused 2026-10-08 until the library is in (A2); the live gateway is untouched |
| B7 | **The reviewer's rulings of 2026-10-08** (arms H, F+G, C→DELTA_KEY, B, instruments, observer) each end "its own all-25" | Paused by A2. Several are now subsumed by the library plan (the observer's full vector → readings.json; types → the readings' type column; INSTRUMENTS → readings) | **Annotate each**: paused; folded into the library work where it overlaps; re-read under one pinned all-25 when testing resumes |
| B8 | **2026-09-30 "Commits require full green"** | The hook is off (A10) | **Add**: the gate is restored by `fast_check.py`. Pending Isaiah's ruling on whether a pass reused on byte-identical inputs counts as full green |
| B9 | **The seat map's loop sentence** | CORRECTED, after the seat's 12:02 report. seat-act's sentence ("THE FORMULA … the same loop under its other name") is ISAIAH'S OWN 2026-10-06 amendment (F461), not a seat edit. His staged copy of 2026-10-08 (4b476e6) carries the PRE-amendment sentence ("THE_LOOP_reference.md", a file that does not exist). The merge kept the amended sentence; his staged bytes stay in history | **Isaiah to say which wording stands.** If his staged wording, it is a one-line restore. My REPO_AUDIT called the amended line "a seat edit to a corpus file". That was wrong |
| B10 | **2026-10-05 timeline: complete and Kaggle-ready by 2026-10-12** | A2 pauses testing; the readiness items that need runs (solo timing, calibration) wait for it | **No change to the date**, which is Isaiah's. Record that readiness runs follow the library |

## C. Checked and consistent

- **The figures as one self-consistent set, recursively, for both seats** (10-06, 10-07): this whole
  task ran with figure censuses grepped against the SVG text. One misquote of Figure 12 was found and
  corrected.
- **Agency is paramount; we supply means, not meaning** (10-05): the grid meanings, roles and
  orientation are candidates the ground settles. The agent names its own atoms.
- **"+" is a placeholder; the ground settles the bond** (09-22) and **bond sufficiency is decided by
  the board** (09-28): junctions are `?` unless written, and orientation drafts are marked as drafts.
- **Nothing depends on game IDs** (10-01): the library holds no game identifiers.
- **Never judge progress on one game type** (10-07): kept for when testing resumes.
- **Store intents with their meaning; NSM-style grammar for intents** (09-28): `grammar.json` holds
  the NSM frames, primes and prepositions those intents are written in.
- **Click-only cause and effect; extend, do not duplicate** (10-01): CODEBASE_CHECK names the
  duplicates to join (four lighting paths, three perception vocabularies).

## Figure census
Figure 6 (*"What is recorded only grows. What is reachable is derived"*: B3); Figure 13 (*"The set
is closed. The arrangements are not. That gap is why import exists"*: A2, B2); Figure 10 (*"a
convention nothing can check is a constant the seat authored"*: B8). The corpus outranking a
reviewer ruling (B4) is the authority order, not a figure. Strained: none.
