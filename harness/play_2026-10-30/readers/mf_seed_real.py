import json, sys
sys.path.insert(0, sys.argv[1] + "/conform")
from identity_mod_rows import compare
a = [json.loads(x) for x in open(sys.argv[2], encoding="utf-8") if x.strip()]
b = [json.loads(x) for x in open(sys.argv[3], encoding="utf-8") if x.strip()]
n = 0
for r in b:
    if r.get("slot") == "@run" and r.get("event") == "seed":
        r["detail"]["seed"] = "0000000000000000"; n += 1
bad = compare(a, b, set())
print(f"MF real: @run seed rows altered {n}; compare -> {'DIFFERENT' if bad else 'IDENTICAL'}: {bad[:3]}")
sys.exit(0 if bad and n else 1)
