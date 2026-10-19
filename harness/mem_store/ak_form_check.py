"""S4's ak_ FORM CHECK (the reviewer 2026-10-19 08:26 item 3). READ ONLY. The new-form ak_ file a run wrote under
TETHER_MEMORY_STORE (form 2: the questions asked since the last save, each with n = times asked) against the S3-form
file of the same save (ff_on: every question the instance answered, no n). Pass: form == 2, every n >= 1, the
(key, role, o, x, slot) set EQUAL to the S3 file's, N/N. Printed: the n distribution, sum n, and the whole rows.
argv: new_ak_file s3_ak_file"""
import collections
import json
import sys

NEW, OLD = sys.argv[1:3]
with open(NEW, encoding="utf-8") as fh:
    new = json.load(fh)
with open(OLD, encoding="utf-8") as fh:
    old = json.load(fh)
rn = [(e["key"], e["role"], e["o"], e["x"], e["slot"]) for e in new["entries"]]
ro = {(e["key"], e["role"], e["o"], e["x"], e["slot"]) for e in old["entries"]}
ns = [e.get("n") for e in new["entries"]]
print("FORM", new.get("form"), f"rows {len(rn)}", f"distinct {len(set(rn))}", f"s3 rows {len(ro)}", sep="\t")
print("N", f"all >= 1: {all(isinstance(n, int) and n >= 1 for n in ns)}", f"sum {sum(n or 0 for n in ns)}",
      f"distribution {sorted(collections.Counter(ns).items())[:30]}", sep="\t")
print("WHOLES", f"new {sum(r[4] is None for r in rn)}", f"s3 {sum(r[4] is None for r in ro)}", sep="\t")
print("SET", f"equal {set(rn) == ro}", f"only new {len(set(rn) - ro)}", f"only s3 {len(ro - set(rn))}", sep="\t")
for r in sorted(set(rn) ^ ro, key=repr)[:10]:
    print("DIFF", json.dumps(r), "new" if r in set(rn) else "s3", sep="\t")
