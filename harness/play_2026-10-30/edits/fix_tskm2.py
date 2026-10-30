p = "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/test_store_key_memo.py"
s = open(p, encoding="utf-8").read()
reps = [
 ("import hashlib, json, sys\n", "import hashlib, json, random, sys\n"),
 ("    for _g in range(games):\n        tether, env, ag = tc.agent(lineage_dir=d)\n",
  "    for _g in range(games):\n"
  "        # a handle's suffix is random.choices when the agent seed is off (test_consolidate's\n"
  "        # agent); the same seed per game makes the ON and OFF writes comparable\n"
  "        random.seed(1000 + _g)\n"
  "        tether, env, ag = tc.agent(lineage_dir=d)\n"),
 ("      dump of every table (iterdump; SQLite's page layout is not promised). PRECONDITION: the\n"
  "      ON writes reused (hit > 0).\n",
  "      dump of every table (iterdump; SQLite's page layout is not promised). Python's random is\n"
  "      seeded per game (a handle's suffix draws from it), and a CONTROL writes OFF twice and\n"
  "      must be identical first. PRECONDITION: the ON writes reused (hit > 0).\n"),
 ("    a, b, c = (os.path.join(tmp, x) for x in (\"on\", \"off\", \"one\"))\n"
  "    for x in (a, b, c):\n",
  "    a, b, c, b2 = (os.path.join(tmp, x) for x in (\"on\", \"off\", \"one\", \"off2\"))\n"
  "    for x in (a, b, c, b2):\n"),
 ("    off = _run(\"write\", b, \"2\", env_extra={\"TETHER_STORE_KEY_MEMO\": \"0\"})\n",
  "    off = _run(\"write\", b, \"2\", env_extra={\"TETHER_STORE_KEY_MEMO\": \"0\"})\n"
  "    _run(\"write\", b2, \"2\", env_extra={\"TETHER_STORE_KEY_MEMO\": \"0\"})\n"
  "    assert _files(b) == _files(b2), \"CONTROL: two OFF writes differ, so (2) cannot read W1\"\n"),
]
for o, n in reps:
    assert s.count(o) == 1, o[:60]
    s = s.replace(o, n)
open(p, "w", encoding="utf-8").write(s)
print("ok")
