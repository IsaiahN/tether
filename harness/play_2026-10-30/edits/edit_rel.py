import sys
sys.dont_write_bytecode = True
p = "c:/Users/Admin/Documents/GitHub/tether/tether.py"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
pairs = [
 ("        owed: dict = {}\n        if b2 is not None and self._dw_owed and _OWED_REJUDGE:\n",
  "        owed: dict = {}\n        released: set = set()        # 1d: judged on this frame; only a later one re-raises\n"
  "        if b2 is not None and self._dw_owed and _OWED_REJUDGE:\n"),
 ("                if why is not None:\n                    self._owed_release(d, ct, why)\n                    b2[\"dropped\"] += 1\n                    continue\n",
  "                if why is not None:\n                    self._owed_release(d, ct, why)\n                    released.add(d)\n                    b2[\"dropped\"] += 1\n                    continue\n"),
 ("                if d in self.wants or before.get(d) is None or after.get(d) in (None, before[d]):\n",
  "                if (d in self.wants or d in released or before.get(d) is None\n"
  "                        or after.get(d) in (None, before[d])):\n"),
]
for a, b in pairs:
    a, b = a.replace("\n", nl), b.replace("\n", nl)
    assert s.count(a) == 1, (a[:70], s.count(a))
    s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
