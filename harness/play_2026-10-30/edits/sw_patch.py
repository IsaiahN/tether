import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
old1 = '    seen = {c: {"present": None, "frame_break": 0} for c in first}\n'
new1 = '    seen = {c: {"present": None, "frame_break": 0, "next": None} for c in first}\n    nxt = {c + 1: c for c in first}\n'
old2 = '            if not m or int(m.group(1)) not in seen:\n                continue\n            c = int(m.group(1))\n'
new2 = ('            if not m:\n                continue\n            c = int(m.group(1))\n'
        '            if c in nxt and c not in seen and \'"event": "present"\' in ln and seen[nxt[c]]["next"] is None:\n'
        '                d = json.loads(ln)["detail"]\n'
        '                seen[nxt[c]]["next"] = {k: (len(v) if isinstance(v, list) else v)\n'
        '                                        for k, v in d.items() if k in ("was", "now", "came", "gone")}\n'
        '            if c not in seen:\n                continue\n')
old3 = "{p.get('came')} gone {p.get('gone')} orphaned {p.get('orphaned')} | {seen[int(x[3])]['frame_break']}\")\n"
new3 = ("{p.get('came')} gone {p.get('gone')} orphaned {p.get('orphaned')} | {seen[int(x[3])]['frame_break']}\"\n"
        "              f\" | next cycle present {seen[int(x[3])]['next']}\")\n")
for o, n in ((old1, new1), (old2, new2), (old3, new3)):
    assert s.count(o) == 1, o[:60]
    s = s.replace(o, n)
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched")
