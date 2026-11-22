WATSON 59 — nested-method composition was always planned; habitats must be real-world (2026-11-22)

ISAIAH'S TWO DIRECTIVES:
(1) "nested method composition was always part of the plan — check the history and docs for
confirmation." (2) "Whatever habitats you build, make them based on real-world problems or
scenarios that animals and humans alike must face. Use WATSON to see how to make your desired
test goal implicit via the use cases that already exist in nature and the real world."

I checked the history first. My earlier framing ("kernel work, off-limits, species change") was
WRONG and is corrected here.

## DIRECTIVE 1 — CONFIRMED: nested methods were always in the plan
Evidence from the repo (not a new idea):
- `docs/03-DESIGN/08-METAPROGRAMMING_DESIGN.md` (2026-10-08), §0: lists `Term` ("atom chain,
  `operand`, `operand_term`, `guard`") as "the compiled form of every grounded candidate"; shows
  nested trees (`both< abs_delta . sign . holds >( sign . holds . negate )`); cites Fig 12
  "A settled molecule becomes an atom for whatever composes over it."
- Commit `2f794f8e` "THE MINT DEEPENS ITS TREES": a node's branch fed by "a one-atom term over
  another of the slot's binds" — nested operand composition, priced by the mint's own bargain.
- F470 (INDEX): "THE OPERAND TREE CROSSES AS A TYPED SCHEMA... plan item 2's first piece."
- F325 (INDEX): "A TERM SETTLES UNDER ONE IDENTITY AND IS PROMOTED UNDER ANOTHER... the reusable
  chunk is a different computation from the one the ground paid for" — the promotion defect Fix 1
  repaired (WATSON 54).

So nested-method composition is a DESIGNED capability whose promotion path broke. Fig 13 :114 "The
set is closed. The arrangements are not" and Fig 12 :103-106 make it a requirement, not an
invention. My "kernel work off-limits" framing conflated "repair a designed path" with "amend the
kernel" — Fig 4's rule (M2 in the derivation log) distinguishes them. The repair is legitimate.

## THE PRECISE GAP (write site, verified)
`_branches()` (tether.py:15822-15837) builds operand-arm terms from `self.gamma.atoms` only —
one atom, never a settled unit/method. `_deepen_trees` (28045) grows a branch by one atom over
"another of the slot's binds," not by reusing a settled method. So chains get the Fig 12 shortcut
(`units()` promotes settled chains), but the OPERAND ARM does not: a settled method cannot become
the branch of a deeper tree. Fix 1 made the method survive promotion; the missing piece is letting
the mint's branch vocabulary offer settled units as operands. This is a bounded change in the
mint's library-derived branch source, behind an arm, priced by the existing bargain — not a
kernel rewrite. The real cost/benefit: offer settled methods as branches; the SAME `_cannot_pay`
and `pays` decide whether any such tree is bought. Nothing is admitted by decree.

## DIRECTIVE 2 — habitats from real-world problems (WATSON)

QUESTION (effect terms): what real scenario makes "a learned method becomes an operand of a
deeper behavior" the thing that decides success, with the goal implicit and no encoded answer?

DOMAIN CENSUS:
- R: arity = (learned subassembly, target composite); symmetry = a subassembly can be reused as
  a unit or its parts; scale = one bout of action.
- domains: child/adult human (actors: hands+cups / currency: moves / anchor: nested stack); great
  ape (actors: stick+probe / currency: termites gathered / anchor: termite nest); agent (actors:
  terms+actions / currency: bits+actions / anchor: board).
- union: "a constructed unit moved as a component" spans all three; order: the physical cases
  witness the abstraction the agent must form.

TETHER (primary, verbatim, from source SVGs):
- Fig 12 :5 "A set of ingredients is not one. The bond is the rest of the information."
- Fig 12 :103-106 "A settled molecule becomes an atom for whatever composes over it."
- Fig 11 :39-40 "capability is a property of agent-and-habitat... an improvement that does not
  change contact changes nothing." → the habitat must make reuse-of-a-unit load-bearing.
- Fig 9 :60 filters are not verdicts → the goal must be implicit in the task, never published as
  "reuse the method."

WORLD (secondary, sources read):
- Nesting-cup / subassembly (Greenfield 1972; Hayashi & Takeshita 2009; Lam et al. 2022,
  "Hierarchical object combination and tool use in the great apes and human children"): children
  and adult chimpanzees both reach the "subassembly" stage — a previously built pair of cups is
  MOVED AS A UNIT into another cup. PREDICTS: the capability is not "more actions" but "treat a
  built unit as an operand." Corroborates Fig 12 :103. It is a real developmental problem with an
  implicit goal (nest all cups, fewest moves) — exactly the habitat shape Isaiah asked for.
- Chimpanzee termite fishing (Byrne, Sanz & Morgan 2013): subroutines (manufacture brush-tip,
  puncture nest, fish) are reused across tasks and OMITTED when already available. PREDICTS: reuse
  of a learned routine as a component, and conditional omission — a second real-world habitat.
- Hierarchical action control (Dezfouli & Balleine, Frontiers 2019): "habits... combine or chunk
  with other actions... form the elements of chunked action sequences." PREDICTS: a learned chunk
  becomes an element of a higher sequence. Corroborates the figure's unit=atom reading.
- Percussive tool use (Nature Comm Biol 2026): chimp and human PTU sequences are hierarchical;
  "one chunk... achieved by embedding one chunk (i.e., strike, eat) within a longer chunk."
  PREDICTS: nested chunks are measurable in natural behavior; corroborates.

VERDICT (from the figures, triangulated Fig 12 + Fig 11 + Fig 13, corroborated by 4 independent
real-world sources): nested-method composition is a planned capability (confirmed in repo history),
and the legitimate way to exercise it is a habitat modeled on the nesting-cup / subassembly or
termite-fishing scenario — a real problem humans and apes face, with the goal implicit (fewest
moves to a nested stack / gather food), where reusing a built unit as a component is what pays.
The agent-side change is bounded: offer settled methods as operand-arm branches, priced by the
existing bargain; no atom, threshold, or check changed.

COST IF WRONG: a branch vocabulary that offers useless units — paid for by the bargain, so the
cost is search budget, not correctness; OFF is byte-identical. UNDOABLE: yes, behind an arm with an
OFF-identity row. REVERSED BY: a panel where no settled method ever passes `_cannot_pay` as a
branch (then the wall is price, not representation).

HABITAT DESIGN (next, per directive 2): a "nesting" world where the agent must assemble objects
into a stack by REUSING a pair it already built as a unit — the goal is "fewest moves to the
completed nest," implicit in the board, never published as "reuse the method." Modeled on the
nesting-cup subassembly task. No ARC game, no colour key, no encoded answer.

FIGURE CENSUS: Fig 1 · Fig 3 dependency order · Fig 4 methods-up/bindings-down · Fig 9 filters-not-
verdicts · Fig 11 habitat/enumerate/contact · Fig 12 bond/arrangement/settled-molecule-becomes-atom ·
Fig 13 closed-set-open-arrangements. Strained: none.

Sources: [Greenfield 1972 / Hayashi & Takeshita 2009 / Lam et al. 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9463204/);
[Byrne, Sanz & Morgan 2013](https://congo-apes.org/wp-content/uploads/2021/07/Byrne-Sanz-Morgan-2013-Chimpanzees-plan-their-tool-use-1_compressed-1.pdf);
[Dezfouli & Balleine 2019](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.02735/full);
[Percussive tool-use hierarchy 2026](https://www.nature.com/articles/s42003-026-09633-8).
