import os

T = "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv"
p = os.path.join(T, "tether.py")
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
old = '''                for e_ in t2:
                    if self._kind_store is not None:
                        kn, lv = self._kind_store["t2"][e_]
                        last = (self._kind_last[e_][3] if e_ in self._kind_last
                                else lv[3] if lv[0] is not None else 0)
                    else:
                        kn = self._kind_known_n.get(e_, 1)
                        last = self._kind_last.get(e_, (0, 0, 0, 0))[3]
                    n_[e_[0]] += kn
                    l_[e_[0]] = max(l_.get(e_[0], 0), last)
'''.replace("\n", nl)
new = '''                for e_ in t2:
                    # its own name: "last" is the per-entry recency DICT that T1d reads below, and
                    # re-binding it to a number here raised there whenever T2 and T1d both held one
                    if self._kind_store is not None:
                        kn, lv = self._kind_store["t2"][e_]
                        seq_ = (self._kind_last[e_][3] if e_ in self._kind_last
                                else lv[3] if lv[0] is not None else 0)
                    else:
                        kn = self._kind_known_n.get(e_, 1)
                        seq_ = self._kind_last.get(e_, (0, 0, 0, 0))[3]
                    n_[e_[0]] += kn
                    l_[e_[0]] = max(l_.get(e_[0], 0), seq_)
'''.replace("\n", nl)
assert s.count(old) == 1, s.count(old)
s = s.replace(old, new)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
