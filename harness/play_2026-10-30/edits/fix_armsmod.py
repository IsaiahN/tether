W = "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/"


def edit(path, pairs):
    s = open(W + path, encoding="utf-8", newline="").read()
    eol = "\r\n" if "\r\n" in s else "\n"
    s = s.replace(eol, "\n")
    for o, n in pairs:
        assert s.count(o) == 1, (path, o[:60])
        s = s.replace(o, n)
    open(W + path, "w", encoding="utf-8", newline="").write(s.replace("\n", eol))


edit("instruments.py", [
    ("# TETHER_HOLES_REPOINT (step 6).\n"
     "ARM_MODULES = (\"tether\", \"arc_percept\", \"arc_world\", \"arc_atoms\", \"compile_term\", \"gridworld\",\n"
     "               \"interface\", \"lineage\", \"gamma\", \"instruments\", \"sensors_heavy\", \"relations\",\n"
     "               \"ledger\")\n",
     "# TETHER_HOLES_REPOINT (step 6). lineage_store from 2026-10-21, for TETHER_STORE_KEY_MEMO (W1).\n"
     "ARM_MODULES = (\"tether\", \"arc_percept\", \"arc_world\", \"arc_atoms\", \"compile_term\", \"gridworld\",\n"
     "               \"interface\", \"lineage\", \"gamma\", \"instruments\", \"sensors_heavy\", \"relations\",\n"
     "               \"ledger\", \"lineage_store\")\n"),
])
edit("conform/arms.py", [
    ("    \"TETHER_STORE_KEY_MEMO_CHECK\": \"W1's check run: every reuse also encodes fresh and compares; the \"\n"
     "                                   \"fresh string is used. A measurement switch. default OFF\",\n",
     "    \"TETHER_STORE_KEY_MEMO_CHECK\": \"W1's check run: every reuse also encodes fresh and \"\n"
     "                                   \"compares; the fresh string is used. A measurement \"\n"
     "                                   \"switch. default OFF\",\n"),
    ("    \"TETHER_LOAD_KEY_MEMO_CHECK\": \"W2's check run: every reuse also decodes fresh and compares; the \"\n"
     "                                  \"fresh tuple is used. A measurement switch. default OFF\",\n",
     "    \"TETHER_LOAD_KEY_MEMO_CHECK\": \"W2's check run: every reuse also decodes fresh and \"\n"
     "                                  \"compares; the fresh tuple is used. A measurement \"\n"
     "                                  \"switch. default OFF\",\n"),
])
print("ok")
