A = "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/conform/arms.py"
s = open(A, encoding="utf-8", newline="").read()
eol = "\r\n" if "\r\n" in s else "\n"
s = s.replace(eol, "\n")
assert "TETHER_STORE_KEY_MEMO" not in s
old = '    "TETHER_FIT_DEDUP": "(2a), ONE DEFINITION ONCE PER FIT'
assert s.count(old) == 1
new = ('    "TETHER_STORE_KEY_MEMO": "W1 (S2V; the reviewer 2026-10-21 15:38): lineage_store._merge_kinds "\n'
       '                             "keeps each kind value\'s JSON string for one merge, keyed on its "\n'
       '                             "repr (1, True and 1.0 encode apart); other types encoded fresh. "\n'
       '                             "OFF: json.dumps per row (23a9077). default ON",\n'
       '    "TETHER_STORE_KEY_MEMO_CHECK": "W1\'s check run: every reuse also encodes fresh and compares; the "\n'
       '                                   "fresh string is used. A measurement switch. default OFF",\n'
       '    "TETHER_LOAD_KEY_MEMO": "W2 (S2V; the reviewer 2026-10-21 15:38): the store load decodes each "\n'
       '                            "kind sym id once per load, reusing the tuple when hashable. OFF: "\n'
       '                            "json.loads per row (23a9077). default ON",\n'
       '    "TETHER_LOAD_KEY_MEMO_CHECK": "W2\'s check run: every reuse also decodes fresh and compares; the "\n'
       '                                  "fresh tuple is used. A measurement switch. default OFF",\n'
       + old)
s = s.replace(old, new)
open(A, "w", encoding="utf-8", newline="").write(s.replace("\n", eol))
print("ok")
