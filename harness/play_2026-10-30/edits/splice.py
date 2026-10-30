import sys
p, blk = sys.argv[1], sys.argv[2]
s = open(p, encoding='utf-8', newline='').read()
a = s.index('def _held_in_store('); b = s.index('def _ch(cand: dict)')
nl = '\r\n' if '\r\n' in s else '\n'
new = open(blk, encoding='utf-8').read().replace('\r\n', '\n').replace('\n', nl)
s = s[:a] + new + nl + nl + s[b:]
open(p, 'w', encoding='utf-8', newline='').write(s); print('ok crlf', nl == '\r\n')
