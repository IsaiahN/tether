"""Item 6, R-g2's "was" check and the handle note (the reviewer 2026-10-22 20:14)."""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
p = Path(sys.argv[1]) / "tests" / "test_lineage_carry.py"
s = p.read_text(encoding="utf-8")
crlf = "\r\n" in s
s = s.replace("\r\n", "\n")
R = [
    ('''The OFF identity is a lane in RL-0's form, not this fixture.
''',
     '''The OFF identity is a lane in RL-0's form, not this fixture.

DETERMINISTIC IN VERDICTS AND CONTENTS, NOT IN BYTES (the reviewer 2026-10-22 20:14): both seeds are
pinned, but with TETHER_AGENT_SEED off a term's handle takes the process's unseeded random suffix
(gamma.Term.handle), so handles, and with them the generation hashes, vary run to run (E8 Q24).
'''),
    ('''    blob = ag.gamma.blob()
    assert ag.gamma.evidence and ag._dormant, ("fixture: no evidence or no dormant record",
''',
     '''    blob = ag.gamma.blob()
    names = [r["name"] for r in ag.gamma.blob(with_names=True)["terms"]]
    assert ag.gamma.evidence and ag._dormant, ("fixture: no evidence or no dormant record",
'''),
    ('''    folded = [{k: v for k, v in r.items() if k != "born"} for r in f["terms"]]
    assert folded == blob["terms"], "R-g2 terms"
''',
     '''    folded = [{k: v for k, v in r.items() if k not in ("born", "was")} for r in f["terms"]]
    assert folded == blob["terms"], "R-g2 terms"
    # "was" is R7i's field, which the generation ADDS (lineage.write, TETHER_REPLAY_UNIT): each
    # row's must be that term's own name, checked rather than ignored (the reviewer 20:14 b)
    assert [r.get("was") for r in f["terms"]] == names, ("R-g2 was", names)
'''),
]
for a, b in R:
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)
if crlf:
    s = s.replace("\n", "\r\n")
p.write_bytes(s.encode("utf-8"))
print("ok")
