import sys
sys.dont_write_bytecode = True
p = "c:/Users/Admin/Documents/GitHub/tether/tether.py"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
pairs = [
 ("                    # newer evidence supersedes the stored one; a transition already asked is\n"
  "                    # not new evidence (7f's tried set), so it never replaces an unasked one\n"
  "                    if t_new != ct[1] and t_new not in self._dw_tried.get(d, ()):\n",
  "                    if self._supersedes(d, ct, t_new):   # newer evidence replaces the stored one\n"),
 ("    def _owed_release(self, d: str, ct: tuple, why: str) -> None:\n",
  "    def _supersedes(self, d: str, ct: tuple, t_new: tuple) -> bool:\n"
  "        \"\"\"1d: the slot's newer transition replaces an owed ask's stored one -- unless it was\n"
  "        already asked, which is not new evidence (7f's tried set): carrying it would let B2's\n"
  "        deferral reopen a settled question.\"\"\"\n"
  "        return t_new != ct[1] and t_new not in self._dw_tried.get(d, ())\n\n"
  "    def _owed_release(self, d: str, ct: tuple, why: str) -> None:\n"),
]
for a, b in pairs:
    a, b = a.replace("\n", nl), b.replace("\n", nl)
    assert s.count(a) == 1, (a[:70], s.count(a))
    s = s.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
