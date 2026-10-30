"""Q9(a): module-level UPPERCASE assignments in tether.py whose value contains a numeric literal (or a numeric
default string in os.environ.get), with the comment tag MAGIC / VALUE / convention on the 6 lines above, if any.
argv: file"""
import ast
import re
import sys

src = open(sys.argv[1], encoding="utf-8").read()
lines = src.splitlines()
tree = ast.parse(src)
for n in tree.body:
    if isinstance(n, ast.Assign) and all(isinstance(t, ast.Name) and t.id.isupper() for t in n.targets):
        nums = [c.value for c in ast.walk(n.value) if isinstance(c, ast.Constant)
                and (isinstance(c.value, (int, float)) and not isinstance(c.value, bool)
                     or isinstance(c.value, str) and re.fullmatch(r"-?[0-9][0-9_.]*", c.value))]
        if nums:
            above = " ".join(lines[max(0, n.lineno - 7):n.lineno - 1])
            tag = [t for t in ("MAGIC", "VALUE", "convention", "DECLARED", "derived", "Isaiah") if t in above]
            print(f"{n.lineno:6d} {n.targets[0].id:28s} {str(nums)[:40]:40s} {tag}")
