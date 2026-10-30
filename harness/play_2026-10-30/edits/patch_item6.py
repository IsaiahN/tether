"""Item 6: the three tests read a lineage file as the lineage does (lineage_store.file_bytes)."""
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
    ("import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)\n",
     "import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)\n"
     "import lineage_store  # item 6: a lineage file read as the lineage reads it\n"),
    ('    gens = [json.loads(Path(d, f).read_text(encoding="utf-8"))\n',
     '    gens = [json.loads(lineage_store.file_bytes(Path(d, f)))\n'),
])
edit("tests/test_lineage_carry.py", [
    ("import arc_holdout  # noqa: E402\n",
     "import arc_holdout  # noqa: E402\n"
     "import lineage_store  # noqa: E402  item 6: a lineage file read as the lineage reads it\n"),
    ('    return json.loads((Path(d) / w["written"]).read_text(encoding="utf-8"))\n',
     '    return json.loads(lineage_store.file_bytes(Path(d) / w["written"]))\n'),
])
edit("tests/test_index_carry.py", [
    ("import compile_term  # noqa: E402\n",
     "import compile_term  # noqa: E402\n"
     "import lineage_store  # noqa: E402  item 6: a lineage file read as the lineage reads it\n"),
    ('        for e in json.loads(f.read_bytes())["entries"]:\n',
     '        for e in json.loads(lineage_store.file_bytes(f))["entries"]:\n'),
])
