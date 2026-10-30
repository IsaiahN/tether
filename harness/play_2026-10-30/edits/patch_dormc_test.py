"""(c)'s checks in test_lineage_carry R-g2 and the stale stub's fix (the reviewer 2026-10-22 20:57)."""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
p = Path(sys.argv[1]) / "tests" / "test_lineage_carry.py"
s = p.read_text(encoding="utf-8")
crlf = "\r\n" in s
s = s.replace("\r\n", "\n")
R = [
    ('''    assert f["dormant"] == ag._dormant, "R-g2 dormant"
''',
     '''    # (c), the reviewer 20:57: the boundary item is written WHOLE, each Term in its term-row form
    gen_rr = json.loads(lineage_store.file_bytes(Path(rr) / f"gen_{_h}.json"))
    assert gen_rr["dormant_refused"] == [], ("R-g2 dormant refused", gen_rr["dormant_refused"])
    assert f["dormant"] == [lineage.term_form(x) for x in ag._dormant], "R-g2 dormant"
    live = {(i, k): t for i, x in enumerate(ag._dormant)
            for k, t in x["stores"]["want_terms"].items()}
    assert live, "fixture: no Term in the dormant record"
    assert all(f["dormant"][i]["stores"]["want_terms"][k]["__term__"] == t.name
               and f["dormant"][i]["stores"]["want_terms"][k]["atoms"] == [a.name for a in t.atoms]
               for (i, k), t in live.items()), "R-g2 dormant: the record is not the live Term's"
    # MUST-FAIL: OFF, the write's own encoder refuses the item, named (the check above would fire)
    arm = lineage._DORMANT_TERM_FORM
    lineage._DORMANT_TERM_FORM = False
    try:
        off, off_refused = lineage.dormant_items(ag._dormant)
    finally:
        lineage._DORMANT_TERM_FORM = arm
    assert not off and off_refused and off_refused[0]["type"] == "Term", ("R-g2 MF", off_refused)
    print(f"  R-g2 dormant: {len(ag._dormant)} boundary item(s) written whole, {len(live)} Term(s) "
          f"in their term-row form; OFF the write refuses {off_refused}", flush=True)
'''),
    ('''    def counted(_self, game):
''',
     '''    def counted(_self, game, seed=None):    # term.handle takes the draw seed (HOLD_SEED)
'''),
]
for a, b in R:
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)
if crlf:
    s = s.replace("\n", "\r\n")
p.write_bytes(s.encode("utf-8"))
print("ok")
