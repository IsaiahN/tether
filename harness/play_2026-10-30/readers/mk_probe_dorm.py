import sys
sys.dont_write_bytecode = True
src = open(sys.argv[1], encoding="utf-8").read()
OLD_ANCHOR = "OLD = '    assert folded == blob[\"terms\"], \"R-g2 terms\"\n'"
assert src.count(OLD_ANCHOR) == 1
src = src.replace(OLD_ANCHOR, "OLD = '    assert f[\"dormant\"] == ag._dormant, \"R-g2 dormant\"\n'")
a0 = src.index("NEW = (")
a1 = src.index("assert src.count(OLD) == 1")
NEW = '''NEW = (
    '    import json as _j\n'
    '    _fa, _ga = f["dormant"], ag._dormant\n'
    '    _rt = [lineage.dec(lineage.enc(x)) for x in _ga]\n'
    '    _i = next((i for i, (a, b) in enumerate(zip(_fa, _ga)) if a != b), None)\n'
    '    print("OUT " + _j.dumps({"n_fold": len(_fa), "n_agent": len(_ga),\n'
    '        "fold_equals_enc_dec_of_agent": _fa == _rt, "first_diff": _i,\n'
    '        "fold_i": repr(_fa[_i])[:700] if _i is not None else None,\n'
    '        "agent_i": repr(_ga[_i])[:700] if _i is not None else None,\n'
    '        "types_fold": sorted({type(x).__name__ for x in _fa}),\n'
    '        "types_agent": sorted({type(x).__name__ for x in _ga})}, default=str), flush=True)\n'
    '    raise SystemExit(0)\n')
'''
src = src[:a0] + NEW + src[a1:]
src = src.replace("named in the 20:00 post", "named in the 20:28 post; the dormant record")
open(sys.argv[2], "w", encoding="utf-8", newline="\n").write(src)
print("ok")
