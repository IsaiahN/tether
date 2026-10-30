import sys
sys.dont_write_bytecode = True
sys.path.insert(0, ".")
import compile_term
import tether
tether._library()
T = sys.modules["library_runtime"].TEMPLATES
rd = compile_term.readings()
print("x" in rd, rd.get("x"))
for lab, t in T.get((rd.get("x") or {}).get("type"), ()):
    print(lab, "|", t)
