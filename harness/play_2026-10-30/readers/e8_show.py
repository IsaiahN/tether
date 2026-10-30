"""Print the first row of each named event from e8_*.json for one ledger tag, detail truncated. argv: json tag events..."""
import json
import sys

d = json.load(open(sys.argv[1], encoding="utf-8"))
tag = next(t for t in d if sys.argv[2] in t)
for e in sys.argv[3:]:
    r = d[tag]["first"].get(e)
    if r is None:
        print(f"== {e}: none")
        continue
    s = json.dumps(r, ensure_ascii=True)
    print(f"== {e} ({d[tag]['counts'].get(e)}): {s[:900]}")
