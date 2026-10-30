import sys

sys.dont_write_bytecode = True
p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
anchor = "- **(B), IN-GAME RECOVERY AFTER AN AGENT FAULT"
i = s.index(anchor)
j = s.index("\n", i) + 1
LINE = (
    "- **ITEM 6, THE TESTS READ A LINEAGE FILE AS THE LINEAGE DOES, AND (c) THE DORMANT ITEM WRITTEN "
    "WHOLE (the design post 2026-10-22 15:13; the reviewer 18:37, 19:04, 19:12, 19:39, 19:47, 20:14, "
    "20:57).** THE LINEAGE CHANGE, (c) (TETHER_DORMANT_TERM_FORM, default ON): a boundary item "
    "(tether._hold_lineage copies every _LINEAGE_STORES store in instance form) holds live Terms in its "
    "want_terms copy (_want_terms is dict[str, Term]); lineage.enc has no form for a Term, so one Term "
    "made the write refuse the WHOLE boundary record (wants, reach_tested, undone, trace, every store), "
    "named in dormant_refused: a CARRY DEFECT (20:57). Now lineage.write encodes dormant items through "
    "lineage.dormant_items, which writes each Term as its term-row record (lineage.term_form: "
    "__term__ name, atoms, guard, guard_ref, operand, operand_term), a record nothing rebuilds a Term "
    "from (lineage.load reads no dormant record back); the live record and the in-life restart carry "
    "are untouched. No dormant store is keyed by a Term (read per store; measured: dormant_refused [] "
    "on the fixture). The real lineage (19 generations at the S3O point, sha-checked copies) had 0 "
    "dormant items and 0 refused, with a denominator of 0: no real game reached a retarget. "
    "Post-freeze: refusal at store granularity for any other unencodable type. THE TESTS: "
    "tests/test_7lm.py:89, tests/test_lineage_carry.py:65 and tests/test_index_carry.py:103 read a "
    "zlib lineage file as text; each decodes through lineage_store.file_bytes. Past the decode, each "
    "reached assertions never exercised, all stale expectations, measured where they bore on a ruling: "
    "test_7lm L2 reads the load report's kinds_known (the store load keeps _kind_known empty by "
    "design); test_index_carry R-d3's reference compiles with the subject, as _held_index does (the "
    "probe: the carried compile equals it on 8976 of 8976 pairs, against 2827 from the stale "
    "reference; the 18:20 compile-cache premise stands on it); test_lineage_carry: R-g3 asserts the "
    "measured parent == w3 and head == the child, and keeps never-overwrite DIRECTLY (a write of w3's "
    "bytes is refused by the \"xb\" open, w3's file hash unchanged); R-g1 PLANTS one real 2-atom chain "
    "before game 1's write and requires it to cross as a composition (the carry's wiring, never that "
    "game 1 composes, Fig 11 :70); R-g2 strips R7i's \"was\" and checks it is each term's own name; "
    "R-g2 dormant checks (c) ON (dormant_refused [], the fold equals term_form of the record, the "
    "record's name and atoms equal the live Term's) and its must-fail OFF (the write refuses the item, "
    "type Term); the identity section's handle stub takes the draw seed. test_lineage_carry's --on "
    "child pins TETHER_AGENT_SEED=0 and PYTHONHASHSEED=0 (MOVED FORWARD from the post-freeze list for "
    "this one test: R-g1's fixture rode the birth seed); it is deterministic in verdicts and contents, "
    "NOT in bytes: with the seed arm off a handle takes the process's unseeded random suffix "
    "(gamma.Term.handle), so handles and generation hashes vary (E8 Q24, answered; the seeded handle "
    "post-freeze). test_lineage_boundary stays FLAKY. test_index_carry's CONVERSE check SKIPS (the "
    "gridworld signature holds no \"below\"): NOT COVERED.\n")
assert "ITEM 6, THE TESTS READ A LINEAGE FILE AS THE LINEAGE DOES" not in s
nl = "\r\n" if "\r\n" in s[:2000] else "\n"
s = s[:j] + LINE.replace("\n", nl) + s[j:]
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
