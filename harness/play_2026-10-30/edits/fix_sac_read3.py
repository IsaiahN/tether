import sys
from pathlib import Path

sys.dont_write_bytecode = True
p = Path(sys.argv[1])
s = p.read_text(encoding="utf-8")
OLD_HEAD = '''s3o = rows(S3O_LED)
s3o_res = json.load(open(S3O_LED.replace(".jsonl", ".result.json"), encoding="utf-8"))
point_head = lin_of(s3o_res).get("parent")
print(f"    the S3O point's head (S3O sp80's generation's parent): {point_head}; a equal: "
      f"{la.get('lineage_parent') == point_head}; b equal: {lb.get('lineage_parent') == point_head}")
'''
NEW_HEAD = '''s3o = rows(S3O_LED)


def point_tip(lin):
    """the point's head: of the generations its manifest names, the one no other names as parent (read from the
    copy, which the chain verified equal to the point)"""
    gens = {f[4:20]: gen(os.path.join(lin, f)) for f in known if f.startswith("gen_")}
    parents = {g.get("parent") for g in gens.values()}
    tips = [h for h in gens if h not in parents]
    return tips[0] if len(tips) == 1 else tips


pt_a, pt_b = point_tip(box["a"]["lin"]), point_tip(box["b"]["lin"])
point_head = pt_a
print(f"    the point's head (the manifest's one generation no other names as parent): a's copy {pt_a}, b's copy "
      f"{pt_b}; the load read it: a {la.get('lineage_parent') == point_head}, b {lb.get('lineage_parent') == point_head}")
'''
assert s.count(OLD_HEAD) == 1
s = s.replace(OLD_HEAD, NEW_HEAD)
OLD_DOC = ("      load report) EQUAL on both copies, timing keys named and masked; and both equal to the S3O point's own load\n"
           "      record: the head = S3O's sp80 generation's parent; the @run arms row's generation, seed, seed_source and the\n")
NEW_DOC = ("      load report) EQUAL on both copies, timing keys named and masked; and both equal to the S3O point's own load\n"
           "      record: the head = the point's tip (the manifest's one generation no other names as parent); the @run\n"
           "      arms row's generation, seed, seed_source and the\n")
assert s.count(OLD_DOC) == 1
s = s.replace(OLD_DOC, NEW_DOC)
p.write_text(s, encoding="utf-8", newline="\n")
print("ok")
