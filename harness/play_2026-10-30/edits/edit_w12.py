W = "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/"


def edit(path, pairs):
    s = open(W + path, encoding="utf-8", newline="").read()
    eol = "\r\n" if "\r\n" in s else "\n"
    s = s.replace(eol, "\n")
    for old, new in pairs:
        assert s.count(old) == 1, (path, s.count(old), old[:70])
        s = s.replace(old, new)
    open(W + path, "w", encoding="utf-8", newline="").write(s.replace("\n", eol))


# ---- W1: lineage_store._merge_kinds' key encodings, memoized per merge on repr ----
ls_old_merge_head = ("def _merge_kinds(con: sqlite3.Connection, s: \"Syms\", g: dict) -> None:\n"
                     "    def kkey(e):\n"
                     "        return (s(e[0]), s(e[1]), s(_j(e[2])), s(_j(e[3])))\n")
ls_new_merge_head = ("def _merge_kinds(con: sqlite3.Connection, s: \"Syms\", g: dict) -> None:\n"
                     "    _j = _key_memo()\n"
                     "\n"
                     "    def kkey(e):\n"
                     "        return (s(e[0]), s(e[1]), s(_j(e[2])), s(_j(e[3])))\n")
edit("lineage_store.py", [
    ("import codecs\nimport hashlib\n", "import codecs\nimport hashlib\n"),
    ("from pathlib import Path\nfrom typing import Any\n",
     "from pathlib import Path\nfrom typing import Any\n\nimport armflag\n"),
    ("def _j(x: Any) -> str:\n    return json.dumps(x, sort_keys=True)\n",
     "def _j(x: Any) -> str:\n    return json.dumps(x, sort_keys=True)\n"
     "\n\n"
     "# W1 (S2V; the reviewer 2026-10-21 15:38): _merge_kinds encoded the same few kind values with\n"
     "# json.dumps once per row (607,920 key builds at one sp80 boundary). One merge keeps each value's\n"
     "# string, keyed on repr(value): 1, True and 1.0 compare and hash alike and encode apart, and their\n"
     "# reprs differ; a value of another top-level type is encoded fresh. OFF: _j per row (23a9077)\n"
     "_KEY_MEMO = armflag.arm(\"TETHER_STORE_KEY_MEMO\", default=True)\n"
     "# W1's check run: every reuse also encodes fresh and compares; the fresh string is used. OFF: none\n"
     "_KEY_MEMO_CHECK = armflag.arm(\"TETHER_STORE_KEY_MEMO_CHECK\")\n"
     "KEY_MEMO_N: dict = {\"hit\": 0, \"bypass\": 0, \"agree\": 0, \"disagree\": 0}\n"
     "_MEMO_TYPES = (list, tuple, str, int, float, bool)\n"
     "\n\n"
     "def _key_memo():\n"
     "    \"\"\"_j for one merge, remembering each value's string (W1).\"\"\"\n"
     "    if not _KEY_MEMO:\n"
     "        return _j\n"
     "    memo: dict = {}\n"
     "\n"
     "    def j(x: Any) -> str:\n"
     "        if type(x) not in _MEMO_TYPES:\n"
     "            KEY_MEMO_N[\"bypass\"] += 1\n"
     "            return _j(x)\n"
     "        k = repr(x)\n"
     "        out = memo.get(k)\n"
     "        if out is None:\n"
     "            out = memo[k] = _j(x)\n"
     "            return out\n"
     "        KEY_MEMO_N[\"hit\"] += 1\n"
     "        if _KEY_MEMO_CHECK:\n"
     "            fresh = _j(x)\n"
     "            KEY_MEMO_N[\"agree\" if fresh == out else \"disagree\"] += 1\n"
     "            out = fresh\n"
     "        return out\n"
     "    return j\n"),
    (ls_old_merge_head, ls_new_merge_head),
])

# ---- W2: lineage._load_from_store's key(), decoded once per sym id per load ----
edit("lineage.py", [
    ("_MEMORY_STORE = armflag.arm(\"TETHER_MEMORY_STORE\", default=True)\n",
     "_MEMORY_STORE = armflag.arm(\"TETHER_MEMORY_STORE\", default=True)\n"
     "# W2 (S2V; the reviewer 2026-10-21 15:38): the store load decoded a kind field's JSON once per row\n"
     "# (885,038 json.loads at one sp80 load). One load decodes each sym id once and reuses the tuple when\n"
     "# it is hashable (immutable all the way down); otherwise it decodes fresh. OFF: per row (23a9077)\n"
     "_LOAD_KEY_MEMO = armflag.arm(\"TETHER_LOAD_KEY_MEMO\", default=True)\n"
     "# W2's check run: every reuse also decodes fresh and compares; the fresh tuple is used. OFF: none\n"
     "_LOAD_KEY_MEMO_CHECK = armflag.arm(\"TETHER_LOAD_KEY_MEMO_CHECK\")\n"
     "LOAD_KEY_MEMO_N: dict = {\"hit\": 0, \"unhashable\": 0, \"agree\": 0, \"disagree\": 0}\n"),
    ("        def key(*xs):\n"
     "            return tuple(tuple(json.loads(sym[x])) if i in xs[0] else sym[x]\n"
     "                         for i, x in enumerate(xs[1:]))\n",
     "        km: dict = {}\n"
     "\n"
     "        def dec(x):\n"
     "            if not _LOAD_KEY_MEMO:\n"
     "                return tuple(json.loads(sym[x]))\n"
     "            v = km.get(x)\n"
     "            if v is None:\n"
     "                v = tuple(json.loads(sym[x]))\n"
     "                try:\n"
     "                    hash(v)\n"
     "                    km[x] = v\n"
     "                except TypeError:\n"
     "                    LOAD_KEY_MEMO_N[\"unhashable\"] += 1\n"
     "                return v\n"
     "            LOAD_KEY_MEMO_N[\"hit\"] += 1\n"
     "            if _LOAD_KEY_MEMO_CHECK:\n"
     "                fresh = tuple(json.loads(sym[x]))\n"
     "                LOAD_KEY_MEMO_N[\"agree\" if fresh == v and repr(fresh) == repr(v)\n"
     "                                else \"disagree\"] += 1\n"
     "                v = fresh\n"
     "            return v\n"
     "\n"
     "        def key(*xs):\n"
     "            return tuple(dec(x) if i in xs[0] else sym[x] for i, x in enumerate(xs[1:]))\n"),
])
print("ok")
