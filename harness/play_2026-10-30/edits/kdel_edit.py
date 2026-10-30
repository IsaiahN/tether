"""The Kaggle deletion's line edits (4b step b), each range asserted by its first and last line
before it is cut, so a shifted file refuses rather than cuts the wrong lines. argv: TREE"""
import sys

T = sys.argv[1]


def lines(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return fh.read().split("\n")


def write(p, ls):
    with open(p, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(ls))


# tests/test_entry.py: 1-indexed inclusive ranges, with the text their first lines must start with
p = f"{T}/tests/test_entry.py"
L = lines(p)
cuts = [(340, 342, "def fake_make("), (345, 362, "def _carries_in_order("),
        (365, 390, "def check_the_runner_carries_in_order_per_worker("),
        (393, 437, "def check_serve_opens_one_card_and_always_closes_it("),
        (440, 467, "def check_the_notebook_runs_our_runner_in_place_of_swarm("),
        (470, 479, "def check_the_bundle_holds_no_test_file("),
        (493, 509, "def check_the_bundle_carries_every_module_the_harness_file_imports("),
        (512, 541, "_ISOLATED = \"\"\""), (544, 555, "def _bundle_reaches_its_library("),
        (558, 568, "def check_the_bundle_reaches_its_library_in_isolation("),
        (572, 664, "def gateway_one_card_takes_every_worker_process(")]
for a, b, head in cuts:
    assert L[a - 1].startswith(head), (a, L[a - 1][:60])
    assert L[b].strip() == "" or L[b].startswith(("def ", "_", "if __name__")), (b, L[b][:60])
assert L[481].startswith("def check_the_census_is_never_an_input("), L[481][:60]
keep = set(range(len(L)))
for a, b, _ in cuts:
    keep -= set(range(a - 1, b))
    # the blank lines that separated the cut block from the next one
    j = b
    while j < len(L) and L[j].strip() == "" and j in keep:
        keep.discard(j)
        j += 1
L2 = [x for i, x in enumerate(L) if i in keep]
txt = "\n".join(L2)
nl = "\r\n" if "\r\n" in txt else "\n"
old_main = ('    # `--gateway` runs the server-backed wiring check ALONE: ~2 min, past the per-commit seat\'s\n'
            '    # ruled 180s stage cap, so it is run explicitly rather than on every commit.\n'
            '    gw = "--gateway" in sys.argv\n').replace("\n", nl)
assert txt.count(old_main) == 1, "the --gateway comment block moved"
txt = txt.replace(old_main, "")
old_sel = ('    checks = [v for k, v in sorted(globals().items())\n'
           '              if (k.startswith("gateway_") if gw else k.startswith("check_"))]\n'
           ).replace("\n", nl)
assert txt.count(old_sel) == 1, "the collector line moved"
txt = txt.replace(old_sel, '    checks = [v for k, v in sorted(globals().items()) if k.startswith("check_")]'
                  + nl)
# keep the file's own spacing: at most two blank lines between top-level blocks
while nl * 4 in txt:
    txt = txt.replace(nl * 4, nl * 3)
open(p, "w", encoding="utf-8", newline="").write(txt)
print("test_entry: cut", sum(b - a + 1 for a, b, _ in cuts), "lines in", len(cuts), "ranges")

# conform/lint.py: the comment and the three kaggle_agent COLLECTORS rows
p = f"{T}/conform/lint.py"
txt = open(p, encoding="utf-8", newline="").read()
old = ('    # the ARC harness (ARC-AGI-3-Agents) collects the Agent subclass the notebook registers by\n'
       '    # name and calls its two abstract methods; nothing in the package may import the harness\n'
       '    # (14a, F457), so no in-package reference can exist. One module, three exact names.\n'
       '    ("kaggle_agent", "MyAgent"),\n'
       '    ("kaggle_agent", "is_done"),\n'
       '    ("kaggle_agent", "choose_action"),\n')
nl = "\r\n" if "\r\n" in txt else "\n"
old = old.replace("\n", nl)
assert txt.count(old) == 1, "lint rows moved"
open(p, "w", encoding="utf-8", newline="").write(txt.replace(old, ""))
print("lint: 6 lines cut")

# conform/fast_check.py: the clause naming kaggle_bundle
p = f"{T}/conform/fast_check.py"
txt = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in txt else "\n"
old = ("# step 2, 2026-10-11 -- the glob is kept, as a reuse input it costs nothing); kaggle_bundle reads"
       + nl + "# docs/example.")
assert txt.count(old) == 1, "fast_check comment moved"
open(p, "w", encoding="utf-8", newline="").write(
    txt.replace(old, "# step 2, 2026-10-11 -- the glob is kept, as a reuse input it costs nothing)."))
print("fast_check: comment clause cut")
