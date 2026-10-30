"""r371: 4's goal_hypotheses fields named for what they count -- compile_reads, not_admitted. Applied with
r370's fix in the follow-up commit. argv: repo root. Every occurrence is replaced by a full-text pass
on the three files, each count asserted first."""
import re
import sys

sys.dont_write_bytecode = True
R = sys.argv[1].rstrip("/")


def sub(rel, pairs):
    p = f"{R}/{rel}"
    s = open(p, encoding="utf-8", newline="").read()
    for pat, rep, n in pairs:
        got = len(re.findall(pat, s))
        assert got == n, (rel, pat, got, n)
        s = re.sub(pat, rep, s)
    open(p, "w", encoding="utf-8", newline="").write(s)


sub("tether.py", [
 (r"detail\.update\(compiled=compiled\[0\], uncompiled=",
  "detail.update(compile_reads=compiled[0], not_admitted=", 1),
])
sub("conform/arms.py", [
 (r"\"compiled, uncompiled, phases and wall_s; open, ranked and refused cover \"",
  "\"compile_reads (compile-cache reads in the phases run), not_admitted \"\r\n"
  "                          \"(texts in a phase never run: no route-first, compile or filter), \"\r\n"
  "                          \"phases and wall_s; open, ranked and refused cover \"", 1),
])
sub("tests/test_plan_narrow.py", [
 (r"\"compiled\", \"uncompiled\"", "\"compile_reads\", \"not_admitted\"", 2),
 (r"d\.get\(\"uncompiled\"\)", "d.get(\"not_admitted\")", 2),
 (r"\{d\['compiled'\]\} compiled", "{d['compile_reads']} reads", 1),
 (r"\{d\['uncompiled'\]\} left uncompiled", "{d['not_admitted']} not admitted", 1),
 (r"d_on\[\"uncompiled\"\]", "d_on[\"not_admitted\"]", 1),
 (r"\{d_on\['uncompiled'\]\} uncompiled", "{d_on['not_admitted']} not admitted", 1),
 (r"texts left uncompiled", "texts not admitted", 2),
 (r"nothing left uncompiled", "nothing left unadmitted", 1),
 (r"nothing uncompiled", "nothing unadmitted", 1),
])
print("ok")
