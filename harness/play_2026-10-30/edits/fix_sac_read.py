import sys
from pathlib import Path

sys.dont_write_bytecode = True
p = Path(sys.argv[1])
s = p.read_text(encoding="utf-8")
R = [
    ("import json\nimport os\nimport sys\nimport zlib\n",
     "import ast\nimport json\nimport os\nimport sys\nimport zlib\n"),
    ('def rows(p):\n',
     'def lin_of(res):\n'
     '    """result.json writes "lineage" as the repr of the write\'s dict (game_one); read it back as data"""\n'
     '    v = res.get("lineage")\n'
     '    return ast.literal_eval(v) if isinstance(v, str) else (v or {})\n\n\n'
     'def rows(p):\n'),
    ("lineage written {res.get('lineage', {}).get('hash')}", "lineage written {lin_of(res).get('hash')}"),
    ('point_head = (s3o_res.get("lineage") or {}).get("parent")', 'point_head = lin_of(s3o_res).get("parent")'),
    ('wrote = (box[b]["res"].get("lineage") or {}).get("hash")', 'wrote = lin_of(box[b]["res"]).get("hash")'),
]
for a, b in R:
    assert s.count(a) == 1, (a[:60], s.count(a))
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8", newline="\n")
print("ok")
