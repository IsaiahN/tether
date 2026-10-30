"""Item 6, R-g1's planted composition (the reviewer 2026-10-22 19:47)."""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
p = Path(sys.argv[1]) / "tests" / "test_lineage_carry.py"
s = p.read_text(encoding="utf-8")
crlf = "\r\n" in s
s = s.replace("\r\n", "\n")
R = [
    ('''        as IMPORTED naming game 1's generation; a second process given the chain starts the same.
''',
     '''        as IMPORTED naming game 1's generation; a second process given the chain starts the same.
        THE PLANT (the reviewer 2026-10-22 19:47): one real 2-atom chain accepted into game 1's
        Gamma before its write must cross as a COMPOSITION. It tests the CARRY's wiring (written,
        read back by a fresh agent, kept a composition), never that game 1 composes (Fig 11 :70)
'''),
    ('''    for _ in range(N):
        ag1.step()
    ag1.end_run("cap")
    w1 = lineage.write(d, ag1, "default")
''',
     '''    for _ in range(N):
        ag1.step()
    plant = next((t for t in ag1.gamma.enumerate_closure("val", "val", 2, 4000, {})
                  if len(t.atoms) == 2 and t.name not in ag1.gamma.library), None)
    assert plant is not None, "fixture: no new 2-atom chain to plant"
    ag1.gamma.accept(plant, seq=len(ag1.led), residual=f"o1.x@{ag1.cycle}")
    ag1.end_run("cap")
    w1 = lineage.write(d, ag1, "default")
'''),
    ('''    assert composed, ("fixture: nothing crossed as a composition", composed, unbound)
''',
     '''    assert composed, ("fixture: nothing crossed as a composition", composed, unbound)
    tp = _held(ag2).get(_key(plant))
    cp = ag2.gamma.carried.get(tp.name, {}) if tp is not None else {}
    assert tp is not None and tp.origin == gamma.IMPORTED and "unbound" not in cp, (
        "R-g1 the planted chain did not cross as a composition", plant.name, cp)
    assert cp.get("parent") == w1["hash"], ("R-g1 the plant's parent", cp, w1["hash"])
    print(f"  R-g1 plant: {plant.name} crossed as a composition, IMPORTED, parent "
          f"{cp['parent']} (w1 {w1['hash']})", flush=True)
'''),
]
for a, b in R:
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)
if crlf:
    s = s.replace("\n", "\r\n")
p.write_bytes(s.encode("utf-8"))
print("ok")
