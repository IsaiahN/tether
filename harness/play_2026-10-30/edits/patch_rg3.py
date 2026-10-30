"""Item 6, R-g3 ruled in with its guard kept (the reviewer 2026-10-22 19:12 a, b, c)."""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
p = Path(sys.argv[1]) / "tests" / "test_lineage_carry.py"
s = p.read_text(encoding="utf-8")
crlf = "\r\n" in s
s = s.replace("\r\n", "\n")
R = [
    ("import json\nimport os\n", "import hashlib\nimport json\nimport os\n"),
    ('''    again = lineage.write(d, ag3, "default")
    assert "refused" in again, ("R-g3 overwrite", again)
    assert lineage.head(d)[0] == w3["hash"], "R-g3 one chain"
    print(f"  R-g3: {w2['hash']} -> parent {w1['hash']}; unchanged {w3['hash']} holds 0 term "
          f"rows; rewrite refused", flush=True)
''',
     '''    # a second write by the same agent EXTENDS its first under TETHER_LINEAGE_BOUNDARY
    # (lineage.py, F2): a child of w3, measured, never assumed (the reviewer 19:12 a, b)
    again = lineage.write(d, ag3, "default")
    assert "written" in again and again["parent"] == w3["hash"], ("R-g3 child of w3", again, w3)
    assert lineage.head(d)[0] == again["hash"], "R-g3 one chain"
    # NEVER OVERWRITE, direct (19:12 c): a write whose bytes are w3's aims at w3's own name through
    # the "xb" open; it is refused, naming w3's file, and w3's bytes are unchanged
    p3 = Path(d) / w3["written"]
    before = hashlib.sha256(p3.read_bytes()).hexdigest()
    raw3, real_dumps, used = lineage_store.file_bytes(p3), lineage._dumps, []

    def once(x):
        if used:
            return real_dumps(x)
        used.append(1)
        return raw3
    lineage._dumps = once
    try:
        same = lineage.write(d, ag3, "default")
    finally:
        lineage._dumps = real_dumps
    assert used and w3["written"] in str(same.get("refused")), ("R-g3 never overwrite", same)
    assert hashlib.sha256(p3.read_bytes()).hexdigest() == before, "R-g3 w3's bytes changed"
    print(f"  R-g3: {w2['hash']} -> parent {w1['hash']}; unchanged {w3['hash']} holds 0 term "
          f"rows; a second write is its child {again['hash']} (parent {again['parent']}); a write "
          f"aimed at {w3['written']} refused ({same['refused']}), its bytes unchanged", flush=True)
'''),
]
for a, b in R:
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)
if crlf:
    s = s.replace("\n", "\r\n")
p.write_bytes(s.encode("utf-8"))
print("ok")
