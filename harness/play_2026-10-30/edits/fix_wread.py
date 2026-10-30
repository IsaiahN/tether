import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
old1 = '''def rows(p):'''
new1 = '''def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def rows(p):'''
old2 = '''        res = json.load(open(os.path.join(RUN, f"{g}_spy{s}", f"{g}.result.json"), encoding="utf-8"))'''
new2 = '''        res = load(os.path.join(RUN, f"{g}_spy{s}", f"{g}.result.json"))'''
old3 = '''    w = json.load(open(os.path.join(RUN, f"{g}_spy1", f"{g}.w.json"), encoding="utf-8"))'''
new3 = '''    w = load(os.path.join(RUN, f"{g}_spy1", f"{g}.w.json"))'''
old4 = '''        print(f"   -- BYTES at {r['when']}: commit {r['commit_mb_before_walk']} MB (after the walk "
              f"{r['commit_mb_after_walk']}), sized {r['sized_mb']} MB in {r['objects']:,} objects, walk {r['walk_s']} s")'''
new4 = '''        print(f"   -- BYTES at {r['when']}: commit {r['commit_mb_before_walk']} MB (after the walk "
              f"{r['commit_mb_after_walk']}), sized {r['sized_mb']} MB in {r['objects']:,} objects, "
              f"walk {r['walk_s']} s")'''
old5 = '''            if x["mb"] >= 0.05 or key == "end" and x["name"].startswith("ledger"):'''
new5 = '''            if x["mb"] >= 0.05 or (key == "end" and x["name"].startswith("ledger")):'''
for o, n in ((old1, new1), (old2, new2), (old3, new3), (old4, new4), (old5, new5)):
    assert s.count(o) == 1, o
    s = s.replace(o, n)
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("ok")
