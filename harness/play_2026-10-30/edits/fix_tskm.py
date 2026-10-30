p = "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/test_store_key_memo.py"
s = open(p, encoding="utf-8").read()
a = s.index('"""W1 / W2'); b = s.index('from __future__')
doc = '''"""W1 / W2, THE STORE'S KEY MEMOS (TETHER_STORE_KEY_MEMO, TETHER_LOAD_KEY_MEMO; the reviewer
2026-10-21 15:38). The fake ARC game; every probe its own process, hash and agent seeds pinned.

  (1) W1's PLANT, the type hazard: 1 == True == 1.0 hash alike and json writes [1], [true],
      [1.0]. One merge's memo gives each of [1], [True], [1.0], (1,), [1] the string json.dumps
      gives it fresh; a memo keyed on the value (tuple(v)) gives [True] the string of [1] --
      shown to FAIL.
  (2) W1, BYTE-IDENTICAL: two fake games written into a fresh lineage (the second merges onto
      the first), memo ON and OFF: every file's bytes equal, and memory.db equal by an ordered
      dump of every table (iterdump; SQLite's page layout is not promised). PRECONDITION: the
      ON writes reused (hit > 0).
  (3) W2: that lineage loaded ON, OFF and ON+CHECK: the carried stores equal (_kind_known_dk,
      _kdk_last, the offered/known stores, the store's t2 and pairs); CHECK 0 disagree.
      PRECONDITION: hit > 0.
  (4) W2's memo is per load: a second load in one process (a one-game lineage first, then the
      two-game one) equals the two-game lineage loaded alone.

    python test_store_key_memo.py
"""
'''
s = s[:a] + doc + s[b:]
reps = [
 ('    return hashlib.sha256(json.dumps(out, sort_keys=True).encode()).hexdigest(), {k: len(v) for k, v in out.items()}\n',
  '    sha = hashlib.sha256(json.dumps(out, sort_keys=True).encode()).hexdigest()\n'
  '    return sha, {k: len(v) for k, v in out.items()}\n'),
 ('    print(json.dumps({"sha": res[0], "sizes": res[1], "n": lineage.LOAD_KEY_MEMO_N, "on": lineage._LOAD_KEY_MEMO}))\n',
  '    print(json.dumps({"sha": res[0], "sizes": res[1], "n": lineage.LOAD_KEY_MEMO_N,\n'
  '                      "on": lineage._LOAD_KEY_MEMO}))\n'),
 ('    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0", **(env_extra or {}))\n',
  '    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0", TETHER_AGENT_SEED="0",\n'
  '               **(env_extra or {}))\n'),
 ('    print(f"(1) the type plant: the memo gives {got[:3]} (each its fresh string); a value-keyed memo "\n'
  '          f"gives {wrong[:3]}")\n',
  '    print(f"(1) the type plant: the memo gives {got[:3]} (each its fresh string); a "\n'
  '          f"value-keyed memo gives {wrong[:3]}")\n'),
 ('    assert fa == fb, [k for k in set(fa) | set(fb) if fa.get(k) != fb.get(k)][:5]                  # (2)\n',
  '    assert fa == fb, [k for k in set(fa) | set(fb) if fa.get(k) != fb.get(k)][:5]        # (2)\n'),
 ('    print(f"(2) two games written ON and OFF: {len(fa) - 1} files byte-identical and memory.db\'s dump "\n'
  '          f"identical; the ON writes reused {on[\'n\'][\'hit\']} encodings ({on[\'n\'][\'bypass\']} bypassed)")\n',
  '    print(f"(2) two games written ON and OFF: {len(fa) - 1} files byte-identical and "\n'
  '          f"memory.db\'s dump identical; the ON writes reused {on[\'n\'][\'hit\']} encodings "\n'
  '          f"({on[\'n\'][\'bypass\']} bypassed)")\n'),
 ('    l_chk = _run("load", a, env_extra={"TETHER_LOAD_KEY_MEMO": "1", "TETHER_LOAD_KEY_MEMO_CHECK": "1"})\n',
  '    l_chk = _run("load", a, env_extra={"TETHER_LOAD_KEY_MEMO": "1",\n'
  '                                       "TETHER_LOAD_KEY_MEMO_CHECK": "1"})\n'),
 ('    assert l_on["sha"] == l_off["sha"] == l_chk["sha"], (l_on, l_off, l_chk)                          # (3)\n',
  '    assert l_on["sha"] == l_off["sha"] == l_chk["sha"], (l_on, l_off, l_chk)             # (3)\n'),
 ('    assert two["sha"] == l_on["sha"], (two, l_on)                                                     # (4)\n',
  '    assert two["sha"] == l_on["sha"], (two, l_on)                                        # (4)\n'),
]
for o, n in reps:
    assert s.count(o) == 1, o[:60]
    s = s.replace(o, n)
open(p, "w", encoding="utf-8").write(s)
print("ok")
