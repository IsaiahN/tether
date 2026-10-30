"""Read-only: the keys of conform/arms.py's VALUES dict (by ast, the file is not imported), and how many say MAGIC."""
import ast, sys
sys.dont_write_bytecode = True
t = ast.parse(open(sys.argv[1], encoding="utf-8").read())
for n in t.body:
    if isinstance(n, ast.Assign) and any(getattr(x, "id", None) == "VALUES" for x in n.targets):
        keys = [k.value for k in n.value.keys]
        vals = [ast.literal_eval(v) if isinstance(v, ast.Constant) else ast.unparse(v) for v in n.value.values]
        magic = [k for k, v in zip(keys, vals) if "MAGIC" in str(v)]
        print("VALUES keys", len(keys), "| MAGIC", len(magic), magic)
