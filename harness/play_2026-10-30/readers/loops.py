"""Every for/while loop (with its line and header) inside the named Agent methods, top-level loops of the method
marked with depth. argv: tether.py name..."""
import ast
import sys

src = open(sys.argv[1], encoding="utf-8").read()
lines = src.splitlines()
tree = ast.parse(src)
agent = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Agent")
meths = {f.name: f for f in agent.body if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef))}
for name in sys.argv[2:]:
    f = meths.get(name)
    if f is None:
        print("NO", name)
        continue
    print(f"== {name} ({f.lineno}-{f.end_lineno})")

    def walk(node, depth):
        for c in ast.iter_child_nodes(node):
            if isinstance(c, (ast.For, ast.While, ast.AsyncFor)):
                print(f"   {'  ' * depth}{c.lineno}: {lines[c.lineno - 1].strip()[:100]}")
                walk(c, depth + 1)
            elif not isinstance(c, (ast.FunctionDef, ast.Lambda)):
                walk(c, depth)
    walk(f, 0)
