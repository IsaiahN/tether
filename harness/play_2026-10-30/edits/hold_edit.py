p = "tether.py"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"


def rep(old, new):
    global s
    old, new = old.replace("\n", nl), new.replace("\n", nl)
    assert s.count(old) == 1, (old[:60], s.count(old))
    s = s.replace(old, new)


rep("        self._hyp_known = 0\n",
    "        self._hyp_known = 0\n"
    "        self._hyp_why: str | None = None  # 18:40 (iii): why a held hypothesis did not act\n"
    "        self._hyp_plat: list = []     # 18:40: the platform actions withheld while touched\n")
rep("                            phase=phase, by=by, stage=self.chain.seg.stage(),\n",
    "                            phase=phase, by=by, stage=self.chain.seg.stage(),\n"
    "                            **({} if self._hyp_why is None else {\"hyp_why\": self._hyp_why}),\n")
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
