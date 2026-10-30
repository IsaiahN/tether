import sys
sys.dont_write_bytecode = True
p = sys.argv[1]
s = open(p, encoding="utf-8", newline="").read()
R = [
    ('    assert "planted_before" in inv and "planted_now" not in inv, ("C3 inventions", inv)\n',
     '    assert sorted(inv) == ["planted_bad", "planted_before"], ("C3 inventions", inv)\n'),
    ('    assert len(ic) == 1 and ic[0]["reinvented"] == ["planted_before"] and not ic[0]["refused"], (\n'
     '        "C3: the carried invention (a real template) must re-invent", ic, r["plants"])\n',
     '    assert len(ic) == 1 and ic[0]["reinvented"] == ["planted_before"], (\n'
     '        "C3: the carried invention (a real template) must re-invent", ic, r["plants"])\n'
     '    bad = ic[0]["refused"]\n'
     '    assert [b["name"] for b in bad] == ["planted_bad"] and "names no reading" in bad[0]["why"], (\n'
     '        "C3-BAD: the malformed record must be refused WITH its why", ic)\n'),
    ('          f"invention_carried row {ic}")\n',
     '          f"invention_carried row {ic}")\n'
     '    print(f"  C3-BAD the malformed record (template \'{{o}}.{{r}} > 0\') refused and recorded: "\n'
     '          f"why {bad[0][\'why\']!r}")\n'),
]
for a, b in R:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
