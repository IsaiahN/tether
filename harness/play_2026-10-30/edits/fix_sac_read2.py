import sys
from pathlib import Path

sys.dont_write_bytecode = True
p = Path(sys.argv[1])
s = p.read_text(encoding="utf-8")
R = [
    ("import ast\nimport json\nimport os\nimport sys\nimport zlib\n",
     "import json\nimport os\nimport re\nimport sys\nimport zlib\n"),
    ('def lin_of(res):\n'
     '    """result.json writes "lineage" as the repr of the write\'s dict (game_one); read it back as data"""\n'
     '    v = res.get("lineage")\n'
     '    return ast.literal_eval(v) if isinstance(v, str) else (v or {})\n',
     'def lin_of(res):\n'
     '    """result.json writes "lineage" as a TRUNCATED repr of the write\'s dict (game_one), so only its leading\n'
     '    hash and parent are read, by pattern"""\n'
     '    v = res.get("lineage")\n'
     '    if isinstance(v, dict):\n'
     '        return v\n'
     '    v = str(v or "")\n'
     '    out = {}\n'
     '    for k in ("hash", "parent"):\n'
     '        m = re.search(r"\'" + k + r"\': \'([0-9a-f]{16})\'", v)\n'
     '        out[k] = m.group(1) if m else None\n'
     '    return out\n'),
]
for a, b in R:
    assert s.count(a) == 1, (a[:60], s.count(a))
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8", newline="\n")
print("ok")
