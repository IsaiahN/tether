"""Item 6's two ruled fixes: test_7lm L2 reads the load report (19:04 1); test_index_carry R-d3's
reference compiles with the subject as tether._held_index does (19:04 2, the probe: 0 of 8976)."""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
root = Path(sys.argv[1])


def edit(rel, pairs):
    p = root / rel
    s = p.read_text(encoding="utf-8")
    crlf = "\r\n" in s
    s = s.replace("\r\n", "\n")
    for a, b in pairs:
        assert s.count(a) == 1, (rel, a[:80], s.count(a))
        s = s.replace(a, b)
    if crlf:
        s = s.replace("\n", "\r\n")
    p.write_bytes(s.encode("utf-8"))
    print("ok", rel)


edit("tests/test_7lm.py", [
    ('print("OUT " + json.dumps({"kinds_known": len(ag._kind_known)}))\n',
     'print("OUT " + json.dumps({"kinds_known": rest[-1]["lineage"]["kinds_known"]}))\n'),
])
edit("tests/test_index_carry.py", [
    ('''    def comp(cond):
        return compile_term.compile_candidate({"condition": cond}, atoms)
    for key, role in pairs:
        fresh = [(c, comp(c["if"]), comp(c["then"])) if role == "CAUSE"
                 else (c, None if "quantifier" in c else comp(c["condition"]), None)
''',
     '''    def comp(cond, subject):     # as _held_index compiles: the subject under the abduction arm
        return compile_term.compile_candidate(
            {"condition": cond}, atoms, subject=subject if tether._LIBRARY_ABDUCE else None)
    for key, role in pairs:
        fresh = [(c, comp(c["if"], tether.PH_O), comp(c["then"], tether.PH_X)) if role == "CAUSE"
                 else (c, None if "quantifier" in c else comp(c["condition"], tether.PH_O), None)
'''),
])
